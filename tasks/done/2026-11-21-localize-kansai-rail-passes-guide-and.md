---
id: 2026-11-21-localize-kansai-rail-passes-guide-and
title: Localize kansai-rail-passes-guide and osaka-kyoto-nara-4-day-itinerary into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-21T15:00:16Z
created_at: 2026-11-21T15:00:15Z
completed_at: 2026-11-21T15:35:35Z
branch: agy/localize-wave3c-kansai-pair-batch7
depends_on: []
scope:
  - apps/api/app/guides/content/kansai-rail-passes-guide.json
  - apps/api/app/guides/content/osaka-kyoto-nara-4-day-itinerary.json
  - apps/web/public/guides/kansai-rail-passes-guide
  - apps/web/public/guides/osaka-kyoto-nara-4-day-itinerary
---

# Localize kansai-rail-passes-guide and osaka-kyoto-nara-4-day-itinerary into en, ja, ko, zh-CN (Route B)

## Why

Wave 3C Batch 7 of the Mokaair multi-locale guide localization program batches the two high-traffic Kansai flagship guides (whose live `zh-TW` v8 documents match the repository byte-for-byte) into one combined Route B PR:

1. `howto/kansai-rail-passes-guide` (live `zh-TW` v8)
2. `howto/osaka-kyoto-nara-4-day-itinerary` (live `zh-TW` v8)

Adding `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG diagrams (decision tree + Kansai triangle travel-time map) unlocks 8 new indexable guide URLs across search engines and AI crawlers.

## Definition of done

- [x] Both `kansai-rail-passes-guide.json` and `osaka-kyoto-nara-4-day-itinerary.json` contain validated `en`, `ja`, `ko`, and `zh-CN` documents with `zh-TW` preserved byte-for-byte (0 deleted lines).
- [x] All 8 localized 1600×900 SVG diagrams (`diagram-1-{en,ja,ko,zh-cn}.svg` for each slug) are placed under `apps/web/public/guides/<slug>/`, visually verified in headless Chromium (fixing the original `zh-TW` box-overflow and label-collision issues), and have `<desc>` matching the corresponding `image` block `description` byte-for-byte.
- [x] Independent locale reviewers (`antigravity-reviewer-{en,ja,ko,zh-CN}`, distinct from translators `antigravity-translator-{en,ja,ko,zh-CN}`) audited all 8 `(slug, locale)` targets; all findings were resolved and the combined `route-b-review-v1` receipt passed `prepare_route_b_bundle.load_review` with 8/8 `PASS` and `open_findings: 0`.
- [x] `pack_cli lint`, `pytest tests/test_guides_content_pack.py`, and `docs/news-2026-batch-4/translation_checks.py` pass for both slugs.
- [x] An unclaimed follow-up release task is filed for host-side bundle preparation and publication after deploy.

## Steps

- [x] Pin live `zh-TW` baselines (`repo_hash == live_hash`) and verify live cross-article link locales for both guides.
- [x] Translate both guides and build localized 1600×900 SVGs for `en`, `ja`, `ko`, and `zh-CN`.
- [x] Render all 8 SVGs with headless Chromium and visually inspect for clipping, box overflow, track-line grazing, and CJK glyph correctness (`Noto Sans CJK SC/JP/KR` + explicit `lang`).
- [x] Run independent per-locale reviews across all 8 targets, apply every review fix, and re-render/re-inspect modified SVGs (`kansai-passes` `en`/`zh-CN`, `osaka-kyoto-nara` `en`/`ja`).
- [x] Merge into both content packs, copy all 8 SVGs, run full lint/pytest/translation checks, and validate the combined `route-b-review-v1` receipt.

## How to verify

```bash
git diff apps/api/app/guides/content/ | grep -E '^-[^-]'
cd apps/api && uv run python -m app.guides.pack_cli lint --slug kansai-rail-passes-guide
cd apps/api && uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content kansai-rail-passes-guide osaka-kyoto-nara-4-day-itinerary
npm run check:tasks
```

## Notes

### Pinned Live `zh-TW` Baselines (`repo_hash == live_hash`)

- **`kansai-rail-passes-guide`** (`howto`, live v8):
  - `source_sha256`: `88de29318908fd9b1a607322c2456483636086f3a6eae8d73cb1bb0d3c2962cc`
  - Cross-article links: `howto/kansai-airport-to-osaka-kyoto` is live in all 5 locales and retained at `block[27]` with each locale's exact verbatim title; the other 6 `zh-TW`-only article blocks (`kanazawa-2-day-itinerary`, `kyoto-bus-subway-guide`, `japan-ic-card-suica-icoca-guide`, `osaka-kyoto-nara-4-day-itinerary`, `himeji-castle-day-trip`, `kobe-arima-day-trip`) are omitted (29 blocks, 1 `article` inline). Final link localized to `/<locale>/destinations/osaka-kyoto`.
- **`osaka-kyoto-nara-4-day-itinerary`** (`howto`, live v8):
  - `source_sha256`: `dbfed6f33456622b99e16d1a7e1d219d5ce566343e75660aac33670baede4507`
  - Cross-article links: 29 blocks, 0 `article` inlines. Final 2 links localized to `/<locale>/destinations/osaka-kyoto` and `/<locale>/foods?city=osaka-kyoto`.
  - Upstream note (from all independent reviewers): `zh-TW` itself writes `四天三夜` in `title`/`blocks[1]` alongside `住大阪四晚` / `前兩晚住京都、後兩晚住大阪` in `description`/`blocks[0]`/`blocks[3]`/`blocks[5]`; all four target locales faithfully mirror `zh-TW` without altering source numbers (leaving any upstream `zh-TW` copy refresh to existing unclaimed P3 ticket `2026-10-06-itinerary-osaka-kyoto-nara-full-recheck`).

### Localized Deliverables & Hashes

#### `kansai-rail-passes-guide`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | How to Choose a Kansai Rail Pass: JR West Passes, Osaka Amazing Pass, KANSAI RAILWAY PASS LITE & Day Passes (Sep 2026 Fares & Decision Tree) | `74c1eae0515df9c01333aff6b0132e8dc7abe3dceaa7d2bc0283bcbbc76bad83` | `/guides/kansai-rail-passes-guide/diagram-1-en.svg` (`152ebc73cd527833a6308f4632f4de10afd168970c6b4e2517fd70241fd70e57`) |
| `ja` | 関西の交通パス選び方ガイド：JR関西エリアパス、大阪周遊パス、KANSAI RAILWAY PASS LITE、各社1日券を徹底比較（2026年9月料金・選び方フローチャート付） | `7664ed12cbcd6bce8640e6807dba8be812343d5ffff3e802eb3ab4a917703cca` | `/guides/kansai-rail-passes-guide/diagram-1-ja.svg` (`a234d632c25e869171a0729a65ba95ff9de898f2348d73eaa19a5984bd8bd73d`) |
| `ko` | 간사이 교통 패스 선택 가이드: JR 간사이 에어리어 패스, 오사카 주유패스, KANSAI RAILWAY PASS LITE, 각 노선 1일권 비교(2026년 9월 요금·선택 트리) | `949a367b4247b208a9d3f22fd8b5f53b9163465dfc0de8f83db836d020e9c94a` | `/guides/kansai-rail-passes-guide/diagram-1-ko.svg` (`b86a74331fb8b9909e01ba199db7434aaa177e7e4a36f6edd84e209524ed48b8`) |
| `zh-CN` | 关西交通通票怎么选：JR 关西地区铁路周游券、大阪周游卡、KANSAI RAILWAY PASS LITE 与各家一日券（2026 年 9 月票价与决策图） | `6ff317318cb5a46ccf91d12678853d7d0cc294acf4b939956c8467ef6c8cf2ff` | `/guides/kansai-rail-passes-guide/diagram-1-zh-cn.svg` (`dc3357808d6ce1ce69d81d532cf7cd35e77e39d5fb174358a00e68c3d6b8beed`) |

#### `osaka-kyoto-nara-4-day-itinerary`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Osaka, Kyoto, and Nara 4-Day Itinerary: A First-Timer’s Route for Kansai | `c3d49b3ed3193446cf2d21fd44ed403b98b1e0feaa4d86bdea35b9f068d5d140` | `/guides/osaka-kyoto-nara-4-day-itinerary/diagram-1-en.svg` (`dd86cfca222867dd119ec4fa2e319667a8d6fcabc353e0b7ec7037f40e15b16f`) |
| `ja` | 大阪・京都・奈良3泊4日モデルコース：初めての関西旅行に最適な回り方 | `299fc08a05bf4f4cc6b766510e2d923ba614feedfaf50e6c29d15c2c414ec8f7` | `/guides/osaka-kyoto-nara-4-day-itinerary/diagram-1-ja.svg` (`5b75fb783149f404299421dad6b021a52ed7b36fdeca0b461f8ec1938f07e87f`) |
| `ko` | 오사카·교토·나라 3박 4일 일정 추천: 처음 가는 간사이 여행 코스 | `8124b54dc4da0e9b60376bf5119f979c83dcae4c0b8f255870f8e294147c7408` | `/guides/osaka-kyoto-nara-4-day-itinerary/diagram-1-ko.svg` (`080431b579bbcd1b4c0d57106deefae5c4a95998fdf06a0648c3ad429733cd08`) |
| `zh-CN` | 大阪、京都、奈良四天三晚行程范例：第一次去关西这样排 | `62005772dbbd12878088450e3618cff313d7abe79c20f46933ce61623f166f63` | `/guides/osaka-kyoto-nara-4-day-itinerary/diagram-1-zh-cn.svg` (`0fcb6ca04249fa31d7eaa6cf188cf7709d5e872106a1c9cf22eb07d8e13b4d66`) |

### Independent Review Summary & Receipt

- Combined `route-b-review-v1` receipt validated via `prepare_route_b_bundle.load_review`:
  - `evidence_sha256`: `345ef52c1630b7fe676e18a11618e0871b15aaedff567ecd475af1f370b376b2`
  - `review_sha256`: `54463afc9650b9cdd617ef120f8e1907319ad895664c296bb8cd0d62c434c376`
  - Targets: 8/8 `PASS`, `open_findings: 0`, distinct translators (`antigravity-translator-<locale>`) and reviewers (`antigravity-reviewer-<locale>`).
- Key independent review fixes applied before merge:
  - `en`: standardized all clock times to US 12-hour AM/PM (`5:30 PM`, `9:00 PM`, `7:30 AM–5:30 PM`, `8:00 AM–5:00 PM`, `9:00 AM–6:00 PM`); replaced `"JR Pass"` heading shorthand with `"a JR West Pass"`; harmonized `Hankyu Hanshin` and `Kyoto Subway & Bus 1-Day Pass`; shifted Kyoto–Nara label box and expanded `Kintetsu Rapid Express / Express ~35 min` in Osaka SVG and re-verified in Chromium.
  - `ja`: corrected callout title to `鉄道会社をまたいでの利用は不可`; replaced `旧関西周遊カード` calque with official `旧KANSAI THRU PASS`; updated pre-2009 `近鉄難波駅` to official `大阪難波駅` (`Osaka Metroなんば駅`); generalized `帰国便` → `帰りの便`; unified `公式料金`/`紙の乗車券（磁気券）`; shifted Osaka–Nara & Kyoto–Nara SVG boxes clear of teal track borders and re-verified in Chromium.
  - `ko`: fixed `MAJOR` break-even ride count mistranslation (`하루에 왕복 두 번` → `하루에 왕복 한 번(총 2회)`); replaced plumbing false friend `배관 시간 안내` → `관람 시간 안내`; unified polite `해요체` (`~묵을까요?`, `~필요할까요?`); generalized `별도 교통 패스는 필요 없어요` and harmonized station naming (`오사카난바역`, `긴테쓰나라역`).
  - `zh-CN`: restored `的` in `2026 年 10 月 6 日的起价` to remove effective-date ambiguity; tightened `出发前买好` / `明确说明`; added consistent spacing and `日元` unit on the 4-price JR Kansai Area Pass card in `diagram-1-zh-cn.svg` and re-verified in Chromium.
