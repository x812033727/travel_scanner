---
id: 2026-09-06-admin-planner-test-real-candidates
title: 後台 AI 規劃連線測試送空候選，看不見真正會壞的那一步
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T14:52:05Z
created_at: 2026-09-06T14:52:03Z
completed_at: 2026-09-06T14:52:06Z
branch: fix/admin-planner-test-real-candidates
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/tests/test_admin_provider_settings.py
---

# 後台 AI 規劃連線測試送空候選，看不見真正會壞的那一步

## Why

`/admin/settings` 的「AI 行程規劃」按「測試連線」時，`_test_provider` 建的請求是
`AIItineraryRequest(...)` 而沒有 `candidates`，所以 `candidates` 走 `Field(default_factory=list)`
變成空清單。它因此只驗證了「金鑰有效、供應商連得到、結構化輸出解析得動」。

**這正是 `2026-09-06-tokyo-planner-duration-500` 全程綠燈的原因。** 那個缺陷發生在
`_load_ai_planner_candidates` 用 `metadata_json` 建 `AIPlannerCandidate` 的那一步，一筆
20 分鐘的種子值低於 `Field(ge=30)` 就拋 `ValidationError`，而 `main.py` 只註冊了 `AppError`
與 `RequestValidationError`，於是每一次東京的 AI 規劃都回 500。測試送空候選，永遠走不到那一步。

換句話說，這個健康檢查量的東西不是使用者會遇到的東西。

## Definition of done

- [x] 「測試連線」會載入該城市真實的候選地點，走過與真正建立行程相同的候選建構程式碼。
- [x] 候選建構失敗時，測試失敗並顯示原因，而不是回報成功。
- [x] 成功訊息帶出候選數量，讓操作者一眼看出它真的讀到資料了。

## Steps

- [x] `_test_provider` 增加 `session` 參數，`test_provider_connection` 把自己的 session 傳進去。
- [x] `ai_planner` 分支延遲 import `_load_ai_planner_candidates`（`app.trips.router` 會 import
      `app.admin.service`，模組層 import 會造成循環），載入 `TEST_DESTINATION_NAME` 的候選並放進請求。
- [x] 目的地抽成常數並註明它必須是 `match_destination` 解析得出的名稱，否則候選會是空的、
      等於這個修改沒有生效（已驗證「東京」解析為 `tokyo`）。
- [x] 兩個測試：候選真的被載入並傳進請求、以及候選建構失敗時測試會失敗。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_provider_settings.py -k ai_planner -q
```

部署後在 `/admin/settings` → AI 服務 → AI 行程規劃 按「測試連線」，訊息應為
`minimax / MiniMax-M3 結構化行程驗證成功（東京 N 個候選地點）`，其中 N 大於 0。

## Notes

**刻意沒有把「候選數為 0」當成失敗。** 全新安裝或還沒匯入種子的環境本來就會是 0，把它當錯誤
會製造假警報。數量顯示在訊息裡，操作者看得到；真正該擋下的是候選**建構失敗**，那已經會讓測試失敗。

**成本**：測試現在會把真實候選放進提示詞，token 用量比以前高。這是手動按鈕，不是排程檢查，可以接受，
而且這正是它該做的事——用和真實請求一樣的輸入去驗證。

**同一輪查證中確認、但不在此處理的**：`_configured()` 只憑金鑰存在與否判斷就緒狀態，所以卡片可能
顯示綠燈而功能不通；`booking_demand` 的測試停在城市 ID 解析、從不解析真正的旅館報價。兩者都是同一個
形狀的問題——健康檢查量的不是使用者會遇到的東西——但各自要動不同的程式碼，值得另開任務。
