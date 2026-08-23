from tools import tool_registry
import json
from tools import tool_schemas
from llm import call_llm

MAX_AGENT_STEPS = 10


def execute_tool_call(tool_call) -> str:
    """
    Parse and Extract which tool to call.
    Return the tool result if executed successfully else return error as tool result so that LLM can know what went wrong
    """

    function_name = tool_call.function.name
    # parse arguments
    try:
        raw_arguments = json.loads(
            tool_call.function.arguments
        )  # raw arguments passed by the LLM
    except json.JSONDecodeError as e:
        return f"Tool ${function_name} can't be executed \n because of error in parsing arguments: {e}"

    print(f"\nTool requested: {function_name}")
    print(f"Arguments: {raw_arguments}")

    # find the actual tool to call
    tool = tool_registry.get(function_name)

    if tool is None:
        tool_result = f"Unknown tool: {function_name}"

    tool_function = tool.function
    args_model = tool.args_model  # this is the validation model for arguments

    # --------------------------
    #  argument validation
    # -------------------------
    try:
        validated_arguments = args_model.model_validate(raw_arguments)
    except Exception as e:
        return f"Tool {function_name} can't be executed \n because of error in validating arguments: {e}"

    # --------------------------
    #  tool execution
    # -------------------------
    try:
        tool_result = tool_function(**dict(validated_arguments))
    except Exception as e:
        return f"Tool {function_name} can't be executed \n because of error in executing tool: {e}"

    return str(tool_result)


def run_agent_loop(user_message: str) -> str:
    """
    Run our agent until the LLM returns a final answer

    The Loop works like :

    1.Send users message to LLM
    2. LLM decided whether it want a tool call or not
    3. If needed , out agent(code) will call the tool
    4. Agent send the tool result back to LLM
    5. Repeat the loop until the LLM need no more tool call and return a final answer

    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant."
                "You may use Multiple tools when needed"
                "Use search_archive tool when user ask for academic research papers, scientific studies, research literatures etc"
                "Use search_web tool when user ask for general information about a topic or you think that not related to academic research papers"
                "While using tools if you encounter an error, you can try other tools if they are relevant else clearly response to the user that"
                "you encountered an error while accessing tools so you can fulfill the request"
                "Hard Rule You Should Follow"
                "1. Always use tools when needed"
                "2. Always use tools when you think that they are relevant"
                "3. If user ask for latest result and tool calls fails don;t response with old data or data that is not recent from your knowledge base"
            ),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    for step in range(1, MAX_AGENT_STEPS + 1):
        print(
            f"=============== Currently Agent is running step: {step} ==============="
        )
        #  Asking the LLM what to do next
        assistant_message = call_llm(
            messages=messages,
            tools=tool_schemas,
        )
        # preserve the assistant response in history
        messages.append(assistant_message)

        # =============================
        # if there are no tool calls ,
        # the agent has finished
        # =============================
        if not assistant_message.tool_calls:
            return assistant_message.content

        # =============================
        # the LLM decided to call a tool
        # Our Agent need to call the tool and pass result to the LLM
        # =============================

        for tool_call in assistant_message.tool_calls:

            tool_result = execute_tool_call(tool_call)
            print(f"Tool result: {tool_result}")
            # add result to history and let LLM know the tool call result
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

    # Agent exceeded its budget step
    return f"Agent stopped after reaching the maximum " f"of {MAX_AGENT_STEPS} steps."
