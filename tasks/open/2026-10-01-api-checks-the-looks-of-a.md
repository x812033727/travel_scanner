---
id: 2026-10-01-api-checks-the-looks-of-a
title: API checks the looks of a setting book's characters
status: in-progress
priority: P3
area: api
owner: claude-opus-5-5-api-looks
claimed_at: 2026-10-01T12:21:51Z
created_at: 2026-10-01T03:45:56Z
completed_at:
branch: claude/api-checks-character-looks
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_series.py
  - docs/videos/SERIES.md
---

# API checks the looks of a setting book's characters

## Why

Since task `2026-09-29-let-a-drama-character-s-look`, a character in a series' setting book
(or a one-off's story bible) may carry `looks: [{ id, from, to?, appearance, sheet_prompt?,
voice_style? }]`: the appearance, sheet prompt and voice style it has in episodes `from` to
`to` (docs/videos/SERIES.md, 換裝與變化). The worker checks that shape before it files a
document (`looksProblem` in tools/video/automation/series.mjs, called from `documentProblem`),
and so do the plans' validators, which call `documentProblem`.

The site does not: `doc_problem` in apps/api/app/video_automation/series.py checks only that each
character has an id, a name and an appearance. A setting book the owner edits by hand on
/admin/videos (`PUT …/series/{slug}/docs/{kind}`) or one that reaches the site another way can
therefore hold a look the worker would have refused: two looks covering one episode, a `to`
before `from`, a look without an appearance. The worker reads such looks defensively
(`lookFor` skips a look without an appearance or an integer `from`, and takes the first look
that covers an episode), so nothing breaks, but the owner is not told the look will not apply.

The contract says `doc_problem` and `documentProblem` agree on document shapes.

## Definition of done

- [x] `doc_problem` refuses a setting book or story bible whose characters' `looks` break the
  rules `looksProblem` applies, with the same meaning: a list; each look an object with an id
  (`^[a-z][a-z0-9-]{1,23}$`, unique within the character) and an appearance; integer `from` >= 1;
  `to` absent, null or an integer >= `from`; `from` not after `planned_episodes`;
  `sheet_prompt` and `voice_style` text when given; `voice_style` only on a character whose
  voice provider is `gemini`; no two looks of one character covering the same episode.
- [x] A setting book without `looks` is filed exactly as before.
- [x] Tests in apps/api/tests/test_video_series.py for each refusal and for a valid book.

## Steps

- [x] Read `looksProblem` in tools/video/automation/series.mjs and mirror it in `doc_problem`.
- [x] Add the tests.

## How to verify

From apps/api: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests`,
`uv run pytest tests/test_video_series.py -q`.

## Notes

- Filed by the tool-side change (branch `claude/drama-character-look-change`), which stopped
  at the tool side as asked.
- The owner's admin error messages are not localized (SERIES.md: 後台路徑不需要四語錯誤).
- Claimed with `--force` (2026-10-01): the only overlaps were stale claims whose PRs are merged:
  `2026-09-27-video-drama-room-withdraw-a-one` (PR #870, merged 2026-09-28, ticket still in
  review) and the codex-ten-drama tickets from PR #978.
- Done (2026-10-01): `_looks_problem` in series.py, called from `doc_problem` for every character
  of a setting book or story bible right after the id/name/appearance check (the worker checks
  in the same order, character by character). It mirrors `looksProblem` rule for rule and uses
  its messages word for word, so the worker and the owner read the same reason. No new context
  was needed: `planned_episodes` comes from the series `doc_problem` already receives, the voice
  provider from the character's own `voice`. JS `undefined` is a missing key here and JS `null`
  is `None`: `looks: null` and `voice_style: null` are refused as in Node, `to: null` means
  "to the end". Booleans are not episode numbers (Number.isInteger(true) is false).
- The owner's hand edit (`PUT .../docs/{kind}`) reaches `doc_problem` when it asks to approve
  (`_check_document_approval`), as before; a saved-for-review edit is checked on approval.
- Scope: added docs/videos/SERIES.md, whose 換裝與變化 paragraph said the server does not check
  looks yet; it now says it does.
- Tests: one parametrized case per refusal (20 cases), a valid book with looks (adjacent looks,
  open-ended `to: null`, a Gemini `voice_style`), an empty looks list, a book without looks, and
  a one-off story bible (one episode, so a look from episode 2 is refused). No Node/Python
  cross-check exists in the repo, so none was invented; the cases copy the Node rules.
