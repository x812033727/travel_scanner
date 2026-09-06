---
id: 2026-09-06-account-signed-out-states
title: 未登入開 /account 會同時看到三種互相矛盾的狀態
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:11:05Z
created_at: 2026-09-06T17:32:56Z
completed_at: 2026-09-06T18:21:33Z
branch: claude/account-signed-out
depends_on: []
scope:
  - apps/web/components/account-saved-items.tsx
  - apps/web/components/account-list.tsx
  - apps/web/app/[locale]/account/page.tsx
---

# 未登入開 /account 會同時看到三種互相矛盾的狀態

## Why

未登入開 `/zh-TW/account`（桌機與手機都一樣），同一個畫面上同時有三種說法：

1. 收藏統計「全部 0 / 景點 0 / 美食 0 / 店家 0 / 餐廳 0」——看起來像「你沒有收藏」。
2. `role=alert`：「收藏暫時無法載入：請先登入，收藏才會跟著你的帳號。」——看起來像故障。
3. 最下面另一句要求登入的話。

`/trips` 與 `/alerts` 的做法是對的：一句「登入後才能查看這裡的內容」加一顆「前往登入」。
2026-09-07 已經把 `account-panel` 換成那個樣子，但同一頁的收藏卡與清單還各自處理 401。

另外量到未登入的 `/account` 會打 10 次 API，其中 8 次回 401（`auth/me` 三次、
`saved-items` 兩次）。

## Definition of done

- [x] 未登入的 `/account` 只有一種說法：一句話、一顆按鈕。
- [x] 不再對已知未登入的情況重複打 API。

## Notes


`components/account-list.tsx` 裡的 `LoadError` 已經是想要的樣子，可以抽成共用元件。

### 做完之後（2026-09-07，claude-opus-5）

收藏卡未登入時**整張不顯示**，而不是換一句話。理由是 `account-panel` 已經在同一頁講了那句話
配那顆按鈕（2026-09-07 改的），收藏卡再講一次就又變成兩種說法——這張任務要的是「一句話、一顆按鈕」，
不是「兩張漂亮的卡」。

不重複打 API 的做法：`SavedItemsProvider` 已經問過 `/saved-items` 並把答案發成
`loading / authenticated / signed_out / unavailable` 四種狀態，收藏卡改成等它的答案，
只有 `authenticated` 才自己去拿完整清單。因此少一次注定 401 的請求，
未登入時骨架也不會空轉（`ready` 由狀態推導，不再 `setLoaded(true)`——
在 effect 裡同步 setState 會被 lint 的 cascading-render 規則擋下來）。

順手拿掉 `copy` 表裡五個語系的 `signIn` 字串與 `ApiError` 的 import：那條 401 分支已經沒有讀者。

**正式站量到的完整數字**（未登入 `/zh-TW/account`）：十個請求、八個 401——
`auth/me` ×3、`saved-items` ×2、`usage`、`auth/identities`、`usage/history` 各一。
這張修掉其中一個 `saved-items`，剩下的都在 `account-panel` 與 `site-header`（不在本 scope），
連同量到的數字另立 `2026-09-06-signed-out-account-requests`。
