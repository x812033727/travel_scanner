# 《闖禍小浣熊》（`raccoon-mischief`）系列規則

這份是《闖禍小浣熊》的系列個別規則（2026-11-03 零台詞系列企劃盲評第 1 名，中位數 89 分、三位評審一致最想追看）。共用規則見 [`../README.md`](../README.md)、[`../WRITING.md`](../WRITING.md)、[`../REVIEW.md`](../REVIEW.md)。

---

## 一、系列定位與固定笑點公式

| 項目 | 設定 |
| --- | --- |
| **系列名稱** | 闖禍小浣熊（`raccoon-mischief`） |
| **預設標籤** | `["闖禍小浣熊", "浣熊", "無厘頭", "零台詞", "AI短劇"]` |
| **畫風與世界觀** | 寫實 AI，真實外觀的浣熊一家像人一樣雙足站立、穿毛衣與連帽衫過日子；世界裡沒有人類 |
| **固定場景** | 同一間溫暖的木質客廳，每集換一個角落（花瓶邊桌、客廳吊燈、電視櫃、掛鐘牆面、陽台盆栽區） |
| **五拍公式** | **① 闖禍弄壞家裡某樣東西（0.8–2.5s，配 `shatter`/`crunch`）** → **② 門外鑰匙聲、呆臉轉頭（固定壓在 `0.6–0.8s`，配 `keys`）** → **③ 跳過偽裝過程，硬切看到豆豆本人已假扮成那樣東西、地毯鼓起一包（2.2–3.0s）** → **④ 媽媽或爸爸面不改色地「把他當那樣東西用」（1.5–2.2s）** → **⑤ 結尾補刀：另一個家人也在偽裝，或豆豆被用到隔天／發芽（2.4–3.0s，配 `sting`＋`hold: 0.6–0.9s`）** |
| **系列招牌道具** | **媽媽的「青蔥」**（幾乎每集都會出現：插在花瓶裡、種在盆栽裡、電視購物台）、**地毯下鼓起的一包**（藏著被弄壞的碎片） |

---

## 二、角色與英文定妝錨點（`intros` 一字不差照抄）

每集 JSON spec 的 `base` 固定指向 `"raccoon-mischief-e01"`；若該集爸爸沒有出場，程式自動從 `intros` 移除 `baba`（避免模型多畫一隻浣熊）：

| 角色代號 | 中文設定 | 英文 `intros` 固定字串 |
| --- | --- | --- |
| **`doudou`** | **豆豆（小浣熊）**：年輕小浣熊，穿亮黃色連帽衫、背後披一條紅浴巾當披風 | `"the photo of Doudou, a real young raccoon in a bright yellow hoodie with a red towel cape: keep his face, fur, hoodie and cape, change the pose and place as described"` |
| **`mama`** | **浣熊媽媽**：成年浣熊，穿綠色針織毛衣、戴珍珠項鍊，常拿一袋青蔥 | `"the photo of Mama raccoon, a real adult raccoon in a green knitted sweater with a pearl necklace: keep her face, fur, sweater and necklace, change the pose and place as described"` |
| **`baba`** | **浣熊爸爸**：成年浣熊，圓肚子、白襯衫外穿藍色針織背心、戴小老花眼鏡 | `"the photo of Papa raccoon, a real adult raccoon with a round belly in a blue knitted vest over a white shirt with small reading glasses: keep his face, fur, vest, shirt and glasses, change the pose and place as described"` |

---

## 三、本系列專屬的 AI 避險與實戰教訓

1. **鑰匙聲反應鏡（`s02-key`）一律砍到 `0.6–0.8 秒`**：
   - 第一版每集 `s02-key` 都剪了 2.0–2.5 秒，兩位笑點審片人同時指出「呆臉停太久、節奏掉拍」。在 `recut.py` 統一縮到 **0.6–0.8 秒** 後，緊接第 3 拍偽裝揭曉，笑點立刻跳出來。
2. **偽裝造型必寫靜態結果，且絕不提原物件名**：
   - 第一版 `e01` 寫「豆豆把自己偽裝成花瓶」，模型畫成他抱著一塊布；`redo4.py` 補畫 `s03b-vase` 時直接寫 **`Doudou the raccoon himself is sitting inside a large blue ceramic vase, only his head and green onions poking out of the top`**，一次就畫出爆笑畫面。
   - `e04` 掛鐘鏡不要寫「原本掛時鐘的牆上」（會畫出真時鐘），直接寫 **`Doudou himself is pressed flat against the wall, his red towel cape spread into a round circle behind him, one arm pointing up and one arm pointing right`**。
3. **同機位多姿勢（如 `e03` 電視換台）必須共用同一張首格底圖**：
   - `s03`、`s05`、`s06`、`s07` 四鏡都是豆豆坐在空電視框裡換姿勢（跳舞 → 新聞主播 → 抱青蔥 → 關機躺平），必須從 `s03` 首格用 Qwen Image Edit 只改框內姿勢，電視外框與地毯鼓包才不會跳動。
4. **媽媽看手錶（`e04`）避免拍手腕**：
   - 浣熊戴手錶的特寫極易畫出人類手腕與五指；實戰解法是**裁切只留媽媽的臉部上半段**（`push: [1.7, 1.85], anchor: [0.5, 0.0]`），演出「先低頭看下方手腕、再抬眼看牆上起疑」配 `tick` 滴答聲，既避開人手又清楚傳達意思。

---

## 四、已完成集數（EP1–EP5）定版剪接表與品管紀錄

五集皆已通過第 1 關自動檢查與第 2 關雙人笑點審核（`QA-2026-11-04.md`，好笑度 `3–4/5`），完整製作檔備份於雲端硬碟 `AI/備份/Shorts/闖禍小浣熊/`：

| 集數 | 題目 | 定版鏡數與總長 | 定版剪接結構（`recut.py`） | 笑點審核分數（A／B） |
| --- | --- | --- | --- | --- |
| **e01** | 〈花瓶〉 | 5 鏡 / 9.9s | `s01-crash` 撞碎花瓶 (`0.8s, shatter`) → `s02-key` 鑰匙聲 (`0.8s, keys`) → `s03b-vase` 豆豆整隻蹲在藍色大花瓶裡咬青蔥 (2.6s) → `s05-mama` 媽媽進門 (2.4s) → `s04-lamp` 旁邊爸爸頭頂檯燈罩假扮檯燈、被按開關 (`2.6s, sting, click, hold: 0.7`) | **3／4**（補畫 s03b 花瓶造型與加開關聲後過關） |
| **e02** | 〈吊燈〉 | 8 鏡 / 12.7s | `s01-crop` 盪壞吊燈 (`1.2s, shatter`) → `s02-key` (`0.6s, keys`) → `s03-chandelier` 豆豆掛天花板拿手電筒當吊燈 (3.0s) → `s05-on` 媽媽開燈 (2.2s) → `s06-read` 媽媽在底下看書 (1.2s) → 快切開關與翻頁 (`0.6s + 0.9s`) → `s07-dawn` 撐到天亮黑眼圈 (`3.0s, sting`) | **3／3**（補切開關翻頁節奏後過關） |
| **e03** | 〈電視〉 | 7 鏡 / 14.9s | `s01-kick` 踢球砸裂電視 (2.0s) → `s02-key` (`0.7s, keys`) → `s03-frame` 坐進空電視框 (2.8s) → `s04-remote` 爸爸按遙控器前停頓 (`1.8s, beep, hold: 0.8, music_off`) → `s05-anchor` 變新聞主播 (1.8s) → `s06-onions` 變青蔥節目 (`2.0s, beep`) → `s07-off` 關機躺平 (`3.0s, tvoff, sting`) | **4／4**（過關） |
| **e04** | 〈掛鐘〉 | 6 鏡 / 13.8s | `s01-swing` 盪壞大掛鐘 (`2.8s, shatter, boing`) → `s02-key` (`0.6s, keys`) → `s03-hands` 貼牆披風攤圓用雙臂當指針 (`2.2s, tick, hold: 0.7`) → `s04-watch` 媽媽低頭看錶抬眼起疑 (`2.0s, push: 1.85`) → `s05-spin` 手臂狂轉 (`2.2s, ratchet`) → `s06-cuckoo` 咕咕鐘門彈出爸爸頭 (`2.4s, cuckoo, sting, hold: 0.9`) | **4／3**（裁切 s04 媽媽臉部放回看錶拍後過關） |
| **e05** | 〈龜背芋〉 | 6 鏡 / 12.6s | `s01-pot` 撞倒大盆栽 (`2.8s, crunch`) → `s02-key` (`0.6s, keys`) → `s03-plant` 站進花盆舉兩片大葉子當植物 (3.0s) → `s04-can` 媽媽拿水壺澆水 (`0.8s, pour`) → `s05-wet` 淋成落湯雞 (1.8s) → `s06-sprout` 頭頂「啵」一聲冒出青蔥 (`3.0s, poof, sting, hold: 0.6`) | **4／3**（過關） |

---

## 五、待拍集數儲備（EP6–EP8）

1. **EP6〈聖誕樹〉（12 月季節限定，已改稿儲備，約 13 秒）**：
   - `s01-tree` (1.0s)：豆豆撲倒客廳角落的聖誕樹（`crunch`）。
   - `s02-key` (0.7s)：門外鑰匙聲（`keys`）。
   - `s03-wrap` (2.6s)：**跳過過程**——豆豆本人站在花盆裡，全身纏滿還沒亮的彩色小燈泡串、頭頂戴著一顆大金星，雙臂張開假扮聖誕樹；腳邊地毯鼓起一大包。
   - `s04-plug` (1.5s, `hold: 0.4, music_off`)：媽媽彎腰把地上的插頭插進牆壁插座（`click`）。
   - `s05-glow` (2.8s, `hold: 0.8`)：豆豆身上的燈完全沒亮，反而是他腳邊**地毯底下那一包**亮起五顏六色的光芒並傳出聖誕音樂盒聲（`musicbox, sting`），豆豆低頭看著發光的地毯定格。
2. **EP7〈衣帽架〉（季終反轉：這次闖禍的是媽媽，約 13 秒）**：
   - `s01-snap` (1.0s)：浣熊媽媽把重重的購物袋掛上玄關木頭衣帽架，衣帽架當場斷成兩截（`crunch`）。
   - `s02-key` (0.7s)：門外傳來爸爸跟豆豆回家的鑰匙聲，媽媽耳朵貼平（`keys`）。
   - `s03-stand` (2.4s)：**跳過過程**——媽媽本人筆直站在玄關角落，戴著一頂大草帽遮住臉，雙臂舉成 Y 字形假扮衣帽架。
   - `s04-hang` (2.2s)：豆豆走過，順手把自己的紅浴巾披風甩在媽媽左臂上；爸爸走過，把老花眼鏡與藍背心掛在媽媽右臂與鼻頭上。
   - `s05-onions` (2.5s, `hold: 0.8, music_off`)：媽媽的手臂微微發抖，豆豆又回頭把一袋沉甸甸的青蔥掛在她頭頂草帽上（`thud, sting`），媽媽翻白眼定格。
3. **EP8〈掃地機器人〉（新規劃，約 10.5 秒）**：
   - 見 [`../WRITING.md`](../WRITING.md) 範例：踩壞圓形掃地機器人 → 鑰匙聲 (`0.7s`) → 豆豆本人趴在地板背頂大白圓蓋用四隻短爪貼地滑行撞牆轉 90 度 (`2.8s, hum, thud`) → 媽媽順手把濕藍抹布與一袋青蔥壓在圓蓋上繼續擦地 (`2.6s, poof, sting, hold: 0.8, music_off`)。
