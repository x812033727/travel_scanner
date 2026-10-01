---
id: 2026-09-30-shorts-md-knock-timer-wording
title: SHORTS.md still says the worker knocks at the start of each round
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-shorts-knock
claimed_at: 2026-10-01T12:39:29Z
created_at: 2026-09-30T16:10:39Z
completed_at:
branch: claude/shorts-md-knock-timer
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

- [x] SHORTS.md describes the knock as running on its own 5-minute timer beside `auto`, and says a
      STOP file in the work directory pauses it (as docs/videos/AUTOMATION.md now does).

## Steps

- [x] Reword that sentence in SHORTS.md; check the T1 row of the phase table and the
      `tools/video/automation/shorts.mjs` row for the same claim.

## How to verify

Read the paragraph against `ops/video/worker.sh`'s `knock_loop`.

## Notes

Only one sentence or two; nothing else in SHORTS.md needs to move.

2026-10-01 (claude-opus-5-5-shorts-knock): claimed with `--force`. The overlapping claim on
SHORTS.md belongs to `2026-09-30-a-cut-short-is-not-asked`, whose PR #998 is already merged
(2026-09-30T04:14:38Z); that ticket was left in `open/` and was not touched here.

Changed three places, checked against `knock_loop` in `ops/video/worker.sh` and the STOP
paragraph in `docs/videos/AUTOMATION.md`:

- the 「誰在什麼時候動手」 paragraph: the knock is a background loop of its own beside `auto`,
  every `VIDEO_SHORTS_KNOCK_SECONDS` (default 300); it does not wait for an `auto` round or look
  at the automation switch, and pauses while a `STOP` file is in the work directory;
- the `tools/video/automation/shorts.mjs` row: that module (still only planned) no longer calls
  `tick` first; only `shortsStep()` has to run before the automation-switch check;
- the T1 row of the phase table: same wording as the paragraph, with the STOP pause.
