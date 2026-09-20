---
id: 2026-09-20-korea-food-specials-backlinks
title: Link city itineraries and must-eat to the Korea food specials
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T09:41:00Z
completed_at:
branch:
depends_on:
  - 2026-09-20-launch-korea-food-specials-1
scope:
  - apps/api/app/guides/content/korea-food-guide-must-eat.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/busan-3-day-itinerary.json
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/api/app/guides/content/daegu-2-day-itinerary.json
  - apps/api/app/guides/content/jeonju-hanok-village-day-trip-from-seoul.json
---

# Link city itineraries and must-eat to the Korea food specials

## Why

2026-09-20 的韓國美食與咖啡特輯（22 篇）上線後，既有的韓國內容還不知道它們存在。讀者看完「韓國必吃美食」不會知道每道菜都有一篇寫哪裡吃得到；看完首爾四天行程也連不到當地的美食特輯。

**刻意不寫總覽文章**（那會是一直長大的清單，又跟 `korea-food-guide-must-eat` 搶同一批查詢），所以這些反向連結就是讀者發現新文章的主要路徑。

順便修掉兩個已知的用詞與事實問題：

| 檔案 | 問題 | 依據 |
| --- | --- | --- |
| `korea-food-guide-must-eat.json` | 寫「參雞湯」，特輯與料理資料庫的定案是「**蔘雞湯**」（KTO 繁中料理辭典官方名） | `docs/korea-food-specials/handoff/glossary.json` |
| `daegu-2-day-itinerary.json` | 寫「막창구이：烤牛的第四個胃 홍창」 | 官方來源今天不是這樣寫（大邱豬、牛都有，沒有來源用 홍창）。R-daegu 研究階段查證 |

## Definition of done

- [ ] `korea-food-guide-must-eat` 的「各城市代表」一節，每個城市加一段連到該城市的美食特輯
- [ ] 五篇城市行程各自連到該城市的美食／咖啡特輯
- [ ] 「參雞湯」統一成「蔘雞湯」
- [ ] 大邱行程的 막창 描述改成官方頁真的寫的內容
- [ ] 每篇都通過 `pack_cli ingest --dry-run`

## Steps

- [ ] 等 `2026-09-20-launch-korea-food-specials-1` 的 22 篇在正式站發布
- [ ] 用 article inline（不是裸連結）連過去；目標都是 `howto`，不連 intel
- [ ] 重新查證大邱 막창 的官方寫法再改
- [ ] `guides-links-rebuild` 與 `guides-links-check --locale zh-TW`

## How to verify

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤，且 `korea-food-guide-must-eat` 頁面上每個城市段落都有一個連到特輯的連結。

## Notes

- 22 篇的 slug 清單在 `2026-09-20-launch-korea-food-specials-1` 的 scope 裡。
- 不要在這些文章裡重寫特輯已經寫過的東西（店家清單、菜單解讀），一句話帶過再連過去就好。
- 相關：`2026-09-14-answer-first-howto-descriptions`。
