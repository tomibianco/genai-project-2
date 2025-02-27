from crewai import Crew, Process
from crewai.project import CrewBase, crew, before_kickoff, after_kickoff
from memory import MemoryManager
import re


memory = MemoryManager()


@CrewBase
class Crew:
    """Equipo completo de vendedores capacitados para vender."""

    @before_kickoff
    def prepare_inputs(self, sender):
        """Recupera historial de conversación"""
        history = memory.get_history(sender)
        context = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])
        return context
 
    @crew
    def process_message(self, sender: str, message: str) -> Crew:
        """Procesa un mensaje y devuelve la respuesta como un array de oraciones""" 
        return Crew(
            agents=self.agent,
            tasks=self.task,
            process=Process.sequential,
            verbose=True
        )

    @after_kickoff
    def process_output(self, sender, message):
        """Convierte respuesta de Agente en Tupla para envío a Whatsapp"""
        raw_response = str(crew.kickoff())
        
        # Crea diccionario con respuestas divididas en oraciones terminadas en: . , ! o ?
        response = re.split('(?<=[.!?])\s+', raw_response.strip())
        response = tuple(s.strip() for s in response if s.strip())

        # Guarda en memoria la respuesta original
        memory.store_message(sender, message, response)
        
        return response