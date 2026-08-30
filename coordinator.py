from observability import elapsed_seconds
from observability import create_trace_id, log, now
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

    # ========== Workflow ==========
    trace_id = create_trace_id()
    log(trace_id, "Workflow Started...")

    state = AgentState(user_question=question)

    # ========== PLANNER ==========
    log(trace_id, "Planner Started...")
    start = now()

    state.plan = create_research_plan(state.user_question)

    duration = elapsed_seconds(start)
    log(trace_id, f"Planner Finished in {duration:.2f}s")

    # ========== RESEARCHER ==========
    log(trace_id, "Researcher Started...")
    start = now()

    research_result = run_researcher_agent(state.user_question, state.plan, trace_id)

    print("\n========== RESEARCH RESULT ==========", research_result)
    state.evidence = research_result.evidence

    duration = elapsed_seconds(start)
    log(trace_id, f"Researcher Finished in {duration:.2f}s")

    # ========== WRITER ==========
    log(trace_id, "Writer Started...")
    start = now()

    state.current_answer = run_writer_agent(
        state.user_question, state.evidence, state.current_answer, []
    )

    duration = elapsed_seconds(start)
    log(trace_id, f"Writer Finished in {duration:.2f}s")

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
