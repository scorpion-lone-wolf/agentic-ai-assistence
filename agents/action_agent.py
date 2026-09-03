from tools import get_tool_schemas
from approval import request_human_approval
from runtime.tool_executor import execute_prepared_tool
from runtime.tool_executor import action_requires_approval
from runtime.tool_executor import prepare_tool_call
from llm import call_llm

MAX_ACTION_STEPS = 5

ALLOWED_TOOLS = {"arxiv_search", "web_search"}
action_tool_schemas = get_tool_schemas(ALLOWED_TOOLS)


def run_action_agent(request: str):
    """
    This agent can perform actions like sending an email, updating a database, etc. as requested by user
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a action agent whose job is to perform actions on behalf of the user. "
                "You can perform actions like sending an email, updating a database, etc. as requested by the user. "
                "Never clam task as success unless you have performed the task and you got result from tool"
            ),
        },
        {
            "role": "user",
            "content": request,
        },
    ]
    for step in range(1, MAX_ACTION_STEPS + 1):
        print("\n ========== ACTION step - " + str(step) + " ==========")
        assistant_message = call_llm(
            messages=messages,
            tools=action_tool_schemas,
        )

        messages.append(assistant_message)

        if not assistant_message.tool_calls:

            return assistant_message.content

        for tool_call in assistant_message.tool_calls:

            action, error = prepare_tool_call(tool_call)

            if error:
                tool_result = error
            elif action_requires_approval(action):

                approved = request_human_approval(action)

                if approved:

                    tool_result = execute_prepared_tool(action)
                    print("After approval", tool_result)
                else:

                    tool_result = f"Tool '{action.tool_name}' required Human Approval and human rejected the action."
            else:
                tool_result = execute_prepared_tool(action)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

    return "Action agent stopped because the " "maximum step limit was reached."
