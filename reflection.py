from llm import call_llm_text


# =====================
# * Generator (this will generate the first draft)
# =====================
def generate_draft(task: str) -> str:
    """
    It take the task and generate the first draft
    """
    message = [
        {
            "role": "system",
            "content": (
                "You are a technical writer"
                "Create a accurate , clear and informative answer"
                "to the user's task"
            ),
        },
        {
            "role": "user",
            "content": task,
        },
    ]

    return call_llm_text(message)


# =====================
# * Critique (this will critique the first draft and give feedback)
# =====================
def critique_draft(task: str, draft: str) -> str:
    """
    This takes actual task and the first generated draft and returns critique
    """
    message = [
        {
            "role": "system",
            "content": (
                "You are a strict reviewer"
                "You should check the draft carefully"
                "You should give feedback on the draft if the draft is not accurate, not clear or not informative"
                "It should also check if the draft is related to the task"
                "Do not change the original draft, instead only actionable critiques should be provided"
            ),
        },
        {
            "role": "user",
            "content": (f"Original Task: \n{task}\n\n" f"Draft: \n{draft}"),
        },
    ]
    return call_llm_text(message)


# =====================
# * Revise (this will apply the critique and generate the final draft)
# =====================
def revise_draft(task: str, draft: str, critique: str) -> str:
    """
    This takes actual task , first draft and critique and returns the final draft
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a careful editor."
                "You should change the draft based on critiques."
                "You should check the draft carefully and apply critiques"
                "as some part are already good and some part are not so good"
                "So apply the critiques and generate a final result"
            ),
        },
        {
            "role": "user",
            "content": (
                f"Original Task: \n{task}\n\n"
                f"Original Draft: \n{draft}\n\n"
                f"Critique: \n{critique}"
            ),
        },
    ]
    return call_llm_text(messages)


# run reflection workflow
def run_reflection(task: str) -> str:
    # generate draft
    print("-----------------------Generating draft...")
    draft = generate_draft(task)
    print(draft)

    # critique draft
    print("-----------------------Critique draft...")
    critique = critique_draft(task, draft)
    print(critique)

    # revise draft
    print("-----------------------Revision...")
    final_draft = revise_draft(task, draft, critique)
    print(final_draft)

    return final_draft
