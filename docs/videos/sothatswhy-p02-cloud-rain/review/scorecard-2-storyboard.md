# 評分 2（只評分鏡）：sothatswhy-p02-cloud-rain 重畫後的 103 張

2026-11-03，獨立評分。評分者沒有畫這批圖，也沒有做第 1 輪評分；第 1 輪的 31／60 只拿來對照，沒有當起點。

- 評分表：[`docs/videos/so-thats-why/dialogue-pilot-20261103/SCORECARD.md`](../../so-thats-why/dialogue-pilot-20261103/SCORECARD.md) 第二段〈分鏡〉六項，每項 1–10，門檻總分 ≥ 42 且沒有一項低於 5。
- 依據：分鏡聯絡表 v2 五頁（103 張，依畫面順序，逐列放大檢查，可疑的單張再放大）、設定圖 `characters/chief/103.jpg`（圓黑框眼鏡、黑髮帶一撮灰、低馬尾、耳後鉛筆、芥末黃開襟衫）與 `characters/kid/002.jpg`（八歲女孩、黑色妹妹頭、齊瀏海加一撮翹毛、深藍雨衣外套、芥末黃帽兜）、`script.md` 每鏡台詞、`node tools/video/cli.mjs lint --slug sothatswhy-p02-cloud-rain`（0 錯、20 警告；估 11.5 分鐘）。
- 每鏡秒數是 lint 的估算（`craftChecks` 加 `estimateTimeline`），不是剪好的片。
- 聯絡表上每張旁邊的「9.29/10」是出圖端自己的檢查分數，跟這份評分無關；像 `sign-anvil`、`rain-stops`、`cumulonimbus` 都標 9.29，卻跟台詞矛盾，所以那個分數不能當驗收。

## 總表

| 項目 | 分數 | 證據 |
| --- | --- | --- |
| 角色一致 | **4** | 大多數鏡頭已經認得出是同兩個人，比上一輪穩；但「所長偶爾變成別人」「髮型在兩三種之間漂」兩句 4 分描述仍然成立。所長有 10 張明顯走樣：`chief-window`、`chief-laugh`、`chief-how-high` 變成滿頭灰白的老太太，`chief-explains-mist`、`chief-expands`、`chief-falls-slowly`、`chief-answer-one`、`chief-anvil` 沒有灰髮或換了細框眼鏡，`chief-batch` 變短髮沒馬尾，`chief-second` 整個換成另一種畫風。小問有 9 張明顯走樣：棕髮（`kid-puzzled`、`kid-elevator`）、雙丸子頭加裙子（`kid-why-not-fall`）、男孩沖天髮（`kid-million`、`kid-noon-guess`、`kid-flat-bottoms`）、馬尾小人（`kid-vapour-guess`）、戴安全帽騎機車（`hot-street`）、遮陽帽吊帶褲（`sea-breeze`）。另有 7–8 張出現不在演員表裡的第三者（見清單 C）。約兩成鏡頭有角色問題，扣到 4。 |
| 開場 30 秒 | **6** | 前 30 秒開始的圖有 7 張（`balcony-call` 0.0 s 到 `town-cloud-wide` 29.6 s），數量過關。但第一張的主體是小問在陽台上指，雲只是背景小小一團，還不是「第一張就是問題本身」；第二張 `tower-greying` 才是那朵雲，卻沒畫出「下面變成灰色」，屋頂上還多一個黃色怪人。第 7 張配「幾頭大象」卻畫街口和騎機車的小孩，招牌有亂碼。 |
| 一人一事 | **6** | 沒有發現兩個主角同框，大部分人物鏡頭是一個人朝鏡頭做一件事，這點做到。扣分在：第三者入鏡 7–8 張（清單 C）；人物小到只佔畫面一角、其餘是空牆的 5 張（`kid-vapour-guess`、`kid-who-cools`、`condense-high`、`small-clouds`、`droplet-vanish`）；沒有人的空景 14 張（lint `risk.decorative` 14%，目標 ≤ 10%），其中 `spout-gap`、`warm-bubble`、`elephants`、`rain-drags`、`cold-top` 有回答台詞，算插入鏡頭可以接受。 |
| 畫面與旁白對得上 | **5** | 約 85 張對得上，好的例子：`chief-a-day`（時鐘）、`feather-stone`、`palm-raindrop`、`chief-still-there`、`rain-shaft`、`cloud-stays`、`rain-drags`、`sign-gust`。但有 12 張跟台詞矛盾或在講別件事（清單 B），其中幾張是本集的關鍵畫面：`cumulonimbus` 把積雨雲畫成一棵樹、`sign-anvil` 說「頭頂變平攤開」卻看不到頂、`rain-stops` 說「雨停了」窗外還在下、`tower-greying` 說「下面變灰」雲底是白的。剛好在 4 分描述之上一格。 |
| 沒有假字 | **6** | 雲上不再有臉，這是比上一輪進步最多的地方。仍有 4 張有像字的塗鴉或印章：`town-cloud-wide` 路牌是亂碼「⟨叩忠⟩」、右邊立牌有假字；`chief-whiteboard` 方塊上一個紅色假漢字；`chief-stamp` 紙上蓋出紅色假印文；`chief-second` 左牆告示有紅色塗鴉字。另 `cumulonimbus` 背景樓房有紅色招牌色塊（輕微）。「招牌有亂碼」「有印章」各還有一例，扣到 6。 |
| 換圖間隔 | **9** | lint 估算：人物鏡頭中位數 5.9 s、最長 9.3 s（`kid-was-snow`）；加進文字卡後最長一段約 12.5 s（`drop-shapes` 卡，兩句）。評分表要中位數 6–12 s、最長 ≤ 20 s：最長遠低於上限，中位數比下限快 0.1 s，對觀眾不是缺點。不給 10 是因為這是估算，剪完要用實際秒數再量一次。 |
| **總分** | **36／60** | **沒過**：門檻 ≥ 42，而且「角色一致」4 分低於單項下限 5。 |

比上一輪（31）多 5 分，主要來自假字（雲臉沒了）與畫面對旁白；角色一致仍是卡住的那一項。

## 清單

### A. 角色走樣

所長（10 張要重畫）：

| 鏡頭 | 問題 |
| --- | --- |
| `chief-window` | 滿頭灰髮、紅唇、米色襯衫加胸章，看起來是另一位年長女性 |
| `chief-explains-mist` | 沒有灰髮、頭髮散開沒馬尾、髮夾取代鉛筆、紅唇 |
| `chief-expands` | 棕髮、沒有灰髮那一撮、沒有鉛筆 |
| `chief-laugh` | 整頭灰白像奶奶 |
| `chief-second` | 換成另一種平塗畫風、臉型不同、眼鏡變細 |
| `chief-falls-slowly` | 沒有灰髮、細框棕眼鏡、行舉手禮 |
| `chief-answer-one` | 細框小眼鏡、沒有灰髮，像路人 |
| `chief-batch` | 短髮沒有馬尾 |
| `chief-how-high` | 整頭白髮，老化 |
| `chief-anvil` | 細框眼鏡、鉛筆頂在頭上、灰髮幾乎不見 |

所長（可以容忍）：`chief-kettle`、`supercooled`、`chief-air-holds`（低馬尾變成包頭，其他都對）；`chief-later`（多了領帶與紅唇）；`chief-no-pinch`（頭頂被裁掉，灰髮看不到）；`nucleus-droplet`、`chief-remember`（略顯年長但特徵都在）。

小問（9 張要重畫）：

| 鏡頭 | 問題 |
| --- | --- |
| `kid-puzzled` | 棕髮、側分沒有齊瀏海 |
| `kid-why-not-fall` | 雙丸子頭、白裙 |
| `kid-vapour-guess` | 馬尾，人小到看不出是誰（另見 D） |
| `hot-street` | 戴安全帽騎機車送貨，認不出是小問，八歲騎車也不合理 |
| `kid-flat-bottoms` | 刺蝟男孩頭，沒有妹妹頭 |
| `kid-elevator` | 棕色捲髮、綠眼睛 |
| `kid-million` | 男孩沖天髮、沒有瀏海 |
| `kid-noon-guess` | 男孩沖天髮 |
| `sea-breeze` | 遮陽帽、吊帶褲，雨衣外套不見 |

小問（可以容忍）：`kid-elephants`、`kid-pinch`、`kid-snowball`、`cold-gust`、`kid-top-bubbling`（翹毛變成小馬尾或沖天，但瀏海、外套對）；`kid-ten-km`（偏男孩臉）；`kid-burger`（髮色略棕、較長）；`droplet-vanish`、`snow-to-rain`（頭頂小包頭）。

### B. 畫面跟台詞矛盾或在講別件事

| 鏡頭 | 台詞 | 畫面 | 處置 |
| --- | --- | --- | --- |
| `tower-greying` | 現在下面變成灰色了 | 雲底是白的，屋頂多一個黃色怪人 | 重畫 |
| `town-cloud-wide` | 五百公噸，大概是幾頭大象？ | 街口、騎機車的小孩，沒有大象 | 重畫（也在 E） |
| `hot-street` | 太陽把地面曬熱… | 機車送貨，看不出熱 | 重畫（也在 A） |
| `chief-second` | 這些水分成非常非常多顆 | 所長比兩個 YA，空白板 | 重畫（也在 A） |
| `chief-falls-slowly` | 它一直在往下掉，只是很慢 | 所長行舉手禮，沒有東西在掉 | 重畫（也在 A） |
| `collision` | 大的掉得快，追上撞上小的 | 小問舉著漏勺 | 重畫 |
| `chief-batch` | 雨滴一秒落下六、七公尺 | 所長用水壺倒水 | 重畫（也在 A） |
| `small-clouds` | 那種小小、扁扁的白雲 | 幾乎沒有雲，只有紙飛機 | 重畫 |
| `cumulonimbus` | 一路往上衝的雲，雲頂超過十公里 | 雲長在一根樹幹上，像一棵樹；兩隻貓 | 重畫 |
| `sign-anvil` | 頭頂變平了，往旁邊攤開 | 雲塞滿畫面看不到頂，屋頂有小怪人 | 重畫 |
| `rain-stops` | 雨也停了 | 窗外還在下雨 | 重畫 |
| `chief-stamp` | 引擎關掉，雲就散了 | 所長蓋印章 | 重畫（也在 E） |

可以容忍（弱但不矛盾）：`chief-answer-one`（空白畫架，已列 A）、`chief-anvil`（沒有鐵砧，已列 A）、`chief-phone-call`（沒畫花椰菜雲）、`chief-ice-wins`（只拿一杯水）、`chief-magnifier`（放大鏡照空白）、`kid-snail`（沒有對照物）、`chief-yes`（說五百公噸但畫面沒有雲）、`condense-high`、`grey-base`（雲底灰了，但人飛在空中，見 C）。`chief-not-tear` 的卡片畫成淚滴形，是在示範「大家都這樣畫」，可以接受。

### C. 不在演員表裡的第三者

| 鏡頭 | 問題 | 處置 |
| --- | --- | --- |
| `tower-greying` | 屋頂上的黃色圓臉怪人 | 重畫（已列 B） |
| `cauliflower-grow` | 戴頭盔的藍色小怪物在放風箏 | 重畫 |
| `grey-base` | 長翅膀的小人飛在雲底下 | 重畫 |
| `cumulonimbus` | 兩隻有表情的貓 | 重畫（已列 B） |
| `sign-anvil` | 屋頂上三個小怪人 | 重畫（已列 B） |
| `mountain-hike` | 陌生男孩登山 | 容忍：台詞對「你」說，可以讀成觀眾的替身 |
| `flat-bases` | 戴斗笠的農夫 | 容忍：很小，雲底平的有畫出來 |

### D. 空景或裝飾性畫面

人小到只剩一角：`kid-vapour-guess`（已列 A，重畫）、`kid-who-cools`、`condense-high`、`small-clouds`（已列 B）、`droplet-vanish`；後三張以外都可容忍。純空景 14 張中，`spout-gap`、`warm-bubble`、`elephants`、`cold-top`、`rain-drags`、`mountain-clouds` 有回答台詞，當插入鏡頭保留。

### E. 假字與印章

| 鏡頭 | 問題 | 處置 |
| --- | --- | --- |
| `town-cloud-wide` | 綠色路牌亂碼「⟨叩忠⟩」，右側立牌有假字 | 重畫 |
| `chief-whiteboard` | 白板方塊上一個紅色假漢字 | 重畫（或修掉那一塊） |
| `chief-stamp` | 紙上紅色假印文 | 重畫（已列 B） |
| `chief-second` | 左牆告示上的紅色塗鴉字 | 重畫（已列 A） |
| `cumulonimbus` | 背景樓房紅色招牌色塊 | 跟著 B 重畫 |

雲或物件上畫臉：這輪**沒有**。

## 建議真正重畫的鏡頭（30／103）

依畫面順序：

`tower-greying`、`kid-puzzled`、`chief-window`、`town-cloud-wide`、`kid-why-not-fall`、`hot-street`、`kid-vapour-guess`、`chief-explains-mist`、`chief-expands`、`kid-flat-bottoms`、`cauliflower-grow`、`chief-whiteboard`、`chief-laugh`、`chief-second`、`chief-falls-slowly`、`kid-elevator`、`chief-answer-one`、`kid-million`、`collision`、`chief-batch`、`chief-how-high`、`small-clouds`、`cumulonimbus`、`kid-noon-guess`、`sea-breeze`、`grey-base`、`sign-anvil`、`chief-anvil`、`rain-stops`、`chief-stamp`

估計：只重畫角色走樣的 19 張，「角色一致」可回到 6–7；B 的 12 張改好，「畫面與旁白」可到 7；E 的 4 張清掉，「假字」可到 8–9。三項都做到，總分大約 44–47，可以過 42。開場可以順便把 `balcony-call` 改成雲佔畫面主體、小問在前景指著它。

可以容忍、這輪不必花錢的：A、B、C、D 各表「容忍」列出的鏡頭。
