---
id: 2026-10-05-ai-head-to-head-hands-on
title: Hands-on AI head-to-head articles once real accounts can run the tests
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T08:44:16Z
completed_at:
branch:
depends_on: []
scope:
  - docs/life-ai-head-to-head
---

# Hands-on AI head-to-head articles once real accounts can run the tests

## Why

The owner asked for same-task comparisons like the reference site's (Claude vs ChatGPT vs
Gemini writing long text, reading PDF reports, translating, Excel clean-up, making slides,
whether Cursor is worth paying for). An honest comparison needs the tools run on real
accounts with a fixed prompt set; the 2026-10-05 session had no such accounts or API keys,
so the owner dropped these six from the office batch rather than publish spec-table
"comparisons" dressed up as tests.

## Definition of done

- [ ] A test protocol per article (frozen prompts and files, scoring rubric, what to record,
      dates and plan names) under `docs/life-ai-head-to-head/`.
- [ ] Runs done on real accounts (the owner, or the host's AI account proxy for the tools it
      covers), raw outputs kept with the run date.
- [ ] Articles written from those records through `content-pipeline`, never from memory.

## Notes

The Shorts "AI 實測" line (`docs/videos/SHORTS.md`) already freezes prompts and runs each
model once on the host; reuse its harness where the tool is one it covers.
