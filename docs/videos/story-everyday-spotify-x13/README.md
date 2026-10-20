# X13｜Spotify 買兩家播客公司，財報能證明回本嗎？

**v9 離線前製作者稿，仍待此版獨立 SEC 逐句審核與兩名全新讀者盲評；未批准付費媒體或開 PR。** [v8 來源審核](reviews/script-source-audit-v8-independent.md)記錄原件及工人 40k 預覽限制；[v8 盲讀 A](reviews/blind-a-v8-independent.md) 與 [B](reviews/blind-b-v8-independent.md) 共同對 Q7／Q8／Q13 答 NO，A 另對 Q2 答 NO，合併敘事 HOLD。v9 把開場已揭的節目關閉改成未揭結果的內容調整紀錄，讓早期問題對準後文有答案的收入機制與成本歸欄，刪掉重複的負毛利、沖銷與成本下降數字，收短 Premium 與 2026 規模支線，最後揭兩案各自買價。舊版票不能批准本版；更早退修見[審查可採性](reviews/review-provenance.md)。

本集屬 20 支新品牌故事 `brand-stories-everyday-reversals-extra` 的第 13 支。主線只問**2019 年 Anchor 與 Gimlet 兩筆收購能否從公開紀錄判定回本**。Anchor 對價 €136m、Gimlet €172m，合計 €308m，含股份獎酬而非全是現金。2020 Q1 的**整個 Ad-Supported 業務**收入同比 +€22m、**總成本** +€42m，播客內容成本 +€12m 與版稅 +€20m 是總成本變動中的不同分項；2023 Q2 的 €30m 僅是**部分播客內容資產**沖銷；2024 首個全年營業獲利屬**全公司**；2025 廣告欄播客成本同比 −€21m 包含分類變化，不能全當真正節省。這些紀錄沒有兩案各自的累計淨回收，因此不能判定是否已回本。S8 的 2026 全服務規模留在來源矩陣備查，**不在 v9 旁白或數字卡**。匿名外部查帳者、聽眾、創作者與無字卡均為示意，不是 Spotify 員工、真節目、合約或內部會議。

主片可讀母稿在 [drafts/narration.md](drafts/narration.md)，SEC 原件 URL／位元組／雜湊及口徑在 [source-matrix.md](source-matrix.md)，六章路線在 [treatment.md](treatment.md)，畫面限制在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 編成 `video.json`、逐句稿、作者來源索引與 `series.json`。兩支獨立 Shorts 在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、逐句稿、作者來源索引與 [9:16 逐拍計畫](shorts-portrait-plan.md)，並直接跑 `episodeShortsProblems(shorts, video)`。每次更動母稿或編譯器都須重新產生 JSON，並重做綁新 SHA 的來源與盲讀審查。

v9 主片 119 句（含最後三句），濃縮開場 227 個稿文字元，實質正文 2,504 字元；103 張待生成插畫、11 張後製數字卡。第一章後插正式 5 秒片頭，最後三句後接官方 21 秒 v4 片尾。lint 對**全片**估約 11.2 分鐘，正文按 300 字元／分鐘約 8:21；兩者都不是錄音測量。正式 TTS 須驗正文 ≥8:00、成片約 10 分鐘。兩支 Shorts 為 9 拍與 7 拍，需真音檔驗各 25–55 秒、真 9:16 畫面及 360px 手機可讀性。繁中 CC 可關閉，不燒在畫面上。MiniMax `image-01` 加 `look: {"preset":"cute-mystery"}`；AI 圖不畫商標、真節目封面、真人或可讀字，品牌名／數字由後製排版。整集付費含 Shorts、評審及稅費硬上限 US$25，見 [估算](production-quote.md)。

**v9 作者凍結待審雜湊（SHA-256）：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `adb9ada1334e2f60118315ff6b3113848ab124d296911aa441583603d3235a8d` |
| `treatment.md` | `2286f4386e1d3d999685d6f3569480185559c4c4cf0cd164e5818c2d72d68c0f` |
| `drafts/narration.md` | `e00a533b7c096b1662a686b9605d5cae01b03c460dc10c1c64ccc62f3612544a` |
| `drafts/shorts.md` | `0a51f17807a42d11de0ef7d5d798a7df350f5a672ce57270699e72e94091b67c` |
| `visual-plan.md` | `5b29cc787e3970eaa365f098ca2d89ba76cbf8cdaea47163cb276d856bf2456c` |
| `video.json` | `fe84e6e051c6e3b24fbc75517243d57b6ffbb69a162448cd724bff0bcc97be0c` |
| `shorts.json` | `7c6f6086c7e1da9d07402ee125d1e39a00008356abe5a939e8a490d63d792afc` |
| `shorts-portrait-plan.md` | `df785fb86048681cfb56a416a199c118becedfb84fe0d7b62e26a141455a8d87` |

本機驗證：`compose-video.mjs` 與 `compose-shorts.mjs` 重編後，長片 lint **0 錯誤、0 警告**；直接呼叫 `episodeShortsProblems(shorts, video)` 得 **[]**，兩張 `big` 卡分別綁有效 `shot` `x13-b01-s05`／`x13-b06-s12`；兩支 Shorts 個別 `validate --source-base` 均通過；`npm run test:docs-videos` **236／236** 通過；`npm run check:tasks` exit 0（僅既有跨案警告）；`git diff --check` exit 0。這些是**結構及紙面檢查**，不是來源、敘事、配音或成片 PASS。

[上架交接](publishing-handoff.md) 列未做工作及正式動畫 SHA。此雲端沒有官方動畫檔、未付費製作、沒有 MP4、真 CC 或 YouTube 發布收據；來源連結是真 SEC URL，影片／Shorts／播放清單網址只在實際上傳後回填。
