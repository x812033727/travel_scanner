---
id: 2026-09-11-quota-and-limits-shown-too-late
title: 餘額與行程上限都只在使用者投入之後才告知
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T17:18:54Z
created_at: 2026-09-11T03:20:35Z
completed_at: 2026-09-11T17:37:02Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/components/usage-catalog-provider.test.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
  - apps/web/components/usage-catalog-provider.tsx
  - apps/web/messages/en/newTrip.json
  - apps/web/messages/ja/newTrip.json
  - apps/web/messages/ko/newTrip.json
  - apps/web/messages/zh-CN/newTrip.json
  - apps/web/messages/zh-TW/newTrip.json
---

# 餘額與行程上限都只在使用者投入之後才告知

## Why

兩個限制都是「填完才知道」：

**20 筆行程上限。** `apps/api/app/usage/service.py:114` 的 `COMMON_LIMITS = {"saved_trips": 20, "price_alerts": 20}`。`new-trip-form.tsx:225-238` 的 `validate()` 完全沒有容量檢查，使用者填完目的地、日期、人數、偏好、備註，按下建立才被 `:273` 的 POST 打回。五語系的 `newTrip.json` 從頭到尾沒提過這個上限。`search-experience.tsx:812-833` 的 `save(plan)` 也一樣——而那是在一次已經扣過次數的搜尋之後。

`account-list.tsx:269-276` 確實有顯示數量，但只在 `/trips` 頁、而且只在「已有行程」的分支裡。第一次建行程的人看不到。

**剩餘次數。** 精靈、`/trips/new`、規劃器都不顯示餘額。`useOperationCharge`（`usage-catalog-provider.tsx:72-82`）只給「這個動作要扣幾次」的標籤，不給「你還有幾次」。`usage-insufficient-notice.tsx:21-27` 是**失敗之後**才去抓 `/usage`。

## Definition of done

- [x] 使用者在開始填表之前就知道自己還有幾次、還能存幾個行程。
- [x] 已達 20 筆上限時，建立表單在送出前就擋下並說明，而不是讓人填完才失敗。
- [x] 五語系文案都提到上限數字。

## Steps

- [x] `usage-catalog-provider.tsx` 增加一個回傳餘額與 `COMMON_LIMITS` 用量的 hook（`/usage` 已同時回傳 `available_uses`、`limits`、`counts`，一次請求就夠）。
- [x] `new-trip-form.tsx` 的 `validate()` 加容量前檢，達上限時停用送出鈕並給出「先刪掉一個行程」的連結。
- [x] 在精靈與規劃器頂部常駐顯示餘額與本次將扣次數。
- [x] 五語系 `newTrip.json` 補上限相關文案。

## How to verify

```bash
cd apps/web && npm run test:web -- new-trip-form usage
cd apps/api && uv run pytest tests -k usage -q
```

手動：用一個已有 20 筆行程的帳號開 `/zh-TW/trips/new`，應在填表前就被告知。

## Notes

- 線上 `operation_costs` 全為 0，所以「還有幾次」目前永遠是 3。若決定長期維持 0 扣次，這裡要顯示的可能不是次數而是行程配額——動工前先跟站主確認哪一個數字對使用者有意義。
- 本任務刻意不把 `search-workbench.tsx` 納入 scope，以免與 `2026-09-11-wizard-crash-when-all-criteria-any` 互卡。精靈的餘額顯示等那張做完再併入，或由同一人連著做。

## 完成紀錄（claude-opus-5, 2026-09-11）

`usage-catalog-provider.tsx` 多了 `useAccountUsage()`：打一次 `/usage`，同時拿到 `available_uses`、`limits`、`counts`。原本那裡只有 `useOperationCharge()`，它回答的是「這個動作要扣幾次」，沒有任何東西回答「你還有幾次」。

搭配一個 `savedTripsAtCapacity()`，刻意只在**確知**上限且已達到時回 true。摘要讀不到就不擋——伺服器本來就會擋，前端讀不到餘額不該變成連表都不能填。

用在兩個地方：

- `new-trip-form.tsx`：表單上方常駐一行「剩餘 8 次 · 已儲存 3／20 個行程」；達上限時換成一張說明卡（含「去管理我的旅程」連結），`fieldset` 與送出鈕一起停用，`validate()` 也加了前檢當作第二道。
- `search-experience.tsx`：`chargeHelp` 那一行後面接上「目前可用 N 次」。這支只在 `authState === "signed_in"` 時才呼叫 hook——未登入的人不該為了一個註定 401 的請求被問一次，layout 對 `/auth/me` 與 `/saved-items` 也是同樣的處理。

### 驗證

`usage-catalog-provider.test.tsx`（新檔）四個案例釘住 hook 本身：一次請求拿齊三個數字、未登入不發請求、失敗時回 `unavailable` 而不是猜、以及 `savedTripsAtCapacity` 的四種狀態。

`new-trip-form.test.tsx` 加三個案例：填表前就看到餘額、達上限時擋在前面（斷言送出鈕與目的地欄位都 disabled、連結指向 `/zh-TW/trips`）、以及摘要讀不到時表單仍可用。

原本的 `expect(fetch).not.toHaveBeenCalled()` 改寫成「掛載時只會有 `/usage` 這一個請求」——那條斷言的用意是「不要自動呼叫 AI／路線／地理編碼」，現在寫成實際的意思，而不是放寬成不檢查。

把 `atCapacity` 改成常數 `false` 之後，「stops at the trip limit」那條變紅；復原後 38 passed，整套 228 files / 2309 tests 全過。

### 沒做的

Steps 第三條寫的是「精靈與規劃器頂部常駐顯示」。精靈做了；規劃器（`trip-editor.tsx`）沒有——它在 `2026-09-10-seoul-day2-transport-ux` 的 scope 裡，而且規劃器本身不扣次數（扣次的是它裡面的 AI 安排與搜尋動作，那些已經各自顯示扣次標籤），常駐一條餘額的價值比在建立表單與精靈上低很多。
