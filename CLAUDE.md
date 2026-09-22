# agent-harness — working agreement

This is a research/design workspace, not a codebase (except `harness/`, an
explicit experiment — see its own README). The purpose is to build a
self-healing agentic harness. The output of research work here is markdown:
indexes, summaries, proposals, and occasionally a spec.

## Primary workflow: the user hands you a link
The main loop for new research is: the user pastes a link (video, article,
GitHub repo, whatever), and you turn it into organized, navigable content
without being asked step by step. On any new link, do all of this by
default:
1. Fetch it — `yt-dlp` for video transcripts, `WebFetch` for articles/repos.
2. Save the raw/cleaned content under `sources/` (transcript, article, or
   repo-readme writeup as appropriate).
3. Add a row to `sources/INDEX.md`.
4. Write a summary in `summaries/`, cross-linked both ways.
5. Only write a `proposals/` entry if the content clearly suggests something
   to build, or the user asks for one — don't force a proposal out of every
   source.
Don't wait for the user to ask for each of these steps individually — a
bare link is enough to trigger the full pipeline.

## Directory contract
- `sources/` — raw external input only. Never edit a source's content after
  saving it; if it needs correcting, add a note, don't rewrite it.
  - Every new source gets a row in `sources/INDEX.md`.
  - Videos → transcript via `yt-dlp` (see below), cleaned into a plain
    markdown file in `sources/transcripts/`.
  - Articles → `WebFetch` extraction saved to `sources/articles/`.
  - Screenshots/diagrams → saved to `docs/`, referenced from wherever they're
    relevant (source, summary, or proposal).
- `summaries/` — one file per source or per closely-related source pair.
  Filename pattern: `YYYY-MM-DD-topic-slug.md`. Always link back to the
  source(s) in `sources/` and forward to any proposal it fed.
- `proposals/` — numbered (`000N-slug.md`), never renumbered or deleted.
  Track status in a `Status:` field at the top (Draft → Scoped → Building →
  Shipped) instead of moving the file around. Cross-link to the relevant
  `specs/harness-spec.md` component(s) when a proposal fleshes out a
  component that spec only described at the conceptual level.
- `specs/` — tech-agnostic, conceptual specs (`harness-spec.md`) and
  methodology (`adoption-plan.md`) for the harness as a whole. These sit a
  level above individual proposals; a proposal should reference the spec
  component(s) it's implementing, not duplicate them.
- `harness/` — the one place actual implementation code lives: a Python
  experiment demonstrating a specific harness mechanism (see its README).
  Proposals may point here as a reference pattern, but don't add new
  production code outside this folder without an explicit decision to do so.
- `*.html`, `presentation.html`, `questions.html` — polished write-ups
  published via GitHub Pages (see `.github/workflows/static.yml`). Treat
  these as a published output format, not a place to draft new research —
  draft in `sources/`/`summaries/`/`proposals/` first, and only turn
  something into an HTML page once it's a settled, presentable piece.
- Cross-link liberally with relative markdown links between sources,
  summaries, proposals, and specs — this repo is meant to be navigable, not
  just archived.

## Getting a YouTube transcript
`yt-dlp` is installed via Homebrew. Pull captions without downloading video:
```
yt-dlp --write-auto-sub --write-sub --sub-lang en --skip-download \
  --sub-format vtt -o "sources/transcripts/%(title)s.%(ext)s" "<url>"
```
Then strip VTT timing/markup into a clean paragraph (dedupe repeated caption
lines — VTT rewrites the same line multiple times with rolling word
highlights). Save as `sources/transcripts/<slug>.md` with a one-line source
link at the top.

## Tone
Keep summaries and proposals terse and concrete — bullet points over prose,
concrete mechanisms over abstractions. This repo exists so future sessions
(and future you) can pick up cold; write for that reader.

## Don't
- Don't build implementation code here beyond `harness/` — proposals stay
  design-only until there's an explicit decision to start building, and if
  so, that likely belongs in a separate repo (or, for a scoped experiment,
  `harness/`).
- Don't delete or rewrite files under `sources/` — they're the raw record.
