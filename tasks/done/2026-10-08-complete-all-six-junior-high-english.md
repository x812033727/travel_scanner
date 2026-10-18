---
id: 2026-10-08-complete-all-six-junior-high-english
title: Complete all six junior high English seasons
status: done
priority: P2
area: tools
owner: codex-junior-high-complete
claimed_at: 2026-10-08T02:33:45Z
created_at: 2026-10-08T02:33:36Z
completed_at: 2026-10-08T03:49:22Z
branch: codex/junior-high-english-complete-20261008
depends_on: []
scope:
  - tools/video/junior_high
  - docs/videos/english-junior-high-complete
---

# Complete all six junior high English seasons

## Why

The user requested continuation through the complete junior-high English series after receiving preschool and elementary courses. Deliver six seasons of twelve lessons, two per grade (7–9), with contextual grammar, guided reading and speaking, independent reading questions, and short writing tasks.

## Definition of done

- [x] All 72 lessons have complete five-language teaching scripts and four translated CC sources, with coherent progression and independently reviewed worksheets.
- [x] All 72 films, 360 standalone audio masters, four CC languages, and English embedded in the picture pass source-bound timing, integrity and full-decode checks.
- [x] Six season ZIPs and a combined ZIP contain verified offline players, catalogs and printable reading/writing practice.
- [x] Appropriate repository checks and independent delivery review pass; the source/tools/evidence are committed and a draft continuation PR is opened.

## Steps

- [x] Inspect current environment, task ownership, local/worktree branches, remote heads and open PRs; claim isolated paths and branch from the completed elementary series.
- [x] Define grade progression, 72 topics, media/language contract and independent worksheet structure.
- [x] Author and cross-review six complete seasons; freeze each before audio production.
- [x] Build and visually verify the junior-high renderer, source-bound pipeline and worksheet layouts.
- [x] Produce all five-language audio and all 72 films, preserving prior course sources and media.
- [x] Verify every film, all seven packages and player variants; complete documentation and draft PR.

## How to verify

- `npm run test:tools` and `npm run check:tasks`; meaningful pipeline failure/source-admission regressions.
- New `junior_high/verify_series.py` against current authoring and all 72 output episodes, including measured shared English demonstrations, response intervals, exact CC, current renderer and full-decode SHA receipts.
- Independent art checks: layout bounds, before-reveal answer invariance, guided text pixel preservation and actual encoded-film samples.
- Worksheet source/answer consistency, PDF text/page counts and visual samples; independent ZIP CRC/member-SHA/player-asset/catalog/caption checks.
- jsdom controls for all 72 episodes and each standalone twelve-episode season. Actual browser playback is separately identified as unverified under the already observed local-file administrator policy.

## Notes

- Output: `/workspace/junior-high-series-output`; all media, font files and voice caches remain outside the public repository. Existing preschool, elementary S1 and complete elementary sources/tools/media remain unchanged.
- This continues the user's adopted 3–5 minute English lesson format, with ten scenes and independent written activities; it is separate from the generic 8-minute technology-explainer format in the video skill. No fresh format permission is needed for the authorized series continuation.
- Contract: five audio tracks (en, zh-TW, zh-CN, ja, ko), the same original English demonstrations in each, four translated CC tracks and no English CC; English is fixed in the picture. Five-second ordinary response intervals and six-second quiz intervals are retained.
- Video choice activities are explicitly guided listening/reading practice. Each worksheet adds a level-appropriate original passage, three independently answerable questions, and one writing task with separate example answers. The series does not claim to replace a region's complete school curriculum or certify proficiency.
- Voices remain Microsoft Edge read-aloud trial voices. No backend production credentials/capabilities are configured; this work produces the agreed local deliverables and does not publish videos.
- Current cloud environment is ready, network policy enforced/unrestricted, no VPN, no configured production secrets. Keep inherited proxy and CA settings. Previously blocked real-browser local-file access is not retried through a bypass.
- The new branch is based on elementary completion commit `800df37f0ad1492610bfeb9e72d32c990e3d3202` and will target `codex/elementary-english-complete-20261008` (draft PR #1380). Related open work consists only of our parent PRs #1376, #1377 and #1380; no competing junior-high task or PR was found.

- Delivery completed 2026-10-08: 72/72 current-source films verified, total 14,687.891 seconds (4:04:48), with 360 M4A, 288 SRT and 288 VTT files. All films have SHA-bound full-decode receipts.
- Independent delivery audit passed all seven ZIP CRCs, exact member lists (209 per season / 1229 combined), per-file hashes, actual media streams, catalogs, all reading/writing fields and PDF pages. Combined ZIP: 1,224,416,404 bytes. Practice: 72 readings, 216 questions, 72 writing tasks; 97 combined PDF pages / 17 per season.
- All 720 scenes / 2,160 phase frames passed artwork checks. Actual encoded frames from ep24/36/48/60/72 were separately inspected; the coordinating agent also viewed ep01 and ep72. These are selected-frame checks, not a claim of complete audiovisual viewing.
- All seven player variants passed mocked jsdom controls. Real-browser playback remains unverified under the previously observed administrator local-file policy; no alternate-route workaround was attempted.
- Local checks: npm run test:tools exited 0 (2013 total, 2010 passed, 3 skipped); 23 junior-high Python pipeline regressions rerun on final authoring and passed. npm run check:tasks passed before the delivery commit and is repeated after this final task closure.
- Final authoring SHA: f499f5313c32246f397f0b525574047c525c978d2ae21b5d614a962822c320eb. Portable delivery, authoring, artwork and selected-frame evidence lives in the new documentation directory. Existing course source/tool paths have no diff from the parent commit.
- Draft continuation PR: https://github.com/x812033727/travel_scanner/pull/1381, based on codex/elementary-english-complete-20261008 (#1380). The task closure is the final PR commit per the task-board skill. CI status is tracked on the PR; no merge, backend voice integration, video upload or publication was performed.
