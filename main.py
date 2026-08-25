from grounded_reflection import run_grounded_reflection_loop
from research import run_research_agent

task = (
    "Find recent research about reflection in AI agents "
    "and summarize the main ideas."
)

# do the research and give preliminary answer
research = run_research_agent(task)

# run grounded reflection loop and revise the preliminary answer
final_answer = run_grounded_reflection_loop(task, research)

print("\n=============== FINAL ANSWER:===============\n")
print(final_answer)
