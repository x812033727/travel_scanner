# X13｜Spotify 關掉節目，真的放棄播客了嗎？

**v13 離線前製稿：獨立事實 PASS、雙盲合併敘事 PASS，正式媒體待製作。** [本版 SEC 查核](reviews/script-source-audit-v13-independent.md)重抓九份原件；兩名全新[讀者 A](reviews/blind-a-v13-independent.md)／[讀者 B](reviews/blind-b-v13-independent.md)在同一 SHA 上沒有共同否決的必答題，依官方雙讀者規則合併通過。[合併票](reviews/narrative-v13-adjudication.md)保留 B 對重述／成本換欄段落的 Q8／Q13 異議及兩人對章名 Q9 的 advisory 異議；[作者回覆](reviews/author-response-v13.md)記錄 v12→v13 修稿。此包尚無配音、插畫、MP4、Shorts 成片、平台真網址或發布證明；正式製作由任務 `2026-10-21-spotify-x13-media-links` 續辦。

本集是 `brand-stories-everyday-reversals-extra` 第 13 支。六章追同一道問題：2019 年 Spotify 買進 Anchor 創作／發行工具與 Gimlet 節目製作能力；2020 Q1 整個 Ad-Supported 業務成本增額超過收入增額；2023 Q2 沖銷部分播客內容資產、關閉若干節目；2024 的免費播客目錄、播客廣告曝光與發行者付款仍在運作；2025 為合格影片播客創作者推出 Partner Program，相關 Premium 新觀看體驗的成本部分改列會員服務。這些時間點不構成「2020 成本直接造成 2023 關閉」的來源證明，也不能把 2023 被關節目畫成 2025 新影片。兩案是否回本、逐檔節目去向、播客獨立損益及 2025 廣告欄成本下降中真節省的比例都未公開到可下結論的程度。

2026-10-21 作者下載 S1–S9 與兩份背景年報，SEC 原始 HTML 比 10 月 20 日舊回應各多 9 bytes；[v13 獨立來源審核](reviews/script-source-audit-v13-independent.md)重新取得同日原件；舊日差異是頁尾安全 script URL 輪替。[來源矩陣](source-matrix.md)保留原件 URL、bytes、SHA 與工人約 40k 文字預覽可能截不到的段落位置，正式匯入仍須定向攝取或列人工查核。

可讀母稿在 [drafts/narration.md](drafts/narration.md)，六章設計在 [treatment.md](treatment.md)，畫面口徑在 [visual-plan.md](visual-plan.md)。`compose-video.mjs` 離線編成 `video.json`、`script.md`、`line-source-matrix.md` 和 `series.json`。兩支各自成題的 Shorts 母稿在 [drafts/shorts.md](drafts/shorts.md)；`compose-shorts.mjs` 編成 `shorts.json`、`shorts-script.md`、`shorts-source-matrix.md` 與[原生直式逐拍計畫](shorts-portrait-plan.md)。v13 主片的 scene 提示已改，Shorts 台詞和 `shorts.json` 位元組未變；新的直式計畫仍須重審有效 shot 與手機構圖。

主片紙本 109 句，濃縮開場 233 字元、實質正文 2,472 字元，按 300 字元／分鐘約 8:14；lint 口播單位 2,436，約 8:07，估計全片 11.0 分鐘。這些都不是錄音測量，正式 TTS 必須驗正文 ≥8:00。六章有 96 張待生成匿名插畫與 9 張後製數字卡。第一章後接官方 5 秒片頭，恰三句尾聲後接官方 21 秒 v4 片尾。兩支 Shorts 分別 9／7 拍，真 TTS 各須量 25–55 秒。繁中 CC 可關閉，不燒畫面；MiniMax `image-01` 用 `look: {"preset":"cute-mystery"}`，AI 圖無商標、真節目封面、真人或可讀字，品牌、日期與數字由後製排字。全套付費硬上限 US$25，見[估算](production-quote.md)。

**v13 作者凍結 SHA-256：**

| 檔案 | SHA-256 |
| --- | --- |
| `source-matrix.md` | `3332f6fc3671fa9ac9be675f6076d4c795c90a42bd0aaf81716613d7da6d94f3` |
| `treatment.md` | `b5b76a7fb01d3ccb79eed12bf75c59d6d3bb908a59b2bb3216559e42d5a48749` |
| `drafts/narration.md` | `f1445943fba144e583d1712252a9401fd705b532dd58bcfe49b3fd9e94bfa82a` |
| `drafts/shorts.md` | `b15015c060bab0934faba940ff221a62bfb30066718e2527003e8d673269129a` |
| `visual-plan.md` | `a3a2622213d4bf41d097cf50acb79f0e96700c3cb20f95c3abdad0e44d382d16` |
| `video.json` | `1e17d3e2b3fba5f7376986b952c4345224da68d771820799c75fc179a53ac2d9` |
| `shorts.json` | `7fe87423bed274677ce10d4699b8fd343d6a4760afe50240eb069b2ab2674579` |
| `shorts-portrait-plan.md` | `e6c8883dcf2efe920b3ad10e7d10f369f03463d529bd29576f26118ad0f12639` |

離線主片 lint：0 錯誤／0 警告；`episodeShortsProblems=[]`，兩支 Shorts 各自 schema 驗證為空；`npm run test:docs-videos` 236／236，`npm run check:tasks` exit 0（既有其他任務警告）。獨立來源與雙盲敘事另有上列本版 PASS 收據；上述離線檢查仍不能代替實際配音或成片驗收。

[上架交接](publishing-handoff.md)列正式工人攝取、片頭片尾、TTS、圖片、CC、Shorts 與站主驗收。這台雲端沒有官方動畫檔，也沒有製作 MP4、真 CC、手機 QA 或 YouTube 發布收據。影片、Shorts、播放清單的真 URL 只在實際上傳後回填。
