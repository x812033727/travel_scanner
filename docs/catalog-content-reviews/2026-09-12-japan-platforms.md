# 日本訂位平台查核紀錄（2026-09-12）

2026-09-11 那輪把 296 間公開美食店家全查過一遍，日本 96 間只查出 2 間可訂位。原因不是漏查，
是白名單裡沒有日本人實際在用的平台：當時的證據欄裡躺著食べログ 47 筆、AutoReserve 27 筆、
ホットペッパー 26 筆、ぐるなび 19 筆候選頁，全都存不進去。

使用者 2026-09-12 決定把 **食べログ、ホットペッパーグルメ、ぐるなび、AutoReserve、네이버 예약**
一起納入白名單。這份紀錄是納入之後對日本店家重查一輪的結果。

**寫入候選 106 筆：verified 12、disabled 86、not_found 8。**
逐筆資料在 [`2026-09-12-japan-platforms.json`](../../apps/api/app/foods/data/platform_reviews/2026-09-12-japan-platforms.json)。
沒有送出任何訂位，也沒有查空位；「可訂位」指的是頁面上有本店自己的訂位入口，不是保證訂得到。

## 各平台結果

| 平台 | 可訂位 | 有店頁但不能訂位 | 店頁已不存在 | 合計 |
| --- | ---: | ---: | ---: | ---: |
| 食べログ | 2 | 43 | 0 | 45 |
| ホットペッパーグルメ | 4 | 16 | 6 | 26 |
| ぐるなび | 2 | 15 | 2 | 19 |
| AutoReserve | 4 | 11 | 0 | 15 |
| Catchtable Global | 0 | 1 | 0 | 1 |

## 可訂位的店家

| 店家 | 平台 | 網址 |
| --- | --- | --- |
| やさい巻き串屋 ねじけもん | ホットペッパー | https://www.hotpepper.jp/strJ001025125 |
| 森八 本店 | ぐるなび | https://r.gnavi.co.jp/r6pyrfvf0000 |
| 矢場とん 矢場町本店 | ホットペッパー | https://www.hotpepper.jp/strJ000107401 |
| 琉球料理 赤田風 | AutoReserve | https://autoreserve.com/ja/restaurants/pY8eo63z1LYemPW9xxgg |
| 琉球料理 美榮 | AutoReserve | https://autoreserve.com/ja/restaurants/BPPgH4xy6to737C6QtQk |
| 首里 東道Dining | ぐるなび、AutoReserve | https://r.gnavi.co.jp/ejp0u6h60000 |
| 月と太陽BREWING 本店 | 食べログ、ホットペッパー | https://tabelog.com/en/hokkaido/A0101/A010103/1047035 |
| ジンギスカン ひげのうし 本店 | 食べログ、ホットペッパー | https://tabelog.com/en/hokkaido/A0101/A010103/1004766 |
| 炙屋十兵衛 | AutoReserve | https://autoreserve.com/ja/restaurants/MnzSEZfmc7Us9RLdv11o |

食べログ 的兩筆另存了繁中、簡中、韓文與英文四個語系頁，四頁都實際開過，都是同一個店家編號、
標題各自寫「Reservation」「可預約」「可预约」「예약가능」。日文版（無語系目錄）沒有存：
食べログ 的日文路徑擋掉了本次的抓取，沒有親眼確認過。

## 怎麼判斷一頁「真的能訂位」

四個平台都會在店頁上放**別家店**的訂位按鈕，照字串搜尋「ネット予約」必定誤判。實際依據：

| 平台 | 可訂位的標記 | 會誤判的東西 |
| --- | --- | --- |
| 食べログ | 側欄 `rstdtl-side-yoyaku__booking`，含日期日曆 | 頁尾推薦店家 |
| ホットペッパーグルメ | `<title>` 帶「＜ネット予約可＞」，JSON-LD `ReserveAction` 指向本店 `/strJ…/yoyaku/` | 「このエリアのお店」清單裡別家的ネット予約標籤 |
| ぐるなび | 連往本店 `plan-reserve/plan/plan_list/` 的「空席確認・予約する」 | 每頁都有的「ネット予約して来店すると、楽天ポイントが貯まる！」 |
| AutoReserve | 有「予約する」與空席欄位，且沒有「予約代行不可」 | 標題有沒有「の予約」與能不能訂位無關 |

AutoReserve 是**代訂服務**：送出後由 AutoReserve 代為向店家訂位，不是餐廳自己的線上訂位系統。
這四筆的說明欄都寫明了這一點。

## 日本的覆蓋率為什麼還是低

102 間日本公開店家裡，這輪之後有 19 間有訂位按鈕。不是查得不夠，是清單本身的組成：
沒有連結的 83 間裡，咖啡店與甜點佔 42 間、拉麵與麵食佔 17 間，這些店在日本本來就不收線上訂位。
逐頁打開的 105 個平台店頁裡，只有 12 頁有本店自己的訂位入口。

另外查到 43 間在 2026-09-11 沒有任何候選頁的店家（用食べログ英文站的站內搜尋），其中 0 間可訂位。

## 韓國：規則做好了，但這輪找不到店家頁

`네이버 예약`（`booking.naver.com/booking/{分類}/bizes/{id}`）的網址規則與測試都進去了，
驗證方法也找到了（Naver 自己的 GraphQL 會回店名、道路名住址與可訂項目），
但**找不到商家編號**：DuckDuckGo 查幾次就封鎖並改出圖形驗證、Bing 忽略 `site:` 運算子、
Naver 自己的地圖搜尋要 captcha token、WebSearch 的 user agent 被 naver.com 擋。
73 間待查的韓國店家裡只有 3 間有官網，也沒辦法從官網反查。留成 `2026-09-12-naver-booking-ids`。

首爾 하니칼국수 是唯一因規則放寬而能存進來的韓國店家（CatchTable id `hani._.noodle` 的中間分段
只有一個底線）。存為停用而非公開：該店在 CatchTable 上的服務是現場候位與優先入場，不是一般桌位訂位，
與 2026-09-11 其他候位型頁面的處理一致。

## 順帶查到的問題

食べログ 把 `osaka-kyoto-tables-coffee-bakery-diner` 標為已停業，ぐるなび 店頁轉回首頁，
ホットペッパー 店頁 404。三個平台同時消失，但這家店還公開在清單上。已另開
`2026-09-12-tables-coffee-closed`。
