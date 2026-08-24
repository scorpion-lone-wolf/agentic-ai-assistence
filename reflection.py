import json
from llm import call_llm_text

from typing import Literal

from pydantic import BaseModel, Field

MAX_REFLECTION_STEPS = 3


class CritiqueResult(BaseModel):
    status: Literal[
        "pass", "needs_revision"
    ]  # cannot be anything else only pass or needs_revision

    feedback: list[str] = Field(default_factory=list)


# =====================
# * Generator (this will generate the first draft)
# =====================
def generate_draft(task: str) -> str:
    """
    It take the task and generate the first draft
    """
    message = [
        {
            "role": "system",
            "content": (
                "You are a technical writer"
                "Create a accurate , clear and informative answer"
                "to the user's task"
            ),
        },
        {
            "role": "user",
            "content": task,
        },
    ]

    return call_llm_text(message)


# =====================
# * Critique (this will critique the first draft and give feedback)
# =====================
def critique_draft(task: str, draft: str) -> str:
    """
    This takes actual task and the first generated draft and returns critique
    """
    message = [
        {
            "role": "system",
            "content": (
                "You are a strict reviewer"
                "You should check the draft carefully"
                "You should give feedback on the draft if the draft is not accurate, not clear or not informative"
                "It should also check if the draft is related to the task"
                "Do not change the original draft, instead only actionable critiques should be provided if needed"
                "You should output in the following JSON format"
                "{{ 'status': 'pass' or 'needs_revision', 'feedback': ['feedback1', 'feedback2', 'feedback3'] }}"
                "if status is pass then feedback should be empty"
                "Strictly follow the JSON format(HARD RULE OUTPUT)"
            ),
        },
        {
            "role": "user",
            "content": (f"Original Task: \n{task}\n\n" f"Draft: \n{draft}"),
        },
    ]
    response = call_llm_text(message)
    raw_data = json.loads(response)

    return CritiqueResult.model_validate(raw_data)


# =====================
# * Revise (this will apply the critique and generate the final draft)
# =====================
def revise_draft(task: str, draft: str, critique: CritiqueResult) -> str:
    """
    This takes actual task , first draft and critique and returns the final draft
    """
    feedback_text = "\n".join(f"- {item}" for item in critique.feedback)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a careful editor."
                "You should change the draft based on Feedback."
                "You should check the draft carefully and apply Feedback"
                "as some part are already good and some part are not so good"
                "So apply the Feedback and generate a revised result"
                "Output Should be the revised answer"
            ),
        },
        {
            "role": "user",
            "content": (
                f"Original Task: \n{task}\n\n"
                f"Original Draft: \n{draft}\n\n"
                f"REVIEW FEEDBACk: \n{feedback_text}"
            ),
        },
    ]
    return call_llm_text(messages)


# run reflection workflow
def run_reflection(task: str) -> str:
    # generate draft
    print("-----------------------Generating draft...")
    current_draft = generate_draft(task)
    print(current_draft)

    for reflection_step in range(1, MAX_REFLECTION_STEPS + 1):
        print(f"\n========== REFLECTION STEP " f"{reflection_step} ==========\n")

        # critique draft
        print("-----------------------Critique draft...")
        critique = critique_draft(task, current_draft)

        # check if status is pass
        if critique.status == "pass":
            print("\nCritic accepted the answer.")
            return current_draft

        # revise draft (as it needs revision)
        print("-----------------------Revision...")
        current_draft = revise_draft(task, current_draft, critique)
        print(current_draft)

    print("\nMaximum reflection steps reached. " "Returning latest revision.")
    return current_draft
