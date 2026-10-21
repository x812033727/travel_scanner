# C03｜旁白縮編後的場景轉換條件

狀態：**版型與時長預算，尚非正式分鏡或通過 lint 的劇本**。20 段旁白已縮編；`video.json` 要等最終雜湊的獨立查核完成再建立。下列時間仍待逐句場景與 TTS 時間軸核對。

## 先處理時長

2026-10-21 初稿的同一算法為 **3,100 spoken units**，因此已縮編。現稿 `01｜` 至 `20｜` 去掉方括號製作註記及 Markdown 粗體後為 **2,160 spoken units**；其中 02–20 為 **2,025 units**，按 `DEFAULT_CPM = 250` 約 8:06。全稿純語音約 8:38；若拆成約 94 個各有一行旁白的場景，暫按每行後 300 ms、每場結束再加 700 ms，概算約 **10:12**。這只是本機時間軸估算，並非 TTS 實測。

目前以約 **10:12** 的 94 場景正文規劃，仍須實測 02–20 段旁白是否達八分鐘；正式剪輯不能靠場景間隔、快唸、凍格或片頭片尾補足正文。來源限定詞、1995／1997／2007／2013／2016–17／2025／2026 H1 的不同事件，以及每章尾的跨章問題都保留。

```powershell
node --input-type=module -e 'import fs from "node:fs"; import {spokenUnits,DEFAULT_CPM} from "./tools/video/core/timeline.mjs"; const t=fs.readFileSync("docs/videos/story-everyday-moleskine-c03/narration-draft.md","utf8"); const p=[...t.matchAll(/^(\d\d)｜(.+)$/gm)].map(x=>x[2].replace(/\[[^\]]+\]/g,"").replace(/\*\*/g,"")); const u=p.reduce((sum,x)=>sum+spokenUnits(x),0); console.log({paragraphs:p.length,spokenUnits:u,minutesSpeechOnly:u/DEFAULT_CPM});'
```

## 分鏡容量與資料結構

沿用 [插畫與成本前檢](shot-plan.md)的 **83 張 still + 11 張後製卡 = 94 正文場景**，六章分配依序為 8／17／17／21／16／15 場。若縮編稿的章節長度大幅改變，依實際 TTS 停頓重配張數，不硬套下表。全片平均正文每畫面約 6 秒；每個 `shot` 的預估旁白最長 12 秒，超過需拆鏡。故事規則的平均 still 時長 5–11 秒。

| 章 | 對應稿段號 | 初排場景 | 現稿概算時間 | 現稿 spoken units | 揭露與字卡位置 |
| --- | --- | ---: | ---: | ---: | --- |
| Hook | 01 | 7 still + 1 card | 0:40 | 135 | 2013 掛牌，留下品牌年齡與後來易主的疑問；濃縮後才接頻道片頭。 |
| Origin | 02–04 | 15 still + 2 cards | 1:25 | 284 | Chatwin 敘述必有歸屬；1995 生產與 1997 商標分卡。 |
| Idea | 05–07 | 15 still + 2 cards | 1:43 | 358 | 「待寫的書」是發行人定位；書店策略與批發據點的性質分清。 |
| Engine | 08–12 | 19 still + 2 cards | 2:21 | 501 | 2006 投資、2007 公司名、2013 上市及 2016 通路數；市值不等於銷售額。 |
| Turn | 13–16 | 14 still + 2 cards | 1:55 | 413 | 2016 簽約與 2017 完成收購分開；2017 紙本占比與營運成本。 |
| Now | 17–20 | 13 still + 2 cards | 2:08 | 469 | 2025 批發與減損、2026 H1 回升與仍虧損並列；三句收尾。 |

第六章已將 **2026 H1** 納入畫面界線；轉正式 `video.json` 時仍須保留這個較新的營運節點，避免把 2025 的下降當成持續現況。卡片安排需手工檢查最多三張連續；story lint 本身沒有這項上限。

`video.json` 對照 C02 使用 `format: "drama"`、`category: "explainer"`、`look: {"preset":"cute-mystery"}`、`characters: []`、`series: {"slug":"brand-stories-everyday-reversals","episode":3,"chapter":1}`。`category: "explainer"` 才允許 `stats`／`compare`／`steps`／`table` 等後製資料卡；旁邊的 `series.json` 的 `kind: "story"` 仍會啟用品牌故事專屬 lint。每個插畫場景必填 `template: "shot"`、`data.prompt`、`data.visual: "still"`、唯一短行 ID 和非空旁白。實際縮編後，再寫 `loops`、至少三個 HTTPS `sources`、縮圖與 YouTube 文案。

轉換後的唯讀檢查：

```powershell
node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03 --json
```

這只證明本機 JSON／brief／來源與腳本規則可過；仍需獨立逐句查核、兩位盲評、TTS 量長、音訊檢查和付費前整片報價。
