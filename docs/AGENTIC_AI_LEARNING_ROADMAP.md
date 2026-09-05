# Agentic AI Engineering Learning Roadmap

## Purpose

This is the **stable curriculum and project-goal document** for the Agentic AI Engineering learning project.

**Important rule:** This file is the long-term roadmap. It is **not a session handoff/status file** and should not be rewritten at the end of a ChatGPT session. Session progress belongs in `AGENTIC_AI_LEARNING_STATUS.md`.

When a new chat starts, read this roadmap for the overall goal and curriculum, then read `AGENTIC_AI_LEARNING_STATUS.md` for the current progress and next step.

Repository: `https://github.com/scorpion-lone-wolf/agentic-ai-assistence`
Default branch: `master`

---

# 1. Overall learning goal

The goal is not merely to build a working chatbot. The goal is to understand how agentic AI systems work by building the important runtime/orchestration pieces ourselves first.

We are learning from a Node.js developer background, using Python for the agentic AI implementation.

Core goals:

- Learn Python concepts needed for agentic AI engineering.
- Use Gemini through Google AI Studio using an OpenAI-compatible endpoint.
- Use the OpenAI Python SDK for model calls.
- Build our **own agent runtime/orchestration first** instead of starting with OpenAI Agents SDK.
- Understand tool calling deeply.
- Understand agent loops, planning, state, reflection, multi-agent workflows, security, human approval, MCP, async execution, context management, caching, observability, evaluation, and production architecture.
- Only after understanding the internals, compare our custom runtime with OpenAI Agents SDK and understand what a framework abstracts away.

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

# 2. Teaching method

The learner wants each milestone taught slowly and incrementally.

For each new step:

1. Explain the **problem** we are solving.
2. Give a simple **mental model**.
3. Make **one small code change**.
4. Explain why the code exists and what breaks without it.
5. Run/test it.
6. Only then move to the next small change.

Do not dump a large implementation without mapping it to the exact file and section.

Do not silently redesign the architecture just because a shorter implementation exists. The purpose is to learn the underlying concepts.

Do not start the project by relying on a high-level agent framework. The custom runtime comes first.

---

# 3. Curriculum

## Milestone 1 — Project setup

Topics:
- Python project structure
- dependencies
- environment setup
- repository organization

## Milestone 2 — Raw Gemini / OpenAI-compatible model call

Topics:
- Gemini endpoint
- OpenAI Python SDK
- messages
- model responses

## Milestone 3 — Manual tool calling

Topics:
- function/tool schemas
- model proposes a tool call
- application executes the function
- result is returned to the model

## Milestone 4 — Tool registry + generic agent loop

Topics:
- reusable tool registry
- generic tool execution
- model -> tool -> result loop

## Milestone 5 — Web search

Topics:
- external web retrieval as an agent tool
- current/general information retrieval

## Milestone 6 — arXiv search

Topics:
- scholarly retrieval
- choosing tools based on research intent

## Milestone 7 — Hardened agent loop

Topics:
- maximum loop steps
- stopping runaway tool loops

## Milestone 8 — Pydantic validation

Topics:
- validate LLM-supplied tool arguments
- reject malformed/unexpected arguments
- keep tool inputs structured

## Milestone 9 — LLM provider retries

Topics:
- transient model failures
- retry behavior

## Milestone 10 — Reusable Tool abstraction

Topics:
- common Tool object
- tool metadata
- schemas
- risk metadata
- async capability metadata

## Milestone 11 — Reflection fundamentals

Topics:
- model-generated critique
- reflection as a separate reasoning stage

## Milestone 12 — Iterative reflection + structured critic

Topics:
- critic result structure
- repeated critique/revision
- stopping after a maximum critique count

## Milestone 13 — Grounded research + reflection

Topics:
- evidence-backed writing
- distinction between evidence and model-generated claims
- reflection over retrieved evidence

Key lesson to preserve:

> Correct tool selection does not guarantee relevant evidence.

Evaluation must measure evidence quality, not only whether a tool was called.

## Milestone 14 — Structured planning

Topics:
- planner agent/function
- structured `ResearchPlan`
- research steps and reasons
- passing the plan into the Researcher

## Milestone 15 — State / memory

Topics:
- `AgentState`
- preserving question, plan, evidence, current answer, and reflection progress

## Milestone 16 — Multi-agent workflow

Topics:
- Coordinator
- Planner
- Researcher
- Writer
- Critic
- handoffs between agents

Target orchestration:

```text
Planner -> Researcher -> Writer -> Critic -> Revision
```

## Milestone 17 — Human-in-the-loop + side-effect tools

Topics:
- risk levels
- human approval
- side-effecting tools
- separating authorization from LLM intent

Security model:

```text
LLM proposes action
    -> runtime validates
    -> runtime checks agent allowlist
    -> unauthorized: BLOCK
    -> authorized: check risk
        -> READ: automatic
        -> WRITE / DESTRUCTIVE: approval / stronger policy
```

The LLM must never control an approval flag such as `approved=True` as a security decision.

## Milestone 18 — MCP foundation

Topics:
- MCP server
- MCP client
- MCP tool
- MCP resource
- calling an MCP tool from a client

MCP should first be learned as a foundation, then integrated properly later.

## Milestone 19 — Security / guardrails

Topics:
- allowlists
- risk levels
- approval policy
- external content treated as untrusted data
- runtime-enforced policy rather than LLM-enforced policy

## Milestone 20 — Observability basics

Topics:
- trace ids
- simple logs
- timestamps
- elapsed time

Advanced tracing is intentionally postponed until production refactoring so the basic concepts remain understandable.

## Milestone 21 — Agent evals / testing

Topics:
- deterministic security tests
- tool-selection evals
- mocked agent tests
- tool-failure tests
- stopping-condition tests
- critic quality tests
- writer revision tests
- end-to-end workflow tests
- regression-testing strategy

The goal is to learn that an agent can be executable yet still produce poor behavior or poor evidence.

## Milestone 22 — Async + parallel execution

Topics:
- Python `asyncio`
- `async` / `await`
- sequential vs concurrent awaits
- `asyncio.gather()`
- `asyncio.to_thread()` for blocking functions
- async-aware tool execution
- concurrency policy
- safe parallel execution
- concurrency limits
- timeouts
- partial-failure handling
- testing actual concurrency

Important design principle:

```text
LLM-visible tool schema
        !=
internal execution implementation
```

Parallelism is a runtime policy, not an LLM decision.

Start conservatively: READ-only tools are parallel-safe.

## Milestone 23 — Context management

Topics:
- context window limits
- message growth
- evidence growth
- pruning
- summarization
- evidence compression
- token budgets
- deciding what remains in model context
- preventing context explosion

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

This is the stage for deliberately resolving temporary learning/demo decisions and consolidating the system into a production-oriented architecture.

## Milestone 26 — Final agentic research system

Assemble the complete architecture:

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

Concepts combined:
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

Compare the custom runtime with OpenAI Agents SDK.

Concept mapping to study:

```text
Our agent loop            -> Agents SDK Runner
Our Tool                  -> SDK tool
Our Coordinator/handoffs  -> SDK agent + handoffs
Our security              -> SDK guardrails / policy mechanisms
Our tracing               -> SDK tracing
Our state                 -> SDK context/session concepts
```

The objective is understanding what the framework abstracts, not blindly replacing the implementation.

---

# 4. Architecture principles

## Custom runtime first

Build core orchestration ourselves so the internal mechanics are understood before using a framework.

## Runtime controls security

The LLM can propose an action. The runtime decides whether it is authorized and whether it requires approval.

## External content is untrusted

Search results, MCP resources, emails, and other external data are data, not instructions.

## Parallelism is a runtime policy

The model may propose multiple tool calls, but the runtime decides which can safely run concurrently.

## Start conservative

Only operations explicitly classified as safe should be parallelized. READ-only is the initial policy.

## Infrastructure is introduced progressively

Do not introduce production-level infrastructure before the underlying concept has been learned in a simpler form.

---

# 5. Important lessons we expect to preserve

1. Correct tool selection does not guarantee useful evidence.
2. Tool-call message fields must match the provider/API contract exactly.
3. `async def` changes the calling convention; callers must `await` it.
4. `asyncio.gather()` provides concurrency only when the operations are genuinely non-blocking or moved off the event loop.
5. `asyncio.to_thread()` is a bridge for blocking synchronous work.
6. Do not parallelize write/destructive operations merely for speed.
7. Validate and authorize actions before executing them.
8. Do not classify an accumulating list inside the same loop that is building it.
9. Do not create evidence records before tool execution results exist.
10. Keep LLM-visible schemas separate from runtime security and execution policy.

---

# 6. Stable scope of the project

The roadmap intentionally covers the complete path from a raw model call to a multi-agent, tool-using, secure, observable, evaluated, async, context-aware, cached, MCP-enabled research system, followed by a framework comparison.

The **roadmap is stable**. Changes to what has been completed, what is currently being implemented, bugs discovered during a session, and the next action belong in `AGENTIC_AI_LEARNING_STATUS.md`.
