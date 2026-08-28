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
