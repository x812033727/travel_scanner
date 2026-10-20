# X17 Lululemon｜正式製作與連結交接

本包是**v4 離線候選稿**：v3 獨立來源審核因「第一季後七週」歧義而 HOLD，兩位新盲讀也要求修訂；那些票均不能轉作 v4 的 PASS。本版仍待全新獨立 SEC 查核及兩位全新敘事盲讀，也沒有真實配音、插畫、聲畫、正式機匯入、影片 ID 或發布網址。檔案可供獨立審核，但不能把此包寫成已通過事實審、已開工或已上架。成片必要事實只用 Lululemon 向 SEC 提交的原件 S1–S5、S6a；其中 S1、S3、S5、S6a 是短附件，S2、S4 必要段落在前 40,000 個解析文字內。其餘長 10-K 與 S7a 留作審稿補充。

**獨立審核交接。** 第二位審稿者應重抓 [`source-matrix.md`](source-matrix.md) 的六個成片 URL，核原始 byte 數／SHA，再逐行查 [`line-source-matrix.md`](line-source-matrix.md) 與 [`shorts-source-matrix.md`](shorts-source-matrix.md)。必查：S2 的一般配送流程不能冒充涉事批次史實；S3 的產線評估仍在進行、夥伴教學是後續安排、公司當時財測未變；S4 的網站轉換率／客單價、毛利率其他因素，以及 `last seven weeks of the first quarter` 必須是**第一季最後七週**；S4 其他既有商品與新品只被公司用來解釋可比門市增長，不能變成黑褲單獨銷售數；3 月的 `pull-back` 只限部分黑 Luon；4 月是布料**可能**達舊測試且多因素交疊；US$12–17m／US$57–67m 是三月**預測少賣**；US$17.5m 是 Q1 **已入帳存貨準備**；6 月 10 日的「90 天內回店」聲明晚於 5 月 5 日 Q1 截止；FY2013 營收／毛利率都是公司整體數字，FY2012 還多一週。兩位不看作者意圖的全新敘事盲讀，應在同一版 SHA 上評開場、物件連續性、章尾問題、是否成為年份／數字清單，以及兩支 Short 是否各自成篇。任一必要 claim 讀不到或盲讀要求重寫，就改母稿、重編所有 JSON、重取 hash，再審。

**媒體交接。** 待審核通過後，正式機先按 [`production-quote.md`](production-quote.md) 讀回**全項 US$25 上限**與餘額。用 `image-01`、精確 `look: {"preset":"cute-mystery"}` 生成並審核 100 張概念靜態圖，0 支生成影片 clip；用原生後製卡片排字，不生成商標或假文書。配音使用 `video.json` 的繁中逐句 `say` 暫擬發音，台灣口音 TTS 先試讀 Lululemon／Luon，人工審音再鎖。若需要改讀法，更新 `say`、`say_for` 並重編 hash；不要靠放慢語速補長。以 TTS timeline 量**實質正文 ≥8:00**，照音檔調整 16:9 剪點，短片各實測 25–55 秒，手機逐拍驗 `shorts-portrait-plan.md` 的直式裁切。字幕需可關閉，與台灣繁中成音逐字對齊。

**官方動畫和 YouTube 連結。** 第一章 30–60 秒濃縮後接頻道既有 v4 **5 秒**動畫片頭；末三句後接既有 v4 **21 秒**動畫片尾。工作樹只有交接 cue，沒有聲稱持有官方資產或製作了代用品。先在正式機確認可用素材的身分、時長、聲量和位置，再合成。最後 16 秒在 YouTube Studio 設「最符合觀眾喜好」影片、訂閱、「最新上傳」影片；私人上傳後在播放器逐一點擊驗證，靜態 MP4 畫面不能代替真連結。`video.json` 的 `youtube.video_id` 目前為 `null`，兩支 Short 沒有預填 watch URL；實際上傳後才把主片、兩支 Short、播放清單的真實 ID／URL 回填至 YouTube 描述欄、置頂留言與彼此導流位置，並做點擊驗收。此包不含上架授權。

**離線重建與確認。** 在 repo 根目錄依序跑 `node docs/videos/story-everyday-lululemon-x17/compose-video.mjs`、`node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs`；其後主片 lint、Shorts 各自 schema／主片 shot hash 驗證、`npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。兩個 composer 只寫本包檔案，不連供應商或發布平台。重新編譯會改 hash，因此獨立審核必須針對交接時 README 的**實際檔案 SHA**；舊版審核不得沿用到改稿版。
