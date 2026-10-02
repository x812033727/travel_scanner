---
id: 2026-09-06-oka-amerikamura-wrong-qid
title: 沖繩美國村的 Wikidata QID 指到大阪，座標也是
status: in-progress
priority: P3
area: api
owner: claude-opus-5-5-oka-qid
claimed_at: 2026-10-02T19:27:19Z
created_at: 2026-09-06T20:29:26Z
completed_at:
branch: claude/oka-american-village-qid
depends_on: []
scope:
  - apps/api/app/hotspots/bootstrap.json
  - apps/api/app/hotspots/shopping_bootstrap.json
  - apps/api/app/hotspots/service.py
  - apps/api/tests/test_hotspot_areas.py
  - apps/api/tests/test_shopping_bootstrap.py
  - apps/api/tests/test_hotspot_wikimedia.py
  - apps/api/tests/test_hotspot_depth_catalog.py
  - docs/hotspot-themes.md
---

# 沖繩美國村的 Wikidata QID 指到大阪，座標也是

## Why

`wikidata-q4745722`（沖繩「美國村」）用的是 **Q4745722**，那是**大阪**的アメリカ村。座標也跟著錯：
`tests/test_hotspot_areas.py::AREA_MISPLACED_SEEDS` 早就記著這一筆「北谷的美國村落在大阪」。

2026-09-06 加購物店家種子時撞到了：大阪アメリカ村本人要進 catalog，但 QID 在 repo 裡必須唯一，
被沖繩那一列佔著。所以 `kix-amerikamura` 只好把 `wikidata_item_id` 留 null，只在 `source_urls`
引用該 item 取座標。修好這一列，大阪那一列就能拿回自己的 id。

## Definition of done

- [x] 沖繩美國村改用正確的 QID（Depot Island／美浜アメリカンビレッジ）或留 null，座標指向北谷町。
- [x] `AREA_MISPLACED_SEEDS` 少一筆。
- [x] `kix-amerikamura` 拿回 `wikidata_item_id: "Q4745722"`（順手改，或另開一次）。

## Steps

- [x] 找出這列在哪個 bootstrap 檔（`slug` 是 `wikidata-q4745722`，city_code `OKA`）。
- [x] 用 Wikidata 或沖繩觀光官方頁核實北谷町美浜的座標，照 `shopping_bootstrap.json` 的規矩
      在 `source_urls` 引用來源、`coordinate_source` 寫實。
- [x] `tests/test_hotspot_areas.py` 移除該 slug，確認 `resolve_area("OKA", …)` 有值。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_areas.py tests/test_shopping_bootstrap.py -q
```

## Notes

- 換掉 QID 會讓下一次 collect run 重抓那一列的 Wikipedia／Wikidata 資料，這是預期的。
- 別把沖繩那列直接刪掉：`TARGET_PUBLIC_HOTSPOTS` 與各城市筆數的測試會一起垮。

### 2026-10-03 做了什麼（claude-opus-5-5-oka-qid）

- 這列其實在 `bootstrap.json`，不在原 scope 寫的 `secondary_bootstrap.json`／`base_bootstrap.json`
  （後者不存在）。scope 改成實際動到的檔：`bootstrap.json`（那一列）、`shopping_bootstrap.json`
  （大阪拿回 QID）、`test_shopping_bootstrap.py`（拿掉 `QID_HELD_ELSEWHERE` 例外）、
  `test_hotspot_wikimedia.py`（原本斷言 `kix-amerikamura` 的 QID 是 null）、
  `test_hotspot_depth_catalog.py` 與 `test_hotspot_wikimedia.py` 的 QID 總數 580 → 581、
  `service.py` 的 docstring 與 `docs/hotspot-themes.md` 的待辦（都寫著這個錯還在）。
  `bootstrap.json` 與 `service.py` 跟 claude-fable-5-1 的兩張 `review` 票重疊
  （`2026-09-19-foreign-place-reason`、`2026-09-12-discovery-only-sees-100-articles-per-centre`），
  那兩張的分支 `claude/travel-scanner-pr-552-rpq36m` 的 PR #561／#563／#565 都已合併、沒有開著的 PR，
  是過期認領；我沒有動那兩張票。
- 正確的 item 是 **Q11609171**「美浜タウンリゾート・アメリカンビレッジ」（P131 北谷町 Q1351759，
  P31 resort／theme park，別名 American Village／美浜アメリカンビレッジ），P625
  26.316183, 127.756668；ja-wiki 同名頁的 `wikibase_item` 就是它、座標相同。沒有 en-wiki 條目，
  所以 `wikipedia_project` 改成 `ja.wikipedia.org`。「Depot Island」在 Wikidata 沒有對應 item。
- OSM 交叉比對（Nominatim 一次）：美浜アメリカンビレッジ北口／南口兩個公車站，距 P625 136 m 與
  216 m，地址都是北谷町美浜。上游座標沒錯，所以 `coordinate_source` 寫 `wikidata_p625`，
  `source_urls` 引 Wikidata 與 ja-wiki，不需要 `admin_verified`＋OSM。
- `names` 的 en／ja／ko 用 `app.hotspots.wikidata_labels` 的 `site_labels`＋`apply_labels` 從
  Q11609171 重新產生（舊值是大阪那個 item 的標籤）；zh-CN 與 `local_name` 不變。
- **slug 刻意釘在 `wikidata-q4745722`**（在列裡寫明 `slug`）。slug 本來由 QID 推導，換 QID 會讓
  種子在正式站新增第二列美國村，而舊的那列（Q4745722、大阪座標）會繼續上架，`kix-amerikamura`
  也拿不到 QID（`seed_catalog` 看到 Q4745722 已被別列持有就跳過）。釘住 slug 後，只要正式站那列
  還歸種子管，下一輪 collector 就會就地改成 Q11609171 與北谷座標，同一輪大阪那列拿回 Q4745722。
- 新測試 `test_okinawa_american_village_is_in_chatan_not_osaka`：沖繩那列的 QID 不是 Q4745722、
  座標在沖繩本島的框內、區域是 `chatan`，大阪那列持有 Q4745722 且落在大阪的區域。換回舊種子時
  它與 `test_curated_seeds_all_resolve_to_an_area` 都會失敗。
- 沒碰正式站。正式站那列若曾被人審過、補過 Place ID 或已有探索列持有 Q11609171，種子會跳過它，
  而後台不能換既有 QID（409 `hotspot_wikidata_identity_locked`）；它掛著的 guides、AI 介紹與
  place profile 也可能是大阪的內容。這些另開主機步驟票 `2026-10-02-oka-american-village-prod-check`。
- `tools/generate_hotspot_bootstrap.py` 的 OKA 規格仍寫 `("American Village", "美國村", …)`，
  en-wiki 會把它轉址到大阪的 Amerikamura。那支產生器早已無法重現現在的 `bootstrap.json`
  （它不寫 `names`／`local_name`），沒有改它。
