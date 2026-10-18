# A01 輪子行李箱 r22：時間與來源界線整合候選 — HOLD

r22 從已固定的 r21 **另建**，針對 [r21 獨立史實與企劃全文審查](../A01-editorial-candidate-20261019-r21/independent-fact-full-plan-review-20261019.md)的 P1 2／P2 6 及[離線敘事盲讀](../A01-editorial-candidate-20261019-r21/blind-story-review-20261019.md)的轉場意見修正。建置器核對 r21 manifest SHA-256 `5131D53CEF6F20184C1D5043CF63428602DEB1551FFB9808CA42E940F190E900`、史實審查 `A2570970DC7A240B2E7ED25313EE2AB787214F155E11DE5FDAEC0E86051E0409`、盲讀 `939EE33E1656E4BE78A0E48762EACAD8DB581B518BD6CF4196A9EC06F52DBECD`，但**不繼承前版審核結果**。r21、舊候選與收據均不改動。

## 與 r21 的精確差異

- `turn-09b` 口播先說明安檢那次是**推車鎖上硬殼箱**，後來的 Rollaboard 才是**直立雙輪、可收拉桿**；`turn-09` 繼續分別歸屬 Travelpro 的 1987 年與 Plath 簡歷的 1988 年。插圖也明寫不可把螺絲推車試作畫成同一只定型箱。[2012 年 USA TODAY／ABC 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)未標安檢／車庫故事年份；[Travelpro 官方沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)才把直立雙輪拉桿設計記於 1987 年，並另記 1989 年生產搬離車庫。兩份 23／25 來源企劃的 turn 章和待查欄已把這些分成不同事件。
- `hook-anita` 改成**1928 年那趟旅行出發前**完成嬰兒車輪改箱，不替改箱指定 1928 年內的製作日；`idea-memory` 改「多年後」，不從 1939 年巡講替 Sadow 的靈感事件計算未證實的三十多年。對應插圖不標阿魯巴返程的精確年份。[Winnetka 館方輪箱文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)與 [Sadow 2010 年訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)是各自來源。
- `i35` 的否定句限於**本集核對的那篇 ABC 訪談未提 Anita 或兩人交接**；它不宣稱所有史料都沒有直接關係。
- 兩份企劃的 1921 年首旅待查句只說搭火車抵達新地方後，丈夫找廉價住處、Anita 與四個孩子守行李；[Winnetka 官方生涯文章](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)沒有指明守行李發生在車站。
- 兩份企劃分清 [2012 年報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)中旅客費力想卸箱的**記者敘述**，與 Plath 對安檢員答話的**直接引語**。企劃的背景來源和 ABC 2010 來源也改稱 **1970 年 10 月店內人偶展示**及 Macy's 決定進貨；[原訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)未給精確首次開賣日期。

來源 URL、引用索引與數量不變：65 鏡、77 句、74 筆仍為 `PENDING` 的主張、18 個公開來源、23 筆編輯來源與 25 筆擬採用來源。`source-map.json`、`source-alignment.json` 與 `validation.json` 記錄本版差異；`plan-source-addition.json` 仍僅是舊版未採用提案。所有更動須再由獨立讀者查核，r21 收據不是 r22 的 PASS。

## 使用界線

紙上秒數不是實際 TTS、剪輯或成片。Winnetka 原文頁本輪逾時，1939 年原報紙掃描仍未直接逐頁目視，Chinook 官方 PDF 與 `sl8.com` 鏡像也未位元組比對。正式機六章、主張 ID／來源合併、verifier、listener、兩名敘事讀者及正式 `story/reviews/script-review.json` 仍待完成。維持 **HOLD**，本候選不授權主機寫入、解除 STOP、付費製作或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r22/build.mjs --check
```
