---
id: 2026-09-11-catchtable-underscore-segment-id
title: CatchTable 店家 id 有底線分段時存不了訂位連結
status: done
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-11T19:26:00Z
completed_at: 2026-09-12T06:00:41Z
branch:
depends_on: []
scope:
  - apps/api/app/foods/platform_links.py
  - apps/api/tests/test_food_platform_links.py
  - apps/web/lib/reservation-platforms.ts
  - apps/web/lib/reservation-platforms.test.ts
---

# CatchTable 店家 id 有底線分段時存不了訂位連結

## Why

PR #397 讓 CatchTable 的店家 id 可以含點號（例如 `yosukgung.kr`），規則是每個點分段都要以英數開頭（`_CATCHTABLE_SLUG`，`apps/api/app/foods/platform_links.py:65`）。

但實際資料裡有 id 是 `hani._.noodle`（首爾 하니칼국수），中間那段只有一個底線，所以
`https://www.catchtable.net/shop/hani._.noodle` 被判為不是精準店家頁，存不進訂位平台欄位。
這一頁在 2026-09-12 的查核中，由兩個獨立代理分別確認過就是該店（퇴계로 411-15、02-3298-6909）
且頁面可以訂位，純粹卡在網址規則。

## Definition of done

- [x] `hani._.noodle` 這類 id 能通過前後端驗證，且沒有放寬到會接受搜尋頁、目錄頁或路徑穿越。
- [x] Python 與 TypeScript 兩邊判斷一致，各自有測試。
- [x] 首爾 하니칼국수 的連結存得進去了；狀態改為停用而非公開，理由見備註。

## Steps

- [x] 放寬 `_CATCHTABLE_SLUG`：分段可以用底線開頭，但仍禁止空分段，整體仍要以英數開頭。
- [x] 同步改 `apps/web/lib/reservation-platforms.ts` 的對應規則。
- [x] 補測試：`hani._.noodle` 會過；`a..b`、`.abc`、`abc.`、`_abc`、`shop/search` 仍被拒。

## How to verify

- `cd apps/api && pytest tests/test_food_platform_links.py`
- `cd apps/web && npx vitest run lib/reservation-platforms.test.ts`

## Notes

- 查核證據在 `apps/api/app/foods/data/platform_reviews/2026-09-11-public-merchants.json` 裡
  `seoul-hanikalgugsu` 那筆，狀態是 `ambiguous`，網址放在 `evidence` 的
  `unstorable_candidate` 角色下。改完規則後把它改成 `verified` 再跑一次匯入指令即可。
- 相關任務：`2026-09-11-food-reservation-link-backfill`。

- 2026-09-12：規則已在 `2026-09-12-japan-korea-reservation-platforms` 一併放寬並補測試
  （分段可以用底線開頭，整體仍要以英數開頭；`a..b`、`.abc`、`_abc`、`abc.` 仍被拒）。
- 但這家店最後存成 **停用**，不是公開。原因是本票的 Why 寫「頁面可以訂位」與證據不符：
  同一筆查核紀錄的 `booking_observation` 寫的是 CatchTable 上只有現場候位與優先入場
  （`WAITING_GLOBAL`／`RESERVED_ENTRY_GLOBAL`），不是一般桌位訂位，而且查核當天沒有實際看到
  候位或優先入場畫面。2026-09-11 那輪對 seoul-mokmyeoksanbang 等其他候位型頁面都記成停用，
  這裡照同一把尺。
- 若擁有者認為「優先入場」算可訂位，把 `2026-09-12-japan-platforms.json` 裡 seoul-hanikalgugsu
  那筆改成 `verified` 再跑一次匯入指令即可，網址規則這一關已經過了。
