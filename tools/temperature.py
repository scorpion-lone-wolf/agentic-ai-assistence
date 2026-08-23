from tool import Tool
from pydantic import Field
from pydantic import ConfigDict
from pydantic import BaseModel


class TemperatureArgs(BaseModel):
    # this means if any other field is passed ,this validator will raise error
    model_config = ConfigDict(extra="forbid")

    city: str = Field(
        max_length=20,
        min_length=3,
    )


def get_current_temperature(city: str) -> str:
    """
    Fake weather tool for learning tool calling.
    """

    temperatures = {
        "delhi": "33°C",
        "mumbai": "29°C",
        "bangalore": "24°C",
        "london": "18°C",
    }

    return temperatures.get(city.lower(), f"No temperature data available for {city}")


temperature_tool = Tool(
    name="get_current_temperature",
    description="Fetch the current temperature of a city",
    function=get_current_temperature,
    args_model=TemperatureArgs,
)
