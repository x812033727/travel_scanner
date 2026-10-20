---
id: 2026-10-20-brand-story-peloton-x12
title: Brand story Peloton X12
status: in-progress
priority: P1
area: docs
owner: codex-x12
claimed_at: 2026-10-20T19:25:53Z
created_at: 2026-10-20T19:25:50Z
completed_at:
branch: codex/brand-story-peloton-x12
depends_on: []
scope:
  - docs/videos/story-everyday-peloton-x12
  - tasks/open/2026-10-20-brand-story-peloton-x12.md
---

# Brand story Peloton X12

## Why

The user wants the next missing brand-story film after X11 in the 奇聞檔案局 look. Peloton's Ohio Output Park is a source-backed reversal: a 2021 multiyear US$400m plan for a factory intended to start production in 2023 became a facility Peloton was marketing for sale in the FY2022 and FY2023 SEC filings. The story must keep plan, expenditure and sale status separate while taking a main film and two Shorts through full production.

## Definition of done

- [ ] A source-verified, two-reader narrative-approved long-form script and two standalone 25–55s Shorts, with reproducible JSON and source links.
- [ ] An actual film with ≥8:00 substantive body after excluding hook, closing three lines and official 5s/21s animations, plus reviewed MiniMax illustrations, music, Sulafat narration and removable zh-TW CC.
- [ ] Total paid work including retries, Shorts, audio QA and tax ≤US$25; YouTube IDs and clickable Studio elements are only marked complete after real upload.

## Steps

- [x] Inspect five SEC originals and draft a single-project Ohio story with line-source mapping, 15 loop payoffs, visual plan and two Shorts.
- [x] Compose `video.json` and `shorts.json`; schema lint 0 errors/0 warnings and per-Short validation empty.
- [ ] Another agent independently verifies every factual line and the same frozen SHA. V4 has an independent source PASS; v5 changes need same-hash delta review.
- [ ] Two untouched blind readers assess the same frozen main/Shorts SHA. Two v4 blinds gave mandatory NO for payoff and recap; v5 requires two new blind reviews.
- [ ] Price live paid stages, synthesize and time narration, review audio and keyframes, assemble/QA; only use licensed official branding and music for formal cut.
- [ ] Finish PR after content gate; update task with real video and URL status.

## How to verify

`node docs/videos/story-everyday-peloton-x12/compose-video.mjs`; `node docs/videos/story-everyday-peloton-x12/compose-shorts.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-peloton-x12`; `node --input-type=module -e 'import {readFileSync} from "node:fs"; import {validate} from "./tools/video/shorts/core.mjs"; for(const d of JSON.parse(readFileSync("docs/videos/story-everyday-peloton-x12/shorts.json"))) if(validate(d).length) process.exit(1)'`; `npm run test:docs-videos`; `npm run check:tasks`. Factual review must cite SEC originals, not this author's source matrix alone. Paid media QA remains pending.

## Notes

2026-10-20 author branch `codex/brand-story-peloton-x12`, worktree `/workspace/travel_scanner_peloton_x12`. Five SEC URLs, exact downloaded SHA values and caveats in `docs/videos/story-everyday-peloton-x12/source-matrix.md`. Current v5 candidate `video.json` SHA-256 `1c1383dfb4f0db37607b12cd181e7b432bd12b4968dcd7073109042301ca0b3e`, `shorts.json` SHA-256 `01deabd137e928f9f6070053730c0fdc2b07e71eaf472aaefb20c6c1ea4a428b`. Historical v1–v4 source and blind receipts remain byte-for-byte in `docs/videos/story-everyday-peloton-x12/reviews/`; v5 factual, narrative and visual deltas are in `reviews/blind-remediation-v5.md`. V4 source PASS applies **only to v4 hashes**; both v4 blind reads failed. V5 has 112 lines/scenes, 99 illustrated shots and 13 native cards; 207 hook chars and 2,557 body chars (paper estimate ~10:14 at 250 cpm; ~8:31 at 300 cpm), **not actual TTS timing**. At X09's observed 291 cpm, that is ~8:47 substantive body. Short scripts 195/172 chars (~46.8s/~41.3s paper) and 9:16 numeric overlays on physical shots. No paid calls, no generated media or official brand assets. FY2022 ends 2022-06-30; 2022-07-12 owned-manufacturing exit is **after** that year-end. `Rexon` announced as future main Bike/Tread maker and Taiwan `Tonic` suspension must never become Ohio closure; FY2023 still marketing/intend-to-sell, not sale or accounting held-for-sale. US$400m planned vs US$86.6m invested vs US$40.3m impairment involving Ohio and related manufacturing assets; none is sale price. Source and two-new-blind gate before TTS. The `node_modules` symlink in the worktree is untracked setup and must not enter commit.
