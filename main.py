from coordinator import run_multi_agent_workflow

question = """
Find recent research on reflection in AI agents
and compare the academic techniques with current
practical implementations.
"""


state = run_multi_agent_workflow(question)


print("\n========== FINAL ANSWER ==========\n")

print(state.current_answer)
