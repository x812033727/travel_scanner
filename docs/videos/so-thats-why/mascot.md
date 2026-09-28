# 原來如此事務所：所長與片頭

2026-09-28 起草。吉祥物「所長」出現在每集片頭、章節卡與結尾蓋章；關鍵影格要拿選定的設定圖當參考圖，100 集才會長得一樣。這份給三個造型方向讓站主選，選定後照漫劇路線的 `look` 流程生成候選設定圖（`node tools/video/cli.mjs look --slug <SLUG> --candidates 3`），站主在後台選一張，雜湊記在最後一節。

## 共同規則

- **原創**：不能像任何既有卡通角色、頻道吉祥物或品牌吉祥物。不用黑貓（參考頻道是黑貓研究院）、不用貓頭鷹博士這種常見「知識動物」套路、不用柯南式偵探帽加放大鏡的組合。
- **辨識度**：縮成 64 px 的剪影也認得出來；一個招牌配件、一個招牌顏色。
- **好畫**：扁平插畫、粗描邊、身體比例 2–2.5 頭身，四肢簡單，避免手指特寫（AI 最容易畫錯）；需要拿東西時用整隻手掌或爪子握。
- **角色職責**：所長是「受理問題、蓋章結案」的人。不講話（全片只有旁白），表情與動作負責反應：驚訝、思考、恍然大悟。
- **招牌動作**：印章。片頭蓋「受理」，片尾蓋「原來如此」。印章上的字由合成時的卡片疊上去，不讓圖片模型寫字（`negative` 擋文字）。

## 系列畫風（三個方向共用）

`video.json` 的 `look`：

```json
{
  "preset": "custom",
  "style": "flat editorial illustration, bold clean outlines, limited palette of warm cream #F6EFE3, ink navy #1F2A44, stamp red #D8452F and mustard #E8B64C, soft paper grain, simple shapes, generous negative space, friendly and clear, 16:9 composition, no gradients heavier than two tones",
  "negative": "photorealistic, 3d render, cinematic lighting, text, letters, watermark, logo, brand marks, extra fingers, deformed hands, cluttered background, black cat",
  "candidates": 3
}
```

色盤取名：奶油紙底、墨藍、印章紅、芥末黃。印章紅只給「答案」與蓋章用，觀眾看到紅色就知道答案要來了。

## 方向 A：水豚所長（推薦）

慢條斯理、什麼都不驚訝的水豚，戴圓框眼鏡、穿芥末黃背心，手上一個紅色大印章。

- 為什麼：水豚在各語系都有好感、中日韓都紅，性格「淡定」跟「原來如此」的恍然大悟可以做反差（平常淡定，答案揭曉時眼睛放大）。體型圓、四肢短，好畫又不容易畫錯。
- 風險：水豚表情包很多，要靠眼鏡＋背心＋印章做出自己的樣子。

```text
appearance: An original mascot: a round, calm capybara standing upright, 2.2 heads tall, warm brown fur with a slightly lighter muzzle, small round ears, thin round wire-framed glasses, a mustard-yellow vest with one pocket, holding a large red rubber stamp with both paws. Short stubby limbs, no visible fingers. Calm half-closed eyes by default. Flat editorial illustration with bold navy outlines.
sheet_prompt: Character turnaround sheet of the capybara mascot on a plain cream background: front, three-quarter, side and back views, plus four expressions (calm, thinking with paw on chin, surprised with wide eyes, satisfied smile while stamping). Same proportions in every view.
```

## 方向 B：郵差鴿所長

帶著郵差包、把觀眾的問題一封一封收進事務所的灰鴿子，招牌是寫著問號的信封。

- 為什麼：「收到你的問題」和留言點題單元（路線圖第 2 季）直接接得上；飛行可以串場換景。
- 風險：鳥的翅膀拿東西不好畫；信封上的問號要合成時疊上。

```text
appearance: An original mascot: a plump grey pigeon with an iridescent teal-and-purple neck band, 2 heads tall, wearing a navy postal cap and a mustard-yellow messenger bag across the body, a red stamp tucked into the bag. Wings used like hands but without feathers splayed as fingers. Bright curious eyes. Flat editorial illustration with bold navy outlines.
sheet_prompt: Character turnaround sheet of the pigeon mascot on a plain cream background: front, three-quarter, side and back views, plus four expressions (curious head tilt, thinking, surprised with feathers puffed, satisfied while stamping). Same proportions in every view.
```

## 方向 C：燈泡機器人所長

頭是一顆燈泡的小機器人，想通時燈泡亮起來。

- 為什麼：「亮燈＝想通」一眼就懂，所有語系都不用翻譯；科技軸題目特別搭。
- 風險：燈泡頭是很常見的「點子」符號，辨識度要靠身體造型與配色；商業、旅遊題氣氛較冷。

```text
appearance: An original mascot: a small boxy robot, 2.5 heads tall, whose head is a rounded glass bulb with a simple filament face (two dot eyes, a line mouth), cream metal body with navy trim, a mustard-yellow scarf, and a red stamp built into its right arm like a tool. Mitten-like hands, no fingers. The bulb glows warm yellow when it understands something. Flat editorial illustration with bold navy outlines.
sheet_prompt: Character turnaround sheet of the bulb-head robot mascot on a plain cream background: front, three-quarter, side and back views, plus four expressions (bulb off and neutral, thinking with flickering bulb, surprised, bulb fully glowing while stamping). Same proportions in every view.
```

## 片頭 3 秒（每集相同，做一次重用）

| 時間 | 畫面 | 運鏡（`camera`） | 聲音 |
| --- | --- | --- | --- |
| 0.0–1.0 秒 | 事務所木門，門上毛玻璃（字由卡片疊上：原來如此事務所／各語系名稱） | `push-in` | 敲門兩聲 |
| 1.0–2.0 秒 | 門打開，所長坐在桌後抬頭，桌上一封寫著問號的信 | `drift` | 開門聲 |
| 2.0–3.0 秒 | 所長在信上蓋章，紅色「受理」印出（卡片疊字） | `push-in` | 蓋章「咚」 |

## 結尾蓋章（每集最後 3 秒）

所長在答案卡上蓋「原來如此」（該語系的口號，見 README），配同一個「咚」。這一格也是 Shorts 最後導回長片的畫面。

## 章節卡

每章一張：所長在白板前、手指（整隻手掌）指向章節標題，標題由 `chapter` 卡片疊字。三個方向都用同一個構圖。

## 選定紀錄

| 項目 | 值 |
| --- | --- |
| 方向 | （站主選 A／B／C） |
| 選定的設定圖 | （檔名與 SHA-256，圖檔留在 repo 外的 `VIDEO_WORKDIR`） |
| 核准日期 | |
