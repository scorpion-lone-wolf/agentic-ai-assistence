from agents.researcher import run_researcher_agent
from agents.writer import run_writer_agent
from agents.critic import run_critic_agent
from planner import create_research_plan
from state import AgentState

MAX_CRITIQUE_STEPS = 5


def run_multi_agent_workflow(question: str):
    """
    Coordinates Planner, Researcher, Writer and Critic agents
    """
    state = AgentState(user_question=question)

    print("\n========== PLANNER ==========")

    state.plan = create_research_plan(state.user_question)

    print("\n========== RESEARCHER ==========")

    state.evidence = run_researcher_agent(state.user_question, state.plan)

    print("\n========== WRITER ==========")

    state.current_answer = run_writer_agent(
        state.user_question, state.evidence, state.current_answer, []
    )

    for critic_step in range(1, MAX_CRITIQUE_STEPS + 1):

        print(f"\n========== CRITIC step - {critic_step} ==========")

        critic_result = run_critic_agent(
            state.user_question,
            state.evidence,
            state.current_answer,
        )
        state.reflection_steps = critic_step

        if critic_result.status == "pass":
            break

        state.current_answer = run_writer_agent(
            state.user_question,
            state.evidence,
            state.current_answer,
            critic_result.feedback,
        )

    return state
