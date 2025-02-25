import logging
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from typing_extensions import TypedDict
from tools import scientific_calculator


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

builder = StateGraph(State)
memory = MemorySaver()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.4, openai_api_key=OPENAI_API_KEY)

# prompt = PromptTemplate.from_messages(
#     {
#     "role": "Eres un experto en ventas de servicios, tu nombre es Adrián y tienes 32 años, eres de Valparaiso, Chile.",
#     "instructions": "Responde de manera amable y persuasiva."
#     }
# )

tools = [scientific_calculator]
llm_tools = llm.bind_tools(tools=tools)
tool_node = ToolNode(tools=tools)

def assistant(state: State):
    try:
        response = {"messages": [llm_tools.invoke(state["messages"])]}
        logging.info(f"Respuesta correctamente generada por el agente")
        return response
    except Exception as e:
        logging.error("Error al procesar el mensaje", exc_info=True)
        raise e


builder.add_node("assistant", assistant)
builder.add_node("tools", tool_node)
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
builder.add_edge("assistant", END)
graph = builder.compile(checkpointer=memory)