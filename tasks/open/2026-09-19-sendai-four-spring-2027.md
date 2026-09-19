---
id: 2026-09-19-sendai-four-spring-2027
title: 仙台四篇 2027 年春季改正複查：空港線（03-20 後）、立石寺（03-25 起）、蔵王 GTFS（03-31 前）、るーぷる與地鐵（04-01 前）、jreast 重試
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/sendai-airport-access-loople-bus-guide.json
  - apps/web/public/guides/sendai-airport-access-loople-bus-guide
  - apps/api/app/guides/content/sendai-matsushima-2-day-itinerary.json
  - apps/api/app/guides/content/yamadera-day-trip-from-sendai.json
  - apps/web/public/guides/yamadera-day-trip-from-sendai
  - apps/api/app/guides/content/zao-fox-village-from-sendai.json
  - apps/web/public/guides/zao-fox-village-from-sendai
---

# 仙台四篇 2027 年春季改正複查：空港線（03-20 後）、立石寺（03-25 起）、蔵王 GTFS（03-31 前）、るーぷる與地鐵（04-01 前）、jreast 重試

## Why

仙台四篇（`sendai-airport-access-loople-bus-guide`、`sendai-matsushima-2-day-itinerary`、`yamadera-day-trip-from-sendai`、`zao-fox-village-from-sendai`）共用市內票券的數字（空港線 680／IC 672、るーぷる 260／630／920、地鐵一日券 840／620、仙台まるごとパス 2,930／1,470），規格要求任何一篇改，同一個 PR 改其他篇；JR 東日本、るーぷる、立石寺、蔵王的巴士都在 3 月底到 4 月初換年度。四份規格的「上線後與交叉檢查」各要求上線 PR 開票並寫明日期，山寺篇更寫明「和第 9、10 篇同一天複查」。

## Definition of done

- [ ] 2027-03-20 後：空港線 680／672、首末班（5:31／23:23、5:45／23:10）與白天 20 分班距核對完；有變同時改交通篇 H2-1 表格、H2-2、summary、FAQ 第 1 題與 diagram-1（五處一致）。
- [ ] 2027-03-25 起：立石寺入山料（500／200，令和 7 年 4 月 1 日改定）與參拜時間（4-9 月、12-3 月兩段）核對完，10 月與 11 月的時段若補上就改 H2-3 表格一、H2-4、summary 第四句、FAQ 第 1 題（四處一致）。
- [ ] 2027-03-31 前：takeyakotsu 運賃 1,000／500 與四個班次時刻重抓（現行 GTFS 有效期間到 2027-03-31）；時刻變了重算去程約 34 分、回程約 36 分，改表格二、tip callout、summary 第二句、FAQ 第 3 題與 diagram-1（五個地方）。
- [ ] 2027-04-01 前：るーぷる 260／630／920、地鐵 840／620、8 月 15 分間隔公告，以及仙台まるごとパス 2,930／1,470、連續兩天與フリーエリア 區間（山寺還在不在範圍內）核對完，四篇同一個 PR 對齊。
- [ ] JR 春季改正後：松島篇的仙石線班次與「一小時兩班」核對完，有變改 H2-1、H2-3 與 summary；jreast.co.jp 讀得到就把四篇的 JR 區間「以官網為準」換成實際票價與車程。
- [ ] 每次改動更新 `checked_on`，lint 通過（三張圖上的數字都在正文）。做完這一輪就 done，下一年度另開票。

## Steps

- [ ] **2027-03-20 之後**（JR 東日本 2027 年春季改正之後）：重開 `https://www.senat.co.jp/fare/sendaiair/` 與兩個時刻表頁，核對交通篇。
- [ ] **2027-03-25 起（每年 3 月底）**：重開 `https://www.rissyakuji.jp/` 核對山寺篇。
- [ ] **2027-03-31 前（之後每年 4 月）**：重開 `https://takeyakotsu.jp/zao-access/` 與 `https://takeyakotsu.jp/assets/download/gtfs-hokan-takeyakotsu.zip` 核對蔵王篇。
- [ ] **2027-04-01 前**：重看 `https://loople-sendai.jp/about/`（平日時刻表標「令和7年9月1日改正」）與 `https://www.kotsu.city.sendai.jp/fare/waribiki/`；四篇同一天複查 `https://www.kotsu.city.sendai.jp/fare/sendai_area_pass/`。範圍一旦不含山寺，山寺篇 H2-2 要整段改寫。
- [ ] **每年 3 月 JR 改正後**：松島篇仙石線；**jreast.co.jp 讀得到時**：交通篇、松島篇（仙台→松島海岸）、山寺篇（仙山線 仙台⇄山寺，補進 H2-1 與 H2-2 並更新 summary、FAQ 第 3 題與 diagram-1）、蔵王篇（仙台→白石蔵王）同 PR 補票價；仍然 403 就維持原樣，在各篇 `notes.md` 記一筆。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug sendai-airport-access-loople-bus-guide --slug sendai-matsushima-2-day-itinerary --slug yamadera-day-trip-from-sendai --slug zao-fox-village-from-sendai
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出改過的 slug 為 `update`，再 `--publish`；四篇的 2,930／1,470 與 630／920 逐字相同。

## Notes

- 來源：`docs/travel-guides-batch-7/sendai-airport-access-loople-bus-guide.md`、`sendai-matsushima-2-day-itinerary.md`、`yamadera-day-trip-from-sendai.md`、`zao-fox-village-from-sendai.md` 的「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 松島篇的 diagram-1 只畫移動順序，沒有票價，所以 scope 沒列它的圖目錄；其他三篇的圖有數字。
- 地下鐵分區間票價表只有圖片與 PDF：這台機器裝了 pdftotext 之後可把均一區外的票價補進交通篇 H2-3；SENDAI AREA PASS 價格出現在交通局官網時補一句進まるごとパス段落。都不是必要條件。
- 2026 年第四季的仙台項目分別在 `2026-09-19-sendai-airport-intl-2026-10`、`2026-09-19-sendai-matsushima-recheck-2026-q4`、`2026-09-19-zao-fox-winter-2026-11`。反向連結在「既有文章補連第七批」。`tasks/BOARD.md` 不要提交。
