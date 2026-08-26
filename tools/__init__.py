from tools.email import email_tool
from tools.arxiv_search import arxiv_search_tool
from tools.web_search import web_search_tool
from tools.temperature import temperature_tool

ALL_TOOLS = [arxiv_search_tool, web_search_tool, temperature_tool, email_tool]

tool_registry = {tool.name: tool for tool in ALL_TOOLS}

tool_schemas = [tool.to_llm_schema() for tool in ALL_TOOLS]
