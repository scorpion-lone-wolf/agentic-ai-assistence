from mcp_servers.research_server import mcp
import asyncio
from mcp import Client


async def main():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "calculate_word_count",
            {"text": "Agentic AI systems can use external tools."},
        )
        print("Tool result ", result.structured_content)


asyncio.run(main())
print("I am here....")
