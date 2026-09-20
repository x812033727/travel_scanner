---
id: 2026-09-20-loy-krathong-yi-peng-2026-intel
title: 清邁水燈節與天燈節 2026 時效情報：10 月中旬官方日程公布後再寫（第八批規劃時官方來源還沒公布）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:27:36Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/loy-krathong-yi-peng-2026-chiang-mai.json
  - apps/web/public/guides/loy-krathong-yi-peng-2026-chiang-mai
---

# 清邁水燈節與天燈節 2026 時效情報：10 月中旬官方日程公布後再寫

## Why

站上的 `chiang-mai-3-day-itinerary` 只用一句話提到 2026 年滿月落在 11 月 24 日與湄登的私人天燈場次，沒有一篇講清楚
水燈節（Loy Krathong）與清邁天燈節（Yi Peng）怎麼安排。第八批規劃（2026-09-20）時這題被 drop，不是題目不好，
而是最關鍵的三組數字一組都讀不到：

- 清邁市政府 `cmcity.go.th` 最新的日程公告仍是 2568 年（2025 年，11 月 4 到 6 日），沒有 2569 年的公告。
- TAT 新聞室 `tatnews.org` 搜 Loi Krathong 最新一篇是 2025-11-01，沒有 2026。
- TAT 東京辦事處的清邁天燈節頁列的是 2024 年的節目表，頁面自己寫「最新資訊請向清邁市或 TAT 清邁辦事處確認」。
- 天燈施放的禁區與航道管制沒有官方依據：民航局 `caat.or.th` curl 與 WebFetch 都 403。

清邁市政府往年在 10 月中旬公布日程。這篇的 `valid_until` 約 2026-11-30，要趕在 10 月底前上線才有用。

## Definition of done

- [ ] 2026 年 10 月中旬重讀 `cmcity.go.th` 與 `tatnews.org`；讀得到 2026 年官方日期與節目表才寫，
      讀不到就再延後並記下試過的網址。合法施放場次與價格只寫官方或主辦單位讀得到的。
- [ ] intel、zh-TW、destination_id `chiang-mai`、topics `season`／`culture`、上限 2,200 字、`valid_until` 約 2026-11-30；
      互連 `chiang-mai-3-day-itinerary`，以及第八批的 `chiang-mai-night-markets-walking-streets`、
      `chiang-mai-airport-transport-where-to-stay`、`thailand-temple-etiquette-dress-code`（已上線的才連）。
- [ ] 過期處理：`valid_until` 隔天拿掉其他文章連過來的連結（照第七批 README 的時效規則）。

## Steps

- [ ] 重讀官方來源 → 規格 → 撰稿 → 獨立查核 → 出圖與照片 → PR → 匯入

## How to verify

`pack_cli lint --kind intel --slug loy-krathong-yi-peng-2026-chiang-mai`；正式站頁面 200、可索引。

## Notes

- 研究紀錄在第八批規劃工作區的泰國研究檔第 10 節（不在 repo）；重點已抄在上面。
- 對外請求 UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不得帶任何人的 email 或個人資料。
