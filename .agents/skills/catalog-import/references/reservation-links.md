# 訂位平台連結（韓國以外）

訂位連結是 `food_merchant_platform_links` 另一張表，**不是**店家來源也不是地點證據。規則全文：`docs/food-reservation-platforms.md`（白名單、各平台網址規則、後台編輯器、API）；歷次查核紀錄在 `docs/catalog-content-reviews/`（`2026-09-11-reservation-links.md`、`2026-09-12-japan-platforms.md`、`2026-09-12-japan-platforms-second.md`、`2026-09-13-non-japan-platforms.md`）。韓國：CatchTable 走 skill `catchtable-discovery`；네이버 예약的驗證法（免金鑰 GraphQL）與「找不到 business id」的死路記在 `tasks/open/2026-09-12-naver-booking-ids.md`。

## 白名單

`apps/api/app/foods/platform_links.py` 的 `PLATFORMS_BY_PROVIDER`，共 17 個 provider：國家預設 `tablecheck`（JP）、`catchtable_global`（KR）、`eztable`（TW）、`chope`（SG）、`openrice`（HK）、`hungry_hub`（TH）、`pasgo`（VN）；另加 `inline`、`maifood`、`sevenrooms`、`ikyu`（一休）、`myconcierge`、`tabelog`、`hotpepper`、`gurunavi`、`autoreserve`、`naver_booking`。國家預設只是提示，不是限制。新增平台要改程式（host、路徑規則、語言目錄）與測試，不是資料工作。

網址必須是 https、精確 host、指到單一分店的路徑；首頁、搜尋、清單、分店選擇頁都被拒。在地化網址要與 canonical 是同一分店。食べログ的語言目錄 `/en/`、`/tw/`、`/cn/`、`/kr/`、`/th/` 對應站台語系，無前綴是日文；AutoReserve 的 20 字元 ID 區分大小寫；ぐるなび的 `r.gnavi.co.jp/{shop}` 與 `gurunavi.com/{lang}/{shop}/rst` 不互通。

## 狀態

`verified`（頁面上有**本店自己**的訂位控制項，才公開成按鈕）、`disabled`（有本店頁但不能訂：只有電話、候位、「不接受線上訂位」）、`not_found`、`ambiguous`。站主 2026-09-11 決定：能開但不能訂的頁存 `disabled`，不公開。`verified` 與 `disabled` 必須附 evidence。

## 本店的訂位鈕 vs 鄰店的廣告

搜 HTML 裡的「予約」「Book」一律是假陽性：日本四個平台與 OpenRice 都在店頁上放別家的訂位徽章。只認下列本店控制項：

| 平台 | 能訂的證據 | 陷阱 |
| --- | --- | --- |
| 食べログ | 側欄 `rstdtl-side-yoyaku__booking` 區塊（有日期日曆）；英文標題多 `Reservation`、`/tw/` 標題「可預約」、`/kr/`「예약가능」 | 區域輪播裡的「ネット予約」是別家 |
| ホットペッパー | `<title>` 含「＜ネット予約可＞」且 JSON-LD `ReserveAction` 指向本店 `/strJ…/yoyaku/` | 網路訂位是付費會員功能，老店、咖啡、麵店幾乎沒有 |
| ぐるなび | 連到本店 `plan-reserve/plan/plan_list/` 的「空席確認・予約する」 | 每頁都有的「楽天ポイントが貯まる」橫幅不算 |
| AutoReserve | 「予約する」加空席欄，且**沒有**「予約代行不可」 | 標題結尾「の予約」不代表什麼；它是代訂 |
| OpenRice | 本店區塊的訂位控制項 | 頁下 Suggested Restaurants 的 Book 是廣告；多數只有電話 |
| Chope | 標題 `… - Book and Save On Chope` 且有 `id="time-field"` | `… - Discover On Chope` 加 `Sorry, this restaurant is not accepting reservations on Chope.` 是不能訂；JS 裡的 `not accepting any more reservations for the selected date` 每頁都有 |
| inline | 日期與人數表單 | 「抱歉，目前尚不開放線上訂位」＝不能訂；按壓不放的驗證牆可能一直不解 |
| EZTABLE | `/restaurant/{id}` 的 `__NEXT_DATA__` 帶 `info.active`、`info.hide` | — |
| Hungry Hub | 搜尋 `searchScore` 高分才是同名店 | 低分是平台推薦補位；同品牌不同分店要對座標 |

同一棟樓多家店（百貨、本店大樓）以目錄那一列自己的官網與招牌菜對，不挑最好看的那家。代理可以找頁、判斷分店；**能不能訂要機械判定**，不交給代理的感覺。

## 哪些網域讀得到

| 網域 | 讀法 |
| --- | --- |
| `tabelog.com` | 日文路徑 plain fetch 403、內建瀏覽器卡機器人牆；`/en/`、`/tw/`、`/cn/`、`/kr/` 讀得到且標記相同。搜尋用 `https://tabelog.com/en/rstLst/?sw=<關鍵字>`；比對店名用 `/tw/`（英文版只有音譯） |
| `hotpepper.jp`、`autoreserve.com` | 直接 fetch |
| `r.gnavi.co.jp` | fetch 403，用內建瀏覽器；量大時在任一 `r.gnavi.co.jp` 頁的 console 以同源 `fetch('/{shopid}/')` 一次抓幾十頁，檢查內文有沒有 `plan-reserve/plan/plan_list` |
| EZTABLE | `api-evo.eztable.com/search/autocomplete?keyword=` |
| Chope | 官方 `sitemap.xml` 全量比對 |
| Hungry Hub | `puma.hungryhub.com/graphql` 的 `SearchSuggestions` |
| PasGo | `pasgo.vn/Search/SearchHeader`（`keySearch`，含變音字） |
| inline、SevenRooms | 限定該網域的網路檢索 |

先拿平台上**已知存在**的店試搜尋管道，確定會回正確結果，才拿空結果當「查無」的證據（DuckDuckGo 對某些網域沒有索引，回的永遠是同一批無關結果）。

## 平台審查檔

`apps/api/app/foods/data/platform_reviews/<date>-<name>.json`：

```json
{
  "schema_version": 1,
  "batch_id": "2026-10-01-example",
  "researched_at": "2026-10-01T02:00:00+00:00",
  "records": [
    {
      "merchant_id": "…worklist 的 id…",
      "slug": "tokyo-example",
      "provider": "autoreserve",
      "status": "verified",
      "canonical_url": "https://autoreserve.com/…",
      "localized_urls": {"en": "https://autoreserve.com/en/…"},
      "review_note": "看到什麼、何時",
      "evidence": [{"url": "…", "role": "shop_page", "observation": "…"}],
      "name": "只給人看", "country_code": "JP", "booking_observation": "只給人看"
    }
  ]
}
```

- 每筆欄位額外的鍵會被拒（`extra="forbid"`）；一筆壞整檔拒收。`merchant_id` 與 `slug` 從 `export-food-merchant-worklist --status all` 取，兩者對不上 → `skipped_slug_mismatch`。
- 有審核者（後台存過）的列不會被覆寫，除非該筆帶上研究當時那一列的 `expected_checked_at` 且至今沒變；否則 `skipped_admin_reviewed`／`skipped_changed_since_research`，改在後台處理並記進報告。
- 同一個分店網址已掛在別家 → `skipped_branch_conflict`。
- 寫入時每列一筆 `food_merchant.cli_platform_link_reviewed` 稽核（含舊網址）。

套用：本機 `<PY> -c "from pathlib import Path; from app.foods.platform_review_import import load_review_file; print(len(load_review_file(Path('<file>')).records))"` → 主機 `apply-food-platform-reviews --file /dev/stdin` dry-run → `--apply` → 重跑全是 `unchanged`。

## 驗證

- 公開 API 的 `reservation_links`：`curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=tokyo&limit=50"`；換 `X-Travel-Locale` 看語系選擇（例如食べログ zh-TW → `/tw/`、zh-CN → `/cn/`、en → `/en/`、ko → `/kr/`，沒存日文變體的 ja 落回 canonical）。
- 頁面：`/zh-TW/foods` 上的按鈕。

## 覆蓋率為什麼低（別當成查核失敗）

2026-09 兩輪之後公開店家有訂位鈕的是 59／331：日本多是咖啡、甜點、拉麵這類不上付費平台的店；台灣、越南、泰國、新加坡 2026-09-13 用各平台自己的搜尋重查 105 家，新增 0。已查無的清單在上面的紀錄檔裡，不要重查同一批。
