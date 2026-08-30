from models.research import EvidenceItem
from planner import ResearchPlan
from pydantic import Field
from typing import Any
from pydantic import BaseModel


class AgentState(BaseModel):
    user_question: str  # original task

    messages: list[Any] = Field(default_factory=list)  # conversation history

    plan: ResearchPlan | None = None

    evidence: list[EvidenceItem] = Field(
        default_factory=list
    )  # EvidenceItem : evidence collected during tool calls

    current_answer: str | None = None  # e.g based on this critique will be happening

    agent_steps: int = 0

    reflection_steps: int = 0
