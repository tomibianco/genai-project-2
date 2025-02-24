import boto3
import json
from langchain.memory import ConversationBufferMemory


# Configurar cliente de S3
s3_client = boto3.client("s3")
BUCKET_NAME = "agent-memory"

def load_memory(session_id):
    """Carga el historial de conversación desde S3"""
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=f"memory/{session_id}.json")
        memory_data = json.loads(response['Body'].read().decode('utf-8'))
        return ConversationBufferMemory(memory_key="history", chat_memory=memory_data)
    except s3_client.exceptions.NoSuchKey:
        return ConversationBufferMemory(memory_key="history")

def save_memory(session_id, memory):
    """Guarda el historial de conversación en S3"""
    memory_data = memory.chat_memory
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=f"memory/{session_id}.json",
        Body=json.dumps(memory_data)
    )