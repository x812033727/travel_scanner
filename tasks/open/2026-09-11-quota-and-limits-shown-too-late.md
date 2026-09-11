---
id: 2026-09-11-quota-and-limits-shown-too-late
title: 餘額與行程上限都只在使用者投入之後才告知
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/new-trip-form.tsx
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

- [ ] 使用者在開始填表之前就知道自己還有幾次、還能存幾個行程。
- [ ] 已達 20 筆上限時，建立表單在送出前就擋下並說明，而不是讓人填完才失敗。
- [ ] 五語系文案都提到上限數字。

## Steps

- [ ] `usage-catalog-provider.tsx` 增加一個回傳餘額與 `COMMON_LIMITS` 用量的 hook（`/usage` 已同時回傳 `available_uses`、`limits`、`counts`，一次請求就夠）。
- [ ] `new-trip-form.tsx` 的 `validate()` 加容量前檢，達上限時停用送出鈕並給出「先刪掉一個行程」的連結。
- [ ] 在精靈與規劃器頂部常駐顯示餘額與本次將扣次數。
- [ ] 五語系 `newTrip.json` 補上限相關文案。

## How to verify

```bash
cd apps/web && npm run test:web -- new-trip-form usage
cd apps/api && uv run pytest tests -k usage -q
```

手動：用一個已有 20 筆行程的帳號開 `/zh-TW/trips/new`，應在填表前就被告知。

## Notes

- 線上 `operation_costs` 全為 0，所以「還有幾次」目前永遠是 3。若決定長期維持 0 扣次，這裡要顯示的可能不是次數而是行程配額——動工前先跟站主確認哪一個數字對使用者有意義。
- 本任務刻意不把 `search-workbench.tsx` 納入 scope，以免與 `2026-09-11-wizard-crash-when-all-criteria-any` 互卡。精靈的餘額顯示等那張做完再併入，或由同一人連著做。
