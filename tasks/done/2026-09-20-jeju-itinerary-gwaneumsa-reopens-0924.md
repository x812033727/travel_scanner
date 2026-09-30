---
id: 2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924
title: jeju-3-day-itinerary：漢拏山觀音寺路線 2026-09-24 重開，「觀音寺顯示預約限制」那句要改
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T02:39:30Z
created_at: 2026-09-20T00:24:19Z
completed_at: 2026-09-30T02:45:08Z
branch: claude/jeju-gwaneumsa-hallasan
depends_on: []
scope:
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/web/public/guides/jeju-3-day-itinerary/diagram-1.svg
---

# jeju-3-day-itinerary：漢拏山觀音寺路線 2026-09-24 重開，「觀音寺顯示預約限制」那句要改

## Why

第八批規劃的韓國研究（2026-09-20）讀到漢拏山國立公園公告板 2026-09-18 的公告：觀音寺探訪路「三角峰↔白鹿潭頂」區間
2026-09-24（四）05:00 起重新開放（https://visithalla.jeju.go.kr/board/boardView.do?bbsId=notice&seq=1300）。
既有 `jeju-3-day-itinerary` Day 3 方案 B 寫的是「城板岳正常開放預約、觀音寺顯示預約限制」，9/24 之後這句就錯了。

## Definition of done

- [x] 2026-09-24 之後重讀公告板（`bbsId=notice`）確認已重開，改掉那一句（該文章若有其他語系，同一句一起改）。
- [x] sources 的 `checked_on` 只更新實際重讀的那一條；`check`／lint 通過；`guides-import --slug jeju-3-day-itinerary`（動作是 update）。

第八批審查（2026-09-20）併進來的三件事，**同一個 PR 一起做**（協調者裁決：這個檔只有這一張票，不另開）：

- [x] 全文 **14 處「漢拿山」改成「漢拏山」**（目的地目錄的寫法）：`title`、`description`、`blocks[0]`、`blocks[2]`（5 處）、`blocks[3]`（2 處）、`blocks[14]`、`blocks[18]`、`blocks[19]`、`blocks[28]`；改完 `grep -c 漢拿山` 是 0。
- [x] 「登頂只有城板岳與觀音寺兩條路線，都採線上預約制」補上**只有上半段要預約**：`blocks[19]` 那一句，以及 `blocks[3]`（diagram-1 的 `description`）的「觀音寺 8.7 公里採預約制」。
- [x] 觀音寺過期句**兩處**都改：`blocks[19]`（「2026 年 9 月 13 日查詢時城板岳正常開放預約、觀音寺顯示預約限制」）與 `blocks[28]`（行前檢查 list 的「2026 年 9 月觀音寺顯示預約限制」）。
- [ ] (moved to its own ticket) 第八批第 8、9 篇上線後：`blocks[19]` 改句時在同一個 `rich_paragraph` 裡插一個 `article` inline 連 `hallasan-hiking-reservation-guide`（該塊現在是 `paragraph`，要改型別），`related`（現在是 `null`）補 `hallasan-hiking-reservation-guide` 與 `marado-gapado-ferry-day-trip`。
- [x] `blocks[30]` 的 `foods?city=jeju` **不要改**（協調者 2026-09-20 裁決：`?city=` 不是錯，`apps/web/lib/foods.ts` 兩個參數都讀，兩張相關的票已結案）。

## Steps

- [x] 重讀公告 → 改句 → lint → PR → 匯入
- [x] 同一個 PR 做上面四件事（位置與出處見 Notes）；`blocks[2]` 是 `table`、`blocks[28]` 是 `list`，兩種都放不了 inline，只改字

## How to verify

`cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto --slug jeju-3-day-itinerary`；正式站該頁的那一句已更新。

## Notes

- 第八批候選 `hallasan-hiking-reservation-guide` 會把預約制與各管制所時間寫完整；這張票只修既有文章的過期句。

### 2026-09-20 併進來的四件事（協調者裁決：`jeju-3-day-itinerary` 只有這一張票，不另開）

`docs/travel-guides-batch-8/FOLLOWUPS.md` 第 2、3 節有完整脈絡。區塊編號與次數都是 2026-09-20 打開
`apps/api/app/guides/content/jeju-3-day-itinerary.json` 的 zh-TW 實際數過的（全篇 31 個區塊）。

1. **「漢拿山」14 處 → 「漢拏山」**。目錄的寫法：`apps/api/app/hotspots/areas.py` 第 742 行「漢拏山／思連伊林蔭路」、
   `apps/api/app/destinations/catalog.py` 第 232 行「漢拏山周邊步道」。位置：`title`、`description`、`blocks[0]`、
   `blocks[2]`（table，5 處）、`blocks[3]`（image 的 `description`，2 處）、`blocks[14]`、`blocks[18]`、`blocks[19]`、`blocks[28]`（list）。
   `aliases` 可以收「漢拿山」，舊搜尋詞不失效。第八批第 8、9 篇一律寫「漢拏山」，**不照抄這篇的舊寫法**。
2. **觀音寺過期句兩處**：`blocks[19]`（Day 3 方案 B）與 `blocks[28]`（行前檢查的 list 第 4 項）。
   出處：漢拏山國立公園公告 `https://visithalla.jeju.go.kr/board/boardView.do?bbsId=notice&seq=1300`（2026-09-18 發布，
   2026-09-20 重讀 200）：觀音寺探訪路「三角峰↔白鹿潭頂」自 2026-09-24（四）05:00 起重新開放、預約自 09-21 09:00 起恢復。
   寫法用「自……起」這種過了 2026 年還讀得通的說法，不要寫「即將」「近期」「這個月才剛重開」。
3. **「都採線上預約制」漏了只有上半段**：依公告 `seq=1284`（2025-04-23），預約只管**金達萊田↔白鹿潭**與
   **三角峰↔白鹿潭**兩個上半段區間；下半段與御里牧、靈室、頓乃克、石窟庵、御乘生不用預約。
   要改的是 `blocks[19]` 那一句，以及 `blocks[3]` 圖說的「城板岳 9.6 公里、觀音寺 8.7 公里採預約制」
   （**這一處審查記錄沒列到**，彙整時打開內容包才發現）。`blocks[2]` 表格 Day 3 寫的是「漢拿山城板岳採預約制」，
   只講城板岳、語意沒錯，改字時只換譯名。
4. **反向連結與 `related`**：第八批第 8 篇 `hallasan-hiking-reservation-guide`、第 9 篇 `marado-gapado-ferry-day-trip`
   上線後才做（inline 指向的 slug 要先存在，否則 `guides-links-check` 會紅）。`blocks[19]` 目前是 `paragraph`、放不了 inline，
   改句時整塊改成 `rich_paragraph`、原文其他文字一字不改。
   `jeju-car-rental-guide` 的 `related` 走「既有文章補連第八批」那張票，**不在這張票裡**。

- `blocks[30]` 的 `foods?city=jeju` 不是錯、不要改（`apps/web/lib/foods.ts` 第 176–179 行 `destination_id` 與 `city` 兩個參數都讀，canonical 先讀）。
- 這個檔同時是第八批「既有文章補連第八批」票刻意避開的檔案：那張票的 scope 不含 `jeju-3-day-itinerary.json`，所以不會和這張票搶。
- 2026-09-30 (claude-opus-5-5): notice seq=1300 (2026-09-18) re-read: 삼각봉↔백록담
  정상 reopened from 2026-09-24 05:00, bookings from 09-21 09:00; it is still the
  newest notice (no later one). seq=1284 re-read: only 진달래밭↔백록담 and
  삼각봉↔백록담 need booking; 어리목, 영실, 돈내코, 석굴암, 어승생 do not.
- Done: 14 漢拿山 → 漢拏山 in the pack, plus the 4 in `diagram-1.svg`, which the
  ticket did not list (scope widened to that file; the rendered diagram shows 拏
  correctly). blocks[19], blocks[3] description and blocks[28] now say only the
  upper sections need booking and that the Gwaneumsa section reopened "自 2026 年
  9 月 24 日起". Both notices added to sources (2026-09-30); the booking-system
  entry is left at 2026-09-13 because its page was not re-read.
- Not done: `aliases` for 漢拿山 (optional; importing new aliases would replace
  any an editor added in the admin), and the batch 8 #8/#9 link and `related`
  item, because `hallasan-hiking-reservation-guide` and
  `marado-gapado-ferry-day-trip` do not exist yet. That item stays unticked for
  whoever publishes them.
- Checks: `grep -c 漢拿山` 0 in pack and diagram; lint 0 errors; content pack
  tests green. Left unticked: production import after merge and deploy.

- The batch 8 link item moved to `2026-09-30-link-jeju-3-day-itinerary-to`.
