from agent import run_agent_loop

result = run_agent_loop(
    "Find recent arXiv papers about reflection in AI agents "
    "and summarize the main research directions."
)

print("LLM says Result : \n", result)
