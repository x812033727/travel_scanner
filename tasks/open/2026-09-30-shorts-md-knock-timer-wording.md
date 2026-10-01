---
id: 2026-09-30-shorts-md-knock-timer-wording
title: SHORTS.md still says the worker knocks at the start of each round
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-30T16:10:39Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-knock-long-rounds-and
scope:
  - docs/videos/SHORTS.md
---

# SHORTS.md still says the worker knocks at the start of each round

## Why

Since `2026-09-28-video-shorts-knock-long-rounds-and`, `ops/video/worker.sh` knocks
(`node tools/video/shorts/cli.mjs tick`) from a background loop of its own every
`VIDEO_SHORTS_KNOCK_SECONDS` (default 300), beside `auto` rather than before it, and skips the
knock while `$VIDEO_WORKDIR/STOP` exists. `docs/videos/SHORTS.md` (§ the paragraph that starts
「審核檔案區只掛在 API 容器」, around line 217) still says the worker calls the knock "每一輪（5 分鐘）
一開始", and does not mention STOP. That ticket's scope did not include SHORTS.md.

## Definition of done

- [ ] SHORTS.md describes the knock as running on its own 5-minute timer beside `auto`, and says a
      STOP file in the work directory pauses it (as docs/videos/AUTOMATION.md now does).

## Steps

- [ ] Reword that sentence in SHORTS.md; check the T1 row of the phase table and the
      `tools/video/automation/shorts.mjs` row for the same claim.

## How to verify

Read the paragraph against `ops/video/worker.sh`'s `knock_loop`.

## Notes

Only one sentence or two; nothing else in SHORTS.md needs to move.
