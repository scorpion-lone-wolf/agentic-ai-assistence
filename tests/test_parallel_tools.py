import time
import asyncio
from tools.arxiv_search import arxiv_search_async
from tools.web_search import web_search_async


async def run_parallel_searches():
    results = await asyncio.gather(
        web_search_async("AI reflection agents"),
        arxiv_search_async("AI reflection agents"),
    )
    return results


def test_search_tool_run_concurrently():
    start = time.perf_counter()

    result = asyncio.run(run_parallel_searches())

    end = time.perf_counter()

    duration = end - start

    assert len(result) == 2

    print(f"\nTook {duration:.2f} seconds")
