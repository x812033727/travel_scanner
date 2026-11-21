---
id: 2026-11-21-localize-seoul-4-day-itinerary-into
title: Localize seoul-4-day-itinerary into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-21T04:18:42Z
created_at: 2026-11-21T04:18:08Z
completed_at: 2026-11-21T04:50:36Z
branch: agy/localize-wave3c-seoul-batch3
depends_on: []
scope:
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/web/public/guides/seoul-4-day-itinerary
---

# Localize seoul-4-day-itinerary into en, ja, ko, zh-CN (Route B)

## Why

`seoul-4-day-itinerary` (`kind: howto`) is Mokaair's flagship Seoul itinerary guide that was previously published only in `zh-TW` (live v12, normalized `source_sha256: 92a89aee443596da96a98ca0d8c29966a85707b52c430dbe0f038a65b9a94b2c`, matching repo bytes). Adding `en`, `ja`, `ko`, and `zh-CN` expands organic search and AI-answer visibility across four international locales as Wave 3C Batch 3 of the frontend exposure rescue program.

## Definition of done

- [x] All five locales (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) validate cleanly against `GuideDocument` with 37 localized blocks (40 source blocks minus 3 `zh-TW`-only promo/link blocks), 20 sources, and localized 1600×900 SVG schematic area maps (`diagram-1-{en,ja,ko,zh-cn}.svg`).
- [x] `zh-TW` document and original assets (`hero.jpg`, `photo-1.webp`, `photo-2.webp`, `diagram-1.svg`) are byte-identical to baseline (`92a89aee443596da96a98ca0d8c29966a85707b52c430dbe0f038a65b9a94b2c`, zero deleted lines in `seoul-4-day-itinerary.json`).
- [x] Every target locale underwent independent translation (`antigravity-translator-<loc>`) and separate independent text + rendered-SVG review (`antigravity-reviewer-<loc>`), with all findings fixed (`open_findings: 0`) and hash-bound in a validated `route-b-review-v1` receipt (`sha256: 23ffafc1feaf6b493dc5c259be5043157d92a1a350641d7065166bd8e6f0cf19`).
- [x] Cross-article links keep `intel/korea-autumn-leaves-2026` with exact verbatim published target-locale titles, convert/omit all 15 `zh-TW`-only slugs per Route B policy, and localize destination/food links to `/<locale>/destinations/seoul` and `/<locale>/foods?city=seoul`.
- [x] `pack_cli lint --slug seoul-4-day-itinerary` exits 0 with zero errors; `pytest tests/test_guides_content_pack.py` and `translation_checks.py` pass cleanly.
- [x] Follow-up unclaimed release ticket filed with `depends_on` pointing to this task.

## Steps

- [x] Pin live `zh-TW` v12 document from `mokaair.com` and confirm `repo_hash == live_hash` (`92a89aee…`).
- [x] Produce `en`, `ja`, `ko`, and `zh-CN` documents and localized 1600×900 SVGs via four separate translator subagents.
- [x] Render all four SVGs via headless Chromium and run four independent reviewer subagents.
- [x] Apply all reviewer text and SVG geometry fixes (Romanization, polite-form consistency, AREX wording accuracy, Day 2 arrow/stroke clearance, Han River label placement, Gyeongchun/ITX-Cheongchun station clarity, `en.description` <= 500 chars), re-render, and visually inspect all four PNGs.
- [x] Validate `route-b-review-v1` receipt via `prepare_route_b_bundle.load_review`, merge into content pack, copy SVGs, and pass lint/tests/translation checks.
- [x] File unclaimed follow-up release task for host publication.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug seoul-4-day-itinerary
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content seoul-4-day-itinerary
npm run check:tasks
```

## Notes

- **Pinned `zh-TW` source**: live version `12`, normalized `source_sha256`: `92a89aee443596da96a98ca0d8c29966a85707b52c430dbe0f038a65b9a94b2c`.
- **Localized documents & SVG assets**:
  - `en`: `4-Day Seoul Itinerary: Gyeongbokgung Hanbok Entry, Bukchon Curfew, Nami Island Day Trip, Hongdae, Seongsu & Han River` — `document_sha256`: `2a0fb8741e340213d34741df5d4ac240dd3de9a9717bf8781debe4c4decc790c`; `diagram-1-en.svg`: `f5387a5f10625285a5d5071bfaa55c35de89287a5b586f61ae9e15884732aa1a`
  - `ja`: `ソウル3泊4日モデルコース：景福宮の韓服無料入場・北村の時間制限・南怡島日帰り・弘大と聖水・漢江` — `document_sha256`: `7e35b675a33e5477dcf01a62d8bf53b0b4a3206c66f761160be6a1ab77762f5e`; `diagram-1-ja.svg`: `f72e288b9fab2c6b58233de3920f495fce122e4214bb14e77c6cb26d09de5fed`
  - `ko`: `서울 3박 4일 여행 코스: 경복궁 한복 무료입장, 북촌 관광 시간 제한, 남이섬 당일치기, 홍대·성수·한강` — `document_sha256`: `674f79f6986c651a73903e214ae2934c35e3087c4e5165955803a3eff9034958`; `diagram-1-ko.svg`: `a7c887c19b02627a9080564183c3ed4cf80d3a15a0357220e52bb3eeed39e769`
  - `zh-CN`: `首尔四天三晚行程攻略：景福宫韩服免门票、北村时段限制、南怡岛一日、弘大圣水汉江` — `document_sha256`: `2c553935668cd8a81af3bcdbe34c1adc1ead850e59ba917ca21f14564793560a`; `diagram-1-zh-cn.svg`: `b7e16618fd1749c009e468df36efbcae5066a42f6c2bcb2fcbe7cc69dd61360e`
- **Independent review highlights**:
  - `en`: fixed `Hwaseong Eocha` spelling, tightened `description` cleanly under 500 chars (`421` chars), polished `curated boutiques` and `travel times and fares`, widened Day 2/Day 4A badge clearance, shifted Han River label cleanly below bank, unified `·` dots and solid Day 2 arrows.
  - `ja`: unified checklist items to polite `です／ます`, fixed `1エリアに絞って回りましょう`, `現実的な回り方としては`, `四幅パジ（韓服ズボン）`, `龍山駅発着`, enlarged Day badges to `r="30"`, shifted Han River label below bank, unified Japanese `〜`/`／` punctuation.
  - `ko`: fixed `AREX 일반열차 직통` contradiction (`일반열차로 환승 없이 이동`), fixed `출국 시` / `인천국제공항으로` / `이삼 일` / `편집숍`, aligned `경춘선(상봉·청량리) · ITX-청춘(용산역)`, trimmed airport arrow and Day 2 red arrows cleanly clear of box/circle strokes.
  - `zh-CN`: shifted Han River label to `y="732"` cleanly clear of the river band, trimmed Day 2 red arrowheads cleanly clear of card borders, unified `·` middle dots, aligned `京春线（上凤·清凉里）/ ITX-청춘（龙山站）`, and tightened `description` (`仅至 17:00`) and table phrasing.
- **Work artifacts**: kept outside the repository in the session's persistent scratch directory (`route-b-review-v1` receipt `sha256: 23ffafc1feaf6b493dc5c259be5043157d92a1a350641d7065166bd8e6f0cf19`, `evidence_sha256: e5f0b1d9ff6e2efbfb06da1709ee54cba47b88aa6eda61c353a5fa7b90669e34`).
- **Lint warnings retained intentionally**: `no_summary` across all 5 locales and `text_length` on `en` (10,671 chars); per `article-localization` rules, source structure is preserved and translated prose is not trimmed to silence `text_length`.
