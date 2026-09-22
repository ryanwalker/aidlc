# Agent Harness — High-Level Spec

Tech-agnostic. This describes the capability areas a harness needs, not an implementation — no framework, language, or SDK is assumed. Derived from the research in this repo (`00-master-summary.html`, `02-agent-harness-engineering.html`, `questions.html`).

Working definition: **Agent = Model + Harness**. The model reasons; the harness is everything else — and is where most of the behavior actually gets decided. Each component below has a **What** (the capability needed and why) and a **How** (the general pattern for providing it, still at the conceptual level — not a technical design).

## Components

### 1. A way for the agent to get context

**What:** The model only knows what's in its context window on a given turn. The harness needs a mechanism to assemble that window from the right sources — project docs, retrieved knowledge, prior session state, examples — and decide what's loaded every turn versus fetched on demand. Get this wrong and the agent is either blind (missing what it needs) or drowning (context rot from loading everything, always).

**How:** Split context into static (always loaded — instructions, guardrails, core tool definitions) and dynamic (loaded on demand — retrieved knowledge, situational examples, session history). Use progressive disclosure: keep a lightweight index always present, and pull full detail in only once the task at hand matches it. Large or open-ended knowledge bases are retrieved (query → top-relevant chunks) rather than loaded wholesale.

### 2. Instructions the agent always operates under

**What:** A small, always-loaded doc — rules, conventions, constraints, operational boundaries — that every turn is built on top of. This is the static floor of context: cheap to load, expensive to bloat.

**How:** Kept deliberately short. Each rule should trace back to a specific past failure or an external constraint — no speculative or orphan rules. Treated as reviewed, versioned material rather than something edited freely mid-task.

### 3. Tools that connect the model to the world

**What:** Functions, APIs, or external services the agent can invoke. Without tools the agent can only talk; tools are what let it act — read files, run code, call services, query data.

**How:** Each tool is registered with a name, an input/output shape, and prose describing when and how to use it — the description is what the model actually reasons over when deciding whether to call it. Tools can be all registered upfront or discovered as needed; either way the model needs enough information to choose correctly, not just execute correctly.

### 4. A bounded execution environment

**What:** A defined space of what the agent can reach and what it can't — filesystem scope, network access, credentials, blast radius. This is what turns "the agent could do anything" into "the agent can do this specific set of things," and it's the layer that makes destructive mistakes recoverable instead of catastrophic.

**How:** An explicit allow-list (or deny-list) of what's reachable, enforced at a boundary the agent cannot talk its way around — not a prompt instruction asking it to stay in bounds, but something that fails the action if it's out of bounds.

### 5. Orchestration logic

**What:** Something has to decide who runs next, with which model, and how work hands off between them when more than one agent (or one agent across multiple stages) is involved. Even a single-agent harness needs a minimal version of this: the loop that decides "keep going or stop."

**How:** Favor deterministic control flow over letting one model decide everything — a fixed sequence or graph, with model judgment only at the individual steps. Start with rule-based model routing (role → model, by task difficulty) before reaching for adaptive routing. When work spans multiple agents, hand off through a shared artifact (a plan, a spec, a result) rather than raw conversation, and keep any spawned sub-agent's work scoped and isolated, returning only a result rather than its full working history.

### 6. Guardrails enforced in code, not just in prompts

**What:** Deterministic checks that catch what the model is asked not to do but might do anyway under pressure. A written rule is a request; a guardrail is a wall. Reserve this for the things that are unacceptable to get wrong.

**How:** Wired at fixed points in the agent's action loop — before it takes an action, after it changes something, before anything irreversible — as code that runs regardless of what the model decided, not as additional prompt text.

See [[../proposals/0001-review-swarm-and-risk-gate.md]] for a concrete
instance: a deterministic, short-circuiting risk gate (PR state → blast
radius → diff size → LLM check) gating auto-approval of PRs.

### 7. Memory across turns and sessions

**What:** State that persists beyond a single context window — what the agent has already tried, decisions already made, facts already established — so work doesn't restart from zero every time the window fills or a new session begins.

**How:** Short-term memory lives in the running session (a log of what's happened so far, summarized or trimmed as it grows); long-term memory lives in a persistent store outside any one session, indexed lightly and recalled on demand rather than replayed in full every time.

### 8. A way to verify output, separate from producing it

**What:** Checks that confirm the agent actually succeeded, run by something other than the agent that did the work. Self-review by the same agent that generated the output doesn't catch much; the harness needs an independent check built in, not bolted on after.

**How:** Tests cover the deterministic parts (given this input, that exact output); evals cover the non-deterministic parts (did it take a reasonable path, choose the right tools, meet a quality bar) via a dataset of cases, a task run, and a scorer. Prefer scorers that are code, not a model's opinion, wherever a deterministic check is possible; reserve a model-as-judge (with a written rubric) for genuinely subjective calls. Whoever authors the checks should be separate from whoever's work is being checked.

See [[../proposals/0001-review-swarm-and-risk-gate.md]] for a concrete
instance: an independent multi-agent review swarm (distinct lens + model per
reviewer) checking PRs the authoring agent didn't review itself.

### 9. Observability into what the agent actually did

**What:** Visibility covering not just the final output but the path taken to get there. Without this, a harness can silently drift — quietly getting worse or more expensive — with no signal until something breaks downstream.

**How:** Capture the trajectory (which tools were called, in what order, on what reasoning) alongside the result, plus cost and latency per run. Aggregate over time so a regression shows up as a trend, not just a single bad run someone happens to notice.

## Notes

- Items 1–4 are mostly about what the agent has access to; 5–7 are about how work flows and persists; 8–9 are about knowing whether any of it is actually working.
- None of these are one-time builds — each is expected to evolve as failures surface (the "ratchet principle": every mistake becomes a permanent rule, hook, or gate rather than a one-off fix).
- The **How** sections here are still conceptual patterns, not a technical design — they intentionally stop short of naming a stack, framework, or protocol. `questions.html` goes one level deeper on four of these (context loading, orchestration hand-offs, test-gaming prevention, eval setup) and is worth reading before turning any item into an actual technical design.
