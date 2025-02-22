from langchain.tools import Tool
import requests

def search_wikipedia(query: str) -> str:
    """Busca un término en Wikipedia y devuelve un resumen."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("extract", "No se encontró información.")
    return "Error al obtener datos de Wikipedia."

wikipedia_tool = Tool(
    name="WikipediaSearch",
    func=search_wikipedia,
    description="Busca información en Wikipedia sobre un tema."
)