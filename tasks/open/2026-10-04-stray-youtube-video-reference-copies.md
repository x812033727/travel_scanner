---
id: 2026-10-04-stray-youtube-video-reference-copies
title: Remove the stray tracked copies under .claude/skills/youtube-video/references
status: open
priority: P3
area: meta
owner:
claimed_at:
created_at: 2026-10-04T15:44:28Z
completed_at:
branch:
depends_on: []
scope:
  - .claude/skills/youtube-video/references
---

# Remove the stray tracked copies under .claude/skills/youtube-video/references

## Why

Only each skill's SKILL.md is mirrored to `.claude/skills/<name>/` (`tools/skills.test.mjs`); references
live once under `.agents/skills/`. Four tracked files under `.claude/skills/youtube-video/references/`
(`animation-production.md`, `drama.md`, `prompts/writer-drama.md`, `prompts/writer-series.md`) are
old copies that no longer match the `.agents` files (`drama.md` differs around line 93), so a reader
of the Claude copy gets stale rules.

## Definition of done

- [ ] The stray copies are removed (or the test is extended to fail on any file other than SKILL.md under `.claude/skills/`).
- [ ] `tools/skills.test.mjs` passes and nothing reads those paths.

## Steps

- [ ] `git grep` for the four paths; delete them; consider a test that lists every file under `.claude/skills/`.

## How to verify

```bash
node --test tools/skills.test.mjs
```

## Notes

- The youtube-video SKILL.md pair is bound by the long-form review receipt; this task does not touch it.
- Found while writing `2026-10-04-animation-preproduction-skill`.
