import json
from llm import call_llm_text
from pydantic import Field
from typing import Literal
from pydantic import BaseModel
from datetime import datetime


class ResearchStep(BaseModel):
    # which tool to use
    tool: Literal[
        "search_arxiv",
        "search_web",
    ]
    # what query to pass to the tool
    query: str = Field(
        min_length=1,
        max_length=500,
    )

    # why to use this tool
    reason: str = Field(
        min_length=1,
        max_length=500,
    )


class ResearchPlan(BaseModel):
    # user's goal for the research
    goal: str = Field(
        min_length=1,
        max_length=1000,
    )
    steps: list[ResearchStep] = Field(default_factory=list)


def create_research_plan(goal: str) -> ResearchPlan:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Research Planner. "
                "Your Task is to write a research plan , so that an agent should execute step by step in order to achieve user's goal."
                f"Current Date is -> {str(datetime.now())}"
                "You are not responsible for executing any step, just write the plan."
                "You have a access to the tools , so you can add to the plan if needed"
                "You should only write the plan and nothing else"
                "Available Tools :- \n"
                "- search_arxiv: academic papers and scholarly research\n"
                "- search_web: recent/current general web information\n\n"
                "Return ONLY valid JSON in this format:\n"
                """
                    {
                        "goal" : <"The Goal of the Research that user want to do research you and for which you should plan the steps">
                        "steps": [
                            {
                                "tool": <"The tool to use for this step">,
                                "query": <"The query to pass to the tool">,
                                "reason": <"Why to use this tool? like why you decide to do that">
                            }
                        ]
                    }
                """
            ),
        },
        {
            "role": "user",
            "content": goal,
        },
    ]
    raw_response = call_llm_text(messages)

    data = json.loads(raw_response)
    print(data)
    return ResearchPlan.model_validate(data)
