# 歷史與奇異：畫面規格與畫風樣張

2026-10-10 起草。畫面參考 cheap（`@cheapaoe`）的可愛卡通，站主要求「內容相關的可愛插畫」、「跟原來如此系列比較像」，全部由 **MiniMax `image-01`** 生成，不再由 Claude 或 Codex 手繪 SVG。這份寫 MiniMax 的限制、系列的 `look`、每張 prompt 的寫法、照片怎麼貼、片頭片尾，與 2026-10-10 畫的四種候選畫風樣張。

## MiniMax `image-01` 的事實（決定畫風怎麼寫）

2026-10-04 AI 名詞那條線實測、2026-10-06 投影片改相容（[`../ILLUSTRATED.md`](../ILLUSTRATED.md) §樣張只畫給吃得下的模型）、2026-10-10 畫樣張再確認：

| 事實 | 對畫風的影響 |
| --- | --- |
| 不吃畫風樣張（`style` 參考圖只有 Gemini 會收），只收一張 `character` 參考圖而且不保證同一張臉 | 一整支影片的一致性全靠 `look.style` 的文字；每張 prompt 不再重寫風格，風格句子只寫在 `look` 裡 |
| `look.negative` 會被接成「Avoid: …」放進正向提示詞 | 系列的 `negative` 留空（`""`）；不想要的東西用正向寫法避開（要「沒有字」就寫「a blank wooden sign」，不寫「no text」） |
| 提示詞含畫風上限 1,500 字（`tools/video/media/prompt-budget.mjs`） | `look.style` 約 300–400 字，prompt 留 1,000 字以內；`keyframes --dry-run` 會印「prompt budget」 |
| 只出 1K（1280×720），沒有 2K | 運鏡的放大幅度照插圖投影片預設即可（6 秒最多放大到 1.25 倍不會糊） |
| 每張 US$0.0035；審圖（Gemini judge）每次 US$0.01、每張含審圖約 30 秒 | 審圖是主要花費；每月上限是張數（後台漫劇分頁的預算上限） |
| 多人互動聽不懂；水彩、水粉在近景會跑成照片質感；全彩細描與版畫穩 | 一張圖一個主體一個動作；畫風寫「cartoon／flat colours／cel shading」這類穩的字 |
| 審圖是文字版（judge 只拿 `look` 的描述比對） | `look.style` 要把「可愛卡通」寫成 judge 能核對的具體特徵（大頭、粗線、平塗），不寫抽象的形容詞 |

## 系列畫風：可愛卡通（候選 A–D）

共同特徵（cheap 的畫面，2026-10-10 看〈韓戰的歷史〉的畫格）：大頭大眼、表情誇張、粗而乾淨的描邊、飽和的平塗加柔和的 cel 陰影、背景簡單、一個主體放在畫面中間三分之一。四種候選只差在「多可愛」與「色盤」：

| 候選 | `look.style` | 適合 |
| --- | --- | --- |
| **A 大頭卡通**（最像 cheap） | cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, bright saturated flat colours with soft cel shading, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9 | 兩個系列共用的家族畫風 |
| **B 軟繪本** | cute soft storybook cartoon: rounded simplified characters with small dot eyes and rosy cheeks, thin warm-brown outlines, pastel flat colours, gentle paper texture, cozy and friendly, uncluttered scene, one subject in the centre third, 16:9 | 原來如此事務所（溫和、生活科學） |
| **C 懸疑色盤**（這個系列自己的） | cute cartoon with a mystery mood: chibi characters with big heads and expressive eyes, thick dark outlines, flat colours limited to deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, one dramatic light source, one subject in the centre third, 16:9 | 歷史與奇異：夜空藍＋牛皮紙黃＋褪色青＋警示紅，紅只給「檔案章」 |
| **第 3 版（選定，2026-10-10）** | cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, flat colours with soft cel shading, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9 | 歷史與奇異：A 的媒材句＋C 的色盤句 |
| **D 動物代人** | cute cartoon with anthropomorphic animal characters standing in for people (bears, cats, raccoons, rabbits) wearing period costume, big heads, large expressive eyes, thick clean outlines, bright flat colours with soft cel shading, simple backgrounds, one subject in the centre third, 16:9 | 不想畫真實人物時的替身；cheap 的縮圖做法 |

`video.json` 的寫法（以 C 為例）：

```json
{
  "look": {
    "preset": "custom",
    "style": "cute cartoon with a mystery mood: …（上表）",
    "negative": "",
    "motion": "slow push in or gentle drift, no cuts",
    "candidates": 3
  }
}
```

站主選定後，把它加成 `tools/video/core/drama.mjs` 的具名預設（例如 `cute-mystery`，票 `2026-10-10-explainer-route-takes-a-series-look`），之後 `look.preset` 寫名字就好；原來如此事務所選 A 或 B（票 `2026-10-10-sothatswhy-minimax-images`）。

## 樣張（2026-10-10，MiniMax image-01，每種 4 張、1 次嘗試）

四個場景跨四種題材與光線：羅斯威爾的牧場（白天戶外、一個人撿東西）、無人的帆船（海上黃昏）、燭光下寫詩的老學者（室內夜、歷史人物）、雪地裡割開的帳篷（夜景、沒有人）。樣張與對照表在 repo 外 `mokaair-work/videos/_audition/look-20261010-curio/`（`<look>/<shot>.png`、`contact.jpg`），花費約 US$0.22（16 張圖加 16 次審圖）。

| 候選 | 看到的事 | judge（九題是非題，門檻 7） |
| --- | --- | --- |
| **A 大頭卡通** | 最像 cheap：大頭大眼、粗而乾淨的描邊、亮色 cel 陰影，四張風格一致（牧場的白天、海上黃昏、燭光室內、雪夜都還是同一支筆）；牧場主人被畫成小孩版、羊很可愛；學者那張接近吉卜力式賽璐珞；筆記本上有假字跡（judge 沒扣） | 4／4 過，各 9.29 |
| **B 軟繪本** | 柔和、偏水彩繪本，人物小而完整、腮紅點眼；比 A 安靜，少了 cheap 的誇張表情；四張一致 | 4／4 過，各 9.29 |
| **C 懸疑色盤（第 1 版）** | 寫了 mystery mood／dramatic light source，模型漂了：牧場那張變成**寫實照片**、學者變成 **3D CGI** 加黑邊；帆船與帳篷兩張是對的（夜空藍＋牛皮紙黃很有檔案感） | 2／4 過（牧場 9.71 但 style 不過、學者 7.29 不過） |
| **C 第 2 版** | style 開頭改成「2D flat cartoon illustration with thick dark ink outlines and visible paper grain, hand-drawn cel animation look」再接色盤：四張都回到 2D、夜空藍＋牛皮紙黃的色盤一致、很有檔案感；但人物變成寫實比例、帆船偏油畫，**不夠可愛**；帳篷旁又多了一個小人（judge 抓到） | 1／4 過（分數 9–9.71，不過的都是「不夠 chibi」「多了人」） |
| **第 3 版（A 的整句＋C 的色盤句）** | 站主選定後畫的確認樣張（`c3-curio/`）：可愛度回到 A、色盤是 C 的夜空藍＋牛皮紙黃＋褪色青，四張同一支筆；帳篷那張寫了 plain canvas tent 與 nobody，帳篷口仍有一個小小的臉狀物，之後空景要再加一句「the only shapes are the tent, snow and trees」 | 4／4 過，各 9.29 |
| **D 動物代人** | 熊牧場主人加三隻小動物很討喜，但「動物代人」會讓模型**到處加角色**：帳篷那張 prompt 沒有人，畫出一家動物站在帳篷前；帆船變 3D 又多了甲板上的人；學者變 3D | 2／4 過 |

量到的三件事：

1. **畫風文字的第一句決定媒材**：開頭寫「cute … cartoon」四張全是 2D；開頭寫情緒（mystery mood）或光（dramatic light source）就往寫實與 3D 漂。系列的 `look.style` 一律先寫媒材與線條，再寫色盤，不寫 cinematic／dramatic／moody 這類詞。
2. **沒有人物的場景會把表情貼到物件上**：A、B 的帳篷都長了一張臉。空景的 prompt 要寫 `a plain canvas tent`、`an empty deck with nobody on it`，把「沒有人」寫成正向描述（MiniMax 沒有 negative）。
3. **每張都被裁掉 4–8% 的紙邊**（`media/trim.mjs` 自動處理），運鏡不受影響；MiniMax 偶爾回 HTTP 502，重跑 `keyframes` 會接著畫沒畫的 shot。九題是非題之下分數不再頂在 7（多數 9.29），judge 抓到的都是真的漂（寫實、3D、黑邊、多出來的人）。

建議：歷史與奇異用 **A 的整句（chibi、big round heads、thick clean dark outlines、cel shading）＋C 的色盤句**，也就是第 3 版，在試片票裡先畫 4 張確認；原來如此用 **A**（或站主偏好溫和一點就 B）。C 第 2 版證明色盤句本身不會漂，漂的是「mystery mood／dramatic light」；可愛要靠 A 的那幾個詞。

## 每張 prompt 怎麼寫

跟插圖投影片一樣（[`../ILLUSTRATED.md`](../ILLUSTRATED.md) §畫面不像 AI）：景別 → 地點與時間 → 一個人（或一個物件）做一件事 → 視線落點的物件與材質 → 光從哪來。另外這個系列：

- **一個主體一個動作**（MiniMax）：「一個牧場主人蹲下撿起一片反光的碎片」可以，「三個軍官圍著碎片爭論」不行——拆成三張。
- **不寫風格、不寫色盤**：風格在 `look`；prompt 裡出現 cartoon／chibi／navy 這類字，lint 會警告「抄 look」。
- **文字一律不畫**：報紙、文件、路牌寫成 `a blank newspaper front page`、`a plain manila folder`；字由卡片疊上。
- **真實人物**：過世超過 70 年的用描述不用名字（「a bearded sixteenth-century scholar in a dark robe」），畫成卡通；在世或近代人物不畫，用照片或剪影（[`README.md`](README.md) §內容守則）。
- **表情是主角**：每章至少一張人物表情特寫（驚訝、害怕、得意），cheap 的畫面一半靠表情。
- **一整天的光**：夜景與燭光最多一半（lint 會警告）；懸疑題材容易全部寫成夜晚，白天的場景要刻意安排。
- **連續三張不同運鏡**（lint 錯誤）；shot 的句子不 `reveal`。
- **景別輪替**：遠景（地點）→ 中景（人做事）→ 特寫（物件或表情），一章至少各一張。

## 照片：貼圖式照片卡

馬臉姐的做法是主持人旁邊「彈出」一張去背的照片或截圖。我們沒有主持人，照片卡的規格：

| 項目 | 規格 |
| --- | --- |
| 版面 | 照片像一張印出來的相片：白邊 24px、微傾（`data.tilt` −3°～+3°；沒寫時依場景 id 固定取 ±1.5°、±2° 或 ±2.5°，同一景永遠同一個角度，一支片裡左右都有）、柔和投影；相片連白邊佔畫面高度 70%（756px），有 `caption` 時讓出一行、約 65%（700px）；水平置中（Short 從 16:9 裁中間，置中才留得住），直向與方形照片照高度放；`caption` 一行在相片下方（卡片字，不燒進照片，≤40 字）。底是影片主題的底色：系列自己的底色（C 的夜空藍）要等解說路線吃系列畫風的票 |
| 出處 | 相片右下角深色膠囊（`data.credit`，一行、≤60 字；直向相片比膠囊窄時，膠囊會像標籤一樣橫跨出相片左緣）：「Photo: 作者／機構（授權）」；完整出處在說明欄的「📷 圖片來源」區塊（`composeDescription` 自動長出） |
| 運鏡 | 緩慢 push in（相片上的細節）或 drift；一張照片停 4–8 秒 |
| 寫法 | `photo` 版型（2026-10-10 落地，票 `2026-10-10-photo-paste-card`）：`{ "template": "photo", "data": { "image": "stock/<sha256>.jpg" 或 repo 內的檔, "caption"?, "credit"?, "tilt"? } }`，沒有逐條出現（一景一個畫面）。要框出重點的截圖與文件原件仍用 `screenshot`（`data.highlight`）。本機路線可以直接寫；主機的自動撰稿還不會用（等解說路線的票） |
| 登記 | 每張進 `assets[]`：`path`、`source`（廠商或館方要的那句）、`license`、`author`、`url`；`render` 擋沒登記的照片（`photo` 卡的照片放在 repo 裡也要登記） |
| 來源 | 公有領域（維基共享資源標 PD 的、美國聯邦政府作品、NASA）、CC BY／BY-SA（標作者與授權）、Pexels／Pixabay（`stock search`／`stock fetch`）、自己截的官方頁（合理引用、標出處） |
| 不用 | 來源不明的網路圖、新聞媒體照片、在世人物的肖像用在負面情境、遺體與血腥、有版權的電影劇照與書封 |

一集 5–10 張照片，放在「流傳的版本」與「檔案裡有什麼」兩段：當年的報紙版面、文件原件、事件地點的現代照片。照片卡與插圖交錯，連續兩張照片之間至少隔一張插圖或一張卡片。

## 片頭 3 秒與結檔章（每集相同，做一次重用）

| 時間 | 畫面 | 運鏡 | 聲音 |
| --- | --- | --- | --- |
| 0.0–1.0 | 一排老式鐵檔案櫃，中間一格抽屜被拉開（畫面裡沒有人） | push in | 抽屜滑動聲 |
| 1.0–2.0 | 一份牛皮紙檔案夾被抽出來放在桌上，夾子上一個空白標籤（系列名由卡片疊上） | drift | 紙的摩擦聲 |
| 2.0–3.0 | 紅色印章落下蓋在檔案夾上（「開檔」由卡片疊上） | push in | 蓋章「咚」 |

結檔：答案卡（`big`，夜空藍底）被同一個紅章蓋「存檔」（有定論）或「未結」（沒定論）；這一格也是 Shorts 導回長片的畫面。章節卡：牛皮紙檔案夾的一頁，頁籤是褪色青、印著章節序號，標題由 `chapter` 卡片疊字。紅色只給印章，觀眾看到紅色就知道「檔案要結了」——跟原來如此事務所的「印章紅只給答案」同一套手法。

## 縮圖

`thumb` 版型（[`../README.md`](../README.md) §版型）：左 40% 標籤（主軸名：歷史懸案／奇異現象／預言／外星／都市傳說）＋ ≤6 字的大字 ＋ 一行小字；右 60% 一張插圖，優先放**角色的表情特寫**（cheap 的縮圖九成是大臉），其次是最有衝擊的物件；大字不重複標題前 10 字。B／C 變體：B 換成數字或年份（「1872」「72 秒」），C 換成兩件東西的對比。

## 選定紀錄

| 項目 | 值 |
| --- | --- |
| 畫風 | 第 3 版（A 的媒材句＋C 的色盤句；站主 2026-10-10「用你建議的」） |
| `look.style` 最終文字與 `look_hash` | |
| 片頭關鍵影格 1（檔案櫃） | （檔名與 SHA-256，圖檔留在 repo 外） |
| 片頭關鍵影格 2（檔案夾） | |
| 片頭關鍵影格 3（蓋章） | |
| 站主確認日期 | |
