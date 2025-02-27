from crewai import Task
from crewai.project import CrewBase, task


@CrewBase
class SalesTeam():
  """Equipo encargado de manejar las ventas."""

  agents_config = "prompts/agents.yaml"

  @task
  def sales_task(self) -> Task:
    return Task(
      config=self.tasks_config["sales_task"]
    )