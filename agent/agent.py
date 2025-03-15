import asyncio
from agents import Agent, Runner, ModelSettings
from dotenv import load_dotenv
from langfuse_log import get_prompt
import logging
from memory import MemoryManager
from tools import rag_docs
import os


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
memory = MemoryManager()


def initialize_agent() -> Agent:
    """Definición de agente vendedor"""
    try:
        agent = Agent(
            name="seller",
            instructions=get_prompt,
            model="gpt-3.5-turbo-0125",
            model_settings=ModelSettings(
                temperature=0.4,
                max_tokens=150
            ),
            tools=[
                rag_docs(
                    tool_name="retrieval",
                    tool_description="Complementa la consulta con información de la BBDD de la empresa"
                )
            ],
        )
        return agent
    except Exception as e:
        return f"Error en creación de agente: {str(e)}"
    
def prepare_inputs(inputs):
    """En caso de existir, recupera historial de conversación y la anexa a nueva consulta"""
    sender = inputs.get("sender")
    history = memory.get_history(sender)
    context = "\n".join([f"User: {h["user"]}\nAgent: {h["agent"]}" for h in history])
    inputs["context"] = context
    return inputs

def ....
context_message = f"{context}\nUsuario: {message}"

async def run_agent(inputs):
    inputs = prepare_inputs(inputs)
    agent = initialize_agent()
    response = await Runner.run(agent, context_message)
    return response