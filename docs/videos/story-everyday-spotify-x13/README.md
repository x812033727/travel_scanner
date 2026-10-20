# X13｜Spotify 買兩家播客公司，財報能證明回本嗎？

**v4 離線前製候選，等待新一輪獨立 SEC 逐句審核與兩名完全新讀者盲評；未批准付費媒體或開 PR。** 前一版 v3 的獨立來源審核 HOLD、兩份隔離盲讀 6／7 且 No，見 [審查可採性](reviews/review-provenance.md)。v4 已修正 S9 日期、沒有證據的舊節目／排程、畫面提早變成影片觀看、章名跨季跨年因果；並將中後段改為同一個「2019 兩筆收購能否判定回本」問題逐件核對證據。這些都是作者修訂，**不能沿用 v3 的退修票作 v4 PASS**。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支，與既有品牌題不撞主事件。故事線是**疑問型**，貫穿物是觀眾視角的無字核帳資料夾，而非 Spotify 的真實內部文件；不同章的匿名播客卡不扮成同一檔節目。2019-02-14／15 的 Anchor、Gimlet 收購對價共 €308m，2023 Q2 的 €30m 僅是**部分播客內容資產**沖銷，2023-07-25 的逾十萬個影片播客是**公告當時**數量，2024 首次全年營業獲利屬**全公司**。2025 部分合格影片播客相關成本轉列 Premium，廣告欄播客成本同比 −€21m 無法全部當真正節省。公開資料無播客或兩案的獨立損益，不能判定回本。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，原始 SEC URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面與素材限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支可獨立觀看的 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v4 主片 125 句（含最後三句），濃縮開場 197 字元，實質正文 2,533 字元；112 張待生成插畫、9 張後製數字卡、13 個綁句 ID 的問答環。第一章後插正式 5 秒片頭，最後三句後接官方 21 秒 v4 片尾。lint 對**全片**估 11.2 分鐘，正文若按 300 字元／分鐘約 8:27，兩者都不是錄音測量；正式 TTS 須驗正文 ≥8:00、成片約 10 分鐘。兩支 Shorts 為 9 拍與 7 拍，需真音檔驗各 25–55 秒、真 9:16 畫面及 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見 [估算](production-quote.md)。

**v4 凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `a92ee1784c9977e7633e7359b25d1edc16335302566cfd537c0645e9c4e9b017` |
| `treatment.md` | `e550d5a23e41d3fd24fbfa98c3a776d7c911ecc2f236a8d2c234aeb8f48a757f` |
| `drafts/narration.md` | `f2d6c47b4fdd637ba6b2915e6fcffd22e3c93001a9be80d82ce0d80909bfb886` |
| `drafts/shorts.md` | `f16fb5d95f2ffcb6f7392326d356fe986df02174bbcdaf6a36676f9162cb7676` |
| `visual-plan.md` | `1dbf333e3f54867162b227d28f3ca170c9f93c55035684ebba446b2ba97eb7ae` |
| `video.json` | `22e9a6f21ecddbce71066dd798843db7eec612030e53b69b2975198bf2dc9317` |
| `shorts.json` | `07950bc98a030f359d0137e733a531b45f8ba0ab8452864b01c7f6eb83562142` |
| `shorts-portrait-plan.md` | `509cc5af6c8c53b5acbc41525713037bd89bcd080faa1b07d3cdd46d13f3f7f1` |

本機驗證：`node docs/videos/story-everyday-spotify-x13/compose-video.mjs`、`compose-shorts.mjs` 後，`node tools/video/cli.mjs lint --slug story-everyday-spotify-x13` 為 **0 錯誤、0 警告**；兩支 Shorts 的個別 JSON `validate --source-base` 通過，`npm run test:docs-videos` 與 `npm run check:tasks` exit 0（tasks 現存跨案警告）；`git diff --check` 待提交前再跑。這些是**結構及紙面檢查**，不是來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
