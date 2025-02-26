from prueba import ChatBot
from fastapi import FastAPI
from pydantic import BaseModel
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()
agent = ChatBot()

class MessageRequest(BaseModel):
    sender: str
    message: str

@app.get("/")
def index():
    return {"Mensaje": "API de conversación con Agente Vendedor usando CrewAI"}

@app.post("/lambda")
async def lambda_handler(request: MessageRequest):
    try:
        # body = json.loads(event.get("body", "{}"))
        # sender = body.get("sender")
        # message = body.get("message", "")
        sender = request.sender
        message = request.message
        logging.info(f" Mensaje recibido de {sender}: {message}")
        response = agent.process_message(sender, message)
        logging.info(f" Respuesta generada por el agente")
        return {"response": response}
    except Exception as e:
        logging.error(f" Error en handler: {str(e)}")