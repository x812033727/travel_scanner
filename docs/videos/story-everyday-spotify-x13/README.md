# X13｜Spotify 買兩家播客公司，財報能證明回本嗎？

**v8 離線前製作者稿，仍待此版獨立 SEC 逐句審核與兩名全新讀者盲評；未批准付費媒體或開 PR。** [v7 來源審核](reviews/script-source-audit-v7-independent.md)重抓 S1–S9 並 PASS；[v7 盲讀 A](reviews/blind-a-v7-independent.md) 與 [B](reviews/blind-b-v7-independent.md) 均對 Q4／Q5／Q8／Q11 答 NO，B 另對 Q3 答 NO，合併敘事 HOLD。兩人也發現當時 Shorts 把長片 `stats` 當成 `shot`，會被製作管線拒絕。v8 作者改成三個未揭結果的具體開場動作、第二章首句直答播放不等於回本、剪掉逐案歸類和成本換欄的重複說明，並改用**有效 shot 背景＋原生 `big` 直式數字**。舊版 PASS／HOLD 票不能沿用來批准 v8；更早的退修票見[審查可採性](reviews/review-provenance.md)。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支，與既有品牌題不撞主事件。主線只問**2019 年 Anchor 與 Gimlet 兩筆收購能否從公開紀錄判定回本**。兩案對價合計 €308m；2020 Q1 的**整個廣告業務**收入同比 +€22m、總成本 +€42m，播客內容成本 +€12m 與版稅 +€20m 是總成本中的不同分項；2023 Q2 的 €30m 僅是**部分播客內容資產**沖銷；2024 首個全年營業獲利屬**全公司**；2025 廣告欄播客成本同比 −€21m 包含分類變化，不能全當真正節省；2026 Q2 的 777m 月活與 300m Premium 訂閱戶口徑重疊、不能相加，屬全服務規模，不是兩案回款。這些紀錄沒有兩案各自的累計淨回收，因此不能判定是否已回本。v8 **新增** S8 使用規模入旁白與兩張長片數字卡，須由新版來源審核逐項查核。觀眾視角的無字核帳資料夾只是示意工具，不冒充 Spotify 內部文件；各章匿名播客卡不扮成同一檔節目。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)，並直接跑 `episodeShortsProblems(shorts, video)`。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v8 主片 119 句（含最後三句），濃縮開場 227 個稿文字元，實質正文 2,512 字元；102 張待生成插畫、12 張後製數字卡、17 個綁句 ID 的問答環。第一章後插正式 5 秒片頭，最後三句後接官方 21 秒 v4 片尾。lint 對**全片**估約 11.2 分鐘，正文若按 300 字元／分鐘約 8:22；兩者都不是錄音測量。正式 TTS 須驗正文 ≥8:00、成片約 10 分鐘。兩支 Shorts 為 9 拍與 7 拍，需真音檔驗各 25–55 秒、真 9:16 畫面及 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見 [估算](production-quote.md)。

**v8 作者凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `966e217eac99368048cbb58ced83ad502096c2f7b39a76c56aaa679323b5a1b0` |
| `treatment.md` | `76194d2664fd7c55f68e8fa6cea419f1ed34385a3de368a682767a399cdb4c6b` |
| `drafts/narration.md` | `3f433c5c44d0215cce2a825ec87a58b64883facd553de71a50d6ac18f12b218a` |
| `drafts/shorts.md` | `1c1321e69df9864fba151bdbafccdd1adf76c3d504b0b1af6b7ae2e250ed0cdd` |
| `visual-plan.md` | `6b878807e5b16c36f6897a5784f0f54f4fced0143de759002b06334621f31d4f` |
| `video.json` | `70963bccd37b68aa67163a1d31b5f1db48d52bd772ccdf55f41be90615a7f928` |
| `shorts.json` | `8b0c0d88e1f568154e2ba076feab755657fd422a971da504b8562bcb38afe1ec` |
| `shorts-portrait-plan.md` | `b6b71b32b71aec6efcafa924d2c3e5731eed9c25af5f8a6d0b6f2f97de0feb61` |

本機驗證：`compose-video.mjs` 與 `compose-shorts.mjs` 重編後，長片 lint **0 錯誤、0 警告**；直接呼叫 `episodeShortsProblems(shorts, video)` 得 **[]**，兩張 `big` 卡分別綁有效 `shot` `x13-b01-s05`／`x13-b06-s12`；兩支 Shorts 個別 `validate --source-base` 均通過；`npm run test:docs-videos` **236／236** 通過；`npm run check:tasks` exit 0（僅既有跨案警告）；`git diff --check` exit 0。這些是**結構及紙面檢查**，不是來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
