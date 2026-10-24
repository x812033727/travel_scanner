---
id: 2026-10-11-render-repeat-draws-a-marked-video
title: Render repeat draws a marked video without its mark
status: done
priority: P3
area: tools
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:23:00Z
created_at: 2026-10-11T16:51:06Z
completed_at: 2026-10-24T13:23:19Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/video/render/repeat.mjs
  - tools/video/render/render.test.mjs
---

# Render repeat draws a marked video without its mark

## Why

`tools/video/render/repeat.mjs` draws a video's slide states several times and says which
frames differ between runs. It plans with `renderPlan(doc, themeHash(), ROOT)` and has no work
directory, so it cannot read the video's `watermark.json`: a video that carries the channel
mark (docs/videos/WATERMARK.md) is planned without it. Its comment says "the whole video is
planned, so the keys are render's"; for a marked video they no longer are, and the frames it
proves repeatable are not the frames the video uses.

## Definition of done

- [x] `repeat.mjs --workdir D` reads the video's pin and plans with the same mark render used.
- [x] Without `--workdir` it says the frames are drawn without the mark.

## Steps

- [ ] `readWatermarkPin` (tools/video/core/watermark.mjs) and the `watermark` option of
      `renderPlan`.
- [ ] A test of `drawOnce`'s plan for a pinned work directory.

## How to verify

`node tools/video/render/repeat.mjs --slug <slug> --workdir <dir> --channel msedge`: the stills
it writes with `--out` show the mark.

## Notes

- 2026-10-24: The coordinator claimed this task and authorized adding the existing
  render-test file to its scope. `--workdir` names the exact video work directory;
  repeat reads its watermark pin and passes that same checked mark to renderPlan.
  It never adopts or rewrites a pin. Without a work directory it explicitly says
  the frames are unmarked.
- The focused repeat regressions passed 2/2, zero skips, on bundled Node 24.19.0:
  pinned state keys and HTML equal the ordinary renderer's, embedded PNG bytes
  are present, no-pin behavior stays unchanged, and a stale pin hash is refused.
  No source media was regenerated and no production or paid service was used.

- The mark is a data URI inside the page, so it draws from memory and should not add a source
  of difference between runs; worth confirming once.


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- - [ ] `repeat.mjs --workdir D` reads the video's pin and plans with the same mark render used.
- - [ ] Without `--workdir` it says the frames are drawn without the mark.
- 2026-10-24 execution: Repeat reads same pinned watermark/workdir, rejects pin hash drift;full render40 tests passed. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
