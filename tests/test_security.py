from security import RiskLevel
from security import requires_human_approval
from security import is_tool_allowed
from agents.researcher import RESEARCHER_ALLOWED_TOOLS


def test_researcher_allows_web_search():
    assert is_tool_allowed(
        "web_search",
        RESEARCHER_ALLOWED_TOOLS,
    )


def test_researcher_blocks_email():
    assert not is_tool_allowed(
        "send_email",
        RESEARCHER_ALLOWED_TOOLS,
    )


def test_read_tool_does_not_require_approval():
    assert not requires_human_approval(RiskLevel.READ)


def test_write_tool_requires_approval():
    assert requires_human_approval(RiskLevel.WRITE)


def test_destructive_tool_requires_approval():
    assert requires_human_approval(RiskLevel.DESTRUCTIVE)
