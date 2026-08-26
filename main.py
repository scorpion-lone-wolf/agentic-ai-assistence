from planner import create_research_plan
from state import AgentState
from grounded_reflection import run_grounded_reflection_loop
from research import run_research_agent

task = (
    "Find recent research about reflection in AI agents "
    "and summarize the main ideas."
)


# ---------------------------------------------------------
# 1. Initialize workflow state
# ---------------------------------------------------------
state = AgentState(user_question=task)


# ---------------------------------------------------------
# 2. Planning
# ---------------------------------------------------------
state.plan = create_research_plan(state.user_question)


# ---------------------------------------------------------
# 3. Research
# ---------------------------------------------------------
research_result = run_research_agent(state.user_question)

state.current_answer = research_result.preliminary_answer

state.evidence = research_result.evidence

# ---------------------------------------------------------
# 4. Reflection
# ---------------------------------------------------------
state.current_answer = run_grounded_reflection_loop(
    task=state.user_question,
    research=research_result,
)


print("\n=============== FINAL ANSWER:===============\n")
print(state.current_answer)
