---
id: 2026-09-12-non-japan-reservation-sweep
title: 台灣、新加坡、泰國、越南的訂位連結再掃一輪
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T13:54:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/platform_reviews/2026-09-13-non-japan-platforms.json
  - docs/catalog-content-reviews/2026-09-13-non-japan-platforms.md
---

# 台灣、新加坡、泰國、越南的訂位連結再掃一輪

## Why

日本第二輪（`2026-09-12-japan-korea-reservation-platforms`）證明了一件事：2026-09-11 那一輪留下的
候選頁很稀，不是因為店家沒有平台頁，而是因為當時的查法沒掃到。同樣 83 間店，第一輪只有 44 個候選頁，
第二輪用「每店一個代理去搜五個平台網域」拿到 259 個，多出來的裡面有 5 間真的能訂位。

其他國家還沒用這個方法掃過：

| 國家 | 公開店家 | 有訂位連結 |
| --- | ---: | ---: |
| 台灣 | 55 | 5 |
| 越南 | 24 | 0 |
| 泰國 | 25 | 5 |
| 新加坡 | 24 | 13 |

（香港由 `2026-09-12-hk-openrice-public` 另外處理，不要重複。）

## Definition of done

- [ ] 這四國沒有訂位連結的店家都用第二輪的方法查過一次。
- [ ] 能訂位的公開，不能訂位的存成停用，結果走 `apply-food-platform-reviews --file` 匯入。

## Steps

- [ ] 取出四國沒有 `reservation_links` 的店家清單（公開 API 逐頁）。
- [ ] 每間一個代理，在該國的支援平台網域上找店頁並判斷是不是同一家分店。
- [ ] 候選頁一律機械化驗證能不能訂位，不讓代理判斷。
- [ ] 產出 review 檔與查核摘要，PR、合併、部署、試跑、`--apply`。

## How to verify

`https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁統計 `reservation_links`。

## Notes

- 各國的支援平台：台灣 inline／EZTABLE／Maifood，新加坡 Chope／SevenRooms，泰國 Hungry Hub，
  越南 PasGo。日本新加的四個平台對這些國家沒用。
- **代理只找頁、不判斷能不能訂位**。這些平台同樣會在店頁上放別家店的訂位按鈕
  （2026-09-11 就被 OpenRice 的 Suggested Restaurants 騙過）。
- 這一輪沒做的原因：WebSearch 在 2026-09-12 那個 session 用滿 200 次額度，
  日本那 83 間就把配額吃完了。四國合計 121 間，需要一個乾淨的 session，或把
  `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` 調高。
- 越南那 24 間上一輪在 PasGo 上全數查無。越南的路邊攤與老店本來就少有線上訂位，
  期望值最低，可以排最後。
