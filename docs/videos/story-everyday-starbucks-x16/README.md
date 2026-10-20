# X16｜星巴克關店名單七成很新：最後關了幾家？

**狀態：離線前製 v5，等待對新 SHA 的獨立逐句 SEC 複核與兩名新讀者盲評。v3 [來源審核](reviews/script-source-audit-v3-independent.md) HOLD、兩份 [盲評 A](reviews/blind-a-v3-independent.md)／[盲評 B](reviews/blind-b-v3-independent.md)都要求重寫；v4 修正來源和敘事後因正文紙面時長風險由作者擴為 v5，兩版都尚未取得獨立 PASS。沒有付費媒體、成片、Shorts MP4、YouTube 連結或發布收據。** 這是二十支新品牌故事系列 `brand-stories-everyday-reversals-extra` 的第 16 支，與 `原來如此` B07 的 Tall 杯型命名題不同；只追 2008 年美國直營店的擴張與盤點。

主問題源自 2008-07-01 星巴克的 SEC 8-K 展品：公司**計畫**關約 600 家表現不佳的美國直營店，**其中約七成入選店從 FY2006 起才開**。店齡是這群店的統計特徵，不是公告列出的選店標準。故事跟著一張沒有地址的示意店卡：2008 年一月董事會宣布將放慢展店，七月列出單店獲利、預期回報及場址等條件；FY2008 七月群組已關 205，全年美國直營仍淨增 445；FY2009 群組再關 383，另一批約 200 家另算；FY2010 美國熟店銷售轉正，卻不能獨占成因。最後合計同一七月群組實關 588。計畫、實關、淨店數與同店各有自己的分母。

五份 SEC 原件的 URL、HTTP bytes、原始 SHA-256 與口徑在 [source-matrix.md](source-matrix.md)。長片稿在 [script.md](script.md)，六章 treatment 在 [treatment.md](treatment.md)，兩支 Shorts 逐句稿與 [逐拍直式構圖](shorts-portrait-plan.md)各自完整；[作者逐句來源表](line-source-matrix.md)與 [Shorts 作者來源表](shorts-source-matrix.md)不冒稱獨立審核。`drafts/` 是可讀母稿，`compose-video.mjs` 與 `compose-shorts.mjs` 重建 JSON、逐句稿和矩陣；更改母稿後重新產生 SHA、重審同版。

目前 JSON：主片 175 句、濃縮開場 148 字、實質正文 **2,498 字**、30 個已綁句 ID 的問答環、97 個待生圖插畫 shot、10 張後製精確數字卡；兩支 Shorts 各 8 拍、157／166 字。主片插畫占非片尾場景約 90.7%；lint 估含濃縮與結尾約 10.8 分鐘，無警告。Gemini Sulafat 指示平穩說書約每分鐘 230–250 字；紙面正文按 250 字／分鐘約 10:00，但真音檔正文 **≥8:00 仍待實測**。總片目標約 10 分鐘、Shorts 各 25–55 秒。正式 5 秒片頭在濃縮後，最後三句後接官方 21 秒 v4 片尾；繁中 CC 可關閉，AI 插畫不畫可讀字／商標／真人，縮圖品牌名由模板排橘字。整片含 Shorts、圖片評審與複查不得超 US$25，見 [production-quote.md](production-quote.md)。

v5 凍結 SHA-256：`video.json` `579015b364c78a2374b62a0a3c226c35fac3d2c1484b5b47c652f53cd859a69d`；`shorts.json` `250c52b6cc98629849ab704ce3262c638c3f8ff7382232eca5e6bc1013a6ffb2`。任何字句、鏡頭或上架文案改動都須重新編譯、更新凍結值，再請獨立審查以新 SHA 開始。

重新編譯與本機驗證：

```bash
node docs/videos/story-everyday-starbucks-x16/compose-video.mjs
node docs/videos/story-everyday-starbucks-x16/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-starbucks-x16
```

短片 JSON 是兩支腳本的陣列；`tools/video/shorts/cli.mjs validate` 每次只吃一支物件，驗證時把陣列的第 1、2 項各寫到暫存 JSON，配 `--source-base docs/videos/story-everyday-starbucks-x16`。正式媒體、音軌、結束畫面、手機版和平台網址的待辦在 [publishing-handoff.md](publishing-handoff.md)；這些尚未做，不能把前製的結構檢查當成成片 QA。
