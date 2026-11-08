# 查核報告 2（sothatswhy-p05-down-jacket）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有做查核第 1 輪）
- 日期：2026-11-04
- 範圍：`git diff bf9b75d54 HEAD -- video.json`（commit f186ad498「round-1 revision from the fact-check and two blind readers」）改動或新增的部分。比對時先去掉台詞編號再逐句對照（第 1 輪後台詞從 p001–p176 重新編號成 p001–p168），所以下表的行號都是**現在** `video.json` 的編號。沒改動的句子沿用 verify-1 的結論，不再重查。
- 方法：逐句讀新增與改寫的 55 句台詞、改動的卡片 `data`、章名、YouTube 說明，以及 12 個新增或改過的 `shot` 提示詞。對照 `claims.md` 的 C01–C07，並為 claims.md 沒涵蓋的新主張另找來源（熱不會自己從冷往熱跑、拉鍊沒拉好時風從開口灌進去）。來源都重新打開讀原文。
- 打不開的來源：ILO《職業安全衛生百科》「Heat exchange through clothing」這次仍回 503；Springer 與 SAGE 上兩篇衣物通風論文需要登入（303／403），沒有引用。開口讓保暖下降改用 Kim 與 McCullough（2001）的摘要（koreascience.or.kr 讀得到）。
- 字數上限：小問 ≤15 字、所長 ≤25 字，數法照 `build_scenes.py` 的 `length()`（不算標點），下方替換句都已用程式數過。
- 結論統計（新增或改寫的台詞 55 句）：OK 52、FIX 3（p129、p150、p163）、CUT 0。另外說明欄、2 張卡片、6 個章名共 9 項：OK 8、FIX 1（章名「保溫瓶連空氣都抽掉了」）。畫面提示詞 12 個：全部 OK。
- verify-1 的 13 項建議都已照字句改進稿子（F09、F10 所在的 p141–p142 已整句改寫，見下方 p138–p139）。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| G01 | p150（所長） | 很多人都會這樣猜。可是它沒有熱可以給冰塊， | FIX（說法錯） | 羽絨衣放在房間裡，溫度跟房間一樣，比冰塊暖，所以它**有**熱會流進冰塊（只是很少，而且它自己不會再補）。p018 才剛說羽絨衣「放久了都跟房間一樣」，這句跟它矛盾。改前的「羽絨衣不會發熱」是對的。OpenStax 13.1：兩個接觸的物體會走向同溫；OpenStax 15.3："Heat transfer occurs spontaneously from higher- to lower-temperature bodies"。替換句用本集的「暖爐」說法，不重複「不會發熱」四個字（盲評嫌重講），意思一樣正確 |
| G02 | p129（所長） | 風就從前面灌進去，把關住的空氣換掉。 | FIX（說法不準） | 本集的「關住的空氣」一路指的是羽絨小空間裡的空氣（p092、p096、p110）。拉鍊沒拉好時，風從前襟開口灌進去，換掉的是**衣服跟身體之間**那層被你弄暖的空氣；羽絨格子裡的空氣被內外兩層布包著，不是從前襟被換掉的（那是 p125「外層布要擋風」講的事）。方向沒錯：Kim 與 McCullough（2001）用會動的暖體假人量測：「when there was an opening involved in design the system, insulation decreased」。改成回呼 p082、p121 那層「貼著你的暖空氣」，正確，也接得上前面 |
| G03 | p163（所長） | 下次你穿上它，等個幾秒， | FIX（無來源的細節） | 穿上後多久覺得暖，跟衣服厚薄、室溫、穿之前身體多冷都有關；沒有找到可引用的時間。claims.md 的原則是不給沒有來源的時間。改成「等一下下」也剛好回收 p006「穿一下下，怎麼就暖了？」的伏筆 |
| G04 | 章名（scene `chief-same-job`） | 保溫瓶連空氣都抽掉了 | FIX（太肯定） | 同一章的台詞 p135 說「幾乎都抽掉了」、p139 說「幾乎什麼都沒有」，章名卻說全部抽掉。Wikipedia："a partial-vacuum which reduces heat conduction or convection"。章名跟台詞一致即可 |

## 二、逐項核對（OK 的項目與依據）

### 台詞

| 行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p002 | 寒流來了，打開衣櫃，羽絨衣是冰的 | OK | OpenStax 13.1 | 小問的感覺；寒流時房間本來就冷，衣服跟房間同溫，摸起來冰 |
| p004 | 你摸摸自己的手，是暖的吧？ | OK | — | 反問句；接下來小問自己答「暖的」，跟衣服比，手的確較暖 |
| p005–p006 | 它又沒插電；穿一下下，怎麼就暖了？ | OK | — | 小問的疑問與伏筆，沒有事實主張 |
| p008、p012、p013 | 答案比你想的還要近；弄懂這件衣服冬天很多怪事都說得通；冰冰的衣服為什麼穿上就暖 | OK | — | 承諾句與問題，沒有事實主張 |
| p011 | 公園的鐵欄杆，為什麼摸起來比木椅冰那麼多？ | OK | HyperPhysics | 已照 verify-1 F01 加「摸起來」 |
| p015–p016 | 隔天早上，溫度計量到的跟房間差不多；它沒有比較暖？ | OK | OpenStax 13.1 | 內容同 verify-1 已查核的句子，只是改了說法；「差不多」措辭恰當 |
| p022–p023 | 打開來看只有羽絨和布；它要是會發熱，溫度計早就量到了 | OK | OpenStax 13.1 | 放了一整晚的東西如果自己會產熱，裡面的溫度會一直比周圍高；量到跟房間差不多，就表示它沒有在產熱。推理正確 |
| p039 | 發抖時放出的熱可以是安靜坐著的好幾倍 | OK | OpenStax 7.8 表 7.5 | 已照 verify-1 F02 改 |
| p051–p052 | 熱不會倒過來跑嗎？自己不會。你的手，從來不會被冰塊弄得更暖 | OK | OpenStax 15.3 | "Heat transfer occurs spontaneously from higher- to lower-temperature bodies but never spontaneously in the reverse direction."「自己不會」正好對應 spontaneously（冰箱靠外力把熱往外搬，不算「自己」）。手的溫度一定高於冰塊，所以「從來不會被冰塊弄得更暖」成立 |
| p064 | 其實差不多一樣冷 | OK | HyperPhysics | 已照 verify-1 F03 改 |
| p071–p072 | 羽絨衣的拉鍊頭也比布冰；同一件衣服、同一個溫度，金屬就是比較會搬熱 | OK | HyperPhysics；OpenStax 14.5 表 14.3 | 同一件衣服放在同一個房間，拉鍊頭和布同溫；金屬導熱比布和背後的羽絨快得多，摸起來就冰。HyperPhysics："steel feels colder than wood because its thermal conductivity is much higher"。拉鍊頭也有塑膠或包橡膠的，但畫面（kid-zipper-pull）明寫 metal zipper pull，所長下一句也說「金屬」，片中這件是金屬的，可以 |
| p077 | 身邊最會擋熱的，是空氣 | OK | OpenStax 14.5 表 14.3 | 已照 verify-1 F04 改 |
| p088 | 一團羽絨傳熱的本事，跟空氣差不多 | OK | OpenStax 14.5 表 14.3 | 已照 verify-1 F05 改（Down feathers 0.025、空氣 0.023） |
| p092 | 空氣被關在這些小空間裡，想飄也飄不走 | OK | OpenStax 14.6 | "trapping it in spaces too small to support convection"。「飄不走」回呼 p082「被弄暖就往上飄走」，說的是對流被擋住，正確 |
| p094–p095 | 一大片空氣會自己轉圈，把熱帶走；切成很多很小的格子，它才轉不起來 | OK | OpenStax 14.6 | 自然對流在大空間裡形成循環（暖的上升、冷的下沉）；"spaces too small to support convection"。「轉圈」對兒童是合理的說法 |
| p096 | 擋熱的不是羽毛本身，是羽毛關住的空氣 | OK | OpenStax 14.5、14.6 | "incorporate many small pockets of air, taking advantage of air's poor thermal conductivity"。中文「羽毛」包含羽絨，回答的是 p087 小問「羽毛很暖」的猜想，可以。若想跟 p088 用字一致，可改「羽絨」（非必要） |
| p106–p107 | 坐在羽絨衣上，屁股底下那一塊被壓得最扁 | OK | OpenStax 14.6（機制推得） | 攤開坐上去時，全身重量壓在屁股與大腿下面，其他地方只承受衣服自己的重量，屁股下面最扁是直接的力學結果；接著 p104–p105 已講過扁掉的地方關住的空氣變少、沒那麼暖。沒有給數字，可以 |
| p115 | 衣服一濕，熱就跑得快很多，穿起來就沒那麼暖 | OK | ColumbiaDoctors | 已照 verify-1 F06 改。"Wet clothing greatly increases heat loss through conduction and evaporation." |
| p116 | 羽絨濕了還會塌下去，撐不起那些小空間 | OK | US4992327 | 已照 verify-1 F07 改 |
| p121–p123 | 還記得那層會往上飄的暖空氣嗎？風一來，它還沒飄走就被吹散；冷空氣換得更勤，熱就跑得更快 | OK | OpenStax 14.6；NWS | "A cold wind is much more chilling than still cold air"；NWS："As the wind increases, it draws heat from the body"。「還沒飄走就被吹散」說的是貼身那層暖空氣被風刮薄、換得更快，對兒童是正確的簡化，也跟卡片 wind-chill「沒有風：換得慢／有風：一直被換掉」一致 |
| p124 | 這就叫做風寒：同樣的溫度，有風就覺得冷很多 | OK | NWS | 已照 verify-1 F08 改 |
| p126 | 外面那層布也最好別讓雨滲進去 | OK | ColumbiaDoctors；US4992327 | 濕衣服熱損失大增；羽絨泡水後密度變高、蓬鬆度下降。「最好」措辭恰當，接得上 p111–p116 淋濕那段 |
| p128 | 那拉鍊沒拉好呢？ | OK | — | 問句 |
| p130 | 你應該被這樣冷過一次 | OK | — | 經驗句 |
| p136–p137 | 羽絨衣是把空氣關起來，它是連空氣都不要？ | OK | Wikipedia；伊利諾大學物理系 | 小問的說法，所長下一句用「幾乎」修正 |
| p138 | 羽絨衣裡的空氣動不了，熱還能慢慢碰過去 | OK | OpenStax 14.5、14.6 | 對流被擋住後，熱仍會以傳導慢慢穿過靜止的空氣（空氣 0.023 不是 0）。「慢慢」正確 |
| p139 | 保溫瓶中間幾乎什麼都沒有，熱連碰都很難 | OK | Wikipedia；伊利諾大學物理系 | "a partial-vacuum which reduces heat conduction or convection"。「幾乎」「很難」措辭正確；說的是夾層，沒有說整個瓶子擋住全部的熱，所以不跟瓶口傳熱的事實衝突（verify-1 F09、F10 的問題已隨改寫消失） |
| p140–p141 | 保溫瓶是更厲害的羽絨衣？可以這樣想，只是它穿不上身 | OK | 同上；OpenStax 14.5 | 兩者都靠擋住熱的路；羽絨衣還留著靜止空氣可以傳熱，真空夾層連這條路都幾乎擋掉，同樣厚度下更會擋熱，「更厲害」成立。「可以這樣想」是比喻的口氣，不是精確比較 |
| p144 | 羽絨衣也一樣，它不管熱是往裡還是往外 | OK | SFI；Tes；ASHRAE／WGBH | SFI："the coat will keep the snowman cold by not letting the warmer air in"；Tes："the insulating material cannot be heating the ice up"；ASHRAE："Insulation is a material that slows heat energy from passing through it." 保暖材料只是讓熱難以通過，不分方向 |
| p148–p149 | 開頭那顆包著羽絨衣的冰塊呢？會融得更快吧？ | OK | — | 回收開場的問題；小問的猜想 |
| p151 | 只會讓房間的熱，很難跑進去 | OK | SFI | "not letting the warmer air in"。「很難」沒說完全擋住，正確（前半句見 G01） |
| p154 | 包起來，反而比較慢？！ | OK | SFI；Tes | 小問的反應，結論同 p153 |
| p155–p156 | 穿上會暖，是我的熱被它留住了 | OK | SFI；OpenStax 14.6 | "Coats keep you warm by keeping the heat of you body in" |
| p157–p158 | 剛拿出來冰冰的，要等我的熱，先把裡面弄暖 | OK | OpenStax 13.1、14.5 | 剛穿上時衣服內面跟房間同溫，你的熱先流進去把內襯和貼身空氣弄暖，之後熱才跑得慢。物理正確 |
| p164 | 慢慢暖起來的那個，就是你自己 | OK | SFI | 意思是暖來自你自己的熱；修辭句，與全片結論一致（前半句見 G03） |

### 說明、卡片與章名

| 項目 | 內容 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| `youtube.description` | 「寒流來的早上……」、「鐵欄杆為什麼摸起來比木椅冰」 | OK | HyperPhysics | 已照 verify-1 F12 改；其餘文字未改，verify-1 已查 |
| 卡片 iron-wood `data.title` | 溫度差不多，摸起來不一樣 | OK | HyperPhysics | 跟 p064「差不多一樣冷」一致 |
| 卡片 wind-chill `left.points[0]` | 身上那層暖空氣換得慢 | OK | OpenStax 14.6 | 已照 verify-1 F11 改 |
| 章名 closet-jacket | 寒流那天，羽絨衣是冰的 | OK | OpenStax 13.1 | 寒流時房間冷，衣服跟房間同溫，「冰」是摸起來的口語說法 |
| 章名 kid-thermometer | 溫度計在羽絨衣裡放了一晚 | OK | — | 對應 p014「你可以試試看」的想像實驗，不是宣稱做過 |
| 章名 chief-temper | 鐵欄杆其實沒有比較冷 | OK | HyperPhysics | 否定的是「鐵本來就比較冷」，跟「差不多一樣冷」一致 |
| 章名 chief-air | 羽絨把空氣關了起來 | OK | OpenStax 14.6 | — |
| 章名 chief-not-heater | 包起來的冰塊融得比較慢 | OK | SFI；Tes | 事實正確。另見下方「非事實的備註」 |

## 三、畫面提示詞

新增 10 個、改過 2 個，逐一看過，沒有畫出錯誤事實的：

- kid-reverse-q（小問捏著冰塊瞇眼看）、chief-one-way、chief-same-coat、chief-sit、chief-zip、chief-cant-wear：只有表情與手勢，沒有事實內容。
- kid-zipper-pull：同一件珊瑚橘羽絨衣的**金屬**拉鍊頭，跟 p071–p072 一致。
- kid-sit-jacket：羽絨衣攤在公園長椅上、小問坐在上面，跟 p106–p107 一致。
- kid-better-coat：小問把保溫瓶抱在胸前像件小外套，配的是比喻句，可以。
- kid-zip-up：小問把羽絨衣像毯子一樣披在肩上；台詞「下次你穿上它」是對觀眾說的，畫面沒穿上也不衝突（NOTES 規定小問不穿上主線外套）。
- chief-feather（改）：一團白色羽絨，跟 p088「一團羽絨」一致，verify-1 F13 已處理。
- thermos-magnifier（改）：加了 "the two walls joined only at the rim"，正確（伊利諾大學物理系："except perhaps at the lip where the walls are joined together"）。

## 非事實的備註（不影響查核結論，給撰稿者參考）

- 章名「包起來的冰塊融得比較慢」出現在 p150 開頭，比 p153 揭曉早三句；YouTube 章節列表一打開就看得到，等於先講掉 p009–p010 的開場題。要保留懸念，可以改成事件式但不給答案的章名（例如「那顆包著羽絨衣的冰塊」）。
- p096 用「羽毛」、p088 用「羽絨」，意思都對；想統一可以都用「羽絨」。

## 建議修改

- p150：很多人都會這樣猜。可是它沒有熱可以給冰塊， → 很多人都會這樣猜。可是它裡面沒有暖爐，（17 字）
  （另一個也正確的寫法：很多人都會這樣猜。可是它自己不會發熱，17 字）
- p129：風就從前面灌進去，把關住的空氣換掉。 → 風就從前面灌進去，把貼著你的暖空氣吹走。（18 字）
- p163：下次你穿上它，等個幾秒， → 下次你穿上它，等一下下，（10 字）
- 章名（scene `chief-same-job` 的 `chapter`）：保溫瓶連空氣都抽掉了 → 保溫瓶把空氣幾乎抽光了
- 改 `build_scenes.py` 後重產 `video.json` 與 `script.md`（NOTES：不要只改 `video.json`）。

## 來源

這一輪實際打開並讀到原文的頁面，格式可直接放進 `video.json` 的 `sources`。前兩筆是現有 `sources` 沒有、建議新增的（p052、p129 的依據）；其餘已在 `sources` 裡。

```json
[
  {"title": "OpenStax College Physics 2e: 15.3 Introduction to the Second Law of Thermodynamics", "url": "https://openstax.org/books/college-physics-2e/pages/15-3-introduction-to-the-second-law-of-thermodynamics-heat-engines-and-their-efficiency", "checked_on": "2026-11-04"},
  {"title": "Kim & McCullough (2001), The Effect of Adjustable Garment Closures and Layering on Insulation in Cold Weather, The Korean Fashion and Textile Research Journal 3(5)", "url": "https://koreascience.or.kr/article/JAKO200123659443366.page", "checked_on": "2026-11-04"},
  {"title": "ColumbiaDoctors: Cold Exposure, Ways the Body Loses Heat", "url": "https://www.columbiadoctors.org/health-library/article/cold-exposure-ways-body-loses-heat", "checked_on": "2026-11-04"}
]
```

其餘引用（OpenStax 7.8、13.1、14.5、14.6，HyperPhysics，NWS，伊利諾大學物理系，Wikipedia Vacuum flask，SFI，Tes，US4992327）沿用 verify-1 讀到的原文；ASHRAE／WGBH 的那句引文取自 claims.md C07，verify-1 與這一輪都沒有重新打開，p144 另有 SFI、Tes 支持，不靠它。
