# 第五片 verify3：當前視覺delta與固定依賴知情獨立查核

**PASS。** 當前ca1e只包含兩項視覺修正（在source中為三個資料路徑）：input-columns去除重複key、縮圖加入具正確credit的原創subject。111完整line物件、voice、claims、SQL及數據未改。獨立fresh native靜態capture確認修卡與最終縮圖皆0layout，buffer逐bytes等於frozen樣本；63個原static PNG／keys不變。

**範圍：只批准這次視覺delta及目前固定依賴的連續支持；不表示audio通過、fresh narrative通過或whole-production-ready。** 查核時間：2026-10-26T01:38:06Z。

當前source：`/workspace/work/travel-scanner-duckdb/docs/videos/duckdb-agent-full-export/video.json`。

fullsourceSHA：`ca1ef60f4e9fd98f7c2e336a7fc8ab339c58b94f557ba0a7f6b8fb7cc279e1bf`。

claimsSHA：`cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`。

7d baseline：`7d150fc4e8a818e80560c80e4a392e93699666571c3647d4471b4222bcfb0726`；archive：`/workspace/work/ai-tech-next/fifth-visual-archives/before-visual-polish-7d`。350c只保留歷史，未作當前source。

## 實際source變動與完整不變證據

逐物件比較後，只需恢復以下三個路徑，即重建baseline完整bytes，SHA精確回到7d：

1. 恢復input-columns的`data.key = 先認出五個欄位`。
2. 移除`thumbnail.data.asset`。
3. 將`assets`恢復原空陣列。

其餘全部欄位精確相同。111個完整line物件逐一相等，包含text、say、say_for、emotion、IDs及其他既有欄位；完整line陣列的canonical SHA為`4711b7accb7c06764653d48d56f6bdc656d632652c23ae2b23ba2834110bad5b`。voice物件完全相同；native speechHash前後都是`38cf9292f6945199`。64景／6章、全部claim references、所有圖卡SQL／值、thumbnail既有headline／tag／sub及來源限制亦未改。JSON內保存當前完整111物件，不只比對text。

input-columns只刪與title重複的optional key；title、欄位／意思兩欄、五列原名與中文意思及來源均精確保持。實看修卡五列完整、來源清楚，沒有重複key-band或裁切。

## 完整當前21項claim狀態

下列每項 **CONFIRMED** 都明確沿用verify2已查明且未改的事實／RUN／官方capture證據，並重核當前依賴身份與source連續性；不是新live GET或新的音訊／成片驗收，也不是靠關鍵字掃描代替逐項判斷。全部21項五欄完整、場景列表逐序相同，used=defined。

| Claim | 當前狀態 | 主張 | 此輪連續證據與限制 |
|---|---|---|---|
| c1 | **CONFIRMED** | 原創1200筆虛構fixture及作者生成規則 | 沿verify2；當前原CSV、原始93檔及本例1200筆身分重核。不是真公司／個資／公共統計或AI產品回應。 |
| c2 | **CONFIRMED** | 1200筆原表，顯示40，省略1160 | 沿verify2；當前raw footer、省略字串與原表／固定檔身分再核。縮圖40指preview全表顯示，不是查詢或儲存刪列。 |
| c3 | **CONFIRMED** | 作者故意actual_day錯字；兩mode均報錯 | 沿verify2；typo SQL與兩mode stderr／RUN收據未變，作者故意及非AI事故的完整line物件未改。 |
| c4 | **CONFIRMED** | 480筆完整主清單及逐列核對 | 沿verify2；當前主CSV全部5欄再次吻合從原表計算的oracle；讀回CSV／Parquet與raw依賴身分未改，未新跑Parquet decoder。 |
| c5 | **CONFIRMED** | delivered且actual>promised；在途與NULL界線 | 沿verify2；當前WHERE、INTEGER型別、CSV及圖卡值／全部SQL未改；縮圖箭頭明示按條件另存。 |
| c6 | **CONFIRMED** | agent是CLI回覆模式，非內建模型評測 | 沿verify2；官方capture原bytes／SHA及當前identity-index再核，原Markdown／JSON RUN依賴不變。不是新live GET或模型測試。 |
| c7 | **CONFIRMED** | 完整可讀SQL、9條公開命令與固定2.0 | 沿verify2；111 full objects及全部scene data SQL未改，當前9條RUN依賴由266／253 manifest與固定98檔重核。未重跑CLI。 |
| c8 | **CONFIRMED** | 960已送達、240在途且實際天數空白 | 沿verify2；當前原CSV及狀態計數raw身分不變，圖卡數值未改；只屬虛構fixture分布。 |
| c9 | **CONFIRMED** | P0002、P0005、P0001同表個案與手算 | 沿verify2；當前輸入／主單／變式身分、個案圖卡完整值及旁白物件不變，沒有另造個案。 |
| c10 | **CONFIRMED** | 交付5欄、差值、排序及完整COPY條件 | 沿verify2；當前主CSV全欄oracle相符，兩段COPY及所有顯示SQL未改；非從40列預覽複製。 |
| c11 | **CONFIRMED** | >與>=是兩個明示需求 | 沿verify2；原SQL／變式SQL／目的檔及圖卡不變，current720與240個零差值點算相符；不把原480稱錯。 |
| c12 | **CONFIRMED** | 單行合法JSON與mixed stderr不是單一JSON | 沿verify2已完成的json.loads判斷；當前stderr及候選欄位依賴bytes未變，完整相關旁白物件不變。不是新consumer事故或壞JSON聲明。 |
| c13 | **CONFIRMED** | 完整480筆CSV、HEADER及讀回count | 沿verify2；當前480全欄oracle相符，CSV／完整COPY／raw count身分不變；CSV／COPY是既有能力。 |
| c14 | **CONFIRMED** | 相同條件匯出Parquet再讀成CSV | 沿verify2原生RUN及讀回證據；當前Parquet／readback SQL／CSV依賴均未改，未新解碼或量測格式性能。 |
| c15 | **CONFIRMED** | 同一2.0兩mode得到相同清單 | 沿verify2；原binary相關93檔及兩mode RUN／匯出身分均未改，不是跨版、模型、速度或費用比較。 |
| c16 | **CONFIRMED** | R2／R3各240、末端紀錄與正確原表分組來源 | 沿verify2修正後結論；當前主CSV路線計數再次為各240，rxjg完整物件仍為按原規則分組，未觸及其SQL或事實。 |
| c17 | **CONFIRMED** | 完整資料、SQL、原創HTML及教材產物 | 沿verify2；當前原產物依賴、原93檔及42-entry公開ZIP逐bytes身分再核；不聲稱公開下載URL或已上傳。 |
| c19 | **CONFIRMED** | 10/9介紹、10/21正式2.0；匯出是既有能力 | 沿verify2官方原文／release結論；本輪只重核10/25 capture bytes／SHA及identity-index，沒有今日live GET。 |
| c20 | **CONFIRMED** | 新目錄、:memory:、同版兩mode的作者方法 | 沿verify2；當前完整命令、原始RUN依賴及相應旁白／voice未改；不是舊資料庫升級。 |
| c23 | **CONFIRMED** | 固定fixture／SQL，未測模型、費用或跨版性能 | 沿verify2；全部方法限制、命令、voice及完整line物件未改。這次只做視覺delta及依賴核對。 |
| c24 | **CONFIRMED** | 另存>=變式720筆，含240準時件 | 沿verify2全欄oracle及條件結論；當前變式檔身分未變，720及240個零差值再次點算相符；仍不是720筆全晚到。 |

## 真正靜態視覺查核

本審者實際看了最終input-columns PNG、最終thumbnail JPG及原創subject PNG，亦用既有`PLAYWRIGHT_BROWSERS_PATH=/workspace/work/playwright`獨立執行native openRenderer capture。只在記憶體取得兩個buffer，沒有寫任何新影像檔、全片render、TTS或ASR。Native fake origin僅從本地供應資源，不依賴外部網路。

| 畫面 | 本次fresh layout | 本次buffer SHA256 | 與frozen樣本 |
|---|---|---|---|
| input-columns | 0 | `84e76da5e6ab103ce2ea6484e69f864eed4663f7e26860ae5176fdc3929033b4` | 逐bytes完全相同 |
| thumbnail | 0 | `9cf4fe7a61b9d8acc128a178bb91e43ab53b56b594847d9264b0f844abccff8e` | 逐bytes完全相同 |

其餘63個state的actual PNG bytes及native keys逐一對7d，全部相同；只有修卡改變。當前64個state又逐一等於已修卡的中間static樣本，但中間稿只作位元組來源追溯。當前native renderPlan全部64 keys及thumb key直接對上ca1e sample manifest；manifest對64state及縮圖均記0layout。本輪原生schema、template、SVG security及lint均0問題（lint 0 warnings）。

## 縮圖語意與原創credit

成品明示「同一份配送表」「按條件另存完整結果」。40列位於回覆預覽區；下方是完整交付檔CSV／Parquet，並標原創示意／可重開核對。原圖是簡化欄線示意，沒有冒充40筆原生UI截圖，也沒有寫成「同一份查詢」。

直接對當前SQL及資料：preview.sql查全表，沒有WHERE；40是其顯示列數，raw同時記1200總列及1160 omitted。followup.sql由同表套delivered且actual>promised的WHERE，另存符合條件的完整子集。本輪主CSV480筆全部5欄再對原表oracle相符，R2／R3各240；變式720及240個零差值也與保留依賴一致。圖未揭480／1200等後段筆數，條件箭頭沒有把40列說成匯出全集。

| 原創資產 | bytes | SHA256 |
|---|---:|---|
| content-addressed PNG | 80989 | `9317157458b260eae8f2a98503fa39c36a33024e5bdb2cd77d422995e90cb2de` |
| SVG | 2385 | `9213cc69a0c11e951d7da284c0000fe775c313951a23d3e37cb9612c84d50474` |
| thumbnail-credit.json | 222 | `075087110c1f52b9abc8351637f0582833235c584a980022316cc3be050cc12b` |

source的asset path、assets[0]及credit JSON逐物件相同；PNG檔名16位fingerprint對上實際full SHA，canonical PNG與fingerprinted PNG逐bytes相同。Generator內的原創SVG literal精確等於保存SVG，沒有執行generator或重新寫資產。Native SVG安全檢查0問題。Credit明示「本片原創教學示意｜虛構配送資料與本地2.0輸出｜非DuckDB官方UI」，license=CC0-1.0，與實際示意圖一致；未將DuckDB或官方文稿重新授權。

## 固定依賴及當前manifest

當前episode manifest **266/266**大小／SHA核對，未列一般檔案為0；manifest SHA `febc17b61b32b9e2092f985714aeb739bee4aede628f9e9df38363d66badb3bb`。7d archive manifest **253/253**核對，SHA `c19ce4845423d67bb9da328711518421ebdc00971ba5380b25dd9585a2ad7ab8`。除9份已授權source／衍生說明檔外，其餘preexisting檔案與7d逐bytes相同；9份為：`README.md`、`assets/source-content-audit.json`、`duration-plan.json`、`line-id-provenance.json`、`narration.md`、`native-schema.json`、`scene-plan.md`、`verification.json`、`video.json`。

原scratch固定98檔及原fifth-demo **93/93**也按原manifest重核。當前公開ZIP仍26,889B／42 entries／SHA `74064ba70799606bf6c8fbc970109bfad26d0d8a02b73e2c5691534678b9fdf2`，CRC正常，全部entry bytes對上public-run，未重包。

官方來源identity-index的11個條目逐一對上原scratch保存bytes；五份primary capture真正GET時間仍是2026-10-25T23:05:58.419240Z至23:06:02.830654Z。本次未連網，沒有今日live GET。Full external HTML／text按設計仍在原scratch，不冒稱已放入episode或公開教材；episode的release及MIT小型保存件與原件相符。

## 歷史與操作界線

原verify1 REVISE、verify2的7d PASS及reader5／6 raw/native歷史檔案保持原bytes／SHA；沒有清理歷史問題、改分、重給fresh score或把歷史答案改綁ca1e。當前ca1e的本次PASS由上述實際delta、身份、native plan與fresh static capture支持。

只新寫scratch `fifth-verify-3.json`及`fifth-verify-3.md`；未修改source、claims、assets、教材或repo。未跑paid、模型、TTS、ASR、DuckDB／SQL、後台、全片render或assemble。只做兩個原生靜態in-memory capture。voice／say未改不代表音訊已聽驗，10.47分鐘仍為原生文字估值；未核實影片實際時長／聲畫同步或公開下載／後台完成狀態。

