from crewai import Agent, Task, Crew, LLM, Process
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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


from memory import MemoryManager

memory = MemoryManager()


class ChatBot:
    def __init__(self):
        # Configurar el agente
        self.agent = Agent(
            role='Vendedor Inteligente',
            goal='Proporcionar respuestas muy breves',
            backstory="""Eres un asistente IA experto en ventas.""",
            verbose=True
        )
        
    def process_message(self, sender: str, message: str) -> str:
        """Procesa un mensaje y devuelve la respuesta"""

        # Recuperar el historial de conversación
        history = memory.get_history(sender)

        # Formatear historial para pasarlo al agente
        context = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

        try:
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

            # Ejecutar el crew
            response = str(crew.kickoff())

            # Guardar en memoria
            memory.store_message(sender, message, response)
            
            return response
            
        except Exception as e:
            return f"Error procesando el mensaje: {str(e)}"
