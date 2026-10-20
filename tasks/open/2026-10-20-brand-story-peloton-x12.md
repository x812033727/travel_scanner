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

- [x] Inspect five SEC originals and draft a single-project Ohio story with line-source mapping, 16 loop payoffs, visual plan and two Shorts.
- [x] Compose `video.json` and `shorts.json`; schema lint 0 errors/0 warnings and per-Short validation empty.
- [ ] Another agent independently verifies every factual line and the same frozen SHA. V9 exact-SHA SEC audit passed; v10 changes factual lines and visual cues, so it needs a fresh exact-SHA audit.
- [ ] Two untouched blind readers assess the same frozen main/Shorts SHA. Genuine v9 A2 blind read held at 8/12 and clean v9 B at 11/12; v10 needs two fresh blind reads on the same new hashes.
- [ ] Price live paid stages, synthesize and time narration, review audio and keyframes, assemble/QA; only use licensed official branding and music for formal cut.
- [ ] Finish PR after content gate; update task with real video and URL status.

## How to verify

`node docs/videos/story-everyday-peloton-x12/compose-video.mjs`; `node docs/videos/story-everyday-peloton-x12/compose-shorts.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-peloton-x12`; `node --input-type=module -e 'import {readFileSync} from "node:fs"; import {validate} from "./tools/video/shorts/core.mjs"; for(const d of JSON.parse(readFileSync("docs/videos/story-everyday-peloton-x12/shorts.json"))) if(validate(d).length) process.exit(1)'`; `npm run test:docs-videos`; `npm run check:tasks`. Factual review must cite SEC originals, not this author's source matrix alone. Paid media QA remains pending.

## Notes

2026-10-20 author branch `codex/brand-story-peloton-x12`, worktree `/workspace/travel_scanner_peloton_x12`. Five SEC originals and exact downloaded SHA values remain in `docs/videos/story-everyday-peloton-x12/source-matrix.md`. [V9 source audit](../../docs/videos/story-everyday-peloton-x12/reviews/source-audit-v9-independent.md) PASS and [genuine v9 A2 blind read](../../docs/videos/story-everyday-peloton-x12/reviews/blind-a2-v9-independent.md) HOLD and [clean v9 B blind read](../../docs/videos/story-everyday-peloton-x12/reviews/blind-b-clean-v9-independent.md) HOLD apply only to v9 hashes. Current v10 candidate `video.json` SHA-256 `de57163608a389ba50093b2fe0499f4bba6dfa2415c2a4a99ff833127c89b7a0`, `shorts.json` SHA-256 `ba992f09bb766de57441c9a11c8ddbfaeda976590c2616523df0b172d52e6180`. The [v10 author note](../../docs/videos/story-everyday-peloton-x12/reviews/blind-remediation-v10.md) gives changed line IDs; historical independent receipts remain untouched. V10 has 102 lines/scenes, 93 illustrated shots and 9 native cards (91.18% illustrated), 217 opening chars, 2,496 substantive body chars (~8:19 paper at 300 cpm, ~8:35 at observed X09 291 cpm), **not actual TTS timing**. Both Short scripts have 197 chars (~47.3s paper at 250 cpm), seven/eight scenes. `shorts.json` records per-beat 9:16 crop focus, safe boxes and type scales as a **plan, not rendered verification**. No paid calls, generated media or official brand assets.

Chronology is February 2022 Ohio shell completion-then-sale **plan**; June 30 FY2022 result as later context, **not** cause proved for February; July 12 wider owned-manufacturing exit with Rexon **future** main Bike/Tread role; September K22 and FY2023 K23 still marketing/intending sale, with no completed sale or held-for-sale classification inferred. Taiwan Tonic suspension is separate from Ohio. US$400m planned, US$86.6m invested and US$40.3m impairment involving Ohio plus related manufacturing assets are distinct and none is a sale price. New independent source audit plus two fresh blind reads must pass before TTS or other paid media. The `node_modules` symlink is untracked setup and must not enter commit.
