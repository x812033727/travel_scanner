# 2026-09-08 內建瀏覽器補證與座標更正

本輪於 08:54 UTC 完成一批來源修補；不是宣稱所有待審場所已符合發布條件。
前一輪全目錄評估留下的模型紀錄不變，這次依官方來源與內建瀏覽器補證，未重跑相同 Gemini 評估、增加候選或調整任何 API 額度。

## 實際結果

- 9 間店補上直接來源與官方地址，其中 4 間另取得獨立永久座標並核准。
- 另外 5 間仍缺獨立座標；來源修補已存檔，但保持 pending／inactive。
- 發現舊座標流程把 Google 座標標成 admin_verified；本次未沿用此標記作發布依據。
- 同一缺陷也影響上一輪由本任務核准的 4 間店，已撤回自己的核准，保留歷史並清除不成立的驗證標記。
- 本輪來源修補稽核 9 筆、更正稽核 4 筆，另各有既有店家更新稽核；13 筆全部重播成功，沒有重複寫入。

| 店家 | 結果 | 本次獨立來源及判斷 |
| --- | --- | --- |
| 鏞記酒家 Yung Kee | 核准 | [官方首頁](https://yungkee.com.hk/en/home/)的 Restaurant JSON-LD 同時指明餐廳名稱、威靈頓街 32–40 號及自有座標 22.2819, 114.1553；精準地圖同店，不混用 Yung's Bistro。 |
| 洪師父牛肉麵建北門市 | 核准 | [官方 LINE](https://page.line.me/ikz5554k)確認建國北路二段 72 號；[政府友善店家 CSV](https://data.taipei/api/frontstage/tpeod/dataset/resource.download?rid=5a5b36e0-f870-4b7f-8378-c91ac5f57941)的同分店原始座標 25.054943, 121.536473 與精準地圖交叉核對。 |
| 良品牛肉麵 | 核准 | 同份[政府友善店家 CSV](https://data.taipei/api/frontstage/tpeod/dataset/resource.download?rid=5a5b36e0-f870-4b7f-8378-c91ac5f57941)明列開封街一段 10 號、25.045914, 121.513928；精準地圖同店。排除字串近似但不同業態的林果良品。 |
| 三味食堂 | 核准 | [政府店家改造 CSV](https://data.taipei/api/frontstage/tpeod/dataset/resource.download?rid=af4a3527-e6c6-4c43-a127-6f1f4c893582)第 4 項明列貴陽街二段 116 號、25.039895, 121.502716；精準地圖同店。 |
| 何洪記希慎廣場 | 補證、待審 | 瀏覽器讀取[官方分店頁](https://tasty.com.hk/en/location/%E5%B8%8C%E6%85%8E%E5%BB%A3%E5%A0%B4-hysan-place/)，確認希慎廣場 12 樓 1204–1205 號舖，並比對精準地圖；頁面內嵌地圖不作永久座標證據。 |
| 聚興家 | 補證、待審 | [香港旅發局指定店家頁](https://www.discoverhongkong.com/eng/place-to-go/travel.guide-ju-xing-home.html)及精準地圖確認砵蘭街 418 號。不新增米其林主張；缺永久座標。 |
| 勝香園 | 補證、待審 | [香港旅發局指定店家頁](https://www.discoverhongkong.com/eng/place-to-go/travel.guide-sing-heung-yuen.html)與精準地圖確認美輪街 2 號；缺永久座標。 |
| Soup Curry Suage+ | 補證、待審 | [官方 Suage+ 分店頁](https://suage.mom/stores/suage-plus/)與精準地圖確認都志松ビル 2F；Suage2 是不同店，不能混用。缺永久座標。 |
| 欣葉台菜創始店 | 補證、待審 | [官方創始店頁](https://www.shinyeh.com.tw/content/zh/brand/Store.aspx?BrandId=1&Id=1)與精準地圖確認雙城街 34-1 號；其他分店及 Google iframe 不作座標佐證。 |

9 間店的精準 Google Place ID 均來自既有資料庫並逐一以內建瀏覽器實際開啟核對。沒有產生新 ID、保存 Google 評論、評分、照片或把其座標換標成官方資料。台北 CSV 的「友善」不代表寵物友善，沒有因此新增寵物接待條件。

## 開放資料來源與顯名

採用臺北市政府產業局商業處發布的原始經緯度欄位，不是 Google 內嵌地圖：

- [友善店家清冊](https://data.taipei/dataset/detail?id=d807396c-e41f-4005-be42-0160280783a1)，實讀 `11506-友善店家總表.csv`，993 列；中文檔更新時間 2026-07-20 11:38:58。
- [店家改造資料](https://data.taipei/dataset/detail?id=0d09e03e-bb11-4213-a9c8-6bfd392fbb16)，實讀 `店家改造資料_11502.csv`，201 列；更新時間 2026-03-04 16:54:20。
- 依平台[政府資料開放授權條款第 1 版](https://data.taipei/rule)使用；資料提供機關、年份、資料集名稱與 OGDL-1.0 已放入來源顯示名稱。沒有複製整份名冊或將名冊收錄等同營業／品質背書。

## 上一輪核准的更正

Yamamotoya Honten、Ukishima Brewing Tap Room、Gecko – Huế Cuisine & Craft Beer、Kanomwan Chang Moi 的前次核准依賴舊 admin_verified 欄位；這次追查其 coordinate_source_url 全部是 Google Maps，無法支持永久座標來源。山本屋及浮島的已知官方／觀光頁補查也未找到頁面自有結構化座標。

已只撤回本任務自己的 4 次核准，不批次修改其他管理員既有公開店家。更正為 pending／inactive、map unverified、coordinate_source_type=null；保留原 ID、歷史座標和來源 URL，完整 before／理由／先前核准稽核 ID 都留在獨立更正紀錄。這不是停業或店家不存在的判定，取得獨立座標後可再審。

前面 5 間仍缺座標的補證店家，也清除同種舊驗證標記。既有服務要求 map verified 必須同時有有效永久座標，因此完整定位狀態維持 unverified，這次已完成的分店身分核對另存稽核。

## 其他已查來源、未變更項目

| 店家 | 保留的具體原因 |
| --- | --- |
| Len Kyoto Kawaramachi | [官方 café/bar 頁](https://backpackersjapan.co.jp/kyotohostel/cafebar/)可證明一樓向非住客供應餐飲，卻未提供獨立座標；不把既有來源未重讀部分一併刷新。 |
| 太平館 | [官方頁](https://www.taipingkoon.com.hk/index.php/zh-hk/contact/locations)有四間分店，既有泛稱須先確定是哪一分店。 |
| 瓢亭 | [官方頁](https://hyotei.co.jp/en/)的本店／別館共用地址，但不是同一用餐產品；需核對精準身分。 |
| 並木薮蕎麦 | 行業組合名冊支持雷門 2-11-9，更新日期不明；不能套用栃木另一家堀江店資料。 |
| うどん平 | 招聘頁主體歸屬未充分確認，官方舊名冊仍是舊址。 |
| 戴記獨臭之家 | 市場處當期報導主體是石牌分店，不得套用到永吉候選；既有 Facebook 讀取受阻。 |
| 東一排骨 | 官方舊專訪有行政區筆誤；本輪未取得獨立座標與充分當前佐證。 |
| 宋廚菜館 | 可讀官方刊物較舊，沒有充分當前資料。 |
| 江豪記 | 品牌官網可證明公司旗下品牌，但總部／工廠地址不是門市地址。 |
| People & Life.Cafe | 官方 Facebook 讀取被阻擋；沒有繞過限制或採第三方舊食記直接核准。 |

上述 10 筆只記錄研究結果，未更改正式狀態或刷新來源查核日期。唯一待審風格 ACME 北美館維持原有待補證據理由；其餘景點也未重複消耗 Gemini 額度。

## 驗證與後續

- 公開 BFF：新核准 4 間各回傳 1 個精準結果；待審 5 間與撤回 4 間均回傳 0。
- 正式店家最終：273 核准／163 待審／3 拒絕。新增 4 核准與撤回自己的 4 次核准抵銷，不把修補筆數誤報為淨上架數。
- 初始全目錄的最終狀態數仍為：景點 435 退回、1,780 待審；店家 4 核准、163 待審；風格 43 核准、1 待審。核准店家名單已由本文件取代前一輪報告所列的名單。
- `followup-before.dump` 12,565,997 bytes、`followup-final.dump` 12,582,384 bytes，均 mode 600，`pg_restore --list` 通過；保留在原本伺服器私有審核目錄，未加入 Git。
- 9 筆 source_repaired 與 4 筆 provenance_correction 全部冪等重播成功。完整快照／真實操作者／前後值與服務正常稽核在同一交易提交。
- 第一輪套用完成 4 核准後，服務拒絕「verified 但清除永久座標來源」的待審修補。該筆交易回滾；調整為完整定位 unverified 後重播，前 4 筆不重複寫入，後 5 筆成功。沒有放寬服務驗證。
- 正式 `/ready` 為 database／redis ok、schema `0063_destination_offers`。未部署應用程式、改 schema、會員或帳務；本輪 Gemini 新增呼叫為 0，實際使用內建瀏覽器及公開來源查核。
- Ruff、format、容器 py_compile、JSON 解析、任務板與 diff 檢查通過。不宣稱已執行應用程式完整 CI。
- 已將舊 coordinate_queue 的來源誤標問題登錄為 P1 待辦 `2026-09-08-prevent-google-coordinates-being-labelled-durable`，本輪不混入未授權的程式部署或其他公開資料批次更正。

操作清單為 `ops/catalog_review_followup_20260908.json`，操作程式為同名 `.py`。它們是有日期、實體白名單及快照限制的一次性紀錄，不能當成自動核准工具。
