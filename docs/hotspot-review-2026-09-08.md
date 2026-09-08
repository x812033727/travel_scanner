# 景點候選瀏覽器補查 — 2026-09-08

## 實際結果

本輪限定台北／高雄 12 筆既有候選，使用內建瀏覽器的 Google 官方 Place ID Finder，並交叉閱讀官方場館／觀光資訊及 Wikidata 原始 P625。**11 筆核准、1 筆保留待審**，已寫入正式環境並驗證公開清單。沒有全數核准其餘候選，也沒有新增探索、調高額度、呼叫 Mokaair 付費供應商 API、合併 PR 或部署程式。

2026-09-08 09:32 UTC 最終狀態：

| 狀態 | 本輪前 | 本輪後 |
|---|---:|---:|
| approved | 1,049 | 1,060 |
| pending | 1,780 | 1,769 |
| rejected | 1,060 | 1,060 |
| disabled | 5 | 5 |

尚有 **1,769 筆待審**，仍需逐筆補齊可信來源及精準地圖身分；本文件不代表整個待審清單已完成。

## 逐筆判定

精確 UUID、Place ID、座標、快照 hash、決策及全部引用見 [已執行 manifest](../ops/hotspot_review_20260908.json)。

| 候選 | 結果 | 查證重點與來源 |
|---|---|---|
| 國立科學工藝博物館 | 核准 | 九如一路720號北館，非南館／圖書館。保留部分展廳及南館施工限制，不能視為全館無限制開放。[官方最新管制公告](https://www.nstm.gov.tw/ActivitiesDetailC001110.aspx?Cond=5230dcb2-2a3c-4927-bdec-79fa1c6b3d06) |
| 哈瑪星臺灣鐵道館 | 核准 | 蓬萊路99號B7/B8館舍，非鐵道文化園區或小火車。2026新展及近期觀光資訊優先於舊災休資料，不保證所有舊模型復原。[官方新展證據](https://www.khm.org.tw/tw/news/472) |
| 大港橋 | 核准 | 核對第三船渠旋轉橋，區分同名道路地址與周邊店家；不保存旋轉分鐘數斷言，通行仍依現場管制。[觀光署景點頁](https://www.tad.gov.tw/m1.aspx?id=A12-00474&sNo=0001121) |
| 高雄市電影館 | 核准 | 河西路10號本館。原資料引用的 Wikidata 與目前 P625 不符；改用觀光署直接列出的經緯度及正確來源標記。[官方票務](https://kfa.kcg.gov.tw/tw/ticket)、[官方經緯度欄位](https://www.tad.gov.tw/m1.aspx?id=9284&sNo=0001016) |
| 高雄市文化中心 | 核准 | 五福一路67號，非捷運站或其他文化中心；Wikidata preferred 座標有 OSM 溯源。[官方位置頁](https://khcc.kcg.gov.tw/rwd_home02.aspx?DATA=37329&EXEC=L&ID=%241101&IDK=2) |
| 中都唐榮磚窯廠 | 核准 | 中華橫路220號工業遺產；僅部分廠區開放，不代表全部窯體可進入。採文化資產局經記憶庫發布的古蹟代表點。[文化部資料](https://tcmb.culture.tw/zh-tw/detail?id=20050311000001&indexCode=BOCH_CountryCulture_11) |
| 四四南村 | 核准 | 松勤街50–56號園區，非單一店家；B館公共參觀與C館未開放分開判讀，不沿用舊C/D館資訊。[現行管理單位服務資訊](https://xydo.gov.taipei/News_Content.aspx?n=51D1E85EF9360CD6&s=B839F2810E8F54EA) |
| 國家鐵道博物館 | 核准 | 市民大道五段50號，非臺博鐵道部園區。第一階段開放不代表全工場均開放。[官方常見問題](https://www.nrm.gov.tw/News_Toggle.aspx?n=3361&sms=13224) |
| 富邦美術館 | 核准 | 松高路79號美術館，非整棟總部或會員咖啡廳。[官方參觀資訊](https://www.fubonartmuseum.org/Visit?tab=regulations) |
| 富陽自然生態公園 | 核准 | 臥龍街272巷公園，非公廁。不得把場租時段當遊客營業時間，遵守現場封閉／維護管制。[市府場地資料](https://service.gov.taipei/rental/VenueDetail/cf8368195c0b) |
| 松山文化創意園區 | 核准 | 整體園區，非單一倉庫、台北文創大樓或大巨蛋；不把戶外開放條件泛化為所有室內展覽。[官方FAQ](https://www.songshanculturalpark.org/service/qa) |
| 國立國父紀念館 | 保留待審 | 官方現行頁仍說明館內自2024-02-26起整修不開放；不能以戶外文化園區開放代替館舍復開證據。[官方辦公／參觀時間](https://www.yatsen.gov.tw/cp.aspx?n=8139) |

以上限制為編輯審核紀錄，沒有另外新增公開營業時間、門票、局部封閉 UI 或各語系介紹文案。

## 身分與座標邊界

- 在內建瀏覽器逐筆搜尋、選取並讀取 [Google 官方 Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder) 的實際識別碼；没有以 CID／十六進位地圖片段猜造 Place ID。
- 僅保存允許持久保存的 Place ID 及編輯核對結論。沒有下載或保存 Google 地圖截圖、地址原始 payload、瀏覽器地圖座標或評論。
- 9 筆採本日直接讀取的 Wikidata P625，1 筆採官方觀光頁經緯度，1 筆採文化部文化資產資料。全部如實保留來源，不使用 `admin_verified` 包裝 Google 座標。
- Wikidata 部分 claim 沒有 references；哈瑪星有兩個 normal claim，採精度較佳的一筆。這些是場館／園區代表點，不是已測量的遊客入口。國家鐵道博物館代表點與地圖館舍點不同，不代表跨館識別錯置。
- 電影館所用官方觀光開放資料有 [OGDL 授權](https://data.gov.tw/dataset/7777)，但資料集備註提到以 Google 座標地圖為主；本輪僅聲明使用官方發布欄位，**不宣稱其上游完全沒有 Google 或出自獨立測量**。文化記憶庫文字／事實與受限照片授權分開，未下載照片。
- 檢查 TPE／KHH 中英文同名／別名及所選11個Place ID，未發現既有景點占用這些ID；相鄰館舍、總部、捷運站、停車場未混用。

## 安全寫入與驗證

執行 [一次性審核程式](../ops/hotspot_review_20260908.py)，使用現有後端 `review_hotspot_candidates` 授權／發布契約，不直接用SQL改審核狀態。

- 真實管理員來自原已驗證請求及稽核，確認目前仍為有效管理員，且每筆都屬原候選集合；沒有建立合成管理員或存取瀏覽器 Cookie。
- 嚴格限定12個UUID、理由、來源URL、完整前置快照hash、列鎖、正常審核稽核及同交易提交後hash收據。
- 完整 dry-run 通過後才逐筆提交。11筆 `publication_gaps=[]`；國父維持 `pending`、`is_active=false`。
- 12筆重新執行皆回傳 `replayed`。正常 `hotspot_candidates_reviewed` 12筆、獨立來源 `hotspot_candidate_browser_reviewed` 12筆，沒有重播重複。
- pending 的既有 `review_reason` 依原服務契約不覆寫；本輪補查理由可於正常及補充稽核讀取。新來源URL存稽核，不直接覆寫舊 `TravelHotspot.source_urls`。
- 公開intro端點：11筆×5語系=55次HTTP200；國父5次HTTP404。
- 前台排名使用快照。以既有 `refresh_rankings` 及已儲存訊號重建本日衍生資料，另留1筆 `hotspot_rankings_refreshed` 稽核；沒有探索、外部API或虛構互動。操作時背景快照已含新資料，重建前後皆3,666筆。
- 公開BFF排名搜尋：12筆×5語系=60個查詢，11筆各返回唯一對應候選且map verified，國父各語系均不返回。
- 五語系名稱映射有值，但這12筆目前無額外 `hotspot_localizations`，使用既有繁中名稱回退；**不是已完成五語系人工翻譯**。
- 最終 `/ready` 回傳 ready，PostgreSQL／Redis正常。兩次相關服務檔案hash核對與本工作目錄一致；期間其他部署替換API容器後僅恢復一次性工具，未改部署。
- Ruff check／format、Python import與編譯、23個隔離防護／提交收據斷言通過；實際PostgreSQL dry-run、提交、重播及HTTP讀取通過。本輪沒有修改API/Web應用程式，未重跑整套產品CI。
- `check:tasks` 通過；`test:tools` 24項通過、1項因本獨立工作目錄未安裝 `@playwright/test` 而無法載入航空爬蟲測試。這是未修改工具的依賴缺口，不是全套工具測試通過；任務板測試另以聚焦命令驗證。

## 備份及復原線索

使用兩個現有部署鎖，正式備份與完整稽核保留於私有維運目錄 `/root/mokaair-catalog-review-20260908-RHlybdu8`。沒有刪除原備份或歷史候選。

| 備份 | 大小 | 權限 | 索引驗證 |
|---|---:|---|---|
| `hotspot-before.dump` | 12,588,102 bytes | 600 | `pg_restore -l` 成功 |
| `hotspot-final.dump` | 12,603,672 bytes | 600 | `pg_restore -l` 成功 |

Manifest SHA256：`fc0b00adbc676ef71f8d4ec3c9cbcf39c4218e30c9091b830d58e0d31ffa30b4`。
程式 SHA256：`cdddaba427f8f251d0a7a511fcf04f2ffc3a59becc8ece56c5b955978bd93901`。

需要復原時應先檢查後續異動及稽核，再做逐筆補償；不可直接覆蓋整個資料庫而破壞本輪後的會員／行程資料。剩餘候選必須使用新的來源判定與快照，不重用本批manifest冒充已審核。
