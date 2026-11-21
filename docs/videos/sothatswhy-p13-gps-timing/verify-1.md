# 查核報告 1（sothatswhy-p13-gps-timing）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-11
- 方法：逐句讀 `video.json` 的 199 句台詞（p001–p199），加上 YouTube 標題、說明與縮圖文字（headline「藍點／跳到對街？」、sub「差百萬分之一秒，差三百公尺」）。對照 `claims.md` 的 C01–C22 當線索，但不採用它的引文，每個來源當天重新打開讀原文（curl GET，HTML 去標籤轉純文字後 grep 並讀上下文）：
  - GPS.gov 現行頁：〈GPS Accuracy〉node/70（200，53,877 bytes）、〈Frequently Asked Questions〉faq（200）、〈Space Segment〉（200）、〈Augmentation Systems〉（200）。另開典藏頁 archive.gps.gov〈GPS Accuracy〉（200，頁首 "have not been updated since February 2025"），只用來對照現行頁刪了哪些句子。
  - DoD《GPS SPS Performance Standard》第 5 版（2020 年 4 月）：curl 200（2,166,466 bytes），`pdftotext -layout` 讀 §2.2 與 Fig. 2.2-1、§3.4.1 Table 3.4-1 與 Notes、A.8.2、B.2.1、B.2.4.3.4、B.3、Glossary。
  - FAA〈Satellite Navigation - GPS - How It Works〉（200）。
  - ESA Navipedia：〈Code Based Positioning (SPS)〉oldid=12251、〈Multipath〉oldid=11617、〈Ionospheric Delay〉oldid=13741、〈Klobuchar Ionospheric Model〉oldid=16790、〈TTFF〉oldid=13355（皆 200）。
  - Blay, Wang & Akos 2021（NAVIGATION 68(1):217）：navi.ion.org 期刊 HTML 全文（200，226,281 bytes），讀 §1、§2、§2.1、§2.3。
  - Ashby 2003（Living Reviews in Relativity 6:1）：Europe PMC `fullTextXML`（PMC5253894，200，289,549 bytes），讀式 (35)–(36) 前後、Figure 2 說明、Rubidium 鐘一段、「factory frequency offset」一段。
  - van Diggelen & Enge 2015（ION GNSS+ 2015）：ion.org 摘要頁（200），**只有摘要**。
  - NOAA NWS〈Understanding Lightning: Thunder〉（200）、NIST CODATA 光速（200）。
  - 自己重算：4.4647×10⁻¹⁰ × 86,400 s = 38.575 µs；38.575 µs × 299,792,458 m/s = 11,564 m；10⁻⁶ s × c = 299.8 m；20,200 km ÷ c = 67.4 ms（正上方）；1 英里 1,609 m ÷ 5 s = 322 m/s，即每公里 3.1 秒。
- 打不開／沒讀到原文的：ION GNSS+ 2015 論文全文要付費，只讀摘要（4.9 m 的量法、是否限開闊天空、統計方式都沒讀到全文）；Blay 2021 的 800 m 引自 Van Diggelen 2009（《A-GPS》一書），原書沒有讀；IS-GPS-200 沒有試（片中沒依賴）。其餘來源都讀到原文。
- 結論統計（台詞 199 句）：正確 194、需改 5、錯誤 0。另外標題、說明、縮圖 3 項：正確 2、需改 1（說明）。另有 6 處選修建議（不影響結論，見文末）。
- 字數：下表建議句含標點計算（英文字母、空格各算一字），小問 ≤15、所長 ≤25。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p095–p096（所長） | 美國政府承諾，訊號本身的誤差，／九成五的時間在兩公尺以內。 | 需改（少了「全部衛星平均」的條件） | 2 公尺是**整個星座的平均**，不是每一顆衛星的訊號。GPS.gov node/70："the government commits to broadcasting the GPS signal in space with a daily global average user range error (URE) of ≤2.0 m (6.6 ft.), with 95% probability, across all healthy satellites in constellation slots." SPS PS Table 3.4-1 對**每一個**訊號的承諾是另一個數："7.0 m 95% Global Statistic URE during Normal Operations over all AODs … For any trackable and healthy SPS SIS"；2.0 m 那一列的條件是 "Across all trackable and healthy SPS SISs from satellites occupying constellation slots … for the ensemble of constellation slots"。原句讓人聽成手機收到的每一顆衛星訊號都在 2 公尺內 | p095：美國政府承諾，所有衛星平均，訊號本身的誤差，（22 字）；p096：九成五的時間在兩公尺以內。（13 字，照原句） |
| F02 | p126（所長） | 美國政府的 GPS 網站回答：沒有。 | 需改（把答案接到錯的問題上） | 小問問的是兩件事：「軍用的比較準」「給我們的比較爛」。GPS.gov 的「No.」回答的是 "Doesn't the Government Degrade Civilian GPS Accuracy? No. During the 1990s, GPS employed a feature called Selective Availability that intentionally degraded civilian accuracy … In May 2000 … ended its use"。另一題 "Is Military GPS More Accurate Than Civilian GPS?" 在現行頁**沒有**回答「沒有」，只說 "Using two GPS frequencies improves accuracy … With augmentation systems, civilian users can actually receive better GPS accuracy than the military."（典藏頁還有 "most of today's civilian devices use only one GPS frequency, while military receivers use two"）。單說「沒有」會被聽成「軍用並沒有比較準」，來源沒這樣說。p127–p129 本身正確 | 美國政府的 GPS 網站說：沒有故意把民用的弄差。（25 字；p127–p129 照留） |
| F03 | p138（所長） | 衛星的鐘一天大約快三十八微秒。 | 需改（四捨五入不對） | Ashby 2003 式 (35)："+2.5046 × 10⁻¹⁰ − 6.9693 × 10⁻¹⁰ = −4.4647 × 10⁻¹⁰. The negative sign in this result means that the standard clock in orbit is beating too fast"。4.4647×10⁻¹⁰ × 86,400 s = **38.58 µs**，四捨五入是 39，不是 38；「大約三十八」是捨去。p141 用「十一公里多」（11.56 km）已是「多」的說法，同一段宜一致。說法「照……換算」本身誠實（原文沒有寫 38 這個數） | 衛星的鐘一天快了三十八微秒多。（15 字；p139 小問「三十八微秒，」可照留） |
| F04 | p173（所長） | 時間每差一秒，量出的距離就錯大約八百公尺。 | 需改（錯的是「算出的」不是「量出的」；數字是二手引用） | Blay et al. 2021 §2.1："the problem is that the time is in error, so the normal four-state least squares algorithm can not solve … When [t] is incorrect, so is [the satellite position] and [the predicted range]. For each one second of error, the pseudoranges would be incorrect on the order of 800 m (Van Diggelen, 2009)."。手機量到的訊號沒有錯，錯的是用錯的時間**算出來**的衛星位置與預期距離（p171 自己也說「算出的衛星位置就錯」）。另外 800 m 是 Blay 引 Van Diggelen 2009 的書，不是 Blay 的量測；p172「論文回顧一個常用的方法」沒有說錯，但說清楚是引用更好（見選修 S3）。Blay §1 也確認那個方法 "is the one that is representative and is being widely used" | 時間每差一秒，算出的距離就錯大約八百公尺。（21 字） |
| F05 | YouTube 說明 | 衛星送得很準，誤差多半在最後一段路——大樓擋住、牆面反彈、高空的電離層，還有衛星時鐘要修的相對論 | 需改（把相對論與電離層歸成「最後一段路」） | 相對論是**衛星時鐘本身**的頻率偏移，在發射前或在廣播的鐘差修正裡就處理掉（Ashby："This adjustment is accomplished on the ground before the clock is placed in orbit."；Rubidium 鐘 "their frequencies are measured and the actual frequency corrections needed are incorporated in the clock correction polynomial that accompanies the navigation message"），不是訊號在路上的誤差，也不是藍點偏的原因。電離層在高空（Navipedia Klobuchar 模型假設 "concentrated in a thin layer at 350 kilometres in height"），不是「最後一段路」。片中也沒有說「最後一段路」；GPS.gov 只說 "URE is not user accuracy. User accuracy depends on a combination of satellite geometry, URE, and local factors such as signal blockage, atmospheric conditions, and receiver design" | 「衛星送得很準，藍點偏多半是訊號離開衛星以後的事——大樓擋住、牆面反彈、高空的電離層；另外，衛星時鐘還有一點相對論的差，一定要先修好；」其餘照留 |

## 二、逐段核對（正確的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p006 | 小問的藍點跳到對面那條街又跳回來 | 正確 | — | 小問的經驗，片中沒有用數字支持「對街」 |
| p007–p008 | 在大樓中間很常見；叫車時車停在對面 | 正確 | GPS.gov node/70 | "their accuracy worsens near buildings, bridges, and trees"；叫車是生活情境 |
| p009–p010 | 手機靠時間算位置；差百萬分之一秒距離差三百公尺 | 正確 | FAA；NIST | FAA "uses the time difference … to compute the distance, or range"；10⁻⁶ s × 299,792,458 m/s = 299.8 m。說「距離」不說「位置」，用詞準 |
| p011 | 差那麼遠？ | 正確 | — | 問句 |
| p012 | 手機要聽的衛星至少四顆 | 正確 | FAA | "a combination of signals from at least four satellites"；輔助 GPS 要五顆的情形在 p176 另外交代 |
| p013–p017 | 跟著這段路找答案；是不是手機問衛星（錯猜） | 正確 | — | 錯猜，p018 糾正 |
| p018–p022 | 衛星不知道你在哪；GPS 網站說衛星像燈塔一直往下廣播；手機只聽，自己算 | 正確 | GPS.gov faq；FAA | faq "the GPS satellites themselves do not track anything on the ground. They are simply beacons, like lighthouses, broadcasting one-way reference signals." 引用位置正確 |
| p023–p024 | 只用聽的？聽什麼？ | 正確 | — | 問句 |
| p025–p027 | 數閃電到打雷；氣象局說雷聲約五秒一英里，約三秒一公里 | 正確 | NWS | "it takes the sound of thunder about 5 seconds to travel a mile"；1,609 m ÷ 5 = 322 m/s，每公里 3.1 秒，「差不多三秒」恰當 |
| p028–p029 | 數到六秒就是兩公里 | 正確 | NWS（換算） | 6 ÷ 3.1 = 1.93 km（用 343 m/s 是 2.06 km），小孩的估算可留 |
| p030–p032 | 哨子遊戲：戴準錶的朋友整點吹哨；晚多久就知道多遠 | 正確（比喻） | FAA | 對應 "time difference between the time of signal reception and the broadcast time" |
| p033–p034 | 衛星帶原子鐘；訊號裡寫著發出的時間 | 正確 | FAA | "GPS satellites carry atomic clocks … The time information is placed in the codes broadcast by the satellite so that a receiver can continuously determine the time the signal was broadcast." |
| p035–p036 | 訊號要走多久 | 正確 | — | 問句 |
| p037–p038 | 大約兩萬公里高；通常六十到九十毫秒 | 正確 | GPS.gov Space Segment；Blay 2021 §2.3 | "at an altitude of approximately 20,200 km"；"the travel time from satellite to receiver is typically 60 to 90 milliseconds"。20,200 km ÷ c = 67 ms（正上方），斜向更遠，一致 |
| p039–p042 | 跟光一樣快，一秒約三十萬公里；三百公尺就是這樣來的 | 正確 | NIST；FAA | 299,792,458 m/s → 「大約三十萬公里」。真空值；大氣拖慢在 p115–p116 交代（FAA "propagation delays or decreases in the signal's speed caused by the ionosphere and the troposphere"） |
| p043–p045 | 差一點時間差那麼遠；今天的題目 | 正確 | — | 定性說法 |
| p046–p052 | 聽一顆只知道距離，一整圈；太空是一整顆球面；第二、第三個疊起來縮小範圍 | 正確（示意） | FAA；Navipedia SPS | FAA "With information about the ranges to three satellites … the receiver can compute its own three-dimensional position."；Navipedia "solving a geometric problem from the measured ranges" |
| p053 | 畫圓圈只是示意 | 正確 | Navipedia SPS | 明說示意，與 p074–p075 接收機實際做法呼應 |
| p054–p058 | 三顆夠，但條件是手上要有一顆跟 GPS 對好時間的原子鐘（FAA） | 正確 | FAA | "An atomic clock synchronized to GPS is required in order to compute ranges from these three signals." 引用位置正確 |
| p059–p061 | 手機裡有沒有原子鐘：沒有那麼準的鐘 | 正確（撰稿推論） | FAA | "by taking a measurement from a fourth satellite, the receiver avoids the need for an atomic clock"；片中沒給手機鐘的誤差數字 |
| p062–p064 | 錶慢一秒，每聲哨子都以為走得短，每個朋友近了三百多公尺 | 正確（比喻的算術） | NWS（換算） | 聲音約 322–343 m/s，「三百多公尺」對；錶慢→量到的延遲變短→以為較近，方向對 |
| p065–p067 | 大家一起變近；找不到一個點跟每個距離都對得上 | 正確 | — | 共同偏差下圓一般不交於一點 |
| p068–p071 | 多聽一個朋友，把錶差當成要算的答案；東西、南北、高低加錶差，四個未知數要四顆 | 正確 | FAA；Navipedia SPS | FAA "the receiver uses four satellites to compute latitude, longitude, altitude, and time."；Navipedia "the four unknown parameters: The receiver coordinates (x,y,z) and the receiver clock offset δt." 公園那段只說「多聽一個」，第四顆的四個未知數放在「換回衛星」，沒有混 |
| p072–p073 | 第四顆是來幫手機對錶的（小問） | 正確（簡化） | FAA | FAA 本身也這樣說："by taking a measurement from a fourth satellite, the receiver avoids the need for an atomic clock"。p074–p075 立刻補「四個答案一次算出來」，不會被聽成只有第四顆負責時鐘 |
| p074–p076 | 真的手機不是畫圓圈，四個答案一起算；超過四顆找跟大家最合得來的答案 | 正確（簡化） | Navipedia SPS | 線性化後解；"an over-dimensioned system is obtained (for n > 4), which can be solved using the Least Squares adjustment."。附註：「一次算出來」指同時求解，實際是在近似位置附近反覆修正，不影響 |
| p077–p080 | GPS 網站說基本排法二十四個位置，幾乎任何地方看得到至少四顆 | 正確 | GPS.gov Space Segment | "This 24-slot arrangement ensures users can view at least four satellites from virtually any point on the planet."；附註：同頁說現在實際是 "effectively operates as a 27-slot constellation"，片中說「基本排法」恰當 |
| p081–p082 | 同樣四顆每次都一樣準嗎 | 正確 | — | 問句 |
| p083–p084 | 官方性能標準：位置誤差大約是量距離的誤差乘上放大倍數 | 正確 | SPS PS B.2.1 | "Accuracy = UERE x DOP (B-1). Equation B-1 is a simple approximation that has been found adequate for many applications."「大約」保住了近似；「量距離的誤差」對應 UERE（含使用端的誤差），跟 p095 的「訊號本身的誤差」（URE）分開講，層次正確 |
| p085 | 倍數看衛星和你的相對位置好不好 | 正確 | SPS PS Glossary | "Dilution of Precision (DOP). The magnifying effect on GPS position error induced by mapping URE into a position solution … through the relative satellite-to-receiver geometry." |
| p086 | 位置太差甚至算不出來 | 正確 | SPS PS A.8.2 | "Without 'good geometry', it can sometimes be impossible for users to even determine a PVT solution." 「太差的時候」是條件，可留 |
| p087 | 五顆以上去算，倍數一定不會比四顆差 | 正確 | SPS PS B.2.4.3.4 | "Using five or more SISs for the PVT solution or time transfer solution always results in DOP values that are at least as good as the 4-SIS DOP values." |
| p088–p091 | 大樓擋住一部分衛星，能用的變少，倍數可能變大 | 正確（推論，已用「可能」） | GPS.gov node/70；SPS PS | "Satellite signal blockage due to buildings"；少用衛星 DOP 不會變好，推論成立 |
| p092–p094 | 是衛星訊號不準嗎（錯猜）；衛星送得其實很準 | 正確 | GPS.gov node/70 | "Actual performance is typically much better." |
| p095–p096 | 兩公尺承諾 | 見 F01 | — | — |
| p097 | 2021-04-20 實際量到的還不到六十五公分 | 正確（附註） | GPS.gov node/70 | "On April 20, 2021, the global average URE across all satellites was ≤0.643 m (2.1 ft.), 95% of the time."。0.643 m → 「不到六十五公分」對；也是全部衛星平均，採 F01 後同一個語境就交代了 |
| p098–p101 | 官方說訊號誤差不等於你手上的誤差；還要看排法、遮擋、大氣、手機 | 正確 | GPS.gov node/70 | "To be clear, URE is not user accuracy. User accuracy depends on a combination of satellite geometry, URE, and local factors such as signal blockage, atmospheric conditions, and receiver design features/quality." |
| p102–p103 | 史丹佛一門線上課，上千人在一百個國家用手機量；開闊的地方平均約五公尺 | 正確（附註） | ION 2015 摘要；GPS.gov node/70 | 摘要 "created by the authors for Stanford University"；"with over one thousand participants in one hundred countries, the measured mean accuracy, remarkably, came to 4.9 meters."；GPS.gov 把它寫成 "typically accurate to within a 4.9 m (16 ft.) radius under open sky"。附註：摘要只說這個實驗 "studied GNSS accuracy … both in the open and in urban environments"，4.9 m 是開闊處的平均是從上下文（"Open-sky GNSS accuracy … has often been claimed to be 'about 5 meters'"）與 GPS.gov 的轉述讀出來的，全文沒讀到；是 2014 年課程、當年的手機，片中沒說是現在的手機 |
| p104 | 城市裡誤差跟大樓高度關係很大 | 正確 | ION 2015 摘要 | "the accuracy in urban areas showed a remarkable correlation with building height" |
| p105–p110 | 有時擋住，有時撞牆反彈才進手機；繞遠路以為比較遠；叫多路徑 | 正確 | GPS.gov node/70；Navipedia Multipath | "Signals reflected off buildings or walls ("multipath")"；"when a signal arrives, by different ways, at the antenna"。反射路徑較長，量到的距離變長，方向對 |
| p111–p112 | 教材說主要因天線太靠近反射物；低處斜進來的衛星影響最大 | 正確 | Navipedia Multipath | "Its principal cause is the antenna closeness to the reflecting structures, and it is important when the signal comes from the satellite with low elevation."；圖 2 說明 "the largest multipath at the satellite rising and setting (i.e., due to the low elevation rays)"，「影響最大」有據 |
| p113–p116 | 訊號穿過電離層會被拖慢 | 正確 | Navipedia Ionospheric Delay；FAA | 碼量測 "suffer a positive delay"；FAA "decreases in the signal's speed caused by the ionosphere" |
| p117–p118 | 單頻接收機只能用模型猜；這個效應可以到幾十公尺 | 正確 | Navipedia Ionospheric Delay | "single frequency receivers have to apply an ionospheric prediction model to remove (as much as possible) this effect, that can reach up to several teens of meters"（原文 "teens" 應是 tens 的筆誤）。說的是效應本身，不是修正後的殘差，對 |
| p119 | 廣播的修正模型全世界平均大約修掉一半 | 正確（附註） | Navipedia Klobuchar | "is estimated to reduce about the 50% RMS ionospheric range error worldwide"。附註：原文是「估計」、以 RMS 計，「大約」可留 |
| p120–p123 | 拖慢多少跟頻率有關；雙頻比一比；可以去掉九成九以上 | 正確 | Navipedia Ionospheric Delay | "the GNSS signals refraction depends on its frequencies (as the squared inverse). This dependence on the signal frequency allows us to remove its effect up to more than 99.9% using two frequency measurements"；「九成九以上」比 99.9% 保守，沒說過頭。高低兩支哨子是示意（空氣中的聲音不會這樣），可留 |
| p124–p125 | 軍用比較準、給我們的比較爛（小問） | 正確 | — | 錯猜，見 F02 |
| p126 | GPS 網站回答：沒有 | 見 F02 | — | — |
| p127 | 以前故意讓民用變不準，二〇〇〇年停了 | 正確 | GPS.gov node/70 | "During the 1990s, GPS employed a feature called Selective Availability that intentionally degraded civilian accuracy … In May 2000 … ended its use of Selective Availability" |
| p128 | GPS 以外幫忙提高準確度的叫增強系統 | 正確 | GPS.gov Augmentation Systems | "A GPS augmentation is any system that aids GPS by providing accuracy, integrity, availability, or any other improvement … that is not inherently part of GPS itself." |
| p129 | 民用加上它甚至可以比軍用還準 | 正確 | GPS.gov node/70 | "With augmentation systems, civilian users can actually receive better GPS accuracy than the military." |
| p130–p132 | 衛星原子鐘會不會不準；會，相對論 | 正確（附註） | Ashby 2003 | Ashby 自己寫 "the standard clock in orbit is beating too fast"；見選修 S1 |
| p133–p135 | 高處地球拉得沒那麼用力，鐘走快；跑得快的鐘走慢；加起來還是快 | 正確（簡化） | Ashby 2003 | 式 (35) 正負號：+2.5046×10⁻¹⁰（速度）− 6.9693×10⁻¹⁰（重力位）= −4.4647×10⁻¹⁰，"beating too fast, primarily because its frequency is gravitationally blueshifted"；"for a GPS satellite clock, the gravitational blueshift is greater"。重力與速度的方向、合起來的正負都對；「拉得沒那麼用力」是重力位的口語說法 |
| p136–p137 | 快多少；照一篇相對論回顧換算 | 正確 | Ashby 2003 | 誠實標「換算」 |
| p138 | 一天大約快三十八微秒 | 見 F03 | — | — |
| p139–p142 | 很短吧；光在這段時間跑十一公里多；所以一定要修 | 正確 | Ashby 2003；NIST（換算） | 38.58 µs × c = 11.56 km，「十一公里多」對。沒有說「不修每天定位飄 11 公里」（接收機鐘差未知數會吸收共同偏差），措辭恰當 |
| p143–p144 | 有些鐘上去之前在地面調慢；有些上去後再量，把修正寫進廣播 | 正確 | Ashby 2003 | "This adjustment is accomplished on the ground before the clock is placed in orbit."；"the 'factory frequency offset', which is applied to GPS clocks before launch"；"It has become common practice not to apply such offsets to Rubidium clocks … after such clocks are placed in orbit their frequencies are measured and the actual frequency corrections needed are incorporated in the clock correction polynomial that accompanies the navigation message."（2003 年的說法） |
| p145–p148 | 剛開地圖為什麼要等；還要知道衛星在哪、鐘差多少 | 正確 | FAA；SPS PS Fig. 2.2-1 | FAA "The signal contains data that a receiver uses to compute the locations of the satellites"；Subframe 1 "Satellite Clock Correction Terms"、Subframe 2–3 "Ephemeris Parameters" |
| p149–p150 | 寫在廣播裡，講得很慢，一秒五十個位元 | 正確 | SPS PS §2.2 | "the LNAV data also clocked at 50 bps" |
| p151–p153 | 位元是最小的一格；朋友一個字一個字慢慢念 | 正確（一般定義＋比喻） | — | — |
| p154 | 一整輪三十秒，才從頭再講一次 | 正確 | SPS PS Fig. 2.2-1；Blay §2 | "Frame (30 sec repeat)"；"the 30 second navigation frame"。附註：曆書要 25 頁才輪完，片中講的是含位置與鐘差的那一框，可留 |
| p155 | 傳統接收機要把前三段聽完，最久約三十六秒 | 正確 | Blay 2021 §2 | "Conventional GNSS receivers need to receive the data from the first three subframes of the 30 second navigation frame … it can take as long as 36 seconds" |
| p156–p157 | 三十六秒我都走到對街了 | 正確 | — | 小孩的反應 |
| p158–p160 | 冷開機要把整片天空找一遍；手上已有精確衛星位置叫熱開機，不用再等廣播 | 正確（簡化） | Navipedia TTFF | "Cold start: … the receiver entails a full search of the sky for all satellites"；"Hot start: … the receiver has both accurate ephemeris and information on frequency offset as well as an accurate initial solution"；"in case the receiver already has a valid navigation message, it does not need to decode it"。沒講暖開機、熱開機還要初始位置與頻率偏差，簡化可留 |
| p161 | 大樓中間訊號斷斷續續，等待更久 | 正確（附註） | Navipedia TTFF | "in harsh environments, such as urban canyons, the signals may suffer interruptions or even obstruction blocking the TTFF process"。「訊號斷斷續續」是條件，推論成立 |
| p162–p163 | 我的手機一打開就有藍點 | 正確 | — | 小問的經驗；見選修 S4 |
| p164–p166 | 輔助 GPS：透過行動網路先拿到衛星位置和鐘差，只收幾毫秒訊號就能算位置 | 正確 | Blay 2021 §2 | "With the A-GNSS technique, receivers can solve for position with only milliseconds of IF data … the precise orbital and clock parameters, also known as the assistance data … For the mobile phone, this data is typically provided through the cellular network using the Secure User Plane Location (SUPL) protocol" |
| p167–p169 | 有人先傳訊息告訴你朋友站哪；有沒有缺點 | 正確（比喻） | — | — |
| p170–p171 | 沒從廣播讀到精確時間；衛星在動，時間錯一點，算出的衛星位置就錯 | 正確 | Blay 2021 §1、§2.1 | "most A-GNSS techniques aim to achieve a coarse time estimate"；"the time is in error … When [t] is incorrect, so is [the satellite position]" |
| p172 | 一篇導航期刊論文回顧一個常用的方法 | 正確（附註） | Blay 2021 §1 | "van Diggelen's technique … is the one that is representative and is being widely used"；見 F04、選修 S3 |
| p173 | 每差一秒距離錯約八百公尺 | 見 F04 | — | — |
| p174–p176 | 又是時間；手機把現在大概是哪一刻也當成答案；第五個未知數，要至少五顆 | 正確（附註） | Blay 2021 §2.1 | "Since there are now five columns of the H matrix, there now must be at least five satellites to solve for δx. Thus, a closed-form five-state solution has been developed to solve for the position without precise time."。附註：這是 p172「常用的方法」的做法，不是每支手機都一定這樣，見選修 S5 |
| p177–p180 | 導航帶錯路不一定是 GPS 錯；官方說很多時候硬體沒問題，錯的是地圖：路畫錯、店標錯、少了路 | 正確 | GPS.gov node/70 | "In many cases, a device's GPS hardware is working fine, but its mapping software is faulty. For example, users are often misled by: Incorrectly drawn maps; Mislabeled businesses and other points of interest; Missing roads, buildings, communities, etc." |
| p181–p188 | 小問總結：衛星像吹哨的朋友；聽訊號走多久；多聽一顆對錶；就知道在哪 | 正確 | 同 p030–p073 | 與已核說法一致 |
| p189–p192 | 大樓中間衛星被擋、訊號反彈、時間多算一點，藍點跳到對街 | 正確（附註） | GPS.gov node/70；ION 2015 摘要；Navipedia Multipath | 遮擋與反射是 GPS.gov 列的常見原因；ION 摘要說城市誤差與大樓高度高度相關（並提出 "Law of Urban Multipath"）。附註：Navipedia 說碼的多路徑 "Typically, it is less than 2 or 3 meters"、"upper values more than 15 meters are difficult to observe"；能不能偏到對街，來源沒有給數字，這是小問用自己的經驗收尾，片中沒有用數字撐它，可留 |
| p193–p194 | 所長意見：手機每次定位都在幫自己對錶 | 正確（意見已標明） | Navipedia SPS；FAA | 每次解算都把鐘差當未知數 |
| p195–p199 | 公園到了；留言題；訂閱 | 正確 | — | — |
| YouTube 標題 | GPS 差一點時間，位置怎麼差那麼遠？ | 正確 | 同 p009–p045 | 定性說法 |
| YouTube 說明 | 見 F05；其餘（哨子遊戲、百萬分之一秒三百公尺、第四顆衛星算錶差、網路省等待卻要多找一顆、藍點對了地圖畫錯、畫圓圈是示意、AI 插圖） | 需改（一處） | 同前 | 除 F05 那一句外與片中核過的說法一致；「畫圓圈找交點只是示意，真正的接收機是把位置和時間一起估算出來」交代得好 |
| 縮圖 | 藍點／跳到對街？／差百萬分之一秒，差三百公尺 | 正確（附註） | NIST；FAA | 10⁻⁶ s × c = 299.8 m。附註：sub 說的是距離（量距離）差三百公尺，片中 p010 也說「距離」；跟「跳到對街」放在一起可能被聽成藍點偏三百公尺，但字面沒錯，可留 |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| C11 「每日全球平均」「所有健康衛星」的限定省略 | 需改（F01）：SPS PS 對單一訊號的承諾是 7.0 m 95%，2.0 m 只對整個星座平均成立，省略會把平均說成每顆 |
| C15 只用現行頁兩句，不用典藏頁的軍民比較 | 方向對，但 p126「回答：沒有」把「是否故意弄差」的答案接到「軍用是否較準」上（F02） |
| C16 38 微秒、十一公里多 | 十一公里多正確；38.58 微秒說成「大約三十八」是捨去（F03）。正負號、重力與速度、發射前調慢與入軌後量測都對 |
| C20 800 m 歸屬 | Blay 引 Van Diggelen 2009，片中沒說成 Blay 的量測；但「量出的距離」應為「算出的距離」（F04） |
| C12 4.9 m 是否限開闊天空 | 摘要沒有明寫 4.9 m 是開闊處的值，靠上下文與 GPS.gov 轉述；全文付費沒讀，片中「開闊的地方」可留 |
| C14 雙頻去掉多少 | 正確。Navipedia "more than 99.9%"，片中「九成九以上」保守 |
| C10 被擋→倍數可能變大 | 正確，已用「可能」 |
| 其他：說明欄 | 需改（F05）：相對論與電離層不是「最後一段路」 |

## 建議修改

必改：

- F01 p095：美國政府承諾，訊號本身的誤差， → 美國政府承諾，所有衛星平均，訊號本身的誤差，（22 字；p096 照留）
- F02 p126：美國政府的 GPS 網站回答：沒有。 → 美國政府的 GPS 網站說：沒有故意把民用的弄差。（25 字）
- F03 p138：衛星的鐘一天大約快三十八微秒。 → 衛星的鐘一天快了三十八微秒多。（15 字）
- F04 p173：時間每差一秒，量出的距離就錯大約八百公尺。 → 時間每差一秒，算出的距離就錯大約八百公尺。（21 字）
- F05 YouTube 說明：「衛星送得很準，誤差多半在最後一段路——大樓擋住、牆面反彈、高空的電離層，還有衛星時鐘要修的相對論；」 → 「衛星送得很準，藍點偏多半是訊號離開衛星以後的事——大樓擋住、牆面反彈、高空的電離層；另外，衛星時鐘還有一點相對論的差，一定要先修好；」

選修（不影響本輪結論）：

- S1 p132：會，原因很有名：相對論。…… → 從地面看，它走得比地上快，原因很有名：相對論。（23 字；後半「我們只講需要修的那一點。」可併入下一句或刪）。鐘在自己的位置走得很準，是從地面看才快；Ashby 用 "beating too fast"，原句可留，但「會不準」容易被聽成鐘壞了。
- S2 p097：可加「全部衛星平均」以外不必再改；若 F01 不採用，至少在 p097 說「所有衛星平均」。
- S3 p172：一篇導航期刊的論文回顧一個常用的方法： → 一篇導航期刊的論文，引用這個方法發明人的估算：（23 字）。800 m 來自 Van Diggelen 2009，Blay 是轉引；原句沒說錯，改了歸屬更清楚。
- S4 p164：那是輔助 GPS。手機透過行動網路， → 那多半是輔助 GPS。手機透過行動網路，（20 字）。Blay 只說 A-GNSS 能 "reduce the time to first fix (TTFF) dramatically"；手機一打開就出現的藍點，也常來自 Wi-Fi／基地台定位或上一次的位置，這些本次沒有讀來源，所以只建議加「多半」，不列必改。
- S5 p175：所以手機把現在大概是哪一刻，也當成要算的答案。 → 所以有些手機，把現在大概是哪一刻也當成答案。（22 字）。Blay 說這方法 "representative and is being widely used"，不是每支手機都如此；p172 已說「一個常用的方法」，原句可留。
- S6 p119：全世界平均大約修掉一半 → 估計全世界平均大約修掉一半（Navipedia "is estimated to reduce about the 50% RMS"）；原句有「大約」，可留。
