# 店家主幹

規則的全文：補資料的邊界與 Gemini 模式在 `docs/catalog-review.md`（"Merchant enrichment" 一節），寫入規則在 `apps/api/app/foods/enrichment.py` 與 `apps/api/app/foods/trend_import.py` 的模組說明，風格店家批次在 `docs/merchant-styles.md`。`<SSH>`、`<API>`、`<PY>` 的意思同 SKILL.md。

## 邊界（站主 2026-09-12 決定，至今沒變）

- Google、Naver、米其林、食べログ、OpenRice、CatchTable 等只當**定位與發現**。寫進資料庫的地址、來源、商圈、分類要有店家官網（`merchant_official` → `merchant_website`）或觀光局／政府講這一家的頁（`official_tourism` → `merchant_listing`）佐證。第三種較弱的 `merchant_platform` 只有 CatchTable 轉檔器與後台表單能寫（skill `catchtable-discovery`）。
- AI 與批次**永遠不寫** `map_match_status`、`review_status`、`is_active`、`naver_map_url`；座標只有 `fill-food-merchant-coordinates` 從店家自己引用的頁讀結構化資料來寫。
- 來源只收 https；只有 http 的官網先確認 https 版能開，不要盲改。

## 1. `seed-foods`

upsert `app/foods/catalog.py`、`merchant_catalog.py`、`area_catalog.py`、`category_catalog.py` 的種子，印 `foods`、`areas`、`categories`、`merchants`、`merchant_category_links`、`merchants_with_area` 計數。只補空：管理員設過或清掉的欄位維持原樣；平台列只建不改，所以**不能拿它改訂位連結**，也只涵蓋精選目錄的店家。部署帶來新分類或商圈資料後在主機跑一次（hotspot collector 只在 `hotspots` profile 下跑，不能等它）。

## 2. `import-trend-merchants`

輸入是 JSON **清單**，每筆：`destination`、`district_key`（`app/foods/area_catalog.py` 該城市的 `key`，對不到填 `null`）、`name_zh`、`name_en`（選填，拉丁字母）、`local_name`（原文名含分店名）、`address_local`（選填，來源頁印了才填）、`category_slugs`（1–3 個，第一個是主分類）、`source_url`、`source_title`、`source_kind`（`merchant_official` 或 `official_tourism`）、`note`（給人看、不入庫）、`confidence`、`slug`（小寫 kebab、`<destination>-` 開頭；省略時自動生）、選填 `styles`（風格標籤，見 `docs/merchant-styles.md`）。

- 檔內重複 slug 或重複 `(destination, local_name)` 整檔拒收；壞一筆整檔拒收。
- 資料庫去重兩層：slug 撞到 → `skipped_existing_slug`；同目的地同 `local_name` → `skipped_same_name`。不合併。與精選目錄同 slug 不同店會被拒（改 slug）。
- 建出的列：`pending`、`is_active=false`、`map_match_status=unverified`，一個 `FoodMerchantSource`、分類 `source=admin`、每批一筆 `food_merchant_created` 稽核。
- 做法：本機 `<PY> -c "from pathlib import Path; from app.foods.trend_import import load_trend_merchants; print(len(load_trend_merchants(Path('<file>'))))"` 驗檔 → 主機 `--file /dev/stdin` dry-run → 檔案隨 PR 部署後 `--file app/foods/data/<file>.json --apply` → 重跑應全是 `skipped_existing_slug`。
- 事後補了檔案裡的 `name_en`，已匯入的列不會自己變：跑 `backfill-merchant-english-names`（只讀預設的 `trend_merchants.json`）。

## 3. 座標：`fill-food-merchant-coordinates`

只看 `merchant_website`、`merchant_listing` 來源（`destination_context` 的城市美食指南不算），只讀頁面自己的 schema.org JSON-LD 與 geo meta；內嵌 Google 地圖的座標刻意不讀。一頁多個地點時，名稱對上本店或全頁只有一個座標才收，否則 `ambiguous` 留給人。KR 不跳過。官網幾乎不發 JSON-LD，所以補完官網後再跑一次才有收穫；還是沒有就走政府開放資料、Wikidata，或 OpenStreetMap 節點當 `admin_verified`（後台手填）。座標佇列審核者不可把 Google 候選的座標當耐久。

## 4. Place ID：`match-food-merchant-places`

只寫 `google_place_id`，KR 跳過（沒有 API 身分，要 Naver 精準頁）。寫進去不代表分店對：公開前要有人看過分店。怎麼看、怎麼挑、佇列怎麼審，走 skill `hotspot-review`。

## 5. 補資料

兩條路，寫入都走同一個 `apply_merchant_enrichment`（只填空欄位、來源以網址 upsert、分類只增、Place ID 只在空且沒人佔用時寫）。

**Gemini 路（後台同一個功能的 CLI 版）**

```bash
<SSH> "<API> enrich-food-merchants --actor-email <admin> --dry-run"
<SSH> "<API> enrich-food-merchants --actor-email <admin> --destination tokyo --limit 5 --max-calls 6"
```

每 5 家 2 次 Gemini；全部項目都是 `needs_review`，修正要在後台 `/admin/catalog-review` 按 `apply_corrections`。預算：每 run 上限 `catalog_review_max_calls`（預設 80，在 `/admin/settings` 的「Gemini 多語文章搜尋」卡）；160 家左右約 66 次（最壞 99），全量前把上限調到 120 或用 `--destination` 分批（每目的地 ≤ 40 家約 16 次）。Google 端每家沒有 Place ID 的店至多一次 Text Search Pro。

**研究路（人或代理用瀏覽器查）**

1. `<SSH> "<API> export-food-merchant-worklist --status pending" > worklist.json`（UTF-8 讀；`--out` 會寫在容器裡）。已被 committed 補資料檔以 `found`／`not_found` 結案的店家預設不列，`blocked_retry_later` 會再列。
2. 依國家切成至多四個瀏覽器分片，先試 30 家。每家：Google Maps 分店頁只做身分核對、從展開後的網址取 Place ID（短網址會被拒）；KR 在 `naver` 記 `not_possible_in_pane` 或網址 → 搜官網、開頁確認店名／這家分店地址／仍營業，逐字引文 ≤ 300 字 → 觀光局頁只收 `TRUSTED_SOURCE_HOSTS`（`apps/api/app/catalog_review/repository.py`）→ 商圈依 worklist 的 `match_terms`、分類 ≤ 3。
3. 寫成 `apps/api/app/foods/data/enrichment/<date>-<name>.json`：檔頭 `schema_version: 1`、`batch_id`、`researched_at`、`researched_by`、`method`、`records`。每筆 `merchant_id`、`slug`、`name`、`local_name`、`country_code`、`destination_id`、`outcome`（`found`、`partial`、`not_found`、`blocked_retry_later`）、帶時區的 `checked_at`、`official_website`／`listing_source`（`url`、`title`、`quote`）、`address_local`（`value`、`source_url` 必須是前兩者之一、`quote`）、`google_maps_url` 或 `google_place_id`＋`map_identity_observation`、`area_slug`（`<destination>-` 開頭）、`category_slugs`、`evidence`（1–10 筆 `url`／`role`／`observation`）。`found` 要有官網或觀光局頁，KR 以外還要有 Google 身分；`not_found`／`blocked_retry_later` 不能帶任何提案，只留一筆稽核讓下次 worklist 知道看過了。完整驗證在 `apps/api/app/foods/enrichment_import.py`。
4. `<PY> -m app.cli apply-food-merchant-enrichment --file <file> --check`（不開資料庫）→ 主機 `--file /dev/stdin` dry-run → `--apply --limit 30` → 再 dry-run 應只剩 `unchanged`／`already_noted`。
5. 查到的訂位連結不寫進補資料檔，另寫平台審查檔（`reservation-links.md`）。

## 6. 訂位平台列

見 `reservation-links.md`。

## 7. 公開

後台 `/admin/foods`：地點驗證（`map_match_status=verified`）＋核准＋啟用，一次儲存或批次的 `verify_activate`。閘門在 `commands.md` 的「公開閘門」。KR 的 Naver 精準頁怎麼拿、座標怎麼找，照 `.agents/skills/catchtable-discovery/references/admin.md`。驗證：公開 API `https://mokaair.com/api/travel/foods/merchants?destination_id=<D>&limit=50`（帶 `X-Travel-Locale`），數字對上報告才算完。
