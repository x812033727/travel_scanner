---
id: 2026-09-11-offer-cards-hardcoded-zh-tw
title: 機票與飯店結果卡硬編碼繁中
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T16:02:08Z
created_at: 2026-09-11T03:20:36Z
completed_at: 2026-09-11T16:19:38Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/flight-offer-card.tsx
  - apps/web/components/hotel-offer-card.tsx
  - apps/web/components/flight-offer-card.test.tsx
  - apps/web/components/hotel-offer-card.test.tsx
  - apps/web/components/offer-cards-i18n.test.tsx
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

- [x] 兩個結果卡不再有寫死的使用者可見中文。
- [ ] `/en/search` 跑完一次搜尋，整頁（含結果卡）沒有中文。

## Steps

- [x] 字串搬進 `messages/*/search.json`，沿用既有的 `search.results` 命名慣例。
- [x] `` `${hours} 小時` `` 這類插值改用 ICU 參數。
- [x] 金額與數字格式依 locale。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run test:web -- offer-card
```

## Notes

- 與 `2026-09-11-search-result-dead-ends` 共用 `messages/*/search.json`，兩張任務不要同時認領。

## 瀏覽器實測補充（2026-09-11 第二輪）

用真實瀏覽器對 `en` / `ja` / `ko` 共 12 條路由，搜尋第一輪點名的 27 個寫死繁中字串，**零命中**。

**這不代表本任務的問題不存在，而是那些程式路徑在唯讀環境下走不到**：刪除確認框需要帳號裡有行程（測試帳號 0 筆）、機票與飯店卡需要完成一次搜尋（環境只轉讀取，不送寫入）、行程時間軸需要行程裡有項目。

所以本任務的狀態是**未驗證**，不是**已推翻**。接手的人請自己建一筆有內容的行程再確認，不要因為「掃描沒掃到」就把它關掉。

順帶澄清一個第二輪用過的無效指標：曾以「頁面漢字佔比」推估洩漏程度，但**日文本來就使用漢字**（實測 `ja` 頁面漢字 28–37%，同時有大量假名，是真正的日文），該指標對日文無效，不可採信。英文頁實測漢字僅 0.2–5.2%，且經逐一檢查後確認全部來自語言切換器的語言名稱（繁體中文／简体中文／日本語），屬正確做法。

## 完成紀錄（claude-opus-5, 2026-09-11）

兩張結果卡的漢字歸零。新增 `search.results.flightCard.*`（42 個 key）與 `search.results.hotelCard.*`（18 個），能重用的就重用既有的 `search.results.*`：`stops`、`direct`、`sourceLine`、`unlabelled`、`refundable`、`goToProvider`、`recheckExternal`、`stationWalk`、`room`、`imageCredit`，以及 `source.{live,test,mock,estimate}`。

`hotel-offer-card.tsx` 原本自己有一份 `sourceLabels`，四句話和 `search.results.source.*` 一字不差——那份是死的第二套，直接刪掉改讀 catalog。

`` `${hours} 小時` `` 這種字串拼接改成三個 ICU key（`durationHoursMinutes` / `durationHours` / `durationMinutes`），讓語系自己決定要不要空格、單位放哪裡。

### 兩件順手修的事

1. **`twd.format()` 會把沒換算成功的價格標成台幣。** `duffel.py:194-205` 換匯失敗時會保留原幣，把 `display_currency` 留在原幣，而 `offer.currency` 就是這個欄位——同一張卡的 `PriceAlertButton` 早就在讀它。兩張卡都改成 `formatCurrency(value, offer.currency || "TWD")`。
2. 航班卡的「原幣」那一行本來寫死和 `"TWD"` 比較，現在和 `offer.currency` 比較，否則上面那種情況會出現「原幣 JPY … 」而主價格也是 JPY。

### 驗證

新增 `offer-cards-i18n.test.tsx`，做法和 `account-list-i18n.test.tsx` 一樣：catalog 回傳 `[namespace.key]`、fixture 一律英文、斷言畫面零漢字。額外設 `document.documentElement.lang = "en"`，因為 `formatCurrency` 和 `toLocaleString` 讀的是文件語言而不是 hook（zh-TW 的日期會印出「下午」，那是漢字）。

覆蓋到收合與展開的航班卡、重新驗價後的「已售罄」訊息、以及過期的飯店報價。把航班卡的「可退款／不可退款」和飯店卡的「住宿總價」還原成寫死之後：

```
× writes no Chinese of its own on a flight, open or collapsed
× says a fare sold out without falling back to Chinese
× writes no Chinese of its own on an expired hotel quote
AssertionError: hardcoded copy after re-checking a price: expected '不可退款' to be undefined
```

復原後 3 passed，原本的 `flight-offer-card.test.tsx` 與 `hotel-offer-card.test.tsx` 共 7 個案例照舊通過。

### 沒打勾的那一項

「`/en/search` 跑完一次搜尋，整頁（含結果卡）沒有中文」—— **沒有實際跑過**。本機環境接 production 資料的轉接層是唯讀的（只轉 GET），而搜尋是 POST 加 SSE，所以跑不了一次真的搜尋；對 production 送出搜尋會消耗站主的次數與供應商額度，不該由我代為觸發。

改以元件測試覆蓋兩張卡的每一種狀態（含展開、售罄、過期），並確認 `search-experience.tsx` 本身在 `tasks/done/2026-09-06-search-results-i18n.md` 已經搬完。整頁的實際確認要留給有辦法跑搜尋的人——站主自己用 `/en/search` 跑一次最快。
