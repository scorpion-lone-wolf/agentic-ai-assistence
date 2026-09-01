# here we are testing the whole workflow, not the individual span

from agents.critic import CritiqueResult
from models.research import EvidenceItem
from models.research import ResearchResult
from planner import ResearchStep
from planner import ResearchPlan
from coordinator import run_multi_agent_workflow
import coordinator


def test_complete_workflow(monkeypatch):

    # ---------------------------------
    #  fake the planner
    # ---------------------------------
    fake_plan = ResearchPlan(
        goal="Test Research goal",
        steps=[
            ResearchStep(
                tool="search_web",
                query="Test query",
                reason="Test reason",
            )
        ],
    )

    # ---------------------------------
    #  fake the researcher
    # ---------------------------------
    fake_evidence = [
        EvidenceItem(
            tool_name="search_web",
            tool_arguments={"query": "test query"},
            content="Test research evidence.",
        )
    ]
    fake_research_result = ResearchResult(tool_used=[], evidence=fake_evidence)

    # ---------------------------------
    #  fake the writer
    # ---------------------------------
    fake_answer = "This is the test answer based on the provided evidences."

    # ---------------------------------
    #  fake the critic
    # ---------------------------------
    fake_critic_result = CritiqueResult(
        status="pass",
        feedback=[],
    )

    # ---------------------------------------------
    # Replace real components
    # ---------------------------------------------
    monkeypatch.setattr(
        coordinator,
        "create_research_plan",
        lambda goal: fake_plan,
    )
    monkeypatch.setattr(
        coordinator,
        "run_researcher_agent",
        lambda question, plan, trace_id: fake_research_result,
    )

    monkeypatch.setattr(
        coordinator,
        "run_writer_agent",
        lambda question, evidences, current_answer, feedback: fake_answer,
    )
    monkeypatch.setattr(
        coordinator,
        "run_critic_agent",
        lambda question, evidence, current_answer: fake_critic_result,
    )

    # ---------------------------------------------
    # Run complete workflow
    # ---------------------------------------------

    state = run_multi_agent_workflow("Test question")

    # ---------------------------------------------
    # Verify final state
    # ---------------------------------------------

    assert state.plan == fake_plan

    assert state.evidence == fake_evidence

    assert state.current_answer == fake_answer
