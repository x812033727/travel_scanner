---
id: 2026-10-01-youtube-narration-language-consumer
title: Align YouTube language consumer with narration locale
status: done
priority: P1
area: api
owner: codex-narration-consumer
claimed_at: 2026-10-01T10:25:29Z
created_at: 2026-10-01T10:24:54Z
completed_at: 2026-10-01T10:42:20Z
branch: codex/branding-cc-prompt-20261001
depends_on: []
scope:
  - apps/api/app/video_youtube/language_package.py
  - apps/api/tests/test_video_youtube_language_package.py
---

# Align YouTube language consumer with narration locale

## Why

Main's narration-locale packaging preserves the original narration and zh-TW
automatically. The API language consumer still treats every selected locale as
foreign, drops zh-TW from English narration packages, and requires a duplicate
English synthesized dub or an English localization for original metadata.

## Definition of done

- [x] Explicit language choices preserve approved original narration and zh-TW assets.
- [x] Original metadata stays immutable and an own-narration dub needs no extra track.
- [x] Source identities, compact choices and attachment hashes remain strict.

## Steps

- [x] Audit active worktrees, remote branches and open PRs before a narrow claim.
- [x] Implement narration-aware composition and positive/tamper regressions.
- [x] Validate focused/affected API checks and actual Node-emitted English bytes.

## How to verify

Run focused language package pytest and affected renewal/review/sync/VPS pytest
with `-p no:cacheprovider`, ruff and mypy. Offline Node narrationFixture exports
must pass the real Python compose consumer for none, foreign-only and own-locale
choices, with rehashed original-text and duplicate-dub tampering refused.

## Notes

Root authorized this narrow compatibility fix on the shared branding branch.
Fresh audit: branch codex/branding-cc-prompt-20261001 at 089c20a01f2426b5f188a3ddd71c9392ad9a7f7f;
origin/main b03e938e0a6185b0c5f0d3b66e3ce30c63146576. No active worktree or
remote language/narration branch and no open PR touches these two consumer files.
The only claim refusal was the historical 2026-09-30-youtube-approved-languages-sync
scope. Its PR #1048 is MERGED at 2026-10-01T02:20:49Z and its branch has no active
worktree/open PR. Root explicitly authorized forcing only this own new claim;
the historical task and original producer work remain untouched.
No live/API/media requests, credential reads or commits are authorized here.

Final verification at 2026-10-01 10:40 UTC: standalone language package pytest
48 passed; affected language/long-renewal/review-renewal/reviews/sync/VPS set
177 passed, both with `-p no:cacheprovider`. Scoped ruff and mypy (2 files) pass.
Root full ruff passes; full mypy app (447 files) and tests (340 files) pass, with
logs in `C:/Users/x8120/mokaair-work/channel-intro-20260930/brand-package-v2-cc/rollout/compat-{ruff,mypy-app,mypy-tests}.log`.
Task check validates 1244 files with existing stale/overlap warnings; independent
branding_architecture read review reports no major or blocking finding.

Consumer SHA256: 74b8abfa8baa1e69cf9c7876015d08b21b6907c77c796e36fd76fb8f12887ecb.
Test SHA256: 51c649f95efbd8f921bb9f6a81ae43dc140b76fdb605c97b3c39baa9d0c30517.
Actual Node producer SHA256: 25226ae410ec8f75f8b5cd61158d617c41ca47036fc14410ae3ae606cc1bd379.
Offline English proof: 5 real-byte acceptances, 42 consumer refusals (source,
choices, files, rehashed original text/timeline and native dub tampering), plus
4 producer refusals with zero uploaded attachments; no unexpected outcome.
Fresh zh-TW proof: 85 scenarios, 83 consumer calls (9 accept / 74 reject), plus
2 producer refusals. All five positive manifest/review/attachment bytes are
identical to the prior R3 receipt.
Compact receipt:
`C:/Users/x8120/.codex/visualizations/2026/09/30/01a0efc3-57f6-7da3-b4d0-51c50a0304af/contract-probe-20261001/r4-compatibility-summary.json`
SHA256 3c7f3b95457ee76f866432de53e0f9fac0883cd84ac8d342a7e9f1a193b40cc1.
Its immutable referenced reports are r4-en/narration-consumer-report.json
(a2cc9f698a53dd3ace9d3e4406a069c7d53181946ed52024e7486b311ca77671)
and r4-zhTW/consumer-report.json
(dbe18428bda963dae43a48dfa41f26c674884c6c87061692405aef458d75235f).

Package acceptance does not establish English YouTube upload acceptance:
requests.py still hardcodes zh-TW transport defaults/localization filtering.
Root requested an unclaimed follow-up, 2026-10-01-youtube-narration-request-transport;
this narrow patch does not modify request transport. Current 17 renewal sources
are zh-TW and remain unaffected by that boundary.
