---
id: 2026-09-06-admin-load-error-copy
title: 後台載入失敗時把原始 JS 例外與 ADMIN_EMAILS 提示一起丟給管理者
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:26:18Z
created_at: 2026-09-06T13:26:22Z
completed_at: 2026-09-06T18:41:42Z
branch: claude/admin-error-copy
depends_on: []
scope:
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 後台載入失敗時把原始 JS 例外與 ADMIN_EMAILS 提示一起丟給管理者

## Why

（原本的內容是沒填的模板，以下是動手時查出來的實際情形。）

`admin-settings-panel.tsx` 載入後台快照的錯誤處理只有一行：

```tsx
.catch((reason: Error) => { if (active) setLoadError(reason.message); });
```

畫面固定長這樣：標題、`reason.message`、然後**永遠**接一句
「請先在主機設定 ADMIN_EMAILS，或將帳號的 is_admin 設為 true。」

兩個問題：

1. **不是所有失敗都來自伺服器。** `fetch` 本身失敗時（斷線、DNS、CORS）丟的是瀏覽器的
   `TypeError`，`reason.message` 是 `Failed to fetch` 這種字串——五個語系都不會翻，而且講的是
   網路不是權限。`api()` 只有在拿到 HTTP 回應時才丟 `ApiError`，那種才有本地化過的訊息。
2. **ADMIN_EMAILS 那句只有 401／403 成立。** 500、502 或斷線時照樣顯示，等於叫一個網路斷掉的
   管理者跑去改主機環境變數。

## Definition of done

- [x] 網路層失敗顯示本地化的「連不到伺服器」，不再把瀏覽器的原生例外字串丟給使用者。
- [x] ADMIN_EMAILS 提示只在 401／403 出現。
- [x] 伺服器有回訊息時仍然顯示伺服器的訊息（那是已經本地化過、而且更具體的）。
- [x] 可以重試的情況要有重試的路。

## Steps

- [x] 把「失敗是什麼」抽成 `loadFailure(reason)` 純函式，回 `permission` / `unreachable` / `failed`。
- [x] `unreachable` 用新的 `settingsPanel.loadErrorUnreachable`，其餘沿用伺服器訊息。
- [x] 提示與重試按鈕依 kind 顯示；有 request id 就一起顯示，方便回報。
- [x] 測試涵蓋三種失敗。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run check:i18n
cd apps/web && npx vitest run admin-settings
```

## Notes

`loadErrorRequestId` 顯示的是 `X-Request-Id`，在伺服器 log 裡查得到，比原始例外字串有用得多。

## Result（2026-09-07 完成）

三種失敗現在分開處理：

| 狀況 | 訊息 | ADMIN_EMAILS 提示 | 重試 |
| --- | --- | --- | --- |
| 401／403 | 伺服器的訊息（例：此功能僅限系統管理員使用） | 有 | 沒有（重載也會被擋） |
| 其他 HTTP 狀態 | 伺服器的訊息 | 沒有 | 有 |
| `fetch` 本身失敗 | 「連不到伺服器。請確認網路連線，或稍後再試。」 | 沒有 | 有 |

**伺服器訊息保留下來了。** 我一開始把 401／403 換成自己寫的通用句，既有測試立刻擋下來——
伺服器回的「此功能僅限系統管理員使用」比通用句具體，而且 `api()` 已經依 `X-Travel-Locale`
本地化過。所以 kind 只決定「要不要顯示提示與重試」，訊息一律用伺服器的。

順帶：`useEffect` 直接呼叫 async 函式會被 eslint 的 cascading-renders 規則擋下，
所以載入邏輯留在 effect 的 promise 鏈裡，只把失敗判定抽成純函式給重試共用。

檢查：`lint:web`、`typecheck:web`、`check:i18n`（含 staged Han guard）、
`vitest run admin-settings`（28 passed）全綠。
