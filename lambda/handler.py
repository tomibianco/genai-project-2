import json
import logging
from agents import process_message

logging.basicConfig(level=logging.INFO)

def lambda_handler(event):
    try:
        # Extraer el JSON del body
        body = json.loads(event.get("body", "{}"))
        sender = body.get("sender")
        message = body.get("message", "")
        logging.info(f" Mensaje recibido de {sender}: {message}")

        # Procesamiento del mensaje con los agentes
        response = process_message(sender, message)
        response_array = {
            "response": [{"message": resp} for resp in response]
        }
        logging.info(f" Respuesta del agente: {response}")

        # Devolver la respuesta en JSON
        return {
            "statusCode": 200,
            "body": json.dumps(response_array)
        }
    except Exception as e:
        logging.error(f" Error en la Lambda: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }