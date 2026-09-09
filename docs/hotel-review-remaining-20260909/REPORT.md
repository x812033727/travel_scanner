# 飯店待審補證：2026-09-09

本輪使用內建瀏覽器實際核對 24 個新訂房網址，經正常管理流程核准 21 筆；
另留下 3 筆連結檢查保留與 3 筆京都地圖補證保留紀錄。這是已完成的補證批次，
不是全部飯店已可上架；尚有 20 間飯店與 84 筆訂房連結待補證。

## 正式資料結果

| 城市 | 已核准飯店 | 待審飯店 | 已核准連結 | 待審連結 | 前台可見連結 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 東京 | 10 | 0 | 57 | 3 | 57 |
| 大阪 | 10 | 0 | 44 | 16 | 44 |
| 京都 | 0 | 10 | 44 | 16 | 0 |
| 首爾 | 10 | 0 | 50 | 10 | 50 |
| 釜山 | 0 | 10 | 40 | 20 | 0 |
| 台北 | 10 | 0 | 41 | 19 | 41 |
| 合計 | 40 | 20 | 276 | 84 | 192 |

- 本輪新增核准：東京 9 筆、釜山 12 筆，共 21 筆。
- 前台由 183 增至 192 筆；新增釜山連結仍受待審飯店保護，不公開。
- 60 間飯店的整筆資料完全未變；原有 295 筆已核准飯店／連結均未變。
- 420 筆資料成員不增不減，實際有 399 筆整筆未變。
  operator 的 `untouched_rows=393` 指清單外資料；再加 6 筆原樣保留即 399。
- 新網址只填原空白欄位，正常 edit 與 review 各加一版，全部成功項目由版本 1 到 3。
  `property_id` 保持 null，不啟用報價，也不更改價格、分潤或其他設定。

## 保留原因

1. Agoda 的 Shilla Stay Busan Haeundae、Paradise Hotel Busan、Toyoko Inn Busan Seomyeon：
   內建瀏覽器可讀館名與街址，但正常流程回傳 `service_link_unavailable`。
   不繞過安全／可用性檢查；網址編輯與正常稽核完整回滾，只留下原樣保留收據。
   原欄位仍為空，版本仍為 1。瀏覽器觀察到的候選網址僅保留於證據文件。
2. Hotel Granvia Kyoto、Miyako Hotel Kyoto Hachijo、The Westin Miyako Kyoto：
   官方短地圖連結已在內建瀏覽器顯示同館身分，但未取得直接觀察到的 Google Place ID。
   官方 finder 在本輪一次重試仍為空白。沒有從 CID 轉造 ID，也沒有保存 Google 座標。
   既有獨立 CC0 座標候選不能取代地圖身分要求，因此不更改飯店欄位。
3. 首爾／釜山 Park Hyatt 與 Grand Hyatt Taipei 的既有官網連結再次顯示空白。
   這些重複的未解決狀態只補充本地紀錄，沒有再次新增相同保留收據。
   其他京都／釜山定位、來源授權及 Hyatt Regency Kyoto 營運日期限制繼續保留。

剩餘 84 筆連結中，73 筆尚無可用的已存精確網址，11 筆有既有網址但仍待確認。
搜尋未找到或網站無法讀取，不等於供應商沒有販售。
[remaining-items.json](remaining-items.json) 保留全部 104 筆未完成項目，舊證據仍附原時間，
不宣稱本輪重新驗證全部項目。

## 驗證與安全

- 操作前新建 PostgreSQL 備份，13,109,408 bytes，檔案 600／目錄 700；
  `pg_restore -l` 成功讀取 917 行索引，未宣稱已做完整還原演練。
  SHA256：`b0ef66c82bc36facd8b6268bca160f2a914410080212edc935c35540b4ed96f5`。
- 七個 live 管理／授權／資料模型／連結檢查檔案與本地版本 SHA256 相同。
- 正式唯讀 dry-run 27 筆通過；92 項離線 operator 測試、全新增 Python 的 scoped Ruff 通過。
- 首次唯讀 SQL 發現 JSON／JSONB 比較不相容，當時尚無正式審核寫入。
  保留失敗輸出，修正型別後使用同一 v2 SQL 完成 before／after／after-replay 三相比對。
- 27 個唯一收據，21 個正常 edit audit、21 個正常 review audit，皆屬原有效管理員。
  原 290 + 67 個歷史收據及所有原有稽核資料完整不變。
- 27 筆冪等重播回傳相同收據 ID，沒有新增稽核或變更資料。
- 三相 SQL 均為 REPEATABLE READ / READ ONLY；設定、品牌、報價、點擊紀錄未變。
- 前、後、重播後各 6 城市 × 5 語系，共 90 次匿名 GET，全部 200／no-store。
  原有 40 間飯店及 183 筆公開連結保留，待審飯店與選項不公開，價格仍為未知。
- 最終 `/ready` 正常，schema 仍為 `0063_destination_offers`。未遷移、部署或重啟服務。
- [verification-report.json](verification-report.json) 的獨立驗證結果為 `passed`，
  所有必要證據齊全。離線測試不等於另做了真實資料庫競爭測試；上述 SQL 為真實唯讀快照。

本輪沒有 Gemini 呼叫或增加額度。既有 Gemini 目錄審核只支援景點、美食、店家，
不把飯店偽裝成其他類型；本次使用使用者允許的內建瀏覽器。
沒有選日期、查價、訂房、點擊分潤連結、啟用分潤、上傳私密資料或修改原工作目錄。

## 重現與證據

本輪基準時間：`2026-09-08 21:18:03.737914+00:00`。
最終快照時間：`2026-09-08 21:48:36.678504+00:00`。
manifest 檔案 SHA256：`0924c315ee74cf344aa5dfe65949922750d88cd747d87ab8033153e70f5e45ba`。
基準、清單、正式 stdout、SQL 與公開 GET 均是獨立檔案，不覆寫前兩批證據。

```powershell
$env:PYTHONPATH = (Resolve-Path -LiteralPath apps/api).Path
& 'C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanㄐ/apps/api/.venv/Scripts/python.exe' -B -m pytest docs/hotel-review-remaining-20260909/test_operator_guards.py -q
& 'C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanㄐ/apps/api/.venv/Scripts/python.exe' -B docs/hotel-review-remaining-20260909/verify_results.py --require-complete
& 'C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanㄐ/apps/api/.venv/Scripts/ruff.exe' check ops/hotel_review_remaining_20260909.py docs/hotel-review-remaining-20260909/*.py --config apps/api/pyproject.toml
```

正式 operator 使用 `hotel-review-remaining-20260909` 收據命名空間與固定基準。
這批已套用的 manifest 不可修改後重新使用；後續補證必須重新擷取當時狀態與建立新批次。
僅保留本地功能分支與提交，未建立 PR、推送或合併。
