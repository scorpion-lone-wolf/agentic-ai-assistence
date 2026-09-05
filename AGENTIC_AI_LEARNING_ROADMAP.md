# Agentic AI Engineering Learning Roadmap

## Purpose of this file

This file is the persistent handoff document for the Agentic AI Engineering learning project in this repository.

When starting a new ChatGPT conversation, **read this file first and continue from the exact `CURRENT STATE` and `NEXT ACTION` sections below**. Do not restart the curriculum from the beginning unless explicitly asked.

The GitHub repository is the source of truth for the implementation. This document is the source of truth for the learning roadmap, milestones, teaching approach, and handoff state.

Repository: `https://github.com/scorpion-lone-wolf/agentic-ai-assistence`
Default branch: `master`

---

# 1. What we originally wanted to learn

The goal is not merely to build a working chatbot. The goal is to understand how agentic AI systems work by building the runtime ourselves first.

Core learning goals:

- Python for agentic AI engineering, starting from a Node.js developer background.
- Gemini through Google AI Studio using an OpenAI-compatible endpoint.
- OpenAI Python SDK for model calls.
- Build our **own agent runtime/orchestration** first instead of starting with OpenAI Agents SDK.
- Understand tool calling deeply.
- Understand agent loops, planning, state, reflection, multi-agent workflows, security, human approval, MCP, async execution, context management, caching, observability, evals, and production architecture.
- Only after understanding the internals, compare the custom runtime with OpenAI Agents SDK and understand what the framework abstracts away.

Target system:

```text
User
  -> Coordinator
      -> Planner
      -> Researcher
          -> native tools
          -> MCP tools
      -> Evidence
      -> Writer
      -> Critic
      -> Revision
      -> Security / Approval
      -> Final answer
```

---

# 2. Teaching rules for future chats

The learner explicitly wants the project taught slowly.

For each new step:

1. Explain the **problem** we are solving.
2. Give a simple **mental model**.
3. Make **one small code change**.
4. Explain why the code exists and what breaks without it.
5. Run/test it.
6. Only then move to the next small change.

Do not dump a large implementation without mapping it to the exact file and section.

Do not silently redesign the architecture just because a shorter implementation exists. The purpose is learning the underlying concepts.

When a milestone is complete, it is useful to review the repository once and update this document. **Do not inspect GitHub after every tiny step unless specifically needed or requested.**

---

# 3. Milestone roadmap

## Milestone 1 — Project setup

Completed.

Topics:
- Python project structure
- dependencies
- environment setup
- basic repository organization

## Milestone 2 — Raw Gemini / OpenAI-compatible model call

Completed.

Topics:
- Gemini endpoint
- OpenAI Python SDK
- messages
- model responses

## Milestone 3 — Manual tool calling

Completed.

Topics:
- function/tool schemas
- model proposes a tool call
- application executes the function
- result is returned to the model

## Milestone 4 — Tool registry + generic agent loop

Completed.

Topics:
- reusable tool registry
- generic tool execution
- model -> tool -> result loop

## Milestone 5 — Web search

Completed.

Topics:
- external web retrieval as an agent tool
- current/general information retrieval

## Milestone 6 — arXiv search

Completed.

Topics:
- scholarly retrieval
- choosing tools based on research intent

## Milestone 7 — Hardened agent loop

Completed.

Topics:
- maximum loop steps
- stopping runaway tool loops

Current Researcher limit remains:

```python
MAX_RESEARCH_STEPS = 5
```

## Milestone 8 — Pydantic validation

Completed.

Topics:
- validate LLM-supplied tool arguments
- reject malformed/unexpected arguments
- keep tool inputs structured

## Milestone 9 — LLM provider retries

Completed.

Topics:
- transient model failures
- retry behavior

## Milestone 10 — Reusable Tool abstraction

Completed.

Topics:
- common Tool object
- tool metadata
- schemas
- risk metadata
- async capability metadata via `inspect.iscoroutinefunction`

## Milestone 11 — Reflection fundamentals

Completed.

Topics:
- model-generated critique
- reflection as a separate reasoning stage

## Milestone 12 — Iterative reflection + structured critic

Completed.

Topics:
- critic result structure
- repeated critique/revision
- stopping after a maximum critique count

Current coordinator limit remains:

```python
MAX_CRITIQUE_STEPS = 5
```

## Milestone 13 — Grounded research + reflection

Completed.

Topics:
- evidence-backed writing
- distinction between evidence and model-generated claims
- reflection over retrieved evidence

Important lesson discovered:

> Correct tool selection does not guarantee relevant evidence.

An arXiv retrieval can technically succeed and still return poor/irrelevant papers. Evaluation therefore has to measure evidence quality, not only whether a tool was called.

## Milestone 14 — Structured planning

Completed.

Topics:
- planner agent/function
- structured `ResearchPlan`
- research steps and reasons
- passing the plan into the Researcher

## Milestone 15 — State / memory

Completed.

Topics:
- `AgentState`
- preserving question, plan, evidence, current answer, reflection progress

## Milestone 16 — Multi-agent workflow

Completed.

Current high-level orchestration is in `coordinator.py` and includes Planner, Researcher, Writer, and Critic.

## Milestone 17 — Human-in-the-loop + side-effect tools

Completed.

Topics:
- risk levels
- human approval
- side-effecting tools
- separating authorization from LLM intent

Important security model:

```text
LLM proposes action
    -> runtime validates
    -> runtime checks agent allowlist
    -> unauthorized: BLOCK
    -> authorized: check risk
        -> READ: automatic
        -> WRITE / DESTRUCTIVE: approval / stronger policy
```

The LLM must never be trusted to provide an `approved=True` type of control flag.

## Milestone 18 — MCP foundation

Completed as a learning/demo foundation.

Current learning/demo files include:

- `mcp_client.py`
- `mcp_servers/research_server.py`

Current MCP demo concepts:
- MCP server
- MCP tool
- MCP resource
- MCP client calling an MCP tool

Important: MCP is **not yet fully integrated into the main Researcher/runtime**. Deeper MCP integration is intentionally reserved for the production-architecture phase.

## Milestone 19 — Security / guardrails

Completed.

Topics:
- allowlists
- risk levels
- approval policy
- external content treated as untrusted data
- runtime-enforced policy rather than LLM-enforced policy

## Milestone 20 — Observability basics

Completed at the intentionally simplified level.

Current approach:
- trace id
- simple logs
- timestamps / elapsed time

Advanced tracing with full spans, token accounting, handoff traces, etc. is intentionally postponed until production refactoring.

## Milestone 21 — Agent evals / testing

Completed conceptually and mostly implemented.

Covered:
- deterministic security tests
- real LLM tool-selection eval
- mocked Researcher happy path
- mocked tool-failure tests
- max-step stopping test
- Critic groundedness eval
- Writer revision eval
- end-to-end workflow test
- regression-testing strategy

Important debugging lesson:

A real Researcher LLM run previously exposed a bad tool-result message field (`tool_id` instead of `tool_call_id`). The implementation was corrected.

Current tests include:

- `tests/test_async_executor.py`
- `tests/test_critic.py`
- `tests/test_parallel_tools.py`
- `tests/test_researcher.py`
- `tests/test_researcher_mocked.py`
- `tests/test_security.py`
- `tests/test_workflow.py`
- `tests/test_writer.py`

## Milestone 22 — Async + parallel execution

**CURRENT MILESTONE — IN PROGRESS**

Goal:
- understand Python `asyncio`
- understand `async` / `await`
- understand sequential vs concurrent awaits
- understand `asyncio.gather()`
- adapt blocking tool functions with `asyncio.to_thread()`
- support async-aware tool execution
- enforce runtime concurrency policy
- execute multiple safe tool calls concurrently
- add concurrency limits
- add timeouts
- handle partial failures
- test actual concurrency

What has already been learned/implemented:

1. Python async/await mental model.
2. `asyncio.run()`.
3. Sequential vs concurrent `await`.
4. `asyncio.gather()` basics.
5. Why synchronous blocking tools cannot simply be dropped into concurrent execution.
6. Async wrappers for web search and arXiv using `asyncio.to_thread()`.
7. `Tool.is_async` metadata using `inspect.iscoroutinefunction`.
8. Async executor `execute_prepared_tool_async()`.
9. Unit tests for sync and async tools.
10. A test showing real web + arXiv async wrappers can be gathered.
11. Security policy for concurrency:

```python
can_run_in_parallel(risk_level)
```

Current policy is intentionally conservative: only `READ` tools are parallel-safe.

12. Added `action_can_run_in_parallel()` to the runtime executor.
13. Converted `run_researcher_agent()` to async.
14. Converted the coordinator path so it awaits the Researcher.
15. Restructured Researcher execution into:

```text
prepare all
    -> classify
        -> parallel actions
        -> sequential actions
    -> execute
    -> store results
```

16. Current Researcher uses `asyncio.gather()` for the parallel-safe action group.

### CURRENT IMPORTANT STATE

`agents/researcher.py` currently contains the parallel execution architecture. However, **M22 is not considered fully complete until the complete test suite has been run and all resulting failures are fixed**.

The last known immediate action before this handoff was to run:

```bash
pytest -q
```

Then fix the failures caused by the async Researcher/coordinator changes.

### Important implementation nuance to revisit during M22

The registered `web_search_tool` and `arxiv_search_tool` currently point at the synchronous tool functions, while async wrappers also exist in their modules. The project must eventually resolve this deliberately so that the runtime's normal Tool registry can execute the appropriate async implementation without confusing the LLM-visible tool name/schema.

Do not skip understanding this distinction:

```text
LLM-visible tool name/schema
        !=
internal execution implementation
```

### M22 remaining work

Do these in order:

1. Run `pytest -q`.
2. Fix any async caller/test failures.
3. Add a deterministic test proving two slow async tools actually overlap in execution time.
4. Add a concurrency limit so an LLM cannot create an unbounded number of simultaneous tasks.
5. Add per-tool timeout handling.
6. Decide and implement partial-failure behavior for `asyncio.gather()`.
7. Verify security behavior is preserved: allowlist, Pydantic validation, approval policy, and READ-only parallel policy.
8. Verify evidence/tool-message ordering and identifiers remain correct.
9. Verify the complete workflow still works.
10. Run the complete test suite.
11. Only when all of the above are complete, mark M22 complete and perform a repo review.

---

# 4. Future milestones after M22

## Milestone 23 — Context management

Topics:
- context window limits
- message growth
- evidence growth
- pruning
- summarization
- evidence compression
- token budgets
- what should remain in model context
- avoiding context explosion

Key question:

> What information is necessary for the next model step, and what can safely be removed or compressed?

## Milestone 24 — Caching + performance

Topics:
- duplicate-call prevention
- tool-result cache
- search cache
- cache keys
- TTL
- freshness / invalidation
- reducing latency
- reducing token usage

## Milestone 25 — Production architecture refactor

Topics:
- clean package structure
- configuration boundaries
- dependency boundaries / interfaces
- error architecture
- remove temporary/tutorial code
- proper MCP client/adapter architecture
- MCP tool discovery and routing
- MCP security integration
- advanced observability / tracing
- final cleanup of unused imports, dead code, and old demo artifacts

Likely cleanup candidates to review here (do not delete early just because they look unused):
- `tools/temperature.py`
- unused global `tool_schemas` in `tools/__init__.py` if no longer referenced
- unused imports in `agents/researcher.py`
- unused import(s) in `runtime/tool_executor.py`
- MCP demo files after deciding which parts become production components

Also review known runtime issues before calling the refactor complete, including the `tool is None` path in `prepare_tool_call()`.

## Milestone 26 — Final agentic research system

Final architecture target:

```text
User
  -> Coordinator
      -> Planner
      -> Researcher
          -> native tools
          -> MCP tools
      -> Evidence
      -> Writer
      -> Critic
      -> Revision
      -> Security / Approval
      -> Final answer
```

This milestone assembles all previous concepts:
- state
- reflection
- planning
- tools
- MCP
- security
- human approval
- async execution
- context management
- caching
- observability
- evaluation

## Milestone 27 — Framework comparison

Compare our implementation with OpenAI Agents SDK.

Concept mapping to study:

```text
Our agent loop           -> Agents SDK Runner
Our Tool                 -> SDK tool
Our Coordinator/handoffs -> SDK agent + handoffs
Our security             -> SDK guardrails / policy mechanisms
Our tracing              -> SDK tracing
Our state                -> SDK context/session concepts
```

The goal is to understand **what the framework abstracts**, not to blindly replace our implementation.

---

# 5. Current repository architecture

High-level repository structure currently includes:

```text
agents/
  action_agent.py
  critic.py
  researcher.py
  writer.py

mcp_servers/
  research_server.py

models/
  actions.py
  research.py

runtime/
  tool_executor.py

agents / coordinator / planner / state / observability / approval

mcp_client.py
security.py
tool.py
llm.py

models + tests + tools

tools/
  arxiv_search.py
  email.py
  temperature.py
  web_search.py
```

Important implementation responsibilities:

- `coordinator.py` — orchestration of Planner -> Researcher -> Writer -> Critic loop.
- `agents/researcher.py` — research agent, tool selection, tool-result loop, evidence collection.
- `runtime/tool_executor.py` — parsing, Pydantic validation, allowlist checks, approval checks, sync/async execution.
- `security.py` — risk policy, allowlist, approval policy, parallel-execution policy.
- `tool.py` — reusable Tool abstraction and tool metadata.
- `tools/` — concrete tools.
- `state.py` — workflow state.
- `planner.py` — structured research planning.
- `observability.py` — simplified logging/tracing foundation.
- `mcp_client.py` / `mcp_servers/` — MCP learning/demo foundation.
- `tests/` — deterministic and agent behavior tests.

---

# 6. Important design decisions already made

### Custom runtime first

We intentionally build orchestration ourselves first to learn the fundamentals.

### Runtime controls security

The LLM can propose a tool call. The runtime decides whether it is allowed and whether it needs human approval.

### External content is untrusted

Search results, MCP resources, emails, and other external data are data, not instructions.

### Parallelism is a runtime policy

The LLM does not decide which actions are safe to parallelize.

### Start conservative

Only `READ` tools are currently parallel-safe.

### Advanced infrastructure comes later

Full tracing, production MCP integration, robust context management, and extensive cleanup belong to later milestones instead of complicating the early learning stages.

---

# 7. Known lessons / pitfalls

1. A correct tool call can still produce poor evidence.
2. LLM tool-call message fields must match the API contract exactly; `tool_call_id` matters.
3. `async def` changes the calling convention; callers must `await` it.
4. `asyncio.gather()` gives concurrency, but only when the supplied operations are genuinely asynchronous/non-blocking.
5. `asyncio.to_thread()` is a bridge for blocking synchronous functions.
6. Do not parallelize write/destructive operations merely for speed.
7. Prepare and validate actions before deciding concurrency.
8. Do not classify an accumulating list inside the same loop that is building it, or earlier actions can be classified multiple times.
9. Do not create evidence records before actual tool execution results exist.
10. Keep LLM tool schema concerns separate from runtime security and execution policy.

---

# 8. Exact handoff instructions for a new ChatGPT chat

When starting a new chat for this project, use this sequence:

```text
1. Read AGENTIC_AI_LEARNING_ROADMAP.md.
2. Read CURRENT STATE.
3. Read NEXT ACTION.
4. Continue from that exact step.
5. Do not restart old milestones.
6. Do not jump ahead multiple steps.
7. Teach one small change at a time.
8. Check GitHub/repository state when a milestone is completed or when the current code state is unclear.
```

Suggested first message in a new chat:

> We are continuing my Agentic AI Engineering learning project. Read `AGENTIC_AI_LEARNING_ROADMAP.md` in the repository first. Use it as the handoff/source of truth, check the current code only as needed, and continue from the exact `CURRENT STATE` and `NEXT ACTION`. Teach one small step at a time.

---

# 9. CURRENT STATE

**Current milestone:** M22 — Async + Parallel Execution

**Current implementation stage:**

- Researcher is async.
- Coordinator awaits the Researcher.
- Tool calls are prepared first.
- Prepared actions are classified into parallel-safe and sequential groups.
- Parallel-safe actions are executed with `asyncio.gather()`.
- Results are converted back into evidence and tool messages.

**M22 completion status:** NOT YET COMPLETE.

We have not yet declared M22 complete because the full test suite still needs to be run after the async Researcher/coordinator changes, and the remaining reliability/performance work has not yet been completed.

---

# 10. NEXT ACTION

Start here in the next chat:

```bash
pytest -q
```

Then inspect the failures and fix them **one at a time**.

Do not start M23 until M22 is explicitly marked complete in this file.

After M22 is completed, update this document with:

- final M22 status
- tests added
- any design decisions made
- exact starting point for M23

---

# 11. Rule for maintaining this document

At the end of every completed milestone, update this file with:

```text
CURRENT MILESTONE
STATUS
WHAT WE LEARNED
WHAT WE IMPLEMENTED
TESTS / VERIFICATION
KNOWN ISSUES
NEXT MILESTONE
NEXT FIRST STEP
```

This file is intended to prevent loss of learning context across ChatGPT conversations.