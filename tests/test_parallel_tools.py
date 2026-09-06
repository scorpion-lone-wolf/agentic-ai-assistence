from runtime.tool_executor import execute_prepared_tool_async
from models.actions import PendingAction
from tools import tool_registry
from tool import Tool
from pydantic import BaseModel
import pytest
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


# creating a fake slow tool function
async def slow_tool(name: str):
    await asyncio.sleep(0.2)
    return name


class SlowToolArguments(BaseModel):
    name: str


active_tools = 0  # current how many are active
max_active_tools = 0  # how many we have seen max active


# testing that two async tools actually overlap and run concurrently
@pytest.mark.anyio
async def test_two_slow_async_tool_overlap():
    start = time.perf_counter()

    result = await asyncio.gather(
        slow_tool("one"),
        slow_tool("two"),
    )

    end = time.perf_counter()
    elapsed = end - start
    assert result == ["one", "two"]
    assert elapsed < 0.35


async def tracked_slow_tool(name: str):
    global active_tools, max_active_tools
    active_tools += 1
    max_active_tools = max(max_active_tools, active_tools)
    await asyncio.sleep(0.2)
    active_tools -= 1
    return name


tracked_slow_tool_definition = Tool(
    name="tracked_slow_tool",
    description="A slow test tool used to measure concurrency.",
    function=tracked_slow_tool,
    args_model=SlowToolArguments,
)
tool_registry["tracked_slow_tool"] = tracked_slow_tool_definition


@pytest.mark.anyio
async def test_six_tools_run_with_max_three_at_the_same_time():
    global active_tools, max_active_tools
    active_tools = 0
    max_active_tools = 0

    actions = [
        PendingAction(
            tool_name="tracked_slow_tool",
            tool_arguments={"name": "one"},
            tool_id="test-one",
        ),
        PendingAction(
            tool_name="tracked_slow_tool",
            tool_arguments={"name": "two"},
            tool_id="test-two",
        ),
        PendingAction(
            tool_name="tracked_slow_tool",
            tool_arguments={"name": "three"},
            tool_id="test-three",
        ),
        PendingAction(
            tool_name="tracked_slow_tool",
            tool_arguments={"name": "four"},
            tool_id="test-four",
        ),
        PendingAction(
            tool_name="tracked_slow_tool",
            tool_arguments={"name": "five"},
            tool_id="test-five",
        ),
        PendingAction(
            tool_name="tracked_slow_tool",
            tool_arguments={"name": "six"},
            tool_id="test-six",
        ),
    ]

    results = await asyncio.gather(
        *(execute_prepared_tool_async(action) for action in actions)
    )

    assert results == ["one", "two", "three", "four", "five", "six"]
    assert max_active_tools == 3


@pytest.mark.anyio
async def test_parallel_tools_keep_successful_results_when_one_tool_fails():
    async def successful_tool(name: str):
        await asyncio.sleep(0.1)
        return name

    async def failing_tool(name: str):
        await asyncio.sleep(0.1)
        raise ValueError("test failure")

    successful_tool_definition = Tool(
        name="successful_test_tool",
        description="A successful test tool.",
        function=successful_tool,
        args_model=SlowToolArguments,
    )

    failing_tool_definition = Tool(
        name="failing_test_tool",
        description="A failing test tool.",
        function=failing_tool,
        args_model=SlowToolArguments,
    )

    tool_registry["successful_test_tool"] = successful_tool_definition
    tool_registry["failing_test_tool"] = failing_tool_definition

    actions = [
        PendingAction(
            tool_name="successful_test_tool",
            tool_arguments={"name": "one"},
            tool_id="test-one",
        ),
        PendingAction(
            tool_name="failing_test_tool",
            tool_arguments={"name": "two"},
            tool_id="test-two",
        ),
        PendingAction(
            tool_name="successful_test_tool",
            tool_arguments={"name": "three"},
            tool_id="test-three",
        ),
    ]

    results = await asyncio.gather(
        *(execute_prepared_tool_async(action) for action in actions)
    )

    assert results[0] == "one"
    assert "failed with ValueError: test failure" in results[1]
    assert results[2] == "three"


@pytest.mark.anyio
async def test_slow_tool_timeout():
    # create a very slow tool (function)
    async def very_slow_tool(name: str):
        await asyncio.sleep(3)
        return name

    # create a slow tool definition
    very_slow_tool_definition = Tool(
        name="very_slow_tool",
        description="A very slow test tool.",
        function=very_slow_tool,
        args_model=SlowToolArguments,
    )

    # add the tool to the registry
    tool_registry["very_slow_tool"] = very_slow_tool_definition

    # create a pending action
    action = PendingAction(
        tool_name="very_slow_tool",
        tool_arguments={"name": "one"},
        tool_id="test-one",
    )

    # only wait for 1.0 seconds, if more than 1.0 seconds passed, them raise TimeoutError
    # but out function should handle that timeout and return timeout error for that particular tool
    result = await execute_prepared_tool_async(action)
    assert "timeout" in result.lower()
