---
id: 2026-11-21-localize-da-nang-hoi-an-4
title: Localize da-nang-hoi-an-4-day-itinerary into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-21T05:00:41Z
created_at: 2026-11-21T04:59:34Z
completed_at: 2026-11-21T05:29:36Z
branch: agy/localize-wave3c-danang-batch4
depends_on: []
scope:
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
  - apps/web/public/guides/da-nang-hoi-an-4-day-itinerary
---

# Localize da-nang-hoi-an-4-day-itinerary into en, ja, ko, zh-CN (Route B)

## Why

`da-nang-hoi-an-4-day-itinerary` (`kind: howto`) is Mokaair's flagship Central Vietnam itinerary guide that was previously published only in `zh-TW` (live v10, normalized `source_sha256: cef37cac40c3be0921e18fc51e91169ec06783562744e029c0e1fd72b95f8fec`, matching repo bytes). Adding `en`, `ja`, `ko`, and `zh-CN` expands organic search and AI-answer visibility across four international locales as Wave 3C Batch 4 of the frontend exposure rescue program.

## Definition of done

- [x] All five locales (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) validate cleanly against `GuideDocument` with 27 localized blocks (31 source blocks minus 4 `zh-TW`-only standalone link blocks), 20 sources, and localized 1600×900 SVG route zone maps (`diagram-1-{en,ja,ko,zh-cn}.svg`).
- [x] `zh-TW` document and original assets (`hero.jpg`, `photo-1.webp`, `photo-2.webp`, `diagram-1.svg`) are byte-identical to baseline (`cef37cac40c3be0921e18fc51e91169ec06783562744e029c0e1fd72b95f8fec`, zero deleted lines in `da-nang-hoi-an-4-day-itinerary.json`).
- [x] Every target locale underwent independent translation (`antigravity-translator-<loc>`) and separate independent text + rendered-SVG review (`antigravity-reviewer-<loc>`), with all findings fixed (`open_findings: 0`) and hash-bound in a validated `route-b-review-v1` receipt (`sha256: 8061ab34924470e809e238a370844698eb3a3a55bea52d6c95c987dcf344b05a`).
- [x] All 7 `zh-TW`-only cross-article references are cleanly converted to plain prose or omitted per Route B policy, while destination and food-directory links resolve to `/<locale>/destinations/da-nang` and `/<locale>/foods?city=da-nang`.
- [x] `pack_cli lint --slug da-nang-hoi-an-4-day-itinerary` exits 0 with zero errors; `pytest tests/test_guides_content_pack.py` and `translation_checks.py` pass cleanly.
- [x] Follow-up unclaimed release ticket filed with `depends_on` pointing to this task.

## Steps

- [x] Pin live `zh-TW` v10 document from `mokaair.com` and confirm `repo_hash == live_hash` (`cef37cac…`).
- [x] Produce `en`, `ja`, `ko`, and `zh-CN` documents and localized 1600×900 SVGs via four separate translator subagents.
- [x] Render all four SVGs via headless Chromium and run four independent reviewer subagents.
- [x] Apply all reviewer text and SVG geometry fixes (US English `elevator`/`standard fare`, Japanese `旧市街の夜` & `〜` punctuation, Korean `투이선 봉우리` & `인파가 몰리기 전에`, Simplified Chinese `交通车票`/`国内到达区` & widened Day 4 Marble Mountains card + lowered Airport→Hoi An label), re-render, and visually inspect all four PNGs.
- [x] Validate `route-b-review-v1` receipt via `prepare_route_b_bundle.load_review`, merge into content pack, copy SVGs, and pass lint/tests/translation checks.
- [x] File unclaimed follow-up release task for host publication.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug da-nang-hoi-an-4-day-itinerary
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content da-nang-hoi-an-4-day-itinerary
npm run check:tasks
```

## Notes

- **Pinned `zh-TW` source**: live version `10`, normalized `source_sha256`: `cef37cac40c3be0921e18fc51e91169ec06783562744e029c0e1fd72b95f8fec`.
- **Localized documents & SVG assets**:
  - `en`: `Da Nang & Hoi An 4-Day Itinerary: Airport Transfers, Ba Na Hills Golden Bridge, Hoi An Tickets & Marble Mountains` — `document_sha256`: `75ae13a06d21901e96ef563001ac915dd3ced24e9c593bbc1007be7cb2fa097e`; `diagram-1-en.svg`: `422eda54d4fb4a543bed392b12b3df0a067adcfb77227ecf86ca5c37fa01f004`
  - `ja`: `ダナン・ホイアン3泊4日モデルコース：空港アクセス、バーナーヒルズのゴールデンブリッジ、ホイアン旧市街チケットと五行山の回り方` — `document_sha256`: `6967d5b92646a1d1ba9755150770212bf0c9ef085141005cefbd570e04b83c20`; `diagram-1-ja.svg`: `53ac4feee9d9e71c0e8e6fdb83fe3a81d4cae6bbcc5cf65951d5aec9a1a4df4b`
  - `ko`: `다낭·호이안 3박 4일 완벽 가이드: 공항에서 시내·호이안 이동, 바나힐 골든브리지, 호이안 올드타운 입장권과 오행산 코스 총정리` — `document_sha256`: `eba86a7b96ca8f1419396cf4ffaafce25a0430bbf5e2cafb624b0e0052be4675`; `diagram-1-ko.svg`: `6b4c8250036231fa9a7965bdcc7442f747f3d64b3ec3007e44567f9029f5fc4f`
  - `zh-CN`: `岘港会安四天三晚攻略：机场到市区与会安、巴拿山黄金桥、会安古城门票与五行山怎么排` — `document_sha256`: `490a5843f74849cafe12d26103565793a8d647d9d32c311561a7d9532154ce19`; `diagram-1-zh-cn.svg`: `0dd8de8ce27744ec35ddbe3b043dbc2017160eb3bfe528d0782efeffd2eed81a`
- **Independent review highlights**:
  - `en`: aligned `elevator` and `standard fare` wording across SVG and prose, clarified Day 4 three-way choice in table, tightened table caption & 4 source titles cleanly under 200 chars, gave Hoi An ticket line extra margin inside Day 3 card.
  - `ja`: changed `古鎮の夜` → `旧市街の夜`, fixed `非常に至近` → `非常に近い`, unified `〜` and `・` separators across SVG, trimmed legend dash stub.
  - `ko`: fixed `투이선 봉우리·후옌콩 동굴` ambiguity, generalized `단체 관광객` → `인파`, clarified `한강(Sông Hàn)`, unified `Sun World 바나힐` and `~` time range, raised `다낭 공항 DAD` label for extra clearance.
  - `zh-CN`: widened Day 4 Marble Mountains card (`width="370"`, `font-size="20"`) to eliminate border contact, moved `机场 → 会安 29 km · 约 50 分钟` cleanly down to `y="595"`, fixed `交通票券` → `交通车票` and `国内线入境区` → `国内到达区`, unified `乘` verb phrasing.
- **Work artifacts**: kept outside the repository in the session's persistent scratch directory (`route-b-review-v1` receipt `sha256: 8061ab34924470e809e238a370844698eb3a3a55bea52d6c95c987dcf344b05a`, `evidence_sha256: 56db5f7a931285e49d3a1800d6edf7cc4c22473b72eeab3ef64ed479bf90e193`).
- **Lint warnings retained intentionally**: `no_summary` across all 5 locales and `text_length` on `en` (10,501 chars); per `article-localization` rules, source structure is preserved and translated prose is not trimmed to silence `text_length`.
