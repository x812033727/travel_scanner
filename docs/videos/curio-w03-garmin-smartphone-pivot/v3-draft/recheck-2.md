# 第二輪複查：curio-w03-garmin-smartphone-pivot v3-draft

複查者：Claude（獨立審查，沒參與撰稿），2026-11-05。對象：`video.json`（134 景，全部 shot，144 句）、`script.md`、`structure-map.md` 的第二輪說明；
標準沿用 `alignment.md` 與 `verify-1.md`。未修改 video.json。另外用 `garmin-v3/spec-v1.py` 對 `spec.py` 比對出這一輪實際改動的句子。

機械檢查：提示詞最長 300 字元（tables-marathon），全部 ≤350；沒有 no／not／without／text／blank，也沒有畫風字。
`data.characters: ["researcher"]` 共 36 景，跟提示詞裡出現 Ada 的景完全一致。以每秒 4.3 字估算，沒有一景超過 12 秒（最長 origin-bench 11.4 秒）。
lint 0 錯誤 1 警告（縮圖大標跟標題重複「Garmin」，不在這次範圍）。`loops` 的 17 組行號都對到新編號。
嚴重度：**必修**＝圖文矛盾、可能被讀成真人，或會逼出假字而被評審退；**建議**＝修了更好。

---

## 一、對齊複查

### 1-1 上輪 32 景：逐景結果

| 景 | 上輪問題 | 這輪 | 結果 |
|---|---|---|---|
| google-writing | 部落客會被讀成本人、螢幕空白 | 改成店老闆讀筆電 | 對象到位。**新問題：畫面是 blog post 加 tombstone，會逼出假字（墓碑上的 RIP、文章標題）**，見 1-4 |
| origin-navcomm | 會被讀成 Gary Burrell | 年輕女機師比讚 | 到位 |
| origin-new | 會被讀成高民環、「進到你車裡」沒畫 | 家用車頂綁軍用接收機 | 到位（駕駛性別沒寫，是男性也不至於被讀成高民環，因為整張是搞笑反差） |
| google-planes | 一景兩主體 | 拆成 google-planes、google-rivals | 到位；技工外型殘留已刪 |
| tables-marathon | 手機沒入畫 | 兩個跑者，一個把手機綁在手臂上 | 到位（兩人同框，見 1-5） |
| tables-panel | 手機沒入畫 | 手機歪貼在儀表板上 | 到位 |
| open-tease-pen | 頁面空白、只拍手 | 女主管寫年報，圖表先升後平 | 到位 |
| halt-callback | 回收不像開場 | 同一套 PEN 提示詞，只改動作 | 到位 |
| open-tease-phone | 看不出是導航機公司 | 滿桌導航機的工程師舉手機 | 到位 |
| phone-callback | 回收不像開場 | 同一套 PHONE 提示詞 | **大致到位，差一處**：開場寫 `tilting her head at it`，回收只寫 `smiling knowingly`，沒有 her，模型可能畫成男性，觀眾就認不出是同一張。見必修 |
| crash-plan | 西裝男會被讀成執行長 | 公園下棋的人 | 到位，下一景 phone-logic 接得上 |
| boom-doubt | 西裝男 | 店老闆 | 到位 |
| origin-zhushan | 農夫會被讀成本人 | 竹山遠景加一頭水牛 | 到位 |
| origin-degree | 純物件 | 校園、學士帽、行李箱、飛機 | 到位 |
| origin-cockpit-radio | 只有手、螢幕空白 | 年輕女技師測無線電 | 到位 |
| phone-factory | 讀成自家產線做手機 | 女工回頭看外面送進來的手機 | 到位（兩人同框，見 1-5） |
| halt-own | 兩個原因沒畫 | 研究員加軟木板三張圖 | 主體到位。**第三張是 newspaper with a big downward arrow，會逼出報紙標題**，見 1-4 |
| wrist-won | 裁判手勢讀不出「沒贏」 | 終點線，智慧錶先撞線 | 到位 |
| wrist-one-q | 跟旁白無關 | 研究員撕一頁日曆 | 到位（日曆頁會有數字，可接受） |
| margin-card | 卡片四格多於旁白 | 改成 margin-jars 插圖 | 卡片問題消失。**新問題：比例畫錯**，見 1-2 |
| turn-tables | 比喻沒鋪 | 旁白先鋪一句、畫面一大三小 | 到位 |
| tables-old | 只有船 | 漁夫對低飛的飛機揮手 | 到位，也跟 origin-boat 同一位漁夫 |
| margin-opinion | 書記沒交代、頁面空白 | 研究員點紅短條與藍長條 | 到位 |
| phone-blog | 打字的人會被讀成作者 | 只畫筆電 | 作者問題到位。**「blog page」加上圈了日期的月曆，兩樣都會逼出字**，見 1-4 |
| google-android | 商標、笑點 | 工程師舉原型機、尷尬笑 | 到位。建議把 `small gadgets around her` 改回 `small navigation boxes`，跟 open-tease-phone 是同一張工作台，觀眾才知道是 Garmin 的手機 |
| tables-watch | 錶面空白 | 等高線地圖加小路 | 到位 |
| crash-quarter | 頭版空白 | 頭版畫紅色箭頭與股價圖 | 不空白了，**但報紙頭版一定會被畫上標題字**，見 1-4 |
| close-not-only | 少一樣、報紙空白 | 四樣東西 | 數量到位。**報紙與劃掉的價格牌都會逼出字**，見 1-4 |
| origin-bench | 只有手 | 1989 年空工作室 | 到位。併進 t017 後少了「Gary 和 Min 拼在一起」，見 1-3 |
| origin-colleagues | 純物件 | 兩個杯子兩件外套 | 到位 |
| phone-alliance | 雙手特寫 | 兩位員工在記者會上握手 | **改出新問題**：記者會上握手的兩個人，最自然的讀法是兩家公司的老闆，其中一位就是在世的高民環（華碩那邊也是在世的人）。見必修 |
| close-mount | 純物件 | 女駕駛把手機夾進原本吸盤的位置 | 到位，跟 open-dash 同一位女駕駛 |

小結：32 景裡 27 景完全到位；phone-callback 差一個字；google-writing、phone-blog、crash-quarter、close-not-only、halt-own 的主體修好了，但換來假字風險；phone-alliance 改出誤讀風險；margin-jars 改出比例錯誤。

### 1-2 卡片改成的 14 張插圖：圖文相符嗎、接得住梗嗎

| 景 | 旁白 | 判斷 | 建議 |
|---|---|---|---|
| open-72 | 2008 年七成多靠車用 | 四分之三的圓餅，數字跟 72.6% 接近，接得住 | 不改 |
| open-double | 2025 年度營收是那一年的兩倍多 | 右邊那疊剛好兩倍高；now-total 用同一位女生回收，很好 | 可以把 `exactly twice` 改成 `a little more than twice`，跟「兩倍多」對齊（建議） |
| car-10x | 最多準十倍 | 一台機器螢幕上的紅點，加副駕座位紙地圖上的模糊大圈，兩個「誤差」分在兩個東西上，不好讀 | 建議：`...a small dashboard navigation box whose screen shows a tight red pin on a street corner inside a much larger faded circle that is shrinking away...`（同一個螢幕上大圈縮成小點） |
| boom-170 | 車用這一塊呢？多了 170% | 新堆幾乎頂到天花板、舊堆很小，2.7 倍可接受 | 不改 |
| google-free | 免費；貴的要 60 英鎊 | 撕價格牌，牌子會被畫上數字 | **必修（假字）**：改成手機綁上禮物緞帶，見 1-4 |
| google-asp | 平均售價掉 18% | 小價格牌貼在大價格牌上，兩張都會有數字 | **必修（假字）**：改成綁在盒子上的氣球慢慢消下去，見 1-4 |
| tables-share | 車用占比 58% 降到 19% | 貨架車用區縮小、手錶區擴大，接得住 | 不改 |
| now-split | 健身三分之一、戶外兩成八、航海飛航各一成多 | 四區大小順序對 | 不改 |
| wrist-premium | 500 美元以上 Garmin 第一 | 精品店領獎台，接得住；但三個人同框 | 不改（見 1-5） |
| now-guidance | 全年預估 81 億多，還沒發生 | 虛線箭頭指向一朵雲，「還沒發生」表達得好 | 不改 |
| margin-jars | 車用每百塊毛利 38.5，飛機 67 | **圖文矛盾**：`a nearly empty jar` 對 38.5，`much fuller` 對 67。38.5 是 67 的一半多，畫成「快空了」誇大了差距，會被讀成車用幾乎不賺 | **必修**：一罐裝到三分之一多一點、一罐裝到三分之二，提示詞見 1-4 |
| crash-quote | 「可能拖慢我們的成長」 | 研究員讀年報、旁邊亮著手機，接得住 | 不改（旁白見二） |
| turn-61 | 三塊賺六成一、營收只占三成八 | 天平飛機船鞋那邊重，接得住 | 不改 |
| tables-399 | 建議售價 399 美元；我是不會買，我連山都不爬 | 「超長價格牌」這個梗要靠牌子上的數字才成立，一定會畫出假數字 | **必修（假字）**：改成打開零錢包飛出一隻小蛾，見 1-4 |

### 1-3 併景之後，畫面還對得上加長的旁白嗎

| 景 | 併進來的句子 | 判斷 | 建議 |
|---|---|---|---|
| origin-bench | t016 ProNav ＋ t017 改名 Garmin，Gary 加 Min | 11.4 秒，只畫了「自己開公司」，名字的梗沒畫 | 建議在工作台加兩塊拼在一起的大拼圖，不用字也能表達「拼在一起」，提示詞見 1-4 |
| boom-170 | 問句加答案 | 對得上 | — |
| boom-nuvi | t031 主角是 nüvi ＋ t032 28%、52%、64% | 三排由左到右變高，最後一排占滿大半個貨架，對得上 | — |
| turn-61 | 61% ＋ 38% 是我算的 | 天平只畫利潤那一半，營收占比沒畫，可以接受 | — |
| tables-399 | 售價 ＋ 我不會買 | 見 1-2 | 必修 |
| tables-wait | 2019 年度追回 ＋ 整整十一年 | 線越過舊高點，旁邊一疊撕下來的日曆頁，「十一年」接得住 | — |
| now-pnd | 吸盤那種呢？＋ 還在賣、歸在戶外 | 卡車司機把導航機吸上擋風玻璃，「還在賣」接得住 | — |
| now-date | 這日子眼熟嗎？＋ 十七年前同一天 | 月曆圈一天，旁邊釘著有地圖的手機，接得住 | — |
| close-mount | 吸盤的位置呢？＋ 手機搶走了一大塊 | 對得上，也跟 open-dash 首尾呼應 | — |
| close-outro | 好啦 ＋ 留言 | 研究員闔檔案、旁邊一台舊導航機，對得上 | — |
| halt-callback ／ halt-quote | 拆成兩景 | halt-callback 跟開場同一套構圖；halt-quote 兩頁圖從上升變平，筆在中間，對得上「可能拖慢」換成「已經停止」 | — |
| google-planes ／ google-rivals | 拆成兩景 | 對得上 | — |
| close-answer ／ close-answer-b | 問句與答案拆兩景 | close-answer 研究員平靜地闔上報告，問句的張力沒出來 | 建議改成手按在報告上、抬頭看向觀眾、挑眉（建議） |

### 1-4 Ada 的 36 景：是不是都在講她在做的事

逐景看過，36 景都是研究員在「翻帳、讀年報、釘圖、秤錢、看圖表」，動作都跟當句旁白有關，沒有掛名入畫、跟旁白無關的景。需要調的：

| 景 | 問題 | 建議 |
|---|---|---|
| margin-jars | 比例矛盾（見 1-2） | **必修**：`Medium shot of Ada at a wooden desk holding up two glass money jars side by side, the jar beside a small toy car filled with coins a little over a third of the way up, the jar beside a small toy airplane filled two thirds of the way up, curious look, soft window light` |
| turn-why | t092 車用營業利益「兩年從五億二掉到兩億五」約剩一半，畫面寫 `a nearly empty one`，同樣誇大 | **必修**：`Medium shot of Ada at her desk beside a small toy car holding up two coin purses, a plump one from an old drawer in one hand and one about half as plump in the other, frowning, soft window light` |
| google-when | `one sentence circled on a report page` 會逼出一行假字；而且沒接上 crash-risk、google-unchanged 那張三角警告貼紙 | 建議：`Close-up of Ada holding a pencil over a small warning-triangle sticker in the margin of a report page, drawing a circle around it, looking up thoughtfully, lamp light` |
| tables-stuck | 旁白說「還掉到二十六億多」，畫面是 flat line | 建議：`...looking at a chart pinned to the wall whose line runs flat and then dips, chin in hand, lamp light` |
| google-year、halt-fall、tables-stuck | 三張都是「Ada 看牆上的圖表」，換季節而已，分鏡卡上會像同一張 | 建議 halt-fall 換動作，例如把一枚硬幣從高高的一疊拿走、疊變矮（建議） |
| tables-399、phone-reaction、tables-open | 這幾景的旁白是「我」（我不會買、我第一次讀到也覺得聰明、我不覺得這叫臨危換跑道），畫面是 Ada 在做這件事；可是 t039 介紹她用的是第三人稱「我們檔案局的研究員」。觀眾會分不清旁白的「我」是不是她 | 見三、必修 |
| wrist-q1（不是 Ada 景） | `a market researcher in a cardigan`：研究員、開襟衫、坐在桌前，跟 Ada（芥末黃開襟衫）太像，會被當成 Ada，或讓人以為 Ada 是 Counterpoint 的人 | 建議：`Medium shot of a young man in a grey hoodie at an office desk in spring sorting a pile of smartwatches into five small rows, focused, soft window light` |

### 1-5 會逼出假字的景，以及改成不需要字的畫面

站主已經定了畫面上不放文字，image-01 碰到報紙頭版、網頁、價格牌、新聞稿，幾乎一定會畫出亂碼字；九題評審的「文字」那題會退，重畫也是白花錢。
把字當主角的景都要改（**必修**）；錶面數字、月曆格子這種小面積的，評審通常不會退，列為建議。

| 景 | 會出字的東西 | 改成（全部 ≤350 字元，沒有禁用字） |
|---|---|---|
| crash-quarter | 報紙頭版 | `Medium shot of a worried shop owner in an empty electronics store in late autumn watching a small television on the counter whose screen shows a red line plunging down, rain on the window behind him, grey light` |
| halt-own | 軟木板上的報紙 | `Medium shot of Ada holding up a thick report beside a cork board pinned with three pictures: a smartphone with a map, a new car with a built-in dashboard screen, and a little grey storm cloud over a shop, serious, soft window light` |
| close-not-only | 報紙＋劃掉的價格牌 | `Medium shot of a shop owner in an electronics store looking at four things on his counter: a smartphone showing a map, a toy new car with a tiny dashboard screen, a little grey storm cloud figure and two toy navigation boxes in boxing gloves, thoughtful, soft store light`（景氣＝烏雲，跟 halt-own 同一個符號；價格戰＝戴拳擊手套的兩台導航機） |
| google-writing | 部落格文章、墓碑 | `Medium shot of a worried navigation-box shop owner at his counter in the evening reading a laptop whose screen shows a big picture of a small navigation box with tiny angel wings and a halo floating up into clouds, boxed navigation devices stacked behind him, warm lamp light` |
| phone-blog | blog page＋月曆日期 | `Close-up of a laptop on a desk late at night, its screen filled with a large street map and a blue route line, a red maple leaf and a coffee mug beside it, screen glow`（「二十八號」本來就畫不出來，楓葉交代十月就夠；now-date 那張月曆保留，因為旁白在問「這個日子」） |
| google-killer | 財經網站頁面 | `Close-up of a woman in an office in the afternoon looking at a laptop whose screen shows a big picture of a giant smartphone looming over a tiny navigation box, a big question mark floating between them, eyebrows raised, soft window light` |
| google-free | 撕價格牌 | `Medium shot of a grinning commuter on a train holding up a smartphone showing a simple map with a blue route line, the phone wrapped in a shiny red gift ribbon tied in a bow, soft window light` |
| google-asp | 價格牌疊價格牌 | `Medium shot of a store clerk in 2009 beside a long shelf of boxed dashboard navigation devices, holding a balloon tied to one box as it slowly shrinks and sags, a sheepish look, warm store light` |
| tables-399 | 超長價格牌 | `Medium shot of Ada in a sports shop holding a boxed outdoor watch in one hand and peering into her open coin purse with a startled look as a little moth flutters out, bright store light`（同時接得住下一句「我是不會」） |
| margin-price（建議） | 劃掉價格牌、貼小牌 | `Close-up of a shop assistant sliding a boxed navigation device down a playground slide on the counter toward a small pile of coins at the bottom, a long row of the same boxes waiting behind, soft store light` |
| turn-title、halt-release（建議） | 新聞稿紙面 | 現在的寫法把重點放在三張小圖上，可以先畫；評審因字退件再改成「信封裡滑出三張小照片」 |
| 錶面與螢幕數字（建議，不必改） | origin-cockpit-radio、origin-navcomm 的頻率數字；tables-runner、tables-fitness、wrist-rise、late-wrist、tables-watch 的配速、心率、高度；wrist-list 的 step counts | 面積小，可以先畫。被退時把 `a pace number` 換成 `a small heart icon` 或 `a small route line` |
| `photo` 這個字（建議） | phone-reaction、google-killer、google-legend、halt-cancel-b、halt-release、tables-open 寫 `photo of …` | 改成 `picture of …`，免得把畫風拉向照片質感 |

### 1-6 其他

- **phone-alliance（必修，誤讀）**：記者會上握手的兩個人會被讀成兩家公司的老闆，其中 Garmin 那位就是在世的高民環。改成只畫物件：
  `Close-up of a new smartphone showing a map with a blue route line standing on a press-conference table, tied with two ribbons of different colours knotted into one big bow, microphones in front of it and camera flashes glowing behind, warm stage light`
- **phone-callback（必修，呼應）**：補上 her，讓它跟開場是同一個人：
  `Medium shot of an engineer at a workbench crowded with small navigation boxes holding up a new smartphone whose screen shows a simple map with a blue route line, tilting her head at it with a knowing smile, soft lamp light`
- **origin-bench（建議）**：`Wide shot of a small rented workshop in 1989 at night, two empty stools at a cluttered workbench with a half-built circuit box, two big wooden puzzle pieces fitted together beside two coffee mugs, moving boxes stacked by the door, warm lamp light`
- **google-you（建議）**：t066「你可能也是那幾年，把車上那台拿下來的」現在是一隻手的特寫。改成 open-dash 那位女駕駛把導航機拔下來，第三次用到同一套擋風玻璃構圖，呼應更完整，也少一張手部特寫。
- **多人同框（建議，看評審結果再說）**：phone-factory、tables-marathon、wrist-won（兩人）、wrist-premium、close-tables（三人）。curio-episode skill 提醒 MiniMax 處理多人互動常出錯；這幾張的笑點都靠兩人對照，先畫，評審退了再改成單人加道具。
- 在世或 1956 年後過世的人：除了 phone-alliance，其他景都避開了。car-tv 空講台、phone-blog 只畫筆電、origin 三景都是無關人物或物件。open-tease-pen、halt-you 的女主管是虛構人物，Garmin 歷任執行長都是男性，不會被讀成特定的人。

---

## 二、事實複查

### 2-1 上輪要求的修句

| 原行 | 新行 | 新句 | 結果 |
|---|---|---|---|
| t007 | t007 | 還在交給主管機關的年報裡，親手寫下：我們的成長，已經停了。 | 照改 ✓ |
| t014 | t014 | Garmin 說，他替私人小飛機這個市場，設計出第一套成功的導航通訊機。 | 照改 ✓ |
| t020 | t020 | 這時候，它的產品是給飛機和船用的，不是給你家車上的。 | 照改 ✓ |
| t040 | t042 | 那年最後一季，營收掉了一成四；它自己寫的原因是景氣差，金融風暴來了。 | 照改 ✓ |
| t075 | t078 | …年報寫得很短：已經取消。 | 照改 ✓ |
| t130 | t134＋t135 | 所以，Garmin 到底有沒有在導航機上贏過手機？／沒有。手機讓它的成長停了，這句是它自己在年報裡寫的。 | 照改 ✓（拆成問答，「它自己寫的」只掛在「成長停了」上，意思跟建議句一樣） |
| t134 | t139＋t140 | 那擋風玻璃上那個吸盤的位置呢？／照它自己的年報，手機確實搶走了一大塊。 | 照改 ✓ |
| t028 | t028 | 再過六年，到了二〇〇六年，它的生意爆了：全公司營收一口氣多了七成三。 | 照改 ✓（2000＋6＝2006，因果拿掉了） |
| t041 | t043 | 在美國上市的公司，每年都要交一份年報給美國證券主管機關… | 照改 ✓ |

`sources` 已經補上 Volopedia、Garmin 2019-06-14 新聞稿、AOPA 2019-06-13、gps.gov、govinfo 白宮聲明、Garmin 2002 年度 10-K；說明欄已改成「資料截至 2026-11-05」；research-new.md 的 N3 已改成 leadership positions、06-14。上輪的「其他」也都處理了。

### 2-2 這一輪新增或改寫的句子

| 行 | 句子 | 判斷 |
|---|---|---|
| t009 | 故事的第一位主角，在台灣南投的竹山出生，名字叫高民環。 | 拿掉年代，沒有新事實 ✓。竹山出生仍沿用 10-31 的官網紀錄（#25），上輪已註明官網改版打不開；如果上架前還找不到第二個來源，退回「在台灣出生」 |
| t015 | 一九八三年，高民環也轉到一家做飛機電子儀器的公司，兩人成了同事。結果呢？ | 拿掉「後來」，變成 1983 年就是同事。Wikipedia（Burrell 在 King Radio 時於 1983 年找來高民環）支持 ✓。「結果呢？」不是事實 |
| t016、t017 | 一開始叫 ProNav。／後來改名 Garmin，就是把 Gary 和 Min 拼在一起。 | 原句拆開，N5、#25 ✓ |
| t029、t030 | 車用這一塊呢？／多了百分之一百七十。 | 原卡片句改成問答，#8 ✓ |
| t039 | 我們檔案局的研究員，把那一年的帳攤開來。 | 沒有事實；人稱的問題見三 |
| t040 | 車用每賣一百塊，毛利只有三十八塊半；飛機用的有六十七塊。 | 刪了「那一年」，上一句已經交代，#11 ✓ |
| t041 | 我覺得這個數字很值得記住：賣得最多的那一塊，每一百塊留得最少。 | 「留得最少」是跟全部四個事業比。#11 的四個毛利率（飛航 67.3、戶外健身 57.7、航海 54.5、車用 38.5）車用最低；車用 2008 年營收最大（#1、#2，72.6%）✓。「留」是指毛利，口語可以接受 |
| t044 | 二〇〇九年二月，Garmin 交出的這一份，風險那一段寫了什麼？ | 問句，#1 ✓ |
| t045 | 手機導航如果被大家接受，可能拖慢我們的成長。 | 引文本身 #4 ✓。**但原本有卡片標出這是年報原文，現在沒有卡片了，旁白直接說「我們的成長」，聽起來會像頻道自己在說「我們」**。建議改成「它寫：手機導航如果被大家接受，可能拖慢我們的成長。」（建議，不是事實錯） |
| t067 | 四個月後，它交出下一份年報。你猜，那句「可能」改了嗎？ | 2009-10-28 到 2010-02-24 約四個月，#5 ✓ |
| t073、t074 | 拆成兩句 | 意思沒變 ✓ |
| t083 | 同一句話，「可能拖慢」換成了「已經讓我們的成長停止」。 | 從 halt-quote 卡片拆出來，跟上輪 t080 同一句 #6 ✓；前面有引號，不會被聽成頻道的「我們」 |
| t093 | 把它的生意想成幾張桌子：車用那張最大，旁邊還擺著三張小的。 | 2010 年度車用 62%（#6）最大 ✓；「三張」對應新聞稿標題的戶外健身、飛航、航海（#21）✓ |
| t110 | 整整十一年。 | 卡片的「11 年」改成旁白，#32 ✓ |

**事實結論：沒有新的錯誤事實，也沒有改了意思的句子**。上輪九句都照改。只建議 t045 加「它寫：」。

---

## 三、故事連貫性（不能沒頭沒尾）

| 位置 | 問題 | 建議 |
|---|---|---|
| **t039 margin-ada（必修）** | 旁白從 t027 起就用「我」（我覺得、我算的、我不會買），t039 卻用第三人稱介紹「我們檔案局的研究員」。之後 phone-reaction（我第一次讀到也覺得聰明）、tables-open（我不覺得）、tables-399（我是不會）都是 Ada 在畫面上做旁白「我」的事。觀眾會卡在「說話的人是誰？那個女生是誰？」 | 兩種改法擇一：(a) Ada 就是旁白：t039 改成「我是檔案局的研究員，那一年的帳，我們攤開來看。」（沒有新事實，聲音也一樣是 Sulafat）；(b) Ada 不是旁白：把旁白說「我覺得、我不會買」的那幾景換成不是 Ada 的畫面。建議 (a)，改一句就好 |
| t008 → t009 | 承諾句問「營收憑什麼還翻了一倍？」，下一句直接跳到「故事的第一位主角」，沒有轉場；畫面上也沒有章節卡，只能靠旁白帶 | 建議 t009 改成「要回答這個問題，得從兩個人講起。第一位主角，在台灣南投的竹山出生，名字叫高民環。」（約 8 秒，不超過 12 秒上限） |
| t113 → t114 | t113 列了健身、戶外、航海、飛航四塊，t114 卻說「你可能會想：七成縮到不到一成」。「不到一成」那一塊還沒被說出來，聽的人要自己用 100 減 80 幾 | 建議 t113 結尾補「剩下最小的一塊，不到一成。」，t114 才接得上（建議） |
| t045 | 見二：沒有卡片之後，引文要用旁白標出是誰說的 | 加「它寫：」 |
| t134 | 「Garmin 到底有沒有在導航機上贏過手機？」這個問題前面沒有正式埋過（承諾句問的是營收），但 t004「大家都說被打趴」可以算鋪過，t137 也回收了承諾句 | 可以不改 |
| 畫面上的呼應 | phone-callback 少了 her（見 1-6）；google-android 的工作台改成 small gadgets，跟 open-tease-phone 那張斷了線 | 見上 |

**逐項確認已經接上的**：開場六個鉤子都有回收（t003→t111、t004→t141、t005→t112、t006→t047、t007→t082、t008→t137，加上 t001→t117、t139、t143 的擋風玻璃）；
t034 汐止、中壢、林口的自家工廠 → t053 不是自家工廠造的；t045 的「可能」→ t067、t068 → t076 → t083；t093 先鋪桌子 → t094 問 → t095 答 → t119、t137、t138、t141 都用同一個比喻；
t055 另一家公司 → t056 Google；t087「同一天」→ t088；Oct 28 → t131、t132。
人物都有先介紹：高民環、Gary Burrell、華碩（台灣的華碩）、賽斯納飛機、Counterpoint（市調公司）、9to5Mac（報導）、英國廣播公司。

---

## 結論

**還不能直接進配音與畫圖，要先修下面這些**（都是小修，改完不必再走一輪完整查核）。事實部分已經可以：上輪九句全部照改，新句沒有新事實。

**必修（配音前）**

1. **t039**：旁白「我」跟 Ada 的人稱統一，建議改成「我是檔案局的研究員，那一年的帳，我們攤開來看。」

**必修（畫圖前）**

2. **margin-jars**：兩個罐子比例照 38.5 對 67 畫，不要寫 nearly empty。
3. **turn-why**：兩個錢包改成「約一半」，不要寫 nearly empty。
4. **phone-alliance**：拿掉記者會握手的兩個人（會被讀成在世的高民環），改成綁蝴蝶結的手機。
5. **phone-callback**：補 her，跟 open-tease-phone 同一人。
6. **會逼出假字的 9 景**：crash-quarter、halt-own、close-not-only（報紙）、google-writing、phone-blog、google-killer（網頁）、google-free、google-asp、tables-399（價格牌），照 1-5 的提示詞換掉。

**建議（不擋進度）**：t045 加「它寫：」；t009 加轉場句；t113 補「剩下最小的一塊，不到一成」；google-android 改回 navigation boxes；google-when 圈三角貼紙；wrist-q1 換掉開襟衫研究員；origin-bench 加拼圖；
tables-stuck 加下跌；car-10x 把兩個誤差畫在同一個螢幕上；open-double 改成 a little more than twice；close-answer 改成抬頭挑眉；google-you 沿用 open-dash 構圖；halt-fall 換個動作；margin-price 改成溜滑梯；`photo` 改 `picture`；竹山出生上架前補第二個來源，找不到就退回「在台灣出生」。
