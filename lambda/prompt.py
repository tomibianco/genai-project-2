import boto3
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Configurar cliente de S3
s3 = boto3.client("s3")

# Parámetros de S3
BUCKET_NAME = "mi-bucket-prompt"
PROMPT_FILE = "prompts/prompt.json"

def prompt_s3():
    """Descarga y lee el prompt JSON desde bucket S3"""
    response = s3.get_object(Bucket=BUCKET_NAME, Key=PROMPT_FILE)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)