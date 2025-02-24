import boto3
import json

# Configurar cliente de S3
s3 = boto3.client("s3")

# Parámetros de S3
BUCKET_NAME = "BUCKET_S3"
PROMPT_FILE = "prompt.json"

# def prompt_s3():
#     """Descarga y lee el prompt JSON desde bucket S3"""
#     response = s3.get_object(Bucket=BUCKET_NAME, Key=PROMPT_FILE)
#     content = response['Body'].read().decode('utf-8')
#     return json.loads(content)

PROMPT_FILE_PATH = "/home/tomibianco/genai_2/prompt_test.json"
def prompt_s3():
    """Lee el prompt JSON desde un archivo local"""
    with open(PROMPT_FILE_PATH, 'r', encoding='utf-8') as file:
        content = file.read()
    return json.loads(content)