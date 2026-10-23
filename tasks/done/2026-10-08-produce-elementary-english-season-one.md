---
id: 2026-10-08-produce-elementary-english-season-one
title: Produce elementary English season one
status: done
priority: P2
area: tools
owner: codex-elementary-series
claimed_at: 2026-10-08T00:32:58Z
created_at: 2026-10-08T00:32:52Z
completed_at: 2026-10-08T00:52:29Z
branch: codex/elementary-english-season01-20261008
depends_on: []
scope:
  - tools/video/elementary
  - tools/video/preschool/build.py
  - tools/video/preschool/player.py
  - tools/video/preschool/verify_series.py
  - docs/videos/english-elementary-series
  - docs/videos/english-preschool-series/README.md
---

# Produce elementary English season one

## Why

After the completed 48-episode preschool course and draft PR #1376, the user explicitly selected beginning elementary English. The first lower-elementary season develops complete sentences and short classroom exchanges while retaining the established multilingual delivery contract.

## Definition of done

- [x] Twelve lessons have complete English, Traditional Chinese, Simplified Chinese, Japanese and Korean teaching scripts.
- [x] Each measured film embeds English, contains five audio tracks and four translated CC tracks, and preserves English demonstrations across tracks.
- [x] A standalone season player, downloadable ZIP and curriculum catalog are verified outside the public repository.
- [x] Shared tools retain preschool renderer hashes and existing 48-delivery compatibility; source and validation are ready for the continuation PR.

## Steps

- [x] Open preschool draft PR #1376 and create the continuation branch.
- [x] Plan 12 lessons, ten scenes each, with at least three listening questions and guided sentence reading per episode.
- [x] Author and independently check the five-language scripts and new classroom artwork.
- [x] Implement explicit renderer profiles and elementary verification/packaging adapters.
- [x] Synthesize, render, fully decode and package all twelve episodes.
- [x] Record actual validation and delivery links; complete relevant repository checks.

## How to verify

- Load all twelve lessons with the shared audio source validator; inspect cross-language meaning and listening-question answer timing.
- Run dependency-free profile/integrity regressions through `npm run test:tools` and `npm run check:tasks`.
- Run elementary source/timing/audio/CC/media verification, full FFmpeg decode during production, player interaction checks and ZIP CRC/file-hash checks.
- Confirm the original preschool renderer fingerprint and completed-media validation still accept the retained 48 films.

## Notes

- Preschool draft PR: https://github.com/x812033727/travel_scanner/pull/1376. This branch is intentionally based on its source commit; no merge requested.
- Audience: approximately ages 6–8 with exposure to the preschool vocabulary. Ten scenes per lesson, target about 3–4 minutes; measured speech timing takes priority, with a hard 3–5-minute media validation range. This is the established short children's course format, separate from the general long-form pipeline.
- Media destination: `/workspace/elementary-season01-output`. Original preschool outputs remain untouched.
- Only lesson instructions are localized. English example clips are shared across the original English and four localized audio tracks. English is embedded in the picture; no English CC is generated.
- Guided sentence reading includes a spoken model; it is not an independent reading or phonics assessment. Listening questions leave six seconds before displaying the answer and translations; other practice leaves five seconds.
- Trial synthesis retains Microsoft Edge voices used for preschool. No configured backend voice, upload, publication or complete human pronunciation review is implied.
- Authors own separate `part01-04.json`, `part05-08.json`, `part09-12.json`; root assembles `lessons.json`. Artwork and pipeline implementations have separate file ownership.

Validation in progress: full tools suite passed (2,008 passed, 3 skipped, 2,011 total), including 10 elementary/profile/batch and 10 preschool integrity regressions. Read-only preschool compatibility recheck passed all 48 media with zero errors at `/tmp/elementary-preschool-compatibility.json`. Preschool PR #1376 is still draft; all reported CI checks have passed, including api/web/containers/full-stack-smoke. No merge performed.

Final editorial correction: changed episode 05 title to “Asking Politely” / “有禮貌地提出請求” with aligned four-language titles. The old title contained “pencil” in the persistent picture header and could hint at quiz answers. The lesson examples remain unchanged; regenerated source-bound audio receipts and rerendered only ep05.

Browser limitation: real headless Chromium 151 launched but rejected local `file://` navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. No policy bypass attempted. Saved `browser-checks.json` with `passed:false`; jsdom UI checks pass and FFmpeg handles real media decoding separately.

Delivery complete: 12/12 verified, zero errors; 2,162.36 seconds total. Single-season ZIP: `/workspace/elementary-season01-output/Sunny_Pip_Elementary_Season_01.zip`, 157,405,581 bytes and 207 entries, CRC/hash checks passed. Full directory and actual ZIP player both pass jsdom controls; all 84 relative media/poster assets present. Source and art reports, ep11 five-track amplitude spot check, CSV and complete media records retained beside delivery. Original preschool films/ZIPs unchanged; shared content-addressed speech cache reused.

Repeated branch/worktree/remote/open-PR collision checks before the continuation PR. The only related open PR is our own parent #1376; this continuation intentionally targets its branch so reviewers see only elementary changes. Both remain drafts and neither is merged.
