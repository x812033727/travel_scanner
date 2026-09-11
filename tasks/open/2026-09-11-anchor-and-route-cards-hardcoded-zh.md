---
id: 2026-09-11-anchor-and-route-cards-hardcoded-zh
title: 航班錨點卡與路線卡仍是硬編碼繁中
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T16:15:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/flight-anchor-card.tsx
  - apps/web/components/route-segment-card.tsx
  - apps/web/lib/itinerary-messages
---

# 航班錨點卡與路線卡仍是硬編碼繁中

## Why

行程時間軸本體已經在 `2026-09-11-itinerary-timeline-hardcoded-zh-tw` 清乾淨了，但它渲染的兩張子卡沒有：

- `flight-anchor-card.tsx`：「去程航班」「回程航班尚未設定」等。
- `route-segment-card.tsx`：「步行 · 18 分鐘」這類交通摘要。

和時間軸同一個問題、同一個後果：行程分享給日本或韓國朋友，頁首是他的語言，行程內容混著中文。時間軸的新測試（`itinerary-timeline.test.tsx` 的「the timeline in a language that is not Chinese」）刻意不放 route 與 flight anchor，就是因為這兩張卡會讓那個斷言在別人的問題上變紅——修完這張之後，那個 fixture 應該補回去。

## Definition of done

- [ ] 兩個檔案都沒有寫死的使用者可見中文。
- [ ] `itinerary-timeline.test.tsx` 的跨語系案例把 route 與 flight anchor 放回 fixture，仍然零漢字。

## Steps

- [ ] 用既有的 `lib/itinerary-messages/` 側 catalog，透過 `itineraryCopy(activeLocale())` 取用——和時間軸一致。
- [ ] 時間格式同樣依 locale。
- [ ] 更新 `itinerary-timeline.test.tsx` 的 fixture 與註解。

## How to verify

```bash
cd apps/web && npm run test:web -- itinerary && npm run check:i18n
```

## Notes

- 做法可以照抄 `itinerary-timeline.tsx` 這次的 commit：`itineraryCopy` + `itineraryText`，加上一個 `document.documentElement.lang = "en"` 的跨語系測試。
- `route-segment-card.tsx` 在 `2026-09-10-seoul-day2-transport-ux` 的 scope 裡（該任務已 stale 且工作已併入 main），claim 前先確認一下。
