# curio-s26-v2 查核第二輪（2026-11 重做稿）

- **查核日期**：2026-11-13。查核者沒有參與撰稿。
- **範圍**：`video.json` 的 `scenes[].lines[].text`，共 130 句（t001–t130）、124 景（`say` 只管讀音，沒有查），加上 `youtube.title`、`youtube.description` 裡的事實。章名（`chapter`）有事實的也順手看了。
  另外查了 `curio-redo-handoff/drafts/curio-s26-v2/changes.md`：〈【待查】清單〉寫「0 條」，但列了 10 處「算術或改寫後說法跟原句不完全一樣」（t011、t047、t049、t076、t085、t089、t090、t109、t120、t123）；
  第 6 點〈刪掉的句子〉、第 7 點〈新寫的轉場句〉也有改寫。這些逐條判定如下。
  （`video.json` 和草稿資料夾那份台詞一字不差，差在 `target_minutes`、`music`、`pauses` 等其他欄位。）
- **方法**：逐句看人名、年份、數字、引號裡的話、誰說的、事件順序，以及「第一個」「親口」「從來」「完全」「一定」「才」「沒人」「不可能」這類強詞。對照的是 `claims.md`（行號還是舊的 mb101–mb918，這次照句子內容對回去）、
  `verify-1.md`（第一版查核加獨立覆核，40 列，含「旁白不要說…」「改成…」的但書）、`brief.md`、`NOTES.md`。這次沒有只照抄前一份：`video.json` 的 `sources` 列的固定文本，抓得到的都**重新抓下來逐字核對**：
  - CONF-1782＝archive.org `j1782lesconfessio02rous` OCR：書名頁「LES CONFESSIONS DE J. J. ROUSSEAU, Suivies DES RÊVERIES Du Promeneur Solitaire, TOME SECOND, A GENÈVE. M. DCC. LXXXII.」；
    卷六 pp. 181–182 Mably、Arbois 白酒、「je n'ai jamais pu boire sans manger」、「Un beau Monsieur, l'épée au côté, aller chez un boulanger acheter un morceau de pain, cela se pouvoit-il ?」、
    「Enfin je me rappellai le pis-aller d'une grande Princesse à qui l'on disoit que les paysans n'avoient pas de pain, & qui répondit, Qu'ils mangent de la brioche. Encore, que de façons pour en venir-là ! Sorti seul à ce dessein, je parcourois quelquefois toute la ville, & passois devant trente pâtissiers avant d'entrer chez aucun」（沒有「J'achetai de la brioche.」，跟 verify-1 #12 一樣）；
    同卷「maintenant que j'écris ceci, infirme & presque sexagénaire」
  - Lausanne 1782＝`d1782lesconfessi02rous` OCR：書名頁「TOME SECOND. A LAUSANNE, Chez François Grasset & Comp. M. DCC.LXXXII.」；p. 180「Enfin je me rappellai le pis-aller d'une grande Princesse … qui répondit : qu'ils mangent de la brio-che.」
  - CONF-1783＝`confessionsjjro01rousgoog` OCR（London, J. Bew）：pp. 136–137「At last I recollected the [last shift] of a great princess, to whom it was told the peasants had no bread. Why then, said she, let them eat pastry.」「my dear bit of cake」（OCR 把 last shift、eat 讀錯，同 verify-1 #14）
  - CONF-EN＝Gutenberg #3913（1903 英譯）：卷六「I had two under my care」「white Arbois wine」「"Then let them eat pastry!"」「the dear little cake」「at the moment I write this, though infirm, near sixty」「after a year's trial … I determined to quit my pupils」；卷七開頭「The history of the first part of my life was written from memory, and is consequently full of errors.」
  - KARR 1841＝`bub_gb_pCv7DOf42bsC`（中繼資料「Les guêpes Alphonse Karr Novembre」「1841」）：p. 61「Cet aperçu rappelle le mot vrai ou faux qu'on rapporte de Marie Antoinette : — S'il n'y a pas de pain on mangera de la brioche.」
  - KARR 1843＝`lesgupes04karruoft` p. 260，「Avril 1843」一節（前一節「Mars 1843」）：「On se rappelle quelle indignation on excita, dans le temps … entendant dire que le peuple était malheureux et qu'il n'avait pas de pain … « Eh bien ! qu'il mange de la brioche. » Le hasard m'a fait un de ces jours derniers rencontrer un livre daté de 1760 — où on raconte le même mot d'une duchesse de Toscane, — ce qui me paraît prouver à peu près que le mot n'a pas été dit par Marie-Antoinette, mais retrouvé et mis en circulation contre elle.」
  - ARNETH＝`mariatheresiaund00mari`：p. 149「A Versailles, le 22 juin 1775.」「Le sacre a été parfait」「d'être si bien reçu deux mois après la révolte et malgré la cherté du pain, qui malheureusement continue」「nous sommes encore plus obligés de travailler à leur bonheur. Le roi m'a paru pénétré de cette vérité」；
    p. 155「Versailles, le 14 juillet 1775.」「le peuple, qui a tant souffert de la cherté du pain. Heureusement l'espérance commence à renaître; les blés sont très-beaux et on est sûr que le pain diminuera après la moisson.」。
    **新發現**：書名頁寫「ZWEITE VERMEHRTE AUFLAGE … LEIPZIG … 1866」，是**第二版**；〈Vorwort zur ersten Auflage〉署「Wien, im December 1864」，〈Vorwort zur zweiten Auflage〉說「binnen Jahresfrist eine zweite Auflage dieser Publication nothwendig wurde」，署「Wien, im Jänner 1866」（見 t064）
  - BOIGNE＝Gutenberg #29613（這是 1921 年 Émile-Paul 的全本）：第 II 章章目「Cour de Mesdames, filles de Louis XV. … Madame Victoire」；「Madame Victoire avait fort peu d'esprit et une extrême bonté. C'est elle qui disait, les larmes aux yeux, dans un temps de disette où on parlait des souffrances des malheureux manquant de pain: «Mais, mon Dieu, s'ils pouvaient se résigner à manger de la croûte de pâté!»」；
    作者自序「Au commencement de 1835 … Quelques mois après l'événement」「Mon premier projet … était uniquement de retracer ce que j'avais entendu raconter à mes parents sur leur jeunesse et la Cour de Versailles」；編者說明「elle est née le 19 février 1781」，第一部寫的是「des faits ou de simples épisodes survenus pendant son enfance et, parfois même, avant sa naissance」
  - WP（二手，重抓頁面）：英文〈Let them eat cake〉「the traditional translation」「a bread enriched with butter and eggs, considered a luxury food」「absorbing 50 percent of their income … obsessional national interest」「published when she was 26, eight years after she became queen」「he may have invented the anecdote altogether」「Anti-monarchists during the French Revolution never cited this anecdote」；
    英文〈Marie Antoinette〉「born on 2 November 1755 at the Hofburg Palace in Vienna」「15th child of Empress Maria Theresa」「on 19 April 1770 she was married by proxy … Vienna」「16 May 1770 in the Palace of Versailles」、在位「10 May 1774」「The Flour War of 1775 … damaged her reputation」「During the French Revolution, she became known as Madame Déficit」「executed by guillotine on 16 October 1793」；
    英文〈Adèle d'Osmond〉「Starting in 1835 … published in 1907 in an abridged version and in full in 1921」；英文〈Flour War〉「April to May 1775, in the northern, eastern, and western parts」；英文〈Brioche〉「high egg and butter content」；
    法文〈Guerre des farines〉「le 13 septembre 1774」「devant Versailles le 2, et, le 3 mai, la foule pille les boulangeries de Paris」；法文〈Jean-Jacques Rousseau〉「Naissance 28 juin 1712」「Décès 2 juillet 1778」「où il arrive le 1er mai 1740」「retourne auprès de Mme de Warens en mai 1741」「du 22 mars 1766 au 1er mai 1767. C'est là qu'il écrit les premiers chapitres」；法文〈Les Confessions〉「en 1782 pour la première partie」「rédigée en 1765-1767」
  - 沒有重開、**沿用 verify-1** 的：法文維基文庫 1889 年本（這次 API 回 429，抓不到；「J'achetai de la brioche.」與卷七「Ma première partie a été toute écrite de mémoire ; j'y ai dû faire beaucoup d'erreurs.」照 verify-1 #1、#15，意思已用 1903 英譯重抓核對）、
    1783 英譯是「最早的英譯」（來源表）、Johnson 1990 與 Fraser 原書、卡爾 1841 是「le premier auteur connu」（法文 WP 引 Campion-Vincent，verify-1 #17）、1907 年節本的內文（只開了 1921 全本，見 t109）。
- **結論摘要**：主幹沒有問題。四十八年、兩封信（日期、內容、十一天、三個星期）、卡爾 1841 的「不知真假、人家傳說」、1843 的「大致證明」與托斯卡尼公爵夫人、「鄉下人」變「人民」、
  《懺悔錄》1782 年日內瓦與洛桑兩個版本都有這句、作者 1778 年先過世、第六卷「快六十歲」、1783 與 1903 英譯是 pastry、1783 同段有「a bit of cake」、維多利亞夫人「不太聰明但極好心」與含淚說酥皮，都逐字對得上。
  verify-1 的但書（目前找得到最早、只說一八四三年、研究者說找不到、不說饑荒、十來歲／還不到十三歲、一七六〇年代後半、第六卷不定年、有學者懷疑、能確定的只有他已經知道這個段子、不說她從來沒說過）全部守住了。**要改 4 句**（其中一處是三句一起調順序）：
  - tutor-arrive（t011）「一個**二十八歲**的年輕人來到這裡」：盧梭 1712 年 6 月 28 日生，1740 年 5 月 1 日到里昂時是**二十七歲**，兩個月後才滿二十八。
  - thirty-shops（t020，連帶 recall、peasants、buys-brioche、alone-errand t024–t026、t021）**事件順序反了**：原文是先想起公主的話、改買布里歐，「為了這件事」一個人出門，才有跑遍全城、走過三十家糕點店；現在的稿子把三十家糕點店放在想起公主之前，還用「所以」「最後」接起來。第一版（mb806–mb808）就是這個順序，verify-1 沒抓到，這次重抓 1782、1783、1903 三個本子都一樣。
  - invented（t041）「也有學者懷疑，**糕點店這段故事**，根本是他編的」：WP 那句緊接在公主那段引文後面，說的是「the anecdote」（公主說了這句話），不是盧梭自己在糕點店門口的事。第一版 mb813 只說「這段故事」。
  - empress（t064）「這些信**到一八六六年才整批印出來**」：1866 年的萊比錫本是第二版；第一版的序署 1864 年 12 月，第二版序說第一版出來「不到一年」就要再版。
- changes.md：【待查】**確實沒有新事實**，10 處逐條看過：**t011 要改**（二十七歲）；t047、t049、t076、t085、t089、t090、t120 **通過**；t109、t123 **通過（記一筆）**。另外 changes.md 沒列、但這次改寫碰到的：t020 的順序（要改）、t041 的「糕點店」（要改），t064 是第一版就有的錯（要改）。
- `youtube.description`：**要改一處**。「本集插圖由 AI 生成；畫中的歷史人物都是卡通化的角色，不寫名字、不追求相似」跟新稿不符：重做稿的歷史人物一律用物件代稱、不畫人像（changes.md〈畫面改了什麼〉）。changes.md 第 5 點自己也列了這一條待改。其餘事實逐句對過都對；「資料截至」那行建議順手補上這次重做的日期。
- `youtube.title`「書裡那一天，比她出生早 15 年」：**通過（記一筆）**。算法：書裡那件事發生在盧梭住 Mably 家那一年，法文 WP 是 1740 年 5 月 1 日到、1741 年 5 月離開；瑪麗‧安東妮 1755 年 11 月 2 日出生。
  照年份相減是 1755－1740＝15；照月份算，那件事在出生前 **14 年半到 15 年半**之間（書裡沒寫是那一年的哪一天），四捨五入就是 15 年，標題的「15 年」成立。兩個條件：
  一、「那一天是 1740 年前後」不是書上寫的，是傳記（法文 WP 引 Trousson）排出來的盧梭年表，《懺悔錄》這段附近沒有年份（verify-1 #6）；
  二、這是盧梭二十多年後憑記憶寫的，他自己說錯一定很多，也有學者懷疑公主這段是他編的（#15）。旁白在 t038–t042 都有交代，說明欄也有，標題可以照用。

## 判定表

| 景 id（句 id） | 句子（原文） | 判定 | 依據 | 建議改法 |
| --- | --- | --- | --- | --- |
| tutor-arrive（t011，changes 待查） | 一個二十八歲的年輕人來到這裡，住進憲兵總監的家。 | 要改 | 法文 WP〈Jean-Jacques Rousseau〉（重抓）「Naissance 28 juin 1712」「où il arrive le 1er mai 1740」：到里昂那天是 27 歲 10 個月，6 月 28 日才滿 28。changes.md 的依據只有「1712 年生」（verify-1 #39 備註），claims mb704 用的是年份相減（1740－1712），只適合說「二十幾歲」。「憲兵總監」照 CONF-1782「M. de Mably」、CONF-EN「chief Provost of Lyons」、verify-1 #3 | 一個二十七歲的年輕人來到這裡，住進憲兵總監的家。（或「一個快滿二十八歲的年輕人」） |
| thirty-shops（t020） | 所以他在街上走，走過三十家糕點店，還是不敢推門。 | 要改（事件順序） | CONF-1782 卷六（重抓）的順序是：不敢自己買麵包 →「Enfin je me rappellai le pis-aller d'une grande Princesse …」→「Encore, que de façons pour en venir-là ! Sorti seul à ce dessein, je parcourois quelquefois toute la ville, & passois devant trente pâtissiers avant d'entrer chez aucun」→ 店裡只能有一個人 →「ma chère petite brioche」。1889 年本在「Qu'ils mangent de la brioche.」後面多一句「J'achetai de la brioche.」（verify-1 #1），順序一樣。CONF-1783「What ceremonies even to attain that! Going out alone on this errand, I ran all over the town, and passed by thirty shops」、CONF-EN「At length I recollected … Yet even this resource was attended with a difficulty. I sometimes went out alone for this very purpose … passing thirty pastry cook's shops」（都重抓）。三十家糕點店是**想起公主、改買布里歐之後**的事；稿子放在之前，又用「所以」接在「不敢進麵包店」後面、t024 用「最後」接想起公主，聽起來是「找了三十家糕點店都不敢進，最後才想到那句話」，正好倒過來。另外原文跑遍全城、走過三十家都在「quelquefois」（有時）底下 | 把 recall、peasants、buys-brioche（t024–t026）移到 you-suit（t019）後面，再接 thirty-shops、alone-errand、one-person、peek，然後 brioche（t027）。t024「最後，他想起…」照用（原文就是 Enfin）；t026 改「他把這句話當成不得已的辦法：改買布里歐。」；t020 改「可是就連買布里歐也不容易：他會走過三十家糕點店，還是不敢推門。」；t021 改「他一個人出門，就是為了這一塊布里歐；有時候跑遍全城。」。loops 的 t024→t025 仍然相鄰，不受影響；畫面不用重畫，只是換順序 |
| alone-errand（t021） | 他一個人出門，就是為了這一塊麵包；有時候跑遍全城。 | 要改（跟 t020 一起） | 「Sorti seul à ce dessein」的「這件事」指買布里歐（同上）。布里歐也算麵包，單句不算錯，但放回正確順序後要寫明 | 他一個人出門，就是為了這一塊布里歐；有時候跑遍全城。 |
| buys-brioche（t026） | 他把這句話當成不得已的辦法，買了布里歐。 | 通過（跟 t020 一起調） | 「pis-aller」（#1）；「J'achetai de la brioche.」只在 1889 年本，1782 兩個本子都沒有（重抓），但同段「ma chère petite brioche」表示買到了，verify-1 #12 說旁白不提版本差異 | 照 t020 的順序改時，改成「他把這句話當成不得已的辦法：改買布里歐。」 |
| invented（t041） | 也有學者懷疑，糕點店這段故事，根本是他編的。 | 要改 | 英文 WP〈Let them eat cake〉（重抓）：先引盧梭那句「the last resort of a great princess who, when told that the peasants had no bread, replied …」，緊接著「Rousseau does not name the "great princess", and he may have invented the anecdote altogether, as the Confessions is not considered entirely factual.」（引 Johnson 1990，原書沒開）。被懷疑是編的，是**公主說過這句話**這件軼事，不是盧梭自己在糕點店門口徘徊。claims mb813 只說「這段故事」，「糕點店」是這次改寫加的 | 也有學者懷疑，那位公主的故事，根本是他編的。 |
| empress（t064） | 媽媽，是奧地利的女皇瑪麗亞．特蕾莎；這些信到一八六六年才整批印出來。 | 要改 | ARNETH（重抓）書名頁「ZWEITE VERMEHRTE AUFLAGE … LEIPZIG … 1866」；〈Vorwort zur ersten Auflage〉末署「Wien, im December 1864」；〈Vorwort zur zweiten Auflage〉「dass binnen Jahresfrist eine zweite Auflage dieser Publication nothwendig wurde」。我們開的是 1866 年第二版，第一版更早（序署 1864 年 12 月；第一版的書名頁沒開，確切年份不寫）。claims 自己也標了這句「出版年取自來源表，不是逐項查核表」。另外第一版序說有些內容「eine gewisse Begränzung der Veröffentlichung」（有所保留），「整批」也嫌滿。女皇身分照英文 WP「Empress Maria Theresa」（重抓） | 媽媽，是奧地利的女皇瑪麗亞．特蕾莎；這些信要到一八六〇年代，才印成書。 |
| open-you、open-queen（t001–t002） | 你一定聽過這句話：沒有麵包，就吃蛋糕。／大家都說，這是法國王后瑪麗．安東尼說的。 | 通過 | 流傳的版本，用「你一定聽過」「大家都說」框住，不當事實講（claims mb101、#14、#19）。「沒有麵包就吃蛋糕」去標點正好八個字 | — |
| open-blame（t003） | 八個字，讓她背到今天：一個不知道百姓有多苦的王后。 | 通過 | 名聲，不是事實主張；WP〈Let them eat cake〉「The quote is taken to reflect either the princess's frivolous disregard for the starving peasants or her poor understanding of their plight」（重抓） | — |
| open-48（t004） | 可是目前找得到最早把它寫到她名下的文字，在她死後四十八年。 | 通過 | 1793-10-16（WP 重抓）到 KARR 1841 年 11 月號（重抓）＝48 年又 1 個月左右；「目前找得到最早」照 #17、#19 | — |
| open-15（t005） | 更早白紙黑字寫下這句話的書裡，那件事，比她出生還早了十五年。 | 通過（記一筆） | 同標題的算法：1740-05 到 1741-05 對 1755-11-02，差 14 年半到 15 年半。「書裡…那件事」框在書裡，年份是傳記排的（#6）。但書在 t031–t042 才交代，鉤子可以先不講 | — |
| open-letter（t006） | 更怪的是，她自己寫信給媽媽的時候，還真的寫到了麵包。 | 通過 | ARNETH p. 149、p. 155（重抓） | — |
| open-karr（t007） | 而目前找得到最早把話記在她名下的人，兩年後自己說：大概不是她。 | 通過（記一筆） | KARR 1843「prouver à peu près」（重抓）。「兩年後」是 1841→1843 的年份相減；實際是 1841 年 11 月到 1843 年 3、4 月（「Avril 1843」一節，verify-1 #18 覆核說可能三月寫），大約一年半。verify-1 的 mb412、mb506 都說「兩年後」並通過，不改 | — |
| open-promise、open-route（t008–t009） | 今天我們就來聊聊……／我們照時間順著走，從一家糕點店的門口開始。 | 通過 | 承諾句與路線圖，沒有事實 | — |
| lyon（t010） | 故事要回到一七四〇年的五月，法國里昂。 | 通過（二手） | 法文 WP「où il arrive le 1er mai 1740」（重抓）。說的是他到里昂，不是買布里歐那天，對 | — |
| pupils（t012） | 他的工作是當家教，教主人家的兩個學生。 | 通過 | CONF-EN（重抓）「M. Deybens proposed my educating M. Malby's children」「I had two under my care」 | — |
| tutor-wine、jura（t013–t014） | 在這戶人家裡，他偷喝過主人的白酒。／那是一種侏羅產的小白酒；他自己說，酒很不錯。 | 通過 | CONF-1782（重抓）「je m'avisai de convoiter un certain petit vin blanc d'Arbois très-joli」「je m'en accommodai de tems en tems de quelques bouteilles pour boire à mon aise」；Arbois 在侏羅（#3 備註） | — |
| must-eat、dare-not（t015–t016） | 可是他有個習慣：喝酒，一定要配東西吃。／照理說，出門買一塊麵包就好了。可是，他不敢。 | 通過 | 同上「je n'ai jamais pu boire sans manger」「En acheter moi-même, je n'osai jamais.」（重抓）；t016 是 changes 第 7 點的新轉場句 | — |
| sword、unthinkable（t017–t018） | 他腰上佩著劍，為什麼連一塊麵包都不敢買？／他後來寫：一個佩劍的體面先生，走進麵包店買一塊麵包，這像話嗎？ | 通過 | 同上「Un beau Monsieur, l'épée au côté, aller chez un boulanger acheter un morceau de pain, cela se pouvoit-il ?」（重抓） | — |
| you-suit（t019） | 你大概也有過：穿得太體面，反而不好意思走進一家小店。 | 通過 | 「你」的旁白，共同經驗，有「大概」 | — |
| one-person、peek（t022–t023） | 問題來了：就算要進門，店裡也只能有一個人，／而且那個人的長相，還要很討他喜歡。 | 通過 | CONF-1782（重抓）「Il falloit qu'il n'y eût qu'une seule personne dans la boutique, & que sa physionomie m'attirât beaucoup pour que j'osasse franchir le pas.」說的是糕點店（見 t020） | — |
| recall、peasants（t024–t025） | 最後，他想起一位偉大的公主說過的話：／聽說鄉下人沒有麵包，她就回答：那讓他們吃布里歐吧。 | 通過 | CONF-1782「Enfin je me rappellai le pis-aller d'une grande Princesse à qui l'on disoit que les paysans n'avoient pas de pain, & qui répondit, Qu'ils mangent de la brioche.」（重抓）。「最後」對 Enfin；順序問題見 t020 | — |
| brioche、not-cake（t027–t028） | 布里歐，是加了奶油和雞蛋的麵包，在當時算奢侈的食物。／注意：是麵包，不是蛋糕。…… | 通過（二手） | WP〈Let them eat cake〉「a bread enriched with butter and eggs, considered a luxury food」、〈Brioche〉「high egg and butter content」（重抓）；#13 | — |
| excuse（t029） | 他不是在罵那位公主，是拿這句話，替自己解圍。 | 通過（記一筆） | #1 備註（pis-aller＝不得已的辦法）。這是解讀；1903 英譯把 pis-aller 譯成「the thoughtless saying」（重抓），譯者讀成帶貶義，所以這句是一種讀法，不是唯一讀法。verify-1 通過，不改 | — |
| is-rousseau（t030） | 這個連麵包都不敢買的家教，叫盧梭。他在里昂，待了一年就走了。 | 通過（記一筆） | CONF-EN「after a year's trial … I determined to quit my pupils」、「the year I passed at M. Malby's」；法文 WP「mai 1741」（重抓）。嚴格講他離開的是 Mably 家：法文 WP 同段寫他回 Warens 夫人身邊幾個月後「retourne à Lyon」 | （可選）這個連麵包都不敢買的家教，叫盧梭。他在這戶人家，待了一年就走了。 |
| fifteen（t031） | 那一年是一七四〇年前後；瑪麗．安東尼，還要再過十五年才出生。 | 通過（記一筆） | 算法見標題那一段；1755-11-02（WP 重抓）。verify-1 #6 覆核要「掛在盧梭說底下，下一句接但書」；新稿的但書在 t038–t042（能記得多準、錯一定很多、有學者懷疑、能確定的只有），隔了七句才到，中間的 t032–t037 是在交代這本書，聽起來還順。要更穩可以在這句先掛條件。注意不能寫「照他書裡寫的」：書上沒有年份 | （可選）如果他沒記錯，那一年是一七四〇年前後；瑪麗．安東尼，還要再過十五年才出生。 |
| how-know、wrote（t032–t033） | 可是，一個家教買麵包的小事，我們今天怎麼會知道？／因為二十多年後，他自己把這件事寫進了一本書。 | 通過 | changes 第 7 點的新轉場句。「二十多年」：1740–41 到 1766–1768（#7）是 25–28 年 | — |
| england、wootton、which-castle（t034–t036） | 一七六〇年代後半，他先在英國鄉下，後來在一座城堡裡，寫下第一部。／頭幾卷，是一七六六年三月到隔年五月，在英國寫的；／寫到糕點店的第六卷呢？是不是也在那裡寫完，沒人能確定。 | 通過（二手） | 法文 WP（重抓）「du 22 mars 1766 au 1er mai 1767. C'est là qu'il écrit les premiers chapitres」；卷七「à Wooton ou dans le château de Trye」（#7，沿用）；#7 覆核「一七六〇年代後半」「卷六不要定在 1766 年」。「頭幾卷」對「premiers chapitres」、「沒人能確定」對覆核的「可能寫在 Trye，或之後還修過」，claims mb702、mb712 已這樣寫 | — |
| sixty（t037） | 他在這一卷裡寫：寫下這些的時候，自己已經體弱，快六十歲了。 | 通過 | CONF-1782 卷六（重抓）「maintenant que j'écris ceci, infirme & presque sexagénaire」；CONF-EN 卷六（Book VI 範圍內，重抓）「though infirm, near sixty」 | — |
| you-old（t038） | 你想想，一個老人，在寫自己二十幾歲的事，能記得多準？ | 通過 | 1740 年 27–28 歲（見 t011）；「老人」接他自己說的快六十歲 | — |
| recalled（t039） | 注意他用的動詞：「我想起」。他不是在記新鮮事，是在翻一段舊記憶。 | 通過（記一筆） | 「je me rappellai」（重抓）。後半是解讀（claims mb606 標了）。「我想起」是 1740 年的盧梭想起公主的話，放在講 1766 年寫書這一章，可能被聽成 1766 年的盧梭在回想；t042 接「他寫書的時候，已經知道這個段子」，意思還通 | — |
| errors（t040） | 他自己也承認：第一部全憑記憶寫，錯一定很多。 | 通過 | 卷七開頭「Ma première partie a été toute écrite de mémoire ; j'y ai dû faire beaucoup d'erreurs.」（法文沿用 verify-1 #15）；CONF-EN「was written from memory, and is consequently full of errors」（重抓） | — |
| sure（t042） | 能確定的只有：他寫書的時候，已經知道這個段子。 | 通過 | #6 覆核原話 | — |
| vienna、under13（t044–t045） | 她一七五五年在維也納出生，這時候還在那裡，是個十來歲的小女孩。／也就是說，盧梭寫下那位公主的時候，她還不到十三歲，連法國都沒去過。 | 通過 | WP「born on 2 November 1755 at the Hofburg Palace in Vienna」（重抓）；#8 覆核「十來歲」「還不到十三歲」（Trye 到 1768-06，她 12 歲） | — |
| carriage（t046） | 一七七〇年四月，她先在維也納辦了代理婚禮；五月才到凡爾賽，那年十四歲。 | 通過（二手） | WP（重抓）「on 19 April 1770 she was married by proxy … Vienna」「16 May 1770 in the Palace of Versailles」；1770 年 11 月前是 14 歲 | — |
| queen（t047，changes 待查） | 四年後，一七七四年，十八歲的她當上了法國王后。 | 通過 | WP 在位「10 May 1774」（重抓）；1755-11-02 生，1774-05-10 是 18 歲半；1770→1774 四年 | — |
| legend（t048） | 傳說裡，她說那句話的時候，法國的百姓正缺麵包。真的有過這樣的日子嗎？ | 通過 | 「傳說裡」框住；不說饑荒（#27） | — |
| price-up（t049，changes 待查） | 有，就在她當上王后的隔年春天，麵包的價錢漲了起來。 | 通過 | 1774-05 當上王后，1775 年春天就是隔年春天，跟原句「還不到一年」都對；英文 WP〈Flour War〉「It followed an increase in grain prices, and subsequently bread prices」（重抓） | — |
| half-income、obsess（t050、t052） | 傳記作者估計，那時老百姓一半的收入，都花在麵包上。／所以傳記作者說，麵包，是全國上下最掛心的事。 | 通過（二手） | WP 引 Fraser（重抓）「absorbing 50 percent of their income … the whole topic of bread was therefore the result of obsessional national interest」；「傳記作者估計」照 #26 | — |
| you-salary（t051） | 想想看，你每個月最大的一筆開銷忽然漲價，你會不會上街？ | 通過 | 「你」的旁白 | — |
| grain、riots、crowd-gate、looted（t053–t056） | 導火線，是前一年九月，政府放開了穀物的買賣。／四月到五月，北部、東部、西部……鬧起了暴動；／五月初，人群一路鬧到凡爾賽宮門口。／第二天，巴黎的麵包店也被搶了。後來的人，叫它「麵粉戰爭」。 | 通過（二手） | 法文 WP（重抓）「le 13 septembre 1774」「devant Versailles le 2, et, le 3 mai, la foule pille les boulangeries de Paris」；英文 WP（重抓）「April to May 1775, in the northern, eastern, and western parts」 | — |
| reputation（t057） | 研究她的人說，這場風波，傷了她在百姓心裡的名聲。 | 通過（二手） | WP〈Marie Antoinette〉（重抓）「The Flour War of 1775 … damaged her reputation among the general public」 | — |
| deficit、deficit-b（t058–t059） | 但這還不是最糟的：後來反對王室的文宣，叫她「赤字夫人」；／說法國的錢，是她一個人花光的。 | 通過（二手） | WP〈Let them eat cake〉（重抓）「anti-monarchist polemics demonized Antoinette as Madame Déficit, who had single-handedly ruined France's finances」。「但這還不是最糟的」是 changes 第 7 點的新轉場，屬旁白的評語 | — |
| sticks（t060） | 我覺得，這就是這八個字黏得住她的原因：外國來的、愛花錢、又是王后。 | 通過 | 標成意見（「我覺得」）；#31 備註 | — |
| crowned、letter-june（t062–t063） | 知道，而且她自己寫下來了。那年六月十一日，國王加冕；／十一天後，她寫信給媽媽，日期是六月二十二日。 | 通過 | ARNETH p. 149（重抓）「A Versailles, le 22 juin 1775.」「Le sacre a été parfait」；加冕 6 月 11 日是 WP（#29，沿用）；6/11→6/22 十一天 | — |
| june-quote、duty、king（t065–t067） | 她寫：暴動過了兩個月，大家還這樣歡迎我們。可惜，麵包還是很貴。／「看到這些受苦、卻還這樣待我們的人，我們更應該為他們的幸福努力。」／她還寫，國王看起來，也深深明白這個道理。 | 通過 | ARNETH p. 149（重抓）「d'être si bien reçu deux mois après la révolte et malgré la cherté du pain, qui malheureusement continue」「en voyant des gens qui dans le malheur nous traitent aussi bien, nous sommes encore plus obligés de travailler à leur bonheur. Le roi m'a paru pénétré de cette vérité」。「還是很貴」照 #30 覆核，不說「還在漲」 | — |
| letter-july、wheat（t069–t070） | 沒有。三個星期後，她又寫：百姓為了麵包貴，吃了好多苦。／「好在麥子長得很好；收成以後，麵包一定會便宜。」 | 通過 | ARNETH p. 155（重抓）「Versailles, le 14 juillet 1775.」「le peuple, qui a tant souffert de la cherté du pain. Heureusement l'espérance commence à renaître; les blés sont très-beaux et on est sûr que le pain diminuera après la moisson.」6/22→7/14 是 22 天 | — |
| surprised、nineteen（t071–t072） | 我第一次讀到這兩封信，老實說，有點意外。／寫信的是一個十九歲的王后，口氣不像會說「吃蛋糕」的人。 | 通過 | 旁白的感覺，「老實說」框住；1775 年 6 月她 19 歲 | — |
| cannot（t074） | 不能。信說明的是她的態度，不是她說過什麼。 | 通過 | #30 覆核原話 | — |
| you-postcard（t075） | 你寫給媽媽的信，也只能證明你那天在想什麼。 | 通過 | 「你」的旁白 | — |
| rousseau-dies（t076，changes 待查） | 一七七八年，盧梭過世；那本寫到糕點店的書，還沒有印出來。 | 通過 | 法文 WP「Décès 2 juillet 1778」（重抓）；法文 WP〈Les Confessions〉「publication entièrement posthume : en 1782 pour la première partie」（重抓） | — |
| printer（t077） | 四年後的一七八二年，日內瓦印出了它的第一部：盧梭的《懺悔錄》。 | 通過 | CONF-1782 書名頁（重抓）「TOME SECOND, A GENÈVE. M. DCC. LXXXII.」；1778→1782 四年 | — |
| page-six（t078） | 里昂那一段，就在第六卷；同一年在洛桑印的另一個版本，也有這一句。 | 通過 | CONF-1782 p. 181；Lausanne 書名頁「A LAUSANNE, Chez François Grasset & Comp. M. DCC.LXXXII.」、p. 180「qu'ils mangent de la brio-che」（都重抓） | — |
| nameless（t079–t080） | 那書裡這位偉大的公主，是誰？／盧梭沒寫：沒有名字，沒有國家，也沒有年份。 | 通過 | 「une grande Princesse」，整段沒有名字、國別、年代（#2；重抓段落確認） | — |
| queen-reads、neat（t081–t082） | 書印出來的時候，瑪麗．安東尼二十六歲，已經當了八年王后。／這就很妙了：書出來的時候，讀者身邊，正好有一位王后。 | 通過（二手） | WP（重抓）「published when she was 26, eight years after she became queen」；後一句是旁白的反應 | — |
| translation、cake-bit（t083–t084） | 隔年，最早的英文譯本出來了，布里歐被翻成「酥皮點心」；／奇怪的是，同一段裡，這個譯本也把布里歐叫作「一小塊蛋糕」。 | 通過 | CONF-1783（重抓）書名頁 London, J. Bew；pp. 136–137「let them eat pastry」「my dear bit of cake」。「最早」照來源表（沿用） | — |
| pamphlets（t085，changes 待查） | 到了法國大革命，也有人寫文宣罵她。 | 通過 | WP〈Marie Antoinette〉（重抓）「During the French Revolution, she became known as Madame Déficit because the country's financial crisis was blamed on her lavish spending」；WP〈Let them eat cake〉「Anti-monarchists during the French Revolution」。比原 mb411 的「預設有人寫」有更直接的出處 | — |
| missing、odd、you-pamphlet（t086–t088） | 可是研究者說，大革命當時的文宣裡，找不到這句話。／這就很怪了：照這個說法，……／你如果是當年寫小冊子罵她的人，…… | 通過 | WP「Anti-monarchists during the French Revolution never cited this anecdote」（重抓）；照 #21 的上限措辭（研究者說、找不到），反應掛在「照這個說法」底下 | — |
| she-dies（t089，changes 待查） | 一七九三年，她過世了；目前找得到的文字裡，這句話還不在她名下。 | 通過 | WP「16 October 1793」（重抓）；#17、#19（「目前找得到」保留了 Karr 1843「dans le temps」暗示口頭可能更早的空間）。處決只講這一次，不說斷頭台（#37） | — |
| karr（t090，changes 待查） | 直到四十八年後，一八四一年十一月，一位作家卡爾，才把它寫進刊物。 | 通過（記一筆） | KARR 1841 十一月號 p. 61（重抓）；48 年同 t004。「直到…才」是強詞，但緊接在 t089「目前找得到的文字裡」後面，意思是目前找得到的第一筆，可以 | — |
| wasp、hearsay、passing-on（t091–t093） | 刊物叫《黃蜂》。他寫：人家傳說，瑪麗．安東尼講過一句話，／「沒有麵包，就吃布里歐。」不知道是真是假。／注意他的用字：人家傳說、不知真假。卡爾是轉述，不是發明。 | 通過 | KARR 1841（重抓）「le mot vrai ou faux qu'on rapporte de Marie Antoinette : — S'il n'y a pas de pain on mangera de la brioche.」 | — |
| pen-again（t094） | 兩年後，卡爾自己又拿起筆，寫了一篇文章。他寫了什麼？ | 通過（記一筆） | 同 t007（實際約一年半）；「一篇文章」其實是《黃蜂》1843 年那一期裡的一小段，verify-1 通過，不改 | — |
| rumour、which-year（t095–t096） | 那是一八四三年。他回想，當年有人散布謠言，／說她聽到「人民」沒有麵包，就說了那句話；可是「當年」是哪一年，他沒寫。 | 通過 | KARR 1843 p. 260（重抓）「dans le temps … en faisant courir le bruit — que, entendant dire que le peuple était malheureux et qu'il n'avait pas de pain」；只說年份（#18 覆核） | — |
| old-book、duchess（t097–t098） | 接著他說，前幾天，碰巧讀到一本一七六〇年的書，／書裡把同一句話，記在誰身上？一位托斯卡尼的公爵夫人。 | 通過 | 同上「Le hasard m'a fait un de ces jours derniers rencontrer un livre daté de 1760 — où on raconte le même mot d'une duchesse de Toscane」 | — |
| proof、proof-b、rueful（t099–t101） | 卡爾寫：這大致證明，這句話不是瑪麗．安東尼說的，／而是被人找了出來，拿去對付她的。／你看，有意思了：…… | 通過 | 同上「ce qui me paraît prouver à peu près que le mot n'a pas été dit par Marie-Antoinette, mais retrouvé et mis en circulation contre elle」；「大致」「大概」對 à peu près | — |
| no-title（t102–t103） | 那本更老的書，叫什麼名字？／卡爾沒寫書名，我們也沒有找到。 | 通過 | 同上沒有書名；#18 UNOPENED | — |
| people（t104–t105） | 還記得盧梭寫的是「鄉下人」嗎？／到了卡爾筆下，變成了「人民」。 | 通過 | 「les paysans」（CONF-1782 重抓）對「le peuple」（KARR 1843 重抓）；#2 | — |
| sixty-years（t106） | 你看，這句話在路上走了六十年，連聽話的對象都換了。 | 通過 | 1782→1843＝61 年（claims mb610） | — |
| not-over、pastry-1903（t107–t108） | 故事到這裡還沒結束。有沒有哪一份紀錄，寫出了說話的人是誰？／先說一件小事：一九〇三年的英譯本，也還是酥皮點心。 | 通過 | CONF-EN「"Then let them eat pastry!"」（重抓）；兩句前半是 changes 第 7 點的新轉場 | — |
| countess（t109，changes 待查） | 四年後的一九〇七年，一位伯爵夫人的回憶錄出版了。 | 通過（記一筆） | WP〈Adèle d'Osmond〉（重抓）「published in 1907 in an abridged version and in full in 1921」；1903→1907 四年。記一筆：我們核對引文用的 Gutenberg 本是 **1921 年全本**（Émile-Paul），1907 年的是節本，維多利亞夫人那段在不在 1907 年節本裡沒有開書核對（很可能在，但沒看到）。t110「書裡寫出了名字」接在 1907 後面，嚴格講是「這份回憶錄裡」 | （可選）四年後的一九〇七年，一位伯爵夫人的回憶錄開始出版。 |
| victoire、victoire-kind（t110–t111） | 書裡寫出了名字：路易十五的女兒，維多利亞夫人。／伯爵夫人寫她：不太聰明，但是極好心。 | 通過 | BOIGNE 第 II 章章目「Cour de Mesdames, filles de Louis XV. … Madame Victoire」；「Madame Victoire avait fort peu d'esprit et une extrême bonté.」（重抓） | — |
| disette、tears、crust（t113–t115） | 她寫，在一次缺糧的時候，維多利亞夫人聽人說起窮人沒有麵包，／含著眼淚說：「天啊，要是他們肯將就，吃肉派的酥皮，就好了！」／酥皮，就是包在肉派外面的那一層。 | 通過 | 同上「C'est elle qui disait, les larmes aux yeux, dans un temps de disette où on parlait des souffrances des malheureux manquant de pain: «Mais, mon Dieu, s'ils pouvaient se résigner à manger de la croûte de pâté!»」（重抓）；沒有日期（#24） | — |
| kind（t117） | 這個版本裡，說話的人不是冷漠，是好心。 | 通過 | 「une extrême bonté」「les larmes aux yeux」；#24 備註 | — |
| heard-it（t119） | 寫回憶錄的伯爵夫人，一七八一年才出生；這件事，是她聽來的。 | 通過（記一筆） | 編者說明「elle est née le 19 février 1781」、作者自序「Mon premier projet … était uniquement de retracer ce que j'avais entendu raconter à mes parents sur leur jeunesse et la Cour de Versailles」、編者「des faits … survenus pendant son enfance et, parfois même, avant sa naissance」（都重抓）。這次有一手的根據，比 verify-1（WP 二手）穩。記一筆：這一段本身沒寫她是聽誰說的，而且她母親是 Adélaïde 夫人的女官、她嬰兒時就被帶到 Bellevue（同章，重抓），不能排除小時候在場；「是她聽來的」是根據她自己的寫作方式推的 | （可選）寫回憶錄的伯爵夫人，一七八一年才出生；這件事，多半是她聽來的。 |
| late-pen（t120，changes 待查） | 她一八三五年才動筆，寫的時候，已經五十多歲了。 | 通過 | 自序「Au commencement de 1835 … Quelques mois après l'événement」（重抓）；WP「Starting in 1835」；1781-02-19 生，1835 年 53–54 歲 | — |
| cake-later（t121） | 至於蛋糕，是後來才成了那句話最通行的英文譯法。 | 通過（二手） | WP「the traditional translation」（重抓）；#14 覆核「不說英譯原本完全沒有 cake」，這句沒說，而且 t084 已講 1783 有 bit of cake | — |
| rewind（t122） | 倒回去看：一個家教在里昂不敢買麵包，想起一位公主的話； | 通過 | 回收；「倒回去看」是 changes 第 7 點的新轉場 | — |
| rewind-b（t123，changes 待查） | 四十多年後，這段話印進他的書；將近六十年後，才被寫到她名下。 | 通過（記一筆） | 1740→1782＝42 年；1782→1841＝59 年（接在「印進書」之後算）。「才被寫到她名下」少了全片一直保留的「目前找得到」，是強詞；收尾倒帶、前面講過很多次，不致誤導 | （可選）四十多年後，這段話印進他的書；目前找得到最早寫到她名下的，又是將近六十年後。 |
| needed（t124） | 我們覺得，這句話一直在找主人，是因為大家需要一位不知道麵包多貴的公主。 | 通過 | 標成意見（「我們覺得」） | — |
| asks、verdict（t125–t126） | 所以，開頭那個問題：瑪麗皇后真的說過嗎？／她這一輩子有沒有隨口說過什麼，紀錄沒辦法告訴我們。 | 通過 | 不說「她從來沒說過」（S26.md〈給撰稿的提醒〉） | — |
| verdict-b（t127） | 可是，書裡這句話，說的不可能是她。 | 通過（記一筆） | 「不可能」是強詞，但範圍限定在「書裡這句話」：照書裡的敘事，盧梭在 Mably 家（1740–41）就已經「想起」這句話，她 1755 年才出生；就算只看寫作年代（1766–68），她還不到十三歲、沒去過法國（#2、#6、#8、#10）。這個推論不依賴盧梭有沒有記錯年份的細節，成立 | — |
| outro、subscribe（t128–t130） | 這份檔案，存檔。／你第一次聽到這句話，是在哪裡、聽誰說的？留言告訴我。／這個頻道只講紀錄裡找得到的，想一起開檔案，就訂閱。 | 通過 | 片尾，沒有事實 | — |
| youtube.title | 瑪麗皇后真說過「吃蛋糕」？書裡那一天，比她出生早 15 年｜奇聞檔案局 | 通過（記一筆） | 見開頭結論摘要：Mably 家那一年 1740-05-01 到 1741-05（法文 WP 重抓），出生 1755-11-02（WP 重抓），相差 14 年半到 15 年半，年份相減 15；年份來自傳記不是書本身，而且是盧梭憑記憶寫的。旁白 t031、t038–t042 與說明欄都有交代 | 可以照用 |
| youtube.description | 「本集插圖由 AI 生成；畫中的歷史人物都是卡通化的角色，不寫名字、不追求相似；現代研究者不入畫。」 | 要改 | 重做稿的歷史人物一律用固定物件代稱，不畫人像（changes.md〈畫面改了什麼〉「具名的歷史人物一律用固定物件代稱，不畫人像」）；提示詞掃過也是這樣（見下節）。changes.md〈要站主決定的事〉第 5 點也列了這句待改。畫面上的人物只有虛構的研究者 Ada 和無名的一般人 | 本集插圖由 AI 生成；歷史人物不畫人像，用物件代表（例如三角帽、絲扇）；畫面裡的研究者與一般人都是虛構角色。 |
| youtube.description（資料日期） | 「資料截至 2026-10-19（2026-10-25 照新規則重寫）」 | 記一筆 | 2026-11 又重做了一次（順敘、全插圖），這次也重抓了來源（2026-11-13） | （建議）資料截至 2026-10-19，2026-11-13 重新核對（2026-11 照新規則重做）。 |
| youtube.description（其餘） | （全文） | 通過 | 逐句對過：一七七五年麵粉戰爭後的兩封信寫到麵包貴、百姓受苦（ARNETH 重抓）；卡爾一八四一年十一月《黃蜂》「人家傳說、不知道真假」、一八四三年「大致證明」（重抓）；《懺悔錄》第六卷、一七八二年出版、「一位偉大的公主」（重抓）；一七四〇年前後的里昂、早十五年（見標題）；brioche 是奶油雞蛋麵包、1783 與 1903 英譯都是 pastry（重抓）；一七六〇年代後半、第六卷不定年、「十來歲」「還不到十三歲」（#7、#8）；憑記憶寫錯很多、「編的」只是學者懷疑；一七六〇年的書沒有書名；「革命文宣找不到」是研究者的說法、卡爾的「當年」沒寫年份；維多利亞夫人出自 Boigne 回憶錄、是轉述；意見標成看法。說明欄沒有提 1866 年，不受 t064 影響 | 只改上面兩列 |

**其餘全部通過**（逐句看過，都是問句、轉場、點名的回呼、「你」的旁白或旁白的反應，沒有暗含新事實）：t043、t061、t068、t073、t112、t116、t118。

## changes.md 逐條

- **【待查】清單「0 條」**：同意沒有用到查核表以外的事實，但 10 處覆核項目裡有一處算錯：
  - tutor-arrive（t011）「二十八歲」：**要改**。用的是年份相減，盧梭 1712-06-28 生（法文 WP 重抓），1740-05-01 到里昂時 27 歲。
  - queen（t047）：通過（1774-05-10 時 18 歲半）。
  - price-up（t049）：通過（「隔年春天」與「還不到一年」都成立）。
  - rousseau-dies（t076）：通過（1778-07-02，法文 WP 重抓）。
  - pamphlets（t085）：通過，而且英文 WP〈Marie Antoinette〉「During the French Revolution, she became known as Madame Déficit」（重抓）比原 mb411 的預設更直接。
  - she-dies（t089）：通過（「目前找得到的文字裡」守住 #19 的但書）。
  - karr（t090）：通過（記一筆，「直到…才」靠前一句的「目前找得到」撐住）。
  - countess（t109）：通過（記一筆，1907 是節本；我們核對的是 1921 全本）。
  - late-pen（t120）：通過，這次有一手根據（自序 1835、編者 1781-02-19）。
  - rewind-b（t123）：通過（記一筆，少了「目前找得到」）。
- **changes.md 沒列、但這次改寫碰到的**：
  - thirty-shops（t020）與 alone-errand（t021）：**要改（事件順序）**。順敘以後用「所以」「最後」把三十家糕點店放在想起公主之前，跟原文相反；第一版 mb806–mb808 就是這個順序，verify-1 沒抓到。
  - invented（t041）：**要改**。「糕點店這段故事」是這次加的，WP 說可能是編的是公主那則軼事。
  - empress（t064）：**要改**。第一版 mb303 就有，claims.md〈待查〉也點名要覆核；重抓 ARNETH 書名頁與兩篇序，1866 是第二版。
- **第 6 點〈刪掉的句子〉**：逐條看過（mb110、mb313、mb408、mb509–mb510、mb801 的「還記得」、mb815），都不是保留「可能」「據說」「目前找得到」的地方，沒有把但書刪掉。mb509「比卡爾早將近六十年」刪掉後，這個數字移到 t123，算術一樣對。
- **第 7 點〈新寫的轉場句〉**：t016、t032、t033、t058、t107、t108、t122 都通過；其中 t033 帶了一個數字（「二十多年後」），算術對（見判定表）。
- **第 8 點（旁白的反應都交給 Ada）**：t060、t071、t082、t087、t101、t124 的「我覺得」「老實說」「這就很妙了」「這就很怪了」「你看，有意思了」「我們覺得」都還在，意見都有標。
- **第 2 點（鉤子講得懂）**：t001–t007 逐句看過都通過；t005 的「十五年」與 t007 的「兩年後」記一筆（見判定表）。
- **〈要站主決定的事〉**：第 1、3、4、6、7 點不屬於查核，略；第 2、8 點見下一節；第 5 點的 `youtube.description` 就是上面要改的那一句。

## 畫面與規則（只影響畫面，記一筆）

- 在世或 1956 年後過世的人：124 個提示詞裡**沒有**任何真人的名字，也沒有寫歷史人物的臉或肖像。歷史人物都用物件代稱（三角帽、淺藍絲扇、搖籃等），研究者（Fraser、Johnson、Trousson）都沒有入畫；
  有人的景只有虛構的 Ada 和無名的一般人（「你」的六個現代人、麵包店老闆娘、抱空籃的母親、市場婦人、學徒、群眾、印刷工、寫小冊子的年輕人、說閒話的婦人）。
- 只畫手或腳的景：must-eat、buys-brioche、alone-errand、sixty 是盧梭（棕色袖口、三角帽），duty 是王后（淺藍蕾絲袖口），都過世超過兩百年，不在規則範圍內；changes.md 第 8 點已經提了 duty 要不要換成無人的封蠟信。
- 如果 t020 照建議調順序，peek（老闆娘遞出布里歐）、buys-brioche（拿起布里歐）會排在 thirty-shops 前後，畫面不用重畫；peek 遞的是布里歐，正好對上原文的「ma chère petite brioche」。
- sixty 畫的是「old wrinkled hand」：盧梭寫第六卷時 54–56 歲、自稱快六十，畫成老人的手跟旁白一致。
- 章名順手看了：「一九〇七年，一份寫出名字的回憶錄」同 t109（1907 是節本）；其他章名的年份（一七四〇、一七六〇年代後半、一七七五、六月二十二日、一七八二、一八四一年十一月、一八四三）都對。
- lint 目前 0 警告，開場長度沒有問題，不需要開場補句。

## 要改的句子清單

- tutor-arrive（t011）｜一個二十八歲的年輕人來到這裡，住進憲兵總監的家。｜一個二十七歲的年輕人來到這裡，住進憲兵總監的家。
- thirty-shops（t020）｜所以他在街上走，走過三十家糕點店，還是不敢推門。｜可是就連買布里歐也不容易：他會走過三十家糕點店，還是不敢推門。（連同 t021–t023 移到 t026 之後）
- alone-errand（t021）｜他一個人出門，就是為了這一塊麵包；有時候跑遍全城。｜他一個人出門，就是為了這一塊布里歐；有時候跑遍全城。
- buys-brioche（t026）｜他把這句話當成不得已的辦法，買了布里歐。｜他把這句話當成不得已的辦法：改買布里歐。（跟著順序調；新順序是 t019 → t024 → t025 → t026 → t020 → t021 → t022 → t023 → t027）
- invented（t041）｜也有學者懷疑，糕點店這段故事，根本是他編的。｜也有學者懷疑，那位公主的故事，根本是他編的。
- empress（t064）｜媽媽，是奧地利的女皇瑪麗亞．特蕾莎；這些信到一八六六年才整批印出來。｜媽媽，是奧地利的女皇瑪麗亞．特蕾莎；這些信要到一八六〇年代，才印成書。
- `youtube.description`｜本集插圖由 AI 生成；畫中的歷史人物都是卡通化的角色，不寫名字、不追求相似；現代研究者不入畫。｜本集插圖由 AI 生成；歷史人物不畫人像，用物件代表（例如三角帽、絲扇）；畫面裡的研究者與一般人都是虛構角色。

旁白以外的事（本輪沒有改）：

- `video.json` 的 `sources` 第 8 條（ARNETH）寫「Leipzig 1866」，建議補成「第二版（Zweite vermehrte Auflage），Leipzig 1866；第一版序署 1864 年 12 月」，免得下一個人再把 1866 當成首次出版。
- `claims.md` 的行號還是舊的 mb101–mb918，跟這次的 t001–t130 對不上；mb303（1866）、mb704（1740 年二十八歲）、mb806–mb808（順序）、mb813 的依據要照上面更新。
- `verify-1.md` 第 39 列備註「盧梭 1712 年生」可以補上「6 月 28 日」，第 6 列可以補一句「1740-05 到 1741-05，相對 1755-11 是 14 年半到 15 年半」；下一次重抄 verify 表時處理。
- t020 調順序時，`script.md` 的時間碼和 `structure-map.md` 要跟著重產；`loops` 裡 t024→t025 仍相鄰，t025→t104 不受影響。
