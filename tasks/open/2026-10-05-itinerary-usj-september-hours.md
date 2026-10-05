---
id: 2026-10-05-itinerary-usj-september-hours
title: 大阪京都奈良四天行程的環球影城營業時間與票價寫死 2026 年 9 月
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T07:05:00Z
completed_at:
branch:
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

- [ ] Day 4 的營業時間不再綁某一個月份：寫成讀者能自己查的形式（例如開園、閉園時間的大致範圍加「出發前一週看官網時間表」），
      或換成查證當月的數字並寫明月份。
- [ ] 票價是改寫當天在官方或官方指定售票網站看到的起價，`sources` 的 `checked_on` 是那天。
- [ ] 合併後由協調者在站主同意下跑 `guides-import --slug osaka-kyoto-nara-4-day-itinerary`（dry-run 再 publish）。

## Steps

- [ ] 用編輯 UA 讀 `https://www.usj.co.jp/web/zh/tw/park-guide/schedule/park-hour2`、`https://www.usj.co.jp/web/zh/tw/tickets`、
      `https://www.usjticketing.com/`。
- [ ] 改 Day 4 段落；`cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary`、
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
