---
id: 2026-09-07-pre-departure-loop
title: 出發前閉環：提醒連得回旅程、錨點能追價、航班動態寫得回去
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T00:45:08Z
created_at: 2026-09-07T00:44:58Z
completed_at: 2026-09-07T08:59:29Z
branch: claude/pre-departure-loop
depends_on: []
scope:
  - apps/api/app/alerts/router.py
  - apps/api/app/trips/flight_anchor.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_alerts_integration.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/web/app/[locale]/flights/status/page.tsx
  - apps/web/components/account-list.test.tsx
  - apps/web/components/account-list.tsx
  - apps/web/components/flight-anchor-card.test.tsx
  - apps/web/components/flight-anchor-card.tsx
  - apps/web/components/flight-status-search.test.tsx
  - apps/web/components/flight-status-search.tsx
  - apps/web/components/line-link-panel.test.tsx
  - apps/web/components/line-link-panel.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-price-watch.test.tsx
  - apps/web/components/trip-price-watch.tsx
  - apps/web/e2e/full-stack.spec.ts
  - apps/web/lib/trip-types.ts
  - apps/web/messages/en/alerts.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/alerts.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/alerts.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/alerts.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/alerts.json
  - apps/web/messages/zh-TW/trips.json
  - docs/user-flow-plan.md
---

# 出發前閉環：提醒連得回旅程、錨點能追價、航班動態寫得回去

## Why

`docs/user-flow-plan.md` 的 PR F。旅程存下來之後，出發前的四個工具（價格通知、LINE、
航班動態、錨點）各自為政：提醒清單只列得出標題，點下去沒有任何回旅程的路；旅程層的價格
通知追的是 `trip.total_price`——一個把真實報價和估算混在一起、而且沒有任何 provider 會
重查的數字，所以它永遠只能是 `manual_only`，文案還叫人「在搜尋頁手動查看」，但那個搜尋頁
根本不存在；航班動態查完就散在畫面上，回不到旅程。

這張任務接在 PR #249（`2026-09-06-search-from-a-saved-trip`）之後，分支從它長出來，PR 是 #313。

## Definition of done

- [x] 提醒回應帶 `links {trip_id, search_id}`，清單與三個單筆讀取都有；只認同一位會員的
      旅程與搜尋。
- [x] 提醒卡連得回旅程；`manual_only` 那行從死路改成「到旅程頁重新查價」。
- [x] 錨點有報價時可以直接在卡片上建機票提醒。
- [x] 旅程層的提醒改成對每一筆報價各建一筆（機票建機票、住宿建住宿），沒有報價時說清楚
      為什麼還不能追。
- [x] `/flights/status` 可以從旅程預填，查到的動態寫得回錨點，錨點卡顯示狀態與延誤。
- [x] LINE 綁定過期與錯誤兩個訊息都給得出 `/alerts` 的去處。
- [x] 五語系文案、單元／整合／e2e 測試。

## Steps

- [x] 後端 `alert_links()` 一次查完整份清單，四個序列化點共用。
- [x] `POST /trips/{id}/flight-anchors/{direction}/flight-status`：伺服器重讀該會員自己的
      `FlightStatusLookup`，客戶端只給 `lookup_id` 與 `item_id`。
- [x] 前端 `trip-price-watch.tsx`、`flight-status-search.tsx` 的旅程模式、錨點卡的狀態列。
- [x] 整合測試（需要 Postgres/Redis）、e2e 兩個 viewport（六個情境全過）。
- [x] 開 PR：#313，base 是 #249 的分支。
- [ ] 合併（#249 先合，這個 PR 的 base 會自動變成 main）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_alerts_integration.py tests/test_integration_postgres_redis.py
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npx playwright test e2e/full-stack.spec.ts
```

## Notes

- **scope 和 `2026-09-06-search-from-a-saved-trip` 重疊，用 `--force` 認領**：那張是同一個
  owner、正在等 PR #249 合併，這張的分支就是從它長出來的，所以重疊是預期的而不是撞車。
  重疊的檔案：`apps/api/app/trips/flight_anchor.py`、`apps/api/app/trips/router.py`、
  `apps/web/components/flight-anchor-card.tsx`、`apps/web/components/trip-editor.tsx`、
  `apps/web/e2e/full-stack.spec.ts`、`apps/web/lib/trip-types.ts`、四個 `trips.json`、
  `docs/user-flow-plan.md`。#249 先合，這個分支再 rebase。
- 航班動態的寫回沒有做成規劃裡的 `PUT …/status_snapshot`：那會讓客戶端寫進任意狀態文字。
  改成伺服器自己重讀 lookup，客戶端只指名要哪一筆。
- 這個 repo 的 CI 在 push 與 pull_request 都跑，`tools/check-i18n.mjs` 的 CI 模式比對
  `HEAD^..HEAD`，所以合併提交會讓它看不到 main 帶進來的中文。這個分支只 rebase，不 merge。
- 「新增一餐」原本也在 PR F 的範圍裡，抽出來成 `2026-09-07-add-a-meal-to-a-day`。
- e2e 的 `pickTripDay()` 原本以 `page.waitForLoadState("networkidle").catch(() => {})` 開頭，
  但那個等待沒有自己的 timeout：`/trips/new` 在這個環境永遠到不了 networkidle，所以 `catch`
  永遠不會執行，整個測試的 150 秒就這樣被吃掉，失敗還報在下一行——看起來像月份按鈕壞了。
  補上 5 秒 timeout 之後，同一批六個情境從 9.5 分鐘的逾時變成 59 秒全過。
- 另外兩件順手記下的：`2026-09-07-fixed-email-in-integration-tests`（整合測試用寫死的 email，
  同一個資料庫跑第二次就 UniqueViolation）、`2026-09-07-board-conflicts-on-every-pr`
  （BOARD.md 是產生檔卻讓每個 PR 互相衝突，#249 在 90 分鐘內因此 dirty 兩次）。
