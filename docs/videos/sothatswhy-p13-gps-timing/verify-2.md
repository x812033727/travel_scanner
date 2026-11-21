# 查核報告 2（sothatswhy-p13-gps-timing）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒參與第一輪查核）
- 日期：2026-11-11
- 範圍：第一輪查核（`verify-1.md`）之後為了說故事改寫的 **52 句新增或改字的台詞**（以目前 `video.json` 的編號：p006、p010–p013、p033、p038、p041–p046、p054、p055、p057、p058、p060、p077、p079、p089、p090、p113、p114、p117、p121、p127、p131、p132、p134–p140、p142–p144、p152–p155、p157、p161、p176、p177、p180、p182–p185），加上改過的 YouTube 說明。沒改的句子沿用第一輪的結論，本輪不重判。
- 方法：在 `video.json` 的 `scenes[].lines` 裡讀每一句改過的台詞和它的前後文（全片 p001–p190 讀過一遍），說明欄讀 `youtube.description`。`claims.md` 只當線索，不採用它的引文。每個來源都在當天重新打開讀原文：curl GET，HTML 去掉標籤轉成純文字以後 grep，再讀上下文；PDF 用 `pdftotext -layout` 轉。
  - GPS.gov〈GPS Accuracy〉node/70（200，53,877 bytes）：讀 URE 承諾、"URE is not user accuracy" 一段，以及 Selective Availability 一題。
  - GPS.gov〈Frequently Asked Questions〉faq（200）讀燈塔一句；〈Space Segment〉（200）讀 20,200 km 和 24 個位置。
  - DoD《GPS SPS Performance Standard》第 5 版，2020 年 4 月（200，2,166,466 bytes）：讀 §2.2 的 50 bps，以及 Fig. 2.2-1 的 Subframe 1–3 和 "30 sec repeat"。
  - FAA〈Satellite Navigation - GPS - How It Works〉（200）：讀原子鐘、至少四顆、"An atomic clock synchronized to GPS is required"，以及電離層和對流層一句。
  - ESA Navipedia：〈Ionospheric Delay〉oldid=13741、〈Klobuchar Ionospheric Model〉oldid=16790、〈Multipath〉oldid=11617、〈TTFF〉oldid=13355、〈Code Based Positioning (SPS)〉oldid=12251，另外讀〈About navipedia〉oldid=16646 確認是誰的網站（皆 200）。
  - Blay, Wang & Akos 2021（NAVIGATION 68(1):217）：navi.ion.org 期刊 HTML 全文（200，226,281 bytes），讀摘要、§1、§2、§2.1、§2.3。
  - Ashby 2003（Living Reviews in Relativity 6:1）：Europe PMC fullTextXML（200，289,549 bytes），讀式 (35)–(36)，以及 "before the clock is placed in orbit" 一句。
  - van Diggelen & Enge 2015（ION GNSS+ 2015）：ion.org 摘要頁（200）。
  - NOAA NWS〈Understanding Lightning: Thunder〉（200）；NIST CODATA 光速（200）。
  - 自己重算：4.4647×10⁻¹⁰ × 86,400 s = 38.575 µs；38.575 µs × 299,792,458 m/s = 11,564 m；10⁻⁶ s × c = 299.8 m；1 英里 1,609.3 m ÷ 5 s = 321.9 m/s；「三秒一公里」= 333 m/s。
- 打不開或沒讀到原文的：ION GNSS+ 2015 論文全文要付費，只讀了摘要。Van Diggelen 2009（800 m 的原始出處）沒讀。電離層閃爍（scintillation）和都市裡非直視訊號（NLOS）的誤差大小，在本輪讀的來源裡都沒有數字，下文判斷時只當附註，沒拿來當依據。
- 結論統計，52 句改過的台詞：**正確 51、需改 1、錯誤 0**。YouTube 說明 1 項：**需改 1**。另外有 4 處選修建議，不影響結論，見文末。
- 字數：建議句含標點計算，小問 ≤15、所長 ≤25。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| G01 | p142（所長） | 所以把你甩到對街的，不是天上那段路。 | 需改（撰稿推論說成定論） | p138 的推論說得通，見下表（電離層不會在幾十公尺之間突然變），但它只能說明電離層**不太會讓藍點突然跳**，不能說明電離層**完全沒有**讓藍點偏。單頻修正以後還留下約一半：Navipedia〈Klobuchar〉"is estimated to reduce about the 50% RMS ionospheric range error worldwide"，而效應本身 "can reach up to several teens of meters"（〈Ionospheric Delay〉）。FAA 也把對流層列為路上的延遲："propagation delays or decreases in the signal's speed caused by the ionosphere and the troposphere"，片中沒有排除它。來源也沒有任何數字說哪一個原因把人「甩到對街」。說明欄自己用的是「多半」，台詞應該一致 | 所以把你甩到對街的，多半不是天上那段路。（20 字） |
| G02 | YouTube 說明 | 高空的電離層也會拖慢訊號，但它整片天空一起變，大多修得掉 | 需改（兩處說過頭） | ①「大多修得掉」只有雙頻做得到。單頻用廣播模型只修掉約一半：Navipedia〈Klobuchar〉"estimated to reduce about the 50% RMS ionospheric range error worldwide"；"more than 99.9%" 是 "using two frequency measurements"（〈Ionospheric Delay〉）。片中 p139–p141 本來就分開講，說明欄把兩者合成一句「大多」。②「整片天空**一起**變」比片中的「慢慢變」更強，會讓人以為各地都一樣。來源寫的是會隨地點變："The TEC, and thence, the ionospheric refraction depends on the geographical location of the receiver, the hour of day and the solar activity"，並提到 "equatorial anomalies"。 | 「高空的電離層也會拖慢訊號，但它是整片天空慢慢變，不會在大樓之間突然跳，而且修得掉一部分，同時聽兩個頻率幾乎全修掉；」其餘照留（另見選修 S4） |

## 二、逐句核對（改過的句子：正確的依據）

| 行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p006 | 重開地圖，藍點還等好久（小問） | 正確 | — | 小問的經驗；p143–p160 回收（冷開機、三十六秒） |
| p010–p011 | 差百萬分之一秒，距離會差多少；小問猜一兩公尺 | 正確 | — | 問句與錯猜，p041–p042 回答 |
| p012 | 比你猜的多很多；手機至少要聽四顆衛星 | 正確 | FAA | "a combination of signals from at least four satellites, to determine their location and time" |
| p013 | 多出來的那一顆在幫誰 | 正確 | — | 懸念，p083–p088 回答 |
| p033 | 衛星就是那個朋友；帶著原子鐘，非常非常準的鐘 | 正確 | FAA | "GPS satellites carry atomic clocks that provide extremely accurate time." |
| p038 | 通常只要六十到九十毫秒；一毫秒是千分之一秒 | 正確 | Blay 2021 §2.3 | "the travel time from satellite to receiver is typically 60 to 90 milliseconds"；毫秒＝10⁻³ 秒是定義 |
| p041–p042 | 剛剛那百萬分之一秒，光跑了大約三百公尺，不是一兩公尺 | 正確 | NIST（換算） | 10⁻⁶ s × 299,792,458 m/s = 299.8 m。這是第一章的回收：回答 p010、糾正 p011 |
| p043–p045 | 差一點點都不行；衛星的錶真的那麼準嗎（小問） | 正確 | — | 反應與提問 |
| p046 | 原子鐘很準，可是還有一件事要修 | 正確 | FAA；Ashby 2003 | FAA "extremely accurate time"；Ashby "the standard clock in orbit is beating too fast"，所以要修 |
| p054 | 一微秒，就是開頭那個百萬分之一秒 | 正確 | 定義 | 微秒＝10⁻⁶ 秒，跟 p010 的「百萬分之一秒」相同 |
| p055 | 那也太短了吧（小問） | 正確 | — | 反應；p056 用十一公里多回答（沒改，第一輪已判正確） |
| p057 | 不修的話，哨子報的時間，一天就錯這麼多 | 正確（附註） | Ashby 2003（換算） | 錯的是衛星報的**時間**：−4.4647×10⁻¹⁰ × 86,400 s ≈ 38.58 µs，換成光跑的距離是 11.56 km（p056）。句子主語是「哨子報的時間」，沒有說「定位每天飄 11 公里」（接收機的鐘差未知數會吸收共同偏差），措辭守住了。附註：「這麼多」緊接在「十一公里多」後面，小孩可能聽成藍點會偏 11 公里；字面沒錯，可留 |
| p058 | 有些衛星的鐘，上去之前就先在地面調慢 | 正確 | Ashby 2003 | "This adjustment is accomplished on the ground before the clock is placed in orbit."；"[1 − 4.4647×10⁻¹⁰] × 10.23 MHz = 10.22999999543 MHz"（往下調）；「有些」對應 Rubidium 鐘入軌以後才量的另一種做法（p059，沒改） |
| p060 | 時間能信了（小問） | 正確（簡化） | Ashby 2003；SPS PS Fig. 2.2-1 | 相對論修好，廣播裡還有 "Satellite Clock Correction Terms"；用小孩的話收段，可留 |
| p077 | 回到公園；哨子是聲音；假設你的錶慢了一秒 | 正確（比喻） | — | 錶慢一秒，所以量到的延遲短了一秒 |
| p079 | 還記得雷聲三秒一公里？每個朋友都像近了三百多公尺 | 正確 | NWS（換算） | NWS "it takes the sound of thunder about 5 seconds to travel a mile" → 1,609 m ÷ 5 = 322 m/s；「三秒一公里」→ 333 m/s；兩種算法都落在「三百多公尺」。錶慢 → 以為比較近，方向對。哨子遊戲用聲速，GPS 用光速，片中分得清楚（p077 先說「哨子是聲音」） |
| p089–p090 | 還記得那些圓圈；真的手機不畫圈，四個答案一次算出來 | 正確（簡化） | Navipedia SPS | "the four unknown parameters: The receiver coordinates (x,y,z) and the receiver clock offset δt"，用線性化求解。「一次算出來」指同時求解，實際是反覆修正，跟第一輪附註相同 |
| p113–p114 | 會不會給我們的故意弄不準（小問） | 正確 | — | 錯猜，p115–p117 回答 |
| p117 | 而且訊號本身變差，到處都會偏，不會專挑大樓中間 | 正確（撰稿推論，合理） | GPS.gov node/70 | "Selective Availability that intentionally degraded civilian accuracy on a global basis"。訊號本身的誤差（URE）是衛星端的性質，到哪裡都一樣，所以不會只出現在大樓中間，推論成立。附註：①大樓中間的放大倍數（DOP）較大，訊號變差時那裡偏得更多，但「不會**專挑**」仍然對；②接在「二〇〇〇年就停了」後面，「訊號本身變差」是假設語氣，省略了「就算」，見選修 S1 |
| p121 | 手上的誤差，還要加上訊號在路上遇到的事 | 正確（簡化） | GPS.gov node/70 | "User accuracy depends on a combination of satellite geometry, URE, and local factors such as signal blockage, atmospheric conditions, and receiver design features/quality."；幾何已在 p098–p106 講過，「路上遇到的事」涵蓋遮擋和大氣，沒提接收機品質，簡化可留 |
| p127 | 還記得那條天空的縫；有時候是擋住，有時候更麻煩 | 正確 | GPS.gov node/70 | "Satellite signal blockage due to buildings"、"Signals reflected off buildings or walls ("multipath")"；「更麻煩」是所長的說法 |
| p131–p132 | 歐洲太空總署的導航教材說：主要是因為天線太靠近會反射的東西 | 正確（附註） | Navipedia Multipath；About navipedia | "Its principal cause is the antenna closeness to the reflecting structures"；"NAVIPEDIA is an initiative of the European Space Agency … conceived as a collaborative GNSS encyclopaedia"。歸屬對：網站是 ESA 發起並主辦；它自稱「百科」，說成「教材」有點寬，見選修 S2 |
| p134–p135 | 會不會是天上那段路把藍點弄歪（小問） | 正確 | — | 錯猜 |
| p136 | 天上會拖慢訊號；高空有一層叫電離層 | 正確 | Navipedia Ionospheric Delay；FAA | "extends itself from about 60 km until more than 2.000 km in high"；碼量測 "suffer a positive delay"；FAA "decreases in the signal's speed caused by the ionosphere" |
| p137 | 只聽一個頻率（像只聽一種音高），這個效應可以到幾十公尺 | 正確 | Navipedia Ionospheric Delay | "single frequency receivers have to apply an ionospheric prediction model to remove (as much as possible) this effect, that can reach up to several teens of meters"（"teens" 應是 tens 的筆誤，「幾十公尺」合理）。說的是效應本身，不是修正後剩下的；音高是示意 |
| p138 | 可是它是整片天空慢慢變，不會在兩棟大樓之間突然跳 | 正確（撰稿推論，合理；附註） | Navipedia Ionospheric Delay；Klobuchar | 來源沒有直接寫這句。依據：電離層在 60–2,000 多公里高；"The TEC, and thence, the ionospheric refraction depends on the geographical location of the receiver, the hour of day and the solar activity"，變化的尺度是地理位置、時刻、太陽活動，不是幾十公尺；廣播模型把它當作 "a thin layer at 350 kilometres in height"，夜間是 "a constant value"、白天是 "a half-cosine function"。兩棟大樓相隔幾十公尺，訊號穿過的是同一片電離層，所以「不會在兩棟大樓之間突然跳」是公平的推論。附註：句子用肯定語氣，沒有加保留詞；「慢慢變」在磁赤道附近的異常區（Navipedia 提到 "equatorial anomalies"，台灣在其北側）有閃爍等快速變化的例外，本輪來源沒讀到細節。重點是「空間上不會在大樓之間跳」，這部分站得住，可留 |
| p139 | 衛星廣播的修正，估計全世界平均約修掉一半 | 正確 | Navipedia Klobuchar | "GPS satellites broadcast the parameters … estimated to reduce about the 50% RMS ionospheric range error worldwide"；已補上「估計」（第一輪的 S6） |
| p140 | 同時聽高低兩個頻率，像比一比兩支哨子 | 正確（示意） | Navipedia Ionospheric Delay | "refraction depends on its frequencies (as the squared inverse)"；兩支哨子是示意（空氣中的聲音沒有這種色散），p141 的九成九以上沒改 |
| p143–p144 | 重開地圖那次，藍點怎麼等那麼久（小問） | 正確 | — | 接回 p006 |
| p152 | 一整輪要三十秒，才從頭再講一次 | 正確 | SPS PS Fig. 2.2-1 | "Frame (30 sec repeat)" |
| p153 | 鐘差跟衛星在哪，放在每一輪最前面的三段 | 正確 | SPS PS Fig. 2.2-1 | Subframe 1 "… Health, and Satellite Clock Correction Terms"；Subframe 2、3 "Ephemeris Parameters"。Subframe 1 也有健康狀態等，簡化可留 |
| p154 | 傳統的做法要聽完這三段，最久要等大約三十六秒 | 正確 | Blay 2021 §2 | "Conventional GNSS receivers need to receive the data from the first three subframes of the 30 second navigation frame … it can take as long as 36 seconds" |
| p155 | 等那麼久（小問） | 正確 | — | 反應 |
| p157 | 所以開機有分冷、熱 | 正確（簡化） | Navipedia TTFF | 來源列了 cold、warm、hot start，片中省略暖開機，第一輪已接受 |
| p161 | 可是有時候（小問） | 正確 | — | 接 p162 |
| p176 | 你在街角一打開就看到的藍點，可能就是這樣算出來的 | 正確（推論已用「可能」） | Blay 2021 摘要、§1、§2.1 | "assisted GPS/GNSS can reduce the time to first fix (TTFF) dramatically"；"van Diggelen's technique … is the one that is representative and is being widely used"；"there now must be at least five satellites … a closed-form five-state solution has been developed to solve for the position without precise time"。前一句 p174 已說「有些手機」，這句再用「可能」，沒有說每支手機都這樣。附註：一打開就出現的藍點也常來自 Wi-Fi、基地台或上一次的位置，本輪沒讀來源；「可能」已經把這些可能性留下 |
| p177 | 難怪它有時候一下就出來（小問） | 正確 | — | 「有時候」對應「可能」 |
| p180 | 你剛剛就走在那兩排大樓中間，你說呢 | 正確 | — | 把問題交給小問 |
| p182–p183 | 剛剛那個撞牆的訊號，晚到一點點，就把我算到對街（小問） | 正確（附註） | ION 2015 摘要；Navipedia Multipath | ION 摘要："the accuracy in urban areas showed a remarkable correlation with building height … we are moved to propose a 'Law of Urban Multipath'"，把城市裡的誤差歸到多路徑，方向有據。附註：Navipedia 說碼的多路徑 "can reach up to 450 meters … although upper values more than 15 meters are difficult to observe. Typically, it is less than 2 or 3 meters"，能不能單靠一個反彈訊號偏到對街，來源沒有數字；這是小問自己的結論，所長只回「說得好」，沒有用數字撐它，可留。比起舊版（遮擋、反彈、時間合在一起說），現在只講反彈，少了 p105–p106 的放大倍數 |
| p184 | 說得好；還記得那支慢一秒的錶嗎 | 正確 | — | 接回 p077 |
| p185 | 最神奇的是：手機每次定位，都在幫自己對錶（所長意見） | 正確（意見已標明） | Navipedia SPS；FAA | 每次求解都把 "receiver clock offset δt" 當成未知數；FAA "the receiver uses four satellites to compute latitude, longitude, altitude, and time" |
| YouTube 說明（其餘） | 公園哨子遊戲；百萬分之一秒差三百公尺；相對論要先修好；手機沒有原子鐘，多聽第四顆算錶差；衛星送得很準，在大樓中間把藍點甩到對街的多半是大樓擋住和牆面反彈；網路省下等待卻得多找一顆衛星；畫圓圈是示意；AI 插圖 | 正確（除 G02） | 同上各列 | 「多半」用得好，正是 G01 要求台詞跟上的說法。第一輪 F05 的問題（把相對論和電離層說成「最後一段路」）已經改掉。另見選修 S3、S4 |

本輪順帶核對的歸屬（句子沒改或只改了前後文）：p026「美國氣象局說」（NWS 頁，正確）；p122「史丹佛的一門線上課」（ION 2015 摘要："This MOOC 'GPS: An Introduction to Satellite Navigation' was created by the authors for Stanford University, and is hosted by Coursera"，正確）；p171「一篇導航期刊的論文，引用這個方法發明人的估算」（Blay 2021 "on the order of 800 m (Van Diggelen, 2009)"，van Diggelen 正是這個方法的提出人，正確，已採用第一輪的 S3）。

## 三、撰稿者自己標成推論的四句

| 句子 | 結論 |
| --- | --- |
| p138「是整片天空慢慢變，不會在兩棟大樓之間突然跳」 | **公平的推論**。電離層的變化尺度是地理位置、時刻、太陽活動（Navipedia 原文），不是幾十公尺。沒有加保留詞，但在它說的尺度（兩棟大樓之間）站得住。可留 |
| p142「所以把你甩到對街的，不是天上那段路」 | **說過頭**（G01）。p138 只能排除「突然跳」，不能排除「偏」。單頻修正以後還剩約一半，對流層也沒有交代。加「多半」以後就是公平的結論，跟說明欄一致 |
| p117「到處都會偏，不會專挑大樓中間」 | **公平的推論**。GPS.gov 的 "on a global basis" 直接支持。只是假設語氣省略了「就算」，見選修 S1 |
| p176「可能就是這樣算出來的」 | **公平而且有保留**。「有些手機」（p174）加「可能」兩層保留，Blay 支持這個方法 "being widely used" |

## 建議修改

必改：

- G01 p142：所以把你甩到對街的，不是天上那段路。 → 所以把你甩到對街的，多半不是天上那段路。（20 字）
- G02 YouTube 說明：「高空的電離層也會拖慢訊號，但它整片天空一起變，大多修得掉；」 → 「高空的電離層也會拖慢訊號，但它是整片天空慢慢變，不會在大樓之間突然跳，而且修得掉一部分，同時聽兩個頻率幾乎全修掉；」

選修（不影響本輪結論）：

- S1 p117：而且訊號本身變差，到處都會偏，不會專挑大樓中間。 → 而且就算訊號變差，也是到處都偏，不會專挑大樓中間。（25 字）。原句接在「二〇〇〇年就停了」後面，可能被聽成訊號現在變差，跟 p109「衛星送得其實很準」打架。
- S2 p131：歐洲太空總署的導航教材說， → 歐洲太空總署發起的導航百科說，（15 字）。Navipedia 自稱 "an initiative of the European Space Agency … collaborative GNSS encyclopaedia"。原句的歸屬沒錯，可留。
- S3 YouTube 說明：「手機怎麼靠網路省下等待，卻得多找一顆衛星」→「手機怎麼靠網路省下等待，有些手機卻得多找一顆衛星」。片中 p174 說「有些手機」，Blay 也只說這個方法 "widely used"。
- S4 YouTube 說明開頭「藍點突然跳到對面那條街，過一下又跳回來」：目前片中 p004–p006 沒有「又跳回來」（p006 改成「重開地圖，藍點還等好久」）。這不是事實錯誤，但說明欄和片子對不上，可以改成「藍點突然跳到對面那條街，重開地圖還等好久」。
