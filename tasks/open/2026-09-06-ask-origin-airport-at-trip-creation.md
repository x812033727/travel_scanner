---
id: 2026-09-06-ask-origin-airport-at-trip-creation
title: 建立旅程時就問出發機場，不要等到查機票才問
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T20:33:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/messages/en/newTrip.json
  - apps/web/messages/ja/newTrip.json
  - apps/web/messages/ko/newTrip.json
  - apps/web/messages/zh-TW/newTrip.json
  - apps/web/messages/zh-CN/newTrip.json
---

# 建立旅程時就問出發機場，不要等到查機票才問

## Why

空白旅程沒有出發機場，但查機票一定要一個。PR #249 讓 `/search?trip_id=…` 在缺出發地時
於頁內問一次並用 `PATCH /trips/{id}` 存回旅程，所以流程是通的——只是問的時機不對：
使用者已經按下「查機票」、心裡準備看價格了，卻先被攔下來回答一個建立旅程時就知道的問題。

`docs/user-flow-plan.md` 的 Q2 早就寫下建議做法：(a) 建立旅程的表單多一格，(c) 預設值來自
會員偏好（像 `preferred_currency` 那樣）。後端已經備好：`SaveTripRequest.origin_airport`
會寫進 `data`，`PATCH /trips/{id}` 也收這個欄位，兩邊都有測試。缺的只有表單那一格。

## Definition of done

- [ ] 建立旅程的表單有出發機場，預設 TPE，桃園／松山／高雄三選一（和規劃工作台同一組）。
- [ ] 新建立的旅程按「查機票」直接開始搜尋，不再被出發地面板攔一次。
- [ ] 沒填也不會擋住建立旅程：後端仍然接受沒有出發地的旅程，`/search` 的面板仍是後備。

## Steps

- [ ] `new-trip-form.tsx` 的旅伴那一步加上出發機場，送進 `POST /trips` 的 `origin_airport`。
- [ ] 文案進五個語系的 `newTrip.json`；機場名稱沿用 `search.workbench.originTpe/Tsa/Khh`
      的說法，不要再寫一組。
- [ ] （選配，會超出目前 scope）把預設值改成讀會員偏好，需要 API 那邊多一個欄位，
      要做的話另開一張 api 的任務，不要在這張裡動後端。

## How to verify

```bash
npm run test:web -- components/new-trip-form.test.tsx
npm run check:i18n && npm run typecheck:web
```

手動：建立一個空白旅程並選高雄，開旅程頁按「查機票 · 消耗 N 次」，應該直接進搜尋條件、
沒有「這趟旅程還沒有出發機場」那一段。

## Notes

- 後端不用改：`origin_airport` 從 PR B 起就在 `SaveTripRequest`，PR #249 又補上 `PATCH`。
- `/search` 的出發地面板留著：從搜尋存下來的舊旅程、或使用者略過這一格時仍然需要它。
