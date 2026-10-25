# ForTy 最終開場／七章名定向複核

日期：2026-10-25（Asia/Taipei）。依root委派，只核對本輪開場一句、七章名、metadata實際輸出與版本；沒有重做前輪85句完整查核，亦未修改原稿／音訊／狀態。原verify-1與verify-2保留原結論及綁定版本。

**結果：PASS（本輪指定差異的事實與metadata），0 must-fix。** 不代表盲讀、旁白、字幕或最終成片關卡通過。

## 綁定版本

- video.json：`97f8953911c0de4b64f7fcbeaee5a3bd32970156d3bada2adcefecdae4876609`
- claims.md：`861262f13b7b86c93b522e44fdcdbd037221b4ad52230591fad3c6ca3158f135`
- 未動verify-1 SHA：`5bc134669e77a972707bc5782df7e7aa53bcc015f196264f0257edb2c6403f10`，仍為原稿REVISE。
- 未動verify-2 SHA：`a985bf9f4c721da6bfd4b5a06ebb1f861c1f8f809449a022d1f0980678348081`，PASS仍綁前稿17011f…3387，不直接套給本輪。

## 開場8aw6：CONFIRMED

實際新句：

> 我從二〇二〇年的台灣資料，取出這個ForTy綠格。

- **2020資料年正確。** 來源物件路徑、Figshare版本與原始JSON皆為Forest Typology2020 v1，本輪沒有把發布年2026或early2017–2025系列當實算年份。
- **台灣位置正確。** A請求121.4°E／24.7°N，指定像素中心121.4000409261°E／24.7000060514°N；是全球ForTy資料中的台灣取樣。「台灣資料」在本句指取樣位置，未聲稱台灣另發官方資料。
- **本次取出／讀格行動有RUN證據。** 實際已取得公開COG、裁出A窗口、推導Other及本地最大值分類，A指定格第2類唯一最高、圖中呈綠色。畫面caption仍明列「公開模型輸出；本片裁切與計算」，沒有冒充衛星照片、現地調查或官方App成功操作。
- claims.md c1與新句、first-grid／8aw6完全對應；其來源仍是本次2020公開資料實作，不是新增私人經驗。

Primary證據：

https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif

https://api.figshare.com/v2/articles/32288616

沿用本日已核對的官方API200與獨立206 Range／固定SHA原始JSON收據；本輪不需要重抓整個COG。A JSON SHA仍為`867aa186e25b6a59ea5dcf32a100646d68497fa064d177e674f2674f42a362ba`。

## 七章名：全部CONFIRMED

| Scene | 新章名 | 對應內容／界限 |
| --- | --- | --- |
| first-grid | 讀出一個台灣綠格 | A實際2020取樣；不是現況或地面真值宣稱。 |
| label-meaning | 把綠色對回六種類型 | 六類定義仍含OtherLand，不稱六種全都是森林。 |
| pixel-record | 找到指定格的五個值 | 對應年份／位置／band順序／有效值與五個真實儲存值。 |
| residual-rule | 補出第六類，選出最高 | A補Other2後比較六分數，第2類唯一最高；沒有稱第6類本身最高。 |
| b-selected-grid | 換一格，再算六類分數 | B完整輸入／補數／分數與並列；沒有新樣本或精度主張。 |
| score-question | 把分數和年份寫進紀錄 | 對應校準限制及資料年／early系列界線，沒有把score改成實際正確率。 |
| complete-pixel-record | 完成一列像素紀錄 | 回收年份／位置／六分數／所有最高者的閱讀方法，無不存在的外部下載承諾。 |

## 實際compose與原生lint

guard_review另以唯讀方式實際執行`composeDescription`，採正式body/sources/assets/tags/category/campaign、`locale:'zh-TW'`、`timeline:estimateTimeline(doc)`、`article:null`。

結果：**2549 UTF-8 bytes、7章、5條完整圖片credits、checkYoutubeFields=[]**。作者Neumann等（2026）、Forest Typology2020(v1)、可點DOI、CC BY4.0與改作均保留；說明正文仍有`https://creativecommons.org/licenses/by/4.0/`。相較前輪2561 bytes，本輪章名與估時更換後變成2549，沒有把舊byte數當成新結果。

標題與縮圖未改，沒有新增事實風險。七章估時實際為00:00／00:23／02:06／03:06／04:52／06:43／08:13；這是文字估時metadata，不是實際音訊時戳。

本輪實跑`node tools/video/cli.mjs lint --slug forty-forest-map --json`，exit0、errors0、warnings5：首章約24秒，以及248／250／86／77在完整算式中的重複數字heuristic。工具估1755 spoken units、8.4333分鐘（506秒）；未聲稱已有音訊。無TTS或媒體生成。

本收據只確認本次指定差異，不替盲讀評分或其他關卡作通過判斷，也不覆寫先前負評及收據。
