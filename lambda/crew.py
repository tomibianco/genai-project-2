import os
import re
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, after_kickoff, before_kickoff, crew, task
from memory import MemoryManager
from tools import scientific_calculator, rag_docs


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

memory = MemoryManager()

llm = LLM(
    model="gpt-3.5-turbo-0125",
    temperature=0.4,
    max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42
)

@CrewBase
class SalesCrew:
    """Equipo completo de vendedores capacitados para vender."""
    agents_config = "prompts/agents.yaml"
    tasks_config = "prompts/tasks.yaml"

    @before_kickoff
    def prepare_inputs(self, inputs):
        """Recupera historial de conversación"""
        sender = inputs.get("sender")
        history = memory.get_history(sender)
        context = "\n".join([f"User: {h["user"]}\nBot: {h["bot"]}" for h in history])
        inputs["context"] = context
        self._last_inputs = inputs.copy()
        return inputs
    
    @after_kickoff
    def process_output(self, output):
        """Convierte respuesta de Agente en Tupla para envío a Whatsapp"""
        inputs = self._last_inputs
        sender = inputs.get("sender")
        message = inputs.get("message")
        raw_response = str(output)
        # Crea diccionario con respuestas divididas en oraciones terminadas en: . , ! o ?
        response = re.split(r"(?<=[.!?])\s+", raw_response.strip())
        response = tuple(s.strip() for s in response if s.strip())
        # Guarda en memoria la respuesta original
        memory.store_message(sender, message, response)
        return response
    
    @agent
    def seller(self) -> Agent:
        return Agent(
            config=self.agents_config["seller"],
            llm=llm,
            tools=[scientific_calculator, rag_docs],
            verbose=True
        )
    
    @task
    def sales_task(self) -> Task:
        return Task(
            config=self.tasks_config["sales_task"]
        )
 
    @crew
    def crew(self) -> Crew:
        """Procesa un mensaje y devuelve la respuesta como un array de oraciones""" 
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )