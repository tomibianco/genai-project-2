from crewai import Agent, LLM
from crewai.project import CrewBase, agent
from dotenv import load_dotenv
import os


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = LLM(
    model="gpt-3.5-turbo-0125",
    temperature=0.4,
    max_tokens=100,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42
)

@CrewBase
class SalesTeam():
  """Equipo encargado de manejar las ventas."""

  agents_config = "prompts/agents.yaml"

  @agent
  def seller(self) -> Agent:
    return Agent(
      config=self.agents_config["seller"],
      llm=llm,
    #   tools=[],
      verbose=True
    )