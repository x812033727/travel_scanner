# 第五片 verify4：公開教材連結與當前來源綁定

**PASS。** 本輪只核對說明欄加入兩個真實 immutable 公開教材連結；完整111句物件、64景、voice、claims、資料與歷史審查未改。沒有新的音訊、敘事或整片完成判定。

查核時間：2026-10-26T03:41:58.900Z。當前 source SHA：`40eb4df54489ed6a8c82012ff028ed5608390fec2d614a75093c1426f6ae58aa`；claims：`cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`。

## 實際核對

- 從已推送410633ab Git blob獨立讀取ca1e前版，逆轉唯一/youtube/description後完整source bytes／SHA相同。
- 作者freeze17檔逐檔SHA／大小一致；原287檔除5項授權來源／進度說明外，其餘282檔逐bytes相同。
- native screenplay重新由當前source在記憶體生成，SHA仍為`7aac2017419c82a4b81fb40050f067c9e021312600e5d66ec70846b58946107b`；speech38cf9292f6945199、visual9f1673219982b59d、narrative33aca1b29ba7817a。既有本地script採用仍綁完全相同script.md，不建立新核准。
- 正常composeMetadata無問題，完整說明2212 UTF-8 bytes，小於5000。公開CSV和42-entry ZIP沿用root於02:39實際GET200／完整SHA收據；當前本地bytes再次符合。未再次GET，未單獨GET GitHub資料夾HTML。

公開教材：[9條實跑命令與資料](https://github.com/x812033727/travel_scanner/tree/410633ab4addde4d4590dfecc0e138d48d072d3b/docs/videos/duckdb-agent-full-export/public-run)；[完整fixtures ZIP](https://raw.githubusercontent.com/x812033727/travel_scanner/410633ab4addde4d4590dfecc0e138d48d072d3b/docs/videos/duckdb-agent-full-export/duckdb-public-fixtures.zip)。

## 21項當前主張連續性

每項CONFIRMED沿用verify3已查明且本輪逐bytes未改的固定依賴；不冒稱新live官方查核。c17另由上述真實公開GET收據支持目前下載連結。

| Claim | 狀態 | 範圍 |
|---|---|---|
| c1 | CONFIRMED | 原創1200筆虛構fixture及作者生成規則；定義、scene與既有證據未改。 |
| c2 | CONFIRMED | 1200筆原表，顯示40，省略1160；定義、scene與既有證據未改。 |
| c3 | CONFIRMED | 作者故意actual_day錯字；兩mode均報錯；定義、scene與既有證據未改。 |
| c4 | CONFIRMED | 480筆完整主清單及逐列核對；定義、scene與既有證據未改。 |
| c5 | CONFIRMED | delivered且actual>promised；在途與NULL界線；定義、scene與既有證據未改。 |
| c6 | CONFIRMED | agent是CLI回覆模式，非內建模型評測；定義、scene與既有證據未改。 |
| c7 | CONFIRMED | 完整可讀SQL、9條公開命令與固定2.0；定義、scene與既有證據未改。 |
| c8 | CONFIRMED | 960已送達、240在途且實際天數空白；定義、scene與既有證據未改。 |
| c9 | CONFIRMED | P0002、P0005、P0001同表個案與手算；定義、scene與既有證據未改。 |
| c10 | CONFIRMED | 交付5欄、差值、排序及完整COPY條件；定義、scene與既有證據未改。 |
| c11 | CONFIRMED | >與>=是兩個明示需求；定義、scene與既有證據未改。 |
| c12 | CONFIRMED | 單行合法JSON與mixed stderr不是單一JSON；定義、scene與既有證據未改。 |
| c13 | CONFIRMED | 完整480筆CSV、HEADER及讀回count；定義、scene與既有證據未改。 |
| c14 | CONFIRMED | 相同條件匯出Parquet再讀成CSV；定義、scene與既有證據未改。 |
| c15 | CONFIRMED | 同一2.0兩mode得到相同清單；定義、scene與既有證據未改。 |
| c16 | CONFIRMED | R2／R3各240、末端紀錄與正確原表分組來源；定義、scene與既有證據未改。 |
| c17 | CONFIRMED | 完整資料、SQL、原創HTML及教材產物；增加真實公開CSV／ZIP的既有GET證據，資料夾HTML未另抓。 |
| c19 | CONFIRMED | 10/9介紹、10/21正式2.0；匯出是既有能力；定義、scene與既有證據未改。 |
| c20 | CONFIRMED | 新目錄、:memory:、同版兩mode的作者方法；定義、scene與既有證據未改。 |
| c23 | CONFIRMED | 固定fixture／SQL，未測模型、費用或跨版性能；定義、scene與既有證據未改。 |
| c24 | CONFIRMED | 另存>=變式720筆，含240準時件；定義、scene與既有證據未改。 |

R2兩讀者各12/13 false、no_recap／no_detour及root教學取捨原樣保留。paid TTS仍0、未做音檢／全片render／QA；官方片頭尾已在本系列隔離來源恢復，但第五片尚未套用。這份報告不授予伺服器核准，也不代表八語完成。
