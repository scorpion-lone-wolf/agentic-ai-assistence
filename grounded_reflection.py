import json
from llm import call_llm_text
from pydantic import Field
from typing import Literal
from pydantic import BaseModel
from research import format_evidence
from research import ResearchResult

MAX_GROUNDED_REFLECTION_STEPS = 3


class GroundedCritique(BaseModel):

    status: Literal[
        "pass",
        "needs_revision",
    ]

    feedback: list[str] = Field(default_factory=list)


# ? TASk = Is this a good answer given what the evidence actually supports?
def critique_research(task: str, answer: str, research: ResearchResult):
    """
    This function will critique the research result and give feedback
    It will check whether the answer is accurate, clear and informative and upto the fact based on research evidence
    - task = user's task or question
    - answer = preliminary answer from research agent
    - research = research result (contains all the evidence collected during research in the form of array of evidence items)
    """
    evidence_text = format_evidence(research.evidence)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict research reviewer. "
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
                f"QUESTION:\n{task}\n\n"
                f"ANSWER:\n{answer}\n\n"
                f"RESEARCH EVIDENCE:\n{evidence_text}"
            ),
        },
    ]
    raw_response = call_llm_text(messages)  # no tools here in this step
    data = json.loads(raw_response)

    return GroundedCritique.model_validate(data)


def revise_grounded_answer(
    task: str,
    answer: str,
    research: ResearchResult,
    critique: GroundedCritique,
) -> str:

    evidence_text = format_evidence(research.evidence)

    feedback_text = "\n".join(f"- {item}" for item in critique.feedback)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a careful research writer. "
                "Revise the answer using the research evidence "
                "and reviewer feedback. "
                "Do not add claims that are unsupported by the evidence. "
                "If the evidence is insufficient, explicitly say so. "
                "Preserve useful URLs and source information when present. "
                "Return only the revised answer."
            ),
        },
        {
            "role": "user",
            "content": (
                f"QUESTION:\n{task}\n\n"
                f"CURRENT ANSWER:\n{answer}\n\n"
                f"REVIEW FEEDBACK:\n{feedback_text}\n\n"
                f"RESEARCH EVIDENCE:\n{evidence_text}"
            ),
        },
    ]

    return call_llm_text(messages)


def run_grounded_reflection_loop(task, research: ResearchResult):
    current_answer = research.preliminary_answer

    for step in range(1, MAX_GROUNDED_REFLECTION_STEPS + 1):
        # step 1: critique the answer based on research evidence
        critique = critique_research(task, current_answer, research)

        # check if status is pass
        if critique.status == "pass":
            print("\nCritic accepted the answer.")
            return current_answer

        # step 2 : revise the answer based on critique
        current_answer = revise_grounded_answer(
            task, current_answer, research, critique
        )

    print("\nMaximum reflection steps reached. " "Returning latest revision.")
    return current_answer
