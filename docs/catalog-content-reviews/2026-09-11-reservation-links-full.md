# 美食訂位平台連結：公開店家全面查核

接續 [首批 10 間紀錄](2026-09-11-reservation-links.md)。這一輪把沒有訂位按鈕的公開店家全部查過一次，結果存成可直接匯入的資料檔 [`apps/api/app/foods/data/platform_reviews/2026-09-11-public-merchants.json`](../../apps/api/app/foods/data/platform_reviews/2026-09-11-public-merchants.json)，由 `apply-food-platform-reviews` 指令寫入正式資料庫。

<!-- RESULTS -->

## 範圍

- 2026-09-11 16:00 UTC 讀公開 API `https://mokaair.com/api/travel/foods/merchants`，共 331 間：JP 102、KR 80、TW 55、TH 25、SG 24、VN 24、HK 21。
- 其中 35 間（37 列）已有公開按鈕，都是 2026-09-11 09:13–12:56 UTC 由另一個後台帳號在後台逐筆存的。這些不重查，只複查新加坡與曼谷的 Chope 頁是否仍收訂位。
- 其餘 296 間是這一輪的查核對象。

## 查核方法

全程用內建瀏覽器，分三組平行：日本；韓國與越南；台灣、香港、新加坡與泰國。每間店依序做三件事：

1. 有官網就先開官網，找出訂位連結實際連到哪個平台。店家自己連出去的平台頁是最強的證據。
2. 用 DuckDuckGo HTML 搜尋，限定在當地常見的支援平台網域。
3. 打開平台分店頁，核對店名與分店地址，並記下頁面有沒有訂位功能。

沒有送出任何訂位表單、沒有查空位、沒有登入，也沒有解驗證碼。DuckDuckGo 偶爾出現驗證頁，都是等候後重試，沒有繞過。

## 判定規則

- `verified`：12 個支援平台之一的精準分店頁，店名與分店都對得上，而且頁面可以訂位。OpenRice 則以餐廳概覽頁為準。只有這種會出現在前台。
- `disabled`：分店頁存在，但頁面明寫不接受透過該平台訂位。依 2026-09-11 的決定不公開，改用店家官網實際連出的平台。
- `not_found`：官網與當地常見平台都查過，沒有這家分店的頁面。記在該國的預設平台上，note 寫明查過哪些平台。
- `ambiguous`：有候選頁，但無法確認是同一家分店。不存網址，候選頁只放在證據裡。
- 12 個平台以外的訂位頁（Tabelog、Hot Pepper、AutoReserve、Naver 預約、Grab Dine Out 等）只記在 `unsupported_platform_evidence`，不寫入。

## 寫入方式與保護

- 指令預設只試跑，加 `--apply` 才寫入。它只寫訂位平台列，不動店家資料、座標、來源、分類或上架狀態。
- 每筆都用後台編輯器同一套規則（`MerchantPlatformLinkPayload`）驗證。任何一筆不合格，整個檔案就拒絕。
- 後台人工審核過的列一律跳過，除非紀錄帶著那一列目前的 `checked_at`。
- 同一個平台分店頁若已掛在別家店，該筆跳過。
- 每寫一列留一筆稽核，動作為 `food_merchant.cli_platform_link_reviewed`，並記錄新舊狀態與新舊網址。
- 資料檔另用前台的 `reservationPlatformHref` 逐一驗過，確保每個網址都會正常顯示成按鈕。
