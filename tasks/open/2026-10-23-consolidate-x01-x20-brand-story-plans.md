---
id: 2026-10-23-consolidate-x01-x20-brand-story-plans
title: Consolidate X01-X20 brand-story plans for paused admin import
status: in-progress
priority: P2
area: docs
owner: claude-opus-x-series
claimed_at: 2026-10-23T18:49:17Z
created_at: 2026-10-23T18:48:42Z
completed_at:
branch: claude/pr-x-series-backend-deploy-9fe314
depends_on: []
scope:
  - docs/videos/brand-stories-company-turns-20261024
  - apps/api/app/video_automation/stories.py
  - apps/api/tests/test_video_story_import.py
  - apps/api/tests/test_video_story.py
  - apps/web/components/admin-video-stories.tsx
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
---

# Consolidate X01-X20 brand-story plans for paused admin import

## Why

The owner asked (2026-10-24) to complete the X brand-story series and put it on the video
admin, then close its PRs. X01–X15 sit in fifteen open Codex preproduction PRs
(#1619–#1640) and X16–X19 only on branches; none of them is a six-chapter plan row with a
hash-bound independent review, so the importer cannot take them. The owner chose to fill
the series to twenty with a new X20 and to import it the way the C series was (#1778):
series paused, every episode planned, no worker start and no paid generation.

## Definition of done

- [x] Twenty X01–X20 episode rows reflect each branch's source-checked treatment (X20 a new topic).
- [x] Another reviewer verifies each row against its sources with a hash-bound receipt; the
      builder emits `stories.json` only after all twenty pass.
- [x] The importer accepts the X letter only for this series and creates it paused with
      planned rows; the C series keeps its behaviour.
- [ ] Production dry-run, apply and readback: one paused series, twenty planned episodes,
      zero new drama requests. The X PRs are closed with a pointer to the merged package.

## Steps

- [x] Series folder, X20 topic, twenty episode rows.
- [x] Independent reviews and build.
- [x] Generalise the review-only import (JS and Python) with tests.
- [ ] PR, CI, deploy, production import and readback.
- [ ] Close the X PRs.

## How to verify

`node docs/videos/brand-stories-company-turns-20261024/build.mjs`;
`node --test tools/video/story-plans/plan.test.mjs`;
`cd apps/api && uv run pytest tests/test_video_story_import.py`; production
`video-story-import --series brand-stories-company-turns` dry-run, then `--apply`, then readback.

## Notes

Claim override rationale: the reported overlap `2026-10-18-story-thumbnail-brand` is stale (its
work landed as #1568, no live branch); #1778's tickets overrode it for the same reason.

2026-10-24: Four authoring agents wrote X01–X20 from each branch's last passing treatment
(X20 Nespresso is new research: Swiss Federal Supreme Court 4A_61/2021, the French competition
authority's 2014 commitments, Nestlé releases). Four different agents (x_review_a–d) opened the
sources and wrote hash-bound receipts; 18 rows were fixed, 2 passed. The worker reads whole pages
(`story.mjs` asks for `whole: true`), so only pages over 3 MB or PDFs make a fact `reviewer_only`:
X01 has 4 such facts (Adobe 10-Ks), X11 has 6 (FedEx 10-Ks, 3.4–9 MB). X15 Garmin shares its
subject with the 100-bank C15; only one should be produced. The review-only import is now keyed by
`REVIEW_ONLY_SERIES` (C everyday reversals, X company turns); the C03 link stays C-only.
