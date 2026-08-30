from types import SimpleNamespace
import agents.researcher as researcher

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


def fake_execute_tool_call(
    tool_call,
    allowed_tools,
):
    return "Fake arXiv research result"


def test_researcher_records_mocked_arxiv_tool(
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
        "execute_tool_call",
        fake_execute_tool_call,
    )
    result = researcher.run_researcher_agent("Find papers about reflection agents.")

    assert "arxiv_search" in result.tool_used
    assert result.evidence[0].content == "Fake arXiv research result"


def fake_failed_tool_call(
    tool_call,
    allowed_tools,
):
    return "Tool execution failed with some error :  fake error"


def test_researcher_store_tool_failure_as_evidence(monkeypatch):
    # inside the researcher module , replace call_llm with fake_call_llm
    monkeypatch.setattr(
        researcher,
        "call_llm",
        fake_call_llm,
    )
    # same for execute_tool_call
    monkeypatch.setattr(
        researcher,
        "execute_tool_call",
        fake_failed_tool_call,
    )

    result = researcher.run_researcher_agent("Find papers about reflection agents.")

    assert len(result.evidence) == 1
    assert (
        result.evidence[0].content
        == "Tool execution failed with some error :  fake error"
    )
