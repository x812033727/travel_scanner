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
- [ ] Another agent independently verifies every factual line and the same frozen SHA. V10 exact-SHA SEC audit passed for the previous candidate; v11 adds source-backed scenes and changes factual lines, so it needs a fresh exact-SHA audit.
- [ ] Two untouched blind readers assess the same frozen main/Shorts SHA. Genuine fresh v10 blind A/B reads failed at 8/12 and 10/12; v11 needs two new blind reads on its own hashes.
- [ ] Price live paid stages, synthesize and time narration, review audio and keyframes, assemble/QA; only use licensed official branding and music for formal cut.
- [ ] Finish PR after content gate; update task with real video and URL status.

## How to verify

`node docs/videos/story-everyday-peloton-x12/compose-video.mjs`; `node docs/videos/story-everyday-peloton-x12/compose-shorts.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-peloton-x12`; `node --input-type=module -e 'import {readFileSync} from "node:fs"; import {validate} from "./tools/video/shorts/core.mjs"; for(const d of JSON.parse(readFileSync("docs/videos/story-everyday-peloton-x12/shorts.json"))) if(validate(d).length) process.exit(1)'`; `npm run test:docs-videos`; `npm run check:tasks`. Factual review must cite SEC originals, not this author's source matrix alone. Paid media QA remains pending.

## Notes

2026-10-20 author branch `codex/brand-story-peloton-x12`, worktree `/workspace/travel_scanner_peloton_x12`. Five SEC originals and exact downloaded SHA values remain in `docs/videos/story-everyday-peloton-x12/source-matrix.md`. [V10 exact-SHA SEC audit](../../docs/videos/story-everyday-peloton-x12/reviews/source-audit-v10-independent.md) PASS, but fresh [blind A](../../docs/videos/story-everyday-peloton-x12/reviews/blind-a-v10-independent.md) 8/12 and [blind B](../../docs/videos/story-everyday-peloton-x12/reviews/blind-b-v10-independent.md) 10/12 both failed narrative. They apply only to v10 hashes. Current frozen v11 candidate `video.json` SHA-256 `c66ea0f17970f19d4a3b3a9df4e26286dcc4872f2258beb83a294026c26013b9`, `shorts.json` SHA-256 `8602834e0e4d4baa09267c191492307b90dc823360ad69fc4af17ef0b9ba6f1d`; [v11 author note](../../docs/videos/story-everyday-peloton-x12/reviews/blind-remediation-v11.md) gives changed line IDs. V11 has 96 lines/scenes, 90 illustrated shots and 6 native cards (93.75% illustrated), 237 opening characters, 2,660 substantive body characters (~8:52 paper at 300 cpm, ~9:08 at observed X09 291 cpm), **not actual TTS timing**. Short 1/2 have 197/181 characters (~47.3/43.4s paper at 250 cpm), seven scenes each. `shorts.json` records per-beat native 9:16 recomposition, safe boxes and type scales as a **plan, not rendered verification**. No paid calls, generated media or official brand assets.

Chronology is 2021 Precor-already-owned Ohio expansion puzzle and supply strain; February 2022 Ohio shell completion-then-sale **plan**; June 30 FY2022 result as later context, **not** cause proved for February; July 12 wider owned-manufacturing exit with Rexon **future** main Bike/Tread role; September K22 still marketing/intending sale; FY2023 K23 says sale **has experienced delays** and disposal work **has caused** operational disruption, still marketing/intending sale. No completed sale or held-for-sale classification is inferred. Taiwan Tonic suspension is separate from Ohio. US$400m planned, US$86.6m invested and US$40.3m impairment involving Ohio plus related manufacturing assets are distinct and none is a sale price. New independent source audit plus two fresh blind reads must pass before TTS or other paid media. The `node_modules` symlink and root-level untracked `reviews/` are unrelated setup and must not enter commit.
