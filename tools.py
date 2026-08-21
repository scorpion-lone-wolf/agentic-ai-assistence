# function
import arxiv
from ddgs import DDGS


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


def search_arxiv(query: str, max_results: int = 2):
    """
    Search query in arxiv and return the top 5 max_results
    """
    client = arxiv.Client()
    results = arxiv.Search(
        query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []

    for index, paper in enumerate(client.results(results), start=1):
        title = paper.title
        url = paper.entry_id
        description = paper.summary
        published = paper.published
        authors = ", ".join(author.name for author in paper.authors)

        papers.append(f"""
            Result {index}
            title : {title}
            url : {url}
            published : {published}
            description : {description}
            authors : {authors}
        """.strip())

    if not papers:
        return "No arxiv search results found."

    return "\n\n".join(papers)


# =========================================================================
# Tool definition sent to LLM (By this LLM will know what all tools are available)
# =========================================================================
tool_schemas = [
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
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "Using this when you need to search the web for information to answer a question or provide information to a user"
                "Search the web for the given query which return the top max_results(default to 5) in form of string separated by two new line"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search the web",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "number of results to return",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_arxiv",
            "description": (
                "Using this when you need to search the archive for academic research papers to answer a question or provide information to a user"
                "Search the archive for the given query which return the top max_results(default to 5) in form of string separated by two new line"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query topic to search",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "number of results to return",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

# ==========================================================
# Tool registry used by OUR Python program
# ==========================================================
tool_registry = {
    "get_current_temperature": get_current_temperature,
    "search_web": search_web,
    "search_arxiv": search_arxiv,
}
