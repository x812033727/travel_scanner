---
id: 2026-09-20-chiang-mai-old-city-chedi-luang
title: chiang-mai-old-city-slow-day：「柴迪隆寺」改成目錄寫法「契迪龍寺」
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-content-names
claimed_at: 2026-10-02T18:52:36Z
created_at: 2026-09-20T03:13:23Z
completed_at:
branch: claude/chiang-mai-chedi-luang-name
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

- [x] 三處改成「契迪龍寺」（`description`、`blocks[2]`、`sources[1]` 標題）；`blocks[2]` 的其他文字不動。
- [x] 若該內容包有 `aliases` 欄位，收進「柴迪隆寺」。（沒有這個欄位，見 Notes。）
- [x] `grep -c "柴迪隆" apps/api/app/guides/content/chiang-mai-old-city-slow-day.json` 是 0；圖不用改（`apps/web/public/guides/chiang-mai-old-city-slow-day/diagram-1.svg` 2026-09-20 確認沒有這個詞）。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug chiang-mai-old-city-slow-day` 是 `update` 再 `--publish`。（lint 與測試已綠；匯入留給部署後，見 Notes。）

## Steps

- [x] 改三處、確認 grep 0 命中。
- [ ] lint、pytest、PR；部署後匯入。（lint、pytest、PR 已做；匯入未做。）

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
- 2026-10-03（claude-opus-5-5-content-names）：只有 zh-TW 一個語系。動手前再數一次，「柴迪隆寺」正好 3 處，就是 `description`、`blocks[2]`、`sources[1]` 的 `title`，三處都只換這四個字，其他文字（含 `blocks[2]` 其餘句子與 `sources[1]` 的網址、`checked_on`）沒動。
  依據再核一次：`apps/api/app/hotspots/bootstrap.json` 第 346 行仍是 `"name": "契迪龍寺"`。
  repo 的 `apps/` 下 grep「柴迪隆」改完是 0（含 `apps/web/public/guides/` 的圖），所以圖不必動。
- `aliases`：這個內容包沒有 `aliases` 欄位（只有 `slug`、`kind`、`destination_id`、`topics`、`featured`、`display_order`、`locales`），所以沒有可收的地方，也沒有為此新增欄位。
- 檢查：`pack_cli lint --slug chiang-mai-old-city-slow-day` 0 error（唯一一則 warning `no_summary` 是原本就有的）；`pack_cli lint --kind howto` 152 篇 0 error；`pytest tests/test_guides_content_pack.py -q` 9 passed、5 skipped（那 5 個要 PostgreSQL 整合服務，本機不跑，CI 跑）。
- 沒做：正式站匯入。這個 PR 只改 repo；合併並部署後，在主機上經站主同意，照 How to verify 跑 `guides-import --slug chiang-mai-old-city-slow-day --dry-run`（應該只有 zh-TW 是 `update`）再 `--publish`。照同批票 `2026-09-20-chiang-rai-wat-phra-kaew-hours` 的做法，票隨 PR 移到 done，匯入那一格留空；匯入前用不帶 slug 的 dry-run 也看得到這篇在積壓裡。
