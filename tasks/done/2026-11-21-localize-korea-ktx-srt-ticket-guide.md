---
id: 2026-11-21-localize-korea-ktx-srt-ticket-guide
title: Localize korea-ktx-srt-ticket-guide and jeju-3-day-itinerary into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-21T17:09:48Z
created_at: 2026-11-21T16:34:56Z
completed_at: 2026-11-21T17:10:52Z
branch: agy/localize-wave3c-korea-pair-batch8
depends_on: []
scope:
  - apps/api/app/guides/content/korea-ktx-srt-ticket-guide.json
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/web/public/guides/korea-ktx-srt-ticket-guide
  - apps/web/public/guides/jeju-3-day-itinerary
---

# Localize korea-ktx-srt-ticket-guide and jeju-3-day-itinerary into en, ja, ko, zh-CN (Route B)

## Why

Wave 3C Batch 8 of the Mokaair multi-locale guide localization program batches the two high-traffic Korea flagship guides (whose live `zh-TW` documents match the repository byte-for-byte) into one combined Route B PR:

1. `howto/korea-ktx-srt-ticket-guide` (live `zh-TW` v10)
2. `howto/jeju-3-day-itinerary` (live `zh-TW` v8)

Adding `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG route/itinerary diagrams unlocks 8 new indexable guide URLs across search engines and AI crawlers.

## Definition of done

- [x] Both `korea-ktx-srt-ticket-guide.json` and `jeju-3-day-itinerary.json` contain validated `en`, `ja`, `ko`, and `zh-CN` documents with `zh-TW` preserved byte-for-byte (0 deleted lines).
- [x] All 8 localized 1600×900 SVG diagrams (`diagram-1-{en,ja,ko,zh-cn}.svg` for each slug) are placed under `apps/web/public/guides/<slug>/`, visually verified in headless Chromium (fixing the original `zh-TW` top-card overflow and curve-label collisions), and have `<desc>` matching the corresponding `image` block `description` byte-for-byte.
- [x] Independent locale reviewers (`antigravity-reviewer-{en,ja,ko,zh-CN}`, distinct from translators `antigravity-translator-{en,ja,ko,zh-CN}`) audited all 8 `(slug, locale)` targets; all findings were resolved and the combined `route-b-review-v1` receipt passed `prepare_route_b_bundle.load_review` with 8/8 `PASS` and `open_findings: 0`.
- [x] `pack_cli lint`, `pytest tests/test_guides_content_pack.py`, and `docs/news-2026-batch-4/translation_checks.py` pass for both slugs.
- [x] An unclaimed follow-up release task is filed for host-side bundle preparation and publication after deploy.

## Steps

- [x] Pin live `zh-TW` baselines (`repo_hash == live_hash`) and verify live cross-article link locales for both guides.
- [x] Translate both guides and build localized 1600×900 SVGs for `en`, `ja`, `ko`, and `zh-CN`.
- [x] Render all 8 SVGs with headless Chromium and visually inspect for clipping, box overflow, curve overlaps, and CJK/Hangul glyph correctness (`Noto Sans CJK SC/JP/KR` + explicit `lang`).
- [x] Run independent per-locale reviews across all 8 targets, apply every review fix (including all `CRITICAL`/`MAJOR` findings), and re-render/re-inspect modified SVGs (`ktx-srt` `en`/`ja`/`ko`, `jeju-3day` `en`/`ja`/`zh-CN`).
- [x] Merge into both content packs, copy all 8 SVGs, run full lint/pytest/translation checks, and validate the combined `route-b-review-v1` receipt.

## How to verify

```bash
git diff apps/api/app/guides/content/ | grep -E '^-[^-]'
cd apps/api && uv run python -m app.guides.pack_cli lint --slug korea-ktx-srt-ticket-guide
cd apps/api && uv run python -m app.guides.pack_cli lint --slug jeju-3-day-itinerary
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content korea-ktx-srt-ticket-guide jeju-3-day-itinerary
npm run check:tasks
```

## Notes

### Pinned Live `zh-TW` Baselines (`repo_hash == live_hash`)

- **`korea-ktx-srt-ticket-guide`** (`howto`, live v10):
  - `source_sha256`: `a1f2009e10ef794a922f992b0be47e4fd7ecc1e28fe7a4c603b12d0fa76ce0ee`
  - Cross-article links: original `block[25]` converted to a plain `paragraph` retaining 100% of Gyeongju/Dongdaegu/Jeonju facts without unpublished cross-links; `seoul-4-day-itinerary` and `busan-3-day-itinerary` omitted; all 3 live 5-locale `article` inlines (`howto/gyeongju-day-trip-from-busan`, `howto/seoul-subway-t-money-guide`, `intel/korea-autumn-leaves-2026`) retained with exact verbatim live target-locale titles (35 blocks, 3 `article` inlines). Final 2 links localized to `/<locale>/destinations/seoul` and `/<locale>/destinations/busan`.
- **`jeju-3-day-itinerary`** (`howto`, live v8):
  - `source_sha256`: `b90731ffa49e2dd425111e9a0e7b0b12fb1f030539050ddac839c77e4855e164`
  - Cross-article links: original `block[7]` and `block[13]` converted to plain `paragraph` blocks keeping the Jeju Old City / Black Pork Street / Dongmun Market and Sehwa / Aewol cafe geographic context with zero unpublished links (33 blocks, 0 `article` inlines). Final 2 links localized to `/<locale>/destinations/jeju` and `/<locale>/foods?city=jeju`.

### Localized Deliverables & Hashes

#### `korea-ktx-srt-ticket-guide`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Seoul–Busan KTX & SRT Ticket Guide: Seoul Station vs. Suseo Station, Korail Talk & SRT App Booking, and Is the KORAIL PASS Worth It? | `940911c46443775da4c3e85d209c4f20159d742b66232c947557118b4736b17e` | `/guides/korea-ktx-srt-ticket-guide/diagram-1-en.svg` (`02cc87df753e05c5d0db21a89f2ab36b4820e77736708c2f9ad74bee795f83c7`) |
| `ja` | ソウル・釜山KTX＆SRT購入ガイド：ソウル駅と水西駅の違い、Korail Talk・SRTアプリの予約方法とKORAIL PASSが元を取れる条件 | `7104b1518c2fb642a15fb075971e35f840fb542fe6d520a60bf890c239bef525` | `/guides/korea-ktx-srt-ticket-guide/diagram-1-ja.svg` (`5a37976c5b874b150905abd44312bfc458f9b1bfd78487cdd1f940742c34d953`) |
| `ko` | 서울-부산 KTX·SRT 예매 가이드: 서울역과 수서역 선택, 코레일톡·SRT 앱 예매 방법, 코레일 패스 가성비 | `b1aacedecdd7619e8f060c316846674ab9aaa9b9e56c722b41c0293d008925e8` | `/guides/korea-ktx-srt-ticket-guide/diagram-1-ko.svg` (`16ae6c9c9ff0e112ffd7ee9c9584560f3a01e1dce9e59f18ce6d6e3eade2390c`) |
| `zh-CN` | 首尔釜山 KTX 与 SRT 购票攻略：首尔站还是水西站、Korail Talk 与 SRT App 怎么订、KORAIL PASS 划不划算 | `6fd2cb8b1dea8d712734769b1d5a5d787cca105556573beebff9e8ad43926ff7` | `/guides/korea-ktx-srt-ticket-guide/diagram-1-zh-cn.svg` (`b0a9808827dfd381606616affe6cc6630d8233606d5f2e997ab7f759953bdcee`) |

#### `jeju-3-day-itinerary`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Jeju 3-Day Itinerary: Seongsan Ilchulbong & Udo on the East Coast, Seogwipo Waterfalls or Hallasan, and Rental Car vs. Bus | `97f4034865d84744c587b928ffe9026b5d036ce84359c06bb4cce61888c041fc` | `/guides/jeju-3-day-itinerary/diagram-1-en.svg` (`a16ddbf29c067470a5fbd146913a3e064423c49a992fe3ac0025f84ca45a14a5`) |
| `ja` | 済州島2泊3日モデルコース：東海岸の城山日出峰と牛島、西帰浦の滝かハルラ山、レンタカーとバス徹底比較 | `4d00779b8deef6658eb2f30fac314eec2b624e816828d0eab09158a8166b5389` | `/guides/jeju-3-day-itinerary/diagram-1-ja.svg` (`ff6d590dfae7fbe241d8371def72552f0087f4fd7bc3d559484bc23f2e3868a8`) |
| `ko` | 제주도 2박 3일 일정 가이드: 동부 성산일출봉·우도, 서귀포 폭포와 한라산, 렌터카와 버스 선택 | `f33f7466631e51799384075a022ba795d19c1e3d465db76c61f73958a6a85e1c` | `/guides/jeju-3-day-itinerary/diagram-1-ko.svg` (`ca21936527a6f2119b5da8f31bd629d3a2b88466092e9800c9cc876ac009a921`) |
| `zh-CN` | 济州岛三天两晚怎么玩：东线城山日出峰与牛岛、西归浦瀑布或汉拿山、租车还是坐公交 | `cbf4a10526ff97c1fe21425ffa3c5e1b4e7d927eaceb51fda875231576f6a8c1` | `/guides/jeju-3-day-itinerary/diagram-1-zh-cn.svg` (`a2e2676beb4c3689d05a92214aff2b86ac4a1450663ed45ba13f366366abe9f6`) |

### Independent Review Summary & Receipt

- Combined `route-b-review-v1` receipt validated via `prepare_route_b_bundle.load_review`:
  - `evidence_sha256`: `c306c969cd00a840762960d690ff11e1773e3189dd7f1a05d395327d421bc507`
  - `review_sha256`: `1dc16df1c4353e6767b90e95587410fc8f4502ab74bfb57bc532d4c89d7d2129`
  - Targets: 8/8 `PASS`, `open_findings: 0`, distinct translators (`antigravity-translator-<locale>`) and reviewers (`antigravity-reviewer-<locale>`).
- Key independent review fixes applied before merge:
  - `en`: fixed `MAJOR` Bus 600 direction reversal (`check airport-bound departure times from Seogwipo separately`); clarified Day 1 trunk vs. express bus fare (`₩1,150` trunk); broadened `priority passengers (such as seniors and travelers with disabilities)`; aligned SRT fare heading (`x="390"`) and shifted `Jungmun Tourist Complex` cleanly below the island outline in SVGs.
  - `ja`: fixed two `MAJOR` Jeju issues—replaced fabricated kanji `摂支コジ` with official `ソプチコジ` across JSON and SVG, and corrected `飲食持込不可` → `食べ物持込不可` in Jeju SVG; replaced `安全ドア` → `ホームドア`, `延伸ルート` → `周辺都市へのアクセス`, qualified `台湾外交部`, unified polite `です・ます` checklist, and refined SVG line-name delimiters.
  - `ko`: fixed `MAJOR` Bus 600 direction reversal (`서귀포 출발(공항 방면) 시각은`); fixed `배차 간격이 넉넉하지 않고` → `배차가 뜸하고`; disambiguated trunk vs. express bus fares; scoped overseas IDP/passport checklist; aligned `승객 유형` terminology and SVG legend parentheses.
  - `zh-CN`: fixed `CRITICAL` verbatim live title match for `intel/korea-autumn-leaves-2026` (`汉拏山` matching live target title byte-for-byte); replaced residual `机台` → `自助机`, `便利店` → `商店`, `交会` → `交汇`, `直达西归浦` → `到西归浦` (Bus 600 vs direct Bus 800); lifted `灵室 5.8 km` cleanly above the Day 3 badge in Jeju SVG and re-verified in Chromium.
