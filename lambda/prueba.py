# from crewai import Agent, Task, Crew, LLM, Process
# from dotenv import load_dotenv
# from memory import MemoryManager
# import os


# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# memory = MemoryManager()

# llm = LLM(
#     model="gpt-3.5-turbo-0125",
#     temperature=0.4,
#     max_tokens=150,
#     top_p=0.9,
#     frequency_penalty=0.1,
#     presence_penalty=0.1,
#     stop=["END"],
#     seed=42
# )


# class ChatBot:
#     def __init__(self):
#         # Configurar el agente
#         self.agent = Agent(
#             role='Vendedor Inteligente',
#             goal='Proporcionar respuestas muy breves',
#             backstory="""Eres un asistente IA experto en ventas.""",
#             verbose=True
#         )
        
#     def process_message(self, sender: str, message: str) -> str:
#         """Procesa un mensaje y devuelve la respuesta"""
#         try:
#             # Recuperar historial de conversación
#             history = memory.get_history(sender)
#             context = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

#             # Crear tarea dinámica con el mensaje del usuario
#             task = Task(
#                 description=f"{context}\nUsuario: {message}",
#                 agent=self.agent,
#                 expected_output='Una respuesta muy breve'
#             )
            
#             # Configurar el crew
#             crew = Crew(
#                 agents=[self.agent],
#                 tasks=[task],
#                 process=Process.sequential
#             )

#             # Ejecutar el crew
#             response = str(crew.kickoff())

#             # Guardar en memoria
#             memory.store_message(sender, message, response)
            
#             return response
            
#         except Exception as e:
#             return f"Error procesando el mensaje: {str(e)}"









from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv
from memory import MemoryManager
import re
import os


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


class ChatBot:
    def __init__(self):
        # Configurar el agente
        self.agent = Agent(
            role='Vendedor Inteligente',
            goal='Proporcionar respuestas muy breves',
            backstory="""Eres un asistente IA experto en ventas.""",
            verbose=True
        )

    def process_message(self, sender: str, message: str) -> list:
        """Procesa un mensaje y devuelve la respuesta como un array de oraciones"""
        try:
            # Recuperar historial de conversación
            history = memory.get_history(sender)
            context = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

            # Crear tarea dinámica con el mensaje del usuario
            task = Task(
                description=f"{context}\nUsuario: {message}",
                agent=self.agent,
                expected_output='Una respuesta muy breve'
            )
            
            # Configurar el crew
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                process=Process.sequential
            )

            # Ejecutar el crew y procesar la respuesta
            raw_response = str(crew.kickoff())
            
            # Crear diccionario con respuestas divididas en oraciones terminadas en: . , ! o ?
            response = re.split('(?<=[.!?])\s+', raw_response.strip())
            response = tuple(s.strip() for s in response if s.strip())

            # Guardar en memoria la respuesta original
            memory.store_message(sender, message, response)
            
            return response
            
        except Exception as e:
            return [f"Error procesando el mensaje: {str(e)}"]
