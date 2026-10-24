# S48 R10｜新三景候選提示詞獨立書面覆核

2026-10-20 UTC。**三句候選的來源／書面畫面邊界 PASS；付費試畫、九題圖像評審與原生圖驗收 NOT RUN。** 我未撰寫[新方案預檢](r10-alternate-art-paper-preflight.md)，也未改 `video.json`、劇本、畫風、媒體或網站卡。此判定只綁預檢中的三句候選 prompt；它們尚未進入凍結分鏡。舊方案兩輪各 **0／3 KEEP** 的 STOP 仍有效。

## 重開的證據與凍結版

從固定 Git 提交重新取得 Russell 1865 年船上記述 [R](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt)，全文 SHA-256 `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；以及 Field 後出家族敘事與內引航程日記 [F](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt)，全文 SHA-256 `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。現行 `video.json` SHA-256 `dd91631217153e3fec5e0117dea73faa30811991fce3a211aad7d99615cca018`、`claims.md` `5b0714fafe2d0537d03309aac08d1dff8de0656337223689b7033866a5ccbbf7`、`script.md` `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd`；候選預檢 SHA-256 `9ce14f807f217b41e1ed491989c9dd459380c311d1ecf3120625c5c9f9a30cf4`。核對時三個候選都**不在** `video.json` 中。

我重新開啟三張第二輪原生 1280×720 JPG，SHA 分別為 `atl001` `f2024ccfaf6ac585af5f986c2d62c6243883cdfd9e44471c1cf6d8cf75cfeab2`、`atl017` `01b8ea0d747ee8dc6d83a57e81fb1747eb4bc3e0822b8b16b43493c0fb61ac62`、`atl070` `57c42f823814af6620f76c87fac04916092aecc3d93f5fc74f36ec7bf352128e`。錯誤確為駕駛舵輪／頭髮般電纜、巨大空板中央光點與童貌觀察者、以及數尺寬海堤；機器分數不能代替這三個主物件的驗收。

| 候選景 | 獨立判讀 | 書面結論與原圖必要條件 |
| --- | --- | --- |
| `atl001` | [R3778–3800](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3778-L3800) 記纜由船首進入、經收線機械與捲鼓向船後移動；候選把水面、連續纜線、低架橫鼓和單名甲板工排成一個可讀動作，對準舊圖舵輪錯誤。鼓的確切數目、實心形制、軸向與工人身份**不是已驗機械復原**；採入時維持示意界線，不加可讀儀表數字。 | **PASS，限卡通示意。** 新原圖必須讓線從船外水面接上低架收線裝置再入甲板；若又成駕駛舵輪、髮絲、斷線即 REJECT。 |
| `atl017` | [R2899–2915](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L2899-L2915) 確有小鏡反射的光點沿刻度移到末端並消失。候選把刻度、端點與成年觀察者同框；`palm-length`、米黃色及鏡的圓形是讓物件易畫的**示意尺寸／造型**，不得呈現為有史料量測的器具復原。 | **PASS，限卡通示意。** 1280×720 原圖需有可辨的成年觀察者、小刻度與**末端**光點；巨大空板、中心光球、針式指針或童貌人物即 REJECT。鏡面到刻度的完整光路不要求 AI 精確畫出。 |
| `atl070` | [F8990–9035](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L8990-L9035) 的內引日記記 1866 年新線抵 Heart's Content，安排 Medway 鋪上岸端，當日下午登岸；電報站亦在港。候選畫的是**同日下午新線的示意登岸動作**，不應誤標為 1865 年舊線已撈回，也不宣稱某名工人／海灘形狀精確如此。 | **PASS，限後出書內引的同日場景。** 原圖需是一人雙手握住從水際連續上岸、約繩粗的纜；若成可走的海堤／道路、塑膠管或現代安全裝備即 REJECT。多一名無害卡通路人本身不是退圖理由。 |

三句候選都以單人單動作、物件及柔和光源寫法配合系列 `cute-mystery`，沒有在 prompt 另寫畫風；可避免把插畫當原件照片。現行 99 景仍是舊 `visual_hash`，三句採入後要重跑 lint、綁定及來源／書面畫面差分；本頁只完成**候選文字**的獨立覆核，不能移轉舊分鏡或舊圖的 PASS。

新方案預先訂的 **3／3 原生 KEEP、每個失敗景最多一次有界改詞／重試、再失敗即 STOP** 合理守住三個核心物件。其 US$0.15 試畫累計及 US$4.16 整集累計上限只是待站台新價與 ledger 重報的提案，不能由本頁自動核准支出。圖片評審和配樂本月額度皆已用盡；額度恢復並核實精確版前，不應產圖、配樂或聲稱整片插畫通過。
