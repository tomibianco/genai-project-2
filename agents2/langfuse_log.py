from dotenv import load_dotenv
from langfuse import Langfuse
import os
import time
import uuid


load_dotenv()
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")

langfuse = Langfuse(
  secret_key=LANGFUSE_SECRET_KEY,
  public_key=LANGFUSE_PUBLIC_KEY,
  host="https://cloud.langfuse.com"
)

conversation_traces = {}

def get_trace(sender):
    """Obtiene o crea un trace único para la conversación."""
    if sender not in conversation_traces:
        trace_id = str(uuid.uuid4())
        trace = langfuse.trace(name=f"conversation_{sender}", trace_id=trace_id)
        conversation_traces[sender] = trace
    return conversation_traces[sender]

def log_message(trace, sender, message):
    """Registra el mensaje del cliente."""
    trace.span(
        name="user_message",
        input={"sender": sender, "message": message}
    )

def log_response(trace, response, start_time):
    """Registra la respuesta del agente y su tiempo de procesamiento."""
    response_time = time.time() - start_time
    trace.span(
        name="agent_response",
        output=str(response),
        metadata={"response_time": response_time}
    )