---
id: 2026-09-16-existing-guides-season-sources
title: 既有文章依第七批規劃修正：沒有出處的季節月份與霧霾說法
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-16T23:06:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/bangkok-4-day-itinerary.json
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
---

# 既有文章依第七批規劃修正：沒有出處的季節月份與霧霾說法

## Why

規劃第七批時，季節篇的研究代理讀到泰國觀光局東京辦事處的天氣頁
（`thailandtravel.or.jp/about/weather/`）有 8 個地區乘 12 個月的官方月份表，
比各城市頁完整。對照之下，三篇既有文章寫的月份沒有出處，而且會和第七批的
季節篇（`southeast-asia-seasons-when-to-go`）互相矛盾——兩篇在季節段互連，
讀者點過去就會看到同一件事兩套說法。

## Definition of done

- [ ] `bangkok-4-day-itinerary` 的「5 到 10 月雨季」改成 TAT 月份表的口徑
      （多雨 7 月到 10 月、少雨 1 月到 4 月與 12 月），sources 補上月份表那一頁。
- [ ] `chiang-mai-3-day-itinerary` 的「PM2.5 常在 3 月最嚴重」拿掉哪一個月最嚴重的說法，
      改成「2 月到 4 月前後是燒田季，出發前查 Air4Thai 即時數據」。
      Air4Thai 與污染管制廳的頁面在這台機器上讀不到，不要補數值。
      同篇的雨季月份（6 到 10 月）若也沒有出處，一併改成以 TAT 月份表為準。
- [ ] `da-nang-hoi-an-4-day-itinerary` 的季節月份取自 vietnam.travel 的城市頁，
      與同站的氣候總頁差一個月。確認要以哪一頁為準，兩處寫法一致，並在 sources 標明。
- [ ] 改完之後，三篇與 `southeast-asia-seasons-when-to-go` 的說法一致。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
```

## Notes

- 這三篇已經上線，改的是既有內容包，`modified_at` 會動，屬預期。
- 第七批的季節篇規格（`docs/travel-guides-batch-7/southeast-asia-seasons-when-to-go.md`）
  的「官方來源」一節有月份表的網址與逐字讀到的月份，直接照它寫。
- 最好等第七批上線後和它一起改，兩邊同一個口徑；先改也可以，只要以月份表為準。
