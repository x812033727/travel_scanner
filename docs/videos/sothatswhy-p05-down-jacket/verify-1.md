# 查核報告 1（sothatswhy-p05-down-jacket）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-04
- 方法：逐句讀 `video.json` 的 176 句台詞（p001–p176）、每張卡片的 `data`、YouTube 標題與說明、縮圖文字，以及每個 `shot` 的畫面提示詞。對照 `claims.md` 的 C01–C07，並另外查核撰稿者在 claims.md 之外加進來的「常識」句（熱從手跑進冰、暖空氣比較輕會上浮、空氣要切成小格子才動不了、濕頭髮變乾時會冷、夏天穿羽絨衣也在留熱、溫度計放在羽絨衣裡量到室溫、保溫瓶的熱從瓶口溜走）。每一條都重新打開來源讀原文，不只沿用 claims.md 的引文。
- 打不開的來源：Science Foundation Ireland 的 PDF 用 WebFetch 讀不到文字，改用 pdftotext 解出原文後核對；美國專利 US4992327 的 USPTO PDF 回 403，改讀 Google Patents 的同一份專利全文。ILO《職業安全衛生百科》「Heat exchange through clothing」這次沒有再試，凡是需要它的句子（壓扁變差）都只靠 OpenStax 的機制，不依賴它。
- 字數上限：小問 ≤15 字、所長 ≤25 字，下方所有替換句都已用程式數過。
- 結論統計（台詞 176 句）：OK 166、FIX 10、CUT 0。另外標題、說明、縮圖與 9 張卡片共 12 項：OK 10、FIX 2（說明 1、卡片 wind-chill 1）。畫面提示詞 1 處建議修改（chief-feather，隨 p086 一起改）。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p012（所長） | 還有，公園的鐵欄杆，為什麼比木椅冰那麼多？ | FIX | 片子後面（p060–p061）要推翻的正是「鐵本來就比較冷」；開頭由所長說「比木椅冰那麼多」，會被讀成溫度真的比較低，跟本集的結論互相矛盾。HyperPhysics："With both objects at 0 C, steel feels colder than wood because its thermal conductivity is much higher"。加「摸起來」就沒問題 |
| F02 | p038（所長） | 發抖的時候，放出的熱是安靜坐著的好幾倍。 | FIX（太肯定） | OpenStax 表 7.5：Shivering 425 W、Sitting at rest 120 W，約 3.5 倍，而且這是 76 公斤成年男性在用力發抖時的單一數值。輕微發抖遠低於此。把「是」改成「可以是」 |
| F03 | p061（所長） | 其實一樣冷。 | FIX（太肯定） | HyperPhysics 的例子是**假設**兩者同溫（都在 0 °C）。真實的公園裡，鐵和木頭吸收陽光、晚上散熱、早上回溫的速度都不同，溫度只會「差不多」，不保證完全一樣。前一句 p060 已經說「整晚都待在同一個公園」，改成「差不多一樣冷」不影響推理 |
| F04 | p075（所長） | 答案可能會讓你意外：是空氣。 | FIX（太肯定） | 回答的是 p074「什麼最會擋熱」。同一集後面（p138–p142）就說保溫瓶的真空比空氣更會擋；OpenStax 表 14.3 的保麗龍（0.010）也低於空氣（0.023），只是它也是靠關住的氣體。限定成「身邊」最會擋熱的就成立，也不跟保溫瓶段落打架 |
| F05 | p086（所長） | 羽毛本身傳熱的本事，其實跟空氣差不多。 | FIX（說法錯） | OpenStax 表 14.3 的 "Down feathers 0.025" 量的是一整團羽絨**加上它裡面的空氣**（體積大部分是空氣），不是羽毛的角蛋白本身。羽毛材料本身是實心的蛋白質，傳熱比空氣快；正因為一團羽絨的數字接近空氣，才說明擋熱的是被關住的空氣。查到的羽毛類保溫材料量測（0.024–0.045 W/(m·K)）也都是整團材料的數值，沒有單講角蛋白的。說「一團羽絨」就正確，也跟 p095 的結論一致。**claims.md C02 的「羽毛本身」說法也有同樣問題** |
| F06 | p112（所長） | 所以衣服一濕，熱就跑掉了，穿起來就不暖。 | FIX（太肯定） | ColumbiaDoctors："Wet clothing greatly increases heat loss through conduction and evaporation."。來源說的是熱跑得「多很多」，不是全部跑掉、完全不暖。卡片 water-air 的副標「衣服一濕，熱就跑得快」措辭已經正確，台詞跟它一致即可 |
| F07 | p113（所長） | 羽絨濕了還會黏成一團，撐不起那些小空間。 | FIX（無來源的細節） | claims.md C04 已註明「黏成一團」只有戶外用品網站的說法。我找到唯一非廣告的資料是美國專利 US4992327 的實驗表：羽絨／羽毛（80/20）泡水 6 小時後密度 56.91 kg/m³、晾 30 分鐘後 83.37 kg/m³，遠高於對照的合成棉（約 4.5–17 kg/m³），並寫合成棉 "retain loft while wet"、保暖 "to a far greater degree than does down"。這支持「濕了會塌、蓬鬆度變差」，但沒有「黏成一團」的說法。改成「塌下去」 |
| F08 | p121（所長） | 氣象局把這叫做風寒：同樣的溫度，有風就覺得冷很多。 | FIX | 片子講的是美國國家氣象局的風寒指數（卡片出處也寫美國國家氣象局）。台灣觀眾聽到「氣象局」會想到中央氣象局，但它 2023 年已改名中央氣象署，對外發布的也是「體感溫度」而不是「風寒」。拿掉「氣象局」就沒有這個誤會。NWS："Wind chill is based on the rate of heat loss from exposed skin caused by wind and cold." |
| F09 | p141（所長） | 對。兩層瓶壁不碰在一起，中間又沒有空氣可以帶， | FIX（說法錯） | 兩層瓶壁在瓶口是接在一起的。伊利諾大學物理系：兩壁 "are not in contact"，但 "except perhaps at the lip where the walls are joined together"；Wikipedia："Most heat transfer occurs through the neck and opening of the flask, where there is no vacuum."。p145 也說熱從瓶口溜走，所以 p141 說「不碰在一起」前後矛盾。改成「中間隔開」 |
| F10 | p142（所長） | 熱就少了兩條路。 | FIX（太肯定） | claims.md C06 已提醒要說「擋住大部分」「很難過去」，不能說完全擋住。Wikipedia：真空 "reduces heat conduction or convection"（是減少，不是消除），而瓶口仍會傳熱。改成「幾乎走不通」 |
| F11 | 卡片 wind-chill（`left.points[0]`） | 沒有風：身上那層暖空氣留著 | FIX（說法錯） | 同一集 p080–p084 剛說過：就算站著不動，暖空氣也會往上飄、一直被換掉。OpenStax 14.6："hot air rises because density decreases as temperature increases"。沒有風時只是換得**慢**，不是留著不動 |
| F12 | `youtube.description` | ……同一個公園裡的鐵欄杆為什麼比木椅冰…… | FIX | 理由同 F01 |
| F13 | 畫面 chief-feather（p086） | holding a single small white feather | 建議修改 | 隨 F05 改成講「一團羽絨」，畫面也要改成拿著一團羽絨，不然話和畫面對不上。原提示詞把羽毛畫成一根羽毛（有羽軸），不是羽絨 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p006、p014 | 剛拿出來的羽絨衣跟房間一樣冷；羽絨衣自己不產生熱 | OK | OpenStax 13.1；SFI | OpenStax："any two systems placed in thermal contact … will reach the same temperature"。SFI 教師附註："Coats keep you warm by keeping the heat of you body in" |
| p015–p019 | 溫度計塞進羽絨衣放一晚，量到的跟房間差不多；房間比手冷，摸起來就冰 | OK | OpenStax 13.1、14.5 | 熱平衡：沒有熱源的東西放久了會跟周圍同溫。「差不多」措辭恰當。摸起來冰是熱從手流出去（OpenStax 14.5 "net flux of heat from the hot body to the colder body"） |
| p020–p025 | 羽絨衣裡只有羽絨和布；暖爐是你自己 | OK | OpenStax 7.8 | 一般羽絨衣的填充物是羽絨（常混一些小羽毛），兒童片說「羽絨和布」可以接受 |
| p027–p030 | 吃下去的東西身體會拿來用；用掉的能量最後大部分變成熱 | OK | OpenStax 7.8 | "By far the largest fraction goes to thermal energy" |
| p031–p032；卡片 body-heat | 大人安靜坐著，大約一直放出一百瓦左右的熱，跟一顆老式燈泡差不多 | OK | OpenStax 7.8 表 7.5 | Sleeping 83 W、Sitting at rest 120 W（76 公斤男性）。「大約一百瓦左右」落在睡覺到安靜坐著之間，可以。比喻只比放出的熱，不比亮度 |
| p034–p035 | 小朋友放出的熱少一些；連睡覺都在放 | OK | OpenStax 7.8 | 表上數值是成年男性，兒童身體小、總產熱較少；Sleeping 83 W |
| p037 | 發抖是身體在把火力開大 | OK | OpenStax 7.8 | Shivering 425 W，比安靜坐著高。下一句的倍數見 F02 |
| p043–p049 | 熱一定從熱往冷跑；手上的熱跑進冰塊，不是冷跑進手 | OK | OpenStax 14.5 | "a net flux of heat from the hot body to the colder body"。「一定」指的是淨流向，符合熱力學第二定律 |
| p050–p052、p067 | 光腳踩磁磚，熱跑進地板；磁磚把熱搬得比地毯快 | OK | OpenStax 14.5 | "the heat loss during the same time interval is greater for skin in contact with the tiles than with the carpet" |
| p054–p056 | 你比外面暖，熱就一直往外跑；衣服只能讓它跑慢一點 | OK | OpenStax 14.5；SFI | 同上；SFI："Coats keep you warm by keeping the heat of you body in" |
| p059–p060、p062–p065；卡片 iron-wood | 鐵和木頭同溫，鐵摸起來冰是因為搬熱快；手不是溫度計 | OK（p061 見 F03） | HyperPhysics；OpenStax 14.5 | "steel feels colder than wood because its thermal conductivity is much higher"；HyperPhysics 開宗明義說摸的感覺不能當溫度計 |
| p066；卡片 steel-wood | 鋼鐵傳熱比木頭快上百倍 | OK | OpenStax 14.5 表 14.3 | 鐵 80、不鏽鋼 14、木頭 0.08–0.16 → 不鏽鋼約 90–175 倍，鐵約 500–1000 倍，「上百倍」成立 |
| p068–p070 | 夏天曬燙的鐵比木頭更燙手 | OK | HyperPhysics | 100 °C 時鋼比木頭燙，因為把熱送進皮膚更快 |
| p071–p074 | 摸到冰冰的東西，想是它冷還是它很會搬熱 | OK | HyperPhysics | 同上 |
| p076–p078 | 不會動的空氣非常不會傳熱；空氣很難乖乖不動 | OK | OpenStax 14.5、14.6 | 空氣 0.023，表上最低之一；空氣會產生自然對流 |
| p079–p084 | 貼著你的空氣被弄暖後往上飄，換冷空氣來，熱被一路帶走；暖空氣比冷空氣輕會浮上去；站著不動熱也被帶走 | OK | OpenStax 14.6 | "Natural convection is driven by buoyant forces: hot air rises because density decreases as temperature increases"；"warm air near your body is replaced by cooler air from elsewhere"。「比較輕」指同樣大小的空氣，對兒童可以 |
| p087–p090、p093–p095；卡片 down-works | 羽絨是很細的小絲往四面八方張開，撐出很多小空間；空氣被關在小空間裡動不了，熱跑得慢；真正擋熱的是關在裡面的空氣 | OK | OpenStax 14.5、14.6 | "incorporate many small pockets of air"；"trapping it in spaces too small to support convection" |
| p091–p092 | 一大片空氣會流動，熱一樣被帶走 | OK | OpenStax 14.6 | 同上：空間夠大就會對流 |
| p096–p100 | 羽絨衣是裝滿空氣的衣服；毛衣、棉被也用同一招 | OK | OpenStax 14.6 | "Fur, fiber, and fiberglass also take advantage of the low conductivity of air by trapping it"。p098–p099 是所長的意見句，有「我覺得」 |
| p101–p104 | 壓扁的地方關住的空氣變少，那裡就沒那麼暖 | OK | OpenStax 14.5、14.6（機制推得） | 沒有找到可引用的數字；台詞只講機制、用「沒那麼暖」，不給數字，可以 |
| p105–p107 | 重不重不是重點，重點是關住多少不會動的空氣 | OK | OpenStax 14.6 | 簡化說法（還有防風、乾濕等因素，片子另外講），對兒童可接受 |
| p108–p110 | 濕了水跑進小空間，把空氣擠出去 | OK | ColumbiaDoctors；US4992327 | 濕衣服熱損失大增；專利實驗顯示濕羽絨密度變高、蓬鬆度下降 |
| p111；卡片 water-air | 水傳熱大約是空氣的二十幾倍 | OK | OpenStax 14.5 表 14.3 | 0.6／0.023 ≈ 26 倍。卡片副標「衣服一濕，熱就跑得快」也正確 |
| p114 | 淋過冬天的雨應該記得那種冷 | OK | — | 經驗句，沒有事實主張 |
| p115–p116 | 頭髮沒吹乾也好冷；水在乾掉時還會從你身上帶走熱 | OK | ColumbiaDoctors | "Evaporation of water from your skin if it is wet"；"Wet clothing greatly increases heat loss through conduction and evaporation" |
| p117–p120 | 身上一直貼著一層被你弄暖的空氣；風一吹被吹走，換成冷空氣，熱跑得更快 | OK | OpenStax 14.6；NWS | "A cold wind is much more chilling than still cold air"；"warm air near your body is replaced by cooler air" |
| p122–p124 | 風寒說的是露在外面的皮膚；溫度計自己不發熱，風再大也只會跟空氣一樣 | OK | NWS | "rate of heat loss from exposed skin"；"The inanimate object will NOT cool below the actual air temperature."（前提是乾的溫度計；本集畫面就是乾的） |
| p125–p127 | 羽絨衣外層布最好能擋風，不然風鑽進去，關住的空氣被換掉 | OK | OpenStax 14.6（機制推得） | 「最好」措辭恰當 |
| p128–p131、p146–p147 | 保溫瓶跟羽絨衣做同一件事；不加熱也不製冷，只讓熱很難進出；熱湯保熱、冰水保冰 | OK | 伊利諾大學物理系；SFI | "designed to be a good thermal insulator for keeping the contents hot or cold"；SFI："Flasks keep things really hot, or really cool" |
| p132–p137；卡片 three-ways | 熱有三條路：碰到、被流動的空氣帶走、直接照過去；火堆讓臉熱是照過去的；太陽的熱照到地球 | OK | OpenStax 14.4 | 三種方式的定義；"In a fireplace … Radiation is responsible for most of the heat transferred into the room"；"the warming of the Earth by the Sun" |
| p138–p140 | 保溫瓶是兩層瓶子，中間的空氣幾乎都抽掉；熱很難用碰的、用帶走的過去 | OK | Wikipedia；伊利諾大學物理系 | "a partial-vacuum which reduces heat conduction or convection"；「幾乎」「很難」措辭正確（p141–p142 見 F09、F10） |
| p143–p144 | 瓶壁亮亮的像鏡子，把照過來的熱擋回去很多 | OK | 伊利諾大學物理系；Wikipedia | "coated with a highly reflective material"；"minimized by silvering flask surfaces facing the gap" |
| p145 | 瓶口沒有真空，熱還是會從那裡慢慢溜 | OK | Wikipedia | "Most heat transfer occurs through the neck and opening of the flask, where there is no vacuum." |
| p148–p150 | 夏天穿羽絨衣一樣把你的熱留住，只是你不想留 | OK | OpenStax 14.6；SFI | 機制同前；一般夏天氣溫仍低於皮膚溫度，身體的熱照樣被留住 |
| p151–p158；卡片 two-cubes | 很多學校課堂會做這個比較；包起來的冰融得比較慢；羽絨衣不發熱，只讓房間的熱很難跑進去 | OK | SFI；ASHRAE／WGBH ZOOM；Tes | SFI："They could compare these with an unwrapped ice cube"、"the coat will keep the snowman cold by not letting the warmer air in"。Tes："if you wrap a lump of ice in bubblewrap it will melt less quickly than a piece of ice left in the warm air"、"the insulating material cannot be heating the ice"。台詞沒有給時間或溫度，符合 claims.md C07 的限制。愛爾蘭、英國、美國都有，「很多學校課堂」可以 |
| p159–p172；卡片 outro | 總結：暖爐是你；羽絨衣用關住的空氣讓熱跑得慢；壓扁、淋濕、被風吹透熱就留不住；剛拿出來是冰的是因為還沒裝到你的熱；保暖是保住你的暖 | OK | 同上各段 | 只是重述前面已查核的內容。p166「熱就留不住了」是小問的口語總結，前面已經講清楚是「變差」，可接受 |
| p173–p176 | 留言題與訂閱 | OK | — | 沒有事實主張 |
| `youtube.title` | 羽絨衣一點熱都不會產生，為什麼穿上就暖？ | OK | OpenStax 7.8；SFI | — |
| `thumbnail` | 羽絨衣 **不會發熱**／暖爐其實是你自己 | OK | 同上 | — |
| `youtube.description` 其餘文字 | 功率與倍數都是教科書的典型值或數量級；插圖由 AI 生成 | OK | — | 鐵欄杆那句見 F12 |

## 三、畫面提示詞

除了 F13，沒有發現畫出錯誤事實的提示詞。逐項看過的重點：

- ice-teaser、ice-back（用羽絨衣包冰塊）：claims.md C07 說這只能當「想像實驗」插圖，台詞說的是「很多學校課堂都會做」，沒有說我們做過，可以。
- kid-feather-nose（小問拿一根大羽毛搔鼻子）：配的是小問的錯誤猜想（p085），畫成一般羽毛沒關係。
- down-palm、down-magnifier、kid-jar：畫的是一團一團的白色羽絨，細絲往四面張開，正確。
- kid-warm-air：暖空氣從身上往上飄，跟 p080 一致。
- thermos-magnifier：兩層薄瓶壁中間有空隙，正確。若要更精確，可在提示詞加上 "the two walls joined only at the rim"，與 F09 的修改一致（非必要）。
- kid-thermo-wind：溫度計是乾的，配 p124 正確。

## 建議修改

- p012：還有，公園的鐵欄杆，為什麼比木椅冰那麼多？ → 還有，公園的鐵欄杆，為什麼摸起來比木椅冰那麼多？（24 字）
- p038：發抖的時候，放出的熱是安靜坐著的好幾倍。 → 發抖的時候，放出的熱可以是安靜坐著的好幾倍。（22 字）
- p061：其實一樣冷。 → 其實差不多一樣冷。（9 字）
- p075：答案可能會讓你意外：是空氣。 → 答案可能會讓你意外：身邊最會擋熱的，是空氣。（22 字）
- p086：羽毛本身傳熱的本事，其實跟空氣差不多。 → 一團羽絨傳熱的本事，其實跟空氣差不多。（19 字）
- p112：所以衣服一濕，熱就跑掉了，穿起來就不暖。 → 所以衣服一濕，熱就跑得快很多，穿起來就沒那麼暖。（24 字）
- p113：羽絨濕了還會黏成一團，撐不起那些小空間。 → 羽絨濕了還會塌下去，撐不起那些小空間。（19 字）
- p121：氣象局把這叫做風寒：同樣的溫度，有風就覺得冷很多。 → 這就叫做風寒：同樣的溫度，有風就覺得冷很多。（22 字）
- p141：對。兩層瓶壁不碰在一起，中間又沒有空氣可以帶， → 對。兩層瓶壁中間隔開，又沒有空氣可以帶，（20 字）
- p142：熱就少了兩條路。 → 這兩條路就幾乎走不通。（11 字）
- 卡片 wind-chill（scene `wind-chill`）`data.left.points[0]`：身上那層暖空氣留著 → 身上那層暖空氣換得慢
- `youtube.description`：同一個公園裡的鐵欄杆為什麼比木椅冰 → 同一個公園裡的鐵欄杆為什麼摸起來比木椅冰
- 畫面 chief-feather `data.prompt`：holding a single small white feather between two fingers and studying it → holding a small fluffy white down cluster between two fingers and studying it
- （給 claims.md 的維護者，不屬本片）C02「羽毛本身傳熱的本事，跟空氣差不多」應改成「一團羽絨」；表上的 Down feathers 0.025 是含空氣的整團羽絨的數值。

## 來源

只列查核者這次實際打開並讀到原文的頁面，格式可直接放進 `video.json` 的 `sources`。`video.json` 現有的 13 筆來源中，查核者這次沒有重新打開的是 OpenStax University Physics 1.6 與 ASHRAE／WGBH Keep-A-Cube；它們支持的內容都另有已讀到的來源，保留無妨。

```json
[
  {"title": "OpenStax College Physics 2e: 7.8 Work, Energy, and Power in Humans", "url": "https://openstax.org/books/college-physics-2e/pages/7-8-work-energy-and-power-in-humans", "checked_on": "2026-11-04"},
  {"title": "OpenStax College Physics 2e: 13.1 Temperature", "url": "https://openstax.org/books/college-physics-2e/pages/13-1-temperature", "checked_on": "2026-11-04"},
  {"title": "OpenStax College Physics 2e: 14.4 Heat Transfer Methods", "url": "https://openstax.org/books/college-physics-2e/pages/14-4-heat-transfer-methods", "checked_on": "2026-11-04"},
  {"title": "OpenStax College Physics 2e: 14.5 Conduction", "url": "https://openstax.org/books/college-physics-2e/pages/14-5-conduction", "checked_on": "2026-11-04"},
  {"title": "OpenStax College Physics 2e: 14.6 Convection", "url": "https://openstax.org/books/college-physics-2e/pages/14-6-convection", "checked_on": "2026-11-04"},
  {"title": "HyperPhysics: Steel and Wood at Zero Celsius", "url": "https://hyperphysics.gsu.edu/hbase/thermo/woodmet.html", "checked_on": "2026-11-04"},
  {"title": "ColumbiaDoctors: Cold Exposure, Ways the Body Loses Heat", "url": "https://www.columbiadoctors.org/health-library/article/cold-exposure-ways-body-loses-heat", "checked_on": "2026-11-04"},
  {"title": "National Weather Service: Wind Chill Chart", "url": "https://www.weather.gov/safety/cold-wind-chill-chart", "checked_on": "2026-11-04"},
  {"title": "University of Illinois Physics, Ask the Van: Characteristics of Dewars", "url": "https://van.physics.illinois.edu/ask/listing/1680", "checked_on": "2026-11-04"},
  {"title": "Wikipedia: Vacuum flask", "url": "https://en.wikipedia.org/wiki/Vacuum_flask", "checked_on": "2026-11-04"},
  {"title": "Science Foundation Ireland: What Material Will Keep Ice Lollies the Coolest?", "url": "https://www.sfi.ie/site-files/primary-science/media/pdfs/col/keeping_ice_lollies_cool.pdf", "checked_on": "2026-11-04"},
  {"title": "Tes Magazine: Iceman cometh (1998)", "url": "https://www.tes.com/magazine/archive/iceman-cometh", "checked_on": "2026-11-04"},
  {"title": "US Patent 4,992,327: Synthetic down (wet loft comparison with down)", "url": "https://patents.google.com/patent/US4992327A/en", "checked_on": "2026-11-04"}
]
```
