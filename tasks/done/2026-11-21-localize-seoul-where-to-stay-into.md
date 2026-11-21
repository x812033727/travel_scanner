---
id: 2026-11-21-localize-seoul-where-to-stay-into
title: Localize seoul-where-to-stay into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-21T06:19:51Z
created_at: 2026-11-21T06:18:35Z
completed_at: 2026-11-21T10:14:15Z
branch: agy/localize-wave3c-seoul-stay-batch5
depends_on: []
scope:
  - apps/api/app/guides/content/seoul-where-to-stay.json
  - apps/web/public/guides/seoul-where-to-stay
---

# Localize seoul-where-to-stay into en, ja, ko, zh-CN (Route B)

## Why

`seoul-where-to-stay` (`kind: howto`) is Mokaair's flagship Seoul neighborhood accommodation guide that was previously published only in `zh-TW` (live v6, normalized `source_sha256: 288e9bc10a2b14dc8f34aa31316168befb1f224fade50b13b5865b541c810cd0`, matching repo bytes). Adding `en`, `ja`, `ko`, and `zh-CN` pairs directly with `seoul-4-day-itinerary` and `incheon-airport-to-seoul` to capture high-intent Seoul accommodation queries across all five locales as Wave 3C Batch 5 of the frontend exposure rescue program.

## Definition of done

- [x] All five locales (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) validate cleanly against `GuideDocument` with 1-to-1 parity across all 30 blocks, 8 sources, and localized 1600×900 SVG area-and-airport-transit maps (`diagram-1-{en,ja,ko,zh-cn}.svg`).
- [x] `zh-TW` document and original assets (`hero.jpg`, `photo-1.webp`, `photo-2.webp`, `diagram-1.svg`) are byte-identical to baseline (`288e9bc10a2b14dc8f34aa31316168befb1f224fade50b13b5865b541c810cd0`, zero deleted lines in `seoul-where-to-stay.json`).
- [x] Every target locale underwent independent translation (`antigravity-translator-<loc>`) and separate independent text + rendered-SVG review (`antigravity-reviewer-<loc>`), with all findings fixed (`open_findings: 0`) and hash-bound in a validated `route-b-review-v1` receipt (`sha256: 824f94ae224a75db5b89e901ec5aea4dfc00bb886fb9920f9a0d2eecc0bb1c7b`).
- [x] `block[21]` keeps `howto/incheon-airport-to-seoul` with exact verbatim published target-locale titles; `block[28]`/`block[29]` localize to `/<locale>/destinations/seoul` and `/<locale>/foods?city=seoul`; Taiwan-only carrier framing in `block[24]`/`block[25]` is generalized cleanly.
- [x] `pack_cli lint --slug seoul-where-to-stay` exits 0 with zero errors; `pytest tests/test_guides_content_pack.py` and `translation_checks.py` pass cleanly.
- [x] Follow-up unclaimed release ticket filed with `depends_on` pointing to this task.

## Steps

- [x] Pin live `zh-TW` v6 document from `mokaair.com` and confirm `repo_hash == live_hash` (`288e9bc1…`).
- [x] Produce `en`, `ja`, `ko`, and `zh-CN` documents and localized 1600×900 SVGs via four separate translator subagents.
- [x] Render all four SVGs via headless Chromium and run four independent reviewer subagents.
- [x] Apply all reviewer text and SVG geometry/glyph fixes (`en` Hongdae card & AREX clearance + `min` uniformity, `ja` Bus `6001／6015` arc clearance above Hongdae card + Line 1 label placement + explicit noise phrasing, `ko` Line 1 label separation + `#arrowOrange` `refX="10"` border clearance + `맛집 목록`, `zh-CN` `lang="zh-CN"` + `'Noto Sans CJK SC'` glyph fix for `门`), re-render, and visually inspect all four PNGs.
- [x] Validate `route-b-review-v1` receipt via `prepare_route_b_bundle.load_review`, merge into content pack, copy SVGs, and pass lint/tests/translation checks.
- [x] File unclaimed follow-up release task for host publication.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug seoul-where-to-stay
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content seoul-where-to-stay
npm run check:tasks
```

## Notes

- **Pinned `zh-TW` source**: live version `6`, normalized `source_sha256`: `288e9bc10a2b14dc8f34aa31316168befb1f224fade50b13b5865b541c810cd0`.
- **Localized documents & SVG assets**:
  - `en`: `Where to Stay in Seoul: Myeongdong, Hongdae, Gangnam, Dongdaemun & Jongno — Airport Transit, Late Check-In & Luggage` — `document_sha256`: `ad1545bffea60391ab4a7c6967dea0182103f19af419e89b313c486e45b504ff`; `diagram-1-en.svg`: `e9843ffb7fea1fe2fc438320dcb3b09f1cef785f0bdd8fb07b1df282d1ecaeb9`
  - `ja`: `ソウル宿泊エリア比較：明洞・弘大・江南・東大門・鐘路の空港アクセス、深夜チェックインと荷物配送` — `document_sha256`: `fb4de3b1c5ecf628d801a682d3683d1aaa419a0d97c016e99119edbef916f918`; `diagram-1-ja.svg`: `f4ac3abd6ee33d0cf43f4c929ef079c16def8a8e69090e57197148c6914854ec`
  - `ko`: `서울 숙소 어디로 잡을까? 명동·홍대·강남·동대문·종로 비교, 공항 교통과 심야 체크인·짐 배송 정리` — `document_sha256`: `06b5d54c6dd4d879eb8cfe7ca12c8c499951eb40da8b6c8db44c9e9eb764df8d`; `diagram-1-ko.svg`: `0b038c575db2c27624f13b5668dd83d73f1f3071dbc7e64e94a2cb4000d27620`
  - `zh-CN`: `首尔住哪一区：明洞、弘大、江南、东大门、钟路对比，机场交通、深夜入住与行李配送` — `document_sha256`: `360459d8aedae36d4e2579f10e99650ee76616e80343b16596892511bedd2cff`; `diagram-1-zh-cn.svg`: `87e312296773121bbb57b35d1eb1e0d929df93cea5694e1d113ed43ba67667b5`
- **Independent review highlights**:
  - `en`: aligned `No specific hotel picks (rates vary by season)` in `description`, fixed `Nearby` for Yeonnam-dong and `in the middle of the night`, changed `boutique hotels` to `small-to-midsize hotels`, raised Hongdae card 8 px and AREX labels 4 px for breathing room, standardized `min` across district cards.
  - `ja`: raised Bus `6001／6015` dashed arc cleanly above Hongdae card and shifted Line 1 label into open right space, aligned `約60分／約65分` and `・` separators, removed unbacked `清涼里`, tightened explicit noise warnings and polite `絞り込みましょう` / `昼間ははるかに静かです`.
  - `ko`: moved `1호선 → 종각` cleanly right of the dotted Line 1 connector to eliminate crossing with the orange bus curve, set `#arrowOrange` `refX="10"` and trimmed all four orange bus endpoints cleanly outside borders, refined `낮에는 훨씬 조용하고` and `서울 맛집 목록`.
  - `zh-CN`: added `lang="zh-CN" xml:lang="zh-CN"` and `'Noto Sans CJK SC'` so `门` and Simplified glyphs render in authentic SC forms rather than JP fallback, removed unbacked `清凉里` in SVG, polished `坐深夜巴士最直接的区域`.
- **Work artifacts**: kept outside the repository in the session's persistent scratch directory (`route-b-review-v1` receipt `sha256: 824f94ae224a75db5b89e901ec5aea4dfc00bb886fb9920f9a0d2eecc0bb1c7b`, `evidence_sha256: 9c9154fd80d69da74d224423a2e74ed1965ff43582ab2dc60b41e1e47a2691f4`).
- **Lint warnings retained intentionally**: `no_summary` across all 5 locales and `text_length` on `en` (11,878 chars); per `article-localization` rules, source structure is preserved and translated prose is not trimmed to silence `text_length`.
