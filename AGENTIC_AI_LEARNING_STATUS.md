# Agentic AI Engineering Learning Status

## Purpose

This file is the **session-to-session progress and handoff document** for the Agentic AI Engineering project.

- `AGENTIC_AI_LEARNING_ROADMAP.md` = stable overall goal, curriculum, and architecture principles.
- `AGENTIC_AI_LEARNING_STATUS.md` = what we have completed, current stage, known issues, and what to do next.

When a new chat starts:

1. Read `AGENTIC_AI_LEARNING_ROADMAP.md` to understand the overall project and learning goal.
2. Read this file to understand where we currently are.
3. Continue from **NEXT ACTION**.

The roadmap should **not** be changed merely because a session ends. Update this file when progress or the current implementation state changes.

---

# Current stage

**Milestone 22 — Async + Parallel Execution — IN PROGRESS**

We have already learned and implemented the basic async/parallel architecture. M22 is not complete yet.

---

# What we have done so far

## M1–M10 — Core agent foundation

Completed:

- Python project setup.
- Gemini through Google AI Studio using the OpenAI-compatible endpoint.
- OpenAI Python SDK model calls.
- Manual function/tool calling.
- Tool registry and generic agent loop.
- Web search tool.
- arXiv search tool.
- Maximum research-step protection.
- Pydantic validation for LLM tool arguments.
- LLM provider retry handling.
- Reusable `Tool` abstraction with metadata and async capability detection.

## M11–M13 — Reflection and grounded research

Completed:

- Reflection fundamentals.
- Structured critic.
- Iterative critique/revision.
- Evidence-backed research and writing.

Important lesson:

> Correct tool selection does not guarantee relevant evidence.

## M14–M16 — Planning, state, multi-agent workflow

Completed:

- Structured `ResearchPlan`.
- Agent state/memory.
- Coordinator orchestration.
- Planner -> Researcher -> Writer -> Critic workflow.

## M17–M19 — Approval, MCP foundation, security

Completed:

- Risk levels.
- Human approval for side-effecting actions.
- Runtime-enforced tool allowlists.
- External content treated as untrusted data.
- Basic MCP server/client/tool/resource learning demo.
- Security/guardrail tests.

MCP is currently a foundation/demo, not fully integrated into the main Researcher/runtime. Full MCP architecture is intentionally later in the roadmap.

## M20 — Observability basics

Completed at the intentionally simple level:

- trace id
- logs
- timestamps / elapsed time

Advanced tracing is deferred to the production architecture stage.

## M21 — Agent evals / testing

Completed conceptually and mostly implemented:

- deterministic security tests
- real LLM tool-selection evaluation
- mocked Researcher happy path
- mocked tool failures
- max-step stopping test
- Critic groundedness evaluation
- Writer revision evaluation
- end-to-end workflow test
- regression-testing strategy

A real Researcher run previously exposed an API message-field bug: `tool_id` was used where `tool_call_id` was required. That was corrected.

Current test files include:

```text
tests/test_async_executor.py
tests/test_critic.py
tests/test_parallel_tools.py
tests/test_researcher.py
tests/test_researcher_mocked.py
tests/test_security.py
tests/test_workflow.py
tests/test_writer.py
```

---

# M22 progress — Async + parallel execution

## Learned

- `async` / `await`.
- `asyncio.run()`.
- Sequential versus concurrent awaits.
- `asyncio.gather()`.
- Why blocking synchronous functions cannot simply be treated as asynchronous.
- `asyncio.to_thread()` as a bridge for blocking synchronous work.

## Implemented

- Async wrappers for web search and arXiv search using `asyncio.to_thread()`.
- `Tool.is_async` using `inspect.iscoroutinefunction`.
- `execute_prepared_tool_async()` in the runtime executor.
- Tests for sync and async tool execution.
- A parallel web-search + arXiv wrapper test.
- `can_run_in_parallel()` security policy.
- `action_can_run_in_parallel()` runtime helper.
- `run_researcher_agent()` converted to async.
- Coordinator updated to await the Researcher.
- Researcher restructured into prepare -> classify -> execute -> store results.
- Parallel-safe actions are executed with `asyncio.gather()`.

Current concurrency policy is deliberately conservative:

```text
READ          -> may run in parallel
WRITE         -> not parallel-safe
DESTRUCTIVE   -> not parallel-safe
```

---

# Important current implementation notes

### 1. Tool registry async implementation needs deliberate resolution

The web-search and arXiv modules have async wrappers, but the registered `Tool` objects currently point to the synchronous functions.

We need to decide how the registry should expose the correct execution implementation while keeping the LLM-visible name/schema stable.

Mental model:

```text
LLM-visible tool name/schema
        !=
internal execution implementation
```

Do not change this blindly; use it as a learning step.

### 2. `prepare_tool_call()` has a known unknown-tool-path bug

The function can reach `tool.function` after the registry lookup fails. This should be fixed during an appropriate runtime cleanup step, not forgotten.

### 3. Some temporary/unused code exists

Known cleanup candidates include:

- `tools/temperature.py`
- global `tool_schemas` in `tools/__init__.py` if unused
- unused imports in `agents/researcher.py`
- unused import(s) in `runtime/tool_executor.py`
- MCP demo artifacts after the production MCP design is decided

Do not delete these just to make the current milestone look cleaner. Review them during the production architecture milestone.

---

# NEXT ACTION

Run the complete test suite:

```bash
pytest -q
```

Then:

1. Paste the complete output here.
2. Fix **one failure at a time**.
3. Re-run the relevant test.
4. Continue until the suite is clean.

After the existing async caller/test failures are resolved, continue M22 in this order:

1. Deterministic test proving two slow async tools actually overlap.
2. Runtime concurrency limit.
3. Per-tool timeout handling.
4. Partial-failure behavior for concurrent tool execution.
5. Verify allowlist, Pydantic validation, approval policy, and READ-only parallel policy.
6. Verify evidence ordering and `tool_call_id` handling.
7. Verify the complete workflow.
8. Run the full test suite again.
9. Only after all M22 work passes, review the repository and mark M22 complete.

---

# Working rules for future sessions

- Do not inspect GitHub after every tiny step.
- Review the repository at milestone completion or when the implementation genuinely requires it.
- Teach one small concept/change at a time.
- Explain the problem, mental model, exact change, why it exists, and how to test it before moving on.
- Do not jump ahead to future milestones merely because the implementation could be made more sophisticated.
- Keep this file updated with progress and the next action.
- Keep `AGENTIC_AI_LEARNING_ROADMAP.md` stable; it contains the overall plan and should not become the session log.
