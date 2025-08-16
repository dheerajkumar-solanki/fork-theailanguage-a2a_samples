import asyncio
import traceback
from datetime import datetime

from google.genai import types
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


class TellTimeAgent:
    def __init__(self):
        self.agent = self._build_agent()
        self._user_id = "time_agent_user"
        self.runner = Runner(
            app_name=self.agent.name,
            agent=self.agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    @staticmethod
    def _get_current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _build_agent(self):
        return Agent(
            model=LiteLlm(
                model="openai/qwen3:4b",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
            ),
            name="time_agent",
            description="A agent that tells the time",
            instruction="You are a time agent that tells the time",
            tools=[TellTimeAgent._get_current_time],
        )

    async def invoke(self, query: str, session_id: str) -> str:
        try:

            session = await self.runner.session_service.get_session(
                app_name=self.agent.name,
                user_id=self._user_id,
                session_id=session_id,
            )

            if session is None:
                session = await self.runner.session_service.create_session(
                    app_name=self.agent.name,
                    user_id=self._user_id,
                    session_id=session_id,
                )

            content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=query)]
            )

            last_event = None
            async for event in self.runner.run_async(
                user_id=self._user_id,
                session_id=session.id,
                new_message=content,
            ):
                print(event.model_dump_json(indent=2))
                last_event = event

            if (
                last_event is None or
                last_event.content is None or
                last_event.content.parts is None or
                len(last_event.content.parts) == 0
            ):
                return ""

            return "\n".join([
                p.text for p in last_event.content.parts if p.text
            ])

        except Exception as e:
            print(
                f"🔥🔥🔥 An error occurred in TellTimeAgent.invoke: {e}"
            )

            traceback.print_exc()

            return (
                "Sorry, I encountered an internal error and couldn't "
                "process your request."
            )


async def main():
    agent = TellTimeAgent()
    print(10 * "=")
    response = await agent.invoke("What is the time?", "session_1")
    print(response)
    print(10 * "=")
    response2 = await agent.invoke("What is the current date?", "session_1")
    print(response2)
    print(10 * "=")


if __name__ == "__main__":
    asyncio.run(main())
