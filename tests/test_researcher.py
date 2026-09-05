from agents.researcher import run_researcher_agent
import pytest


@pytest.mark.anyio
async def test_researcher_uses_arxiv_for_academic_query():
    result = await run_researcher_agent(
        "Find recent research paper on reflection in AI agents",
    )
    print(result)
    assert "arxiv_search" in result.tool_used
