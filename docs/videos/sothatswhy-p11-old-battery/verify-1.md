# 查核報告 1（sothatswhy-p11-old-battery）

- 查核者：Claude（獨立查核代理，未參與撰稿）
- 日期：2026-11-08
- 方法：逐句讀 `video.json` 的 205 句台詞（p001–p205），加上 YouTube 標題、說明與縮圖 headline／sub。對照 `claims.md` 的 C01–C20，但不採用其中的引文，而是用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓下每個來源，轉成文字後讀原文：Apple〈iPhone battery and performance〉（101575）、〈Battery and performance of iPhone 11 and later〉（106348）、〈About Charge Limit and Optimized Battery Charging on iPhone〉（108055）、〈Why lithium-ion〉、〈Maximizing performance〉、〈Important safety information for iPhone〉；Google〈Understand your Pixel battery〉（15738128）、〈Get the most life from your Pixel battery〉（6090612）；Samsung IE〈Battery protection in One UI 6.1〉；Battery University BU-808、BU-808b、BU-903；Münster MEET〈Battery Aging〉。claims.md 只讀到摘要的 Edge et al. 2021（PCCP 23:8200），這次經 OpenAlex 找到 Guelph 大學機構典藏的開放全文 PDF（CC-BY 3.0，atrium.lib.uoguelph.ca），用 pdftotext 讀了 SEI 一節與「實驗觸發條件」一節。claims.md 沒有的來源另外找了：Google〈Extended Repair Program for Pixel 7a〉（16043453），用來核對「鼓起來就停用」。
- 打不開的來源：pubs.rsc.org 的 Edge 2021 頁面與 HTML 全文回 403，改讀上述機構典藏 PDF（同一篇、同頁碼 8200–8221）。Samsung 官方的鼓脹電池說明頁沒有找到，搜尋只得到 Samsung Community 版主回覆（論壇，不採用為來源）。
- 對 claims.md 的更正：C08 寫「只適用 iPhone 15 機型」；Apple 106348 現在的原文是「Batteries of iPhone 15 models **and later** are designed to retain 80 percent of their original capacity at 1000 complete charge cycles under ideal conditions」，101575 仍寫「iPhone 15 models」。另外 Google 15738128 也寫 Pixel 8a 以後「Should retain up to 80% capacity for about 1000 charge cycles」，Pixel 3 到 8 Pro 約 800 次，iPhone 14 以前 500 次。所以一千次只適用**較新的**機型，而片中拿來對照的是「媽媽的舊手機」，見 F03。C05 的「最常被提到」：Edge 全文原句是「SEI layer growth is often quoted as **one of** the main degradation modes」，不是「最常」，見 F01。C10「抽屜裡水垢也會長」現在有直接來源：Edge「The SEI begins to form as soon as the NE is lithiated … and will grow even if the battery is not then used」「high temperatures increase … the SEI growth rate」；C16「滿電放久水垢長得比較快」也有：Edge「it grows even when the cell is at rest at high SoC, albeit at slower rates (this contributes to calendar ageing)」。
- claims.md 請查核者判斷的項目：
  1. 水垢「佔掉能裝電的地方」（C06，p063）：**改**。Edge 原文：「Capacity is irreversibly lost due to otherwise cyclable lithium being trapped within the SEI」，另寫 SEI「consumes the electrolyte solvent」；BU-808b 寫鋰「permanently lodged on the anode」。容量變少的原因是能搬電的鋰被薄膜吃進去、卡住，不是薄膜佔了空間。熱水壺水垢的直覺正好是「佔空間」，小孩會照字面記住錯的機制；改成「把能存電的東西卡在裡面」一樣短、一樣在比喻裡，而且跟 p068「退不掉」接得更好（irreversibly）。見 F02。p064「長得越厚，壺能裝的電就越少」照留。
  2. 「插上電就能再打開」（p124）：**改**。Apple 101575 只說關機是「intentional from the device perspective」「to preserve these electronic components」，沒有說之後怎麼重新開機，也沒有說一定沒壞；同頁還寫「In extreme cases, shutdowns can occur more frequently, making the device unreliable or unusable」。「它沒有壞」也比 p009「多半沒有壞」絕對。見 F05。
  3. 「將近三年」（C09，p081–p082）：**保留**。1000 ÷ 365 ≈ 2.74 年，「將近三年」正確，片中明說「我們自己粗算」與前提「每天剛好用掉一整壺」。但一千次只適用 iPhone 15 以後、Pixel 8a 以後，舊機型是 500 或約 800 次，而片中的主角是媽媽的**舊**手機；p076 要讓觀眾知道這是較新的一批手機，p078 也要說是「設計成」（Apple「are designed to retain」；Google「Should retain up to」），不是測出來的結果。見 F03。
  4. 鼓起來 → 不要再用、不要充電（C20，p188–p189）：**保留**。Apple 安全資訊「If you suspect damage to iPhone or the battery, discontinue use of iPhone, as it may cause overheating or injury」；Google Pixel 7a 延長維修頁列出鼓脹症狀（「The phone may appear thicker than usual, or the back cover might be bulging」）並寫「we recommend you stop using the device」。「不要充電」是停用的一部分，不算新事實；「馬上告訴大人」是給小孩的安全說法。
- 結論統計（台詞 205 句）：OK 196、FIX 9（共 7 項，F01–F07）、NOT FOUND 0。另外標題、說明、縮圖 headline、縮圖 sub 共 4 項：OK 3、FIX 1（F08）。
- 品牌：全片只說「手機公司」「有一家」「有的」，沒有比較品牌，也沒有暗示哪一家比較好。p163「大約要學兩個禮拜」是 Google；p167「最多只充到八成」Apple（108055，Charge Limit 最低 80%）、Google（Pixel 6a 以後）、Samsung（One UI 6.1 的 Maximum）都有，說「有些手機」正確。
- 與官方保養說法是否衝突：沒有。p170「想充就充」對上 Apple「Charge your Apple lithium-ion battery whenever you want」與 Google「Charge as much or as little as needed」；p172–p173 引 BU-808「Partial discharge on Li-ion is fine」「If at all possible, avoid full discharges」，跟 Apple 不衝突（Apple 只說不必等用光，長期存放也說不要放到全空）。Google 另說 Pixel 每第 10 次循環要充滿一次以校正讀數，片中沒講，不影響「交給手機就好」。
- 安全判斷：小孩可能照做的動作都有大人或官方說法把關：查設定請大人（p040）、不要放冷凍庫（p097）、不要自己拆（p186）、鼓脹／很燙／怪味就停用並告訴大人（p189）、用合格充電器（p192）。唯一的混淆是 p174 小孩說充電時「好燙」，所長只教拿掉手機殼，後面 p188 又說「很燙就不要再用、不要充電」，同一個「燙」得到兩種處理，見 F06。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p062（所長） | 水垢是最常被提到的一種。 | FIX（比來源絕對） | Edge et al. 2021 全文：「SEI layer growth is often quoted as one of the main degradation modes」；BU-808b 把 SEI 列為「four suspected renegades」之一；MEET 把它列在一串機制的第一個。沒有來源說它是「最常」被提到的。**建議改成**：「水垢是常被提到的主要原因之一。」（15 字） |
| F02 | p063（所長） | 水垢會佔掉一些本來能裝電的地方。 | FIX（機制說錯，見上方判斷 1） | Edge：「Capacity is irreversibly lost due to otherwise cyclable lithium being trapped within the SEI」；BU-808b：鋰「permanently lodged on the anode」。不是佔空間，是把能搬電的東西卡住。**建議改成**：「水垢會把一些本來能存電的東西，卡在裡面。」（19 字）。p064 照留 |
| F03 | p076、p078（所長） | 有一家手機公司說，它有一批手機的電池，／大約一千次循環以後，壺還有原來的大約八成大。 | FIX（設計目標說成結果；只適用較新機型） | Apple 106348「Batteries of iPhone 15 models and later are designed to retain 80 percent … at 1000 complete charge cycles under ideal conditions」、「iPhone 14 models and earlier … at 500」；Google 15738128 Pixel 8a 以後約 1000 次、Pixel 3–8 Pro 約 800 次。主角拿的是舊手機，不說「較新」，觀眾會以為自己的舊手機也能撐一千次。**建議改成**：p076「有一家手機公司說，它較新的一批手機電池，」（19 字）；p078「設計成大約一千次循環後，壺還有原來的大約八成大。」（23 字）。p077、p081–p086 照留 |
| F04 | p097、p098（所長） | 千萬不要！太冷也不行。／手機公司說，最好待在大約零度以上。 | FIX（答非所問，理由跟來源對不上） | 小問問的是「放冷凍庫就不會老」，是存放。Apple〈Maximizing performance〉的 0–35°C 是「work best at … ambient temperatures」，是**使用**範圍；同頁的存放範圍是「Storage temperature: -4° to 113° F (-20° to 45° C)」，一般冷凍庫在這個範圍內，所以「太冷也不行」用在存放上沒有來源。真正能回答她的是：冰起來還是會老（Edge「will grow even if the battery is not then used」；BU-808 表 3：0°C 存放一年仍只剩 98%／94%）。「不要」照樣擋住小孩的動作。**建議改成**：p097「不要喔！冰起來也還是會老。」（12 字）；p098「手機公司說，用的時候最好在大約零度以上。」（19 字） |
| F05 | p124（所長） | 它沒有壞，插上電就能再打開。 | FIX（沒有來源；比 p009 絕對） | 見上方判斷 2。Apple 101575 只說關機是為了「preserve these electronic components」，沒有「插上電就能再打開」，也寫極端時會「unreliable or unusable」。**建議改成**：「所以它多半沒有壞，只是先關機保護自己。」（18 字） |
| F06 | p174（小問） | 充電時它好燙， | FIX（跟 p188「很燙就停用」打架） | Apple 安全資訊：iPhone 與充電器符合表面溫度限制，但長時間接觸「warm surfaces」可能不舒服；Google 6090612「Your phone warms up when it's plugged in」；Apple〈Maximizing performance〉的對策是「take it out of its case first」。充電時變熱是正常的，拿掉手機殼是對這種情況；p188 的「很燙」是損壞的徵兆，要停用並告訴大人。小孩先聽到「好燙→拿掉殼」，再聽到「很燙→停用」，會不知道該照哪一個。**建議改成**：「充電時它熱熱的，」（8 字）。p175–p177、p188–p189 照留 |
| F07 | p201（所長） | 先別怪它，它是在保護自己。 | FIX（片尾把每一次黑掉都說成保護） | Apple 101575 只說「低電量、老化、低溫」時的意外關機是保護元件；手機突然黑掉也可能是別的原因。p009 說「多半沒有壞」，片尾要跟它一致。**建議改成**：「先別怪它，它多半是在保護自己。」（14 字） |
| F08 | youtube.description | 片中的數字都是手機公司說明裡的大約數字， | FIX（不完全正確） | 「將近三年」是我們自己粗算（p081），「百分之二十」是小問看到的，都不是手機公司的數字。**建議改成**：「片中的數字大多是手機公司說明裡的大約數字，「將近三年」是我們自己粗算，」 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p008 | 冷天在公園用媽媽的舊手機拍松鼠，還有百分之二十，一按拍照就黑掉；剛買時一整天都有電；是不是壞了 | OK | — | 角色經歷與問題。「百分之二十」是小問看到的數字，不需要「大約」 |
| p009–p010 | 多半沒有壞；很多舊手機都可能這樣突然關機 | OK | Apple 101575 | 「You're more likely to experience unexpected shutdowns when your battery has a low state of charge, a higher chemical age, or when you're in colder temperatures.」有「多半」「可能」 |
| p011–p014 | 為什麼舊的才會；電池老了；電量還有怎麼會老 | OK | Apple 101575 | 「A battery's impedance can increase if a battery has a higher chemical age.」 |
| p015 | 很多人以為電量還多，電池就還好 | OK（歸納） | — | 轉向觀眾，不是事實主張 |
| p016 | 那一下黑掉是手機自己決定的 | OK | Apple 101575 | 「While this shutdown is intentional from the device perspective, it might be unexpected by the user.」 |
| p017–p018 | 電池裡正偷偷長著一層東西 | OK | Edge 2021；BU-808b | 「the thickness of the SEI layer increases … as the cell ages」 |
| p019–p021 | 承諾與全片問題 | OK | — | — |
| p022–p031 | 電池像裝電的水壺；電是水；百分比是還剩幾分滿；用電是喝水、充電是裝滿 | OK（比喻） | — | 比喻，claims.md 已標明 |
| p032–p037 | 充到百分百不一定跟新的一樣多；舊壺比新的小，一樣裝滿水比較少 | OK | Apple 101575 | 「As lithium-ion batteries chemically age, the amount of charge they can hold diminishes」 |
| p038–p039 | 難怪充滿也撐不了一整天 | OK | Apple 101575 | 「which might result in fewer hours of usage between charges」 |
| p040 | 請大人打開設定找找看 | OK（安全） | — | 由大人操作 |
| p041–p042 | 很多手機有「最大容量」或「電池健康度」，說的是壺還剩多大 | OK | Apple 101575；Google 15738128 | Apple「Maximum battery capacity measures the device battery capacity relative to when it was new」；Google「Battery health … an estimate of your device's remaining battery capacity compared to its original capacity」。Google 也寫 Pixel 6a–8 Pro 不顯示健康狀態，片中說「很多手機」不說全部，可以 |
| p043–p046 | 跟全新時比、自己估出來的，不一定很準 | OK | Google 15738128；Apple 101575 | 「Capacity is estimated by the battery's fuel gauge」「Initial battery health values are based on lab results and may differ from your actual battery state」；Apple iOS 14.5 曾修正「inaccurate estimates of battery health reporting」 |
| p047–p049 | 百分比也是估的：看倒得多有力、數倒出去多少，大約算出來 | OK（比喻） | BU-903 | 電壓法「simple, but it can be inaccurate」；庫侖計數「measuring the in-and-out-flowing current」 |
| p050–p055 | 壺裡會長水垢；熱水壺的白白硬硬的東西就是水垢 | OK（比喻＋常識） | — | 熱水壺水垢是生活常識 |
| p056–p058 | 不是真的水垢，是很像水垢的薄膜；用越久長越厚 | OK | Edge 2021；BU-808b | 「the thickness of the SEI layer increases … as the cell ages」；「The film gets thicker」 |
| p059–p061 | 不只水垢；科學家找到好幾種原因 | OK | Edge 2021 摘要與全文 | 「Five principal and thirteen secondary mechanisms」 |
| p062 | 水垢是最常被提到的一種 | 見 F01 | — | — |
| p063 | 水垢佔掉能裝電的地方 | 見 F02 | — | — |
| p064 | 長得越厚，能裝的電越少 | OK | Edge 2021 | 「Capacity is irreversibly lost due to … lithium being trapped within the SEI」 |
| p065–p068 | 刷掉不就好了；刷不到、長在最裡面、長了退不掉 | OK（比喻＋事實） | Edge 2021；BU-808b | 「irreversibly lost」；「a phenomenon that is irreversible」。「最裡面」是比喻 |
| p069–p072 | 充一次就長一次嗎；差不多，不過手機算的是一次循環 | OK（附註） | BU-808b | 「the SEI layer grows as the battery cycles」。「差不多」略鬆，但 p089–p090 立刻補上不用也會長，不會誤導 |
| p073–p074 | 半壺加半壺，加起來一整壺才算一次 | OK | Apple〈Why lithium-ion〉；Google 15738128 | 「use 75% … one day … 25% the next day … add up to one charge cycle」；Pixel「100% to 50% … calculated as 0.5 cycles」 |
| p075 | 喝很多次以後呢 | OK | — | 問題 |
| p076、p078 | 一批手機、一千次後還有八成 | 見 F03 | — | — |
| p077 | 在很理想的情況下 | OK | Apple 101575／106348 | 「under ideal conditions」 |
| p079–p082 | 要用好幾年吧；我們自己粗算，每天剛好一整壺，大約將近三年 | OK（自行計算，已標明） | — | 1000 ÷ 365 ≈ 2.74 年。前提與「我們自己粗算」都說出來，見判斷 3 |
| p083–p086 | 才少了大約兩成；那是很理想的情況，要看怎麼用、放哪裡 | OK | Apple 101575；Google 15738128 | 100% − 80% = 20%，有「大約」；Google「Your battery's actual lifespan depends on usage patterns and other factors」 |
| p087–p090 | 不充電就不會長水垢嗎；放著不用也會老，收在抽屜也會長 | OK | Edge 2021；Apple 101575 | 「will grow even if the battery is not then used」；chemical age「is more than just the passage of time」 |
| p091–p092 | 放很熱的地方長得特別快，像夏天大太陽下的車子裡 | OK（附註） | Edge 2021；Apple〈Maximizing performance〉；BU-808 | 「high temperatures increase diffusion rates and hence also the SEI growth rate」；「Even storing a battery in a hot environment can damage it irreversibly」。車子是例子，來源沒有原句，但屬於高溫環境 |
| p093–p094 | 多熱算太熱；手機公司說大約超過三十五度 | OK | Apple〈Maximizing performance〉 | 「avoid exposing your device to ambient temperatures higher than 95° F (35° C), which can permanently damage battery capacity」。有「大約」 |
| p095–p096 | 放冷凍庫就不會老吧 | OK | — | 小孩的錯猜，由 p097 回答 |
| p097–p098 | 太冷也不行；最好在大約零度以上 | 見 F04 | — | — |
| p099–p101 | 壺變小只是比較快沒電，怎麼會黑掉；水垢也把壺嘴堵窄 | OK | Edge 2021；BU-808b；Apple 101575 | SEI「increase the overall impedance of cells, leading to power fade」；「resulting in an increase of internal resistance」；Apple「peak power … might decrease」 |
| p102–p106 | 壺嘴寬不寬決定一次倒多快；窄壺嘴倒一大杯要等好久 | OK（比喻） | Apple 101575 | 對應「impedance」與「instantaneous power delivery」 |
| p107–p109 | 小口喝窄一點沒關係；平常慢慢用電來得及 | OK | Apple 101575 | 「A battery with a high impedance might not be able to provide sufficient power to the system that needs it」，問題出在瞬間大量用電 |
| p110–p113 | 開相機拍照、玩很忙的遊戲，一下子要很多電 | OK（附註：例子） | Apple 101575 | 頁面沒有點名遊戲；但效能管理最極端時「the camera flash will be disabled」，可見相機（閃光燈）屬於高峰用電；遊戲對應「CPU and GPU」高峰 |
| p114–p117 | 壺嘴太窄倒不出來，零件拿不到夠多的電，就沒辦法好好工作 | OK | Apple 101575 | 「Electronic components require a minimum voltage to properly operate」 |
| p118–p123 | 不是壞掉；手機搶先自己關機保護零件；看到的是突然黑掉，其實是故意的 | OK | Apple 101575 | 「the system will perform a shutdown to preserve these electronic components. While this shutdown is intentional from the device perspective, it might be unexpected by the user.」 |
| p124 | 它沒有壞，插上電就能再打開 | 見 F05 | — | — |
| p125–p127 | 百分比是不是騙人；還記得百分比是估的，不一定很準 | OK | BU-903 | 見 p047–p049 |
| p128–p129 | 它沒騙人，壺裡多半還有水，只是壺嘴太窄 | OK | Apple 101575 | 電壓在大量用電時「drop to a greater degree」，電量不是零也會關機。有「多半」 |
| p130–p132 | 水、壺多大、壺嘴多寬是三件事；電量多不代表壺還大、壺嘴還寬 | OK（歸納） | Apple 101575 | 頁面分開講 state of charge、maximum capacity、peak performance capability |
| p133–p136 | 水多倒起來比較有力；水少再碰上窄壺嘴就容易倒不夠 | OK（比喻） | Apple 101575 | 「A battery's impedance will temporarily increase at a low state of charge … When coupled with a higher chemical age, the impedance increase will be more significant.」 |
| p137–p142 | 天冷壺嘴暫時變窄，回到暖和就好一些；難怪在冷冷的公園黑掉 | OK | Apple 101575；Apple〈Maximizing performance〉 | 「impedance will temporarily increase … in a cold temperature environment」；「For a low battery state of charge and colder temperatures, performance-management changes are temporary」；冷天「this condition is temporary」 |
| p143–p146 | 手機變慢有時候是；有些手機會讓自己跑慢一點，少大口喝電 | OK | Apple 101575 | 「iOS will dynamically manage the maximum performance of some system components, such as the CPU and GPU」，列明機型，所以「有些手機」恰當 |
| p147–p149 | 故意跑慢的好處：比較不會突然關機 | OK | Apple 101575 | 「dynamically manages performance peaks to prevent the device from unexpectedly shutting down」 |
| p150–p151 | 我覺得別每次變慢都怪電池，原因很多 | OK（意見） | — | 標了「我覺得」；Apple 頁面也列出很多不受影響的項目 |
| p152–p155 | 怎麼讓它老得慢；很多事手機已經在幫你做 | OK | Apple 108055；Google 6090612；Samsung | 三家都有內建的電池保護 |
| p156–p157 | 電池不喜歡一直滿滿的放很久，那樣水垢也長得比較快 | OK | Samsung；Apple〈Maximizing performance〉；Edge 2021 | 「Keeping your battery at a full 100% charge for a long time can reduce its lifespan」；「if you store it fully charged for an extended period of time, the battery may lose some capacity」；SEI「grows even when the cell is at rest at high SoC」 |
| p158–p160 | 很多手機學你的習慣，先充到大約八成，停一下，快起床再充滿 | OK | Apple 108055；Samsung；Google 6090612 | Apple「delay charging past 80 percent in certain situations … learn your daily charging routine」；Samsung Adaptive「charges to 100% an hour before you wake up」；Pixel「charge to 100% one hour before you unplug」 |
| p161–p163 | 它會記住你什麼時候拔線；有的手機公司說大約要學兩個禮拜 | OK | Google 6090612 | 「This feature needs about 14 days to learn your charging habits」。有「大約」 |
| p164–p166 | 要不要自己盯著到八成拔；不用，交給手機 | OK（意見） | Apple 108055 | 與官方的自動功能一致 |
| p167 | 有些手機能設定最多只充到八成 | OK | Apple 108055；Google 6090612；Samsung | Charge Limit「between 80 percent and 100 percent」；「limit charging of your phone to 80%」（Pixel 6a 以後）；Maximum「stop charging when it reaches 80%」（One UI 6.1 以前是 85%，片中說「有些」）。是設定值，不加「大約」可以 |
| p168–p171 | 要用到沒電才能充嗎；不用，想充就充，不用等用光，也不用教它認識壺 | OK | Apple〈Why lithium-ion〉；Google 6090612 | 「Charge … whenever you want. There's no need to let it discharge 100% before recharging」；「You don't need to teach your phone how much capacity the battery has by going from full to zero」 |
| p172–p173 | 研究電池的人說用一點充一點沒關係，不要常常用到完全沒電比較好 | OK（二手來源） | BU-808 | 「Partial discharge on Li-ion is fine」「If at all possible, avoid full discharges」。用「能不要常常」，不是絕對；與 Apple 不衝突 |
| p174 | 充電時它好燙 | 見 F06 | — | — |
| p175–p177 | 手機公司建議先把手機殼拿掉，別在大太陽底下充電 | OK | Apple〈Maximizing performance〉 | 「If you notice that your device gets hot when you charge it, take it out of its case first」；「Charging the device in high ambient temperatures can damage it further」。大太陽是高溫的例子 |
| p178–p181 | 舊手機還有救嗎；水垢退不掉，壺變不回原來大 | OK | Edge 2021；Apple 101575 | 「irreversibly lost」；「all rechargeable batteries are consumables … eventually needing to be replaced」 |
| p182–p183 | 太舊了請大人帶去，讓專業的人換新電池 | OK | Apple 安全資訊；Apple 101575 | 「should only be repaired by a trained technician」；「replacing your device battery can help」 |
| p184–p186 | 自己拆不比較快；電池弄壞了可能變燙甚至起火 | OK（安全） | Apple 安全資訊 | 「to avoid battery damage, which could cause overheating, fire, or injury」 |
| p187–p189 | 鼓鼓的、很燙、有怪味就不要再用、不要充電，馬上告訴大人 | OK（安全，附註） | Apple 安全資訊；Google Pixel 7a 延長維修頁 | 「If you suspect damage … discontinue use」；鼓脹症狀「back cover might be bulging」與「we recommend you stop using the device」。怪味是懷疑損壞的例子，見判斷 4 |
| p190–p193 | 充電器不能隨便用；要用合格的充電器和線，不合格可能不安全 | OK | Apple 安全資訊；Google 6090612 | 「compliant with USB 2.0 or later and with applicable … safety standards. Other adapters may not meet applicable safety standards, and charging with such adapters could pose a risk of death or injury」；Google「Other power adapters … can also damage your phone or battery」 |
| p194–p199 | 小問自己說：拍照要大口喝電、舊壺嘴太窄、天氣又冷，手機先關機保護自己 | OK | 同上各段 | 與 p110–p142 一致 |
| p200 | 對，就是這樣！下次手機突然黑掉， | OK | — | 接 p201 |
| p201 | 先別怪它，它是在保護自己 | 見 F07 | — | — |
| p202–p205 | 原來如此；留言題；訂閱 | OK | — | 片尾 |
| youtube.title | 電量還有，手機電池為什麼已經老了？ | OK | Apple 101575 | 問句，前提正確 |
| youtube.description | 小問的經歷；水壺比喻；水垢讓壺變小、壺嘴變窄；倒不夠快就先關機保護零件；想充就充；鼓起來、很燙、有怪味要停用並告訴大人；比喻與 AI 插圖說明；資料截至 2026-11-08 | OK，一句見 F08 | 同上各段 | 「讓壺變小」在 F02 改寫後仍成立（容量確實變小，只是原因改說成「卡住」）。數字那句見 F08 |
| thumbnail.headline | 電量還有／電池已經老了 | OK | Apple 101575 | 與標題同一個主張 |
| thumbnail.sub | 還有百分之二十，手機卻黑掉 | OK | — | 小問的經歷；Apple 說低電量時更容易意外關機 |
