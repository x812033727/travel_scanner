# X13｜Spotify 買兩家播客公司，財報能證明回本嗎？

**v6 離線前製候選，尚待此版獨立 SEC 逐句審核與兩名全新讀者盲評；未批准付費媒體或開 PR。** [v5 來源審核](reviews/script-source-audit-v5-independent.md)因廣告收入與「播客內容成本」追問的比較範圍不一致而 HOLD；[v5 盲讀 A](reviews/blind-a-v5-independent.md) 與 [B](reviews/blind-b-v5-independent.md) 分別只有 6／12、7／12 必答關卡為 YES，均 HOLD。v6 直接讓 2020 年整個廣告業務的收入增額對上同一分類的總成本增額，再把播客內容成本標成其中一項；第二、三、四章首尾相接，刪掉 2023 影片供給旁支。開場和 Short 1 的對價卡只揭金額，非純現金到後段才揭；Short 2 的首卡也只給口徑和 −€21m，未知拆分留待後段。這些是作者修訂，不能沿用前版評語當作 v6 PASS；更早的退修票見[審查可採性](reviews/review-provenance.md)。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支，與既有品牌題不撞主事件。主線只問**2019 年 Anchor 與 Gimlet 兩筆收購能否從公開紀錄判定回本**。兩案對價合計 €308m；2020 Q1 的整個廣告業務收入同比 +€22m、總成本 +€42m，播客內容成本 +€12m 是總成本中的一項；2023 Q2 的 €30m 僅是**部分播客內容資產**沖銷；2024 首個全年營業獲利屬**全公司**；2025 廣告欄播客成本同比 −€21m 包含分類變化，不能全當真正節省。這些紀錄沒有兩案各自的累計淨回收，因此不能判定是否已回本。觀眾視角的無字核帳資料夾只是示意工具，不冒充 Spotify 內部文件；各章匿名播客卡不扮成同一檔節目。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v6 主片 119 句（含最後三句），濃縮開場 212 字元，實質正文 2,472 字元；104 張待生成插畫、10 張後製數字卡、15 個綁句 ID 的問答環。第一章後插正式 5 秒片頭，最後三句後接官方 21 秒 v4 片尾。lint 對**全片**估約 11.0 分鐘，正文若按 300 字元／分鐘約 8:13；兩者都不是錄音測量。正式 TTS 須驗正文 ≥8:00、成片約 10 分鐘。兩支 Shorts 為 9 拍與 7 拍，需真音檔驗各 25–55 秒、真 9:16 畫面及 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見 [估算](production-quote.md)。

**v6 凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `21151d0290bc70461daaffeeadfc33caaf31aef9a6a3a7eb372d10b2db94fae2` |
| `treatment.md` | `2dd28484aab2c1d58c53d593df6e4e36708b7a5e58227f8585c497794c957ec8` |
| `drafts/narration.md` | `274b9d356275e2d23dca2da04f0b51d8ebe1cc51086ebc1b7c178aa777d0c9bd` |
| `drafts/shorts.md` | `17e46c204167f2175977090033117da4eb10f1b80776dedbef7d43a2ed55be2e` |
| `visual-plan.md` | `316c781d37a88b931e2916b9c3fc3fb2f856b692c9c56c0b7a4db2124a0a564b` |
| `video.json` | `efdbda8ce678347b7c19eba7b39c83d162bfb437f8c6bdef611fb2121718da15` |
| `shorts.json` | `af51e6827ecdbc8059752a2c9380bc2d1ad122c7d9c46a0586905d28f05a5bf5` |
| `shorts-portrait-plan.md` | `1afdff8741e324700c1f9e68e4bca1a0966078b91fbb0d187c2636286fd66acd` |

本機驗證：`compose-video.mjs` 與 `compose-shorts.mjs` 重編後，長片 lint **0 錯誤、0 警告**；兩支 Shorts 個別 `validate --source-base` 均通過，`npm run test:docs-videos` **236／236** 通過，`npm run check:tasks` exit 0（僅既有跨案警告），`git diff --check` exit 0。這些是**結構及紙面檢查**，不是來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
