# here we are testing the whole workflow, not the individual span

import pytest
from agents.critic import CritiqueResult
from models.research import EvidenceItem
from models.research import ResearchResult
from planner import ResearchStep
from planner import ResearchPlan
from coordinator import run_multi_agent_workflow
import coordinator


@pytest.mark.anyio
async def test_complete_workflow(monkeypatch):

    # ---------------------------------
    #  fake the planner
    # ---------------------------------
    fake_plan = ResearchPlan(
        goal="Test Research goal",
        steps=[
            ResearchStep(
                tool="web_search",
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
            tool_name="web_search",
            tool_arguments={"query": "test query"},
            content="Test research evidence.",
        )
    ]
    fake_research_result = ResearchResult(tool_used=[], evidence=fake_evidence)

    async def fake_run_researcher_agent(question, plan, trace_id):
        return fake_research_result

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
        fake_run_researcher_agent,
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

    state = await run_multi_agent_workflow("Test question")

    # ---------------------------------------------
    # Verify final state
    # ---------------------------------------------

    assert state.plan == fake_plan

    assert state.evidence == fake_evidence

    assert state.current_answer == fake_answer
