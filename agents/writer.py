from models.research import format_evidence
from models.research import EvidenceItem
from llm import call_llm_text
from llm import call_llm


def run_writer_agent(
    question: str,
    evidences: list[EvidenceItem],
    current_answer: str,
    feedback: list[str],
) -> str:
    """
    Writer agent will write the first draft based on the collected evidence and user's question
    """
    evidence_text = format_evidence(evidences)

    feedback_text = "\n".join(f"- {item}" for item in feedback)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a research writer revising an answer. "
                "Address the critic's feedback while remaining strictly "
                "grounded in the supplied evidence. "
                "Do not invent unsupported facts."
            ),
        },
        {
            "role": "user",
            "content": (
                f"QUESTION:\n{question}\n\n"
                f"CURRENT ANSWER:\n{current_answer}\n\n"
                f"CRITIC FEEDBACK:\n{feedback_text}\n\n"
                f"EVIDENCE:\n{evidence_text}"
            ),
        },
    ]

    return call_llm_text(messages)
