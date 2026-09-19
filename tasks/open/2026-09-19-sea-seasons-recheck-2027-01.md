---
id: 2026-09-19-sea-seasons-recheck-2027-01
title: southeast-asia-seasons-when-to-go 上線後複查：H2-3 補連越南兩篇、2027 年 1 月 TAT 東京行事曆與月份表、Air4Thai 與常年值換版
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:42Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/southeast-asia-seasons-when-to-go.json
  - apps/web/public/guides/southeast-asia-seasons-when-to-go
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
---

# southeast-asia-seasons-when-to-go 上線後複查：H2-3 補連越南兩篇、2027 年 1 月 TAT 東京行事曆與月份表、Air4Thai 與常年值換版

## Why

`southeast-asia-seasons-when-to-go` 的泰國月份來自 TAT 東京的行事曆頁與月份表（`/about/weather/`），每年 1 月前後換成新年度；本批第 3 到 7 篇的季節段都跟著本篇的月份寫。越南兩篇（`hue-day-trip-from-da-nang`、`ha-long-bay-cruise-from-hanoi`）上線後，規格允許在 H2-3 中部與北部小段各加一個 article inline（2026-09-19 查內容包，還沒有這兩個連結）。規格 `docs/travel-guides-batch-7/southeast-asia-seasons-when-to-go.md`「上線後與交叉檢查」列了這些與 Air4Thai、常年值換版的條件。

## Definition of done

- [ ] H2-3 中部與北部小段各加一個 article inline（`kind: howto`）連 `hue-day-trip-from-da-nang` 與 `ha-long-bay-cruise-from-hanoi`；加之前確認本篇連結總數與段落分布沒有把某一段塞滿連結。
- [ ] 2027 年 1 月前後：TAT 東京行事曆頁 2027 年版的宋干節日期與「暑期／雨期／乾期」月份、月份表色塊核對完，有改就同時改正文、表一、summary 與 diagram-1，並通知第 3 到 7 篇對月份（任何一篇改月份，同一個 PR 改其他篇）。
- [ ] `2026-09-16-existing-guides-season-sources` 把 `bangkok-4-day-itinerary`、`chiang-mai-3-day-itinerary` 的三處月份口徑修好之後，本篇的第 (3)、(4)、(5) 條小心事項一起更新。
- [ ] 每次改動更新 `checked_on`，lint 通過。做完 2027 年這一輪就 done，下一年度另開票。

## Steps

- [ ] **可立即做**：H2-3 補兩個 article inline，跑 `guides-links-check --locale zh-TW`。
- [ ] **2027-01 前後**：重看 TAT 東京行事曆頁與 `/about/weather/` 月份表。
- [ ] **Air4Thai 之後讀得到的話**：在清邁段補上官方的空氣品質月份或指標說明，並同步改 `chiang-mai-3-day-itinerary`；在那之前兩篇都維持「2 月到 4 月前後、出發前查 Air4Thai」。
- [ ] **常年值換版時**：新加坡氣象署與香港天文台的氣候頁目前是 1991–2020 年常年值；換成下一期時重查 171 天、2,113.3 毫米、28.6 度、26.8 度、80% 雨量、最乾與日照月份，有變就改表二、H2-4、H2-5 與 summary。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`，再 `guides-links-rebuild`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug southeast-asia-seasons-when-to-go
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `southeast-asia-seasons-when-to-go` 為 `update`，再 `--publish`；`guides-links-check --locale zh-TW` 沒有壞連結，打開 `/zh-TW/guides/howto/southeast-asia-seasons-when-to-go` 看 H2-3 與表一。

## Notes

- 來源：`docs/travel-guides-batch-7/southeast-asia-seasons-when-to-go.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 共用月份必須一字不差：普吉與喀比「乾季 11 月到 3 月、熱季 4 月到 5 月、雨季 6 月到 10 月」、清邁「11 月到 2 月最舒服、2 月到 4 月前後霧霾」；用字依各頁原文（普吉「綠季（雨季）」、喀比「雨季」），不要拿本篇的用字去改第 3、4 篇。
- 2028-01-01 拆 `taiwan-long-weekends-2027-flight-planning` 連結在 `2026-09-19-sea-seasons-unlink-2028-01-01`；斯米蘭、瑪雅灣封閉日期以普吉篇為準，複查在 `2026-09-19-dnp-park-closures-2027-01-15`。
- 反向連結（七篇既有文章季節段）在票 `2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批），三處月份待修在 `2026-09-16-existing-guides-season-sources`。`tasks/BOARD.md` 不要提交。
