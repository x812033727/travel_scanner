# X17 Lululemon｜正式製作與連結交接

本包是**離線候選稿**：沒有獨立來源審核收據、兩位盲讀結論、真實配音、插畫、聲畫、正式機匯入、影片 ID 或發布網址。檔案可供獨立審核，但不能把此包寫成已通過事實審、已開工或已上架。所有內容只使用 Lululemon 向 SEC 提交的可讀短原件 S1–S5、S6a、S7a 作必要事實；長 10-K 留作審稿補充，不作工人必需段落。

**獨立審核交接。** 第二位審稿者應重抓 [`source-matrix.md`](source-matrix.md) 的七個成片 URL，核原始 byte 數／SHA，再逐行查 [`line-source-matrix.md`](line-source-matrix.md) 與 [`shorts-source-matrix.md`](shorts-source-matrix.md)。必查：3 月的 `pull-back` 只限部分黑 Luon；4 月是布料**可能**達舊測試且多因素交疊；US$12–17m／US$57–67m 是三月**預測少賣**；US$17.5m 是 Q1 **已入帳存貨準備**；FY2013 營收／可比店／總可比分母與多一週的 FY2012；FY2014 毛利下降不可直接歸咎撤貨。兩位不看作者意圖的敘事盲讀，應在同一版 SHA 上評開場、物件連續性、章尾問題、是否成為年份／數字清單，以及兩支 Short 是否各自成篇。任一必要 claim 讀不到或盲讀要求重寫，就改母稿、重編所有 JSON、重取 hash，再審。

**媒體交接。** 待審核通過後，正式機先按 [`production-quote.md`](production-quote.md) 讀回**全項 US$25 上限**與餘額。用 `image-01`、精確 `look: {"preset":"cute-mystery"}` 生成並審核 116 張概念靜態圖，0 支生成影片 clip；用原生後製卡片排字，不生成商標或假文書。配音使用 `video.json` 的繁中逐句 `say` 暫擬發音，台灣口音 TTS 先試讀 Lululemon／Luon，人工審音再鎖。若需要改讀法，更新 `say`、`say_for` 並重編 hash；不要靠放慢語速補長。以 TTS timeline 量**實質正文 ≥8:00**，照音檔調整 16:9 剪點，短片各實測 25–55 秒，手機逐拍驗 `shorts-portrait-plan.md` 的直式裁切。字幕需可關閉，與台灣繁中成音逐字對齊。

**官方動畫和 YouTube 連結。** 第一章 30–60 秒濃縮後接頻道既有 v4 **5 秒**動畫片頭；末三句後接既有 v4 **21 秒**動畫片尾。工作樹只有交接 cue，沒有聲稱持有官方資產或製作了代用品。先在正式機確認可用素材的身分、時長、聲量和位置，再合成。最後 16 秒在 YouTube Studio 設「最符合觀眾喜好」影片、訂閱、「最新上傳」影片；私人上傳後在播放器逐一點擊驗證，靜態 MP4 畫面不能代替真連結。`video.json` 的 `youtube.video_id` 目前為 `null`，兩支 Short 沒有預填 watch URL；實際上傳後才把主片、兩支 Short、播放清單的真實 ID／URL 回填至 YouTube 描述欄、置頂留言與彼此導流位置，並做點擊驗收。此包不含上架授權。

**離線重建與確認。** 在 repo 根目錄依序跑 `node docs/videos/story-everyday-lululemon-x17/compose-video.mjs`、`node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs`；其後主片 lint、Shorts 各自 schema／主片 shot hash 驗證、`npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。兩個 composer 只寫本包檔案，不連供應商或發布平台。重新編譯會改 hash，因此獨立審核必須針對交接時 README 的**實際檔案 SHA**；舊版審核不得沿用到改稿版。
