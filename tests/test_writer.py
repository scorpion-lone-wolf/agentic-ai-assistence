from agents.writer import run_writer_agent
from models.research import EvidenceItem


def test_writer_removes_unsupported_claims():
    evidences = [
        EvidenceItem(
            tool_name="mock_source",
            tool_arguments={},
            content=(
                "Reflection techniques can help AI agents "
                "review previous outputs and improve subsequent attempts."
            ),
        )
    ]

    current_answer = "Reflection improves agent accuracy by exactly 40%."
    question = "Does reflection improve agent accuracy?"
    feedback = [
        "The exact '40%' improvement is not supported by the supplied evidence. This need to be re-evaluated."
    ]

    revised_answer = run_writer_agent(
        question=question,
        evidences=evidences,
        current_answer=current_answer,
        feedback=feedback,
    )
    assert "40%" not in revised_answer
