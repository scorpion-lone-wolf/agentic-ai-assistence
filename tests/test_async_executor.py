import asyncio
from types import SimpleNamespace

import pytest
from pydantic import BaseModel

import runtime.tool_executor as tool_executor

from tool import Tool
from models.actions import PendingAction


class FakeToolArgs(BaseModel):
    text: str


def sync_tool_function(text: str, max_results: int = 2) -> str:
    return f"sync: {text}"


async def async_tool_function(
    text: str,
    max_results: int = 2,
) -> str:
    await asyncio.sleep(0.01)
    return f"async: {text}"


sync_tool = Tool(
    name="sync_test",
    description="Test sync tool",
    function=sync_tool_function,
    args_model=FakeToolArgs,
)


async_tool = Tool(
    name="async_test",
    description="Test async tool",
    function=async_tool_function,
    args_model=FakeToolArgs,
)


@pytest.mark.anyio
async def test_async_executor_runs_async_tool(
    monkeypatch,
):

    monkeypatch.setattr(
        tool_executor,
        "tool_registry",
        {
            "async_test": async_tool,
        },
    )

    action = PendingAction(
        tool_name="async_test",
        tool_arguments={
            "text": "hello",
        },
        tool_id="test-1",
    )

    result = await tool_executor.execute_prepared_tool_async(action)

    assert result == "async: hello"


@pytest.mark.anyio
async def test_async_executor_runs_sync_tool(
    monkeypatch,
):

    monkeypatch.setattr(
        tool_executor,
        "tool_registry",
        {
            "sync_test": sync_tool,
        },
    )

    action = PendingAction(
        tool_name="sync_test",
        tool_arguments={
            "text": "hello",
        },
        tool_id="test-2",
    )

    result = await tool_executor.execute_prepared_tool_async(action)

    assert result == "sync: hello"
