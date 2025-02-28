import os
import re
# from docx import Document
from dotenv import load_dotenv
import pandas as pd
from pinecone import Pinecone
import PyPDF2
from langchain_community.embeddings import OpenAIEmbeddings


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
FOLDER_PATH = os.getenv("FOLDER_PATH")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("genaiproject2")

embed = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)


def extract_text_pdf(file_path):
    """Extrae texto de un archivo PDF."""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text

def extract_text_excel(file_path):
    """Extrae texto de un archivo Excel convirtiéndolo en string."""
    df = pd.read_excel(file_path)
    return df.to_string()

def extract_text_csv(file_path):
    """Extrae texto de un archivo CSV convirtiéndolo en string."""
    df = pd.read_csv(file_path)
    return df.to_string()

def extract_text_word(file_path):
    """Extrae texto de un documento Word."""
#     doc = Document(file_path)  # Changed from docx.Document to Document
#     text = " ".join([para.text for para in doc.paragraphs])
    return text

def extract_text(file_path):
    """Detecta el tipo de archivo y extrae el texto correspondiente."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_pdf(file_path)
    elif ext in [".xls", ".xlsx"]:
        return extract_text_excel(file_path)
    elif ext == ".csv":
        return extract_text_csv(file_path)
    elif ext in [".doc", ".docx"]:
        return extract_text_word(file_path)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {ext}")

def split_text(text, chunk_size):
    """ Divide el texto en fragmentos de tamaño 'chunk_size' palabras."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def get_embedding(text):
    """ Función para generar el embedding de un texto usando el modelo "text-embedding-3-small."""
    embedding = embed.embed_query(text)
    return embedding

def sanitize_filename(filename):
    """Sanitiza el nombre del archivo para usar como ID en Pinecone."""
    sanitized = re.sub(r'[^a-z0-9-]', '-', filename.lower())
    sanitized = re.sub(r'-+', '-', sanitized)
    return sanitized.strip('-')

def process_file(file_path):
    """
    Procesa un archivo completo:
    - Extrae el texto.
    - Lo segmenta en chunks.
    - Genera embeddings para cada chunk.
    - Sube los vectores a Pinecone junto con metadatos.
    """
    print(f"Procesando: {file_path}")
    text = extract_text(file_path)
    chunks = split_text(text, chunk_size=500)
    vectors = []
    base_filename = sanitize_filename(os.path.basename(file_path))
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        vector_id = f"{base_filename}-{i}"
        metadata = {
            "file": os.path.basename(file_path),
            "chunk": i
        }
        vectors.append((vector_id, embedding, metadata))
    index.upsert(vectors)
    print(f"Archivo {os.path.basename(file_path)} procesado y subido a Pinecone.")


def main():    
    """Recorremos todos los archivos en el directorio."""
    for file in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, file)
        try:
            process_file(file_path)
        except Exception as e:
            print(f"Error procesando {file}: {str(e)}")


if __name__ == '__main__':
    main()