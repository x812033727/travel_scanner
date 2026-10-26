# 第五支AI／科技時事企劃草稿：看懂省略標記，交出完整跟進清單

狀態：**scratch正式brief草稿，推薦A；未送Jev、未正式採用／登記episode或task、未操作後臺、未製作配音／成片。** 研究日2026-10-25 UTC。第四片已進實際製作，本稿只是下一題準備，不取代前三片／第四片的未完成工作。root可依既有委派採用推薦並送正常關卡，不再為例行選題問使用者；本稿不假造選題分數、介面核准或製作啟動。

推薦片名方向：**「表格只顯示40列？用DuckDB 2.0交出完整跟進清單」**。AI／科技時事解說，主角是一份原創虛構配送資料與其完整跟進檔。新版agent模式已在本機RUN；沒有登入／測試Claude Cowork等AI產品，沒有另呼叫模型，也不把SQL執行說成已測AI推理。縮圖可從「還有省略列」或「拿到完整檔」發展，不能寫「AI漏看1160筆」「省59%費用」等未測結論。

繁中主片，slides／paper／ai-news，目標8–12分鐘；**正文實際音長至少8分鐘**，不靠片頭片尾、靜音、重複警告或慢播補時。正式旁白先以約2200–2600中文spoken units起稿，依自然TTS量測與內容調整；估秒不算達標。CC可關閉、不燒錄，沿有效頻道聲音。預設加en／ja／ko／es／pt／id／vi／th八語metadata、七章、縮圖文字、CC與配音，各語交可下載M4A；不能把八語文字稱八語媒體完成。

本輪只寫`fifth-topic-research.md`、本brief及`fifth-demo/`，不改repo／task／後臺／系統／正式站、不付費、不用帳號／秘鑰、不安裝大型服務或模型、不下載他人整片、不spawn、不碰現有影片source或媒體。後續正式採用由root沿正常直接工具流程持續完成，據實報告每步產物。

## 觀眾、主問題與查重

會讓AI協助讀CSV／做小報表的一般工作者與科技觀眾，對「AI操作資料工具」有興趣，但不想從安裝資料庫服務學起。懂表格有列、有欄就能跟上；SQL是本例完整可照寫的規則，不做函數大全、寫程式課或資料工程服務導覽。

主問題：**「螢幕只印了一部分，我怎麼確認看到的是預覽，並交出真正完整、條件正確的跟進名單？」** 一個任務走到底：同一份原創1,200筆虛構配送紀錄→切換兩種輸出→讀明確省略提示→看欄位與修正規則→完整480筆CSV／Parquet→可核對報告。沒有真公司、客戶、個資或真實AI失敗事件。

查重已唯讀檢查四個本地repo的全部`docs/videos/**/video.json`，160個不同slug／title組合；搜尋tasks/open與done、讀當前30個open PR題名／body，證據存`fifth-demo/local-topic-inventory.json`及`fifth-openprs.json`。未見同題DuckDB片。PR1852另排PDF報價比較，第四片是PDF到四頁簡報；本題用配送CSV，不碰PDF／金額加總。既有token／context成本、活動資料夾和Gemini報表內容有相鄰概念，本片以新版CLI輸出契約和完整跟進交付區隔。未查後臺或所有未推送分支，正式登記時root補正常查重，不宣稱全站絕無重複。

## 觀眾看完能做到的三件事

- **切換新模式，分清預覽與完整結果。** 能照寫`-agent`／`-no-agent`，讀本次「前20＋後20／1200列、1160省略」；知道省略的是列印內容，不是查詢或儲存真的少資料。證據為同一2.0二進位、同一SELECT的兩份完整stdout；舊的人類模式也有40 shown提示，不捏造只有新模式才會告知。
- **用欄位與完整條件拿到正確跟進單。** 能先看欄位，再將「已送達且實際天數大於承諾天數」寫成完整SQL，選出五個交付欄、按parcel_id升冪；知道在途空值不等於零天或已送達延遲。故意少寫一個s的欄位例子用於讀懂JSON錯誤及修正，不冒充AI犯錯。證據為實際SQL、兩模式錯誤和成功結果。
- **交出全量檔，而不只貼螢幕截圖。** 能用COPY留下完整480筆CSV和同內容Parquet，讀回核對筆數與逐列內容；把小摘要／HTML報告連到完整檔和SQL。證據為實際可下載文件、獨立標準函式庫oracle、Parquet往返及全檔SHA。結果hash是輔助辨識，不替代條件查核。

三項都有能照做的輸入、動作和實物，不以「注意風險」「知道一個新名詞」代替能力。主要篇幅放在完成跟進清單，不展開AI職涯預測、模型排行或通用安全清單。

## 站主觀點

套用立場：**2、3、4、6、7**。已讀root於2026-10-25T18:55:29.788Z正常工具GET留下的`formal-context.json`有效`channel_stance`，不是HANDS-OFF草稿。

第2點官方原文優先：發表日、LTS與相容條件採當天官方頁；第3點數字歸屬：官方TPC-H實驗、第三方YT快照與本地stdout bytes分開；第4點點開來源核對：版本、套件SHA、SQL、輸出和本片資料都可追查；第6點實測誠實：只有本地CLI是RUN，產品／模型推理未測，作者故意錯字不說成真事故；第7點可做動作：交一份完整跟進清單與可重用規則。

擬議觀點：「我想拿到能交出去的完整名單，而不是把螢幕印出的幾列當成全部。新版輸出可以讓省略和錯誤更明確；條件怎麼寫、完整檔裡有什麼，仍要自己核對。」由本次RUN支持，沒有宣稱agent模式保證AI不再漏看或一定省錢。

可用「我」限本次事實，例如「我讓同一條查詢切換兩種模式」「我故意少寫了一個s」「我把完整檔再讀回來核對」。不能編成站主物流／分析師工作經驗、客戶事故、已付費或用過Cowork、AI曾漏掉某客戶、長期使用習慣。

## 一個任務的來源、版本與實物

官方新聞：[10月9日agent模式介紹](https://duckdb.org/2026/10/09/agent-mode.html)；[10月21日2.0正式公告](https://duckdb.org/2026/10/21/announcing-duckdb-200)；[正式release](https://github.com/duckdb/duckdb/releases/tag/v2.0.0)，`published_at=2026-10-21T12:49:12Z`、非prerelease。**模式10/9已介紹，10/21隨2.0正式版提供；CSV／SQL／COPY／Parquet是既有能力。** 不說2.0第一次可以讀CSV、做篩選或匯出。

本輪先讀MIT及固定v2.0.0的CLI相關程式碼，再下載24,424,037 bytes官方Linux amd64壓縮包，與release digest相符。SHA256：`c6507206baf7793c6013dbd82368469a45f20dc0e17a6f92f204602f652ed2bc`；實際版本`v2.0.0 (Cyanoptera) d54cbbe3df`。執行檔只解到scratch，無系統安裝或服務啟動。精確命令／時間／stdout／stderr在`runlogs/`；主要RUN為2026-10-25 22:30:17–22:30:20 UTC，非影片音長或效能基準。

| 例子進度 | 具體可見結果 | 不得混用的範圍 |
|---|---|---|
| 來源CSV預覽 | 全表1200筆；兩模式都只呈前後40列；agent輸出明示1160 omitted | 40是輸入全表預覽顯示列數，**不是跟進檔只有40筆，也不是1200只剩40筆**。 |
| 同一SELECT切模式 | 人類stdout4232 bytes、agent1664 bytes；同版2.0，查詢資料相同 | 這是列印bytes，不是token／美元、執行效能或模型正確率。不要拿比例比官方59%。 |
| 作者刻意拼錯actual_day | 兩模式均失敗；agent error行是合法JSON，帶COLUMN_NOT_FOUND與候選actual_days | 不是AI真實錯誤，也不是只有agent能查到欄位問題。 |
| 正確定義與匯出 | 960已送達、240在途；已送達延遲480筆，R2／R3各240 | 這是同一虛構fixture，不是真公司／公共統計。影片不要把輸入預覽1200與篩選輸出480混成同一查詢。 |
| 完整檔驗證 | CSV逐列等於獨立Python oracle；Parquet讀回CSV逐列相同 | 檢查本例內容一致，不代表任意查詢／軟體／AI均正確。 |

主交付物：`fifth-demo/output/late-followup.csv`、`late-followup.parquet`、`followup-report.html`；完整欄位／型別／篩選／COPY在`sql/03-followup.sql`。原創資料、報告與自寫程式可按CC0-1.0重用，DuckDB按MIT，官方頁原文仍屬原作者。練習包只附小型輸入、SQL、程式、輸出、必要授權和證據，不把大型CLI或官方網站全文捆綁成自己的作品。正式公開資料URL由root落地後GET核實，本稿不造下載頁。

## 三個cold hooks（原創計畫值，非已測留存）

**A／推薦：一份完整名單該怎麼拿到。**

> 同一份表格，螢幕只印前後四十列。旁邊卻寫著，還有一千一百六十列被省略。DuckDB二點零把這種提示改得更明白。我先分清預覽，再寫條件、匯出完整檔。跟著這份虛構配送紀錄，交出一份真的能核對的跟進清單。

**B／模式對照：變的是資料還是交付方式。**

> 這條查詢沒有換，表格的印法卻換了。十月二十一日推出的DuckDB二點零，多了給AI代理讀取的輸出模式。一個故意少寫的字母，還會回成結構化錯誤。我用同一份配送資料，切模式、改欄位、存完整檔。最後看清楚，新模式到底改了哪一層。

**C／先看實物：先有跟進檔，再解釋怎麼來。**

> 這個檔案裡，有四百八十筆需要跟進的配送紀錄。它們來自一份原創練習表，不是實際客戶資料。DuckDB二點零的新模式，讓工具回覆更適合代理讀取。我把預覽、查詢和匯出分開核對。你也能照同一條規則，交出完整清單和可讀報告。

A最早提出觀眾會遇到的輸出問題，並立即走向正向成果；B較偏技術，C先揭結果但新特性進入較慢。片中不演出不存在的模型誤判，不用「AI只看到40筆」當已觀察結論；若正式標題採疑問句，前30秒要說明本次是CLI輸出樣本，未測特定模型是否誤讀。

## 完整可照寫的指令與規則

本片不教安裝大型服務。練習包README指定本次Linux amd64、官方2.0 CLI與SHA，觀眾須已有相符工具；其他平台按官方安裝頁選擇，不假稱跨平台已測。命令用既有檔案和完整SQL，原始資料均留在本地。本輪精確RUN用`-c`傳完整SQL，以下`-f`是同一CLI列明的讀檔方式，可供簡潔照寫；不能假稱兩種呼叫都各完成了獨立效能評測。

```sh
python -B run_demo.py
./bin/duckdb -no-init -no-agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/03-followup.sql
```

旁白完整讀兩條模式命令的有意義部分：`-no-init`略過預設初始化檔、`-agent`／`-no-agent`明確選擇印法、`:memory:`本次臨時資料庫、`-f`讀本片完整SQL檔；不把路徑／套件SHA逐字唸滿一章。不要要求改HOME／全域PATH、貼API key或打開伺服器。

完整建表前提（片中分卡可讀，下載檔全文保留；型別未省略）：

```sql
CREATE TABLE parcels AS
SELECT * FROM read_csv('input/parcels.csv',
  columns={'parcel_id':'VARCHAR', 'route':'VARCHAR',
           'promised_days':'INTEGER', 'status':'VARCHAR',
           'actual_days':'INTEGER'}, header=true);
DESCRIBE parcels;
```

跟進規則要整段口述，讓只聽配音／外語CC的觀眾也能照做：

```sql
SELECT parcel_id, route, promised_days, actual_days,
       actual_days - promised_days AS days_late
FROM parcels
WHERE status = 'delivered'
  AND actual_days > promised_days
ORDER BY parcel_id;
```

口語：「只取已送達，而且實際天數大於承諾天數的紀錄。交出包裹代號、路線、承諾天數、實際天數與晚了幾天，依包裹代號升冪排列。」用一筆實際4天／承諾3天→晚1天、另一筆在途／空值→不進已送達清單，說清兩個條件怎麼落到同一份資料；不把空值自動當零，亦不把規律fixture當現實分布。

完整COPY在下載的`03-followup.sql`，畫面可展開一種，再把同一SELECT逐字重用到另一格式，不能用`...`省略實際篩選／排序：

```sql
COPY (
  SELECT parcel_id, route, promised_days, actual_days,
         actual_days - promised_days AS days_late
  FROM parcels
  WHERE status = 'delivered'
    AND actual_days > promised_days
  ORDER BY parcel_id
) TO 'output/late-followup.csv' (HEADER, DELIMITER ',');
```

Parquet同一SELECT、五欄與排序不變，輸出行改為`TO 'output/late-followup.parquet' (FORMAT PARQUET);`；實際檔中有兩個完整COPY，沒有省算步或靠觀眾補條件。下載HTML只展示前8＋後4列並標樣本，完整檔才有480列。Parquet是交付格式選項，不在本片教內部欄式儲存或宣稱省空間。

可提供給觀眾的完整AI協助提示，為本次原創教學文字，**未另貼進任何被評測產品**：

> 只用這份原創配送CSV。先列欄位與型別，找出status是delivered、而且actual_days大於promised_days的紀錄；在途空值不要當已送達。選parcel_id、route、promised_days、actual_days，再算days_late，依parcel_id升冪。用DuckDB二點零的agent模式回報查詢；先分清螢幕預覽與總筆數，再把完整結果匯出CSV和Parquet。保留實際錯誤和完整SQL，讀回檔案核對；沒有執行的步驟不要寫成功，不連服務、不安裝擴充，也不需要任何帳號或秘鑰。

提示若出現，必須完整口述並分成可讀連續卡，說明欄附可複製全文；不能只說「prompt在下面」。本輪由本對話助理寫SQL／呼叫本機工具，沒有獨立產品前後測、成功率或模型版本評比。

## JSON輸出契約：精確處理，不製造壞JSON故事

作者故意少寫s，令`actual_day`不等於存在的`actual_days`。人類模式回文字錯誤；agent模式stderr本次有**startup說明文字＋一行合法JSON物件**，JSON帶`exception_type`、`error_subtype`、`name`和候選欄位。修正仍要對回DESCRIBE與需求，不把候選建議當業務真相。

實際解析採「辨識JSON行，再解析那個物件」。若consumer預期整條stderr只能是一個JSON物件，就與這個混合stream契約不一致；這不表示錯誤JSON本身壞掉，也不是DuckDB輸出無效JSON。本輪沒有聲稱某個真實第三方consumer因此故障。正式稿如不教consumer程式，只讀合法JSON行中的欄位和修正即可，這個界線一句說清，不另擴一章故障清單。

## 大綱A（推薦）：先辨識省略，再完成同一跟進名單

| 章／估秒 | 同一任務的進度與兩個以上可做動作 | 主要畫面／收尾問題 |
|---|---|---|
| 1. 表格後面還有省略列／24 | 呈同一原創CSV的真實預覽，圈40 shown／1160 omitted；承諾交完整跟進檔 | 真實兩模式輸出重排成可讀中文卡，保留原輸出可查；接「這只是少印，還是資料真的少了？」 |
| 2. 切換模式，先知道自己看的是什麼／105 | 寫兩條模式命令；對同版2.0的粗框／Markdown，讀總列數、省略標記和完整輸出位置 | `terminal`／`compare`，螢幕只取必要前後列；明說查詢／儲存未因省略少資料。接「要交的名單，該怎麼寫條件？」 |
| 3. 把配送問題寫成完整規則／110 | 讀五欄／型別；完整口述SELECT／WHERE／排序；在途空值與已送達延遲用本例各算一筆 | 原創欄位卡→完整SQL→一筆晚1天、一筆在途，讓觀眾看到每條條件的作用。接「欄位少一個字，工具怎麼回答？」 |
| 4. 讀錯誤、改欄位，再把全量存下來／125 | 明示作者故意actual_day錯字；讀合法JSON錯誤行、修成actual_days；完整COPY同一條件至CSV／Parquet | `compare`人類／JSON、`code`修正與COPY；startup混合stream契約只說一次。接「畫面只顯示樣本，完整檔怎麼驗？」 |
| 5. 打開完整清單，回查同一份結果／115 | 讀480筆CSV；分組路線摘要對回全檔；Parquet再讀回CSV逐列一致；看可下載HTML連結與原始SQL | 真實CSV頭尾／完整檔計數、HTML與驗證卡；hash只作輔助，命令與完整AI協助提示可分卡回收。接「為了這個新模式，現有工作要立刻升級嗎？」 |
| 6. 用得上新模式，也要選對升級範圍／65 | 一張卡分新agent模式／既有CSV-SQL-COPY；交代10/9介紹／10/21正式、LTS至少2027/10、既有庫相容文件 | 唯一集中說適用界線：同版兩模式，未測模型／成本／升級，先在新scratch任務試；不逐項巡禮server等沒測功能。 |
| 7. 下次交完整檔，也留完整規則／25 | 回答開場省略的是印出的列；觀眾用同一命令留全量檔／SQL再核對 | `outro`三句：回答、留言問「你最常交預覽還是完整檔？」、有理由訂閱，不預告下一片。 |

合計569秒，約9分29秒；**正文五章520秒，約8分40秒**。是計畫值，不是配音驗收；正式稿約2200–2600spoken units起步，實際TTS/body timeline≥480秒才達標。若不足，補完整指令、欄位／條件兩筆推導、COPY和讀回交付，不重報跑幾次／SHA／警告，不延長空白或另找無關案例。

三條冷開場預告迴圈可定為：省略列去哪裡→第2章；欄位不一致怎麼改→第4章；完整檔怎麼確認→第5章。每60–90秒以觀眾下一個疑問接本例立即推進，之後正式稿另存loops並按全文審。這是原創節奏設計，未聲稱從YT測得留存。

## 備選大綱B／C（同一主角與產物，不另造實驗）

B「從一份可交付清單倒推」：開場實物24秒→寫明跟進規則115→完整輸入／欄位100→切兩模式與省略110→錯字修正／COPY／讀回135→新聞與升級界線65→收尾25。合計574秒，正文525秒。較適合已做報表的人，但新模式出現較晚，非首選。

C「先看合法結構化錯誤，再改出名單」：開場同查詢兩種錯誤24秒→對欄位與consumer契約105→完整篩選條件110→模式與預覽110→全量匯出／HTML／讀回130→新聞與升級65→收尾25。合計569秒，正文520秒。JSON比資料任務更早，對一般觀眾負擔較高，非首選；不能為戲劇效果偽造產品消費端失敗。

## 六筆海外文字參考與製作映射

完整標題／日期／觀看／訂閱／第三方來源在研究稿和`youtube-metadata-snapshots.json`。本輪沒看片、沒有精確片長，未量鏡位／剪點／音效／CTR／留存；公開中繼頁不是YT live API。五個頻道六則內容跨7–30天，兩則同頻道，不能只按raw views排行或推因果。

| 已讀文字參考 | 快照與已觀察 | 本片原創設定／驗收 |
|---|---|---|
| [Baig Academy：Claude Cowork AI Analyst](https://www.youtube.com/watch?v=JhkPKg6z-Cg) | 10/2、332 views；描述先定指標→local DuckDB→報告／排程，未重現產品 | 只留一個資料任務到完整交付；實際CSV／SQL／HTML可核對，不冒稱Cowork操作。 |
| [Lore So What：Being a Data Analyst…](https://www.youtube.com/watch?v=dGUXygMCBv8) | 10/15、16,949；描述談SQL與業務語意，5倍錯誤故事未核 | 先完整定義delivered-late；不借故事或職涯斷言。 |
| [Karina：Brutal Truth…](https://www.youtube.com/watch?v=TUwwD6OuzkU) | 10/16、5,376；描述／章節先問題、邏輯後程式 | 用一條predicate完成名單，觀眾能照讀條件，無須背函數。 |
| [El Tío Tech：Excel＋IA Clase1](https://www.youtube.com/watch?v=yoTqfZ7yUoI) | 10/19、19,653；描述prompt／複製／檢查，速度未測 | 完整可照寫命令和條件逐字呈現；不採幾秒／免費承諾。 |
| [El Tío Tech：Clase3](https://www.youtube.com/watch?v=OiHNzp1jtVc) | 10/22、4,159；描述分組／篩選 | 路線摘要對回完整清單，顯示摘要與全檔的關係，不說分組是新特性。 |
| [Josh Dev PH：Data Engineering Lab](https://www.youtube.com/watch?v=u_ZnAqb45c8) | 10/2、138；描述含DuckDB的大型lakehouse服務實驗 | 反向取捨為一個本機CLI，不裝服務；所有新增輸入／產物留scratch。 |

未看過的片段不描述「每幾秒切卡」、音效或演示品質。推薦A由本輪RUN、新版資訊增益和可完成任務支持，不把某參考高views當製作成功保證。

## 有界限制與後續門檻

研究保存正常UA官方GET與每host至少1.1秒開始間隔；最多5次web呼叫已用完。版本、MIT、套件digest與相關CLI程式先讀後跑；沒有下載>50MB模型／資料、大型服務或私人資料，沒有安裝到系統。HTML已用現有Chromium的set_content直接渲染自寫內容並截圖，13個表格列含標頭、無水平溢出，已實際看過全頁；這不是產品截圖或私人瀏覽器。先前內建browser不存在、file導覽受既有政策限制的原始狀態保留，沒有下載browser或改政策。

**一段集中界線：** 新agent模式整理CLI交給讀取者的輸出，不執行AI模型、不確保查詢／業務語意正確；40列是1200筆輸入預覽、480是篩選後交付；JSON行合法，consumer若預期整stream單一JSON是契約不合；同版兩模式不是跨版效能基準，bytes不等於token／費用。LTS與新儲存格式相容條件依官方，現有資料庫未測，不把新模式當全面升級理由。

正式落地後root再正常登記、送Jev、保存採用理由與關卡實錄。先核輸入／輸出全SHA與claims，再寫稿／獨立事實核對與聽眾審稿；語音實測正文≥8分鐘，樣卡實際看完、全部CC／音訊按最新hash檢查。官方動態來源正式寫稿日重核，別把本輪快照稱發布日狀態。只要未真正生成、上傳或通過，便不報成完成；發布由站主操作。
