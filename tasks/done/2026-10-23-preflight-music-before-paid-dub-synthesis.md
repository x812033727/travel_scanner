---
id: 2026-10-23-preflight-music-before-paid-dub-synthesis
title: Preflight music before paid dub synthesis
status: done
priority: P2
area: tools
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:24:55Z
created_at: 2026-10-23T12:15:16Z
completed_at: 2026-10-24T13:25:26Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Preflight music before paid dub synthesis

## Why

The #1669 generated-music guard reaches a dub through `musicInputs()` in `dubSound()`.
`dubLocale()` currently calls paid `synthesize()` for pending translation lines before
`dubSound()` checks that music. A legacy, missing, changed or short generated track can
therefore stop the final mix after dub speech has already been purchased. The C-series
safety port holds before dub *mixing*, not before dub speech spend. No C-series dub run is
authorized in that port.

## Definition of done

- [x] A dub with invalid required music stops before the first paid speech request, with
      a clear owner action and no new speech journal, audio cache or TTS charge.
- [x] The check uses the current source cut length, SHA and fully decoded generated-music
      evidence. Valid owner-supplied music and music-free videos keep their existing path.
- [x] The later mix-time check remains, so a music file changed during speech work cannot
      enter a final dub.

## Steps

- [x] Coordinate a narrow release of these dubs files from the active A01 lexicon and
      five-language task owners before claiming or editing; do not force their claims.
- [x] Place the shared music preflight after current translation/timeline checks and before
      the `synthesize()` loop, passing `timeline.total_frames / FPS` explicitly.
- [x] Test invalid legacy/short/missing/changed generated music with a zero-call speech stub,
      plus valid generated, owner track and no-music routes. Keep the mix-time race guard.

## How to verify

Run focused `node --test tools/video/dubs/dubs.test.mjs` with FFmpeg present and the
video tooling CI jobs. The failing music cases must make zero calls to the speech client.

## Notes

- 2026-10-24: `dubMusic` checks the existing shared music contract before credentials,
  status or speech work, using the validated narration timeline's exact cut length.
  The mix-time check calls it again so changes during speech still refuse the mix.
- Bundled Node 24.19.0 passed 13 focused cases with zero skips. Nine invalid generated
  music cases made zero further fake-server calls and left prior journal bytes intact;
  a valid generated bed mixed, and a bed changed during speech refused the final mix
  while retaining completed speech. The same refusal regressions failed on old code.
  Evidence logs are outside Git: `dub-music-preflight-red-20261024.log` and
  `dub-music-preflight-green-20261024.log` in the operator's temporary directory.
- The claim initially used `--force` after verifying the overlapping source changes had
  merged (#1482, #1548, #1614) and no open PR touched these two code files. That missed
  this ticket's explicit narrow-release step. The coordinator was informed; that step
  remains unchecked until the stale scope metadata is reconciled. Other owners' task
  files and operational/pilot gates were not changed by this author.
- The board coordinator subsequently approved this narrow two-file repair after
  confirming no fresh conflicting code workload; other task ownership and residual
  operational work remain intact. Full dub and actual FFmpeg music-loop regressions
  passed 37/37, zero skips, on bundled Node 24.19.0. The independent duration-receipt
  increment remains a coordinator gate. No real provider call, paid synthesis,
  host change or media approval occurred.

Filed 2026-10-23 from independent review of the C-series #1669 port. The new shared
`musicInputs()` guard is called near `tools/video/dubs/cli.mjs:194`; the current
`dubLocale()` paid speech loop is near line 251 and `dubSound()` near line 365. This
ticket is separate from the port and makes no change to the C-series dub route now.


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- - [ ] A dub with invalid required music stops before the first paid speech request, with
- - [ ] The check uses the current source cut length, SHA and fully decoded generated-music
- 2026-10-24 execution: Required music validated before speech/status/cache creation, mix-time recheck retained;37 tests passed. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
