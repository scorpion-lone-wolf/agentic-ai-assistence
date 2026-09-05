from models.actions import PendingAction
import pytest
from types import SimpleNamespace
import agents.researcher as researcher

# simple name space is used to create object without defining class
fake_tool_call = SimpleNamespace(
    id="fake-call-1",
    function=SimpleNamespace(
        type="function",
        name="arxiv_search",
        arguments='{"query": "Machine Learning"}',
    ),
)


fake_assistant_message = SimpleNamespace(
    content=None,
    tool_calls=[fake_tool_call],
)


def fake_call_llm(messages, tools=None):
    return fake_assistant_message


async def fake_execute_tool_call(action: PendingAction):
    return "Fake arXiv research result"


@pytest.mark.anyio
async def test_researcher_records_mocked_arxiv_tool(
    monkeypatch,
):
    # inside the researcher module , replace call_llm with fake_call_llm
    monkeypatch.setattr(
        researcher,
        "call_llm",
        fake_call_llm,
    )
    # same for execute_tool_call
    monkeypatch.setattr(
        researcher,
        "execute_prepared_tool_async",
        fake_execute_tool_call,
    )
    result = await researcher.run_researcher_agent(
        "Find papers about reflection agents."
    )

    assert "arxiv_search" in result.tool_used
    assert result.evidence[0].content == "Fake arXiv research result"


async def fake_failed_tool_call(action: PendingAction):
    return "Tool execution failed with some error :  fake error"


@pytest.mark.anyio
async def test_researcher_store_tool_failure_as_evidence(monkeypatch):
    # inside the researcher module , replace call_llm with fake_call_llm
    monkeypatch.setattr(
        researcher,
        "call_llm",
        fake_call_llm,
    )
    # same for execute_tool_call
    monkeypatch.setattr(
        researcher,
        "execute_prepared_tool_async",
        fake_failed_tool_call,
    )

    result = await researcher.run_researcher_agent(
        "Find papers about reflection agents."
    )

    assert (
        result.evidence[0].content
        == "Tool execution failed with some error :  fake error"
    )


@pytest.mark.anyio
async def test_researcher_respects_max_steps(monkeypatch):
    call_count = 0

    def fake_looping_llm(messages, tools=None):
        nonlocal call_count
        call_count += 1
        return fake_assistant_message

    def fake_tool_call(action: PendingAction):
        return "Fake research result"

    monkeypatch.setattr(
        researcher,
        "call_llm",
        fake_looping_llm,
    )

    monkeypatch.setattr(
        researcher,
        "execute_tool_call",
        fake_tool_call,
    )
    result = await researcher.run_researcher_agent(
        "Find papers about reflection agents."
    )
    assert call_count == researcher.MAX_RESEARCH_STEPS
