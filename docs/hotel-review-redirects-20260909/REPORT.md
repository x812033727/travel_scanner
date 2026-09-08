# 飯店審核續批：3 個實際落地網址（2026-09-09）

已透過正常管理服務核准 **3 個釜山 Agoda 訂房選項**，沒有修改飯店本體。
本批不是全部飯店已通過的宣告，也不是再次套用上一批失敗的收據。

| 飯店 | 本批訂房選項結果 | 飯店本體 |
| --- | --- | --- |
| Shilla Stay Busan Haeundae | Agoda 核准，healthy，版本 1 → 3 | 維持待審 |
| Paradise Hotel Busan | Agoda 核准，healthy，版本 1 → 3 | 維持待審 |
| Toyoko Inn Busan Seomyeon | Agoda 核准，healthy，版本 1 → 3 | 維持待審 |

## 查核依據與限制

內建瀏覽器實際觀察到三個原 /en-us/ 網址落到各自 /zh-tw/ 飯店頁，
再直接重新載入落地網址，於 2026-09-08 23:13:55 UTC 核對名稱與完整地址。
地址與原有已核准官方來源紀錄一致；官方頁本批沒有重新讀取，保留原查核日期。
精確 URL、名字、地址及方法見 [iab-observations.json](iab-observations.json)。

正常伺服器 URL 檢查仍將三個原網址判為 unsafe，三個新觀察的落地網址均為 healthy。
這是 [link-diagnostics.json](link-diagnostics.json) 的實測結果，不把 unsafe 解讀成惡意網站，
也沒有放寬同站、路徑、DNS、重導向或身分檢查。
本批以新的基準、固定三個 UUID／精確 URL 和新收據命名空間處理；
舊批次的 guard failure 與證據完全保留。

沒有建立 property_id、取得有效房價、選日期、訂房、點擊分潤或新增分潤授權。
三個父飯店仍缺完整地圖／可持續使用座標證據，不能因訂房平台身分核准而公開。

## 目前目錄與剩餘工作

| 類型 | 已核准 | 待審 |
| --- | ---: | ---: |
| 飯店本體 | 40 | 20 |
| 獨立訂房選項 | 279 | 81 |

公開目錄仍是 40 間飯店、192 個訂房選項，未公開京都／釜山待審父飯店。
剩餘 81 個選項中，70 個尚無已存的精確網址，11 個有網址但尚未通過。
20 間待審飯店及 81 個選項的既有理由保存在 [remaining-items.json](remaining-items.json)；
這些原證據附原始時間，不宣稱本批全部重新審過，也不把找不到或讀不到解讀成未販售。
後續應取得新的精確平台／地圖身分、可持續使用座標或營運日期依據，再開新批次；
不能改已套用 manifest 後重用這批收據。

## 驗證

- 操作前新建 13,217,278 bytes 的 PostgreSQL 備份，成功讀取還原索引；
  檔案 600、目錄 700，未宣稱做完整還原演練。詳見 [preflight.json](preflight.json)。
- 7 個 live 正常服務檔案與本地未修改檔案 SHA256 相符。
- 3 筆正式環境 dry-run；正常 edit 與 review 稽核各新增 3 筆，審核收據 3 筆，
  均核對原有效管理員及已驗證的管理請求來源。
- 原 316 筆已核准資料、全部 60 間飯店、其餘 417 筆完整資料保持不變。
- 三相獨立 SQL 均為 REPEATABLE READ / READ ONLY，成功 ROLLBACK 後才輸出 JSON。
  13 組保護指紋相同：包含 9,330 筆歷史稽核、384 筆舊飯店審核收據、
  完整設定、品牌、報價及點擊資料。
- 3 筆冪等重播回傳相同收據 ID，420 筆資料不變，沒有新增稽核或收據。
- 前、後、重播後各 6 城市 × 5 語系，共 90 次匿名 GET 全為 200 / no-store；
  各組公開 ID、標題／來源標示／空房價／選項內容指紋完全一致。
- 172 項離線測試、使用 API 專案設定的 scoped Ruff 及任務板檢查通過；完整獨立驗證通過，見
  [verification-report.json](verification-report.json)。未跑部署／完整 CI，因本批是資料審核操作，
  不包含應用程式改版。
- 最後 /ready 顯示 schema 0063_destination_offers、資料庫與 Redis 正常；
  未部署、遷移或重啟，未呼叫 Gemini 或提高 API 額度。

基準 2026-09-08 23:08:17.381350+00:00；審核後快照 23:25:37.047143+00:00；
重播後快照 23:26:31.177948+00:00。manifest 檔案 SHA256：
7da37d9f0df1c7c79bd7e6465aac9f2a5be0b9f664410b5ffee69b29abc87d51。
原 operator 以 SHA256 固定匯入，wrapper 只縮限本批三個身分，沿用原授權與回滾安全規則。

## 本機重驗

使用既有 API Python runtime，PYTHONPATH 指向本工作樹 apps/api：

```powershell
python -B -m pytest --import-mode=importlib -q docs/hotel-review-remaining-20260909/test_operator_guards.py docs/hotel-review-redirects-20260909/test_operator_guards.py docs/hotel-review-redirects-20260909/test_verify_results.py
python -B docs/hotel-review-redirects-20260909/verify_results.py --require-complete
ruff check --config apps/api/pyproject.toml ops/hotel_review_redirects_20260909.py docs/hotel-review-redirects-20260909
node tools/tasks.mjs check
```

本批資料審核已在正式環境生效；工作紀錄只提交本機功能分支，不推送、開 PR 或部署。
