import sympy as sp
from crewai.tools import tool

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