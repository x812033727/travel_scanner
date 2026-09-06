---
id: 2026-09-06-hotspot-themes-api
title: 熱門景點季節與購物主題：資料模型、種子與公開 API
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T14:48:16Z
created_at: 2026-09-06T14:48:15Z
completed_at:
branch: claude/attractions-seasonal-categories-4817d7
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/migrations/versions/0050_hotspot_themes_intros.py
  - apps/api/app/hotspots/theme_catalog.py
  - apps/api/app/hotspots/theme_bootstrap.json
  - apps/api/app/hotspots/themes.py
  - apps/api/app/hotspots/service.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/trips/itinerary.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_hotspot_theme_catalog.py
  - apps/api/tests/test_migration_0050_hotspot_themes.py
  - apps/api/tests/test_hotspot_themes_integration.py
  - apps/api/tests/test_planner_candidates.py
  - apps/api/tests/test_hotspot_seed_reconciliation.py
  - apps/api/tests/test_schema.py
  - docs/hotspot-themes.md
---

# 熱門景點季節與購物主題：資料模型、種子與公開 API

## Why

`/hotspots` 只有一個 `category` 欄位（culture／nature／shopping…），沒有「這個景點什麼時候值得去」（賞櫻、賞楓、滑雪、花火、燈飾、賞雪）也沒有「這是哪一種店」（藥妝、電器、百貨、Outlet、伴手禮、二手古著、動漫周邊、商店街）。產品決定：景點保留 category，另加一層正交的 **theme** 標籤，季節帶適用月份（札幌櫻花是 5 月，可逐景點覆寫），購物店家當成 `category=shopping` 的景點再掛店型標籤。這張任務是第一刀：資料表、種子、公開 API 與規劃器 seam；後台編輯、前端 chips、介紹文、規劃器偏好各自另開任務（見 `docs/hotspot-themes.md` 的分工）。

## Definition of done

- [x] `GET /hotspots/rankings?theme=sakura` 只回帶該主題的景點；未知或停用的 slug 回 422 `unsupported_theme`。
- [x] 每筆 ranking item 有 `themes: [{slug, kind, name, months}]`，名稱依 `X-Travel-Locale` 本地化，月份已套用逐景點覆寫。
- [x] `GET /hotspots/facets` 有 `themes`（六季節在前、八店型在後，含零筆的啟用主題與 public 筆數）。
- [x] 每次 collect run 都會把 `theme_bootstrap.json` 的指派同步進 `hotspot_theme_links`，且不動後台／AI 建立的 link，也不會復活後台移除過的 seed link（墓碑）。
- [x] `ItineraryHotspot.themes` 帶到規劃器；`_collect_ranked(theme=)` 可依主題分頁。

## Steps

- [x] `models.py`：`HotspotTheme`、`HotspotThemeLink`、`HotspotIntro`、`HotspotIntroRun`（後兩張表給介紹文任務用，一次建完免得再搶 migration 編號）。
- [x] migration `0050_hotspot_themes_intros`（照 0036 的 inspect-first 守衛；用 `op.get_context().as_sql` 判斷 offline，讓 migration 測試能在裸 `Operations.context` 下跑）。
- [x] `theme_catalog.py`：14 筆 seed 與 import 時驗證。
- [x] `theme_bootstrap.json`：96 筆指派（只收計畫裡標「confident」的；「needs check」列留在計畫附錄 B，逐筆確認後再加）。
- [x] `themes.py`：loader、`seed_hotspot_themes`、`sync_hotspot_themes`、`theme_name/theme_ref`、`resolve_theme`、`theme_filter`、`load_hotspot_themes`、`theme_facets`、`python -m app.hotspots.themes` 回填入口。
- [x] `service.py`／`router.py`／`trips/itinerary.py`／`i18n.py` 接線。
- [x] 測試：純資料、migration（整合）、rankings／facets／sync（整合）、planner 透傳。
- [x] `docs/hotspot-themes.md`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
cd apps/api && RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_hotspot_themes_integration.py tests/test_migration_0050_hotspot_themes.py
cd apps/api && uv run python -m app.hotspots.themes      # 一次性回填，印出 links_created 等計數
curl -H "X-Travel-Locale: en" "$API/hotspots/facets" | jq .themes
curl "$API/hotspots/rankings?destination_id=tokyo&theme=sakura&limit=5" | jq '.items[].themes'
curl -i "$API/hotspots/rankings?theme=bogus"              # 422 unsupported_theme
```

## Notes

- 主題標籤在伺服器端本地化（像 areas 的 `names`），不進 web 的 message catalog；zh-CN 缺時退回 zh-TW，再退 en。
- `theme_bootstrap.json` 的 slug 是 **resolved** slug（顯式 `slug`、`LEGACY_SLUGS`、或 `wikidata-<qid>`），loader 在 import 時對 `HOTSPOT_SEEDS` 驗證，打錯字整個 API 起不來——這是故意的。
- 店型標籤只掛在 `category == "shopping"` 的景點（loader 強制）；建檔時因此略過 太陽城（family）、國際通（food）、白色戀人公園（family）、迪化街（culture）。要掛就先修 category。
- 種子覆蓋很薄的主題：ski 2（藻岩山、天狗山）、fireworks 2、drugstore 2、electronics 1、outlet 0。專門店家（唐吉訶德、BIC CAMERA、Olive Young、各 Outlet）在另一張 seed 任務，座標要逐筆核實後才進 repo。
- 順手發現、另開任務：`2026-09-06-seed-category-shopping-mistakes`（四筆 seed 的 category 是錯的 `shopping`）、`2026-09-06-gemini-guide-run-check`（`HotspotGuideAISearchRun.provider` 的 CHECK 沒有 gemini，選 Gemini 會 500）。
- 自我稽核抓到的一個真缺陷：整合測試原本寫 `AppError.status_code`，但 `AppError` 只有 `.status`（`app/problems.py:10-14`）——那行只在有 PostgreSQL 的 CI 跑，本機永遠碰不到。已改正，並補了兩個不需要資料庫的 `resolve_theme` 單元測試，讓同類錯誤在預設測試集就會現形。
- 稽核也修了三筆季節資料：釜山溫泉川的櫻花補回三月下旬（`[3,4]`）、小樽運河的賞雪拿掉只有二月的覆寫（二月是雪燈之路，雪景整個冬天都在）、東急歌舞伎町 TOWER 拿掉 `department-store`（那是飯店與展演空間，沒有賣場樓層，八個店型都不合），並補上建長寺的賞楓。
- 不動 `catalog.py`（PR #238 在改）、`cli.py`／`main.py`（PR #236 在改）、`areas.py`（in-progress）。
