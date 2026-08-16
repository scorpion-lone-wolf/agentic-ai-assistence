from tools import get_current_temperature
import json
from llm import call_llm

# this is the available tools that an LLM can ask for tool call
tools = [
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
    }
]


messages = [
    {
        "role": "system",
        "content": """
            You are a helpful assistant.
            You can use available tools if strictly needed.
        """,
    },
    {"role": "user", "content": "What is weather in mumbai?"},
]


assistant_message = call_llm(messages, tools=tools)

messages.append(assistant_message)

# is ai asking for tool call?
if assistant_message.tool_calls:
    tool_to_call = assistant_message.tool_calls[0]
    function_to_call = tool_to_call.function.name
    args = json.loads(tool_to_call.function.arguments)

    print("Gemini Requested tool", function_to_call)
    print("Arguments:", args)

    if function_to_call == "get_current_temperature":
        tool_result = get_current_temperature(city=args["city"])
    else:
        tool_result = "Tool not found"

    messages.append(
        {"role": "tool", "tool_call_id": tool_to_call.id, "content": tool_result}
    )
    final_msg = call_llm(messages, tools=tools)
    print(final_msg.content)

else:
    print(assistant_message.content)
