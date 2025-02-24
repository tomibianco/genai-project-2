from langchain.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
import pinecone
import os


PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

pc = Pinecone(api_key="PINECONE_API_KEY")

index_name = "genai_prject_2"

pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

embeddings = OpenAIEmbeddings(openai_api_key="OPENAI_API_KEY")

# Vectorización de documentos
document_text = "Colocar ruta de archivos"
vector = embeddings.embed_query(document_text)

# Creación de conexión al índice
index = pinecone.Index(index_name)

# Subir el vector al índice de Pinecone
index.upsert([(f"doc1", vector)])