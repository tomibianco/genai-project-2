import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from agents import function_tool


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

client = OpenAI()
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("genaiproject2")

def get_embedding(text):
    """ Función para generar el embedding de un texto."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    embed = response.data[0].embedding
    return embed
    
@function_tool
def rag_docs(message: str) -> str:
    """Complementa la consulta con información de la BBDD de la empresa"""
    try:
        message_embedding = get_embedding(message)
        rag_result = index.query(
            vector=message_embedding,
            top_k=3,
            include_metadata=True
        )
        context_info = []
        for match in rag_result["matches"]:
            file_name = match["metadata"].get("file", "Desconocido")
            similarity = match["score"]
            chunk_text = match["metadata"].get("text", "Texto no disponible")
            context_info.append(f"--- Fragmento de {file_name} (Relevancia: {similarity:.2f}) ---\n{chunk_text}\n")
        if not context_info:
            return "No se encontró información relevante en la base de datos."
        return "Información encontrada en la base de datos:\n\n" + "\n".join(context_info)
    except Exception as e:
        return f"Error al obtener retrieval de la BBDD vectorizada: {str(e)}"