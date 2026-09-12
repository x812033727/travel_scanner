---
id: 2026-09-12-naver-booking-ids
title: 找出韓國店家的 Naver 예약 商家編號
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-12T05:54:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/platform_reviews/2026-09-12-naver-booking.json
  - docs/catalog-content-reviews/2026-09-12-naver-booking.md
---

# 找出韓國店家的 Naver 예약 商家編號

## Why

韓國 80 間公開美食店家只有 7 間有訂位按鈕。CatchTable Global 上多半只有候位或電話，韓國餐廳實際
在用的是 Naver 예약。`naver_booking` 平台在 `2026-09-12-japan-korea-reservation-platforms` 已經
納入白名單，規則、測試、驗證方法都有了，只差**找不到每家店的商家編號**。

## Definition of done

- [ ] 73 間沒有訂位連結的韓國店家都有查核結果，能訂位的公開。
- [ ] 每筆 verified 都附 Naver 自己的 API 回傳的店名與道路名住址，證明是本店。

## Steps

- [ ] 找一個能查到 `booking.naver.com/booking/{分類}/bizes/{id}` 的檢索管道。
- [ ] 逐筆用 Naver 的 GraphQL 驗明正身（見下）。
- [ ] 結果寫成 review 檔，走 `apply-food-platform-reviews --file` 匯入。

## How to verify

驗證單一商家編號（不需登入、不需金鑰）：

```bash
curl -s -X POST https://booking.naver.com/graphql -H 'Content-Type: application/json'   --data '{"query":"query{ business(input:{businessId:\"215439\"}){ id name serviceName businessDisplayName businessCategory isDeleted addressJson bizItems{ id name } } }"}'
```

`bizItems` 非空且 `isDeleted` 為 false 就是真的在收訂位；`businessCategory` DL06 是餐飲、DL07 是美髮，
可以用來擋掉同名的美容院。`addressJson.roadAddr` 拿來跟清單住址對。

## Notes

2026-09-12 試過而且**不通**的管道，別再走一次：

- DuckDuckGo HTML 版（`html.duckduckgo.com/html/?q=site:booking.naver.com …`）：前兩三次可用，
  之後整批 403，再之後改出圖形驗證。隔一陣子會解，所以這條之後或許還能用，但要壓低頻率。
- Bing：忽略 `site:` 運算子，回傳完全無關的結果。
- `map.naver.com/p/api/search/allSearch`：回 `ncaptcha`，要 captcha token。
- `pcmap.place.naver.com/restaurant/{id}/home`：429。
- WebSearch 工具：`allowed_domains` 指定 naver.com 會直接被拒（naver 擋掉該 user agent），
  不指定的話結果裡也沒有 booking.naver.com。
- 從官網反查：73 間裡只有 3 間有官網。
- 內建瀏覽器直接開 `booking.naver.com`：被政策擋掉。

相關：`2026-09-12-japan-korea-reservation-platforms`。
