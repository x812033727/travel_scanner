---
id: 2026-09-06-signed-out-account-requests
title: 未登入的 /account 仍打七次注定 401 的請求
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T19:04:50Z
created_at: 2026-09-06T18:20:44Z
completed_at: 2026-09-06T19:29:58Z
branch: claude/signed-out-requests
depends_on: []
scope:
  - apps/web/app/[locale]/layout.tsx
  - apps/web/components/account-panel.tsx
  - apps/web/components/account-panel.test.tsx
  - apps/web/components/currency-switcher.tsx
  - apps/web/components/currency-switcher.test.tsx
  - apps/web/components/header-session.tsx
  - apps/web/components/site-navigation.tsx
  - apps/web/components/site-navigation.test.tsx
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

- [x] 未登入的 `/account` 對 `auth/me` 只送一次請求。
- [x] 已知未登入時，不再送 `usage`、`usage/history`、`auth/identities`。
- [x] 已登入的行為完全不變（三塊資料都還在，且不多送請求）。

## Steps

- [x] 看 `SavedItemsProvider` 的形狀：它已經是「問一次、把 loading／authenticated／
      signed_out／unavailable 四種狀態發給所有人」的樣子。帳號狀態需要同一個東西，
      可以是新的 provider，也可以擴充現有的。
- [x] `account-panel` 的三個請求改成等狀態確定是 authenticated 才送。
- [x] `site-header` 與使用次數區塊改讀同一個狀態，不要各自打 `auth/me`。

## How to verify

未登入開 `/zh-TW/account`，DevTools 的 network 面板過濾 `/api/travel/`：
`auth/me` 只有一次，`usage`、`usage/history`、`auth/identities` 都不出現。
登入後再看一次，三塊資料都在。

## Notes

- `analytics/config` 與 `auth/oauth/providers` 回 200，本來就該送，不在此列。
- 順帶一提：`saved-items` 那一次是 provider 自己的，它就是判斷登入狀態的那個請求，該留。

### 做法（2026-09-07）

不必新開 provider：`HeaderSessionProvider` 早就是那個形狀（loading／authenticated／
signed_out／unavailable 四態、一個 `/auth/me`），只是被掛在 `site-navigation.tsx` 裡面，
所以只有導覽列讀得到。把它搬到 `app/[locale]/layout.tsx`，整頁就共用同一個答案。

三處改動：

- `header-session.tsx`：`HeaderUser` 補上 `/auth/me` 其餘欄位（`preferred_currency`、
  `has_password`、`auth_methods`、`identity_count`），context 多發一個 `setUser`，
  讓解除綁定與換幣別能把新的 profile 寫回共用狀態。
- `currency-switcher.tsx`：不再自己打 `/auth/me`；幣別由 `user.preferred_currency` 推導，
  本地選擇（`chosen`）蓋在上面。401 → provider 說 `signed_out` → 整塊不顯示；
  503 → `unavailable`，仍給預設幣別的可用控制項（原本的行為）。
- `account-panel.tsx`：`/usage` 與 `/auth/identities` 移進 `status === "authenticated"` 的
  effect，`/usage/history` 同樣加守衛；`me` 直接讀 provider。非 401 的載入失敗原本秀 API
  回來的句子，現在 provider 不留訊息，改成固定一句「目前無法載入帳號資料，請稍後再試。」

`site-navigation.test.tsx` 那三個 render 現在要自己包 provider（真實情況由 layout 包）。
兩支測試各加一個案例把次數釘住：未登入時 `auth/me` 恰好一次、`usage`／`identities` 完全沒送；
已登入時四個端點各一次。

### 沒改的

- `admin-nav.tsx`、`new-trip-auth-gate.tsx`、`offline-trip-cache.tsx`、`search-experience.tsx`
  也各自打 `/auth/me`，但都不在 `/account` 這一頁上，而且 `admin-nav` 要的 `can_deploy` 不在
  `/auth/me` 給 header 的欄位裡。留給需要時另立任務。
- `auth/oauth/providers` 照 Notes 第一行，維持每次都送。
