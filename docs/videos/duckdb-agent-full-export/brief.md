# 表格只顯示40列？用DuckDB 2.0交出完整跟進清單

## 觀眾

會用AI協助讀CSV、製作小報表的一般工作者；懂表格的列與欄即可。本片回答：「螢幕只印一部分，怎麼確認那是預覽，並交出條件正確的完整跟進名單？」主角只有同一份原創1,200筆虛構配送紀錄，從辨識預覽、定義已送達延遲，到留下完整CSV／Parquet和可讀報告。

採用AI／科技時事的教學卡片路線，目標8–12分鐘。既有推薦A已由協調代理依站主2026-10-25「依據你的推薦或jev選擇就好，不用問我」授權採用；這是編輯選擇，沒有Jev分數、伺服器核准或已完成媒體。本階段只研究、正式建檔與登記。後續依有效預設製作繁中及en／ja／ko／es／pt／id／vi／th的metadata、CC、配音，各語按真實收據交付。

## 觀眾看完能做到的事

- **切換CLI印法並讀懂預覽的邊界。** 完整寫出同版2.0的`-agent`／`-no-agent`命令，看同一查詢的前20＋後20列、總數1,200與省略1,160；分清列印省略和資料遺失。RUN：[兩種預覽及原始指令](data/runlogs/)、[本次結果](data/results.json)。一般模式也有40 shown提示，不說只有新模式才會告知。
- **編輯並執行跟進規則，而不是只重跑現成包。** 先讀五欄與型別，把「已送達，而且實際天數大於承諾天數」寫成完整SELECT、WHERE和排序；對照一筆已送達延遲與一筆在途空值。再把需求明確改成「剛好準時或晚到」，實際把`>`改為`>=`，另存720筆，辨認新增的240筆`days_late=0`，不把提前2天也算進去。故意少寫s的欄位錯誤則用於讀合法JSON行後修回。RUN：[原規則](data/sql/03-followup.sql)、[新需求原始SQL](data/variant/variant.sql)、[變式結果](data/variant/variant-results.json)、[刻意錯字](data/sql/02-intentional-typo.sql)；另附[可攜路徑SQL](data/variant/variant-portable.sql)，只調相對路徑、未在建檔時重新執行。後兩者是作者有意的需求變化／格式示範，不是觀察到AI犯錯；480原檔不覆寫。
- **交出並驗證完整檔。** 把相同五欄、條件和排序COPY成480筆CSV與Parquet，再讀回比對；用可讀HTML連到全檔和SQL。RUN：[完整CSV](data/output/late-followup.csv)、[Parquet](data/output/late-followup.parquet)、[保留的讀回CSV](data/output/parquet-readback.csv)、[報告](data/output/followup-report.html)。獨立標準函式庫重算確認逐列與CSV bytes一致；Parquet的實際讀回是原始CLI執行證據，本次獨審沒有重新解碼其二進位內容。

## 站主觀點

套用立場：2、3、4、6、7、8

「我想拿到能交出去的完整名單，而不是把螢幕印出的幾列當成全部。新版輸出讓省略和錯誤更明確；條件怎麼寫、完整檔裡有什麼，仍要自己核對。新版本不是既有工作立刻升級的理由。」立場文字已從本次正常VideoTool settings GET讀回，完整採用紀錄見[研究與製作起步紀錄](production-start.md)。

第一人稱只指2026-10-25這次原創程式、SQL與保存的本地RUN；不編造站主物流職業、客戶事故、長期產品習慣或付費經驗。

## 示範或實算

製作路線：教學卡片。`format: slides`；無`shot`、無付費AI插圖或模型實測。輸出與圖解使用原創資料和真實保存的stdout／stderr，不把本地HTML排版成產品操作截圖。

**同一份輸入與完整條件。** [parcels.csv](data/input/parcels.csv)有1,200筆：960已送達、240在途；承諾3天，在途`actual_days`為空值。這是規律的虛構fixture，不代表真實配送分布。規則及授權見[data/README.md](data/README.md)。交出`parcel_id`、`route`、`promised_days`、`actual_days`及`actual_days - promised_days AS days_late`，只取`status = 'delivered' AND actual_days > promised_days`，依`parcel_id`升冪。兩種完整COPY均在SQL內，畫面和旁白不以`...`省略條件或排序。

**不用這個方法。** 同版DuckDB 2.0的人類模式仍可做相同查詢及完整匯出；完整CSV不是agent模式新能力。對照RUN是同一二進位、同一輸入、同一SELECT的`-no-agent`與`-agent`：本次stdout為4,232／1,664 UTF-8 bytes，兩種模式都只顯示40列；新模式改的是適合代理讀取的Markdown、明確省略資訊和結構化錯誤。這不是跨版本速度、token、費用或模型正確率比較。觀眾需要機器讀取輸出時才選agent印法；一般閱讀或既有穩定工作不因本片而必須升級。

**信任及前提在操作前。** 官方v2.0.0 Linux amd64 CLI已在原研究scratch執行，未安裝到系統、未啟動服務、未連產品帳號或生產資料；原始套件digest、版本、MIT及HTTP來源收據保留。正式episode資料只附約百KB的小型重現材料，不附24MB壓縮包、77MB執行檔、外站完整HTML或PDF。所有十份保存的命令argv實際使用`-no-init`；舊研究／license review的`-init /dev/null`敘述不當作已執行命令。

**命令要能照寫。** 原研究精確RUN以`-c`傳完整SQL；`-f`是同版help列明的檔案方式，不冒稱另做一輪效能實驗。畫面讀得完並口述必要旗標、完整SELECT／WHERE／排序與COPY；SQL檔全文可下載。

```sh
./bin/duckdb -no-init -no-agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/01-preview.sql
./bin/duckdb -no-init -agent :memory: -f sql/03-followup.sql
```

`-no-init`略過使用者初始化檔，`:memory:`是本次臨時資料庫；不要求改HOME、全域PATH或貼任何key。資料包未包含CLI，重新執行前須依README取得官方固定版本並核對digest；本階段沒有重新下載或執行。

**預期／實際／核對。** 完整結果480筆，R2和R3各240；CSV與獨立Python oracle逐列及bytes一致，CSV與保留的Parquet讀回CSV相同，SHA256均為`7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5`。結果hash只輔助辨識，不取代條件查核；agent footer的結果hash不依列順序，不當作檔案SHA256或排序證明。

**同一案例、觀眾真的改一行。** 在原480筆完整交付已核對後，新增需求才改為`actual_days >= promised_days`；完整建表／五欄／排序／COPY見[data/variant](data/variant/README.md)。實跑新檔720筆，其中240筆剛好3天、`days_late=0`；不選提前2天，也不選在途空值。另檔清楚標新需求，未覆寫原「嚴格晚到」480筆。這是可修改、可執行且結果不同的延伸對照，不只是把現成包再跑一次。

**錯誤契約。** agent stderr是startup文字加一行合法JSON；辨識JSON行後才解析。不能把整條stream當單一JSON物件後，稱DuckDB輸出壞JSON。兩種模式都能報欄位錯誤；沒有測某個真實consumer或AI因此失敗。

畫面進度：原創輸入／真實兩模式預覽→完整欄位卡與SQL→兩筆條件推導→作者刻意錯字與JSON行→完整COPY→CSV頭尾、路線摘要、保留讀回與原創HTML。每個卡片狀態以有意義的5–8秒變化為目標，最後以正式render檢查為準，不把規劃當已看過的成片。

## 大綱

### 選項 A：先辨識省略，再交完整跟進名單（推薦）

一行說明：一份配送資料一路走到可驗收檔案，新聞只作入口；協調代理已依既有委派採用A。

開場鉤子：「十月二十五日，我用這份配送表執行查詢。這份練習清單，正在找需要跟進的包裹。螢幕留下前後四十列，中間出現省略標記。這份表真的只剩這些紀錄嗎？實際天數的欄位，等一下會少一個字母。清單另外存成檔案，又怎麼確認內容完整？我把查詢和交付檔一起留下，讓每筆資料能回查規則。」

正式劇本另做原生敘事審讀，這裡沒有通過收據。

案例與結果：「原創1,200筆配送CSV，RUN取得已送達延遲的完整480筆CSV／Parquet和可讀報告；40是輸入預覽，不是跟進檔的筆數。」

| 章／計畫秒數 | 同一任務的狀態、可做動作與畫面 | 收尾問題 |
| --- | --- | --- |
| 配送清單只顯示一部分／35 | 當次本地查詢、同一虛構配送表；只立完整名單目標及三個未揭曉問題 | 只是少印，還是資料真的少了？ |
| 先看完整資料，再選輸出模式／96 | `code`完整命令→`compare`同版兩模式；讀總數與省略提示 | 跟進名單應該怎麼寫條件？ |
| 把跟進需求寫成完整條件／130 | `steps`五欄／型別→`code`完整SELECT／WHERE／排序→延遲／在途／剛好準時三個邊界 | 欄位少一個s，工具怎麼回答？ |
| 讀懂錯誤，再把完整清單存下來／145 | 明示作者故意錯字；兩模式錯誤→合法JSON行→修欄位→完整CSV／Parquet COPY | 畫面還是樣本，完整檔怎麼核對？ |
| 打開完整檔，核對每筆交付／122 | 全檔逐列oracle→CSV／Parquet讀回→改`>=`另存720筆，新增240筆剛好準時→原創HTML | 為這種新印法，現有工作要立刻升級嗎？ |
| 把新模式放進合適的工作範圍／110，含outro | 分新agent印法／既有匯出、新聞日期、LTS與相容界線；最後`keep-the-rule`才是實際outro，回答開場並邀留言／訂閱 | 不預告下一片 |

此版正式brief與同時撰寫的scratch稿對齊為**六章，outro歸第六章，不另起第七章**。上表四捨五入合計638秒；原生estimateTimeline最新計畫637.37秒，coldopen34.97秒，真正outro約11.8秒，保守排除兩者仍590.6秒。這些全是250 spoken units/min加原生停頓的文字估時，不是音長PASS。協調代理已明確要求本片coldopen30–45秒，取約35秒；不沿用早期快照24秒。正式當前旁白及成片正文仍須實測至少480秒，不靠空白、重述或慢播補時。三個預告會回收：省略去哪裡、錯欄位怎麼修、全檔怎麼驗；聲音與畫面均未生成或驗收。

### 選項 B：從交付檔倒推規則

一行說明：先看原創480筆成果，再倒推完整條件、輸入、兩模式、省略、JSON錯字、COPY與讀回。

開場鉤子：「這份檔案有四百八十筆要跟進的配送紀錄，來源是一份原創練習表。我要先把交付條件寫清楚，再回查每一筆如何進來。」

案例、證據和適用界線與A相同；比較偏已做報表的觀眾，新模式較晚出場，非首選。六章計畫：實物35→規則115→輸入100→模式110→匯出讀回及新需求135→升級與收尾90（含outro），合計585秒；不是實測音長。

### 選項 C：從合法JSON錯誤走回完整名單

一行說明：從作者刻意少寫s的兩種錯誤呈現開始，再對欄位、條件、預覽和完整匯出。

開場鉤子：「同一個少寫的字母，這裡回文字，那裡回一行合法JSON；但修正仍得對回原來欄位。」

JSON比任務更早，對一般觀眾較重，非首選；不製造真實第三方consumer事故。六章計畫：錯誤35→欄位契約105→規則110→模式110→全量匯出讀回及新需求130→升級與收尾90（含outro），合計580秒；不是實測音長。

## 會過期的事實

- [agent模式介紹](https://duckdb.org/2026/10/09/agent-mode.html)：10月9日已介紹，不能說10月21日才首次公開這個想法。
- [2.0公告](https://duckdb.org/2026/10/21/announcing-duckdb-200)與[正式release](https://github.com/duckdb/duckdb/releases/tag/v2.0.0)：10月21日正式提供，release `published_at=2026-10-21T12:49:12Z`，非prerelease；LTS承諾至少到2027年10月。以上是2026-10-25正常官方GET所得，不是本地測出的支援承諾。
- [migration文件](https://duckdb.org/docs/2.0/operations_manual/migration.html)：新預設儲存格式與2.0前版本的讀取相容性、既有舊格式保留條件，寫稿／發布前再核。未測現有資料庫升級或回滾。
- 原研究實際二進位為`v2.0.0 (Cyanoptera) d54cbbe3df`；套件digest與原始下載收據在[data/sources](data/sources/)及[package-check.json](data/package-check.json)。同版兩印法不等於跨版基準。
- 官方特定TPC-H實驗的59%輸出token與約0.5%總輸入，不作本片本地成果，不換算成費用或效能承諾；正文推薦不報這兩個數字。

## 素材

- [研究摘要與來源](research.md)、[小型資料包](data/README.md)、[SQL](data/sql/)、[全量CSV](data/output/late-followup.csv)、[Parquet](data/output/late-followup.parquet)、[可讀HTML](data/output/followup-report.html)、[真實命令日誌](data/runlogs/)。本階段均是實際本地檔案；尚未commit／發布，不造公開下載URL。
- 原創fixture、程式、SQL與報告按[CC0](data/LICENSE-ORIGINAL.txt)；DuckDB原始MIT另附[data/sources/duckdb-license.raw](data/sources/duckdb-license.raw)。官方文件與第三方metadata不被改授權為原創。
- 六則海外文字參考、原始watch連結、來源日期和觀察限制見[research.md](research.md)。只讀文字metadata，沒有看片或量剪點；沒有CTR、留存或精確片長證據。
- 不帶入CLI壓縮包／執行檔、外站全文、PDF或既有片子的圖／媒體；不修改共享`docs/videos/lexicon.json`。

## 不做的事

不測AI模型、Cowork或帳號產品；不冒稱原創配送資料是客戶事故；不把刻意錯字說成AI出錯。CSV／SQL／COPY／Parquet均是既有能力，不包裝為2.0首創。輸出bytes不是token或美元，結果hash不是來源／排序／業務正確性證書。沒有服務、擴充安裝、生產資料庫遷移或升級基準。界線集中說明，正文主要用同一份資料完成實際跟進交付。未做的Jev、盲讀、TTS、音檢、卡片／成片QA與八語交付均保持待辦。
