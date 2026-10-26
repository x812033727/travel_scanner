# ForTy 正式稿獨立事實查核 R1

查核日期：2026-10-25（Asia/Taipei）。查核者 news_verify，未參與正式文稿撰寫。本輪只寫本收據，不修改 video.json、claims.md、原始資料、圖卡或音訊。

**結論：REVISE。正文、圖卡與數據未發現實質事實錯誤；有 1 項發布 metadata 必修，修好前不稱整稿已驗證。**

綁定的原稿：

- video.json SHA-256：`fd713ae54b271d74984c2c633f103d05caff1dc758ef77de67f9c588311420a2`
- claims.md SHA-256：`e8b15b7cb0a26e43bdc5a30468363a4dcafe65b826850802156d1e9d5901d98c`
- 96 場、100 句、7 章。100 個 claim 的實際 text／line ID／scene ID 與 claims.md 逐一相符。所有 say 均未填，沒有另一套改寫旁白待核對。

## 必修 R1-M1：把資料署名與授權連結送到觀眾看得到的說明欄

位置：`video.json youtube.description`（原稿第25行）；並影響後續所有語言說明欄。

現況：五張 SVG 頁腳有資料作者、版本、文字 DOI、CC BY4.0 名稱與改作標記，但沒有 license URL。video.assets 的 source/license 是內部資料欄位；不能假定它們一定進入上架說明。已唯讀核對原生 `tools/video/core/metadata.mjs`：`creditedAssets` 只採有 author 或 url 的 asset，目前五筆均只有 path/source/license，因此 `pictureCredits` 不會輸出它們。`composeDescription` 會列 doc.sources，但現有五個 sources 也沒有 DOI 及 license URL。

第一手依據：Figshare API 的 license.name=CC BY4.0、license.url=`https://creativecommons.org/licenses/by/4.0/`，HTTP200；同日正常編輯 UA 開啟 Creative Commons 授權頁亦 HTTP200。授權頁定位短引：`provide a link to the license`。此處不是要求改旁白或新增法律解釋，只補已確認且實際使用的資料署名。

最小建議，在 youtube.description 追加：

> 資料：Neumann 等（2026），Forest Typology 2020（v1），https://doi.org/10.25452/figshare.plus.32288616.v1 。授權：CC BY 4.0，https://creativecommons.org/licenses/by/4.0/ 。本片改作：裁切、推導其他土地、取首分類與重繪。

修後驗收：保留新 video SHA、重跑原生 lint，並唯讀 compose 實際上架說明，確認 DOI、license URL、作者與改作標記都在可交付文字中。外語 metadata 應保留同一來源與授權連結。本輪收據仍保留原稿 REVISE；不把原收據靜默改為 PASS。

## 證據來源與讀取界線

本輪重讀本日已取得的官方原文，不以作者 claims.md 自證。來源快照及 HTTP 收據在 `/workspace/work/ai-tech-next/verify-research.*`，完整事實表在本片 source-facts.md。沒有重複大範圍搜尋、付費、登入或 API 寫入。

| 代碼 | Primary URL | 實際取得範圍／HTTP狀態 |
| --- | --- | --- |
| B | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ | 2026-10-25 HTTP200 原文；10/22 date-only、年度早期序列、輸入／訓練概述 |
| C | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection | 同日 HTTP200 原文；六類操作定義、40年 proxy、分數／band／尺度及校準限制 |
| F | https://api.figshare.com/v2/articles/32288616 | 同日 HTTP200 API；發布時間、版本、band順序、補數、除法、授權與 DOI。人類網頁403，不把 API200 寫成人類網頁200 |
| N | https://www.nature.com/articles/s41597-026-08299-5 | 只採出版者 metadata／abstract 的官方索引內容；直接頁遇驗證轉址，沒有宣稱 HTTP200 全文讀取或全文已讀 |
| G | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif | 本日六次206 Range的獨立解碼收據；只讀已取回tile，非整個COG或全圖重驗 |
| L | https://creativecommons.org/licenses/by/4.0/ | 本輪正常編輯UA開啟HTTP200；授權連結與改作署名要求 |

## 重要事實與數據的本輪重核

1. **日期與新聞範圍成立。** c1/8aw6 是10/22研究介紹；c85/rume 正確保留2020基準五月已公開；API原始時間2026-05-22T23:22:30Z（台北5/23）。c86/pvkj 的10/21是正式論文出版metadata，c87/ncx4 另分2017–2025早期年度序列。沒有把各日期混成首次公布，也未補官方未列時區。
2. **六類定義成立。** c9–22與相應表格依官方順序。第3類輪伐期>40、第4類≤40；c14/njnw明說本資料操作定義，c15/v9fh與c18/3x99明說輪伐期不等於當前樹齡；c95/ci5j保留歷史／用途另查參考。沒有把 proxy 當成衛星直接知道經營計畫。OtherLand含部分有樹土地，不是裸地同義詞。
3. **模型輸入敘述有原文依據。** c25–28：AlphaEarth多年觀測表示是重要輸入之一，官方 blog 明列 planting patterns／growth cycles／harvest rhythms、結構和季節線索，以及專家、國家／區域與難例標註來源。沒有冒稱本次重訓、重跑全球模型或從單張照片直接量到經營史。
4. **本輪重新讀 repo data 的完整原始數組並重算。** A 的 `[0,248,0,0,0]` 和248，Other2，六分數`[0,.992,0,0,0,.008]`，唯一最高第2類。B 的`[0,86,0,1,77]`和164，Other86，六分數`[0,.344,0,.004,.308,.344]`，第2及6類並列。六分數皆加總1，存值均有效。不是只依舊73PASS判定正式稿。
5. **本地顯示規則與刻意選樣成立。** c61/appe、c62/beg8先揭露同一區塊刻意找低最大分數，不能估全圖精度；c77/wnrz明說我們衍生圖取第一個最高者，沒有宣稱官方硬分類層也採同一 tie 規則。兩ROI不被說成相鄰格。完整B選樣範圍、五格邊界與同最低時取row-major首值在資料紀錄；正文未擴大成全台／全球最不確定位置。
6. **座標和格網範圍成立。** A畫面121.4E/24.7N是請求座標；SVG另標指定像素中心121.40004093E/24.70000605N。B中心121.42233836E/24.69527608N。來源正Y步長對應SVG row0在下、row9在上；紅框是[5,5]，沒有稱偶數窗口精確幾何中心。10m被標名目輸出尺度，正文無森林面積或逐樹定位宣稱。
7. **校準說明成立。** c92/vb62所述未事後校準出自C。c93/8m2e對獨立參考的解釋是該限制的合理說明，不是聲稱已完成校準或只要一份參考就足夠。c94/bs4s明確否定0.992等於單格99.2%判對機率；未把總和1當校準證據。正式稿沒有新增全域accuracy或F1數字，亦未利用未讀Nature全文延伸方法。
8. **年份與證據範圍成立。** 說明欄及c96/88pk只稱2020版本兩個真實模型輸出；年度段是應保存欄位的編輯建議，並未聲稱拿到年度像素或測到真實地類變化。
9. **CTA沒有不存在的來源承諾。** complete-pixel-record只邀請留年份／類別／完整分數、留言環境用途、訂閱；未承諾文章、下載包、說明欄連結或已上線資料頁。來源本身確實存在；只剩R1-M1補觀眾可見署名。

本輪重讀A JSON SHA：`867aa186e25b6a59ea5dcf32a100646d68497fa064d177e674f2674f42a362ba`；B JSON SHA：`4ebd1c412fe85576277d0b8c4ab96fce31254abe41b6c07ba3ca203220db101a`，均與獨立資料查核原始輸入及圖卡manifest一致。

## 圖卡與metadata的獨立補核

另一唯讀代理 guard_review 另查五SVG與兩份JSON，並回報具體格序／座標／比例結果。A六分數與B六分數順序及800單位長條比例吻合；B100格逐格對class_ids，類別數19／14／67；row0在y594、row9在y180，符合來源正northing步長；紅框row5/col5。comparison兩組100格及中心座標一致；兩點投影距離2316.25m，可說約2.3km，但正文沒有必要唸此距離。所有五圖均明列2020與改作歸屬，未使用衛星底圖；圖卡hash全部吻合manifest。

這些是SVG源資料與版面座標查核，**不是尚未產出的最終成片視覺QA**；不得用本收據取代render後實際觀看、字幕與音檢。

## 聽眾／工具檢查（報告，不改文風）

- 100句全部≤40字；沒有say分歧、旁白URL或括號。Latin專名只有DeepMind／ForTy／AlphaEarth／AI；本輪原生lint沒有字典缺詞錯誤。
- 沒有「經查證／根據官方文件／本影片」式驗證旁白。B分數圖在並列引入後；comparison在B完整計算和本地取首之後，未先洩露B結果。
- 站主觀點與brief一致：用定義和真實模型輸出教會可重算讀法；沒有私人現地經驗、土地用途認定或法規建議。
- 實跑 `node tools/video/cli.mjs lint --slug forty-forest-map --json`，cwd為本worktree，exit0，errors0，warnings6。六警告為已核准約25秒首章、完整算式必須重用248／250／86／77的四項、標題「怎麼讀」heuristic一項，均不是新事實錯誤。本收據不對文風或剪輯作PASS判決。
- 工具估9.7056分鐘、2013spoken units、100句；這不是實際音訊時長。七章估時00:00／00:25／02:52／04:09／05:49／07:57／09:30。

**必修數：1（metadata署名／授權連結），正文事實改動數：0；NOT FOUND正文事實：0。** 未直接修改任何原稿。第二輪「超過3個事實改動」規則本輪未觸發；仍須對R1-M1修訂與新SHA回讀並重跑lint，不能把本R1當PASS。未執行TTS、媒體生成、旁白批准或發布。

## 逐句完整核對表

下表保留全部100句原文、實際line/scene及作者來源對照。CONFIRMED涵蓋直接來源、真實輸出重算及明標編輯推論；純提問／CTA列OUT OF SCOPE，不把它們冒充官方實驗。Before→After均為原句→不改；唯一待改是上列R1-M1。每句所在scene.data也另列於表後逐場核對。

| # | Original claim | Actual scene / line | Evidence URL / status | Verdict | Before -> After / basis |
| --- | --- | --- | --- | --- | --- |
| c1 | 本週十月二十二日，DeepMind介紹了ForTy森林地圖。 | first-grid / 8aw6 | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F03 |
| c2 | 這個二〇二〇年資料的格子，被塗成自然更新林。 | first-label / gngj | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c3 | 你可能會問：有樹，不就好了？ | viewer-question / ep85 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c4 | 讀類名、補分數，才看得到顏色沒寫完的資訊。 | read-more / jw6i | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c5 | 跟著兩個真實格子，把五個值還原成六類結果。 | one-promise / 5ur9 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c6 | 開頭那個自然更新林，描述的是森林怎麼形成。 | label-meaning / m2p6 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F06 |
| c7 | 你看一般地圖的綠色，通常先想到那裡有樹。 | cover-or-type / mu7d | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c8 | 但要讀這個類別，就得把覆蓋和土地用途分開。 | cover-or-type / pwc4 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c9 | 先看原始林，它要求原生樹種，沒有可見人為干擾。 | primary-definition / erqz | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F05 |
| c10 | 自然更新林則以自然長回來為主，也含恢復中的次生林。 | regeneration-definition / t4w3 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F06 |
| c11 | 所以這格的類名，沒有替它宣告從未受過干擾。 | regeneration-choice / zpjv | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c12 | 如果森林是人種的，又要怎麼放進這張表？ | planted-question / 66nz | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c13 | 人工栽植林主要由栽植或播種形成。 | planted-origin / 3pse | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F07 |
| c14 | 這份資料把輪伐期超過四十年，列入這一類的操作定義。 | planted-cycle / njnw | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F07 |
| c15 | 輪伐期說的是從種下、經營到再次採收的安排，和這棵樹現在幾歲不同。 | rotation-meaning / v9fh | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c16 | 林木種植園的經營更密集，常有少數樹種、同齡和規則間距。 | plantation-pattern / 7id9 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F08 |
| c17 | 它採用的輪伐期條件，是四十年或以下。 | plantation-cycle / 2vcb | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F08 |
| c18 | 這個門檻分的是資料類型，不能拿樹齡直接代替。 | cycle-is-not-age / 3x99 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c19 | 至於油棕、橡膠和果園，會進到樹木作物與農林複合。 | tree-crop-definition / yiya | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F09 |
| c20 | 這裡關心的是非木材的農產品，不能只看枝葉夠不夠綠。 | crop-purpose / sd2k | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F09 |
| c21 | 剩下的其他土地，也可能包括城市樹木或稀疏木本。 | other-definition / rrgq | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F10 |
| c22 | 這個類別能包含有樹的土地；看見其他土地時，不能直接改寫成裸地。 | other-annotation / icp9 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c23 | 把這六個名稱固定下來，後面每個數都要依序對回去。 | keep-order / fbc5 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c24 | 可是隔著衛星影像，模型能從哪裡讀出這些差別？ | signal-question / gsa7 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c25 | 模型的重要輸入之一，是AlphaEarth把多年衛星觀測濃縮成的表示。 | alphaearth-input / 9wmz | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F12 |
| c26 | ForTy再利用這些表示，找種植形狀、季節和生長週期的線索。 | signal-chain / jkby | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F12 |
| c27 | 訓練還要搭配專家與區域資料標記的地點，讓觀測線索對回土地類型。 | training-reference / 5nt9 | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F13 |
| c28 | 所以模型讀出的是這些訊號支持的類別分數。 | type-scores / 528p | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F12 |
| c29 | 我們手上這個格子的分數，就藏在五個整數裡。 | stored-question / m8cb | https://api.figshare.com/v2/articles/32288616 ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F15 |
| c30 | 先在這份像素紀錄填上資料年份和位置。 | pixel-record / p2ry | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c31 | 位置用東經一百二十一點四、北緯二十四點七。 | requested-coordinate / u5js | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c32 | 指定格周圍取十乘十格，紅框只標出我們要算的那一格。 | a-window / 7732 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c33 | 十公尺網格是輸出尺度，不是每棵樹的定位清單。 | grid-scale / yi97 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F14 |
| c34 | 讀值之前，把前五類的順序固定在這張表上。 | band-order / 2k27 | https://api.figshare.com/v2/articles/32288616 ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F15 |
| c35 | 第一欄到第五欄，依序對應剛才那些森林和樹作類型。 | position-matters / us3c | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c36 | 零是有效分數的儲存值，兩百五十五才是無資料記號。 | valid-or-missing / vk36 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c37 | 遇到無資料就先停下，不把它拿進補數計算。 | missing-action / gfes | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c38 | 這一格的五個值都有資料，也都在有效範圍內，可以繼續補第六類。 | a-valid / e826 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c39 | 依序讀到零、兩百四十八、零、零、零。 | a-five-input / bxdi | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c40 | 數值越大，表示這類得到的模型分數越高；它們不是面積或樹木的棵數。 | stored-value-meaning / anxa | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c41 | 欄位名稱要跟著值走，單看一串數字分不出是哪一類。 | keep-value-label / svhy | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c42 | 可是表上有六類，這裡為什麼只存五個值？ | sixth-value-question / 3gwz | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c43 | 第六類留在總量裡，用兩百五十扣回來。 | residual-rule / 7iv8 | https://api.figshare.com/v2/articles/32288616 ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F15 |
| c44 | 先把這格的五個值相加，總和是兩百四十八。 | a-sum / up9r | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c45 | 兩百五十減兩百四十八，其他土地得到二。 | a-other / 3p97 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c46 | 補回這個二，六類才都到齊。 | a-six-complete / 8qmt | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c47 | 完整值依序是零、兩百四十八、零、零、零、二。 | a-six-values / jd7t | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c48 | 補完後先檢查，六個值都要在零到兩百五十之間，總和也要回到兩百五十。 | six-value-check / 4av2 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c49 | 這些儲存值，要怎麼換成零到一的模型分數？ | normalization-rule / 8hpb | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c50 | 每一項都除以兩百五十，自然更新林的兩百四十八就得到零點九九二。 | a-regeneration-score / ywu9 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c51 | 其他土地的二，除完是零點零零八。 | a-other-score / u362 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c52 | 原始林、人工栽植林、林木種植園和樹作類，這格都是零。 | a-zero-scores / eym7 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c53 | 把六項分數加起來，剛好是一。 | a-total / k3i2 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c54 | 這是同一個總量的拆分，不是六次互不相關的打分。 | shared-total / p9sg | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c55 | 比較這六項，只有自然更新林最高。 | a-unique / dkq3 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c56 | 選最大值來畫分類，紅框格就呈現它的綠色。 | a-score-result / w86h | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c57 | 這個動作叫取最大值，選的是類別，不會留下所有分數。 | argmax-action / wh49 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c58 | 所以在這份紀錄上，寫自然更新林唯一最高，附上完整六分數。 | a-annotation / 6ybg | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c59 | 只看綠格能讀類名，展開數值才知道這格的分布。 | a-simple-expanded / xxju | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c60 | 另一個同來源格子，也能這樣乾脆地選出來嗎？ | b-forward / endc | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c61 | 換到同一區塊的另一格，這次刻意挑最高分最低的位置。 | b-selected-grid / appe | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c62 | 這是閱讀練習，不是拿隨機樣本估整張圖的精度。 | b-selection-purpose / beg8 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c63 | 沿用相同類別順序，五值是零、八十六、零、一、七十七。 | b-five-input / 54sx | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c64 | 八十六加一再加七十七，總和是一百六十四。 | b-sum / mfsh | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c65 | 兩百五十減一百六十四，其他土地得到八十六。 | b-other / 578j | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c66 | 六類值依序是零、八十六、零、一、七十七、八十六。 | b-six-values / siyh | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c67 | 每一項除以兩百五十，現在把各類攤開來讀。 | b-scale / 8mtz | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c68 | 自然更新林的八十六，變成零點三四四。 | b-regeneration-score / 97h6 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c69 | 林木種植園的一，變成零點零零四。 | b-plantation-score / 4amm | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c70 | 樹木作物與農林複合的七十七，變成零點三零八。 | b-crop-score / ux8j | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c71 | 其他土地同樣是八十六，所以也是零點三四四。 | b-other-score / mrsv | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c72 | 原始林和人工栽植林都是零。 | b-zero-scores / y64h | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c73 | 等等，這格有兩項並列最高。 | b-tie-reveal / jbsn | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c74 | 自然更新林和其他土地，沒有誰比另一個更高。 | b-score-result / n6j6 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c75 | 如果只能塗一種顏色，畫面會選哪一個？ | one-color-question / 8k4a | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c76 | 只選一個顯示，是把六項分數壓成一個標籤；並列者不會因此自動分出高低。 | label-compression / z33x | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c77 | 我們這張衍生圖，用類別順序取第一個最高者。 | local-tie-rule / wnrz | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c78 | 所以它也塗成自然更新林的顏色。 | b-green-label / ywz8 | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; B original JSON re-read; deliberate selection, tie and local first-maximum verified |
| c79 | 還記得開頭那個綠格嗎，它的最高者只有一個。 | a-b-comparison / ww8v | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; A original JSON re-read and arithmetic / coordinate / class display verified |
| c80 | 把兩格擺在一起，同樣的顏色就不再是同樣的資訊。 | a-b-comparison / mx7g | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c81 | 你的紀錄要留下自然更新林和其他土地並列，再註明取首顯示。 | b-annotation / 7qfx | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c82 | 需要比較結果時，就讀這條註記，而不是讓顏色替你省略答案。 | use-annotation / hbci | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c83 | 那把這種讀法用到新年度，資料年又該放在哪裡？ | annual-forward / sbkg | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c84 | 把年份放進每一列紀錄，你才有辦法接上新的年度資料。 | year-in-record / 6ss6 | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c85 | 二〇二〇基準資料在五月就已公開，不能把它當成本週才出現。 | baseline-release / rume | https://api.figshare.com/v2/articles/32288616 ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F01 |
| c86 | 正式資料論文在十月二十一日出版。 | paper-date / pvkj | https://www.nature.com/articles/s41597-026-08299-5 ; official metadata/abstract only; direct challenge | CONFIRMED | Unchanged; CITED：source-facts.md F02 |
| c87 | 開頭那次介紹，另外分享二〇一七到二〇二五年的早期年度序列。 | annual-release / ncx4 | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F03 |
| c88 | 一個位置可以多出不同年份的輸出，分類問題也能沿時間展開。 | time-dimension / j5kv | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c89 | 要比較同一處，先固定位置，再保留每年的類別順序和六分數。 | annual-reading-fields / nqyj | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c90 | 只換顏色，會把剛才看到的並列和分數差距藏起來。 | color-change-reading / wfb2 | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c91 | 這裡還有一個容易誤讀的地方：零點九九二，究竟代表什麼？ | score-question / upmh | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c92 | 它是模型分數，還沒有做事後的機率校準。 | uncalibrated-score / vb62 | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F19 |
| c93 | 要把分數當成正確機率，還得用獨立參考，檢查分數和真實結果是否相符。 | calibration-reference / 8m2e | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F19 |
| c94 | 所以不能直接說，這格有百分之九十九點二的機率判對。 | not-correctness / bs4s | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F19 |
| c95 | 模型看見的是觀測線索，土地歷史和經營用途還要對照參考資料。 | reference-needed / ci5j | https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; CITED：source-facts.md F11 |
| c96 | 同樣地，二〇二〇的兩格，只能回答這個版本的輸出長什麼樣。 | baseline-scope / 88pk | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c97 | 想追年度變化，就把對應年份的輸出和獨立參考一起帶進來。 | annual-next-input / bu6j | https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ ; 200 (2026-10-25 official snapshot) | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c98 | 還記得那個綠格，六個分數才把它讀完整。 | complete-pixel-record / hr4b | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | CONFIRMED | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c99 | 你常用地圖看哪種環境？ | complete-pixel-record / 4w7g | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |
| c100 | 訂閱，一起讀懂AI的真實輸出。 | complete-pixel-record / 39nc | https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif ; 206 Range + local JSON re-read | OUT OF SCOPE (question / CTA) | Unchanged; Original editorial question, instruction or inference; no additional measured result asserted |

## Complete scene.data review (96 scenes)

Each row is the actual scene data checked with its associated claim(s). SVGs were separately checked against both complete ROI JSON arrays and the manifest. Prompts and composition choices carry no extra measured fact. R1-M1 is the only unresolved metadata issue.

| Scene | Template | Actual data | Verdict / scope |
| --- | --- | --- | --- |
| first-grid | diagram | {"svg":"docs/videos/forty-forest-map/assets/roi-a-grid.svg","caption":"ForTy 2020｜公開模型輸出；本片裁切與計算","key":"2020模型輸出，從這一格開始"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| first-label | big | {"text":"自然更新林","key":"A格的衍生分類結果","kicker":"A格｜2020基準"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| viewer-question | big | {"text":"有樹，不就好了？","key":"讀類型，能多看見什麼"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| read-more | big | {"text":"把色塊讀完整","key":"類名與分數，一起讀"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| one-promise | big | {"text":"五個值，六類結果","key":"跟著兩個真實格子親手算"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| label-meaning | big | {"text":"森林怎麼形成","key":"開頭的類名，有它的定義"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| cover-or-type | compare | {"left":{"heading":"樹木覆蓋","points":["先看有沒有樹"]},"right":{"heading":"ForTy類型","points":["再分形成方式與用途"]},"keys":["先看見樹木覆蓋","把同一片綠，讀到土地類型"],"source":"編輯判讀｜同一份真實輸出"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| primary-definition | table | {"columns":["ID","類名","形成與歷史"],"rows":[["1","原始林","原生樹種；無可見人為干擾"]],"key":"PrimaryForest","source":"官方資料目錄｜2026-10-25","title":"自然形成的兩種類別"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| regeneration-definition | table | {"columns":["ID","類名","形成與歷史"],"rows":[["2","自然更新林","自然長回；包括恢復中的次生林"]],"key":"NaturallyRegeneratingForest","source":"官方資料目錄｜2026-10-25","title":"自然形成的兩種類別"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| regeneration-choice | big | {"text":"自然更新≠從未干擾","key":"讀類名，不替它補上歷史"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| planted-question | big | {"text":"人種的，又怎麼分？","key":"分類還要讀經營方式"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| planted-origin | table | {"columns":["ID","類名","建立方式"],"rows":[["3","人工栽植林","主要由栽植或播種形成"]],"key":"PlantedForest","source":"官方資料目錄｜2026-10-25","title":"人工建立的森林"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| planted-cycle | big | {"text":"超過40年","key":"這份資料的操作性分類條件","kicker":"人工栽植林"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| rotation-meaning | big | {"text":"輪伐期，看經營週期","key":"種植到再次採收的安排"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| plantation-pattern | table | {"columns":["ID","類名","常見特徵"],"rows":[["4","林木種植園","少數樹種；同齡；規則間距"]],"key":"PlantationForest","source":"官方資料目錄｜2026-10-25","title":"集約經營的類型"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| plantation-cycle | big | {"text":"40年或以下","key":"同一套資料，另一側的輪伐條件","kicker":"林木種植園"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| cycle-is-not-age | big | {"text":"輪伐期≠樹齡","key":"分類條件要讀對"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| tree-crop-definition | table | {"columns":["ID","類名","例子"],"rows":[["5","樹木作物與農林複合","油棕、橡膠、果園"]],"key":"TreeCropsAndAgroforestry","source":"官方資料目錄｜2026-10-25","title":"有樹的農業系統"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| crop-purpose | big | {"text":"讀用途，別只看綠色","key":"非木材農產品的樹木作物"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| other-definition | table | {"columns":["ID","類名","包含範圍"],"rows":[["6","其他土地","城市樹木、稀疏木本等"]],"key":"OtherLand","source":"官方資料目錄｜2026-10-25","title":"最後一類也可能有樹"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| other-annotation | big | {"text":"其他土地，不直接改成裸地","key":"依類別定義，保留它的範圍"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| keep-order | big | {"text":"把六類順序固定","key":"後面每個數，都要對回類名"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| signal-question | big | {"text":"衛星看得出差別？","key":"模型需要哪些可觀測線索"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| alphaearth-input | big | {"text":"多年觀測的表示","key":"AlphaEarth｜重要輸入之一","sub":"把觀測整理成分類模型可用的特徵"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| signal-chain | steps | {"steps":[{"title":"衛星觀測","detail":"結構、季節與生長線索"},{"title":"ForTy分類","detail":"利用表示推測類型"}],"key":"觀測線索，走向類別分數","source":"DeepMind研究介紹｜2026-10-22"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| training-reference | big | {"text":"線索需要參考答案","key":"標註地點，把訊號對回類型"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| type-scores | big | {"text":"模型輸出類別分數","key":"它讀的是觀測訊號"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| stored-question | big | {"text":"分數藏在五個整數裡","key":"同一格，開始拆開資料"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| pixel-record | table | {"columns":["欄位","A格輸入"],"rows":[["資料年","2020 v1"],["位置","121.4°E，24.7°N"]],"key":"年份與位置，和數值一起保存","source":"2020公開資料實算｜2026-10-25｜A格","title":"先把位置留在紀錄"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| requested-coordinate | big | {"text":"121.4°E，24.7°N","key":"定位A格的請求座標","kicker":"A格｜真實輸入"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-window | diagram | {"svg":"docs/videos/forty-forest-map/assets/roi-a-grid.svg","caption":"ForTy 2020｜公開模型輸出；本片裁切與計算","key":"紅框是指定格，並非整個窗口"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| grid-scale | big | {"text":"10公尺網格","key":"這是輸出格網的名目尺度"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| band-order | table | {"columns":["位置","對應類別"],"rows":[["1／2","原始林／自然更新林"],["3／4","人工栽植林／林木種植園"],["5","樹木作物與農林複合"]],"key":"先固定順序，再讀五個值","source":"官方資料目錄｜2026-10-25","title":"前五類依序對應"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| position-matters | big | {"text":"數值要帶著類名","key":"同一串數字，不能任意換欄"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| valid-or-missing | compare | {"left":{"heading":"0–250","points":["有效儲存值","零也有意義"]},"right":{"heading":"255","points":["無資料記號","排除後再計算"]},"key":"零是有效值；255是無資料","source":"2020公開資料實算｜2026-10-25｜A格"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| missing-action | big | {"text":"無資料就先停下","key":"不要把255帶進補數算式"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-valid | big | {"text":"五個值都有資料","key":"指定格可以進入實算"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-five-input | table | {"columns":["原始林","自然更新","人工栽植","種植園","樹作農林"],"rows":[["0","248","0","0","0"]],"key":"五個儲存值，依官方順序","source":"2020公開資料實算｜2026-10-25｜A格","title":"A格的五個真實值"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| stored-value-meaning | big | {"text":"儲存值越大，模型分數越高","key":"數值不是面積，也不是樹木棵數"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| keep-value-label | big | {"text":"數字和欄位一起讀","key":"不要把248移到別的類別"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| sixth-value-question | big | {"text":"第六類在哪裡？","key":"表有六類，檔案只存五值"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| residual-rule | big | {"text":"250−前五類總和","key":"其他土地，用補數取得"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-sum | big | {"text":"0+248+0+0+0=248","key":"先把A格的五個值相加","kicker":"A格｜加總"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-other | big | {"text":"250−248=2","key":"A格的其他土地，補回2","kicker":"A格｜補數"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-six-complete | big | {"text":"補回第六類","key":"六類現在全部有值"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-six-values | table | {"columns":["ID","類別","完整儲存值"],"rows":[["1","原始林","0"],["2","自然更新林","248"],["3","人工栽植林","0"],["4","林木種植園","0"],["5","樹木作物與農林複合","0"],["6","其他土地","2"]],"key":"前五值後面，接上其他土地","source":"2020公開資料實算｜2026-10-25｜A格"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| six-value-check | big | {"text":"補完，再檢查總量","key":"六值有效，而且加總回到250"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| normalization-rule | big | {"text":"每一項÷250","key":"把儲存值放到0–1刻度"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-regeneration-score | big | {"text":"248÷250=0.992","key":"A格｜自然更新林"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-other-score | big | {"text":"2÷250=0.008","key":"A格｜其他土地"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-zero-scores | table | {"columns":["類別","分數"],"rows":[["原始林","0"],["人工栽植林","0"],["林木種植園","0"],["樹木作物與農林複合","0"]],"key":"這一格，其餘四類都是零","source":"2020公開資料實算｜2026-10-25｜A格","title":"A格的其餘四類"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-total | big | {"text":"0.992+0.008=1","key":"六類分數，共用同一總量"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| shared-total | big | {"text":"一個總量的拆分","key":"類別之間，要一起讀"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-unique | big | {"text":"唯一最高：自然更新林","key":"A格的分數，只有一個最大者"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-score-result | diagram | {"svg":"docs/videos/forty-forest-map/assets/roi-a-scores.svg","caption":"ForTy 2020｜公開模型輸出；本片裁切與計算","key":"取最大值，得到A格的衍生類別"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| argmax-action | big | {"text":"選出類別，留下分數","key":"取最大值是顯示時的一個選擇"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-annotation | table | {"columns":["欄位","內容"],"rows":[["結果","自然更新林唯一最高"],["分數","0.992；完整六分數附後"]],"key":"類名、最高者、完整分數一起留","source":"2020公開資料實算｜2026-10-25｜A格","title":"把A格寫成可用紀錄"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-simple-expanded | compare | {"left":{"heading":"只看色塊","points":["讀到一個類名"]},"right":{"heading":"展開同一格的值","points":["讀到六類分數分布"]},"key":"同一個輸入，展開被色塊省略的資訊","source":"2020公開資料實算｜2026-10-25｜A格"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-forward | big | {"text":"另一格，也這麼明確？","key":"同一份資料，換一個實際輸出"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-selected-grid | diagram | {"svg":"docs/videos/forty-forest-map/assets/roi-b-grid.svg","caption":"ForTy 2020｜公開模型輸出；本片裁切與計算","key":"B格｜刻意選低最大分數的閱讀例"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-selection-purpose | big | {"text":"刻意選樣，練習讀分數","key":"B不是隨機精度樣本"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-five-input | table | {"columns":["原始林","自然更新","人工栽植","種植園","樹作農林"],"rows":[["0","86","0","1","77"]],"key":"沿用同一類別順序，讀B格","source":"2020公開資料實算｜2026-10-25｜B格","title":"B格的五個真實值"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-sum | big | {"text":"86+1+77=164","key":"零不改變加總，總和164","kicker":"B格｜加總"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-other | big | {"text":"250−164=86","key":"B格的其他土地，補回86","kicker":"B格｜補數"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-six-values | table | {"columns":["ID","類別","完整儲存值"],"rows":[["1","原始林","0"],["2","自然更新林","86"],["3","人工栽植林","0"],["4","林木種植園","1"],["5","樹木作物與農林複合","77"],["6","其他土地","86"]],"key":"其他土地補回86，六類完整","source":"2020公開資料實算｜2026-10-25｜B格"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-scale | big | {"text":"每一項÷250","key":"B格也換到同一個分數刻度"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-regeneration-score | big | {"text":"86÷250=0.344","key":"B格｜自然更新林"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-plantation-score | big | {"text":"1÷250=0.004","key":"B格｜林木種植園"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-crop-score | big | {"text":"77÷250=0.308","key":"B格｜樹木作物與農林複合"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-other-score | big | {"text":"86÷250=0.344","key":"B格｜其他土地"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-zero-scores | table | {"columns":["類別","分數"],"rows":[["原始林","0"],["人工栽植林","0"]],"key":"另外兩類，在這一格都是零","source":"2020公開資料實算｜2026-10-25｜B格","title":"B格的另外兩類"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-tie-reveal | big | {"text":"兩項並列最高","key":"這一次，沒有唯一最高者"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-score-result | diagram | {"svg":"docs/videos/forty-forest-map/assets/roi-b-scores.svg","caption":"ForTy 2020｜公開模型輸出；本片裁切與計算","key":"自然更新林與其他土地，同為0.344"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| one-color-question | big | {"text":"只能塗一色，選誰？","key":"顯示需要再做一個選擇"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| label-compression | big | {"text":"顯示一類，不會解開並列","key":"六分數縮成一個標籤時的選擇"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| local-tie-rule | steps | {"steps":[{"title":"保留並列者","detail":"第2類與第6類同高"},{"title":"本圖取首","detail":"按類別順序，顯示第2類"}],"key":"本圖取首顯示；並列仍要保留","source":"2020公開資料實算｜2026-10-25｜B格"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-green-label | big | {"text":"仍顯示自然更新林","key":"這是本圖的取首規則"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| a-b-comparison | diagram | {"svg":"docs/videos/forty-forest-map/assets/pixel-comparison.svg","caption":"ForTy 2020｜公開模型輸出；本片裁切與計算","key":"兩個綠格，分數資訊不同"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| b-annotation | table | {"columns":["欄位","內容"],"rows":[["最高者","第2類／第6類並列"],["分數","0.344／0.344"],["顯示選擇","本圖取首，顯示第2類"]],"key":"並列與顯示規則，分開寫","source":"2020公開資料實算｜2026-10-25｜B格","title":"把B格的資訊寫完整"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| use-annotation | big | {"text":"比較時，讀完整註記","key":"不要讓單一顏色省略並列者"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| annual-forward | big | {"text":"資料年，也要留下","key":"這種讀法如何接上年度資料"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| year-in-record | big | {"text":"每一列，保留資料年","key":"從一個像素走向年度紀錄"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| baseline-release | big | {"text":"五月已公開","key":"2020 v1是本片實算的資料","kicker":"資料公開時間"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| paper-date | big | {"text":"2026年10月21日","key":"正式資料論文出版；日期不自補時區"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| annual-release | big | {"text":"2017–2025早期序列","key":"10月22日研究介紹另外分享","kicker":"新增的年度維度"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| time-dimension | big | {"text":"同一位置，不同資料年","key":"類型可以沿時間展開"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| annual-reading-fields | steps | {"steps":[{"title":"固定位置","detail":"比較同一處的輸出"},{"title":"保留資料年","detail":"每年分開記錄"},{"title":"對齊六類","detail":"保留順序和完整分數"}],"key":"同位置、資料年、六分數一起保存","source":"編輯判讀｜同一份真實輸出"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| color-change-reading | big | {"text":"比較的不只顏色","key":"同一套註記，帶進每個年份"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| score-question | big | {"text":"0.992代表什麼？","key":"模型分數，能怎麼解讀"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| uncalibrated-score | big | {"text":"未做事後機率校準","key":"它是模型的類別分數"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| calibration-reference | big | {"text":"用獨立參考檢查對應","key":"分數與真實結果，需要另外比較"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| not-correctness | big | {"text":"分數≠實際正確率","key":"0.992不能直接當99.2%判對"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| reference-needed | big | {"text":"線索要對照參考資料","key":"地面歷史與經營用途，另有證據"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| baseline-scope | big | {"text":"2020版本的真實輸出","key":"A／B兩格的證據範圍"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| annual-next-input | big | {"text":"年度輸出＋獨立參考","key":"讓要回答的問題，配上對應資料"} | PASS: source facts / original data / explicitly editorial display, as applicable |
| complete-pixel-record | outro | {"title":"把色塊讀完整","cta":"留下年份、類別與完整分數","lines":["兩個真實例子，對回自己的地圖問題"],"key":"六類輸出，比單一顏色多一步"} | PASS: source facts / original data / explicitly editorial display, as applicable |

## Complete additional metadata / assets review

| Path | Actual content | Verdict |
| --- | --- | --- |
| youtube.category_id | 28 | CONFIRMED / editorial or standard platform configuration |
| youtube.made_for_kids | false | CONFIRMED / editorial or standard platform configuration |
| youtube.default_language | "zh-TW" | CONFIRMED / editorial or standard platform configuration |
| youtube.title | "Google AI 森林地圖怎麼讀？ForTy 台灣像素實算" | CONFIRMED / editorial or standard platform configuration |
| youtube.description | "讀懂 ForTy 森林地圖，從一個色塊走到六個完整分數。給想看懂 AI 地理資料、但沒讀過遙測檔案的你。\n\n以台灣兩個真實像素示範類別、補數、分數與並列註記。實算使用 Forest Typology 2020 v1；2026 年 10 月研究介紹分享的 2017–2025 早期年度序列另行區分。資料圖為原創裁切與計算，B 為刻意挑選的低分閱讀例，不能用於估計整張地圖精度。" | REVISE R1-M1: add visible dataset attribution + DOI + license link + modifications |
| youtube.tags | ["ForTy", "Google AI", "森林地圖", "AlphaEarth", "衛星資料", "AI 科技", "自然更新林"] | CONFIRMED / editorial or standard platform configuration |
| youtube.video_id | null | CONFIRMED / editorial or standard platform configuration |
| thumbnail | {"template": "thumb", "data": {"headline": "**綠色**\n還藏什麼", "tag": "ForTy 真實像素", "sub": "五個值，讀出六類結果"}} | CONFIRMED: real pixels, 5 stored values -> 6 class scores; original headline, not an accuracy claim |
| assets[0] | {"path": "docs/videos/forty-forest-map/assets/roi-a-grid.svg", "source": "https://doi.org/10.25452/figshare.plus.32288616.v1", "license": "CC BY 4.0; Neumann et al. (2026), Forest Typology 2020 (v1). Original Mokaair composition; changes: crop, Other residual, first-maximum classification, charts."} | Source / author / version / modifications confirmed; license link delivery is R1-M1 |
| assets[1] | {"path": "docs/videos/forty-forest-map/assets/roi-b-grid.svg", "source": "https://doi.org/10.25452/figshare.plus.32288616.v1", "license": "CC BY 4.0; Neumann et al. (2026), Forest Typology 2020 (v1). Original Mokaair composition; changes: crop, Other residual, first-maximum classification, charts."} | Source / author / version / modifications confirmed; license link delivery is R1-M1 |
| assets[2] | {"path": "docs/videos/forty-forest-map/assets/roi-a-scores.svg", "source": "https://doi.org/10.25452/figshare.plus.32288616.v1", "license": "CC BY 4.0; Neumann et al. (2026), Forest Typology 2020 (v1). Original Mokaair composition; changes: crop, Other residual, first-maximum classification, charts."} | Source / author / version / modifications confirmed; license link delivery is R1-M1 |
| assets[3] | {"path": "docs/videos/forty-forest-map/assets/roi-b-scores.svg", "source": "https://doi.org/10.25452/figshare.plus.32288616.v1", "license": "CC BY 4.0; Neumann et al. (2026), Forest Typology 2020 (v1). Original Mokaair composition; changes: crop, Other residual, first-maximum classification, charts."} | Source / author / version / modifications confirmed; license link delivery is R1-M1 |
| assets[4] | {"path": "docs/videos/forty-forest-map/assets/pixel-comparison.svg", "source": "https://doi.org/10.25452/figshare.plus.32288616.v1", "license": "CC BY 4.0; Neumann et al. (2026), Forest Typology 2020 (v1). Original Mokaair composition; changes: crop, Other residual, first-maximum classification, charts."} | Source / author / version / modifications confirmed; license link delivery is R1-M1 |
| sources[0] | {"title": "DeepMind：Beyond tree cover", "url": "https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/", "checked_on": "2026-10-25"} | CONFIRMED with retrieval boundary listed above |
| sources[1] | {"title": "ForTy 2020 v1.0 官方資料目錄", "url": "https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection", "checked_on": "2026-10-25"} | CONFIRMED with retrieval boundary listed above |
| sources[2] | {"title": "Forest Typology 2020 v1：資料metadata", "url": "https://api.figshare.com/v2/articles/32288616", "checked_on": "2026-10-25"} | CONFIRMED with retrieval boundary listed above |
| sources[3] | {"title": "Scientific Data：出版metadata與摘要", "url": "https://www.nature.com/articles/s41597-026-08299-5", "checked_on": "2026-10-25"} | CONFIRMED with retrieval boundary listed above |
| sources[4] | {"title": "本次兩ROI的公開原始COG", "url": "https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif", "checked_on": "2026-10-25"} | CONFIRMED with retrieval boundary listed above |
| loops[0] | {"setup": "ep85", "payoff": "t4w3", "what": "有樹之外，類型還描述形成方式與用途"} | CONFIRMED: referenced IDs exist and question / payoff match; not a new empirical claim |
| loops[1] | {"setup": "jw6i", "payoff": "mx7g", "what": "同樣色塊省略了哪些分數資訊"} | CONFIRMED: referenced IDs exist and question / payoff match; not a new empirical claim |
| loops[2] | {"setup": "5ur9", "payoff": "3p97", "what": "五個儲存值怎麼補出第六類"} | CONFIRMED: referenced IDs exist and question / payoff match; not a new empirical claim |
| loops[3] | {"setup": "8hpb", "payoff": "ywu9", "what": "儲存整數如何換到零到一的模型分數"} | CONFIRMED: referenced IDs exist and question / payoff match; not a new empirical claim |
| loops[4] | {"setup": "endc", "payoff": "jbsn", "what": "另一格會不會也有唯一最高者"} | CONFIRMED: referenced IDs exist and question / payoff match; not a new empirical claim |
| loops[5] | {"setup": "sbkg", "payoff": "nqyj", "what": "六類讀法接上年度資料要保留哪些欄位"} | CONFIRMED: referenced IDs exist and question / payoff match; not a new empirical claim |

Appendix counts: 100 narration claims; 96 scenes; 88 CONFIRMED, 12 OUT OF SCOPE question/CTA; 0 changed; 0 not found. Metadata: 1 required revision (R1-M1).
