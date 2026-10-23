# A01 r44 獨立來源審查

**來源裁決：PASS；P1 0、P2 0。** 這是 r44 凍結候選的獨立離線來源審查；整體製作流程仍為 **HOLD**。我從 r44 本身重新核對 55 筆主張、51 景及全部圖片提示詞，沒有把 r43 的裁決當作 r44 核准。

指定 `manifest.json` SHA-256 為 `62cec617460b882309a48ca76c69615ec20789502538149cc94e47a632144190`，讀回相符。`node build.mjs --check` 通過：51 景、52 句、55 筆主張、零 lint／cute 錯誤；正文 275 字／分紙面估時 424.0 秒。這些是機械與紙面結果，不是 TTS、圖片或成片檢驗。

## 主張、場景與來源

- `candidate/claims.md` 的 q001–q055 均唯一，狀態全為 `PENDING`。每筆在 `candidate/video.json` 所指場景恰出現一次，51 個場景 ID 唯一，合計 55 次主張使用；`source-alignment.json` 的 55 列與主張 URL 完全吻合。
- 公開來源 6 筆、候選企劃來源 6 筆、研究企劃來源 25 筆；前 6 筆 URL 及順序一致，19 筆研究專用來源未混入公開清單。六個公開 URL 分別綁定 12、9、3、5、1、25 筆主張，`source-map.json` 的 ID 清單與各來源綁定相符。所有索引在範圍內且指向相同的精確 URL。
- 來源內容核對：[ABC／USA TODAY 2012 年 Plath 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)記未標年的安檢、車庫螺絲樣品與對話；[Travelpro 公司沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)記直立雙輪、可收拉桿、機組先用、車庫轉倉庫與後來全職經營；[2007 年 Ballis 訪談](https://www.globaltravelerusa.com/reinventing-the-wheel/)記其他機師看到 Plath 的輪箱後請他製作；[US4995487A 專利](https://patents.google.com/patent/US4995487A/en)有 1989-08-08 申請日、外置輪架先前技術及一體箱設計目的；[1993 年 Dash 第一人稱實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)記四牌比較及那只 Travelpro 的外袋加衣書、收納失敗、取出後收納；[RNPA《Contrails》2016 年官方 PDF 第 48 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)重印 Joe Sharkey 2010 年文章，記旅客看見空服員快步拉 Rollaboard。PDF 可讀，64 頁，第 48 頁確有該文和段落。

口播仍將未標年的安檢螺絲樣品、一體 Rollaboard 成品與 1993 年上市 Travelpro 分成不同實物；沒有用 1989 年專利申請日當成品推出年，也沒有選定公司史 1987／索引文字 1988 的爭議年份。Dash 的既有輪具、一般走道描述和四牌地面／機上實測分開；路緣與樓梯不指定實際地點及先後，衣書的加放和取出不指定地點或各袋分布。

## r43 五組 P2 的 r44 讀回

1. **Plath 自己推車的「笨重」屬性：已修。** `hook-security`、`origin-garage`、`origin-fastened`、`origin-return`、`origin-demand`、`origin-ok` 的提示詞（`candidate/video.json:199,310,328,346,364,382`）不再指定重量或材質；僅 `origin-cord` 的**前方旅客**輪架保留有 [ABC 原文](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)支持的笨重金屬。
2. **安檢回答混入記者解釋：已修。** `origin-demand/q016` 的 `candidate/script.md:62` 現把 Plath 的回答「拿不下來」與旁白補充的螺絲背景分句；`candidate/claims.md:19` 也明示螺絲不是他當時被引述的解釋。畫面 `candidate/video.json:364` 禁止指螺絲手勢；與 [ABC 引語](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)一致。
3. **路緣與樓梯同地點：已修。** `hook-curb/q008` 的 `candidate/video.json:236` 只畫路緣；`turn-curb/q042` 用兩個不連通、無地點的分格，未聲稱測試順序。符合 [Dash 原文](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)的記載範圍。
4. **四箱同場選箱：已修。** `engine-competition/q035` 的 `candidate/video.json:691` 改為四個無地點、無時間線及選箱動作的比較分格；沒有把 [Dash 的四牌實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)拍成同一商店展示。
5. **記者走過轉盤再選箱：已修。** `turn-dash/q036` 的 `candidate/video.json:709` 把手提行李與空轉盤分在兩格，禁止走過轉盤、選箱或時間順序；與 [Dash 的一般旅行偏好](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)對應。

另逐景核對 r43 畫面稽核所指出的生成風險：螺絲樣品與後期成品的名詞分開，`origin-garage` 在未接合的兩件物品上開始鎖螺絲；`turn-choose` 不再把伸縮把手誤接到樣品。直到 `now-pocket` 揭曉前，所有相關畫面均要求遮住外袋；揭曉後只確認複數可擴外袋，不指定總數或每袋裝物分布（`candidate/video.json:981,999,1017`）。`now-zipper` 不指定拉鍊在箱上的位置（`candidate/video.json:908`）；`engine-public-sight` 畫面明確是空服員（`candidate/video.json:655`）。51 景掃描後未發現新增的 P1／P2 來源越界。

**非阻擋畫面界限：** `engine-plath-career` 的關置物櫃、`turn-fabric` 的扶箱等是匿名插畫轉場／示意手勢，來源沒有記其具體動作。成圖時應維持示意性，不宣稱它們是史實重建；尚無生成圖片可驗證觀眾是否會如此理解。

## 收據與正式關卡

`source-map.json:3` 為 `ALTERNATE_PROPOSAL_HOLD_R44_SOURCE_MAP`，`source-alignment.json:3` 為 `ALTERNATE_PROPOSAL_HOLD_R44_EXACT_SOURCE_ALIGNMENT`。其引用的 r43 獨立來源報告 SHA-256 與 `reference/r43/independent-source-review.md` 實際雜湊一致；該引用只證改稿來源，不繼承前版核准。`source-alignment.json` 的 `host_adoption_allowed=false`、`paid_media_allowed=false` 仍有效。`validation.json` 在凍結時仍記 `independent_r44_source_review=NOT_RUN`、正式六章審稿 `NOT_RUN`、正式稿件收據 `NOT_ISSUED`；本報告另存後也不改寫這些凍結欄位。

55 筆主張仍待正式逐章查核；站主尚未核准替代企劃的新標題、縮圖與 brief。實際 TTS、圖片、成片及上架均未檢驗。本次複核沒有修改候選稿、manifest 或 build 輸出，也沒有操作主機或呼叫付費媒體。
