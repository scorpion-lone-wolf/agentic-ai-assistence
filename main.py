import asyncio
from coordinator import run_multi_agent_workflow

question = """
Find recent research on reflection in AI agents
and compare the academic techniques with current
practical implementations.
"""


state = asyncio.run(run_multi_agent_workflow("your question"))


print("\n========== FINAL ANSWER ==========\n")

print(state.current_answer)


# from agents.action_agent import (
#     run_action_agent,
# )

# request = """
# Send an email to alice@example.com.

# Subject:
# AI Research Complete

# Body:
# The AI agent research has been completed.
# """


# result = run_action_agent(request)


# print("\n========== RESULT ==========\n")

# print(result)
