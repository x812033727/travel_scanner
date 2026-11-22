# 《網美小豬》（`influencer-piglet`）系列規則

這份是《網美小豬》的系列個別規則（2026-11-03 第二批零台詞系列企劃盲評第 2 名，中位數 84 分）。共用規則見 [`../README.md`](../README.md)、[`../WRITING.md`](../WRITING.md)、[`../REVIEW.md`](../REVIEW.md)。

---

## 一、系列定位與固定笑點公式

| 項目 | 設定 |
| --- | --- |
| **系列名稱** | 網美小豬（`influencer-piglet`） |
| **預設標籤** | `["網美小豬", "網美", "水豚", "小豬", "零台詞", "AI短劇"]` |
| **畫風與世界觀** | 寫實 AI，真實外觀的粉紅小豬與水豚像人一樣雙足站立、穿衣服；世界裡完全沒有人類 |
| **五拍公式** | **① 唯美網美照特寫（固定壓在 `1.2s`，`0.9s` 打快門聲 `shutter`，可直接用首格靜圖 `-still`）** → **② 拉遠揭曉超陽春假景（`1.8–3.0s`，`0.0s` 打黑膠刮擦聲 `recordscratch`＋道具運轉聲）** → **③ 水豚男友在畫面外當苦力製造特效（`1.6–2.4s`，面無表情）** → **④ 成品照／蓄力拍（`1.0–2.4s`，成品照角落露出水豚的臉，或水豚憋氣蓄力 `music_off`）** → **⑤ 假景崩塌或男友失誤補刀（`1.6–3.6s`，配 `hold: 0.6–0.8s` 或 `lights_out`）** |
| **同框鐵律** | **小豬粉粉與水豚男友在現實鏡頭裡永遠不同框！**（成品照片裡不小心拍到水豚的頭／鼻子是唯一例外，屬於照片裡的笑點破綻） |

---

## 二、角色與英文定妝錨點（`intros` 一字不差照抄）

每集 JSON spec 的 `base` 固定指向 `"influencer-piglet-e01"`：

| 角色代號 | 中文設定 | 英文 `intros` 固定字串 |
| --- | --- | --- |
| **`fenfen`** | **粉粉（粉紅小豬網美）**：真實粉紅小豬，穿白蕾絲洋裝、戴大草帽配粉紅緞帶與珍珠髮夾 | `"the photo of Fenfen, a real pink pig standing upright: keep her face and skin, change the pose and place as described"`（每鏡 `ff` 補上招牌穿搭：`in her white lace dress and wide straw hat with a pink ribbon and pearl hairpin`） |
| **`capy`** | **水豚男友（工具人攝影師）**：真實水豚，戴綠漁夫帽、穿灰 T 恤、脖子掛無品牌行動電源，永遠面無表情 | `"the photo of the capybara boyfriend, a real capybara in a green bucket hat and grey T-shirt: keep his face, fur, hat and shirt, change the pose and place as described"` |

---

## 三、本系列專屬的 AI 避險與實戰教訓

1. **第 1 鏡唯美照一律固定 `1.2 秒`，拿掉多餘的「快門閃光鏡」**：
   - 第一版每集開頭放了 3 秒唯美照＋1.6 秒快門閃光鏡（共 4.6 秒什麼事都沒發生），兩位笑點審片人都指出開頭太拖。
   - **定版規則**：第 1 鏡固定剪 **`1.2 秒`**（甚至直接用首格靜圖 `s01-still`，在 `0.9s` 配一聲 `shutter`），原本的 `s02` 閃光鏡整鏡刪除，第 `1.2 秒` 直接進 `s03` 拉遠揭曉假景配 `recordscratch`！
2. **嚴禁寫「像雜誌封面（like a magazine cover）」**：
   - 第一版在成品照鏡頭寫了 `like a magazine cover`，模型自動在畫面上下方印出假的英文刊名、條碼與浮水印。
   - **定版規則**：成品照一律寫 **`a vertical framed photo print with a clean white border, no text, no letters, no logos`（2026-11-22 改：`preflight.mjs` 連否定句裡的 watermark 也判錯，改寫 no logos）**。
3. **爆發笑點前必加 `1.0 秒` 蓄力拍（`inhale`＋`music_off`）**：
   - 在 `e02`（雪國刨冰機）中，第一版水豚男友直接打噴嚏把刨冰噴到小豬身上，審片人判「噴嚏沒交代清楚、太突然」。
   - **解法**：在成品照與噴嚏之間，插入 **`1.0 秒` `s05b-inhale`（水豚眉毛結霜、仰頭閉眼深吸一口氣，配 `inhale` 音效＋`music_off: True`）**，再接噴嚏爆開，笑點分數直接從不過跳到 `4／4`！
4. **水豚大動作（如打噴嚏、抱水塔）只取臉還沒變形的前段**：
   - H3 在水豚張大嘴打噴嚏的後半段容易把水豚臉變形成狗或熊；剪接時只取前 `2.5–3.0 秒` 臉型還完全是水豚的那一段，後面用 `"hold": 0.8` 定格。

---

## 四、已完成集數（EP1–EP5）定版剪接表與品管紀錄

五集皆已通過第 1 關自動檢查與第 2 關雙人笑點審核（`QA-2026-11-04.md`，好笑度幾乎全拿滿分 `4／4`），完整製作檔備份於雲端硬碟 `AI/備份/Shorts/網美小豬/`：

| 集數 | 題目 | 定版鏡數與總長 | 定版剪接結構（`recut.py`） | 笑點審核分數（A／B） |
| --- | --- | --- | --- | --- |
| **e01** | 〈夕陽海邊〉 | 6 鏡 / 13.4s | `s01-sunset` 唯美夕陽海邊 (`1.2s, shutter`) → `s03-pullback` 拉遠揭曉大海是藍色防水布 (`3.0s, recordscratch`) → `s04-boyfriend` 水豚男友舉著紅色保溫燈當夕陽 (1.6s) → `s05-photo` 成品照 (2.4s) → `s06-again` 燈泡裂開 (`2.2s, crack`) → `s07-sun` 夕陽裡印著水豚大臉 (3.0s) | **4／4**（砍掉閃光鏡、縮短開頭後過關） |
| **e02** | 〈雪國〉 | 6 鏡 / 13.6s | `s01-snow` 唯美雪景 (`1.2s, shutter`) → `s03-rooftop` 拉遠揭曉頂樓刨冰機配電風扇 (`3.0s, recordscratch, blender`) → `s04-boyfriend` 水豚搖刨冰機凍到結霜 (2.2s) → `s05-still` 成品照 (`2.4s, shutter`) → `s05b-inhale` 水豚仰頭憋噴嚏吸氣 (`1.0s, inhale, music_off`) → `s06-sneeze` 噴嚏把小豬埋成雪人 (`3.0s, sneeze, hold: 0.8`) | **4／4**（補畫 s05b 憋噴嚏蓄力鏡後過關） |
| **e03** | 〈仙境瀑布〉 | 4 鏡 / 10.6s | `s01-falls-still` 唯美瀑布首格 (`1.2s, shutter`) → `s03-roof` 拉遠揭曉頂樓破水塔漏水 (`3.0s, recordscratch, pour`) → `s04-boyfriend` 水豚用圓肚子堵住水塔另外兩個破洞 (`2.4s, splash`) → `s05-crop` 成品照慢推到瀑布頂端冒出的水豚頭 (`3.4s, shutter, gurgle, push: 1.8, hold: 0.6`) | **4／4**（重畫水豚堵水塔＋改以成品照慢推水豚頭收尾後過關） |
| **e04** | 〈櫻花雨〉 | 5 鏡 / 13.2s | `s01-sakura` 唯美櫻花雨 (`1.2s, shutter`) → `s03-lot` 拉遠揭曉空停車場與吹葉機 (`3.0s, recordscratch, blower`) → `s04-boyfriend` 水豚扛吹葉機吹粉紅紙片 (2.2s) → `s05-photo-v2` 成品照 (2.4s) → `s06-dump` 整袋紙花倒頭蓋臉把小豬埋住 (`3.6s, whoosh, thud, poof, hold: 0.8`) | **4／4**（過關） |
| **e05** | 〈螢火蟲〉 | 7 鏡 / 11.0s | `s01-fireflies` 唯美森林螢火蟲 (`1.2s, shutter`) → `s03-garage` 拉遠揭曉車庫釣竿吊綠燈串 (`1.8s, recordscratch, hum`) → `s04-boyfriend` 水豚胸掛行動電源晃釣竿 (2.2s) → `s05-photo` 成品照 (1.8s) → `s06-tangle` 燈串纏住 (1.5s) → 回切 `s04` 推近行動電源沒電 (`0.9s, powerdown, push: 2.2, box`) → `s06` 分三段熄燈全黑 (`1.6s, click, lights_out, music_off`) | **4／3**（加 box 暗屏與三段熄燈後過關） |

---

## 五、待拍集數儲備（EP6–EP8）

1. **EP6〈頭等艙出國〉（新規劃，約 12 秒）**：
   - `s01-plane-still` (1.2s, `shutter`)：粉粉坐在看似飛機橢圓窗邊，窗外是潔白雲海，優雅地托腮。
   - `s02-laundry` (2.8s, `recordscratch, hum`)：拉遠揭曉——「飛機窗」其實是陽台滾筒洗衣機打開的圓玻璃門框，粉粉坐在小板凳上貼著門框背面。
   - `s03-boyfriend` (2.2s, `hum`)：洗衣機另一側，水豚男友正把一大團白色枕頭棉花塞在玻璃門前慢慢轉動當雲海。
   - `s04-photo` (3.2s, `shutter, pop, push: [1.0, 1.8], hold: 0.8, music_off`)：成品照看起來像頭等艙窗景，但鏡頭慢推到窗外潔白雲海中央——印著水豚男友貼在洗衣機玻璃上被壓扁的大鼻子與兩顆呆眼睛，定格。
2. **EP7〈無邊際泳池〉（新規劃，約 11.5 秒）**：
   - `s01-pool-still` (1.2s, `shutter`)：粉粉戴太陽眼鏡趴在蔚藍波光的水池邊，面前漂著一盤熱帶水果。
   - `s02-basin` (2.8s, `recordscratch, pour`)：拉遠揭曉——所謂無邊際泳池只是頂樓地上一個淺藍色塑膠小澡盆，水果盤放在小塑膠凳上。
   - `s03-boyfriend` (2.0s, `gurgle`)：水豚男友趴在澡盆邊緣，嘴角含著一根粗吸管往水裡吹氣製造水波（`gurgle`）。
   - `s04-bubble` (1.0s, `inhale, music_off`)：水豚鼓起雙頰用力過猛。
   - `s05-splash` (2.6s, `splash, poof, hold: 0.8`)：澡盆炸出一顆超大水泡破開，粉粉草帽歪掉、滿臉水珠呆坐定格。
3. **EP8〈極光露營〉（新規劃，約 12 秒）**：
   - `s01-aurora-still` (1.2s, `shutter`)：粉粉坐在浪漫三角帳篷前，夜空飄著夢幻翠綠極光。
   - `s02-livingroom` (2.8s, `recordscratch, blower`)：拉遠揭曉——客廳關了燈，帳篷是兩張椅子披床單，頭頂掛著一條透明綠紗巾被小風扇吹動。
   - `s03-boyfriend` (2.2s)：水豚男友站在小梯子上，兩隻毛爪拿著綠色手電筒往綠紗巾上晃，頭頂還夾著一盞藍色捕蚊燈。
   - `s04-zap` (2.5s, `click, powerdown, lights_out: [0.4, 0.8], music_off`)：手電筒滑落掉進床單帳篷裡，綠光直接從粉粉下巴由下往上照亮成搞笑夜光臉，接著兩聲 `click` 全黑。

---

## 六、2026-11-22 Google Flow 重製版（取代第四節的 H3 版）

照新規則重寫、盲評、分鏡審、用 Google Flow 重拍（流程見 [`../PRODUCTION-ROUTES.md`](../PRODUCTION-ROUTES.md) 第 8 項，教訓見 [`../../lessons/shorts.md`](../../lessons/shorts.md) 2026-11-22）。製作檔備份在雲端硬碟 `AI/備份/Shorts/<系列>/`，網站上的五集等站主核准。

- 成片審核：審片人 A 一輪、B 兩輪（B2），五集都可上架；e05 s06 可再剪短到 2.4 秒（選做）
- 排程提醒：e02 與 e03、e04 與 e05 不要相鄰

| 集 | 片長 | 盲評中位數 | 標題 |
|---|---|---|---|
| e01 | 9.2s | 71（修 s04 後） | 網美夕陽照拍到一半，負責舉夕陽的男友睡著了 #網美小豬 |
| e02 | 10.4s | 76 | 大熱天想拍雪國網美照，男友搬來一台刨冰機 #網美小豬 |
| e03 | 10.6s | 80 | 想拍仙境瀑布網美照，頂樓只有一個漏水的水塔 #網美小豬 |
| e04 | 9.4s | 68（修 s02 後，接受） | 櫻花樹上只有幾朵紙花，男友搬出了鼓風機 #網美小豬 |
| e05 | 11.0s | 65 → 照三位評審共識修改後接受，未再盲評 | 螢火蟲燈拍到一半全暗了，男友拔了插頭去吹電扇 #網美小豬 |
