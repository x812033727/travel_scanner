---
id: 2026-09-20-nozomi-all-reserved-wording
title: のぞみ「全席指定席」統一：五個內容包與一張圖把「全車指定席」改成官方原文
status: done
priority: P3
area: docs
owner: claude-opus-5-5-content-names
claimed_at: 2026-10-02T19:07:23Z
created_at: 2026-09-20T03:12:48Z
completed_at: 2026-10-02T19:13:41Z
branch: claude/nozomi-all-reserved-wording
depends_on: []
scope:
  - apps/api/app/guides/content/japan-golden-week-2027.json
  - apps/api/app/guides/content/japan-shinkansen-ticket-guide.json
  - apps/web/public/guides/japan-shinkansen-ticket-guide
  - apps/api/app/guides/content/japan-cherry-blossom-2027.json
  - apps/api/app/guides/content/taiwan-long-weekends-2027-flight-planning.json
  - apps/api/app/guides/content/takayama-shirakawago-day-trip.json
---

# のぞみ「全席指定席」統一：五個內容包與一張圖把「全車指定席」改成官方原文

## Why

のぞみ 在旺季不設自由席，官方原文一律寫「**全席指定席**」：JR 東海・JR 西日本 2026-05-21 新聞稿
https://jr-central.co.jp/news/release/_pdf/000045592.pdf （2026-09-20 讀到「『全席指定席（自由席設定なし）』として運行」），
スマートEX トピックス id=851 同樣用字。站上寫法不一致，`japan-golden-week-2027` 同一篇裡就自相矛盾（標題「全車」、內文「全席」）。
2026-09-20 掃過全部內容包，**指のぞみ的「全車指定席」在五個檔與一張圖裡**：

- `japan-golden-week-2027`：`title`「…のぞみ全車指定席與台灣勞動節撞期」與 `blocks[8]`（heading）「新幹線：黃金週是のぞみ全車指定席的三大尖峰期之一」；同篇 `blocks[9]`、圖說與 sources 已經寫「全席指定席」。
- `japan-shinkansen-ticket-guide`：`blocks[6]`（callout 標題「旺季 のぞみ 全車指定席，JR 東日本 3 月起運賃調漲」與內文「2026 年度 のぞみ 全車指定席（不設自由席）的期間」）、`blocks[24]`（image 的 `description`）、`blocks[28]`（list 最後一項）、`sources[10]` 的標題，以及 `apps/web/public/guides/japan-shinkansen-ticket-guide/diagram-1.svg` 的 2 處。
- `japan-cherry-blossom-2027` `blocks[18]`：正文「のぞみ為什麼全車指定席」＋連結文字（引用黃金週篇的 title）。
- `taiwan-long-weekends-2027-flight-planning` `blocks[10]`：連結文字（引用黃金週篇的 title；同篇正文寫的是「全席指定席」）。
- `takayama-shirakawago-day-trip` `blocks[29]`：連結文字「日本新幹線車票攻略：…旺季 のぞみ 全車指定席」。

`japan-year-end-new-year-2026-2027` 全篇已是「全席指定席」，第八批第 2 篇 `japan-public-holidays-2027` 也明訂照官方原文寫，所以剩下的就是這幾處。

**不要改的**：`japan-shinkansen-ticket-guide` `blocks[4]` 與 `sources[17]` 的「はやぶさ、かがやき（こまち、つばさ）全車指定席」是指**車種**（整列車都是指定席），
那是正確用法；`fuji-kawaguchiko-day-trip` 與 `nikko-day-trip-from-tokyo` 圖上的「全車指定席」也是車種用法。兩義混用才是這張票要收掉的問題。

## Definition of done

- [x] 五個內容包裡**指のぞみ旺季**的「全車指定席」全部改成「全席指定席」：黃金週篇 `title`＋`blocks[8]`；新幹線篇 `blocks[6]`（標題與內文各一）、`blocks[24]`、`blocks[28]`、`sources[10]`；櫻花篇 `blocks[18]` 正文；三處引用黃金週篇 title 的連結文字（櫻花篇 `blocks[18]`、台灣連假篇 `blocks[10]`、高山白川鄉篇 `blocks[29]` 那一處是引用新幹線篇的自訂連結文字）。
- [x] `apps/web/public/guides/japan-shinkansen-ticket-guide/diagram-1.svg` 的 2 處「のぞみ 全車指定席」跟著改，同一張圖的「かがやき 全車指定席」**不動**。
- [x] 改完 `grep -c "のぞみ.\{0,2\}全車指定席"` 在五個檔與那張 SVG 都是 0；`grep "かがやき 全車指定席"` 仍然命中。
- [x] 黃金週篇改了 `title` 之後，`description` 與三處引用它 title 的連結文字與新 title 一致（連結文字可以縮短，但不能還留「全車」）。
- [ ] lint（`--kind howto` 與 `--kind intel`）與內容包測試綠；部署後五個 slug 一起 dry-run 再 `--publish`。（lint 與測試已綠；匯入留給部署後，見 Notes。）

## Steps

- [x] `japan-golden-week-2027`：`title`、`blocks[8]`。
- [x] `japan-shinkansen-ticket-guide`：`blocks[6]`、`blocks[24]`、`blocks[28]`、`sources[10]`、`diagram-1.svg`（2 處）。
- [x] `japan-cherry-blossom-2027` `blocks[18]`（正文一處＋連結文字）。
- [x] `taiwan-long-weekends-2027-flight-planning` `blocks[10]`（連結文字）。
- [x] `takayama-shirakawago-day-trip` `blocks[29]`（連結文字）。
- [x] 全站再 grep 一次確認沒有漏；車種用法一處都沒改到。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run python -m app.guides.pack_cli lint --kind intel
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug japan-golden-week-2027 --slug japan-shinkansen-ticket-guide --slug japan-cherry-blossom-2027 --slug taiwan-long-weekends-2027-flight-planning --slug takayama-shirakawago-day-trip --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug japan-golden-week-2027 --slug japan-shinkansen-ticket-guide --slug japan-cherry-blossom-2027 --slug taiwan-long-weekends-2027-flight-planning --slug takayama-shirakawago-day-trip --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-japan.md` B-2 裁決與 C3 第 8、9 條（協調者 2026-09-20 同意開一張低優先票），彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節。
- **審查記錄寫「既有三篇」**，彙整時打開內容包發現實際是**五個檔＋一張 SVG**：多出來的是兩篇的連結文字（它們引用黃金週篇的 title）與 `takayama-shirakawago-day-trip`。
- 這是用字口徑、不是事實錯誤，所以 P3；但站上「全車指定席」另有車種用法，兩義混用比不統一更糟，這是裁決要開票的理由。
- 時效：`japan-golden-week-2027` 與 `japan-cherry-blossom-2027` 都在 2027-05-10 到期。這張票若拖到 2027-05-11 之後，那兩篇的部分就不必做（改由日期票 `japan-holidays-2027-link-expiries` 處理）。
- 改 `title` 會動到列表頁與搜尋摘要，`guides-import` 之後要看一次正式站的 `/zh-TW/guides/intel` 列表。
- `takayama-shirakawago-day-trip` 另有 `2026-09-20-shirakawago-bus-times-and-reservation-rule`（`blocks[23]`／`blocks[4]`／`blocks[7]` 與圖）也在同一個檔上，兩張票不能同時 claim。
- 2026-10-03（claude-opus-5-5-content-names）：官方用字動手前再讀一次。JR 東海・JR 西日本 2026-05-21 新聞稿 PDF（HTTP 200）標題是「…「のぞみ」号を全席指定席として運行する期間の追加について」，內文「『全席指定席（自由席設定なし）』として運行」；スマートEX トピックス `https://smart-ex.jp/topics/detail/?id=851`（HTTP 200）標題「東海道・山陽新幹線「のぞみ」全席指定席対象期間について」，內文「「のぞみ」を「全席指定席」で運行」。兩頁都沒有「全車指定席」。`sources[10]` 引的 JR 東海英文時刻表頁 `https://global.jr-central.co.jp/en/info/timetable/` 寫的是 All seats on Nozomi trains … are reserved seats during the major peak periods，沒有日文原文，所以來源標題裡的日文是我們的寫法，照官方日文改成「全席指定席」不會扭曲那一頁。
- 五個內容包都只有 zh-TW。改法：每個檔先數到預期的片語次數才寫（「のぞみ全車指定席」「のぞみ 全車指定席」「のぞみ為什麼全車指定席」），改完逐字比對前後只差「車→席」一個字、所有數字不變。共 13 處：黃金週 2、新幹線內容包 5、新幹線圖 2、櫻花 2、台灣連假 1、高山白川鄉 1，和這張票列的位置一致。
- 圖：新幹線圖的 2 處一處是 `<desc>`（和 `blocks[24]` 的 `description` 同一段），一處是畫面上「旺季與價格」框裡的「年末年始、黃金週、盂蘭盆節：のぞみ 全席指定席，先劃位」。repo 裡沒有這張圖的產生腳本，只換一個等寬的漢字，用 Chrome 渲染成 PNG 看過，沒有疊字或超框；頁尾「はやぶさ、かがやき 全車指定席」沒動。
- 全站掃過所有內容包與 `apps/web/public/guides/*/*.svg`：「のぞみ」後 4 個字以內接「全車指定席」的剩 0 處。留下的「全車指定席」都是車種用法：新幹線篇 `blocks[4]` 與 `sources[17]`、新幹線圖頁尾，以及富士回遊、Romancecar、HARUKA、Rapi:t、μ-SKY、SPACIA X、かがやき、はやぶさ、ゆふいんの森、旭川方向特急等其他十幾篇，一處都沒動。
- 黃金週篇新 title 是「…日本人怎麼連休、のぞみ全席指定席與台灣勞動節撞期」，`description` 原本就寫「全席指定席」；櫻花篇與台灣連假篇的連結文字是新 title 的縮短版（少「日本人怎麼連休、」），本來就這樣，只換了「車→席」。黃金週篇有 `aliases`（黃金周、ゴールデンウィーク），和這張票無關，沒動。
- 檢查：五個 slug 的 `pack_cli lint --slug …` 0 error（新幹線篇與高山白川鄉篇各一則原本就有的 `no_summary` warning）；`pack_cli lint --kind howto` 152 篇 0 error；`--kind intel` 22 篇 0 error；`pytest tests/test_guides_content_pack.py -q` 9 passed、5 skipped（PostgreSQL 整合測試，本機不跑，CI 跑）。
- 沒做：正式站匯入。這個 PR 只改 repo；合併並部署後，在主機上經站主同意，照 How to verify 把五個 slug 一起 dry-run（應該只有這五篇的 zh-TW 是 `update`）再 `--publish`，然後看一次 `/zh-TW/guides/intel` 列表（黃金週篇的 title 改了）。照同批票 `2026-09-20-lodging-tax-wording-site-wide` 的做法，票隨 PR 移到 done，匯入那一格留空；要在 2027-05-10 黃金週篇與櫻花篇到期前匯入才有意義。
