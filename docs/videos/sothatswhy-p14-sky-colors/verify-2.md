# 查核報告 2（sothatswhy-p14-sky-colors）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有做查核第 1 輪）
- 日期：2026-11-06
- 範圍：`git diff HEAD~1 -- script.md claims.md video.json`（commit 816c7eb5b「revision after fact-check round 1 and the blind panel」）改動或新增的部分。比對時先去掉台詞編號再逐句對照（修改後台詞從 p001–p265 重新編號成 p001–p262），所以下表的行號都是**現在** `video.json` 的編號。沒改動的句子沿用 verify-1 的結論，不再重查。`script.md` 是 `build_scenes.py` 產生的，抽查改過的 11 句都與 `video.json` 一致，舊句（「四倍」「一九一一」「好久」「噴到」）都已不在。
- 方法：逐句讀新增與改寫的 33 句台詞、改過的 1 個與新增的 5 個 `shot` 提示詞、`sources`，以及 claims.md 的改動。被刪掉的 23 句（太陽旁偏白與背對太陽、海水吸收紅光、大氣折射三段，對應 C04、C18 與 C19 的海水部分）不再需要查核。來源都重新打開讀原文（curl 抓頁面轉成文字後逐句比對）；牛頓的國籍是 claims.md 沒有涵蓋的新主張，另找了來源。
- 打不開的來源：NOAA JetStream「The Color of Clouds」用 curl 仍回 403（CloudFront），改用 WebFetch 讀到原文，p135 用到的句子核對過。其餘來源都直接讀到。
- 字數上限：小問 ≤15 字、所長 ≤25 字，數法照 `build_scenes.py` 的 `length()`（不算標點），用程式數過全部 262 句，沒有超過的。本輪沒有替換句。
- 結論統計（新增或改寫的台詞 33 句）：OK 33、FIX 0、NOT FOUND 0。另外標題、說明、縮圖、章名都沒改動（沿用 verify-1 的 OK）。畫面提示詞 6 個：全部 OK。
- verify-1 的 7 項 FIX（F01–F06，F04 是 p154–p155 一組）都已改成來源支持的說法；F02、F03、F04 的字句與建議不同，但意思正確（見下方第一節）。verify-1 的可選建議（four-blue 改 "several"）也已採用。

## 一、第 1 輪 FIX 的落實情形

| 第 1 輪 | 現在的行 | 現在的句子 | 結論 | 依據 |
| --- | --- | --- | --- | --- |
| F01 | p079（所長） | 藍光被彈開的，比紅光多好幾倍。 | OK | 與建議字句相同。JetStream "about four times stronger than red light waves"、Gibbs "(700/400)^4 ~= 10"、Corfidi "three to four times"，「好幾倍」在三種取法下都成立。p080 小問「好幾倍？藍光好忙！」只是反應 |
| F02 | p091（所長） | 後來，物理學家愛因斯坦在一九一〇年算出來： | OK | Wikipedia「Critical opalescence」："In 1910 Albert Einstein showed that the link between critical opalescence and Rayleigh scattering is quantitative"，書目 Einstein, A. (January 1910), Annalen der Physik 33 (16): 1275–1298。加了「物理學家」也正確。claims.md C14 的年份也已改成 1910 |
| F03 | p135（所長） | 晴天時，一半以上的陽光，還是直直照到地面。 | OK | JetStream："over one-half of the sun's white light continues through the atmosphere reaching the Earth's surface"（WebFetch 讀到）。直射部分：PVEducation 的 I_D = 1.353 · 0.7^(AM^0.678)，"about 70% of the radiation incident on the atmosphere is transmitted"；"The intensity of AM1.5D radiation can be approximated by reducing the AM0 spectrum by 28%"。代入 AM1、1.5、2 分別約為 70%、62%、56%，台灣冬天中午（天頂角約 48°，AM 約 1.5）也超過一半。附註：太陽很低時（AM 約 2.6 以上）即使晴天直射也會低於一半，但這段講的是「白天」（p136–p137），不必再加限制 |
| F04 | p150–p151（所長） | 等太陽貼到地平線上，光要穿過的空氣，／大約是太陽在頭頂時的三十多倍。 | OK | 數字現在掛在「貼到地平線上」。Wikipedia「Air mass (solar energy)」："At sea level the air mass towards the horizon (z = 90°) is approximately 38"。前一句 p148–p149「快下山時……斜斜地，貼著地面穿過來」沒有數字，時間點不再混淆。兩句合計 30 字，比原本多 5 字，但各句都在 25 字上限內 |
| F05 | p154（小問） | 光要走好長的路！ | OK | 與建議字句相同；說的是路長，不是時間 |
| F06 | p232（所長） | 後來細細的小顆粒，飄在大約二、三十公里高。 | OK | Corfidi："exist as thin veils of dust or sulfuric acid droplets at altitudes of 12 to 18 miles"（約 19–29 公里），是停留高度。加了「後來」更貼近 Wikipedia「1991 eruption of Mount Pinatubo」："Sulfur dioxide oxidized in the atmosphere to produce a haze of sulfuric acid droplets, which gradually spread throughout the stratosphere over the year following the eruption"（噴發時火山灰柱 "35 km (22 mi) into the atmosphere"，台詞沒有說噴多高）。p233「飛那麼高？」仍接得上 |

## 二、逐項核對（新增與改寫的句子）

### 台詞

| 行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p015–p017 | 月球上？我猜不出來。可是還有雲！天空是藍的，雲怎麼是白的？ | OK | — | 小問的反應與問題，沒有事實主張；答案在 p189–p192、p247–p252 |
| p029 | 它們一起跑進眼睛，大腦就把它們看成白的 | OK | NASA Goddard | "Our brains then integrate these signals into a perceived white color."（與 verify-1 已查的舊 p036–p037 同一件事，移到這裡） |
| p034 | 很久以前，英國科學家牛頓，就用三稜鏡把陽光分開過 | OK | Gibbs；Wikipedia「Isaac Newton」 | Gibbs："This was demonstrated by Isaac Newton, who used a prism to separate the different colours and so form a spectrum."；Wikipedia："Sir Isaac Newton (… 1643 – 1727) was an English polymath who was a mathematician, physicist, astronomer …"。「英國」對應 English，中文慣用說法；「科學家」對應 physicist／astronomer。Gibbs 沒寫國籍，建議把 Wikipedia 這一頁加進 `sources`（見文末） |
| p037–p038 | 對，一個都沒少。白光好擠喔！ | OK | Gibbs | 回答 p035–p036 小問列的六色「全部擠在白光裡？」。Gibbs："The white light from the Sun is a mixture of all colours of the rainbow"。「一個都沒少」說的是她列的顏色都在，不是說只有這六色 |
| p080 | 好幾倍？藍光好忙！ | OK | — | 小問的擬人化反應 |
| p109 | 陽光裡的紫光，本來就比較少 | OK | Gibbs | "the spectrum of light emission from the Sun is not constant at all wavelengths … giving less violet in the light" |
| p110–p111 | 有一些在很高的空中，被那裡的空氣吸收了；吸收就是被吞進去，到不了地面 | OK | Gibbs | "and additionally is absorbed by the high atmosphere, giving less violet in the light"。「有一些」對應 part of the answer，沒有說全部；「到不了地面」說的是被吸收的那一部分，定義上成立。p114–p117 仍說天空裡有紫光，不矛盾 |
| p112 | 空氣還會偷吃一點！ | OK | Gibbs | 小問的白話；「一點」措辭恰當 |
| p122 | 我的眼睛是調色盤！ | OK | — | 小問的比喻，接 p121「眼睛也參了一腳」（verify-1 已 OK） |
| p136–p137 | 難怪白天，地上還是亮亮的！ | OK | JetStream | 與 verify-1 已查的舊 p141 同一件事，改由小問說 |
| p159–p162 | 日出也是這樣嗎？一樣，日出的時候，光也是貼著地面斜斜穿過來，只是太陽換到了東邊 | OK | HyperPhysics Red Sunset；Corfidi；UCAR Colors of the Sky | HyperPhysics："The equivalent phenomenon can be seen at sunrise"；Corfidi："At sunrise or sunset, sunlight takes a much longer path through the atmosphere than during the middle part of the day"；UCAR："During sunrise and sunset, the Sun is low in the sky. Light has to travel through more atmosphere than it does when it's overhead." 太陽從東邊升起是常識 |
| p186–p188 | 做完杯子，你再抬頭看看窗外的雲。雲也被同一個太陽照，它怎麼不藍也不紅？ | OK | — | 轉場與問題，沒有事實主張 |
| p215 | 這種霧濛濛的一層，叫做霾 | OK | Wikipedia「Haze」；Corfidi | Wikipedia："Haze is traditionally an atmospheric phenomenon in which dust, smoke, and other dry particulates suspended in air obscure visibility and the clarity of the sky."「這種」指上一句 p213–p214 灰塵和煙造成的「一層白紗」，正好是 haze 的定義；Corfidi 也稱近地面那層 "contains most of the atmosphere's dust and haze" |
| p216 | 霾多的時候，中午的天空也可能白白一片 | OK | UCAR Colors of the Sky；Corfidi | UCAR："When there are lots of aerosols, the sky might even look white in the middle of the day, even if there are no clouds."；Corfidi："hazy daytime skies, instead of being bright blue, appear grayish or even white"。「可能」措辭恰當 |
| p227–p228 | 所以傍晚最紅的，常常是高高的雲：照到它的光，還沒穿過底下那層霾 | OK | Corfidi | "To produce vivid sunset colors, a cloud must be high enough to intercept "unadulterated" sunlight...i.e., light that has not suffered attenuation and/or color loss by passing through the atmospheric boundary layer. (The boundary layer is the layer near the surface which contains most of the atmosphere's dust and haze). This largely explains why spectacular shades of scarlet, orange, and red most often grace cirrus and altocumulus layers, but only rarely low clouds such as stratus or stratocumulus." 「常常」對應 most often；Corfidi 說的「高」包括中層的高積雲，台詞的「高高的雲」是相對於低雲，可以。「所以」接 p224–p226 飛機爬過霾的段落，邏輯一致 |
| p229 | 高的雲，先拿到紅光！ | OK | Corfidi | 小問的白話：高雲收到的光還沒被底下的霾削弱。附註：「先」也可能被聽成時間上先變紅（日落時其實是高雲比低雲**晚**暗下來）；若想避開，可改「高的雲，最先染紅！」（7 字）也同樣有歧義，或「高的雲，紅得最漂亮！」（8 字）——非必要 |
| p254–p256 | 我在頂樓看到的藍和紅，是同一道光，走了短的路和長的路！ | OK | HyperPhysics Red Sunset；UCAR | 小問的總結，重述 p146–p156：頭頂時穿過的空氣少、地平線時多。說的是藍天與紅太陽分別對應短的與長的光路，與 verify-1 已查的內容一致；p005 也已說是「同一道陽光」 |

### 說明、卡片與章名

`youtube.title`、`youtube.description`、`thumbnail` 與 7 個章名都沒有改動，沿用 verify-1 的 OK。本集沒有卡片。

## 三、畫面提示詞

改過 1 個、新增 5 個，逐一看過，沒有畫出錯誤事實的：

- four-blue（改）：已採用 verify-1 的可選建議，"several short bright blue arrows" 對一支紅箭頭，與 p079「好幾倍」一致。
- kid-busy、chief-absorb、kid-absorb、chief-high-cloud：只有表情與手勢（揮手、握拳像接住東西、驚訝的 O 嘴、舉手），沒有事實內容。
- kid-bright：小問在陽光下的頂樓張開手臂，配 p136–p137「白天地上還是亮亮的」，正確。

刪掉的 8 個場景（kid-near-sun、chief-near-sun、kid-turn、kid-sea-why、chief-sea-why、chief-bend、kid-bend-q、chief-bend2）隨台詞一起移除，不再需要查核。

## 非事實的備註（不影響查核結論，給 claims.md 的維護者參考）

- claims.md「撰稿提醒」仍寫「『超過一半的陽光』到達地面（C17）」，C17 的標題也仍是「超過一半的陽光仍然直接照到地面」；片中已改成「晴天時，一半以上的陽光」。不影響影片，可以順手同步。
- C19 新增的「這種霧濛濛的一層，叫做霾」沒有列出定義霾的來源；本輪用 Wikipedia「Haze」核對，可加進 claims.md 的來源清單。
- C08 的「可用說法」已與 p148–p151 一致；C12、C14 的改動與片中一致。

## 建議修改

- 台詞：無。
- （可選）p229：高的雲，先拿到紅光！ → 高的雲，紅得最漂亮！（8 字，與原句同長）
- `sources` 加一筆 Wikipedia「Isaac Newton」，作為 p034「英國科學家」的依據（Gibbs 沒寫國籍）。

## 來源

這一輪實際打開並讀到原文的頁面，格式可直接放進 `video.json` 的 `sources`。前兩筆是現有 `sources` 沒有、建議新增的（p034、p215 的依據）；其餘已在 `sources` 裡。

```json
[
  {"title": "Wikipedia: Isaac Newton", "url": "https://en.wikipedia.org/wiki/Isaac_Newton", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Haze", "url": "https://en.wikipedia.org/wiki/Haze", "checked_on": "2026-11-06"},
  {"title": "Philip Gibbs, Why is the sky blue? (Physics FAQ, UC Riverside)", "url": "https://math.ucr.edu/home/baez/physics/General/BlueSky/blue_sky.html", "checked_on": "2026-11-06"},
  {"title": "Stephen F. Corfidi, The Colors of Sunset and Twilight (NOAA/NWS Storm Prediction Center)", "url": "https://www.spc.noaa.gov/publications/corfidi/sunset/", "checked_on": "2026-11-06"},
  {"title": "NOAA JetStream: The Color of Clouds", "url": "https://www.noaa.gov/jetstream/clouds/color-of-clouds", "checked_on": "2026-11-06"},
  {"title": "UCAR Center for Science Education: The Colors of the Sky", "url": "https://scied.ucar.edu/kids/sky-wonders/colors-sky", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics: Red Sunset, Green Flash", "url": "https://hyperphysics.gsu.edu/hbase/atmos/redsun.html", "checked_on": "2026-11-06"},
  {"title": "NASA Goddard: What Color is the Sun?", "url": "https://science.gsfc.nasa.gov/attic/eclipse2017.gsfc.nasa.gov/what-color-sun.html", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Air mass (solar energy)", "url": "https://en.wikipedia.org/wiki/Air_mass_(solar_energy)", "checked_on": "2026-11-06"},
  {"title": "PVEducation: Air Mass", "url": "https://www.pveducation.org/pvcdrom/properties-of-sunlight/air-mass", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Critical opalescence (Einstein 1910)", "url": "https://en.wikipedia.org/wiki/Critical_opalescence", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: 1991 eruption of Mount Pinatubo", "url": "https://en.wikipedia.org/wiki/1991_eruption_of_Mount_Pinatubo", "checked_on": "2026-11-06"}
]
```

其餘引用（NASA Space Place、UCAR Appearance of the Sky、HyperPhysics Blue Sky、NASA Science 月球南極、NASA Dark Sky, Bright Sun）只支持沒改動的句子，沿用 verify-1 讀到的原文。
