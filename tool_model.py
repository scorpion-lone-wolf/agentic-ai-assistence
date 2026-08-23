from pydantic import ConfigDict
from pydantic import Field
from pydantic import BaseModel


class TempeartureArgs(BaseModel):
    # this means if any other field is passed ,this validator will raise error
    model_config = ConfigDict(extra="forbid")

    city: str = Field(
        max_length=20,
        min_length=3,
    )


class WebSearchArgs(BaseModel):
    # this means if any other field is passed ,this validator will raise error
    model_config = ConfigDict(extra="forbid")
    query: str = Field(
        max_length=500,
        min_length=1,
    )
    max_results: int = Field(
        default=2,
        ge=1,
        le=10,
    )


class ArxivSearchArgs(BaseModel):
    # this means if any other field is passed ,this validator will raise error
    model_config = ConfigDict(extra="forbid")
    query: str = Field(
        max_length=500,
        min_length=1,
    )
    max_results: int = Field(
        default=2,
        ge=1,
        le=10,
    )
