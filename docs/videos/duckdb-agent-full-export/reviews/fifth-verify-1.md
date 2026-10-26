# 第五R2獨立事實查核 verify-1

**結論：REVISE。** 核心數據、完整SQL、同版兩模式實跑收據、官方日期／版本、JSON訊息契約及產物身分均通過本輪證據核對；只發現一處應窄修的資料來源措辭。未改稿。

scope：獨立事實及技術證據審查；不作narrative打分、音訊／實片驗收或全製作就緒批准。

查核時間：2026-10-26T00:37:01Z。

fullsourceSHA：`1a267cb77e4d3eeddffc850dca6616c68a3c66afcaed38576b6e776a3ca62bf2`。

claimsSHA：`cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`。

## 唯一修正事項

**V1-F1｜minor｜c16｜route-summary-result｜[rxjg]**

原句：「剛剛分組的完整檔，路線二和路線三各有兩百四十筆。」

`video.json:1550` 的這句把分組對象稱為完整檔；但前景 `route-summary-query` 的圖卡及 `demo/followup.sql:5–8` 都是 `FROM parcels`，先套原條件再分組，而且位於寫檔的COPY之前。它沒有讀取已匯出的CSV或Parquet做GROUP BY。R2、R3各240本身正確。

建議窄修為：「剛剛按原規則分組，路線二和路線三各有兩百四十筆。」只需使旁白對上實際讀取來源；不需改SQL、數字或重跑教材。此為正式verify的技術敘述問題，未據此改動任何narrative boolean。

## 21項主張與五欄

21項ID／等級、主張、證據、範圍、場景均完整非空；全部場景列表逐序匹配當前source。used與defined相等，無未用或未定義claim。ID保留原有跳號。111句原話、對應場景與claim均已保存在JSON逐句查核紀錄，64景圖卡全部讀完。

| Claim | 結論 | 獨立核對與範圍 |
|---|---|---|
| c1 | PASS | 獨立以fixture-description規則重建全部1200筆，逐列與原始CSV相等。run_demo.py:20–25明示作者生成，原創CC0與虛構標示一致。 範圍：非公司／個資／真業務／公共統計，非獨立AI產品回應。 |
| c2 | PASS | 兩模式預覽均逐值匹配原表最前20及最後20筆，總40；一般footer為1200 rows (40 shown)，agent原樣標1160 omitted。1200−40=1160。 範圍：僅顯示省略，不是查詢或儲存刪除。 |
| c3 | PASS | typo.sql故意使用actual_day；兩條raw stdout空、exit1，human明示找不到欄位，agent合法物件name=actual_day且exception_message含actual_days及parcel_id候選。原始作者程式註解與旁白[xj3j]均明示故意。 範圍：不是觀察到的AI失誤，也不是agent獨有報錯能力。 |
| c4 | PASS | 用標準函式庫從原CSV獨立重算全部480筆及5欄和順序，與main CSV及Parquet-readback CSV完全相等；兩CSV亦逐byte相等。 範圍：本例交付核對；本輪未重新執行SQL或解碼Parquet，讀回執行由固定raw receipt佐證。 |
| c5 | PASS | 主SQL完整使用status=delivered AND actual_days>promised_days；兩天數讀為INTEGER。240筆在途actual_days全部空白，raw預覽為NULL；無填零操作。 範圍：是作者需求，並非真物流政策。 |
| c6 | PASS | 官方2.0 agent文件與實際輸出支持compact Markdown、明示結果範圍、JSON錯誤及強制mode flags。CLI輸出供外部AI coding agent讀取；本例只有CLI+確定性SQL，沒有模型推理。 範圍：不把agent名稱當作內建模型／獨立AI產品測試。 |
| c7 | PASS | 9條公開根目錄./duckdb命令逐argv、cwd、exit及stdout/stderr bytes+SHA核對。5張命令卡正規化shell續行後精確命中receipt；14張SQL卡均匹配標示檔案完整行範圍與總行數。 範圍：只支持實跑Linux amd64 v2.0.0；未宣稱其他OS實測或本輪重跑。 |
| c8 | PASS | 獨立計數delivered=960、in_transit=240；在途actual_days全空白。raw followup狀態計數與圖卡一致。 範圍：此虛構fixture的分布。 |
| c9 | PASS | 逐原表確認P0002/R2為delivered、3→4、差1；P0005在途且實際空白；P0001/R1為3→3，主單排除而變式納入。相關圖卡與檔案一致。 範圍：同一份表的個案與整體條件，沒有另造外部數據。 |
| c10 | PASS | 主SQL選parcel_id、route、promised_days、actual_days、days_late，差值在SELECT計算，CSV/Parquet兩段COPY都保留WHERE及ORDER BY parcel_id；無LIMIT或顯示列數設定。CSV欄序及全列順序逐項相同。 範圍：新差值不改原天數；顯示限制不套入匯出。 |
| c11 | PASS | 主條件>排除差0；變式>=加入差0且排除負差值。在途仍由delivered條件排除；另目的檔不覆寫main。 範圍：需求變更，並非480筆原單錯誤。 |
| c12 | PASS | 以json.loads實驗驗明raw stderr恰有兩個實體行：startup文字與一行合法JSON；單獨第二行可解析，整stream引發JSONDecodeError。候選名確實在exception_message，而非誤造獨立JSON key。 範圍：mixed stream不是單一JSON；不是DuckDB壞JSON或真第三方consumer故障。 |
| c13 | PASS | CSV實際480資料列，header恰為5個交付欄名；raw讀回count為480。完整COPY保存條件，並非從40列預覽複製。 範圍：CSV／SQL／COPY是既有能力；沒有宣稱2.0才首次能匯出。 |
| c14 | PASS | Parquet兩份原始bytes一致且PAR1頭尾正確；原生readback.sql確實按parcel_id讀回再存CSV，raw執行receipt exit0。讀回CSV與主CSV逐byte及獨立oracle全欄相同。 範圍：沒有新跑Parquet decoder，沒有格式性能或壓縮比較。 |
| c15 | PASS | public receipts的兩mode均同一./duckdb runtime及同一followup.sql；各mode執行後CSV SHA都為7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5。version raw及既有binary SHA相符。 範圍：不是2.0對1.5，不提供模型／成本／時間效果。 |
| c16 | REVISE | R2與R3各240，末四筆P1191/1194/1198/1199與圖卡全部相符。唯一需修的是[rxjg]把原表套條件的GROUP BY稱為分組完整檔；目前圖卡SQL及原始followup.sql:5–8均是FROM parcels。 範圍：數字正確；資料來源描述需精確，等量摘要不能獨立證明全量內容。 |
| c17 | PASS | 主CSV、Parquet、完整SQL、原創HTML及原始教材ZIP均存在。HTML四個相對連結在本地可解析；原教材ZIP內相應HTML/CSV/Parquet/SQL bytes與原檔一致。新公開根目錄ZIP也已逐entry核對。 範圍：教材為本地existing artifacts；沒有本片公開下載URL、公開上傳或成片聲明。新public ZIP不含HTML，HTML是既有原教材的產物。 |
| c19 | PASS | captured agent介紹日期2026-10-09，官方正式公告及non-prerelease API published_at為2026-10-21。官方文件明示2.0引入agent呈現模式；本片未宣稱CSV/SQL/Parquet是新增。 範圍：本輪只讀10/25 capture，沒有今日live GET或重新下載。 |
| c20 | PASS | 真實命令cwd是新fifth-draft/public-run目錄，使用:memory:與-no-init；明確兩mode同版、固定輸入，沒有開既有資料庫檔。作者方法與實際收據相符。 範圍：不等於完成既有資料庫升級，也不構成全面採用建議。 |
| c23 | PASS | 本地Python生成fixture、執行固定CLI+SQL；setup禁extension自動安裝/載入。原始results列未測AI reasoning、token/dollar、speed、server及migration；旁白、description與圖卡的界線相符。 範圍：不把輸出bytes、CLI執行時間或agent名稱換算成模型或成本收益。 |
| c24 | PASS | 獨立>= oracle逐列吻合720筆與全部5欄，恰240筆差值0，無負差值；主480檔及SHA保留。P0001進變式。SQL仍有delivered條件並另存due-or-late.csv；旁白稱剛好準時或晚到。 範圍：不是全部720都晚到，不含在途或早到；是明示新需求。 |

## 獨立重算與完整顯示

以Python標準函式庫從原CSV重算，不以作者或root的PASS代替計算。全部1200筆也逐筆對上作者公開生成規則。狀態為960已送達、240在途；在途實際天數均空白，CLI顯示為NULL。主條件只納入已送達且actual_days>promised_days，全部480筆、5欄與排序均吻合；路線R2/R3各240。變式保留delivered條件、把>改>=並另存，全部720筆、5欄與排序吻合，其中恰240筆days_late=0，無負差值。P0001、P0002、P0005與末四筆圖卡逐值一致。

兩種預覽的最前20及最後20筆均逐值對回原表；顯示合計40，1160只屬省略。一般模式同樣有1200 rows (40 shown)提示。未把預覽顯示限制塞進完整COPY。

14張SQL卡逐字匹配caption指定原檔行範圍，且全檔行數正確。5張命令卡只把反斜線換行正規化為shell參數，再對照真正./duckdb實跑receipt。4張quote卡的內容均原樣存在raw輸出。HEADER、欄序、差值、排序、另存目的檔及正確NULL／在途條件均核對。

## 9條真實公開根目錄命令

逐條檢查README命令、argv、cwd、exit、兩個raw stream的byte數與SHA；本輪沒有重跑CLI。其真實observed_at為2026-10-25T23:50:19.009788Z至23:50:22.745662Z。兩條故意錯字命令exit1且stdout空，其餘exit0。

| 名稱 | 原樣命令 | exit |
|---|---|---|
| version | `./duckdb --version` | 0 |
| human-preview | `./duckdb -no-init -no-agent :memory: -f demo/preview.sql` | 0 |
| agent-preview | `./duckdb -no-init -agent :memory: -f demo/preview.sql` | 0 |
| human-typo | `./duckdb -no-init -no-agent :memory: -f demo/typo.sql` | 1 |
| agent-typo | `./duckdb -no-init -agent :memory: -f demo/typo.sql` | 1 |
| agent-followup | `./duckdb -no-init -agent :memory: -f demo/followup.sql` | 0 |
| human-followup | `./duckdb -no-init -no-agent :memory: -f demo/followup.sql` | 0 |
| readback | `./duckdb -no-init -no-agent :memory: -f demo/readback.sql` | 0 |
| variant | `./duckdb -no-init -agent :memory: -f demo/variant.sql` | 0 |

兩模式用相同v2.0.0 (Cyanoptera) d54cbbe3df及同一followup.sql；各mode執行後主CSV SHA均為`7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5`。不屬跨版本或模型成效比較。

## 合法JSON與讀回界線

獨立json.loads核對agent-typo.stderr.txt實際恰兩個實體行：startup文字＋單行合法JSON物件。只解析第二行成功；整段當單一JSON解析失敗。錯字actual_day、Binder、COLUMN_NOT_FOUND及說明內候選actual_days／parcel_id均與圖卡相同。作者原始程式及[xj3j]明示故意錯字，沒有觀察到AI事故或第三方consumer故障的主張。

主CSV與Parquet讀回CSV不只480筆相等，也逐byte相等；本輪兩份CSV全部欄位均獨立對回原表條件。Parquet原檔bytes與public-run原檔相同，PAR1頭尾正確；readback.sql與成功receipt也核對。沒有聲稱本輪新跑Parquet decoder、SQL或量測格式性能。

## 官方capture與版本／license

本輪network requests=0。以下是既有capture真正GET刷新時間，非今日live GET；五份本地stored bytes／SHA全部逐一符合原收據。

| Capture | 真正retrieval UTC | bytes | SHA256 |
|---|---|---:|---|
| duckdb-news | 2026-10-25T23:05:58.419240+00:00 | 577272 | `a6b42354bea9180169fbfb0a323aaafbadf6ad6a10d39c556c1c6c58c2daa146` |
| duckdb-agent-news | 2026-10-25T23:05:59.521959+00:00 | 553376 | `efc708e83651355784e0f8170cebc77549d1b27a3c2e37bb38d5f2fb6a26140f` |
| duckdb-agent-doc | 2026-10-25T23:06:00.630718+00:00 | 358168 | `091aaa73784352e1c1d03a020b8cf2eded1aefaa6e7f30216d5e240a5372eefd` |
| duckdb-migration | 2026-10-25T23:06:01.730457+00:00 | 377166 | `5c86b9d1386bda0f66d612106155ec40820ecd04a99013f83979ac70b532346a` |
| duckdb-release | 2026-10-25T23:06:02.830654+00:00 | 140951 | `12d8a1c2490a9abdb5e5b0a36e10f137598ca9ef8b2fa04c26f93b6130bad323` |

官方原文支持2026-10-09介紹agent模式、2026-10-21正式提供2.0，release API的tag=v2.0.0、published_at=2026-10-21T12:49:12Z、draft=false、prerelease=false及commit=d54cbbe3df17e8e5ce68312f483b4155836112aa相符。agent是供外部AI coding agent讀取的CLI呈現方式；本片沒有搬用官方模型、token、費用或速度實驗結論。

官方Linux amd64 archive現存24,424,037B，SHA `c6507206baf7793c6013dbd82368469a45f20dc0e17a6f92f204602f652ed2bc` 與release asset digest一致。現存CLI為77,526,584B，SHA `c41f957db5645d545a9caef430994cf262d24fad9297fef70c691395aadb43fb`；public-run/duckdb symlink解析到這個既有binary。此處只讀hash；子任務另以tarfile串流hash archive內唯一duckdb member，得到相同大小與SHA，沒有extract／copy／execute。原archive GET為2026-10-25T22:26:51.961566Z。

完整MIT條款保存在fifth-demo/sources/duckdb-license.raw，1072B／SHA `075c33400ffcb0c586dd106a029d3e733e9da3693f8fcb9cebfc651c8a2f14e3`；原GET為2026-10-25T22:25:40.515380Z。原創fixture、作者程式及報告的CC0明確排除DuckDB與官方文稿，沒有將它們重新授權。

## ZIP、HTML與原生純讀檢查

新duckdb-public-fixtures.zip為26,889B、42 entries，SHA `74064ba70799606bf6c8fbc970109bfad26d0d8a02b73e2c5691534678b9fdf2`。ZIP CRC正常；41項manifest逐檔檢查byte數與SHA，全42 entries（包括manifest本身）與public-run檔案bytes相同。沒有binary、symlink、官方HTML、官方raw archive或路徑跳脫；未重包ZIP。既有fixtures-manifest的40檔也全吻合。

本地原創HTML報告及其原教材ZIP存在，四個相對連結均可定位到現存檔案，ZIP內HTML／CSV／Parquet／SQL亦對上原檔。HTML是既有原教材產物，新public ZIP不含HTML。本片並無公開下載URL或公開上傳之證據或聲稱。

本輪直接執行原生lint：exit0，0 errors／0 warnings；直接validateVideo與renderProblems為0問題；純記憶體HTML compose得到64景／64 states及thumbnail HTML。這沒有呼叫browser、截圖或媒體render，也不證明實際圖卡停留或排版可讀性。原生10.47分鐘僅timeline估值。

## 本次範圍與完整性

source與claims收尾SHA仍符合任務指定；repo、來源稿、claims及教材未修改。未使用付費、TTS、render、後台、模型或網路；未複製77MB CLI或重新打包。未聽音訊、未看成片、未核實實際媒體長度。本次REVISE只針對[rxjg]的一句技術來源描述，不能當作whole production-ready判定。

