# 飯店審核續批：21 個平台身分（2026-09-09）

已透過內建瀏覽器核對名稱、分店與完整地址，並由正常管理服務核准 **21 個訂房選項**。
正式資料已生效，前台增加 20 個可見選項；本批沒有核准或修改飯店本體，也不宣稱全部通過。

| 區域 | 本批核准 | 前台新增 | 飯店本體 |
| --- | ---: | ---: | --- |
| 大阪 | Expedia 7、Agoda 2 | 9 | 原已核准，保持不變 |
| 台北 | Expedia 5、Agoda 6 | 11 | 原已核准，保持不變 |
| 京都 | Agoda 1 | 0 | Daiwa Roynet Kyoto Terrace 仍待審，不公開 |

## 查核依據與精確修改

[iab-observations.json](iab-observations.json) 保存本批實際瀏覽的原始／落地網址、
名稱、完整地址、時間與操作方式；來源研究檔只是查找線索，不能代替瀏覽器驗證。
本批瀏覽時間為 2026-09-08 23:42–23:52 UTC。
既有官方身分紀錄只作為帶原查核日期的比對依據，本批沒有重新瀏覽官方頁。

- 20 個空的待審選項填入實際觀察到的個別飯店網址及相同證據網址。
- Kyoto Daiwa 一筆既有待審選項，精確改為實際觀察並重新載入的 `/zh-tw/` 落地頁；
  原網址及官方證據仍留在新審核來源與歷史資料。沒有改 parent、provider 或 property ID。
- WESTGATE 從實際評論頁的「立即預訂永安棧」連結取得飯店頁，再核對名稱及地址，
  不是用字串拼接猜測 URL。
- Swissotel／Granvia 的 Agoda URL 雖含 `kobe-jp`，實際飯店名稱與大阪完整地址均已核對；
  保留實際 URL，沒有自行改城市路徑。Hankyu RESPIRE OSAKA 與 GRAN 分館未混用。

正常 URL 檢查為 Agoda 9 筆 `healthy`、Expedia 12 筆 `unconfirmed`，見
[link-diagnostics.json](link-diagnostics.json)。後者由本批實際 IAB 證據走既有人工查核流程；
沒有放寬 DNS、同站、重導向、路徑或身分條件，也沒有覆寫 unsafe／unavailable 結果。
全部 21 筆由正常 edit、review 通過，版本 1 → 3，沒有 guard hold。

沒有建立 property ID、取得有效房價、選擇日期／房型、訂房或點擊分潤。
平台身分核准不是報價 API 能力或分潤使用權的證明，也不會替代飯店地圖審核。
Google 官方 Place ID Finder 文件的內嵌工具本次未載入可用結果；沒有取得新的 Place ID，
沒有轉換 CID、擷取平台座標、借用憑證或以猜測值補齊地圖資料。

## 目前目錄及未完成項目

| 類型 | 已核准 | 待審 |
| --- | ---: | ---: |
| 飯店本體 | 40 | 20 |
| 訂房選項 | 300 | 60 |

公開目錄仍為 40 間飯店，可見訂房選項 **192 → 212**。
京都與釜山各 10 間飯店仍待審；其中已核准的獨立平台選項也不會繞過父飯店公開條件。
60 個待審選項中，50 個缺已存的精確平台網址，10 個已有網址但仍有未解條件。

[remaining-items.json](remaining-items.json) 保存 20 間飯店與 60 個選項的原始逐項理由、
來源及查核時間；所有保留列與本批前的完整資料相同。
這些是帶日期的既有評估，不宣稱本批重新查核全部，也不將「未找到」解讀為未販售或下架。
仍須補充精確地圖／平台身分、可持續使用的座標及來源，或處理既有營運日期限制。
後續新證據應另建新基準與新批次，不能修改本批已套用 manifest 或清空待審。

## 實際驗證

- 操作前新建 PostgreSQL 備份 13,221,370 bytes，還原索引可讀；檔案 600、目錄 700。
  未做完整還原演練，舊備份全保留。詳見 [preflight.json](preflight.json)。
- 7 個 live 正常服務檔案 SHA256 與本地未修改應用程式一致；21 筆無寫入 dry-run 通過。
- 實際新增正常 edit 21 筆、review 21 筆、審核收據 21 筆；操作者與原有效管理員請求一致。
- 全部 60 間飯店、原 319 筆已核准資料、範圍外 399 筆完整列保持不變。
- 前／後／重播後獨立 SQL 使用 REPEATABLE READ / READ ONLY，成功 ROLLBACK 才輸出。
  13 組保護指紋相同，包含 9,663 筆歷史稽核、387 筆舊收據、完整設定、品牌、報價與點擊。
- 重播 21 筆使用相同收據 ID；完整 420 列不變，沒有新增正常稽核或收據。
- 三階段各 6 城市 × 5 語系，共 90 次匿名公開 GET 均為 200 / no-store。
  原 192 個選項及所有既有公開欄位不變；僅增加本批已核准且父飯店可公開的 20 個選項。
- 178 項離線測試通過（既有核心 92、新操作防護 35、新完整驗證 51）；
  scoped Ruff、任務板與完整驗證通過。見 [verification-report.json](verification-report.json)。
- 本批審核時 /health 正常，/ready 為 schema 0063、PostgreSQL／Redis 正常。
  審核與重播完成後釋放兩個部署鎖，讓另一個已授權任務取得部署窗口；
  此處只是當時的健康證據，不宣稱後續部署已完成。

本批基準 2026-09-08 23:37:42.330750+00:00，重播後快照
2026-09-09 00:14:07.932005+00:00。manifest 檔案 SHA256：
`39b81265da878c2ab252357650e976160b120b0fc329ffa6c7c305931d931fe0`。
操作器以 SHA256 固定原核心，保留授權、完整列鎖定、交易回滾及冪等規則；
僅容許精確 manifest 與唯一既有 Daiwa URL 修正，其他選項仍須原本為空。

## 本機重驗

在本工作樹使用既有 API Python runtime，PYTHONPATH 指向 `apps/api`：

```powershell
python -B -m pytest --import-mode=importlib -q docs/hotel-review-remaining-20260909/test_operator_guards.py docs/hotel-review-platforms-20260909/test_operator_guards.py docs/hotel-review-platforms-20260909/test_verify_results.py
python -B docs/hotel-review-platforms-20260909/verify_results.py --manifest-sha256 39b81265da878c2ab252357650e976160b120b0fc329ffa6c7c305931d931fe0 --require-complete
ruff check --config apps/api/pyproject.toml ops/hotel_review_platforms_20260909.py docs/hotel-review-platforms-20260909
node tools/tasks.mjs check
```

本批是正式環境資料審核，不修改應用程式；未跑部署／完整 CI。
未呼叫 Gemini、提高 API 額度、部署、遷移或重啟。證據只提交本機功能分支，不推送或開 PR。
