import os
import sympy as sp
from crewai.tools import tool
from langchain_community.embeddings import OpenAIEmbeddings
from pinecone import Pinecone


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("genaiproject2")

embed = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

def get_embedding(text):
    """ Función para generar el embedding de un texto usando el modelo "text-embedding-3-small."""
    embedding = embed.embed_query(text)
    return embedding

@tool("Calculadora Científica")
def scientific_calculator(expression: str) -> str:
    """
    Evalúa una expresión matemática usando SymPy. Soporta operaciones científicas avanzadas.
    """
    try:
        result = sp.sympify(expression)
        return str(result)
    except Exception as e:
        return f"Error en el cálculo: {str(e)}"
    
@tool("RAG de Base de Datos")
def rag_docs(message: str) -> str:
    """
    Herramienta de acceso a BBDD e información vectorizada de la empresa.
    """
    try:
        message_embedding = get_embedding(message)
        response = index.query(vector=message_embedding, include_metadata=True)
        return response
    except Exception as e:
        return f"Error al obtener retrieval de la BBDD vectorizada: {str(e)}"
