# sothatswhy-p02-cloud-rain 分鏡評分（第四輪，獨立評分）

- 評分表：`docs/videos/so-thats-why/dialogue-pilot-20261103/SCORECARD.md` 第二段〈分鏡〉，六項各 1–10，門檻總分 ≥ 42 且沒有任何一項低於 5。
- 評分者：獨立代理，沒有畫這批圖，也沒有看 `review/` 裡先前的評分檔。
- 看過的材料：分鏡v4-1～5 總表（100 鏡）、`keyframes/manifest.json` 指到的 100 張 1280×720 原圖（四張一組放大逐張看過，可疑處再裁切放大）、所長 `characters/chief/103.jpg` 與小問 `characters/kid/002.jpg` 參考圖、`video.json` 每鏡台詞、`node tools/video/cli.mjs lint` 的時間估算。總表上的「x/10」是出圖工具自己的評審，不當證據。
- 時間：依 lint 的 11.5 分鐘按字數比例分給各鏡（含 `pause_after_ms`），117 場（100 張圖、17 張文字卡）。

## 分數

| 項目 | 分數 | 一句話 |
| --- | --- | --- |
| 角色一致 | **5** | 所長大多認得出來，但髮型在低馬尾和包頭之間換來換去，有幾張變成別人；小問的髮型至少在五種之間漂 |
| 開場 30 秒 | **7** | 30 秒內有 6 張圖；第一張是小問指著雲，雲在畫面裡但不是主體；第二張才是那朵雲本身 |
| 一人一事 | **6** | 兩個角色從不同框（好）；但有 12 張空景、4 張出現路人、7 張主角小到看不清臉，大半張只是站著說話 |
| 畫面與旁白對得上 | **6** | 關鍵比喻大多畫到了，但冰飲料杯外面沒有水珠、積雨雲畫成像爆炸蕈狀雲，另有約十張畫面在講別件事 |
| 沒有假字 | **5** | 3 張有印章（紙角紅印、紅色圓章、郵票），另有 3 張出現明顯的假字，還有 8 張有細小亂碼 |
| 換圖間隔 | **9** | 估算每張圖中位數約 5.9 秒（連文字卡算約 6.1 秒），最長的圖約 10 秒、最長的文字卡約 14 秒，都不到 20 秒 |
| **總分** | **38／60** | **不通過**（門檻 42；沒有一項低於 5，但總分不到） |

## 各項依據

### 1. 角色一致：5

參考圖：所長是圓形粗黑框眼鏡、深色頭髮帶一撮灰、低馬尾、鉛筆夾在耳後、芥末黃開襟衫；小問是黑色短鮑伯頭、齊瀏海、頭頂一根翹毛、海軍藍雨衣配芥末黃帽兜。

- **所長變成別人**：`chief-later` 像一位年長女性，灰髮一圈包住臉、中分，戴細的棕色圓框眼鏡，不是粗黑框，看不出是所長。`chief-second` 是方框眼鏡，看不到灰色那一撮。`chief-anvil` 是細框眼鏡，臉型和畫風都換了。
- **所長的髮型在兩種之間漂**：參考圖是低馬尾，可是有 9 張是包頭或高髮髻（`chief-kettle`、`mist-puff`、`chief-whiteboard`、`chief-answer-one`、`supercooled`、`chief-still-there`、`chief-ice-wins`、`chief-remember`、`chief-not-tear`）。髮色也會變成棕色（`chief-folder`、`chief-no-pinch`、`chief-told-you`）。`chief-remember` 是整個頭頂都灰，不是一撮灰。
- **小問的髮型漂得更厲害**：
  - 馬尾或沖天辮：`kid-why-not-fall`、`clear-morning`、`kid-snowball`（還多了紅色髮圈）、`cold-gust`
  - 包頭：`kid-vapour-guess`（雙包頭）、`droplet-vanish`、`kid-noon-guess`（紅髮繩）、`kid-laundry-run`
  - 長髮過肩：`kid-puzzled`、`kid-burger`（捲的）
  - 怪的長髮絲：`kid-no-weight`（一條垂到腰的黑髮）
  - 戴帽子：`updraft-section`
  - 畫得像男孩：`kid-flat-bottoms`、`kid-elephants`、`kid-ten-km`
- 加分的地方：配色（芥末黃配海軍藍）幾乎張張都對，所長的眼鏡和鉛筆大多都在，所以觀眾分得出誰是誰。

這正好是評分表 4 分的描述：「髮型在兩三種之間漂、所長偶爾變成別人」。因為配色守得住，給 5 分。

### 2. 開場 30 秒：7

- 前 30 秒有 6 張圖：`balcony-call` 0 秒、`tower-greying` 5.5 秒、`chief-folder` 9.7 秒、`kid-puzzled` 13.0 秒、`chief-yes` 17.2 秒、`chief-window` 23.4 秒；`town-cloud-wide` 在 29.9 秒才進來。≥ 3 張這條達到了。
- 第一張 `balcony-call`：主體是小問在陽台上指東西，雲在她背後的天空裡，看得到是什麼，但畫面重點是人不是雲。第二張 `tower-greying` 才是「問題本身」：那朵雲，下面發灰。
- 扣分：
  - `chief-folder` 的台詞是「等一下可能要收衣服」，畫面卻是所長在辦公桌前看文件，沒有雲，也沒有衣服。
  - `kid-puzzled` 的紙上有印章（見第 5 項）。
  - `chief-yes` 講「五百公噸的水」，畫面只是所長攤手，沒有雲。

  開場最貴的 30 秒裡，只有兩張在畫那朵雲。

### 3. 一人一事：6

- 好的地方：沒有任何一張是所長和小問同框，大部分角色鏡頭的臉都朝向鏡頭。
- **空景（沒有人，也不算回答問題的插入鏡頭）**：`tower-greying`、`spout-gap`、`warm-bubble`、`nucleus-droplet`、`iced-cup`、`cauliflower-grow`、`elephants`、`cold-top`、`grey-base`、`rain-drags`、`sign-anvil`、`cumulonimbus`，共 12 張。其中 `tower-greying`、`spout-gap`、`rain-drags`、`sign-anvil` 本身就是證據，可以留下。
- **路人或不明人物**：`hot-street`（騎機車的八字鬍大叔）、`mountain-hike`（穿綠外套的男孩，乍看像另一位主角）、`flat-bases`（戴斗笠的農夫）、`condense-high`（遠處戴黃帽的小人和拖傘）。
- **主角小到看不清臉，或只拍到側面**：`kid-vapour-guess`、`condense-high`、`updraft-section`、`cloud-stays`、`small-clouds`、`mountain-clouds`、`chief-how-high`（所長小小的側身摸牆，畫面約九成是空牆）。
- 大半張圖的動作只是「站著說話」或「看」（`chief-answer-one`、`chief-caveat`、`chief-stamp`、`kid-elevator` 等）。lint 也報 `motion.look` 100%。

### 4. 畫面與旁白對得上：6

畫到了的：水壺口那段透明（`spout-gap`）、`mist-puff`、熱空氣泡（`warm-bubble`）、`kid-balloon`、放大鏡下的微粒（`chief-magnifier`）、凝結核（`nucleus-droplet`）、平底的雲（`flat-bases`）、`elephants`、羽毛和石頭（`feather-stone`）、時鐘（`chief-a-day`、`kid-noon-guess`）、雨柱（`rain-shaft`）、`rain-drags`、鐵砧雲（`sign-anvil`）、衣服被風吹起（`sign-gust`）、`kid-burger`。

對不上的：

- `iced-cup`：台詞是「杯子外面會冒出水珠」，放大看，杯子外壁沒有水珠，只有一杯畫了笑臉的飲料。這是本章的關鍵比喻。
- `cumulonimbus`：台詞是「雲頂可以超過十公里，跟客機一樣高」。畫面是一朵有臉的蕈狀雲，底下接一根像煙囪的柱子，蓋在城市上方，空中飛的是一個像炸彈的怪東西，沒有客機，兩邊還有黃色小怪物。很容易被看成爆炸。
- `chief-how-high`：講「雲能長多高」，畫面是所長摸牆，沒有雲。
- `chief-folder`：講收衣服，畫面是看文件。
- `chief-batch`：講「雨滴一秒落下六、七公尺」，畫面上沒有雨滴。
- `chief-anvil`：講「像一個鐵砧」，畫面上沒有鐵砧，也沒有雲，只有舉手。
- `chief-phone-call`：講「還記得花椰菜嗎…你抬頭就看得到」，畫面是講電話。
- `chief-stamp`：講「引擎關掉雲就散了，每一顆是一百萬顆雲滴」，畫面是拿一個空白文件夾。
- `supercooled`：講「零度以下卻沒結冰的小水滴」，放大鏡裡畫的是冰晶。
- `dry-afternoon`：講濕度、高空溫度和風，畫面是海邊拿冰淇淋。
- `chief-laugh`：講「你家上面可能也浮著一朵」，畫面上沒有雲。
- `chief-yes`：講五百公噸的水，畫面上沒有雲。
- `kid-vapour-guess`：問水蒸氣，畫面是空背景上很小的小問。

### 5. 沒有假字：5

逐張放大後找到：

- **印章**：
  - `kid-puzzled`：小問手上那張紙，左上角和右下角各有一個紅色小方印。
  - `chief-expands`：所長頭旁有一個紅色圓章，章裡有字形筆畫。
  - `chief-later`：畫面下緣有一張紅色郵票，帶齒孔邊。
- **明顯的假字**：
  - `kid-why-not-fall`：雨衣胸口有「UPL」樣的字母。
  - `chief-no-pinch`：頭上的紅色驚嘆符號被畫成「H:」、「L:」樣的字形。
  - `rain-stops`：小問手上的紙寫滿紅色像字的筆畫，而且在畫面正中。
- **細小亂碼**（播放尺寸下不太顯眼）：
  - `cold-top`：機身有一排假字，機尾有標誌。
  - `chief-blocked`：白板向下的箭頭裡有手寫小字。
  - `cold-gust`：右緣門牌上有紅字。
  - `kid-laundry-run`：洗衣籃裡的盒子上有字。
  - `kid-but-stays`：筆記本封面有字。
  - `kid-ten-km`：粉紅色筆記本封面有字。
  - `kid-vapour-guess`：卡片上有紅字。
  - `balcony-call`：紙角有小字。
  - `kid-million`：桌上的紙有表格狀的假字。

評分表 4 分的描述是「角落有印章、招牌有亂碼」。這批有 3 張真的有印章，另外 3 張有明顯的假字，所以在下限給 5 分。

### 6. 換圖間隔：9

- 依 lint 的總長按字數比例估算：100 張圖每張的中位數約 5.9 秒；把 17 張文字卡也算進去，中位數約 6.1 秒。lint 自己算的鏡頭中位數是 5.9 秒。
- 最長的圖是 `kid-was-snow` 約 10.0 秒，其次是 `kid-ten-km` 9.7 秒、`cumulonimbus` 9.2 秒。最長的文字卡是 `outro` 約 14 秒、`drop-shapes` 約 13.9 秒。都在 20 秒以內。
- 中位數落在評分表 6–12 秒的下緣；只算圖的話略快於 6 秒，但評分表的 4 分是「太慢」，太快不算犯規，所以只扣 1 分。注意：lint 用的 drama-craft 標準是 2–4 秒，比這張評分表嚴格得多，兩者並不衝突。

## 問題鏡頭清單

### 必須重畫（13 張）

| 鏡頭 | 問題 |
| --- | --- |
| `kid-puzzled` | 紙角有兩個紅印章；小問變成過肩長髮、皺眉 |
| `chief-expands` | 紅色圓章，章裡有字形 |
| `chief-later` | 所長變成別人（年長、細棕框、灰髮包臉）；下緣有郵票 |
| `rain-stops` | 手上紙張滿是紅色假字，在畫面正中 |
| `chief-no-pinch` | 驚嘆符號畫成「H:」、「L:」假字；頭髮變棕色 |
| `kid-why-not-fall` | 雨衣胸口有「UPL」字母；小問綁馬尾 |
| `kid-million` | 雙手像半透明的鬼影；下方紙張有表格狀假字 |
| `kid-no-weight` | 一條黑髮從頭垂到腰，像壞掉的筆畫；表情凶 |
| `chief-second` | 方框眼鏡，看不到那撮灰髮 |
| `chief-anvil` | 細框眼鏡，臉不像所長；台詞講鐵砧，畫面上沒有鐵砧也沒有雲 |
| `iced-cup` | 關鍵比喻「杯子外面冒水珠」沒畫出來 |
| `cumulonimbus` | 看起來像爆炸蕈狀雲加煙囪，沒有客機，有怪物和像炸彈的東西 |
| `chief-how-high` | 所長小小的側身，九成是空牆，沒有雲（出圖工具自己也只給 7.18） |

### 可以容忍（有空再修）

- **小問髮型漂移**：`clear-morning`、`kid-vapour-guess`、`kid-snowball`、`droplet-vanish`、`kid-noon-guess`、`cold-gust`、`kid-laundry-run`、`kid-burger`、`updraft-section`、`kid-flat-bottoms`、`kid-elephants`、`kid-ten-km`
- **所長包頭或棕髮**：`chief-folder`、`chief-kettle`、`mist-puff`、`chief-whiteboard`、`chief-answer-one`、`supercooled`、`chief-still-there`、`chief-ice-wins`、`chief-remember`、`chief-not-tear`、`chief-told-you`
- **細小假字**：`cold-top`、`chief-blocked`、`cold-gust`、`kid-laundry-run`、`kid-but-stays`、`kid-ten-km`、`kid-vapour-guess`、`balcony-call`
- **畫面和台詞偏離**：`chief-folder`、`chief-yes`、`chief-laugh`、`chief-batch`、`chief-phone-call`、`chief-stamp`、`supercooled`、`dry-afternoon`、`kid-vapour-guess`
- **路人**：`hot-street`、`mountain-hike`、`flat-bases`、`condense-high`
- **主角太小或空景偏多**：`kid-vapour-guess`、`updraft-section`、`cloud-stays`、`small-clouds`、`mountain-clouds`、`warm-bubble`、`cauliflower-grow`、`elephants`、`cold-top`、`grey-base`（雲底畫成黑洞，有點怪）
- **開場**：`balcony-call` 可以考慮把雲拉成主體，或對調前兩張，讓第一張就是那朵雲。

## 預估

如果 13 張必須重畫的都修好：
- 「沒有假字」可以到 8
- 「角色一致」可以到 6（小問的髮型漂移仍普遍）
- 「畫面與旁白」可以到 7

總分約 6 + 7 + 6 + 7 + 8 + 9 = 43，剛好過門檻。想要穩過，還要把「可以容忍」清單裡小問的髮型統一回鮑伯頭，並把 `chief-folder`、`chief-yes` 改成畫雲。
