# A01 r20 獨立史料差異複核 — HOLD

- 審查日期：2026-10-19。審查對象是離線候選 r20；`manifest.json` SHA-256：`78826BCFC6356335855756FC7F81A7C846087DF340C4A7753C270C186D1077EB`。
- 另釘選 r20 `candidate/claims.md` SHA-256：`F4D91A46C6B7D8A1005053D506A09BC15B8AF592DF26BF8404F84CDAE2FA8388`；`candidate/video.json`：`3045312831B7DC08E2C2AF1F284F7B56F05F58E92C9D78A3C3DB1A5B4B8059F8`；`candidate/script.md`：`173B921FBCB14DA1DBDD6D1B89E63D00F7B21BD60A7388A4012B765FEB923386`。前版 r19 manifest 為 `9E2EBDD0C82F61BAA8CF50041B13E47E1070BD0C7950D2E577890313D6DB1F6E`，其獨立稽核 SHA-256 為 `03A9B3BD20F45D97408E561EAF390AB0B0AF253D0B679C3D13BC136A7BFF0273`。
- **結論：P0 0、P1 1（沿用的 `h6`）、P2 1（企劃的無證據措辭），HOLD。** r20 修改的 8 筆主張本身未發現新的史實錯誤；但這不是全部 74 筆的重新逐條原始史料核准，也不是正式機審稿收據、製作或付費許可。

## 差異與來源結果

逐列比對 r19／r20 `candidate/claims.md`：74 個 ID、排列與狀態不變；**66 列位元組相同**，只變動 `h4 o1 o32 t5 t46 n16 n61 n63` 八列。`candidate/video.json` 的 65 鏡、77 句、74 個各唯一的場景主張引用、18 個公開來源 URL 與排列不變。實際場景差異限於 `hook-04` 的台詞與年代中性插圖、`origin-r12-01`／`origin-01b` 的台詞、`turn-06` 的「試圖卸下」插圖、`now-outro` 的台詞；`turn-05`／`turn-06` 原口播分別是「正費力處理」和「得解開……再卸下」，描述困境／所需步驟，沒有宣稱旅客已成功卸箱。

| r20 改動 | 獨立核對 |
| --- | --- |
| `h4`、`hook-04` | [Sadow 2010 年 ABC 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)記樣品調整後到紐約百貨推銷、遭拒、再由 Macy 副總裁試拉與進貨，明記 **1970 年 10 月**是 Macy 展示人偶，沒有逐店拜訪確切日期。r20 改「後來」與年代中性插圖有根據。 |
| `o1`、`o32`、兩句旅行台詞 | [Winnetka 輪箱收藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)區分 1921–22 與 1928–30 兩次旅程；[家族史](https://www.winnetkahistory.org/who-were-the-burnhams/)具體記首趟歐洲、非洲及第二趟亞洲、非洲、歐洲。改為「第二趟長途旅行」避免暗示首趟環球。家族史支持母女三人以畫換餐宿，但沒有特定站點交易。 |
| `t5`、`t46`、`turn-06` 插圖 | [2012 年 USA TODAY／ABC Plath 報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)第 7 段說前方旅客 **struggling to free** 以彈力繩綁在笨重金屬推車上的箱子，未說成功卸下；這是記者敘述，Plath 的逐字引言在後段安檢員對話。r20 改「費力想」並將插圖停在嘗試階段，修復 r19 的兩筆 P1。 |
| `n16`、`n61`、`n63`、片尾台詞 | ABC 訪談支持 Sadow 的店家障礙，Winnetka 該篇未敘 Anita 對後兩人的直接影響；[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)第 267、274 段**確實稱** Plath 改良 Sadow 的設計，但沒記 Plath 親眼見過 Sadow 原型，也沒提 Anita。r20 各列限定於該篇資料，片尾改為「我們查到的資料還不能證明三人一棒接一棒」，有必要且措辭可守。公司史的改良說法須保留歸屬，不等於已證實原型直接傳遞。 |

## 尚存發現

**P1 — `h6`，`hook-06`，沿用而先前稽核漏標。** 這筆主張仍寫 Plath 看見旅客「在安檢**拆外置推車後**」才回車庫；「拆……後」在此語境中表示旅客已完成拆卸。[2012 年原報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)只說他看見旅客**正在費力想**把箱子從推車卸下，沒有說結果。r20 的 `t5`、`t46` 已正確限縮，同一場景的 `h6` 也應寫成「看見旅客正費力想解下……，之後回車庫……」；`hook-06` 的「安檢口的一幕，讓一位機師回車庫動手」口播不需因這點改動。r19 的獨立稽核曾把 `h6` 歸為可對讀，這一點不能沿用為通過。

**P2 — 編輯企劃與擬採用企劃仍有廣泛的「沒有證據」語句。** `candidate/series.json` 與 `proposed-25-source-series.json` 的 `logline`、第一章 `point`、`plan.must_verify[0].claim` 仍以「沒有證據顯示直接承襲」／「無證據顯示她影響 Sadow」概括來源外所有可能史料；r20 的 `n61` 和口播已正確收斂為本集查到的資料。這些企劃語句宜同步改成「本集所查資料未證實」。這是編輯企劃的殘留風險，沒有出現在 r20 片尾口播。

## 結構與限制

獨立驗證 `candidate/series.json` 編輯來源 **23** 個；`proposed-25-source-series.json` 擬採用來源 **25** 個，其前 23 個 URL 與編輯企劃逐一相同，新增索引 23／24 對應校友刊及 Travelpro 樓梯文章；公開 `candidate/video.json` 引用 **18** 個且 URL 各唯一。`source-alignment.json` 的 74 筆 ID、企劃索引、公開索引與 URL 均可對到各自陣列，`source-map.json` 的 18 組覆蓋 74 筆。來源對照表排序有局部差異（例如 `n55`／`n56`），但集合、索引與 URL 一致。`node .../r20/build.mjs --check` 成功，回報零 lint／畫風錯誤與 r20 manifest 相同雜湊；這只證離線機械驗證。

原始史料再讀的範圍是上述四組變動所用 ABC／USA TODAY、Winnetka 官方索引文字及 Travelpro 公司文章；66 筆未改列只是逐列證明與 r19 **位元組相同**，沒有當成 r20 的新獨立 PASS。Winnetka 正文頁在這次直接開啟逾時，以官方搜尋索引文字對讀；1939 年原報紙掃描仍只有先前館藏 OCR、未直接逐頁視讀；Chinook 的 `sl8.com` 鏡像也未做逐位元組比對。未測實際 TTS／剪輯、正式機六章、host verifier／listener、兩名敘事讀者或 `story/reviews/script-review.json`。全部 74 筆仍是 `PENDING`；本收據**不授權**改正式機、解除 HOLD／STOP、付費媒體製作或上傳。
