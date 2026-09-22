# Summary: Cole Medin's AI skills repo

- **Source:** [article](../sources/articles/coleam00-skills-repo.md)
- **Date:** 2026-08-27

## The core idea
Skills are markdown procedure files that load lazily — an agent only sees the
one-line description until the work actually matches, then pulls in the full
body. This is the scaling argument against one giant `CLAUDE.md`: everything
in a monolithic file is always in context, whether relevant or not; skills
are loaded on demand.

## The PIV loop
Plan → Implement → Validate is positioned as the central workflow: planning,
implementation, validation, review, commit, PR — as a repeatable unit rather
than one-off ad hoc steps.

## Hooks as guarantees
The most interesting mechanical idea: deterministic code hooked into agent
lifecycle events *guarantees* certain behavior happens (vs. an instruction in
a prompt, which is a request the agent might skip or forget). This is a
stronger primitive than "tell the agent to check X" — worth treating as the
implementation mechanism for the deterministic parts of any gate we build
(e.g., PR-state / blast-radius / diff-size checks in the StampHog-style risk
gate from [[2026-08-27-code-review-agents.md]]).

## Meta-skills
Tools for building more of the system itself: rules creation, drift checking
(does behavior still match the rules), skill authoring, hooks creation. This
is a harness that includes tooling for maintaining itself — directly relevant
to "self-healing."

## Relevance to this project
Two sources now point at complementary halves of the same problem:
- PostHog material → how to gate/triage/escalate *review* specifically.
- This repo → the broader lifecycle (plan/implement/validate/ship) plus
  meta-tooling (drift checking, skill authoring) for keeping the harness
  itself correct over time — which is the actual "self-healing" part.

## Open questions
- What does "drift checking" actually check against — the skill's own
  described behavior, or some external spec?
- Is the NPX CLI's "works across 75+ agents" claim about a shared skill
  format, or just file-copying with light templating?
- Worth cloning the repo locally to read actual skill files rather than just
  the README, once we're ready to compare concrete implementations.
