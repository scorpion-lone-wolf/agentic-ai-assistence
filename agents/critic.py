from models.research import format_evidence
from models.research import EvidenceItem
from llm import call_llm_text
import json

from pydantic import Field
from typing import Literal
from pydantic import BaseModel


class CritiqueResult(BaseModel):
    status: str = Literal["pass", "needs_revision"]
    feedback: list[str] = Field(default_factory=list)


def run_critic_agent(
    question: str, evidence: list[EvidenceItem], answer: str
) -> CritiqueResult:
    """
    Critic Specialist
    Evaluate whether an answer is backed by evidence or not and if need revision or pass
    """
    evidence_text = format_evidence(evidence)

    message = [
        {
            "role": "system",
            "content": (
                "You are a strict research Critic. "
                "Evaluate the answer against BOTH the user's question "
                "and the supplied research evidence. "
                "Do not assume unsupported facts are true. "
                "Flag claims that are not supported by the evidence. "
                "Flag current or latest claims if no current evidence "
                "supports them. "
                "Check whether important evidence was misrepresented. "
                "Return ONLY valid JSON with this structure:\n"
                "{\n"
                '  "status": "pass" or "needs_revision",\n'
                '  "feedback": ["specific issue", "..."]\n'
                "}"
            ),
        },
        {
            "role": "user",
            "content": (
                f"QUESTION:\n{question}\n\n"
                f"ANSWER:\n{answer}\n\n"
                f"EVIDENCE:\n{evidence_text}"
            ),
        },
    ]

    raw_response = call_llm_text(message)

    data = json.loads(raw_response)

    return CritiqueResult.model_validate(data)
