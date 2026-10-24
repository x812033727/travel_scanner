---
id: 2026-10-24-avoid-false-written-language-lint-hit
title: Avoid false written-language lint hit inside Japanese text
status: in-progress
priority: P1
area: tools
owner: codex-c-series-integration
claimed_at: 2026-10-24T03:31:50Z
created_at: 2026-10-24T03:31:46Z
completed_at:
branch: codex/c15-frixion-canonical-preflight-20261024
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Avoid false written-language lint hit inside Japanese text

## Why

The Chinese `WRITTEN_ONLY` list rejects `本文` in narration. Its substring check also
finds those two characters across `日本文` in words such as `日本文字` and `日本文化`.
C15 FriXion's owner-approved T07 says `日本文字`, so the false positive must be fixed
in the lint rule without rewriting the approved script.

## Definition of done

- [x] `日本文字` and `日本文化` no longer raise a `本文` written-language error.
- [x] A real `本文` still raises the error, including when it follows `日本文字` on the same line.
- [x] Focused lint tests pass without changing the C15 script or project files.

## Steps

- [x] Add a regression covering false positives, genuine self-reference, and mixed occurrences.
- [x] Check `本文` per occurrence, excluding only a match preceded by `日`.

## How to verify

- `node --test tools/video/core/lint.test.mjs`: 50/50 PASS.
- `git diff --check`: PASS.

## Notes

The new regression failed before the lint edit on C15 T07 (`1 !== 0`), then passed
after the fix. Other `WRITTEN_ONLY` phrases keep their existing substring behavior.
The implementation checks each occurrence, so an earlier `日本文字` cannot hide a
later actual `本文`. No paid calls, C15 script edits, branch changes, commits, or
pushes were made under this task.
