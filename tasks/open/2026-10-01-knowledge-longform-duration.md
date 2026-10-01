---
id: 2026-10-01-knowledge-longform-duration
title: Apply the eight-minute minimum to all knowledge and story long-form plans
status: in-progress
priority: P1
area: docs
owner: codex-longform-plans
claimed_at: 2026-10-01T16:00:40Z
created_at: 2026-10-01T15:59:48Z
completed_at:
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - docs/videos/long-form
  - tools/video/long-form
  - docs/videos/so-thats-why/README.md
  - docs/videos/so-thats-why/season2/README.md
  - docs/videos/KNOWLEDGE-STORIES.md
---

# Apply the eight-minute minimum to all knowledge and story long-form plans

## Why

The owner expanded the eight-minute long-video minimum to season 1, season 2, season 3, the 100 brand stories and the 81 AI terms. Existing estimates and historical text-review hashes must not be mistaken for measured video duration.

## Definition of done

- [ ] All 473 retained catalog entries have explicit production targets and a 480-second content/final minimum; the eight rejected season-2 duplicates stay excluded and the covered AI term stays covered.
- [ ] Season-2 effective six-chapter plans total 600 seconds and their copyable inputs no longer request 480 seconds.
- [ ] Existing facts, independent reviews, original Shorts, schedules and longer brand/AI targets remain intact and verifiable.
- [ ] Catalog completeness, stale sources, shortened targets and covered-item production requests are rejected by the local validator.

## Steps

- [x] Audit five catalogs, existing consumers, active worktrees and open PR paths.
- [ ] Write the authoritative duration revision and generated plans, with original source hashes.
- [ ] Validate every catalog entry and obtain independent duration-only review.

## How to verify

Run `node tools/video/long-form/cli.mjs check`, its Node tests, all ten original season-2 validators, `npm run test:tools` and `npm run check:tasks`.

## Notes

The source planning packages and their fact-review receipts remain historical originals; effective plans carry a separate duration revision. No media generation, imports, production changes or publication occur here.

Collision audit: the README overlap is the >24-hour old `sothatswhy-shorts-from-episode` claim from 2026-09-28. Its branch has no active worktree or current remote, and implementation already landed in #904 (`26a5bfb9`). The narrow new claim was forced for the duration paragraph only; no Shorts files or another owner's ticket are changed. Open #1098 is this branch's draft; old batch #1083 is unrelated historical delivery. AI-term review-owned directories and brand-story source hashes are left untouched.
