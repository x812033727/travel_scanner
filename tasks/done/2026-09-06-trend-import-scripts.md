---
id: 2026-09-06-trend-import-scripts
title: 把潮流街區的匯入腳本收進 repo
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:57:11Z
created_at: 2026-09-06T00:52:35Z
completed_at: 2026-09-06T03:09:01Z
branch: claude/foods-data-p1
depends_on: []
scope:
  - apps/api/app/foods/trend_import.py
  - apps/api/app/cli.py
  - apps/api/tests/test_trend_import.py
---

# 把潮流街區的匯入腳本收進 repo

## Why

2026-09-06 我用臨時腳本往正式機寫了兩批資料：57 個潮流商圈（`food_areas`，
`source='admin'`）和 99 家店家（`food_merchants`，全部 `pending`）。那些腳本只存在
於當次 session 的 scratchpad 目錄，session 結束就消失。

後果是：沒有人能重跑、驗證或延伸這條管線。第 3 張任務（21 個空街區）要再匯入一批
店家時，得從零把同樣的東西再寫一次，而且無從得知上次的欄位怎麼填、去重規則是什麼。
資料本身也一樣：哪 101 家通過、哪 143 家被刷掉、各自的理由，全部只在 scratchpad。

## Definition of done

- [x] 倉庫裡有一個可重跑的匯入路徑，任何人 `python -m app.cli <指令> --file <json> --apply`
      就能把同樣格式的店家資料寫進資料庫，且重跑不會產生重複列。
- [x] 匯入的資料檔（店家清單）也在倉庫裡，不是散在某台機器上。
- [x] 有測試涵蓋去重與拒絕規則，不需要資料庫就能跑。

## Steps

- [x] 把 scratchpad 的 `import_trend_merchants.py` 整理成 `apps/api/app/foods/trend_import.py`：
      解析 → 驗證 → 建立 `FoodMerchant` + `FoodMerchantSource` + `FoodMerchantCategory`。
- [x] 在 `apps/api/app/cli.py` 加一個子指令（比照既有的 `import-hotspot-candidates`：
      `--file` / `--limit` / `--apply`，預設 dry-run）。
- [x] 資料檔放進倉庫（建議 `apps/api/app/foods/data/trend_merchants.json`，第 3 張任務會往
      這個路徑加新的一批）。
- [x] 測試：slug 格式、五語系名稱、https 來源網址、分類 slug 必須存在、
      同 slug 與同 `(destination_id, local_name)` 兩種去重、`source_kind` 對應的
      `source_scope`。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trend_import.py -q
```

正式機上先 dry-run 再 apply，dry-run 對已匯入的資料應該回報全部 skipped（冪等）：

```bash
docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.cli import-trend-merchants --file <path>
```

## Notes

**2026-09-06 完成。** scratchpad 的腳本已經消失，模組是照正式機實際寫入的形狀重建的（查了
`tokyo-dandelion-chocolate` 這一列與它的來源、分類、稽核列）：`apps/api/app/foods/trend_import.py`
（`parse_merchant` 驗證 → `parse_merchants` 檔內兩層去重 → `persist_trend_merchants` 對資料庫再做一次兩層去重、
缺商圈／缺分類會回報而不是崩、`--apply` 才寫入並記一列 `AdminAuditLog`）、`cli.py` 的
`import-trend-merchants --file --limit --apply`（`--file` 預設就是倉庫裡的資料檔）、
`apps/api/app/foods/data/trend_merchants.json`（正式機 `/root/trend-merchants.json` 的 101 列，含 slug）、
`unidecode` 進 `pyproject.toml`（`slug_for()` 只在資料檔沒給 slug 時才用）。
測試：`tests/test_trend_import.py`（無 DB：13 種壞列各自的拒絕理由、檔內兩種重複、slug 推導、整批 101 列都指向
`TREND_AREA_SEEDS` 與既有分類、與精選目錄剛好重疊兩家台南店家）；`tests/test_trend_import_integration.py`
（CI 的 Postgres：seed 後 dry-run 回報 99 would_create + 2 skipped 且零寫入、apply 建 99 列並逐欄比對形狀、
再 apply 一次全部 skipped 且稽核仍只有一列）。

**已知限制**：正式機那批店家的 `name` 直接是中文名（`name_zh`），沒有英文名，`names_json` 為空，所以英文語系看到的是中文店名；
模組沿用這個形狀以保持與正式機一致，補英文名是資料工作，不在這張範圍。

**寫進正式機的規則（已驗證可用，照抄即可）**

- 全部以 `review_status='pending'`、`is_active=False`、`map_match_status='unverified'`
  落地。這條路徑不能、也不該讓任何東西直接公開 —— 發布仍要走人工核准 + 耐久座標。
- `area_id` 由 `f"{destination}-{district_key}"` 去 `food_areas` 查；`area_source='admin'`
  才不會被 `seed-foods` 蓋掉。
- `display_order` 用 100（種子商圈是 1..N，潮流商圈我給 200+）。
- 來源列：`merchant_official` → `source_scope='merchant_website'`；
  `official_tourism` → `'merchant_listing'`；`claims_json=["display_name","address"]`。
- 分類最多取 3 個，第一個 `is_primary=True`，`source='admin'`。
- 稽核：一次匯入寫一列 `AdminAuditLog`（`action='food_merchant_created'`）。

**去重要兩層**，只比 slug 不夠：2026-09-06 那次有兩家台南店家已經在目錄裡，一家撞
slug、另一家 slug 不同但 `local_name` 相同（`tainan-a-song-ge-bao`）。

**Slug 產生方式**：優先抽店名裡的拉丁字品牌（潮店幾乎都有，例如 FUGLEN TOKYO →
`tokyo-fuglen-tokyo`），沒有才用 `unidecode` 轉寫（`喫茶半月` → `tokyo-chi-cha-ban-yue`）。
拼音式 slug 看起來不漂亮但沒關係 —— merchant slug 不會出現在公開 API 輸出裡，純內部識別碼。
`unidecode` 已在 api 的 venv 裡（我裝的），要正式使用得加進 `pyproject.toml`。

**來源網址必須 https**。那批資料只有一筆是 http（`fromafar-tokyo.com`），我確認過它的
https 版本回 200 才改寫。不要無條件把 http 改成 https，會產生連不上的來源。

**資料在哪**（會隨 session 消失，要救趁早）：
`%TEMP%\claude\C--Users-x8120-mokaair--claude-worktrees-affiliate-marketing-config-97c4cb\e1250ed6-85e4-4712-8c07-fa3f611cc1f1\scratchpad\`
底下的 `trend-merchants.json`（101 家含 slug）、`trend-merchants-dropped.json`（143 家
被刷掉的與理由）、`trend-food-areas.json`（57 個商圈）、`import_trend_merchants.py`、
`create_trend_food_areas.py`、`slugify_merchants.py`。正式機的 `/root/trend-merchants.json`
和 `/root/trend-food-areas.json` 是同樣內容的副本，比較不會消失。
