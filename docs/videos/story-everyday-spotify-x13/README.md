# X13｜Spotify 關掉節目，真的放棄播客了嗎？

**v12 離線前製作者稿，仍待此版獨立 SEC 逐句審核與兩名真正新讀者盲評；未批准付費媒體或開 PR。** [v11 來源審核](reviews/script-source-audit-v11-independent.md)對前版完整 SEC 原件事實給 PASS，但正式工人定向攝取仍待驗。[v11 盲讀 A](reviews/blind-a-v11-independent.md) 和 [B](reviews/blind-b-v11-independent.md) 共同對必答 Q8 重複事實、Q13 2024 財務支線離題答 NO；A 另對 Q12 播客決策線答 NO，合併敘事 HOLD。v12 刪去 2020 分類和付款資格的重念，將 2024 非播客財務橋壓到三句，改用仍可收聽、賣出廣告曝光和既有發行者合作，接向 2025 新影片方案。前版票均不能沿用。

2026-10-21 作者重新下載 S1–S9 和兩份背景年報，各份 SEC 回應均比前一天的原始位元組多 9 bytes；[來源矩陣](source-matrix.md)記錄本次實際回應的大小與 SHA-256。這次更新不能代替另一代理對同版原件內容及每句主張的獨立審核。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支。主線從 2019 年 Anchor 創作／發行工具與 Gimlet 節目製作能力的兩筆收購出發，看 2020 Q1 整個 Ad-Supported 業務成本跑贏收入、2023 Q2 部分內容資產 €30m 沖銷與若干節目關閉；S9 的 **2023-07-25 公告**另載，當時平台可用影片播客逾十萬、同季播客廣告收入同比增逾三成，這些是不同內容或業務範圍的觀測，不代表關掉的節目改成影片。2024 Q2 整條廣告業務毛利率回到正 13%，但更直接的播客線索是免費服務仍提供線上／離線播客、播客廣告曝光售出增加、廣告網路仍支付發行者；它們也無法交代已關節目去向。2025 Partner Program 為合格影片播客創作者引入按觀看表現給付，部分市場的 Premium 會員得到沒有動態插播的新影片體驗。能證明的是**縮掉部分內容與開出新合作方式並存，並非全面放棄播客**，不能從年代相接推成單一決策因果、逐檔回歸或播客獨立獲利。兩案是否回本缺逐案損益，僅留在來源界線。匿名聽眾、創作者、播放器與無字卡均為不同時刻示意，不是假扮真節目或真員工。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)，並直接跑 `episodeShortsProblems(shorts, video)`。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v12 主片 109 句（含最後三句）、濃縮開場 233 稿文字元、實質正文 2,495 稿文字元；96 張待生成插畫、9 張後製數字卡。正文按 300 字元／分鐘約 8:19，lint 口播單位 2,455 約 8:11、全片估時約 11.1 分鐘；都不是錄音測量。正式 TTS 須實測正文 ≥8:00、成片約 10 分鐘。第一章後插正式 5 秒片頭，恰三句結尾後接官方 21 秒 v4 片尾。兩支 Shorts 分別 9／7 拍，仍須真音檔驗各 25–55 秒、原生 9:16 畫面與 360px 手機可讀性；Short 2 口播明念「歐元」。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見[估算](production-quote.md)。

**v12 作者凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `2431601fef57ad59774f620028933b261d0e2e775af933cf4c34a15f815433d0` |
| `treatment.md` | `4b32bdd7e1a47f146df1ccc3e60cc28f6ed1768ec649e6c4bd82d42db1206662` |
| `drafts/narration.md` | `ea8cdd4176e9a0ad73fcc4119068c7b40f562e418b06706ed25e5b29c03128b9` |
| `drafts/shorts.md` | `559007c4a6b45fa54e45f02deb100de24a72f4c2c534d827fb3279f61c68bec4` |
| `visual-plan.md` | `6914f69dd52f4aad53cb13dc5c3bb94e6f0b4bcca7cd143a8afae21002b71578` |
| `video.json` | `3535eaf115165d1ea3acfce1d583a947e0f28add5796f3a60e72f26753b009d8` |
| `shorts.json` | `7fe87423bed274677ce10d4699b8fd343d6a4760afe50240eb069b2ab2674579` |
| `shorts-portrait-plan.md` | `799736322511feb04ba5e118f671e53c93609eb4b44f43de1ef7bd59610e8808` |

本機編譯 lint 為 0 錯誤／0 警告；`episodeShortsProblems(shorts, video)` 為空，兩支 Shorts 個別 schema／來源 SHA 驗證通過；docs-video 測試 236／236，任務看板檢查 exit 0（仍有既有警告）。以上是作者稿與結構檢查，不能代替此版獨立來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
