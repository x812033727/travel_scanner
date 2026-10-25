# ForTy：兩個真實 2020 ROI 的可重現證據

更新日期：2026-10-25。這份文件記錄資料讀取與實算，不是地面驗證、年度變化量測或影片完工收據。對應企劃 `brief.md`，全部原始證據目前在 `/workspace/work/ai-tech-next/forty-demo/`。

## 能支持的成果

**RUN：** 從官方公開COG微量讀取真實五band，產出兩份完整10×10 GeoTIFF與所有原始值；重開小檔並補出第六類、正規化及最大值。**已觀看：** 本次原創資料衍生PNG；不是官方App介面。**CITED：** 官方類別定義、score語義與發布資訊。**未成功SEEN：** 兩個匿名公共App本環境只顯示底圖，沒有ForTy資料層。

獨立審查：`independent-review.md`、`independent-results.json`，73項PASS。審查者重新取同一generation的六個Range，依TIFF tag自行計算offset，再用系統libzstd加Predictor2逐列累加mod256獨立解碼；與新GDAL及兩份crop的各500個原始值一致。這份收據只綁其列出的資料與圖像SHA，不代表後續旁白、中文卡或成片QA通過。

## 正式來源與時間

| 來源 | URL／已核對範圍 |
| --- | --- |
| DeepMind研究介紹 | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ：2026-10-22；說明ForTy、AlphaEarth表示與早期2017–2025逐年序列。 |
| Earth Engine catalog | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ：六類、band順序、Other補數、0–250、10m、未事後校準及官方GCS前綴。 |
| Figshare官方API | https://api.figshare.com/v2/articles/32288616 ：created/published均2026-05-22T23:22:30Z；DOI `10.25452/figshare.plus.32288616.v1`；CC BY4.0。 |
| 正式論文 | https://www.nature.com/articles/s41597-026-08299-5 ：出版者官方索引列2026-10-21。直接頁面遇驗證轉址，未繞過，未假稱完整打開全文。 |
| 基準App | https://nature-trace.projects.earthengine.app/view/forest-typology-2020 ：匿名HTML200，真Google底圖；未見ForTy overlay、年份、legend或score。 |
| 年度App | https://nature-trace.projects.earthengine.app/view/forest-typology ：同上；不能把HTML200當成功資料操作。 |

**2020是資料描述年份；五月是基準資料公開；十月是正式論文與研究介紹／早期年度序列消息。** 本次未讀年度序列的像素，不能把兩例寫成逐年轉換案例。

## 來源物件與微量擷取

官方catalog明列後端前綴 `gs://nature-trace/export_rasters/forest_typology_2020_v1_0/`。本次使用：

```text
https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif
```

| 欄位 | 紀錄 |
| --- | --- |
| 大小 | 7,293,206 bytes，來自GCS metadata與Content-Range |
| generation | `1777582191968217`；獨審以`?generation=1777582191968217`固定重取 |
| GCS metadata md5Hash | `/+qFVW6EBHvCe15/Zjd1SA==`；未下載整物件重算MD5 |
| 來源 | EPSG:32651，五個uint8 band，nodata255，512×512 block |
| affine | `[10,0,317440,0,10,2692000,0,0,1]`；Y步長正，不能沿用負Y顯示假設 |
| 最終擷取 | TIFF標頭及五個所需壓縮tile，六個HTTP206，共160,141資料bytes |
| 未取得 | 整個來源COG、450,067,989-byte Figshare 51R ZIP、全球檔、年度像素 |

| HTTP Range | 回傳資料bytes | SHA-256 |
| --- | ---: | --- |
| `0-65535` | 65536 | `67f858ed4a840e7433ccb5cdcd85b95cf86aa0be433a126a75a4ffcda24484af` |
| `4416787-4449437` | 32651 | `a2cb24199d8d561ca85b694ae7cfdcb46465f30e209855e57313e139409750b1` |
| `6384356-6435997` | 51642 | `125bca7d6028168605a350425525102cf019a0ad15a70706dd5f75c88c9a2e8f` |
| `6803030-6803185` | 156 | `8e9329964025a6447d7ecedca5f4bfa399634778962f807bf710823981a5e291` |
| `6936849-6937609` | 761 | `e768dfb8f2eb20ad4e6dcecb8499005aea491591c1ed449192e17487bbee2f12` |
| `7143959-7153353` | 9395 | `8509481e57cc5c8711de560fa24b51011644fa773a93bbd6ab36bf03587ee84d` |

160,141只計最終資料擷取，不包含早期ZIP尾段探查、metadata、App測試或獨審重取。請勿宣稱這是整個研究的總流量。

直接以GDAL遠端開啟曾遇到其libcurl憑證鏈問題；保留失敗，沒有關閉TLS。成功方法使用既有平台代理與正常CA的requests做受限Range，將確實取得的header／tiles寫到稀疏中間檔，再以本地rasterio讀小窗口。稀疏中間檔未取回的區段是空洞；只交付完整的小ROI供重用，不能把中間檔當完整COG四處取樣。

## 類別與計算規則

| ID | 官方名稱 | 本片繁中稱呼／必要區分 |
| --- | --- | --- |
| 1 | PrimaryForest | 原始林：原生樹種的自然森林，無明顯人為干擾跡象。 |
| 2 | NaturallyRegeneratingForest | 自然更新林：主要透過自然更新形成，含恢復中的次生林；不等於原始林。 |
| 3 | PlantedForest | 人工栽植林：主要經栽植或播種形成；此資料用操作性輪伐期超過40年區分。 |
| 4 | PlantationForest | 林木種植園：集約經營，常見一兩種樹、同齡、規則間距；此資料用40年以內的輪伐期proxy。 |
| 5 | TreeCropsAndAgroforestry | 樹木作物與農林複合：非木材農產品的樹作及混合系統，例如油棕、橡膠、果園。 |
| 6 | OtherLand | 其他土地：還可包括稀疏木本、城市樹木、小樹片等；不等於「完全沒有樹」。 |

來源TIFF沒有文字band description；名稱依官方順序對應，不是假稱從檔案自帶的名稱讀出。計算先轉有號整數，排除255與無效和，避免uint8相減回繞。對有效像素：

```text
other = 250 - sum(stored_five)
six_values = [band1, band2, band3, band4, band5, other]
six_scores = six_values / 250
maximizers = all class IDs with the largest score
display_id = first maximum index + 1  # this video's local rule
```

`display_id`只是本片原創圖的NumPy取首規則；並列時必須保留全部maximizers。未實測官方另行硬分類層的tie規則。官方分數是未事後校準的模型輸出，不能當單點正確率。

## A：固定座標的實算

輸入請求lon121.4、lat24.7；source row4067／col2070。ROI `Window(col_off=2065,row_off=4062,width=10,height=10)`，指定像素在ROI `[5,5]`（從0編號）。它是指定格的中心，**不是偶數10×10窗口的精確幾何中心**。

指定像素中心UTM為338145／2732675；經緯度121.40004092613184／24.700006051424293。完整5×10×10值及變換在 `actual-roi-result.json` 與 `actual-2020-10x10-roi.tif`。

| 計算 | 結果 |
| --- | --- |
| 原始五值 | `[0,248,0,0,0]` |
| 加總 | `0+248+0+0+0=248` |
| Other | `250−248=2` |
| 六分數 | `[0,.992,0,0,0,.008]` |
| 唯一最大者 | ID2，NaturallyRegeneratingForest，自然更新林 |
| 全ROI本地分類 | 100個有效格均為ID2，最大分數範圍.992–.996 |

預期：完整小檔可重新開啟，五值、Other與分類可重算。實際：`reopen-validation.json`與獨立解碼均一致。`.992`不改寫為「99.2%實際判對」。

## B：刻意挑選的低分閱讀練習

使用A讀取時已取得的同一512×512 block：row3584、col2048起。262,144有效格，排除五格邊界後有252,004候選；對各格補六分數，取每格最大值，再找其中最小值。最低為86／250=.344，兩個位置同低；按row-major取第一個。B選樣零額外網路請求。

所選source row4012／col2295；ROI `Window(col_off=2290,row_off=4007,width=10,height=10)`，指定ROI像素仍為`[5,5]`。格心UTM340395／2732125；lon121.42233836084972、lat24.695276083224126。

| 計算 | 結果 |
| --- | --- |
| 原始五值 | `[0,86,0,1,77]` |
| 加總 | `0+86+0+1+77=164` |
| Other | `250−164=86` |
| 六分數 | `[0,.344,0,.004,.308,.344]` |
| 最大者 | ID2與ID6並列，沒有唯一最高 |
| 本圖取首顯示 | ID2；標明這是本地規則 |
| 全ROI本地分類 | ID2有19格、ID5有14格、ID6有67格；2格出現最高分並列 |

B不是隨機抽樣，不是「AI判錯」的地面證據，也不能估台灣或全球錯分率。A與B約差225col／55row，名目投影距離約2.3km；稱「同一已取回block裡的兩個例子」，不用「隔壁一格」。

## 顯示方向、範圍與圖像

每格名目投影面積100m²；每個10×10窗口是100m×100m=10,000m²=1ha的**格網範圍**。不稱已確認一公頃森林、現地面積或保育成效。

源affine正Y；圖以`origin=lower`令row0在下、northing向上，east向右。圖片是原創資料圖，無衛星底圖；不是現地照片或已成功操作的官方App畫面。

已實際觀看的圖：`real-forty-2020-two-rois.png`（267,347 bytes），另有同源SVG（182,667 bytes）。A全綠，B有黃／橙／綠；兩指定像素紅框與B的.344並列棒圖可讀。此為英文研究樣圖；正式片要拆為中文狀態，保留英文類名對照、數值及改作署名。

## 可重現命令與工件

這些是已寫好並執行的自有腳本，沒有執行未檢視的外部repo程式。一般觀眾不需跟著安裝；資料包提供想重算的人使用。以現有隔離環境重跑：

```bash
cd /workspace/work/ai-tech-next/forty-demo
venv/bin/python read_actual_roi.py
venv/bin/python find_uncertain_roi.py
python render_real_data_figure.py
venv/bin/python independent_check.py
```

最後一個是獨立審查者的可重跑腳本，不把它列成本作者自評。環境：Python3.12.14；rasterio1.5.2、GDAL3.12.2；requests2.34.2；tifffile2026.10.15；NumPy2.5.4。圖使用已存在的matplotlib／PIL。重跑網路步驟前保留平台代理、TLS與固定編輯UA，不關驗證、不繞403。

| 工件 | 大小／用途／SHA-256 |
| --- | --- |
| `actual-2020-10x10-roi.tif` | 585 bytes；完整A小檔；`05b05f2ea81849d620036994190d24d500684cad1dc70d402925074f4725f9d7` |
| `actual-2020-uncertain-10x10-roi.tif` | 747 bytes；完整B小檔；`cecd23a1aab413fa4dbeb339e2924793a3e86262f560f70a6549298780092271` |
| `actual-roi-result.json` | 原始五band、100格、Range與座標；`867aa186e25b6a59ea5dcf32a100646d68497fa064d177e674f2674f42a362ba` |
| `actual-uncertain-roi-result.json` | B選樣、100格、tie；`4ebd1c412fe85576277d0b8c4ab96fce31254abe41b6c07ba3ca203220db101a` |
| `real-forty-2020-two-rois.png` | 原創衍生圖；`2d08ccf33eff293e4b8040a9cfa940612dc2d976f6a3f485c104f56636719190` |
| `real-forty-2020-two-rois.svg` | 同源向量圖；`8ee820b92e0734b5c905579d0c118ed109ac9051dab172c9d0d9eadad683de66` |
| `manifest.json` | 原擷取與圖檔manifest；不含之後新增的獨立審查檔，審查輸入hash另見`independent-results.json`。 |
| `app-check/README.md` | 匿名App操作方法、兩張實際底圖截圖與network紀錄；ForTy overlay未成功，不能拿來演成功操作。 |

## 引用與改作

Neumann, Maxim; Raichuk, Anton; Potapov, Peter; Lesiv, Myroslava; Overlan, Matthew; Rey, Melanie; et al. (2026). *Forest Typology 2020 (v1).* Figshare+. Dataset. https://doi.org/10.25452/figshare.plus.32288616.v1 . **CC BY4.0**。改作：裁切、Other補數、取首argmax與圖表。

不用catalog的placeholder署名。資料CC BY不自動包含Google Earth／Maxar／Airbus圖像。`google-deepmind/forest_typology/forty_v1/` 是不同的2025訓練benchmark（八類及unknown、CC BY-SA4.0），不混入本片資料或授權。

## 尚未完成的製作工作

兩個資料成果可以作為正片基礎。協調者已在本片`assets/`產出`pixel-comparison.svg`、`roi-a-scores.svg`、`roi-b-scores.svg`及來源manifest，並實際render觀看；它們是真實模型輸出的繁中衍生圖，不是地面真值。其餘逐步中文卡、七章完整旁白、字幕、八外語翻譯與配音、實際音長、縮圖及媒體QA尚待原生製作流程。這份證據不含TTS呼叫，不把企劃估時說成實測片長。
