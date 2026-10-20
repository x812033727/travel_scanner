---
id: 2026-10-20-brand-story-garmin-x15
title: Brand story Garmin X15
status: in-progress
priority: P1
area: docs
owner: codex-x15
claimed_at: 2026-10-20T20:19:53Z
created_at: 2026-10-20T20:19:50Z
completed_at:
branch: codex/brand-story-garmin-x15
depends_on: []
scope:
  - docs/videos/story-everyday-garmin-x15
  - tasks/open/2026-10-20-brand-story-garmin-x15.md
---

# Brand story Garmin X15

## Why

The owner asks for another missing-brand video under the established 奇聞檔案局／brand-story rules, a reviewable PR when ready, and then the next topic. Garmin is already a verified C15 idea in the 100-topic catalogue but has no X-series production or PR. Its own SEC filings reveal a dated reversal: 2008 mobile navigation was a possible risk to the automotive/mobile business; by the 2011 Form 10-K the company said adoption had halted growth. Later revenue became spread across several businesses. The film must not claim that phones alone caused the decline or that one watch alone caused recovery.

## Definition of done

- [ ] Source-verified, independently reviewed main story with measured substantive body ≥8:00 and approximately 10-minute target, 30–45-second story turns, two standalone 25–55s Shorts, actual official 5s/21s branding, clean video with Traditional Chinese optional CC, and reviewable sources/visuals.
- [ ] Paid generation stays under the already authorized US$25 full-episode cap; links are filled only after real uploads.
- [ ] Open a draft PR only after independent source and two fresh blind narrative checks of frozen scripts and Shorts; record real media and QA limits without overstating completion.

## Steps

- [x] Confirm no duplicate Garmin X-series worktree or PR; select verified catalogue idea C15 without changing the 100-topic plan.
- [x] Fetch and hash six worker-readable SEC originals plus one oversized reviewer-only 10-K; draft source matrix, six-chapter treatment, and two standalone Short concepts.
- [x] Have an independent agent redownload originals and audit this packet against exact hashes, periods, segment denominators, and the two story concepts; fix any HOLD findings. See `reviews/source-audit-independent.md` PASS on commit `af55507e`.
- [x] Build source-tagged six-chapter main script, production JSON and two independent Shorts. v1 at `e0c97132` was HOLD in [SEC review](../../docs/videos/story-everyday-garmin-x15/reviews/script-source-audit-v1-independent.md), [blind A](../../docs/videos/story-everyday-garmin-x15/reviews/blind-a-v1-independent.md) and [blind B](../../docs/videos/story-everyday-garmin-x15/reviews/blind-b-v1-independent.md). v2 was again HOLD in [SEC review](../../docs/videos/story-everyday-garmin-x15/reviews/script-source-audit-v2-independent.md), [blind A](../../docs/videos/story-everyday-garmin-x15/reviews/blind-a-v2-independent.md) and [blind B](../../docs/videos/story-everyday-garmin-x15/reviews/blind-b-v2-independent.md). Revise to v3: `video.json` SHA-256 `c0019158d98130c1e456050f4d0f9716d4905115574b86d9fa540190dcb1b1d1`, `shorts.json` SHA-256 `b473ec1c522f5c3cb0e9239e7907d192511845d08cd51dbd6980feda5217b1fb`; video lint 0 errors/0 warnings, Shorts validator 0 problems, docs video tests 236/236 and tasks check exit 0. The next step records the v3 reviews.
- [x] v3 [independent SEC audit](../../docs/videos/story-everyday-garmin-x15/reviews/script-source-audit-v3-independent.md) PASS; [blind A](../../docs/videos/story-everyday-garmin-x15/reviews/blind-a-v3-independent.md) and [blind B](../../docs/videos/story-everyday-garmin-x15/reviews/blind-b-v3-independent.md) HOLD on the opener, repeated caveats, late division catalog and paper runtime. v4 source draft and derived files are frozen at `video.json` SHA-256 `4ada054a0a6e3c1e396e1ecc8cf8550d6ff9c0a72bab0062e29ef02c5b582e00`, `shorts.json` SHA-256 `9dc9be2a237ea6aabbd60d3268351ee16ea72daa54f0f6822e5c5990788b9d2e`; the 144-line main has 2,415 substantive body characters, paper estimate 9:37 body and 11:10 all-in with official 5s/21s branding. Video lint 0 errors/0 warnings; both standalone Shorts validate and all 18 portrait source shots have distinct centered crop targets. No paid media exists.
- [ ] Have a different agent independently verify every spoken main and Short claim against G1–G6 originals, then obtain two fresh blind narrative ballots on the exact audited hashes; repair and repeat if either finds a material problem.
- [ ] Produce and QA affordable media/animation/CC and actual links as available, then open a truthful PR and continue the next brand.

## How to verify

Read `docs/videos/story-everyday-garmin-x15/source-matrix.md`, independently HTTP-download each SEC original, and compare byte size and SHA-256 to the table. Recompute ratios from primary tables and inspect risk-factor wording in 2008/2011 10-Ks. Later use the video lint, docs tests, task validation, measured audio timeline and two independent narrative ballots bound to exact script hashes. Packet-stage documentation checks: `npm run test:docs-videos` and `npm run check:tasks`.

## Notes

2026-10-20 source-first packet lives in `docs/videos/story-everyday-garmin-x15/`. SEC downloads G1–G6 each returned HTTP 200 and are under 3 MiB; 2023 10-K is 3,683,117 bytes and therefore reviewer-only. Independent source packet audit PASS was committed as `1897396a`. 2008 automotive/mobile is broader than car navigation, and 2025 Auto OEM is not the same historical division. The 2025 total is US$7,245.519m revenue, not profit. The original C15 story/review remain unchanged. No paid generation, finished film, YouTube ID or PR exists. Official branding assets and current site music quota remain unavailable in this cloud workspace; do not fabricate them or upload links.
