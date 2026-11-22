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
5. **豆豆不戴眼鏡（2026-11-22 Flow 重製）**：同一個 Flow 專案只要附了爸爸的定妝照，豆豆就常被畫上眼鏡。生圖訊息開頭寫 `Doudou the young raccoon never wears glasses (only Papa wears glasses)`，首格逐張檢查。
6. **2026-11-22 重製版已用過的梗（下一批避開）**：
   - 「家長把扮植物的豆豆拿來澆水、噴水」用了兩次（e01 花瓶、e05 龜背芋），兩集發片不要相鄰。
   - 「張開雙臂的 T／Y 字偽裝」用了三次（e02 吊燈、e04 時鐘指針、e05 樹枝）。
   - 灰色膠帶出現在三集。
   - 同一集裡後面幾個偽裝鏡的首格，都要從第一張偽裝首格編輯出來（第 3 條）；這次電視、時鐘小屋、花瓶都有跳連戲。

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

## 五、EP06–EP50 擴充集數總表（共 45 集，全部過關可開拍）

全 45 集完整分鏡劇本見 [`../episodes/raccoon-mischief-ep06-50.md`](../episodes/raccoon-mischief-ep06-50.md)，獨立三評審盲評（多輪改稿收斂至 **45/45 通過**、中位數 **73–92**、平均 **83.0**）與 Stage 2 技術分鏡終審（**0 High / 0 Medium**）完整紀錄見 [`../reviews/raccoon-mischief-review.md`](../reviews/raccoon-mischief-review.md)。

- **S 級（≥ 85，首波優先開拍）**：20 集｜**A 級（78–84，主力排程）**：16 集｜**B 級（70–77，常規儲備）**：9 集

| 集數 | Slug | 題目 | 鏡數／總長 | 縮圖鏡 | 盲評中位數（三評審） | 優先級 | 狀態 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **EP06** | `raccoon-mischief-e06` | 〈聖誕樹〉 | 6 鏡 / 11.0s | `s03-wrap` | **89** (88/89/89) | S | 已過盲評＋技審 |
| **EP07** | `raccoon-mischief-e07` | 〈衣帽架〉 | 6 鏡 / 11.0s | `s06-onions` | **85** (88/85/84) | S | 已過盲評＋技審 |
| **EP08** | `raccoon-mischief-e08` | 〈掃地機器人〉 | 6 鏡 / 11.1s | `s03-slide` | **79** (82/79/79) | A | 已過盲評＋技審 |
| **EP09** | `raccoon-mischief-e09` | 〈電風扇〉 | 6 鏡 / 11.2s | `s03-fan` | **77** (84/77/76) | B | 已過盲評＋技審 |
| **EP10** | `raccoon-mischief-e10` | 〈招財貓〉 | 6 鏡 / 11.4s | `s03-beckon` | **92** (92/92/92) | S | 已過盲評＋技審 |
| **EP11** | `raccoon-mischief-e11` | 〈烤麵包機〉 | 7 鏡 / 11.7s | `s06-pop` | **91** (91/88/91) | S | 已過盲評＋技審 |
| **EP12** | `raccoon-mischief-e12` | 〈魚缸金魚〉 | 6 鏡 / 11.0s | `s03-bowl` | **83** (86/82/83) | A | 已過盲評＋技審 |
| **EP13** | `raccoon-mischief-e13` | 〈體重計〉 | 6 鏡 / 11.0s | `s06-flat` | **92** (86/92/93) | S | 已過盲評＋技審 |
| **EP14** | `raccoon-mischief-e14` | 〈微波爐〉 | 6 鏡 / 11.1s | `s03-spin` | **90** (92/90/76) | S | 已過盲評＋技審 |
| **EP15** | `raccoon-mischief-e15` | 〈穿衣鏡〉 | 6 鏡 / 11.2s | `s06-caught` | **87** (90/86/87) | S | 已過盲評＋技審 |
| **EP16** | `raccoon-mischief-e16` | 〈留聲機〉 | 6 鏡 / 11.3s | `s05-dj` | **77** (77/71/80) | B | 已過盲評＋技審 |
| **EP17** | `raccoon-mischief-e17` | 〈電暖爐〉 | 6 鏡 / 11.0s | `s06-blush` | **78** (72/79/78) | A | 已過盲評＋技審 |
| **EP18** | `raccoon-mischief-e18` | 〈客廳矮茶几〉 | 6 鏡 / 11.2s | `s06-juggle` | **77** (51/77/78) | B | 已過盲評＋技審 |
| **EP19** | `raccoon-mischief-e19` | 〈玄關迎賓踏墊〉 | 6 鏡 / 11.2s | `s06-lift` | **87** (82/87/92) | S | 已過盲評＋技審 |
| **EP20** | `raccoon-mischief-e20` | 〈書架書擋〉 | 6 鏡 / 11.0s | `s06-globe` | **78** (78/86/76) | A | 已過盲評＋技審 |
| **EP21** | `raccoon-mischief-e21` | 〈腳踏垃圾桶〉 | 6 鏡 / 11.1s | `s06-stuffed` | **85** (85/89/85) | S | 已過盲評＋技審 |
| **EP22** | `raccoon-mischief-e22` | 〈雨傘桶〉 | 6 鏡 / 11.1s | `s06-drag` | **85** (79/85/87) | S | 已過盲評＋技審 |
| **EP23** | `raccoon-mischief-e23` | 〈餐桌旋轉盤〉 | 6 鏡 / 11.0s | `s06-sushi` | **87** (87/92/82) | S | 已過盲評＋技審 |
| **EP24** | `raccoon-mischief-e24` | 〈衛生紙捲架〉 | 6 鏡 / 11.1s | `s06-red` | **88** (80/88/88) | S | 已過盲評＋技審 |
| **EP25** | `raccoon-mischief-e25` | 〈飲水機〉 | 6 鏡 / 11.0s | `s06-jet` | **74** (80/74/60) | B | 已過盲評＋技審 |
| **EP26** | `raccoon-mischief-e26` | 〈壁掛鹿頭裝飾〉 | 6 鏡 / 11.1s | `s03-antler` | **82** (73/82/84) | A | 已過盲評＋技審 |
| **EP27** | `raccoon-mischief-e27` | 〈吸塵器〉 | 6 鏡 / 11.2s | `s03-vac` | **76** (82/74/76) | B | 已過盲評＋技審 |
| **EP28** | `raccoon-mischief-e28` | 〈牆上名畫框〉 | 6 鏡 / 11.1s | `s03-paint` | **73** (67/73/79) | B | 已過盲評＋技審 |
| **EP29** | `raccoon-mischief-e29` | 〈沙發大抱枕〉 | 6 鏡 / 11.0s | `s06-blizzard` | **81** (68/88/81) | A | 已過盲評＋技審 |
| **EP30** | `raccoon-mischief-e30` | 〈廚房計時器〉 | 6 鏡 / 11.2s | `s03-tomato` | **90** (90/87/91) | S | 已過盲評＋技審 |
| **EP31** | `raccoon-mischief-e31` | 〈保險箱〉 | 6 鏡 / 11.2s | `s03-safe` | **92** (92/92/89) | S | 已過盲評＋技審 |
| **EP32** | `raccoon-mischief-e32` | 〈地球儀〉 | 6 鏡 / 11.0s | `s06-continents` | **85** (85/75/86) | S | 已過盲評＋技審 |
| **EP33** | `raccoon-mischief-e33` | 〈門擋〉 | 6 鏡 / 11.0s | `s06-popout` | **82** (68/82/86) | A | 已過盲評＋技審 |
| **EP34** | `raccoon-mischief-e34` | 〈吹風機架〉 | 6 鏡 / 11.2s | `s06-suck` | **91** (91/91/90) | S | 已過盲評＋技審 |
| **EP35** | `raccoon-mischief-e35` | 〈茶壺套組〉 | 6 鏡 / 11.0s | `s06-teabag` | **73** (76/73/57) | B | 已過盲評＋技審 |
| **EP36** | `raccoon-mischief-e36` | 〈抽油煙機〉 | 6 鏡 / 11.2s | `s03-hood` | **77** (77/74/86) | B | 已過盲評＋技審 |
| **EP37** | `raccoon-mischief-e37` | 〈加濕器〉 | 6 鏡 / 11.0s | `s06-wig` | **80** (80/80/89) | A | 已過盲評＋技審 |
| **EP38** | `raccoon-mischief-e38` | 〈跑步機〉 | 6 鏡 / 11.3s | `s05-cramp` | **78** (83/78/72) | A | 已過盲評＋技審 |
| **EP39** | `raccoon-mischief-e39` | 〈咖啡機〉 | 6 鏡 / 11.1s | `s06-foam` | **79** (86/79/76) | A | 已過盲評＋技審 |
| **EP40** | `raccoon-mischief-e40` | 〈電鍋〉 | 6 鏡 / 11.2s | `s05-reveal` | **90** (89/90/92) | S | 已過盲評＋技審 |
| **EP41** | `raccoon-mischief-e41` | 〈陽台曬衣夾架〉 | 7 鏡 / 11.4s | `s06-hang` | **73** (83/69/73) | B | 已過盲評＋技審 |
| **EP42** | `raccoon-mischief-e42` | 〈搖椅〉 | 6 鏡 / 11.2s | `s06-mama` | **84** (82/86/84) | A | 已過盲評＋技審 |
| **EP43** | `raccoon-mischief-e43` | 〈玄關鞋櫃〉 | 6 鏡 / 11.2s | `s06-catapult` | **78** (60/78/85) | A | 已過盲評＋技審 |
| **EP44** | `raccoon-mischief-e44` | 〈存錢筒〉 | 6 鏡 / 11.1s | `s03-piggy` | **79** (79/76/82) | A | 已過盲評＋技審 |
| **EP45** | `raccoon-mischief-e45` | 〈客廳大窗簾〉 | 6 鏡 / 11.1s | `s06-silhouette` | **82** (77/82/92) | A | 已過盲評＋技審 |
| **EP46** | `raccoon-mischief-e46` | 〈重低音喇叭〉 | 6 鏡 / 11.2s | `s05-thump` | **81** (81/90/71) | A | 已過盲評＋技審 |
| **EP47** | `raccoon-mischief-e47` | 〈餐桌水果籃〉 | 6 鏡 / 11.2s | `s06-peace` | **85** (85/86/82) | S | 已過盲評＋技審 |
| **EP48** | `raccoon-mischief-e48` | 〈廚房切菜砧板〉 | 6 鏡 / 11.1s | `s05-sweat` | **89** (93/84/89) | S | 已過盲評＋技審 |
| **EP49** | `raccoon-mischief-e49` | 〈日曆撕頁掛架〉 | 6 鏡 / 11.1s | `s06-circle` | **91** (93/84/91) | S | 已過盲評＋技審 |
| **EP50** | `raccoon-mischief-e50` | 〈客廳大沙發〉 | 6 鏡 / 11.4s | `s05-baba` | **84** (84/92/79) | A | 已過盲評＋技審 |
---

## 六、2026-11-22 Google Flow 重製版（取代第四節的 H3 版）

照新規則重寫、盲評、分鏡審、用 Google Flow 重拍（流程見 [`../PRODUCTION-ROUTES.md`](../PRODUCTION-ROUTES.md) 第 8 項，教訓見 [`../../lessons/shorts.md`](../../lessons/shorts.md) 2026-11-22）。製作檔備份在雲端硬碟 `AI/備份/Shorts/<系列>/`，網站上的五集等站主核准。

- 成片審核：審片人 A 一輪、B 兩輪，五集都可上架
- 排程提醒：e01 與 e05 結構相近，排程時不要相鄰

| 集 | 片長 | 盲評中位數 | 標題 |
|---|---|---|---|
| e01 | 10.9s | 78 | 打破花瓶的下一秒，媽媽就開門進來了 #闖禍小浣熊 |
| e02 | 9.2s | 73（刪 s02 後） | 我把吊燈踢下來了，媽媽就在客廳看書 #闖禍小浣熊 |
| e03 | 10.5s | 86 | 一腳把電視踢破，爸爸剛好要來看電視 #闖禍小浣熊 |
| e04 | 9.7s | 76 | 掛鐘被我弄掉了，媽媽正盯著牆上等水滾 #闖禍小浣熊 |
| e05 | 9.5s | 74 | 我把龜背芋啃光的時候，爸爸就在旁邊打瞌睡 #闖禍小浣熊 |
