from pydantic import BaseModel


class PendingAction(BaseModel):
    tool_name: str
    tool_arguments: dict
    tool_id: str
