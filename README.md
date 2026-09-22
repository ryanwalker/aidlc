# agent-harness

Workspace for researching and designing a self-healing agentic harness.

## Layout

```
sources/        Raw external input, unmodified. Start here for "what did we read/watch".
  INDEX.md        Table of every source: link, local copy, status
  transcripts/    Cleaned video transcripts
  articles/       Saved/converted articles
summaries/      Our distilled takeaways per source, cross-linked to sources/INDEX.md
proposals/      Numbered design docs for pieces of the harness we want to build
specs/          Tech-agnostic conceptual specs and adoption methodology
  harness-spec.md   The 9 capability areas a harness needs, what/how per component
  adoption-plan.md  How to stand the harness up alongside a new codebase
harness/        Python experiment: a directory-restricted implementer subagent
docs/           Diagrams and reference images
*.html          Published write-ups (GitHub Pages, see .github/workflows/static.yml)
CLAUDE.md       Working agreement for how Claude should operate in this repo
```

## Workflow
1. New content comes in (video, article, screenshot) → save it under
   `sources/` and add a row to `sources/INDEX.md`.
2. Read/watch it → write a summary in `summaries/`, linked from the source's
   row in the index.
3. If a summary suggests something we want to build → write a numbered
   proposal in `proposals/`, linked from the summary and cross-linked to the
   relevant `specs/harness-spec.md` component(s).
4. Proposals stay in `proposals/` even after being built — update their
   `Status` field (Draft → Scoped → Building → Shipped) rather than deleting.
5. Settled, presentable research gets turned into a published `.html`
   write-up — draft in the sources/summaries/proposals pipeline first.

## Current state
- Research pipeline (`sources/`, `summaries/`, `proposals/`): one source
  thread captured so far — PostHog's agentic-code-review material and Cole
  Medin's AI-skills-repo writeup. See
  [[summaries/2026-08-27-code-review-agents.md]] and
  [[summaries/2026-08-27-coleam00-skills.md]].
- One draft proposal: [[proposals/0001-review-swarm-and-risk-gate.md]] —
  adapting PostHog's review-swarm + risk-gate pattern. Not yet scoped.
- Spec layer (`specs/`): `harness-spec.md` defines the 9 capability areas
  tech-agnostically; `adoption-plan.md` covers greenfield adoption.
- `harness/`: a scoped Python experiment (directory-restricted `implementer`
  subagent) demonstrating gen/eval separation from `adoption-plan.md` step 2.
- Published HTML write-ups (`00`–`07`, `presentation.html`, `questions.html`,
  `new-sdlc-summary.html`) cover the broader "New SDLC with vibe coding"
  research that predates the sources/summaries/proposals pipeline.
