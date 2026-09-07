---
id: 2026-09-07-observe-the-funnel
title: 觀測：漏斗看得見——事件名脫離 DB CHECK，關鍵動作由伺服器送
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-07T02:25:46Z
created_at: 2026-09-07T02:25:42Z
completed_at: 2026-09-07T08:59:31Z
branch: claude/observe-the-funnel
depends_on: []
scope:
  - apps/api/app/alerts/router.py
  - apps/api/app/analytics/context.py
  - apps/api/app/analytics/schemas.py
  - apps/api/app/analytics/service.py
  - apps/api/app/foods/router.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/middleware.py
  - apps/api/app/models.py
  - apps/api/app/restaurants/user_router.py
  - apps/api/app/search/router.py
  - apps/api/app/trips/router.py
  - apps/api/app/trips/share_router.py
  - apps/api/app/trips/stay_router.py
  - apps/api/app/usage/service.py
  - apps/api/migrations/versions/0054_analytics_event_names.py
  - apps/api/tests/test_analytics_events.py
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/components/admin-analytics-panel.tsx
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/components/search-workbench.tsx
  - apps/web/lib/analytics.ts
  - apps/web/lib/api.ts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/user-flow-plan.md
---

# 觀測：漏斗看得見——事件名脫離 DB CHECK，關鍵動作由伺服器送

## Why

`docs/user-flow-plan.md` 的 PR I（§4.5）。今天後端一個事件都不送：五個事件名
（`page_view`、`registration_completed`、`search_completed`、`trip_created`、
`outbound_click`）全部由瀏覽器送，所以首頁推薦、加入行程、AI 套用、最佳化套用、報價帶回
錨點、提醒建立、分享、扣次、402 全都看不到。管理後台的漏斗因此只有
`sessions → search_completed → trip_created → outbound_click`，中間發生什麼事只能猜。

事件名還是資料庫的 `CHECK`（`models.py:257-262` 的 `ck_analytics_event_name`），所以每加
一個事件就要一次 migration；`planning-flow-spec.md` §3 已經說過不要重複這個模式。

## Definition of done

- [x] 事件名的唯一真相在 Python，不在資料庫的 `CHECK`。
- [x] 伺服器送得出事件，而且送事件失敗不會讓被觀測的那個請求跟著失敗。
- [x] 伺服器事件和瀏覽器事件用同一個 session 身分，漏斗的每一步才可比。
- [x] `trip_created` 改由伺服器送（含 `source`），瀏覽器那兩處移除。
- [x] 管理後台漏斗改成 `discover_requested → trip_created → offer_attached → outbound_click`。
- [x] 事件屬性不含任何個資：只放列舉值與數字，不放 id、Email、自由文字。

## Steps

- [x] migration 拿掉 `ck_analytics_event_name`（編號改成 0055，main 在這期間用掉了 0054）。
- [x] `analytics/context.py`：仿 `i18n.py` 的 contextvar，由 `RequestContextMiddleware` 綁定，
      這樣 `usage/service.py` 這種拿不到 `Request` 的地方也送得出事件。
- [x] `record_event()`：直接寫 `analytics_events`，不經過訪客 ingest 的 IP／session 速率限制。
- [x] 逐一接上事件（見規劃文件 §4.5 的表）。
- [x] 前端：`lib/api.ts` 帶 `X-Travel-Analytics-Session`、BFF 轉發、`discover_requested`
      與 `login_resumed`、移除瀏覽器的 `trip_created`、後台漏斗文案。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
RUN_INTEGRATION_TESTS=1 uv run pytest
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- **`offer_attached` 只接得到一半。** 規劃寫的是「`from-offer` 與住宿 `select`」，但
  `POST /trips/{id}/flight-anchors/{direction}/from-offer` 只存在於 #249 的分支上。這個分支
  從 main 長出來，所以先接住宿那一半；機票那一行等 #249 進 main 之後補。
- **`_properties()` 的第一版寬到讓 UUID 通過**（`[a-z0-9_.\-]{1,48}` 正好是 UUID 的形狀），
  是自己寫的測試抓到的，不是審查抓到的。現在只放行 `[a-z][a-z0-9_]*`：沒有連字號、沒有點、
  沒有大寫，所以 UUID、Email、主機名稱、會員打的名稱全部整個丟掉而不是截斷——截斷過的
  識別碼還是識別碼。call site 傳的每個列舉值都在 `test_every_literal_the_call_sites_pass_survives_the_filter`
  裡釘住，改名成過不了的形狀會被測試擋下來，而不是安靜地少一個欄位。
- **舊 bundle 的 `trip_created` 是接受但丟掉，不是拒絕。** 拒絕會讓整批 422，那一個分頁
  接下來的 page_view 全部跟著不見；為了修一筆重複而弄丟一整個 session 不划算。
- 這張任務的 scope 和 #249／#313 有三個檔案重疊（`trips/router.py`、`alerts/router.py`、
  `search-experience.tsx`），那兩個 PR 都在等審查。誰先合誰不動，後合的 rebase。
