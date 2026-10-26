# DuckDB 2.0 agent模式：原創配送跟進清單

這是2026-10-25的本地教學實跑，不是實際業務資料、AI模型評測或Claude Cowork產品操作。原創1,200筆虛構配送紀錄，任務是找出「已送達，而且實際天數超過承諾天數」的跟進清單；在途紀錄不當成已送達延遲。

原研究實際運行DuckDB2.0.0 Linux amd64 CLI，官方MIT授權。套件24,424,037 bytes，SHA256 `c6507206baf7793c6013dbd82368469a45f20dc0e17a6f92f204602f652ed2bc`，與正式release asset digest相符；二進位僅解到原研究scratch，沒有安裝到系統或啟動服務。本可攜子集不附壓縮包或執行檔，也沒有重新下載或執行DuckDB。原創練習資料、報告與自寫程式可按[CC0-1.0](LICENSE-ORIGINAL.txt)重用；DuckDB仍依其[MIT授權](sources/duckdb-license.raw)，原始官方網站文字不在此授權之列。

已完成輸出：

- [完整CSV](output/late-followup.csv)：完整480筆，不是螢幕預覽。
- [Parquet](output/late-followup.parquet)：同一結果的原始交付檔；原研究再讀出成[CSV](output/parquet-readback.csv)，逐列完全相同。
- [原創中文HTML報告](output/followup-report.html)：可直接打開，連到完整輸出、SQL與結果紀錄。
- [runlogs](runlogs/)：同一2.0 CLI的`-agent`／`-no-agent`完整stdout、stderr、精確argv與時間。這不是2.0對1.5的速度比較。
- [完整SQL](sql/03-followup.sql)：建表前提、欄位型別與兩份完整COPY；[刻意錯字](sql/02-intentional-typo.sql)是作者的格式示範，不是觀察到的AI失誤。
- [來源HTTP收據](sources/)、[固定套件資料](selected-package.json)、[下載校驗收據](package-check.json)：保留官方URL、日期與digest。收據中的原始scratch下載路徑是歷史來源，不表示那些大檔存在於本子集。

先依[KIT-README](KIT-README.md)在自己的Linux amd64副本準備固定CLI和套件；本子集尚未具備它們。以下重跑只寫執行者自己的資料夾，會更新輸出與時間紀錄；不能拿重跑後的收據冒充這份2026-10-25原始快照：

```sh
python -B run_demo.py
```

或直接讀同一份輸入預覽，明確選人類／agent輸出，不依賴自動偵測：

```sh
./bin/duckdb -no-init -no-agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/03-followup.sql
```

`-no-init`是為了不讀使用者的預設初始化檔；`:memory:`是本次臨時資料庫。原始資料和輸出仍是此目錄的本機檔案。沒有伺服器、遠端查詢、擴充套件安裝、帳號或API秘鑰。先看程式與SQL再執行，與本輪預先讀MIT／CLI相關程式碼的做法相同。

核心規則可以完整照寫：

```sql
SELECT parcel_id, route, promised_days, actual_days,
       actual_days - promised_days AS days_late
FROM parcels
WHERE status = 'delivered'
  AND actual_days > promised_days
ORDER BY parcel_id;
```

COPY的完整資料庫建立、型別與輸出位置都在`sql/03-followup.sql`，沒有省略讀檔前提。

新特性是2.0 CLI agent模式的緊湊Markdown、明確遺漏行標記／結果hash與JSON錯誤；CSV讀取、SQL篩選／分組、CSV和Parquet匯出是既有功能。當畫面只顯示前後列，不能將其當完整名單。這次全量CSV由獨立Python標準函式庫逐列核對，並完成Parquet往返；沒有量測模型理解、token、費用、速度節省或生產環境升級。

官方資訊：10月9日agent模式介紹，10月21日2.0正式release；2.0 LTS支援至少到2027年10月。相容限制與現有資料庫遷移依當天官方migration文件，這次沒有更動舊資料庫。今日官方GET採正常editorial UA，每次請求開始至少間隔1.1秒；沒有重試403或繞過限制。

本子集的檔案範圍及SHA見[新manifest](manifest.json)，沒有沿用包含大檔的舊manifest。獨立標準函式庫再次驗證1,200筆輸入與480筆排序結果；Parquet只核對保留的實際讀回CSV、檔案框架與digest，沒有在這次獨審重新解碼二進位。[獨立核對說明](../reviews/portable-artifact-review-20261025.md)保留方法與限制。

命令來源校正：舊`license-code-review.json`及早期研究文字曾稱`-init /dev/null`；實際十份保存argv全為`-no-init`。該舊收據未納入本子集，精確命令以[runlogs](runlogs/)為準。原始CSV、SQL、程式及結果未為了這次正式建檔而重寫。
