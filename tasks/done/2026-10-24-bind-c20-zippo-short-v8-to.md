---
id: 2026-10-24-bind-c20-zippo-short-v8-to
title: Bind C20 Zippo short v8 to same backend episode row
status: done
priority: P1
area: api
owner: codex-c20-same-row-import
claimed_at: 2026-10-24T09:15:22Z
created_at: 2026-10-24T09:14:30Z
completed_at: 2026-10-24T09:21:02Z
branch: codex/c20-short-v8-same-row-import-20261024
depends_on: []
scope:
  - tasks/open/2026-10-18-story-thumbnail-brand.md
  - apps/api/app/video_automation/stories.py
  - apps/api/tests/test_video_story_import.py
---

# Bind C20 Zippo short v8 to same backend episode row

## Why

C20's approved 36-line Zippo short-v8 plan changes its compiled slug from
`story-everyday-zippo-c20` to `story-everyday-zippo-c20-short-v8`. The review-only
importer currently rejects that change even if the series is paused and episode #20
is still planned. An exact same-row update is needed to keep backend progress tied
to the approved version without creating a second episode or moving the old video
project. The owner authorized releasing only `stories.py` from the stale thumbnail
ticket; that release is recorded in the old ticket's Notes.

## Definition of done

- [x] A dry-run reports only C20 as an update when the other 19 production rows match
      the certified bundle; applying preserves episode #20's id/number and every
      other row, and repeat import is unchanged.
- [x] An existing old-slug VideoProject is preserved byte-for-byte; a conflicting
      new-slug project or episode refuses the import.
- [x] Active series, advanced/foreign C20 row, or a drama request refuses the import.
- [x] No production import, deploy, media purchase, or worker dispatch occurs here.

## Steps

- [x] Confirm C12 branch is clean and its commit remains on the local branch;
      start this work from the latest `origin/main` in the same shared checkout.
- [x] Record the owner's exact narrow release of `stories.py` from
      `2026-10-18-story-thumbnail-brand`, preserving its other scope and Notes.
- [x] Admit only C20/#20 old slug to approved short-v8 slug in the paused,
      planned review-only importer.
- [x] Add focused positive and negative tests, run the relevant API checks and
      task-board validation, then obtain an independent read-only review.
- [x] Close this ticket in the implementation PR and keep it draft/no-auto-merge.

## How to verify

`uv run pytest tests/test_video_story_import.py -q` from `apps/api`, `uv run ruff
check app/video_automation/stories.py tests/test_video_story_import.py`, `npm run
check:tasks`, `git diff --check`, and an independent diff review. Host readback and
deployment are later gates.

## Notes

- PR #1568 merged the thumbnail implementation as
  `498b1dbfc78f44dfa79926b0c979cb26d3b5202f` on 2026-10-18; the old branch
  is absent locally and on GitHub, with no open PR. The old claim nonetheless
  continued to hold `stories.py` until the owner's 2026-10-24 narrow release.
- The old 10-minute MiniMax ticket lists the API test file in its scope but is
  `open` with no owner, so it does not hold the path. Do not alter that ticket.
- Import #1824's compiled bundle only after the separately approved C08 short-v8
  same-row update has landed in production. Before then the same file can report
  C08 and C20 updates together; an operator must require `update=[C20]` and
  `create=[]` before applying C20.
- Local pre-review checks: `uv run pytest tests/test_video_story_import.py -q`
  passed 22/22; Ruff passed both changed API files; mypy passed both changed API
  files; `npm run check:tasks` validated 2159 task files; `git diff --check`
  passed. Test cases include C20 dry-run, same row id, all old VideoProject
  columns after a fresh database reload, idempotence, active series,
  foreign/malformed row ID or JSON shape, ready/started
  row, and occupied new video/episode/request slug.
- Independent reviewer `/root` checked fixed commit `eea582a9e` and the
  exact follow-up delta at `82fad085f`; both received PASS. The latter adds
  non-dict beats refusal and verifies the old project from a fresh DB read.
  Neither commit ran a host import or paid call. The PR remains a merge gate;
  production dry-run/apply are separate downstream steps after C08 readback.
