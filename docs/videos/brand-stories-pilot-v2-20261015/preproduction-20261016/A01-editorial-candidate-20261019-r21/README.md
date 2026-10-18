# A01 輪子行李箱 r21：安檢事實與敘事節奏候選 — HOLD

這是從 r20 離線候選另建的版本。建置器先核對 r20 `manifest.json`（SHA-256 `78826BCFC6356335855756FC7F81A7C846087DF340C4A7753C270C186D1077EB`）、[獨立史料差異複核](../A01-editorial-candidate-20261019-r20/independent-fact-delta-review-20261019.md)（`116A048AB552F19850F58AACCC22B8E7324591E992A7A828737CAD2DBAB5AE85`）與[故事盲讀](../A01-editorial-candidate-20261019-r20/blind-story-review-20261019.md)（`903CE88B8E43526A3862760DC198BA789B27278F891520DD84490B9A67F4701E`）。兩份審查是修改依據，**不構成 r21 的核准**。r18、r19、r20 及其審查收據均不改動。

## 與 r20 的精確差異

- `h6` 修正為 [2012 年 USA TODAY／ABC 報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)能支持的「安檢旅客正費力**想**把彈力繩綁住的箱子從金屬推車解下」；報導未說旅客是否成功。車庫後續是把行李推車**用螺絲固定在硬殼箱上**，再帶回機場。這篇未給事件精確年份。`hook-06` 口播已只說那一幕讓機師回車庫，無需改句。`t5`、`t46` 繼續維持 r20 的嘗試中界線。
- `origin-01b` 不再緊接 `origin-r12-01` 重複「第二趟長途旅行」，改說兒子改好箱子後一家六口啟程；1928 年與前後事件仍由 r20 的來源和前句界定。[Winnetka 家族史](https://www.winnetkahistory.org/who-were-the-burnhams/)記載兩次旅程。
- `engine-porter` 第一次說到 Shiller 時稱「耶魯教授」，`e37` 明確標出這是 [Yale 2008 年課堂](https://oyc.yale.edu/economics/econ-252-08/lecture-3)上的轉述，而非採購文件或 Sadow 錄音。
- 安檢員「好」之後先讓 `turn-09b` 揭曉直立雙輪、伸縮把手，再由 `turn-09` 比對 Travelpro 1987 年與 Plath 簡歷 1988 年的歧異。兩鏡只調換順序並各自修正插圖提示詞；`t7`／`t7b`／`t31` 原場景引用及各自年份歸屬不變。實際配音與剪輯停頓仍須試看。
- 23 筆編輯來源企劃與擬採用的 25 筆來源企劃同步把廣泛的「無證據顯示直接承襲／她影響 Sadow」限縮成「**本集所查來源未證實**」；`logline`、第一章 `point`、`takeaway`、`must_verify[0].claim` 共四處，來源 URL、索引和順序不變。[Travelpro 公司史](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)稱 Plath 改良 Sadow 設計，本稿仍保留這項歸屬，不把它擴大成三人直接交接原型的確證。

鏡頭 65、口播句 77、主張 74（**全為 `PENDING`**）、公開來源 18、23／25 筆企劃來源、setup／payoff ID 都不變。`plan-source-addition.json` 僅保留 r20 的未採用提案。所有編輯改動仍需新的獨立查核及故事盲讀。

## 使用界線

`validation.json` 只估算文字時間，沒有實際 TTS、剪輯、圖片或成片。1939 年報紙仍只有 OCR、未直接逐頁視讀；Chinook 的 `sl8.com` 鏡像尚未和官方 PDF 位元組比對。正式機六章、主張 ID／來源合併、verifier、listener、兩名獨立敘事讀者及正式 `story/reviews/script-review.json` 均尚未完成。保持 **HOLD**；本候選不授權主機寫入、解除 STOP、付費媒體製作或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r21/build.mjs --check
```
