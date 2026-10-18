# A01 r22 獨立史實差異審查（HOLD）

- 審查對象：`story-rolling-suitcase-v2` 的 r22 隔離離線候選。綁定 r22 `manifest.json` SHA-256 `9AB4E2BCA9411951E9471E414EC4170A3ED3D793D645ED9C5921CB941E12B33D`；所依 r21 manifest 為 `5131D53CEF6F20184C1D5043CF63428602DEB1551FFB9808CA42E940F190E900`，r21 獨立史實／雙企劃審查收據為 `A2570970DC7A240B2E7ED25313EE2AB787214F155E11DE5FDAEC0E86051E0409`。
- r22 實際輸出雜湊：`candidate/video.json` `1a56a4e829aa33396e395c1b87cc232e3eab44c6132fdc344fa87fe71c35908b`；`candidate/script.md` `5cea97977f294eb62982a3e32bb6497f9afd16f27d8be1d10bc5a50d4e317633`；`candidate/claims.md` `cccc1c720177742c2f43cda3dc7837eede26717477b096e229d8ca44b48fa7a2`；23 來源 `candidate/series.json` `346fcc5baf1c310c1c795465c58b6f6a3156a509f30935053d472065ccc44ec2`；25 來源 `proposed-25-source-series.json` `bc57c532440616965d0fdc61566b8170a5e4a580a2bba91927d1d50875f2987c`。所有 manifest 列出的輸出檔實際 SHA-256 皆相符。
- 審查邊界：逐項比對 r21→r22 的 3 個口播 line ID（`r17h01/r14i01/3zwf`）、2 個視覺提示、`i35`、兩份企劃相同的 6 個文字欄位；回歸檢查 74 claim、18 公開來源的索引與對位、65 鏡／77 行、未變的企劃欄位和相關前後場景。r21 的 74 個 ID 及其順序維持，僅 `i35` 的內容與核對日期改動，其餘 73 個 claim 文字行相同；公開 source URL、鏡頭次序、line ID、setup/payoff 均維持。這是有界差異與快速全文回歸，**不是**所有原始 PDF 的新一輪完全目視查核。
- 結論：r21 的 **2 P1＋6 P2 所指具體舊措辭均已處理**；但 r22 新引入 **P1 1**，另有 **P2 1** 來源措辭需同步修正。P0 0；**維持 HOLD**，沒有正式 worker 或付費製作 PASS。

## P1 — 新口播將車庫動作移到安檢現場

`candidate/script.md` 的 `turn-09b` 約第 224 行及 `candidate/video.json` 對應 line `3zwf` 說：「安檢時，他把推車鎖上硬殼箱。後來的 Rollaboard 才是直立雙輪，拉桿能收回。」前半句若照字面聽，是 Plath **在安檢現場**把推車鎖到箱上；[USA TODAY／ABC 2012 原報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603) 第 7 行明說他先在安檢看見旅客費力解開彈力繩綁住的箱子，**前往車庫**把推車用螺絲固定在硬殼箱上，**再返回機場**。`h6`、`t6`、兩份 r22 企劃 `chapters.turn.point` 與既有 `turn-07` 口播都正確指出在車庫動手，因此這是 r22 新轉場句自相矛盾。建議口播：「看完安檢那一幕，他回車庫把推車鎖上硬殼箱；後來的 Rollaboard 才是直立雙輪、可收拉桿。」原報導未標該安檢／車庫事件的確切年份；不得再以 1987 年補齊。

## P2 — Travelpro 的「operations」被寫成「生產」

[Travelpro 官方歷史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage) 第 275 行寫 1989 年因需求增加，Plath `moved operations from his garage to a warehouse`；它沒有單獨記載生產線搬遷。r22 兩份企劃 `chapters.turn.point` 約第 78 行及 `must_verify[4].claim` 約第 122 行新寫「1989 年**生產**搬離車庫」。同一過強詞亦已存在於 `candidate/claims.md` `n42` 約第 82 行、`candidate/script.md` `now-11` 約第 247 行及 video 對應 text。請同步降為「1989 年將營運／作業從車庫搬到倉庫」；不把官方原文推成確定的生產線遷移。這是本次改動欄位又擴散的舊精度問題，需一併改稿。

## r21 八項逐一回歸

1. **1987 車庫 Rollaboard 混同（舊 P1）**：兩份企劃現分開無年分的 ABC 安檢／車庫故事與 Travelpro 的 1987 直立雙輪設計，並標 1989 車庫搬遷；舊合一措辭已去除。這不豁免上面的 `operations` P2。
2. **安檢箱／Rollaboard 的可聽轉場（舊 P1）**：`turn-09b` 現用「後來的 Rollaboard 才是」分清外形，畫面也明寫不得等同螺絲推車箱；舊混同已去除，但同一句前半產生本次新的安檢現場時序 P1。
3. **1921 車站候宿（舊 P2）**：`must_verify[8]` 現只說搭火車到新地方、丈夫找便宜住處、Anita 守行李，並說館方未指明地點；與 [Winnetka 館方生涯文章](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/) 可得文字一致。
4. **兒子改箱定在 1928 年內（舊 P2）**：`hook-anita` 改「1928 年那趟旅行出發前」；[Winnetka 輪箱藏品文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)只支持出發前已完成，未把 1927 圖說當作同一只的確切製作年。
5. **1939→Sadow 三十多年（舊 P2）**：`idea-memory` 改「多年後」，新視覺提示只說在 1970 專利申請前且不指定旅行日期；[ABC 2010 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)與[專利申請紀錄](https://patents.google.com/patent/US3653474A/en)沒有被用來虛構確切阿魯巴回程年。
6. **`i35` 廣泛無證據結論（舊 P2）**：新句限於「本集核對的這篇 ABC 訪談未提 Anita，也未記兩者直接交接」，是對引用文章的有限觀察，不再由單篇推所有史料皆無交接。
7. **2012 記者敘述／直接引言（舊 P2）**：兩份企劃 turn 與 `must_verify[3]` 已把旅客正費力卸箱歸給記者敘述，Plath 直接引語只用於安檢員對話；對應 `h6/t5/t46` 保持「未說是否成功」。[原報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)第 7–9 行支持此區分。
8. **1970 年 10 月開賣（舊 P2）**：兩份企劃 source `supports[4]` 與 `[6]` 改為 Macy's 決定進貨、1970 年 10 月店內人偶展示，並明說 ABC 未給精確首次開賣日；與[ABC 2010 報導](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)相符。

## 驗證與限制

- `node .../A01-editorial-candidate-20261019-r22/build.mjs --check` 退出碼 0，65 scenes、77 lines、74 claims、18 public sources、1867 spoken units；250／275／300 cpm 紙上時間 518.5／478／442.8 秒，lint／cute 錯誤 0。這不是實際 TTS、剪輯或成片試看。
- r21 已聲明的限制仍在：Winnetka 原站逾時，採官方搜尋索引；1939 Midland 48 MB 原報紙只有官方庫 OCR 索引、未直接逐頁目視；RNPA 2016 PDF 本輪未重看，先前獨立 r19 審查曾直接核 pp. 46–48；Chinook 官方 PDF 與 sl8 鏡像未位元組比對；Briggs & Riley 新聞稿以 PRNewswire 原站索引核要點。這些 claim 仍是 `PENDING`，不能宣稱全面原件覆核。
- 無正式機六章銜接、worker 新 claim ID／source merge、verifier、listener、兩名敘事讀者或正式 `story/reviews/script-review.json` 收據。本文不得作為解鎖 STOP、主機寫入、付費媒體製作、YouTube 上傳的依據。下一版需要新的 manifest 與獨立審查。

本次只新增這份 r22 收據，沒有修改候選、r21／舊收據、任務票、PR、主機或任何付費資產。
