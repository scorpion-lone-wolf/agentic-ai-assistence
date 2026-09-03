from security import RiskLevel
from pydantic import BaseModel
from typing import Type
from typing import Callable
import inspect


class Tool:
    """
    Represent one tool available to the agent
    """

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        args_model: Type[BaseModel],
        risk_level: RiskLevel = RiskLevel.READ,
    ):
        self.name = name
        self.description = description
        self.function = function
        self.args_model = args_model
        self.risk_level = risk_level
        self.is_async = inspect.iscoroutinefunction(function)

    def to_llm_schema(self):
        """
        This is the schema what openai expects
        {
            "type": "function",
                "function": {
                    "name": "get_current_temperature",
                    "description": "Fetch the current temperature of a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The name of the city",
                            }
                        },
                        "required": ["city"],
                    },
                },
        },
        """

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.args_model.model_json_schema(),  # same format what openai schema expects
            },
        }
