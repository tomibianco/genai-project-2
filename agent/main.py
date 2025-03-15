from agent import run_agent
from langfuse_log import get_trace, log_message, log_response
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import time


logging.basicConfig(level=logging.INFO)

app = FastAPI()

class MessageRequest(BaseModel):
    sender: str
    message: str

@app.get("/")
def index():
    return {"Mensaje": "API de ventas con Agente Vendedor"}

@app.post("/agent_response")
async def agent_response(request: MessageRequest):
    try:
        sender = request.sender
        message = request.message
        trace = get_trace(sender)
        log_message(trace, sender, message)
        logging.info(f" Mensaje recibido de {sender}: {message}")
        start_time = time.time()
        response = run_agent(
            inputs={
                "sender": sender,
                "message": message
            }
        )
        logging.info(f" Respuesta generada por el agente")
        log_response(trace, response, start_time)
        return {"response": response}
    except Exception as e:
        logging.error(f" Error en agent_response: {str(e)}")
        return {"error": "Ocurrió un error en el procesamiento del mensaje", "details": str(e)}