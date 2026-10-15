# curio-h03-v2 查核第一輪

- 查核 2026-10-13，Claude Opus 5（獨立查核代理，不是撰稿的那一個；沒有參與這一版的任何一句）。
- 方法：先把 `video.json` 的每句旁白（`text`；158 句，沒有一句帶 `say` 或 `say_for`）、每張卡片的 `data` 欄、標題、說明欄、標籤、縮圖字、`sources[]` 與 `loops[]` 抽成 209 條清單
  （`<tmp>\scratchpad\verify-h03\assertions.tsv`、`extract.txt`），再把這 209 條逐條對回
  [`claims.md`](claims.md) 的 42 列（h1–h42），每一列再對回
  [`../history-curiosity/topic-checks/H03.md`](../history-curiosity/topic-checks/H03.md)。
- 然後把查核檔與 `claims.md` 列出的網址當天自己重開一遍：`curl`，User-Agent
  `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒以上（腳本 `fetch.mjs` 按主機記時間戳，實際間隔 1.3 秒）。
  PDF 用 `pdftotext` 取全文，HTML 去標籤後讀全文，BSE 以 windows-1251 解碼。沒有用網路搜尋（0 次）。
  每個網址的 HTTP 狀態在下一節，全部是我今天親自拿到的。
- 這一集沒有第一版腳本在這個倉庫裡，所以我沒有舊稿可比。唯一的上游是 H03.md（查核日 2026-10-10，同日獨立覆核，處置 ADOPT_WITH_CHANGES，文末「未結」）。
  凡是查核檔與原始來源都找不到的說法，我一律判 NOT FOUND，不替它找理由。
- 來源分量：一手或權威優先——NASA 四頁（美國聯邦政府作品）、Britannica、Longo 2007 的專書章（作者自存 PDF）、
  Boslough 與 Bruno 2025（Scientific Reports，開放取用）、Nature 1965／1973／1974／1993 的頁面、Terra Nova 2007／2008 存檔、
  Doklady 2017、Icarus 2019 摘要存檔、Sandia 新聞稿。APS News、Armagh、Ohio State Origins、Linda Hall、《蘇聯大百科》轉錄、
  維基共享的檔案頁只當佐證或當查核檔指名的那一個來源用。Wikipedia 條文沒有用。
- 我沒有改動 `video.json`、`claims.md`、`brief.md`、`NOTES.md` 的任何一個位元組；每個要改的地方寫在最後一節，附行 id、改前與建議的改後。
- 我沒有跑 git，沒有跑任何影片階段（含 `lint`），沒有花任何供應商的錢。所以這一輪沒有單位數與時長的數字可報。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| N115 | https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/ | 200 |
| N19 | https://www.nasa.gov/solar-system/tunguska-revisited-111-year-old-mystery-impact-inspires-new-more-optimistic-asteroid-predictions/ | 200 |
| N08 | 存檔：https://web.archive.org/web/20210101030522/https://science.nasa.gov/science-news/science-at-nasa/2008/30jun_tunguska/ | 200 |
| EO | https://science.nasa.gov/earth/earth-observatory/a-cosmic-explosion-over-siberia-154488/ | 200 |
| EB | 存檔：https://web.archive.org/web/20260901073916/https://www.britannica.com/event/Tunguska-event | 200 |
| EB（直連） | https://www.britannica.com/event/Tunguska-event （與查核檔當天一樣擋了，所以引句一律用存檔） | 403 |
| L07 | https://www-th.bo.infn.it/tunguska/Asteroids-Chapter-18.pdf （19.3 MB，pdftotext 全文 73 KB） | 200 |
| BO | https://www-th.bo.infn.it/tunguska/ | 200 |
| BB25 | https://www.nature.com/articles/s41598-025-98362-9 | 200 |
| SNL | https://newsreleases.sandia.gov/releases/2007/asteroid.html | 200 |
| C93 | https://www.nature.com/articles/361040a0 | 200 |
| AM65 | https://www.nature.com/articles/206861a0 | 200 |
| BH73 | https://www.nature.com/articles/245088a0 | 200 |
| BT74 | https://www.nature.com/articles/250555a0 | 200 |
| R17 | https://link.springer.com/article/10.1134/S1028334X17100269 | 200 |
| J19 | 存檔：https://web.archive.org/web/20260411202527/https://ui.adsabs.harvard.edu/abs/2019Icar..327....4J/abstract | 200 |
| G07 | 存檔：https://web.archive.org/web/20230211163937/https://onlinelibrary.wiley.com/doi/10.1111/j.1365-3121.2007.00742.x | 200 |
| C08 | 存檔：https://web.archive.org/web/20230210215017/https://onlinelibrary.wiley.com/doi/10.1111/j.1365-3121.2008.00791.x | 200 |
| APS | https://www.aps.org/apsnews/2018/06/tunguska-event （第一次連線被對方重設，間隔後重試成功） | 200 |
| OSU | https://origins.osu.edu/milestones/june-2018-1908-tunguska-event-and-threats-tomorrow | 200 |
| LH | https://www.lindahall.org/about/news/scientist-of-the-day/leonid-kulik/ | 200 |
| AOP | https://armagh.space/weather/history/tunguska-event | 200 |
| BSE | https://booksite.ru/FullText/1/001/008/067/252.htm | 200 |
| COMMONS-SZ | https://commons.wikimedia.org/wiki/File:1908-07-29-SibirskayaZshizn-135.jpg | 200 |
| RMG | https://www.rmg.co.uk/stories/space-astronomy/tunguska-event （只為確認那個不能引的面積數字長什麼樣） | 200 |

查核檔列的 K49（tunguska.tsc.ru）與維基共享其他檔案頁這一輪沒有開：這一版 `assets[]` 是空的、沒有照片卡，
所有與照片授權、1929 年、攝影者有關的事都不入稿，開了也沒有對應的主張。

## 主張表

判定：CONFIRMED 看到了／CHANGED 要改／NOT FOUND 沒看到，拿掉或換掉／OUT OF SCOPE 問句、升級句、編輯決定、系列安排，不動。
「位置」用 `場景/行id`；卡片用 `場景.data.欄`。

| # | 主張 | 位置 | claims | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|---|
| 1 | 通古斯大爆炸：森林倒了，坑在哪裡？ | youtube.title | h3 | N115、EB、LH（1927 年走到中心沒有坑）；標題不放棵數 | 200 | CONFIRMED | — |
| 2 | 說明欄第一段：日期、七點多、六十四公里外被掀下椅子、約兩千平方公里朝外倒、當天晚上夜空亮著 | youtube.description | h1,h3,h4,h7 | N115 7:15、N08 7:17／40 miles／hurled from his chair、EB 約 2,000 km²＋bright nighttime skies in Siberia and Europe | 200 | CONFIRMED | — |
| 3 | 說明欄第二段：敘事順序，含「最常被引用的『八千萬棵樹』不是數出來的」 | youtube.description | h33 | BB25 | 200 | CONFIRMED（當被駁回的數字講） | — |
| 4 | 說明欄第三段「每個數字、年份與引述的出處列在下方參考資料」 | youtube.description、sources | — | `sources[]` 只有 12 筆，`claims.md` 另外靠 10 個來源撐旁白（OSU、LH、BSE、AOP、Commons、G07、C08、AM65、BH73、BT74） | 200 | CHANGED | 見改動清單 C10 |
| 5 | 說明欄第四段：AI 插圖、歷史人物卡通化、不寫名字、在世或近代人物不入畫 | youtube.description | — | 與 112 個 prompt 核對：沒有一個 prompt 出現人名；研究者的場景用背影或只拍手。兩處可議見文末「附註」 | — | CONFIRMED（附註） | — |
| 6 | 資料截至 2026-10-10 | youtube.description | — | 查核檔的查核日 | — | CONFIRMED | — |
| 7 | 十個標籤（通古斯大爆炸、通古斯、歷史懸案、西伯利亞、庫利克、空爆、切科湖、未解之謎、1908、奇聞檔案局） | youtube.tags | — | 都是題目裡出現過的詞；沒有棵數、沒有「隕石坑」斷言 | — | CONFIRMED | — |
| 8 | 「樹站著／沒有坑」「一九〇八年的檔案」 | thumbnail.data | h17,h18 | N115「trees remained standing」、EB「a marshy bog but no crater」 | 200 | CONFIRMED | — |
| 9 | 一九〇八年六月三十日，早上七點多 | summer-river-morning/tg1a | h1 | N115「At about 7:15 am local time on June 30, 1908」、N08「7:17 a.m.」、EB「7:14 a.m. plus or minus one minute」——三個時刻，旁白只講「七點多」 | 200 | CONFIRMED | — |
| 10 | 西伯利亞一間交易站的門廊上坐著一個男人 | porch-with-mug/tg1b | h3,h4 | N08「sitting on the front porch of a trading post at Vanavara in Siberia」；名字不講 | 200 | CONFIRMED | — |
| 11 | 一聲巨響、他整個人被掀下椅子 | streak-over-treeline/tg1c、chair-tips-back/tg1d | h4 | N08「he will be hurled from his chair」、APS「thrown several feet from his chair」、AOP「a great blast pushed him off his chair」 | 200 | CONFIRMED | — |
| 12 | 卡片「1908.6.30／通古斯大爆炸／早上七點多」＋「那一聲後來叫做通古斯大爆炸」 | named-the-blast.data、tg1e | h1,h3 | 同 #9；L07「Tunguska event」 | 200 | CONFIRMED | — |
| 13 | 聲音的中心離他六十四公里 | across-the-haze/tg1f | h4 | N08 與 APS 都寫 40 miles（查核檔把兩頁當一個來源）；AOP 寫 65 km。40 英里＝64.4 公里 | 200 | CONFIRMED | — |
| 14 | 埃文基人的帳篷被撞得搖晃、人被震倒在地上 | tents-shuddering/tg1g、steadying-on-a-pole/tg1h | h5 | OSU「something suddenly hit her tent」「the tent shook again knocking them over」；N115 更重（blown into the air and knocked unconscious），旁白取較輕的那個 | 200 | CONFIRMED | — |
| 15 | 沒有人說得出剛剛是什麼 | steadying-on-a-pole/tg1i | 無 | h5 只蓋到帳篷與人被震倒；L07 的「Nobody considered a link between these phenomena」講的是當時沒人把夜亮、地震紀錄連起來，不是目擊者說不出話 | 200 | NOT FOUND | 見 C3 |
| 16 | 那天晚上從西伯利亞到歐洲夜空都亮著 | pale-night-roofs/tg1j | h6 | EB「abnormally bright nighttime skies in Siberia and Europe」、L07「Bright nights were observed over much of Eurasia」＋圖 18.6 標 1908-06-30 當夜 | 200 | CONFIRMED | — |
| 17 | 亮到有人半夜不點燈就讀起了報紙 | reading-without-a-lamp/tg1k | h6 | L07 逐字：「at midnight, it was possible to read the newspaper without artificial lights」（單一來源，查核檔已註明） | 200 | CONFIRMED | — |
| 18 | 那片森林裡的樹全部朝著外面倒了下去 | timber-from-above/tg1l、tg1m | h7 | N08「lying in a radial pattern」、N115「trees blown over for miles」、LH「the tops of the felled trees pointed outward, away from a center」、EB「the felled trees all pointed away from it」 | 200 | CONFIRMED | — |
| 19 | 第一章收尾問句 | looking-up-from-the-ground/tg1n | 無（應補進豁免名單） | — | — | OUT OF SCOPE | 見 C5 |
| 20 | 那幾個亮著的晚上之後，西伯利亞的地方報就登出了這件事 | column-circled-in-pencil/tg2a | h8 | L07「Up to 1921, meager information about a great 1908 bolide was published only in some local Siberian newspapers」、LH「Local newspapers carried stories about the flash, and the noise, and the heat」 | 200 | CONFIRMED | — |
| 21 | 報紙是七月十二號出的，離那個早上十二天 | twelve-days-of-marks/tg2b | h8 | COMMONS-SZ 檔案頁 Date 欄「12 July 1908」，Source 欄「№ 135 ... 29 июня (старый стиль)」，說明欄「сделанное «по слухам» через 12 дней после его падения」——十二天是來源自己寫的，不是本稿算的；檔名裡的「07-29」沒有被唸出來 | 200 | CONFIRMED | — |
| 22 | 俄國當時用的是舊曆，那天寫的是六月十七日 | two-calendars-side-by-side/tg2c | h2 | OSU「June 30, 1908 (June 17 according to the Russian calendar at the time)」。數字對，但「那天」緊接在 tg2b 的七月十二號之後，會被聽成報紙那天——報紙那天的舊曆是六月二十九日 | 200 | CHANGED | 見 C11 |
| 23 | 伊爾庫次克的觀測站更快，爆炸當天就開始向各地通訊員徵集目擊報告 | observatory-dome/tg2d、telegraph-forms-stacked/tg2e | h9 | L07 逐字：「Immediately after the registration of the earthquake N° 1536, in the morning of 30 June 1908, Voznesenskij sent to all his correspondents a request to report what they or other people had observed on that morning」 | 200 | CONFIRMED | — |
| 24 | 所以說十九年都沒有人知道，是不對的 | empty-chair-at-the-desk/tg2f | h9 | L07（#20、#23）；N115 講的是「No scientific expeditions ... for nearly 20 years」，旁白正好改成「沒有人走到」而不是「沒有人知道」 | 200 | CONFIRMED | — |
| 25 | 真正被放下的是地震儀和氣壓計上的紀錄；要到一九二五年和一九三〇年才被連回那個早上 | seismograph-drum/tg2g,tg2h、rolls-on-a-shelf/tg2i | h10 | L07：地震波「the first paper that connected to the TE ... was published only in 1925 (Voznesenskij 1925)」；氣壓紀錄「were associated with the TE some twenty years later (Whipple 1930; Astapovich 1933)」 | 200 | CONFIRMED | — |
| 26 | 爆心附近的埃文基人，起初不願意談這件事 | tent-flap-half-closed/tg2j,tg2k | h11 | N08 逐字是「At first, the locals were reluctant to tell Kulik about the event」——不願意談的對象是庫利克（一九二七年以後），這一句卻排在庫利克出場（tg2o）之前；「埃文基人」＝「the locals」由 N115「the local Evenki people」與 APS「mostly indigenous Evenki natives」支撐，這部分沒問題 | 200 | CHANGED（低） | 見 C12 |
| 27 | 他們認為是神靈奧格迪降臨了 | carved-pole-in-the-clearing/tg2l | h11 | N08 引 JPL 的 Yeomans：「They believed the blast was a visitation by the god Ogdy」（單一來源，查核檔已註明）；只當他們的信仰講一次，沒有當笑點 | 200 | CONFIRMED | — |
| 28 | 缺的從來不是消息，是有人走到那片森林裡 | rail-ends-at-the-forest/tg2m | 無（應補進豁免名單） | 是 #24、#25 的敘事收攏，不是新事實 | — | OUT OF SCOPE | 見 C4 |
| 29 | 這件事等了十三年 | rail-ends-at-the-forest/tg2n | 算術（claims.md 已列） | 1908→1921 | — | CONFIRMED | — |
| 30 | 一九二一年蘇聯科學院派出一位地質學家 | academy-corridor/tg2o | h12 | N115 逐字：「The Soviet Academy of Sciences first sent geologist Leonid A. Kulik on an expedition to the site in 1921」；LH「he convinced the Academy of Sciences to sponsor a trip to the region. This was in 1921」 | 200 | CONFIRMED | — |
| 31 | 他叫庫利克，一八八三年八月十九日生 | geologist-with-a-hammer/tg2p | h13 | LH「born Aug. 19, 1883」；BSE「[7(19).8.1883, Дерпт...]」。出生地（塔爾圖）按長度取捨沒講 | 200 | CONFIRMED | — |
| 32 | 他相信那裡有一塊鐵隕石，只要走到就能挖出來 | iron-lump-in-a-palm/tg2q,tg2r | h14 | L07「continued searching for an iron body, similar to one found in Arizona」；LH「with perhaps tons of meteoritic iron」；APS「to possibly salvage any meteoric iron」；OSU「there should be fragments of a ferrous space rock」 | 200 | CONFIRMED | — |
| 33 | 結果那一帶根本走不進去 | bog-swallows-the-cart/tg2s | h12 | N115「the area proved so inaccessible that he could not reach it」；APS「the harsh conditions ... foiled his team's efforts to reach the blast area」 | 200 | CONFIRMED | — |
| 34 | 那一年和第二年，他最遠只到坎斯克 | end-of-the-road-town/tg2t | h12 | L07「the first Kulik expedition (1921–1922)」「The first expedition could not go farther than Kansk」 | 200 | CONFIRMED | — |
| 35 | 卡片「六百公里／離現場還有」「0 次／走到爆心」＋「離現場還有六百公里」「他沒有走到」 | still-six-hundred.data、tg2u、tg2v | h12 | L07「Kansk, about 600 km from the Tunguska explosion site」；N115「he could not reach it」。卡片出處欄「波隆那大學專書章 2026-10-10」對得上 | 200 | CONFIRMED | — |
| 36 | 他回去以後沒有放棄，六年後又出發了 | coat-on-a-hook/tg2w,tg2x | h15（六年＝算術） | LH 不只支持算術，還直接寫「it took him 6 years to persuade his superiors that it was worth further investigation. In 1927, he returned with a small party」。L07 從一九二二年起算寫「Five years later」，旁白沒有用五年這個講法 | 200 | CONFIRMED | — |
| 37 | 一九二七年，他終於走到了 | wading-the-last-stretch/tg3a | h15 | N115「Not until 1927 did Kulik succeed in reaching his goal」；LH、APS 同 | 200 | CONFIRMED | — |
| 38 | 最先看到的是倒下的樹；樹幹像輪子的輻條全部指著外面；順著方向往裡走就能走到中心 | first-fallen-trunks/tg3b、spokes-of-a-wheel/tg3c,tg3d、walking-the-arrows/tg3e | h7,h15 | LH「the fallen trees formed a vast radial ring, with the tops of the felled trees pointed outward, away from a center」；EB「The epicentre was easy to pinpoint because the felled trees all pointed away from it」 | 200 | CONFIRMED | — |
| 39 | 那是他第一次走到那裡 | walking-the-arrows/tg3f | h15 | N115（#37）；一九二一年沒走到見 #33、#34 | 200 | CONFIRMED | — |
| 40 | 後來量出來的範圍，大約兩千一百五十平方公里 | butterfly-of-ruin/tg3g | h16 | L07「devastated 2 150 ± 50 km2」。旁白保留「大約」，±50 沒講；EB 的 2,000 與 G07 的「over 2000」按「一個事實只講一次」沒重複 | 200 | CONFIRMED | — |
| 41 | 不是一個圓，是一隻蝴蝶的形狀 | butterfly-of-ruin/tg3h | h16 | N115「a butterfly-shaped area of destruction」；EO「the butterfly-shaped blast zone」。兩個蝴蝶場景的 prompt 都寫「two uneven wings」，沒有畫正圓 | 200 | CONFIRMED | — |
| 42 | 但這還不是最奇怪的地方 | hand-on-a-root-plate/tg3i | 豁免 | 升級句 | — | OUT OF SCOPE | — |
| 43 | 走到正中央樹還站著；枝葉被剝光、樹皮也沒了；上面還有燒過的痕跡 | standing-at-the-middle/tg3j、stripped-bark-close/tg3k、scorch-on-the-wood/tg3n | h17 | N115 逐字：「Near the epicenter, trees remained standing but with broken branches and stripped of bark, with evidence of burning」 | 200 | CONFIRMED | — |
| 44 | 一根一根像一排電線桿；那片枯樹後來被人叫做電線桿森林 | poles-in-a-row/tg3l,tg3m | h17 | LH：「he encountered what he called a 'telegraph-pole forest,' with dead trees still standing, but stripped on all their branches」——這個說法是庫利克當場自己取的，不是後來別人叫的 | 200 | CHANGED | 見 C8 |
| 45 | 他要找的那個坑不在那裡；正中央是一片沼澤 | hammer-down-in-the-moss/tg3o,tg3p | h17,h18 | LH「when Kulik got to the center, he did not find the expected crater」；EB「at that spot, investigators observed a marshy bog but no crater」；APS「surprised, upon arrival, to see that there was no impact crater」 | 200 | CONFIRMED | — |
| 46 | 方圓一萬五千平方公里之內沒有一個撞擊坑／卡片「沒有坑／一九二七年的爆心／一萬五千平方公里之內都沒有」 | no-crater/tg3q、no-crater.data | h18 | L07 的原文是「neither macroscopic fragments ... nor a typical signature of an impact, like a crater, have **ever** been found in an area of 15 000 km2」——這是寫到二〇〇七年為止的累計結果，不是一九二七年那一趟的結論。一九二七年證明的是爆心沒有坑（N115、EB、LH） | 200 | CHANGED | 見 C4 |
| 47 | 碎片也沒有 | no-crater/tg3r | h18 | L07 的限定詞是「macroscopic」；N19「no one found fragments」；但 EB 寫「The only likely remains ... are a few small fragments, each less than a millimetre across」，本稿自己在 tg4q 也講了微小碎屑 | 200 | CHANGED | 見 C5（補「大塊」） |
| 48 | 後面那幾年他又帶隊回去了幾次 | boots-back-on-the-trail/tg3s | h19 | EB「first investigated from 1927 to 1930 in expeditions led by ... Kulik」；BSE「в 1927—30 и в 1938—39 возглавлял экспедиции」；APS「Over three successive expeditions」 | 200 | CONFIRMED | — |
| 49 | 每一次都在找同一樣東西，一塊鐵 | sieve-of-grit/tg3t,tg3u | h14 | L07（#32）；OSU「trying and failing to find it」 | 200 | CONFIRMED | — |
| 50 | 今天你查通古斯，最常看到的數字是八千萬棵倒樹 | number-on-every-screen/tg3v | h33 | BB25「the '80 million trees' claim has propagated into other sources as if it were an established fact that needs no citation」；我今天自己看到照寫的頁面：N08（NASA）「Eighty million trees were on their sides」、L07「Eighty millions trees were flattened」、AOP「80 million trees over ... 2150 square kilometres」。講法是「最常看到的數字」，不是事實 | 200 | CONFIRMED（當流傳的數字） | — |
| 51 | 「這個數字從哪裡來，等一下會回來」「壓倒這片森林的東西到底去哪裡了？」 | knot-in-a-string/tg3w,tg3x | 豁免 | 前向鉤子與章末問句 | — | OUT OF SCOPE | — |
| 52 | 庫利克的答案是它還在地底下；他認為沼澤底下就是那個大撞擊坑 | pointing-at-the-ground/tg4a、round-hollows-in-the-bog/tg4b | h20 | G07「concluded that he had discovered the remains of a large impact crater now hidden by a swamp」 | 200 | CONFIRMED | — |
| 53 | 沼澤上有一些圓形的凹坑，他把它們當成隕石砸出來的小坑 | round-hollows-in-the-bog/tg4c、pacing-the-rim/tg4d | h20 | G07「a number of secondary bowl-shaped holes of different sizes covered by peat bogs possibly caused by a fragmented body」；APS「several small 'pothole' bogs that he assumed were meteorite craters」 | 200 | CONFIRMED | — |
| 54 | 其中一個叫蘇斯洛夫坑 | pacing-the-rim/tg4e | h21 | APS「(dubbed the 'Suslov crater')」（單一來源，查核檔已註明） | 200 | CONFIRMED | — |
| 55 | 他決定把水抽乾 | planks-across-the-peat/tg4f | h21 | APS「when he finally drained one of the bogs」 | 200 | CONFIRMED | — |
| 56 | 人、木板和幫浦，全部搬進沼澤 | planks-across-the-peat/tg4g | h21 | 今天開的每一頁都只說他「抽乾了其中一個」，沒有一頁交代用什麼抽、有沒有鋪木板。h21 只掛 APS 那一句 | 200 | NOT FOUND | 見 C7 |
| 57 | 水一點一點降下去 | hand-pump-working/tg4h | h21 | APS「drained」 | 200 | CONFIRMED | — |
| 58 | 露出來的不是鐵，是一截老樹樁 | stump-breaks-surface/tg4i,tg4j | h21 | APS 逐字：「an old stump at the bottom proved it could not be such a crater」 | 200 | CONFIRMED | — |
| 59 | 他抽的那個坑裡，始終沒有大塊殘骸 | silted-floor-of-the-pit/tg4k | h22 | G07「All attempts at finding macro-remnants of the cosmic body in these circular depressions were unsuccessful」（來源講的是所有圓坑，旁白收窄到他抽的那一個，沒有講多） | 200 | CONFIRMED | — |
| 60 | 「這一段我讀起來最難受」「他站的地方是對的，想的東西不對」 | sitting-on-the-planks/tg4l,tg4m | 豁免 | 標成講述者自己的感受 | — | OUT OF SCOPE | — |
| 61 | 接著三年他大多在找鐵質碎片，一塊都沒有找到 | magnet-over-a-tray/tg4o、empty-specimen-boxes/tg4p | h23 | OSU 逐字：「Kulik spent the better part of the next three years in the Tunguska taiga trying and failing to find it」 | 200 | CONFIRMED | — |
| 62 | 後來有人找到一些微小的碎屑，可是沒辦法確定跟那一聲有關 | grain-under-glass/tg4q,tg4r | h24 | N115 逐字：「later expeditions found microparticles indicating an extra-terrestrial origin, these remnants could not be conclusively tied to the blast」；EB「a few small fragments, each less than a millimetre across」 | 200 | CONFIRMED | — |
| 63 | 離那片沼澤不遠還有一座湖，叫切科湖 | round-lake-from-the-air/tg4s | h25 | EO「nearby Lake Cheko」；G07「located ∼8 km NNW of the inferred explosion epicenter」；C08「a few kilometres downrange from the assumed epicentre」 | 200 | CONFIRMED | — |
| 64 | 它要很久以後才變成線索，晚一點再說 | round-lake-from-the-air/tg4t | 豁免 | 前向鉤子 | — | OUT OF SCOPE | — |
| 65 | 他還在挖的時候，別人已經開始往天上找了 | chalk-on-a-lecture-board/tg4u | 豁免 | 接續句 | — | OUT OF SCOPE | — |
| 66 | 一九三〇年，有人提出它是一顆彗星的碎片 | comet-over-a-field/tg4v | h27 | APS「the object that exploded in the atmosphere was a comet (possibly the Comet Encke). This notion was first proposed in 1930 by British astronomer F. J. W. Whipple」；L07「Shapley (1930) was the first to suggest that the Tunguska event was caused by the impact of a comet」——一九三〇年提的是「一顆彗星」，沒有一頁寫「碎片」 | 200 | CHANGED | 見 C6 |
| 67 | 彗星說要解釋的，就是那個沒有坑的問題 | comet-on-a-glass-plate/tg4w | h27 蓋不到 | 兩份講一九三〇年彗星說的頁面給的理由都不是「沒有坑」：APS「a hypothesis supported in part by the glowing skies observed after the blast」、EB「On the basis of historical records of significant noctilucent cloud development」。而 L07 明寫「Kazantsev was the first who explained the lack of fragments or impact craters in Tunguska by an explosion in the atmosphere」——本稿自己在 tg5g 就是這樣講的，所以 tg4w 同時沒來源又跟 tg5g 相衝 | 200 | NOT FOUND | 見 C2 |
| 68 | 這個說法一直留到今天 | comet-on-a-glass-plate/tg4x | 無 | EB「either a comet or an asteroid」；AOP「Some argue that it was a small asteroid, others that it must have been a small comet (or a comet fragment)」——事實站得住，只是沒有主張列 | 200 | CONFIRMED（主張列缺） | 見 C14 |
| 69 | 最早這樣說的是誰，兩份資料寫的不一樣 | two-plaques-on-a-wall/tg4y | h27 | APS 記 F. J. W. Whipple、L07 記 Shapley；旁白兩個名字都不講，只講「不一樣」 | 200 | CONFIRMED | — |
| 70 | 庫利克沒有等到答案；一九四一年開戰以後他加入了民兵 | militia-armband/tg4z,tg4aa | h26 | BSE「В начале Великой Отечественной войны 1941—45 ... вступил добровольцем в народное ополчение」 | 200 | CONFIRMED | — |
| 71 | 受傷、被俘，一九四二年四月十四日過世 | single-bed-in-a-hut/tg4ab | h26 | BSE「был ранен и погиб в плену」＋卒日「14.4.1942」；LH「He died during the war, in 1942」。病名兩個來源都沒給，旁白也沒講 | 200 | CONFIRMED | — |
| 72 | 從出發到過世，他在這件事上花了二十一年 | hammer-left-on-the-sill/tg4ac | 算術（claims.md 已列） | 1921→1942 | — | CONFIRMED | — |
| 73 | 他過世四年後，這件事換了一種講法 | magazine-on-a-kiosk/tg5a | 算術（claims.md 未列） | 1942→1946，與 #71、#74 相容 | — | CONFIRMED（主張列缺） | 見 C15 |
| 74 | 一九四六年，一本蘇聯雜誌登了一篇小說 | magazine-on-a-kiosk/tg5b | h28 | L07 參考文獻：「Kazantsev AP (1946) Vzryv. Vokrug sveta 1:39–46」；篇名與作者都沒講 | 200 | CONFIRMED | — |
| 75 | 故事裡爆炸來自一艘外星核動力太空船 | saucer-over-the-taiga/tg5c | h28 | OSU「an atomically-powered space craft from another planet blew up over Siberia」；L07「Others consider alien spacecrafts (Kazantsev 1946 ...)」 | 200 | CONFIRMED | — |
| 76 | 那是廣島之後寫的；它是小說，不是紀錄 | typewriter-and-a-blank-sheet/tg5d,tg5e | h28 | OSU「Writing after the nuclear detonations that ended World War II」。只當時間座標用，沒有講廣島的倍數；prompt 沒有畫城市 | 200 | CONFIRMED | — |
| 77 | 有一位研究者寫道，最早用在空中爆炸解釋沒有坑的，就是這篇小說 | book-chapter-open/tg5f,tg5g | h28 | L07 逐字：「Kazantsev was the first who explained the lack of fragments or impact craters in Tunguska by an explosion in the atmosphere」。單一來源，旁白已經掛了「有一位研究者寫道」 | 200 | CONFIRMED | — |
| 78 | 一九五〇年代末，還有人為它組了一支民間考察隊 | volunteers-with-packs/tg5h | h29 | OSU「Inspired by Kazantsev's story, an independent cohort of scientists began making annual expeditions to the site of the explosion in the late 1950s」 | 200 | CONFIRMED | — |
| 79 | 更離奇的還在後面 | eyebrow-raised-at-a-journal/tg5i | 豁免 | 升級句 | — | OUT OF SCOPE | — |
| 80 | 一九六五年，有人提出是反物質 | two-particles-meeting/tg5j | h30 | AM65 頁面：〈Possible Anti-Matter Content of the Tunguska Meteor of 1908〉，Nature，Published 29 May 1965 | 200 | CONFIRMED | — |
| 81 | 一九七三年，有人提出是一個黑洞穿過地球 | globe-with-a-thread/tg5k | h30 | BH73 頁面：〈Was the Tungus Event due to a Black Hole?〉，Nature Letter，14 September 1973，摘要只到「a black hole of substellar mass such as those that have been postulated by Hawking could explain many of the mysteries associated with the event」。「穿過地球」在 BH73、L07、BT74、查核檔、claims.md 裡都沒有 | 200 | NOT FOUND | 見 C1 |
| 82 | 兩篇都登在同一份期刊上 | journal-spines-on-a-shelf/tg5l | h30 | AM65 與 BH73 兩個頁面都是 nature.com；旁白沒有唸刊名 | 200 | CONFIRMED | — |
| 83 | 黑洞那一篇，隔年就被另一篇反駁了 | journal-spines-on-a-shelf/tg5m | h30 | BT74：〈Tungus event was not caused by a black hole〉，Nature Letter，01 August 1974；摘要「Several lines of evidence render the black hole hypothesis extremely unlikely」 | 200 | CONFIRMED | — |
| 84 | 剛剛那位研究者寫得很直接：這些說法在技術上站不住 | pen-across-a-paragraph/tg5n,tg5o | h31 | L07「Several of them, though published in scientific journals, were found to be technically groundless, e.g. ... antimatter meteors (Cowan et al. 1965), and tiny black holes (Jackson and Ryan 1973)」，緊接著是他自己的話「Nevertheless, I think that here we can ignore such extremely 'non-traditional' hypotheses」 | 200 | CONFIRMED（附註） | — |
| 85 | 至於特斯拉的死光，是冷戰結束以後才有人提的 | coil-under-a-dust-sheet/tg5p | h32 | OSU「After the end of the Cold War, some have suggested that Nikolai Tesla triggered Tunguska by experimenting with his secret death ray」。特斯拉本人說法的出處查核檔判 NOT FOUND，旁白也沒講 | 200 | CONFIRMED | — |
| 86 | 「這些版本你多半聽過」「最常被引用的那個數字，問題比它們更大」 | nodding-at-a-table/tg5q,tg5r | 豁免 | 轉折句 | — | OUT OF SCOPE | — |
| 87 | 還記得那八千萬棵倒樹嗎 | finger-stops-on-a-figure/tg6a | h33 | 回扣 #50 的「最常看到的數字」，不是新斷言 | 200 | CONFIRMED（當流傳的數字） | — |
| 88 | 二〇二五年，一篇期刊評論去追它的來歷 | reviewer-at-two-screens/tg6b | h33 | BB25：Scientific Reports 15:13869，2025，Matters Arising，開放取用 | 200 | CONFIRMED | — |
| 89 | 他們一路追到一九三三年 | oldest-box-in-the-stack/tg6c | h33 | BB25 參考文獻 5＝「Astapovich, I. S. ... Astron. Zh. 10, 465–486 (1933)」 | 200 | CONFIRMED | — |
| 90 | 那一年有人要估這場爆炸的能量；要估能量先要知道倒樹的面積 | slide-rule-and-blank-pad/tg6d,tg6e | h33 | BB25 逐字：「The sole aim of the primary source was to roughly estimate the energy of the explosion, starting with an educated guess about the area to approximate the number of fallen trees as a step toward his goal」 | 200 | CONFIRMED | — |
| 91 | 他假設那個面積是大約八千平方公里；再從面積換算出棵數 | tracing-a-rough-outline/tg6f,tg6g | h33 | BB25 引 Astapovich 原文：「Apparently, it can be assumed that the area of the fallen forest occupies about 8000 km2」，結論「the work of the windfall of 8⋅10⁷ trees would be 4.4⋅10²¹ ergs」 | 200 | CONFIRMED | — |
| 92 | 問題是，那個面積錯了 | outline-too-big/tg6h | h33 | BB25「the area of devastation that he overestimated by a factor of about four」 | 200 | CONFIRMED | — |
| 93 | 對照卡「一九三三年假設 約 8,000 平方公里／為了估能量而設」對「後來量到 約 2,150 平方公里／蝴蝶形，不是圓」，裁定「高估約四倍」，出處「二〇二五年期刊評論、波隆那大學專書章」 | assumed-against-measured.data | h16,h33 | 左欄來自 BB25 引的 Astapovich 1933；右欄的 2,150 來自 L07；「高估約四倍」是 BB25 自己的字。卡片上沒有棵數 | 200 | CONFIRMED | — |
| 94 | 實際量到的範圍，只有他假設的四分之一左右 | assumed-against-measured/tg6i | h16,h33 | 這是 BB25「a factor of about four」的倒數，不是本稿拿 2,150÷8,000 自己算出來的比例；本稿也沒有自己換算任何棵數 | 200 | CONFIRMED | — |
| 95 | 一邊是假設，一邊是後來量到的 | assumed-against-measured/tg6j | h16,h33 | 同 #93 | 200 | CONFIRMED | — |
| 96 | 所以棵數從一開始就高估了 | tree-count-crossed-out/tg6k | h33 | BB25「inflating the number of fallen trees by a factor of about four」。旁白只說「高估」，沒有給一個「正確棵數」 | 200 | CONFIRMED | — |
| 97 | 更麻煩的是接下來發生的事；這個數字被一篇一篇抄下去 | stack-of-offprints/tg6l,tg6m | 豁免（tg6l）、h33（tg6m） | BB25「misinformation was introduced in a chain of citations」 | 200 | CONFIRMED | — |
| 98 | 他們追的是一條引用鏈；每一篇都只是引上一篇 | four-links-of-a-chain/tg6n,tg6o | h33 | BB25 的鏈條：Bunch et al.→Brazo & Austin 1982→（引）Whipple 1934→（實為一位通信者，依據）Crommelin 1934→Astapovich 1933 | 200 | CONFIRMED | — |
| 99 | 一九三四年有兩篇文章引了它 | letters-column-in-a-journal/tg6p | h33 | BB25 參考文獻 3＝Whipple 1934（R. Meteorol. Soc. Q. J. 60）、4＝Crommelin 1934（J. Br. Astron. Assoc. 44）；旁白不唸刊名與人名 | 200 | CONFIRMED | — |
| 100 | 其中一篇引的，是一位通信者的話，不是作者自己說的 | letters-column-in-a-journal/tg6q、wrong-name-on-a-card/tg6r | h33 | BB25 逐字：「The 80 million trees claim was not actually made by Whipple but by a correspondent, based on Crommelin, whose source was Astapovich」 | 200 | CONFIRMED | — |
| 101 | 一九八二年又有人照抄 | wrong-name-on-a-card/tg6s | h33 | BB25「Brazo and Austin ... who wrote 'eighty million trees in the taiga ... were uprooted and blown down' with a citation to a 1934 paper by Whipple」，並寫「Since Brazo & Austin's 1982 article was published」 | 200 | CONFIRMED | — |
| 102 | 抄到後來，它變成一個不用附出處的事實 | no-footnote-left/tg6t | h33 | BB25 的字是「has propagated into other sources **as if it were** an established fact that needs no citation」——「好像是」這個鉤子掉了 | 200 | CHANGED | 見 C9 |
| 103 | 九十幾年後，你還會在影片和文章裡看到它 | same-line-in-two-places/tg6u | h33（九十幾年＝算術，已列） | 1933→2026＝93；我今天自己在 N08（NASA）、L07、AOP 三頁上看到它照寫 | 200 | CONFIRMED | — |
| 104 | 「這一集不會把它當事實講」「紀錄撐得住的，只有那個面積」 | file-set-straight/tg6v,tg6w | 豁免／h33 | 前句是編輯決定；後句對應 L07 的 2,150 ± 50 | 200 | OUT OF SCOPE／CONFIRMED | — |
| 105 | 是什麼東西壓出剛剛那隻蝴蝶的形狀？ | wings-on-the-moss/tg6x | 豁免 | 章末問句 | — | OUT OF SCOPE | — |
| 106 | 壓出那個形狀的，是一個幾十公尺大的天體 | burst-high-above/tg7a | h35 | 四個估計：N115「130 feet」（約 40 m）、N08「about 120 feet」、N19「between 164 and 262 feet」、EB／EO「50–100 m」——全部落在「幾十公尺」，旁白沒有挑一個數字 | 200 | CONFIRMED | — |
| 107 | 它衝進大氣，在半空中炸開 | rock-against-the-sky/tg7b | 無 | EO「an object ... plunged into Earth's atmosphere, creating a brilliant fireball that exploded over a remote part of Siberia」；N115「an asteroid plunged into Earth's atmosphere and exploded in the skies over Siberia」。事實站得住，但這是本集的主線句，卻沒有主張列 | 200 | CONFIRMED（主張列缺） | 見 C13 |
| 108 | 主流的估計是離地五到十公里 | ridge-far-below/tg7c | h34 | EB「at an altitude of 5–10 km (15,000–30,000 feet)」；L07「height of the explosion (5–10 km)」；G07「exploded about 5–10 km above ground」；EO「about 6 to 10 kilometers」 | 200 | CONFIRMED | — |
| 109 | 卡片「幾十公尺／天體大小」「5–10 公里／離地高度」「10–14 公里／二〇一九年模擬」，出處「大英百科、波隆那大學專書章、美國太空總署」 | how-high.data | h34,h35 | 兩個高度範圍都在卡片上，沒有被併成一個數字；三個出處都對得上 | 200 | CONFIRMED | — |
| 110 | 二〇一九年的一次模擬估到十到十四公里 | how-high/tg7e | h34 | N19「at 6 to 9 miles altitude」＝9.7–14.5 公里；單位換算正確，而且旁白把它標成「二〇一九年的一次模擬」，沒有跟 5–10 公里混成一個範圍 | 200 | CONFIRMED | — |
| 111 | 衝擊波往下往外壓，剛剛那些朝外倒的樹就是這樣倒的 | trunks-go-over-together/tg7f,tg7g | h7,h36 | N115「The resultant shock wave and thermal radiation most likely correlate with ... the destruction described by later expeditions」；SNL「the center of mass of an asteroid exploding above the ground is transported downward at speeds faster than sound」 | 200 | CONFIRMED | — |
| 112 | 本體幾乎全部氣化，所以地上沒有坑 | nothing-left-in-the-air/tg7h,tg7i | h18,h36 | EO「vaporizing the vast majority of the incoming bolide」；N115「A mid-air explosion most likely vaporized the object」；EB「Because the object exploded in the atmosphere high above Earth's surface, it created a fireball and blast wave but no impact crater」。「幾乎」這個鉤子有留住 | 200 | CONFIRMED | — |
| 113 | 換成炸藥，三百萬噸到三千萬噸都有人算過 | sacks-on-a-weighbridge/tg7k | h37 | SNL「what scientists had thought to be an explosion between 10 and 20 megatons was more likely only three to five megatons」；N19「a 10 to 30 megaton explosion」；EB「as much as 15 megatons」；L07 另記 10–15 與 30–50。三到三十百萬噸是查核檔指定的講法，旁白用「都有人算過」而不是「是」 | 200 | CONFIRMED | — |
| 114 | 有模擬把它往低的一端壓，到現在還沒有定論 | simulation-on-a-screen/tg7l | h37 | SNL 同上（10–20→3–5） | 200 | CONFIRMED | — |
| 115 | 還記得那座切科湖嗎；二〇〇七年有一隊人說，湖底像撞擊坑 | boat-on-the-round-lake/tg7m,tg7n | h38 | G07〈A possible impact crater for the 1908 Tunguska Event〉：「Its funnel-like bottom morphology and the structure of its sedimentary deposits ... all suggest that the lake fills an impact crater」 | 200 | CONFIRMED | — |
| 116 | 二〇〇八年另一隊說，極不可能 | sonar-trace-rejected/tg7o | h38 | C08〈Evidence that Lake Cheko is not an impact crater〉：「We therefore conclude that Lake Cheko is highly unlikely to be an impact crater」 | 200 | CONFIRMED | — |
| 117 | 二〇一七年的研究說，沉積比那場爆炸老 | core-tube-of-mud/tg7p | h38 | R17〈Sedimentation rate in Cheko Lake ...〉，Doklady Earth Sciences，Published 04 November 2017：「indicate that Cheko Lake is significantly older than the 1908 Tunguska Event」（論文的結論其實更強——湖本身更老；旁白只講沉積，講得比來源少） | 200 | CONFIRMED | — |
| 118 | 湖底的事，到現在沒有結論 | core-tube-of-mud/tg7q | h38,h42 | EO「Some researchers have proposed that nearby Lake Cheko may have formed as a result of a falling bolide fragment, but other research teams dispute that idea」 | 200 | CONFIRMED | — |
| 119 | 二〇一九年一篇論文統計，倒樹區內外至少三十人；其中至少三人因此過世 | names-on-a-tally/tg7s,tg7t | h39 | J19 摘要逐字：「We find that inside and near the tree-fall area were at least 30 people. Many lost consciousness and at least 3 passed away (immediately or later) as a direct consequence of the Tunguska event」 | 200 | CONFIRMED | — |
| 120 | 也有資料只記兩則未經證實的報告 | two-slips-in-a-tray/tg7u | h39 | AOP 逐字：「Apart from two unconfirmed reports there are thought to have been no human casualties caused by the Tunguska event」 | 200 | CONFIRMED | — |
| 121 | 有沒有人喪生，也沒有結論 | two-folders-left-open/tg7r | h39,h42 | J19 與 AOP 兩說並列（另有 OSU「At least two others appear not to have been so fortunate」、N115「very few human casualties resulted」，旁白沒有再加） | 200 | CONFIRMED | — |
| 122 | 那個天體是石質小行星還是彗星碎片，還在爭論 | stone-and-ice-side-by-side/tg7v | h40 | EB 兩說並列；AOP「Some argue that it was a small asteroid, others that it must have been a small comet (or a comet fragment)」——「彗星碎片」這個字在 AOP 上；C93 石質小行星；L07「It is difficult to definitely support one or the other hypothesis」。N115 的「most scientists today believe it was an asteroid」旁白沒有拿來當定論 | 200 | CONFIRMED | — |
| 123 | 二〇一三年二月十五日，車里雅賓斯克上空 | contrail-over-a-city-street/tg7z | h41 | N19「February 15, 2013 ... near Chelyabinsk, Russia」；N115 同日期 | 200 | CONFIRMED | — |
| 124 | 很多人第一次親眼看到空爆 | faces-turned-up/tg7aa | h41 | N19 寫的是「This highly documented fireball created an opportunity for researchers to apply modern computer modeling techniques」，沒有寫「第一次有人親眼看到空爆」。這是查核檔〈給撰稿的提醒〉的原句，照它寫了 | 200 | CONFIRMED（附註） | — |
| 125 | 卡片「未結／通古斯大爆炸／紀錄到今天還沒有定論」＋「那個早上到現在，一百一十八年」 | still-open.data、tg7ac | h42（一百一十八年＝算術，已列） | 1908→2026；查核檔文末「未結」 | — | CONFIRMED | — |
| 126 | 這份檔案，蓋的是未結 | outro/tg7ad | h42 | 同上 | — | CONFIRMED | — |
| 127 | 片尾卡字「那個早上掉下來的東西，從來沒有落地」 | outro.data.lines[0] | h42 | EO 只說「vast majority」被氣化；EB 記有毫米級碎片；而本集自己在 tg7n–tg7q 把「有沒有碎片砸出切科湖」列為沒有結論。這一句把那件沒有結論的事講成定論，而且是觀眾記得最牢的位置 | 200 | CHANGED | 見 C6 |
| 128 | 片尾問句與訂閱句 | outro/tg7ae,tg7af | — | 不講下一支，沒有事實 | — | OUT OF SCOPE | — |
| 129 | `loops[]` 五條（tg1g→tg2j、tg1k→tg2g、tg1m→tg3c、tg3v→tg6a、tg4t→tg7m） | loops | — | 內部標記；五個 payoff 行都在稿內，對得上 | — | OUT OF SCOPE | — |
| 130 | `sources[]` 12 筆、checked_on 全為 2026-10-10 | sources | — | 12 個網址我今天全部重開，全部 200（Britannica 用存檔，直連 403）；日期標 2026-10-10 與查核檔一致 | 200 | CONFIRMED（但見 #4） | — |
| 131 | 112 個 prompt 沒有人名、沒有廣島城市、沒有死去的馴鹿或傷者、蝴蝶形不畫正圓、信仰不當笑點 | scenes[].data.prompt | — | 逐個看過；見文末「附註」兩處 | — | CONFIRMED（附註） | — |

## 第 4 點：第六章那個被駁回的數字

**結論：這一章沒有把「八千萬棵樹」當事實講，來歷與引用鏈都對得上 BB25，沒有一個數字是本稿自己算的。** 逐條說：

1. **從來沒有當事實講。** 全稿「八千萬」只出現在四個地方，我每一個都看過原文：
   - `loops[3].what`「八千萬棵這個數字從哪裡來」——內部標記，不會被唸、不會上畫面。
   - 說明欄：「二〇二五年一篇期刊評論追出來的事：最常被引用的『八千萬棵樹』不是數出來的」——加了引號，而且當場否定。
   - tg3v：「今天你查通古斯，**最常看到的數字**是八千萬棵倒樹」——說的是「你會看到這個數字」，不是「有八千萬棵」。
   - tg6a：「還記得那八千萬棵倒樹嗎」——回扣 tg3v 的同一個框。

   另外，**標題沒有棵數、十個標籤沒有棵數、縮圖沒有棵數、六張卡片（含對照卡）一個棵數都沒有**——查核檔要的「棵數不上卡片」做到了。
   tg6v 還明說「這一集不會把它當事實講」。

2. **掛在一九三三年、掛在高估約四倍的面積上。** tg6c「一路追到一九三三年」對應 BB25 參考文獻 5（Astapovich 1933，Astron. Zh. 10）；
   tg6d／tg6e「那一年有人要估這場爆炸的能量／要估能量先要知道倒樹的面積」逐字對應 BB25「The sole aim of the primary source was to roughly estimate
   the energy of the explosion, starting with an educated guess about the area to approximate the number of fallen trees as a step toward his goal」；
   tg6f「他假設那個面積是大約八千平方公里」對應 BB25 引的原句「Apparently, it can be assumed that the area of the fallen forest occupies about 8000 km2」；
   tg6h／tg6k「那個面積錯了／所以棵數從一開始就高估了」對應「the area of devastation that he overestimated by a factor of about four」與
   「inflating the number of fallen trees by a factor of about four」。對照卡 `assumed-against-measured` 把 8,000 標成「一九三三年假設／為了估能量而設」、
   把 2,150 標成「後來量到」，裁定「高估約四倍」，出處欄寫「二〇二五年期刊評論、波隆那大學專書章」——分得清楚，沒有把 2,150 算到 BB25 頭上。

3. **四分之一是 BB25 的數，不是本稿的算術。** tg6i「實際量到的範圍，只有他假設的四分之一左右」正好是 BB25「a factor of about four」的倒數。
   我特別查過：BB25 全文唯一的面積數字是 Astapovich 的「8000 km」，它沒有提出自己的面積值，所以本稿把 2,150 掛在 L07（「2 150 ± 50 km2」）是對的做法。
   本稿也**沒有**自己換算任何棵數——查核檔明令不准的「自己換算出來的棵數」一個都沒有。

4. **引用鏈對得上 BB25，不是本稿重排的。** BB25 的鏈條是：Astapovich 1933 →（Crommelin 1934）→ Whipple 1934 裡**一位通信者**的話（不是 Whipple 本人）→ Brazo 與 Austin 1982 → 之後各處照抄。
   腳本 tg6n–tg6s 講的是：一條引用鏈／每一篇只引上一篇／一九三四年有兩篇文章引了它／其中一篇引的是一位通信者的話／不是作者自己說的／一九八二年又有人照抄。
   逐條都在 BB25 的那一段裡，連「不是作者自己說的」都是 BB25 的「was not actually made by Whipple but by a correspondent」。刊名與人名一個都沒唸，符合查核檔「不講名字」的尺度。

5. **唯一要改的一句**是 tg6t「抄到後來，它變成一個不用附出處的事實」：BB25 的原文有「**as if it were**」這個鉤子（「好像是一個不需要出處的既定事實」），
   中文的「變成一個……事實」會被聽成「它成了事實」。改成「被當成」就完全貼回來（見 C9）。
   其餘這一章的每一句我都判 CONFIRMED。tg6u「你還會在影片和文章裡看到它」我另外自己證實了：
   N08（NASA 的頁面）、L07、AOP 三頁今天還照寫著「八千萬棵」。

## 第 5 點：五件沒有定論的事，與不能講的事

**五件都是範圍或兩說並列，沒有一件被講成一個答案。** 逐件說：

| 未定論的事 | 腳本怎麼講 | 判定 |
|---|---|---|
| **天體本身** | 大小：tg7a「幾十公尺大的天體」＋卡片「幾十公尺／天體大小」——四個來源給 130 ft／120 ft／164–262 ft／50–100 m，旁白沒有挑一個。性質：tg7v「石質小行星還是彗星碎片，還在爭論」，兩說並列，沒有採用 N115 的「多數科學家偏小行星」當定論 | 兩說並列 ✓ |
| **能量** | tg7k「三百萬噸到三千萬噸都有人算過」（＝3–30 百萬噸，查核檔指定的範圍），tg7l「有模擬把它往低的一端壓，到現在還沒有定論」。沒有一句說「是幾百萬噸」 | 範圍＋明說未定論 ✓ |
| **爆炸高度** | tg7c「主流的估計是離地五到十公里」＋tg7e「二〇一九年的一次模擬估到十到十四公里」，兩個範圍各唸一次，`how-high` 卡上兩格都有。兩個範圍沒有被併成「五到十四公里」 | 兩個帶出處的範圍 ✓ |
| **切科湖** | tg7n 二〇〇七年「湖底像撞擊坑」／tg7o 二〇〇八年「極不可能」／tg7p 二〇一七年「沉積比那場爆炸老」，tg7q「湖底的事，到現在沒有結論」。沒有說「切科湖就是隕石坑」，也沒有說「切科湖不是」 | 三個帶年份的說法＋明說未定論 ✓ |
| **有沒有人喪生** | tg7s／tg7t 二〇一九年論文「至少三十人／至少三人因此過世」對 tg7u「也有資料只記兩則未經證實的報告」，tg7r「有沒有人喪生，也沒有結論」。沒有「無人傷亡」，也沒有把三人講成確數以外的東西 | 兩說並列＋明說未定論 ✓ |

全檔蓋「未結」也做到了：`still-open` 卡（未結／紀錄到今天還沒有定論）、tg7ad「這份檔案，蓋的是未結」、`outro.data.title`「未結」。
**但片尾卡字 `outro.data.lines[0]`「那個早上掉下來的東西，從來沒有落地」把切科湖那件沒有結論的事講成定論**——這是我在這一點上唯一的異議，寫成 C6。

**查核檔說不能講的，我逐項搜過全檔（旁白、卡片、標題、說明欄、標籤、縮圖、112 個 prompt），結果：**

| 不能講的事 | 全檔命中 | 判定 |
|---|---|---|
| 廣島的倍數（N08 的 185 顆、EB／L07 的約一千倍） | 「廣島」全檔只出現一次，在 tg5d「那是廣島之後寫的」，當一九四六年那篇小說的時間座標用；「原子彈」「一千顆」零次；`typewriter-and-a-blank-sheet` 的 prompt 沒有畫城市 | 沒有出現 ✓ |
| 這種事多久發生一次（N08 三百年／N19 千年尺度／RMG 一世紀／EB 幾百年） | 「三百年」「千年」「一世紀」「幾百年」「多久一次」全部零次。EB 那句「once every few hundred years」與 N19 的「on the order of millennia」我都在頁面上讀到了，稿裡沒有 | 沒有出現 ✓ |
| 一九二九年那張照片（年份、攝影者、授權） | 「1929」「一九二九」零次；`assets[]` 是空陣列、全稿沒有照片卡；「照片」兩個字全檔只出現一次，在 tg1j 場景的 `emotion` 欄「像在描一張老照片」（給配音的語氣提示，不會被唸）；「Krinov」零次 | 沒有出現 ✓ |
| 那個不能引的面積數字（RMG 的 1,287 平方公里，查核檔疑為 800 哩的換算筆誤） | 「1287」「1,287」「一千二百八十七」零次。我今天開了 RMG 頁面確認它確實寫著「1287 square kilometres of forest were flattened」。稿裡的面積只有三個：8,000（一九三三年的假設，掛 BB25）、2,150（量到的，掛 L07）、說明欄的「大約兩千平方公里」（EB）——都不是它。另外 BB25 本身沒有提出自己的面積值，所以也不存在「把評論自己的面積拿來用」的問題 | 沒有出現 ✓ |
| 庫利克的病名 | tg4ab 只到「受傷、被俘，一九四二年四月十四日過世」，與 BSE 的「был ранен и погиб в плену」一致；「斑疹」「傷寒」「病」全檔零次 | 沒有出現 ✓ |
| 目擊者的名字 | 「Semenov」「謝梅諾夫」「Akulina」「阿庫莉娜」「Ivan」「伊凡」全檔零次。tg1b 只說「一間交易站的門廊上，坐著一個男人」；tg1g 只說「埃文基人的帳篷」。APS 給了交易站那人的名字、OSU 給了帳篷那兩人的名字，稿裡一個都沒有 | 沒有出現 ✓ |
| 其他：「證實是小行星」「找到隕石」「切科湖就是隕石坑」「無人傷亡」 | 「證實」全檔只出現在 tg7u 的「未經證實的報告」；沒有任何一句宣稱找到隕石（tg3r、tg4p、tg4q 都是反向）；切科湖三說並列；傷亡兩說並列 | 沒有出現 ✓ |
| 一九三〇年代那些流傳版本的人名（Kazantsev、Shapley、Whipple、Astapovich、Crommelin、Brazo） | 旁白與 prompt 零次（Boslough、Bruno、Longo、Jenniskens 只出現在 `sources[]` 的書目標題裡，與 curio-h01 的做法一致） | 沒有出現 ✓ |

## 改動清單

照查核提示：只寫事實與連帶的地方，不碰風格、順序、節奏；行 id 不變；不加場景、不加句子。每一條我都給了一個長度與現稿相當的替代句。
**我沒有動 `video.json`，請由別人套用。**

### 要改的（事實）

**C1　tg5k（`globe-with-a-thread`）—— 一個沒有來源的細節**
- 改前：「一九七三年，有人提出是一個黑洞穿過地球。」
- 建議：「一九七三年，有人提出是一個小黑洞。」
- 為什麼：BH73 的頁面摘要只寫到「We suggest that a black hole of substellar mass such as those that have been postulated by Hawking could explain many of
  the mysteries associated with the event」，沒有「穿過地球」。L07 只寫「tiny black holes (Jackson and Ryan 1973)」，BT74 的反駁摘要也沒有。
  查核檔與 `claims.md` h30 也都沒有這四個字。這是全稿唯一一個我找不到任何依據的實質細節。

**C2　tg4w（`comet-on-a-glass-plate`）—— 沒有來源，而且跟 tg5g 相衝**
- 改前：「彗星說要解釋的，就是那個沒有坑的問題。」
- 建議（兩案選一）：（a）「彗星說靠的是事後那幾個亮著的晚上。」（b）整句刪掉，tg4x 接上去也通。
- 為什麼：講一九三〇年彗星說的兩個來源給的理由都不是「沒有坑」——APS「a hypothesis supported in part by the glowing skies observed after the blast」、
  EB「On the basis of historical records of significant noctilucent cloud development in the skies over Europe following the event」。
  更要緊的是 L07 明寫「Kazantsev was the first who explained the lack of fragments or impact craters in Tunguska by an explosion in the atmosphere」，
  而本稿自己在 tg5g 就是這樣講的（「最早用在空中爆炸解釋沒有坑的，就是這篇小說」）。留著 tg4w，第四章與第五章會互相打臉。
  （a）案的好處是順便把彗星說與第一章的「夜空都亮著」接起來，兩個來源都撐得住。

**C3　tg1i（`steadying-on-a-pole`）—— 沒有來源的概括**
- 改前：「沒有人說得出剛剛是什麼。」
- 建議：「他們不知道那是什麼。」（改成那兩個人的狀態，OSU 寫了「I was scared, screamed」「They heard a thunderous noise, saw blinding light」）
  或直接刪掉，tg1h 接 tg1j 也通。
- 為什麼：h5 只蓋到帳篷搖晃與人被震倒。L07 的「Nobody considered a link between these phenomena」講的是當時沒有人把夜亮、地震與氣壓紀錄連起來（第二章的事），
  不是目擊者說不出話。現在這一句是全稿的概括斷言，沒有來源。

**C4　tg3q 與 `no-crater.data`—— 一個累計結果被掛在一九二七年**
- 改前：tg3q「方圓一萬五千平方公里之內，沒有一個撞擊坑。」／卡片 kicker「一九二七年的爆心」、sub「一萬五千平方公里之內都沒有」
- 建議：tg3q「到今天，方圓一萬五千平方公里之內都沒有坑。」／卡片 sub 改成「到今天，一萬五千平方公里之內都沒有」（kicker 不動）
- 為什麼：L07 的原句是「have **ever** been found in an area of 15 000 km2」——這是寫到二〇〇七年為止、一個世紀的搜尋結果。
  一九二七年那一趟證明的是**爆心沒有坑**（N115、EB、LH 都只講到這裡），不是有人已經搜過一萬五千平方公里。
  現在卡片的 kicker 把這個數字鎖在一九二七年，是這一版最大的年代併接。

**C5　tg3r（`no-crater`）—— 掉了來源的限定詞**
- 改前：「碎片也沒有。」
- 建議：「大塊的碎片也沒有。」
- 為什麼：L07 的字是「neither **macroscopic** fragments ... have ever been found」。EB 另記「The only likely remains of the object that have been found are
  a few small fragments, each less than a millimetre across」，本稿自己在 tg4q 也講了「後來有人找到一些微小的碎屑」。
  補上「大塊」同時修好兩件事：貼回來源，也解掉與 tg4q 的矛盾。順帶一提，`claims.md` h18 的寫法（「也沒有碎片」）也掉了同一個限定詞，建議一起補。

**C6　`outro.data.lines[0]`—— 把沒有結論的事講成定論**
- 改前：「那個早上掉下來的東西，從來沒有落地」
- 建議：「那個早上掉下來的東西，到今天還沒有找到」
- 為什麼：EO 只說「vaporizing the **vast majority** of the incoming bolide」，EB 記有毫米級碎片，而本集自己在 tg7n–tg7q 把「有沒有碎片砸出切科湖」列為沒有結論
  （G07 說像、C08 說極不可能、R17 說湖更老）。「從來沒有落地」在片尾卡上，是觀眾帶走的最後一句，卻正好否定了本集說沒有結論的那一件事。
  建議案保留了與 tg1n（「那天早上掉下來的東西，到底掉在哪裡？」）的呼應，而且只講紀錄裡有的。

**C7　tg4g（`planks-across-the-peat`）—— 沒有來源的器材細節**
- 改前：「人、木板和幫浦，全部搬進沼澤。」
- 建議：「人和工具，全部搬進沼澤。」
- 為什麼：APS 只寫「when he finally drained one of the bogs」，今天開的頁面沒有一個交代他用什麼抽、有沒有鋪木板；h21 也只掛 APS 那一句。
  木板與手搖幫浦留在 `planks-across-the-peat` 與 `hand-pump-working` 的 prompt 裡沒有問題（那是畫面），但旁白不該當成紀錄講。

**C8　tg3m（`poles-in-a-row`）—— 掉了一個出處**
- 改前：「那片枯樹，後來被人叫做電線桿森林。」
- 建議：「那片枯樹，他叫它電線桿森林。」
- 為什麼：LH 的原句是「he encountered what he called a 'telegraph-pole forest'」——這個說法是庫利克當場自己取的，不是後來別人叫的。
  改成「他叫它」字數相同，而且把這一句從泛稱變成有主的一手說法。（`claims.md` h17 的「後來被叫做」同樣要跟著改。）

**C9　tg6t（`no-footnote-left`）—— 掉了「好像是」這個鉤子**
- 改前：「抄到後來，它變成一個不用附出處的事實。」
- 建議：「抄到後來，它被當成不用附出處的事實。」
- 為什麼：BB25 的字是「has propagated into other sources **as if it were** an established fact that needs no citation」。
  「變成一個……事實」中文會被聽成「它成了事實」；「被當成」正好是「as if it were」。
  後面 tg6v 雖然補了「這一集不會把它當事實講」，但第六章的主題就是這個數字不是事實，這一句不該留下任何讀成相反意思的空間。

**C10　`sources[]`—— 說明欄答應的事沒有兌現**
- 現狀：說明欄寫「每個數字、年份與引述的出處列在下方參考資料」，但 `sources[]` 只有 12 筆，而 `claims.md` 另外靠 10 個來源撐著旁白：

| 要補的來源 | 它在稿裡撐的是哪幾句 | 我今天拿到的 HTTP |
|---|---|---|
| OSU https://origins.osu.edu/milestones/june-2018-1908-tunguska-event-and-threats-tomorrow | tg2c（舊曆六月十七日）、tg1g／tg1h、tg2q、tg4o／tg4p、tg5c／tg5d、tg5h、tg5p | 200 |
| LH https://www.lindahall.org/about/news/scientist-of-the-day/leonid-kulik/ | tg2p（生日）、tg2x（六年後）、tg3m（電線桿森林）、tg3o | 200 |
| BSE https://booksite.ru/FullText/1/001/008/067/252.htm | tg4aa、tg4ab（卒日一九四二-〇四-一四） | 200 |
| AOP https://armagh.space/weather/history/tunguska-event | tg7u（兩則未經證實的報告）、tg7v（彗星碎片這個講法） | 200 |
| Commons https://commons.wikimedia.org/wiki/File:1908-07-29-SibirskayaZshizn-135.jpg | tg2b（七月十二號、十二天） | 200 |
| G07 存檔 https://web.archive.org/web/20230211163937/https://onlinelibrary.wiley.com/doi/10.1111/j.1365-3121.2007.00742.x | tg4b、tg4c、tg4k、tg7n | 200 |
| C08 存檔 https://web.archive.org/web/20230210215017/https://onlinelibrary.wiley.com/doi/10.1111/j.1365-3121.2008.00791.x | tg7o | 200 |
| AM65 https://www.nature.com/articles/206861a0 | tg5j | 200 |
| BH73 https://www.nature.com/articles/245088a0 | tg5k | 200 |
| BT74 https://www.nature.com/articles/250555a0 | tg5m | 200 |

- 建議：把這十筆加進 `sources[]`（`checked_on` 填 `2026-10-10`，與現有 12 筆一致——這十個網址我 2026-10-13 也全部重開，都是 200）。
  不加的話，說明欄那一句要改成「主要出處列在下方」。curio-h01 的 `sources[]` 有 18 筆、涵蓋它用到的每一個來源，這一集只列了一半多。

**C11　tg2c（`two-calendars-side-by-side`）—— 指涉含糊，錯的那個讀法會得到錯的數字**
- 改前：「俄國當時用的是舊曆，那天寫的是六月十七日。」
- 建議：「俄國當時用的是舊曆，那個早上寫的是六月十七日。」
- 為什麼：數字沒錯（OSU：「June 30, 1908 (June 17 according to the Russian calendar at the time)」），但這一句緊接在 tg2b 的「報紙是七月十二號出的」之後，
  「那天」會被聽成報紙那一天——而報紙那一天的舊曆是**六月二十九日**（Commons 的 Source 欄「29 июня (старый стиль)」）。
  改成「那個早上」把指涉釘回爆炸那天，字數只多一個。

**C12　tg2k（`tent-flap-half-closed`）—— 不願意談的對象不見了（低，撰稿方可自行判斷）**
- 改前：「爆心附近的埃文基人，起初不願意談這件事。」
- 建議：「後來去問的人，起初問不出話。」或「爆心附近的人，起初不願意跟外人談。」
- 為什麼：N08 的原句是「At first, the locals were reluctant to tell **Kulik** about the event」——不願意談的對象是庫利克，時間是一九二七年以後。
  這一句排在庫利克出場（tg2o，一九二一年）之前，會被聽成一九〇八年當下他們就不肯講。
  （「埃文基人」代「the locals」我查過沒問題：N115「the few reindeer herders of the local Evenki people」、APS「mostly indigenous Evenki natives」。問題只在時間與對象。）

### 有主張但沒有列進 `claims.md` 的（請補對應表，不必改旁白）

**C13　tg7b（`rock-against-the-sky`）「它衝進大氣，在半空中炸開。」**
這是本集的主線事實，卻沒有任何一列蓋到它（h34 蓋高度、h36 蓋衝擊波與氣化，場景清單裡都沒有 `rock-against-the-sky`）。
事實本身我判 CONFIRMED：EO「an object ... plunged into Earth's atmosphere, creating a brilliant fireball that exploded over a remote part of Siberia」、
N115「an asteroid plunged into Earth's atmosphere and exploded in the skies over Siberia」。請把 `rock-against-the-sky` 加進 h34 或 h36 的場景清單。

**C14　tg4x（`comet-on-a-glass-plate`）「這個說法一直留到今天。」**
h27 只蓋到一九三〇年與「誰先提的不一致」。事實 CONFIRMED：EB 兩說並列、AOP「Some argue that it was a small asteroid, others that it must have been a
small comet (or a comet fragment)」。請把它掛到 h27 或 h40。

**C15　tg5a「他過世四年後」**
一九四二→一九四六的算術，沒有列在 `claims.md` 的算術清單裡（清單有十二天、十三年、六年後、二十一年、九十幾年後、一百一十八年）。數字正確，請補上。

**C16　三個場景不在主張表也不在豁免名單**
`looking-up-from-the-ground`（tg1n 章末問句）、`rail-ends-at-the-forest`（tg2m 敘事收攏；tg2n 的十三年已在算術清單）、
`rock-against-the-sky`（見 C13）。前兩個請加進〈不是來源主張的句子〉那一節，第三個要加主張列。

## 附註（我懷疑但沒有要求改的）

- **tg5n「剛剛那位研究者寫得很直接」**：L07 那一句是被動的「**were found to be** technically groundless」（他在轉述別人的判定），
  但同一段他接著用自己的話說「Nevertheless, I think that here we can ignore such extremely 'non-traditional' hypotheses」。
  把「直接」掛在他身上讀得通，保留。
- **tg7aa「很多人第一次親眼看到空爆」**：N19 的原句只到「This highly documented fireball created an opportunity for researchers」，
  沒有寫「第一次有人親眼看到」。這是查核檔〈給撰稿的提醒〉的原話（「2013-02-15 車里雅賓斯克讓人親眼看到空爆」），照它寫了，保留；第二輪可再看。
- **說明欄的「大約兩千平方公里」對旁白的「兩千一百五十平方公里」**：兩個都有來源（EB 對 L07），兩個都帶「大約」，`claims.md` 也解釋了為什麼分開用。
  不是錯，但同一集的兩個入口給觀眾兩個面積數字，記在這裡。
- **tg7p**：R17 的結論其實比旁白強（「Cheko Lake is significantly older than the 1908 Tunguska Event; therefore, the lake basin cannot be a crater」），
  旁白只講「沉積比那場爆炸老」，講得比來源少，沒有問題。
- **prompt 的兩處（說明欄「在世或近代人物不入畫」）**：
  `names-on-a-tally`（代二〇一九年那篇論文的研究者）寫的是「Medium shot of a researcher in a plain cardigan at a desk」，沒有寫背影，可能會畫到臉；
  同一條線上的 `reviewer-at-two-screens`（代二〇二五年的評論作者）寫了「from behind」、`book-chapter-open` 與 `pen-across-a-paragraph` 只拍書與手，處理得更乾淨。
  另外 `faces-turned-up`（二〇一三年車里雅賓斯克的路人）直接寫了「their faces turned up and their mouths open」。
  兩處都是沒有名字的泛稱人物，不在查核檔「不畫臉」的名單上，所以我沒有列成要改的事，但說明欄自己許下的承諾在這兩格最緊，交給撰稿方決定。
- **BO 與 RMG**：查核檔說這兩頁也照寫「八千萬棵」。我今天開了兩頁，BO 是框架選單頁、取不到正文，RMG 的正文裡我沒有找到棵數（它寫的是 1,287 平方公里）。
  tg6u「你還會在影片和文章裡看到它」靠 N08、L07、AOP 三頁就撐得住，不影響判定，但這兩筆與查核檔的記載有落差，記在這裡。
- **我沒有跑 `lint`**：啟動說明要我不跑影片階段，所以這一輪沒有單位數、句數與時長可報。最長的旁白句是 tg2a（27 個中文字），
  聽眾檢查（24 單位、沒有括號與網址、沒有「經查證」之類的字）請在套用上面的改動後由撰稿方跑一次 `lint` 確認；
  上面每一個建議句我都刻意寫得與現稿字數相當或更短，`stats`／`compare` 卡上的數字我一個都沒有動，所以不會有 `say`／`say_for` 要補。

## 摘要

- 抽出 209 條主張（旁白 158 句、卡片 `data` 欄 20 個、標題 1、說明欄 5 段、標籤 1 組、縮圖 4 欄、`sources[]` 12 筆、`loops[]` 5 筆），
  合併重複後成 131 列：**CONFIRMED 105、CHANGED 9、NOT FOUND 4、OUT OF SCOPE 13**。
- CHANGED 的 9 列對應 9 個要改的地方（C1–C12 裡的事實類共 12 條，其中 C1／C2／C3／C7 判 NOT FOUND、C4 牽動一句旁白與一張卡片）。
- 第 4 點：**過關。** 「八千萬棵樹」從頭到尾只當流傳的數字講，標題、標籤、縮圖與六張卡片都沒有棵數；
  來歷掛在一九三三年一次為估能量的粗估、面積高估約四倍；「四分之一」是 BB25 自己的「factor of about four」的倒數，不是本稿的算術；
  引用鏈（一九三三→一九三四兩篇，其中一篇是通信者的話→一九八二→照抄）逐條對得上 BB25。唯一要改的是 tg6t 掉了「as if it were」（C9）。
- 第 5 點：**五件未定論的事全部是範圍或兩說並列，一件都沒有被講成一個答案**；查核檔點名不能講的七類（廣島倍數、多久一次、一九二九年那張照片、
  那個疑為筆誤的面積數字、庫利克的病名、目擊者的名字，以及「證實是小行星／找到隕石／切科湖就是隕石坑／無人傷亡」）全檔零命中。
  唯一的異議是片尾卡字把切科湖那件沒有結論的事講成了定論（C6）。
- 沒有主張撐著的句子：tg1i（C3，建議改或刪）、tg4g 的器材細節（C7）、tg4w（C2）、tg5k 的「穿過地球」（C1）；
  另有 tg7b、tg4x、tg5a 三處事實站得住但 `claims.md` 沒有列（C13–C15），以及三個場景不在主張表也不在豁免名單（C16）。
- 會過期的事實：沒有。看到的頁面日期：N115 2023-06-30、N19 2019-06-26、N08 存檔 2021-01-01、EB 存檔 2026-09-01、
  L07 2007（Springer 專書章）、BB25 2025（Scientific Reports 15:13869）、SNL 2007-12-17、R17 2017-11-04、J19 2019-07、APS 2018-06。
- 程序：沒有跑 git，沒有跑任何影片階段（含 `lint`），沒有花供應商的錢，沒有改 `video.json`／`claims.md`／`brief.md`／`NOTES.md`。
  所有中間檔在 `<tmp>\scratchpad\verify-h03\`（`extract.txt`、`assertions.tsv`、`http-status.json`、`pages\`、`text\`）。
- **第二輪：需要**（這一輪有 9 列 CHANGED、4 列 NOT FOUND，遠超過 3 個事實）。第二輪請換人，重查 C1–C12 這十二條，
  再隨機抽三分之一的 CONFIRMED；特別請再看一次 C4（一萬五千平方公里的年代）與 C6（片尾卡字），這兩條改到了觀眾最記得的兩個位置。
