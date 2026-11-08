# 查核報告 2（sothatswhy-p11-old-battery）

- 查核者：Claude（第二輪獨立查核代理，未參與撰稿與第一輪）
- 日期：2026-11-08
- 方法：逐句讀第二版 `video.json` 的 179 句台詞（p001–p179），加上 YouTube 標題、說明與縮圖 headline／sub。對照 `claims.md` 的 C01–C20 與 `verify-1.md` 的 F01–F08，但不採用其中的引文，而是用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓下每個來源再讀原文：Apple〈iPhone battery and performance〉（101575）、〈Battery and performance of iPhone 11 and later〉（106348）、〈About Charge Limit and Optimized Battery Charging on iPhone〉（108055）、〈Why lithium-ion〉、〈Maximizing performance〉、〈Important safety information for iPhone〉；Google〈Understand your Pixel battery〉（15738128）、〈Get the most life from your Pixel battery〉（6090612）、〈Extended Repair Program for Pixel 7a〉（16043453）；Samsung IE〈Battery protection in One UI 6.1〉；Battery University BU-808、BU-808b、BU-903；Münster MEET〈Battery Aging〉。Apple 支援頁是用 JavaScript 載入，內文取自頁面內嵌的 `__ACGH_DATA__` JSON。Edge et al. 2021 經 OpenAlex 找到 Guelph 大學機構典藏的 CC-BY 全文 PDF（atrium.lib.uoguelph.ca，頁碼 8200–8221），用 pdftotext 轉文字，讀了摘要、SEI 一節（原理、觸發條件、後果）、正負回饋與結論。另外為了第二版新增或改寫的句子多開了兩頁：Apple〈If your iPhone or iPad gets too hot or too cold〉（118431）與 Apple〈Apple Service and Repair for iPhone Battery〉（support.apple.com/iphone/repair/battery-replacement）。
- 打不開的來源：pubs.rsc.org 的 Edge 2021 PDF 仍回 403，改讀上述機構典藏 PDF。其餘全部 200。
- 這一輪新找到、`claims.md` 沒寫的直接來源（不影響結論，建議補進 `claims.md` 與 `video.json` 的 sources）：
  1. Google 15738128 有一節〈Manage devices with a swollen battery〉：「Place the device on a table or countertop. Let it sit unused for several days until the battery naturally drains.」，不要「press on the cover glass or back cover」「pry open the device」「take the device apart or try to fix a swollen battery yourself」。這是 p167「鼓鼓的……別用也別充」的直接官方來源（放著不用、讓電自然放完，也就是不充電），比 C20 只引 Apple「懷疑損壞就停用」更貼。同節也寫「A swollen battery alone isn't a safety concern」，片中只說別用別充、告訴大人，沒有說它很危險，不衝突。
  2. Apple 118431：「Don't leave your device in a car, because temperatures in parked cars can exceed this range」，避免「Leaving your device in a car on a hot day」。p088「夏天停在大太陽底下的車子裡」現在有原句，不只是例子。同頁「Using … in very cold conditions … could cause your device to turn off. Battery life will return to normal when you bring your device back to higher ambient temperatures」支持 p132–p133。同頁把「games, or features, including camera apps」列為處理器吃重的使用，支持 p107 的例子。
  3. Apple 101575 的電池健康訊息：「An Apple Authorized Service Provider can replace the battery to restore full performance and capacity.」；同頁「replacing your device battery can help」。Apple 維修頁「We'll replace the battery for no extra charge if the capacity drops below 80%」（AppleCare 方案條件，片中不講）。Google 15738128「When the capacity is labeled as "Reduced," Google recommends replacing your battery.」這三句讓 p139 的承諾在 p165–p166 兌現有官方根據。
  4. Apple 108055 現在也寫「Optimized Battery Charging needs at least 14 days to learn your charging habits」。p148「有的手機公司說，大約要學兩個禮拜」原本依 Google「about 14 days」，兩家都對得上；片中仍只說「有的」，不比較品牌。
  5. Google 15738128 另寫「Avoid prolonged, 6 or more hours, exposure to high ambient temperatures more than 35℃」與「Charge your phone in a cool ambient, about 25℃ … and limit exposure to direct sunlight」。p090 的 35 度兩家都有；p160「別在大太陽底下充」有 Google 原句。
- 結論統計（台詞 179 句）：OK 179、FIX 0、NOT FOUND 0。另外標題、說明、縮圖 headline、縮圖 sub 共 4 項：OK 3、FIX 1（F09，說明一句）。
- 品牌：全片仍只說「手機公司」「有一家」「有的」「有些」，沒有比較品牌。
- 與官方保養說法是否衝突：沒有。p155–p156 對上 Apple「Charge your Apple lithium-ion battery whenever you want. There's no need to let it discharge 100% before recharging.」與 Google「Charge as much or as little as needed」。Google 要 Pixel 每第 10 次循環充滿一次以校正、Apple 設了 Charge Limit 時也會「occasionally charge to 100 percent」，都是充滿、不是先用光，跟「也不用特地先用光再充滿」不衝突。
- 安全判斷：第二版只留一句安全提醒 p167，加上 p039 請大人開設定、p093 擋住放冷凍庫、p165 請大人帶去換電池。「熱熱的」（p157，充電時正常變熱：Google「Your phone warms up when it's plugged in」；Apple 118431「These conditions are normal」）與「很燙」（p167，停用）分開了，F06 的混淆已消除。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F09 | youtube.description 第三段 | 也聊到手機怎麼自己照顧電池、為什麼想充就充，以及電池鼓起來或很燙時，要停用並告訴大人。 | FIX（說明答應了片中沒有的內容） | 第二版照盲評刪掉「不用教它認識壺」那句後，p155–p156 只說「想充就充，也不用特地先用光再充滿」，沒有講「為什麼」。說明寫「為什麼想充就充」，觀眾會等一個片中沒有的理由。事實本身沒錯（Apple〈Why lithium-ion〉、Google 6090612），只改措辭，不加新事實。**建議改成**：「也聊到手機怎麼自己照顧電池、充電時可以想充就充，以及電池鼓起來或很燙時，要停用並告訴大人。」 |

台詞沒有要改的句子。

## 二、第一輪 F01–F08 確認

| # | 第一輪建議 | 第二版現況 | 結論 | 依據 |
| --- | --- | --- | --- | --- |
| F01 | 「水垢是常被提到的主要原因之一。」 | p060 同句 | 已改，正確 | Edge 全文：「SEI layer growth is often quoted as one of the main degradation modes」；結論「five principal degradation mechanisms that are most commonly considered … These are SEI layer growth, lithium plating, …」。「之一」與「主要」都有原文 |
| F02 | 「水垢會把一些本來能存電的東西，卡在裡面。」 | p061 同句；p062「長得越厚，壺能裝的電就越少。」 | 已改，正確 | Edge：「Capacity is irreversibly lost due to otherwise cyclable lithium being trapped within the SEI」；BU-808b：鋰「permanently lodged on the anode」 |
| F03 | p076「較新的一批手機電池」、p078「設計成大約一千次循環後……」 | p073「有一家手機公司說，它較新的一批手機電池，」p074「在很理想的情況下，」p075「設計成大約一千次循環後，壺還有原來的大約八成大。」 | 已改，正確 | Apple 106348：「Batteries of iPhone 15 models and later are designed to retain 80 percent of their original capacity at 1000 complete charge cycles under ideal conditions」；「iPhone 14 models and earlier … 500」。101575 仍寫「iPhone 15 models」。「較新的」「設計成」「很理想的情況」都對上 |
| F04 | 「不要喔！冰起來也還是會老。」「手機公司說，用的時候最好在大約零度以上。」 | p093、p094 同句 | 已改，正確 | Apple〈Maximizing performance〉「work best at 32° to 95° F (0° to 35° C)」（使用）與「Storage temperature: -4° to 113° F (-20° to 45° C)」（存放）分開；Apple 118431 同樣分「designed for use」與「Store your device」。「冰起來也還是會老」：Edge「will grow even if the battery is not then used」；BU-808 表 3：0°C 存一年仍剩 98%／94% |
| F05 | 「所以它多半沒有壞，只是先關機保護自己。」 | p117「對，所以它多半沒有壞。」（後半刻意不用，因為 p114–p115 已說「手機會搶先一步，自己關機，保護裡面的零件」） | 部分採用，結果仍正確 | Apple 101575：「the system will perform a shutdown to preserve these electronic components. While this shutdown is intentional from the device perspective, it might be unexpected by the user.」；意外關機多發生在「low state of charge, a higher chemical age, or … colder temperatures」，小問的情境三項都有，所以「多半沒有壞」有根據且有保留。「插上電就能再打開」已整句拿掉，全片沒有其他句子暗示一定能開回來。保護的意思由 p114–p115 講過，前後連起來跟建議句等價 |
| F06 | 小問「充電時它熱熱的，」 | p157 同句 | 已改，正確 | Google 6090612「Your phone warms up when it's plugged in」；Apple 118431 變熱的情況「These conditions are normal」；p167 的「很燙」才停用 |
| F07 | 「先別怪它，它多半是在保護自己。」 | p175 同句 | 已改，正確 | 同 F05 |
| F08 | 「片中的數字大多是手機公司說明裡的大約數字，「將近三年」是我們自己粗算，」 | 說明第四段同句 | 已改，正確 | 片中數字：百分之二十（小問看到的）、一千次與八成（Apple）、將近三年（粗算）、兩成（100−80）、三十五度與零度（Apple、Google）、八成（Apple、Samsung）、兩個禮拜（Google、Apple）。「大多」成立 |

## 三、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p008 | 冷天在公園用媽媽的舊手機拍松鼠，還有百分之二十，一按拍照就黑掉；剛買時一整天都有電；是不是壞了 | OK | — | 角色經歷與問題。「百分之二十」是小問看到的數字 |
| p009 | 先別急；很多舊手機都可能這樣突然關機 | OK | Apple 101575 | 「You're more likely to experience unexpected shutdowns when your battery has a low state of charge, a higher chemical age, or when you're in colder temperatures.」有「可能」 |
| p010–p013 | 為什麼舊的才會；電池已經老了；電量還有怎麼會老 | OK | Apple 101575 | 「A battery's impedance can increase if a battery has a higher chemical age.」 |
| p014 | 很多人以為電量還多，電池就還好 | OK（歸納） | — | 轉向觀眾，不是事實主張 |
| p015–p016 | 黑掉有個想不到的原因；電池裡正偷偷長著一層東西 | OK | Edge 2021；BU-808b | 「the thickness of the SEI layer increases … as the cell ages」 |
| p017–p021 | 承諾與全片問題；先想想水壺 | OK | — | — |
| p022–p030 | 電池像裝電的水壺；電是水；百分比是現在還剩幾分滿；用電是喝水、充電是裝滿 | OK（比喻） | — | claims.md 已標明比喻 |
| p031–p036 | 充到百分百不一定跟新的一樣多；壺有多大百分比不會說；舊壺比新的小 | OK | Apple 101575 | 「As lithium-ion batteries chemically age, the amount of charge they can hold diminishes」；maximum capacity「relative to when it was new」 |
| p037–p038 | 難怪充滿也撐不了一整天 | OK | Apple 101575 | 「resulting in shorter amounts of time before a device needs to be recharged」 |
| p039 | 請大人打開設定找找看 | OK（安全） | — | 由大人操作 |
| p040–p041 | 很多手機有「最大容量」或「電池健康度」，說的是壺現在還剩多大 | OK | Apple 101575／106348；Google 15738128 | Apple「maximum capacity—the measure of battery capacity relative to when it was new」；Google「Battery health … an estimate of your device's remaining battery capacity compared to its original capacity」。「很多」不是「全部」 |
| p042–p045 | 跟全新時比、自己估的，不一定很準 | OK | Google 15738128 | 「Capacity is estimated by the battery's fuel gauge」；「Initial battery health values are based on lab results and may differ from your actual battery state」 |
| p046–p048 | 百分比也是估的：看倒得多有力、數倒出去多少，大約算出來 | OK（比喻，附註） | BU-903；Apple 108055 | 電壓法「simple, but it can be inaccurate」；庫侖計數「measuring the in-and-out-flowing current」；Apple「maintain accurate battery state-of-charge estimates」。比喻只講流出，來源是進出都數，簡化可接受 |
| p049–p053 | 壺怎麼變小；壺裡慢慢長水垢；熱水壺的白白硬硬是水垢 | OK（比喻＋常識） | — | — |
| p054–p056 | 不是真的水垢，是很像水垢的薄膜；用越久長越厚 | OK | Edge 2021；BU-808b | 「the thickness of the SEI layer increases … as the cell ages」；「The film gets thicker」 |
| p057–p060 | 不只水垢；科學家找到好幾種原因；水垢是常被提到的主要原因之一 | OK | Edge 2021 | 「Five principal and thirteen secondary mechanisms」；「often quoted as one of the main degradation modes」（F01） |
| p061–p062 | 水垢把能存電的東西卡在裡面；越厚能裝的電越少 | OK | Edge 2021；BU-808b | 見 F02 |
| p063–p066 | 刷掉不就好；刷不到、長在最裡面、長了退不掉 | OK（比喻＋事實） | Edge 2021；BU-808b | 「irreversibly lost」；「a phenomenon that is irreversible」。「最裡面」是比喻（SEI 長在電池內部的負極表面） |
| p067–p069 | 充一次就長一次嗎；差不多，不過手機算的是一次循環 | OK（附註） | BU-808b | 「the SEI layer grows as the battery cycles」。「差不多」略鬆，p086 接著補上不用也會長 |
| p070–p071 | 喝掉一整壺才算一次；半壺加半壺 | OK | Apple〈Why lithium-ion〉；Google 15738128 | 「use 75% … one day … 25% the next day … add up to one charge cycle」；「100% charge to 50% … calculated as 0.5 cycles」 |
| p072–p075 | 喝很多次以後；較新的一批手機電池，理想情況下設計成大約一千次後還有大約八成 | OK | Apple 106348 | 見 F03。「大約」對上 Google 15738128 同類機型的「about 1000」 |
| p076–p079 | 要用好幾年吧；我們自己粗算，每天剛好一整壺，大約將近三年 | OK（自行計算，已標明） | — | 1000 ÷ 365 ≈ 2.74 年；前提與「我們自己粗算」都說出來 |
| p080–p083 | 才少了大約兩成；那是很理想的情況，要看怎麼用、放哪裡 | OK | Apple 106348；Google 15738128 | 100% − 80% = 20%，有「大約」；Google「Your battery's actual lifespan depends on usage patterns and other factors」；Apple chemical age 包含「how it was cared for」 |
| p084–p086 | 不充電就不會長水垢嗎；就算收在抽屜裡不用，水垢也會慢慢長（第二版合併句） | OK | Edge 2021；Apple 101575 | 「The SEI begins to form as soon as the NE is lithiated … and will grow even if the battery is not then used」；「it grows even when the cell is at rest at high SoC, albeit at slower rates (this contributes to calendar ageing)」；Apple chemical age「is more than just the passage of time」。「慢慢」對上「slower rates」 |
| p087 | 放在很熱的地方，水垢長得特別快 | OK | Edge 2021；Apple〈Maximizing performance〉；BU-808 | 「high temperatures increase diffusion rates and hence also the SEI growth rate」；「Even storing a battery in a hot environment can damage it irreversibly」；BU-808 表 3：40% 電存一年，25°C 剩 96%、40°C 剩 85% |
| p088 | 像夏天停在大太陽底下的車子裡 | OK | Apple 118431 | 「Don't leave your device in a car, because temperatures in parked cars can exceed this range」；「Leaving your device in a car on a hot day」 |
| p089–p090 | 多熱算太熱；手機公司說大約超過三十五度 | OK | Apple〈Maximizing performance〉；Apple 118431；Google 15738128 | 「avoid exposing your device to ambient temperatures higher than 95° F (35° C), which can permanently damage battery capacity」；Google「more than 35℃」。有「大約」 |
| p091–p094 | 放冷凍庫就不會老吧；不要喔，冰起來也還是會老；用的時候最好在大約零度以上 | OK | 見 F04 | — |
| p095–p097 | 壺變小只是比較快沒電，怎麼會黑掉；水垢也把壺嘴慢慢堵窄 | OK | Edge 2021；BU-808b；Apple 101575 | SEI 的各種效應「increase the overall impedance of cells, leading to power fade」；「resulting in an increase of internal resistance」；Apple「peak power … might decrease」 |
| p098–p101 | 壺嘴寬不寬決定一次倒多快；窄壺嘴倒一大杯要等好久 | OK（比喻） | Apple 101575 | 對應「impedance」與「instantaneous power delivery」 |
| p102–p104 | 小口喝窄一點沒關係；平常慢慢用電來得及 | OK | Apple 101575 | 「A battery with a high impedance might not be able to provide sufficient power to the system that needs it」，問題在瞬間大量用電 |
| p105–p108 | 開相機拍照、玩很忙的遊戲，一下子要很多電 | OK（附註：例子） | Apple 101575；Apple 118431 | 101575 效能管理極端時「the camera flash will be disabled」；118431 把「graphics-intensive or processor-intensive apps, games, or features, including camera apps」列為吃重的使用 |
| p109–p112 | 壺嘴太窄倒不出來，零件拿不到夠多的電，就沒辦法好好工作 | OK | Apple 101575 | 「Electronic components require a minimum voltage to properly operate」 |
| p113–p117 | 不是壞掉；手機搶先自己關機保護零件；原來是它自己決定的；多半沒有壞 | OK | Apple 101575 | 見 F05 |
| p118–p122 | 百分比是不是騙人；還記得百分比是估的；它沒騙人，壺裡多半真的還有水，只是壺嘴太窄 | OK | BU-903；Apple 101575 | 電壓在大量用電時「drop to a greater degree」，電量不是零也會關機。有「多半」 |
| p123–p125 | 水、壺多大、壺嘴多寬是三件事；電量多不代表壺還大、壺嘴還寬 | OK（歸納） | Apple 101575 | 頁面分開講 state of charge、maximum capacity、peak power |
| p126–p129 | 電多的時候怎麼不會黑掉；水多倒起來比較有力，水少再碰上窄壺嘴就容易倒不夠 | OK（比喻） | Apple 101575 | 「A battery's impedance will temporarily increase at a low state of charge … When coupled with a higher chemical age, the impedance increase will be more significant.」 |
| p130–p135 | 天冷壺嘴暫時變窄，回到暖和就好一些；難怪在冷冷的公園黑掉 | OK | Apple 101575；Apple 118431；Apple〈Maximizing performance〉 | 「impedance will temporarily increase … in a cold temperature environment」；「For a low battery state of charge and colder temperatures, performance-management changes are temporary」；118431「could cause your device to turn off. Battery life will return to normal when you bring your device back to higher ambient temperatures」 |
| p136–p138 | 怎麼讓電池老得慢；很多事手機已經在幫你做 | OK | Apple 108055；Google 6090612；Samsung | 三家都有內建的電池保護 |
| p139 | 媽媽那支舊手機，等一下也有辦法 | OK（承諾，已兌現） | Apple 101575；Google 15738128 | 在 p161–p166 兌現：換電池。Apple「An Apple Authorized Service Provider can replace the battery to restore full performance and capacity」；Google「Google recommends replacing your battery」 |
| p140–p142 | 電池不喜歡一直裝得滿滿的放很久，那樣水垢也長得比較快 | OK（附註） | Samsung；Google 6090612；Apple〈Maximizing performance〉；Edge 2021；BU-808 | Samsung「Keeping your battery at a full 100% charge for a long time can reduce its lifespan」；Google「isn't at 100% for a long time. This can strain the battery long term」；Edge 把「at rest at high SoC」列為 SEI 增長的觸發條件；BU-808 表 3：25°C 存一年，40% 電剩 96%、100% 剩 80%。附註：滿電久放的損耗也有正極的機制（BU-808b 的電解液氧化、Edge 的高 SoC 正極劣化），片中只講水垢並用「也」字，是簡化不是錯 |
| p143–p145 | 很多手機學你的習慣，先充到大約八成，停一下，快起床再充滿 | OK | Apple 108055；Samsung；Google 6090612 | Apple「delay charging past 80 percent in certain situations … learn your daily charging routine … fully charged when unplugged」；Samsung Adaptive「Use Maximum while you're asleep」（Maximum 停在 80%）、「charges to 100% an hour before you wake up」；Google「charge to 100% one hour before you unplug」 |
| p146–p148 | 它會記住你什麼時候拔線；有的手機公司說大約要學兩個禮拜 | OK | Google 6090612；Apple 108055 | Google「about 14 days」；Apple「at least 14 days」。有「大約」與「有的」 |
| p149–p151 | 要不要自己盯著到八成拔；不用那麼辛苦，交給手機 | OK（意見） | Apple 108055；Google 6090612 | 與官方的自動功能一致 |
| p152 | 有些手機能設定最多只充到八成 | OK | Apple 108055；Google 6090612；Samsung | Charge Limit「between 80 percent and 100 percent」；「limit charging of your phone to 80%」（Pixel 6a 以後）；Maximum「stop charging when it reaches 80%」。設定值，不加「大約」可以 |
| p153–p156 | 要用到完全沒電才能充嗎；不用，想充就充，也不用特地先用光再充滿 | OK | Apple〈Why lithium-ion〉；Google 6090612；BU-808 | 「Charge … whenever you want. There's no need to let it discharge 100% before recharging」；「You don't need to teach your phone how much capacity the battery has by going from full to zero charge or zero to full charge」；BU-808「the battery does not need periodic full discharge cycles」。Google 第 10 次循環充滿與 Apple 偶爾充到 100% 都是充滿、由手機自己做，不是先用光，不衝突 |
| p157–p158 | 充電時它熱熱的，要怎麼辦 | OK | Google 6090612 | 見 F06 |
| p159–p160 | 還記得熱會讓水垢長得快嗎；充電時先把手機殼拿掉，也別在大太陽底下充 | OK | Edge 2021；Apple〈Maximizing performance〉；Google 15738128 | 回呼 p087：「high temperatures increase … the SEI growth rate」。Apple「Charging your device when it's inside certain styles of cases may generate excess heat, which can affect battery capacity. If you notice that your device gets hot when you charge it, take it out of its case first」；「Charging the device in high ambient temperatures can damage it further」；Google「Charge your phone in a cool ambient … and limit exposure to direct sunlight」。回呼的因果（熱→變老快→降溫）有來源 |
| p161–p164 | 媽媽的舊手機有什麼辦法；水垢退不掉，壺變不回原來那麼大 | OK | Edge 2021；Apple 101575 | 「irreversibly lost」；「all rechargeable batteries are consumables … eventually needing to be replaced」 |
| p165–p166 | 真的太舊了，請大人帶去，讓專業的人換一顆新電池 | OK | Apple 101575；Apple 安全資訊；Google 15738128 | 「An Apple Authorized Service Provider can replace the battery to restore full performance and capacity」；「An iPhone battery should only be repaired by a trained technician」；Google 容量低於 80% 或達到額定循環數時「we recommend that you replace your battery」。「真的太舊了」對上這兩個門檻，不講數字可以 |
| p167 | 要是它鼓鼓的、很燙，就別用也別充，馬上告訴大人 | OK（安全） | Google 15738128；Google 16043453；Apple 安全資訊；Apple 118431 | 鼓脹：Google「Let it sit unused for several days until the battery naturally drains」，不要按壓、撬開或自己修；Pixel 7a 頁「back cover might be bulging」「we recommend you stop using the device」。很燙：Apple「If you suspect damage … discontinue use of iPhone, as it may cause overheating or injury」；118431 過熱時「Charging … slows or stops」。「別充」有 Google 原意（放著讓電自然放完），「告訴大人」是給小孩的安全說法 |
| p168–p173 | 那天發生什麼事；小問自己說：拍照要大口喝電、舊壺嘴太窄、天氣又冷，手機就先關機保護自己 | OK | 同上各段 | 與 p095–p135 一致 |
| p174–p175 | 下次手機突然黑掉，先別怪它，它多半是在保護自己 | OK | Apple 101575 | 見 F07 |
| p176–p179 | 原來如此；留言題；訂閱 | OK | — | 片尾 |
| youtube.title | 電量還有，手機電池為什麼已經老了？ | OK | Apple 101575 | 問句，前提正確 |
| youtube.description | 小問的經歷；水壺比喻；水垢讓壺變小、壺嘴變窄；倒不夠快就先關機保護零件；照顧電池；鼓起來或很燙要停用並告訴大人；比喻與 AI 插圖說明；數字說明；資料截至 2026-11-08 | OK，一句見 F09 | 同上各段 | 數字那句 F08 已改，成立 |
| thumbnail.headline | 電量還有／電池已經老了 | OK | Apple 101575 | 與標題同一個主張 |
| thumbnail.sub | 還有百分之二十，手機卻黑掉 | OK | — | 小問的經歷；Apple 說低電量時更容易意外關機 |
