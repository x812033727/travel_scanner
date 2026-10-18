# curio-h02-v2 查核第一輪

- 查核 2026-10-13，Claude Opus 5（獨立查核代理，**不是**寫這份腳本的那一個；這一版的
  `video.json`、`claims.md`、`brief.md`、`NOTES.md` 都不是我寫的，我也沒有改動其中任何一個）。
- 這一集在本倉庫沒有第一版，腳本是直接照 `../history-curiosity/topic-checks/H02.md`
  （2026-10-10 查核、同日另一個代理獨立覆核，處置 ADOPT_WITH_CHANGES）與
  `claims.md` 寫成的，所以這一輪是上機前唯一的一道關。
- 方法：
  1. 先把 `video.json` 的每句旁白（`text`；全檔沒有任何 `say`／`say_for`，所以沒有第二種唸法要查）、
     每張卡片的每個 `data` 欄位、七個章名、標題、說明欄、十個標籤、縮圖文字、`sources[]`
     與 `loops[]` 抽成 234 條清單（旁白 131、卡片欄位展開後 54 個字串、章名 7、標題 1、說明欄 5 段、
     標籤 10、縮圖 3、`sources[]` 19、`loops[]` 4），行 id 照原樣保留，存在
     `<scratch>\verify-h02\claims-list.txt`（抽取腳本與原始網頁、PDF 文字存在同一個資料夾）。
  2. 每一條去對 `claims.md` 的 c1–c45，再把每一列對回 H02.md 的逐項查核表。
  3. H02.md 判 DISPUTED／CHANGED 的那幾列、以及腳本裡的每個數字、年份與引述，當天用 curl 重開來源
     （User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔
     1.2 秒以上；兩本 Gutenberg 讀全文檔，兩個 PDF 用 `pdftotext -layout` 抽文字後比對）。
     引句一字一字比對，共核 90 條引句與數字；名單的 119 個名字我自己重數一次。
  4. 網路搜尋用了 1 次（上限 5）：查 2026-06-04 那則「找到了」有沒有第三方的評估或回應，沒有找到；
     找到的都是 2015–2020 年的報導。另外多開了基金會自己最新的一則新聞（FCF2），確認那是 2024-08-14
     一只銅耳飾的檢驗，跟 Site X／Site Y 的宣告無關。
- 這是歷史題：「官方頁」指一手或權威的來源。最重的是 Gutenberg 轉錄的 Hakluyt 卷 13 所收懷特
  1587、1590 兩篇記述（唯一的目擊紀錄）與 Lawson 1709；其次是美國國家公園管理局三頁、
  Encyclopedia Virginia、Britannica 兩頁、NCpedia 三頁；報導層是 Smithsonian 2017／2020、
  National Geographic 2015、WHRO 2025、Coastal Review 2020、NCLR 書評；基金會自己的網頁只當
  「他們自己說」用。樹輪那篇論文的全文頁（science.org）我沒有開——H02.md 記它對機器回 403、
  沒有可用存檔，摘要在 NCBI 的官方介面上核對，我也照這條路走。
- `assets[]` 是空的、這一集沒有照片卡，所以 H02.md 的六張公有領域圖與兩張未核准的圖都沒有入稿，
  這一輪沒有圖片授權要查。站主要決定的那三件（大英博物館那兩張、1876 年版畫）這一版都沒用到。
- 我沒有跑 git、沒有跑任何影片階段、沒有花任何提供者的錢。腳本有問題的地方一律寫在下面，
  **沒有動 `video.json`**。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| HAK | https://www.gutenberg.org/ebooks/25645 | 200 |
| HAK-txt | https://www.gutenberg.org/cache/epub/25645/pg25645.txt （實際比對引句用的全文檔） | 200 |
| LAW | https://www.gutenberg.org/ebooks/1838 | 200 |
| LAW-txt | https://www.gutenberg.org/cache/epub/1838/pg1838.txt | 200 |
| NHC | https://nationalhumanitiescenter.org/pds/amerbegin/exploration/text6/white.pdf | 200 |
| NPS87 | https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm （頁面標 Last updated: September 20, 2026） | 200 |
| NPS90 | https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm （Last updated: August 14, 2026） | 200 |
| NPSth | https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm （Last updated: July 11, 2025） | 200 |
| EV | https://encyclopediavirginia.org/entries/roanoke-colonies-the/ | 200 |
| EBp | https://www.britannica.com/place/Lost-Colony | 200 |
| EBs | https://www.britannica.com/story/the-lost-colony-of-roanoke （`claims.md` 用它，但不在 `sources[]` 裡，見 #9） | 200 |
| NCp | https://www.ncpedia.org/lost-colony | 200 |
| NCpC | https://www.ncpedia.org/croatoan-indians | 200 |
| NCpD | https://www.ncpedia.org/dare-stones | 200 |
| SM17 | https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/ | 200 |
| SM20 | https://www.smithsonianmag.com/smart-news/new-evidence-roanoke-colonys-disappearance-180976248/ | 200 |
| NG | https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology | 200 |
| WHRO | https://www.whro.org/arts-culture/2025-01-20/new-artifacts-on-hatteras-point-to-the-real-fate-of-the-lost-colony （Published January 20, 2025） | 200 |
| FCF | https://www.firstcolonyfoundation.org/news/lost-colony-is-found/ （`article:published_time` 2026-06-04T18:48Z） | 200 |
| FCF2 | https://www.firstcolonyfoundation.org/news/scientific-tests-confirm-archaeology-discovery/ （這一輪多開的：2024-08-14，銅耳飾，與 Site X／Y 無關） | 200 |
| CR20 | https://coastalreview.org/2020/10/lost-colony-moved-inland-archaeologists/ | 200 |
| NCLR | https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf | 200 |
| SCI | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text | 200 |

沒有開：https://www.science.org/doi/10.1126/science.280.5363.564 （H02.md 記 403、無可用存檔；
摘要讀 SCI 那一列）。沒有開 Commons 的圖片頁（這一集沒有照片）。

## 主張表

判定：CONFIRMED 看到了／CHANGED 要改／NOT FOUND 沒看到，拿掉或換掉／OUT OF SCOPE 風格、問句、
系列安排與明示的意見，不動。「c」是 `claims.md` 的列號。

| # | 主張 | 位置 | claims | 來源 | HTTP | 判定 | 要改成 |
|---|---|---|---|---|---|---|---|
| 1 | 標題「羅阿諾克『消失的殖民地』：CROATOAN 到底是什麼意思？」 | youtube.title | — | 與 H02.md 題目卡的 title 一字不差 | — | CONFIRMED | — |
| 2 | 說明欄第一段：1590-08-18 天剛亮、放下小船、吹號唱歌沒人回應、樹皮上三個大寫字母、木樁離地五英尺一整個字、字上沒有十字、總督寫下他反而很高興 | youtube.description ¶1 | c1–c5 | HAK-txt、NPS90、EBp | 200 | CHANGED | 「吹號、唱歌」的次序與「樹皮」兩處要跟著 #16、#19 一起改（見那兩列） |
| 3 | 說明欄第二段的目錄：三年前為什麼留下、聯名證明、約好的記號與沒加上去的十字、**無敵艦隊那一年補給為什麼開不出去**、四個錨只剩一個、1709 年的轉述、名字怎麼在十九世紀長出來、八百年大旱、驗出黃銅的戒指、兩支團隊方向相反的宣稱 | youtube.description ¶2 | c13–c17、c22、c26、c29、c32、c34、c42 | EV：1588-04-22 兩艘補給船**確實開出去了**（the Brave 與 the Roe，「Despite a prohibition on all English ships leaving port」），是在海上「a fight at sea with the French left the ships limping back to England」；旁白 ro304 自己也這樣講 | 200 | CHANGED | 「補給為什麼開不出去」→「補給為什麼送不到」 |
| 4 | 說明欄第三段：流傳的版本一律標明後來加的、來源不一致就說不一致、沒有定論就說沒有定論、出處列在下方參考資料 | youtube.description ¶3 | — | 與腳本實際做法一致（傳說標成後來的見 #77、來源不一致並列見 #36、沒有定論見 #128 與 #131）；「下方參考資料」由 `composeDescription` 在上架時把 `sources[]` 接到說明欄後面（`tools/video/core/compilation.mjs` 的 `descriptionWithinBudget`），與 curio-h01 同一寫法 | — | CONFIRMED | — |
| 5 | 說明欄第四段：插圖由 AI 生成、歷史人物卡通化、不寫名字、不追求相似、在世或近代人物不入畫，只用一般角色從背後或遠處表示 | youtube.description ¶4 | — | 逐個 `prompt` 核過：現代的考古學家與工作人員都是 seen from behind（`back-to-digging`、`society-2009`、`other-direction`、`two-sites`、`nps-page`、`british-museum-map`），沒有一張寫名字，卡片上的字也沒有人名 | — | CONFIRMED | — |
| 6 | 「資料截至 2026-10-10」 | youtube.description ¶5 | — | `sources[]` 十九筆的 `checked_on` 都是 2026-10-10；我這一輪是 2026-10-13 重開，結果見本表 | — | CONFIRMED | — |
| 7 | 十個標籤（羅阿諾克、失落的殖民地、CROATOAN、歷史懸案、約翰懷特、未解之謎、哈特拉斯島、外灘、北美殖民、奇聞檔案局） | youtube.tags | — | 都是題材詞，沒有宣稱 | — | OUT OF SCOPE | — |
| 8 | 縮圖「他反而／**高興**」「歷史懸案」「一五九〇年的檔案」 | thumbnail | c5 | HAK-txt「yet on the other side I greatly ioyed」；1590 年的事 | 200 | CONFIRMED | — |
| 9 | `sources[]` 十九筆、checked_on 2026-10-10 | sources | — | 十九個網址我這天全部重開，都是 200。但 `claims.md` c28、c31 引的 Britannica 故事頁（EBs）**不在 `sources[]` 裡**；說明欄的參考資料是由 `sources[]` 自動接上的，所以觀眾看不到那一條 | 200 | CHANGED | `sources[]` 補一筆 EBs（https://www.britannica.com/story/the-lost-colony-of-roanoke ，checked_on 2026-10-10）；或把 ro410 的出處改掛 NCp 與 WHRO（見 #77） |
| 10 | `loops[]` 四組（ro111→ro223 沒有十字、ro107→ro409 三個字母、ro101→ro212 八月十八日、ro323→ro604 五十英里） | loops | — | 四個 setup／payoff 的 id 都在檔內，講的事與各自那一列一致 | — | CONFIRMED | — |
| 11 | 六個章名：他們吹了號島上沒有人回應／他們簽了一張紙請總督回英格蘭／一七〇九年有人說祖先是白人／島上的土裡挖出一只戒指／地圖的補丁底下有一個堡壘的記號／沒有遺骸也沒有能確定的房子 | scenes[].chapter | c2–c3、c13、c26、c34、c40、c43 | HAK-txt、NCp、NPSth、SM17 | 200 | CONFIRMED | — |
| 12 | 章名「無敵艦隊那一年，他的補給出不了港」 | war-at-home.chapter | c16、c17 | 同 #3：補給船開出去了，是交戰後折返 | 200 | CHANGED | 「無敵艦隊那一年，他的補給送不到島上」 |
| 13 | 一五九〇年八月十八日，天剛亮 | ro101 | c1 | NPS90「Landing on August 18, 1590」；HAK-txt「we therefore landed at day-breake」 | 200 | CONFIRMED | — |
| 14 | 一艘英格蘭船在羅阿諾克島外放下小船 | ro102 | c1 | HAK-txt：小船是從 Hatorask（外灘的水道口）放的，「we put off from Hatorask, being the number of 19 persons in both boates」，兩艘船在那裡；EV 寫 1590 年「four ships finally sailed for Roanoke」 | 200 | CONFIRMED（建議收緊，見文末〈建議〉1） | — |
| 15 | 三年前，船上那個畫地圖的人把人留在這裡 | ro103 | c8 | NCp「artist John White」；FCF「drawn for Raleigh by the artist John White」；NG「Governor John White's 1585 map」；1587-08-27→1590-08-18 | 200 | CONFIRMED | — |
| 16 | 上岸以後，他們吹號，唱英格蘭的歌 | ro104 | c3 | HAK-txt 的次序**相反**：「we let fall our Grapnel neere the shore and sounded with a trumpet a Call, and afterwardes many familiar English tunes and Songs, and called to them friendly; but we had no answere, **we therefore landed at day-breake**」——吹號、唱歌在船上，沒有回應才上岸；NPS90 沒有提號聲，唯一的來源就是這一段 | 200 | CHANGED | 「靠岸之前，他們吹號，唱英格蘭的歌。」 |
| 17 | 沒有人回應 | ro105 | c2、c3 | HAK-txt「but we had no answere」；NPS90「no signs of life」 | 200 | CONFIRMED | — |
| 18 | 聚落裡只剩下他們留下的東西 | ro106 | c2 | NPS90「found remnants of the colonists but no signs of life」；HAK-txt（鐵條、鉛塊、四門小砲、被挖開的箱子） | 200 | CONFIRMED | — |
| 19 | 一棵樹的**樹皮**上，刻著三個大寫字母 | ro107 | c4 | HAK-txt 寫樹是「vpon a tree, in the very browe thereof were curiously carued these faire Romane letters C R O」——**沒有**提樹皮；「had the barke taken off」是木樁那一根的特徵。這一集的立論就靠樹與木樁分得清楚，把「剝了皮」挪到樹上會把它糊掉 | 200 | CHANGED | 「一棵樹上，刻著三個大寫字母。」 |
| 20 | 再往前，柵欄入口有一根木樁被剝了皮 | ro108 | c4 | HAK-txt「one of the chiefe trees or postes at the right side of the entrance had the barke taken off」 | 200 | CONFIRMED | — |
| 21 | 離地五英尺，刻著一整個字 | ro109 | c4 | HAK-txt「5 foote from the ground in fayre Capitall letters was grauen CROATOAN」 | 200 | CONFIRMED | — |
| 22 | 卡片「CROATOAN／柵欄的木樁上／離地五英尺」 | the-word.data | c4 | 同上；EBp「the word CROATOAN carved on a post of the palisade erected by the settlers and the letters CRO on a tree」 | 200 | CONFIRMED | — |
| 23 | 那個字是克羅托安 | ro110 | c4 | 同上 | 200 | CONFIRMED | — |
| 24 | 字的上面，沒有十字 | ro111 | c4、c15 | HAK-txt「grauen CROATOAN **without any crosse or signe of distresse**」 | 200 | CONFIRMED | — |
| 25 | 他後來寫下，看到這個字，他反而很高興 | ro112 | c5 | HAK-txt「but although it much grieued me to see such spoyle of my goods, yet on the other side **I greatly ioyed** that I had safely found a certaine token of their safe being at Croatoan」；旁白用「他後來寫下」帶，attribution 在 | 200 | CONFIRMED | — |
| 26 | 這個字是什麼意思，為什麼讓他高興？ | ro113 | — | 問句 | — | OUT OF SCOPE | — |
| 27 | 他高興，是因為那個字是**他自己留下**的約定 | ro201 | c5、c15 | HAK-txt 是雙方約的：「a secret token agreed vpon **betweene them and me** at my last departure from them」；ro220「他跟他們約好一個記號」有把它補回來 | 200 | CONFIRMED（建議收緊，見〈建議〉2） | — |
| 28 | 這個人叫約翰．懷特，他是這批人的總督 | ro202 | c8 | NPS87 引殖民者的證明「John White, Governor of the planters in Virginia」；EBp「approximately 100 settlers under **Gov.** John White」 | 200 | CONFIRMED | — |
| 29 | 一五八七年七月二十二日，他們在外灘靠岸 | ro203 | c6 | HAK-txt「The two and twentieth of Iuly wee arriued safe at Hatorask」 | 200 | CONFIRMED | — |
| 30 | 本來要去的是北邊的乞沙比克灣 | ro204 | c7 | HAK-txt「the Bay of Chesepiok where we intended to make our seate and forte」；NPS87「intended to make a new colony in the Chesapeake Bay」 | 200 | CONFIRMED | — |
| 31 | 他們要在那裡蓋房子和堡壘 | ro205 | c7 | 同上（「seate and forte」＝聚落與堡壘） | 200 | CONFIRMED（建議，見〈建議〉3） | — |
| 32 | 可是領航員不肯再往北走 | ro206 | c7 | EV「Fernandes served as chief pilot」；HAK-txt「Vnto this were all the saylers... perswaded by the Master」「the Master of our Admirall Ferdinando」；NPS87 稱他「the fleet's captain, Simon Fernandes, refused to take the colonists farther up the coast」 | 200 | CONFIRMED | — |
| 33 | 一百多個英格蘭人就留在了羅阿諾克 | ro207 | c9 | EBp「approximately 100」、SM17 與 NG「115」、EV「117」、NPS87「118」、NPSth「117 people」、NCp「approximately 150」、WHRO「More than 100 colonists」——「一百多」是這個範圍裡站得住的講法，沒有挑單一數字 | 200 | CONFIRMED | — |
| 34 | 名單上的名字一共一百一十九個 | ro208、count-stats.stats[0] | c9 | HAK-txt「The names of all the men, women and children, which safely arriued in Virginia, and remained to inhabite there. 1587.」我自己重數：男 91、女 17、男孩 9、當地出生 2＝119（「Henry Rufoote Richard Tomkins」之間漏了一個句點，機器切成一個名字，實際是兩個） | 200 | CONFIRMED | — |
| 35 | 卡片註「含後來**離開**的三個」 | count-stats.stats[0].note | c9 | 那三個是懷特、領航員 Simon Fernando 與 George How。前兩個是離開；George How（十二位 Assistant 之一）是 1587-07-28 在島上被殺（HAK-txt），不是離開。H02.md 也要求不畫、不細講他的死 | 200 | CHANGED | 「其中三個沒有留下」（不必提死因，也不再說三個都是離開） |
| 36 | 各家來源寫的，從大約一百到一百五十 | ro209、count-stats.stats[1] | c9 | 同 #33（下界 EBp、上界 NCp） | 200 | CONFIRMED | — |
| 37 | 卡片出處「Hakluyt、NPS、Britannica 2026-10-10」 | count-stats.source | c9 | 三者都用到了 | 200 | CONFIRMED | — |
| 38 | 舊堡壘被夷平，空屋長滿瓜，鹿在裡面吃 | ro210 | c10 | HAK-txt「we found the fort rased downe, but all the houses standing vnhurt, sauing that the neather roomes of them, and also of the forte, were ouergrowen with Melons of diuers sortes, and Deere within them, feeding on those Melons」 | 200 | CONFIRMED | — |
| 39 | 八月十八日，總督的外孫女在島上出生 | ro211 | c11 | HAK-txt「The 18 Elenor, daughter to the Gouernour... was deliuered of a daughter in Roanoak」；旁白沒有講她的名字（照 H02.md 不碰血統說法） | 200 | CONFIRMED | — |
| 40 | 還記得他上岸那天是八月十八日嗎／那天剛好是她三歲生日 | ro212、ro213 | c12 | NCp「On 18 August, the third birthday of his granddaughter, colonist Virginia Dare, White once again landed on Roanoke」 | 200 | CONFIRMED | — |
| 41 | 四天後，全體殖民者找上他 | ro214 | c13 | HAK-txt「The next day, the 22 of August, the whole company both of the Assistants and planters came to the Gouernour」（8/18＋4） | 200 | CONFIRMED | — |
| 42 | 他們要他回英格蘭，親自把補給帶回來 | ro215 | c13 | HAK-txt「with one voice requested him to returne **himselfe** into England, for the better and sooner obtaining of supplies」 | 200 | CONFIRMED | — |
| 43 | 他先拒絕了 | ro216 | c13 | HAK-txt「but he refused it, and alleaged many sufficient causes」「he not once, but often refusing it」 | 200 | CONFIRMED | — |
| 44 | 八月二十五日，他們立下一張聯名的證明 | ro217 | c13 | HAK-txt：證明全文，署「the 25 of August 1587」，「vnder all their handes and seales」 | 200 | CONFIRMED | — |
| 45 | 兩天後的早上，他上了船 | ro218 | c14 | HAK-txt「departed from Roanoak the seuen and twentieth of August **in the morning** and the same day **about midnight, came aboord the Flieboat**」——早上離開羅阿諾克，上船是當天半夜 | 200 | CONFIRMED（建議，見〈建議〉4） | — |
| 46 | 那時候外孫女出生才九天 | ro219 | c14 | 8/18→8/27 | 200 | CONFIRMED | — |
| 47 | 臨走前他跟他們約好一個記號／搬去哪裡就把地名刻下來／有危險就在字上面加一個十字 | ro220、ro221、ro222 | c15 | HAK-txt「a secret token agreed vpon betweene them and me」「they should not faile to write or carue on the trees or posts of the dores the name of the place where they should be seated」「they should carue ouer the letters or name, a Crosse + in this forme」。只有懷特一個目擊來源（1593 年才寄出），旁白用「他跟他們約好」帶 | 200 | CONFIRMED | — |
| 48 | 還記得木樁上那個字沒有十字嗎／照他們的約定，沒有十字就是平安 | ro223、ro224 | c15 | HAK-txt「but we found no such signe of distresse」＋「a certaine token of their safe being at Croatoan」 | 200 | CONFIRMED | — |
| 49 | 他以為自己很快就會回來 | ro225 | 〈不是主張〉 | 旁白用「他以為」標明是推想 | — | OUT OF SCOPE | — |
| 50 | 可是他一離開，英格蘭就打起仗來 | ro301 | （無對應列） | EV：女王「**had been** fighting the Spanish on the seas and in the Netherlands」——他走之前就在打了；1588 年發生的是無敵艦隊與禁止出港（NPS90）。SM17 的「his return was delayed by the outbreak of war with Spain」是報導的簡寫，不足以把開戰放在他離開之後 | 200 | CHANGED | 「可是那幾年，英格蘭正在打仗。」 |
| 51 | 一五八八年，西班牙的無敵艦隊來了 | ro302 | c16 | NPS90「The Spanish Armada... was preparing to attack England directly」；NCp「The Spanish Armada of 1588」 | 200 | CONFIRMED | — |
| 52 | 女王下令，所有英格蘭船留在本土待命 | ro303 | c16 | NPS90「Queen Elizabeth I ordered all English vessels to remain nearby in defense of the homeland」 | 200 | CONFIRMED | — |
| 53 | 那年四月出發的補給船，跟法國人交戰後折返 | ro304 | c17 | EV「a two-ship relief mission that sailed on April 22, 1588... But a fight at sea with the French left the ships limping back to England」 | 200 | CONFIRMED | — |
| 54 | 補給就這樣一直沒有送到島上／卡片「1587 他離開那一年、1590 他回到島上那一年」 | ro305、delay-stats.data | c18 | HAK-txt、NPS90 | 200 | CONFIRMED | — |
| 55 | 再上岸那天，他想往南邊走 | ro306 | c22 | NPS90「White immediately began to sail to Croatoan」；HAK-txt「which letters presently we knew to signifie the place, where I should find the planters seated」 | 200 | CONFIRMED | — |
| 56 | 刻的那個地名，是南邊外灘上的一座島／就是今天的哈特拉斯島一帶／島上住的是克羅托安人 | ro307、ro308、ro309 | c19 | NPSth「Croatoan (present-day Hatteras Island)」「The Croatoan people lived on Croatoan (Hatteras Island)」；NCpC；SM17「Roanoke Island, 50 miles north of Hatteras」。旁白說「一帶」，沒有把族人的島等同整座島 | 200 | CONFIRMED | — |
| 57 | 懷特自己寫，那是他們的朋友 | ro310 | c21 | HAK-txt「the Sauages of the Iland **our friends**」；attribution 在 | 200 | CONFIRMED | — |
| 58 | 不過他們上岸那年的八月，英格蘭人才誤襲過他們一次 | ro311 | c21 | NPS87「In retaliation, White and his men attacked what they thought were Roanoke people... Instead, they attacked friendly Croatoan people」；HAK-txt 同一段（1587 年 8 月）；NPSth 另寫他們起初不願跟英格蘭人交易 | 200 | CONFIRMED | — |
| 59 | 他為什麼沒有過去？ | ro312 | — | 問句 | — | OUT OF SCOPE | — |
| 60 | 船上四個錨只剩下一個／他自己寫天氣一天比一天壞 | ro313、ro314 | c22 | HAK-txt「wee had but one Cable and Anchor left vs of foure, and the weather grew to be fouler and fouler」 | 200 | CONFIRMED | — |
| 61 | 淡水桶還丟在岸上，沒搬回船 | ro315 | c22 | HAK-txt「all our Caske ready filled they left behinde」「to leaue that Caske with fresh water on shoare in the Iland vntill our returne」「our caske and fresh water lost」 | 200 | CONFIRMED | — |
| 62 | 他們決定先南下補水、過冬，明年再回來 | ro316 | c23 | HAK-txt「it was therefore determined that we should goe for Saint Iohn or some other Iland to the Southward for fresh water... we should continue in the Indies all the Winter following... and at our returne to visit our countreymen at Virginia」 | 200 | CONFIRMED | — |
| 63 | 八月二十八日，一場風暴把船吹向亞速群島 | ro317 | c23 | HAK-txt「On the 28. the winde changed... blewe so forcibly, that wee were able to beare no sayle... wee were driuen to change our first determination for Trynidad, and stoode for the Ilands of Açores」 | 200 | CONFIRMED | — |
| 64 | 然後他們就回了英格蘭／那座島，沒有人走到 | ro318、ro319 | c23 | 同上；NPS90「he was forced to return to England, never knowing what became of the Lost Colony」。旁白只說「沒有人走到」，沒有把南邊的距離講成約好的五十英里（H02.md 明令分開講） | 200 | CONFIRMED | — |
| 65 | 那次道別之後，沒有紀錄說英格蘭人再見過他們 | ro320 | c25 | NCp「His departure marked **the last known contact** between the English and their colony in America」 | 200 | CONFIRMED | — |
| 66 | 不過懷特自己的記述裡，還有一件事說不通 | ro321 | — | 敘述轉折 | — | OUT OF SCOPE | — |
| 67 | 他寫過，他們準備搬到內陸五十英里 | ro322 | c24 | HAK-txt（1590 篇）「for at my comming alway they were **prepared to remoue from Roanoak 50 miles into the maine**」；1587 篇另有「they intended to remoue 50 miles further vp into the maine presently」 | 200 | CONFIRMED | — |
| 68 | 先記住這個數字，等一下它會回來 | ro323 | — | loop 的 setup | — | OUT OF SCOPE | — |
| 69 | 可是木樁上刻的，不是內陸的方向 | ro324 | c24 | 克羅托安在南邊的外灘（#56）；HAK-txt 兩句並在一段裡 | 200 | CONFIRMED | — |
| 70 | 南邊那座島上的人，後來講過一件事／一七〇九年，一個旅行的人把它寫下來 | ro401、ro402 | c26 | LAW-txt（1709 年《A New Voyage to Carolina》）「A farther Confirmation of this we have from the Hatteras Indians, who either then lived on Ronoak-Island, or much frequented it」 | 200 | CONFIRMED | — |
| 71 | 哈特拉斯人跟他說，祖先裡有幾個是白人 | ro403 | c26 | LAW-txt「These tell us, that several of their Ancestors were white People」 | 200 | CONFIRMED | — |
| 72 | 還會像**他們**一樣，對著一本書說話 | ro404 | c26 | LAW-txt 是「and could talk in a Book, **as we do**」——「we」是勞森那邊的英格蘭人。前一句的主語是哈特拉斯人，「像他們一樣」最自然的讀法會把意思反過來 | 200 | CHANGED | 「還會像英格蘭人一樣，對著一本書說話。」 |
| 73 | 這是很久以後的轉述，而且只有這一份 | ro405 | c26 | 1709 年＝事後一百二十年；H02.md 與我都只找到勞森一份 | 200 | CONFIRMED | — |
| 74 | 另一個說法更可怕：他們被內陸的大酋長下令殺了／寫下這個說法的人是聽別人說的 | ro406、ro407 | c27 | EV「the Virginia colony's secretary, William Strachey, suggested that the paramount chief Powhatan had ordered them killed」；NCLR「Strachey presents second-hand information」。旁白當「一個說法」講、不給年份、不點名，照 H02.md 的禁令 | 200 | CONFIRMED | — |
| 75 | 而我們今天記得的，是另外一句話 | ro408 | — | 敘述轉折 | — | OUT OF SCOPE | — |
| 76 | 還記得**樹皮**上那三個大寫字母嗎 | ro409 | c4 | 同 #19 | 200 | CHANGED | 「還記得樹上那三個大寫字母嗎？」 |
| 77 | 可是傳到後來，變成樹上刻著一個字 | ro410 | c28 | EBs「The word CROATOAN and the letters CRO, **carved into trees** within the colony's borders」；NCp 也寫成「the word 'CROATOAN' cut into a **tree or post** of a palisade」；WHRO 引發掘方自己轉述流傳版：「they left behind this cryptic message **on a tree**, 'Croatoan'」 | 200 | CONFIRMED | — |
| 78 | 誰最先這樣講，今天查不到 | ro411 | c28 | H02.md 查不到，我這一輪也沒找到 | — | CONFIRMED | — |
| 79 | 更怪的是，連這個案子的名字也是後來才有的 | ro412 | c29 | SM20、NCLR | 200 | CONFIRMED | — |
| 80 | 一八三〇年代，**美國的歷史書**開始這樣寫它 | ro413 | c29 | SM20 說的是「when **a book and a magazine article** cast the settlement as a 'romantic mystery'」，沒有說是歷史書；指名 Bancroft 1834 年美國史的是 Coastal Review 2018 那篇，既不在 `sources[]`、也不在 c29 的出處裡 | 200 | CHANGED | 「一八三〇年代，一本書和一篇雜誌文章這樣寫它。」（或把 Coastal Review 2018 那條補進 `sources[]` 與 c29） |
| 81 | 一八三七年一本小說，看起來是最早用這個名字的 | ro414 | c29 | NCLR「Eliza Lanesford Cushing's 1837 story『Virginia Dare; or, the Lost Colony: A Tale of the Early Settlers.』The authors point out that Cushing『appears to be the first to name the 1587 planters as "The Lost Colony"』」；「看起來是」保住了來源的餘地 | 200 | CONFIRMED | — |
| 82 | 卡片「失落的殖民地／這個名字／一八三〇年代才出現」 | lost-colony-name.data | c29 | SM20「only got its start in the 1830s」；NCLR 的 1837 也落在這十年 | 200 | CONFIRMED | — |
| 83 | 表格「後來加上去的」1709 旅行作家 白人祖先／1837 小說 這個名字／1937 刻字石 四十幾塊 | added-later.rows[0,2,4] | c26、c29、c31 | LAW-txt、NCLR、NCpD | 200 | CONFIRMED | — |
| 84 | 表格列「1830s／**歷史書**／浪漫懸案」 | added-later.rows[1] | c29 | 同 #80（「浪漫懸案」對得上 SM20 的「romantic mystery」，「歷史書」沒有來源） | 200 | CHANGED | 誰欄「歷史書」→「一本書和一篇文章」 |
| 85 | 表格列「1937／戶外劇／**每年上演**」 | added-later.rows[3] | c30 | NCLR 只寫「The year 1937, the time of the premiere of Paul Green's outdoor drama The Lost Colony」；NCp 提到 Paul Green 只在一張照片的圖說裡；兩頁都沒有「每年」「每夏」。我重搜 NCLR 全文也沒有 annual／every summer | 200 | NOT FOUND | 加了什麼欄「每年上演」→「首演」 |
| 86 | 一九三七年，一齣戶外劇在**島上**首演 | ro416 | c30 | 1937 首演：NCLR ✓。首演地點在羅阿諾克島：引用到的來源沒有一個寫（NCp 的圖說只說那張照片拍的是 Fort Raleigh 的戲） | 200 | NOT FOUND（只有地點這一點） | 「一九三七年，一齣戶外劇開始上演。」（或補一個寫出首演地點的來源） |
| 87 | 同一年，第一塊刻字石出現了 | ro417 | c30、c31 | NCpD「The rocks, discovered over a period from 1937 to 1940」；NCLR 把 1937 年的首演與 Dare Stones 放在一起講 | 200 | CONFIRMED | — |
| 88 | 到一九四〇年，一共出現四十幾塊 | ro418 | c31 | NCpD「a series of forty-eight rocks」；NCLR 轉述「the first of forty-seven stones」——旁白說「四十幾塊」，兩說都容得下 | 200 | CONFIRMED | — |
| 89 | 大部分後來被判定是偽造的／第一塊是真是假，沒有人能說 | ro419、ro420 | c31 | NCpD「For the most part, the stones have been determined to be a hoax, with the exception of the first stone discovered. This stone... **has the potential** to have been inscribed during the era of the colonists」；EBs「largely believed to be a hoax」。旁白沒有說「只有第一塊是真的」 | 200 | CONFIRMED | — |
| 90 | 可是那座島上的土裡，有別的東西 | ro421 | — | 轉場 | — | OUT OF SCOPE | — |
| 91 | 一九九八年，一所大學在那座島上挖開一塊沙地 | ro501 | c34 | NG「In 1998, archaeologists from East Carolina University found a ten-carat gold signet ring here」（Cape Creek, Hatteras Island）；SM17 | 200 | CONFIRMED | — |
| 92 | 他們挖到一只戒指，當時說是金的 | ro502 | c34 | SM17「A local jeweler declared it gold」；NG 當年寫「ten-carat gold signet ring」。旁白用「當時說是」保住了 | 200 | CONFIRMED | — |
| 93 | 同一年，另一邊有人在數樹的年輪 | ro503 | c32 | SCI：Science 1998 Apr 24; 280(5363):564-7 | 200 | CONFIRMED | — |
| 94 | 年輪窄的那幾圈，是雨水少的年份 | ro504 | （無對應列） | SCI 的摘要只寫「Tree-ring data from Virginia indicate that... disappeared during the most extreme drought in 800 years」，沒有講年輪寬窄怎麼讀；`claims.md` 也沒有這一列。這是常識，但照規矩指不到來源就不能算 CONFIRMED | 200 | NOT FOUND | 「那份研究從年輪的寬窄，看出雨水多少。」（改成講那份研究的做法，並在 `claims.md` 補一列） |
| 95 | 卡片「樹輪量到的乾旱」stat 1「1587–1589／**殖民者在島上的三年**」 | drought-stats.stats[0] | c32 | SCI 只說羅阿諾克的殖民地「disappeared during the most extreme drought in 800 years (1587-1589)」；NPSth 說大旱從 1587 年起三年。**沒有任何來源說這批人在島上待了這三年**——他們幾時離開羅阿諾克正是全集說「沒有定論」的那件事，NPS87 還寫他們當時分成兩組、一組要往內陸 | 200 | CHANGED | 標籤「殖民者在島上的三年」→「論文算出的乾旱年份」 |
| 96 | 卡片 stat 2「800 年／樹輪裡最旱的一次」、出處「Science 1998、NPS 2026-10-10」 | drought-stats | c32 | SCI、NPSth | 200 | CONFIRMED | — |
| 97 | 那份研究說一五八七到一五八九年特別旱／是八百年裡最嚴重的一次 | ro505、ro506 | c32 | SCI 原句 | 200 | CONFIRMED | — |
| 98 | 不過那份研究量的是這個區域的樹，不是外灘當地 | ro507 | c33 | SCI「Tree-ring data from **Virginia**」 | 200 | CONFIRMED | — |
| 99 | 論文自己也只說，乾旱可能跟這件事有關 | ro508 | c33 | SCI「These extraordinary droughts **can now be implicated** in the fate of the Lost Colony」 | 200 | CONFIRMED | — |
| 100 | 旱不旱，解釋不了那個字 | ro509 | — | 推論、轉折 | — | OUT OF SCOPE | — |
| 101 | 真正讓人回到島上挖的，是那只戒指 | ro510 | c34 | SM17「The 1998 discovery **electrified** archaeologists and historians」；NG 說那是「an unprecedented find in early British America」，戒指出土處 Cape Creek 後來就是年年挖的那個遺址 | 200 | CONFIRMED | — |
| 102 | 二〇〇九年，當地人成立了一個考古團體 | ro511 | c36 | NG「Margaret Dawson, a nurse and volunteer excavator... She and her husband Scott, **a local teacher**, founded the Croatoan Archaeological Society... in 2009」 | 200 | CONFIRMED | — |
| 103 | 後來一所英國的大學也加進來 | ro512 | c36 | NG「Mark Horton, an archaeologist at Britain's **Bristol University**, who heads the excavation on Hatteras」；同頁說那對夫婦「have sponsored Horton's annual digs **ever since**」（也就是 2009 年起） | 200 | CONFIRMED（建議，見〈建議〉5） | — |
| 104 | 二〇一五年春天，他們挖到一截鐵劍柄 | ro513 | c37 | NG「Part of an iron rapier handle was unearthed in the spring of 2015 at the Cape Creek site on Hatteras Island」 | 200 | CONFIRMED | — |
| 105 | **二〇二五年一月**，又挖到成桶的鍛鐵碎屑 | ro514 | c38 | WHRO（Published January 20, 2025）寫的是「Archaeologists **recently** found『buckets』of hammer scale on Hatteras Island」——一月是報導的日期，不是挖到的日期 | 200 | CHANGED | 「二〇二五年初，又挖到成桶的鍛鐵碎屑。」 |
| 106 | 這一條目前只有發掘方受訪的說法 | ro515 | c38 | WHRO 全篇都是 Scott Dawson（該團體的 president）受訪的話；我這一輪也沒有找到發表的報告 | 200 | CONFIRMED | — |
| 107 | 二〇一七年，那只戒指送去化驗／驗出來全部都是黃銅／卡片「黃銅／那只金戒指／二〇一七年驗出」 | ro516、ro517、brass.data | c34 | SM17（2017-04-07）「A team led by archaeologist Charles Ewen **recently** subjected the ring to a lab test at East Carolina University...『**It's all brass**』」 | 200 | CONFIRMED（卡片的 kicker 見〈建議〉6） | — |
| 108 | 跟它一起出土的東西，年代落在一六七〇到一七二〇年／比那批人晚了很久 | ro518、ro519 | c35 | SM17「dating to between 1670 and 1720」 | 200 | CONFIRMED | — |
| 109 | 島上多數歐洲器物，都混在十七世紀中期的東西裡 | ro520 | c39 | NG「Like most of the European finds **at Cape Creek**, however, the artifact was mixed in with objects that date to the mid-17th century」——來源講的是那一個遺址 | 200 | CONFIRMED（建議，見〈建議〉7） | — |
| 110 | 同行說，年代很難定準／也可能是後來交易帶過去的 | ro521、ro522 | c39 | NG「many of their **colleagues** are skeptical that the artifacts can be definitively tied to the ill-fated colonists, given **difficulties in dating them precisely**」；SM17 引 Ewen「it is more likely that the ring was a common mass-produced item **traded** to Native Americans long after the failed settlement attempt」 | 200 | CONFIRMED | — |
| 111 | 南邊這一路，到今天還沒有定論 | ro523 | c39 | 同上；NPSth 的 Hatteras 段 | 200 | CONFIRMED | — |
| 112 | 而另一支團隊，是從一張地圖開始的 | ro524 | c40 | SM17「The digs by the First Colony Foundation were sparked by the 2012 discovery of a patch concealing the image of a fort on a map painted by John White」 | 200 | CONFIRMED | — |
| 113 | 二〇一二年，有人在大英博物館攤開懷特那張地圖 | ro601 | c40 | FCF 自己寫「in 2012, we asked a First Colony board member to determine if the **British Museum** knew what lay underneath two small paper patches」；NG「part of the British Museum's permanent collection, the document made headlines in 2012」；SM17 同。**注意：c40 掛的 NPSth 與 SM20 兩頁都沒有 2012 這個年份**（見〈要改的出處〉） | 200 | CONFIRMED | — |
| 114 | 地圖上貼著一塊補丁 | ro602 | c40 | NPSth「a patch covering a fort-like symbol」；FCF 說地圖上有「two small paper patches」，蓋住堡壘記號的是其中一塊 | 200 | CONFIRMED（建議，見〈建議〉8） | — |
| 115 | 補丁底下，是一個堡壘形狀的記號 | ro603 | c40 | NPSth「a patch covering a **fort-like symbol**」。照 H02.md，不講補丁底下畫的是別的東西（NG 說四角星、SM20 說兩座隱形墨水的堡壘），旁白守住了 | 200 | CONFIRMED | — |
| 116 | 還記得他們說要往內陸搬五十英里嗎／補丁底下那個記號，就在那個距離上 | ro604、ro605 | c24、c40 | NPSth「approximately 50 miles inland」＋HAK-txt「50 miles into the maine」；NG 也把內陸那處寫成「50 miles to the northwest」。旁白把內陸的五十英里和南邊的五十英里分開，沒有混在一起（H02.md 的硬要求） | 200 | CONFIRMED（建議，見〈建議〉9） | — |
| 117 | 位置**是**今天的伯蒂郡 | ro606 | c40 | NPSth「**near** present-day Bertie County」 | 200 | CONFIRMED（建議，見〈建議〉10） | — |
| 118 | 這裡開了兩個工地，挖到歐洲人用的器物 | ro607 | c41 | NPSth「Archeologists have uncovered many English artifacts during the digs」；CR20（Site X、Site Y）。旁白不唸工地的英文名 | 200 | CONFIRMED | — |
| 119 | 二〇二〇年，發掘團隊自己的考古學家說過一句話／其中一個工地，不是這批人搬去的主要地點 | ro608、ro609 | c42 | CR20（2020-10）引基金會的 principal Luccketti：「We all agree that **is not the major relocation site of the Lost Colony**... but again, a satellite site」 | 200 | CONFIRMED | — |
| 120 | 同一年，一所大學的考古學家說，他存疑 | ro610 | c42 | **SM20**「『I am skeptical,』Charles Ewen, an archaeologist at East Carolina University... tells National Geographic」。CR20 整篇沒有這句（見〈要改的出處〉） | 200 | CONFIRMED | — |
| 121 | 可是二〇二六年六月，同一個基金會改口了 | ro611 | c42 | FCF 的 `article:published_time` 是 2026-06-04；同一個基金會 2020 年說 Site Y 不是主要地點，2026 年的頁面寫 Site X、Site Y 是「117 immigrants established their New World home」的聚落 | 200 | CONFIRMED | — |
| 122 | 他們在自己的網頁上宣布，失落的殖民地找到了／卡片「找到了／二〇二六年六月的宣布／基金會自己的網頁」 | ro612、found-it.data | c42 | FCF「The Lost Colony is Found! How We Did It.」「This is not another hoax or false claim.」；旁白與卡片都把它標成基金會自己的宣稱 | 200 | CONFIRMED | — |
| 123 | 那則宣布沒有附新的發掘報告／到今天也沒看到第三方的評估 | ro613、ro614 | c42 | FCF 全頁沒有附報告；FCF2（基金會最新的一則新聞）是 2024-08-14 一只銅耳飾的檢驗，與這個宣告無關；我這天搜了一次，找到的都是 2015–2020 年的報導，沒有針對 2026-06 宣告的同行或媒體評估 | 200 | CONFIRMED | — |
| 124 | 那兩個工地的器物，**一件都還連不上**這批人 | ro615 | c41 | NPSth 的原句是「Even the artifacts found there have **not been definitively linked** to the Lost Colony」，同一段還寫發掘者「believe may have belonged to the colonists」。少了「確定」兩個字，就從「還不能確定」變成「完全連不上」 | 200 | CHANGED | 「那兩個工地的器物，沒有一件能確定屬於他們。」 |
| 125 | 那麼，到底有沒有任何東西能確定是他們的？／沒有 | ro616、ro701 | c41、c43 | NPSth 兩句合起來（遺骸、墳、房子、村落都沒有確定連上；器物也沒有確定連上） | 200 | CONFIRMED | — |
| 126 | 美國國家公園管理局二〇二五年更新了說明 | ro702 | c43 | NPSth 頁尾「Last updated: July 11, 2025」（我這天看到的仍是這個日期） | 200 | CONFIRMED | — |
| 127 | 沒有遺骸、沒有墳、沒有房子能確定屬於他們 | ro703 | c43 | NPSth「no human remains, graves, buildings, or village sites have been definitively linked to the Lost Colony」 | 200 | CONFIRMED | — |
| 128 | 搬去跟克羅托安人一起住，只是最受歡迎的說法之一 | ro704 | c44 | NPSth「The third theory... is, **perhaps, one of the most popular and compelling**」 | 200 | CONFIRMED | — |
| 129 | 寫過一整本書的兩位學者說，他們的答案是不知道 | ro705 | c45 | NCLR 轉述 Ewen 與 Shields（2024）「Both of us will say,『I don't know.』And mean it」（174） | 200 | CONFIRMED | — |
| 130 | 我的看法是，難的不是那個字，是那個字之後 | ro706 | 〈不是主張〉 | 明示的意見，照 README 內容守則第 5 條 | — | OUT OF SCOPE | — |
| 131 | 片尾卡「未結／一個字指出了去處，沒有指出下落／訂閱奇聞檔案局」 | outro.data | c45 | EBp「The mystery of the Lost Colony has never been solved」；去處有線索（木樁上的地名）、下落沒有定論（#124–#128），與全集一致 | 200 | CONFIRMED | — |
| 132 | 你最早聽到的是哪一個版本／這個頻道只講紀錄裡找得到的，想一起開檔案就訂閱 | ro707、ro708 | 〈不是主張〉 | 留言題與訂閱邀請 | — | OUT OF SCOPE | — |

抽出來的 234 條併成上表 132 列（同一個事實在旁白與卡片各出現一次的併為一列）。
判定計數：**CONFIRMED 103、CHANGED 15、NOT FOUND 3、OUT OF SCOPE 11**。

## H02.md 拒絕的四件事，逐件回答

**1. 殖民者的人數（來源從約一百到約一百五十；名單上的 119 個名字跟「當時有多少人」是兩回事）
——仍然被拒絕，守住了。**
全片沒有出現「115」「一百一十五」或任何單一的人數。旁白只說「一百多個英格蘭人」（ro207），
落在 EBp 的「approximately 100」到 NCp 的「approximately 150」之間，WHRO 也寫「More than 100
colonists」。卡片 `count-stats` 把兩件事分開並列：一邊是「119／名單上的名字」（我自己把 Hakluyt
的名單重數一次：男 91、女 17、男孩 9、當地出生 2＝119，與 H02.md 相同），一邊是「100–150／各家
來源的說法」，而且 ro208「名單上的名字」、ro209「各家來源寫的」兩句用詞也沒有把名單當人數。
**唯一要改的是那張卡的註**「含後來離開的三個」：三個裡有一個是 1587 年七月在島上被殺的
George How，不是離開（見主張表 #35）。

**2.「樹上刻著 CROATOAN」——仍然被拒絕，但有兩句的用字要收緊。**
腳本把兩處分得很清楚：ro107 樹上三個大寫字母、ro108–ro110 完整的字在柵欄入口一根剝了皮的木樁上、
ro109「離地五英尺」、ro111「字的上面，沒有十字」，卡片 `the-word` 的 kicker 直接寫「柵欄的木樁上」、
sub 寫「離地五英尺」；第四章還特地把「樹上刻著一個字」標成後來長出來的講法（ro410），
並說誰最先這樣講查不到（ro411）。插圖也配合：`three-notches` 畫樹皮上三道刻痕、`stripped-post`
畫剝了皮的木樁，兩張都沒有把字畫出來。EBp、NPS90、SM20 三個來源都支持這個分法。
**但 ro107 與 ro409 把「樹皮上」用在樹那一邊**——Hakluyt 只在木樁那一根寫了「had the barke taken
off」，樹那一句是「vpon a tree, in the very browe thereof」。剝皮正是木樁的辨識特徵，挪到樹上會把
這一集賴以立論的分別糊掉，所以這兩句要改（#19、#76）。

**3. 與克羅托安人融合是「主流看法」——仍然被拒絕，守住了。**
ro704 的原話是「搬去跟克羅托安人一起住，**只是最受歡迎的說法之一**」，對應 NPSth 的
「perhaps, one of the most popular and compelling」；「只是…之一」比來源更保守，沒有升級成主流或
最多人支持。而且這句之前就先放了 ro701「沒有」、ro702–ro703 國家公園管理局 2025 年更新的那句
（沒有遺骸、墳、房子能確定屬於他們），之後接 ro705 兩位專書作者的「不知道」與片尾卡的「未結」。
全片沒有出現「主流」「證實」「謎團已解」。

**4. 二〇二六年內陸的「找到了」——仍然被拒絕，守住了。**
ro611「同一個基金會改口了」、ro612「他們在**自己的網頁**上宣布」、卡片 `found-it` 的 sub 直接寫
「基金會自己的網頁」、ro613「那則宣布沒有附新的發掘報告」、ro614「到今天也沒看到第三方的評估」，
而且前面先放了 2020 年基金會自己的考古學家說 Site Y 不是主要地點（ro608–ro609，CR20 原句）
與同年另一所大學考古學家的「我存疑」（ro610，SM20 原句），後面接 ro615 NPS 說器物還連不上。
時間順序沒有被寫成「同行回應了 2026 年的宣告」。我這一輪另外確認：FCF 頁面確實是 2026-06-04
發的、頁上沒有附報告；基金會最新的一則新聞（FCF2）是 2024-08-14 一只銅耳飾的檢驗，跟
Site X／Site Y 無關；一次網路搜尋也沒有找到任何第三方對那則宣告的評估。
**唯一要改的是 ro615 少掉的「確定」兩個字**（#124）——NPS 的原句是「not been definitively
linked」，不是「一件都連不上」。

## 要改的地方（請撰稿方套用，我沒有動 `video.json`）

旁白的字數我都控在這一集現有的最長句（25 字）以內。

### 旁白

1. **ro104**　現在：「上岸以後，他們吹號，唱英格蘭的歌。」
   → 「靠岸之前，他們吹號，唱英格蘭的歌。」
   （Hakluyt：在船上吹號、唱歌，沒有回應才「therefore landed at day-breake」。次序剛好相反。）
2. **ro107**　現在：「一棵樹的樹皮上，刻著三個大寫字母。」
   → 「一棵樹上，刻著三個大寫字母。」
   （剝皮只寫在木樁上；見拒絕第 2 件。）
3. **ro409**　現在：「還記得樹皮上那三個大寫字母嗎？」
   → 「還記得樹上那三個大寫字母嗎？」（與 2 連動，`loops[1]` 的 `what` 不用動。）
4. **ro301**　現在：「可是他一離開，英格蘭就打起仗來。」
   → 「可是那幾年，英格蘭正在打仗。」
   （EV：他離開前女王「had been fighting the Spanish」；1588 年發生的是無敵艦隊與禁止出港。）
5. **ro404**　現在：「還會像他們一樣，對著一本書說話。」
   → 「還會像英格蘭人一樣，對著一本書說話。」
   （Lawson 的原文是「as we do」，「we」是英格蘭人；「他們」會被讀成哈特拉斯人。）
6. **ro413**　現在：「一八三〇年代，美國的歷史書開始這樣寫它。」
   → 「一八三〇年代，一本書和一篇雜誌文章這樣寫它。」
   （Smithsonian 2020 的原句是「a book and a magazine article」。若要保留「歷史書」，就得把
   Coastal Review 2018 那條補進 `sources[]` 與 `claims.md` c29。）
7. **ro514**　現在：「二〇二五年一月，又挖到成桶的鍛鐵碎屑。」
   → 「二〇二五年初，又挖到成桶的鍛鐵碎屑。」
   （WHRO 2025-01-20 寫的是「recently found」；一月是報導的日期。）
8. **ro615**　現在：「那兩個工地的器物，一件都還連不上這批人。」
   → 「那兩個工地的器物，沒有一件能確定屬於他們。」
   （NPS：「not been definitively linked」，而且發掘者認為可能屬於他們。）
9. **ro504**　現在：「年輪窄的那幾圈，是雨水少的年份。」
   → 「那份研究從年輪的寬窄，看出雨水多少。」
   （沒有來源講年輪怎麼讀；改成講那份研究的做法就有 SCI 的摘要可指，並請在 `claims.md` 補一列。）
10. **ro416**　現在：「一九三七年，一齣戶外劇在島上首演。」
    → 「一九三七年，一齣戶外劇開始上演。」
    （1937 首演有 NCLR；「在島上」沒有來源寫。若要保留地點，請補一個寫出首演劇場的來源。）

### 卡片

11. **`count-stats`.stats[0].note**　現在：「含後來離開的三個」→ 「其中三個沒有留下」
    （三個裡的 George How 是被殺，不是離開；也不必提死因。）
12. **`drought-stats`.stats[0].label**　現在：「殖民者在島上的三年」→ 「論文算出的乾旱年份」
    （沒有來源說他們在島上待了這三年；他們幾時離開羅阿諾克正是全集說沒有定論的事。）
13. **`added-later`.rows[3][2]**　現在：「每年上演」→ 「首演」
    （引用到的來源只寫 1937 年首演，沒有寫每年演。）
14. **`added-later`.rows[1][1]**　現在：「歷史書」→ 「一本書和一篇文章」（與第 6 條連動。）

### 章名與說明欄

15. **`war-at-home` 的 `chapter`**　現在：「無敵艦隊那一年，他的補給出不了港」
    → 「無敵艦隊那一年，他的補給送不到島上」
    （1588-04-22 兩艘補給船確實開出去了，是在海上與法國人交戰後折返，旁白 ro304 自己也這樣講。）
16. **`youtube.description` 第二段**　現在：「無敵艦隊那一年補給為什麼開不出去」
    → 「無敵艦隊那一年補給為什麼送不到」（同上。）
17. **`youtube.description` 第一段**　「一棵樹的樹皮上刻著三個大寫字母」裡的「樹皮」要跟著第 2 條改成
    「一棵樹上刻著三個大寫字母」。

### 出處（`sources[]` 與 `claims.md`；不影響旁白）

18. **`sources[]` 缺一筆**：`claims.md` c28、c31 引的 Britannica 故事頁
    （https://www.britannica.com/story/the-lost-colony-of-roanoke ，這天 200）不在 `sources[]` 裡。
    說明欄的參考資料是由 `sources[]` 自動接上的，所以觀眾看不到這一條。請補一筆（checked_on
    2026-10-10），或把 ro410 的出處改掛已經在列的 NCp（「cut into a tree or post of a palisade」）
    與 WHRO（發掘方自己轉述流傳版「on a tree」）。
19. **c40 的出處對不上**：「二〇一二年在大英博物館」這個年份，在它掛的 NPSth 與 SM20 兩頁上都沒有；
    有這個年份的是 NG、SM17 與基金會自己的頁（三條都已在 `sources[]`）。請改掛。
20. **c42 的出處對不上**：「I am skeptical」在 SM20，不在 CR20（CR20 整篇沒有 skeptic 這個字）。
    請把 ro610 的出處改掛 SM20；CR20 留給 ro608／ro609 的「not the major relocation site」。
21. **c30 的出處不足**：1937 年首演這件事，NCp 與 NCpD 兩頁都沒有寫，寫的是 NCLR 書評
    （已在 `sources[]`）。請補掛。`added-later` 卡的 `source`「NCpedia、Smithsonian 2026-10-10」
    也建議補上 NCLR。
22. **`claims.md` 編號跳號**：c19 之後直接到 c21，沒有 c20。不是事實問題，但下一輪對照會卡住，
    建議補號或註明。

## 建議（指得出來源、但我不要求改）

1. **ro102**「一艘英格蘭船在羅阿諾克島外放下小船」——Hakluyt 的小船是從 Hatorask 放的
   （「we put off from Hatorask... in both boates」），EV 還寫 1590 年有四艘船出發。
   「一艘英格蘭船在外灘放下小船。」會更準，也不必提翻船那件事（H02.md 不畫）。
2. **ro201**「那個字是他自己留下的約定」——Hakluyt 是「agreed vpon betweene them and me」，雙方約的。
   ro220「他跟他們約好一個記號」已經補回來，所以我不要求改；要改就寫「那個字是他跟他們約好的記號。」
3. **ro205**「蓋房子和堡壘」——原文是「make our seate and forte」（聚落與堡壘）。
4. **ro218**「兩天後的早上，他上了船」——他是 27 日早上離開羅阿諾克，當天「about midnight, came
   aboord the Flieboat」。要準就寫「兩天後的早上，他離開了羅阿諾克。」
5. **ro512**「後來一所英國的大學也加進來」——NG 說那對夫婦 2009 年成立團體後「have sponsored
   Horton's annual digs ever since」，英國那邊幾乎是同時進來的，不是後來才加。
6. **`brass` 卡的 kicker「那只金戒指」**——卡片上「金」沒有引號，單看卡面像在斷定它是金的；
   旁白 ro502「當時說是金的」有救回來。要更穩可以寫「那只『金』戒指」。
7. **ro520**「島上多數歐洲器物」——NG 講的是「most of the European finds **at Cape Creek**」，
   一個遺址，不是整座島。
8. **ro602**「地圖上貼著一塊補丁」——基金會自己寫地圖上有「two small paper patches」，
   蓋住堡壘記號的是其中一塊。
9. **ro605**「就在那個距離上」——NPS 寫的是「approximately 50 miles inland」。
10. **ro606**「位置是今天的伯蒂郡」——NPS 寫的是「**near** present-day Bertie County」。
11. **ro107 的「大寫字母」**——Hakluyt 對樹用的是「faire Romane letters」，「fayre Capitall letters」
    只寫在木樁那一句；但 NPS90、EBp、SM20 都把樹上那三個字寫成大寫的 CRO，所以「大寫」留著。
12. **ro112／縮圖的「反而」**——Hakluyt 的對比是「雖然東西被翻爛了，另一方面我很高興」，
    不是「雖然人不見了，我很高興」。兩種讀法都通，照 H02.md 題目卡的寫法留著。
13. **標題用「消失的殖民地」、片中用「失落的殖民地」**——標題與 H02.md 題目卡一字不差，不是事實
    問題；要統一是風格決定，不在我這一輪的範圍。

## 其他

- **會過期的事實**：ro614「到今天也沒看到第三方的評估」是一句「沒有」的主張，上架前最好再搜一次；
  ro702 綁在 NPSth 的「Last updated: July 11, 2025」，那一頁改版就要重看。另外 NPS 另兩頁這天標的是
  2026-09-20（NPS87）與 2026-08-14（NPS90），`claims.md` 沒有引到它們的更新日，不影響任何一句。
- **只靠一個來源的事**（旁白都已標明說話的人）：約好的記號與十字、懷特看到字很高興（只有他 1593 年
  寄出的記述，ro112、ro201、ro220–ro224 都用「他寫」「他跟他們約好」帶）；1709 年的轉述（只有
  Lawson，ro405 明說「只有這一份」）；哈特拉斯島的鍛鐵碎屑（只有發掘方受訪，ro515 明說）；
  2026 年的「找到了」（只有基金會自己的網頁，ro612–ro614 明說）；1587–1589 的大旱（一篇 1998 年的
  論文，ro507、ro508 兩句都加了但書）。
- **聽眾檢查**：131 句最長 25 字（ro311、ro518），沒有「經查證」「根據官方文件」「本影片」；
  旁白沒有唸出任何拉丁字（Site X／Y、Cape Creek、Bristol、East Carolina、First Colony Foundation
  都改成中文的說法，出處留在 `claims.md` 與說明欄），沒有括號、沒有網址；七個 reveal 都落在介紹
  該項的句子上。
- **內容守則**：流傳的版本都標成後來加的（ro410、ro412–ro417）；沒有宣稱定論；沒有編造任何人的
  對話或心理（ro225「他以為」、ro706「我的看法是」都標明了）；George Howe 被殺、1590 年翻船淹死
  七人、前一批駐軍的骸骨、1586 年酋長被砍頭，全片都沒有提，插圖也沒有畫；Virginia Dare 的名字
  沒有出現，血統的說法沒有碰。
- **圖片**：`assets[]` 空、沒有照片卡，H02.md 的六張公有領域圖與兩張未核准的圖都沒有入稿；
  站主要決定的三件（大英博物館那兩張、1876 年版畫）這一版用不到。
- **第二輪：需要**（這一輪 CHANGED 15 列、NOT FOUND 3 列，遠超過 3 個；15 列裡 4 列是出處與連帶的
  改動，另 11 列是旁白、卡片、章名或說明欄的事實）。第二輪請換人，重查上面 17 條
  旁白／卡片／章名／說明欄的改動與 5 條出處，再隨機抽三分之一的 CONFIRMED；最該重抽的是
  Hakluyt 1590 那一段的次序（#16）與樹／木樁的用字（#19、#76），那兩處是這一集的立論所在。
