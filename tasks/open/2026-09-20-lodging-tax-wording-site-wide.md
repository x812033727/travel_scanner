---
id: 2026-09-20-lodging-tax-wording-site-wide
title: 全站「住宿稅」用詞統一：五篇日本文章的「宿泊稅」與日文字形「宿泊税」
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:12:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/tokyo-where-to-stay.json
  - apps/api/app/guides/content/kanazawa-2-day-itinerary.json
  - apps/api/app/guides/content/japan-onsen-ryokan-guide.json
  - apps/api/app/guides/content/osaka-kyoto-where-to-stay.json
  - apps/api/app/guides/content/kyoto-bus-subway-guide.json
---

# 全站「住宿稅」用詞統一：五篇日本文章的「宿泊稅」與日文字形「宿泊税」

## Why

同一個稅在站上有三種寫法，讀者用「住宿稅」在站內搜尋找不到其中三篇。沖繩縣府自己的繁體中文宣傳單用的是「**住宿稅**」
（縣稅務課頁 https://www.pref.okinawa.lg.jp/kurashikankyo/zeikin/1003660/1036559/1036550.html ），第八批三篇沖繩新文也一律寫「住宿稅」。
2026-09-20 逐處數過的現況：

- `tokyo-where-to-stay`：「宿泊稅」6 處（`title`、`description`、`blocks[1]`、`blocks[27]`、`blocks[28]`、`blocks[29]`），另有 `sources[5]`、`sources[6]` 的日文字形「宿泊税」。
- `kanazawa-2-day-itinerary`：「宿泊稅」4 處（`description`、`blocks[44]`、`blocks[59]`、`sources[19]`）。
- `japan-onsen-ryokan-guide`：「宿泊稅」7 處（`description`、`blocks[0]`、`blocks[2]`×2、`blocks[3]`×2、`blocks[24]`），`sources[7]` 是「宿泊税」。
- `osaka-kyoto-where-to-stay`：「住宿稅」2 處（`description`、`blocks[23]`），但 `blocks[23]` 同一塊裡又有日文字形「宿泊税」2 處，`sources[12]`–`[14]` 也是。
- `kyoto-bus-subway-guide`：「住宿稅」2 處（`description`、`blocks[22]`），`blocks[22]` 另有「宿泊税」1 處、`sources[18]` 1 處。

## Definition of done

- [ ] 五篇**正文、`title` 與 `description`** 的「宿泊稅」全部改成「住宿稅」；改到標題的要確認列表頁讀起來仍通順。
- [ ] 日文字形「宿泊税」只留在**引用日文官方頁名稱的 `sources` 標題與直接引文**裡，正文不留。
- [ ] 五篇若有 `aliases` 欄位，收進「宿泊稅」，舊搜尋詞不失效。
- [ ] 數字一個都沒動：東京 100／200（2027 年 4 月起 3%）、大阪 200／400／500、京都五級、金澤 200／500、入湯稅 150／300。
- [ ] lint（`--kind howto`）與內容包測試綠；部署後五個 slug 一起 dry-run 再 `--publish`。

## Steps

- [ ] 五篇逐篇改（位置見上面的清單），每篇改完 `grep -c "宿泊稅" <file>` 是 0。
- [ ] 確認 `sources` 的日文頁名沒有被改成繁體（那是官方頁名稱）。
- [ ] lint、pytest、PR；部署後一次匯入五篇。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug tokyo-where-to-stay --slug kanazawa-2-day-itinerary --slug japan-onsen-ryokan-guide --slug osaka-kyoto-where-to-stay --slug kyoto-bus-subway-guide --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug tokyo-where-to-stay --slug kanazawa-2-day-itinerary --slug japan-onsen-ryokan-guide --slug osaka-kyoto-where-to-stay --slug kyoto-bus-subway-guide --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-okinawa.md` C3 第 6 條與第八批第 1 篇 `okinawa-lodging-tax-2027` 規格的「上線後與交叉檢查」，彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節。規格**明寫不要跟著第八批的上線 PR 走**，一次改完五篇。
- 第八批 #1 一個外縣市的數字都不寫，所以這張票和它沒有共用的事實，先後順序無所謂。
- `apps/web/public/guides/*/diagram-1.svg` 全掃過，**沒有任何一張圖**含這三種寫法，所以 scope 不含圖目錄。
- `japan-hotel-room-plan-guide` 寫「本文不提供固定住宿稅或兒童年齡門檻」，與這張票無關、不要改。
- `kanazawa-2-day-itinerary` 另有 `2026-09-20-shirakawago-bus-times-and-reservation-rule`（`blocks[55]`）也在同一個檔上，兩張票不能同時 claim。
