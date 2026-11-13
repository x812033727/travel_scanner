# 查核報告 1（sothatswhy-p26-plane-window）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-13
- 方法：逐句讀 `video.json` 的 176 句台詞（p001–p176），加上 YouTube 標題、說明、標籤與縮圖文字（headline「飛機窗戶／為何圓角？」、sub「方角會讓力擠在一起」）。`claims.md` 的 C01–C29 只當線索，不採用它的引文；每個來源當天重新打開（curl GET，HTML 去掉 script／style 與標籤轉純文字後 grep 並讀上下文；PDF 用 `pdftotext -layout`）：
  - 美國 FAA《Pilot's Handbook of Aeronautical Knowledge》（FAA-H-8083-25）第 7 章（200，18,237,698 bytes），讀 Pressurized Aircraft 全節（p.7-34 到 7-36，含 Figure 7-41 標準大氣壓力表、名詞定義、壓差控制與 Decompression 開頭）。
  - FAA〈Lessons Learned from Transport Airplane Accidents: de Havilland DH-106 Comet 1〉（`.../accidents/G-ALYV`，200，151,954 bytes；頁尾 "Last updated: Tuesday, January 6, 2026"），讀全文：Accident Overview（Calcutta、Elba、Naples）、Fuselage Testing、Stress Concentrations at Window Corners、Material Cold-Work Properties、Accident Board Findings、Key Safety Issue(s)、Resulting Safety Initiatives、Airworthiness Directives、Lessons Learned。
  - M. E. Tuttle（University of Washington）〈Stress Concentrations〉講義（200，1,600,137 bytes），讀定義、Kirsch 圓孔解（含 x = a 處的應力）、有限板、Inglis 橢圓孔開頭。
  - DoITPoMS（University of Cambridge）〈Inglis and the crack tip stress idea〉（200，19,825 bytes），讀全頁。
  - UNSW Sydney 材料系 Crack theory 六頁（Introduction、Fatigue failure、Fracture mechanics、Fracture toughness、Brittle fracture、Ductile fracture，皆 200），各讀全頁正文（Fracture toughness 的公式是圖，只剩一句文字）。
  - P. A. Withey〈Fatigue failure of the de Havilland Comet I〉（Failure Analysis Case Studies II，轉載自 Engineering Failure Analysis 4(2) 147–154, 1997；IIT Madras 課程網址，200，199,329 bytes），讀全文（歷史背景、事故調查、ANALYSIS OF THE FAILURE、CONCLUSIONS）。
  - P. A. Withey〈The de Havilland Comet〉RAeS Hamburg 演講（2019-01-24，HAW Hamburg，200，3,489,479 bytes），讀摘要、Technical Detail、Accidents、RAE Investigation – Manufacturing Cracks、De Havilland Comet I（改裝）、Modern Analysis、Comet 4。
  - 14 CFR 25.571（eCFR renderer API，200，18,314 bytes），讀 (a) 全段。
  - Mark Vanhoenacker〈Why are there holes in airplane windows?〉Slate（2015-05-29，200，240,515 bytes），讀全文，並在原始 HTML 確認 GKN Aerospace 與作者身分的原句。
  - **另找的一手來源**：
    - 美國國家運輸安全委員會（NTSB）事故報告 AAR-19/03〈Left Engine Failure and Subsequent Depressurization, Southwest Airlines Flight 1380〉https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1903.pdf（200，6,920,369 bytes），讀 §1.7.1 Cabin Window 與註 69、70。這是三層窗、中層小洞、中層承壓的**一手來源**，可以取代或補強 Slate（見 F01）。
    - 14 CFR 25.775 Windshields and windows（eCFR renderer API，200，6,290 bytes），讀 (d)。
    - Boeing〈787 Dreamliner by design〉https://www.boeing.com/commercial/787/by-design（200，288,299 bytes），讀 composites 與 cabin altitude 兩段（F06、p030 的旁證）。
- 打不開／找不到的：FAA《Aviation Maintenance Technician Handbook—Airframe》講機身開口補強的段落，本輪搜尋只找到書目，沒有找到可讀的現行 PDF 段落；但片中只講彗星號自己的「窗戶周圍金屬加厚」，Withey 1997 這篇同儕審查論文就有原句（見 p149），比 2019 演講投影片更好，不必再找。FAA AC 20-107B 的猜測網址 404，未使用。
- 結論統計（台詞 176 句）：**正確 170、需改 6、錯誤 0**。另外標題、說明、標籤、縮圖 4 項：**正確 3、需改 1（說明欄）**。另有 9 處選修建議（不影響結論，見文末）。
- 彗星號：全部掛在 FAA 教材與 Withey 名下，篇幅短（p108–p132、p148–p151），不講人數、不畫事故；p119 只說「這一架的結論」，符合 RAE 對拿坡里那架 "unable to form a definite opinion"；p124 小問「都是方窗害的」由 p125–p132 推翻，Withey 的說法標成「那位學者認為……可能」，FAA 的方窗角應力集中（p062–p065）也保留，沒有單一原因結論；全片與說明欄都**沒有**「業界因此改用圓窗」，只說彗星號自己後來的改法（p149–p151，FAA 原文只講 Comet 1XB）。沒有找到與 FAA 矛盾的句子。
- 安全面：紙條與迴紋針都是無害的桌上示範，沒有任何一句鼓勵碰飛機窗戶或在機上做實驗；p050–p051「外層壞了中層接手」不會嚇到小孩，NTSB 也證實 737 有 33 次外層破裂都由中層承壓。
- 字數：下表建議句含標點計算，小問 ≤15、所長 ≤25；建議句不含拉丁字母。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p045（所長） | 會。一位機長寫的文章，問過做飛機窗戶的公司： | 需改（作者身分說得比來源多） | Slate 全文只有 "You're an airline pilot, they say."；沒有任何地方說他是 captain（機長）。`claims.md` C08 自己也寫「作者在文中自稱 airline pilot」，台詞卻寫成「機長」。「做飛機窗戶的公司」照原文 "Marlowe Moncur, director of technology for GKN Aerospace, a leading passenger cabin window manufacturer" 沒問題。**一手來源**：NTSB AAR-19/03 §1.7.1："The window components also included an acrylic outer pane, an acrylic middle pane, and a silicon rubber seal between the panes. The outer and middle panes are structural components that carry the applied pressure load. Another window component, the inner pane, does not provide any pressurization capability."；註 69 "The middle pane has a vent hole, which relieves pressure between the outer and middle panes and allows the venting of moisture."；"there were 33 outer pane fracture events in the 737 fleet and 16 such events in the 757 fleet … in all of these cases, the middle pane carried the applied pressure load."　法規 14 CFR 25.775(d)："The windshield and window panels must be capable of withstanding the maximum cabin pressure differential loads … after any single failure in the installation"。p046–p051 的內容因此有一手根據，可以照留；建議 `claims.md` C08 把 NTSB 與 25.775(d) 加為主要來源（NTSB 講的是 737／757 的窗，片中用「通常」，可以） | 一位民航機飛行員寫的文章，問過做飛機窗戶的公司：（24 字；保留開頭「會。」會變成 26 字，超過上限，所以刪掉，p044 的問句不靠它也接得上） |
| F02 | p073（所長） | 洞邊的應力，大約是遠處的三倍。 | 需改（把最大值說成整圈洞邊） | Tuttle："Stresses at the edge of the hole (at x = a): σθθ = σyy = 3σo"；"The stress concentration factor for a circular hole in an infinite plate: Kt = σyy/σo = 3"。三倍只在與拉力垂直的那兩側（x = a）；同一解在順著拉力方向的洞邊應力並不大。片中「洞邊的應力」聽起來像整圈都是三倍。Withey 1997 也只說 "The stress around a cut-out was shown to be over 3 times the remote stress"，用的是最大值的意思。改成「最大的地方」就和講義一致 | 洞邊應力最大的地方，大約是遠處的三倍。（19 字） |
| F03 | p169（小問） | 力就不會擠在角上！ | 需改（小孩的總結把「比較不擠」說成「不擠」，和 p071–p073 打架） | p071–p073 剛說圓洞「也會」擠，洞邊最大約三倍；p134 所長也只說「力不那麼擠」；FAA 原文是 "flows freely around the curved edges with minimal build up"（很少，不是沒有）。p168–p169 是全片的帶走句，小孩會記成「剪圓就沒事」 | 力就沒那麼擠！（7 字） |
| F04 | p056（所長） | 洞那裡沒有金屬，推力只好繞過去。 | 需改（主詞會讓小孩以為「空氣」繞過窗戶） | 「推力」在 p034–p035 是空氣把機身往外推；p048–p049 才說窗戶最外層撐住裡外的壓差，所以空氣的推力其實落在窗戶上。繞過開口的是機身金屬裡的力：FAA "the stress flows freely around the curved edges"；UNSW〈Fracture mechanics〉"The stress cannot be transferred through the crack, and therefore stress is concentrated at either side of the crack."。`claims.md` C10 也承認「推力」接空氣推力、進機身後才改說「力」，但台詞裡這個轉換沒有說出來。機身被撐開時蒙皮受拉，用「拉力」也接得上 p080 的拉紙條 | 洞那裡沒有金屬，機身裡的拉力只好繞過去。（20 字） |
| F05 | p008（所長） | 我這裡有兩條硬紙，一條剪方洞，一條剪圓洞。 | 需改（示範沒有實測，條件也沒講清楚，小孩照做可能得到相反結果） | `claims.md` 文首與 C15 都寫明 p080–p081「方洞那條從角裂開」是**沒有實測**的撰稿示範；依據只有 UNSW 玻璃棒 "Observe how the fracture originates from the notch" 與 Tuttle 的角落應力集中。若小孩在家把圓洞剪得比方洞大、或紙條寬度不同，剩下的紙比較窄的那條會先破，就會學到「圓洞比較容易破」。至少要讓兩個洞一樣寬、紙條一樣寬；開拍前請照這個條件實拉幾次並記錄，結果不同就改 p080–p083 與 `strips-pull` 的提示詞 | 我這裡有兩條硬紙，一條剪方洞，一條剪一樣寬的圓洞。（25 字） |
| F06 | p019（所長） | 就是飛機那一整條長長的身體，外面包著金屬。 | 需改（不是每一種客機都這樣） | Boeing〈787 by design〉："With an airframe composed of about 50% composites by weight, the 787 weighs less than traditional metal airplanes"。小問明天要搭的飛機可能就是 787 或 A350 這種複合材料機身。本集講的是金屬疲勞，說「多半」就夠，不必展開複合材料；p084 小問「真的飛機是金屬」是小孩的話，改了 p019 之後可留 | 就是飛機那一整條長長的身體，外面多半包著金屬。（23 字） |
| F07 | YouTube 說明欄 | 美國聯邦航空總署整理的彗星號例子裡，調查的結論是加壓機艙因為金屬疲勞而壞掉； | 需改（說明欄把兩架合在一起，片中刻意只說「這一架」） | FAA 引 RAE："We have formed the opinion that the accident at Elba was caused by structural failure of the pressure cabin, brought about by fatigue. … we are unable to form a definite opinion on the cause of the accident near Naples"。片中 p119 用「這一架的結論是」守住了；說明欄前文沒有交代是哪一架，讀起來像兩架都有確定結論 | 美國聯邦航空總署整理的彗星號例子裡，調查對厄爾巴島外海那一架的結論，是加壓機艙因為金屬疲勞而壞掉； |

## 二、逐段核對（正確的句子與依據）

### 開場：紙飛機與三個鉤子（p001–p019）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p005 | 紙飛機從方窗的角裂開 | 正確（故事） | — | 故事設定，p080–p083 回收 |
| p006–p007 | 客機座位旁的窗戶四個角都是圓的 | 正確 | FAA Comet | "the round/oval shapes of modern airplane windows" |
| p008–p009 | 兩條硬紙，方洞與圓洞，哪條先破 | 需改（F05） | — | 見表一 |
| p010–p011 | 迴紋針彎一下沒事，彎很多次呢 | 正確（常識） | — | 鉤子，p086–p095 回答 |
| p012–p015 | 飛高後窗外與窗內有很大的不同；為什麼做成圓角 | 正確 | — | 問句與鉤子 |
| p016–p017 | 圓的才不會刮手（錯猜）；答案在窗戶旁邊的機身 | 正確 | FAA Comet | 錯猜由所長推翻；FAA 講的就是窗角周圍的機身應力 |
| p018–p019 | 機身是長長的身體，外面包著金屬 | 需改（F06） | Boeing | 見表一 |

### 加壓與壓差（p020–p043）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p020–p021 | 航空總署手冊說飛得高比較省油、能飛在暴風雨上面 | 正確（簡化） | PHAK p.7-34 | "consumes less fuel for a given airspeed … more efficient at a high altitude"；"bad weather and turbulence may be avoided by flying in relatively smooth air above the storms" |
| p022–p024 | 很稀；約八千五百公尺，空氣壓力只剩地面三分之一左右 | 正確 | PHAK Fig. 7-41 | "Sea level 14.7"、"28,000 4.8"；28,000 ft × 0.3048 = 8,534 m；4.8 ÷ 14.7 = 0.327。標準大氣，片中掛在「手冊說」下面 |
| p025–p028 | 會喘不過氣嗎；不會，機艙封起來、一直打進空氣，比外面多，叫加壓 | 正確（簡化） | PHAK p.7-34 | "sealed unit capable of containing air under a pressure higher than outside atmospheric pressure"；"allows for a constant inflow of air"；"necessary in order to protect occupants against hypoxia"。「空氣比外面多」是壓力較高的白話 |
| p029–p030 | 通常讓機艙像大約兩千四百公尺的山上，人待著比較舒服 | 正確 | PHAK p.7-35；Boeing | "typically maintains a cabin pressure altitude of approximately 8,000 feet at the maximum designed cruising altitude"；"comfortably and safely … particularly if the cabin altitude is maintained at 8,000 feet or below"。8,000 ft = 2,438 m。Boeing 787 頁 "6,000-feet (2,000 feet lower than conventional jets)" 也印證「通常」約 8,000 ft |
| p031–p035 | 氣球比喻；裡面的空氣把機身往外推；裡外推力的差叫壓差 | 正確（比喻） | PHAK p.7-35 | "Differential pressure—the difference in pressure between the pressure acting on one side of a wall and … the other side … the difference between cabin pressure and atmospheric pressure"。「推力的差」對八歲可以（嚴格說是壓力差） |
| p036–p037 | 氣球吹太多會破；所以機艙不會加到跟地面一樣 | 正確（撰稿推論，有據） | PHAK p.7-35、7-36 | "the fuselage is designed to withstand a particular maximum cabin differential pressure"；巡航時艙壓約 8,000 ft 就是結果。見選修 S4 |
| p038–p039 | 手冊說機身設計時定好最多撐多大的壓差，加壓不能超過 | 正確 | PHAK p.7-35 | "Differential control is used to prevent the maximum differential pressure, for which the fuselage was designed, from being exceeded." |
| p040–p043 | 每次飛都推；上去撐一下、落地前放掉鬆回來 | 正確（簡化） | FAA Comet | 水槽 "cycled to simulate many flights"；FAA 把一次加壓循環當一趟飛行（"1,290 pressurized flights"）。「落地前把壓放掉」是循環的白話 |

### 窗戶本身與機身開口（p044–p057）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p044–p045 | 窗戶也被推；一位機長寫的文章問過做窗戶的公司 | 需改（F01） | Slate；NTSB | 見表一 |
| p046–p047 | 客機窗戶通常有三層；中間那層有小洞 | 正確 | Slate；NTSB AAR-19/03 | Slate "you'll see three panes, typically made of acrylic"；NTSB "outer pane, an acrylic middle pane … the inner pane"、註 69 "The middle pane has a vent hole" |
| p048–p049 | 小洞讓夾縫和機艙等壓，平常最外層撐住壓差 | 正確 | Slate（GKN 技術總監）；NTSB | "allow pressure to equilibrate between the passenger cabin and the air gap … applied to only the outer pane"；NTSB "relieves pressure between the outer and middle panes" |
| p050–p051 | 外層壞了，中間那層也撐得住、來接手 | 正確 | Slate；NTSB；14 CFR 25.775(d) | "Both the middle and the outer panes are strong enough to withstand the difference on their own"；"the middle pane takes over"；NTSB 33＋16 次外層破裂 "in all of these cases, the middle pane carried the applied pressure load"；25.775(d) 要求單一失效後仍撐得住 |
| p052–p054 | 手冊說機身能撐多大壓差，看它多強，也常看窗戶和門 | 正確（保留 often） | PHAK p.7-36 | "This differential pressure is determined by the structural strength of the cabin and often by the relationship of the cabin size to the probable areas of rupture, such as window areas and doors." |
| p055 | 窗戶和門都是機身上開的洞 | 正確（常識） | — | — |
| p056 | 洞那裡沒有金屬，推力只好繞過去 | 需改（F04） | FAA Comet；UNSW | 見表一 |
| p057 | 繞過去？怎麼繞 | 正確 | — | 問句 |

### 小溪比喻與應力集中（p058–p083）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p058–p061 | 小溪繞過圓石頭滑過去；方水泥塊的角水擠成一團 | 正確（比喻） | FAA Comet | 見文末「小溪比喻的限度」與選修 S2 |
| p062–p063 | 航空總署說機身裡的力也有點像這樣；圓角讓力順著邊走、不太會堆起來 | 正確 | FAA Comet | "With modern windows, the stress flows freely around the curved edges with minimal build up."「有點像」守住比喻 |
| p064–p065 | 方窗的尖角，力轉不過去，擠在角上 | 正確（簡化） | FAA Comet | "stress cannot smoothly flow around the abrupt corners. This creates stress concentrations."（「轉不過去」略強，見選修 S3） |
| p066–p068 | 角上那一小塊金屬撐的力比旁邊多很多；叫應力集中 | 正確 | FAA Comet；Tuttle | "a very localized area of much higher stress than the surrounding area"；"an area in a object where stress increases over a very short distance" |
| p069–p070 | 應力就是金屬裡每一小塊撐著的力 | 正確（簡化） | — | 嚴格定義是單位面積上的內力；給八歲可以 |
| p071–p072 | 圓洞也會擠；大學講義說一大片被拉的薄板開圓洞 | 正確 | Tuttle | Kirsch "a circular hole in an isotropic 'infinitely large' thin plate" |
| p073 | 洞邊的應力約是遠處三倍 | 需改（F02） | Tuttle | 見表一 |
| p074–p075 | 劍橋大學的教材說，裂縫越尖，尖端的應力就大得多 | 正確 | DoITPoMS | "σt = σ(1 + 2c/b) … For a sharp crack, i.e. c >> b, the stress would be much greater at the crack tip" |
| p076 | 角越尖，力就擠得越厲害 | 正確（撰稿推論，有據） | DoITPoMS；FAA Comet | 從 Inglis 橢圓（c/b 越大越尖）推到轉角，方向與 FAA 的 abrupt corners 一致；沒有給倍數 |
| p077–p079 | 講義說洞、轉角、溝槽、裂縫旁邊常常這樣 | 正確 | Tuttle | "Stress concentrations typically occur due to some localized change in geometry (near holes, filets, corners, grooves, cracks, etc)" |
| p080–p083 | 拉紙條，方洞那條從角裂開；你剪的方角就是力最擠的地方 | 正確（示範，未實測） | UNSW 玻璃棒；Tuttle | 方向合理，但條件與實測見 F05 |

### 金屬疲勞與裂縫（p084–p106）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p084–p086 | 真的飛機是金屬，會被撐壞嗎；撐一次不會 | 正確 | PHAK p.7-36 | 機身設計就是要撐住最大壓差；p084 是小孩的話（F06 改後即可） |
| p087–p088 | 迴紋針扳來扳去就斷 | 正確（常識示範，安全） | — | 所長在 p095 說明與機身不同 |
| p089–p090 | 一次又一次地拉，就算每次都不大，最後也可能裂開，叫金屬疲勞 | 正確 | UNSW Fatigue | "fail after a large number of applications of the stress even though the cyclic stress that is applied is below their yield strength. This mode of failure is termed fatigue."「可能」守住 |
| p091–p092 | 金屬也會累；那是比喻；澳洲一所大學的材料教材說 | 正確 | UNSW | UNSW Sydney School of Materials Science and Engineering |
| p093–p094 | 裂縫常常先從表面冒出一點點，每拉一次往前長一點 | 正確（簡化） | UNSW Fatigue | "Initially, a crack is nucleated, usually at the surface"；"progressive stepwise crack growth"；"Repeated cyclic stresses propagate the crack" |
| p095 | 機身每次被撐，不會像迴紋針那樣被扳彎 | 正確 | UNSW Fatigue | below yield strength 的白話；PHAK 的設計壓差上限 |
| p096–p097 | 飛好多趟；飛一趟就是撐一下再鬆一下 | 正確 | FAA Comet | 同 p040–p043 |
| p098–p100 | 裂縫從哪裡開始；哪裡的力最擠；窗戶的角 | 正確 | FAA Comet | "Production airplanes … were found to form fatigue cracks near the corners of the windows at approximately 1,000 airplane flight cycles" |
| p101 | 教材說疲勞的裂縫，從應力集中的地方長起來 | 正確（引文對；語境見選修 S1） | UNSW Introduction | "In both fast fracture and fatigue, crack growth occurs from the presence of stress concentrations where there is a localised build up of stress around the crack tip." |
| p102–p104 | 裂縫短時撐得住，長到某個長度會突然很快地裂過去 | 正確 | UNSW Fatigue、Introduction | "the crack propagates over time until a critical crack length is reached. Finally … the material undergoes fast fracture"；"suddenly becomes unstable and grows rapidly" |
| p105–p106 | 什麼時候快裂，看裂縫多長、拉得多用力 | 正確 | UNSW Fracture mechanics | "for a given applied stress, there is a crack size at which the crack will propagate"；材料（Kc）在 p138 補上 |

### 彗星號（p107–p132）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p107–p109 | 航空總署整理過彗星號；世界上第一種載客的加壓噴射客機 | 正確 | FAA Comet | "became the world's first pressurized civilian jet transport with its inaugural flight on May 2, 1952" |
| p110 | 一九五四年有兩架在飛行中出事 | 正確 | FAA Comet | Elba 1954-01-10、Naples 1954-04-08；不講人數，1953 加爾各答（官方原因是雷雨）不提，正確 |
| p111–p113 | 調查的人把另一架放進大水槽，往機艙灌水加壓，一次又一次像一趟趟飛行 | 正確 | FAA Comet | "a water tank was constructed to encase the fuselage … additional water was pumped into the cabin until the pressure inside the fuselage reached 1P, the equivalent of flight. This was then cycled to simulate many flights" |
| p114–p116 | 加上以前真的飛過的共三千多次，從方方的艙口窗的角裂開 | 正確 | FAA Comet；Withey 1997 | "G-ALYU had undergone 1,230 pressurized flights before testing and 1,830 tank 'flights' before the fuselage failed at the corner of a squarish forward escape hatch window"；"about 3,060"。Withey 寫 3057（1221＋1836），"from a rivet hole near the forward port escape hatch"；兩者都是「三千多次」、開口角附近 |
| p117–p118 | 海裡撈回的那架，最先裂在機頂兩個方方的天線窗那裡 | 正確 | FAA Comet；Withey 1997 | "ADF windows, also squarish … on the very top of the fuselage … determined to be the first fracture of the Elba crash"；MTCA "in the region of the A.D.F. window"；Withey "near the starboard rear corner of the rear ADF window … emanated from a 10mm diameter bolthole"（「那裡」涵蓋得到；見選修 S5） |
| p119 | 這一架的結論：加壓機艙因金屬疲勞壞掉 | 正確 | FAA Comet | RAE "the accident at Elba was caused by structural failure of the pressure cabin, brought about by fatigue"；只說「這一架」，與 Naples "unable to form a definite opinion" 不衝突 |
| p120–p123 | 航空總署說公司拿一個機身測過一萬六千次；之前被加過兩倍壓力，角上的金屬變了，次數太樂觀 | 正確 | FAA Comet | "De Havilland tested their prototype to 2P, twice the expected operating pressure … great enough to change the material characteristics at these locations"；"withstood 16,000 cycles … would mask the true fatigue vulnerability"。Withey 1997 寫的是前段艙段 18,000 次；片中掛在「航空總署說」下面，照 FAA 可以 |
| p124–p126 | 都是方窗害的？沒那麼簡單；英國學者研究，裂縫都從開口旁邊的鉚釘孔、螺栓孔長出來 | 正確 | Withey 1997 | "All the observed cracks in the pressure cabin [1, 2] emanated from bolt or rivet holes near the cut-out areas"；"none of the cracks in the body or wings of the test Comet emanated from the cut-outs directly"。Withey 署名 School of Metallurgy and Materials, The University of Birmingham，「英國學者」對 |
| p127–p130 | 鉚釘是什麼；釘的孔也是洞；講義說的洞，力也擠在旁邊 | 正確 | Tuttle | "near holes" |
| p131–p132 | 那位學者認為窗戶怎麼固定，可能比形狀還要緊；形狀、孔和做法連在一起 | 正確（有 hedge） | Withey 1997 | "It was probably not the shape of the cut-outs that was so damaging …, rather the method of fixing the windows and doubler plates"；"Had the windows not been square then the 'Redux' glueing method might have been applied to these areas, and the failure avoided."「認為」「可能」照原文的 probably |

### 圓角的意義、材料、改法與現代設計（p133–p164）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p133–p134 | 角圓了，力不那麼擠，裂縫比較難冒出來 | 正確（撰稿推論，有據） | FAA Comet；UNSW | 圓邊 "minimal build up" ＋ 裂縫從應力集中處長 |
| p135–p137 | 航空總署的教訓：要顧的不只形狀；材料、厚度、形狀、受力多大、怎麼保養 | 正確 | FAA Comet Lessons Learned | "Detailed attention must be paid to aspects such as material choice, thickness, geometry, stress levels, maintenance, and usage."（usage 未念，可以） |
| p138–p140 | 澳洲大學的教材比過銅棒與玻璃棒，都刻了小缺口 | 正確 | UNSW Brittle／Ductile | 兩頁各一根有缺口的棒 |
| p141–p143 | 玻璃棒有缺口，很小的力就斷，裂口從缺口開始 | 正確（略強，見選修 S6） | UNSW Brittle | "the force required to cause fracture is greatly reduced, and the rod breaks. Observe how the fracture originates from the notch." |
| p144–p145 | 銅棒有缺口卻先彎，沒有比較容易斷 | 正確 | UNSW Ductile | "the rod plastically deforms and the notch does not decrease the force required to break the rod" |
| p146–p147 | 銅斷前先變形、吸收很多力氣；只是這兩根的比較 | 正確（簡化） | UNSW Ductile | "a lot of plastic deformation, and significant energy is absorbed before the fracture"；p147 的界線很好 |
| p148–p149 | 那位學者整理過：窗戶周圍的金屬加厚 | 正確 | Withey 1997；Withey 2019 | 1997 "de Havilland subsequently redesigned the windows and increased the thickness of the skin in these areas"（同儕審查論文，比演講投影片好，建議 `claims.md` C25 補上）；2019 "Thicker skin around the windows" |
| p150 | 後來的新型號換了窗戶的設計，少打鉚釘 | 正確 | Withey 2019 | "The Comet flew again as the Comet IV – Different window design to reduce riveting – Fewer manufacturing cracks" |
| p151 | 航空總署說有一款改良型窗戶改成橢圓形 | 正確 | FAA Comet | "It wasn't until the next model, the Comet 1XB, that the window shape was changed from squarish to the now-conventional oval shape."只講彗星號，不說全業界改圓窗 |
| p152–p156 | 現在的設計先想好萬一裂了；讓力有別條路走，裂縫能停下或轉向 | 正確（合併說法可接受） | FAA Comet | "In fail-safe design, a critical part has redundancies, alternate load paths, and provisions for cracks to be stopped and turned … Today, both … have evolved into 'damage tolerant' standards, which integrates attributes of each approach"；「小溪分成好幾條」所長答「有點像」 |
| p157–p160 | 美國法規要求證明在能用年限裡不會因疲勞出大事，製造瑕疵也要算 | 正確 | 14 CFR 25.571(a) | "An evaluation of the strength, detail design, and fabrication must show that catastrophic failure due to fatigue, corrosion, manufacturing defects, or accidental damage, will be avoided throughout the operational life of the airplane." |
| p161–p163 | 還要訂好檢查讓維修的人照著做；像看牙醫，有點像 | 正確 | 14 CFR 25.571(a)(3) | "inspections or other procedures must be established … included in the Airworthiness Limitations section of the Instructions for Continued Airworthiness" |
| p164 | 圓角窗是很多設計裡的一個 | 正確 | FAA Comet Lessons Learned | 同 p136 |

### 收尾（p165–p176）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p165–p168 | 紙飛機要怎麼剪；原來如此；窗戶的角剪圓圓的 | 正確 | — | 小孩的結論 |
| p169 | 力就不會擠在角上 | 需改（F03） | Tuttle；FAA | 見表一 |
| p170 | 真的飛機還要常常檢查 | 正確 | 14 CFR 25.571(a)(3) | 同 p161 |
| p171–p172 | 我覺得最妙：小小的圓角背後是一整套設計和檢查 | 正確（標成意見） | FAA；25.571 | — |
| p173–p176 | 明天坐窗邊看圓角；留言；訂閱 | 正確 | — | 只是看一看，不是實驗 |

### 標題、說明、標籤、縮圖

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「飛機窗戶的圓角，怎麼改變機身受力？｜原來如此事務所」 | 正確 | 問句，片中有回答 |
| 說明欄 | 需改一處（F07）；其餘正確 | 加壓、撐一下鬆一下、力繞過洞、小溪、應力集中、金屬疲勞、Withey 的鉚釘孔與「不能只怪窗角」、材料厚度做法與檢查，逐句對得上上面的來源；「AI 生成的示意插圖，不是照片，也不是應力分析的結果」「沒有畫事故畫面」都對。「去找外婆」「用硬紙捲」片中沒說（選修 S8） |
| 標籤 | 正確 | 都是主題詞；「彗星號」台灣也通 |
| 縮圖「飛機窗戶／為何圓角？」「方角會讓力擠在一起」 | 正確 | FAA "stress cannot smoothly flow around the abrupt corners. This creates stress concentrations." |

### 小溪比喻（C28）與兩個桌上示範的限度

- **小溪**：只示意兩件事——開口讓力繞路（p058–p059）、圓邊順而尖角擠（p060–p065），而且所長在 p062 說「也有點像這樣」，依據是 FAA 自己用的 "flows freely around the curved edges／cannot smoothly flow around the abrupt corners"。工程上把應力線比作流線也是常見的教學類比；圓柱繞流與 Kirsch 圓孔的最大值都在兩側，不會教錯。限度：小孩可能把「擠成一團」想成水堆在角上停住；應力在角上是「線擠得很密」而不是停住。建議插圖畫成角上水流變急、起小漩渦（`brief.md` 已寫「角上起白色小漩渦」），台詞見選修 S2。p155「小溪分成好幾條」對應 alternate load paths，所長「有點像」，可留。
- **紙條（p008–p009、p080–p083）**：方向和來源一致，但沒有實測，且台詞沒有要求兩個洞一樣大，見 F05。紙是纖維材料，片中只用它說「裂口從力最擠的角開始」，沒有說紙等於金屬，可以。
- **迴紋針（p010–p011、p086–p095）**：迴紋針是被扳到彎曲變形、幾次就斷，比機身嚴重得多；所長在 p089「就算每次都不大」與 p095「機身不會像迴紋針那樣被扳彎」把差別講清楚了，不會誤導。小孩在家扳迴紋針沒有安全問題。
- **台灣用語**：聯邦航空總署、加壓、壓差、應力集中、金屬疲勞、鉚釘、螺栓、迴紋針、噴射客機、橢圓形、講義，都是台灣慣用說法；建議句「民航機飛行員」也是台灣用法。

## 建議修改

必改：

1. F01 p045（所長）：「會。一位機長寫的文章，問過做飛機窗戶的公司：」 → 「一位民航機飛行員寫的文章，問過做飛機窗戶的公司：」（24 字；「會。」可以刪，或者移到前一個節拍）
2. F02 p073（所長）：「洞邊的應力，大約是遠處的三倍。」 → 「洞邊應力最大的地方，大約是遠處的三倍。」（19 字）
3. F03 p169（小問）：「力就不會擠在角上！」 → 「力就沒那麼擠！」（7 字）
4. F04 p056（所長）：「洞那裡沒有金屬，推力只好繞過去。」 → 「洞那裡沒有金屬，機身裡的拉力只好繞過去。」（20 字）
5. F05 p008（所長）：「我這裡有兩條硬紙，一條剪方洞，一條剪圓洞。」 → 「我這裡有兩條硬紙，一條剪方洞，一條剪一樣寬的圓洞。」（25 字）；開拍前照這個條件實拉幾次並記錄，結果不同就改 p080–p083 與 `strips-pull`。
6. F06 p019（所長）：「就是飛機那一整條長長的身體，外面包著金屬。」 → 「就是飛機那一整條長長的身體，外面多半包著金屬。」（23 字）
7. F07 說明欄：「調查的結論是加壓機艙因為金屬疲勞而壞掉」 → 「調查對厄爾巴島外海那一架的結論，是加壓機艙因為金屬疲勞而壞掉」

連帶要改的（本次查核依指示只寫 verify-1.md）：`claims.md` C08 加上 NTSB AAR-19/03 §1.7.1、註 69 與 14 CFR 25.775(d) 作為三層窗的一手來源，並把「機長」改成「民航機飛行員」；C12 註明三倍是洞邊的最大值；C10 把「推力」改成「機身裡的拉力」；C25 加上 Withey 1997 "increased the thickness of the skin in these areas"；C15 補上「兩個洞一樣寬」的條件與實測紀錄；`script.md`、`build_scenes.py` 的同一行與說明欄一起改。

選修（不影響本輪結論）：

- S1 p101「教材說，疲勞的裂縫，從應力集中的地方長起來」：UNSW 原句講的是裂縫尖端的應力集中讓裂縫長大，不是在講「裂縫從窗角這種幾何轉角開始」；接在小問「窗戶的角！」後面，意思被延伸了。結論本身有 FAA 支持（"form fatigue cracks near the corners of the windows"），可留；若要主詞更乾淨，可改「對。疲勞的裂縫，常從力最擠的地方長出來。」（20 字，不掛來源）。
- S2 p061「水在角那裡，擠成一團！」：可留。若想避免小孩想成「水堆住不動」，可改「水到角那裡，擠得好急！」（11 字），配角上急流與小漩渦的插圖。
- S3 p065「力轉不過去」：FAA 原文是 "cannot smoothly flow around"（轉得不順），力其實還是繞過去了。可改「方窗戶的尖角，力轉得太急，就擠在角上。」（19 字）。
- S4 p037「所以機艙不會加到跟地面一樣」：在地面和低空時機艙就是地面氣壓，這句指的是飛很高的時候；可改「對。所以飛很高時，機艙不會加到跟地面一樣。」（21 字）。
- S5 p117「海裡撈回的那架」：兩架都掉進海裡，只有厄爾巴島那架撈回七成（拿坡里那架 "Very minimal wreckage"）。可改「厄爾巴島外海撈回的那架，最先裂的地方，」（19 字）；不改也不算錯。
- S6 p141「很小的力就斷了」：UNSW 是 "greatly reduced"（少很多），不是「很小」。可改「玻璃棒有了缺口，力小很多就斷了，」（16 字）。
- S7 p122「一萬六千次」：照 FAA 正確；Withey 1997 寫的是前段艙段 18,000 次。片中掛在「航空總署說」底下，不必改，若有留言問可以這樣回答。
- S8 說明欄「小問明天要坐飛機去找外婆，先用硬紙捲了一架小飛機」：片中沒有外婆，也沒說是捲的。不是事實錯誤；若要說明欄只寫片中有的事，刪「去找外婆」。
- S9 p065、p116 的「尖角／方方的」：彗星號的窗其實是小圓角的「squarish」（FAA 用字），不是直角；p116 說「方方的」照 FAA 可以，p065 是泛論。若之後畫彗星號窗戶，畫成小圓角的方窗，不要畫成直角。
