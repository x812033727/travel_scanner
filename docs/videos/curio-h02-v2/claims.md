# curio-h02-v2 主張清單

H02 羅阿諾克的第二版腳本（2026-10-13 寫，照 `script-writing.md` §故事主線與鉤子與 §開場濃縮）。
**事實全部來自** [`../history-curiosity/topic-checks/H02.md`](../history-curiosity/topic-checks/H02.md)
的逐項查核表（2026-10-10 查核，同日由另一個代理獨立覆核，處置 ADOPT_WITH_CHANGES）
與 [`../history-curiosity/topics.json`](../history-curiosity/topics.json) 的 H02 題目卡。
這一版沒有另外查資料、沒有新增、沒有改動任何數字、名字或日期；查證日一律 **2026-10-10**。

2026-10-13 [`verify-1.md`](verify-1.md)（獨立查核的第一輪，不是寫這份稿的代理）把十九個網址
全部重開一次，判 CONFIRMED 103、CHANGED 15、NOT FOUND 3。它要求的十七條內容改動與五條出處
改動都已經套進 `video.json` 與這一份清單；改過的列後面標「**（查核一改）**」，補出來的那一列標
「**（查核一補）**」。`sources[]` 同一天補了 Britannica 的故事頁，共二十筆，`checked_on` 仍是
2026-10-10。

格式：`編號｜主張（旁白或卡片上的說法）｜網址｜查證日｜用到的場景 id`

**編號不重排**：`verify-1.md` 與 `NOTES.md` 都照現在的編號引用，重排會讓第二輪對不上。
原本在 c19 與 c21 之間跳掉的 **c20** 這一輪補上了（查核一第 22 條），內容是樹輪那份研究的
做法，所以它排在第五節的 c32 後面——號碼因此不照順序，這是刻意的，c1 到 c45 現在沒有缺號。

「**DISPUTED**」是 H02.md 判定來源彼此不一致、或只有單一來源的那幾列；旁白一律照 H02.md
許可的說法講（見每一列後面的括號）。

## 一、一五九〇年回到島上

c1｜一五九〇年八月十八日清晨，約翰．懷特一行人上岸羅阿諾克島｜https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm ；https://www.gutenberg.org/ebooks/25645｜2026-10-10｜daybreak-outer-banks, the-mapmaker
c2｜聚落裡只找到殖民者留下的東西，沒有活人的跡象（NPS「found remnants of the colonists but no signs of life」）｜https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm｜2026-10-10｜trumpet-ashore, third-birthday
c3｜**（查核一改）**靠岸之前吹號、唱英格蘭的歌，沒有人回應才上岸：Hakluyt 的次序是「sounded with a trumpet a Call, and afterwardes many familiar English tunes and Songs, and called to them friendly; but we had no answere, **we therefore landed at day-breake**」，所以 `ro104` 從「上岸以後」改成「靠岸之前」，說明欄第一段的「上岸的人吹號、唱歌」也改成「靠岸之前他們吹號、唱歌」｜https://www.gutenberg.org/ebooks/25645 ；https://nationalhumanitiescenter.org/pds/amerbegin/exploration/text6/white.pdf｜2026-10-10｜trumpet-ashore
c4｜**CHANGED（不是「樹上刻著 CROATOAN」）**：樹上只有三個羅馬大寫字母「C R O」；完整的 CROATOAN 刻在柵欄入口一根去了皮的木樁上，離地五英尺，字上面沒有十字或任何求救記號。**（查核一改）**「剝了皮」只寫在木樁那一根（「one of the chiefe trees or postes at the right side of the entrance had the barke taken off」），Hakluyt 對樹的原句是「vpon a tree, in the very browe thereof were curiously carued these faire Romane letters C R O」，沒有提樹皮；這一集的立論就靠樹與木樁分得清楚，所以 `ro107`、`ro409` 與 `loops[1].what` 都不再說「樹皮上」，說明欄第一段也改成「一棵樹上」｜https://www.gutenberg.org/ebooks/25645 ；https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm ；https://www.britannica.com/place/Lost-Colony｜2026-10-10｜five-feet, the-word, remember-no-cross, remember-three-letters
c5｜**DISPUTED（單一目擊來源）**：懷特寫道，看到這個字他反而很高興（原文「I greatly ioyed that I had safely found a certaine token of their safe being at Croatoan」）；旁白用「他後來寫下」帶｜https://www.gutenberg.org/ebooks/25645 ；https://encyclopediavirginia.org/entries/roanoke-colonies-the/｜2026-10-10｜greatly-joyed, his-own-sign, means-safe

## 二、一五八七年：為什麼他們在這裡，和約好的記號

c6｜一五八七年七月二十二日抵達外灘（「The two and twentieth of Iuly wee arriued safe at Hatorask」）｜https://www.gutenberg.org/ebooks/25645 ；https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm｜2026-10-10｜arrive-hatorask
c7｜原定在乞沙比克灣建聚落與堡壘（「the Bay of Chesepiok where we intended to make our seate and forte」），領航員不肯再往北走｜https://www.gutenberg.org/ebooks/25645 ；https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm｜2026-10-10｜chesapeake-plan, pilot-refuses
c8｜懷特是這批殖民者的總督｜https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm ；https://encyclopediavirginia.org/entries/roanoke-colonies-the/｜2026-10-10｜governor-1587, the-mapmaker
c9｜**DISPUTED（來源從約一百到約一百五十）**：旁白只說「一百多個英格蘭人」；卡片並列名單上的 119 個名字（男 91、女 17、男孩 9、當地出生 2）與各家來源的約 100 到約 150。**（查核一改）**卡片的註從「含後來離開的三個」改成「其中三個沒有留下」：那三個是懷特、領航員與 George How，而 George How 是一五八七年七月在島上被殺，不是離開（死因照 H02.md 不講、不畫）｜https://www.gutenberg.org/ebooks/25645 ；https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm ；https://encyclopediavirginia.org/entries/roanoke-colonies-the/ ；https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/ ；https://www.ncpedia.org/lost-colony ；https://www.britannica.com/place/Lost-Colony｜2026-10-10｜left-on-roanoke, count-stats
c10｜舊堡壘被夷平，空屋長滿瓜，鹿在屋子裡吃｜https://www.gutenberg.org/ebooks/25645｜2026-10-10｜melons-and-deer
c11｜一五八七年八月十八日，懷特的外孫女在島上出生，是第一個在維吉尼亞出生的英格蘭孩子（「because this child was the first Christian borne in Virginia, shee was named Virginia」）｜https://www.gutenberg.org/ebooks/25645 ；https://www.ncpedia.org/lost-colony｜2026-10-10｜child-born
c12｜懷特一五九〇年上岸那天（八月十八日）是外孫女的三歲生日｜https://www.ncpedia.org/lost-colony ；https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm｜2026-10-10｜remember-the-date, third-birthday
c13｜一五八七年八月二十二日全體殖民者請懷特回英格蘭帶補給，他先拒絕；八月二十五日眾人立下聯名的證明｜https://www.gutenberg.org/ebooks/25645｜2026-10-10｜all-ask-him, bring-supplies, he-refuses, signed-paper
c14｜八月二十七日早上懷特離開羅阿諾克（「departed from Roanoak the seuen and twentieth of August in the morning」）；那時外孫女出生才九天｜https://www.gutenberg.org/ebooks/25645 ；https://encyclopediavirginia.org/entries/roanoke-colonies-the/｜2026-10-10｜he-sails, nine-days-old
c15｜**DISPUTED（單一目擊來源）**：離開前約好的記號——搬到哪裡就把地名刻下來，有難就在字上面加一個十字（「a secret token agreed vpon betweene them and me at my last departure from them」「they should carue ouer the letters or name, a Crosse + in this forme, but we found no such signe of distresse」）；旁白用「他自己留下的約定」「照他們的約定」帶｜https://www.gutenberg.org/ebooks/25645 ；https://nationalhumanitiescenter.org/pds/amerbegin/exploration/text6/white.pdf｜2026-10-10｜his-own-sign, the-agreement, carve-the-place, a-cross-if-trouble, remember-no-cross, means-safe, the-question

## 三、三年與過不去的那段路

c16｜一五八八年無敵艦隊：女王下令所有英格蘭船留在本土防衛（「Queen Elizabeth I ordered all English vessels to remain nearby in defense of the homeland」）。**（查核一改）**第 3 章的第一句不再說「他一離開，英格蘭就打起仗來」——Encyclopedia Virginia 寫女王在他出發之前就「had been fighting the Spanish on the seas and in the Netherlands」，一五八八年發生的是無敵艦隊與禁止出港，所以 `ro301` 改成「可是那幾年，英格蘭正在打仗」｜https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm ；https://encyclopediavirginia.org/entries/roanoke-colonies-the/｜2026-10-10｜war-at-home, armada-sails, queens-order, delay-stats
c17｜一五八八年四月二十二日出發的兩艘補給船與法國人交戰後折返（「a two-ship relief mission that sailed on April 22, 1588... But a fight at sea with the French left the ships limping back to England」）。**（查核一改）**船**確實開出去了**（EV 同一段寫「Despite a prohibition on all English ships leaving port」），所以第 3 章的章名從「他的補給出不了港」改成「他的補給送不到島上」，說明欄第二段的「補給為什麼開不出去」也改成「補給為什麼送不到」；旁白 `ro304` 本來就講交戰後折返，沒有改｜https://encyclopediavirginia.org/entries/roanoke-colonies-the/｜2026-10-10｜war-at-home, supply-ships
c18｜懷特一五八七年離開、一五九〇年才回到島上（旁白不唸這兩個年份，`delay-stats` 卡片並列它們）｜https://www.gutenberg.org/ebooks/25645 ；https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm｜2026-10-10｜delay-stats
c19｜木樁上刻的地名指向南邊的島，就是今天的哈特拉斯島一帶（NPS「present-day Hatteras Island」；NCpedia 寫大約是哈特拉斯島東西走向的那一段）；旁白只說「今天的哈特拉斯島一帶」「南邊的外灘」｜https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm ；https://www.ncpedia.org/croatoan-indians｜2026-10-10｜south-along-banks, which-island, croatoan-people
c21｜島上住的克羅托安人是懷特說的「朋友」（「the Sauages of the Iland our friends」）；同一批英格蘭人一五八七年八月才誤襲過他們一次，NPS 也寫他們起初不太願意跟英格蘭人交易｜https://www.gutenberg.org/ebooks/25645 ；https://encyclopediavirginia.org/entries/roanoke-colonies-the/ ；https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm｜2026-10-10｜our-friends, mistaken-attack
c22｜四個錨只剩一個、天氣一天比一天壞（「wee had but one Cable and Anchor left vs of foure, and the weather grew to be fouler and fouler」）；淡水桶丟在岸上；NPS 寫風暴打斷了計畫、他被迫回英格蘭｜https://www.gutenberg.org/ebooks/25645 ；https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm｜2026-10-10｜wants-to-cross, why-not-cross, one-anchor, weather-worse, casks-ashore
c23｜船原本決定南下補水、過冬再回來，八月二十八日的風暴把他們逼往亞速群島再回英格蘭（以懷特的記述為準，不寫西印度群島）；到那座島的路沒有人走完｜https://www.gutenberg.org/ebooks/25645｜2026-10-10｜plan-to-winter, storm-azores, home-to-england, never-reached
c24｜**DISPUTED（單一目擊來源，且與刻字矛盾）**：懷特同一句寫殖民者原本準備從羅阿諾克往**內陸**搬五十英里（「prepared to remoue from Roanoak 50 miles into the maine」），刻在木樁上的卻是南邊的島｜https://www.gutenberg.org/ebooks/25645｜2026-10-10｜one-thing-wrong, fifty-inland, remember-number, post-says-south
c25｜一五八七年那次道別之後，沒有紀錄說英格蘭人再見過這批人（NCpedia「the last known contact between the English and their colony in America」）｜https://www.ncpedia.org/lost-colony｜2026-10-10｜last-contact

## 四、後來的轉述與傳說

c26｜**DISPUTED（事後轉述，單一來源）**：一七〇九年勞森記下哈特拉斯人自述，祖先裡有幾個是白人、會像英格蘭人一樣「對著一本書說話」（「several of their Ancestors were white People, and could talk in a Book, as we do」）。**（查核一改）**原文的「we」是勞森那邊的英格蘭人，而前一句的主語是哈特拉斯人，「像他們一樣」會把意思反過來，所以 `ro404` 改成「還會像英格蘭人一樣」｜https://www.gutenberg.org/ebooks/1838｜2026-10-10｜tease-ancestors, island-people-say, traveller-writes, ancestors-white, talk-in-a-book, only-one-source
c27｜**DISPUTED（二手轉述）**：另有人提出內陸的大酋長下令殺了他們；寫下這個說法的人是聽別人說的（Ewen 與 Shields：「Strachey presents second-hand information」）。旁白只當一個說法講，不給年份、不當事實｜https://encyclopediavirginia.org/entries/roanoke-colonies-the/ ；https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf｜2026-10-10｜ordered-killed, second-hand
c28｜「樹上刻著一個字」是後來長出來的講法；誰最先這樣講今天查不到（Britannica 的故事頁也寫「The word CROATOAN and the letters CRO, **carved into trees** within the colony's borders」；NCpedia 寫成「cut into a tree or post of a palisade」，WHRO 也引發掘方轉述流傳版「on a tree」）。**（查核一改出處）**這一頁與 c31 引的是 Britannica 的**故事頁**，原本不在 `sources[]` 裡，而說明欄的參考資料是由 `sources[]` 自動接上的，觀眾看不到它；2026-10-13 已經把它補進 `sources[]`（第二十筆）｜https://www.britannica.com/story/the-lost-colony-of-roanoke ；https://www.gutenberg.org/ebooks/25645｜2026-10-10｜what-we-remember, legend-moves-to-tree, who-first
c29｜「Lost Colony」這個名字是十九世紀才有的：一八三〇年代「a book and a magazine article cast the settlement as a 'romantic mystery'」，一八三七年 Cushing 的小說「appears to be the first to name the 1587 planters as 'The Lost Colony'」。**（查核一改）**Smithsonian 2020 說的是一本書和一篇雜誌文章，**沒有說是歷史書**（指名 Bancroft 一八三四年那本美國史的是 Coastal Review 2018，不在 `sources[]` 裡），所以 `ro413` 改成「一八三〇年代，一本書和一篇雜誌文章這樣寫它」，`added-later` 表格的「誰」欄也從「歷史書」改成「一本書和一篇文章」｜https://www.smithsonianmag.com/smart-news/new-evidence-roanoke-colonys-disappearance-180976248/ ；https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf｜2026-10-10｜even-the-name, 1830s-history, 1837-novel, lost-colony-name, added-later
c30｜一九三七年 Paul Green 的戶外劇《The Lost Colony》首演（NCLR「The year 1937, the time of the premiere of Paul Green's outdoor drama The Lost Colony」），同年第一塊 Dare Stone 出現（NCpedia「discovered over a period from 1937 to 1940」）。**（查核一改）**首演這件事 NCpedia 兩頁都沒有寫（`lost-colony` 只在一張照片的圖說裡提到 Paul Green），所以這一列補掛 NCLR 書評，`added-later` 卡的 `source` 也補成「NCpedia、NCLR、Smithsonian 2026-10-10」；兩頁都沒有「每年」或「每夏」，卡片的「每年上演」改成「首演」；**首演的地點沒有來源寫**，所以 `ro416` 從「在島上首演」改成「開始上演」｜https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf ；https://www.ncpedia.org/dare-stones ；https://www.ncpedia.org/lost-colony｜2026-10-10｜added-later
c31｜**DISPUTED（塊數 47 或 48）**：一九三七到一九四〇年一共出現四十幾塊刻字石，大部分被判定是偽造的；第一塊的真偽沒有定論（NCpedia「a series of forty-eight rocks」，NCLR 書評轉述「the first of forty-seven stones」）。旁白只說「四十幾塊」，不說「只有第一塊是真的」｜https://www.ncpedia.org/dare-stones ；https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf ；https://www.britannica.com/story/the-lost-colony-of-roanoke｜2026-10-10｜added-later, forty-odd-stones, mostly-hoax, first-stone-open

## 五、樹輪與南邊的發掘

c32｜一九九八年的樹輪研究：一五八七到一五八九年是八百年來最嚴重的乾旱（「the most extreme drought in 800 years (1587-1589)」）；NPS 也寫一五八七年起外灘大旱三年。**（查核一改）**`drought-stats` 的第一個標籤從「殖民者在島上的三年」改成「論文算出的乾旱年份」：摘要只說這個殖民地「disappeared during the most extreme drought in 800 years (1587-1589)」，**沒有任何來源說這批人在島上待了這三年**——他們幾時離開羅阿諾克，正是這一集說沒有定論的那件事（NPS 還寫他們當時分成兩組、一組要往內陸）｜https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text ；https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm｜2026-10-10｜tree-rings, drought-stats
c20｜**（查核一補，原本跳掉的號碼）**那份一九九八年的研究是從樹輪推出乾旱的（摘要「**Tree-ring data** from Virginia indicate that the Lost Colony of Roanoke Island disappeared during the most extreme drought in 800 years」）。原本的旁白「年輪窄的那幾圈，是雨水少的年份」在摘要裡指不到來源（摘要沒有寫年輪怎麼讀），所以 `ro504` 改成講那份研究的做法：「那份研究從年輪的寬窄，看出雨水多少。」**還留著的一點**：摘要沒有逐字寫「寬窄」，那是樹輪重建乾旱的通用讀法；第二輪若要再收緊，可以改成「那份研究從年輪，看出雨水多少」｜https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text｜2026-10-10｜how-rings-work
c33｜**那份研究量的是區域的樹輪（「Tree-ring data from Virginia」），不是外灘當地；論文對因果只說乾旱「can now be implicated」**，所以旁白說「可能跟這件事有關」，不說「因為乾旱」｜https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text｜2026-10-10｜regional-not-local, only-implicated, drought-not-answer
c34｜一九九八年 East Carolina 大學在哈特拉斯島挖到一只當時說是金的戒指；二〇一七年檢驗結果是「It's all brass」｜https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/｜2026-10-10｜tease-ring-test, soil-has-things, dig-1998, the-ring, back-to-digging, tested-2017, brass
c35｜跟戒指一起出土的器物年代落在一六七〇到一七二〇年｜https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/｜2026-10-10｜1670-1720, much-later
c36｜Croatoan Archaeological Society 二〇〇九年成立，與一所英國（Bristol）大學合作（二〇一五年報導時）｜https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology｜2026-10-10｜society-2009, british-university
c37｜二〇一五年春天在哈特拉斯島 Cape Creek 遺址挖到一截鐵劍柄（「Part of an iron rapier handle was unearthed in the spring of 2015 at the Cape Creek site on Hatteras Island」）｜https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology｜2026-10-10｜rapier-handle
c38｜**DISPUTED（只有發掘方受訪的說法，沒有發表的報告）**：二〇二五年一月二十日的報導說在哈特拉斯島挖到「buckets」的鍛鐵碎屑；旁白明說「目前只有發掘方受訪的說法」。**（查核一改）**WHRO 寫的是「**recently** found」，一月是報導的日期、不是挖到的日期，所以 `ro514` 從「二〇二五年一月」改成「二〇二五年初」｜https://www.whro.org/arts-culture/2025-01-20/new-artifacts-on-hatteras-point-to-the-real-fate-of-the-lost-colony｜2026-10-10｜hammer-scale, no-report-yet
c39｜多數歐洲器物混在十七世紀中期的東西裡，同行存疑是因為「difficulties in dating them precisely」，也可能是交易帶過去的｜https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology ；https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/｜2026-10-10｜mixed-in, hard-to-date, could-be-trade, south-unsettled

## 六、內陸的發掘與今天的狀態

c40｜懷特的地圖上有一塊補丁，底下是一個堡壘狀的符號，位置在內陸約五十英里、靠今天的伯蒂郡（「On a map created by John White, there is a patch covering a fort-like symbol approximately 50 miles inland, near present-day Bertie County」）；補丁二〇一二年在大英博物館發現。只說「堡壘狀的符號」，不說補丁底下畫的是什麼別的東西。**（查核一改出處）**「二〇一二年在大英博物館」這個年份在 NPS major-theories 與 Smithsonian 2020 兩頁上**都沒有**；有它的是 National Geographic 2015（「the document made headlines in 2012」）、Smithsonian 2017 與基金會自己的頁（「in 2012, we asked a First Colony board member to determine if the British Museum knew what lay underneath two small paper patches」），所以這一列補掛這三條（補丁、堡壘記號、約五十英里與伯蒂郡仍由 NPS 支持）｜https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm ；https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology ；https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/ ；https://www.firstcolonyfoundation.org/news/lost-colony-is-found/ ；https://www.smithsonianmag.com/smart-news/new-evidence-roanoke-colonys-disappearance-180976248/｜2026-10-10｜tease-map-patch, other-direction, british-museum-map, fort-symbol, remember-fifty-inland, bertie-county
c41｜內陸的 Site X 與 Site Y 挖到歐洲人用的器物，NPS 寫「Even the artifacts found there have **not been definitively linked** to the Lost Colony」。**（查核一改）**同一段還寫發掘者認為那些器物「may have belonged to the colonists」，少了「確定」兩個字就從「還不能確定」變成「完全連不上」，所以 `ro615` 從「一件都還連不上這批人」改成「沒有一件能確定屬於他們」｜https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm｜2026-10-10｜two-sites, artifacts-not-linked
c42｜**DISPUTED（來源不一致，且宣告還沒有第三方評估）**：二〇二〇年發掘方（First Colony Foundation）自己的考古學家說 Site Y「is not the major relocation site of the Lost Colony」，同年 East Carolina 大學的 Ewen 說「I am skeptical」；二〇二六年六月四日基金會在自己的網頁上宣布「The Lost Colony is Found! How We Did It.」，沒有附新的發掘報告，查核與覆核時都沒找到同行或媒體的評估。旁白照 H02.md 的許可說法：發掘團隊宣稱找到了，之前官方與同行說證據不夠，之後還沒看到第三方的評估。**（查核一改出處）**「I am skeptical」只在 **Smithsonian 2020**，Coastal Review 整篇沒有 skeptic 這個字：`ro610` 掛 Smithsonian 2020，Coastal Review 留給 `ro608`／`ro609` 的「is not the major relocation site of the Lost Colony」。查核一另外重開了基金會最新的一則新聞（2024-08-14 一只銅耳飾的檢驗），與這個宣告無關，並搜了一次，沒有找到任何第三方對二〇二六年六月那則宣告的評估｜https://coastalreview.org/2020/10/lost-colony-moved-inland-archaeologists/ ；https://www.smithsonianmag.com/smart-news/new-evidence-roanoke-colonys-disappearance-180976248/ ；https://www.firstcolonyfoundation.org/news/lost-colony-is-found/ ；https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm｜2026-10-10｜tease-announcement, their-own-words, not-the-main-site, skeptical, changed-tune, found-it, no-new-report
c43｜美國國家公園管理局 2025-07-11 更新的頁面寫「no human remains, graves, buildings, or village sites have been definitively linked to the Lost Colony」。**（查核一：會過期）**`ro702` 唸的是那一頁的更新年份，2026-10-13 重開仍標 Last updated: July 11, 2025；那一頁改版就要重看這一句（記在 `NOTES.md`〈上架前要再查的兩件事〉）｜https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm｜2026-10-10｜anything-certain, no-such-thing, nps-page, nothing-linked
c44｜**CHANGED（不是「主流看法」）**：搬去與克羅托安人同住，NPS 稱它「perhaps, one of the most popular and compelling」；旁白只說「最受歡迎的說法之一」｜https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm｜2026-10-10｜one-popular-story
c45｜寫過整本專書的兩位學者（Ewen 與 Shields, 2024）說「Both of us will say, 'I don't know.' And mean it」；Britannica 同樣寫「The mystery of the Lost Colony has never been solved.」｜https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf ；https://www.britannica.com/place/Lost-Colony｜2026-10-10｜we-dont-know, outro

## 不是主張的幾句

- `he-expected-to-return`「他以為自己很快就會回來。」——不是查得到的事實，是從 c13、c14（他是去押補給的）
  推出來的敘述句，旁白用「他以為」標明是推想。
- `my-reading`「我的看法是，難的不是那個字，是那個字之後。」——系列自己的解讀，照
  `README.md` 內容守則第 5 條標成意見。
- `outro` **旁白的兩句**（留言題與訂閱邀請）——照 `script-writing.md` §結尾，這幾句不必是
  事實、步驟、理由或結果。第二、三輪盲評把片尾重述的四句與「帶數字的答案」都拿掉了，
  所以 `outro` 只剩這兩句；奇聞檔案局的 `outro` 卡本來就只帶訂閱。
  卡片本身的「未結」是主張，記在 c45。


## H02.md 查核過、這一版沒有講的主張

| 主張 | 為什麼沒講 |
| --- | --- |
| 南邊那座島離羅阿諾克約五十英里（Smithsonian 2020「about 50 miles south of Roanoke」） | 懷特寫的五十英里是**內陸**那一段，這個五十英里是今天的報導給的距離；H02.md 明說兩者不是同一件事，為了不讓觀眾把兩個數字混在一起，旁白只留內陸那一個（`ro322`／`ro604`），南邊只說「今天的哈特拉斯島一帶」 |
| 懷特一五九〇年八月十五日傍晚（EV 寫十六日）下錨 | 來源分歧且不影響故事；上岸日十八日沒有爭議，旁白只講十八日 |
| 懷特記述把留下殖民地的年份印成一五八六 | H02.md 明說那句不引 |
| 外孫女的名字 Virginia Dare | 她被白人至上團體當象徵（Smithsonian 2020），H02.md 要求不碰血統說法；旁白只說「總督的外孫女」「第一個在維吉尼亞出生的英格蘭孩子」 |
| 曼提歐（Manteo）是克羅托安島出生的人 | 湊不進長度；島上住的是誰那一句已經交代 |
| 一五九〇年翻船淹死七人、George Howe 被殺、前一批駐軍的骸骨、一五八六年酋長被砍頭 | H02.md 的「不畫」與「死亡只講一次、不給細節」規則；這一版完全不提 |
| 內陸工地的名字 Site X 與 Site Y | 拉丁字不在 `docs/videos/lexicon.json` 裡（字典不在這份工作的範圍內），旁白改說「兩個工地」「其中一個工地」，卡片寫「內陸工地」 |
| Cape Creek 遺址、Bristol 大學、East Carolina 大學、First Colony Foundation 的英文名 | 同上：拉丁字不在字典裡。旁白說「那座島上」「一所英國的大學」「一所大學的考古學家」「同一個基金會」，出處留在這份 claims.md 與說明欄 |
| 一九九八年 Science 論文的作者與期刊名 | 旁白不唸出處（§句子）；卡片的 `source` 寫「Science 1998、NPS 2026-10-10」 |
| 一九三七年那齣戶外劇的首演地點 | 查核一（2026-10-13）指出引用到的來源沒有一個寫出首演的劇場或地點（NCpedia 只有一張 Fort Raleigh 演出照片的圖說），所以 `ro416` 只說「開始上演」 |
| 一八三〇年代那本把它寫成浪漫懸案的「歷史書」 | 指名 Bancroft 一八三四年美國史的是 Coastal Review 2018，既不在 `sources[]`、也不在 c29 的出處裡；旁白照 Smithsonian 2020 說「一本書和一篇雜誌文章」 |
| 殖民者在島上待了乾旱的那三年 | 沒有來源這樣寫；他們幾時離開羅阿諾克正是這一集說沒有定論的事，所以 `drought-stats` 的標籤只說「論文算出的乾旱年份」 |
| 六張公有領域圖片與兩張未核准的圖 | `cute-mystery` 的 `drama` 形狀沒有照片卡（票 `2026-10-10-photo-paste-card`）；大英博物館那兩張還要站主決定 |
