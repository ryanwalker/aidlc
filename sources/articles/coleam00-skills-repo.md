# Cole's AI Skills Repository

- **Source:** https://github.com/coleam00/skills
- **Author:** Cole Medin
- **Type:** GitHub repo (skills library, not an article/video)

## Overview
33 practical AI agent skills extracted from Cole Medin's personal
`.claude/skills/` folder. Billed as "the AI Layer" from his Agentic Coding
course (dynamous.ai). Built for developers using coding agents day to day.

## Core concept
A skill is a markdown file containing procedures for an agent to follow. The
agent loads only the skill's one-line description at startup, and pulls in
the full skill body only when the work matches it — this is why skills scale
where a 2,000-line `CLAUDE.md` doesn't (everything loaded, all the time,
whether relevant or not).

## Skill categories
- **Planning & priming** — context loading, PRD creation, architecture
  planning, epic slicing
- **PIV loop (Plan → Implement → Validate)** — the central workflow: plan,
  implement, validate, review, commit, open PR
- **Issue management** — investigate + implement fixes with regression
  testing
- **Parallel work** — git worktree management for concurrent development
- **Meta-skills** — tools for building your own AI layer: rules creation,
  drift checking, skill authoring, hooks creation
- **Autonomy** — "Build Dark Factory": end-to-end repo generation and
  validated shipping with minimal human input

## Key feature: hooks
Skills can ship with hooks — deterministic code that runs on lifecycle
events. The pitch: hooks *guarantee* certain agent behavior happens, rather
than just asking the agent nicely and hoping it complies.

## Installation options
- Claude Code plugin (managed, read-only)
- NPX CLI (editable files, claimed to work across 75+ agents)
- Manual clone + copy
- Direct agent-assisted install

## Relevance to this project
Different flavor from the PostHog material — PostHog is about the *review*
stage specifically (multi-agent swarm + risk gate); this repo is a broader
"AI layer" covering the whole plan → implement → validate → ship lifecycle,
plus meta-tooling for building more skills and hooks for guaranteeing
behavior. The PIV loop and hooks-for-guarantees ideas are worth comparing
against our review-swarm/risk-gate proposal — hooks in particular might be
the mechanism for enforcing the deterministic parts of the risk gate (PR
state, blast radius, diff size) rather than relying on an agent to check
them faithfully every time.
