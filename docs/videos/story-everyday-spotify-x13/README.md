# X13｜Spotify 買兩家播客公司，財報能證明回本嗎？

**v7 離線前製作者稿，尚待此版獨立 SEC 逐句審核與兩名全新讀者盲評；未批准付費媒體或開 PR。** [v6 來源審核](reviews/script-source-audit-v6-independent.md)逐項對回 SEC 原件 PASS；[v6 盲讀 A](reviews/blind-a-v6-independent.md) 與 [B](reviews/blind-b-v6-independent.md) 均對 Q8 重複歸類說明答 NO，因此依雙讀者合併規則敘事 HOLD。v7 去掉 2020 播客成本入帳、Premium 月費歸屬及音樂／有聲書界線的重複句，讓開場三個未揭結果時刻變成用途與人手的連續畫面，第一二章直接接「錢從哪裡進來」，並替兩張 Shorts 數字卡明列原生 9:16 排字安全區。這些是作者修訂，不能沿用 v6 PASS 來源票或 HOLD 盲票批准新版；更早的退修票見[審查可採性](reviews/review-provenance.md)。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支，與既有品牌題不撞主事件。主線只問**2019 年 Anchor 與 Gimlet 兩筆收購能否從公開紀錄判定回本**。兩案對價合計 €308m；2020 Q1 的整個廣告業務收入同比 +€22m、總成本 +€42m，播客內容成本 +€12m 是總成本中的一項；2023 Q2 的 €30m 僅是**部分播客內容資產**沖銷；2024 首個全年營業獲利屬**全公司**；2025 廣告欄播客成本同比 −€21m 包含分類變化，不能全當真正節省。這些紀錄沒有兩案各自的累計淨回收，因此不能判定是否已回本。觀眾視角的無字核帳資料夾只是示意工具，不冒充 Spotify 內部文件；各章匿名播客卡不扮成同一檔節目。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v7 主片 119 句（含最後三句），濃縮開場 226 個稿文字元，實質正文 2,520 字元；104 張待生成插畫、10 張後製數字卡、15 個綁句 ID 的問答環。第一章後插正式 5 秒片頭，最後三句後接官方 21 秒 v4 片尾。lint 對**全片**估約 11.2 分鐘，正文若按 300 字元／分鐘約 8:24；兩者都不是錄音測量。正式 TTS 須驗正文 ≥8:00、成片約 10 分鐘。兩支 Shorts 為 9 拍與 7 拍，需真音檔驗各 25–55 秒、真 9:16 畫面及 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見 [估算](production-quote.md)。

**v7 凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `966e217eac99368048cbb58ced83ad502096c2f7b39a76c56aaa679323b5a1b0` |
| `treatment.md` | `ea28a8f00fa78399dbd8d23361fd11c881a679db9327cb3492105817bb91d089` |
| `drafts/narration.md` | `e5d9151e9ba20b1c700020187b5731d0700db246450a50eb2f72a9dbf062d2b2` |
| `drafts/shorts.md` | `17e46c204167f2175977090033117da4eb10f1b80776dedbef7d43a2ed55be2e` |
| `visual-plan.md` | `46500e989ec7a16b4e76966676972f6b76571ca70db6efffaa1a64fe0e8ed0f4` |
| `video.json` | `115c27ef31a1cf4e9cccab7b1350e4b2a1bfc5a531936b8299e2f9b46302894e` |
| `shorts.json` | `af51e6827ecdbc8059752a2c9380bc2d1ad122c7d9c46a0586905d28f05a5bf5` |
| `shorts-portrait-plan.md` | `bf88591e3c74fd9bc0526978936a2395be2ac5ffb3b123ba410fe26ee6b37d95` |

本機驗證：`compose-video.mjs` 與 `compose-shorts.mjs` 重編後，長片 lint **0 錯誤、0 警告**；兩支 Shorts 個別 `validate --source-base` 均通過，`npm run test:docs-videos` **236／236** 通過，`npm run check:tasks` exit 0（僅既有跨案警告），`git diff --check` exit 0。這些是**結構及紙面檢查**，不是來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
