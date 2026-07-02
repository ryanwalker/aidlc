# Adoption Plan — Standing Up the AI SDLC on a Greenfield Project

Companion to `harness-spec.md`. That doc defines *what a harness is* (9 components, tech-agnostic). This doc is *how we adopt it* — the concrete moves to build the harness alongside a new codebase from commit one.

This is methodology and lives here, next to the spec. The **scaffolding it produces** (`AGENTS.md`, `.claude/`, `evals/`, CI) lives in the greenfield project repo, committed with the code — not here.

## The reframe

- **Demo vs. production is a verification-rigor spectrum, not a tooling choice.** The same coding agent sits at either end; position is set by how rigorously output is verified. Adoption = moving rightward on that spectrum (no evals → evals + CI gates → upfront specs + eval suites + structured context).
- **The Ratchet Principle is the engine.** Every agent failure becomes a permanent rule, hook, or eval case — never a one-off manual fix. This is how the harness grows without a big upfront project. On greenfield it starts empty and fills from the first real failure onward.
- **Greenfield advantage:** every harness component gets built at the moment it's cheapest — before there's any code to retrofit it around. No context archaeology, no untangling legacy test-coupling.

## The steps

Not a timeline — these are the moves. Some run in parallel; the ratchet (step 4) is continuous.

### 1. Commit the harness floor before feature code
A lean `AGENTS.md` (stack, conventions, build/test commands, guardrails) + one enforcing hook (work isn't "done" until tests pass) + a green CI. The scaffolding predates the product. Writes each convention into `AGENTS.md` the moment it's decided, not reconstructed later.

### 2. Separate generation from evaluation, enforced in code
The requirement: whatever produces code cannot quietly optimize against the checks it's graded on. Mechanism is open — a dedicated evaluator step, independently-authored tests, a CI gate, or a scoped subagent. (The `harness/` `implementer` subagent is an *experiment* demonstrating the principle, not the prescribed mechanism.) Caveat from `questions.html`: separation alone just moves gaming up a level — pair it with independently-authored tests and code scorers over model-opinion scorers.

### 3. Seed evals from the spec, not from bugs
Greenfield has no incident history yet, so acceptance criteria are the source. Turn each feature's "done" definition into eval cases *before* building it — dataset + task + scorer, code scorers first, model-judge only for genuinely subjective calls. A `for`-loop with asserts is a legitimate eval; graduate to Braintrust/LangSmith when scores need tracking across runs and become a team asset.

### 4. Turn on the ratchet immediately
From the first failure, the fix is a new rule/hook/eval case — so the harness hardens as the codebase grows, never after. Bug-derived eval cases accumulate from here on and supplement the spec-derived ones.

### 5. Hold context discipline from commit one
Default everything to dynamic (skills / RAG / on-demand); promote to always-loaded `AGENTS.md` only when it earns its per-turn cost. Easy to hold when the file starts empty. Treat the static/dynamic boundary as architecture and version it with the code.

### 6. Add trajectory evals + observability when there's volume to observe
Tool-path and step-budget checks wired into a hook; aggregate cost/latency so drift shows up as a trend, not a single noticed bad run. Later — once there's enough traffic to make it meaningful.

## Where things live

| Artifact | Home |
|---|---|
| This adoption methodology | `specs/adoption-plan.md` (here, next to the spec) |
| `AGENTS.md`, `.claude/` hooks+subagents, `evals/`, CI config | the greenfield project repo, committed with `src/` |
| Reference patterns to copy | `harness/` experiment in this repo |
| A short teammate-facing "how our harness works" | `docs/harness.md` in the greenfield repo |

## Open items / cautions

- **Gaming moves up a level.** Code-enforced gen/eval separation is necessary but not sufficient; see `questions.html` for the three safeguards.
- **The `implementer` triad is one experiment, not the answer.** Evaluate mechanisms per context before standardizing.
- **`AGENTS.md` quality caps everything downstream.** Stale or vague context means every step inherits the gap. Prune it like code.
