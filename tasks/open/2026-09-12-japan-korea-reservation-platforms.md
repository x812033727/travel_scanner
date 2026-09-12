---
id: 2026-09-12-japan-korea-reservation-platforms
title: 日本與韓國訂位平台納入白名單，並補上對應店家連結
status: in-progress
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-12T05:00:19Z
created_at: 2026-09-12T05:00:14Z
completed_at:
branch: claude/food-booking-platform-links-db11f4
depends_on: []
scope:
  - apps/api/app/foods/platform_links.py
  - apps/api/app/foods/data/platform_reviews
  - apps/api/tests/test_food_platform_links.py
  - apps/api/tests/test_food_platform_review_import.py
  - apps/web/lib/reservation-platforms.ts
  - apps/web/lib/reservation-platforms.test.ts
  - docs/catalog-content-reviews
---

# 日本與韓國訂位平台納入白名單，並補上對應店家連結

## Why

331 間公開美食店家只有 45 間有訂位按鈕，日本 10/102、韓國 7/80。2026-09-11 那輪已經把 296 間
全查過一遍，所以剩下的空白不是漏查，是白名單太窄：當時決定「只存現有 12 個平台」，日本真正在
收訂位的食べログ（47 筆候選）、AutoReserve（27）、ホットペッパー（26）、ぐるなび（19）全被擋在
證據欄裡，韓國的 Naver 예약 也一樣。

使用者 2026-09-12 決定推翻那條限制，把日本三大加 AutoReserve 與 Naver 예약 一起納入。

## Definition of done

- [x] 五個平台的網址規則前後端一致，各自有正例與反例測試。
- [x] 日本店家依新平台重查一輪，能訂位的公開、不能訂位的存成停用。
- [x] 既有 12 個平台的判斷一個都沒被放寬。

## Steps

- [x] `platform_links.py` 與 `apps/web/lib/reservation-platforms.ts` 加上五個平台。
- [x] 順手修掉 `2026-09-11-catchtable-underscore-segment-id`：CatchTable id 的點分段可以用底線開頭。
- [x] 查核並產出 `apps/api/app/foods/data/platform_reviews/2026-09-12-japan-platforms.json`（106 筆：verified 12、disabled 86、not_found 8）。
- [x] 查核摘要寫進 `docs/catalog-content-reviews/2026-09-12-japan-platforms.md`。
- [ ] PR、合併、部署，在 api 容器試跑 `--file`，確認後 `--apply`。

## How to verify

- `cd apps/api && pytest tests/test_food_platform_links.py tests/test_food_platform_review_import.py`
- `cd apps/web && npx vitest run lib/reservation-platforms.test.ts`
- 部署後：`docker compose -f docker-compose.prod.yml exec -T api python -m app.cli
  apply-food-platform-reviews --file app/foods/data/platform_reviews/2026-09-12-japan-platforms.json`
  （試跑），再加 `--apply`。
- 公開 API `https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁統計 `reservation_links`。

## Notes

### 怎麼判斷一頁「真的能訂位」

四個平台都會在店頁上放別家店的訂位按鈕，照字串搜尋「ネット予約」一定會誤判。各自看這個：

- 食べログ：側欄 `rstdtl-side-yoyaku__booking`（含日期日曆）。英文頁標題也會多一個 `Reservation`，
  繁中頁寫「可預約」、韓文頁寫「예약가능」。
- ホットペッパー：`<title>` 帶「＜ネット予約可＞」，JSON-LD 的 `ReserveAction` 指向本店自己的
  `/strJ…/yoyaku/`。頁面下方「このエリアのお店」清單裡的ネット予約標籤是別家的。
- ぐるなび：有連往 `r.gnavi.co.jp/plan/{id}/plan-reserve/plan/plan_list/` 的「空席確認・予約する」。
  頁尾「ネット予約して来店すると、楽天ポイントが貯まる！」是通用宣傳，每一頁都有。
- AutoReserve：有「予約する」與空席欄位，且**沒有**「予約代行不可」。

### 哪個網域抓得到

- 食べログ：日文路徑（`tabelog.com/osaka/...`）對一般抓取回 403，內建瀏覽器也卡在機器人驗證；
  但 `/en/`、`/tw/`、`/cn/`、`/kr/` 四個語系路徑可以直接抓，內容一樣。站內搜尋
  `https://tabelog.com/en/rstLst/?sw=<關鍵字>` 也通，是找店頁最省事的方法。
- ホットペッパー、AutoReserve：直接抓得到。
- ぐるなび：`r.gnavi.co.jp` 對一般抓取回 403，要用內建瀏覽器。
- Naver：`booking.naver.com` 被內建瀏覽器的政策擋掉，頁面本身又是空殼 SPA。

### Naver 예약：規則做好了，但這輪找不到店家頁

`booking.naver.com/booking/{分類}/bizes/{id}` 的規則與測試都進去了，驗證方法也找到了——
`POST https://booking.naver.com/graphql`，query
`{ business(input:{businessId:"…"}){ id name serviceName businessDisplayName businessCategory
isDeleted addressJson bizItems{ id name } } }`，會回店名、道路名住址與可訂的項目，
`bizItems` 非空且 `isDeleted` 為 false 就是真的在收訂位（`businessCategory` DL06 是餐飲、DL07 是美髮）。

卡住的是**怎麼找到 id**：

- DuckDuckGo HTML 版查幾次就 403，之後改出圖形驗證，不能過。
- Bing 忽略 `site:` 運算子。
- Naver 自己的 `map.naver.com/p/api/search/allSearch` 要 captcha token，`pcmap.place.naver.com` 回 429。
- WebSearch 工具的 user agent 被 naver.com 擋，`allowed_domains` 直接拒絕。
- 韓國 73 間待查店家裡只有 3 間有官網，沒辦法從官網反查。

所以韓國這半留成 `2026-09-12-naver-booking-ids`。等 DuckDuckGo 的封鎖過了（之前的經驗是隔一陣子會解），
或改用有 Google 檢索結果的管道，一輪就能查完——驗證那半已經現成。

### 這輪的結果

PR #428。日本可訂位的 9 間店共 12 筆連結：ジンギスカン ひげのうし 本店與月と太陽BREWING 本店
（食べログ＋ホットペッパー）、やさい巻き串屋 ねじけもん與矢場とん 矢場町本店（ホットペッパー）、
首里 東道Dining（ぐるなび＋AutoReserve）、森八 本店（ぐるなび）、琉球料理 赤田風、琉球料理 美榮、
炙屋十兵衛（AutoReserve）。日本覆蓋率 10/102 → 19/102。

覆蓋率還是低不是查得不夠：沒有連結的 83 間裡，咖啡店與甜點佔 42 間、拉麵與麵食佔 17 間。
逐頁打開的 105 個平台店頁只有 12 頁有本店自己的訂位入口。另外用食べログ英文站搜出 43 間
原本沒有任何候選頁的店家，0 間可訂位——這 43 間不必再查一次。
