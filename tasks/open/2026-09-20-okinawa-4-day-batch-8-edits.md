---
id: 2026-09-20-okinawa-4-day-batch-8-edits
title: okinawa-4-day-itinerary：高速巴士「約 3 小時」是英文頁的數字，要改成 2 小時 30 分（同票做第八批兩個反向連結）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:12:34Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/okinawa-4-day-itinerary.json
---

# okinawa-4-day-itinerary：高速巴士「約 3 小時」是英文頁的數字，要改成 2 小時 30 分（同票做第八批兩個反向連結）

## Why

`okinawa-4-day-itinerary` 的 `blocks[15]`（paragraph）現在寫「官網寫從那霸機場走沖繩自動車道約 2 小時，**搭高速巴士約 3 小時**」。
水族館日文 access 頁 https://churaumi.okinawa/guide/access/ 2026-09-20 讀到的是「那覇空港から、車で約2時間（高速道路利用）、バス（高速バス使用）で約2時間30分です。」
——「3 小時」是同一頁**英文版**的 approximately three hours。站上 `okinawa-car-rental-guide` `blocks[23]` 已經寫「官網寫約 2 小時 30 分」，
讀者現在在同一個站上會看到同一段路兩個數字。

第八批第 1 篇 `okinawa-lodging-tax-2027` 與第 7 篇 `okinawa-without-a-car` 又都要在這一篇加反向連結，其中一個是**新增區塊**，
會讓後面所有 `blocks[n]` 位移。三件事分三張票做一定會互相覆蓋，所以協調者 2026-09-20 裁決：這一篇的所有編輯集中在這一張票
（做法與順序照審查記錄 `plan8/review/review-okinawa.md` 的 C4）。zh-TW 現在共 **26 個區塊**（2026-09-20 實際數過）。

## Definition of done

- [ ] `blocks[15]` 的「搭高速巴士約 3 小時」改成「搭高速巴士約 2 小時 30 分」，同一段其他數字一個都沒動。
- [ ] `blocks[6]` 原地改成 `rich_paragraph`（**不新增區塊**），原文拆成 `text` inline、文字與數字一字不改，結尾加一句並插一個 `article` inline 連 `okinawa-without-a-car`（`kind: howto`）。
- [ ] `blocks[4]`（callout「第一天不要租車」）之後**新增**一個 `rich_paragraph`：一句「2027 年 2 月 1 日起住宿要另付住宿稅，算總預算時要加進去」＋`article` inline 連 `okinawa-lodging-tax-2027`（`kind: intel`）；那一句**拿掉連結後仍讀得通**（不得出現「見下方」「另一篇」）。
- [ ] 插入後全篇 27 個區塊，`blocks[2]`（table）、`blocks[22]`（list）、`blocks[23]`（callout）都沒被動到（三種都放不了 inline）。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug okinawa-4-day-itinerary` 的計畫是 `update`，再 `--publish`。

## Steps

依這個順序做（**從後往前，最後才插入新區塊**）：

- [ ] 1. `blocks[15]`：「搭高速巴士約 3 小時」→「搭高速巴士約 2 小時 30 分」。出處 https://churaumi.okinawa/guide/access/ 「バス（高速バス使用）で約2時間30分」；`sources` 的 `checked_on` 只更新這一條。
- [ ] 2. `blocks[6]`（paragraph → `rich_paragraph`，原地改型別不會位移）：原文拆 `text`，結尾加一句連 `okinawa-without-a-car`，連結文字講「不開車的沖繩能玩到哪裡、末班車幾點」。
- [ ] 3. 最後做：`blocks[4]` 之後新增 `rich_paragraph` 連 `okinawa-lodging-tax-2027`。插入後 `blocks[5]` 起全部往後移一格（原 `[6]`→`[7]`、原 `[15]`→`[16]`、原 `[25]`→`[26]`）。若不照這個順序，就要先算好插入後的新編號再動手。
- [ ] 4. 自檢：兩個新 inline 的 slug 與 kind 都存在、沒有兩個 `article` inline 相鄰、`blocks[16]`（photo-1）與 hero 沒被動。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

改完 `grep -c "3 小時" apps/api/app/guides/content/okinawa-4-day-itinerary.json` 應該不再命中水族館那一段。
部署後：`uv run python -m app.cli guides-import --slug okinawa-4-day-itinerary --dry-run` 只有 zh-TW `update`，確認後 `--publish`，再 `guides-links-check --locale zh-TW`。

## Notes

- 來源：第八批審查記錄 `review-okinawa.md` C3 第 1 條與 C4，彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 2、3 節；由第 1 篇與第 7 篇的規格審查帶出。
- **`blocks[25]` 的 `foods?city=okinawa` 不要改**：協調者 2026-09-20 裁決 `?city=` 不是錯（`apps/web/lib/foods.ts` 第 176–179 行兩個參數都讀，票 `2026-09-14-food-links-city-param-ignored`、`2026-09-19-foods-page-drops-city-on-server` 已結案）。C4 原本的第 1 步已撤銷。
- 這張票要**和第八批 #1、#7 的內容包同一批進站**，不然 inline 指向的 slug 不存在，`guides-links-check` 會紅。
- `blocks[16]`（photo-1）與 `okinawa-car-rental-guide` `blocks[24]` 是同一張 Commons 照片（`Main_tank_of_the_Kuroshio_Sea_in_Okinawa_Churaumi_Aquarium.JPG`，そらみみ，CC BY-SA 4.0）。**這張票不處理**，它的作用是第八批三篇沖繩文章的避開清單。
- `okinawa-car-rental-guide` 的兩件事不在這張票：`blocks[13]` 誤植見 `2026-09-20-okinawa-car-rental-ai-term-inline`，`blocks[23]` 補連第 7 篇走「既有文章補連第八批」。
- 2028-01-01 要拿掉步驟 3 那個 inline（#1 的 `valid_until` 是 2027-12-31），那是上線 PR 另開的日期票。
