# 第五題有界研究：DuckDB 2.0，把資料預覽變成可交付的完整清單

研究日2026-10-25 UTC，開始22:23:07。推薦A：以DuckDB 2.0 CLI的**agent模式**作近期技術入口，跟著同一份原創虛構配送資料，最後交出完整CSV／Parquet跟進清單。新版CLI已實際RUN，套件、授權、相關程式碼、精確指令與輸出均保留；沒有登入產品、呼叫AI模型、測Claude Cowork，亦未對生產資料庫升級。這比只引用需帳號產品的功能介紹更接近可做、可核對的下一題。

目前僅研究與scratch企劃，未送Jev、未建立episode／task／後臺項目，未生成影片或配音，不取代正在製作的前三片／第四片。所有新檔只在本研究、`fifth-topic-brief.md`與`fifth-demo/`。本輪使用5次web工具呼叫（前4次搜尋、末次開6頁metadata），不再擴搜尋；官方GET為正常editorial UA、每次請求開始間隔至少1.1秒，無帳號／API秘鑰或私人憑證。

## 查重與三個候選

唯讀掃描`/workspace/travel_scanner`及三個`/workspace/work/travel-scanner-*`本地repo的全部`docs/videos/**/video.json`，取得160個不同slug／title組合；另查tasks/open與done的題名／關鍵字及當前30個open PR題名和body。存`fifth-demo/local-topic-inventory.json`、`fifth-openprs.json`。沒有同題DuckDB／MarkItDown／Mermaid正式片；相鄰內容與排隊工作仍須避開：

- DNS隔離、ForTy森林像素、Claude255與Notebook四頁大綱流程已在製作／交付；第五題不延伸其中例子。
- PR1852另列接續PDF報價比較，故本輪不採PDF報價／金額加總任務；MarkItDown亦與目前PDF流程較近。
- 既有`ai-terms-prompt-to-graph-engineering`講代理系統分層，`ai-term-token`／Claude context成本片講token；本題不能換皮成「AI少印幾個字就省多少錢」。
- 既有Claude入門活動資料夾、Gemini試算表報表文章／任務有資料處理相鄰內容；本題主角採配送跟進清單，核心是新版CLI的結果呈現／交付，不是活動報名、報價或表格清理大全。

沒有查後臺作品或所有未推送分支內容，本輪明確禁止後臺操作；因此不宣稱全站絕無重複。正式採用前root可沿正常登記流程完成其餘查重。

| 候選 | 當天GET確認的官方消息／授權 | 可以實作的成果 | 判斷 |
|---|---|---|---|
| A：DuckDB2.0 CLI agent模式 | [正式公告](https://duckdb.org/2026/10/21/announcing-duckdb-200)、[release](https://github.com/duckdb/duckdb/releases/tag/v2.0.0)為10/21；[agent模式介紹](https://duckdb.org/2026/10/09/agent-mode.html)為10/9；MIT | 同一查詢的`-agent`／`-no-agent`輸出、明確截斷標記、JSON錯誤，再交完整CSV／Parquet | **推薦；新版已真正RUN**。agent模式不內建模型，也不代表本輪測過模型推理。 |
| B：Microsoft MarkItDown0.1.9 | [官方release](https://github.com/microsoft/markitdown/releases/tag/v0.1.9)，10/21 19:40:32Z；MIT | 小型Office檔轉Markdown，保留原文／輸出比對 | 近期開源更新成立，但本輪未執行；PDF／試算表處理與排隊題材相鄰。版本重點含讀取／串流可靠性和回歸測試，不能說首次提供Office轉換。 |
| C：Mermaid12.2.0 | [官方release](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.2.0)，10/13 08:32:53Z；MIT | 原創mindmap依階層深度著色、可修改SVG | 30天窗內備選；本輪未執行。新特性是opt-in `mindmap.colorBy: depth`，不能說第一次有mindmap或文字製圖。與既有graph概念／可修改動畫相鄰。 |

三者均已保存官方release API、原始程式授權和HTTP200收據；不是依搜尋摘要補日期。A正式release `published_at=2026-10-21T12:49:12Z`，非預覽版。公告稱2.0 LTS支援**至少到2027年10月**；沒有把支援承諾當已實測功能。agent模式10/9已介紹、10/21隨2.0正式版提供，不能說10/21才首次公開這個想法。

## 新版到底新增什麼，舊能力有哪些

本輪真正測的是2.0 CLI的新agent輸出：緊湊Markdown、明確省略列／總數提示、結果hash、stderr JSON錯誤。同一2.0二進位分別用`-agent`與`-no-agent`比較，**不是拿2.0對1.5做速度測試**。

CSV讀檔、SQL篩選／分組、CSV／Parquet匯出是既有能力，片中把它們當完成任務的工具，不包裝為2.0首創。官方另列伺服器、Quack、VARIANT、非同步I/O、triggers等，本輪沒跑，不用功能大全湊片長。

官方agent文章的實驗說其TPC-H條件下CLI回傳給模型的輸出token少59%，並進一步說總輸入只約少0.5%、未反映成總成本／時間節省。那是官方特定實驗，不是本輪結果；建議正文不報59%，避免把小型stdout差異換算成普遍省錢宣傳。實跑只記UTF-8 bytes，沒有量token、價格或模型正確率。

[2.0 migration文件](https://duckdb.org/docs/2.0/operations_manual/migration.html)說新預設儲存格式不能由2.0前版本讀取，而既有舊格式檔可由2.0讀寫並保留原儲存版本；多人／多版本共用檔須先確認相容性，也列出指定storage version的方法。此為CITED升級條件，本輪僅`:memory:`和新的輸出檔，**沒有測舊資料庫遷移／回滾**。CLI help亦保留相容參數，不能只因LTS就主張現有工作應立即升級。

## RUN：同一份配送清單，從預覽到完整交付

先讀MIT與固定v2.0.0的`tools/shell/shell.cpp`相關程式：初始化檔讀取、OpenDB、agent輸出及錯誤設定。完整engine未做安全審計。預設會找使用者`.duckdbrc`，因此本輪每次執行明確用`-no-init`（首次version檢視用`-init /dev/null`）。沒有server／connect／INSTALL命令，關閉自動安裝／載入擴充，只讀寫自己scratch內的檔案。

下載官方Linux amd64 CLI壓縮包，**24,424,037 bytes**，小於50MB，沒有模型或大型資料下載，沒有安裝到系統。套件SHA256：

`c6507206baf7793c6013dbd82368469a45f20dc0e17a6f92f204602f652ed2bc`

與正式release asset的`sha256:` digest一致；解出的執行檔77,526,584 bytes只在`fifth-demo/bin/`。實際`-version`輸出：`v2.0.0 (Cyanoptera) d54cbbe3df`。官方公告使用鳥種英文名，release／CLI用Latin代號，不把名稱寫法差異製造成版本衝突。套件核對、LICENSE與相關程式碼在`selected-package.json`、`package-check.json`、`license-code-review.json`及`sources/`。

單一主角是原創1,200筆虛構配送CSV，不是真業務、公部門資料或AI出錯事件。規則公開：每5個ID一筆在途；其餘已送達；承諾3天；已送達的實際天數為2＋ID除4餘數；在途實際天數留空。R1–R4是虛構路線碼，沒有客戶或個資。這種規律資料用於看懂輸入、條件與完整輸出，不拿來推論真實配送績效。原創fixture／報告／自寫程式以CC0-1.0提供，DuckDB另按MIT，官方頁文字另屬原作者。

任務：「請交出已送達，而且實際天數超過承諾天數的完整跟進清單。」不把仍在途當成已送達延遲。輸入、規則、欄位型別、結果及反向讀回均保存。

| 實際動作 | 觀察與成果 | 能證明／不能外推 |
|---|---|---|
| 同一`SELECT *`，同版切換`-no-agent`／`-agent` | 人類模式stdout4,232 bytes；agent模式1,664 bytes。後者明列「1160 rows omitted」及前20／後20，共1200列 | 是同一資料的呈現差異；一般模式本來也標40 shown，不能說舊模式從不提示截斷。沒有測哪個模型因此改善。 |
| 同一結果改反序輸出 | 兩個agent footer均為`f4d54c52b655fb12` | 此結果hash不依列順序；不是檔案SHA256、不是查詢正確性證書，不能用來證明排序相同。 |
| 作者刻意把`actual_days`寫成`actual_day` | 兩模式都正確失敗；agent stderr JSON可解析為`COLUMN_NOT_FOUND`，列候選欄位 | 展示新格式，不是AI真實失誤或只有agent能發現錯誤。 |
| `DESCRIBE`→正確條件→`COPY`完整匯出 | 960已送達、240在途；完整跟進480筆，R2／R3各240 | 完整CSV與獨立Python標準函式庫逐列相等；這是此虛構fixture，不是公共統計。 |
| 同一結果寫Parquet，再讀出CSV | 480筆逐列等於原CSV | 證明本次交付內容一致，不是新格式速度／壓縮基準。 |
| 原創HTML報告 | 可直接開啟，連到完整CSV／Parquet／SQL，樣本標前8＋後4 | 是本地原創交付頁，不是DuckDB／AI產品畫面。 |

JSON的輸出契約也要說清：本次agent的stderr先有一行startup說明，再有一行合法JSON錯誤物件。實際consumer是取JSON行後解析；若預期「整條stderr是一個JSON物件」，那是consumer預期與混合文字stream不一致，不能稱DuckDB產生壞JSON。兩個模式都能報錯，新模式改的是結構化表示；本輪沒有構造或觀察真實第三方consumer故障。

主要執行2026-10-25 22:30:17–22:30:20 UTC；精確每條argv、時間、stdout／stderr與exit code在`runlogs/`，不是估計時長。本輪有意限制小型資料，沒有試長查詢中止、百萬列cost估計、伺服器模式、雲端I/O或現有資料庫相容性。

HTML已用現有Chromium直接set_content渲染自寫內容，沒有外站或產品導覽；13個表格列含標頭、無水平溢出，實際打開完整截圖確認樣本／完整檔標示和程式區塊可見。最先嘗試的內建browser不存在、file導覽被現有政策擋下，未下載browser／改政策／用私人profile；實際方法存`report-render-check.json`。

可直接下載的主成果在`fifth-demo/output/`：`late-followup.csv`、`late-followup.parquet`及`followup-report.html`。完整重跑為`python -B run_demo.py`，只改本scratch；完整SQL在`sql/`。篩選條件與CSV／Parquet COPY沒有省略前置建表／型別。目錄另提供不含大型執行檔的可攜練習包，正常取得相符CLI後即可照README操作；這是scratch產物，沒有假造正式公開下載網址。

## 六個近期國外YT文字快照

原始watch連結與開啟的第三方文字頁均記在`youtube-metadata-snapshots.json`、`fifth-web5.json`。以下為2026-10-25讀到的公開中繼頁顯示值，**不是YT live API**，crawl age不等於觀看數計數時刻。未下載全片、沒看影片或量剪輯、音效、鏡位、CTR／留存；全數精確片長未知，章節末時間不補成片長。用描述可知為長片相鄰教學／討論，未經播放驗證為Shorts。五個頻道，兩則落在7天內，其餘30天窗；不混成新2.0功能評測。

| 顯示標題／頻道 | 上傳日／觀看／訂閱快照 | 已觀察文字與本片原創映射 |
|---|---|---|
| [Claude Cowork으로 AI 분석가 만드는 방법 (노코드)](https://www.youtube.com/watch?v=JhkPKg6z-Cg)／Baig Academy | 10/2；332；630；[第三方頁](https://zolotube.com/watch?v=JhkPKg6z-Cg)，crawl today | 描述先定指標、建local DuckDB再做報表；鏡像標題韓語本地化，搜尋英語題名。借用「同一資料任務到交付」結構，不稱實測Cowork／排程。 |
| [Unfortunately, Being a Data Analyst Just Changed Forever](https://www.youtube.com/watch?v=dGUXygMCBv8)／Lore So What | 10/15；16,949；155K；[第三方頁](https://zolotube.com/watch?v=dGUXygMCBv8)，crawl last week | 描述區分SQL與業務語意，聲稱AI曾算高5倍，未重現。映射為先定已送達延遲，不借故事冒充我們事故或做職涯預測。 |
| [The Brutal Truth About Data Analytics in the AI Era (stop learning tools!)](https://www.youtube.com/watch?v=TUwwD6OuzkU)／Karina Data Scientist | 10/16；5,376；22.8K；[第三方頁](https://zolotube.com/watch?v=TUwwD6OuzkU)，crawl last week | 描述／章節先把問題寫清，再規劃邏輯與檢查。映射到一條完整predicate和全量清單，不教背SQL函數。 |
| [Curso de Excel + IA GRATIS: Crea Cualquier Fórmula en Segundos \| Clase 1](https://www.youtube.com/watch?v=yoTqfZ7yUoI)／El Tío Tech | 10/19；19,653；2.03M；[第三方頁](https://zolotube.com/watch?v=yoTqfZ7yUoI)，crawl today | 描述完整prompt、複製貼上並檢查。映射為完整指令與實際輸出；不採「免費／幾秒」承諾。 |
| [Curso de Excel + IA: Crea Tablas Dinámicas con IA \| Clase 3](https://www.youtube.com/watch?v=OiHNzp1jtVc)／El Tío Tech | 10/22；4,159；2.03M；[第三方頁](https://zolotube.com/watch?v=OiHNzp1jtVc)，crawl today | 描述分組／百分比／篩選。映射為路線小摘要對回完整清單，不把樞紐分析說成新功能。 |
| [EP03 - Lab: Fundamentals of Data Engineering - Analytics Solutions Bootcamp](https://www.youtube.com/watch?v=u_ZnAqb45c8)／Josh Dev PH | 10/2；138；899；[第三方頁](https://zolotube.com/watch?v=u_ZnAqb45c8)，crawl today | 描述DuckDB搭大型lakehouse／Docker服務。映射為本片刻意縮到單一CLI＋fixture，不重現整套或借效能。 |

觀看數／訂閱規模不同、只有單快照，不作raw views排行、速度或CTR推算。沒有證據說某手法造成高點閱；上表「映射」都是本片編輯決定，不是看片測量。推薦A來自已實作的新特性、可核對輸出和觀眾成果。

## 採用判斷與界線

建議正式企劃走「新版工具如何把結果交清楚」的單任務解說，不做SQL函數大全或AI職涯警告。觀眾可完成三件事：明確切換新模式並讀懂截斷；用欄位及條件修正查詢；拿到全量跟進檔並驗證預覽／CSV／Parquet的關係。完整指令、3個cold hooks和8–12分鐘同主角大綱在`fifth-topic-brief.md`。

可用第一人稱限本輪實跑，不編造站主職業或產品經驗。新模式不是AI模型、結果hash不是來源查核、輸出bytes不是token／費用；一般模式也有截斷提示。這些界線在正式片集中一段，主要篇幅用具體輸入、操作、前後輸出與交付。不宣稱靠新模式就保證AI不再漏看或查詢永遠正確。

研究充分到可選A，但沒有Jev分數、正式片名、註冊或媒體完成。本輪無新代理、無repo／task／後臺／系統設定變更、無付費／帳號／API秘鑰、無大型服務／模型安裝，未碰現有三四片source或媒體。root可依既有委派自主採用，無需再問站主例行選題。
