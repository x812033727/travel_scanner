---
id: 2026-09-20-chiang-mai-old-city-chedi-luang
title: chiang-mai-old-city-slow-day：「柴迪隆寺」改成目錄寫法「契迪龍寺」
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:13:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/chiang-mai-old-city-slow-day.json
---

# chiang-mai-old-city-slow-day：「柴迪隆寺」改成目錄寫法「契迪龍寺」

## Why

`chiang-mai-old-city-slow-day` 把 Wat Chedi Luang 寫成「柴迪隆寺」，站上其他地方寫的是「契迪龍寺」。
2026-09-20 數過的 3 處：`description`（「從帕辛寺或柴迪隆寺擇一開始」）、`blocks[2]`（「帕辛寺和柴迪隆寺都是研究古城行程時可先認識的地點」）、
`sources[1]` 的標題（「泰國觀光局：清邁古城與帕辛寺、柴迪隆寺」）。
依據：熱點目錄 `apps/api/app/hotspots/bootstrap.json` 第 346／349 行 `"name": "契迪龍寺"`／`"en": "Wat Chedi Luang"`，
既有 `chiang-mai-3-day-itinerary` 的正文與 `blocks[7]`（image 的 `description`）也都寫「契迪龍寺」。
協調者 2026-09-20 裁決：全站一律「契迪龍寺」，「柴迪隆寺」不再使用。同一座寺兩種譯名，讀者搜尋與內部連結都對不起來。

## Definition of done

- [ ] 三處改成「契迪龍寺」（`description`、`blocks[2]`、`sources[1]` 標題）；`blocks[2]` 的其他文字不動。
- [ ] 若該內容包有 `aliases` 欄位，收進「柴迪隆寺」。
- [ ] `grep -c "柴迪隆" apps/api/app/guides/content/chiang-mai-old-city-slow-day.json` 是 0；圖不用改（`apps/web/public/guides/chiang-mai-old-city-slow-day/diagram-1.svg` 2026-09-20 確認沒有這個詞）。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug chiang-mai-old-city-slow-day` 是 `update` 再 `--publish`。

## Steps

- [ ] 改三處、確認 grep 0 命中。
- [ ] lint、pytest、PR；部署後匯入。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug chiang-mai-old-city-slow-day --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug chiang-mai-old-city-slow-day --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-thailand-a.md` 第 0.4 節與 C3 第 7 列，彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節。這是協調者裁決的譯名之一（同一批還有「漢拏山」「會安古城」「格蘭島」「契迪龍寺」）。
- 第八批第 11 篇 `chiang-mai-night-markets-walking-streets` 一律寫「契迪龍寺」，不會再產生新的「柴迪隆寺」。
- scope 與「既有文章補連第八批」重疊：那張票要改同一篇的 `blocks[8]`（連 #10）、`blocks[10]`（連 #11，可選）、`blocks[16]`（連 #14）。兩張票不能同時 claim；順手在同一個 PR 做也可以。
