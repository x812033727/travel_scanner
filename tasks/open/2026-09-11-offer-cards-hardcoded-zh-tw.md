---
id: 2026-09-11-offer-cards-hardcoded-zh-tw
title: 機票與飯店結果卡硬編碼繁中
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:36Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/flight-offer-card.tsx
  - apps/web/components/hotel-offer-card.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 機票與飯店結果卡硬編碼繁中

## Why

`tasks/done/2026-09-06-search-results-i18n.md` 把 `search-experience.tsx` 的 102 段文案搬進了 `search.results`，該任務自陳的目標是：

> 用英文填完五步精靈，按下送出，落到一個全繁中的結果頁。

這個目標目前只做到一半。真正的結果卡是兩個獨立檔案，由 `search-experience.tsx:1874` 與 `:1903` 渲染，而它們**從未出現在任何任務的 scope 裡**：

- `flight-offer-card.tsx`：`:87`「供應商未提供」／`:90` `` `${hours} 小時` ``／`:121`「次轉機」「直飛」／`:139`「含手提行李」／`:146`「已更新為供應商最新價格」「此票價目前已售罄」／`:153`「彈性日期估算」「即時航班價格」「航空公司待確認」／`:155-156`「去程」「回程」／`:158`「收合詳細班次」／`:162`「來源：」／`:165`「可退款」「不可退款／需確認」。
- `hotel-offer-card.tsx`：`:43-46` 資料來源標籤（「正式即時資料」「供應商測試資料」「模擬資料」「估算資料」）／`:91`「每晚」／`:95-98`「星」「旅客」「客房」「車站步行 N 分」／`:106-108`「房價」「稅金與費用」「住宿總價」／`:112-113`「早餐已包含」「可退款」／`:116`「來源：…已過期，必須重新確認」／`:118`「前往供應商」。

這是搜尋流程的終點，也是使用者要據以做決定的地方。「可退款／不可退款」「已售罄」「估算 vs 即時」這幾組看不懂，直接影響判斷。

## Definition of done

- [ ] 兩個結果卡不再有寫死的使用者可見中文。
- [ ] `/en/search` 跑完一次搜尋，整頁（含結果卡）沒有中文。

## Steps

- [ ] 字串搬進 `messages/*/search.json`，沿用既有的 `search.results` 命名慣例。
- [ ] `` `${hours} 小時` `` 這類插值改用 ICU 參數。
- [ ] 金額與數字格式依 locale。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run test:web -- offer-card
```

## Notes

- 與 `2026-09-11-search-result-dead-ends` 共用 `messages/*/search.json`，兩張任務不要同時認領。
