# X03 Netflix 郵寄 DVD 與即看｜SEC 原件初查

2026-10-20 唯讀開啟 Netflix 的四份 SEC 原始申報，均回 HTTP 200。本檔記錄**前製題材可用的原件片段**，尚非獨立審稿、逐句稿或付費製作核准。引號內英文摘自申報 HTML，僅合併空白；公司對未來的預期須標明歸屬，不能寫成後見之明。

| 代號 | 原始申報 | 報告期間 | 本機下載 SHA-256 |
| --- | --- | --- | --- |
| N06 | [Netflix 2006 Form 10-K](https://www.sec.gov/Archives/edgar/data/1065280/000119312507042689/d10k.htm) | 財年截至 2006-12-31；申報本文已記載 2007 年 1 月的新功能 | `cd7708d49dbaae5072edad3715f0f8d6d552e347abd66150c15694766020dff9` |
| N07 | [Netflix 2007 Form 10-K](https://www.sec.gov/Archives/edgar/data/1065280/000119312508040378/d10k.htm) | 財年截至 2007-12-31 | `e1f361bd9e1b21e2495f96b968f9093e696d8281306111adbd6ffb7daceda625` |
| N10 | [Netflix 2010 Form 10-K](https://www.sec.gov/Archives/edgar/data/1065280/000119312511040217/d10k.htm) | 財年截至 2010-12-31 | `beb94570bba039de29ca4d028e446320bf833f6fdb9028a3cd0074e50b696e70` |
| N23 | [Netflix 2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/1065280/000106528024000030/nflx-20231231.htm) | 財年截至 2023-12-31 | `5814c4a487f9e2d531ceee9f87ef6b110b41710617522500f73707637854a104` |

## 已可核對的敘事事實

1. **寄片如何運作。** N06／N07 的 Item 1／Business 說訂戶在網站選片，DVD 經郵件送達，訂戶用預付郵資的郵袋寄回；退片後公司才寄下一片：`return them to us at their convenience using our prepaid mailers. After a DVD has been returned, we mail the next available DVD in a subscriber’s queue.` 可畫無標誌信封、光碟及排片清單，不把郵局或特定家庭畫成歷史現場。
2. **2006 年末仍是擴張中的 DVD 訂閱服務。** N06 的 Selected Financial Data／Other Data 列年末總訂戶 2005 年 **4.179 million**、2006 年 **6.316 million**，單位為千人表格；Item 1／Business 稱 DVD 片庫 `more than 70,000 ... titles on DVD`。約 630 萬是**2006 年末帳戶／訂戶**，不是 2007 年 1 月推出即看當天的人數，也不等於每一位實際看過片的人。
3. **公司當時已公開寫出雙軌策略。** N06 的 Item 1／Business：`Our core strategy is to grow a large DVD subscription business and to expand into Internet-based movie delivery as that market develops.` 同段說公司**相信** DVD 在可預見期間仍是居家看片的主要載體；這是當時管理層預期，不能以 2023 結局倒寫成「Netflix 早知寄片會何時終止」。
4. **電腦即看在 2007 年 1 月加入。** N06 的 Item 1／Business 於年度結束後記：`we introduced a new feature in January 2007 that allows subscribers to instantly watch movies and television series on their personal computers`；N07 也記 `In January 2007, we introduced our instant-watching feature for PCs.` 因此不能說即看於 2006 財年已上線，也不能說所有訂戶在上線當日均可使用：N06 說預期六個月內逐步開放。
5. **推出即看的同一年，寄出的 DVD 總片數仍增加。** N07 的 Item 7／Management’s Discussion and Analysis／Cost of Subscription Revenues：`The number of DVDs mailed to paying subscribers increased 20%.` 這是 **2007 全年相對 2006 全年**的寄出片數，不是 2007 年一月即看推出當天、每位訂戶的 DVD 觀看量或訂戶成長率。同段說平均付費訂戶數增 **32%**，而每名平均付費訂戶每月租片數下降，並把這一下降連到較低價方案持續增長；**不能把人均租片下降直接歸因串流**。N07 的 Selected Financial Data／Other Data 另列年末總訂戶 **7.479 million**，前一年末 **6.316 million**；Item 1／Business 約稱 750 萬訂戶、約 9 萬 DVD 片名與超過 6,000 個可在電腦即看的選擇。後兩項是不同交付方式的片庫計數，不能把 9 萬與 6 千當同一分母做「即看只占幾%」的成效結論。
6. **2007 年並非隔夜停寄片。** N07 的 Item 1／Business 仍說公司相信 DVD 將在可預見期間是主要居家觀看載體，同時希望把即看擴到其他平台與合作夥伴。2008 年 1 月的 LG 開發安排在申報中仍寫作 `terms ... have not been finalized`；不可寫成 2007 年已推出一款確定規格的裝置。
7. **2010 年的觀看方式與策略轉折。** N10 的 Item 1／Business／Strategy：`In 2010, we passed a significant milestone with the majority of our subscribers viewing more of their TV shows and movies via streaming than by DVD.` 同節稱 `Our core strategy is to grow our streaming subscription business within the United States and globally`，並預期 DVD-by-mail 成為美國服務的附加選項。這個「多數」指**多數訂戶各自透過串流看的內容多於 DVD**；不是全公司串流營收已超過 DVD、每一名訂戶都改看串流，或當年停止寄片。N10 的年末訂戶 **20.010 million** 是同份申報的另一種指標，不能拿來當觀看時數。
8. **寄片直到 2023 年 9 月才停止。** N23 的 Item 7／Management’s Discussion and Analysis 註腳：`we ceased providing our mailing services to customers on September 29, 2023.` 同表以**千美元**為單位列 2023 年 DVD 營收 `82,839`（US$82.839 million）、串流營收 `33,640,458`（US$33.640458 billion）。DVD 是美國寄片服務，串流是全球業務；2023 DVD 全年營收還包含停止前月份，不能用兩欄直接計算同市場轉換率。申報稱寄片終止對集團營運和財報影響不重大，是公司的財務口徑，不能推論所有使用者都不在意。

## 這條故事能說與不能說的事

可按**寄片模式與 2006 年末成長 → 2007 年電腦即看加入、寄出 DVD 總片數仍增 20% → 2010 年公司報告的觀看方式轉折及核心策略 → 2023 年結束美國寄片**說一條時間線。四份原件足以支持「同一家公司主動開出新的交付路徑」；尚不能單靠它們證明每一步的唯一商業動機、每個使用者的偏好，或串流服務在市場上是第一家。

《原來如此》B08 的 Blockbuster 拒買 Netflix 是**另一個故事**；本集不借用創辦人談判、出售價格、Blockbuster 倒閉或後來市值作主線。示意插圖不使用 Netflix 標誌、實際影片畫面、可讀介面字或真人肖像；品牌名、年份和數字由後製卡片處理。若要講版權成本、郵資使公司改道、網速普及、裝置上的實際上線時間或取消寄片對家庭的影響，須另取同期可歸屬原件，未取得前不進旁白。

後續須讓**另一位代理**逐項複核引文、單位與主線，再寫至少八分鐘逐句稿；此檔本身不批准付費媒體或正式上架。
