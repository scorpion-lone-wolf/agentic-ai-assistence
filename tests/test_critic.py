from agents.critic import run_critic_agent
from models.research import EvidenceItem

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

answer = "Reflection improves agent accuracy by exactly 40%."


def test_critic_reject_unsupported_claims():
    result = run_critic_agent(
        question="Does reflection improve agent accuracy?",
        evidence=evidences,
        answer=answer,
    )
    assert result.status == "needs_revision"
