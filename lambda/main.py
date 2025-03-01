from crew import SalesCrew
from fastapi import FastAPI
from pydantic import BaseModel
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()
sales_crew = SalesCrew()

class MessageRequest(BaseModel):
    sender: str
    message: str

@app.get("/")
def index():
    return {"Mensaje": "API de conversación con Agente Vendedor usando CrewAI"}

@app.post("/lambda")
async def lambda_handler(request: MessageRequest):
    try:
        sender = request.sender
        message = request.message
        logging.info(f" Mensaje recibido de {sender}: {message}")
        response = sales_crew.crew().kickoff(
            inputs={
                "sender": sender,
                "message": message
            }
        )
        logging.info(f" Respuesta generada por el agente")
        return {"response": response}
    except Exception as e:
        logging.error(f" Error en handler: {str(e)}")