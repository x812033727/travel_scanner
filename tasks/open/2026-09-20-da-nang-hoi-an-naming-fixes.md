---
id: 2026-09-20-da-nang-hoi-an-naming-fixes
title: da-nang-hoi-an-4-day-itinerary：「會安古鎮」改目錄的「會安古城」、「峴港觀光局」改成該站署名
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:12:49Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
  - apps/web/public/guides/da-nang-hoi-an-4-day-itinerary
---

# da-nang-hoi-an-4-day-itinerary：「會安古鎮」改目錄的「會安古城」、「峴港觀光局」改成該站署名

## Why

`da-nang-hoi-an-4-day-itinerary` 有兩個名稱和站上目錄、和來源機構的自稱不一致（2026-09-20 逐處數過，全篇 31 個區塊）。

**1. 「會安古鎮」6 處**：`title`、`description`、`blocks[2]`、`blocks[3]`（table）、`blocks[4]`（image 的 `description`）、`blocks[18]`（image 的 `alt`），
外加 `apps/web/public/guides/da-nang-hoi-an-4-day-itinerary/diagram-1.svg` 1 處（「再往南是 Day 3 的會安古鎮，門票 120,000 越南盾」）。
目錄寫的是「**會安古城**」：`apps/api/app/hotspots/areas.py` 第 1020 行 `_area("hoi-an", "會安古城", "Hoi An Ancient Town", …)`、
`apps/api/app/destinations/catalog.py` 第 419／423／424 行（`da-nang` 的 areas 與推薦）、`apps/api/app/hotspots/bootstrap.json` 第 687 行。
第八批第 17 篇 `my-son-sanctuary-day-trip-from-da-nang` 一律寫「會安古城」。

**2. 「峴港觀光局」6 處**：`description`、`blocks[0]`、`blocks[3]`（caption）、`blocks[7]`、`blocks[13]`、`blocks[22]`。
它指的是 `danangfantasticity.com`，但那個站自己的署名是 `DANANG TOURISM PROMOTION CENTER`
（峴港市人民委員會觀光廳所有，授權號 705/GP-STTTT），中文是「**峴港市觀光推廣中心**」，不是觀光局。#17 照該站署名寫，兩篇的機構名稱要一致。

## Definition of done

- [ ] 「會安古鎮」7 處（含 SVG）全部改成「會安古城」；`title`／`description` 改完確認列表頁與搜尋摘要通順。
- [ ] 「峴港觀光局」6 處改成「峴港市觀光推廣中心」（第一次出現可加原文 Danang Tourism Promotion Center）。
- [ ] 票價、時間、距離一個都沒動：古鎮門票 120,000、五行山 40,000／電梯 15,000／來回 30,000、陰府洞 20,000、美山 150,000、06:00–17:00、45／68 公里、巴拿山纜車 1,000,000。
- [ ] 若該內容包有 `aliases` 欄位，收進「會安古鎮」。
- [ ] lint 與內容包測試綠（圖上的字改了要確認 `diagram_number_not_in_text` 沒有變紅）；部署後 `guides-import --slug da-nang-hoi-an-4-day-itinerary` 是 `update` 再 `--publish`。

## Steps

- [ ] 內容包的 6 處「會安古鎮」＋6 處「峴港觀光局」。
- [ ] `diagram-1.svg` 的 1 處「會安古鎮」。
- [ ] `grep -c "會安古鎮\|峴港觀光局"` 在內容包與 SVG 都是 0。
- [ ] lint、pytest、PR；部署後匯入。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug da-nang-hoi-an-4-day-itinerary --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug da-nang-hoi-an-4-day-itinerary --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-vietnam.md` C3 第 3、4 條，彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節。
- **審查記錄的區塊編號不準**：它寫「title 與 `blocks[0]`／`[3]`／`[17]`／`[18]`／`[20]`／`[22]`」，2026-09-20 實際數過「會安古鎮」在 `title`、`description`、`blocks[2]`、`[3]`、`[4]`、`[18]`；`blocks[0]`、`[17]`、`[20]`、`[22]` 沒有這三個字（`blocks[0]`、`[7]`、`[13]`、`[22]` 有的是「峴港觀光局」）。照這張票寫的位置做，動手前再數一次。
- **不要動的**：美山「06:00 開放、17:00 關閉」不是錯（管理處官網就是這一組，另兩個官方頁寫 18:00，三頁哪天統一了再改，那是 FOLLOWUPS 第 1 節第 97 列）；「週一、三、五的 09:00 與 14:45 有占族民歌表演」與「離會安 45 公里、離峴港 68 公里」都已核對正確；`blocks[30]` 的 `foods?city=da-nang` 不是錯。
- scope 與「既有文章補連第八批」重疊：那張票要把 `blocks[22]` 的第一個 `text` 拆成兩段、中間插一個連 #17 的 `article` inline。兩張票不能同時 claim；同一個 PR 一起做也可以。
