# curio-h03-v2 查核第二輪

- 查核 2026-10-13，Claude Opus 5（第三個代理：不是撰稿的那一個，也不是第一輪查核的那一個；這一版的任何一句、第一輪的任何一條判定，我都沒有參與）。
- 範圍照啟動說明：第一輪要求的十二條（[`verify-1.md`](verify-1.md) 的 C1–C12）加上撰稿方自己找到的兩條（一九三〇年提的是「一顆彗星」而不是彗星的碎片、第 7 章章名），
  一共十四條全部重判；第一輪沒有抽的七個章名全部補查；第一輪的 105 條 CONFIRMED 抽 50 條重驗（超過三分之一的 35 條）；
  再按啟動說明回答第 3 點（八千萬棵樹與不能講的事）與第 4 點（未結的事在每一個出口）。
- 方法：先把 `video.json` 重新抽一遍——旁白 158 句、7 張卡片的 `data` 欄、**7 個 `chapter` 欄**、標題、說明欄 5 段、10 個標籤、縮圖 4 欄、`sources[]` 22 筆、`loops[]` 5 筆、112 個 `prompt`——
  再逐條對回 [`claims.md`](claims.md) 的 42 列與 [`../history-curiosity/topic-checks/H03.md`](../history-curiosity/topic-checks/H03.md)，然後才去看第一輪的主張表，
  避免拿它的結論當起點。中間檔在 `<tmp>\scratchpad\v2h03\`（`extract.mjs`、`fetch.mjs`、`totext.mjs`、`q.mjs`、`lines.tsv`、`full.txt`、`http-status.json`、`pages\`、`text\`）。
- 網址我今天自己重開了 24 個（第一輪的 22 筆來源＋Britannica 直連＋RMG）：`curl`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，
  同一主機之間用 1.4 秒的間隔（`fetch.mjs` 按主機記時間戳，所以 web.archive.org 的四筆也是一筆一筆隔開拿的）。
  L07 是 19.3 MB 的 PDF，用 `pdftotext -layout` 取出 80 KB 全文；BSE 以 windows-1251 解碼；其餘 HTML 去標籤後讀全文。下一節是我今天親自拿到的 HTTP 狀態。沒有用網路搜尋（0 次）。
- **Britannica 今天直連回 200**（第一輪與查核檔當天都是 403）。我把直連頁與存檔頁的正文逐句比對過，署名 Edward F. Tedesco 的那段正文兩邊一致，所以第一輪用存檔取的引句今天仍然成立。
  要注意的是 Britannica 頁首現在有幾段標著「This answer is created from Britannica articles using AI」的問答，裡面也有 2,000 km²、15 Mt、comet／asteroid 這些數字；我一律只採署名正文，沒有引那幾段。
- 啟動說明交代的事我都照做了：沒有動 `video.json`、`claims.md`、`brief.md`、`NOTES.md` 的任何一個位元組；沒有跑 git；沒有跑任何影片階段（含 `lint`）；沒有花任何供應商的錢。
  句長我是直接呼叫 `tools/video/core/timeline.mjs` 的 `spokenUnits()` 算的（只是一個函式，不是階段），結果在〈第 6 點〉。

## 當天開過的網址

| 縮寫 | 網址 | HTTP | 備註 |
|---|---|---|---|
| N115 | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ | 200 | |
| N19 | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ | 200 | |
| EO | https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | 200 | 頁面標 Jun 30, 2025 |
| N08 | https://web.archive.org/web/20210101030522/https://science.nasa.gov/science-news/science-at-nasa/2008/30jun_tunguska/ | 200 | 存檔（原址仍 404） |
| EB | https://web.archive.org/web/20260901073916/https://www.britannica.com/event/Tunguska-event | 200 | 存檔 |
| EB（直連） | https://www.britannica.com/event/Tunguska-event | **200** | 第一輪 403；正文與存檔一致 |
| L07 | https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf | 200 | 19,348,345 bytes；`pdftotext` 全文 80 KB |
| BB25 | https://www.nature.com/articles/s41598-025-98362-9 | 200 | |
| SNL | https://newsreleases.sandia.gov/releases/2007/asteroid.html | 200 | |
| C93 | https://www.nature.com/articles/361040a0 | 200 | |
| AM65 | https://www.nature.com/articles/206861a0 | 200 | |
| BH73 | https://www.nature.com/articles/245088a0 | 200 | |
| BT74 | https://www.nature.com/articles/250555a0 | 200 | |
| R17 | https://link.springer.com/article/10.1134/S1028334X17100269 | 200 | |
| J19 | https://web.archive.org/web/20260411202527/https://ui.adsabs.harvard.edu/abs/2019Icar..327....4J/abstract | 200 | 存檔摘要 |
| G07 | https://web.archive.org/web/20230211163937/https://onlinelibrary.wiley.com/doi/10.1111/j.1365-3121.2007.00742.x | 200 | 存檔 |
| C08 | https://web.archive.org/web/20230210215017/https://onlinelibrary.wiley.com/doi/10.1111/j.1365-3121.2008.00791.x | 200 | 存檔 |
| APS | https://www.aps.org/apsnews/2018/06/tunguska-event | 200 | 一次就通，沒有被重設 |
| OSU | https://origins.osu.edu/milestones/june-2018-1908-tunguska-event-and-threats-tomorrow | 200 | |
| LH | https://www.lindahall.org/about/news/scientist-of-the-day/leonid-kulik/ | 200 | |
| AOP | https://armagh.space/weather/history/tunguska-event | 200 | |
| BSE | https://booksite.ru/FullText/1/001/008/067/252.htm | 200 | windows-1251 |
| COMMONS-SZ | https://commons.wikimedia.org/wiki/File:1908-07-29-SibirskayaZshizn-135.jpg | 200 | |
| RMG | https://www.rmg.co.uk/stories/space-astronomy/tunguska-event | 200 | 只為核對那個不能引的面積，與第一輪的一個註記（見〈附註〉） |

`sources[]` 現在的 22 筆，我今天一筆一筆重開，**全部 200**；22 筆正好等於 `claims.md` 引用的 22 個網址，沒有多也沒有少（我用程式比對過兩邊的網址集合）。
查核檔列的 K49（tunguska.tsc.ru）與其餘維基共享檔案頁這一輪同樣沒有開：`assets[]` 仍是空陣列、全稿沒有照片卡，照片授權、一九二九年、攝影者都不入稿，開了沒有對應的主張。

## 十四條改動，逐條重判

判定：CONFIRMED 現在這句站得住／CHANGED 還要改。「來源句」是我今天在頁面上讀到的原文。

| # | 行／欄 | 現在的句子 | 來源句（我今天讀到的） | HTTP | 第二輪判定 |
|---|---|---|---|---|---|
| C1 | `tg5k` | 一九七三年，有人提出是一個小黑洞。 | BH73 摘要全文只到 "We suggest that a **black hole of substellar mass** such as those that have been postulated by Hawking could explain many of the mysteries associated with the event."；L07「antimatter meteors (Cowan et al. 1965), and **tiny black holes** (Jackson and Ryan 1973)」。「穿過地球」在 BH73、BT74、L07 全文都沒有 | 200 | CONFIRMED（「小」掛在 substellar／tiny 上，站得住） |
| C2 | `tg4w` | 彗星說靠的是事後那幾個亮著的晚上。 | APS「This notion was first proposed in 1930 by British astronomer F. J. W. Whipple – **a hypothesis supported in part by the glowing skies observed after the blast**. The dust and particles that caused the glow could have been debris from the disintegrated comet's tail.」；AOP「**The glowing skies** – suggesting high levels of water vapour in the atmosphere – **are more likely to occur due to a comet**」；EB「On the basis of historical records of significant noctilucent cloud development in the skies over Europe following the event, some scientists contend that a comet caused the explosion.」 | 200 | CONFIRMED（三個來源；比第一輪預期的更穩，而且與 `tg5g` 不再相衝） |
| C3 | `tg1i` | 他們不知道那是什麼。 | OSU 記的是那兩個人的反應：「something suddenly hit her tent and 'I was scared, screamed, and woke up Ivan.' As they got up, the tent shook again knocking them over. They heard a thunderous noise, saw blinding light, and felt intense heat」。**沒有一頁寫他們不知道那是什麼**；L07 唯一相近的一句「Many correspondents could not understand what they have seen or heard」講的是寫信給伊爾庫次克觀測站的通訊員（第 2 章的事），不是帳篷裡那兩個人。而本集 `tg2l` 又說「他們認為，是神靈奧格迪降臨了」 | 200 | **CHANGED**（見〈還要改的〉R1） |
| C4 | `tg3q`、`no-crater.data.sub` | 到今天，方圓一萬五千平方公里之內都沒有坑。／卡片 sub「到今天，一萬五千平方公里之內都沒有」 | L07「neither macroscopic fragments of the cosmic body, nor a typical signature of an impact, like a crater, **have ever been found in an area of 15 000 km2**」；「到今天」另有三個較新的來源撐著：N19（2019）「no one found a crater and no one found fragments」、EO（2025）「Direct evidence of craters or the bolide that caused the explosion **remains elusive** and a topic of ongoing study and debate」、EB（2026 存檔與直連）「no impact crater」 | 200 | CONFIRMED（年代併接已解。面積那個數字是 L07 寫到二〇〇七年的，「到今天」靠 N19／EO／EB，兩邊都有來源；卡片 kicker 仍只說「一九二七年的爆心」，sub 以「到今天」開頭把它分開，整張卡讀起來不再把一個世紀的搜尋結果鎖在那一趟） |
| C5 | `tg3r` | 大塊的碎片也沒有。 | L07 的限定詞是 "neither **macroscopic** fragments"；EB「The only likely remains of the object that have been found are a few small fragments, each less than a millimetre across」；N115「later expeditions found microparticles… these remnants could not be conclusively tied to the blast」 | 200 | CONFIRMED（貼回來源，也解掉與 `tg4q` 的矛盾） |
| C6 | `outro.data.lines[0]` | 那個早上掉下來的東西，到今天還沒有找到 | EO「Direct evidence of craters or **the bolide that caused the explosion remains elusive**」；N115「these remnants could not be **conclusively tied to the blast**」；L07「have ever been found」；N19「no one found fragments」；G07「Fragments of the impacting body have never been found」 | 200 | CONFIRMED（不比紀錄更強，也不再碰切科湖那件沒有結論的事；而且仍然接得回 `tg1n` 的問句。全檔「落地」零次） |
| C7 | `tg4g` | 人和工具，全部搬進沼澤。 | APS 只有「when he finally **drained** one of the bogs」。木板與手搖幫浦只留在 `planks-across-the-peat`、`hand-pump-working` 的 `prompt` 裡 | 200 | CONFIRMED（沒有再指名任何器材；「工具」是「抽乾」本身就含的意思，不是新的紀錄主張） |
| C8 | `tg3m` | 那片枯樹，他叫它電線桿森林。 | LH「he encountered **what he called a "telegraph-pole forest,"** with dead trees still standing, but stripped on all their branches」 | 200 | CONFIRMED（一手的說法有主了。N08 另記 Yeomans 的轉述「They looked like a forest of telephone poles」，與這句相容） |
| C9 | `tg6t` | 抄到後來，它被當成不用附出處的事實。 | BB25「the "80 million trees" claim has propagated into other sources **as if it were** an established fact that needs no citation」 | 200 | CONFIRMED（「被當成」正好是 as if it were） |
| C10 | `sources[]` | 12 筆 → 22 筆 | 補進去的十筆（OSU、LH、BSE、AOP、Commons、G07 存檔、C08 存檔、AM65、BH73、BT74）我今天全部重開，全部 200；22 筆與 `claims.md` 引用的網址集合完全相同 | 200 | CONFIRMED。另外我量了一件第一輪沒量的事：**補十筆之後說明欄還放得下**——用 `composeDescription()` 組出來約 4,214 bytes，加上七行章節時間碼約 4,546 bytes，上限 5,000（`metadata.mjs` 的 `DESCRIPTION_MAX_BYTES`）。確切數字請在 `lint` 時看 |
| C11 | `tg2c` | 俄國當時用的是舊曆，那個早上寫的是六月十七日。 | OSU「They were in their tent near the Chambe River on **the morning of June 30, 1908 (June 17 according to the Russian calendar at the time)**」；COMMONS-SZ 的 Source 欄「№ 135. Стр. 4. **29 июня (старый стиль)**」（也就是報紙那一天的舊曆是六月二十九日） | 200 | CONFIRMED（指涉釘回爆炸那個早上，錯的讀法不會再得到錯的數字） |
| C12 | `tg2k` | 爆心附近的埃文基人，起初不願意跟外人談。 | N08「At first, the locals were reluctant to tell **Kulik** about the event」；APS 另給了一條第一輪沒有用到的支撐：「They proclaimed the blast site a sacred space and **guarded it zealously from outsiders – one reason it took nearly two decades before the first scientific expeditions arrived**」 | 200 | CONFIRMED，而且比第一輪想的更站得住：APS 把「不跟外人講」直接接到那將近二十年的空白上，所以這一句排在第 2 章（庫利克出場之前）現在也有來源，不只是「比較弱所以安全」 |
| 另一 | `tg4v` | 一九三〇年，有人提出它是一顆彗星。 | APS「the object that exploded in the atmosphere **was a comet** (possibly the Comet Encke). This notion was first proposed in 1930」；L07「Shapley (1930) was the first to suggest that the Tunguska event was caused by **the impact of a comet**」。兩頁都沒有「碎片」 | 200 | CONFIRMED（撰稿方補的這一條是對的。第一輪主張表第 66 列判了 CHANGED，但改動清單漏了它，指標誤寫成 C6——我核對過，C6 是片尾卡字那一條。現代兩說並列的「彗星碎片」只留在 `tg7v`，那裡有 AOP「a small comet (or a comet fragment)」撐著，不動是對的） |
| 另二 | 第 7 章 `chapter` | 它在半空中就炸開了（原「它根本沒有落地」） | N115「an asteroid plunged into Earth's atmosphere and **exploded in the skies over Siberia**」；EO「The explosion, **an airburst**, likely occurred about 6 to 10 kilometers… above the surface」；EB「Because the object **exploded in the atmosphere** high above Earth's surface, it created a fireball and blast wave but no impact crater」 | 200 | CONFIRMED（新章名講的是主流解釋，不是本集自己說沒有定論的那四件事；而且與片尾卡字的改法一致，兩個出口都不再有「落地」這個斷言） |

**計數：十四條裡 13 條 CONFIRMED、1 條 CHANGED（C3 `tg1i`）。** 另外第一輪列在〈附註〉、明說不要求改而留給第二輪再看的 `tg7aa`，我判 NOT FOUND（見 R2）。

### 第一輪的三個指標誤寫（給下一個人看，不必改稿）

核對十四條的時候對出三處：主張表第 19 列（`tg1n` 章末問句）寫「見 C5」、第 28 列（`rail-ends-at-the-forest`）寫「見 C4」，兩個其實都該指 C16（補豁免名單）；第 66 列（一顆彗星）寫「見 C6」，而改動清單裡根本沒有這一條。
三個裡只有第三個藏掉了一條該改的事實，撰稿方自己抓到了。`claims.md`、`NOTES.md` 現在的記載與實際改動一致，我沒有找到第四處。

## 第 2 點：兩個最重的位置，現在怎麼樣

**片尾卡字（C6）：過關。** 「那個早上掉下來的東西，到今天還沒有找到」——這一句我特別找了反證：EB 確實寫「a few small fragments, each less than a millimetre across」，可是它自己加了 "The only **likely** remains"，而 N115 直接寫那些微粒「could not be conclusively tied to the blast」，EO（2025）寫「the bolide that caused the explosion remains elusive」。
所以「還沒有找到」是紀錄的現狀，不是比紀錄更強的話；它也不再否定本集在 `tg7n`–`tg7q` 說沒有結論的那件事。
`script-writing.md` §結尾那條「片尾不可以比紀錄更強」、以及蓋「未結」的那一集「第一句就講紀錄確定了什麼、或紀錄拒絕了什麼」，兩條都符合：旁白 `tg7ad`「這份檔案，蓋的是未結。」（全片「未結」只唸這一次），卡面那一句只講紀錄裡有的。
唯一要記一筆的是它與 `tg4q`「後來有人找到一些微小的碎屑」聽起來有一點張力，但 `tg4r`「可是沒辦法確定它們跟那一聲有關」當場就解掉了，而且卡上講的是「那個早上掉下來的東西」（本體），不是「任何碎屑」。

**一萬五千平方公里（C4）：過關。** 旁白「到今天，方圓一萬五千平方公里之內都沒有坑」對上 L07 的 "have **ever** been found in an area of 15 000 km2"——這是累計的講法，不是一九二七年那一趟的結論；而「到今天」延伸到二〇二六年也有來源（N19 2019、EO 2025、EB 2026）。
卡片三行一起讀是「沒有坑／一九二七年的爆心／到今天，一萬五千平方公里之內都沒有」：大字與 kicker 講那一趟，sub 以「到今天」開頭把那個面積接到今天，兩件事分開了。
我也確認過卡上沒有新數字被改動，所以不需要補 `say`／`say_for`（`no-crater` 是 `big` 卡，三行都不是朗讀用的欄位）。

## 第 3 點：八千萬棵樹與不能講的事（我自己從來源查一遍）

**一、從頭到尾沒有當事實講。** 我用程式數過整個 `video.json`（旁白、卡片、標題、說明欄、標籤、縮圖、112 個 `prompt`、`loops`、`sources`）：「八千萬」只出現四次——
說明欄（加引號並當場否定：「最常被引用的『八千萬棵樹』不是數出來的」）、`loops[3].what`（內部標記，不唸不上畫面）、`tg3v`「**最常看到的數字**是八千萬棵倒樹」、`tg6a`「還記得那八千萬棵倒樹嗎？」（回扣同一個框）。
**標題、十個標籤、縮圖、七張卡片（含對照卡）一個棵數都沒有**；`tg6v` 還明說「這一集不會把它當事實講」。查核檔要的「棵數不上卡片」做到了。

**二、來歷掛在一九三三年、掛在高估約四倍的面積上。** BB25 的小節標題今天讀到的是 "Claims of more than eighty million fallen trees, up to 1-m in diameter, are exaggerated"，逐句對得上：
- `tg6d`／`tg6e`（那一年有人要估能量／要估能量先要知道面積）← "The sole aim of the primary source was to roughly estimate the energy of the explosion, **starting with an educated guess about the area** to approximate the number of fallen trees as a step toward his goal."
- `tg6f`（他假設那個面積是大約八千平方公里）← Astapovich 原句 "Apparently, it can be assumed that the area of the fallen forest occupies **about 8000 km2**"，結論 "the work of the windfall of 8⋅10⁷ trees would be 4.4⋅10²¹ ergs"
- `tg6h`／`tg6i`／`tg6k`／對照卡裁定 ← "the area of devastation that he **overestimated by a factor of about four**"、"**inflating the number of fallen trees by a factor of about four**"
- `tg6c`（一路追到一九三三年）← BB25 參考文獻 5＝Astapovich, *Astron. Zh.* 10, 465–486 (**1933**)

**三、引用鏈是評論自己的鏈條，不是本稿重排的，也不是本稿的算術。** BB25 的原句是 "The 80 million trees claim was **not actually made by Whipple but by a correspondent, based on Crommelin, whose source was Astapovich**"，
前面還有 "The '> 80 million trees' statement is a modified version of **Brazo and Austin**, who wrote 'eighty million trees in the taiga… were uprooted and blown down' with a citation to a **1934 paper by Whipple**"、"Since Brazo & Austin's **1982** article was published…"。
我核過參考文獻的年份：3＝Whipple (1934)、4＝Crommelin (1934)、5＝Astapovich (1933)、2＝Brazo & Austin (1982)。所以 `tg6p`「一九三四年有兩篇文章引了它」、`tg6q`「其中一篇引的，是一位通信者的話」、`tg6r`「不是作者自己說的」、`tg6s`「一九八二年又有人照抄」逐條成立，刊名與人名一個都沒唸。
`tg6i`「只有他假設的四分之一左右」是 BB25「a factor of about four」的倒數，不是 2,150÷8,000 的自算；**BB25 全文唯一的面積數字就是 Astapovich 的 8000 km²，它沒有提出自己的面積值**（我搜過全文），所以「把評論自己的面積拿來用」這件事在這一集不可能發生，2,150 掛 L07（"devastated 2 150 ± 50 km2"）是對的做法。全稿也沒有任何自己換算出來的棵數。

**四、查核檔點名不能講的事，我逐項搜過全檔（含 112 個 `prompt`）：**

| 不能講的事 | 全檔命中 | 判定 |
|---|---|---|
| 廣島的倍數 | 「廣島」1 次，在 `tg5d`「那是廣島之後寫的」（一九四六年那篇小說的時間座標）；「原子彈」「一千顆」「185」0 次。我今天在四頁上讀到這類倍數——N08「about 185 Hiroshima bombs」、APS「about 185 such bombs」、EB「a thousand times more powerful than the atomic bomb dropped on Hiroshima」、L07「about one thousand times the Hiroshima bomb energy」——稿裡一個都沒有 | 沒有出現 ✓ |
| 這種事多久一次 | 「三百年」「千年」「一世紀」「幾百年」0 次；「多久」1 次，只在 `loops[1].what` 這個內部欄位。來源有：N08「once every 300 years」、N19「on the order of millennia – not centuries」、EB「once every few hundred years」、RMG（見下） | 沒有出現 ✓ |
| 一九二九年那張照片（年份、攝影者、授權） | 「1929」「一九二九」「Krinov」0 次；`assets[]` 是空陣列、沒有照片卡；「照片」2 個字只在 `tg1j` 場景的 `emotion`「像在描一張老照片」（給配音的語氣提示）。EO 今天確實寫著「taken during a Kulik expedition in May 1929」，稿裡沒有 | 沒有出現 ✓ |
| 那個不能引的面積數字 | 「1287」「1,287」「一千二百八十七」0 次。我今天開了 RMG 確認它確實寫著「**1287 square kilometres** of forest were flattened, with **80,000,000 trees** felled」。稿裡的面積只有三個：8,000（一九三三年的假設，掛 BB25）、2,150（量到的，掛 L07）、說明欄的「大約兩千平方公里」（EB「some 2,000 square km」）——都不是它。評論自己的面積值不存在（見上） | 沒有出現 ✓ |
| 庫利克的病名 | `tg4ab` 只到「受傷、被俘，一九四二年四月十四日過世」，對上 BSE「[…— 14.4.1942…] … вступил добровольцем в народное ополчение, **был ранен и погиб в плену**」；「斑疹」「傷寒」0 次 | 沒有出現 ✓ |
| 目擊者的名字 | 「Semenov／謝梅諾夫」「Akulina／阿庫莉娜」「Ivan／伊凡」0 次。APS 今天給了交易站那人的名字（Sergei Semenov）、OSU 給了帳篷那兩人的名字（Akulina、Ivan），稿裡一個都沒有；`tg1b` 只說「一間交易站的門廊上，坐著一個男人」，`tg1g` 只說「埃文基人的帳篷」 | 沒有出現 ✓ |
| 其他（證實是小行星／找到隕石／切科湖就是隕石坑／無人傷亡） | 「證實」只在 `tg7u`「未經證實的報告」；沒有任何一句宣稱找到隕石（`tg3r`、`tg4p`、`tg4q`／`tg4r` 都是反向）；切科湖三說並列；傷亡兩說並列。要注意的是 APS 今天寫「Today there is **strong consensus** that the body… was most likely an asteroid-like object」、N115 寫「most scientists today believe it was an asteroid」——稿子沒有拿這兩句當定論，照查核檔的 DISPUTED 處理，講得比它們保守，不是講得更強 | 沒有出現 ✓ |
| 一九三〇年代那些流傳版本的人名 | Kazantsev、Shapley、Whipple、Astapovich、Crommelin、Brazo 在旁白、卡片與 `prompt` 裡 0 次；Longo、Boslough、Bruno、Jenniskens 只出現在 `sources[]` 的書目標題裡（與 curio-h01 的做法一致） | 沒有出現 ✓ |

## 第 4 點：沒有定論的事，在觀眾會遇到的每一個出口

| 出口 | 它說了什麼 | 判定 |
|---|---|---|
| **標題** | 「通古斯大爆炸：森林倒了，坑在哪裡？」——問句，沒有棵數，沒有給答案 | 沒有把未定論講成定論 ✓ |
| **縮圖** | 「樹站著／沒有坑」「一九〇八年的檔案」——兩個都是 CONFIRMED 的事（N115「trees remained standing」、EB「a marshy bog but no crater」） | ✓ |
| **說明欄** | 「最後是今天的解釋，和**四件**還沒有定論的事」「沒有定論就說沒有定論」 | ✓（四件這個數字見下） |
| **章節列**（會進 YouTube 章節列，也會被組進說明欄） | 七個章名裡沒有一個碰到天體性質、能量、高度、切科湖或傷亡；第 7 章是「它在半空中就炸開了」，講的是主流解釋 | ✓ |
| **卡片** | `how-high` 把「5–10 公里／離地高度」與「10–14 公里／二〇一九年模擬」分成兩格，沒有併成一個數字；`still-open` 是「未結／紀錄到今天還沒有定論」；沒有任何一張卡給天體性質、能量單一值、切科湖裁定或傷亡人數 | ✓ |
| **旁白** | 能量 `tg7l`「到現在還沒有定論」；切科湖 `tg7q`「到現在沒有結論」；傷亡 `tg7r`「也沒有結論」；天體 `tg7v`「還在爭論」。高度兩個範圍各唸一次（`tg7c`／`tg7e`），大小只說「幾十公尺」 | ✓ |
| **片尾卡字** | 「到今天還沒有找到」（見第 2 點） | ✓ |

**四件還是五件：四件是對的，說明欄不用改。** 理由三條：
1. **查核檔自己數的是四件**：H03.md 的 finding 寫「還沒定論的是：它是石質小行星還是彗星碎片、能量是 3 到 5 還是 10 到 30 百萬噸、切科湖是不是碎片撞出來的、有沒有人喪生」——性質、能量、切科湖、傷亡。爆炸高度在同一段裡是**主流解釋的一部分**（「在離地大約 5 到 10 公里處炸開（2019 年的模擬估 10 到 14 公里）」），不在那張未定論名單上。
2. **稿子交出來的也正好是四件**：全片明說「沒有定論／沒有結論／還在爭論」的只有 `tg7l`、`tg7q`、`tg7r`、`tg7v` 四處，`brief.md` 與 `claims.md` h42 寫的也是同樣四件（天體性質、能量、切科湖、傷亡）。
3. **第一輪的「五件」是另一種分法**：它把爆炸高度列成第五件，並把大小與性質併在「天體本身」一列。高度確實是來源不一致（H03 #5），但這一集處理它的方式是「兩個帶出處的範圍各唸一次、卡上兩格都有」，不是提出一個開放問題；大小也是用「幾十公尺」把四個估計全包起來。
   兩種分法都沒有把任何一件講成定論，差別只在要不要把「來源不一致」算成「本集說沒有定論的事」。說明欄那句話後面緊接著「今天的解釋」，高度與大小都在那四個字裡面，所以**四件與稿子、大綱、查核檔三邊一致**，第一輪的五件是較寬的數法。
   唯一的落差在文件裡：`NOTES.md` 第 117 行還留著第一輪的「五件沒有定論的事也都還是範圍或兩說並列」，與說明欄、`brief.md`、`claims.md` 的四件不一致。那不是觀眾看得到的字，我也不能改檔；請下一個動 `NOTES.md` 的人把它對成四件。

## 七個章名，逐個判（第一輪沒有抽）

章名會進 YouTube 的章節列，也會被 `composeDescription()` 組進說明欄（`metadata.mjs`：`📌 章節`），所以它是觀眾最早讀到的一批字——比開場濃縮還早。七個都查了：

| 章 | 章名 | 來源句 | 判定 |
|---|---|---|---|
| 1 | 那天早上，他被掀下椅子 | N08「he will be **hurled from his chair**」；APS「**thrown several feet from his chair**」；AOP「a great blast **pushed him off his chair**」 | CONFIRMED（是事件，不是功能；沒有講後面才揭曉的事） |
| 2 | 一九二一年那趟，他沒走到 | N115「The Soviet Academy of Sciences first sent geologist Leonid A. Kulik… in 1921, but **the area proved so inaccessible that he could not reach it**」；L07「The first expedition could not go farther than Kansk, about 600 km from the Tunguska explosion site」 | CONFIRMED |
| 3 | 一九二七年，他走到正中央 | N115「**Not until 1927 did Kulik succeed in reaching his goal**」；LH「when Kulik got to **the center**」 | CONFIRMED |
| 4 | 他把沼澤裡的圓坑抽乾 | APS「Kulik noted several small 'pothole' bogs that he assumed were meteorite craters, but **when he finally drained one of the bogs** (dubbed the 'Suslov crater'), an old stump at the bottom proved it could not be such a crater」 | CONFIRMED（來源是「抽乾其中一個」；旁白 `tg4e`／`tg4f` 講得明確，章名的中文讀成「那個圓坑」也通。如果有人覺得章名會被讀成「所有圓坑」，「他抽乾了一個圓坑」字數相同——但這是口味，不是事實錯誤） |
| 5 | 一九四六年，一篇小說把它寫成外星太空船 | L07 參考文獻「Kazantsev AP (**1946**) Vzryv. Vokrug sveta 1:39–46」＋正文「Others consider **alien spacecrafts** (Kazantsev 1946…)」；OSU「Eventually **science fiction writers** offered their own ideas. Writing after the nuclear detonations… Russian writer Alexander Kazantsev suggested… **an atomically-powered space craft from another planet blew up over Siberia**」 | CONFIRMED（「小說」靠 OSU 把他列在科幻作家那一段；L07 只給雜誌出處。記一筆：這個「小說」的字面依據是 OSU 的框架，不是 L07 的字） |
| 6 | 二〇二五年，有人去查那個數字的出處 | BB25：*Scientific Reports* 15:13869（2025，Matters Arising，開放取用），小節標題 "Claims of more than eighty million fallen trees… are exaggerated"，內容就是追 Bunch→Brazo & Austin→Whipple→Crommelin→Astapovich 這條鏈 | CONFIRMED（是事件；章名本身不帶棵數） |
| 7 | 它在半空中就炸開了 | N115「exploded in the skies over Siberia」；EO「The explosion, **an airburst**」；EB「the object **exploded in the atmosphere** high above Earth's surface」 | CONFIRMED（改對了：舊章名「它根本沒有落地」與舊片尾卡字是同一個斷言的兩個出口，現在兩個都沒有了。新章名講的是主流解釋，不是那四件沒有定論的事） |

另外兩件我順手核過的：七個章名都是「發生了什麼」而不是功能（〈說故事關卡〉第 9 題的參考題過關，與 h01-v2、h02-v2、l08-v2、u02-v2 的章名寫法一致——那四支的最後一章也都是直接講結果）；
七個章名裡沒有棵數、沒有「隕石坑」或「無人傷亡」這類被禁的斷言。

## 抽查第一輪的 105 條 CONFIRMED：我抽了 50 條

**怎麼抽的**（不用隨機數，用會出事的地方來抽，比抽籤更有用）：
(a) 觀眾在旁白以外讀到的每一個出口——標題、說明欄、標籤、縮圖、`sources[]`、七張卡片；
(b) 第一輪自己註明「單一來源」或掛了附註的每一條；
(c) 每一個帶數字、日期、面積或換算的條目；
(d) 第 6 章引用鏈與第 7 章四件未定論的骨幹句；
(e) 其餘用來補足跨度的幾條（第 1、2、3、4 章各取一條接縫處）。
50 條 > 第一輪 105 條的三分之一（35 條）。編號沿用 `verify-1.md` 的主張表。

| # | 位置 | 我今天看到的來源句 | HTTP | 第二輪 |
|---|---|---|---|---|
| 1 | youtube.title | N115、EB、LH（1927 走到中心沒有坑）；標題無棵數 | 200 | CONFIRMED |
| 2 | youtube.description §1 | N115「At about 7:15 am」；N08「40 miles from ground zero」「hurled from his chair」；EB「some 2,000 square km」「abnormally bright nighttime skies in Siberia and Europe」；L07 Fig. 18.5「the 30 June/1 July 1908」 | 200 | CONFIRMED |
| 3 | youtube.description §2 | BB25（見第 3 點）；說明欄當場否定那個棵數 | 200 | CONFIRMED |
| 6 | 資料截至 2026-10-10 | 查核檔的查核日；`sources[]` 22 筆 `checked_on` 全為 2026-10-10，而且我 10-13 重開全部 200 | — | CONFIRMED |
| 7 | youtube.tags | 十個標籤都是題目裡出現過的詞，沒有棵數、沒有「隕石坑」斷言 | — | CONFIRMED |
| 8 | thumbnail.data | N115「trees remained standing」；EB「a marshy bog but no crater」 | 200 | CONFIRMED |
| 9 | `tg1a` | N115「At about 7:15 am local time on June 30, 1908」；N08「7:17 a.m.」；EB「7:14 a.m. plus or minus one minute」——三個時刻，旁白只講「七點多」 | 200 | CONFIRMED |
| 12 | `named-the-blast.data`、`tg1e` | 同 #9；L07 通篇用 "Tunguska event" | 200 | CONFIRMED |
| 13 | `tg1f` | N08「40 miles from ground zero」；AOP「some **65 km (40 miles)** south of the epicentre」（AOP 自己就寫了 65 km，所以六十四公里不是本稿的換算在冒險） | 200 | CONFIRMED |
| 17 | `tg1k` | L07 逐字「at midnight, it was possible to read the newspaper without artificial lights」。**不再是單一來源**：N08 也寫「reports came in that people who lived as far away as Asia could read newspapers outdoors as late as midnight」 | 200 | CONFIRMED（疑點解除） |
| 20 | `tg2a` | L07「Up to 1921, meager information about a great 1908 bolide was published only in some local Siberian newspapers」；LH「Local newspapers carried stories about the flash, and the noise, and the heat」 | 200 | CONFIRMED |
| 21 | `tg2b` | COMMONS-SZ：Date「12 July 1908」、說明「Первое описание… сделанное «по слухам» **через 12 дней** после его падения」——十二天是來源自己寫的 | 200 | CONFIRMED |
| 23 | `tg2d`／`tg2e` | L07 逐字「Immediately after the registration of the earthquake N° 1536, **in the morning of 30 June 1908**, Voznesenskij **sent to all his correspondents a request** to report what they or other people had observed on that morning」（他是伊爾庫次克磁學與氣象觀測站的台長） | 200 | CONFIRMED |
| 25 | `tg2g`–`tg2i` | L07「the first paper that connected to the TE the origin of these seismic waves was published only in **1925**」「the barograms… were associated with the TE some twenty years later (**Whipple 1930**; Astapovich 1933)」 | 200 | CONFIRMED |
| 27 | `tg2l` | N08 引 JPL 的 Yeomans「They believed the blast was **a visitation by the god Ogdy**」（單一來源）。APS 另寫「attributed the blast to **Agda, the god of thunder**」——同一個信仰、另一個拼法，稿子照查核檔指名的 N08 寫，記在〈附註〉 | 200 | CONFIRMED |
| 29 | `tg2n` | 不只是算術：LH「in the **thirteen years** since the event, no one had been sent to inquire further」 | 200 | CONFIRMED（比第一輪更強） |
| 30 | `tg2o` | N115「first sent geologist Leonid A. Kulik on an expedition to the site in **1921**」；LH「he convinced the Academy of Sciences to sponsor a trip… This was in 1921」 | 200 | CONFIRMED |
| 31 | `tg2p` | LH「born **Aug. 19, 1883**」；BSE「[7(19).8.1883, Дерпт, ныне Тарту…]」 | 200 | CONFIRMED |
| 32 | `tg2q`／`tg2r` | L07「continued searching for an **iron body**, similar to one found in Arizona」；LH「with perhaps **tons of meteoritic iron**」；APS「to possibly **salvage any meteoric iron**」；OSU「there should be fragments of a **ferrous** space rock」 | 200 | CONFIRMED |
| 34 | `tg2t` | L07「the first Kulik expedition (**1921–1922**)」「The first expedition could not go farther than **Kansk**」 | 200 | CONFIRMED |
| 35 | `still-six-hundred.data`、`tg2u`／`tg2v` | L07「Kansk, **about 600 km** from the Tunguska explosion site」；N115「he could not reach it」。卡片出處欄「波隆那大學專書章」對得上 | 200 | CONFIRMED |
| 36 | `tg2w`／`tg2x` | LH「it took him **6 years** to persuade his superiors… **In 1927, he returned** with a small party」 | 200 | CONFIRMED |
| 38 | `tg3b`–`tg3e` | LH「the fallen trees formed a vast **radial ring**, with the tops of the felled trees **pointed outward, away from a center**」；EB「The epicentre was easy to pinpoint because the felled trees all pointed away from it」 | 200 | CONFIRMED |
| 40 | `tg3g` | L07「devastated **2 150 ± 50 km2**」（旁白說「大約」，±50 沒講）；N115 的 830 平方英里＝2,150 km² 相容 | 200 | CONFIRMED |
| 41 | `tg3h` | N115「a **butterfly-shaped** area of destruction of 830 square miles」；EO「the butterfly-shaped blast zone」 | 200 | CONFIRMED |
| 43 | `tg3j`／`tg3k`／`tg3n` | N115 逐字「Near the epicenter, **trees remained standing** but with **broken branches and stripped of bark, with evidence of burning**」 | 200 | CONFIRMED |
| 45 | `tg3o`／`tg3p` | LH「when Kulik got to the center, he **did not find the expected crater**」；EB「investigators observed a **marshy bog but no crater**」；APS「surprised, upon arrival, to see that there was **no impact crater**」 | 200 | CONFIRMED |
| 48 | `tg3s` | EB「first investigated **from 1927 to 1930** in expeditions led by… Kulik」；BSE「в **1927—30** и в 1938—39 возглавлял экспедиции」；LH「he would **return 3 times**」；APS「Over **three successive expeditions**」 | 200 | CONFIRMED |
| 50 | `tg3v` | BB25（它追的就是這個流傳）；我今天自己在四頁上看到照寫的棵數：N08「**Eighty million trees** were on their sides」、L07「Eighty millions trees were flattened」、AOP「more than **80 million trees** over 2150 square kilometres」、RMG「**80,000,000 trees** felled」 | 200 | CONFIRMED（當流傳的數字） |
| 52 | `tg4a`／`tg4b` | G07「concluded that he had discovered **the remains of a large impact crater now hidden by a swamp**」 | 200 | CONFIRMED |
| 53 | `tg4c`／`tg4d` | G07「a number of **secondary bowl-shaped holes** of different sizes **covered by peat bogs** possibly caused by a fragmented body」；APS「several small 'pothole' bogs that **he assumed were meteorite craters**」 | 200 | CONFIRMED |
| 54 | `tg4e` | APS「(dubbed the '**Suslov crater**')」——仍是單一來源，第一輪與查核檔都註明了，旁白只說「其中一個叫蘇斯洛夫坑」 | 200 | CONFIRMED（單一來源） |
| 58 | `tg4i`／`tg4j` | APS 逐字「an **old stump** at the bottom proved it could not be such a crater」 | 200 | CONFIRMED |
| 59 | `tg4k` | G07「**All attempts at finding macro-remnants** of the cosmic body **in these circular depressions were unsuccessful**」（來源講所有圓坑，旁白收窄到他抽的那一個，沒有講多） | 200 | CONFIRMED |
| 61 | `tg4o`／`tg4p` | OSU 逐字「Kulik spent **the better part of the next three years** in the Tunguska taiga **trying and failing to find it**」 | 200 | CONFIRMED |
| 62 | `tg4q`／`tg4r` | N115 逐字「later expeditions found **microparticles** indicating an extra-terrestrial origin, these remnants **could not be conclusively tied to the blast**」；EB「a few small fragments, each less than a millimetre across」 | 200 | CONFIRMED |
| 69 | `tg4y` | APS 記「F. J. W. Whipple」、L07 記「Shapley (1930)」——兩份不一樣，旁白兩個名字都不講 | 200 | CONFIRMED |
| 70 | `tg4z`／`tg4aa` | BSE「В начале Великой Отечественной войны **1941—45**… вступил добровольцем в **народное ополчение**」 | 200 | CONFIRMED |
| 71 | `tg4ab` | BSE「**14.4.1942**」「**был ранен и погиб в плену**」；LH「He died during the war, in 1942」。病名兩個來源都沒給，旁白也沒講 | 200 | CONFIRMED |
| 72 | `tg4ac` | 1921→1942＝21（算術，已列在 `claims.md`） | — | CONFIRMED |
| 74 | `tg5b` | L07 參考文獻「Kazantsev AP (1946) Vzryv. **Vokrug sveta** 1:39–46」；篇名與作者都沒講 | 200 | CONFIRMED |
| 77 | `tg5f`／`tg5g` | L07 逐字「**Kazantsev was the first who explained the lack of fragments or impact craters in Tunguska by an explosion in the atmosphere**」——單一來源，旁白已掛「有一位研究者寫道」 | 200 | CONFIRMED（單一來源） |
| 80 | `tg5j` | AM65 頁面：〈Possible Anti-Matter Content of the Tunguska Meteor of 1908〉，Nature 206:861–865，Published **29 May 1965** | 200 | CONFIRMED |
| 83 | `tg5m` | BT74：〈Tungus event was not caused by a black hole〉，Nature 250:555–556，**01 August 1974**，摘要「Several lines of evidence render the black hole hypothesis **extremely unlikely**」 | 200 | CONFIRMED |
| 84 | `tg5n`／`tg5o` | L07「Several of them, though published in scientific journals, **were found to be technically groundless**, e.g.… antimatter meteors (Cowan et al. 1965), and tiny black holes (Jackson and Ryan 1973)」，緊接著是他自己的話「Nevertheless, **I think** that here we can ignore such extremely 'non-traditional' hypotheses」 | 200 | CONFIRMED（第一輪的附註照舊：轉述層次讀得通） |
| 89 | `tg6c` | BB25 參考文獻 5＝Astapovich, *Astron. Zh.* 10, 465–486 (**1933**) | 200 | CONFIRMED |
| 91 | `tg6f`／`tg6g` | BB25 引 Astapovich 原句「about **8000 km2**」與結論「the work of the windfall of **8⋅10⁷ trees**」 | 200 | CONFIRMED |
| 93 | `assumed-against-measured.data` | 左欄 8,000 ← BB25 引的 Astapovich 1933；右欄 2,150 ← L07；裁定「高估約四倍」← BB25「a factor of about four」；卡上沒有棵數；出處欄把兩個來源分開寫 | 200 | CONFIRMED |
| 99／100 | `tg6p`–`tg6r` | BB25 參考文獻 3＝Whipple (1934)、4＝Crommelin (1934)；正文「**not actually made by Whipple but by a correspondent**, based on Crommelin, whose source was Astapovich」 | 200 | CONFIRMED |
| 103 | `tg6u` | 1933→2026＝93（「九十幾年」）；照寫的頁面見 #50（今天四頁） | 200 | CONFIRMED |
| 106／108／110、109 | `tg7a`、`tg7c`、`tg7e`、`how-high.data` | 大小：N115「130 feet」、N08「about 120 feet」、N19「between **164 and 262 feet**」、EB／EO「**50–100 m**」——全落在「幾十公尺」；高度：EB「at an altitude of **5–10 km**」、L07「height of the explosion (**5–10 km**)」、G07「exploded about **5–10 km** above ground」、EO「about **6 to 10 kilometers**」；N19「at **6 to 9 miles** altitude」＝9.7–14.5 km，旁白與卡片都標成「二〇一九年模擬」的十到十四公里，沒有與 5–10 併成一個範圍 | 200 | CONFIRMED |
| 107 | `tg7b` | EO「an object… **plunged into Earth's atmosphere, creating a brilliant fireball that exploded** over a remote part of Siberia」；N115「an asteroid plunged into Earth's atmosphere and exploded in the skies over Siberia」（`claims.md` h36 已經把這個場景補進去了） | 200 | CONFIRMED |
| 111 | `tg7f`／`tg7g` | N115「The resultant **shock wave** and thermal radiation most likely correlate with… the destruction described by later expeditions」；SNL「the center of mass of an asteroid exploding above the ground is **transported downward** at speeds faster than sound」 | 200 | CONFIRMED |
| 112 | `tg7h`／`tg7i` | EO「**vaporizing the vast majority** of the incoming bolide」；N08「**The great majority** of the asteroid is consumed in the explosion」「**That is why there is no impact crater**」；N115「A mid-air explosion most likely vaporized the object」 | 200 | CONFIRMED（「幾乎」這個鉤子有留住） |
| 113／114 | `tg7k`／`tg7l` | SNL「what scientists had thought to be an explosion between **10 and 20 megatons** was more likely only **three to five** megatons」；N19「depositing the energy of a **10 to 30 megaton** explosion」；EB「as much as 15 megatons」；L07「10–15 Megaton」；BT74 摘要另記「About 10²³ erg (equivalent to **2 Mton** of TNT)」。旁白用查核檔指定的 3–30，並說「都有人算過」 | 200 | CONFIRMED |
| 115／116／117／118 | `tg7n`–`tg7q` | G07「Its **funnel-like bottom morphology**… all suggest that the lake fills an impact crater」；C08「we therefore conclude that Lake Cheko is **highly unlikely** to be an impact crater」；R17（Published 04 November 2017）「Cheko Lake is **significantly older** than the 1908 Tunguska Event」；EO「**other research teams dispute that idea**」 | 200 | CONFIRMED |
| 119／120／121 | `tg7s`／`tg7t`／`tg7u`／`tg7r` | J19 摘要逐字「inside and near the tree-fall area were **at least 30 people**. Many lost consciousness and **at least 3 passed away** (immediately or later) as a direct consequence」；AOP 逐字「Apart from **two unconfirmed reports** there are thought to have been no human casualties」（另有 OSU「At least two others appear not to have been so fortunate」、LH「only a few deaths were reported」、N115「very few human casualties」，旁白沒有再加） | 200 | CONFIRMED |
| 122 | `tg7v` | AOP「Some argue that it was a small asteroid, others that it must have been **a small comet (or a comet fragment)**」；EB 兩說並列；C93 標題〈atmospheric disruption of a **stony asteroid**〉；L07 未釐清 | 200 | CONFIRMED |
| 123 | `tg7z` | N19「**February 15, 2013**… near **Chelyabinsk**, Russia」 | 200 | CONFIRMED |
| 125 | `still-open.data`、`tg7ac` | 1908→2026＝118；查核檔文末「未結」 | — | CONFIRMED |
| 130 | `sources` | 22 筆我今天全部重開，全部 200；與 `claims.md` 的網址集合完全相同 | 200 | CONFIRMED（第一輪的 #4／C10 已解） |

**抽查結果：50 條裡 50 條維持 CONFIRMED，一條都沒有翻案。** 其中兩條比第一輪更強（#17 的讀報不再是單一來源、#29 的十三年有 LH 的原句），一條補了同一信仰的另一個拼法（#27）。

## 第 6 點：改完之後，故事線有沒有被弄壞

**一、五個鉤子都還是用新東西兌現的。** `loops[]` 五條我逐條讀了回收處的下一句：
`tg2j`→不願意跟外人談＋神靈奧格迪（新事實）；`tg2g`→地震儀與氣壓計的紀錄、一九二五與一九三〇（新事實）；
`tg3c`→輻條、循著方向走到中心、二一五〇平方公里、蝴蝶形、正中央的樹還站著（新事實）；`tg6a`→整章的來歷（新事實）；`tg7m`→二〇〇七／二〇〇八／二〇一七三份研究（新事實）。
`tg2j` 這一條是 C12 改過的，改完仍然帶新東西（「不願意跟外人談」＋奧格迪），沒有變成把 `tg1g` 再讀一遍。
「還記得」整支片 **5 句**（`tg2g`、`tg2j`、`tg3c`、`tg6a`、`tg7m`），正好在規則的上限上，沒有連著用，十四條改動也沒有新增一句。

**二、`tg4w` 的「亮著的晚上」第三次出現：撰稿方的理由成立。** 「那幾個亮著的晚上」在旁白裡出現三次——`tg2a`（第 2 章開頭的時間座標）、`tg2g`（點名的回收）、`tg4w`（C2 新寫的）。
重點是**沒有一次在重報那個事實本身**（事實只在 `tg1j`／`tg1k` 講過一次：夜空亮著、半夜不點燈能讀報）：`tg4w` 把這個已知的事實變成一九三〇年彗星說的**證據**，也就是 `script-writing.md` 說的「把那個東西往前推，不是回頭重報一次」。
它也不是「還記得…」句型，不佔那五句的額度。來源上它比被換掉的那一句強得多（APS、AOP、EB 三處都把事後的夜光當成彗星說的依據）。
**判定：沒有違反「一個事實只講一次」。** 唯一可以挑的是三次都用了一字不差的「那幾個亮著的晚上」，念起來有公式感；要避開的話 `tg4w` 改成「彗星說靠的是事後那片發亮的夜空。」（15 單位，比現在少一個）、來源不變。這是口味，我沒有列成要改的事。

**三、每一章的第一句還是接著上一章。** 七章逐個讀過：
第 2 章 `tg2a`「那幾個亮著的晚上之後，西伯利亞的地方報就登出了這件事。」是「接下來發生了什麼」（時間座標，不是總結句）；
第 3 章 `tg3a`「一九二七年，他終於走到了。」直接接第 2 章末的「六年後，他又出發了」；
第 4 章 `tg4a`「庫利克的答案是：它還在地底下。」正好回答第 3 章末的問句「壓倒這片森林的東西，到底去哪裡了？」；
第 5 章 `tg5a`「他過世四年後，這件事換了一種講法。」接第 4 章末的過世；
第 6 章 `tg6a` 是點名回收，而它回收的 `tg3v` 埋在三分多鐘前（不是 L08 被擋下的那種「四秒前才埋、下一章就點名」）；
第 7 章 `tg7a`「壓出那個形狀的，是一個幾十公尺大的天體。」回答第 6 章末的問句。
**十四條改動沒有動到任何一章的第一句**（C11 是第 2 章第三句、C4 在第 3 章中段、章名的改動不影響 `tg7a`），所以這一關沒有被改壞。

**四、沒有新的重複。** 我特別看了 C5 可能造成的一處：`tg3r`「大塊的碎片也沒有」（第 3 章，講整個一萬五千平方公里）與 `tg4k`「他抽的那個坑裡，始終沒有大塊殘骸」（第 4 章，只講他抽乾的那一個坑）。
兩句的範圍不同、章不同，而且 `tg4k` 之後 `tg4q` 馬上補了微小碎屑這個新事實，所以不是同一個事實講兩次；`tg4k` 的「大塊」是 G07 的 macro-remnants，不能拿掉。判定：可接受，不必改。
片尾也沒有重述：`tg7ac` 是一個新數字（一百一十八年），`tg7ad`「未結」全片只唸這一次，`tg7ae` 是留言題，`tg7af` 是帶理由的訂閱邀請，**沒有提下一支／下一集／下一份檔案**（旁白裡 0 次）。

**五、聽眾檢查（我沒有跑 `lint`，只呼叫了 `spokenUnits()`）。** 158 句裡最長的是 `tg2a`（25 單位），正好在 24／25 的上限上，而且是改動沒有碰到的句子；
十四條改過的句子最長 21 單位（`tg2c`），其餘都在 19 以下，所以**沒有一條改動把句子推長到會出問題**（`lint` 的警告線是 40 單位，`SENTENCE_WARN`）。
旁白裡沒有括號、沒有網址、沒有「經查證」「根據官方文件」「本影片」這類字；卡上的數字一個都沒有被改動，所以沒有 `say`／`say_for` 要補。

## 還要改的（兩條，都只動一句旁白，不用重畫任何一張圖）

**R1　`tg1i`（`steadying-on-a-pole`）—— 這一句還是沒有來源，而且與 `tg2l` 打對台**
- 現在：「他們不知道那是什麼。」
- 建議：「有人嚇得大叫。」（6 單位，比現在的 9 單位短）
- 為什麼：OSU 寫的是那兩個人的反應，原文逐字是「something suddenly hit her tent and **"I was scared, screamed, and woke up Ivan."**」——嚇得大叫有原文，「不知道那是什麼」沒有。
  第一輪把原來的全稱斷言（「沒有人說得出剛剛是什麼」）改成這一句，方向對，但換上來的仍然是一句沒有來源的**心理狀態**；而且第 2 章 `tg2l` 緊接著說「他們認為，是神靈奧格迪降臨了」——同一批人，前面說不知道那是什麼，後面說他們認為是神靈降臨，觀眾聽得出來。
  我也找過能撐住一句概括的來源：L07 有「Many correspondents could not understand what they have seen or heard」，但那講的是寫信給伊爾庫次克觀測站的通訊員（也就是 `tg2d`／`tg2e` 那一段的人），寫在第 1 章會把第 2 章的料提前用掉。
  直接刪掉也通：`tg1h`「人被震倒在地上。」接 `tg1j`「那天晚上，從西伯利亞到歐洲，夜空都亮著。」讀得順。`claims.md` h5 的括號說明（「所以旁白只講那兩個人的狀態」）要跟著改成實際採用的那一句。

**R2　`tg7aa`（`faces-turned-up`）—— 「第一次」沒有來源，而且與本集第 1 章矛盾**
- 現在：「很多人第一次親眼看到空爆。」
- 建議：「很多人親眼看到，還拍了下來。」（12 單位，與現在相同）
- 為什麼：N19 的原句只到「This **highly documented** fireball created an opportunity for researchers to apply modern computer modeling techniques」，後面是「The models were used with **video observations of the fireball** and maps of the damage on the ground」——有「很多人看到、被大量記錄下來」，**沒有「第一次」**。
  查核檔〈給撰稿的提醒〉寫的是「2013-02-15 車里雅賓斯克讓人親眼看到空爆」，也沒有「第一次」這三個字。
  更要緊的是本集第 1 章整段就是一九〇八年的人親眼看到那一次空爆（`tg1c`「天的那一邊傳來一聲巨響」、N19 自己也寫「Tunguska is the largest cosmic impact **witnessed by modern humans**」），所以「第一次」會被自己的第 1 章打掉。
  建議句把「被拍下來」這個真正的新鮮事講出來，兩個子句都在 N19 上；`claims.md` h41 的說法（「讓人親眼看到一次空爆」）不必改。

**文件上的一條（不是稿子，我不能改）**：`NOTES.md` 第 117 行的「五件沒有定論的事」要對成四件，理由見第 4 點。

## 附註（我看到但不要求改的）

- **第一輪有一個註記是錯的**：它寫「RMG 的正文裡我沒有找到棵數」。我今天開 RMG 讀到的是「1287 square kilometres of forest were flattened, with **80,000,000 trees** felled」——查核檔的記載（RMG 照寫八千萬棵）才是對的。
  這不影響任何判定，反而讓 `tg6u`「你還會在影片和文章裡看到它」多了第四個今天還照寫的頁面（N08、L07、AOP、RMG）。BO（波隆那大學首頁）我這一輪沒有開，第一輪說它是框架選單頁取不到正文，與判定無關。
- **神靈的名字有兩個拼法**：N08 寫 Ogdy，APS 寫「Agda, the god of thunder」。查核檔指名 N08，旁白寫「奧格迪」，所以沒有問題；但觀眾聽到的是其中一個來源的寫法，記在這裡。
- **前向鉤子兩句明說**：`tg3w`「這個數字從哪裡來，等一下會回來。」與 `tg4t`「它要很久以後才變成線索，晚一點再說。」都是明說的前向鉤子，而 `script-writing.md` §鉤子寫「**前向鉤子整支片最多一句明說**」。
  這是改動之前就有的事、也不是事實問題（第一輪把兩句都判 OUT OF SCOPE），我沒有列成要改的事；但如果站主要照規則收，`tg4t` 後半句刪成「它要很久以後才變成線索。」就夠了，切科湖那個鉤子自己掛得住。
- **同一集兩個面積數字**：說明欄「大約兩千平方公里」（EB）對旁白「兩千一百五十平方公里」（L07）。兩個都有來源、都帶「大約」，`claims.md` 也解釋了為什麼分開用。不是錯，但觀眾的兩個入口會拿到兩個數字（第一輪也記過這一條）。
- **第三個鉤子的回收最弱**：`tg3c`「還記得那些朝外倒下的樹嗎？」之後的 `tg3d`「樹幹像輪子的輻條，全部指著外面。」幾乎是 `tg1m` 的換句話說，真正的新東西落在再下一句 `tg3e`（循著方向可以走到中心）。
  五條鉤子裡只有這一條是「點名之後隔一句才給新東西」，十四條改動沒有碰到它，所以我只記不判。
- **`tg7v` 講得比兩個來源保守**：APS 今天寫「Today there is strong consensus… most likely an asteroid-like object」、N115 寫「most scientists today believe it was an asteroid」，而旁白說「還在爭論」。照查核檔 #9 的 DISPUTED 與「不能講『證實是小行星』」，這樣處理是對的；方向是保守，不是誇大。
- **`tg7p` 也講得比來源少**：R17 的結論是「the lake basin **cannot be a crater**」，旁白只說「沉積比那場爆炸老」。沒有問題。
- **第 5 章章名的「小說」**：字面依據是 OSU 把 Kazantsev 寫在「science fiction writers」那一段，L07 只給了雜誌出處（Vokrug sveta 1:39–46）。兩個合起來夠用，但這個詞的來源不是 L07，記在這裡。
- **兩個 `prompt` 可能畫到臉**（第一輪已記、撰稿方說改不動要花錢）：`names-on-a-tally`（「Medium shot of a researcher…」沒寫背影）、`faces-turned-up`（「their faces turned up and their mouths open」）。
  兩個都是沒有名字的泛稱人物，不在查核檔「不畫臉」的名單上；說明欄「在世或近代人物不入畫」的承諾在這兩格最緊。我同意不為此重畫，留給站主。
- **會過期的事實**：沒有。今天看到的頁面日期：N115 2023-06-30、N19 2019-06-26、EO 2025-06-30、N08 存檔 2021-01-01（原址 404）、EB 存檔 2026-09-01（直連今天 200）、L07 2007、BB25 2025（*Scientific Reports* 15:13869）、SNL 2007-12-17、R17 2017-11-04、J19 Icarus 2019-07、APS 2018-06-30、OSU 2018-05、LH 2023-06-30。

## 摘要

- **十四條改動：13 條 CONFIRMED、1 條 CHANGED。** CHANGED 的是 C3（`tg1i`）；另外第一輪留給第二輪再看的 `tg7aa` 我判 NOT FOUND。要改的只有這兩句旁白（R1、R2），兩句都不動數字、不動卡片、不動任何 `prompt`，所以不用重畫圖、不用補 `say`／`say_for`。
- **兩個最重的位置都過關**：片尾卡字「到今天還沒有找到」有 EO、N115、L07、N19、G07 撐著，不比紀錄更強；一萬五千平方公里的年代併接已經解掉（面積是 L07 的累計結果，「到今天」另有 N19、EO、EB），卡片的 kicker 與 sub 分得清楚。
- **第 3 點：過關。** 「八千萬棵樹」四次出現都是「流傳的數字」，標題、標籤、縮圖、七張卡片零棵數；來歷與引用鏈逐句對得上 BB25（一九三三年的粗估、面積高估約四倍、一九三四兩篇其中一篇是通信者的話、一九八二年照抄）；BB25 自己沒有面積值，稿子也沒有自算的棵數；廣島倍數、多久一次、一九二九年那張照片、那個疑為筆誤的面積、庫利克的病名、目擊者的名字，**全檔零命中**（我在四個來源頁上都讀到了廣島倍數，在四個來源頁上都讀到了棵數，稿裡一個都沒有）。
- **第 4 點：過關，而且「四件」是對的數字。** 標題、縮圖、說明欄、章節列、卡片、旁白、片尾卡字七個出口都沒有把那四件講成定論；高度與大小是帶出處的範圍，屬於說明欄同一句裡的「今天的解釋」。第一輪的「五件」是較寬的數法（把高度算進去），與查核檔的 finding、`brief.md`、`claims.md` h42 的四件不衝突但不同。`NOTES.md` 第 117 行還留著「五件」，請下一個動那個檔的人對齊。
- **七個章名全部查過，全部有來源、全部是「發生了什麼」**；第 7 章從「它根本沒有落地」改成「它在半空中就炸開了」是對的，全檔「落地」零次，同一個斷言的兩個出口（章名與片尾卡字）都收掉了。
- **抽查 50 條 CONFIRMED（>105 的三分之一），50 條維持**，沒有一條翻案；兩條比第一輪更強，一條補了拼法差異。
- **故事線沒有被改壞**：五個鉤子都用新事實兌現、「還記得」5 句在上限上、七章的第一句都還是接著上一章、片尾只帶新東西也不提下一支；`tg4w` 的「亮著的晚上」第三次出現**成立**（它把舊事實推成彗星說的證據，不是重報），撰稿方的理由我同意。
- 程序：沒有跑 git、沒有跑任何影片階段（含 `lint`）、沒有花供應商的錢、沒有改 `video.json`／`claims.md`／`brief.md`／`NOTES.md`。網路搜尋 0 次。中間檔在 `<tmp>\scratchpad\v2h03\`。
- **第三輪：不需要。** 這一輪只剩兩句旁白要改（R1、R2），都在第一輪已經點到的範圍內（C3 是它自己開的條目、`tg7aa` 是它自己要我再看的附註），沒有新的事實類問題。
  改完這兩句之後，這一集的事實面**可以進美術與配音**；套用時請一併修 `claims.md` h5 的括號說明，並由撰稿方跑一次 `lint` 確認 0 錯誤（我沒有跑）。
