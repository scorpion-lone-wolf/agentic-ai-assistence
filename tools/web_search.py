from security import RiskLevel
from tool import Tool
from pydantic import Field
from pydantic import ConfigDict
from pydantic import BaseModel
from ddgs import DDGS


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


def search_web(query: str, max_results: int = 2):
    """
    Search the web for the given query and return the top max_results
    It returns a list of array of results and each result contains
    title, url and description in formatted string
    """
    results = DDGS().text(query, max_results=max_results)

    formatted_results = []

    for index, result in enumerate(results, start=1):
        title = result.get("title", "")
        url = result.get("href", "")
        description = result.get("body", "")

        formatted_results.append(f"""
            Result {index}
            title : {title}
            url : {url}
            description : {description}
        """.strip())
    if not formatted_results:
        return "No web search results found."

    return "\n\n".join(formatted_results)


web_search_tool = Tool(
    name="web_search",
    description="Search the web for information",
    function=search_web,
    args_model=WebSearchArgs,
    risk_level=RiskLevel.READ,
)
