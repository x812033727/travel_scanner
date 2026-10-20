# X13｜Spotify 買兩家播客公司，財報能證明回本嗎？

**v5 離線前製候選，等待獨立 SEC 逐句審核與兩名完全新讀者盲評；未批准付費媒體或開 PR。** v4 的[獨立來源審核](reviews/script-source-audit-v4-independent.md)因新影片體驗可能被讀成只限新訂戶而 HOLD；[盲讀 A](reviews/blind-a-v4-independent.md) 與[盲讀 B](reviews/blind-b-v4-independent.md) 分別只有 5／12、6／12 必答關卡為「是」，均 HOLD。v5 把開場改為 2019 收購場景及三個結果未揭的後來時刻，將 2023 沖銷、2024 全公司年度結果、2025 影片成本歸欄留到後段；刪去 The Ringer 與市場名單旁支，改正 Premium 會員新影片體驗的語意。這些都是作者修訂，**不能沿用 v4 的審查作 v5 PASS**；更早的退修票見[審查可採性](reviews/review-provenance.md)。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支，與既有品牌題不撞主事件。主線只問**2019 兩筆收購能否從公開紀錄判定回本**：Anchor 帶創作／發行工具，Gimlet 帶節目製作能力，兩案收購對價共 €308m。2023 Q2 的 €30m 僅是**部分播客內容資產**沖銷；2023-07-25 的逾十萬個影片播客是**公告當時**可用數；2024 首個全年營業獲利屬**全公司**；2025 廣告欄播客成本同比 −€21m 包含分類變化，不能全當真正節省。這些紀錄沒有兩案各自的累計淨回收，因此不能判定是否已回本。觀眾視角的無字核帳資料夾只是示意工具，不冒充 Spotify 內部文件；各章匿名播客卡不扮成同一檔節目。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v5 主片 125 句（含最後三句），濃縮開場 215 字元，實質正文 2,613 字元；111 張待生成插畫、10 張後製數字卡、14 個綁句 ID 的問答環。第一章後插正式 5 秒片頭，最後三句後接官方 21 秒 v4 片尾。lint 對**全片**估約 11.5 分鐘，正文若按 300 字元／分鐘約 8:43；兩者都不是錄音測量。正式 TTS 須驗正文 ≥8:00、成片約 10 分鐘。兩支 Shorts 為 9 拍與 7 拍，需真音檔驗各 25–55 秒、真 9:16 畫面及 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見 [估算](production-quote.md)。

**v5 凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `21151d0290bc70461daaffeeadfc33caaf31aef9a6a3a7eb372d10b2db94fae2` |
| `treatment.md` | `787e237168f077cee26f9ab615e904c0810e5c678c30ac9b0c66fd534739bd41` |
| `drafts/narration.md` | `7e9a9e0e01c56f4cc66b9eee8e1f15c5a05e31b97d8fa064e12d62f26c0c28b0` |
| `drafts/shorts.md` | `f16fb5d95f2ffcb6f7392326d356fe986df02174bbcdaf6a36676f9162cb7676` |
| `visual-plan.md` | `2ba7f620c47a0f9761986f091ab6ae4cfd8185ebd42933febaa0796c9c94cd0c` |
| `video.json` | `f7b3e849b448bcd7f5d868c84586760abf102111e03981f28be3f17682a6fa75` |
| `shorts.json` | `1cc56e53cf5c34b457d4b462daa282dbd21b80924c11fe01a433e39c09ba2603` |
| `shorts-portrait-plan.md` | `05aa8d8b0327b418638186553a39136588bcc5ab576e562ab966f90800d1e27f` |

本機驗證：`node docs/videos/story-everyday-spotify-x13/compose-video.mjs`、`compose-shorts.mjs` 後，`node tools/video/cli.mjs lint --slug story-everyday-spotify-x13` 為 **0 錯誤、0 警告**；兩支 Shorts 的個別 JSON `validate --source-base` 均通過，`npm run test:docs-videos` 為 236／236 通過，`npm run check:tasks` exit 0（現存跨案警告），`git diff --check` exit 0。這些是**結構及紙面檢查**，不是來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
