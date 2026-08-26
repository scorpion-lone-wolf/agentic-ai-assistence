from pydantic import BaseModel


class EvidenceItem(BaseModel):
    tool_name: str
    tool_arguments: dict
    content: str


def format_evidence(
    evidence: list[EvidenceItem],
) -> str:
    sections = []

    for index, item in enumerate(evidence, start=1):
        sections.append(
            (
                f"EVIDENCE {index}\n"
                f"Tool: {item.tool_name}\n"
                f"Arguments: {item.tool_arguments}\n"
                f"Content:\n{item.content}"
            )
        )

    if not sections:
        return "No external evidence was collected."

    return "\n\n".join(sections)
