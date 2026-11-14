# S38 PF042 最後一次鍵盤琴提示獨立紙面核對

**PASS：僅凍結提示的來源相容性；新原生圖仍須驗收。**

審閱者 `/root/s38_pf021_last_paper`，不同於 verify139 提示作者。

實際遞迴比較 HEAD 與現檔，僅 `/scenes/41/data/prompt` 一葉改變，old/new 逐字符合 verify139；camera、look、112個完整spoken line物件及其餘整景均不變。script與claims未因本次提示改動而修改。

固定原文 `/tmp/s38-r8j-pepys-4200.txt` D2c L65908–65911 記河上載貨船，家當裡常有 “a pair of Virginalls”；L65913–65916編者註解其方形而非三角形、pair意為一組而非兩台。新提示是一件平放木製小矩形鍵盤樂器，一排黑白鍵用來明確區別上次錯誤的無鍵盤弦琴；沒有把pair誤畫成兩台。成人麻袖手、木船、貨箱與陰天是時代相容插圖安排，並不聲稱史料記下擺放方法或鍵位配色。無新增行為結果、人物見證或時間。

## 媒體邊界

原28筆完整記錄 canonical SHA-256仍為 `7dff65d03e0ddc8a5fc1bacaec7f8a278c30d95cd73b1ab0ccdc597bfb5b3450`。加上verify138已驗收PF040與PF041，共30筆KEEP；它們的入選檔案SHA與verify138一致。讀取時manifest實際尚含PF042拒收記錄與PF043未完成記錄，共32個keys，不能誤稱32KEEP；這兩筆不計入KEEP。

30筆KEEP完整記錄 canonical SHA-256：`4e1f9d4b95eecec4881449d62a52e4952dd4d66378323bdf6e9feba43fd9ca85`。

PF042已用2次實際原生圖，僅餘1次，提示變動不重設。PF043已用2次，第二張ready未judge：`pf043-2.jpg` SHA-256 `3d85ec314e6c19de70e1c257b5d43218a7a97aa421fb70651a98d879b4ea6034`，保留現檔及計數，先處理既有cached，不得當作零次。

## 綁定

- `video.json` SHA-256：`2f89bd1d41780f39346ff3a40f0440277be4eab8172be4c22541c5212db19f2f`
- `script.md` SHA-256：`035c8792c44590b6c1e2fcc8cff72bd235ef1ac8002b9c5219bbff03622a71bd`
- `claims.md` SHA-256：`b1a86f5161280e48027cfb6ba1716a8a9eaf0136326a0b4120477507a3c6b02e`

本次只寫本驗收票，沒有修改媒體、創作、manifest、ledger、STOP或git，沒有付費呼叫。
