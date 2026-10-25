# ForTy：B分數加總五句與縮圖署名定向複核

2026-10-25（Asia/Taipei）。本輪僅核新增五句／五張對應卡、縮圖PNG來源與第六筆credit，沒有重審原87句、音訊或盲讀；未改稿、未呼叫TTS。verify-1至4維持原SHA及原結論。

**結果：PASS（本輪指定差異），0 must-fix、0未找到事實。** 本收據不代替新增take音檢或最終成片QA。

## 綁定

- video.json SHA256：`20bb4b24df9b9bcccaf2763598f7478a4a706e859f0e20909a09b9c4d5fca969`
- claims.md SHA256：`f7e7ec21687a9470e3d8cbd15aa77370e9c9188abeab140ddd2d1dd6d7b600d8`
- B資料SHA256：`4ebd1c412fe85576277d0b8c4ab96fce31254abe41b6c07ba3ca203220db101a`
- thumbnail-grid.png SHA256：`dd45ef07a7e773559b297f6d53614585ab566ac48163a38f83a4983ef8f21034`

已讀取forty-sumcheck-completion.json與forty-thumbnail-completion.json；前者明列新增五句且原87句不變，後者記錄縮圖與第六筆來源變更。本輪逐句和實際scene.data、claims的ID核對，不以完成收據代替算術。

## 五句與卡片：全部CONFIRMED

直接從固定SHA的actual-uncertain-roi-result.json讀六分數，轉Decimal計算，未以binary float的顯示近似取代原始小數：

`[0,.344,0,.004,.308,.344]`

| Claim／line／scene | 實際內容 | 獨立結果 |
| --- | --- | --- |
| c88／afyy／b-sumcheck-open | 把第二格填進紀錄前，先把六個分數加起來，檢查總量。 | 原創算術檢查動作；六分數取自既有B輸出，沒有新增樣本或模型測量。 |
| c89／f2ze／b-sumcheck-pair | 兩個零點三四四相加，得到零點六八八。 | Decimal `.344+.344=.688`。卡片標自然更新林＋其他土地，對應第2／6類正確。 |
| c90／ckag／b-sumcheck-crops | 再加零點三零八，得到零點九九六。 | `.688+.308=.996`。卡片對回樹木作物與農林複合，第5類正確。 |
| c91／n37p／b-sumcheck-finish | 最後加零點零零四，剛好是一，另外兩類的零不改變總和。 | `.996+.004+0+0=1.000`。非零項是第4類林木種植園；原始林與人工栽植林為零。 |
| c92／ecb8／b-sumcheck-repair | 總和不對，就檢查漏項和小數位，類別名稱仍要逐項對回。 | 合理的抄錄回查建議；未聲稱總和正確即可證明所有類名／結果正確。表格保留漏項、小數位與逐項對類名。 |

四張big卡（一張引入、三張算式）及一張回查table的實際data均與上表一致。`.688`／`.996`／`1.000`是既有六分數的累計和，不是新的類別分數、accuracy、地面真值或校準結果。加總1也沒有被宣稱成已校準正確機率。

Primary資料仍為2020官方COG與DOI：

https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif

https://doi.org/10.25452/figshare.plus.32288616.v1

沿用同日已核的來源與固定SHA像素數組，本輪不需重抓COG或新model API。

## 新縮圖PNG：CONFIRMED

已實際開啟觀看thumbnail-grid.png（1440×1360，RGBA，透明角落），並以Pillow取兩組所有格心對照原始class_ids，不只依肉眼猜色：

- A100格均為第2類綠色，與A原始分類完全一致。
- B100格逐一相符：第2類19格、5類14格、6類67格；使用與原SVG相同的`#7FBF7B`／`#E6AB02`／`#FDE278`。
- 原始row0在下、row9在上，正northing步長與圖一致；兩組紅框均定位[5,5]。圖上有A／B、2020及「兩處取樣」，沒有把兩窗口畫成一片連續地面或新年度資料。
- B紅框呈綠來自已明列的本地取首規則；PNG沒有新增「唯一最高」或精度文字。既有正文與分數圖繼續保留第2／6類並列資訊。
- PNG的實際SHA與forty-thumbnail-completion.json吻合。assets/manifest.json原本只列五SVG，本輪未假稱PNG已列入該五圖manifest；PNG由專用completion收據及video第六筆source/license/author/url追溯。

新thumbnail sub「五個值，六類結果」與既有實算一致；第六筆asset的Neumann作者、Forest Typology2020(v1)、CC BY4.0、DOI與兩處裁切／補數／取首／重繪改作標記完整。沒有衛星底圖或來源不明照片。

## 實際metadata：CONFIRMED

本輪直接唯讀import原生composeDescription，帶正式body／sources／assets／tags／category／campaign、locale zh-TW、estimateTimeline(doc)、article null。

重得**2921 UTF-8 bytes、creditedAssets=6、實際圖片credit行數6、checkYoutubeFields=[]**。license URL與資料包URL均實際保留在合成說明，DOI與完整題名署名也保留。沒有沿用前稿2701bytes／5credits冒充本輪結果。

本輪沒有將先前478.2秒音訊當成新增五句後時長，沒有作實際音訊或92句全文通過判定；新增take與最新timeline仍交既定音檢、合成及QA流程。舊盲讀評分、敘事heuristic與前輪收據均未被改動。
