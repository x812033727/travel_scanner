# curio-h01 查核第二輪

- 查核 2026-10-10，Claude Fable 5.1（第三個代理：不是撰稿的，也不是第一輪查核的那一個）。
- 範圍照查核提示的第二輪規則：第一輪 9 條 CHANGED 與 2 條 NOT FOUND 全部重查（#6、27、36、50、65、90、92、100、102、105、109），再從 112 條 CONFIRMED 裡隨機抽三分之一（38 條）。抽樣用 `<home>\mokaair-work\videos\curio-h01\_tools\verify2\sample.mjs`（mulberry32，**seed 20261010**，Fisher–Yates 洗牌取前 ⌈112/3⌉），結果存 `sample.txt`：#3、4、8、9、15、17、18、28、31、34、39、44、45、56、57、58、61、62、67、69、71、73、76、78、83、86、88、91、96、97、103、111、112、114、121、124、126、128。編號沿用 `verify-1.md` 的主張表。
- 方法：`video.json` 重新抽成 263 條（`claims-list.txt`，與第一輪同一支 extract.mjs）；第一輪的 24 個網址全部當天用 curl 重開（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒，去掉註解後讀全文），另外開了 maryceleste.net 站內第一輪沒開的 9 頁，其中兩頁是一手文件的全文轉錄：**Austin 勘驗報告（1872-12-23，Fay 1942 自照相版轉錄）** 與 **Dr. Patron 化驗報告（1873-01-30）**，兩頁已加進 `video.json` 的 `sources`。網路搜尋用了 1 次（5 次以內）。
- 改動原則同第一輪：只改事實與連帶的地方；行 id 不變；沒有加場景或句子；每句維持 24 單位以內。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| SM07 | https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/ | 200 |
| EB | https://www.britannica.com/topic/Mary-Celeste （curl 今天開得了） | 200 |
| AH | https://www.americanheritage.com/mystery-mary-celeste | 200 |
| MCN/index | https://www.maryceleste.net/ | 200 |
| MCN/facts | https://www.maryceleste.net/facts.htm | 200 |
| MCN/news | https://www.maryceleste.net/news.htm （Gibraltar Chronicle 1872-12-13、1873-01-31、03-04、03-15） | 200 |
| MCN/survey | https://www.maryceleste.net/survey.htm （Austin 報告全文，第一輪沒開） | 200 |
| MCN/doctor | https://www.maryceleste.net/doctor.htm （Patron 化驗報告全文，第一輪沒開） | 200 |
| MCN/doyle | https://www.maryceleste.net/doyle.htm （道爾小說第一部） | 200 |
| MCN/spencer、briggs、barrel、about、derelict、court、crew、time、genoa、gib | https://www.maryceleste.net/…htm | 200 |
| THP | https://thehistorypress.co.uk/article/the-ongoing-mystery-of-the-mary-celeste/ | 200 |
| HH | https://www.historyhit.com/ghost-ship-what-happened-to-the-mary-celeste/ | 200 |
| FV | https://fishermensvoice.com/archives/201711TheMysteriousCaseOfTheMaryCeleste.html | 200 |
| NEHS | https://newenglandhistoricalsociety.com/mysterious-disappearance-mary-celeste/ | 200 |
| SL | https://www.slate.com/articles/life/culturebox/2011/12/the_mary_celeste_the_unluckiest_ship_to_ever_sail_the_seven_seas_.html | 200 |
| SK | https://skeptoid.com/episodes/289 | 200 |
| WS | https://en.wikisource.org/wiki/J._Habakuk_Jephson%27s_Statement | 200 |
| ACD | https://www.arthur-conan-doyle.com/wiki/Mary_Celeste | 200 |
| C-Amazon / C-Engraving / C-Briggs / C-Sarah / C-Sophia / C-NYT | 六個 Commons 檔案頁（網址同 `assets[]`） | 200 |
| LoC | https://chroniclingamerica.loc.gov/ 搜尋（找 1873–1883 年的報紙轉述） | 403，Cloudflare 擋 → NOT OPENED |
| PP | https://paperspast.natlib.govt.nz/ 搜尋 | Incapsula 擋，空白頁 → NOT OPENED |
| IA | https://archive.org/advancedsearch.php （"Marie Celeste" 1873–1883） | 200，只回法文小說，無關 |
| CDC | https://visitportsmouth.co.uk/conan-doyle/blog/read/2025/03/mary-celeste-or-marie-celeste-b137 （搜尋摘要說 1883-06 洛杉磯時報已有 "standing untasted and scarcely cold"） | 200 但轉到部落格首頁，文章不在；/blog/2025/03 回 404 → NOT OPENED |

## 主張表

判定：CONFIRMED 看到了／CHANGED 改了／NOT FOUND 沒看到，拿掉或換掉／OUT OF SCOPE 不動。「第一輪」欄是第一輪的判定。

### 第一輪改過或沒找到的 11 條

| # | 主張（第一輪改後的現狀） | 位置 | 來源 | HTTP | 第一輪 | 第二輪判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|---|
| 6 | 「只有大約估值五分之一的救難金」 | youtube.description | MCN/news 1873-03-15：$5,700＋$36,943＝$42,643，£1,700「may be set down as one fifth」；SM07 說投保值 $46,000 的六分之一；FV 1/5 | 200 | CHANGED | CONFIRMED（第一輪的改法成立） | — |
| 27 | 「小艇都在，是一八八四年一篇小說加的，熱飯菜更晚才有」 | legend-writer/k2wi | WS 全文：「The boats were intact and slung upon the davits」有，飯菜沒有（全文 breakfast／meal／warm／hot 只出現在敘事者自己的日記）；AH「Other romancers added… a partly consumed breakfast… cups of tea that were still lukewarm」沒有年份；MCN/facts 第 3 條只說 erroneously reported；SK 說道爾加了 meals——與原文不符。「更晚才有」沒有任何開得了的來源給先後；唯一有年份的是搜尋摘要裡的 1883-06 洛杉磯時報（早於道爾），頁面開不了 | 200 | CHANGED | CHANGED（先後拿掉） | 小艇都在，是一八八四年一篇小說加的，熱飯菜更晚才有。 → 小艇都在，是一八八四年一篇小說加的，熱飯菜不是它加的。（22 單位） |
| 36 | 第 3 章卡片「1872 年 12 月 4 日（船上日誌記 5 日）」 | find-chapter.data.subtitle | MCN/facts 第 6 條（12-04 下午 1–2 時，Dei Gratia 日誌海時 12-05）；MCN/time 同；Chronicle 1873-01-31「on the 5th」；AH、FV、NEHS、HH、ACD 4 日 | 200 | CHANGED | CONFIRMED | — |
| 50 | 「十二月四日下午，日誌記五日，另一艘英國船看到她怪怪的」 | find-lookout/ympw | 同 #36；FV「at 1 p.m.… sails were set in an odd manner」 | 200 | CHANGED | CONFIRMED | — |
| 65 | 對照卡出處「左：道爾 1884 與後來的轉述」 | find-compare-legend-record.data.source | 同 #27：「後來的」也是先後的斷言，拿掉 | 200 | CHANGED | CHANGED | 左：道爾 1884 與後來的轉述 → 左：道爾 1884 與其他轉述 |
| 90 | 「船長的劍、衣服、玩具，小孩的衣服都在」 | list-child-dress/cw9n | AH「dresses… articles of child's wearing apparel; also child's toys」、劍在床下；Austin 第 37–46 段：船長艙有風琴、書、小孩高腳椅、藥箱、劍、一袋女士衣物；沒有縫紉機 | 200 | NOT FOUND→玩具 | CONFIRMED（玩具成立）；插圖 prompt 另改，見 R1 | — |
| 92 | 對照卡「衣服、小孩衣物、玩具」 | list-compare.data.right.points[3] | 同 #90 | 200 | NOT FOUND→換 | CONFIRMED | — |
| 100 | 表格「海盜、叛變」提出者「當年的檢察總長與報紙」 | theories-table row 2 col 2 | AH 12-18 聽證（proctor：船員酒後殺了 Briggs 夫婦與大副）；THP 1873-01-22 信；C-NYT 全文「seized by pirates」（Boston Post 1873-02-24）；SK「some believed piracy」 | 200 | CHANGED | CONFIRMED | — |
| 102 | 表格「保險詐騙」提出者「當年就有的猜測」 | theories-table row 3 col 2 | SK「Early theories quickly focused on… insurance fraud」；HH「Insurance fraud and foul play were immediately theorised」 | 200 | CHANGED | CONFIRMED | — |
| 105 | 表格「酒精蒸氣、怕爆炸」提出者「當年的船主，後來的研究者」 | theories-table row 5 col 2 | AH：Morehouse 相信氣體「rumble menacingly」、船主 J. H. Winchester 主張自燃掀開前艙蓋；Cobb 的完整版本由 Bryan 與 Fay 1942 採用；沒有來源給 1920 年代 | 200 | CHANGED | CONFIRMED | — |
| 109 | 表格「誤判進水」提出者「1873 年的美艦艦長，2007 年的紀錄片」 | theories-table row 6 col 2 | MCN/news 1873-03-04 Shufeldt「leaked so much as to seriously alarm the master」；SM07 2007（MacGregor、ICOADS、天文鐘 120 哩、煤灰） | 200 | CHANGED | CONFIRMED | — |

### 隨機抽的 38 條 CONFIRMED

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 3 | 1,701 桶酒精、六個月糧食、不見的小艇與航海儀器 | youtube.description | SM07、AH；Chronicle 1873-01-31 | 200 | CONFIRMED | — |
| 4 | 直布羅陀副海事法院的三個月 | youtube.description | SM07「After more than three months」；HH「after three months of deliberation」；12-18 開庭→03-14 判決 | 200 | CONFIRMED | — |
| 8 | 資料截至 2026-10-10 | youtube.description | 當天 | — | CONFIRMED | — |
| 9 | 標籤 | youtube.tags | — | — | CONFIRMED | — |
| 15 | Sophia 肖像「before 1872」、Unknown author、公有領域 | assets[4]、find-sophia-portrait | C-Sophia：Date「before 1872」、Unknown author、PD-old-100 | 200 | CONFIRMED | — |
| 17 | 一八七二年船還在走，十個人全不見 | hook/mwbb、hook.data | AH「beating northwest under very short canvas」；EB「10 people」 | 200 | CONFIRMED | — |
| 18 | 1872 年 12 月，大西洋 | hook.data.subtitle | AH、MCN/facts 15 | 200 | CONFIRMED | — |
| 28 | 第一段原文 "the derelict brigantine Marie Celeste" | legend-doyle-quote.data | WS 第一段逐字；MCN/doyle 同 | 200 | CONFIRMED | — |
| 31 | 小說裡連船名都拼錯 | 6xr9 | WS、ACD「he spelled the vessel's name as Marie Celeste」、MCN/facts 1 | 200 | CONFIRMED | — |
| 34 | 在葡萄牙外海被發現，離百慕達幾千公里 | legend-chart/j54f | HH「near to the Azores Islands, off the coast of Portugal」；AH「midway between the Azores and Portugal」；FV「nowhere near the Bermuda Triangle」；MCN/about「far, far away」；38°20'N 17°15'W 到百慕達約 4,300 公里是我算的 | 200 | CONFIRMED | — |
| 39 | Briggs 37 歲、麻州 Marion 人 | find-briggs-portrait.data.caption、5imz | NEHS「then 37」；SM07「hometown of Marion, Massachusetts」；C-NYT「of Marion, Mass.」（NEHS 開頭寫 Wareham，少數） | 200 | CONFIRMED | — |
| 44 | 七歲兒子亞瑟留在家上學 | find-son-at-school/u2sf | SM07「the 7-year-old son the Briggses had left behind so he could attend school」；MCN/briggs | 200 | CONFIRMED | — |
| 45 | Sophia Matilda Briggs，1870-10-31 生，上船時剛滿兩歲 | find-sophia-portrait.data、66tg | MCN/briggs「On October 31, 1870, Their daughter Sophia M. was born」；SM07 2-year-old；ACD「Sophia-Matilda」 | 200 | CONFIRMED | — |
| 56 | 甲板上的測深桿、兩具幫浦一具拆開 | find-sounding-rod/mgrf | EB、SM07、HH；Austin 第 49–50 段（一具幫浦的閥拆下來好把測深器放進井裡；測深器就在旁邊） | 200 | CONFIRMED | — |
| 57 | 3.5 英尺、約 1 公尺、船還能航行 | find-stats、nvhj | AH、SM07 3.5 呎；EB「more than 3 feet (1 meter)… seaworthy」；Chronicle 03-04「staunch and sea worthy」 | 200 | CONFIRMED | — |
| 58 | 1,701 桶，只有 1 桶被打開過 | find-stats、rtpc、2rum | Chronicle 1873-01-31「except one which had been started」；AH | 200 | CONFIRMED | — |
| 61 | 艙裡全濕、爐子撞歪、桌上沒有吃的 | find-galley/6y3w | MCN/facts 3–4（法庭證詞）；MCN/index 引法庭紀錄「the stove was knocked out of its place」（Austin 12-23 看到時爐子已歸位，旁白講的是上船當天） | 200 | CONFIRMED | — |
| 62 | 羅經櫃被撞歪、羅盤玻璃罩破 | find-binnacle/kjde | NEHS、FV；Austin 第 51–53 段（固定羅經櫃的壓條換過、兩片玻璃裂、一具羅盤被拿到船長艙） | 200 | CONFIRMED | — |
| 67 | 德沃帶兩個水手把船開到直布羅陀領救難金 | court-chapter/mnce | MCN/facts 8（Deveau、Lund、Anderson）；AH | 200 | CONFIRMED | — |
| 69 | 檢察總長索利弗拉德 | court-prosecutor/u7aq | SM07、HH「Attorney General of Gibraltar」；Austin 第 1 段「H. M's Advocate General… Proctor for the Queen」 | 200 | CONFIRMED | — |
| 71 | 推論：船員偷喝酒精、酒後殺了船長和大副 | court-letter/pdk7 | AH「murdered the Briggses and the chief mate」；THP 1873-01-22 信原文 | 200 | CONFIRMED | — |
| 73 | 船殼無傷、縫紉機油瓶直立 | court-oil-bottle/zz49 | Chronicle 1873-01-31；Austin 第 30 段（大副艙小架上的「縫紉機用油瓶」）；THP 的提醒照舊 | 200 | CONFIRMED（旁白）；插圖 prompt 改，見 R1 | — |
| 76 | 誰說的：檢察總長，在爭救難金的法庭上 | steps[1]、ecs7 | AH、SM07 | 200 | CONFIRMED | — |
| 78 | 美國軍艦艦長說船頭痕跡是海水撕裂的木頭 | court-bow-wood/c8ms | Chronicle 1873-03-04（Shufeldt、USS Plymouth：「splinters… forced off by the action of the sea」） | 200 | CONFIRMED | — |
| 83 | 大約只有船加貨估值的五分之一 | court-one-fifth/zkud | 同 #6 | 200 | CONFIRMED | — |
| 86 | 唯一的小艇不見，一邊欄杆放下，像正常放艇 | list-davits/t3k4 | SK「railings on one side… lowered indicating that the yawl had been launched normally」；AH「one boat was gone」；MCN/facts 2 | 200 | CONFIRMED | — |
| 88 | 六分儀和天文鐘不見 | list-sextant/xakr | AH、SK、FV | 200 | CONFIRMED | — |
| 91 | 六個月食物和水、1,701 桶貨都在 | list-stores/kua2 | AH、SM07 | 200 | CONFIRMED | — |
| 96 | 老船長帶著太太和兩歲女兒 | list-question/npuj | SM07、MCN/briggs（「老」是口語，37 歲；不動） | 200 | CONFIRMED | — |
| 97 | 至少七種說法 | theories-chapter/kp6j | SM07（叛變、海盜、海怪、水龍捲）、AH（章魚、宗教狂、海底火山氣體）、SK（詐保、海震）、EB（誤判進水） | 200 | CONFIRMED | — |
| 103 | 海底地震、水龍捲：船和貨無傷 | theories-waterspout/6jaz、table row 4 | SK（David Williams）；Chronicle 1873-01-31 第 2、3 點；Austin 第 4、57 段 | 200 | CONFIRMED | — |
| 111 | 表格出處：勘驗報告 1872-12-23 | theories-table.data.source | Austin 第 1 段「Monday the 23rd day of Decbr」；Chronicle 1873-01-31 | 200 | CONFIRMED | — |
| 112 | 1870 到 1890 年之間的版畫，繪者不明 | theories-engraving.data | C-Engraving「between 1870 and 1890」、「No illustrator given」、《300 Years of British Gibraltar》 | 200 | CONFIRMED | — |
| 114 | 線索在熱那亞卸貨時出現 | answer-chapter/s6yd、answer-nine-casks.data.kicker | MCN/about「when the cargo was finally unloaded in Genoa nine…」；MCN/barrel；SK 寫 Gibraltar（少數） | 200 | CONFIRMED | — |
| 121 | 帆還張著船繼續走，小艇越離越遠 | answer-sailing-away/9wsg | AH（Cobb 假說）；SK | 200 | CONFIRMED | — |
| 124 | 小艇和十個人從來沒有被找到 | answer-never-found/4f9b | Chronicle 1873-01-31「not a word has been heard, nor a trace discovered」；SK | 200 | CONFIRMED | — |
| 126 | 船沒沉、騙局拆穿、陪審團七比五、三個月後過世 | answer-boston-jury/u2ek | EB「failed to sink」；SL（1885 年 7 月審判、deadlocked 7-5、「three months after his trial」）；FV | 200 | CONFIRMED | — |
| 128 | 10 個人、1 艘小艇、9 個空桶；沒有定論 | outro.data、mnjn | EB、AH、SM07、MCN/barrel | 200 | CONFIRMED | — |

### 這一輪另外處理的

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| R1 | 兩張插圖 prompt 畫了縫紉機（第一輪留給撰稿方的未決點 a） | court-oil-bottle.data.prompt、list-child-dress.data.prompt | Austin 全文：第 30 段是「oil for a sewing machine」、棉線軸、頂針在大副艙小架上；第 37–39 段船長艙是風琴、書、小孩高腳椅、藥箱；Chronicle 1873-01-31 同；AH 列 child's toys；「艙裡有一台縫紉機、線軸立在上面」只在 WS 道爾小說（MCN/index 也說油瓶立在縫紉機上是 invention）；SL 的「sewing machine」是第三方轉述 | 200 | NOT FOUND → 改 prompt | 油瓶：「on the lid of a sewing machine in a tidy cabin… a thimble beside it」→「on a little wooden bracket shelf in a tidy mate's cabin… a thimble and a reel of cotton beside it」；小洋裝：「beside a hand-cranked sewing machine, a wooden spool of thread on the machine's bed」→「beside a little child's high chair, a wooden toy boat resting on the chair's seat」（景別、地點、單一主體、光線都沒動；英文，274／242 字元） |
| R2 | 卡片出處「道爾 1884 年的小說，與後來的轉述」 | legend-list.data.source | 同 #27 | 200 | CHANGED | 與後來的轉述 → 與其他轉述 |
| R3 | 說明欄「哪些是後來小說加進去的」 | youtube.description | 熱飯菜、海怪、百慕達都不是道爾的小說加的（AH、MCN/about） | 200 | CHANGED | 後來小說加進去的 → 後來才加進去的 |
| R4 | 「一位醫生化驗」（第一輪懷疑沒改） | court-chemist/rby8 | MCN/doctor：報告署名「J. PATRON M.D.」 | 200 | CONFIRMED（疑點解除） | — |
| R5 | `sources` 新增兩筆 | sources | MCN/survey、MCN/doctor，checked_on 2026-10-10；標題縮短後說明欄 ≤ 5,000 bytes | 200 | — | 18 筆 → 20 筆 |

## 摘要

- 查了 49 條（11 條第一輪改過或沒找到的＋38 條隨機抽的，seed 20261010）＋ 5 條這一輪另外處理的：CONFIRMED 45（第一輪的 9 處改法有 7 處成立），CHANGED 5（對應 **2 個事實**：熱飯菜的先後、插圖裡的縫紉機；連帶改了 k2wi、兩張卡片的出處、說明欄一句、兩個 prompt），NOT FOUND 1（縫紉機→改 prompt，已計入上面）。沒有數字改動，沒有 `say`／`say_for` 要補。
- 兩個未決點：(a) **縫紉機**——沒有任何權威來源把縫紉機列為船上的東西：Austin 1872-12-23 的報告原文只有「縫紉機用的油瓶、棉線軸、頂針」（大副艙小架上）與船長艙的風琴、高腳椅、藥箱；縫紉機本身出自道爾 1884 的小說。兩個 prompt 已改。(b) **熱飯菜的先後**——道爾原文確定沒有飯菜、有「小艇都在」；但「更晚才有」沒有來源：AH 的「Other romancers added」沒標年份，唯一有年份的線索（1883 年 6 月洛杉磯時報 "standing untasted and scarcely cold"，比道爾早）只在搜尋摘要裡，Conan Doyle Collection 的那篇部落格與 Chronicling America、Papers Past 都開不了。依規則 NOT FOUND 就拿掉斷言：旁白改成「熱飯菜不是它加的」，兩張卡片的「後來的轉述」改成「其他轉述」。**仍未解決**：熱飯菜最早出自誰、哪一年；如果站主要在旁白講先後，需要有人開得了 1883-06 的洛杉磯時報或 Begg／Hicks 的書。
- 與 brief 的衝突：brief 的「觀眾看完能做到的事 1」與「你以為／其實」寫「熱早餐是十二年後一篇小說加進去的」——來源不支持（道爾原文沒有熱早餐），影片已照來源改；brief 沒動，請站主決定大綱的講法要不要跟著改。
- 會過期的事實：沒有。看到的頁面日期：Britannica 頁標「Last updated Sep. 18, 2026」、AH 1981-02／03（頁面標 October 2026 重新上架）、SM07 2007-11、THP 2023-01-05、SK 2011-12-20、SL 2011-12、ACD 2021-10-31、NEHS「updated in 2026」。
- 意見：dxy5「我的看法是…」與 qa9h「目前最站得住的版本」標法不變，與 brief 的站主觀點一致；沒有不符。
- 聽眾檢查：118 句最長 24 單位（k2wi 改後 22）；沒有超過 40 字的句子；沒有「經查證」「根據官方文件」「本影片」；拉丁字只有 Dei Gratia，在 lexicon.json；沒有括號或網址；reveal 都在介紹該項的句子上。
- 內容守則：傳說都標成後來加的（現在不講先後，只講不在道爾原文裡）；沒有定論；沒有編造 Briggs 一家的對話或心理；沒有血腥。照片六張的說明與出處對得上 Commons 頁；1873 年剪報只用了標題。
- Lint：`node tools/video/cli.mjs lint --slug curio-h01` 改後 **0 錯誤**、1 個原本就有的警告（outro 三句共用一個畫面 14.4 秒）。估計 11.0 分鐘、118 句、2,303 單位。
- 懷疑但沒改的：
  - gb9h／表格第 1 列「海怪和百慕達三角，出處是後來的小說和轉述」：道爾的小說裡沒有海怪（是復仇情節），海怪是「當年就有的說法」（MCN/about「A popular theory at the time was that a giant squid, octopus, kraken…」）與後來作者的轉述（AH）；「小說」若讀成泛指的「虛構作品」還說得通，讀成道爾那篇就不對。沒抽到這條（#98），留給站主或撰稿方決定要不要改成「後來的轉述」。
  - 6y3w「廚房的爐子被撞歪」：法庭證詞（MCN/facts 4）說爐子被撞離位、水一兩呎深；Austin 12-23 看到時爐灶與炊具「in good order」——兩者差了兩週半（THP 提醒救難船員會先把船整理好）。旁白講的是上船當天，保留。
  - zz49「連縫紉機的油瓶都還直直立著」：Austin 原文是「oil for a sewing machine」，旁白的講法準確；但 THP 提醒這是船到港兩週半後、可能被整理過的狀態，Dei Gratia 的人作證時沒提到油瓶。保留（旁白說的是驗船結果）。
  - 55b2「工業用的，不能喝」、6mmb「七個船員」、hnsv「十一月七日」：沒抽到，第一輪的保留理由今天重讀各來源仍成立（SM07 industrial、NEHS／FV denatured；SK 說食用級穀物酒精仍是一對四）。
  - 9i5z「第三次作證」、c8ms Shufeldt：仍是單一來源（THP、Chronicle 轉錄），第一輪已註明，保留。
  - C-NYT 內文的「11 月 17 日出港」「約 236 噸」「towed into Gibraltar」與他源不合，旁白只用標題，沒事。
- 程序註記：沒有跑任何 git 指令；沒有改 brief.md、research.md；helper 在 `<home>\mokaair-work\videos\curio-h01\_tools\verify2\`（fetch.sh、fetch2.sh、totext.mjs、extract.mjs、sample.mjs、listener.mjs、apply-edits.mjs；下載的頁面在 `dl/`）。
- **第三輪：不需要**（這一輪改了 2 個事實，不超過 3 個）。但熱飯菜的最早出處仍是未解的點，腳本現在的講法迴避了先後，不算有錯。
