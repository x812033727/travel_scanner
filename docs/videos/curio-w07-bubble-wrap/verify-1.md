# curio-w07-bubble-wrap 查核第一輪

- 查核者：獨立查核代理（Claude Opus 5.5，沒有參與寫稿），日期 2026-11-02。逐句讀 `video.json` 的旁白、字卡、標題與說明欄，對原始來源；`claims.md` 只當線索。
- 親自抓原始 HTML、去標籤後全文搜尋（不經模型轉述）：Google Patents 上 US3142599A、US3026231A、CH366388A、GB978654A、DE1237294B；史密森尼；AP／NBC；Forbes；史蒂文斯；Drumthwacket；encyclopedia.com 與 FundingUniverse 的公司史；IBM 1401 頁；電腦史博物館兩頁；CD&R；CNBC；New Equipment Digest；Dezeen；Fox；Wikipedia。USPTO 函件用 pdftotext 讀原 PDF。US 3,142,599 另把專利局 PDF 第 4 頁算圖、親眼對過首頁與用途句，PDF 文字層也搜過。
- 經 WebFetch 或 API：SEC R15（直接抓是 403，機器人政策；改走 WebFetch，得到逐列數字）；PubMed 兩篇（直接抓是 203 空殼；1994 摘要用 Europe PMC API 取得全文，1992 只有工具轉述與短引句）。
- 打不開、沒有嘗試繞過：sealedair.com（撰稿者記為安全驗證與 403，這輪沒再試）；WSJ 原文（付費牆，沒開）。
- 列號與 `claims.md` 相同；#42–#46 是這輪新增。#42 的瑞士專利已加進 `claims.md` 與 `video.json` 的 sources，旁白還沒用。

## 這輪改了什麼

| 行 | 問題 | 改法 |
|---|---|---|
| t064 | Forbes 原文是 Company legend holds，而且寫 a few years after 1960；舊句當成記者的直述（#19） | 「富比士標明是公司傳說：成立幾年後」 |
| t037、t123 | 把 1961 年當成「傳說」唯一的時間。公司史百科的順序是想到包裝在先、1960 成立在後；Drumthwacket 寫 1957；Forbes 寫成立幾年後（#11、#43） | t037 並列公司史百科；t123 改「比一九六一年那個說法早」 |
| t039 | 全片讓用途句序替「先後」作證，但沒有任何紀錄標出溫室的年份（#9、#44） | 補「排在前面不等於先想到」 |
| t029、t030、`p59-date` 字卡、loop | 「第一次明寫」「第二份」過強：史密森尼寫共六份，另有兩份更早的薄膜專利，這輪只讀了兩份 | 「我找得到最早」「下一份」「我找到的下一份」 |
| t021 | 原文是 useful, among other things, as a wall covering，不是「這是牆面材料」（#6） | 「這種壓紋材料，可以拿來當牆面」 |
| t024 | 原文沒有「最好用乙烯」，只說 vinyl plastic 耐用、可壓細紋（#7） | 「像乙烯塑膠」 |
| t044 | 「富比士只寫吹了」漏掉同句的 does an okay job holding heat，它其實站在有效那邊（#12） | 「保溫還算可以，可是這計畫也吹了」 |
| t065 | 「當時的執行長」聽起來像 1960 年代的人；Hickey 是 2006 年受訪、1980 年才進公司（#20） | 「二〇〇六年的執行長」 |
| t069 | 「講錯」把解讀放在「我覺得」外面；「回憶」不對，他沒經歷那段 | 「零件對不上不算什麼」「幾十年後才講的故事」 |
| t070 | Stephens 是 Product Care 事業部的副總（#22） | 「事業部副總」 |
| t076 | 用 1960 年的募股回答「接到客戶後賺翻了嗎」，時間倒置（#23） | 「倒回去看，公司一九六〇年」 |
| t091 | 公司史寫郵寄袋在 Dunphy 時代「之前」就加了，泳池蓋 1970 年代中、Instapak 1977，都排在 t092 的 1973 之前，暗示因果（#29） | 「鄧菲上任前後」「先是郵寄袋，幾年後才有」 |
| t002 | 103 億是企業價值，不是付給股東的錢（#27）；字卡寫對，旁白沒有 | 「連債算進去一百零三億美元」 |
| t111 | 是公司主管 Gillis 的話，距離從工廠算（#38） | 「引公司主管的話：離工廠超過」 |
| t118 | 社團 50 萬人不等於 50 萬人難過（#41） | 「五十萬人的社團」 |

旁白改過，`narrative` 雜湊變了，盲評要用新稿跑。

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | 流傳版本：壁紙、溫室、才想到包裝 | CONFIRMED（流傳） | Drumthwacket 順序相同，「Finally, in 1957」；史密森尼副標 accidental | 史密森尼；Drumthwacket | https://drumthwacket.org/interactive-map/alfred-fielding-and-marc-chavannes-bubble-wrap.html | ✅ |
| 2 | 史密森尼 2019 的敘述 | CONFIRMED | David Kindy，January 23, 2019；Swiss chemist；Beat generation；two pieces of plastic shower curtain；more than 400；「which was branded Bubble Wrap」語意可鬆可緊，旁白「讀起來像」站得住 | 史密森尼 | https://www.smithsonianmag.com/innovation/accidental-invention-bubble-wrap-180971325/ | ✅ |
| 3 | 紐約設計師上門 | CONFIRMED | 「a New York City designer approached」，出自公司公關 Aurichio。公司史另寫 a client's request | AP／NBC | https://www.nbcnews.com/id/wbna35046691 | ✅ |
| 4 | 機械工廠或車庫 | CONFIRMED | 「machine shop」；「garage in Hawthorne」；AP 還有第三種 small lab | 史蒂文斯；Drumthwacket；AP | https://www.stevens.edu/news/pop-sensation-bubble-wrap-appreciation-day-has-stevens-connection | ✅ |
| 5 | 1959-11-27 申請 | CONFIRMED（對專利局 PDF） | 「Filed Nov. 27, 1959, Ser. No. 855,712」；瑞士、德國同族也主張同日優先權 | US3142599 | https://patents.google.com/patent/US3142599A/en | ✅ |
| 6 | 1957 專利 | CHANGED | 「Filed Dec. 23, 1957」；Patented Mar. 20, 1962；Chavannes 一人；「useful, among other things, as a wall covering」 | US3026231 | https://patents.google.com/patent/US3026231A/en | ✅ |
| 7 | 沒有浴簾；做法；座面 | CHANGED（vinyl） | shower、curtain 全頁 0 處；vacuum 型滾筒；backing「preferably a treated or coated paper」；「soft, resilient and comfortable seating surface」 | US3026231 | 同上 | ✅ |
| 8 | CIP、1964 核發、界線 | CONFIRMED | 「continuation-in-part of my prior application filed December 23, 1957」；Patented July 28, 1964 | US3142599 | https://patents.google.com/patent/US3142599A/en | ✅ |
| 9 | 用途句；沒提電腦 | CONFIRMED（核發文本，算圖親眼對） | 「cushioning and shock absorbing applications as, for example, packaging of products, padding of furniture, cars and trucks, heat insulation and the like」。專利本文與 PDF 文字層 greenhouse、IBM、computer、electronic 都 0 處；HTML 的 computer 只在分類名與引用清單。句序不等於時間 | US3142599；專利局 PDF | https://patentimages.storage.googleapis.com/6d/dc/8a/9e8a092da33c32/US3142599.pdf | ✅ 文字／⚠ 推論 |
| 10 | 1960 成立 | CONFIRMED | 史密森尼、公司史、Forbes 一致 | 同列 | https://www.smithsonianmag.com/innovation/accidental-invention-bubble-wrap-180971325/ | ✅ |
| 11 | 1961 年才決定包裝 | CHANGED | 「It wasn't until they decided the next year」；公司史 1961 是量產。其他版本見 #43 | 史密森尼；公司史 | 同上 | ✅ 說法存在 |
| 12 | 溫室三種說法 | CHANGED（Forbes） | 「proved ineffective」；「some success」；「does an okay job holding heat, that plan didn't work, either」 | 史密森尼；公司史；Forbes | https://www.forbes.com/global/2006/0508/026.html | ✅ |
| 13 | 史蒂文斯：很快丟掉 | CONFIRMED | 「quickly tossed aside, as was insulation (which probably made more sense)」；Fielding '39 | 史蒂文斯 | https://www.stevens.edu/news/pop-sensation-bubble-wrap-appreciation-day-has-stevens-connection | ✅ |
| 14 | 費爾丁飛進紐瓦克 | CONFIRMED | 「according to company lore」「flying into Newark Airport」 | AP／NBC | https://www.nbcnews.com/id/wbna35046691 | ✅ |
| 15 | 夏凡納在小飛機上 | CONFIRMED | 「the story goes」「window of a small plane」 | 史蒂文斯 | 同 #13 | ✅ |
| 16 | 兩人 1994 過世 | CONFIRMED（單一來源） | 「each passed away in 1994」。沒找到第二份 | 史蒂文斯 | 同 #13 | △ |
| 17 | 流傳 IBM 第一個客戶 | CONFIRMED（流傳） | 「first client was IBM」，Wikipedia 引 Forbes，但 Forbes 沒寫 first client | Wikipedia | https://en.wikipedia.org/wiki/Bubble_Wrap_(brand) | ⚠ |
| 18 | 1401 發表、訂單、沒提包裝 | CONFIRMED | 「October 5, 1959」；「More than 5,200 orders … first five weeks」；packag、bubble、ship 0 處。10-05 到 11-27 為 53 天 | IBM | https://www.ibm.com/history/1401 | ✅ |
| 19 | Bowers 與 IBM | CHANGED | 「Company legend holds that a few years after Sealed Air was founded in 1960」。與下一句「IBM had just launched」和史密森尼的 1961 年有出入 | Forbes | https://www.forbes.com/global/2006/0508/026.html | △ 公司傳說 |
| 20 | Hickey 引句 | CONFIRMED，引文逐字相符 | 「Serendipitously, Bubble Wrap and vacuum tubes met」；公司史：joined 1980、CEO 2000 | Forbes；公司史 | 同上 | ✅ |
| 21 | 1401 是電晶體，對不上真空管 | CONFIRMED，比撰稿者找到的更強 | IBM 自己：「one of the first computers to run on transistors instead of power-hungry and fragile vacuum tubes」；CHM「one of IBM's earliest transistorized computers」；修復專案「transistors instead of tubes」。Hickey 可能只是泛指，所以 t069 用「對不上」 | IBM；CHM | https://www.ibm.com/history/1401 | ✅ 事實／⚠ 解讀 |
| 22 | Stephens 引句 | CHANGED（職稱），引文逐字相符 | 「It was the answer to IBM's problems」；vice president … Product Care Division | 史密森尼 | 同 #2 | ✅ |
| 23 | 85,000、1961、AirCap | CONFIRMED（一部公司史） | 「$85,000 raised」「began in earnest the following year」「originally called AirCap」。FundingUniverse、company-histories 等是同文轉載，不算第二來源 | 公司史 | https://encyclopedia.com/books/politics-and-business-magazines/sealed-air-corporation | △ |
| 24 | 漏氣與塗層 | CONFIRMED，第二來源部分支持 | 「slightly leaky bubbles」「by the middle of the decade」「special coating」；Forbes 獨立寫「The original polyethylene layer was permeable」，但沒寫年份與塗層 | 公司史；Forbes | https://www.forbes.com/global/2006/0508/026.html | ✅ 漏氣／△ 年份 |
| 25 | 商標 1968-10 | CONFIRMED | 「FIRST USE: 19681000」；Filing 19810831；Registered 19830802；Reg. 1247076，附在別家公司的官方函件裡。自報日期，字卡有但書 | USPTO | https://tmng-al.uspto.gov/resting2/api/casedoc/cms/case/97065744/office-action/OfficeAction5147662.pdf | ✅ |
| 26 | 1969、1970 | CONFIRMED（一部公司史） | 「sales of $4 million」「small deficit」「President Ted Bowers suddenly resigned」；旁白沒提名字。Bowers 見 #45 | 公司史 | 同 #23 | △ |
| 27 | 收購 | CHANGED（t002） | April 9, 2026；「enterprise value of $10.3 billion」 | CD&R | https://www.cdr.com/news/sealed-air-announces-completion-of-acquisition-by-cd-and-r | ✅ |
| 28 | Dunphy | CONFIRMED | 「an Irishman」「became CEO in 1971」；史密森尼同 | 公司史；史密森尼 | 同 #23 | ✅ |
| 29 | 產品線與 1973 | CHANGED（順序） | 「Just prior to the beginning of the Dunphy era」Mail Lite「first sold in 1971」；「mid-1970s」泳池蓋；Instapak 1977；「after-tax profits topped $1 million for the first time」。沒找到獨立第二來源，搜到的都是同文 | 公司史 | 同 #23 | △ |
| 30 | 1988 | CONFIRMED（一部公司史） | $346 million；$127 million；「more or less replaced Bubble Wrap as the flagship」 | 公司史 | 同 #23 | △ |
| 31 | 1998 Cryovac | CONFIRMED | 「valued at $4.9 billion」「sales triple」；Forbes 獨立寫 $4.9 billion | 公司史；Forbes | 同 #23 | ✅ |
| 32 | 不到一成 | CONFIRMED | 「provides less than 10% of total revenue」 | Forbes | https://www.forbes.com/global/2006/0508/026.html | ✅ |
| 33 | 2025 拆分 | CONFIRMED | Food 3,594.7；Protective 1,765.1；合計 5,359.8（百萬）。旁白「十七億六千萬」是截尾，字卡 17.65 億精確 | 10-K R15 | https://www.sec.gov/Archives/edgar/data/1012100/000101210026000016/R15.htm | ✅ |
| 34 | 霍華回憶 | CONFIRMED，引句相符 | about 5；「The adults at my father's firm likely did so for quality assurance」；「a lot bigger then」 | 史密森尼 | 同 #2 | ✅ |
| 35 | 1992 | CONFIRMED（工具轉述加短引） | Dillon，*Psychological Reports* 71(1)；30 名；「more energized, less tired, and more calm」 | PubMed | https://pubmed.ncbi.nlm.nih.gov/1529063/ | ✅ |
| 36 | 1994 | CONFIRMED（摘要全文） | 「control group having a lower mean」「contrary to our expectation」。摘要沒給 p 值與人數 | Europe PMC | https://pubmed.ncbi.nlm.nih.gov/7984719/ | ✅ |
| 37 | 氣泡紙日 | CONFIRMED | Spirit 95、Bloomington；2001；popping relay、sculpture contest | CNBC | https://www.cnbc.com/2012/01/30/pop-pop-pop-a-great-day-to-pop-some-bubble-wrap.html | ✅ |
| 38 | 150–200 英里、47 車 | CHANGED（出處） | Gillis：「from a … production facility … can be prohibitive」；「47 truckloads」；同文也寫 just under 1/50 | New Equipment Digest | https://www.newequipment.com/research-and-development/article/22058120/the-new-bubble-bubble-wraps-unpoppable-makeover | ✅ |
| 39 | 四十年與心願 | CONFIRMED | 「a 40-year quest」；Hickey 轉述 Fielding 生前的話。Forbes 另寫 40 車抵 1 車（2006 款），與 47 車是不同產品 | Forbes | https://www.forbes.com/global/2006/0508/026.html | ✅ |
| 40 | iBubble、1/50、原版不消失 | CONFIRMED，1/50 兩處都是轉引 | 「one-fiftieth」「The Wall Street Journal reported」；Fox「about 1/50」；「the original version you love to pop isn't going anywhere」。WSJ 原文未讀 | Dezeen；Fox | https://www.dezeen.com/?p=733264 | ✅ 轉引 |
| 41 | 社團 50 萬 | CHANGED（t118） | 「more than 502,000 members」「a stream of posts from sad fans」 | Fox | https://www.foxnews.com/tech/new-and-improved-bubble-wrap-takes-up-less-space-but-doesnt-pop | ✅ |
| 42 | 瑞士同族專利（新增） | CONFIRMED | 1961-01-04 申請、主張 1959-11-27 優先權、1962-12-31 公開；「par exemple pour l'emballage de produits, le rembourrage des meubles, des voitures et des camions, pour l'isolation thermique」。日期欄是 Google 著錄 | CH366388 | https://patents.google.com/patent/CH366388A/en | ✅ |
| 43 | 想到包裝的時間有四種（新增） | CONFIRMED | Drumthwacket 1957；公司史在 1960 成立之前；史密森尼 1961；Forbes 成立幾年後 | 同列 | https://encyclopedia.com/books/politics-and-business-magazines/sealed-air-corporation | ✅ |
| 44 | 溫室沒有年份（新增） | CONFIRMED（讀過的範圍） | 讀過的版本都只有順序，沒有日期、訂單、數字；所以專利不能證明「包裝早於溫室」 | 同 #12 | 同 #12 | ✅ |
| 45 | 兩位 Bowers 是否同一人（新增） | UNVERIFIED | Frederick W.（Forbes，行銷人）與 Ted（公司史，總裁）；搜兩輪找不到連結或否定。旁白 t064 只用姓，t084 只說總裁，沒有連起來 | Forbes；公司史 | — | ⚠ |
| 46 | 片尾字卡「比傳說早」（新增） | CONFIRMED（對 1961 版本） | 「最早寫下包裝的文件，比傳說早」：我們找到的紀錄裡如此，對 1957 的 Drumthwacket 版本則不成立，但那版沒有文件 | 同 #43 | — | △ |

## 其他判定

- **全集論點**：1959-11-27 申請與用途句都對到專利局 PDF，瑞士同族（1961 年 1 月遞件、1962 公開）句序相同。論點站得住的範圍是「1959 申請的專利文本已列包裝」。站不住的是「包裝早於溫室」「不是意外」，旁白已標「我覺得」，並補了 t039。
- **建議，沒改**：t038 的但書可以加一句瑞士同族，等於把文本的最晚時間從 1964 推到 1961 年初，對開場的論點有利。屬於寫稿選擇，交給撰稿者。美國申請原稿仍沒看到，t127 不變。
- **t036**「排在最前面」：核發文本的確如此，同一句是 for example 列舉，沒寫重要性排序。t039 已接住。
- **t085**：史密森尼原句 the company wasn't turning a profit，緊接 1971 年；公司史只明寫 1970 虧損，「第一次超過百萬」也不等於之前都賠。旁白標了史密森尼，t086「還在賠」屬可接受。
- **標題**「1959 年的專利早就寫著包裝」：不算過頭；核發年的但書在 t038 與說明欄。
- **縮圖**「壁紙？／1959 專利早寫著包裝」：同上。
- **提示詞**：沒有公司、人名；`p59-date` 字卡與 loop 已同步。`boss-others` 畫的是泳池蓋，t091 仍提到。`ibm-view` 畫老人回憶，與 t069 改後的語意略有落差，生圖前可換，但不算事實錯誤。
- **風險**：沒有暗示違法；1401 零件那句標成看法，沒有說執行長說謊。
- **lint**：0 錯誤，3 個警告（p59-worse 10.6 秒、ibm-bowers 11.1 秒、開場約 60 秒），前兩個來自查核補的但書。

## 仍只有單一或二手來源

1973 年獲利破百萬、1969 年 400 萬、1970 虧損與辭職、85,000 美元、漏氣的「1960 年代中期」塗層時間、1988 年 Instapak（都只有 *International Directory of Company Histories*，網路上的其他版本是同文）；兩人 1994 過世（史蒂文斯）；Bowers 與 IBM（Forbes 標公司傳說）；IBM 第一個客戶（Wikipedia，而且它引的 Forbes 沒這樣寫）；1/50（WSJ 轉引）。

無法證實：看雲的乘客是誰；IBM 訂單或採購文件；溫室有沒有賣出；1959 年美國申請原稿；兩位 Bowers 是否同一人。
