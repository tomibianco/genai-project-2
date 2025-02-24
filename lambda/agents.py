import logging
import os
import re
from dotenv import load_dotenv
from memory import load_memory, save_memory
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.vectorstores import Pinecone
from prompt import prompt_s3
from tools import wikipedia_tool


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuración de LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.4, openai_api_key=OPENAI_API_KEY)

# Carga de prompt desde S3
prompt_data = prompt_s3()
prompt_template = PromptTemplate.from_dict(prompt_data)

# Herramientas
tools = [wikipedia_tool]

# Crear memoria de conversación
memory = ConversationBufferMemory()

# Inicializar la conexión con Pinecone
# index_name = "genaiproject2"
# vectorstore = Pinecone.from_existing_index(index_name)

# Creación del Agente
agent = AgentExecutor(
    llm=llm,
    tools=tools,
    memory=memory,
    prompt_template=prompt_template,
    # vectorstore=vectorstore
)

def process_message(sender, message):
    try:
        memory = load_memory(sender)
        agent.memory = memory
        user_message = HumanMessage(content=message)
        response = agent.run([user_message])
        memory = save_memory(sender)
        sentences = re.split(r'(?<=[.!?]) +', response)
        logging.info(f"Respuesta generada por el agente: {response}")
        return sentences
    except Exception as e:
        logging.error("Error al procesar el mensaje", exc_info=True)
        raise e