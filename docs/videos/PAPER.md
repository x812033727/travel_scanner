# 紙底版型：米白底、墨黑字、一個紅色強調

站主 2026-10-21 看了兩支深色字卡教學片後說「畫面有點弱」，對照的目標是參考頻道的扁平投影片：
米白底、墨黑字、一個紅色強調、大數字「01 煮菜」、簡單線條圖示、每張底下一句關鍵句、指令真的一個
字一個字打出來。這份寫這套看起來怎樣、`video.json` 怎麼開、哪些東西沒動。研究紀錄在
`docs/videos/reference-study-20261021/README.md`，撰稿規則在
`.agents/skills/youtube-video/references/teaching-flow.md`。

## 色盤

| 用途 | 深色主題（預設） | 紙底 `theme: "paper"` |
| --- | --- | --- |
| 底色 | `#0e2627`（漸層＋點陣） | `#f6efe3` 平塗（點陣改墨色極淡） |
| 面板（卡片、步驟、數字格） | `#173d3e` | `#fffaf1`，淡陰影 |
| 文字 | `#f7f1e8` | 墨藍 `#1f2a44` |
| 次要文字 | `#a8bcb8` | `#55607a` |
| 強調（`**文字**`、章節數字、圖示） | 青綠 `#4fc1b5` | 深青 `#1f6f6b` |
| 重點（一張最多一次：關鍵句帶的邊、大數字、進度條現在這段） | 橘 `#f0a04b` | 印章紅 `#d8452f` |
| 程式碼與終端機視窗 | `#081819` | 墨藍 `#1f2a44`（視窗保持深色，終端機才像終端機） |

字型不變：Noto Sans TC 與 JetBrains Mono。縮圖不套紙底：`thumb` 版型仍是頻道的深色縮圖，影格雜湊也
不動（`tools/video/core/timeline.mjs` `visualHash` 只在有 `theme` 時才把它算進去）。

## video.json 的欄位

| 欄位 | 寫在哪 | 規則 |
| --- | --- | --- |
| `theme: "paper"` | 頂層 | 整支套紙底。沒寫＝深色主題，輸出位元組與以前完全一樣 |
| `keys: ["…", "…"]` | 場景 `data` | 關鍵句帶：**每個渲染狀態一句**（一景一個狀態＋第一句以外每個 `reveal` 一個；第一句的 `reveal` 併進第一個狀態），每句 ≤ 24 個可見字（`**` 不算）、不能換行 |
| `key: "…"` | 場景 `data` | 只有一個狀態的場景寫這個；跟 `keys` 不能並存 |
| `numeral: "1"` | `big` 的 `data` | 一到三位數（「200」也行），畫成「01 ＋ 詞」：數字 420px 用重點色（一位數補零成兩位），`text` 在右邊 150px；`kicker`、`sub` 照舊 |
| `icon: "folder"` | `big.data`、`steps[].`、`compare.left/right.`、`bullets.items[]`（寫成 `{ "text", "icon" }`） | 十六個名字之一：`folder`、`file`、`document`、`checklist`、`terminal`、`clock`、`person`、`warning`、`book`、`gear`、`search`、`chat`、`globe`、`lock`、`lightning`、`arrow`。`bullets` 的圖示取代序號圓圈；`steps` 畫在 STEP 字下；`compare` 畫在標題前；`big` 畫在詞上方。純字串的 `items` 照舊有效，可逐條出現的數量不變 |
| `typing: "human"` | `terminal` 的 `data` | 指令每秒 12 字、輸出每秒 3 行真的打出來（沒寫＝原本 0.6 秒內打完）。`render` 先算這個狀態的打字秒數，比旁白估的時長少 0.5 秒以上才放行，否則報「the narration cannot carry the typing」：多講幾句、把輸出拆成更多 `reveal`，或縮短指令 |

關鍵句帶畫在 y 826–910（白底、左邊 10px 紅邊、44px 字），在 YouTube 下緣 15%（y 918 起）之上；CC 照舊
不燒錄。有帶子的卡片內容區從 778px 縮到 636px，塞滿的 `table`／五步 `steps` 可能放不下，`render` 會照常
報版面問題，撰稿縮短。

內容區被擠矮時，flex 會把每個字框壓得比它的行還矮，最後一行的下半截就被切掉。2026-10-29 的快報就是這樣：
140px 的第二行被切掉 28px，看起來像壓在白條下。`fitText`（`tools/video/render/browser.mjs`）只容許
字形本來就會超出行高的那一點（約 1.45 em 減行高的一半），多出來的就縮字，最多縮到 60%；縮到底還切到，就報
「text does not fit even at 60% size」。卡片上的字畫到白條範圍內，另外報「the card runs under the key
band」。這套縮字規則的版本是 `templates.mjs` 的 `FIT_VERSION`：它算進畫格快取鍵，改版後每一格都會重畫；
它也記在畫格與成片的紀錄裡，紙底、還沒上 YouTube 的影片在下一輪會重畫、重組成片（`fitStale`）。

## 範例

`tools/video/templates/fixtures/paper/video.json`：`theme`、`keys`／`key`、`numeral`、`icon`、`typing` 全用上；
它的 contact sheet 在 [`paper-look-contact-sheet.jpg`](paper-look-contact-sheet.jpg)（2026-10-21 以 Edge 渲染）。
範例只有兩分多鐘，`render` 會停在八分鐘下限的 lint，所以自己看圖用不經 lint 的重畫工具：

```bash
node tools/video/render/repeat.mjs --file tools/video/templates/fixtures/paper/video.json --channel msedge --runs 2 --out <目錄>
```

`<目錄>/run-1/` 是每個狀態的定格與轉場格（終端機的 `-tNNN.png` 逐格看打字），兩輪比對也順便證明紙底的影格可重現。
正式影片照常 `render --slug`。

## 工具裡的落點

- 影格 key＝`hash(theme.css, html, assets)`，所以 `theme.css` 一個位元組都沒改：所有新 CSS 都在
  `tools/video/templates/templates.mjs` 內嵌（`PAPER_CSS`、`KEY_BAND_CSS`、`NUMERAL_CSS`、
  `tools/video/templates/icons.mjs` 的 `ICON_CSS`），只在用到該欄位的頁面才附上，順序是版型自己的
  CSS → 關鍵句帶 → 主題（主題最後，才蓋得過版型的深底規則）。
- 狀態數的規則：`templates.mjs` `stateCount`（鏡射 `core/timeline.mjs` `buildTimeline`），測試對
  `estimateTimeline` 逐景相等。
- 打字：`templates/terminal/terminal.mjs` `HUMAN_KEY_MS`、`HUMAN_LINE_MS`、`terminalSeconds(scene, state)`；
  轉場格上限只對 `terminal` 放寬到 360 格（`render/browser.mjs` `maxTransitionFrames`），其他卡片仍 18。
- `screencast` 景也畫帶子與主題（`screencast/scene.mjs`）。

## 英文卡片的實測上限（2026-10-24，google-ai-search-ads-exception）

字卡主語言是 zh-TW（SKILL.md 規矩 14），但英文名詞、引文本來就多，國際題也可逐支選全英文卡；英文字一多，，這幾個上限 `render` 的版面檢查抓不到，要自己看聯絡表：

| 卡片 | 上限 | 沒守會怎樣 |
| --- | --- | --- |
| `big` 有 `icon` | `text` 一行、≤ 16 字元 | 190px 的英文超過約 16 字元自動折兩行，第二行壓進關鍵句帶；一行帶圖示時下伸字母也被切 |
| `big` 沒 `icon` | 最多兩行（手動 `\n`），每行 ≤ 22 字元 | 三行時最後一行在帶子下面 |
| `big` 的 `**` | 不能跨 `\n` | 跨行時 `**` 原樣印出來 |
| `quote` | 三行 100px，約 85 字元 | 第四行被來源膠囊蓋住；長句只引帶事實的子句，前面加 `…` |
| `steps`、`compare` 帶關鍵句帶 | 不寫卡片 `title` | 636px 的內容區放不下，`render` 這時才會報「text does not fit even at 60% size」 |
| `keys`／`key` | 24 字元 | 英文約四到五個字 |

這些數字量自 `google-ai-search-ads-exception` 2026-10-24 的全英文卡版本（PR #1833 的歷史）；那支片 10-25 重製成 zh-TW 卡（英文名詞、引文保留，`quote` 加 `translation`），所以 repo 裡現在的 video.json 是 zh-TW 卡的範例。
