---
id: 2026-09-11-food-reservation-link-backfill
title: 公開美食店家訂位平台連結補齊（查核與批次匯入）
status: in-progress
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T16:02:41Z
created_at: 2026-09-11T15:58:40Z
completed_at:
branch: claude/food-reservation-link-backfill
depends_on: []
scope:
  - apps/api/app/foods/platform_review_import.py
  - apps/api/app/foods/data/platform_reviews
  - apps/api/app/cli.py
  - apps/api/tests/test_food_platform_review_import.py
  - docs/catalog-content-reviews/2026-09-11-reservation-links-full.md
---

# 公開美食店家訂位平台連結補齊（查核與批次匯入）

## Why

331 間公開美食店家裡，只有 35 間有「查看平台訂位資訊」按鈕。這 35 間是 2026-09-11 有人在後台逐筆存的，另外 296 間從沒查過。
後台一次只能存一個平台，幾百間店逐筆存不實際；而 `seed-foods` 只新增、不更新，也無法用來補。

## Definition of done

- [x] 296 間未查核的公開店家都有查核結果：`verified`、`disabled`、`not_found` 或 `ambiguous`，每筆附證據。
- [ ] 精準分店頁已寫進正式資料庫，前台出現對應按鈕；不能訂位的平台頁不公開。
- [ ] 後台人工審核過的列一筆都沒被覆寫。

## Steps

- [x] `apply-food-platform-reviews` 指令與測試：預設試跑、只寫平台列、每列一筆稽核。
- [x] 用內建瀏覽器查核，結果整理成 `apps/api/app/foods/data/platform_reviews/2026-09-11-public-merchants.json`（311 筆：verified 12、disabled 35、ambiguous 9、not_found 255）。
- [x] 查核摘要 `docs/catalog-content-reviews/2026-09-11-reservation-links-full.md`。
- [ ] PR、合併、部署，在 api 容器試跑，確認後 `--apply`。

## How to verify

- `cd apps/api && pytest tests/test_food_platform_review_import.py tests/test_food_platform_links.py`
- 部署後：`docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews`（試跑），再加 `--apply`。
- 公開 API `https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁統計 `reservation_links`，應等於 verified 的公開店家數。

## Notes

- 接續 `2026-09-11-food-map-reservation-entry` 剩下的店家。那份任務的首批 10 間，後來已由另一個後台帳號在 2026-09-11 09:13–12:56 UTC 逐筆存好（連同其他店共 36 列 verified）。
- 正式資料庫在 2026-09-11 16:00 UTC 的狀態：
  - 未審核的 ambiguous 共 166 列，都是 seed 寫的保守結果。
  - 未審核的 verified 1 列，是 Song Fa 的 seed 列。
  - 人工審核的 verified 36 列。
  - 沒有任何人工審核的 not_found 或 ambiguous 列，所以沒有「已查過但查無」的店可以跳過。
- 使用者決定（2026-09-11）：
  - 只存現有 12 個平台，Tabelog、Grab Dine Out、Naver 預約等只記在證據裡。
  - 平台頁明寫不收訂位的，存成 `disabled`，改用店家官網實際連出的平台。
  - 寫入走批次指令。
  - 查核先用內建瀏覽器，卡住才改用 Gemini。
- 帶點的 Catchtable 店家 ID（例如 `yosukgung.kr`）原本要等 PR #397。#397 已在 2026-09-11 16:05 UTC 合併，本分支也已併入，所以這類頁面現在可以存。
- 查核流程：
  - 起初用三個背景代理分組查（JP／KR+VN／TW+HK+SG+TH），查完 56 間後，於 2026-09-11 16:30 UTC 改成一個 workflow。已查完的 56 間沿用原結果，其餘並行查核。
  - 沒有 verified 頁的店，另派一個代理用不同方法再找一次：地圖頁的訂位按鈕、店名變體、該國所有可能的平台。
  - 每一個 verified 頁都由兩個獨立代理複核，一個查分店身分、一個查訂位功能，兩者都駁不倒才保留。
  - 複核結果由 scratchpad 的 `apply_verdicts.py` 寫回各店的查核檔，再由 `build_reviews.py` 合成資料檔。
- PR #408。CI 的 `api` 與 `full-stack-smoke` 會紅，原因與本 PR 無關：Docker Hub 已不開放匿名拉取，
  `minio/minio:latest` 拉不下來（`docker: pull access denied`）。PR #407 正在把 MinIO 改從 quay.io 拉並釘版本。
  等 #407 進 main，把 main 併進本分支重推一次，CI 就會綠。`containers` 這個 job 本來就是綠的。
