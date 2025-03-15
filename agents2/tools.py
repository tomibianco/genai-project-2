import os

from dotenv import load_dotenv



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("genaiproject2")

embed = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)


@tool("Calculadora Científica")
def scientific_calculator(expression: str) -> str:
    """ Evalúa una expresión matemática usando SymPy. Soporta operaciones científicas avanzadas. """
    try:
        result = sp.sympify(expression)
        return str(result)
    except Exception as e:
        return f"Error en el cálculo: {str(e)}"
    
@tool("RAG de Base de Datos")
def rag_docs(message: str) -> str:
    """ Herramienta de acceso a BBDD e información vectorizada de la empresa. """
    try:
        message_embedding = embed.embed_query(message)
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
