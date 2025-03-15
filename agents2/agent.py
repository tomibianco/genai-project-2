import asyncio
from agents import Agent, Runner, ModelSettings
from dotenv import load_dotenv
from langfuse import Langfuse
import os


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")

langfuse = Langfuse()

def get_langfuse_prompt(*args, inputs):
    message = inputs.get("message")
    prompt = langfuse.get_prompt("prompt1", label="latest")
    compiled_prompt = prompt.compile(message=message)
    return compiled_prompt

agent = Agent(
    name="seller",
    instructions=get_langfuse_prompt,
    model="gpt-3.5-turbo-0125",
    model_settings=ModelSettings(
        temperature=0.4,
        max_tokens=150
    )
)

async def main():
    result = await Runner.run(agent, "Hola, que servicio ofrecen?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())