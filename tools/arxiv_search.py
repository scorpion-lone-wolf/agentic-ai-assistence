from tool import Tool
from pydantic import Field
from pydantic import ConfigDict
from pydantic import BaseModel
import arxiv


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


def search_arxiv(query: str, max_results: int = 2):
    """
    Search query in arxiv and return the top 2 max_results
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


arxiv_search_tool = Tool(
    name="arxiv_search",
    description="Search arxiv for information",
    function=search_arxiv,
    args_model=ArxivSearchArgs,
)
