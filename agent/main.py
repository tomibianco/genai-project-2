from seller_agent import run_agent
from fastapi import FastAPI
from pydantic import BaseModel
import logging


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
        logging.info(f" Mensaje recibido de {sender}: {message}")
        response = run_agent(
            inputs={
                "sender": sender,
                "message": message
            }
        )
        logging.info(f" Respuesta generada por el agente")
        return {"response": response}
    except Exception as e:
        logging.error(f" Error en agent_response: {str(e)}")
        return {"error": "Ocurrió un error en el procesamiento del mensaje", "details": str(e)}