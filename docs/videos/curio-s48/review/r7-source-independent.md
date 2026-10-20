# S48 R7｜獨立史料及書面畫面差分：PASS

2026-10-20 UTC。獨立重開固定 Russell／Field 原文，逐項對照 [R7 作者凍結](../verify-8.md)與 Git 中的 R6 基線。本審稿只裁決 R7 九句改詞、新問答伏筆、逐句主張和**書面**畫面提示詞；沒有修改作者稿、產生媒體或作敘事盲評。

| 精確 R7 輸入 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `video.json` | `143026c1d2306a31ee54ff8970d6f79a353983682f4c756a9fe0575c6a164168` |
| `script.md` | `dcb1e33de833cd2d7d39119ac6bb12c272869bb8b56dfdb5edfebd2eca71f161` |
| `claims.md` | `0b3a2e2db04e667ad49e25b7de25df2509775db078d54b2d4b9010274fcd4594` |

固定全文原始位元組亦核對：Russell `/tmp/s48-russell-atlantic-telegraph.txt` SHA-256 `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；Field `/tmp/s48-field-atlantic-telegraph.txt` SHA-256 `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。來源版本及連結見 [research.md](../research.md)。

## 九句來源覆核

| ID | R7 判讀與固定原文位置 |
| --- | --- |
| `atl029` | Russell R3263–3307 明記 7 月 29 日、已放出 716 nautical miles、船上測到電流直接漏入海水；改成「船上的電路檢查」沒有增加診斷結果。 |
| `atl040` | Russell R3760–3764 記船上水槽不同位置的切開測試，第二切顯示故障在船外；「在船上先做分段測試」與結果相符。 |
| `atl049` | `atl048` 為 8 月 2 日下午放鉤；Russell R3934–3979 接著記 8 月 3 日清晨船頭受牽偏、張力計讀數升高。「隔天清晨」時序正確，也沒有把受力當成目視確認舊線。 |
| `atl054` | Russell R4029–4034 記**轉環銷釘頭**斷裂、鉤與餘索落海；R4040–4045 記工程師 Canning 與 Clifford 即叫人把備用鐵索接另一抓鉤並準備浮標。「接頭斷後」保住 R5→R6 修正，稱 Canning 為工程師亦見 Russell R2103。只點名 Canning 未排除 Clifford。 |
| `atl059` | Russell R4041–4056、R4070–4093 記再備抓鉤與推估搜尋路線，R4280–4335、R4485–4650 記後續索具故障和最後嘗試；「那條舊線會先回來」是問句，沒有宣稱 1865 年舊線曾上甲板。 |
| `atl066` | Russell R4615–4639 記夜間最後嘗試的 hawser 在絞盤處斷裂，船員收工、船準備離開；改詞沒有改變事故次序，也未新增受傷敘述。 |
| `atl090` | Field F9575–9584 寫 Medway 從西邊拉斷舊線後，Great Eastern 所拖的 rope 重量減輕，繼續輕收並監看張力；「抓鉤繩上的重量」比 R6 的「剩下那頭」指涉更清楚。依舊歸後出 Field 敘述。 |
| `atl095` | Field F9687–9719 明示接下來引 *London Spectator* 描述愛爾蘭端反光訊號由亂跳轉為規律；新詞明確保留 Field 引報導的第二層來源，不混入 F9652–9685 的 Dudley 船上見聞。 |
| `atl099` | Field F9721–9746 在暴風段以 “Says Mr. Field” 引 Cyrus Field 第一人稱家訊；「菲爾德在書中引用賽勒斯的話」清楚區分後出作者 Henry 與被引的 Cyrus，且沒有把訊息畫成可讀原電文。 |

新 `atl054→atl056` 伏筆的問句問失落位置能否再找，`atl055–056` 以**浮標標推測搜尋帶、不能指出海底端頭**作有限答案。Russell R4042–4045 寫浮標只求標示「as nearly as could be guessed」，R4080–4093 記其後實際放置，R4116–4131 記靠浮標估位置再找；沒有把推算寫成確定座標。`atl053` 先問如何回頭找，`atl054` 隨即追加位置問題；兩句聽感是否重複仍屬新敘事盲評，不是史料錯誤。

## 對齊、書面畫面與界線

R6→R7 的 `video.json` 遞迴差分只有上述九個 `lines[0].text` 和一條新伏筆，`loops` 由 20 增至 21；全部 setup／payoff ID 存在。`claims.md` 的 102 個 ID 與 `video.json` 同順序、同文字，只有九列口播改詞；`script.md` 的 99 句正文及三句片尾與 `video.json` 逐字一致、ID 唯一。`script.md` 尾部的 narrative／speech 指紋已隨改詞重生。

99 個 `shot` 的 `data.prompt` 與 R6 **逐字相同**。九句對應的書面畫面仍是船上測試、無字張力計、抓鉤與浮標、船上／愛爾蘭端反光點等示意；`atl054` 的備索畫面由接下來 `atl055–056` 的浮標和空白海圖承接新問題。未發現提前畫出 1865 年海底電纜、可讀假電文或宣稱已確定端頭座標的提示詞。這是書面提示詞驗收，**不是生成圖像的驗收**。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json`：**0 errors／0 warnings，102 lines**；`git diff --check -- docs/videos/curio-s48` 通過。`claims.md` 開頭仍寫「R5 前製索引／R5 待覆核」，是過期的狀態說明；逐句史實和這次精確 R7 裁決不受影響，交接時宜另行更新。

**裁決：史料文字 PASS；書面畫面 PASS。** 僅綁上表 R7 五檔。R6 的雙盲、政策、網站劇本卡和 R6 音訊 HOLD 不移轉；R7 仍須兩位此前未讀此稿的隔離讀者作完整敘事盲評，之後按精確 R7 重跑政策／站台流程、改句配音與完整音檢，再走實際插畫及成片關卡。
