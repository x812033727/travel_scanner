---
id: 2026-11-22-localize-ha-long-bay-cruise-from
title: Localize ha-long-bay-cruise-from-hanoi and phuket-airport-transport-where-to-stay into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-22T05:30:09Z
created_at: 2026-11-22T05:30:02Z
completed_at: 2026-11-22T06:39:03Z
branch: agy/localize-wave3c-halong-phuket-batch10
depends_on: []
scope:
  - apps/api/app/guides/content/ha-long-bay-cruise-from-hanoi.json
  - apps/api/app/guides/content/phuket-airport-transport-where-to-stay.json
  - apps/web/public/guides/ha-long-bay-cruise-from-hanoi
  - apps/web/public/guides/phuket-airport-transport-where-to-stay
---

# Localize ha-long-bay-cruise-from-hanoi and phuket-airport-transport-where-to-stay into en, ja, ko, zh-CN (Route B)

## Why

Wave 3C Batch 10 of the Mokaair multi-locale guide localization program batches two high-traffic Southeast Asia flagship guides (whose live `zh-TW` documents match the repository byte-for-byte) into one combined Route B PR:

1. `howto/ha-long-bay-cruise-from-hanoi` (live `zh-TW` v4)
2. `howto/phuket-airport-transport-where-to-stay` (live `zh-TW` v8)

Adding `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG diagrams unlocks 8 new indexable guide URLs across search engines and AI crawlers.

## Definition of done

- [x] Both `ha-long-bay-cruise-from-hanoi.json` and `phuket-airport-transport-where-to-stay.json` contain validated `en`, `ja`, `ko`, and `zh-CN` documents with `zh-TW` preserved byte-for-byte (0 deleted lines).
- [x] All 8 localized 1600×900 SVG diagrams (`diagram-1-{en,ja,ko,zh-cn}.svg` for each slug) are placed under `apps/web/public/guides/<slug>/`, visually verified in headless Chromium (eliminating Thai tofu script on Phuket SVGs, enforcing `>= 15px` label legibility, and fixing EN/JA Ha Long port box margins), and have `<desc>` matching the corresponding `image` block `description` byte-for-byte.
- [x] Independent locale reviewers (`antigravity-reviewer-{en,ja,ko,zh-CN}`, distinct from translators `antigravity-translator-{en,ja,ko,zh-CN}`) audited all 8 `(slug, locale)` targets; all findings were resolved and the combined `route-b-review-v1` receipt passed `prepare_route_b_bundle.load_review` with 8/8 `PASS` and `open_findings: 0`.
- [x] `pack_cli lint`, `pytest tests/test_guides_content_pack.py`, and `docs/news-2026-batch-4/translation_checks.py` pass with 0 errors for both slugs.
- [x] An unclaimed follow-up release task (`2026-11-22-release-localized-ha-long-bay-cruise`) is filed for host-side bundle preparation and publication after deploy.

## Steps

- [x] Pin live `zh-TW` baselines (`repo_hash == live_hash`) and verify live cross-article link locales for both guides.
- [x] Translate both guides and build localized 1600×900 SVGs for `en`, `ja`, `ko`, and `zh-CN`.
- [x] Render all 8 SVGs with headless Chromium and visually inspect for clipping, box overflow, label collisions, and CJK/Hangul glyph correctness.
- [x] Run independent per-locale reviews across all 8 targets, apply all schema/prose/SVG fixes (including `>= 15px` label lint compliance), and re-render/re-inspect all modified SVGs.
- [x] Merge into both content packs, copy all 8 SVGs, run full lint/pytest/translation checks, and validate the combined `route-b-review-v1` receipt.

## How to verify

```bash
git diff -- apps/api/app/guides/content/ | grep -E '^-[^-]'
cd apps/api && uv run python -m app.guides.pack_cli lint --slug ha-long-bay-cruise-from-hanoi
cd apps/api && uv run python -m app.guides.pack_cli lint --slug phuket-airport-transport-where-to-stay
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content ha-long-bay-cruise-from-hanoi phuket-airport-transport-where-to-stay
npm run check:tasks
```

## Notes

### Pinned Live `zh-TW` Baselines (`repo_hash == live_hash`)

- **`ha-long-bay-cruise-from-hanoi`** (`howto`, live v4):
  - `source_sha256`: `348eb359485656ea237d266cbbfe765cad4f1722370b13d5c487b15cbadf27d0`
  - Cross-article links: omitted `zh-TW`-only `hanoi-4-day-itinerary` and `vietnam-domestic-flights-train-guide`; converted `vietnam-money-sim-grab-guide` block into a plain `paragraph` retaining the practical Vinasun/Mai Linh metered taxi tip (35 blocks, 0 `article` inlines). Adapted visa notice, foreign senior 50%-discount exclusion (strictly Vietnamese citizens 60+), and Hanoi flight routing per audience. Localized final 2 links to `/<locale>/destinations/hanoi` and `/<locale>/foods?destination_id=hanoi`.
- **`phuket-airport-transport-where-to-stay`** (`howto`, live v8):
  - `source_sha256`: `dfcf9ca1968b5031e65f90b2f3ee69e15f6c32eafc8ead7a6cea8efa91236738`
  - Cross-article links: omitted Taiwan-specific `taoyuan-airport-departure-guide`, `return-to-taiwan-customs-duty-free-guide`, and `zh-TW`-only `bangkok-airport-to-city`, `bangkok-4-day-itinerary`, `phuket-phi-phi-james-bond-island-hopping`, `krabi-airport-transport-where-to-stay`; converted `southeast-asia-seasons-when-to-go` block to a plain `paragraph` keeping full Phuket season/monsoon/red-flag safety details; retained live 5-locale `howto/thailand-esim-sim-wifi` with exact verbatim target-locale titles (32 blocks, 1 `article` inline). Localized final 2 links to `/<locale>/destinations/phuket` and `/<locale>/foods?city=phuket`.

### Localized Deliverables & Hashes

#### `ha-long-bay-cruise-from-hanoi`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | How to Choose a Ha Long Bay Cruise from Hanoi: Day vs. Overnight, VHL1–VHL8 Sightseeing Fees, and What to Ask Before Booking | `0eae5fd90192a2f4a2116e77d1068f8aa2ecedac0c376ead002b4dcf6ba483be` | `/guides/ha-long-bay-cruise-from-hanoi/diagram-1-en.svg` (`c5d3553eddb27a9cc62f1523de078c9752684c32fa95c126f057f61366130175`) |
| `ja` | ハロン湾クルーズの選び方：ハノイ発の日帰り・宿泊船、VHL1〜VHL8の観光料と宿泊券、料金に含まれるか事前確認 | `d94cb540b8af59e567d33873bb2f92cdce7430a805195a65d3ef356616a146b4` | `/guides/ha-long-bay-cruise-from-hanoi/diagram-1-ja.svg` (`4341fad40da0a33aae3ce439d389f8f1b919ae52f2d9afc653d3a811bd052e49`) |
| `ko` | 하롱베이 크루즈 선택 가이드: 하노이 출발 당일·숙박 크루즈, VHL1~VHL8 관광비와 숙박권, 예약 전 포함 여부 확인법 | `65149f11cb74a5cbc91b71078a539ff98ce400de327545da596fd09cf4241334` | `/guides/ha-long-bay-cruise-from-hanoi/diagram-1-ko.svg` (`d6fb4952aa32220c7017c9c4a8e6700e891e05385c1e3d8288963ae449df86a0`) |
| `zh-CN` | 下龙湾游船怎么选：河内出发一日船还是过夜船、VHL1 到 VHL8 观光费与过夜票，报价含不含先问清 | `2258affc081817b2d5b7af7bc7449769afac6e0fa2cfb04c964d5a1bccae8c10` | `/guides/ha-long-bay-cruise-from-hanoi/diagram-1-zh-cn.svg` (`d43be034e184f5527a007cf70f2018a6596a05c4edc9dc10909b0d2525be122f`) |

#### `phuket-airport-transport-where-to-stay`

| Locale | Title | `document_sha256` | Diagram Asset & `sha256` |
| --- | --- | --- | --- |
| `en` | Phuket Airport to Patong, Karon, Kata, and Old Town: Smart Bus, Airport Bus, Grab, and Taxis Compared—Plus Where to Stay First | `54edaff713bd77be335483d7959796b186f0247383d920ca330b6358d098a712` | `/guides/phuket-airport-transport-where-to-stay/diagram-1-en.svg` (`77fbf60c02e22dde685f3e4f4cd22c93385a24bcb9bf3d443004176c88a73a71`) |
| `ja` | プーケット空港からパトン・カロン・カタ・オールドタウンへのアクセスガイド：Smart Bus・エアポートバス・Grab・タクシー比較と初めての宿泊エリア選び | `18e783c294bd05a0adf500f59041ee65fce68b6390d72b0233d6371e68941c00` | `/guides/phuket-airport-transport-where-to-stay/diagram-1-ja.svg` (`ce66ad7d297d35ba6114ad179ebded50788d82d6cb0fee627e4d8bb16d87d288`) |
| `ko` | 푸켓 공항에서 파통·카론·카타·올드타운까지 교통 가이드: Smart Bus, 공항버스, Grab, 택시 비교와 첫 방문 숙소 추천 구역 | `124a26258c9ed570df679e003b795c4a5f4237086499757310a7f8cd55225b8c` | `/guides/phuket-airport-transport-where-to-stay/diagram-1-ko.svg` (`23c13876e02de8b8f531747942f80c8fbc15212651289c3ce6ebbfc43fcfb808`) |
| `zh-CN` | 普吉机场到芭东、卡隆、卡塔与老城交通攻略：Smart Bus、机场巴士、Grab 与出租车对比，首次去住哪一区 | `f0aca546a487a854c603b22b2e0cfc736135ffe16729362554a37167105f7f5b` | `/guides/phuket-airport-transport-where-to-stay/diagram-1-zh-cn.svg` (`008bb6b780256b0265f83bd734ac9bc342616c243cf7c2bdefb0610d3b4f8537`) |

### Independent Review Summary & Receipt

- Combined `route-b-review-v1` receipt validated via `prepare_route_b_bundle.load_review`:
  - `evidence_sha256`: `3470e699d979019e39d6ddde67209a3eff445df66c132ae13383ee3d90150dc4`
  - `review_sha256`: `55b91228358b4d27a83d51e34e29200847df2edc173231bc17f5be3589a97956`
  - Targets: 8/8 `PASS`, `open_findings: 0`, distinct translators (`antigravity-translator-<locale>`) and reviewers (`antigravity-reviewer-<locale>`).
- Key independent review & lint fixes applied before merge:
  - `en`: tightened `description`, `summary.items[2]`, table captions, and 2 source titles to satisfy `GuideDocument` max-length caps; widened Ha Long City port cards and raised labels to `>= 15px` (fixing `Tuan Chau International Cruise Port` border overflow); standardized English diacritics (`Bai Chay`, `Gia Luan Pier`, `Hai Phong`) and Phuket table/sentence wording.
  - `ja`: harmonized Phuket SVG map label `プーケット旧市街` → `プーケット・オールドタウン`; fixed `22:00以降` inclusive contradiction (`22:00発の後は`); removed Chinese-isms (`非進入` → `乗入なし`, `非経由` → `経由せず`); aligned `〜` ranges and raised all SVG labels to `>= 15px` with widened Ha Long & Laguna boxes.
  - `ko`: polished Ha Long taxi tip phrasing (`이 글에서는 택시 요금을`) and raised SVG sub-labels to `>= 15px` with widened Ha Long & Laguna boxes; verified 100% consistent `푸켓` terminology.
  - `zh-CN`: clarified `boca.gov.tw` attribution (`台湾领事事务局`), aligned Nai Yang marine national park phrasing with `zh-TW` (`属于海洋国家公园`), tightened Vinasun/Mai Linh taxi sentence, and aligned Ha Long pre-booking heading with the 6-item list.
