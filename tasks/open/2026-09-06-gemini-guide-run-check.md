---
id: 2026-09-06-gemini-guide-run-check
title: 選 Gemini 做景點介紹搜尋會 500：run 表的 provider 檢查沒有 gemini
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T15:32:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/migrations
  - apps/api/tests/test_hotspot_admin_guides.py
---
# 選 Gemini 做景點介紹搜尋會 500：run 表的 provider 檢查沒有 gemini

## Why

`hotspot_guide_ai_search_runs.provider` 的檢查條件是 `provider IN ('minimax', 'openai', 'anthropic')`（`apps/api/app/models.py:1145-1148`，由 migration 0021 建立後沒再放寬），但同一條路徑上的兩處早已接受 Gemini：

- `apps/api/app/config.py:358` 的 `hotspot_guide_ai_default_provider` 型別是 `Literal["minimax", "openai", "anthropic", "gemini"]`；
- `apps/api/app/hotspots/admin_router.py:911` 用 `payload.provider or settings.hotspot_guide_ai_default_provider` 決定值，`AIProviderName`（`ai_search.py:44`）也含 gemini。

所以管理員在 `/admin/settings` 把景點介紹搜尋的供應商設成 Gemini（或在請求裡指定 `provider: "gemini"`）後，`POST /admin/hotspots/guides/ai-search` 會在 INSERT 時撞上 CHECK，整個請求 500。PR #204 把 Gemini 加進供應商清單時漏了這張表。

發現於 2026-09-06 熱門景點主題那次改動的稽核；新的 `hotspot_intro_runs` 一開始就把 gemini 寫進 CHECK，所以只剩 guide 這張表要修。

## Definition of done

- [ ] 把 `ai_guide_search` 選成 Gemini 後能成功建立一次 AI 介紹搜尋，不再 500。
- [ ] 資料庫的檢查條件與 `AIProviderName` 一致，不是只有應用層擋。

## Steps

- [ ] 新 migration：`ALTER TABLE hotspot_guide_ai_search_runs DROP CONSTRAINT ck_hotspot_guide_ai_search_provider` 後重建成含 `'gemini'` 的版本（照 0036 的 inspect-first 寫法，`downgrade` 要能回去）。
- [ ] `apps/api/app/models.py:1145-1148` 的 `CheckConstraint` 同步加上 gemini，否則新舊資料庫又不一致。
- [ ] 測試：`tests/test_hotspot_admin_guides.py` 加一個以 gemini 建立 run 的案例；順手檢查 `AIProviderName` 的每個值都通過 CHECK（避免下次再漏）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_admin_guides.py tests/test_schema.py -q
cd apps/api && RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_hotspot_admin_integration.py -q
```

後台：`/admin/settings` 把「AI 景點介紹搜尋」供應商設成 Gemini，再到 `/admin/hotspots#guides` 送一次 AI 搜尋，應該進入 queued 而不是 500。

## Notes

- 同一族的 `hotspot_intro_runs`（migration 0050）已經是四家都允許，可以照抄它的 CHECK 寫法。
- 只改 CHECK 就好，`provider` 欄位長度 `String(16)` 放得下 `gemini`。
