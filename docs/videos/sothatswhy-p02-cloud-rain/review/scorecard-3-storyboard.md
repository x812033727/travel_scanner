# 評分表第二段（分鏡）：sothatswhy-p02-cloud-rain，第三版分鏡

- 評分依據：`docs/videos/so-thats-why/dialogue-pilot-20261103/SCORECARD.md`〈二、分鏡〉六項，每項 1–10，總分 60；門檻總分 ≥ 42，沒有任何一項低於 5。
- 評分者：獨立代理，沒有參與畫圖，也沒有讀過先前的評分檔。
- 看的材料：`分鏡v3-1.jpg` 到 `分鏡v3-5.jpg` 共 102 格（可疑的格子用 ffmpeg 放大兩倍再看）、角色設定圖 `chief/103.jpg` 與 `kid/002.jpg`、`script.md` 每鏡的台詞，以及 `tools/video/core/craft.mjs` 依 video.json 估出的每鏡秒數（還沒錄旁白，秒數都是估計值）。每格旁的「x/10」是畫圖工具自己的評審分數，沒有當成證據。
- 15 張文字卡不在分鏡表上，這次不評。

## 分數

| 項目 | 分數 | 證據 |
| --- | --- | --- |
| 角色一致 | **5** | 小問大多認得出來：深藍外套配芥末黃帽兜、黑色鮑伯頭、手上拿筆記本。可是有好幾張漂掉了：kid-puzzled 頭髮及肩、沒有呆毛；kid-no-weight 臉旁垂下一長撮頭髮；kid-ten-km、kid-million 像小男生；kid-snowball、kid-noon-guess 綁成紅繩馬尾或頭頂包子；balcony-call、kid-why-not-fall 的呆毛畫成了沖天髻。所長漂得更嚴重，髮型在低馬尾、頭頂包子（chief-kettle、mist-puff、supercooled）、短髮（chief-explains-mist、chief-no-pinch、chief-whiteboard）三種之間換來換去，還有幾張根本是另一個人：chief-expands 是短髮、圓臉的中年男性；chief-later 與 nucleus-droplet 換成寫實的成人畫風，擦口紅、戴耳環，chief-later 還打了領帶。這已經是評分表 4 分的描述（「髮型在兩三種之間漂、所長偶爾變成別人」），只靠眼鏡和芥末色開襟衫撐著，給 5 分。 |
| 開場 30 秒 | **7** | 前 30 秒有 7 張圖開始（balcony-call 0.0 s、tower-greying 5.1、chief-folder 9.5、kid-puzzled 13.2、chief-yes 17.4、chief-window 23.2、town-cloud-wide 29.5），遠超過 3 張。第二張 tower-greying 就是那朵下面變灰的雲本身，很好。不過第一張 balcony-call 是小問在陽台上喊人，背景只是普通的白積雲，沒有「一直往上長」的那朵；換句話說，第一張是旁觀的人，不是問題本身。另外第 3–6 張都是人物肖像。 |
| 一人一事 | **6** | 優點：兩個主角從頭到尾沒有同框過，大部分的臉也朝著鏡頭。缺點：沒有人的空景有 15 張（tower-greying、spout-gap、warm-bubble、elephants、collision、cold-top、cumulonimbus、grey-base、rain-drags、sign-anvil 等），雖然多半是科學插入鏡頭，但評分表把空景列為 4 分的特徵。另有配角搶戲：hot-street 的機車大叔、mountain-hike 的登山男孩、flat-bases 的農夫。人物小到看不清在做什麼的：kid-vapour-guess、condense-high、updraft-section、small-clouds、mountain-clouds、rain-shaft、cloud-stays、chief-how-high。側身或背對鏡頭的：kid-top-bubbling、chief-how-high。還有很多張只是站著拿紙、沒有在做事（lint 的 motion.look 也是這個結果）。 |
| 畫面與旁白對得上 | **6** | 大部分對得上，例如 drop-on-nose、elephants、kid-elephants、chief-a-day、feather-stone、chief-air-holds、rain-drags、cold-gust、sign-gust、kid-noon-guess、kid-burger。可是有 8 張講錯或講反，而且多半是解釋機制的關鍵鏡頭：chief-whiteboard 沒有白板也沒有一公里的方塊；collision 的水滴畫成黃色蜂蜜，也沒有在碰撞；cauliflower-grow 是一朵坐在草地上的笑臉雲；chief-not-tear 台詞說雨滴不是淚滴形，所長手上的紙卻畫了淚滴；iced-cup 杯子外面沒有水珠；chief-explains-mist 所長在解答，頭上卻冒問號；cumulonimbus 與 kid-three-pm 的雲畫成有柱子的蕈狀，看起來像爆炸。另有約 12 張只是勉強對得上（清單見下文）。 |
| 沒有假字 | **8** | 白板、時鐘、紙張大致都是空白、箭頭或沒有數字的刻度，沒有招牌亂碼。但 sign-anvil 右下角的牆上有一小塊粉紅色、像字的塗鴉或印章。這是縮圖表的解析度，只放大了 30 多格，建議用原圖再把所有格子的四個角掃一遍。 |
| 換圖間隔 | **8** | 依 video.json 估算（不含文字卡）：每張圖的中位數是 5.84 秒，略低於目標 6–12 秒的下限；最長的是 kid-was-snow 9.3 秒，遠低於 20 秒的上限。過短的有 kid-laundry-run 1.5 s、kid-balloon 2.0 s、kid-noon-guess 2.0 s，在一問一答裡可以接受。節奏偏快不偏慢，所以沒有碰到 4 分的描述；但中位數確實落在目標範圍外，扣 1 分。錄完旁白要用實際秒數再量一次。 |

**總分 40／60，門檻 42，不及格。** 沒有任何一項低於 5，但角色一致只剛好 5 分，總分差 2 分。只要重畫下列必須重畫的鏡頭，角色一致、畫面與旁白、沒有假字這三項應該都能各加 1–2 分，回到門檻以上。

## 必須重畫（15 張）

角色變成別人：

- **chief-expands**：所長畫成短髮、圓臉的中年男性，沒有馬尾。
- **chief-later**（8.0 s）：寫實的成人畫風，擦口紅、打領帶，和設定圖不是同一個人。
- **nucleus-droplet**：一樣是寫實的成人臉，擦口紅、戴耳環，畫風和其他所長的鏡頭斷開。
- **chief-no-pinch**：短髮，看不到馬尾和鉛筆，臉型也不同。
- **chief-whiteboard**（8.2 s）：所長的髮型像小男生，兩手各拿一支鉛筆；台詞說「一公里的大方塊」，畫面卻沒有白板也沒有方塊（同時是畫面與旁白對不上）。

畫面與旁白對不上，或講反了：

- **chief-not-tear**：台詞說「雨滴不是淚滴形」，所長手上的紙卻畫了一顆淚滴，直接教錯。
- **collision**（8.2 s）：水滴是黃色、有臉的蜂蜜滴，只是排成一列，沒有大滴追撞小滴。
- **cauliflower-grow**（8.2 s）：一朵笑臉雲坐在草地上，沒有往上長，也看不出花椰菜形；把雲放在地上會誤導觀眾。
- **iced-cup**：台詞的重點是「杯子外面冒出水珠」，杯子外面卻是乾的。
- **chief-explains-mist**（7.3 s）：所長正在給答案，頭上卻冒兩個問號，表演和台詞相反；髮型也是短髮。
- **cumulonimbus**（8.6 s）：雲從城市中間冒出一根柱子再撐開，看起來像蕈狀的爆炸雲。
- **kid-three-pm**：陽台外那朵「變灰的雲」畫成架在台座上、有柱子的灰色蕈狀煙，看起來像爆炸或煙囪；這朵雲是全片的主角。

不安全的動作或假字：

- **kid-top-bubbling**：小問跨坐在陽台欄杆上，是危險示範；身後那朵雲像一根煙柱；人物是側身。
- **sign-anvil**：右下角的牆上有一塊像字的粉紅色印章或塗鴉。

## 可以接受，有空再修

角色有點漂，但還認得出來：

- kid-puzzled：頭髮及肩，沒有呆毛。
- kid-no-weight：臉旁垂下一長撮頭髮。
- kid-ten-km、kid-million：像小男生。
- kid-snowball、kid-noon-guess：紅繩馬尾或頭頂包子。
- balcony-call、kid-why-not-fall：呆毛畫成沖天髻。
- palm-raindrop：帽兜大得像一頂帽子。
- kid-notebook-done：頭髮蓬成一大團。
- chief-kettle、mist-puff、supercooled：所長綁頭頂包子，不是低馬尾。

畫面和台詞只勉強對得上：

- updraft-section：畫的是放風箏，不是雲裡的上升氣流。
- kid-balloon：畫成玩具紅氣球，不是熱氣球。
- chief-ice-wins：所長拿一杯水，看不出冰晶比水滴更會搶水氣。
- chief-batch：沒有畫出雨滴落下的速度。
- chief-stamp：所長只拿一張空白紙，沒有雲散掉，也沒有雨滴。
- pan-on-stove：鍋子只露出畫面下緣，也沒有火。
- flat-bases：雲小到看不出底部是平的，還多了一個農夫。
- grey-base：雲底畫成一個黑洞，不像變灰的雲底。
- palm-big-drop：台詞說「好大顆」，手上卻沒有雨滴。
- small-clouds：雲太小太淡。
- cloud-stays：雲的形狀有點像蕈狀雲，但有雨幕，看得出是下雨的雲。
- mist-puff：白霧直接從壺嘴冒出，和前一鏡「壺嘴附近是透明的」沒有銜接。

構圖：

- 空景：tower-greying、spout-gap、warm-bubble、elephants、cold-top、rain-drags、mountain-clouds。它們是插入鏡頭，可以留，但不要再增加。
- 人物太小：kid-vapour-guess、condense-high、chief-how-high。chief-how-high 還是側身、貼著牆。
- 配角：hot-street 的機車大叔、mountain-hike 的登山男孩。
- 開場第一張 balcony-call：可以把「一直往上長的那朵雲」放大到前景，讓第一張就是問題本身。
