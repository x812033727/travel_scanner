# curio-s24-v2 查核第二輪（2026-11 重做稿）

- **查核日期**：2026-11-11。查核者沒有參與撰稿。
- **範圍**：`video.json` 的 `scenes[].lines[].text`，共 132 句（ek001–ek132）、114 景（`say` 只管讀音，沒有查），加上 `youtube.title` 與 `youtube.description` 裡的事實。
  另外查了 `curio-redo-handoff/drafts/curio-s24-v2/changes.md` 的〈【待查】〉一節：它寫「沒有新事實，0 條」，下面列了 7 處「換算、改寫或推論」要查核方看（ek005、ek018、ek017、ek095、ek128、ek129、ek003）。
  這 7 處就是這次重新綁定的句子，逐條判定如下。（`video.json` 和草稿資料夾那份只差 `target_minutes`、`music`、`pauses`、`still_motion`，台詞一字不差。）
- **方法**：逐句看人名、年份、數字、引號裡的話、誰說的、事件順序，以及「最早」「從來」「一定」「跑」「才是」這類強詞，對照 `claims.md`、`verify-1.md`（第一版查核加獨立覆核，44 列）、`brief.md`、`NOTES.md`。
  注意：`claims.md` 還是舊編號（ek101–ek722），這次的 ek001–ek132 是照句子內容對回去的。這次沒有只照抄前一份，`video.json` 的 `sources` 列的固定文本，抓得到的都**重新抓下來逐字核對**：
  - VIT-LAT＝維特魯威第九書序與第一書序（LacusCurtius）：https://penelope.uchicago.edu/Thayer/L/Roman/Texts/Vitruvius/9*.html 、…/1*.html
  - PLUT-NP 希臘原文＝PerseusDL `tlg0007.tlg139.perseus-grc2.xml`（canonical-greekLit master）
  - HEATH＝archive.org `worksofarchimede00arch` 的全文 OCR（`_djvu.txt`）
  - CARMEN＝archive.org `bub_gb_d4urIMWhWWYC`（Hultsch 第 2 冊）的全文 OCR，pp. 95–96
  - GAL-FAV＝it.wikisource「Pagina:Le opere di Galileo Galilei I.djvu」第 214–215 頁（Avvertimento，原始碼）；《小天平》正文與英譯用 Rorres 的頁面
  - RORRES＝https://math.nyu.edu/Archimedes/Crown/CrownIntro.html 、…/bilancetta.html ，另外加開 …/magick.html （德拉波爾塔；**不在 `sources` 裡**）
  - SCIAM＝scientificamerican.com 那篇（datePublished 2006-12-08，作者 David Biello）
  - EB1911＝en.wikisource 第 28 冊 p. 166（只核了「is dedicated to Augustus」那一句）
  - PLUT-MARC＝LacusCurtius 的《馬塞盧斯傳》英譯（**不在 `sources` 裡**）
  - 沒有重開、**沿用 verify-1** 的：SMITH〈Nudus〉、WP〈On Floating Bodies〉（重寫本）、WP〈Archimedes〉、WP〈De architectura〉（成書年代）、Morgan 英譯（只當旁證）。
- **結論摘要**：主幹沒有問題。維特魯威的拉丁原文（偶然、澡堂、往家裡、「據說」、量器、揭穿為止）、普魯塔克的希臘原文（ὥς φασιν、沒有 γυμνός、沒有回家、ἐβάδιζεν）、拉丁詩（沒點名、沒有浴池、水中天平）、
  伽利略（1586、只給朋友看、「molto grossa e lontana dall'esquisitezza」、「有些人寫的」、那個時代的作家補的）、Rorres 的數字（1000 g、20 cm、30%、0.41 mm、13.0 g、714 g）和 SCIAM 的兩句引語，都逐字對得上。verify-1 的但書（不說是假的、普魯塔克沒光身子沒回家、走不是跑、二十出頭、三顆骰子、替奧古斯都管弩炮、不提 Proclus 和加州）全部守住了。**要改 6 句**：
  - vitr-who（ek008）「最早寫下這一幕的，**是**維特魯威」：只能說「目前找得到最早」。片子自己在 ek093 還引了伽利略的猜測，說是「那個時代」的作家先寫下來的。
  - vitr-200（ek011）「從阿基米德的**時代**算」：那將近兩百年是從他**過世**（前 212 年）算的。從他在世的時候算會超過兩百年。
  - how-prove（ek041）「那他**回到家之後**，要怎麼證明？」：原文只寫他「往家裡去」，實驗在哪裡做的沒有寫。
  - oil-draw（ek076）「普魯塔克在另一本書裡還寫，他常被人硬拖去洗澡抹油」：普魯塔克的原文是「關於他的那些傳聞」，旁白要保留這個「據說」。
  - reverse（ek079）「有浴池，沒提光身子；那有沒有**反過來**的版本？」接「有」：拉丁詩是沒浴池、**也沒光身子**，不是反過來，邏輯對不上。
  - half-half（ek128）「查得清的，是**誰在哪一年**寫了什麼」：拉丁詩不知作者也不知年代，維特魯威和普魯塔克的年份也只有大概，「誰在哪一年」查不清。
- changes.md 那 7 處：ek005、ek017、ek018、ek095 **通過**；ek003、ek129 **通過但記一筆**；ek128 **要改**（見上）。
- `youtube.description`：**不用改**，每一句都對得上（「目前找得到最早的文字」已經寫了「目前」）。`youtube.title`「最早的紀錄晚了將近 200 年」記一筆：標題要短，可以照用，因為說明欄第一段已經補上「目前找得到」。

## 判定表

| 景 id（句 id） | 句子（原文） | 判定 | 依據 | 建議改法 |
| --- | --- | --- | --- | --- |
| vitr-who（ek008） | 最早寫下這一幕的，是一位羅馬建築師，叫維特魯威。 | 要改 | verify-1 #1 備註：「這是就**流傳到今天**的文獻而言……旁白說『目前找得到最早』，不說『第一個講的人』」。SCIAM（重抓）：「The oldest authority for the naked-Archimedes eureka story is Vitruvius」，說的是 oldest authority（現存最早的出處），不是第一個寫的人。片子自己在 ek093 引伽利略（Rorres 頁面，重抓）：「some author of that time may have then left a written record of this fact」，也就是猜有更早的作家寫過。這句把「最早寫下的人」說死了，跟 ek093 打架 | 目前找得到最早寫下這一幕的，是一位羅馬建築師，叫維特魯威。 |
| vitr-200（ek011） | 從阿基米德的時代算到這裡，就是開頭說的那將近兩百年。 | 要改 | verify-1 #18：「從阿基米德之死算約 180–200 年」（212−30＝182；212−15＝197）；「如果王冠事件真發生在希倫『剛稱王』時……距離還要更久」。SCIAM：「nearly 200 years after the event is presumed to have taken place」。「時代」包括他在世的幾十年，從那時候算就會超過兩百年 | 從阿基米德過世算到這裡，就是開頭說的那將近兩百年。 |
| how-prove（ek041） | 那他回到家之後，要怎麼證明？ | 要改 | VIT-LAT praef. 10–11（重抓）：「nudus vadens domum versus」（往家裡去）之後，接「tum vero ex eo inventionis ingressu duas fecisse dicitur massas」（「從這個發現起步，據說他做了兩塊……」）。原文沒寫他到家了，也沒寫實驗在哪裡做。問句裡夾了原文沒有的事 | 那他接下來，要怎麼證明？ |
| oil-draw（ek076） | 普魯塔克在另一本書裡還寫，他常被人硬拖去洗澡抹油， | 要改 | PLUT-MARC 17.6（LacusCurtius，重抓）：「And therefore we may not disbelieve the stories told about him, how … when he was dragged by main force, as he often was, to the place for bathing and anointing his body, he would … draw lines with his finger in the oil」。普魯塔克是把它當成「關於他的傳聞」轉述的，站主規則要保留原文的「據說」。（另外，同一段在《Non posse》裡也有，就在浴缸故事前面一句，Perseus 重抓：「Ἀρχιμήδην δὲ βίᾳ τῶν διαγραμμάτων ἀποσπῶντες ὑπήλειφον οἱ θεράποντες· ὁ δʼ ἐπὶ τῆς κοιλίας ἔγραφε τὰ σχήματα τῇ στλεγγίδι」，那一版是用刮身板畫在肚子上，不是手指沾油。所以「另一本書」配「手指、油裡」沒錯。）PLUT-MARC 不在 `sources` 裡 | 普魯塔克在另一本書裡還記了一則傳聞：他常被人硬拖去洗澡抹油， |
| reverse（ek079） | 有浴池，沒提光身子；那有沒有反過來的版本？ | 要改 | 下一句 ek080 回答「有。」，指的是拉丁詩。CARMEN vv. 125–140（Hultsch pp. 95–96 OCR，重抓）有國王、金冠、工匠、水中天平，**沒有浴池，也沒有光身子**（verify-1 #28「詩裡沒有浴缸、沒有裸奔、沒有 εὕρηκα」）。「反過來」照字面是「沒浴池、有光身子」，跟詩對不上。brief 的原意是「普魯塔克有浴池，詩有金冠沒浴池」 | 有浴池，沒提光身子；那有沒有連浴池都沒有的版本？ |
| half-half（ek128，changes #5） | 查得清的，是誰在哪一年寫了什麼；回答不了的，是那天到底發生了什麼。 | 要改 | 片中五份紀錄，「誰」和「哪一年」大多查不清：拉丁詩「不知道作者」，年代 verify-1 #29、#42「十九世紀就沒定論」（Hultsch「rem in medio relinquo」）；維特魯威只到「西元前一世紀後期」（#14 確切年份 DISPUTED）；普魯塔克只有「一百多年後」（二手）。只有伽利略 1586、德拉波爾塔 1589 有年份。brief〈站主觀點〉的原話是「把『誰寫的、哪一年、寫了什麼、沒寫什麼』說清楚」，但當結論說成「查得清」太滿了 | 查得清的，是每一份紀錄寫了什麼、沒寫什麼；回答不了的，是那天到底發生了什麼。 |
| open-bath、open-run（ek001–ek002） | 你一定聽過這個故事：阿基米德坐進浴池……／他高興得光著身子衝上大街，一路大喊 Eureka，意思是：我找到了。 | 通過 | 用「你一定聽過」框住，講的是流傳的版本；verify-1 #8 WP〈Archimedes〉「took to the streets naked, having forgotten to dress」。ek033–ek035 有更正。「我找到了」＝VIT-LAT「invenisse quod quaereret」 | — |
| open-you（ek003，changes #7） | 這一幕你可能從小聽到大。可是你想不到，最早寫下它的字，離他已經將近兩百年。 | 通過（記一筆） | 「從小聽到大」是對觀眾的說法，加了「可能」，也沒提課本（NOTES 的提醒）。「最早寫下它的字」跟舊 ek102 一樣，verify-1 通過；照 #1 嚴格講要加「目前找得到」。如果 ek008 照改，這句可以不動；要一起收緊的話：「可是你想不到，目前找得到最早寫下它的字，離他已經將近兩百年。」 | （可選）見依據欄 |
| open-tease-plut（ek004） | 更怪的是，一百多年後又有人寫這場澡，卻少了一樣東西。 | 通過 | verify-1 #24 WP「a century later by Plutarch」（二手）；Perseus 1094C 沒有 γυμνός | — |
| open-tease-gal（ek005，changes #1） | 再過一千多年，一個二十出頭的年輕人讀到這方法，開頭就下了重話。 | 通過 | 換算：普魯塔克約西元一世紀末到二世紀初（「晚維特魯威一百多年」），到 1586 年約 1,450–1,500 年，「一千多年」成立。「二十出頭」照 #31 覆核（1564 年 2 月生，1586 年 21 或 22 歲）。「讀到這方法」：GAL-FAV Avvertimento（重抓 p. 211）說他讀到「quel passo … nel quale si narra il modo」（講這方法的那一段）；沒說讀的是維特魯威，旁白也沒說 | — |
| open-promise、open-route（ek006–ek007） | 今天我們就來聊聊……／我們把寫過這場澡的紀錄，照年代一份一份翻開：五份古書，一個算式。 | 通過（記一筆） | 承諾句與路線圖。「五份古書」大概是指維特魯威、阿基米德自己的書、普魯塔克、拉丁詩、伽利略（德拉波爾塔算第六份）。其中阿基米德的書和拉丁詩都沒寫「這場澡」，片子後面自己就這樣講；伽利略 1586 年的短文也稱不上「古」書。這是包裝的說法，不算事實錯誤 | — |
| vitr-shelf（ek009） | 他還替奧古斯都管過弩炮，是個軍事工程師。 | 通過（記一筆） | VIT-LAT I praef. 2（重抓）：「cum autem concilium caelestium … imperium parentis in tuam potestatem transtulisset, idem studium meum … in te contulit favorem. itaque cum M. Aurelio et P. Minidio et Gn. Cornelio ad apparationem ballistarum et scorpionum reliquorumque tormentorum refectionem fui praesto」。是在奧古斯都手下，照 #13 覆核。原文說他和另外三人一起負責；「管過」可以接受 | — |
| vitr-augustus（ek010） | 他寫了一套《建築十書》，獻給奧古斯都，寫在西元前一世紀後期。 | 通過 | I praef. 1「imperator Caesar」；EB1911 p. 166（重抓）「The treatise De Architectura Libri Decem is dedicated to Augustus.」；年代照 #14 只說「前一世紀後期」 | — |
| vitr-source（ek012–ek013） | 那這個故事，他是從哪裡聽來的？／書裡一個字也沒說。 | 通過 | #1 備註「維特魯威自己沒說故事從哪裡聽來」；IX praef. 9 只寫「id quod exponam」 | — |
| hiero-king、hiero-vow（ek014–ek015） | 故事在第九書的開頭。敘拉古的國王希倫，統治了這座城半個多世紀。／剛掌王權那年，他立誓把一頂金冠獻進神廟。 | 通過 | IX praef. 9「Hiero Syracusis auctus regia potestate … auream coronam votivam diis inmortalibus in quodam fano constituisset ponendam」。不給年份，照 #19；Rorres 頁面圖說「Hiero II 306?-215 BC」。「那年」是口語，原文是「剛取得王權之後」 | — |
| wreath（ek016） | 說是金冠，其實是一圈金葉子做的花環；你腦中那頂鑲寶石的王冠，可以先放下。 | 通過 | RORRES Intro（重抓）：「The crown (corona in Vitruvius's Latin) would have been in the form of a wreath」 | — |
| wreath-remember（ek017，changes #3） | 先記住這頂花環：接下來好幾份紀錄，都會繞回它身上。 | 通過 | 普魯塔克「τὴν τοῦ στεφάνου μέτρησιν」、拉丁詩「coronam」、伽利略「la corona d'oro di Ierone」、德拉波爾塔「a golden Crown」、Rorres「Hiero's wreath」都講到它；阿基米德自己的書沒有，所以用「好幾份」不用「每一份」，對 | — |
| gold-weighed、delivered（ek018–ek019，changes #2） | 國王按重量，把金子交給工匠，請他照這個重量打造花環；／交件那天……一秤，重量分毫不差。 | 通過（記一筆） | IX praef. 9：「manupretio locavit faciendam et aurum ad sacoma adpendit redemptori. is ad tempus opus … regi adprobavit et ad sacoma pondus coronae visus est praestitisse」。「照這個重量打造」是把「locavit faciendam」（發包打造）和交件時「ad sacoma pondus … praestitisse」（照定重交出）合起來講的，成立。「分毫不差」對 Morgan「corresponded precisely」；原文是「visus est」（看起來相符），反正騙局本來就是看起來沒問題，不改 | — |
| accused、cannot-melt、ask-arch（ek021–ek023） | 有人告發……／偏偏那是要獻給神的東西，熔不得，也刮不得。／國王氣歸氣…… | 通過 | IX praef. 10「indicium est factum dempto auro tantundem argenti … admixtum esse, indignatus Hiero … neque inveniens qua ratione id furtum deprehenderet, rogavit Archimeden」。ek022 是 Rorres 的詮釋（重抓：「because the wreath was a holy object dedicated to the gods, he could not disturb the wreath in any way」），加上詩的「inlaeso」；維特魯威沒寫 | — |
| bath-door、basin-edge（ek024–ek025） | 就在這時候，他偶然走進公共澡堂，心裡正掛著這件難事。／他往浴池裡一坐…… | 通過 | IX praef. 10「tunc is cum haberet eius rei curam, casu venit in balineum ibique cum in solium descenderet, animadvertit quantum corporis sui in eo insideret tantum aquae extra solium effluere」 | — |
| he-sees、same-weight（ek027–ek028） | 漫出來的水，讓他看出了揭穿的辦法：／東西放進水裡，排開多少水，它就有多大；一樣重的金和銀，大小不一樣。 | 通過 | praef. 10「idque cum eius rei rationem explicationis ostendisset」；praef. 12「quanto minus magno corpore eodem pondere auri massa esset quam argenti」；Rorres 的密度與體積計算 | — |
| jump-out、eureka（ek029–ek031） | 他一刻也沒等，高興得從浴池跳了出來，／光著身子，往家裡去；一邊跑，一邊大聲喊：／Eureka，Eureka！ | 通過 | praef. 10「non est moratus sed exsiluit gaudio motus de solio et nudus vadens domum versus … nam currens identidem graece clamabat ευρηκα ευρηκα」。「跑」對 currens | — |
| home-lane、from-bathhouse（ek033–ek034） | 它寫的是「往家裡」，沒有寫上街；／從公共澡堂往家裡跑，不是從自己家的浴缸跑出門。 | 通過 | 「domum versus」；balineum 是澡堂（#6） | — |
| later-added、your-version（ek035–ek036） | 「忘了穿衣服」「跑遍大街」，都是後來的人一層一層加上去的。／你小時候聽到的那個滿街跑的版本，就是這樣加出來的。 | 通過 | 維特魯威原文沒有這兩樣；後人的轉述有：HEATH p. xix（重抓 OCR）「he ran naked through the street to his home」；WP〈Archimedes〉「having forgotten to dress」（#8，沿用）。「一層一層」是旁白的比喻 | — |
| nudus-word、nudus-literal（ek038–ek039） | 原文用的拉丁字，有時也指只穿一件短衣；／照字面讀，最自然的意思就是光著。 | 通過（沿用 verify-1，未重開 SMITH） | #9 SMITH「wore only his tunic」；覆核「照字面讀成『光著』比較自然」，沒有拿字義暗示他有穿 | — |
| how-prove、vessel、pour-back（ek042–ek044） | 維特魯威接著寫，而且自己先加了兩個字：據說。／據說他做了兩塊……／再用一個羅馬的量器，一杯一杯量…… | 通過 | praef. 11「duas fecisse dicitur massas aequo pondere quo etiam fuerat corona … vas amplum ad summa labra implevit aqua … refudit sextario mensus」。「兩個字」是中文「據說」兩個字，原文是 dicitur 一個字 | — |
| caught、smith-fate（ek045、ek048） | 花環排開的水，比同樣重的金塊多……／原文沒寫，故事就停在這裡。 | 通過 | praef. 12「invenit plus aquae defluxisse in coronam quam in auream eodem pondere massam … deprehendit argenti in auro mixtionem et manifestum furtum redemptoris」，到這裡就停了 | — |
| vitr-protest、athlete、one-example（ek050–ek052） | 第九書的開頭……替作家抱不平／運動員得到的榮耀，作家也該有，而且要更多。／前一個例子是畢達哥拉斯。 | 通過 | IX praef. 1–2（重抓）「admiror quid ita non scriptoribus eidem honores etiamque maiores sint tributi … quod athletae sua corpora exercitationibus efficiunt fortiora」；praef. 3「e pluribus singula paucorum uti exempla ponam」；praef. 6–8 畢達哥拉斯，緊接 praef. 9「Archimedis vero」 | — |
| arch-works（ek054） | 至少在他流傳到今天的著作裡，一個字也沒提到王冠，也沒有浴缸。 | 通過（記一筆） | HEATH 全文 OCR（重抓）檢索「crown」：只出現在 Heath 的導論 p. xix 與命題 7 後的編者註；「bath」只在導論。SCIAM（重抓）「Archimedes himself never wrote about this episode」。限制同 #20：1906 年後才找到的《方法》不在 Heath 1897 本裡，這次也沒有逐本查；靠 SCIAM 撐「流傳到今天」 | — |
| heath-desk、heath-page（ek055–ek057） | 一八九七年，英國學者希斯編了他的英文全集；／他手上的《浮體論》，只有拉丁譯本。／「王冠」只出現在編者自己的導論和註裡。 | 通過（記一筆） | HEATH（重抓）：「περὶ ὀχουμένων, the Greek title of the treatise On floating bodies, only preserved in a Latin translation」。「王冠」的位置同上。「全集」偏滿：Heath 書名是 *The Works of Archimedes*，收了 1897 年當時知道的全部著作，1912 年才補《方法》。說「英文全集」不算錯；要更穩可以說「英文的著作集」 | （可選）一八九七年，英國學者希斯編了他的英文著作集； |
| lost-kept、palimpsest（ek058–ek059） | 他寫過的書，有的失傳了……／《浮體論》的希臘原文，是後來才在一本被刮掉重寫的羊皮書裡找回來的。 | 通過（沿用 verify-1，未重開 WP） | #23 HEATH 導論「Lost works」；WP〈On Floating Bodies〉「the only known copy … in Greek comes from the Archimedes Palimpsest」（二手）；不講年份 | — |
| floating-book、prop7、weigh-in-water、volume-not（ek060–ek064） | 比水重的東西，放進水裡秤，會變輕；輕掉的，正好是它排開的那些水的重量。／……比的卻是體積，不是這本書裡的道理。 | 通過 | HEATH Prop. 7（重抓 OCR）「A solid heavier than a fluid will … when weighed in the fluid, be lighter than its true weight by the weight of the fluid displaced」；RORRES Intro「it does not make use of Archimedes' Law of Buoyancy or his Law of the Lever」 | — |
| plutarch、plut-hearsay（ek067–ek068） | 開頭說的那個再晚一百多年的版本，出自希臘作家普魯塔克。／他下筆前自己先加了「據說」：到他那時候，這已經是大家在傳的故事。 | 通過 | Perseus 1094C（重抓）「λουόμενος ὥς φασιν」（「據他們說」）；「大家在傳」是 ὥς φασιν 的直接意思，#24 備註也這樣推。年代差是二手 | — |
| plut-bath、plut-leap（ek069–ek070） | 據說阿基米德洗澡時，從溢出來的水，想到怎麼量那頂冠；／像被什麼附了身，跳出來大喊「我找到了」，一路喊著，走了。 | 通過 | Perseus 1094C（重抓，逐字）：「ἐκ τῆς ὑπερχύσεως ἐννοήσας τὴν τοῦ στεφάνου μέτρησιν οἷον ἔκ τινος κατοχῆς ἢ ἐπιπνοίας ἐξήλατο βοῶν εὕρηκα, καὶ τοῦτο πολλάκις φθεγγόμενος ἐβάδιζεν」。沒用英譯加的希倫、金子比例、bathing-stool | — |
| plut-dinner（ek071） | 他講這段，是為了挖苦愛吃的人：從來沒聽過哪個饕客吃完一頓，大喊「我吃到了」。 | 通過（記一筆） | Perseus 1094C（重抓）「οὐδενὸς δʼ ἀκηκόαμεν οὔτε γαστριμάργου περιπαθῶς οὕτω βέβρωκα βοῶντος οὔτʼ ἐρωτικοῦ πεφίληκα」。「從來沒聽過」對 οὐδενὸς ἀκηκόαμεν。他挖苦的對象嚴格講是把肉體享樂看得最重的伊比鳩魯派（這篇的題目就是反駁伊比鳩魯），同一句也挖苦了「我親到了」的情人；「愛吃的人」是簡化的說法，可以照用 | — |
| plut-shrug、plut-walk（ek074–ek075） | 衣服的事，普魯塔克一個字也沒提；／也沒說他往家裡去；他用的字，是「走」，不是「跑」。 | 通過 | 1094C 沒有 γυμνός、沒有 οἴκαδε；ἐβάδιζεν（#41）。只說「沒提」，沒說「證明他沒光著」 | — |
| oil-draw（ek077） | 手指還在身上的油裡畫幾何圖。 | 通過 | PLUT-MARC 17.6「draw lines with his finger in the oil with which his body was anointed」（「據說」加在 ek076） | — |
| plut-guess（ek078） | 難怪這個故事安在他身上這麼順，這是我的猜想。 | 通過 | 推論，已標「我的猜想」，用「難怪」不用「所以」（#26） | — |
| poem、poem-smith、poem-missing（ek080–ek083） | 羅馬帝國晚期，一首不知道作者的拉丁詩，講的顯然是同一個故事：／西西里的國王、獻給神的金冠、偷摻了銀的工匠，都在；／可是沒有浴池……／只說是「敘拉古的大師」。 | 通過 | CARMEN（重抓 OCR，Hultsch p. 95）：「prima Syracusi mens prodidit alta magistri. regem namque ferunt Siculum quam voverat olim caelicolum regi ex auro statuisse coronam, conpertoque dehinc furto — nam parte retenta argenti tantundem opifex immiscuit auro」；年代不給世紀（#29、#42） | — |
| poem-balance、poem-sink（ek084–ek085） | 兩邊放上等重的金和銀，秤平了，再一起放進水裡；一進水，放金子的那一邊，馬上沉了下去。 | 通過 | CARMEN p. 96：「argenti atque auri … impones libras, neutra ut praeponderet, hasque summittes in aquam … protinus inclinat pars haec quae sustinet aurum」 | — |
| gal-1586（ek087–ek088） | 量水那一種，一五八六年就被人嫌過了；／嫌它的，就是開頭那個年輕人：義大利的伽利略。 | 通過 | GAL-FAV p. 211（重抓）「nell'anno 1586」（根據 Viviani）；RORRES「In 1586 at the age of 22, Galileo (1564-1642)」。沒說「最早」 | — |
| gal-writes（ek089） | 他寫了一篇短文，只拿給朋友看，生前沒有印；後人叫它《小天平》。 | 通過（記一筆） | GAL-FAV p. 211：「Tale scrittura non fu data alle stampe vivente l'Autore; ma bensì, mostrata subito … agli amici e conoscenti, più tardi a' discepoli, si diffuse manoscritta」；p. 211「senza titolo」。原文是「先給朋友和熟人看，後來給學生，手抄流傳」，「只拿給朋友看」略窄，但照 #31 覆核的說法，可以照用 | — |
| gal-quote、gal-quote-b（ek090–ek091） | 一開頭就說：照有些人寫的，把王冠放進水裡，看水漲多少來分辨金和銀，／這種說法，老實講，很粗糙，離精確差得遠。 | 通過 | 《小天平》第一段（Rorres 頁面，重抓）：「come da alcuni è scritto, co 'l mettere tal corona dentro a l'aqqua … dalle differenze del far più o meno ricrescere o traboccare l'aqqua … par cosa, per così dirla, molto grossa e lontana dall'esquisitezza」 | — |
| who-some、rumor、writer-adds（ek092–ek094） | 他說「有些人寫的」，沒有點名是誰。／他猜：……那個時代，有位作家把它寫了下來，／為了在聽來的那一點消息上多補一些，就自己加上了量水的做法。 | 通過 | 同上：「Ben crederò io che, spargendosi la fama … fosse poi da qualche scrittore di quei tempi lasciata memoria di tal fatto; e che il medesimo, per aggiugner qualche cosa a quel poco che per fama avea inteso, dicesse Archimede essersi servito dell'aqqua」。「他猜」保留了 crederò | — |
| best-line（ek095，changes #4） | 我們覺得，這是整份檔案裡最妙的一句：量水這一段，被懷疑是寫的人自己補的。 | 通過 | 意見，有標「我們覺得」；後半句照 ek094 的原文只講量水這一段，是「被懷疑」不是「是」 | — |
| only-guess（ek096） | 不過，這是他的猜測，不是證據；他懷疑的也只有方法，不是那場澡。 | 通過 | #33 備註；原文也說「come da alcuni è scritto … co 'l mettere tal corona dentro a l'aqqua」，只針對方法 | — |
| della-porta、super-eureka（ek098–ek099） | 三年後的一五八九年，另一個義大利人在印出來的書裡，也說這個方法難用；／還說自己的辦法，該喊「超級 Eureka」。 | 通過（記一筆） | RORRES magick.html（重抓）：「Giambattista della Porta (1535-1615) published an account … in the 18th book of his work MAGIA NATURALIS (Natural Magic) in 1589」；1658 年英譯：「But the operation is difficult … that we may cry, we have oversounded Supereureka, Supereureka」。這一頁**不在 `video.json` 的 `sources`**，要補 https://math.nyu.edu/Archimedes/Crown/magick.html | — |
| balance（ek101） | 天平。跟剛剛那首詩一樣，在水裡秤。 | 通過 | 《小天平》（Rorres 英譯）：「This method consists in using a balance」；稱重時一端泡在水裡，跟 CARMEN 是同一種做法 | — |
| why-arch、why-arch-2（ek102–ek103） | 伽利略說，這才是阿基米德會用的辦法，／因為它靠的，正是那本書裡證明過的道理。 | 通過（記一筆） | 《小天平》第一段：「il qual modo crederò io esser l'istesso che usasse Archimede, atteso che … depende ancora da dimostrazioni ritrovate dal medesimo Archimede」（Rorres 英譯「I think it probable that this method is the same that Archimedes followed」）。原文有「我認為、大概」，ek100 已用「伽利略自己覺得」框住，所以通過。另外伽利略說他是讀了《浮體論》**和**《論平面平衡》才想到的，方法也用到槓桿；ek103 只說「那本書」，但這個核心原理（在水裡變輕）伽利略自己說是「demonstrated by Archimedes」，就是 Prop. 7，可以 | （可選）伽利略認為，這多半就是阿基米德用的辦法， |
| rorres-calc（ek105） | 數學家羅瑞斯替它算過。先說他的假設：花環重一公斤。 | 通過 | RORRES Intro（重抓）「let us assume that Hiero's wreath weighed 1000 grams」；SCIAM「Chris Rorres, a mathematician」 | — |
| vergina-wreath（ek106） | 真的出土過的、那個時代最大的金花環，七百多公克；取整數算一公斤，我覺得不算離譜。 | 通過（記一筆） | RORRES Intro：「The largest known golden wreath from Archimedes' time is the one pictured from Vergina … a mass of 714 grams, although some of its leaves are missing」。原文是「已知最大的」；Rorres 的圖說寫的是 Vergina「Fourth century BC」，比阿基米德早一點，「那個時代」是照 Rorres 的說法。意見有標 | （可選）目前出土過的、那個時代最大的金花環，七百多公克；…… |
| container、two-in、mm（ek107–ek109） | 三成的金子被換成了銀；容器的口，直徑二十公分。／……只差零點四一公釐，連半公釐都不到。 | 通過 | RORRES Intro：「replaced 30% (300 grams) of the gold in the wreath by silver」「a container with a circular opening of diameter 20 centimeters」「0.206 minus 0.165 centimeters, or 0.41 millimeters」 | — |
| dice、dice-bowl（ek110–ek111） | 差的水量其實不少，大約三顆骰子那麼大；／可是你把三顆骰子丟進一盆水，水面幾乎看不出動靜。 | 通過 | RORRES Intro「the difference in volume … is 13.0 cubic-centimeters … would form a cube of 2.35 centimeters on each side」；#37 覆核「約是三顆一般骰子（邊長約 1.6 公分）」（1.6³≈4.1，×3≈12.3）。ek111 是比喻，對應 Rorres「spread over a container opening … only 0.41 millimeters」 | — |
| balance-q、g-easy（ek113–ek114） | 兩邊會差十三公克；／他說，阿基米德那個時代的秤，很容易就秤得出來。 | 通過 | RORRES Intro：「an imbalance of 13.0 grams. Scales from Archimedes' time could easily detect such an imbalance in mass.」 | — |
| sciam-2006、sciam-b（ek115–ek116） | 二〇〇六年，他對《科學美國人》說：量水的方法，理論上行得通；／可是真的動手做，現實就會擋路。 | 通過 | SCIAM（重抓，datePublished 2006-12-08）：「"The volumetric method works in theory so it sounds right but when you actually try it you find that the real world gets in the way."」 | — |
| wet-wreath（ek117） | 他點了三樣會攪局的：水的表面張力、拿出來時沾著的水、花環縫裡的氣泡。 | 通過（記一筆） | RORRES Intro：「considering the possible sources of error due to surface tension, water clinging to the gold upon removal, air bubbles being trapped in the lacy wreath, and so forth」。三樣都對，但原文後面還有「and so forth」，而且這是他網頁上寫的，不是在 SCIAM 訪問裡說的（SCIAM 只有記者寫的一句表面張力）。接在 ek115–ek116 後面，聽起來像訪問裡說的。不算錯；要更準可以改 | （可選）他在自己的網頁上舉了幾樣會攪局的：水的表面張力、拿出來時沾著的水、花環縫裡的氣泡。 |
| some-truth、buoyancy-moment、not-bathtub（ek119–ek121） | 羅瑞斯說，故事可能有幾分真：阿基米德確實量過東西的體積；／……也許是因為他發現了浮力，／而不是坐在浴缸裡，再光著身子跑過大街。 | 通過 | SCIAM（重抓）：「"There may be some truth to it," Rorres adds. "Archimedes did measure the volume of things but the eureka moment was maybe due to his original discovery [concerning buoyance], not to sitting in the bathtub and then running through the streets of Syracuse naked."」；「可能」「也許」都保留了 | — |
| rewind-lane、rewind-two、rewind-gal（ek123–ek125） | 最早那一份，寫的是往家裡，不是上街；／一百多年後普魯塔克的版本，連衣服的事都沒提；／一千多年後，連量水的方法都被嫌粗糙。 | 通過（ek123 記一筆） | 同 ek033、ek074、ek091。ek123 的「最早那一份」指的是片中翻過的幾份裡最早的，跟 ek003 一樣，ek008 改了之後意思就清楚了 | — |
| answer、answer-b（ek126–ek127） | 光著身子跑回家這一幕，只有開頭那位羅馬建築師，留下一份紀錄；／它到底有沒有發生，沒有任何證據能回答。這一案，未結。 | 通過 | 照覆核：只說「這一幕」只有一份紀錄（普魯塔克沒光身子、拉丁詩沒浴池；德拉波爾塔 1589 年重講時寫「running home」，那是轉述維特魯威，不算獨立紀錄）；不說「這是假的」（#38） | — |
| theme（ek129–ek130，changes #6） | 一個故事每傳一次，就可能多一層、少一塊。那它本來長什麼樣子？／只能一份一份往回翻。 | 通過（記一筆） | 旁白的看法，有「可能」。「多一層」有 #8（後人加上街、忘了穿衣服）撐；「少一塊」拿普魯塔克來講要小心：普魯塔克的出處不知道，不一定是從維特魯威傳下來後「少了」光身子。這句沒有點名誰少了，可以照用 | — |
| outro、subscribe（ek131–ek132） | 你小時候聽到的版本……有沒有穿衣服？留言告訴我。／這個頻道只講紀錄裡找得到的…… | 通過 | CTA，沒有事實 | — |
| youtube.title | 阿基米德真的光著身子喊 Eureka？最早的紀錄晚了將近 200 年｜奇聞檔案局 | 通過（記一筆） | 跟 ek003 同一件事：「最早的紀錄」嚴格講是「目前找得到最早的」。標題要短，說明欄第一段已經寫了「目前找得到最早的文字」，可以照用 | — |
| youtube.description | （全文） | 通過 | 逐句對過：第九書的序、獻給奧古斯都、前一世紀後期、將近兩百年（#1、#13、#14、#18）；金葉花環、告發摻銀、公共澡堂、「nudus vadens domum versus」、εὕρηκα（VIT-LAT 重抓）；「往家裡」沒有「上街」「忘了穿衣服」（#7、#8）；阿基米德自己的著作與《浮體論》（HEATH 重抓，#20–#22）；普魯塔克沒提衣服、沒回家、用「走」（Perseus 重抓）；拉丁詩有金冠沒浴池、水中天平（CARMEN 重抓）；1586、二十出頭、只給朋友看、「很粗糙，離精確差得遠」、那個時代的作家補的（GAL-FAV、Rorres 重抓）；1589 德拉波爾塔嫌難用（magick.html）；Rorres 的假設與 0.41 公釐、13 公克（Intro 重抓）；界線段沒說「是假的」，「這一幕」只有一份紀錄、未結。插圖那段跟提示詞一致（歷史人物都用物件代表，Rorres 不入畫） | 不用改 |

**其餘全部通過**（逐句看過，都是問句、轉場、「你」的旁白，或旁白自己的反應，沒有暗含新事實）：ek012、ek020、ek026、ek032、ek037、ek040、ek046、ek047、ek049、ek053、ek065、ek066、ek072、ek073、ek086、ek097、ek100、ek104、ek108、ek112、ek118、ek122。
（ek023 後半「結果呢？」、ek058 後半「僥倖到什麼程度？」、ek116 後半「擋路的是什麼？」也是問句，前半已列在表裡。）

## 畫面與規則（只影響畫面，記一筆）

- 在世或 1956 年後過世的人：提示詞裡**沒有**畫羅瑞斯本人，rorres-calc 是 Ada 捧花環、mm 是 Ada 瞇眼看。希斯（1861–1940）只畫書和眼鏡（heath-desk），伽利略與德拉波爾塔只畫信和印刷機，都沒有臉。歷史人物一律用物件代表，符合規則。
- 一般人物景（open-you、your-version、plut-hearsay、plut-dinner、you-eat、rumor、how-much、outro）都是無名的一般人，沒有對應到真人。
- caught 的提示詞寫「spilling a much bigger puddle」：維特魯威說花環排開的水比較多，但 ek109 的重點正是差別小到看不出來（0.41 公釐）。不算錯，只是誇張；想讓畫面跟第 7 章一致，可以改成「a slightly bigger puddle」。
- Ada 的 `characters[0].appearance` 寫「a short loose black bob」，每個 Ada 景的提示詞卻寫「wavy black bob with a side fringe」，兩邊不一致（跟事實無關，給畫面的人看）。
- 沒有出現「銅線」（verify-1 #34 的黃銅絲問題這一版用不到）、Proclus、加州州印。

## 要改的句子清單

- vitr-who（ek008）｜最早寫下這一幕的，是一位羅馬建築師，叫維特魯威。｜目前找得到最早寫下這一幕的，是一位羅馬建築師，叫維特魯威。
- vitr-200（ek011）｜從阿基米德的時代算到這裡，就是開頭說的那將近兩百年。｜從阿基米德過世算到這裡，就是開頭說的那將近兩百年。
- how-prove（ek041）｜那他回到家之後，要怎麼證明？｜那他接下來，要怎麼證明？
- oil-draw（ek076）｜普魯塔克在另一本書裡還寫，他常被人硬拖去洗澡抹油，｜普魯塔克在另一本書裡還記了一則傳聞：他常被人硬拖去洗澡抹油，
- reverse（ek079）｜有浴池，沒提光身子；那有沒有反過來的版本？｜有浴池，沒提光身子；那有沒有連浴池都沒有的版本？
- half-half（ek128）｜查得清的，是誰在哪一年寫了什麼；回答不了的，是那天到底發生了什麼。｜查得清的，是每一份紀錄寫了什麼、沒寫什麼；回答不了的，是那天到底發生了什麼。

旁白以外的事（本輪沒有改）：

- `video.json` 的 `sources` 要補兩列：Rorres〈Natural Magick〉https://math.nyu.edu/Archimedes/Crown/magick.html （ek098–ek099）、Plutarch《Marcellus》17.6（LacusCurtius，ek076–ek077）。SMITH〈Nudus〉（ek038）與 WP〈On Floating Bodies〉（ek059）也只列在 S24.md，沒有進 `sources`。
- `claims.md` 的行號還是舊的 ek101–ek722，跟這次的 ek001–ek132 對不上。如果 `tools/video/qa/facts.mjs` 照 id 對，要重排；ek076、ek079、ek128 的依據也要照上面更新。
- `loops` 裡 how-prove（ek041）和 reverse（ek079）的 setup 文字要跟著改句。
- changes.md 的〈【待查】〉一節寫「0 條」，下面列的 7 處都判過了，結果在上面的摘要。
