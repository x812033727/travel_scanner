---
id: 2026-10-05-itinerary-usj-september-hours
title: 大阪京都奈良四天行程的環球影城營業時間與票價寫死 2026 年 9 月
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-usj-hours
claimed_at: 2026-10-06T01:44:35Z
created_at: 2026-10-05T07:05:00Z
completed_at:
branch: claude/usj-hours
depends_on: []
scope:
  - apps/api/app/guides/content/osaka-kyoto-nara-4-day-itinerary.json
---

# 大阪京都奈良四天行程的環球影城營業時間與票價寫死 2026 年 9 月

## Why

`osaka-kyoto-nara-4-day-itinerary` 的 Day 4 段落寫的是「2026 年 9 月的營業時間依日期在 8:00 到 9:00 開園、21:00 到
22:00 閉園」，票價也標成「官方指定售票網站 2026 年 9 月價格」（1 日券 8,400 日圓起、1.5 日券 13,600 起、2 日券 16,000 起）。
十月起這段讀起來就是上個月的資料；環球影城的營業時間每天不同、票價是浮動的，寫死月份的寫法每個月都會過期。
2026-10-05 處理 KANSAI RAILWAY PASS LITE 時（票 `2026-09-14-refresh-kansai-lite-and-expressway-passes`）看到，不在那張票的範圍，沒有動。

## Definition of done

- [x] Day 4 的營業時間不再綁某一個月份：寫成讀者能自己查的形式（例如開園、閉園時間的大致範圍加「出發前一週看官網時間表」），
      或換成查證當月的數字並寫明月份。
- [x] 票價是改寫當天在官方或官方指定售票網站看到的起價，`sources` 的 `checked_on` 是那天。
- [ ] 合併後由協調者在站主同意下跑 `guides-import --slug osaka-kyoto-nara-4-day-itinerary`（dry-run 再 publish）。
      publish after merge (coordinator, owner consent)

## Steps

- [x] 用編輯 UA 讀 `https://www.usj.co.jp/web/zh/tw/park-guide/schedule/park-hour2`、`https://www.usj.co.jp/web/zh/tw/tickets`、
      `https://www.usjticketing.com/`。
- [x] 改 Day 4 段落；`cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary`、
      `PYTHONUTF8=1 uv run pytest tests/test_guides_content_pack.py -q`。

## How to verify

```bash
cd apps/api
grep -n "9 月" app/guides/content/osaka-kyoto-nara-4-day-itinerary.json   # 不再有綁九月的營業時間
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary   # 0 errors
```

## Notes

- 同一篇的 description 與開頭段落也寫「2026 年 9 月查證」；全篇重查時一起換，只改 USJ 段就不必動。
- 這篇沒有 summary 區塊，`pack_cli lint` 一直有 `no_summary` 警告；要補的話照 `docs/travel-guides-batch-7/README.md` §`pack.json`。
- 2026-10-06（claude-opus-5-5-usj-hours）：三頁用 curl 只拿到 app shell（`usj.co.jp` 是 Angular 殼加 Akamai 腳本，
  `usjticketing.com` 是 Vue 殼），沒有任何數字。改用 Playwright（`playwright-core` 1.63）啟動
  `ms-playwright/chromium_headless_shell-1243` 的 headless shell、編輯 UA 渲染，三頁都讀得到：
  - 營業時間日曆（要點月份標題右邊的箭頭換月，日曆文字在 `innerText` 抓不到，截圖或走訪 DOM 才看得到）：
    10/6–10/31 每天 08:00–22:00，只有 10/25 是 08:30–21:30；11 月 08:00–09:00 開園、19:00–22:00 閉園；
    12 月 08:00–09:00 開園、19:00–21:30 閉園，12/31 是 09:00–17:00。日曆只排到 2026 年 12 月。頁首另寫「當天可能會較園區開園時間提早開放入場」。
  - `usjticketing.com`（JTRWeb LTD.，USJ 授權售票）：1 Day Studio Pass 成人 ¥8,400〜、1.5 Day ¥13,600〜、2 Day ¥16,000〜（含稅），
    「Prices vary depending on the date of admission」；跟 9 月的起價一樣。
  - `usj.co.jp/web/zh/tw/tickets`：價格依日期不同、4 至 11 歲兒童票、購買需指定來園日期（購買後可辦改期）、嚴禁轉售、轉賣票的 QR Code 無效，
    段落裡原本這幾句都對得上，沒改。
- 段落改成「營業時間每天不一樣，大致在 8:00 到 9:00 開園、19:00 到 22:00 閉園，少數日子更早閉園」加看官網日曆；範圍取自
  9 月（舊文）到 12 月的日曆，不寫月份。票價改註「官方指定售票網站 2026 年 10 月 6 日的起價」。三筆 USJ 來源的 `checked_on` 改 2026-10-06，
  其他 17 筆沒重開、沒動。
- description、開頭段落與兩張表 caption 的「2026 年 9 月查證」、缺 summary、「這篇／本文」兩次，照上面的 Notes 沒動，開成
  `2026-10-06-itinerary-osaka-kyoto-nara-full-recheck`。
- 檢查：`pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary` 0 errors（`no_summary` 警告是舊的）；`pack_cli lint --kind howto`
  152 篇 0 errors；`pytest tests/test_guides_content_pack.py -q` 9 passed、5 skipped；`intake_check.py --from-content` 的三個 FAIL
  （沒有 summary、`?city=` 連結、自稱兩次）都是 main 上原本就有的。
- DoD 第三項沒做：publish after merge (coordinator, owner consent)。
