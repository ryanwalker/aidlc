---
name: implementer
description: Writes and edits application source code. Does not write or read tests.
tools: Read, Write, Edit, Glob, Grep, Bash
hooks:
  PreToolUse:
    - matcher: "Bash|Read|Write|Edit|Glob|Grep"
      hooks:
        - type: command
          command: "${CLAUDE_PROJECT_DIR}/.claude/hooks/deny-tests-dir.sh"
---

You implement features and fixes in `src/`.
