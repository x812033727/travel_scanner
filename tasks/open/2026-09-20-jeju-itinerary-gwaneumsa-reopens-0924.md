---
id: 2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924
title: jeju-3-day-itinerary：漢拏山觀音寺路線 2026-09-24 重開，「觀音寺顯示預約限制」那句要改
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T00:24:19Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
---

# jeju-3-day-itinerary：漢拏山觀音寺路線 2026-09-24 重開，「觀音寺顯示預約限制」那句要改

## Why

第八批規劃的韓國研究（2026-09-20）讀到漢拏山國立公園公告板 2026-09-18 的公告：觀音寺探訪路「三角峰↔白鹿潭頂」區間
2026-09-24（四）05:00 起重新開放（https://visithalla.jeju.go.kr/board/boardView.do?bbsId=notice&seq=1300）。
既有 `jeju-3-day-itinerary` Day 3 方案 B 寫的是「城板岳正常開放預約、觀音寺顯示預約限制」，9/24 之後這句就錯了。

## Definition of done

- [ ] 2026-09-24 之後重讀公告板（`bbsId=notice`）確認已重開，改掉那一句（該文章若有其他語系，同一句一起改）。
- [ ] sources 的 `checked_on` 只更新實際重讀的那一條；`check`／lint 通過；`guides-import --slug jeju-3-day-itinerary`（動作是 update）。

## Steps

- [ ] 重讀公告 → 改句 → lint → PR → 匯入

## How to verify

`cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto --slug jeju-3-day-itinerary`；正式站該頁的那一句已更新。

## Notes

- 第八批候選 `hallasan-hiking-reservation-guide` 會把預約制與各管制所時間寫完整；這張票只修既有文章的過期句。
