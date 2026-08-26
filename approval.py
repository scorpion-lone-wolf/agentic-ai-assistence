from models.actions import PendingAction


def request_human_approval(pendingAction: PendingAction) -> bool:
    print("\n========== HUMAN APPROVAL REQUIRED ==========")

    print("\nArguments:")

    for key, value in pendingAction.tool_arguments.items():

        print(f"{key}: {value}")

    return input(f"Approve the action ? (y/n): ").lower() == "y"
