from agents import graph
from fastapi import FastAPI
from pydantic import BaseModel
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()

class MessageRequest(BaseModel):
    sender: str
    message: str

@app.post("/lambda")
async def lambda_handler(request: MessageRequest):
    try:
        # Extraer el JSON del body
        # body = json.loads(event.get("body", "{}"))
        # sender = body.get("sender")
        # message = body.get("message", "")
        sender = request.sender
        message = request.message
        logging.info(f" Mensaje recibido de {sender}: {message}")
        # Procesamiento del mensaje con Agente
        config = {"configurable": {"thread_id": "1"}}
        response = graph.stream({"messages": [{"role": "user", "content": message}]}, config, stream_mode="values")
        logging.info(f" Respuesta generada por el agente")
        return response
    except Exception as e:
        logging.error(f" Error en la Lambda: {str(e)}")