# 釜山飯店：可保存座標來源續查

查核日期：2026-09-09（Asia/Taipei；精確 UTC 見相鄰 JSON）。範圍為本輪 `before.json` 的 10 間釜山待審飯店，版本皆為 1；只查公開來源，不操作正式環境。

## 結論

本輪 **0 筆可核准、10 筆維持待審**。找到新的合理來源，但尚未取得任何可重現的飯店原始座標；沒有進行投影轉換，沒有使用 Google、Naver、OTA 或已排除的 KTO/Wikidata 座標。

[行政安全部全國住宿許可資料 15044968](https://www.data.go.kr/data/15044968/fileData.do) 明確標示 EPSG:5174、免費與「利用許可無限制」。其[機讀中繼資料](https://www.data.go.kr/catalog/15044968/fileData.json) 再次確認發布者、座標系統與資料集授權；這是新的可行來源線索，不是把網站的一般版權宣告當成開放資料授權。

然而，官方連出的 [LOCALDATA 檔案入口](https://file.localdata.go.kr/file/lodgings/info) 普通公開 GET 回傳 **403 Forbidden**；主代理以內建瀏覽器正常讀取資料目錄，再前往正式連結，也確認 Forbidden。沒有嘗試偽造 Referer、使用舊下載端點繞過、登入、建立帳號或使用 API key。未取得原始檔，不得用授權中繼資料代替飯店座標證據。

## 授權與來源界線

- 選定資料集的實際標籤是「利用許可無限制」，**不是特定 KOGL1 標章**；保留原標籤，不換成另一種授權。
- [官方利用政策](https://www.data.go.kr/ugs/selectPortalPolicyView.do) 說明已提供的公共資料可不另申請而使用，第三方權利仍需合法授權。KOGL1 可商用、可改作的規則，不會自動套用到其他網站或資料。
- 目錄顯示資料名日期為 20251127、更新日 2026-02-10，並說明每日更新到兩日前。這些是目錄宣告，不等於已取得本日的實際飯店記錄。
- 機讀中繼資料 HTTP 200；UTF-8 解碼本文 SHA-256：`7a989fc2fecedc41fa2f9f9ef827bf54411854644a17c6aea08f473b6f7e3ace`。
- 原始 CSV、許可編號、精確名稱與全地址匹配、營業狀態、X/Y、原始檔 SHA-256 均未取得；沒有可接受的 WGS84 結果。

## 釜山市資料目錄補查

[釜山市官方公共資料目錄](https://data.busan.go.kr/bdip/opendata/dataSet.do) 的公開查詢介面，以「숙박업」取得 36 筆中繼資料（每頁 12，3 頁）。只保留下列與本批行政區相符的資料集識別，未保存無關業者資料、向量或索引內容。

| 資料集 | 管轄區 | 目錄列出的主要欄位 | 本輪不足 |
| --- | --- | --- | --- |
| 3075790 | 海雲台區 | 名稱、道路地址、電話、房間數 | 沒有實際飯店點位記錄 |
| 15025674 | 釜山鎮區 | 行業、住宿分類、名稱、地址 | 沒有實際飯店點位記錄 |
| 15025544 | 釜山鎮區 | 行業、申報日期、名稱、道路與地段地址 | 未取得原檔座標或原檔授權 |
| 3069341 | 中區 | 行業、名稱、地址、電話 | 沒有實際飯店點位記錄 |

目錄沒有列出座標，不足以斷言原始檔永遠沒有座標；本輪只確認未取得可保存點位，不能據此核准。完整 10 個官方路徑與唯讀查詢參數保存在相鄰 JSON，已達預定路徑上限，沒有擴展到更多來源或付費／需登入服務。

## 逐筆結果

| 飯店 | 版本 | 座標結果 | 審核建議 |
| --- | --- | --- | --- |
| Hotel Foret Premier Nampo | 1 | 無合格原始記錄；未轉換 | keep_pending |
| GRAND JOSUN BUSAN | 1 | 無合格原始記錄；未轉換 | keep_pending |
| Toyoko Inn Busan Seomyeon | 1 | 無合格原始記錄；未轉換 | keep_pending |
| Park Hyatt Busan | 1 | 無合格原始記錄；未轉換 | keep_pending |
| Paradise Hotel Busan | 1 | 無合格原始記錄；未轉換 | keep_pending |
| Shilla Stay Haeundae | 1 | 無合格原始記錄；未轉換 | keep_pending |
| L7 HAEUNDAE by LOTTE HOTELS | 1 | 無合格原始記錄；未轉換 | keep_pending |
| ARBAN HOTEL | 1 | 無合格原始記錄；未轉換 | keep_pending |
| LOTTE HOTEL BUSAN | 1 | 無合格原始記錄；未轉換 | keep_pending |
| Stanford Hotel Busan | 1 | 無合格原始記錄；未轉換 | keep_pending |

每筆產品 UUID、來源鍵、原官網身份連結與缺口都在相鄰 JSON。Naver 精準身份由主代理另外核對，本子任務不宣稱已驗證；就算 Naver 身份吻合，也不能補足可保存座標來源。

## 可重現轉換的前提

原始檔恢復正常公開存取後，先取得精確名稱與全地址吻合、唯一許可識別、有效營業狀態，以及官方 X/Y、資料時間和檔案雜湊。再使用來源已確認的 EPSG:5174，以 `Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)` 轉換，保存 pyproj/PROJ 版本、實際 pipeline 和結果。

不得由地圖畫面或地址猜 X/Y；行政許可點位也不得宣稱為實測入口。這次沒有輸入數值，所以轉換次數為 0。

未更改正式資料、飯店、平台選項、設定或額度。報告僅為來源研究與維持待審建議，不代表完成公開上線驗收。
