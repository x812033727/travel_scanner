# 查核報告 1（sothatswhy-p14-sky-colors）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-06
- 方法：逐句讀 `video.json` 的 265 句台詞（p001–p265，與 `script.md` 的 143 個場景一一對應）、YouTube 標題與說明、縮圖文字，以及重點場景的畫面提示詞。本集沒有卡片（全部是 `shot`）。對照 `claims.md` 的 C01–C19，並另外查核 claims.md 之外的句子（夜空變黑表示藍來自陽光、甩快跳繩浪變短、大腦把顏色混成白、紅光大多直直往前走、背對太陽最藍、日出也一樣、灰塵顆粒比較大、火山顆粒噴到的高度、月球「非常稀薄的一點點」）。每一條都重新打開來源讀原文（curl 抓頁面轉成文字後逐句比對），不只沿用 claims.md 的引文。
- 打不開的來源：NOAA JetStream「The Color of Clouds」用 curl 直接抓回 403（CloudFront 擋下），改用 WebFetch 讀到原文，C03、C06、C11、C17、C19 用到的句子都核對過。Princeton 的 Einstein Papers 編注頁（vol3-doc/321–323）是 JavaScript 載入，讀不到內文；愛因斯坦的年份改用 Wikipedia「Critical opalescence」的論文書目與 Straumann & Giulini（arXiv physics/0507107）的史料段落核對。NOAA SciJinks 與 claims.md 一樣沒有使用。
- 字數：替換句都已用程式數過，每句等長或更短；p154–p155 是一組，兩句合計 25 字不變。
- 結論統計（台詞 265 句）：OK 258、FIX 7、NOT FOUND 0。另外標題、說明、縮圖共 3 項：OK 3。畫面提示詞沒有必須修改的地方（four-blue 有一則可選建議）。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p078（所長） | 藍光被彈開的，大約是紅光的四倍。 | FIX（數字會被當成定值） | 倍數取決於拿哪兩個波長比，本集自己的來源就不一致：NOAA JetStream "about four times stronger than red light waves"；Gibbs 拿 400 nm 對 700 nm 算 "(700/400)^4 ~= 10"；Corfidi 說紫光對長波長 "three to four times"。依 λ⁻⁴ 自己算，450 對 700 nm 約 5.9 倍、470 對 640 nm 約 3.4 倍。小朋友會把「四倍」記成固定答案，而它只是其中一種取法。改成「好幾倍」在所有來源下都成立，畫面 four-blue（四支藍箭頭對一支紅箭頭）也還對得上 |
| F02 | p089（所長） | 後來愛因斯坦在一九一一年算出來： | FIX（年份） | 1911 只出現在 Gibbs（1997 年的 FAQ）。愛因斯坦的論文是 "Theorie der Opaleszenz von homogenen Flüssigkeiten und Flüssigkeitsgemischen in der Nähe des kritischen Zustandes", Annalen der Physik 33 (1910): 1275–1298（Wikipedia「Critical opalescence」書目："In 1910 Albert Einstein showed that the link between critical opalescence and Rayleigh scattering is quantitative"）。Straumann & Giulini 引 1910 年 8 月 27 日給 Laub 的信，並說這篇（CPAE Vol. 3, Doc. 9）推出散射係數公式，"With this formula Einstein had found a quantitative relationship between Rayleigh scattering and critical opalescence"。1911 年是 Smoluchowski 發表論文、愛因斯坦回應的年份，不是算出公式的年份。改成一九一〇年；若不想放年份，也可改「後來愛因斯坦仔細算過：」（11 字）。**claims.md C14 的「1911 年」也要一起改** |
| F03 | p140（所長） | 超過一半的陽光，還是直直照到地面。 | FIX（太肯定） | JetStream 原句："over one-half of the sun's white light continues through the atmosphere reaching the Earth's surface"，沒有說是直射。直射的部分要靠 PVEducation 撐：太陽高、晴天時直射光約為大氣外的 72%（"The intensity of AM1.5D radiation can be approximated by reducing the AM0 spectrum by 28%"；I_D = 1.353 · 0.7^(AM^0.678)，AM1 時約 0.95 kW/m²）。但陰天幾乎沒有直射光，太陽低時直射光也少很多，小朋友會把它當成每天的規則。加「晴天時」就成立；原意（不是全部被彈走）不變 |
| F04 | p154–p155（所長） | 這時光要穿過的空氣，／大約是太陽在頭頂時的三十多倍。 | FIX（說得太早） | Wikipedia「Air mass」："At sea level the air mass towards the horizon (z = 90°) is approximately 38"；我用 Kasten–Young 公式自己代入：z = 85° 約 10.3、88° 約 19.8、89° 約 26.9、90° 約 37.9。「三十多倍」只有在太陽貼著地平線時才對，前一句 p152 說的是「快下山時」，用「這時」接上來會被聽成太陽還在天上就有三十多倍。把時間點講成地平線 |
| F05 | p158（小問） | 光要走好久的路！ | FIX（會被當成時間） | 「好久」說的是時間。光多走的這段路只多花不到一毫秒，所長也沒有更正，小朋友會以為傍晚的光要走很久才到。空氣量模型比的是要穿過多少空氣，不是走多久。改「好長」，跟 p157「好遠喔」一致 |
| F06 | p235（所長） | 很細的小顆粒，被噴到大約二、三十公里高。 | FIX（高度與機制混在一起） | Corfidi 的 "12 to 18 miles"（約 19–29 公里）是平流層顆粒**停留**的高度（"exist as thin veils of dust or sulfuric acid droplets at altitudes of 12 to 18 miles"），不是火山噴發能噴到多高。Wikipedia「1991 eruption of Mount Pinatubo」：火山灰柱 "35 km (22 mi) into the atmosphere"，而造成晚霞的細小顆粒主要是二氧化硫在高空 "oxidized in the atmosphere to produce a haze of sulfuric acid droplets, which gradually spread throughout the stratosphere over the year following the eruption"。說「噴到二、三十公里」低估了噴發高度，也暗示這些小顆粒是直接噴上去的。改成「飄在」，只說它們待在哪裡，數字仍然對得上 Corfidi；p236「飛那麼高？」仍接得上 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p010、p015–p018 | 中午藍、傍晚紅；同一道陽光；有看不見的東西在「換」 | OK | — | 開場鋪陳，沒有事實主張。p008「天天貼著你，你卻看不見」指空氣，後面 p095–p098 才揭曉 |
| p011–p014 | 牛奶水與月球兩個預告問題 | OK | — | 只是問題，答案在 p182–p185、p254 |
| p019–p024 | 天空如果本來就藍，晚上不會變黑；藍是陽光帶來的 | OK | NASA Space Place；Gibbs | 「Sunlight … is scattered in all directions by all the gases and particles in the air」。用夜空推論，邏輯對 |
| p025–p028、p036–p037 | 白光是很多顏色混在一起；大腦把它們混成白的 | OK | NASA Space Place；Gibbs；NASA Goddard | "The light from the Sun looks white. But it is really made up of all the colors of the rainbow."；Goddard："Our brains then integrate these signals into a perceived white color." |
| p029–p030 | 水管水霧裡有時會出現小彩虹 | OK | UCAR Appearance of the Sky | "Rainbows result from light that scatters inside of water droplets"。「有時」措辭恰當，片子沒有解釋彩虹成因（符合 brief） |
| p031–p033 | 三稜鏡把陽光分成一排顏色；牛頓做過 | OK | Gibbs；NASA Space Place | "This was demonstrated by Isaac Newton, who used a prism to separate the different colours" |
| p034–p035 | 紅橙黃綠藍紫擠在白光裡 | OK | Gibbs | 小問的口語列舉，少了靛色沒關係（Gibbs："orange, yellow, green, blue and indigo between"） |
| p040–p047 | 光一波一波前進；紅光波長、藍紫光波短；波長不同顏色不同；抖快一點浪變短 | OK | NASA Space Place；UCAR；Gibbs | "Blue light waves are shorter than red light waves"；"The colours of light are distinguished by their different wavelengths"。跳繩在張力不變時波速固定，抖得越快波長越短，比喻沒有錯，也說清楚是「像」 |
| p051–p056 | 一罐空氣看不出顏色；頭頂上的空氣很厚 | OK | Gibbs | 日常觀察；天空的顏色是整層大氣的散射（"molecules in the air scatter blue light"） |
| p057–p058 | 從大約兩萬公尺高的飛機拍到地球邊上一圈薄薄的藍 | OK | HyperPhysics Blue Sky | "taken from a U.S. Air Force U-2 craft at about 70,000 feet"（約 21,300 公尺），「大約兩萬公尺」正確。畫面 earth-layer 也是薄藍帶配黑天 |
| p059–p064 | 空氣由小到看不見的分子組成；吸一口氣吸進好多顆 | OK | UCAR Appearance of the Sky | "Nitrogen and oxygen make up most of the molecules in our atmosphere"。「小球」是比喻 |
| p065–p066 | 一顆分子比光的一個波小上大約一千倍 | OK | Corfidi | "Air molecules are much smaller than this --- about a thousand times smaller."（氮分子約 0.3 nm，可見光 400–700 nm，約一千多倍，「大約」恰當） |
| p067–p073 | 大部分的光穿過去；一部分被彈向四面八方，叫散射；彈開的光還會再被彈 | OK | NASA Space Place；Gibbs；Corfidi | "scattered in all directions"；"blue light is then more likely to be scattered twice or more"；Corfidi "multiple scattering" |
| p074–p077 | 每種顏色都會被彈，短波被彈得特別多 | OK | HyperPhysics；Gibbs | "more effective at short wavelengths"。倍數見 F01 |
| p079–p082 | 紅光比較少被彈開，大多照原方向走 | OK | NASA Space Place | "allowing the reds and yellows to pass straight through to your eyes" |
| p083–p084 | 十九世紀英國科學家瑞利算出：波越短，被彈開得越多 | OK | Corfidi；Gibbs | "the nineteenth century English physicist Lord Rayleigh"；"He showed that the amount of light scattered is inversely proportional to the fourth power of wavelength" |
| p085–p088 | 瑞利他們當時以為是灰塵和小水滴；後來的人發現天空的藍沒有隨天氣變那麼多 | OK | Gibbs | "Tyndall and Rayleigh thought that the blue colour of the sky must be due to small particles of dust and droplets of water vapour"；"there would be more variation of sky colour with humidity or haze conditions than was actually observed"。附註：瑞利本人在 1899 年就已經提出分子本身足以解釋，「當時」指早期的看法，可以接受 |
| p090–p092 | 光靠空氣分子就夠把天空弄藍 | OK（年份見 F02） | Gibbs；Straumann & Giulini | "the molecules of oxygen and nitrogen in the air are sufficient to account for the scattering"；愛因斯坦公式把瑞利散射和密度起伏連起來 |
| p093–p098 | 往哪個方向看都有被彈過來的藍光；空氣不是藍的，是把藍光彈給你看 | OK | HyperPhysics；NASA Space Place | "the light scattered down to the earth at a large angle with respect to the direction of the sun's light is predominantly in the blue end of the spectrum" |
| p099–p102 | 太陽旁邊偏白，離太陽越遠藍得越深 | OK | HyperPhysics | "the blue of the sky is more saturated when you look further from the sun. The almost white scattering near the sun can be attributed to Mie scattering" |
| p103–p105 | 背對太陽看是最藍的嗎？轉一圈比比看；別直接看太陽 | OK | HyperPhysics | 小問的問題，所長沒有肯定，只請觀眾自己比。附註：實際上最飽和的藍常在離太陽約 90° 的方向和頭頂，正背對太陽的地平線附近反而偏淡；台詞沒有下結論，所以不改。安全提醒是常識 |
| p106–p111 | 天空不是海倒映的；山上離海很遠天空一樣藍；從沙灘看海，海藍有一部分是映著天 | OK | Gibbs | "the molecules of oxygen and nitrogen in the air are sufficient"；"When viewed from the beach, the sea is also blue because it reflects the sky"。「一部分」措辭正確 |
| p112–p114 | 海水很深時自己會吃掉一些紅光 | OK | Gibbs | "water absorbs longer wavelengths of light through distances over about 20 metres" |
| p115–p123 | 紫光為什麼不顯：陽光裡紫光少、一部分在高空被吸收、眼睛對紫不敏感；天空裡仍有紫光，混起來成淡藍 | OK | Gibbs；UCAR Colors of the Sky；Corfidi | Gibbs："the spectrum of light emission from the Sun is not constant at all wavelengths, and additionally is absorbed by the high atmosphere, giving less violet"；"our eyes are less sensitive to violet"；"This combination accounts for the pale blue colour"。UCAR："If our eyes were better able to see violet light, then the sky would look violet"。沒有說「紫光不存在」 |
| p124–p127 | 眼睛也參了一腳 | OK | Gibbs | 意見句，有「我覺得」；Gibbs 談錐細胞的段落支持 |
| p128–p129 | 藍光都被彈到天上了 | OK | — | 小問的誇張，p139 由所長更正成「只是一部分」 |
| p130–p134 | 很多人把太陽畫黃色；從太空站看太陽是白的；那裡在大部分空氣外面 | OK | NASA Goddard | "If we were above the atmosphere, say on the International Space Station and looked at the sun (through our filtered visor), the sun would appear white!" |
| p135–p136 | 從地面看偏黃，是一點藍光半路被彈走 | OK | NASA Goddard | "we lose some of the blue tint of the sun as sunlight passes through the atmosphere"；「一點」措辭恰當 |
| p137–p139、p141 | 被彈開的只是一部分；白天的地上還是亮的 | OK（p140 見 F03） | NOAA JetStream | "over one-half of the sun's white light continues through the atmosphere reaching the Earth's surface" |
| p142–p149 | 太陽中午和傍晚一樣，變的是光走的路；路上要穿過的空氣變厚 | OK | HyperPhysics Red Sunset；UCAR | "the light passing at grazing incidence upon the earth must pass through a greater thickness of air than when it is overhead"。p143 是小問的錯猜，p144 有更正 |
| p150–p153 | 太陽在頭頂時直直穿下來，走的空氣少；快下山時斜斜貼著地面穿過來 | OK | PVEducation；HyperPhysics | 空氣量 AM = 1/cos θ 的定義；比的是「頭頂」不是「中午」，符合 claims.md 的提醒。三十多倍見 F04 |
| p156–p157 | 三十多倍？好遠喔！ | OK（p158 見 F05） | Wikipedia Air mass | 小問的反應；在地平線時幾何路徑同樣長很多倍，「好遠」可以 |
| p159–p161 | 藍光一路被彈走，剩下多半是紅橙色；太陽越貼近地平線通常越紅 | OK | NASA Space Place；HyperPhysics；Corfidi | "more of them are scattered out of the beam of sunlight before it reaches you"；「多半」「通常」措辭恰當 |
| p162 | 再紅的太陽也別一直盯著看 | OK | — | 安全提醒，一般常識 |
| p163–p166 | 太陽看起來剛要沉下去時，其實已在地平線下面一點；是空氣把光往下彎進眼睛 | OK | HyperPhysics Red Sunset | "Just before the sun disappears from view, its actual position is about a diameter below the horizon, the light having been bent by atmospheric refraction to reach our eyes." 光線在大氣裡是往地面那邊彎的，「往下彎」方向正確；沒有說「折射」與度數 |
| p167–p170 | 紅太陽是被彈剩下的光；日出也一樣，太陽在東邊 | OK | HyperPhysics Red Sunset | "The equivalent phenomenon can be seen at sunrise" |
| p171–p180 | 被彈走的藍光正讓更遠的地方看到下午的藍天；美國氣象學家說夕陽紅是因為白天的天空藍 | OK | Corfidi | "it could be said that sunsets are red because the daytime sky is blue … A beam of sunlight that at a given moment helps produce a red sunset over the Appalachians is at the same time contributing to a deep blue, late afternoon sky over the Rockies"。Corfidi 是 NOAA/NWS 風暴預報中心的氣象學者；台詞用「這樣說」，沒有當成逐字引語 |
| p181–p187 | 手電筒從側邊照牛奶水，從旁邊看帶淡藍；迎著手電筒看偏橙紅 | OK | Gibbs；UCAR Colors of the Sky | "From the side, the beam can be seen by the blue light it scatters; but the light seen directly from the end is reddened after it has passed through the tank."；「一點淡淡的」措辭恰當 |
| p188–p190 | 牛奶小顆粒像空氣分子在彈光；光走越遠，被彈走的藍光越多 | OK | Gibbs | Tyndall 效應段落；只說「像」，沒有說顆粒跟分子一樣大 |
| p191–p193 | 在家可以試；看不出顏色就再加兩滴 | OK | UCAR Colors of the Sky | "If you don't see any change in color, add a couple more drops of milk to the mixture and try again." |
| p194–p199 | 雲是小水滴，比空氣分子大得多；每種顏色彈得差不多，混起來是白的 | OK | HyperPhysics；NOAA JetStream；Gibbs | "The water droplets that make up the cloud are much larger than the molecules of the air and the scattering from them is almost independent of wavelength"；JetStream："We perceive this equally-scattered light as white." 只比分子，沒有比光的波長（JetStream 與 Gibbs 在這點上說法不同） |
| p200–p203 | 霧也是小水滴，被太陽照是白茫茫 | OK | HyperPhysics Mie | "It also gives us the the white light from mist and fog." |
| p204–p207 | 雲變厚，陽光穿不太過去，看起來灰暗 | OK | NOAA JetStream | "As clouds thicken, sunlight passing through them will diminish or be blocked, giving the cloud a gray color." |
| p208–p210 | 有時是旁邊太亮，眼睛一比就覺得灰 | OK | NOAA JetStream | "the contrast between the background (blue sky or additional clouds) and the foreground cloud overwhelms our vision"；「有時候」措辭恰當 |
| p211–p215 | 傍晚的雲橙紅，因為照到它的光已經被彈成紅的；雲像大布幕 | OK | NOAA JetStream；Corfidi | "a cloud's color will be whatever sunlight color it receives after Rayleigh scattering"；Corfidi："Clouds catch the last red-orange rays … like a theatre screen, and reflect this light to the ground." |
| p216–p219 | 灰塵越多天空越藍？跟瑞利那時的人想的一樣，答案相反 | OK | Gibbs；UCAR | 小問的錯猜，所長更正；呼應 p085–p086 |
| p220–p222 | 灰塵和煙的顆粒比較大，白天的藍變淡；多到一個程度中午也可能白白一片 | OK | Corfidi；UCAR Colors of the Sky | Corfidi："Typical pollution droplets … are on the order of .5 to 1 um"、"hazy daytime skies, instead of being bright blue, appear grayish or even white"；UCAR："the sky might even look white in the middle of the day"。「可能」措辭恰當 |
| p223–p225 | 天空最藍的日子常常是空氣很乾淨的日子 | OK | UCAR Colors of the Sky | "When there are few aerosols in the air, the sky appears clear and deep blue"；「常常」措辭恰當 |
| p226–p229 | 灰塵多時夕陽說不準：有時更紅，有時灰濛濛 | OK | UCAR；HyperPhysics；Gibbs；Corfidi | 來源互相矛盾，台詞兩面都說：UCAR "It also makes sunsets more colorful and red"、HyperPhysics "brilliant reds are seen when there are many airborne particles"、Gibbs "If the air is polluted with small particles … the sunset will be more red"；Corfidi "twilight colors at the surface on dusty or hazy days tend to be muted and subdued" |
| p230–p232 | 傍晚搭飛機，地上的夕陽淡淡的，飛機爬過霾層顏色突然鮮豔 | OK | Corfidi | "A seemingly bland sunset at the ground gives way to vivid color aloft as soon as the plane ascends beyond the haze."「有人」措辭恰當 |
| p233–p234 | 一九九一年菲律賓皮納圖博火山大爆發；有一種特別的晚霞跟火山有關 | OK | Corfidi；Wikipedia 1991 eruption | "the massive eruption of the Philippines volcano Mount Pinatubo in June of that year"（1991）。高度見 F06 |
| p236–p239 | 太陽下山大約十五分鐘後，地面暗了，高空那層還照得到太陽，被照成淡紫色和橙紅色 | OK | Corfidi | "About 15 minutes after sunset, however, with the troposphere in shadow and the stratosphere still illuminated by sunlight"；三種晚霞中有 "a lilac afterglow" 和 "a red-orange afterglow"。「被照成」說明是被陽光照亮、不是自己發光。「地面暗了」指低空已在陰影裡，十五分鐘時還不是全黑，但口語可接受 |
| p240–p241 | 這種火山晚霞斷斷續續出現大約一年半；連地球另一邊的美國都看得到 | OK | Corfidi | "persisted to varying degrees for about 18 months after the initial explosion"；照片攝於 1991 年 9 月 "over the eastern United States"。菲律賓與美國東部經度相差約 165°，「地球另一邊」可以 |
| p242–p245 | 火山幫天空換顏色；看到怪夕陽想想空氣裡多了什麼 | OK | — | 小問的總結與所長的邀請，沒有新的事實主張 |
| p246–p253 | 月球幾乎沒有空氣，只有非常稀薄的一點點；沒有小球彈藍光，天空是黑的 | OK | NASA Science（月球南極）；NASA Dark Sky, Bright Sun | "The Moon, unlike Earth, doesn't have a thick atmosphere to scatter blue light, so the daytime sky is black."；說「幾乎沒有」而非「完全沒有」，正確 |
| p254–p255 | 太陽很亮，月球白天的天空卻是黑的；亮亮的地面配黑漆漆的天 | OK | NASA Science（月球南極） | "Astronauts will see a stark contrast between the dark sky and the bright ground." |
| p256–p262 | 小問的總結；下次抬頭想想光走了多遠 | OK | 同上各段 | 只重述已查核的內容。p258「藍光被彈光了」是小問的口語，p160 已講清楚是「剩下的多半是紅色和橙色」，可接受 |
| p263–p265 | 留言題與訂閱 | OK | — | 沒有事實主張 |
| `youtube.title` | 同一道陽光，天空為什麼是藍的、夕陽卻是紅的？ | OK | 同上 | — |
| `thumbnail` | 天空的藍 **是彈過來的**／同一道陽光，傍晚就變紅 | OK | HyperPhysics；NASA Space Place | — |
| `youtube.description` | 白光裡藏著哪些顏色、空氣把藍光彈向四面八方、為什麼不是紫色、傍晚多走一段路、牛奶水、雲、月球；倍數與距離是大約數量級 | OK | 同上 | 說明裡沒有寫具體倍數或年份，F01、F02 改了也不必動說明 |

## 三、畫面提示詞

沒有發現畫出錯誤事實的提示詞。逐項看過的重點：

- earth-layer：從高空看地球邊緣一圈薄藍、上方黑天，與 p057–p058 和 HyperPhysics 的 U-2 照片一致。
- space-sun、moon-black：白色太陽配黑天，正確（NASA Goddard、NASA Science）。
- four-blue：四支藍箭頭對一支紅箭頭。改成 F01 的「好幾倍」後仍對得上；若想更貼近，可把 "four short bright blue arrows" 改成 "several short bright blue arrows"（非必要）。
- path-overhead、path-sideways：頭頂時光短、斜射時光長且偏紅，正確。
- milk-side、milk-end：側面淡藍、迎光看橙紅，與 Gibbs 一致；畫面是白天室內，UCAR 的「暗房」步驟沒有畫，claims.md 已說明是系列規則。
- droplet-all：水滴把各色均勻彈向四方，與 HyperPhysics「almost independent of wavelength」一致。
- volcano：灰色火山灰柱衝上藍天，搭配 F06 的「飄在」仍然成立（噴發時的灰柱與之後停在高空的細小顆粒是兩件事，畫面只畫噴發）。
- afterglow：日落後高空的淡紫與橙紅，與 Corfidi 的 lilac、red-orange afterglow 一致。
- dust-beam：陽光裡的灰塵配「以為是灰塵」的段落，正確。

## 建議修改

- p078：藍光被彈開的，大約是紅光的四倍。 → 藍光被彈開的，比紅光多好幾倍。（15 字）
- p089：後來愛因斯坦在一九一一年算出來： → 後來愛因斯坦在一九一〇年算出來：（16 字）（或不放年份：後來愛因斯坦仔細算過：）
- p140：超過一半的陽光，還是直直照到地面。 → 晴天時，一半以上陽光直直照到地面。（17 字）
- p154：這時光要穿過的空氣， → 到了地平線，（6 字）
- p155：大約是太陽在頭頂時的三十多倍。 → 光穿過的空氣，大約是頭頂時的三十多倍。（19 字；與 p154 合計 25 字，與原本相同）
- p158：光要走好久的路！ → 光要走好長的路！（8 字）
- p235：很細的小顆粒，被噴到大約二、三十公里高。 → 很細的小顆粒，飄在大約二、三十公里高。（19 字）
- （可選）畫面 four-blue `data.prompt`：four short bright blue arrows → several short bright blue arrows
- （給 claims.md 的維護者，不屬本片）C14「1911 年愛因斯坦算出分子散射的公式」應改成 1910 年（Annalen der Physik 33, 1910）；C03 的「大約四倍」要註明這是 JetStream 的取法，同一批來源也有 3–4 倍與約 10 倍；C12 的「噴到大約二、三十公里高」應改成「停在」，火山灰柱本身約 35 公里。

## 來源

只列查核者這次實際打開並讀到原文的頁面，格式可直接放進 `video.json` 的 `sources`。`video.json` 現有的 13 筆來源都重新讀過；後三筆是這次為了 F02、F06 新增的。

```json
[
  {"title": "NASA Space Place: Why Is the Sky Blue?", "url": "https://spaceplace.nasa.gov/blue-sky/en/", "checked_on": "2026-11-06"},
  {"title": "Philip Gibbs, Why is the sky blue? (Physics FAQ, UC Riverside)", "url": "https://math.ucr.edu/home/baez/physics/General/BlueSky/blue_sky.html", "checked_on": "2026-11-06"},
  {"title": "Stephen F. Corfidi, The Colors of Sunset and Twilight (NOAA/NWS Storm Prediction Center)", "url": "https://www.spc.noaa.gov/publications/corfidi/sunset/", "checked_on": "2026-11-06"},
  {"title": "NOAA JetStream: The Color of Clouds", "url": "https://www.noaa.gov/jetstream/clouds/color-of-clouds", "checked_on": "2026-11-06"},
  {"title": "UCAR Center for Science Education: The Colors of the Sky", "url": "https://scied.ucar.edu/kids/sky-wonders/colors-sky", "checked_on": "2026-11-06"},
  {"title": "UCAR Center for Science Education: The Appearance of the Sky", "url": "https://scied.ucar.edu/learning-zone/atmosphere/appearance-sky", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics: Blue Sky and Rayleigh Scattering", "url": "https://hyperphysics.gsu.edu/hbase/atmos/blusky.html", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics: Red Sunset, Green Flash", "url": "https://hyperphysics.gsu.edu/hbase/atmos/redsun.html", "checked_on": "2026-11-06"},
  {"title": "NASA Goddard: What Color is the Sun?", "url": "https://science.gsfc.nasa.gov/attic/eclipse2017.gsfc.nasa.gov/what-color-sun.html", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Air mass (solar energy)", "url": "https://en.wikipedia.org/wiki/Air_mass_(solar_energy)", "checked_on": "2026-11-06"},
  {"title": "PVEducation: Air Mass", "url": "https://www.pveducation.org/pvcdrom/properties-of-sunlight/air-mass", "checked_on": "2026-11-06"},
  {"title": "NASA Science: 9 Phenomena NASA Astronauts Will Encounter at the Moon's South Pole", "url": "https://science.nasa.gov/solar-system/moon/phenomena-nasa-astronauts-will-encounter-at-moons-south-pole/", "checked_on": "2026-11-06"},
  {"title": "NASA: Dark Sky, Bright Sun", "url": "https://www.nasa.gov/image-article/dark-sky-bright-sun/", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Critical opalescence (Einstein 1910, Annalen der Physik 33)", "url": "https://en.wikipedia.org/wiki/Critical_opalescence", "checked_on": "2026-11-06"},
  {"title": "Straumann & Giulini, Einstein's impact on the physics of the twentieth century (arXiv physics/0507107)", "url": "https://arxiv.org/abs/physics/0507107", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: 1991 eruption of Mount Pinatubo", "url": "https://en.wikipedia.org/wiki/1991_eruption_of_Mount_Pinatubo", "checked_on": "2026-11-06"}
]
```
