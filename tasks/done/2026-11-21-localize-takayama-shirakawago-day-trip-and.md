---
id: 2026-11-21-localize-takayama-shirakawago-day-trip-and
title: Localize takayama-shirakawago-day-trip and nikko-day-trip-from-tokyo into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-21T10:32:30Z
created_at: 2026-11-21T10:31:07Z
completed_at: 2026-11-21T11:05:42Z
branch: agy/localize-wave3c-japan-daytrips-batch6
depends_on: []
scope:
  - apps/api/app/guides/content/takayama-shirakawago-day-trip.json
  - apps/api/app/guides/content/nikko-day-trip-from-tokyo.json
  - apps/web/public/guides/takayama-shirakawago-day-trip
  - apps/web/public/guides/nikko-day-trip-from-tokyo
---

# Localize takayama-shirakawago-day-trip and nikko-day-trip-from-tokyo into en, ja, ko, zh-CN (Route B)

## Why

Wave 3C Batch 6 of the Mokaair multi-locale guide localization program batches the two remaining Japan day-trip flagship guides whose live `zh-TW` document matches the repository (`repo_hash == live_hash`) into a single Route B PR:

1. `howto/takayama-shirakawago-day-trip` (live `zh-TW` v8)
2. `howto/nikko-day-trip-from-tokyo` (live `zh-TW` v8)

Both were previously published only in `zh-TW`. Adding `en`, `ja`, `ko`, and `zh-CN` content packs plus localized 1600×900 SVG route diagrams unlocks 8 new indexable guide URLs across search engines and AI crawlers.

## Definition of done

- [x] Both `takayama-shirakawago-day-trip.json` and `nikko-day-trip-from-tokyo.json` contain validated `en`, `ja`, `ko`, and `zh-CN` documents with `zh-TW` preserved byte-for-byte (0 deleted lines).
- [x] All 8 localized route diagram SVGs (`diagram-1-{en,ja,ko,zh-cn}.svg` for each slug) are placed under `apps/web/public/guides/<slug>/`, visually verified in headless Chromium at 1600×900, and have `<desc>` matching the corresponding `diagram` block `description` byte-for-byte.
- [x] Independent locale reviewers (`antigravity-reviewer-{en,ja,ko,zh-CN}`, distinct from translators `antigravity-translator-{en,ja,ko,zh-CN}`) audited all 8 `(slug, locale)` targets; all findings were resolved and the combined `route-b-review-v1` receipt passed `prepare_route_b_bundle.load_review` with 8/8 `PASS` and `open_findings: 0`.
- [x] `pack_cli lint`, `pytest tests/test_guides_content_pack.py`, and `docs/news-2026-batch-4/translation_checks.py` pass for both slugs.
- [x] An unclaimed follow-up release task is filed for host-side bundle preparation and publication after deploy.

## Steps

- [x] Pin live `zh-TW` baselines (`repo_hash == live_hash`) and check live cross-article link availability for both guides.
- [x] Translate both guides and build localized 1600×900 SVGs for `en`, `ja`, `ko`, and `zh-CN`.
- [x] Render all 8 SVGs with headless Chromium and visually inspect for clipping, overlaps, and CJK glyph correctness (`Noto Sans CJK SC/JP/KR` + explicit `lang`).
- [x] Run independent per-locale reviews across all 8 targets, apply every review fix, and re-render/re-inspect modified SVGs (`takayama` `en`/`ja`, `nikko` `zh-CN`).
- [x] Merge into both content packs, copy all 8 SVGs, run full lint/pytest/translation checks, and validate the combined `route-b-review-v1` receipt.

## How to verify

```bash
git diff apps/api/app/guides/content/ | grep -E '^-[^-]'
cd apps/api && uv run python -m app.guides.pack_cli lint --slug takayama-shirakawago-day-trip
cd apps/api && uv run python -m app.guides.pack_cli lint --slug nikko-day-trip-from-tokyo
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content takayama-shirakawago-day-trip nikko-day-trip-from-tokyo
npm run check:tasks
```

## Notes

### Pinned Live `zh-TW` Baselines (`repo_hash == live_hash`)

- **`takayama-shirakawago-day-trip`** (`howto`, live v8):
  - `source_sha256`: `20d77a324bb70643f4324219ee875738d6e16a2bb4b13aec213d7a0fa1ed60da`
  - Cross-article links: all 4 `zh-TW` article links (`kanazawa-2-day-itinerary`, `nagoya-3-day-itinerary`, `japan-shinkansen-ticket-guide`, `japan-onsen-ryokan-guide`) are `zh-TW`-only live and omitted in target locales (29 blocks, 0 `article` inlines). Final 2 links localized to `/<locale>/destinations/nagoya` and `/<locale>/foods?city=nagoya`.
- **`nikko-day-trip-from-tokyo`** (`howto`, live v8):
  - `source_sha256`: `fe813e51ec6f7615a7ce4254b47e422adc40f83379c4ebbe6d4450661401e1e7`
  - Cross-article links: `howto/tokyo-transit-passes` is live in all 5 locales and retained at `block[7]` with each locale's exact verbatim title; the other 3 `zh-TW`-only article links (`japan-autumn-leaves-2026`, `tokyo-5-day-itinerary`, `kamakura-enoshima-day-trip`) are omitted (27 blocks, 1 `article` inline). Final link localized to `/<locale>/destinations/tokyo`.
  - Note: Legacy unclaimed ticket `2026-10-06-batch-005-nikko-kyoto-translations-refresh` tracked `nikko-day-trip-from-tokyo` alongside `kyoto-bus-subway-guide`; `nikko-day-trip-from-tokyo` is now localized against live `zh-TW` v8 here while `kyoto-bus-subway-guide` remains for that ticket.

### Localized Deliverables & Hashes

#### `takayama-shirakawago-day-trip`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Takayama & Shirakawa-go from Nagoya: JR Hida or Highway Bus, Nohi Bus Reservations, Day Trip vs. Overnight, and 2027 Illumination Rules | `81676cadda894bf145e79fb77513b09fe2198a47b192872cd528e65def2eb30d` | `/guides/takayama-shirakawago-day-trip/diagram-1-en.svg` (`1ab4fb5f0543a3e2b1b602cda29293e7dacc5ed14f4c563ba77a7cd7b34ef6d2`) |
| `ja` | 名古屋発・高山・白川郷完全ガイド：JR特急ひだ・高速バスの選び方、濃飛バスの全便予約、日帰りか1泊2日か、2027年ライトアップ予約ルール | `e1c32f4048720a3697c009916f6c61716c685bff26f6914ba5ab29a2c3c8cda0` | `/guides/takayama-shirakawago-day-trip/diagram-1-ja.svg` (`9cd7f56424368fe4df2d443b2acffefda3d2e9ea100e4c1975204218b42d7957`) |
| `ko` | 나고야 출발 다카야마·시라카와고 여행 가이드: JR 특급 히다와 고속버스 비교, 노히버스 전 편 예약, 당일치기 vs 1박 2일, 2027년 라이트업 규칙 | `933958a08eaf1449c1a54a32144639c18131dc95f1b740ad7ec4044269c7649b` | `/guides/takayama-shirakawago-day-trip/diagram-1-ko.svg` (`edc69c315783f28728be2b44fdca8443ef4972d106d4662ba6eebee113aa5e6b`) |
| `zh-CN` | 名古屋出发高山＋白川乡攻略：JR 特急ひだ 还是高速巴士、浓飞巴士全班预约、一日二选一还是两天一夜、2027 年点灯规则 | `7737aa80a69bcfa51ebbea93851eec4564247bb787b51619a4ea3482927c5c9b` | `/guides/takayama-shirakawago-day-trip/diagram-1-zh-cn.svg` (`6d16e6bb2553d005338d314fcf17643fc86c2146bd3c17207bb500d69375dcf2`) |

#### `nikko-day-trip-from-tokyo`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Nikko Day Trip from Tokyo: Tobu Limited Express from Asakusa, Choosing a NIKKO PASS, and the Bus Route from Toshogu to Lake Chuzenji & Kegon Falls | `6710fd9e114838264417ad02bbae50f13b01d153d530b598aa5af2332b8d6f61` | `/guides/nikko-day-trip-from-tokyo/diagram-1-en.svg` (`cfa4605186605797d88b46d0c89ea720f0b4673b1f55ab714e42d8ad26387823`) |
| `ja` | 日光日帰り旅行ガイド：浅草発の東武特急、NIKKO PASSの選び方、東照宮から中禅寺湖・華厳の滝へのバスルート | `76d89f3103775ea70c8abb8aadf591d858147d02efea3bf9bbbc5369629fb07e` | `/guides/nikko-day-trip-from-tokyo/diagram-1-ja.svg` (`a7e7eb63b0482046bf4c67af3e7e97f901e92bc7339cfb05dedc3f1a2826bd4f`) |
| `ko` | 도쿄 근교 닛코 당일치기 가이드: 아사쿠사 도부 특급, 닛코 패스 선택법, 닛코 도쇼구에서 주젠지 호수·게곤 폭포 버스 동선 | `578510e8f969d739ea451ee993b0149a44dcf5c28b2aad7a511d0841b5140d3a` | `/guides/nikko-day-trip-from-tokyo/diagram-1-ko.svg` (`5c1b7bdc260628de29e40c6551371c4616dd88a259407ea64501b351c6a103e6`) |
| `zh-CN` | 日光一日游攻略：浅草坐东武特急、NIKKO PASS 怎么选、东照宫到中禅寺湖华严瀑布的巴士路线 | `8e8ee2086c290910ba46cf87a1086732e301c5831d01097ebef865ea8e4187f5` | `/guides/nikko-day-trip-from-tokyo/diagram-1-zh-cn.svg` (`374418fe75d1315b47fbb8f977eebb9fb3bf24debfb89be0fe0403ce8b64282d`) |

### Independent Review Summary & Receipt

- Combined `route-b-review-v1` receipt validated via `prepare_route_b_bundle.load_review`:
  - `evidence_sha256`: `185a302d520ebabdaf19e37d6ac1a748c0ece8524a042da6c23d1119203f2649`
  - `review_sha256`: `eeb24d2e006265bee6f7e1a0b6bfedfe2ec1e1ad80aa91fe855160b10b8db4de`
  - Targets: 8/8 `PASS`, `open_findings: 0`, distinct translators (`antigravity-translator-<locale>`) and reviewers (`antigravity-reviewer-<locale>`).
- Key independent review fixes applied before merge:
  - `en`: clarified `private/rental cars or taxis` for Shirakawa-go illumination parking; expanded `12/day each way` and `Reservation required` in Takayama SVG; clarified `regular rail + limited express tickets` for the Nikko day-trip recommendation and `Standard Kegon and Revaty Kegon trains`.
  - `ja`: aligned bus frequency to `1日12往復` across Takayama body/table/description/SVG; corrected `拝観料` → `入館料` for Wada House; unified H2 nominal register and rail fare wording (`乗車には乗車券と特急券が必要で`); clarified Kegon Falls elevator depth as `地下100m`, unified `華厳滝エレベーター`, and added `通常の乗車券・特急券` in Nikko day-trip wording.
  - `ko`: fixed Korean particle `'특급 티켓리스 하야토쿠3'은`, village office `시라카와촌 사무소`, official pier reading `후네노에키 주젠지`, consistent Tobu portal name `도부치케`, `비수기` seasonal wording, and `1박하다` spacing.
  - `zh-CN`: fixed `MAJOR-1` in Nikko day-trip recommendation to explicitly include mandatory round-trip base fare (`基础车费 2,800 日元`) alongside `特急券` and clarify NIKKO PASS separate `特急券` requirement; updated Nikko H2 to canonical `二社一寺`; replaced leftover `票券` in Takayama offer heading with `通票`; removed hybrid Simplified+kana pass names; clarified `SPACIA X 1 号 / 12 号`; shifted `轮王寺 Rinnoji` node in Nikko SVG for balanced inner box padding and re-verified in Chromium.
