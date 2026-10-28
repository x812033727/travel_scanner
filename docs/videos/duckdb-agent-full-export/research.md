# DuckDB 2.0 agent模式：來源、實物與資訊增益

研究與建檔日：2026-10-25 UTC。本片採推薦A，以同一份原創配送CSV交出完整跟進清單；不是DuckDB產品巡禮、AI模型基準或真實客戶事件。完整歷史研究原文保留在[研究快照](planning/source-research-20261025.md)及[企劃快照](planning/source-brief-20261025.md)；那些原文中的「尚未建task／後臺」是當時研究階段狀態，當前狀態以[production-start.md](production-start.md)為準。

## 官方消息與新舊能力

| 主張 | 可核對官方來源 | 本片採用範圍 |
| --- | --- | --- |
| 10月9日已介紹agent模式 | [agent-mode文章](https://duckdb.org/2026/10/09/agent-mode.html) | 不把10月21日誤寫成首次介紹這個想法。 |
| 10月21日正式2.0／非prerelease | [公告](https://duckdb.org/2026/10/21/announcing-duckdb-200)、[v2.0.0 release](https://github.com/duckdb/duckdb/releases/tag/v2.0.0) | release時間`2026-10-21T12:49:12Z`；本地實跑版本`v2.0.0 (Cyanoptera) d54cbbe3df`。 |
| LTS至少到2027年10月 | 同一2.0官方公告 | 支援承諾屬CITED，不是實測；不因LTS而推薦所有現有工作立即升級。 |
| 新agent印法：Markdown、明確省略資訊、結果hash、JSON錯誤 | agent文章、[CLI agent文件](https://duckdb.org/docs/2.0/clients/cli/agent_mode.html)、[固定版本shell.cpp](https://github.com/duckdb/duckdb/blob/v2.0.0/tools/shell/shell.cpp) | 本輪真正RUN的是同版2.0兩模式，不是2.0對舊版的速度或成本比較。 |
| 新舊儲存格式相容條件 | [migration文件](https://duckdb.org/docs/2.0/operations_manual/migration.html) | 本輪只用`:memory:`和新輸出；未測現有資料庫遷移／回滾。 |
| CLI為MIT | [固定v2.0.0 LICENSE](https://github.com/duckdb/duckdb/blob/v2.0.0/LICENSE)、[保存的MIT](data/sources/duckdb-license.raw) | 原創fixture／SQL／報告另按CC0；不把官方原文重新授權。 |

原研究在同日以正常editorial UA取得官方HTTP200收據，見[data/sources](data/sources/)；正式建檔未重複下載。CSV讀取、SQL篩選／分組、COPY和Parquet匯出是既有能力。正文不報官方特定TPC-H的59%輸出token，亦不把本地bytes換算成普遍token／美元節省。版本／相容文件在正式寫稿或發布日改變時須重新查核。

## 已實際保存的同一任務

[輸入](data/input/parcels.csv)有1,200筆原創虛構紀錄。已送達960、在途240；承諾3天，在途實際天數為空值。完整predicate為`status = 'delivered' AND actual_days > promised_days`，五個交付欄位與排序見[完整SQL](data/sql/03-followup.sql)。在途不是已送達延遲，不把空值當零。

| 實際動作 | 本次觀察 | 邊界 |
| --- | --- | --- |
| 同一SELECT，明確切`-no-agent`／`-agent` | stdout 4,232／1,664 UTF-8 bytes；輸入預覽只印前20＋後20，明示省略1,160、總數1,200 | 一般模式也有40 shown；顯示省略不等於資料遺失或匯出少列。未測任何模型是否漏看。 |
| 作者故意寫`actual_day` | 兩種模式均失敗；agent startup文字後的一行JSON可解析，提示`actual_days` | 不冒稱AI失誤或DuckDB輸出壞JSON；consumer須辨識JSON行。 |
| 相同規則完整匯出 | [CSV](data/output/late-followup.csv)480筆，R2／R3各240；[Parquet](data/output/late-followup.parquet)3,067 bytes | 480是篩選交付，不是1,200筆輸入的預覽總數。 |
| 額外明確改需求，`>`改成`>=` | [另檔720筆](data/variant/output/due-or-late.csv)，其中240筆`days_late=0`；原480不覆寫 | 是「剛好準時或晚到」，不包括提前2天，也不是所有一般意義的準時；[變式核對](reviews/variant-artifact-review-20261025.md)逐欄及排序相符。 |
| 獨立標準函式庫重新計算 | 480筆排序與全部欄位相符；CSV及[保留Parquet讀回](data/output/parquet-readback.csv)均7,252 bytes，SHA相同 | 本次獨審未重新解碼Parquet；CLI原始讀回證據與stdout／argv保存，不把框架／hash檢查誇成新的引擎執行。 |
| 反序agent輸出 | footer結果hash仍為`f4d54c52b655fb12` | 此hash不依列順序，不是檔案SHA256、排序或業務正確性證書。 |
| [原創HTML](data/output/followup-report.html) | 樣本前8＋後4列，連到完整檔、SQL與結果 | 本地自寫報告，非產品操作截圖；不把樣本當完整480筆。 |

原研究CLI RUN集中在2026-10-25 22:30:17–22:30:20 UTC，精確命令、工具版本、時間、stdout／stderr及exit code見[data/runlogs](data/runlogs/)與[data/results.json](data/results.json)。正式建檔只複製與靜態核對，不重跑DuckDB或更新舊收據。全部十份保存argv用`-no-init`；早期研究／`license-code-review.json`的`-init /dev/null`文字與日誌不符，正式採日誌，該舊review未納入資料包。

獨立CSV核對：[方法與hash](reviews/portable-artifact-review-20261025.md)。本子集只有小型輸入、程式、SQL、完整交付檔、日誌、MIT與HTTP來源收據；不附官方大包／CLI、外站全文、PNG／ZIP或PDF。新的[data/manifest.json](data/manifest.json)只列實際附上的檔案。

## 六則海外參考：只觀察文字

2026-10-25讀到的第三方公開metadata快照，並非YouTube live API；未看片、未量剪點／音效、CTR／留存或精確片長。五個頻道、六則影片，不作raw views排名或因果推論。

| 影片 | 當時顯示上傳日／views | 本片原創設定 |
| --- | --- | --- |
| [Baig Academy：Claude Cowork AI Analyst](https://www.youtube.com/watch?v=JhkPKg6z-Cg) | 10/2／332 | 只借同一資料任務做到交付的結構，不冒稱操作Cowork。 |
| [Lore So What：Being a Data Analyst…](https://www.youtube.com/watch?v=dGUXygMCBv8) | 10/15／16,949 | 先定義已送達延遲；不借未核實的5倍錯誤故事。 |
| [Karina：Brutal Truth…](https://www.youtube.com/watch?v=TUwwD6OuzkU) | 10/16／5,376 | 完整predicate先於函數清單。 |
| [El Tío Tech：Excel＋IA Clase 1](https://www.youtube.com/watch?v=yoTqfZ7yUoI) | 10/19／19,653 | 完整命令和實際核對；不採幾秒／免費承諾。 |
| [El Tío Tech：Clase 3](https://www.youtube.com/watch?v=OiHNzp1jtVc) | 10/22／4,159 | 路線摘要回到全檔；不說分組是2.0新能力。 |
| [Josh Dev PH：Data Engineering Lab](https://www.youtube.com/watch?v=u_ZnAqb45c8) | 10/2／138 | 縮成單一本地CLI和fixture，不搭大型服務。 |

原始metadata網址、訂閱快照和觀察限制見[文字快照](planning/youtube-metadata-snapshots.json)。全部映射是本片編輯決定，沒有聲稱某手法造成高views。

## 查重與下一步

本次補查四個既有worktree、五條local branch、231個remote heads、30個open PR全文、open／done任務及base／origin/main，沒有同題；[具體相鄰範圍](reviews/collision-inventory-20261025.md)列出PDF四頁簡報、ForTy、Claude255及其他資料題。正常VideoTool route以`limit=200,before`分頁讀完423項，登記前再次核對為361長片／62Shorts，沒有DuckDB／full-export／跟進清單匹配；實際窗口和後臺登記見[production-start.md](production-start.md)。不是全站未來沒有重複的承諾。

下一步由協調代理接同一份資料與推薦A完成正式腳本、來源主張核對、原生敘事與聽眾審稿，再進TTS／音檢、卡片／成片QA和八語交付。這些關卡在本階段均未假造分數、核准或媒體完成狀態。
