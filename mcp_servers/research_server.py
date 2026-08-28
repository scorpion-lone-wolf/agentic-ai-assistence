from mcp.server import MCPServer

# Create a mcp server
mcp = MCPServer("ResearchUtilities")


# ------------------------------
# MCP TOOL
# ------------------------------


@mcp.tool()
def calculate_word_count(text: str) -> int:
    """
    Count the number of word in a text
    """
    return len(text.split(" "))


@mcp.resource("research://guidelines")
def research_guidelines() -> str:
    """
    Return our basic research guidelines.
    """

    return (
        "1. Prefer external evidence for current claims.\n"
        "2. Distinguish evidence from model-generated conclusions.\n"
        "3. Do not claim information is current if retrieval failed."
    )


# ------------------------------
# MCP RESOURCE
# ------------------------------


if __name__ == "__main__":
    mcp.run()
