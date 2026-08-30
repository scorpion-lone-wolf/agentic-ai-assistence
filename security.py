from enum import Enum


class RiskLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    DESTRUCTIVE = "destructive"


def requires_human_approval(risk_level: RiskLevel) -> bool:
    """
    Decides if the action requires human approval or not
    """
    return risk_level in {
        RiskLevel.DESTRUCTIVE,
        RiskLevel.WRITE,
    }


def can_execute_automatically(risk_level: RiskLevel) -> bool:
    """
    Decides if the action can be executed automatically or not
    """
    return risk_level in {RiskLevel.READ}


def is_tool_allowed(
    tool_name: str,
    allowed_tools: set[str],
) -> bool:
    return tool_name in allowed_tools
