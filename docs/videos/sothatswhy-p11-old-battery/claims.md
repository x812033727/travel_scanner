# 主張與來源（sothatswhy-p11-old-battery）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說、來源與注意事項；行號是 `video.json` 的台詞 id（`build_scenes.py` 產生）。
2026-11-08 由研究代理逐頁打開來源寫成筆記（`p11-research.md`），撰稿只用筆記裡的數字；引文照頁面原文。
標「只看到摘要」的是頁面回 403 或只取得摘要，查核時請再開一次。方括號數字對應文末〈來源〉。
品牌：片中只說「手機公司」「有一家手機公司」「有的手機公司」，不比較品牌；是哪一家寫在這裡。

## C01 舊手機還有電也可能突然關機；多半不是壞掉，是電池老了

- **片中**：「先別急，它多半沒有壞。很多舊手機，都可能這樣突然關機。」「因為它的電池，已經老了。」（p009–p010、p012）
- **來源**：[1] "You're more likely to experience unexpected shutdowns when your battery has a low state of charge, a higher chemical age, or when you're in colder temperatures."
- **注意**：高。「多半沒有壞」是依這段的推論：老化、低電量、低溫三個條件都在小問的情境裡。

## C02 百分比是電池「現在」還剩多少；電池老了，裝滿時能存的電也比新的時候少

- **片中**：「螢幕上的百分比，是壺裡現在還剩幾分滿。」「不一定。百分之百，只是這個壺裝滿了。」「舊電池的壺，比新的時候小了。一樣裝滿，裡面的水就是比較少。」（p027、p034–p037）
- **來源**：[1] "As lithium-ion batteries chemically age, the amount of charge they can hold diminishes"；"Maximum battery capacity measures the device battery capacity relative to when it was new."
- **注意**：簡化。「百分比是現在這顆（老了的）電池裝滿的幾成」是研究筆記標明的我們的讀法（SIMPLIFICATION），Apple 沒有這句原文。

## C03 很多手機的設定裡有「最大容量」或「電池健康度」，是跟全新時比的估計，不一定很準

- **片中**：p040–p042、p045–p046
- **來源**：[1] "Maximum battery capacity measures the device battery capacity relative to when it was new."；[7] "Capacity is estimated by the battery's fuel gauge."；"Initial battery health values are based on lab results and may differ from your actual battery state."
- **注意**：「最大容量」是 Apple 的用語，「電池健康度」是一般說法；各家名稱不同，片中說「很多手機有一項……或……」。

## C04 百分比也是估的：手機看電池電壓、再數流進流出的電，大約算出來

- **片中**：「對。手機一邊看壺裡的水倒起來多有力，一邊數倒出去多少，大約算出來。」（p048–p049）；回呼「還記得百分比是估的嗎？它不一定很準。」（p127）
- **來源**：[12] "Measuring state-of-charge by voltage is simple, but it can be inaccurate."；"use coulomb counting to estimate SoC by measuring the in-and-out-flowing current."；[7] "Capacity is estimated by the battery's fuel gauge."
- **注意**：比喻。「倒起來多有力」對應電壓，「數倒出去多少」對應庫侖計數。研究筆記**沒有**找到「老電池最後幾成百分比會亂跳」的官方說法，片中不講跳動。

## C05 電池裡會慢慢長出一層薄膜（SEI），越用越厚；老化原因有好幾種，它是最常被提到的一種

- **片中**：「不是真的水垢，是很像水垢的一層薄膜。電池用得越久，它就慢慢長得越厚。」「不只。科學家找到好幾種讓電池變老的原因，水垢是最常被提到的一種。」（p057–p058、p061–p062）
- **來源**：[11] the film "gets thicker and eventually forms a barrier that obstructs interaction with graphite"；[13] "the unwanted growth of the solid electrolyte interphase (SEI)"；[14] 摘要 "Five principal and thirteen secondary mechanisms were found that are generally considered to be the cause of degradation"
- **注意**：比喻與簡化。「水垢」是我們的比喻（研究筆記用「皮」）。「最常被提到」是依 [11]、[13] 都把 SEI 列為老化主因；[14] 只讀到摘要（RSC 回 403），五個主要機制的名單沒有從全文核對。

## C06 這層薄膜讓電池能存的電變少，而且長了退不掉

- **片中**：「水垢會佔掉一些本來能裝電的地方。長得越厚，壺能裝的電就越少。」「刷不到。它長在電池最裡面，而且長了，就退不掉。」（p063–p064、p067–p068）；回呼 p180–p181
- **來源**：[11] lithium ends up "permanently lodged on the anode"；[5] "Even storing a battery in a hot environment can damage it irreversibly."；[1] 化學老化讓能存的電變少（見 C02）。
- **注意**：簡化。真正的機制是薄膜困住鋰（能搬電的鋰變少），不是「佔掉空間」；片中「佔掉能裝電的地方」是給小孩的說法，查核時請看是否接受。「刷不到」是比喻的延伸。

## C07 一次循環：用掉加起來一整顆電池的量才算一次

- **片中**：「就是喝掉一整壺的量。今天喝半壺，明天再喝半壺，加起來一整壺，才算一次。」（p073–p074）
- **來源**：[4] "you might use 75% of your battery's capacity one day, then recharge it fully overnight. If you use 25% the next day, you will have discharged a total of 100%, and the two days will add up to one charge cycle."；[7] "if you used your Pixel phone from 100% charge to 50% charge and then recharged it to 100%, this is calculated as 0.5 cycles."
- **注意**：高。片中把 75%＋25% 換成半壺＋半壺。

## C08 有一家手機公司說：一批手機的電池在很理想的情況下，大約一千次循環後還有原來大約八成

- **片中**：「有一家手機公司說，它有一批手機的電池，在很理想的情況下，大約一千次循環以後，壺還有原來的大約八成大。」（p076–p078）；小問「才少了大約兩成！」（p084）；所長「那是很理想的情況。真的用起來，要看你怎麼用、放在哪裡。」（p085–p086）
- **來源**：[1] "Batteries of iPhone 15 models are designed to retain 80 percent of their original capacity at 1000 complete charge cycles under ideal conditions."（[2] 重述 1000 次）
- **注意**：官方規格，**只適用 Apple 的 iPhone 15 機型**，是設計目標不是保證；iPhone 14 以前是 500 次。其他品牌另有數字（Google Pixel 8a 以後約 1000 次、Pixel 3–8 Pro 約 800 次），片中不比較品牌，所以只說「有一家手機公司」「一批手機」。

## C09 每天剛好用掉一整壺，一千次大約將近三年（我們自己粗算）

- **片中**：「我們自己粗算：如果每天剛好用掉一整壺，那大約是將近三年。」（p081–p082）
- **來源**：計算：1000 ÷ 365 ≈ 2.7 年。
- **注意**：**這是我們的計算**，片中明說「我們自己粗算」，前提「每天剛好用掉一整壺」也說出來。

## C10 放著不用電池也會老；熱會讓它老得更快，大約超過 35°C 就太熱

- **片中**：「不是喔。放著不用，電池也會慢慢老。就算收在抽屜裡，水垢也會慢慢長。」「尤其放在很熱的地方，水垢長得特別快，像夏天停在大太陽底下的車子裡。」「手機公司說，大約超過三十五度，就太熱了。」（p089–p092、p094）
- **來源**：[1] "chemical age … is more than just the passage of time. It includes different factors, such as the number of charge cycles and how it was cared for."；[10] "Lithium-ion suffers from stress when exposed to heat"；[10] 儲存表：25°C、一年，存 40% 電約保留 96%、存 100% 約 80%；[5] "avoid exposing your device to ambient temperatures higher than 95° F (35° C), which can permanently damage battery capacity."
- **注意**：「放著也會老」靠 [1] 的「不只是時間」（時間是其中之一）與 [10] 的儲存數據；「抽屜裡水垢也會長」是把日曆老化對到比喻，[11] 把 SEI 列為主要機制，但不是每一種日曆老化都是 SEI。「夏天的車子」是例子，不是來源原句。35°C 是 Apple 的數字（「手機公司」）。

## C11 太冷也不好，手機最好在大約 0°C 以上

- **片中**：「千萬不要！太冷也不行。手機公司說，最好待在大約零度以上。」（p097–p098）
- **來源**：[5] "iPhone, iPad, iPod, and Apple Watch work best at 32° to 95° F (0° to 35° C) ambient temperatures."
- **注意**：Apple 的範圍是 0–35°C；片中把下限說成「大約零度以上」。冷凍庫一般低於 0°C。[5] 另有 16–22°C 的理想舒適區，片中不講。冷天**充電**造成鋰析出（BU-410）片中不講。

## C12 電池老了，一下子給出大量電的能力變差；大量用電時電壓掉太低，手機會為了保護元件主動關機

- **片中**：「因為水垢不只讓壺變小，也會把壺嘴慢慢堵窄。」（p101）「手機裡的零件，一下子拿不到夠多的電，就沒辦法好好工作。」「不是。手機會搶先一步，自己關機，保護裡面的零件。」「對。你看到的是突然黑掉，其實是手機故意的。」（p116–p123）；「只是壺嘴太窄，大口倒不出來。」（p129）
- **來源**：[1] "a battery's ability to deliver maximum instantaneous performance, or 'peak power,' might decrease."；"When a device pulls power from a battery with a higher level of impedance, the battery's voltage will drop to a greater degree. Electronic components require a minimum voltage to properly operate."；"the system will perform a shutdown to preserve these electronic components. While this shutdown is intentional from the device perspective, it might be unexpected by the user."；[11] SEI 屏障造成 "an increase of internal resistance."
- **注意**：高（Apple 的官方說明）。「壺嘴」是內阻／供電能力的比喻；「同一層水垢把壺嘴堵窄」依 [11]（SEI 讓內阻上升），其他老化機制也會讓內阻上升，片中只講這一個。p124「它沒有壞，插上電就能再打開」是從「為保護元件而關機」推出的說法，來源沒有這一句。

## C13 開相機、玩遊戲這類事會一下子要很多電

- **片中**：「像開相機拍照、玩很忙的遊戲，手機一下子就要很多電。」（p112–p113）
- **來源**：[1] 說的是系統需要「peak power」的時候（"A battery with a high impedance might not be able to provide sufficient power to the system that needs it."）。
- **注意**：例子是我們舉的（研究筆記的白話說法），Apple 頁面沒有點名相機或遊戲。

## C14 電量低時更容易發生；冷的時候也更容易，但冷的影響是暫時的

- **片中**：「壺裡水多，倒起來比較有力；水少了，再碰上窄壺嘴，就容易倒不夠。」（p135–p136）「有。天氣冷，壺嘴也會暫時變窄一點，回到暖和的地方，就會好一些。」（p139–p140）
- **來源**：[1] "You're more likely to experience unexpected shutdowns when your battery has a low state of charge, a higher chemical age, or when you're in colder temperatures."；"For a low battery state of charge and colder temperatures, performance-management changes are temporary."；[5] in cold "you may notice a decrease in battery life, but this condition is temporary."；[7] aging leads to "a decreased ability to deliver power in extreme temperatures."
- **注意**：「水多倒起來比較有力」是比喻（電量高時電壓較高），Apple 只說低電量時更容易關機。

## C15 有些手機在電池供電能力變差時，會限制自己的最高效能，減少意外關機；但手機變慢不一定是電池

- **片中**：「有時候是。有些手機遇到壺嘴變窄，會讓自己跑慢一點，少大口喝電。」「少一點大口喝，就比較不會突然關機。」（p145–p146、p149）「不過我覺得，別每次手機變慢都怪電池，慢的原因很多，電池只是其中一個。」（p150–p151）
- **來源**：[1] "This feature is enabled only after an unexpected shutdown first occurs on a device with a battery that has diminished ability to deliver maximum instantaneous power."；"iOS will dynamically manage the maximum performance of some system components, such as the CPU and GPU."；[2] "The system allows your iPhone to reduce performance effects from battery aging."
- **注意**：限制效能的說明明列 iPhone 6 到 XR，新機型說法不同，所以片中只說「有些手機」，不說所有手機都會降速。p150–p151 是**意見**，標「我覺得」；「慢的原因很多」研究筆記沒有來源。

## C16 電池不喜歡長時間停在 100%；很多手機會學你的習慣，先充到大約 80%、快拔線前再充滿

- **片中**：「電池也不喜歡一直裝得滿滿的，放很久，那樣水垢也長得比較快。」（p156–p157）「所以很多手機會學你的習慣：先充到大約八成，停一下，快起床時，再把它充滿。」（p158–p160）「它會慢慢記住，你平常什麼時候拔掉充電線。有的手機公司說，大約要學兩個禮拜。」（p162–p163）「有些手機也能設定，最多只充到八成。」（p167）
- **來源**：[9] "Keeping your battery at a full 100% charge for a long time can reduce its lifespan."；[10] "so does keeping a cell at a high charge voltage."；[3] iPhone will "delay charging past 80 percent in certain situations"，學習 "your daily charging routine"，"reducing the time your iPhone spends fully charged."；[8] Adaptive Charging "may turn on to charge to 100% one hour before you unplug"；"needs about 14 days to learn your charging habits."；"limit charging of your phone to 80%"（Pixel 6a 以後）；[9] Maximum "will stop charging when it reaches 80%"
- **注意**：「兩個禮拜」是 Google Pixel；「最多充到八成」是 Pixel 6a 以後與 Samsung One UI 6.1（舊版／其他地區頁面是 85%）；「延後到 80%」是 Apple。三家各自的功能，不比較。「水垢長得比較快」把高電壓老化對到比喻。

## C17 想充就充，不用等用光；不用從滿用到空來「教」手機；用一點充一點沒關係，盡量不要常常用到完全沒電

- **片中**：「不用。現在的手機電池，想充就充。不用等它用光，也不用教它認識壺。」（p170–p171）「研究電池的人也說，用一點、充一點沒關係，能不要常常用到完全沒電，反而比較好。」（p172–p173）
- **來源**：[4] "Charge your Apple lithium-ion battery whenever you want. There's no need to let it discharge 100% before recharging."；[8] "You don't need to teach your phone how much capacity the battery has by going from full to zero charge or zero to full charge."；[10] "Partial discharge on Li-ion is fine." "If at all possible, avoid full discharges."
- **注意**：[10] 是 Battery University（二手教材）。研究筆記提醒 Apple 與 BU-808 語氣不同，片中不說「絕對不要用到零」。Google 另說 Pixel 每第 10 次循環要充滿一次以校正讀數，片中不講。

## C18 充電時發熱，先把手機殼拿掉；不要在高溫下充電

- **片中**：「手機公司建議，先把手機殼拿掉，也別在大太陽底下充電。」（p176–p177）
- **來源**：[5] "If you notice that your device gets hot when you charge it, take it out of its case first."；"Charging the device in high ambient temperatures can damage it further."
- **注意**：Apple。「大太陽底下」是高溫環境的例子。

## C19 老化退不掉；電池要由專業的人更換，自己拆可能讓電池過熱、起火

- **片中**：「真的太舊了，可以請大人帶去，讓專業的人換一顆新電池。」（p182–p183）「不行喔。電池弄壞了，可能會變燙，甚至起火。」（p186）
- **來源**：[6] "An iPhone battery should only be repaired by a trained technician to avoid battery damage, which could cause overheating, fire, or injury."
- **注意**：高。「請大人帶去」是給小孩的安全說法。

## C20 電池鼓起來、很燙、有怪味：不要再用、不要充電，告訴大人；充電要用合格的充電器和線

- **片中**：「像手機變得鼓鼓的、很燙，或有怪味，就不要再用、也不要充電，馬上告訴大人。」（p188–p189）「要用合格的充電器和線。不合格的，可能不安全。」（p192–p193）
- **來源**：[6] "If you suspect damage to iPhone or the battery, discontinue use of iPhone, as it may cause overheating or injury."；第三方線材與轉接器要 "compliant with USB 2.0 or later and with applicable country regulations and international and regional safety standards. Other adapters may not meet applicable safety standards, and charging with such adapters could pose a risk of death or injury."
- **注意**：政策。「鼓鼓的、很燙、有怪味」是懷疑損壞的例子；Samsung 鼓脹電池的官方頁**沒有找到**（只看到舊 FAQ 與論壇摘要），所以只引 Apple 的「懷疑損壞就停用」。「也不要充電」是停用的一部分，Apple 原句沒有單獨這樣說。

## 意見與比喻（不需要來源，但要標成意見或比喻）

- 水壺（電池）、壺裡的水（電）、幾分滿（百分比）、壺多大（最大容量）、壺嘴（供電能力）、水垢（SEI 薄膜）：比喻，全片只用這一個，是我們自己的（研究筆記：沒有找到官方的兒童比喻）。
- p009 所長安撫、p015「很多人都跟你一樣」、p019「我們就來拆開這顆老電池」、p132「電量還多，不代表壺還大、壺嘴還寬」：承諾、問題與歸納，不是新主張。
- p105–p106「用很窄的壺嘴倒一大杯水，是不是要等好久」：比喻的延伸。
- p150–p151「我覺得，別每次手機變慢都怪電池」：意見。
- p200–p201「下次手機突然黑掉，先別怪它，它是在保護自己」：依 C12 的歸納。

## 來源

1. Apple, iPhone battery and performance. https://support.apple.com/en-us/101575
2. Apple, Battery and performance of iPhone 11 and later. https://support.apple.com/en-us/106348
3. Apple, About Optimized Battery Charging on your iPhone. https://support.apple.com/en-us/108055
4. Apple, Why lithium-ion. https://www.apple.com/batteries/why-lithium-ion/
5. Apple, Maximizing performance. https://www.apple.com/batteries/maximizing-performance/
6. Apple, Important safety information for iPhone. https://support.apple.com/guide/iphone/important-safety-information-iph301fc905/ios
7. Google, Understand your Pixel battery. https://support.google.com/pixelphone/answer/15738128?hl=en
8. Google, Get the most life from your Pixel battery. https://support.google.com/pixelphone/answer/6090612?hl=en
9. Samsung (IE), Battery protection in One UI 6.1. https://www.samsung.com/ie/support/mobile-devices/galaxy-battery-protection-feature-in-one-ui-6-1/
10. Battery University, BU-808 How to prolong lithium-based batteries. https://batteryuniversity.com/article/bu-808-how-to-prolong-lithium-based-batteries
11. Battery University, BU-808b What causes Li-ion to die. https://batteryuniversity.com/article/bu-808b-what-causes-li-ion-to-die
12. Battery University, BU-903 How to measure state-of-charge. https://batteryuniversity.com/article/bu-903-how-to-measure-state-of-charge
13. University of Münster MEET, Battery Aging. https://www.uni-muenster.de/MEET/en/research/cell-system/Aging.html
14. Edge, O'Kane et al., "Lithium ion battery degradation: what you need to know", Phys. Chem. Chem. Phys. 23 (2021) 8200–8221（只讀到摘要）. https://doi.org/10.1039/D1CP00359C
