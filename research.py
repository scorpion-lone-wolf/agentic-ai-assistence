import json
from agent import execute_tool_call
from tools import tool_schemas
from llm import call_llm
from openai.types.beta import assistant
from pydantic import Field
from pydantic import BaseModel


class EvidenceItem(BaseModel):
    tool_name: str  # what tool you used
    tool_arguments: str  # what arguments you passed to the tool
    content: str  # what the tool returned or if no tool used then what response you got from LLM


class ResearchResult(BaseModel):
    preliminary_answer: str
    evidence: list[EvidenceItem] = Field(
        default_factory=list
    )  # default factory will create empty list that is not shared across instances


MAX_RESEARCH_STEPS = 5


def run_research_agent(task: str) -> ResearchResult:
    """
    This is the main function that runs the research agent and performs the research task.
    Output : ResearchResult
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Highly Intelligent Research Agent who has access to multiple tools."
                "Using Your Knowledge and Tools you should answer the user's question."
                "You should use tools when needed."
                "You should use tools when you think that they are relevant."
                "When you have sufficient evidence, produce a concise "
                "preliminary answer based only on the available evidence."
            ),
        },
        {
            "role": "user",
            "content": task,
        },
    ]

    # * Execute tool and collect evidence
    evidence: list[EvidenceItem] = []

    for step in range(1, MAX_RESEARCH_STEPS + 1):

        print("\n========== RESEARCH STEP " f"{step} ==========\n")

        assistant_message = call_llm(messages, tools=tool_schemas)
        messages.append(assistant_message)

        # ? does LLM ask for tool calls?
        if not assistant_message.tool_calls:
            return ResearchResult(
                preliminary_answer=assistant_message.content,
                evidence=evidence,
            )

        #  * LLM ask for tool call
        for tool_call in assistant_message.tool_calls:

            tool_result = execute_tool_call(tool_call)
            print("\n Research Tool Result \n")
            print(tool_result)

            arguments = tool_call.function.arguments

            evidence.append(
                EvidenceItem(
                    tool_name=tool_call.function.name,
                    tool_arguments=arguments,
                    content=tool_result,
                )
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )
    return ResearchResult(
        preliminary_answer=(
            "Research stopped because the maximum "
            "number of research steps was reached."
        ),
        evidence=evidence,
    )


def format_evidence(evidence: list[EvidenceItem]) -> str:
    section = []
    for index, item in enumerate(evidence, start=1):
        section.append(
            (
                f"Evidence {index}"
                f"Tool: {item.tool_name}\n"
                f"Arguments: {item.tool_arguments}\n"
                f"Content: {item.content}\n"
            )
        )
    if not section:
        return "No evidence Collected."
    return "\n\n".join(section)
