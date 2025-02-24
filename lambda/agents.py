import logging
import os
import re
from dotenv import load_dotenv
from memory import load_memory, save_memory
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.vectorstores import Pinecone
from prompt import prompt_s3
from tools import search_wikipedia


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def create_agent():
    # Configuración de LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.4, openai_api_key=OPENAI_API_KEY)

    # Carga de prompt desde S3
    prompt_data = prompt_s3()
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=prompt_data)

    # Herramientas
    tools = [search_wikipedia]

    # Crear memoria de conversación
    memory = ConversationBufferMemory(memory_key="history")

    # Inicializar la conexión con Pinecone
    # index_name = "genaiproject2"
    # vectorstore = Pinecone.from_existing_index(index_name)

    # Creación del Agente
    agent = initialize_agent(
        llm=llm,
        tools=tools,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        # vectorstore=?
        verbose=True
    )

    return agent


def process_message(sender, message):
    try:
        agent = create_agent()
        memory = load_memory(sender)
        agent.memory = memory
        user_message = HumanMessage(content=message)
        response = agent.invoke({"input": user_message.content})
        memory = save_memory(sender, memory)
        sentences = re.split(r'(?<=[.!?]) +', response["output"])
        logging.info(f"Respuesta generada por el agente: {response}")
        return sentences
    except Exception as e:
        logging.error("Error al procesar el mensaje", exc_info=True)
        raise e


from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools)