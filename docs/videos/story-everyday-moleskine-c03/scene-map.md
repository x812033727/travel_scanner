# C03｜旁白縮編後的場景轉換條件

狀態：**2026-10-21 的前期轉換表，非現行分鏡**。20 段旁白縮編時尚未建立 `video.json`；下表保留當時的容量估算，不代表目前的鏡頭配置。現行場景與字卡以 [`video.json`](video.json) 和[分鏡修訂表](shot-plan.md)為準：奇聞檔案局規則重剪後，94 景中有 **73 張插畫、21 張字卡**；素材已依新雜湊重綁與渲染，製作端已目視四頁圖聯絡表及兩張繁中財務卡，音訊與成片仍待驗收。

## 先處理時長

2026-10-21 初稿的同一算法為 **3,100 spoken units**，因此已縮編。現稿 `01｜` 至 `20｜` 去掉方括號製作註記及 Markdown 粗體後為 **2,160 spoken units**；其中 02–20 為 **2,025 units**，按 `DEFAULT_CPM = 250` 約 8:06。全稿純語音約 8:38；若拆成約 94 個各有一行旁白的場景，暫按每行後 300 ms、每場結束再加 700 ms，概算約 **10:12**。這只是本機時間軸估算，並非 TTS 實測。

目前以約 **10:12** 的 94 場景正文規劃；更正 79 家直營店後的單句配音仍遇 HTTP 429，故須重錄並實測 02–20 段旁白是否達八分鐘。正式剪輯不能靠場景間隔、快唸、凍格或片頭片尾補足正文。來源限定詞、1995／1997／2007／2013／2016–17／2025／2026 H1 的不同事件，以及每章尾的跨章問題都保留。

```powershell
node --input-type=module -e 'import fs from "node:fs"; import {spokenUnits,DEFAULT_CPM} from "./tools/video/core/timeline.mjs"; const t=fs.readFileSync("docs/videos/story-everyday-moleskine-c03/narration-draft.md","utf8"); const p=[...t.matchAll(/^(\d\d)｜(.+)$/gm)].map(x=>x[2].replace(/\[[^\]]+\]/g,"").replace(/\*\*/g,"")); const u=p.reduce((sum,x)=>sum+spokenUnits(x),0); console.log({paragraphs:p.length,spokenUnits:u,minutesSpeechOnly:u/DEFAULT_CPM});'
```

## 分鏡容量與資料結構

原先預算為 **83 張 still + 11 張後製卡 = 94 場景**，下表六章分配 8／17／17／21／16／15 是建置前初排。實際 `video.json` 的章節場景數已是 6／12／16／22／18／20，現行各章插畫與字卡數見下節及[分鏡修訂表](shot-plan.md)。更正前的 TTS 曾實測，原估時長與舊時間軸都不能代替更正後的音檔；每個畫面仍須按新旁白剪點檢查。

| 章 | 對應稿段號 | 初排場景 | 現稿概算時間 | 現稿 spoken units | 揭露與字卡位置 |
| --- | --- | ---: | ---: | ---: | --- |
| Hook | 01 | 7 still + 1 card | 0:40 | 135 | 2013 掛牌，留下品牌年齡與後來易主的疑問；濃縮後才接頻道片頭。 |
| Origin | 02–04 | 15 still + 2 cards | 1:25 | 284 | Chatwin 敘述必有歸屬；1995 生產與 1997 商標分卡。 |
| Idea | 05–07 | 15 still + 2 cards | 1:43 | 358 | 「待寫的書」是發行人定位；書店策略與批發據點的性質分清。 |
| Engine | 08–12 | 19 still + 2 cards | 2:21 | 501 | 2006 投資、2007 公司名、2013 上市及 2016 通路數；市值不等於銷售額。 |
| Turn | 13–16 | 14 still + 2 cards | 1:55 | 413 | 2016 簽約與 2017 完成收購分開；2017 紙本占比與營運成本。 |
| Now | 17–20 | 13 still + 2 cards | 2:08 | 469 | 2025 批發與減損、2026 H1 回升與仍虧損並列；三句收尾。 |

第六章已將 **2026 H1** 納入畫面界線；正式 `video.json` 仍保留這個較新的營運節點，避免把 2025 的下降當成持續現況。上表只是建置前容量估算；下列才是現行版分配。

## 現行奇聞檔案局規則重剪

| 章 | 現行插畫 | 現行字卡 |
| --- | ---: | ---: |
| Hook | 4 | 2 |
| Origin | 7 | 5 |
| Idea | 13 | 3 |
| Engine | 19 | 3 |
| Turn | 14 | 4 |
| Now | 16 | 4 |
| **合計** | **73** | **21** |

目前插畫占正文 **73／94＝77.7%**，最長連續 2 張字卡；每張 `stats` 卡的主值只放一個數字、名稱、引文或出處。品牌故事仍用 `story-` slug 和 `kind: "story"`，故程式中的 `curioProblems` 不會因 slug 自動檢查此片；本集另依 `.agents/skills/curio-episode/SKILL.md` 人工核對比例、字卡用途與視覺接受標準。現行 `lint` 為 0 錯誤、0 警告；73 張圖已按新畫面雜湊重綁且評審通過、21 卡已渲染，製作端目視四頁圖聯絡表及兩張繁中財務卡。此階段不等於音訊或成片驗收。[Curio 重剪覆核](reviews/curio-rules-recut.md)綁定目前版本雜湊並列出尚待的語音與成片關卡。

`video.json` 對照 C02 使用 `format: "drama"`、`category: "explainer"`、`look: {"preset":"cute-mystery"}`、`characters: []`、`series: {"slug":"brand-stories-everyday-reversals","episode":3,"chapter":1}`。`category: "explainer"` 才允許 `stats`／`compare`／`steps`／`table` 等後製資料卡；旁邊的 `series.json` 的 `kind: "story"` 仍會啟用品牌故事專屬 lint。每個插畫場景必填 `template: "shot"`、`data.prompt`、`data.visual: "still"`、唯一短行 ID 和非空旁白。實際縮編後，再寫 `loops`、至少三個 HTTPS `sources`、縮圖與 YouTube 文案。

轉換後的唯讀檢查：

```powershell
node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03 --json
```

這只證明本機 JSON／brief／來源與腳本規則可過；仍需獨立逐句查核、兩位盲評、TTS 量長、音訊檢查和付費前整片報價。
