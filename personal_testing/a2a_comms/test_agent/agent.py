from datetime import datetime
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


def get_current_time() -> str:
    """
    Returns the current time in the format HH:MM:SS
    Args:
        None
    Returns:
        str: The current time in the format HH:MM:SS
    """
    print("I am running the special tool")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


base_agent = Agent(
    model=LiteLlm(
        model="openai/qwen3:4b",
        api_key="ollama",
        base_url="http://localhost:11434/v1",    
    ),
    name="time_agent",
    description="A agent that tells the time",
    instruction="You are a time agent that tells the time",
    tools=[get_current_time],
)

root_agent = base_agent
