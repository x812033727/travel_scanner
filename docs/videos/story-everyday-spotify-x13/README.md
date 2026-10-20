# X13｜Spotify 關掉節目，真的放棄播客了嗎？

**v10 離線前製作者稿，仍待此版獨立 SEC 逐句審核與兩名真正新讀者盲評；未批准付費媒體或開 PR。** [v9 來源審核](reviews/script-source-audit-v9-independent.md)對綁定的完整 SEC 原件事實給 PASS，但正式工人 40k 文字預覽限制未解；合格 [v9 盲讀 B](reviews/blind-b-v9-independent.md) 與 [C](reviews/blind-c-v9-independent.md) 共同對 Q8 重複說明答 NO，C 另對 Q3／Q7 答 NO，合併敘事 HOLD。[A 評語](reviews/blind-a-v9-independent.md)因作答前看過舊版摘要，僅供編輯參考，不算雙盲票。v10 將主問題從未公開、無法逐案回答的回本改成**2023 年縮掉部分節目後，Spotify 是否全面放棄播客**；v9 票均不能沿用。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支。主線從 2019 年 Anchor 創作／發行工具與 Gimlet 節目製作能力的兩筆收購出發，看 2020 Q1 整個 Ad-Supported 業務成本跑贏收入、2023 Q2 部分內容資產 €30m 沖銷與若干節目關閉；S9 的 **2023-07-25 公告**另載，當時平台可用影片播客逾十萬，這是不同內容的供給數，不代表關掉的節目改成影片。2024 Q2 整條廣告業務毛利率回到正 13%，公司同年首次錄得全公司全年營業獲利；2025 Partner Program 又為合格影片播客創作者引入按觀看表現給付，部分市場的 Premium 會員得到沒有動態插播的新影片體驗。能證明的是**縮掉部分內容與開出新合作方式並存，並非全面放棄播客**，不能從年代相接推成單一決策因果、逐檔回歸或播客獨立獲利。兩案是否回本缺逐案損益，僅在後段一次說明界線。匿名聽眾、創作者、播放器與無字卡均為不同時刻示意，不是假扮真節目或真員工。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)，並直接跑 `episodeShortsProblems(shorts, video)`。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v10 主片 112 句（含最後三句）、濃縮開場 233 稿文字元、實質正文 2,500 稿文字元；98 張待生成插畫、10 張後製數字卡。正文按 300 字元／分鐘約 8:20，lint 全片估時約 11 分鐘；兩者都不是錄音測量。正式 TTS 須實測正文 ≥8:00、成片約 10 分鐘。第一章後插正式 5 秒片頭，恰三句結尾後接官方 21 秒 v4 片尾。兩支 Shorts 分別 9／7 拍，仍須真音檔驗各 25–55 秒、原生 9:16 畫面與 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見[估算](production-quote.md)。

**v10 作者凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `793fa8606ec7947548fbf1ca752e6dea795630a9e9a63f9f2bcb25e6e0b7c6d7` |
| `treatment.md` | `936368c5aab6157710337984869555708a4be94e9c31d1ad06db8df8a26e10f2` |
| `drafts/narration.md` | `16007b05032e99ce7ddc5992293f207b015f40abee947db8e3c29943be461ce0` |
| `drafts/shorts.md` | `ce2a69d957ddd9ad421095d0fbb94d93167ce79f163aa0bb3b04799ab8050633` |
| `visual-plan.md` | `f91b34c3e0f8506be1cee1a1d076d8ffc63fbcce44ed45bb41468566f1987b22` |
| `video.json` | `8d2e2ef6c8c6a59dfbac54c1086f79423e04d975dad9e2e5a5ca93d3fdff92e7` |
| `shorts.json` | `cfc0e99620da3884f459283b0a2e68a97d6801b8b9b3b9b7c8bbf35e93be9f30` |
| `shorts-portrait-plan.md` | `dbdcc8bb7763a1a2ea92b5616be1c33fa1b7427b313a5422263825f41e4a6ce7` |

本機編譯 lint 為 0 錯誤／0 警告；`episodeShortsProblems(shorts, video)` 為空，兩支 Shorts 個別 schema／來源 SHA 驗證通過；docs-video 測試 236／236，任務看板檢查 exit 0（仍有既有警告）。以上是作者稿與結構檢查，不能代替此版獨立來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
