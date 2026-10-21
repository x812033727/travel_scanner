# X16｜星巴克關店名單七成很新：最後關了幾家？

**狀態：離線前製 v11 事實與敘事 HOLD。** [本版獨立 SEC 查核](reviews/script-source-audit-v11-independent.md)指出 `x160213b–c` 把美國**淨新增**門市目標寫得像毛開店目標；兩名新[盲評 A](reviews/blind-a-v11-independent.md)／[盲評 B](reviews/blind-b-v11-independent.md)都對必答 Q7／Q8／Q13 判 No，指出全美淨數提問未回收、關店句重述及同店銷售支線。須修正口徑和主線、凍結新 SHA，再做來源與雙盲查核。這是二十支新品牌故事系列 `brand-stories-everyday-reversals-extra` 第 16 支，與 `原來如此` B07 的 Tall 杯型命名題不同；尚無付費媒體、成片、Shorts MP4、YouTube 連結或發布收據。

2008-07-01 星巴克**計畫**關約 600 家表現不佳的美國直營店，其中約七成入選店自 FY2006 起才開。店齡是入選群組的統計特徵；公告**未列**店齡為選店標準，不能斷言內部全然不看。故事跟著無地址的示意店卡：一月董事會決定放慢展店，一月底先規劃關約 100 家；七月公告列出單店獲利、預期回報與場址等因素；FY2008 原群組實關 205，全美直營卻淨增 445。其後同一七月群組的季末累計到 384、503、563。2009-01 另提的約 200 家美國店因消費環境轉弱與持續盤點而來，明確**在七月群組之外**。最後三句首句才揭曉七月群組跨兩財年實關 **588**。第六章改追租約如何讓費用與關門落在不同時間；FY2010 同店對照留在獨立 Short 2。

十四份 SEC 發行人原件的 URL、2026-10-20 raw bytes／SHA 和口徑見 [source-matrix.md](source-matrix.md)。2026-10-21 重抓的 S2／S4／S11 原始檔因 SEC 防護 script 多 9 bytes，另記於 [v11 作者修訂記錄](reviews/v11-author-remediation.md)。S3 的 13 個月定義與 S4 的 588／租約政策在正式工人約 40k 字預覽之外，必須作 `reviewer_only` 或提供可回核的一手定向短摘錄，不能宣稱來源匯入已放行。[逐句稿](script.md)、[六章 treatment](treatment.md)、[Shorts 逐句稿](shorts-script.md)和[逐拍裁切表](shorts-portrait-plan.md)均為離線交接；[長片來源標記](line-source-matrix.md)及 [Shorts 來源標記](shorts-source-matrix.md)是作者索引，不是獨立 PASS。`drafts/` 是母稿，兩個 `compose-*.mjs` 重建 JSON、稿與矩陣。

目前 JSON：長片 **149 句**、濃縮開場 148 個書寫字元、實質正文 **2,301 個書寫字元**、**2,044 個口播單位**、25 個問答環、95 張待生插畫 shot、7 張後製數字卡、1 張片尾卡；兩支 Shorts 各 8 拍、152／166 字。插畫占非片尾場景 95／102＝93.1%；靜態 lint 0 錯誤／0 警告。紙面時間線含停頓：每分鐘 250／300 單位，開場約 37.3／32.2 秒、正文約 9:30／8:07；**實際 TTS 正文 ≥8:00 尚未證明**。正式 5 秒片頭在濃縮後，最後三句後接官方 21 秒 v4 片尾；繁中 CC 可關閉，插畫不畫可讀字、商標或真人。整片含 Shorts、圖片評審與複查不得超 US$25，見 [production-quote.md](production-quote.md)。

v11 作者凍結 SHA-256：`video.json` `73c8bca81c4870e3303d847bdd81d1d569721a05e6fc5017d521739c88e08533`；`shorts.json` `f570bcecc0068e68939a51a582316272254049908e46e8540cf2c6183117cd66`；`source-matrix.md` `cecc551ebabd3d0c7afc8dc607bfac6b1463acb25b5156640808b79dc1656c54`。[v11 作者修訂記錄](reviews/v11-author-remediation.md)列出五份檔案 SHA。任何字句、鏡頭或上架文案改動都須重新編譯，更新凍結值，再請獨立審查以新 SHA 開始。

重新編譯與本機驗證：

```bash
node docs/videos/story-everyday-starbucks-x16/compose-video.mjs
node docs/videos/story-everyday-starbucks-x16/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-starbucks-x16
npm run test:docs-videos
npm run check:tasks
```

`shorts.json` 是兩支腳本的陣列；`tools/video/shorts/cli.mjs validate` 每次只吃一支物件，驗證時須各自寫暫存 JSON 並配 `--source-base docs/videos/story-everyday-starbucks-x16`。[上架交接](publishing-handoff.md)仍待真實媒體、官方素材、片長、結束畫面與平台網址收據。
