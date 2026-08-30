from agents.researcher import run_researcher_agent


def test_researcher_uses_arxiv_for_academic_query():
    result = run_researcher_agent(
        "Find recent research on reflection in AI agents",
    )
    assert "search_arxiv" in result.tool_used
