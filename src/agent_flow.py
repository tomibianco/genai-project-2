import logging
import os
import re
import time
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner
from monitoring import get_prompt, get_trace, log_message, log_response
from memory import MemoryManager
from tools import rag_docs


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
memory = MemoryManager()


def initialize_agent(context) -> Agent:
    """Definición de agente vendedor"""
    try:
        agent = Agent(
            name="seller",
            instructions=get_prompt(context),
            model="gpt-3.5-turbo-0125",
            model_settings=ModelSettings(
                temperature=0.4,
                max_tokens=150
            ),
            tools=[rag_docs]
        )
        return agent
    except Exception as e:
        logging.error(f"Error en creación de agente: {e}", exc_info=True)
        return None
    
def load_conversation(inputs):
    """En caso de existir, recupera historial de conversación y la anexa a contexto"""
    sender = inputs.get("sender")
    history = memory.get_history(sender)
    context = "\n".join([f"{h["user"]}\n{h.get("agent", "")}" for h in history])
    return context

def process_output(response):
    """Crea diccionario con respuestas divididas en oraciones terminadas en: . , ! o ?"""
    formatted_response = re.split(r"(?<=[.!?])\s+", response.strip())
    formatted_response = [s.strip() for s in formatted_response if s.strip()]
    return formatted_response

async def run_agent(inputs):
    """Corre el flujo de agente para input de usuario"""
    trace = get_trace(inputs["sender"])
    log_message(trace, inputs["sender"], inputs["message"])
    start_time = time.time()
    context = load_conversation(inputs)
    agent = initialize_agent(context)
    response = await Runner.run(agent, inputs["message"])
    raw_response = response.final_output
    log_response(trace, raw_response, start_time)
    memory.store_message(inputs["sender"], inputs["message"], raw_response)
    formatted_response = process_output(raw_response)
    return formatted_response