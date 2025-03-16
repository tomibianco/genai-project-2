import logging
import os
import re
import time
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner
from langfuse_log import get_prompt, get_trace, log_message, log_response
from memory import MemoryManager
from tools import rag_docs


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
    """En caso de existir, recupera historial de conversación y la anexa a contexto"""
    sender = inputs.get("sender")
    history = memory.get_history(sender)
    context = "\n".join([f"User: {h["user"]}\nAgent: {h["agent"]}" for h in history])
    inputs["context"] = context
    return inputs

def message_creation(inputs):
    """Compila el input del usuario con historial de conversación, en caso que exista"""
    message = inputs.get("message")
    context = inputs.get("context")
    context_message = f"{context}\nUsuario: {message}"
    return context_message

def process_output(response):
    """Crea diccionario con respuestas divididas en oraciones terminadas en: . , ! o ?"""
    raw_response = str(response)
    formatted_response = re.split(r"(?<=[.!?])\s+", raw_response.strip())
    formatted_response = tuple(s.strip() for s in formatted_response if s.strip())
    return formatted_response

async def run_agent(inputs):
    """Corre el flujo de agente para input de usuario"""
    trace = get_trace(inputs["sender"])
    log_message(trace, inputs["sender"], inputs["sender"])
    start_time = time.time()
    agent = initialize_agent()
    processed_inputs = prepare_inputs(inputs)
    agent_message = message_creation(processed_inputs)
    response = await Runner.run(agent, agent_message)
    log_response(trace, response, start_time)
    memory.store_message(inputs["sender"], inputs["message"], response)
    formatted_response = process_output(response)
    return formatted_response