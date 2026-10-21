# X16｜星巴克關店名單七成很新：最後關了幾家？

**狀態：離線前製 v10 作者候選，等待同版獨立 SEC 複核與兩名新讀者盲評。** [v9 來源查核](reviews/script-source-audit-v9-independent.md)只對 v9 事實給 PASS；[盲評 A](reviews/blind-a-v9-independent.md)與[盲評 B](reviews/blind-b-v9-independent.md)同時否決 v9 的 Q3／Q8／Q13，故舊版敘事 HOLD，不能沿用審查票。本片是二十支新品牌故事系列 `brand-stories-everyday-reversals-extra` 的第 16 支，與 `原來如此` B07 的 Tall 杯型命名題不同。尚無付費媒體、成片、Shorts MP4、YouTube 連結或發布收據。

2008-07-01 星巴克**計畫**關約 600 家表現不佳的美國直營店，其中約七成入選店自 FY2006 起才開。店齡是入選群組的統計特徵；公告**未列**店齡為選店標準，不能斷言內部全然不看。故事跟著無地址的示意店卡：一月董事會決定放慢展店，一月底先規劃關約 100 家；七月公告列出單店獲利、預期回報與場址等因素；FY2008 原群組實關 205，全美直營卻淨增 445。其後同一七月群組的季末累計到 384、503、563。2009-01 另提的約 200 家美國店因消費環境轉弱與持續盤點而來，明確**在七月群組之外**。最後三句首句才揭曉七月群組跨兩財年實關 **588**。第六章改追租約如何讓費用與關門落在不同時間；FY2010 同店對照留在獨立 Short 2。

十四份 SEC 發行人原件的 URL、2026-10-20 raw bytes／SHA 和口徑見 [source-matrix.md](source-matrix.md)；新 S13／S14 供 v10 獨立審查。S3 的 13 個月定義與 S4 的 588／租約政策在正式工人約 40k 字預覽之外，必須作 `reviewer_only` 或提供可回核的一手定向短摘錄，不能宣稱來源匯入已放行。[逐句稿](script.md)、[六章 treatment](treatment.md)、[Shorts 逐句稿](shorts-script.md)和[逐拍裁切表](shorts-portrait-plan.md)均為離線交接；[長片來源標記](line-source-matrix.md)及 [Shorts 來源標記](shorts-source-matrix.md)是作者索引，不是獨立 PASS。`drafts/` 是母稿，兩個 `compose-*.mjs` 重建 JSON、稿與矩陣。

目前 JSON：長片 **155 句**、濃縮開場 148 個書寫字元、實質正文 **2,377 個書寫字元**、**2,110 個口播單位**、26 個問答環、95 張待生插畫 shot、7 張後製數字卡、1 張片尾卡；兩支 Shorts 各 8 拍、152／166 字。插畫占非片尾場景 95／102＝93.1%；靜態 lint 0 錯誤／0 警告。紙面時間線含停頓：每分鐘 250／300 單位，開場約 37.3／32.2 秒、正文約 9:46／8:20；**實際 TTS 正文 ≥8:00 尚未證明**。正式 5 秒片頭在濃縮後，最後三句後接官方 21 秒 v4 片尾；繁中 CC 可關閉，插畫不畫可讀字、商標或真人。整片含 Shorts、圖片評審與複查不得超 US$25，見 [production-quote.md](production-quote.md)。

v10 作者凍結 SHA-256：`video.json` `f2410a03ab11ad66aeab2143cdf5997bf4c7dcc26edaf4ba276971a0513088e3`；`shorts.json` `001ced8780c9058069bac84fe8f126599cf09cee77415998c8be31e46bac98d5`；`source-matrix.md` `b328facc48dfbe4d7f0f29b00cf945db14e0d79795066fe4a4470d27d081aeb8`。[v10 作者修訂記錄](reviews/v10-author-remediation.md)列出敘事修復、來源新增與驗證邊界。任何字句、鏡頭或上架文案改動都須重新編譯，更新凍結值，再請獨立審查以新 SHA 開始。

重新編譯與本機驗證：

```bash
node docs/videos/story-everyday-starbucks-x16/compose-video.mjs
node docs/videos/story-everyday-starbucks-x16/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-starbucks-x16
npm run test:docs-videos
npm run check:tasks
```

`shorts.json` 是兩支腳本的陣列；`tools/video/shorts/cli.mjs validate` 每次只吃一支物件，驗證時須各自寫暫存 JSON 並配 `--source-base docs/videos/story-everyday-starbucks-x16`。[上架交接](publishing-handoff.md)仍待真實媒體、官方素材、片長、結束畫面與平台網址收據。
