# X16｜星巴克關店名單七成很新：最後關了幾家？

**狀態：離線前製 v9 作者候選；等待同版獨立 SEC 複核與兩名新讀者盲評。** [v8 獨立來源查核](reviews/script-source-audit-v8-independent.md)對 v8 事實給 PASS，但兩份真初讀 [A](reviews/blind-a-v8-independent.md) 與 [B](reviews/blind-b-v8-independent.md) 共同否決 Q7 未回答第二批為何出現、Q8 重複和 Q13 一月季度支線，故 v8 敘事 HOLD。v9 改寫後舊票不能沿用。沒有付費媒體、成片、Shorts MP4、YouTube 連結或發布收據。本片是二十支新品牌故事系列 `brand-stories-everyday-reversals-extra` 的第 16 支，與 `原來如此` B07 的 Tall 杯型命名題不同。

主問題源自 2008-07-01 星巴克的 SEC 8-K 展品：公司**計畫**關約 600 家表現不佳的美國直營店，**其中約七成入選店自 FY2006 起才開**。店齡是入選群組的統計特徵；公告**未列**店齡作為選店標準，不能斷言內部全然不看。故事跟著一張沒有地址的示意店卡：一月董事會宣布將放慢展店，七月列出單店獲利、預期回報與場址等因素；FY2008 原群組已關 205，全年美國直營卻淨增 445；FY2009 三份 10-Q 讓這群店的季末累計先後到 384、503、563。另一份 2009-01-28 原始公告說明因消費環境轉弱與持續盤點而加關，約 200 家美國店**在七月群組之外**，主片不追其逐季算式。最後三句首句才明說同一七月群組跨 FY2008／FY2009 實關 **588**。FY2010 的同店銷售比較留在獨立 Short 2。

十二份 SEC 原件的 URL、HTTP bytes、原始 SHA-256 與分母在 [source-matrix.md](source-matrix.md)。S12 一月短附件是 v9 作者新補的一手文件，**尚未獲獨立查核**。S4 年報的 588／退租細節與 S3 年報的開滿 13 個月定義仍須人工覆核或核准短摘錄，尚不能宣稱正式工人來源匯入放行。[逐句長片稿](script.md)、[六章 treatment](treatment.md)、[兩支 Shorts 逐句稿](shorts-script.md)和 [9:16 逐拍裁切表](shorts-portrait-plan.md)是可重建的離線交接；[長片作者來源表](line-source-matrix.md)與 [Shorts 作者來源表](shorts-source-matrix.md)不冒稱獨立審核。`drafts/` 是母稿，兩個 `compose-*.mjs` 重建 JSON、稿和矩陣。

目前 JSON：長片 154 句、濃縮開場 148 個書寫字元、實質正文 **2,351 個書寫字元**（2,090 個口播單位）、26 個問答環、94 個待生圖插畫 shot、8 張後製數字卡；兩支 Shorts 各 8 拍、152／166 字。插畫占非片尾場景約 92.2%；靜態 lint 估全片約 10.3 分鐘、0 錯誤／0 警告。Gemini Sulafat 指示每分鐘約 230–250 字；含停頓的紙面時間線按 250 字／分鐘算開場 35.5 秒、正文 9:29.7，按較快的 300 字／分鐘算開場 30.3 秒、正文 8:04.5。**真實 TTS 的實質正文 ≥8:00 尚待實測**。正式 5 秒片頭在濃縮後，最後三句後接官方 21 秒 v4 片尾；繁中 CC 可關閉，插畫不畫可讀字／商標／真人，縮圖品牌名由模板排橘字。整片含 Shorts、圖片評審與複查不得超 US$25，見 [production-quote.md](production-quote.md)。

v9 作者凍結 SHA-256：`video.json` `d8e09768665f3ad1783a9a43d62c2ede5a374f35682642cba45521dd7b32ef67`；`shorts.json` `bae123630bfaf9cb49c97998515ecd0f12720beec3bab2d2658d124fff053c37`。[v9 作者改稿記錄](reviews/v9-author-remediation.md)列出 v8 HOLD 到新候選的修訂和查核邊界。任何字句、鏡頭或上架文案改動都須重新編譯、更新凍結值，再請獨立審查以新 SHA 開始。

重新編譯與本機驗證：

```bash
node docs/videos/story-everyday-starbucks-x16/compose-video.mjs
node docs/videos/story-everyday-starbucks-x16/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-starbucks-x16
npm run test:docs-videos
npm run check:tasks
```

`shorts.json` 是兩支腳本的陣列；`tools/video/shorts/cli.mjs validate` 每次只吃一支物件，驗證時把陣列的第 1、2 項各寫到暫存 JSON，配 `--source-base docs/videos/story-everyday-starbucks-x16`。正式媒體、音軌、結束畫面、手機版和平台網址的待辦在 [publishing-handoff.md](publishing-handoff.md)；這些尚未做，不能把前製結構檢查當成成片 QA。
