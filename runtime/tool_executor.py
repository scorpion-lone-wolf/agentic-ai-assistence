from approval import request_human_approval
from models.actions import PendingAction
from tools import tool_registry
import json


def execute_tool_call(tool_call) -> str:
    action, error = prepare_tool_call(tool_call)
    if error:
        return error

    if action_requires_approval(action):
        return (
            f"Tool '{action.tool_name}' requires "
            f"human approval and cannot be automatically executed."
        )

    return execute_prepared_tool(action)


# here we are preparing for execution
# we validate , parse and prepare the tool call
def prepare_tool_call(tool_call):
    """
    parse and validate the tool but don't execute
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

    # Building the Pending Action
    pending_action = PendingAction(
        tool_name=tool.name,
        tool_arguments=dict(validated_arguments),
        tool_id=tool_call.id,
    )

    return pending_action, None


# here we are executing the tool which is already validated
# so we get pending action
def execute_prepared_tool(pending_action: PendingAction) -> str:
    """
    Execute an already validated tool action.
    """
    tool = tool_registry.get(pending_action.tool_name)

    if tool is None:
        return f"Unknown tool '{pending_action.tool_name}'."

    try:

        result = tool.function(**pending_action.tool_arguments)

    except Exception as error:

        return (
            f"Tool '{pending_action.tool_name}' failed with "
            f"{type(error).__name__}: {error}"
        )

    return str(result)


def action_requires_approval(pending_action: PendingAction) -> bool:
    tool = tool_registry.get(pending_action.tool_name)
    if not tool:
        return False
    return tool.requires_approval
