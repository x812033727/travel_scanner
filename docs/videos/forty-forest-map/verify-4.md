# ForTy：B像素定位兩句與公開資料包定向複核

日期：2026-10-25（Asia/Taipei）。依root指示，僅核對新增b-pixel-center兩句／圖卡及description資料包URL與實際metadata；沒有重新全審原85句，沒有修改稿件、音訊或生產旗標。

**結果：PASS（本輪指定差異），0 must-fix。** 前三份收據保留原結論、原SHA；本次不替敘事盲讀、實際旁白、字幕或成片QA判定通過。

## 綁定版本

- video.json SHA-256：`cb6a8a9e21c4e51313c879092b12fbb20cd9fec203ff1216880a56fad0a98c03`
- claims.md SHA-256：`91cb55e8c8faf306f08b18c0c1fff2d493c574f89d4dd596daed13139303c9c8`
- B原始JSON SHA-256：`4ebd1c412fe85576277d0b8c4ab96fce31254abe41b6c07ba3ca203220db101a`
- verify-1／2／3 SHA仍分別為`5bc134669e77a972707bc5782df7e7aa53bcc015f196264f0257edb2c6403f10`／`a985bf9f4c721da6bfd4b5a06ebb1f861c1f8f809449a022d1f0980678348081`／`6d6f829951126cbc5fac200a6c84faa241f5d8a93447a11982e979233ee045db`，未改。

## 新增兩句：CONFIRMED

| Claim／line | 實際原句 | 本輪獨立結果 |
| --- | --- | --- |
| c86／fe8z | 第二格的像素中心在東經一百二十一點四二二三四。 | 原始longitude121.42233836084972，Decimal ROUND_HALF_UP到小數5位是121.42234，中文逐位相符。 |
| c87／ymf8 | 北緯二十四點六九五二八，用這個位置對回紅框。 | 原始latitude24.695276083224126，同法得24.69528，中文逐位相符；四捨五入位置仍落原B像素。 |

本輪直接讀取`data/actual-uncertain-roi-result.json`的selected_pixel，不以作者完成收據代替計算。以既有rasterio/GDAL將四捨五入後WGS84經緯度轉為EPSG:32651，重得：

- x=`340395.1708446171`，y=`2732125.431880638`。
- 使用已核對來源affine：col=floor((x−317440)/10)=2295；row=floor((y−2692000)/10)=4012。
- 與原始B selected_pixel row4012／col2295一致，對應ROI[5,5]紅框。

新表格東經121.42234°、北緯24.69528°與口述相符，標題為「B指定像素中心」，keys明說非窗口幾何中心。這是原中心座標取5位小數的表示，沒有宣稱新的地面定位精度、偶數窗口精確幾何中心或地面土地真值。

Primary來源仍是本日已獨立206 Range解碼的官方COG：

https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif

本次只重讀固定SHA資料與反投影，不重新下載整個COG、不執行模型或地面調查。

## 公開資料包URL：實際可解析，內容與本次資料一致

description新增URL：

https://github.com/x812033727/travel_scanner/tree/e0c70c899/docs/videos/forty-forest-map/data

本輪透過GitHub唯讀connector實際讀取**這個精確目錄URL**，成功返回三個檔案，而非只看本機git或猜測default branch。再讀取公開commit端點，短ref `e0c70c899`解析為：

`e0c70c8993dc158a307afa6faf0a2409065a2ca7`

目錄回傳的三個Git blob SHA，與本輪依本機實際bytes自行算`SHA1("blob "+byteLength+NUL+bytes)`完全相符：

| 公開檔案 | bytes | 公開Git blob SHA＝本機重算 |
| --- | ---: | --- |
| actual-roi-result.json | 18497 | `129dbd271274ed850e9719fd7769a61a3d94ad22` |
| actual-uncertain-roi-result.json | 13394 | `5ce757a779c15f454a952876b2951c9dbe0f7abf` |
| independent-results.json | 14762 | `54ff7872a304700ab9f18b3371f130829b6bd446` |

公開A/B JSON含完整原始數組、指定像素座標；B JSON selection與independent-results的B_search記錄選樣範圍／低最大分數／排除邊界及本地選取規則，支持連結標示的「原始值、座標與選樣規則」。未承諾此目錄含未提供的GeoTIFF、年度資料或完整可安裝工具。此證據是GitHub實際讀取成功及精確ref／blob比對，不將它冒稱為瀏覽器頁面HTTP200測試。

## 實際metadata與lint

guard_review另以唯讀方式對本次video實際呼叫`composeDescription`：正式body/sources/assets/tags/category/campaign、`locale:'zh-TW'`、`timeline:estimateTimeline(doc)`、`article:null`。

結果：**2701 UTF-8 bytes、5條完整圖片credits、checkYoutubeFields=[]**。新增資料包URL確實出現在合成說明中。Neumann作者、Forest Typology2020(v1)題名、DOI、CC BY4.0授權URL及改作標記均保留，未因加資料包而遺失。這是本次新metadata結果，不沿用前輪2549 bytes。

本輪實跑`node tools/video/cli.mjs lint --slug forty-forest-map --json`，exit0，errors0，warnings6。工具估87句、1797spoken units、517.4秒（8:37.4）。六警告為短首章、原數學輸入的四個重用數字，以及第六章06:54–08:25約91秒的open-loop heuristic。這些未被清除或改記PASS；root另處理實際節奏與製作判斷，本收據只確認定位／連結等事實。

章節與時長仍為文字估算，不是實際音訊。本輪未呼叫TTS、未生產音檔、未作旁白批准或發佈動作。
