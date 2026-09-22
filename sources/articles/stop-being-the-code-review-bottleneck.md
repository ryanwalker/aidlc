# Stop Being the Code Review Bottleneck

- **Source:** https://newsletter.posthog.com/p/code-review-tips
- **Author:** Jina Yoon
- **Date:** 2026-07-09
- **Companion video:** [Does anyone read the code anymore?](https://www.youtube.com/watch?v=-l3eW8SSQ5o) — see [[../transcripts/does-anyone-read-the-code-anymore.md]]

## Overview

AI-generated code is produced faster than humans can review it. The fix is not
reviewing code faster — it's reviewing less code, by delegating review work to
agents and building process around verification.

## Four strategies

### 1. Agent-based code review
Deploy multiple agents with different specialized instructions instead of one
human reviewing everything.
- The agent that wrote the code should not review it — agents miss their own
  blind spots and are overconfident.
- Use diverse agents with varied goals and models (cheap models for style,
  stronger models for judgment calls).
- Example: Paul D'Ambra's system (PostHog) spawns four reviewer agents
  (`qa-team`, `security-audit`, `paul-reviewer`, `xp-reviewer`), triages
  findings into actionable / nits / ambiguous, and loops until only ambiguous
  items remain (up to 3 iterations). See [[../../docs/qa-swarm-review-flow.png]].
- Cost note: ~60% of Paul's token spend goes to automating CI/review toil —
  considered worth it for the time saved.
- Lighter-weight alternative if a multi-agent system is too expensive:
  **No Mistake** (MIT-licensed single-agent quality gate between you and git
  remote).

### 2. PR babysitting loops
Automate tedious review-adjacent chores (CI monitoring, test reruns, branch
maintenance, notification triage) to cut context switching.
- Example: Phil Haack's `babysit-prs` skill classifies open PRs as
  quiet / CI-failing / pending / new-comments, and calls a dedicated CI-monitor
  skill on failures.
- Run it as a cron job via a `/loop` command so PRs stay mergeable without
  manual checking.

### 3. PR auto-stamping (risk assessment gate)
Deploy an agent (PostHog's **StampHog**) to auto-approve low-risk PRs via
deterministic safety checks, escalating anything uncertain. See
[[../../docs/safety-checks-risk-assessment.png]].

Trigger: engineer adds a `StampHog` label to the PR. Checks run in order,
gated — later checks only run if earlier ones pass:
1. **PR state** — no requested changes, no merge conflicts.
2. **Blast radius** — deterministic deny-list of sensitive paths (auth,
   secrets, billing, public API, etc.).
3. **Diff size** — under 500 lines and under 20 files changed.
4. **LLM check** — only now does an LLM read the diff, looking for
   showstoppers.

Outcomes:
- **Approve:** bare GitHub approval, no line comments.
- **Refuse/escalate:** 1–2 sentence reason, a risk-level rating, and next
  steps (usually: tag a subject-matter expert).

Impact: resolves 1,500+ PRs/month at PostHog — 1,500 fewer Slack
interruptions.

### 4. Verify by observation, not by argument
Agents are good at explaining why code works even when it doesn't. Don't
trust the rationale — watch the behavior directly (real API request, actual
output) whenever you can.
- Scaling problem: a 3,000-line PR is hard to trust-and-observe.
- Fix: decompose large changes into a **stack of small, single-purpose PRs**
  (under 400 changed lines each), each buildable only on the one below it.
  Use Graphite (or GitHub's native stacked-PR support) to manage the stack.
- Each PR in the stack ships with its own test and a concrete way to observe
  it working (a command to run + expected output).
- Merge bottom-up: each layer only builds on already-verified behavior, so
  early mistakes can't compound and breakage is isolated to one small diff.
- Auto-stamping (#3) compounds well with this — small, focused PRs are
  exactly what a StampHog-style gate can safely auto-approve.
- Especially valuable for front-end work, where deterministic tests miss
  visual/behavioral correctness.

## Referenced tools & skills
- Paul D'Ambra's `qa-swarm` and `review-triage` skills (PostHog)
- Phil Haack's `babysit-prs` skill
- PostHog's **StampHog** auto-approval agent
- **Graphite** — PR stacking
- Pawel Cebula's `qa-frontend` skill (visual testing)
- **No Mistake** — MIT-licensed single-agent git quality gate
