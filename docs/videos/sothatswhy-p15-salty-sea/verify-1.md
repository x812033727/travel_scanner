# 查核報告 1（sothatswhy-p15-salty-sea）

- 查核者：Claude（獨立查核代理，未參與撰稿）
- 日期：2026-11-07
- 方法：逐句讀 `video.json` 的 206 句台詞（p001–p206），加上 YouTube 標題、說明與縮圖 headline／sub。對照 `claims.md` 的 C01–C24，但不採用其中的引文，而是用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓下每個來源，轉成文字後讀原文：NOAA whysalty／riversnotsalty／drinksw、USGS why-ocean-salty／saline-water-and-salinity／how-much-water-there-earth、NASA Earth Observatory A Measure of Salt／Global Accounting of Earth's Rivers、LibreTexts 8.9 Residence Time、Gale〈Ocean Chemical Processes〉（encyclopedia.com）、HELCOM Salinity（archive.iwlearn.org）、NSIDC Science of sea ice、觀光署七股鹽山、水產試驗所 107 年度監測報告 PDF（pdftotext），以及 Wikipedia Dead Sea（raw wikitext）。claims.md 要求補的來源另外找了：Wikipedia Red Sea、Baltic Sea（raw wikitext），以及中文維基〈鹽田〉與英文維基〈Salt evaporation pond〉（曬鹽方法）。
- 打不開的來源：沒有。claims.md 只看到搜尋摘要的 Britannica（紅海 41 psu、河水以碳酸氫鈣為主）這次沒有再開，因為 Wikipedia Red Sea（平均 40‰）與 Gale 表 1（河水 HCO₃⁻ 0.86、Ca²⁺ 0.33 mM，是河水最多的兩種離子）已經能支撐同樣的句子。NOAA COPEPOD 時序沒有開，HELCOM 與 Wikipedia 已足夠。
- 對 claims.md 的更正：C07 說 LibreTexts [9] 寫了「蒸發移除水、留下鹽」，原頁沒有這句；同樣意思在 Gale："Because the water added to the ocean evaporates but the dissolved salts do not"。結論不變，出處要改成 Gale。
- claims.md 請查核者判斷的項目：C04（OK，見第二節 p040–p041）、C06（OK，自行相除 1,338,000,000 ÷ 37,411 ≈ 35,765 年）、C11（OK，中文維基〈鹽田〉找到說明）、C13／C17（原文都是 "probably"，見 F06）、C14（見 F02、F03）、C19（OK，Wikipedia 有 "no significant rivers or streams"）、C20（「天氣涼」沒有來源，見 F07）、C21（OK，NASA 明寫 melting ice）、C23（OK）。
- 結論統計（台詞 206 句）：OK 197、FIX 9（共 7 項）、NOT FOUND 0。另外標題、說明、縮圖 headline、縮圖 sub 共 4 項：OK 4。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p015（所長） | 海底沒有鹽山。 | FIX（說得比來源絕對） | NOAA whysalty："Salt domes also contribute to the ocean's saltiness. These domes, vast deposits of salt … are found underground and undersea around the world."，同頁的配圖說明還有一處海底的 brine seep，"formed from super-saline water flowing from under the seafloor"。所以海底真的有大片鹽層，也有地方在滲出很鹹的水，只是它們不是主要來源："Rocks on land are the major source of salts dissolved in seawater."。小問的錯在「主要靠海底冒鹽」，不在「海底有鹽」。**建議改成**：「海裡的鹽，大部分是從陸地來的。」（14 字）。p016 與 p133「說對了一點點」照留，接得上，而且更準 |
| F02 | p116（所長） | 對。牠們死掉以後，殼就沉到海底， | FIX（珊瑚不會「沉」下去） | p113 的主詞是「貝殼和珊瑚」。珊瑚本來就固定長在海底，骨骼是留在原地，不是沉下去；Gale 講沉下去的是浮游生物的殼（"These hard particles eventually fall toward the ocean floor, where they are buried in the sediment and thus removed from sea water for many millions of years"）。改成「留在」，貝殼與珊瑚兩種都說得通。**建議改成**：「對。牠們死掉以後，殼就留在海底，」（15 字）。p117 照留 |
| F03 | p120（所長） | 被拿走得最快。 | FIX（說得比來源絕對） | Gale 表 2 的滯留時間：Ca²⁺ 約 100 萬年，Na⁺ 8,000 萬年，Mg²⁺ 1,300 萬年，K⁺ 1,200 萬年，SO₄²⁻ 1,000 萬年。在主要成分裡鈣確實最短，但表上的微量元素被拿走得快得多（Fe 約 50 年、Al 約 600 年），「最快」不成立。片中要比的只是「比鹽快」，這有來源支撐（鈣約 100 萬年，鈉約 8,000 萬年、氯約 8,700 萬年，見 LibreTexts）。p119「河水帶來的，有很多正是做殼的材料」OK：Gale 表 1 河水最多的是 HCO₃⁻ 與 Ca²⁺。**建議改成**：「被拿走得比鹽快很多。」（10 字） |
| F04 | p129（所長） | 全世界的海水，大約一千到兩千萬年， | FIX（估計說成定論） | USGS："Estimates of the amount of hydrothermal fluids now flowing from these vents indicate that the entire volume of the worlds oceans **could** circulate through hydrothermal vent systems every 10-20 million years."；Gale 也說 "It is difficult to estimate … a reasonable estimate of once every 10 million years"。p130 的「就會」把估計說成了確定。加上「科學家估計」就好，數字不動。**建議改成**：「科學家估計，全世界的海水大約一千到兩千萬年，」（21 字）。p130 照留 |
| F05 | p135（所長） | 很久很久以前，有些淺淺的海被曬乾了， | FIX（多出沒有來源的細節） | Gale："Evaporation of isolated bodies of sea water accounts for removal of large amounts of salt from the ocean. Salt deposits occur through the geologic record as layers of gypsum, rock salt …"。來源說的條件是「被隔開的海水」，沒有說「淺」（Wikipedia Red Sea 也提到紅海曾經整片蒸乾，"evaporated to an empty hot dry salt-floored sink"，那並不淺）。重點是跟大海斷開，河與海水補不進來，才會被曬乾。這也跟後面的死海段落（p183「水流不出去」）接得上。**建議改成**：「很久很久以前，有些跟大海隔開的海水被曬乾了，」（20 字）。p136 照留 |
| F06 | p143–p144（所長） | 海洋學家說，現在的海，／已經沒有再越變越鹹了。 | FIX（"probably" 被拿掉了） | NOAA riversnotsalty 原文："About the same tonnage of salt from ocean water **probably** is deposited as sediment on the ocean bottom and thus, yearly gains **may** offset yearly losses. In other words, the ocean today **probably** has a balanced salt input and output (and so the ocean is no longer getting saltier)." 括號裡的那句是建立在兩個 probably 上的。Gale 的結論段也說 "the composition of sea water may have changed over the past 700 million years"。保留「大概」。p146「可能只有一點點鹹」對上 "probably only slightly salty"，OK；p147 有 p146 的「可能」帶著，可以留。**建議改成**：p143「海洋學家認為，現在的海，」（12 字）；p144「大概已經沒有再越變越鹹了。」（13 字） |
| F07 | p165–p166（所長） | 北邊的波羅的海剛好相反：天氣涼，／很多河流進來，雨也多。 | FIX（一個原因沒有來源） | HELCOM："The brackish water of the Baltic Sea is a mixture of sea water from the North Sea and fresh water from rivers and rainfall."；Wikipedia Baltic Sea："More than 250 streams drain a basin … Additional fresh water comes from the difference of precipitation less evaporation, which is positive."，以及 "abundant freshwater runoff … combined with the shallowness of the sea itself"。兩個來源都沒有把「天氣涼」列成原因。來源寫的是「下的雨比蒸發走的多」，這句可以直接放進熬湯的比喻（爐火小、加水多），不用另外補一個沒有來源的因果。**建議改成**：p165「北邊的波羅的海剛好相反，」（12 字）；p166「很多河流進來，下的雨也比曬走的多。」（17 字）。p167 小問「一直加水，湯就淡了！」照留 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p012 | 海邊喝到海水好鹹；所長也喝過；河一直流進海；河水淡、海為什麼沒被沖淡 | OK | — | 開場、角色玩笑與問題。p011「每天都把好多淡水倒進海裡」：NASA 全球河川入海年流量 37,411 km³ |
| p013–p014 | 小問猜海底有鹽山一直冒鹽 | OK（錯猜） | — | 由 p015 糾正，見 F01 |
| p015 | 海底沒有鹽山 | 見 F01 | — | — |
| p016–p021 | 海底有個祕密；河水真的沒鹽嗎；把海想成一鍋熬的湯 | OK | — | 鋪陳與比喻。「熬湯」的方向與 Gale "Because the water added to the ocean evaporates but the dissolved salts do not" 一致 |
| p022–p028 | 從山上的雨講起；河水其實有鹽，只是少到嘗不出來；雨水帶一點點酸，慢慢啃石頭 | OK | NOAA whysalty；USGS why-ocean-salty | "Rainwater that falls on land is slightly acidic, so it erodes rocks."；USGS "slightly acidic due to carbonic acid"。「啃」是比喻 |
| p029–p032 | 啃得很慢；石頭裡的小東西溶進水裡，跟著河流下山 | OK | NOAA whysalty；USGS | "This releases ions that are carried away to streams and rivers that eventually feed into the ocean."；USGS "carries salts and minerals along in a dissolved state as ions" |
| p033–p035 | 河水不鹹，因為一直被新的雨水換掉 | OK | NOAA riversnotsalty | "Rain replenishes freshwater in rivers and streams, so they don't taste salty."「鹽還來不及變多」是白話推論，方向對 |
| p036–p039 | 像糖溶在水裡，看不見、嘗不太出來，但真的在 | OK | USGS | 溶解成離子。糖是比喻，只比「看不見」，沒說鹽就是糖 |
| p040–p041 | 我們叫淡水的那種水，鹽連海水的三十分之一都不到 | OK（附註：這是定義） | USGS saline-water-and-salinity | "Fresh water - Less than 1,000 ppm"；"ocean water contains about 35,000 ppm of salt"。1,000／35,000 ≈ 1／35。台詞說的是「我們叫淡水的那種水」，也就是定義的上限，不是說每條河都量過，措辭恰當 |
| p042–p048 | 全世界的河一年大約帶四十億公噸溶掉的鹽進海；一點點乘上很多就不少 | OK | NOAA riversnotsalty | "Throughout the world, rivers carry an estimated four billion tons of dissolved salts to the ocean annually." 來源沒寫是英噸還是公噸（兩者約差一成），有「大約」，數量級不變 |
| p049–p054 | 河一直倒，海沒有滿；海如果是空的，光靠河倒大約三萬多年就滿 | OK（附註：自行換算） | USGS how-much-water；NASA rivers | 海洋 1,338,000,000 km³ ÷ 37,411 km³／年 ≈ 35,765 年。沒有來源直接這樣說，但用了「如果」「光靠」「大約」，是清楚的假設題 |
| p055–p061 | 出口在天上；太陽曬，水變成水氣；成雲、下雨、回到河、再進海 | OK | USGS how-much-water（水循環）；NOAA riversnotsalty | 水循環。「排水孔」是小問的錯猜，所長立刻改正 |
| p062–p064 | 地球的水一百份裡大約九十六份多在海裡 | OK | USGS how-much-water | "the oceans hold about 96.5 percent of all Earth's water" |
| p065–p067 | 杯子裡的水很有可能以前在海裡 | OK | LibreTexts 8.9；USGS | 水會循環，有「很有可能」「說不定」帶著 |
| p068–p071 | 鹽沒有跟著飛；太陽只搬得動水；水曬走鹽留下 | OK | Gale | "the water added to the ocean evaporates but the dissolved salts do not"。「搬」是比喻 |
| p072–p074 | 在家放一小碟鹽水曬幾天，留下一圈白鹽 | OK | Gale（蒸發後溶質留下）；中文維基〈鹽田〉 | 日曬蒸發，不用火也不用喝，安全 |
| p075–p081 | 像熬湯越熬越鹹；河水是加進去帶一點鹽的水，太陽是爐火；雨不是鹹的 | OK | Gale；NOAA riversnotsalty | 比喻與前面一致。p081「被太陽熬出來的淡水」是簡化（陸地上也有水蒸發），方向對 |
| p082–p087 | 海水結冰把鹽擠到旁邊的海水；放了好幾年的老海冰幾乎嘗不到鹹味 | OK | NSIDC | "Because salt doesn't freeze, the crystals expel salt into the water"；"Sea ice that is four or more years older is nearly free of brine."。台詞特別說「老海冰」，避開了新冰 "tends to be very salty" 的狀況，很好 |
| p088–p091 | 台灣以前也這樣做鹽；七股是台灣最大的曬鹽場；海水引進鹽田讓太陽曬乾；曬到二〇〇二年停 | OK | 觀光署七股鹽山；中文維基〈鹽田〉；英文維基 Salt evaporation pond | 「七股鹽場過去是臺灣最大的曬鹽場」「民國91年（西元2002年）5月廢曬，結束臺灣338年曬鹽歷史」。方法：〈鹽田〉「利用太陽能蒸發鹵水中的水分，以取得鹽的結晶」；英文 "seawater or brine is fed into artificially created ponds from which water is drawn out by evaporation"。p089「就有」接著 p091「才停」，不會讓人以為現在還在曬 |
| p092–p093 | 廚房的鹽也有海裡來的；曬出來的海鹽就是海裡留下的 | OK | 中文維基〈鹽田〉；Gale | 「也有」沒說全部都是（Gale：蒸發岩也 "mined for table salt"） |
| p094–p102 | 水只是來作客；一滴水平均在海裡待三千年左右；鹽可以住幾千萬年 | OK | LibreTexts 8.9；Gale 表 2 | "a water molecule spends 3,100 years … before it's evaporated"；chloride "about 87 million years"、sodium "about 55 million years"；Gale 鈉 80 × 10⁶ 年。「左右」「幾千萬年」涵蓋來源之間的差距 |
| p103–p107 | 鹽也會搬走；搬家的地方在海底 | OK | NOAA riversnotsalty；Gale | 沉積與熱泉，見下 |
| p108–p112 | 溶著的東西慢慢沉下去，跟泥沙變成一層層泥和石頭；鍋巴把東西帶出湯 | OK | NOAA riversnotsalty；Gale | NOAA "probably is deposited as sediment on the ocean bottom"；Gale 顆粒 "adsorb dissolved material from sea water and cause them to be buried in ocean floor sediments, thus removed from the ocean"。鍋巴是比喻，台詞用「一些東西」，沒有說得過頭 |
| p113–p115 | 貝殼和珊瑚拿做殼的材料蓋家；殼是用海水裡的東西蓋的 | OK | Gale；NOAA whysalty | Gale "remove calcium or silicon from sea water to make calcium carbonate shells"；NOAA "Many of the dissolved ions are used by organisms in the ocean and are removed from the water." |
| p116 | 死掉以後殼就沉到海底 | 見 F02 | — | — |
| p117–p119 | 材料離開海水；貝殼在幫海搬東西；河水帶來的有很多是做殼的材料 | OK | Gale 表 1、生物段 | 河水最多的是 HCO₃⁻ 與 Ca²⁺；殼 "removed from sea water for many millions of years" |
| p120 | 被拿走得最快 | 見 F03 | — | — |
| p121–p123 | 為什麼不把鹽也拿走；做殼用不到這種鹽；所以留最多的是跟廚房鹽一樣的東西 | OK（附註） | Gale；NOAA whysalty | 殼是碳酸鈣或矽，用不到鈉與氯，這句公平。完整的原因還包括鈉、氯「很好溶、不容易反應」（Gale："Elements with long residence times … tend to be very soluble in sea water"），台詞只講了生物這一半，但沒有講錯；NOAA "Others are not removed, so their concentrations increase over time" 支撐「留在海裡最多」 |
| p124–p125 | 溶著的小東西一百份裡大約八十五份是組成這種鹽的兩種 | OK（附註：來源數字不同） | NOAA whysalty | "chloride and sodium. Together, they make up around 85 percent of all dissolved ions"。USGS 寫 "over 90%"，片中用「大約八十五」跟著 NOAA，可以 |
| p126–p128 | 海底有很燙的熱泉；海水鑽進石頭縫被煮熱再噴出 | OK | NOAA whysalty；USGS | "Ocean water seeps into cracks in the seafloor and is heated by magma … released through vents in the seafloor" |
| p129 | 一千到兩千萬年 | 見 F04 | — | — |
| p130–p134 | 整個鑽過一次；海底真的在冒東西；鹽山說對一點點；熱泉帶進一些、也留下一些在石頭裡 | OK | USGS；Gale；NOAA whysalty | USGS "some of the dissolved salts react with the rock and are removed from seawater"；Gale "loses all its O₂ and all its Mg … gains Ca, Si, Fe, and Mn"；NOAA "hydrothermal fluids" 也是鹽的來源之一 |
| p135 | 淺淺的海被曬乾 | 見 F05 | — | — |
| p136 | 留下厚厚的鹽層，埋進地底下 | OK | Gale | "Salt deposits occur through the geologic record as layers of gypsum, rock salt …" |
| p137–p142 | 河送進來的鹽海底也一直在收；水從天上走、鹽從鍋底走；一邊加一邊結鍋巴，湯一直差不多一樣鹹 | OK | NOAA riversnotsalty；Gale | "yearly gains may offset yearly losses"；Gale "steady state — that is, operating so that the input of salt equals the output"。「差不多」恰當 |
| p143–p144 | 海洋學家說現在的海已經沒有再越變越鹹 | 見 F06 | — | — |
| p145–p147 | 剛出現的海可能只有一點點鹹；後來越來越鹹，直到進出差不多才停 | OK | NOAA riversnotsalty | "the primeval seas were probably only slightly salty. But over time … the ocean has become saltier." p147 是簡化，前一句的「可能」帶著，可留 |
| p148–p151 | 鹽全部鋪在陸地上大約四十層樓厚 | OK | USGS why-ocean-salty | "By some estimates … it would form a layer more than 500 feet (166 meters) thick, about the height of a 40-story office building"。片中不唸公尺，避開頁面 500 英尺與 166 公尺不一致的問題 |
| p152–p158 | 每片海不太一樣；平均一公斤大約三十五公克；連在一起但各地的火和水不同 | OK | NOAA whysalty；NASA A Measure of Salt；NOAA whysalty | "average salinity is about 35 parts per thousand"；NASA "30 to 40 grams per kilogram, with 35 grams being the average"；"varies with temperature, evaporation, and precipitation" |
| p159–p163 | 紅海旁邊是沙漠、太陽大、很少下雨、幾乎沒有河；比平均多大約五公克 | OK | Wikipedia Red Sea；NASA A Measure of Salt | "between arid land, desert and semi-desert"；"rainfall … extremely low, averaging 60 mm per year"；"no significant rivers or streams drain into the sea"；平均 40‰，40 − 35 = 5。NASA "strong evaporation and other processes do make the Red and Mediterranean Seas saltier"。C19 的疑問可結案 |
| p164 | 有沒有很淡的海 | OK | — | 問題 |
| p165–p166 | 波羅的海：天氣涼、河多、雨多 | 見 F07 | — | — |
| p167–p169 | 一直加水湯就淡；最北邊一公斤只有幾公克鹽，嘗起來淡淡的 | OK | HELCOM；Wikipedia Baltic Sea | "1–2 PSU in the northernmost Bothnian Bay and the easternmost Gulf of Finland"；Wikipedia 波的尼亞灣 "around 0.3%"。「幾公克」涵蓋 1–3。「嘗起來淡淡的」沒有叫孩子去喝，不構成安全問題 |
| p170–p172 | 很冷的北邊南邊，冰融成的淡水流進海，海水比較淡 | OK | NASA A Measure of Salt；NSIDC | NASA "significantly fresher waters appear … in the icy high latitudes"、"runoff from rivers and melting ice does make water fresher"；NSIDC "in polar regions, it may be less than 30 PSU"。C21 可結案 |
| p173–p175 | 河流進海的地方附近海水淡一點 | OK | NASA A Measure of Salt | "Rivers such as the Amazon carry tremendous amounts of fresh runoff from land and spread plumes far into the sea." |
| p176–p180 | 台灣附近一公斤大約三十四公克多，跟平均差不多；夏天雨多河水多，近岸淡一點 | OK（附註：量測值） | 水產試驗所 107 年度報告 | 春季「33.72~34.78psu」；夏季「降雨量高河川淡水輸入較多，在較近岸測站有低鹽水出現」「31.35~34.35psu」。「平常」「大約」「多」恰當 |
| p181–p185 | 死海其實是湖，水流不出去只能蒸發；鹹快十倍；人躺上去會浮起來 | OK | Wikipedia Dead Sea | "an endorheic lake, meaning there are no outlet streams"；"342 g/kg … 9.6 times as salty as the ocean"（2011 年），另一處寫 "fluctuates around 31.5%"（約 9 倍）；「快十倍」兩者都涵蓋。"Anyone can easily float in the Dead Sea" |
| p186–p191 | 小問想去浮；每片海鹹不鹹看加多少水、熬走多少水；去海邊猜猜看 | OK | NOAA whysalty；NASA | 總結與前面一致（"varies with temperature, evaporation, and precipitation"）。p186 只是願望，沒有引導危險行為 |
| p192–p193 | 我覺得海最厲害的是一邊收一邊送 | OK（意見） | — | 有「我覺得」標成意見 |
| p194–p198 | 小問整理：河帶一點點鹽進海；太陽只把水熬走；鹽留下；海底慢慢收走 | OK | NOAA whysalty／riversnotsalty；Gale | 與前文一致。若 F01 改成「大部分從陸地來」，這段整理更貼合 |
| p199–p200 | 海水很鹹不要喝；身體要用更多的水排鹽，越喝越渴 | OK | NOAA drinksw | "to get rid of all the excess salt taken in by drinking seawater, you have to urinate more water than you drank. Eventually, you die of dehydration even as you become thirstier." 安全叮嚀到位，用語適合孩子 |
| p201–p202 | 那口鹹是好幾千萬年留下來的味道 | OK（附註：詩意說法） | LibreTexts 8.9；Gale | 鈉、氯滯留時間 5,500 萬到 8,700 萬年，「好幾千萬年」在範圍內 |
| p203–p206 | 原來如此；留言與訂閱 | OK | — | 片尾 |
| youtube.title | 河水一直流進海裡，海為什麼還是鹹？ | OK | — | 問題 |
| youtube.description | 河從石頭帶走一點點鹽；太陽只搬得走水；貝殼、泥沙、熱泉、古老鹽層把鹽收走；紅海特別鹹、波羅的海淡淡的；不要喝海水 | OK（附註） | 同上各段 | 這裡的「鹽」是廣義的溶解鹽類（NOAA、USGS 也這樣用），所以「貝殼把鹽收走」不算錯；但正片 p122 說「做殼用不到這種鹽」，如果想讓說明跟正片的用詞一致，可以把「怎麼把鹽收走」改成「怎麼把海水裡的東西收走」（非必要）。「AI 生成、示意」與「海水很鹹，請不要喝」的聲明都在 |
| thumbnail.headline | 河水一直倒／海還是鹹 | OK | NOAA riversnotsalty | 問題的濃縮 |
| thumbnail.sub | 太陽只搬走水，搬不走鹽 | OK | Gale | "the water … evaporates but the dissolved salts do not" |
