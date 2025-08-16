from typing import List
from pydantic import BaseModel


class AgentCapabilities(BaseModel):
    streaming: bool
    pushNotifications: bool
    stateTransitionHistory: bool


class AgentSkill(BaseModel):
    id: str
    name: str
    description: str
    tags: List[str]
    examples: List[str]


class AgentCard(BaseModel):
    name: str
    description: str
    url: str
    version: str
    capabilities: AgentCapabilities
    skills: List[AgentSkill]


if __name__ == "__main__":
    agent_card = AgentCard(
        name="Test Agent",
        description="This is a test agent",
        url="https://test-agent.com",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="1",
                name="Test Skill",
                description="This is a test skill",
                tags=["test"],
                examples=["This is a test example"]
            )
        ]
    )
    print(100*"#")
    print("Test1:", AgentCard.model_validate(agent_card.model_dump()))
    print(100*"#")
    print("Test2:",
          AgentCard.model_validate(
                                {
                                    "id": 1,
                                    "name": "Test Skill",
                                    "description": "This is a test skill",
                                    "url": "https://test-agent.com",
                                    "version": "1.0.0",
                                    "capabilities": {"streaming": True},
                                    "skills": [
                                        {"id": "1",
                                         "name": "Test Skill",
                                         "description": "This is a test skill",
                                         "tags": ["test"],
                                         "examples": ["This is a test example"]}]
                                }
                            )
    )
    print(100*"#")
