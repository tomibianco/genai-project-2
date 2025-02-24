import boto3
import json
from langchain.memory import ConversationBufferMemory


# # Configurar cliente de S3
# s3_client = boto3.client("s3")
# BUCKET_NAME = "BUCKET_S3"

# def load_memory(session_id):
#     """Carga el historial de conversación desde S3"""
#     try:
#         response = s3_client.get_object(Bucket=BUCKET_NAME, Key=f"memory/{session_id}.json")
#         memory_data = json.loads(response['Body'].read().decode('utf-8'))
#         return ConversationBufferMemory(memory_key="history", chat_memory=memory_data)
#     except s3_client.exceptions.NoSuchKey:
#         return ConversationBufferMemory(memory_key="history")

# def save_memory(session_id, memory):
#     """Guarda el historial de conversación en S3"""
#     memory_data = memory.chat_memory
#     s3_client.put_object(
#         Bucket=BUCKET_NAME,
#         Key=f"memory/{session_id}.json",
#         Body=json.dumps(memory_data)
#     )


# Directorio local para almacenar la memoria
LOCAL_MEMORY_DIR = "memory"

def load_memory(session_id):
    """Carga el historial de conversación desde un archivo local"""
    try:
        file_path = os.path.join(LOCAL_MEMORY_DIR, f"{session_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                memory_data = json.load(file)
            return ConversationBufferMemory(memory_key="history", chat_memory=memory_data)
        else:
            return ConversationBufferMemory(memory_key="history")
    except Exception as e:
        print(f"Error al cargar la memoria: {e}")
        return ConversationBufferMemory(memory_key="history")

def save_memory(session_id, memory):
    """Guarda el historial de conversación en un archivo local"""
    try:
        if not os.path.exists(LOCAL_MEMORY_DIR):
            os.makedirs(LOCAL_MEMORY_DIR)
        file_path = os.path.join(LOCAL_MEMORY_DIR, f"{session_id}.json")
        memory_data = memory.chat_memory
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(memory_data, file)
    except Exception as e:
        print(f"Error al guardar la memoria: {e}")