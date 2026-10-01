---
id: 2026-10-01-api-checks-the-looks-of-a
title: API checks the looks of a setting book's characters
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-01T03:45:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_series.py
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

- [ ] `doc_problem` refuses a setting book or story bible whose characters' `looks` break the
  rules `looksProblem` applies, with the same meaning: a list; each look an object with an id
  (`^[a-z][a-z0-9-]{1,23}$`, unique within the character) and an appearance; integer `from` >= 1;
  `to` absent, null or an integer >= `from`; `from` not after `planned_episodes`;
  `sheet_prompt` and `voice_style` text when given; `voice_style` only on a character whose
  voice provider is `gemini`; no two looks of one character covering the same episode.
- [ ] A setting book without `looks` is filed exactly as before.
- [ ] Tests in apps/api/tests/test_video_series.py for each refusal and for a valid book.

## Steps

- [ ] Read `looksProblem` in tools/video/automation/series.mjs and mirror it in `doc_problem`.
- [ ] Add the tests.

## How to verify

From apps/api: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests`,
`uv run pytest tests/test_video_series.py -q`.

## Notes

- Filed by the tool-side change (branch `claude/drama-character-look-change`), which stopped
  at the tool side as asked.
- The owner's admin error messages are not localized (SERIES.md: 後台路徑不需要四語錯誤).
