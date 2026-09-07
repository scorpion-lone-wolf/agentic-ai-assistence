# Agentic AI Assistant

A Python-based **multi-agent AI research system** that demonstrates how an LLM can break a question into smaller research tasks, use tools to gather evidence, write an answer, and then critique and revise that answer.

The project is primarily an exploration of **agentic workflows**, including planning, tool calling, parallel tool execution, validation, security checks, human approval, and iterative reflection.

> **Project status:** This is an experimental/learning project. Some components are implemented as building blocks and are not yet wired into a complete production-ready assistant.

---

## What does this project do?

Suppose you ask:

> "Find recent research on reflection in AI agents and compare academic techniques with current practical implementations."

Instead of asking one LLM to do everything, the system separates the work into specialized stages:

```text
                    User Question
                          |
                          v
                  +---------------+
                  |    Planner    |
                  +---------------+
                          |
                   Research Plan
                          |
                          v
                  +---------------+
                  |   Researcher  |
                  +---------------+
                          |
                  Search Web / arXiv
                          |
                          v
                       Evidence
                          |
                          v
                  +---------------+
                  |     Writer    |
                  +---------------+
                          |
                       Draft
                          |
                          v
                  +---------------+
                  |     Critic    |
                  +---------------+
                     /          \
              needs revision     pass
                   |               |
                   v               v
                Writer         Final Answer
                   |
                   +-----> Critic
```

The important idea is the **feedback loop**: the writer does not simply generate an answer once. The critic checks the draft against the collected evidence and can send it back to the writer for revision.

---

## The four main agents

### 1. Planner

**File:** `planner.py`

The Planner converts the user's broad question into a structured research plan.

It decides:

- What needs to be researched
- Which tool should be used
- What query should be sent to that tool
- Why that research step is necessary

The plan is validated with Pydantic models before it is used.

Currently supported research tools in the planner are:

- `arxiv_search` — academic papers and scholarly research
- `web_search` — current/general web information

---

### 2. Researcher

**File:** `agents/researcher.py`

The Researcher executes the research plan and collects evidence.

It can:

1. Ask the LLM what tool calls are needed.
2. Parse and validate those tool calls.
3. Check whether the requested tool is allowed.
4. Separate parallel-safe work from sequential work.
5. Execute read-only tools concurrently when possible.
6. Feed tool results back to the LLM.
7. Continue researching until enough evidence has been collected or the research-step limit is reached.

The current researcher allows:

```text
arxiv_search
web_search
```

A maximum of **5 research iterations** is configured.

---

### 3. Writer

**File:** `agents/writer.py`

The Writer takes:

- The original question
- Collected evidence
- The current answer
- Critic feedback

and produces an answer grounded in the available evidence.

The Writer is explicitly instructed not to invent unsupported facts.

---

### 4. Critic

**File:** `agents/critic.py`

The Critic acts as a quality-control layer.

It checks whether:

- The answer actually addresses the user's question
- Claims are supported by the collected evidence
- Evidence has been represented correctly
- Current/latest claims have appropriate current evidence

It returns one of two statuses:

```text
pass
needs_revision
```

If revision is required, its feedback is passed back to the Writer.

The workflow allows up to **5 critique/revision iterations**.

---

## Why multiple agents?

The project demonstrates an important pattern in agentic AI:

> **Different agents can have different responsibilities instead of relying on one large prompt to do everything.**

For example:

| Component | Responsibility |
|---|---|
| Planner | Decide what research should happen |
| Researcher | Gather evidence |
| Writer | Turn evidence into an answer |
| Critic | Check the answer and request revisions |
| Coordinator | Control the overall workflow |
| Tool Executor | Safely prepare and execute tools |
| Security | Enforce tool permissions and risk rules |
| Observability | Track workflow execution |

This separation makes the workflow easier to reason about and provides clear places to add new capabilities.

---

## Tool execution architecture

Tools are registered centrally in `tools/__init__.py`.

The current registry includes:

- `arxiv_search`
- `web_search`
- `temperature`
- `email`

However, **not every tool is currently enabled for every agent**. For example, the Researcher is intentionally restricted to the two research tools, and the current Action Agent configuration is still limited in what it can actually invoke.

This distinction is important: a tool being registered does not automatically mean that every agent is allowed to execute it.

---

## Tool safety model

**Files:** `security.py`, `runtime/tool_executor.py`, `approval.py`

Tools have a risk classification:

```text
READ
WRITE
DESTRUCTIVE
```

The security layer uses this classification to decide whether an action can be executed automatically.

Current policy:

| Risk | Automatic execution | Human approval | Parallel execution |
|---|---:|---:|---:|
| READ | Yes | No | Yes |
| WRITE | No | Yes | No |
| DESTRUCTIVE | No | Yes | No |

Before execution, tool calls go through a preparation stage where arguments are parsed and validated against the tool's Pydantic argument model.

The runtime also limits concurrent tool execution to **3 tools at a time**.

This gives the project a useful architecture for building safer tool-using agents instead of allowing the LLM to directly execute arbitrary functions.

---

## MCP support

The repository also contains MCP-related components:

```text
mcp_client.py
mcp_servers/
    research_server.py
```

The research server provides a foundation for exposing research capabilities through the **Model Context Protocol (MCP)**.

The Researcher also treats external MCP/tool data as untrusted data and is instructed not to follow instructions embedded inside retrieved external content. This is an important defense against prompt-injection-style attacks in tool-using systems.

---

## Project structure

```text
agentic-ai-assistence/
│
├── agents/
│   ├── action_agent.py       # Agent for performing user-requested actions
│   ├── critic.py             # Evaluates generated answers
│   ├── researcher.py         # Gathers evidence using research tools
│   └── writer.py             # Generates and revises answers
│
├── mcp_servers/
│   └── research_server.py    # MCP research server
│
├── models/
│   ├── actions.py            # Action-related data models
│   └── research.py           # Research/evidence data models
│
├── runtime/
│   └── tool_executor.py      # Tool validation, execution and concurrency
│
├── tools/
│   ├── arxiv_search.py       # arXiv search tool
│   ├── email.py              # Email tool
│   ├── temperature.py        # Temperature tool
│   ├── web_search.py         # Web search tool
│   └── __init__.py           # Tool registry
│
├── approval.py                # Human approval mechanism
├── coordinator.py             # Orchestrates the multi-agent workflow
├── llm.py                     # LLM integration
├── main.py                    # Example entry point
├── observability.py           # Basic tracing/logging helpers
├── planner.py                 # Research planning
├── security.py                # Risk and permission rules
├── state.py                   # Shared workflow state
├── tool.py                    # Tool abstraction
├── requirements.txt           # Python dependencies
└── tests/                     # Automated tests
```

---

## End-to-end workflow

The main orchestration happens in `coordinator.py`.

Conceptually, it performs:

```python
question
   ↓
Planner
   ↓
Research Plan
   ↓
Researcher
   ↓
Evidence
   ↓
Writer
   ↓
Draft Answer
   ↓
Critic
   ↓
 ┌─────────────────────┐
 │                     │
pass              needs_revision
 │                     │
 ↓                     ↓
final answer        Writer
                       ↓
                     Critic
```

The coordinator stores the workflow state in `AgentState`, including the question, research plan, evidence, current answer, and reflection count.

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/scorpion-lone-wolf/agentic-ai-assistence.git
cd agentic-ai-assistence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your LLM/tool credentials

The project uses environment-based configuration for external services. Check `llm.py` and the individual tool implementations to see which environment variables are required for the providers you want to use.

Do **not** commit API keys or other secrets to the repository.

### 5. Run the example

```bash
python main.py
```

`main.py` contains a simple example invocation of the multi-agent workflow.

For your own question, replace the placeholder passed to:

```python
run_multi_agent_workflow("your question")
```

with the question you want the system to research.

---

## Running tests

The repository contains tests covering several important parts of the system, including:

- Async tool execution
- Parallel tool execution
- Researcher behavior
- Critic behavior
- Writer behavior
- Security rules
- Workflow behavior

Run the test suite with:

```bash
pytest
```

---

## Key agentic AI concepts demonstrated

This repository is useful as a practical reference for learning several concepts at once:

### Planning

The LLM creates a structured plan before research begins.

### Tool calling

Agents can request tools instead of generating everything from their own knowledge.

### Structured outputs

Pydantic models are used to validate plans, evidence, and critique results.

### Tool permissions

Agents are restricted to explicitly allowed tools.

### Parallel execution

Independent read-only tools can be executed concurrently.

### Human-in-the-loop

Higher-risk actions can require explicit human approval.

### Reflection

A Critic evaluates the Writer's output and can trigger another writing pass.

### Observability

The coordinator creates a trace ID and records workflow stages and execution timing.

### Prompt-injection awareness

External tool/MCP output is treated as untrusted data rather than as instructions for the agent.

---

## Current limitations

This repository is a learning/experimental implementation rather than a finished production assistant.

Some notable areas that can be improved:

- The Action Agent and registered action tools are not yet fully wired together.
- The current example in `main.py` is intentionally minimal.
- Tool configuration depends on the external services being configured correctly.
- The workflow uses fixed iteration limits rather than dynamic budget management.
- Error handling and observability can be expanded for production workloads.
- Persistent memory/state is not yet a full subsystem.
- More comprehensive integration tests would be useful for the complete tool/MCP workflow.

These limitations are also useful extension points if you want to turn the project into a more complete agent framework.

---

## Good next steps for extending the project

If you want to evolve this into a more complete agentic assistant, a sensible progression would be:

1. **Fix and complete the Action Agent tool allow-list** so action tools such as email can actually be used through that agent.
2. Add a clear **CLI/API interface** instead of keeping the question inside `main.py`.
3. Add **persistent conversation state and memory**.
4. Add stronger **tool authorization policies** per user/agent.
5. Add **retry and timeout policies** per tool.
6. Add richer **tracing and metrics** for LLM calls and tools.
7. Add **citation/source tracking** from research tools into the final answer.
8. Add an explicit **workflow graph/state machine** as the number of agents grows.
9. Add integration tests for the complete Planner → Researcher → Writer → Critic loop.
10. Add a user-facing API or web UI.

---

## Learning goal

The main value of this repository is not a single chatbot feature. It is the architecture.

It demonstrates how to move from:

```text
"Ask an LLM a question"
```

toward:

```text
"Build a controlled system where multiple specialized agents
plan, research, use tools, validate results, write, critique,
and revise an answer."
```

That architecture is the core idea behind many modern **agentic AI systems**.

---

## License

Add the project's license here when one is defined for the repository.
