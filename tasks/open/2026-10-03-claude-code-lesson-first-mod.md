---
id: 2026-10-03-claude-code-lesson-first-mod
title: Claude Code tutorial lesson: build your first mod
status: in-progress
priority: P3
area: docs
owner: claude-fable-5-1-first-mod
claimed_at: 2026-10-03T23:46:52Z
created_at: 2026-10-03T19:27:30Z
completed_at:
branch: claude/first-mod-lesson
depends_on: []
scope:
  - docs/claude-code-series/lessons
  - apps/api/app/guides/content/claude-code-first-mod.json
  - apps/web/public/guides/claude-code-first-mod
---

# Claude Code tutorial lesson: build your first mod

## Why

The news article `ai-news-claude-code-mods-20261001` explains what Claude Code mods are and where to start, but does not teach writing one. The Claude Code tutorial series (zh-TW, `docs/claude-code-series`) has lessons on plugins and settings hooks and none on mods.

## Definition of done

- [ ] One zh-TW lesson that builds the documentation's `first-mod` (tool-call counter beside the spinner, `/tally` command, `claude plugin validate`, `claude plugin test`), placed after `claude-code-plugins-guide` and `claude-code-plugin-team-distribution`, with the series' starter materials.

## Steps

- [ ] Read https://code.claude.com/docs/en/plugins/mods/create on the day; every command and file verbatim.
- [ ] Write the lesson spec in `docs/claude-code-series/lessons/`, then the pack and starter zip the way the other advanced lessons do.
- [ ] Link it from the tutorial hub and from the news article's zh-TW body with `pack_cli autolink`.

## How to verify

`pack_cli ingest --dry-run`, `intake_check.py`, `pack_cli lint --kind life`.

## Notes

- Filed by batch 4.11 (`docs/news-2026-batch-4/agents/DELTA-4-11.md` §7).
