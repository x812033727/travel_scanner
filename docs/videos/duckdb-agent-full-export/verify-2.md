# 第五題 verify2：當前單句事實澄清續核

**PASS。** 原verify1唯一問題V1-F1已解決：當前[rxjg]說「按原規則分組」，與實際`FROM parcels`套原WHERE及GROUP BY吻合。R2／R3各240的數字保持正確；未發現新的事實修正事項。

scope：知情、獨立事實及技術續核；沒有新fresh narrative score，沒有媒體或whole-production-ready批准。查核時間2026-10-26T01:02:22Z。

fullsourceSHA：`7d150fc4e8a818e80560c80e4a392e93699666571c3647d4471b4222bcfb0726`。

claimsSHA：`cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`。

歷史來源SHA：`1a267cb77e4d3eeddffc850dca6616c68a3c66afcaed38576b6e776a3ca62bf2`。

## 唯一來源變動

直接遞迴比較完整新舊JSON，只得到一個leaf：`/scenes/51/lines/0/text`，scene=`route-summary-result`，line=`rxjg`。

前：「剛剛分組的完整檔，路線二和路線三各有兩百四十筆。」

後：「剛剛按原規則分組，路線二和路線三各有兩百四十筆。」

其餘110句、全部非text欄位、64景順序、111個line IDs、6章、claim references、圖卡內容、完整SQL／命令及範圍界線皆相同。新句指回前景原規則，沒有再聲稱從交付檔讀取GROUP BY。原始`demo/followup.sql:5–8`的實際來源仍為parcels，兩條COPY在其後，證據與新句相符。

## 逐21項當前結論

五欄均非空；21項場景列表逐序匹配當前source，used=defined，無未用或未定義項。下表是當前事實結論；完整111句逐句引文、scene與claim對應保存在JSON。

| Claim | 結論 | 當前證據 |
|---|---|---|
| c1 | PASS | 獨立以fixture-description規則重建全部1200筆，逐列與原始CSV相等。run_demo.py:20–25明示作者生成，原創CC0與虛構標示一致。 |
| c2 | PASS | 兩模式預覽均逐值匹配原表最前20及最後20筆，總40；一般footer為1200 rows (40 shown)，agent原樣標1160 omitted。1200−40=1160。 |
| c3 | PASS | typo.sql故意使用actual_day；兩條raw stdout空、exit1，human明示找不到欄位，agent合法物件name=actual_day且exception_message含actual_days及parcel_id候選。原始作者程式註解與旁白[xj3j]均明示故意。 |
| c4 | PASS | 用標準函式庫從原CSV獨立重算全部480筆及5欄和順序，與main CSV及Parquet-readback CSV完全相等；兩CSV亦逐byte相等。 |
| c5 | PASS | 主SQL完整使用status=delivered AND actual_days>promised_days；兩天數讀為INTEGER。240筆在途actual_days全部空白，raw預覽為NULL；無填零操作。 |
| c6 | PASS | 官方2.0 agent文件與實際輸出支持compact Markdown、明示結果範圍、JSON錯誤及強制mode flags。CLI輸出供外部AI coding agent讀取；本例只有CLI+確定性SQL，沒有模型推理。 |
| c7 | PASS | 9條公開根目錄./duckdb命令逐argv、cwd、exit及stdout/stderr bytes+SHA核對。5張命令卡正規化shell續行後精確命中receipt；14張SQL卡均匹配標示檔案完整行範圍與總行數。 |
| c8 | PASS | 獨立計數delivered=960、in_transit=240；在途actual_days全空白。raw followup狀態計數與圖卡一致。 |
| c9 | PASS | 逐原表確認P0002/R2為delivered、3→4、差1；P0005在途且實際空白；P0001/R1為3→3，主單排除而變式納入。相關圖卡與檔案一致。 |
| c10 | PASS | 主SQL選parcel_id、route、promised_days、actual_days、days_late，差值在SELECT計算，CSV/Parquet兩段COPY都保留WHERE及ORDER BY parcel_id；無LIMIT或顯示列數設定。CSV欄序及全列順序逐項相同。 |
| c11 | PASS | 主條件>排除差0；變式>=加入差0且排除負差值。在途仍由delivered條件排除；另目的檔不覆寫main。 |
| c12 | PASS | 以json.loads實驗驗明raw stderr恰有兩個實體行：startup文字與一行合法JSON；單獨第二行可解析，整stream引發JSONDecodeError。候選名確實在exception_message，而非誤造獨立JSON key。 |
| c13 | PASS | CSV實際480資料列，header恰為5個交付欄名；raw讀回count為480。完整COPY保存條件，並非從40列預覽複製。 |
| c14 | PASS | Parquet兩份原始bytes一致且PAR1頭尾正確；原生readback.sql確實按parcel_id讀回再存CSV，raw執行receipt exit0。讀回CSV與主CSV逐byte及獨立oracle全欄相同。 |
| c15 | PASS | public receipts的兩mode均同一./duckdb runtime及同一followup.sql；各mode執行後CSV SHA都為7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5。version raw及既有binary SHA相符。 |
| c16 | PASS | 當前[rxjg]為「剛剛按原規則分組，路線二和路線三各有兩百四十筆。」明確指回原規則，與前景完整SQL及demo/followup.sql第5–8行FROM parcels、原WHERE及GROUP BY一致。本輪獨立CSV oracle再次得到R2/R3各240，末四筆及其數值仍吻合。verify1的V1-F1已解決。 |
| c17 | PASS | 主CSV、Parquet、完整SQL、原創HTML及原始教材ZIP均存在。HTML四個相對連結在本地可解析；原教材ZIP內相應HTML/CSV/Parquet/SQL bytes與原檔一致。新公開根目錄ZIP也已逐entry核對。 |
| c19 | PASS | captured agent介紹日期2026-10-09，官方正式公告及non-prerelease API published_at為2026-10-21。官方文件明示2.0引入agent呈現模式；本片未宣稱CSV/SQL/Parquet是新增。 |
| c20 | PASS | 真實命令cwd是新fifth-draft/public-run目錄，使用:memory:與-no-init；明確兩mode同版、固定輸入，沒有開既有資料庫檔。作者方法與實際收據相符。 |
| c23 | PASS | 本地Python生成fixture、執行固定CLI+SQL；setup禁extension自動安裝/載入。原始results列未測AI reasoning、token/dollar、speed、server及migration；旁白、description與圖卡的界線相符。 |
| c24 | PASS | 獨立>= oracle逐列吻合720筆與全部5欄，恰240筆差值0，無負差值；主480檔及SHA保留。P0001進變式。SQL仍有delivered條件並另存due-or-late.csv；旁白稱剛好準時或晚到。 |

## 當前實際資料重新核對

本輪重新以標準函式庫逐筆重建1200筆fixture，並從當前原CSV計算全部輸出。得到960已送達、240在途；在途actual_days全空白。主條件delivered且actual>promised的480筆，全部5欄與排列順序均對上完整CSV及Parquet-readback CSV；R2、R3各240。變式仍保留delivered且actual>=promised，全部720筆及5欄／順序相符，其中恰240筆差值0。兩個模式預覽的前20與後20筆均逐值對原表，共40筆；1160只屬顯示省略。

9條既有./duckdb公開根目錄命令重新檢查argv、cwd、exit及stdout／stderr實際byte數與SHA。它們仍是2026-10-25的真實run receipts，本輪沒有重跑。14張SQL卡精確匹配原檔行範圍、5張命令卡對上receipt、4張quote卡對上raw輸出。合法JSON行及整段混合stderr的解析界線再次以json.loads核實。

主CSV與Parquet-readback CSV逐byte一致；現存Parquet兩份bytes一致且PAR1頭尾正確。未聲稱本輪重新解碼Parquet或執行SQL。原schema／lint與純記憶體HTML compose均由當前source直接檢查：lint 0 errors／0 warnings，schema及template 0問題，64景／64 states。可見圖卡文字SHA仍為`e19f6211333ed4442345eb2f7fa3c7bdc81551adb7144c94c5a5a324bf608a9e`，與verify1一致。

## 固定材料、凍結manifest與歷史保存

只讀子任務獨立核對當前manifest **137/137**大小／SHA；未列一般檔案為0，唯一symlink是排除的public-run/duckdb，manifest未跟隨它。Manifest SHA為`1696d04faab84728214ef734baeefc46986b5ca958217f591dc15cdfc9778192`。歷史before-fact-clarification manifest **133/133**，固定98檔與歷史archive **98/98**逐bytes相同；fifth-demo manifest **93/93**及另兩份supporting documents也符合，10項衍生檔與四項輸入binding均吻合。

本輪也直接重核新ZIP：26,889B、42 entries、CRC正常、41項內部manifest符合，全部entry bytes對上public-run，SHA仍為`74064ba70799606bf6c8fbc970109bfad26d0d8a02b73e2c5691534678b9fdf2`。五份官方stored capture大小／SHA仍符合原收據；真正retrieval為2026-10-25T23:05:58.419240Z至23:06:02.830654Z。本輪未連網，沒有今日live GET。

| 歷史檔案 | 當前SHA256，與原紀錄相同 |
|---|---|
| fifth-verify-1.json | `c75ee8c72de6cdfeacf1e8c45c6cc93993084ba2b8bbc9d4b3d312571a577642` |
| fifth-verify-1.md | `819913f88d6fed802a5a00181aae98fb614e0a4cc6c8bac1ab18f6167e32c5c4` |
| fifth-narrative-r2-reader5.json | `80c9a53897a33bea98172f4511bffe3899f860db8b23ad61b2fb9d0970cf0322` |
| fifth-narrative-r2-reader5.md | `b1b4765afc2dce88d2634287904dd607018fa47c28bebcafe8693a315261453e` |
| fifth-narrative-r2-reader5-native.json | `3774b432b9a4e035c47d3d75a523578831f39556a9095ace36ced1933b629148` |
| fifth-narrative-r2-reader6.json | `6137df200f2ea7a9709ed39ea5836b62195b84c15e94356bada250b3f5b533e2` |
| fifth-narrative-r2-reader6.md | `caaaa5d8d2269c983331a2fc7d8e40af15eba6f532ed0e865bd88f75bb3a20f5` |
| fifth-narrative-r2-reader6-native.json | `1287bf6cd8279a7fe94e60531b97b419d25d8d1ef914fbe7f67860266237f286` |

verify1 JSON與Markdown均匹配我先前交付的完整SHA，原REVISE未覆寫。Reader5／6的raw、Markdown及native六檔仍符合保存hash並綁定歷史1a來源；未改答案、未重評分。claims.md本身也刻意保持原bytes及歷史來源字樣，本verify2用新fullsourceSHA與原claimsSHA建立當前明確綁定，沒有靜默重標歷史表。

## Informed narrative delta：只談改句

「剛剛按原規則分組」更清楚接回前景對原表套條件的操作，減少原表查詢結果與已交付完整檔的指涉混淆。這句沒有新增或移除支線、條件、數字、章節或鉤子；字數／原生spoken units及timeline估值也不變。這只是知情的單句影響說明，不是新盲讀，不給fresh分數，也不改任何歷史boolean或把原raw/native改綁新source。

## 範圍限制與操作

本輪只寫verify2兩檔，未修改source／claims／固定材料／repo或任何歷史review；未複製、抽取或執行77MB CLI，未重包ZIP，未跑paid、網路、後台、TTS、模型或media render。10.47分鐘仍是文字timeline估值；未聽音訊、未看實片或核實實際媒體長度。此PASS不批准模型／token費用／跨版性能／server／升級成效，也不代表公開下載URL或whole production readiness。

