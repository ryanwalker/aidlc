# Proposal 0001: Review-swarm + risk-gate for this harness

- **Status:** Draft / idea — not yet scoped or committed to
- **Inspired by:** [[../summaries/2026-08-27-code-review-agents.md]]
- **Diagrams:** [[../docs/qa-swarm-review-flow.png]], [[../docs/safety-checks-risk-assessment.png]]
- **Implements spec components:** [[../specs/harness-spec.md]] #6 (guardrails
  enforced in code — the deterministic risk gate) and #8 (verify output
  separate from producing it — the independent reviewer swarm)

## Goal
Adapt PostHog's two-part pattern (multi-agent review swarm + deterministic
risk gate) into a self-healing review loop for this harness, so most PRs
resolve without pulling a human in.

## Shape (as understood from the source material)

```
PR opened
  │
  ▼
[risk gate]  PR state → blast radius (deny-list) → diff size → LLM showstopper check
  │  pass all           │ fail any
  ▼                     ▼
auto-approve      [review swarm] N parallel reviewer agents, distinct lens + model
                        │
                        ▼
                  [triage] classify every thread: actionable | nit | ambiguous
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     fix & push    resolve+reply   escalate to human-agent pair
          │                              (autonomy-ladder gate)
          └────────► loop until no new actionable threads (cap ~3x)
```

## What we'd need to define for our own version
- **Deny-list** for blast radius — which paths/areas in our repos count as
  sensitive (auth, secrets, billing, infra, public API surface, etc.).
- **Diff-size thresholds** — start from PostHog's (500 lines / 20 files) and
  adjust based on our own PR size distribution.
- **Reviewer roster** — how many agents, what lens each one takes, which
  model tier per lens (cheap for mechanical checks, stronger for judgment).
- **Triage classifier** — the actual prompt/schema deciding
  actionable vs. nit vs. ambiguous, and what "high certainty" means
  concretely.
- **Escalation path** — who/what is the "human-agent pair" for ambiguous
  items in our workflow, and what does the risk-level rating look like.
- **Loop bound** — iteration cap and stop condition (no new actionable
  threads, same as PostHog's 3x).

## Non-goals (for now)
- Not building the PR-babysitting-loop piece yet (CI monitoring, staleness) —
  separate proposal if we want it.
- Not tackling the stacked-PR / observation-decomposition piece yet — also a
  separate proposal.

## Next steps
1. Decide which repo(s) this would run against first (small blast radius to
   start).
2. Draft the deny-list and diff-size thresholds for that repo.
3. Prototype the risk gate alone (cheapest, most deterministic piece) before
   adding the reviewer swarm.
4. Only then design the triage classifier and escalation path.
