import os
from io import BytesIO
from dotenv import load_dotenv
import pandas as pd
import fitz
from docx import Document
import boto3
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
import pinecone


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)

embed = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

s3 = boto3.client('s3')

# Función para descargar archivos desde S3
def download_from_s3(bucket_name, key):
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return BytesIO(response['Body'].read())

# Función para cargar y procesar archivos XLSX
def load_xlsx(file_path):
    df = pd.read_excel(download_from_s3(S3_BUCKET_NAME, file_path))
    return df.to_string()

# Función para cargar y procesar archivos PDF
def load_pdf(file_path):
    doc = fitz.open(stream=download_from_s3(S3_BUCKET_NAME, file_path), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Función para cargar y procesar archivos DOC
def load_doc(file_path):
    doc = Document(download_from_s3(S3_BUCKET_NAME, file_path))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Listas de archivos en S3
xlsx_files = [f"xlsx/{file['Key']}" for file in s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="xlsx/")['Contents']]
pdf_files = [f"pdf/{file['Key']}" for file in s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="pdf/")['Contents']]
doc_files = [f"doc/{file['Key']}" for file in s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="doc/")['Contents']]

# Cargar y combinar documentos
combined_doc = ""
for file_path in xlsx_files:
    combined_doc += load_xlsx(file_path) + "\n"
for file_path in pdf_files:
    combined_doc += load_pdf(file_path) + "\n"
for file_path in doc_files:
    combined_doc += load_doc(file_path) + "\n"

# Ajustar tamaño del chunk y overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(combined_doc)

index_name = "genaiproject2"

# Verificar si el índice ya existe antes de crearlo
if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Conexión al índice
index = pinecone.Index(index_name)

# Vectorizar y subir documentos al índice
for i, doc in enumerate(documents):
    vector = embed.embed_query(doc)
    index.upsert([(f"doc{i+1}", vector)])