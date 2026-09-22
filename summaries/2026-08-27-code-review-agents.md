# Summary: Agentic code review at PostHog

- **Sources:** [video transcript](../sources/transcripts/does-anyone-read-the-code-anymore.md), [article](../sources/articles/stop-being-the-code-review-bottleneck.md)
- **Date:** 2026-08-27

## The problem
AI lets you write code much faster, but a human reading every line doesn't
scale — you just move the bottleneck from writing to reviewing. PostHog is
merging 6x as many PRs/week as a few months ago.

## The core idea
Don't review harder. Build a system around review so most PRs never need a
human at all:

1. **Independent multi-agent review** (not self-review) — catches what the
   authoring agent is blind to.
2. **Babysitting loops** — automate the chores around review (CI, comments,
   staleness) so humans aren't context-switching to check on things.
3. **Risk-gated auto-approval** — deterministic, cheap checks first (state,
   blast radius, diff size); LLM judgment only after those pass; escalate
   anything uncertain with a reason + risk rating.
4. **Verify by observation, not narrative** — trust what you can run and see,
   not an agent's explanation. Scale this by decomposing big changes into
   small, independently-observable, stacked PRs.

## Concrete mechanisms worth stealing

**QA-swarm / review-triage (Paul D'Ambra):**
- 4 parallel reviewer agents, each a distinct lens + model:
  - `qa-team` — technical (security/db/perf), cheap model (Fable)
  - `security-audit` — SQL/prompt-injection focus, cheap model (Fable)
  - `paul-reviewer` — naming/observability/rollout, written in reviewer's own
    voice, expensive model (Opus)
  - `xp-reviewer` — Extreme Programming lens (readability, best practice),
    expensive model (Opus)
- Triage classifies every unresolved thread into exactly one bucket:
  - **actionable** → fix + push automatically (single-file, high certainty)
  - **nit** → resolve + reply silently (style/dupe/out of scope)
  - **ambiguous** → escalate to a human-agent pair (autonomy-ladder gate)
- Loops up to 3x until no new actionable threads appear.
- Cost: ~60% of token spend goes to this + CI toil — judged worth it.

**StampHog (auto-approval gate):**
- Triggered by a label on the PR.
- Ordered, short-circuiting checks — cheap/deterministic ones first, LLM
  last:
  1. PR state (no conflicts, no requested changes)
  2. Blast radius (deny-list: auth, secrets, billing, public API, etc.)
  3. Diff size (<500 lines, <20 files)
  4. LLM showstopper check (only if 1–3 pass)
- Approve → bare approval, no comments. Otherwise → escalate with reason,
  risk level, and next step (usually: tag an SME).
- 1,500+ PRs/month auto-resolved.

**Observation-driven decomposition (Daniel, for large changes):**
- Split work into a stack of PRs, each <400 changed lines, each building only
  on the one below it (Graphite or GitHub native stacking).
- Every PR ships with its own test **and** a manual observation recipe
  (command to run + expected output).
- Merge bottom-up so verified behavior never gets re-litigated; breakage is
  isolated to one small diff.
- Auto-approval gates (StampHog-style) work well on this scale of PR.

## Open questions / things to dig into next
- What does "autonomy-ladder gate" mean precisely for the ambiguous bucket —
  what decides human-now vs. human-later vs. agent-retries?
- What's the actual prompt/schema for the review-triage classifier?
- Is there a public repo for `qa-swarm` / `review-triage` / StampHog, or only
  the prompts mentioned in the article?
- No Mistake (MIT-licensed single-agent alternative) — worth evaluating as a
  lighter first step before building a full multi-agent swarm.

## Relevance to this project
This is the shape of a **self-healing agentic harness** for code review: cheap
deterministic gates, cheap-model triage, expensive-model judgment only where
needed, and a clear human escalation path for the ambiguous remainder. See
[[../proposals/0001-review-swarm-and-risk-gate.md]] for how we might adapt
this.
