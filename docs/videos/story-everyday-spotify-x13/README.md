# X13｜Spotify 關掉節目，真的放棄播客了嗎？

**v11 離線前製作者稿，仍待此版獨立 SEC 逐句審核與兩名真正新讀者盲評；未批准付費媒體或開 PR。** [v10 來源審核](reviews/script-source-audit-v10-independent.md)對前版完整 SEC 原件事實給 PASS，但正式工人定向攝取仍待驗。[v10 盲讀 A](reviews/blind-a-v10-independent.md) 和 [B](reviews/blind-b-v10-independent.md) 共同對必答 Q7 回呼不足、Q8 重複數字、Q13 全公司年結離題答 NO，合併敘事 HOLD。v11 明確接回開場紀錄與影片入口，刪去重念買價／成本增額及全公司年度旁支；v10 票均不能沿用。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支。主線從 2019 年 Anchor 創作／發行工具與 Gimlet 節目製作能力的兩筆收購出發，看 2020 Q1 整個 Ad-Supported 業務成本跑贏收入、2023 Q2 部分內容資產 €30m 沖銷與若干節目關閉；S9 的 **2023-07-25 公告**另載，當時平台可用影片播客逾十萬，這是不同內容的供給數，不代表關掉的節目改成影片。2024 Q2 整條廣告業務毛利率回到正 13%，仍無逐檔節目去向；2025 Partner Program 又為合格影片播客創作者引入按觀看表現給付，部分市場的 Premium 會員得到沒有動態插播的新影片體驗。能證明的是**縮掉部分內容與開出新合作方式並存，並非全面放棄播客**，不能從年代相接推成單一決策因果、逐檔回歸或播客獨立獲利。兩案是否回本缺逐案損益，僅在後段一次說明界線。匿名聽眾、創作者、播放器與無字卡均為不同時刻示意，不是假扮真節目或真員工。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)，並直接跑 `episodeShortsProblems(shorts, video)`。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v11 主片 112 句（含最後三句）、濃縮開場 233 稿文字元、實質正文 2,537 稿文字元；99 張待生成插畫、9 張後製數字卡。正文按 300 字元／分鐘約 8:27，lint 口播單位 2,503 約 8:20、全片估時約 11 分鐘；都不是錄音測量。正式 TTS 須實測正文 ≥8:00、成片約 10 分鐘。第一章後插正式 5 秒片頭，恰三句結尾後接官方 21 秒 v4 片尾。兩支 Shorts 分別 9／7 拍，仍須真音檔驗各 25–55 秒、原生 9:16 畫面與 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見[估算](production-quote.md)。

**v11 作者凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `5ba178c5413bcc45b5b0e34b6e33fc2e45f6613754ba4e0eac6b0121f3c32d08` |
| `treatment.md` | `b1ff09ff7863170b64b374b0a109ade5323e08a4423dd792e5b49a5c06bc0b99` |
| `drafts/narration.md` | `ccc83bfe58d3075081a3550628285b9b4915eefa51f42bc37a2dad73d7a29e24` |
| `drafts/shorts.md` | `d336ce053708f6a484f908ca7156ef171117c0a555fcb8a2c1e4b327b05fe8ee` |
| `visual-plan.md` | `7043b0de393847425b6dcb689339dec971d72ceb777e20c7481c516f4280a91a` |
| `video.json` | `5d38f42b8c8de9af92d4c944fc2d56bb2bcebd822fdf2c81d11199e691aa4614` |
| `shorts.json` | `cfc0e99620da3884f459283b0a2e68a97d6801b8b9b3b9b7c8bbf35e93be9f30` |
| `shorts-portrait-plan.md` | `8a9db6765e90996d5e101ebf4194b379680e5b96f7c26bd0ec6e04971e8fc5c9` |

本機編譯 lint 為 0 錯誤／0 警告；`episodeShortsProblems(shorts, video)` 為空，兩支 Shorts 個別 schema／來源 SHA 驗證通過；docs-video 測試 236／236，任務看板檢查 exit 0（仍有既有警告）。以上是作者稿與結構檢查，不能代替此版獨立來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
