---
id: 2026-09-06-account-signed-out-states
title: 未登入開 /account 會同時看到三種互相矛盾的狀態
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-06T17:32:56Z
completed_at:
branch:
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

- [ ] 未登入的 `/account` 只有一種說法：一句話、一顆按鈕。
- [ ] 不再對已知未登入的情況重複打 API。

## Notes

`components/account-list.tsx` 裡的 `LoadError` 已經是想要的樣子，可以抽成共用元件。
