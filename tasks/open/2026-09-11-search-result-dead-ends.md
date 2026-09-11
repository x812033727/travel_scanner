---
id: 2026-09-11-search-result-dead-ends
title: 搜尋結果頁的零結果失敗與無逾時三個死路
status: open
priority: P0
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/search-experience.tsx
  - apps/api/app/search/router.py
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 搜尋結果頁的零結果失敗與無逾時三個死路

## Why

搜尋是這個產品的核心，也是唯一會扣次數的動作。目前它有三個各自獨立的死路，共同點是：使用者付出了等待（有時還付出次數），然後沒有任何出路。

**一、搜尋成功但零結果 → 一片空白。**
`search-experience.tsx:1487-1489` 用 `plans.length > 0 || Object.keys(offers).length > 0 || flightDateOptions.length > 0` 決定整個結果區塊要不要掛載。三者皆空時，使用者看到進度條跑到 100%、「分析完成」、「已扣 N 次」（`:1452-1464`），然後下面什麼都沒有。`:2003-2010` 的分頁空狀態 `emptyCategory` 明確不涵蓋 `plans`，而且整個區塊根本沒掛載，所以那句話也不會出現。

**二、搜尋失敗 → 沒有重試鈕，文案還指向一顆不在畫面上的按鈕。**
`:771-778` 失敗時顯示 `t("searchFailed")`，其英文是 *"The search returned no results. Check the data source status and try again."*。但「開始搜尋」鈕在 `:1359` 被 `{!searchId && parsed && …}` 包住，而 `searchId` 已在 `:719` 設值——按鈕早就消失了。唯一出路是改條件（`applyCriteria` 會在 `:959` 重設 `searchId`）或重新整理整頁。

**三、沒有逾時、沒有取消，可以永遠轉下去。**
`:721-793` 整個檔案沒有 `AbortController`，也沒有任何 `setTimeout`。`stream.onerror`（`:779-793`）只在 `readyState === CLOSED` 時處理，但伺服器端正常結束串流時瀏覽器停在 CONNECTING，於是只追加一句 `streamInterrupted` 然後繼續等。後端 RQ job 上限 120 秒（`apps/api/app/search/router.py:117` `job_timeout=120`），但 SSE generator 會空轉 30 × 15 秒 = 7.5 分鐘才返回（`:172-187`），瀏覽器接著自動重連——無限循環。卡在 40% 的搜尋沒有取消鈕，只能按瀏覽器上一頁。

附帶：`:769`、`:777`、`:786` 三處 `await loadFinal(id).catch(() => undefined)`，`/searches/{id}` 失敗時結果就是永遠不出現，畫面上沒有任何錯誤。

## Definition of done

- [ ] 零結果時出現明確的說明與下一步，而不是空白。
- [ ] 失敗時畫面上有一顆可重跑同一組條件的按鈕。
- [ ] 搜尋有整體逾時上限，而且從按下去到結束的任何時刻都能取消。
- [ ] 取消或逾時時，保留的次數會被釋放（目前線上每個操作扣 0 次，但不能靠這個當保險）。
- [ ] `loadFinal` 失敗會顯示錯誤，不再靜默。

## Steps

- [ ] 把 `:1487-1489` 的掛載條件與「有沒有結果」拆開：區塊永遠掛載，內部依據有無結果渲染結果或零結果狀態。
- [ ] 零結果文案要說得出可能原因（日期區間太窄、該航線目前無供應商、篩選條件過嚴）並提供「放寬條件」動作，五語系都要有。
- [ ] 失敗狀態獨立渲染重試鈕；不要靠清 `searchId` 讓舊按鈕回來，那會連帶清掉已收到的部分結果。
- [ ] 加 `AbortController` 與整體逾時（建議 150 秒，略大於後端 120 秒 job 上限），逾時後轉為「失敗＋重試」狀態。
- [ ] 取消鈕：關閉 SSE、abort 進行中的 fetch、呼叫後端釋放保留次數。
- [ ] `apps/api/app/search/router.py:172-187` 的 SSE generator 在送出終局事件後立即結束，不要再空轉到 7.5 分鐘。
- [ ] 三處 `.catch(() => undefined)` 改為設定錯誤狀態。

## How to verify

```bash
cd apps/web && npm run test:web -- search-experience
cd apps/api && uv run pytest tests -k search -q
```

手動：用一個必定沒有結果的條件（極窄日期＋冷門航線）跑一次搜尋，應看到零結果說明。搜尋進行中按取消，應立即回到可編輯條件的狀態。

## Notes

- `:800-805` 已經有先例：次數不足時刻意留在原頁而不跳轉，註解寫著 *"/pricing cannot sell anything yet"*。三個死路都可以沿用那個「留在原頁、給出下一步」的處理方式。
- 線上實測（2026-09-11）：`GET /usage-catalog` 回傳的 `operation_costs` 全部是 0，所以目前失敗不會真的損失次數。但這是設定值，不是程式保證——不要把它當成不用做釋放邏輯的理由。
