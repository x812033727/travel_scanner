---
id: 2026-09-06-signed-out-account-requests
title: 未登入的 /account 仍打七次注定 401 的請求
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T18:20:44Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/account-panel.tsx
  - apps/web/components/site-header.tsx
  - apps/web/components/usage-summary.tsx
---

# 未登入的 /account 仍打七次注定 401 的請求

## Why

2026-09-07 在正式站量的（未登入、`/zh-TW/account`、瀏覽器 network 面板）：

| 請求 | 次數 | 回應 |
| --- | --- | --- |
| `auth/me` | 3 | 401 |
| `saved-items?limit=100` | 2 | 401 |
| `usage` | 1 | 401 |
| `auth/identities` | 1 | 401 |
| `usage/history?kind=all` | 1 | 401 |
| `auth/oauth/providers` | 1 | 200 |
| `analytics/config` | 1 | 200 |

十個請求，八個 401。`2026-09-06-account-signed-out-states` 已經拿掉其中一個
`saved-items`（收藏卡改成聽 `SavedItemsProvider` 的答案，不自己再問一次），剩下七個。

三次 `auth/me` 是三個元件各問一次同一件事：`site-header`、`account-panel`，
以及使用次數那一塊。`usage`、`usage/history`、`auth/identities` 都是 `account-panel`
在還不知道有沒有登入的時候就先發的。

這不是效能問題（都是幾十毫秒），是**同一個事實被問了三次還各自處理失敗**——
`2026-09-06-account-signed-out-states` 修掉的三種互相矛盾的說法就是這樣長出來的。

## Definition of done

- [ ] 未登入的 `/account` 對 `auth/me` 只送一次請求。
- [ ] 已知未登入時，不再送 `usage`、`usage/history`、`auth/identities`。
- [ ] 已登入的行為完全不變（三塊資料都還在，且不多送請求）。

## Steps

- [ ] 看 `SavedItemsProvider` 的形狀：它已經是「問一次、把 loading／authenticated／
      signed_out／unavailable 四種狀態發給所有人」的樣子。帳號狀態需要同一個東西，
      可以是新的 provider，也可以擴充現有的。
- [ ] `account-panel` 的三個請求改成等狀態確定是 authenticated 才送。
- [ ] `site-header` 與使用次數區塊改讀同一個狀態，不要各自打 `auth/me`。

## How to verify

未登入開 `/zh-TW/account`，DevTools 的 network 面板過濾 `/api/travel/`：
`auth/me` 只有一次，`usage`、`usage/history`、`auth/identities` 都不出現。
登入後再看一次，三塊資料都在。

## Notes

- `analytics/config` 與 `auth/oauth/providers` 回 200，本來就該送，不在此列。
- 順帶一提：`saved-items` 那一次是 provider 自己的，它就是判斷登入狀態的那個請求，該留。
