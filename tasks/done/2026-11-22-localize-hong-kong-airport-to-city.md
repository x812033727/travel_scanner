---
id: 2026-11-22-localize-hong-kong-airport-to-city
title: Localize hong-kong-airport-to-city and japan-car-rental-expressway-guide into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-22T01:13:00Z
created_at: 2026-11-22T01:10:46Z
completed_at: 2026-11-22T01:51:47Z
branch: agy/localize-wave3c-hk-jpcar-batch9
depends_on: []
scope:
  - apps/api/app/guides/content/hong-kong-airport-to-city.json
  - apps/api/app/guides/content/japan-car-rental-expressway-guide.json
  - apps/web/public/guides/hong-kong-airport-to-city
  - apps/web/public/guides/japan-car-rental-expressway-guide
---

# Localize hong-kong-airport-to-city and japan-car-rental-expressway-guide into en, ja, ko, zh-CN (Route B)

## Why

Wave 3C Batch 9 of the Mokaair multi-locale guide localization program batches two high-traffic flagship transport guides (whose live `zh-TW` v8 documents match the repository byte-for-byte) into one combined Route B PR:

1. `howto/hong-kong-airport-to-city` (live `zh-TW` v8)
2. `howto/japan-car-rental-expressway-guide` (live `zh-TW` v8)

Adding `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG diagrams unlocks 8 new indexable guide URLs across search engines and AI crawlers.

## Definition of done

- [x] Both `hong-kong-airport-to-city.json` and `japan-car-rental-expressway-guide.json` contain validated `en`, `ja`, `ko`, and `zh-CN` documents with `zh-TW` preserved byte-for-byte (0 deleted lines).
- [x] All 8 localized 1600×900 SVG diagrams (`diagram-1-{en,ja,ko,zh-cn}.svg` for each slug) are placed under `apps/web/public/guides/<slug>/`, visually verified in headless Chromium (fixing the original `zh-TW` A11 Causeway Bay / North Point collision and adapting Japan licensing steps cleanly per audience), and have `<desc>` matching the corresponding `image` block `description` byte-for-byte.
- [x] Independent locale reviewers (`antigravity-reviewer-{en,ja,ko,zh-CN}`, distinct from translators `antigravity-translator-{en,ja,ko,zh-CN}`) audited all 8 `(slug, locale)` targets; all findings were resolved and the combined `route-b-review-v1` receipt passed `prepare_route_b_bundle.load_review` with 8/8 `PASS` and `open_findings: 0`.
- [x] `pack_cli lint`, `pytest tests/test_guides_content_pack.py`, and `docs/news-2026-batch-4/translation_checks.py` pass for both slugs.
- [x] An unclaimed follow-up release task is filed for host-side bundle preparation and publication after deploy.

## Steps

- [x] Pin live `zh-TW` baselines (`repo_hash == live_hash`) and verify live cross-article link locales for both guides.
- [x] Translate both guides and build localized 1600×900 SVGs for `en`, `ja`, `ko`, and `zh-CN`.
- [x] Render all 8 SVGs with headless Chromium and visually inspect for clipping, box overflow, label collisions, and CJK/Hangul glyph correctness (`Noto Sans CJK SC/JP/KR` + explicit `lang`).
- [x] Run independent per-locale reviews across all 8 targets, apply every review fix, and re-render/re-inspect all modified SVGs (`hk-airport` `en`/`ja`, `jp-car` `en`/`ja`/`ko`/`zh-CN`).
- [x] Merge into both content packs, copy all 8 SVGs, run full lint/pytest/translation checks, and validate the combined `route-b-review-v1` receipt.

## How to verify

```bash
git diff apps/api/app/guides/content/ | grep -E '^-[^-]'
cd apps/api && uv run python -m app.guides.pack_cli lint --slug hong-kong-airport-to-city
cd apps/api && uv run python -m app.guides.pack_cli lint --slug japan-car-rental-expressway-guide
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content hong-kong-airport-to-city japan-car-rental-expressway-guide
npm run check:tasks
```

## Notes

### Pinned Live `zh-TW` Baselines (`repo_hash == live_hash`)

- **`hong-kong-airport-to-city`** (`howto`, live v8):
  - `source_sha256`: `a007983a571ef7df3014b8673a503297b8ae2693e2dd03b774afc83c9139b04f`
  - Cross-article links: omitted Taiwan-specific departure/return links (`taoyuan-airport-departure-guide`, `return-to-taiwan-customs-duty-free-guide`) and `zh-TW`-only `hong-kong-4-day-itinerary`; converted original `block[42]` (Sheung Wan Macau Ferry Terminal geographic note) to a plain `paragraph`; retained live 5-locale `howto/hong-kong-ferry-tram-day` with exact verbatim target-locale titles (45 blocks, 1 `article` inline). Final 2 links localized to `/<locale>/destinations/hong-kong` and `/<locale>/foods?city=hong-kong`.
- **`japan-car-rental-expressway-guide`** (`howto`, live v8):
  - `source_sha256`: `689e7d89692f05c33efc49d8ad3d964179ddb8fd97c5b25859b0d04e7c6af51e`
  - Cross-article links: omitted `zh-TW`-only `okinawa-car-rental-guide` and `japan-ski-season-2026-2027`; retained all 3 live 5-locale `article` inlines (`howto/sapporo-3-day-itinerary`, `howto/fukuoka-3-day-itinerary`, `howto/jeju-car-rental-guide`) with exact verbatim target-locale titles (38 blocks, 3 `article` inlines). Final 2 links localized to `/<locale>/destinations/sapporo` and `/<locale>/destinations/fukuoka`.
  - Audience-accurate licensing framing: `en` and `ko` lead with 1949 Geneva Convention IDP + home license + passport alongside the 6 designated translation-track jurisdictions; `ja` addresses domestic Japanese license holders plus inbound visitors; `zh-CN` explicitly warns that China Mainland driver's licenses (including translation certificates) are not recognized in Japan while detailing both legal paths and preserving 100% of `zh-TW` facts/fees/sources.

### Localized Deliverables & Hashes

#### `hong-kong-airport-to-city`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Hong Kong Airport to the City: Airport Express & Group Tickets, A21/A11 Buses, S1 + Tung Chung Line, and Taxis | `09cf25777de54af2cbb8f65329db1798f520dbdda85fa379b99e0becea48dc86` | `/guides/hong-kong-airport-to-city/diagram-1-en.svg` (`6a8be134d47b2303e5fdca00b9219cb388758e42bda53d54cfd6e05443edb3c1`) |
| `ja` | 香港国際空港から市内へのアクセス完全ガイド：エアポート・エクスプレス運賃とグループチケット、A21・A11バス、S1＋東涌線、3色タクシーの選び方 | `eea1d6c3a30629818dc6b2b8993a1713d455439356b40b7ed00c5993298729ea` | `/guides/hong-kong-airport-to-city/diagram-1-ja.svg` (`b47bfa124a5cebbef8cb1108dcaad6cf19e4ebab6905bf8c34c94a9fb3244a9d`) |
| `ko` | 홍콩 공항에서 시내 가는 법 총정리: 공항철도(AEL) 요금과 단체권, A21·A11 버스, S1+퉁청선 환승, 3색 택시 선택 가이드 | `ad119bbf36467f58da8a9689686153912ee994b5fc204d6983d506de34b0ec1e` | `/guides/hong-kong-airport-to-city/diagram-1-ko.svg` (`d477fddbbe78ca923fb57e3e0196cdae5fb62fc5f775b18f599c76c7be36c39c`) |
| `zh-CN` | 香港机场到市区交通攻略：机场快线票价与团体票、A21/A11 巴士、S1 转东涌线、红绿蓝出租车怎么选 | `3a5f9b260e9b2e64f1418a51a28d6e0c4b9c63c022a9da38137634c1dfbb606d` | `/guides/hong-kong-airport-to-city/diagram-1-zh-cn.svg` (`82978ad93765c421ca1d48e5243adbef5f1c16b0d993739bbb984ee3dfe79442`) |

#### `japan-car-rental-expressway-guide`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Driving and Renting a Car in Japan: Licenses (IDP vs. Japanese Translation), Insurance, ETC, Expressway Passes, Winter Driving, and Fines (2026) | `1a81e9d334b9af6cd91fddbfa33e99faa8c7da2d29f3db29aa7f1526c340d7a7` | `/guides/japan-car-rental-expressway-guide/diagram-1-en.svg` (`a9a9910ebdc778b09cf045493b4e5de090022e979e06cd48391a188209c0fead`) |
| `ja` | 日本本土レンタカー・高速道路完全ガイド：免許と翻訳文、免責補償・NOC、ETCと周遊パス（HEP・KEP・TEP）、雪道運転と交通ルール（2026年版） | `eb1a6746bf8dacee25ea75a709075a808dc0a763564ccf569c794148ef7b5c48` | `/guides/japan-car-rental-expressway-guide/diagram-1-ja.svg` (`58276f3b3b3891b1104cf1c30cc652e4371dde2a69f4efea33f021bdfd2e4bf2`) |
| `ko` | 일본 본토 렌터카·고속도로 완벽 가이드: 국제운전면허증과 일본어 번역문, 면책보상(CDW)·NOC, ETC·고속도로 패스, 겨울 운전과 교통법규(2026년판) | `b15f077af1fbd85c745f196e8761993fe30757268740053f1b6c38f871447e6e` | `/guides/japan-car-rental-expressway-guide/diagram-1-ko.svg` (`5ee03a1c9f1ddacaf13df645afbd497dfa202a43b55e8640e9cee80becd1c6ce`) |
| `zh-CN` | 日本本岛自驾全攻略：驾照资格与日文译本、租车保险、ETC 与高速公路周游券、雪季与违章（2026 年版） | `f48388b5b3673b819f572c93d025f110c9f23c2ad9d10e48bcd3b792468947ae` | `/guides/japan-car-rental-expressway-guide/diagram-1-zh-cn.svg` (`1ff65ddc4ea0cd06c836acbf3ec01fae3797e69d4ac1329bb0233de5e55611f1`) |

### Independent Review Summary & Receipt

- Combined `route-b-review-v1` receipt validated via `prepare_route_b_bundle.load_review`:
  - `evidence_sha256`: `d1ccc125d17424a4c929957925fa53b5a107e8289cc671710b7eae46588d83f5`
  - `review_sha256`: `fe498760b7fa83c26e13b31a1ade5d7580224fbd717b24ae372925f453bfa6e9`
  - Targets: 8/8 `PASS`, `open_findings: 0`, distinct translators (`antigravity-translator-<locale>`) and reviewers (`antigravity-reviewer-<locale>`).
- Key independent review fixes applied before merge:
  - `en`: removed unverified airport-purchase claim for MTR Tourist Day Pass in HK guide; aligned `HEP or KEP` between JP Car SVG card and `<desc>`; added `or IDP` to 1-year validity cap; put international `Only 1949 Geneva IDPs are valid / (1968 Vienna & Taiwan IDPs invalid)` first in JP Car SVG Step 1 red box; expanded `IDP/translation` & `expressway`; added Lai King box padding and re-verified both PNGs.
  - `ja`: scoped HK Tourist Octopus non-refundable clause strictly to the HKD 260 Tourist Pass; clarified `IC・タッチ決済運賃`; replaced Chinese-isms `雪季` → `冬季`, `全国越境申請` → `全国どこでも申請可`, `最重で3年以下の懲役（拘禁刑）` → `3年以下の拘禁刑（旧・懲役）`, `放置違反金などの告知書` → `交通反則告知書と納付書` (`反則金`), `監理所` → `台湾監理所`, and re-verified both PNGs.
  - `ko`: fixed `MAJOR` warning inversion (`현지 운전면허증만으로` → `자국 운전면허증 원본만으로`); reframed `한국인은` → `한국 운전면허 소지자는`; scoped Taiwan translation table header (`대만 면허 기준`); replaced `만땅 반납` → `가득 주유 반납` across JSON & SVG; polished HK transfer phrasing (`S1 버스에서 퉁청선으로 갈아타면`), bidirectional table header (`이용역`), and `휴대 수하물`, and re-verified PNG.
  - `zh-CN`: standardized `原件驾照` → `驾照原件` across JSON & SVG; accurately attributed Japan Road Traffic Act penalty notice (`依据日本道路交通法（台北驻日经济文化代表处页面亦有提醒）`); harmonized `使用协议` / `KEP 协议` and `二号客运大楼（T2）`; re-verified PNG.
