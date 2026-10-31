# curio-h09-v2 查核第一輪

- 範圍：`video.json` 全部 149 行旁白、卡片文字、`youtube.title`、`youtube.description`、`thumbnail.data`、畫面提示詞。`claims.md` 只當線索。
- 日期：2026-10-31。所有網址當天重開（curl 用編輯部 User-Agent，或搜尋工具）；1939 情報、日本大使信、無線電紀錄第 2–3 頁是直接看 NARA 的掃描圖。
- 撰稿者說 Jantz 2018「全文付費，只讀摘要」：**TIGHAR 掛了全文 PDF**，這一輪讀了全文。全文推翻了 UPI 的裁縫說法，見 #41。
- 一句話結論：數字與引句大多站得住；最嚴重的是**褲子尺寸的來歷錯了**（#41）、**五年前應為六年前**（#55）、**還在世或過世未滿 70 年的人被畫出來**（#62、#63）。

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | 標題「消失 89 年，2026 年那座島上找到了什麼？」；縮圖「還沒找到飛機」「1937 最後一句話」 | CONFIRMED（問句，沒有斷言；確實找到物件。縮圖把答案講清楚，不強過紀錄） | 1937→2026 = 89；「did not find the wreckage」；「numerous artifacts」 | Purdue 2026-10-18 | https://www.purdue.edu/newsroom/2026/Q4/search-for-amelia-earharts-plane-continues-after-taraia-object-expedition-on-nikumaroro-rules-out-latest-hypothesis/ | ✅ |
| 2 | eh002 超過 25 萬平方英里，約 18 個台灣 | CONFIRMED | 「more than 250,000 square miles」；647,500 ÷ 約 36,000 ≈ 18 | DocsTeach | https://www.docsteach.org/documents/document/earhart-radio-log | ✅ |
| 3 | ch3-stats 262,281 平方英里（統計表合計）；eh050 船 48,000、飛機 149,000 英里；7 月 18 日收隊 | CONFIRMED（OCR 的 TOTAL 格是空的，262,281 是 94,800 + 167,481 的加總，沒有看到原圖那一格） | 94,800；167,481；48,000；149,000 | 海軍搜索報告第 08 號 PDF 第 9 頁 | https://www.archives.gov/files3/research/ameliaearhart/releases/2025/1217/080_PC31-22_146_08_Report_of_Earhart_Search_by_U.S._Navy_and_U.S._Coast_Guard_July_2_18_1937.pdf | ✅ |
| 4 | eh003 巡邏艇冒濃煙指路 | CONFIRMED | 「Commenced laying heavy smoke screen at daylight」；「smoking heavily in order to assist in being sighted」 | 海軍報告 | 同 #3 | ✅ |
| 5 | eh004 08:43 無線電訊息逐字 | CONFIRMED（掃描圖逐字） | 「KHAQQ TO ITASCA WE ARE ON THE LINE 157 337 … WL REPT MSG WE WL REPT THIS ON 6210 KCS WAIT」 | NARA 無線電紀錄第 3 頁（Bellarts 文件） | https://www.archives.gov/files/college-park/highlights/6210268-2016-003-ac.jpg | ✅ |
| 6 | eh013 六點十四分兩百英里、六點四十五分一百英里 | CONFIRMED | 「ABOUT TWO HUNDRED MILES OUT」（0614–15）；「ABT 100 MILES OUT」（0645–46） | NARA 無線電紀錄第 2 頁 | https://www.archives.gov/files/college-park/highlights/6210268-2016-002-ac.jpg | ✅ |
| 7 | eh016 07:42 那句 | CONFIRMED（掃描圖；DocsTeach 是整理過的版本） | 「WE MUST ON YOU BUT CANNOT SEE U BUT GAS IS RUNNING LOW BEEN UNABLE TO REACH YOU BY RADIO WE ARE FLYING AT 1000 FEET」 | NARA 無線電紀錄第 2 頁 | 同 #6 | ✅ |
| 8 | 「ONE HALF HOUR FUEL」（旁白沒用，只說「油不多了」） | CONFIRMED（旁白的保守寫法是對的。半小時確實在當天 Itasca 電報與海軍摘要裡，但**無線電紀錄 07:42 那行沒有這個數**；紀錄裡的「half hour」在 0645 與 0758，意思是回報時間。舊查核 #3 可補註，旁白不要改成半小時） | 「6002 EARHART CONTACT 0742 REPORTED ONE HALF HOUR FUEL AND NO LAND FALL」；另見報告「only one-half hour of fuel」與「1912 one-half hour fuel」 | 海軍報告；NARA 無線電紀錄 | 同 #3、#6 | ✅ |
| 9 | eh017 船回話對方像沒聽到；八點收到訊號測不出方向 | CONFIRMED | 「R MSG R QSA 5 … UNANSWD」；「WE RECD UR SIGS BUT UNABLE TO GET A MINIMUM」（0800–03） | NARA 無線電紀錄第 2 頁 | 同 #6 | ✅ |
| 10 | eh019 從來沒有雙向接通 | CONFIRMED | 「never made two-way voice or telegraph contact」 | 史密森尼 NASM | https://airandspace.si.edu/stories/editorial/answering-your-questions-about-earharts-disappearance-except-big-one | ✅ |
| 11 | eh009–eh011 兩英里長一英里寬、非加油不可、10 點起飛、18 小時 | CONFIRMED | 「only two miles long and one mile wide」；「refueling there was necessary」；「10 am local time」；「18 hour flight」 | 史密森尼 NASM | 同 #10 | ✅ |
| 12 | eh010 大概史上最有名的女飛行員 | CONFIRMED | 「probably the most famous female pilot」 | NASM 館藏說明 | https://airandspace.si.edu/collection-objects/model-static-lockheed-electra-amelia-earhart/nasm_A19600213000 | ✅ |
| 13 | eh012 34 段的第 31 段；不到四分之一 | CONFIRMED（來源之間有落差：普渡寫「third-to-last leg」，34 段的第 31 段是倒數第四；旁白照 NASM，不必改） | 「leg 31 of 34」；22,000 與 7,000（7,000／29,000 ≈ 24%） | NASM；Purdue 10-18 | 同 #10、#1 | ✅ |
| 14 | eh021 157／337 是羅盤上相反的兩個方向 | CONFIRMED | 「157 degrees (roughly southeast)」「337 degrees (roughly northwest)」 | TIGHAR Navigation FAQ（當事人） | https://tighar.org/Projects/Earhart/Archives/Forum/FAQs/navigation.html | ✅ |
| 15 | eh022 艇長判斷是太陽定位線 | CONFIRMED（原文是起航前半小時的假設，「判斷」可以） | 「line of position obtained was a "sun" line」 | 海軍報告，Itasca 艇長報告 | 同 #3 | ✅ |
| 16 | eh026 收訊極好；10:40 認定飛機下去 | CONFIRMED | 「reception excellent」；「At 1040, it was definitely assumed that the plane was down」 | 海軍報告 | 同 #3 | ✅ |
| 17 | eh028「因為旭日太刺眼，連濃煙都沒看到」（撰稿者疑點 3） | CONFIRMED（電文的 missed it 確實指島，但**這不是撰稿者自己併讀**：艇長同一早上的情勢判斷把煙列在一起。句首「相信」蓋得住；仍是假設，不是事實。另一份海軍分析寫南方能見度極佳、煙柱 40 英里外看得到，兩邊都是推測，旁白沒寫死。想更貼電文可改「逆著旭日沒看到島，雖然船一直冒著濃煙」，非必要） | 電文「MISSED IT IN THE GLARE OF RISING SUN THOUGH WE WERE SMOKING HEAVILY」；報告「Assume that plane may have missed smoke screen, ship or island visually due to their lying in the glare of the rising sun」 | 海軍報告 | 同 #3 | ✅ |
| 18 | eh029「所以他往西北開」 | CHANGED：eh029，見備註 A | 電文「SEARCH NORTH WEST QUADRANT」，但實際決定「between bearings 337 and 45 true」、「Searching throughout the day to the northward」 | 海軍報告 | 同 #3 | ✅ |
| 19 | eh030–eh031 洛杉磯四家電台；不能不理 | CONFIRMED | 「four separate radio stations at Los Angeles」；「could not consistently be ignored」 | 海軍報告 | 同 #3 | ✅ |
| 20 | eh032–eh033 Wailupe 電文 | CONFIRMED（「在水面上」譯 ABOVE WATER，可以） | 「281 NORTH HOWLAND CALL KHAQQ BEYOND NORTH DONT HOLD WITH US MUCH LONGER ABOVE WATER SHUT OFF」（OCR 校正）；0242 收到 | 海軍報告 | 同 #3 | ✅ |
| 21 | eh035–eh037 傍晚趕到、探照燈、21:00 的光、歸給天象 | CONFIRMED | 「Arrived about dusk」；「lights which had the appearance of flares」；「meteorological shower」 | 海軍報告 | 同 #3 | ✅ |
| 22 | eh039–eh042 截收不可信；第二階段推測在鳳凰群島陸地；線的東南 | CONFIRMED（線延伸到鳳凰群島不必靠 TIGHAR，報告自己就寫了） | 「subsequent analysis discredits the radio intercepts」；「on land and probably in the Phoenix Islands」；「a position through Howland Island and the Phoenix Group」 | 海軍報告 | 同 #3 | ✅ |
| 23 | eh043–eh046、eh049 7 月 9 日飛加德納；艦長報告；潟湖可迫降；四千噸貨輪 | CONFIRMED（「可以迫降」原文帶 it is believed；旁白掛「報告也寫」可接受） | 「9 July」；「No dwellings appeared on Gardner or any other signs of inhabitation」；「a land plane could make a forced landing there, and the occupants walk ashore」；「four thousand ton tramp steamer」 | 海軍報告；TIGHAR Colorado Search 寫 battleship | 同 #3；https://tighar.org/Projects/Earhart/Archives/Research/ResearchPapers/Coloradosearch.html | ✅ |
| 24 | eh047「帶隊飛行員一週後的信」 | CHANGED：eh047，見備註 B（內容對，文件種類錯；NOTES 的「那封信」與 claims S15 同） | 「signs of recent habitation were clearly visible」；TIGHAR 叫它「a report from Lt. John Lambrecht」；標題「Weekly News Letter – Aircraft Search of Earhart Plane」 | TIGHAR 抄本（Research Document #6，主旨據搜尋摘要） | https://tighar.org/Projects/Earhart/Archives/Documents/Lambrecht's_Report.html | △ |
| 25 | eh048 繞了又繞，沒有人揮手 | CONFIRMED | 「failed to elicit any answering wave」 | TIGHAR Colorado Search | 同 #23 | ✅ |
| 26 | eh044 東南約 400 英里 | CONFIRMED | 「about 400 miles southeast of Howland Island」；《國家地理》350 海里（約 403 英里）一致 | Purdue 10-12 | https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-crew-arrives-at-nikumaroro-launches-critical-phase-of-amelia-earhart-plane-search/ | ✅ |
| 27 | eh051「海軍的結論是：很可能落在兩百英里內的海面」；說明欄「落海是海軍一九三七年的結論」 | CHANGED：eh051，見備註 C（小） | 「the third phase was logically based on the assumption that the plane had landed in the water probably within two hundred miles」；「not above water upon conclusion of the search」 | 海軍報告 | 同 #3 | ✅ |
| 28 | eh052 史密森尼認為最合理 | CONFIRMED | 「The most reasonable explanation」 | NASM 館藏說明 | 同 #12 | ✅ |
| 29 | eh054 探測公司 2002 起三次、合計 3,600 多平方海里 | CONFIRMED（當事人的數字） | 「1860nm2 across 3 expeditions in 2002, 2006, and 2017」；「3610nm2」 | Nauticos | https://www.nauticos.com/ | ✅ |
| 30 | eh055 1939 年 1 月宣告死亡 | CONFIRMED | 「declared legally dead on January 5, 1939」 | NASM The Legend | https://airandspace.si.edu/stories/editorial/legend-amelia-earhart%E2%80%99s-disappearance | ✅ |
| 31 | eh006、eh057–eh064 兩封電報、名字拼錯、六分儀盒、超過四年 | CONFIRMED | 「ask Koata not to talk about skull which is just possibly that of Amelia Earhardt」；「Some months ago working party」；「Bones look more than four years old」 | TIGHAR 公布的殖民地檔案抄本與掃描 | https://tighar.org/Projects/Earhart/Archives/Documents/Bones_Chronology.html | ✅ |
| 32 | eh065–eh068 保密、追問、鞋底、火堆 | CONFIRMED（「猜」是轉述，原文是 my conclusion based on，可接受） | 「Keep matter strictly secret」；「state reason for believing it to be that of a woman」；「Only experienced man could state sex」；「based on sole of shoe」；「remains of fire, turtle and dead birds appear to indicate life」 | 同上第 2 頁 | https://tighar.org/Projects/Earhart/Archives/Documents/Bones_Chronology2.html | ✅ |
| 33 | eh069 卡納瓦棺木 | CONFIRMED | 「may prove of sentimental interest」；「"kanawa"」 | 同上第 3 頁 | https://tighar.org/Projects/Earhart/Archives/Documents/Bones_Chronology3.html | ✅ |
| 34 | eh070「一九四一年二月，箱子上了殖民地的船」 | CHANGED：eh070，見備註 D（小） | 蓋勒格 1940-12-27 的信已寫「are being handed to the Master, R.C.S. "Nimanoa"」；1941-02-06 Isaac 才說「has certain human remains on board」 | 同上第 3 頁 | 同 #33 | ✅ |
| 35 | eh071–eh074 代理醫官、扣四艘船、玻里尼西亞男性、虎頭蛇尾 | CONFIRMED | 「detaining all ships calling at Tarawa (at present four)」；「elderly male of Polynesian race」；「upwards of 20 years」；「Many thanks - rather an anticlimax!」 | 同上第 3 頁 | 同 #33 | ✅ |
| 36 | eh076–eh077 胡德勒斯 13 塊、不到半副、MALE、5 呎 5 吋半、45–55 歲 | CONFIRMED（身高另有 Jantz 全文「about 5'5.5"」佐證） | 「less than half of the total skeleton」；「that of a MALE」；「Average … 5 ft. 5.5 inches」；「between 45 and 55 years」 | 同上第 5 頁；Jantz 2018 全文 | https://tighar.org/Projects/Earhart/Archives/Documents/Bones_Chronology5.html | ✅ |
| 37 | eh078–eh080 祕書批示、蓋勒格改口、英國貨對法國貨 | CONFIRMED | 「cannot be that of the late Amelia Earhart」；「unfortunate native castaway」；「no sextant had actually been found」；「an English one of some age」；「dovetailing … French origin」 | 同上第 5–7 頁 | https://tighar.org/Projects/Earhart/Archives/Documents/Bones_Chronology7.html | ✅ |
| 38 | eh081–eh084 卷宗到八月、蓋勒格過世、珍珠港、1997 找到檔案、1999 起去斐濟 | CONFIRMED | 「Gallagher died at the end of September」；「no mention in the file at all」；「a series of negations」 | TIGHAR Fiji Bone Search II（當事人） | https://tighar.org/Projects/Earhart/Archives/Research/Bulletins/42_FijiBoneSearch.html | ✅ |
| 39 | eh103–eh104 Jantz 只有胡德勒斯的數字；方法不能假設是對的 | CONFIRMED | 「limited to seven measurements」；「cannot be assumed to be correct」 | Jantz 2018 全文 | https://tighar.org/Projects/Earhart/Archives/Research/ResearchPapers/BonesForensicAnalysis/03JantzPaper.pdf | ✅ |
| 40 | eh106 用照片估手臂 | CONFIRMED（全文就有，「據報導」可拿掉） | 「estimated using photographic evidence and regression analysis」；鳴謝 Glickman 估「the scale to estimate her arm length segments」 | Jantz 2018 全文 | 同 #39 | ✅ |
| 41 | eh108「裁縫替她做褲子時量的尺寸」；eh109「你去改褲子留下的數字，八十年後變成法醫證據」；ch6-tailor、ch6-tailor-b | CHANGED：eh108、eh109、兩個提示詞，見備註 E（**事實錯，照抄了 UPI**） | 全文：「came to light in 2017」；「Historic clothing seamstress Paula Guernsey took the measurements」；「inseam length and waist circumference taken from a pair of Earhart's trousers」。UPI 的「in preparation for a new pair of trousers」與論文不符 | Jantz 2018 全文，Materials and Methods；對照 UPI | 同 #39；https://www.upi.com/Science_News/2018/03/07/Bones-found-on-South-Pacific-island-belonged-to-Amelia-Earhart-study-concludes/4101520448446/ | ✅ |
| 42 | eh110–eh111、ch6-99 比 99% 的人更接近；強烈支持 | CONFIRMED（全文數字更細，樣本 2,776 人，她排第 19） | 「more similar to the Nikumaroro bones than 99%」；「Earhart's rank is 19 … 2,758 (99.28%)」；「strongly supports the conclusion」 | Jantz 2018 全文 | 同 #39 | ✅ |
| 43 | Jantz 研究的強度（撰稿者要查）；eh113 比喻 | CONFIRMED（旁白把強弱拆得對。**他自己也寫這不算正式認定**，是比 99% 更好的素材，建議 eh113 後加一句，見備註 F，非必要。統計評論部落格指出 99% 不是機率，與 eh113 同向） | 「Likelihood ratios of 84-154 would not qualify as a positive identification」；「preponderance of the evidence」 | Jantz 2018 全文；Forensic Science, Statistics & the Law 部落格 | 同 #39；https://for-sci-law.blogspot.com/2018/03/likelihood-ratios-for-amelia-earhart.html | ✅ |
| 44 | eh112 通訊社寫 99% 的把握 | CONFIRMED | 「Anthropologist Richard Jantz is 99 percent sure of it.」 | UPI 2018-03-07 | 同 #41 | ✅ |
| 45 | eh115 2015 年論文認為判對了，只讀到轉述 | CONFIRMED（全文仍付費；TIGHAR 頁有摘要） | 「his sex estimate was likely correct」 | Jantz 2018 摘要；TIGHAR 的 Cross-Wright 頁 | https://journals.upress.ufl.edu/fa/article/view/525 ；https://tighar.org/Projects/Earhart/Archives/Research/ResearchPapers/BonesForensicAnalysis/02Cross_Wright_Paper.html | ✅ |
| 46 | eh116 Jantz 不算局外人 | CONFIRMED（全文鳴謝更直接） | 1998 作者 Burns、Jantz、King、Gillespie；「Ric Gillespie and TIGHAR's resources enabled me to get information from Amelia Earhart's clothing」 | TIGHAR；Jantz 全文 | https://tighar.org/Projects/Earhart/Archives/Research/ResearchPapers/BonesForensicAnalysis/BonesForensicAnalysis.html | ✅ |
| 47 | eh119–eh121 諾里奇市號 1929、15 歲女孩、紐約市 | CONFIRMED（內容掛普渡與支持者，標得對；提示詞另見 #62） | 「In 1929」；「then a 15-year-old girl」；「New York City」；「Proponents of the castaway hypothesis believe」 | Purdue 10-16 | https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-weather-prevents-shore-work-for-third-straight-day-crew-to-extend-trip/ | ✅ |
| 48 | eh088–eh092 澳洲週刊、1943 電影、1949、1966 暢銷書 | CONFIRMED（全靠 TIGHAR 一家整理；eh088 標了，1949、1966 沒每句重標。電影另有 NASM；「幾乎就是她」有 TIGHAR「so thinly disguised」） | 「October 16, 1937 issue」；「could find no supporting evidence」；「imprisoned on Saipan, and dying of malnutrition and disease」 | TIGHAR Overview；NASM The Legend | https://tighar.org/Projects/Earhart/Overview/AEoverview.html | △ |
| 49 | eh094–eh096 兩小時節目；出自檔案館；沒有日期 | CONFIRMED | 「two-hour documentary special」；NARA 自己收錄「ONI # 14381 JALUIT HARBOR」；「not marked with a date」 | WPTV／CNN；NARA；National Geographic | https://www.wptv.com/news/national/amelia-earhart-mystery-photo-taken-too-early-to-be-missing-pilot ；https://www.archives.gov/news/topics/earhart | ✅ |
| 50 | eh097「首播當天」到網站輸入環礁名 | CHANGED：eh097，見備註 G（小） | 來源寫的是貼文日期：「noted in a July 9 post」；首播也是 7 月 9 日，但沒有說他哪一天查的。TIGHAR 另寫「Exactly who first discovered the photo in the book is not clear」 | National Geographic；TIGHAR 新聞稿 | https://www.nationalgeographic.com/history/article/amelia-earhart-lost-photograph-discredited-spd ；https://tighar.org/Projects/Earhart/presser_07_11_2017.html | ✅ |
| 51 | eh098–eh100、ch5-1935 照片真的印在 1935 年的書裡（撰稿者要查） | CONFIRMED（**書與日期有圖書館書目獨立確認**；照片對應靠 NatGeo 與 TIGHAR 兩家，兩家立場不同。NDL 內頁這次打不開。「遊記」照 NatGeo；書目其實是「寫眞帖」，可改「南洋寫真帖」，非必要） | CiNii：「海の生命線我が南洋の姿：南洋群島寫眞帖」，1935.10，コロール；NatGeo：「the 10th item」「page 44」「October 1935」「30 minutes」；TIGHAR：「October 10, 1935」「book page 44」 | CiNii；National Geographic；TIGHAR | https://ci.nii.ac.jp/ncid/BA50227442?l=en | ✅ |
| 52 | 碼頭 1936 年才蓋好的主張（撰稿者疑點 2） | OUT OF SCOPE（旁白沒講。原始部落格找不到；只看到論壇摘要說照片裡是珊瑚堤、混凝土碼頭更晚。1939 情報第 2 頁也寫混凝土碼頭當時才「to begin there shortly」，與 1935 年有另一座舊堤不衝突。沒有東西推翻 1935 年的書目） | 「construction on a concrete dock was to begin there shortly」 | NARA 1939 情報第 2 頁 | https://www.archives.gov/files/news/rg-38-entry%2081-a-4-3-earhart-2017-002_ac.jpg | △ |
| 53 | eh101「我翻過的這些紀錄裡，沒有一份能把她放到日本人手裡」（撰稿者疑點 2） | CHANGED：eh101，見備註 H（**這份情報已讀**：標題就寫她是俘虜，內容是一封匿名瓶中信。不能證明，但不提就像沒這份東西） | 「REPORT OF AMELIA EARHART AS PRISONER IN MARSHALL ISLANDS」；「papers found in a bottle washed ashore near Bordeaux」；「I have seen Amelia Earhart (aviatrix)」；無署名。日本大使 1937 信只是致謝與關切，與俘虜無關：「no trace of Miss Earhart has yet been found」 | NARA 1939-01-07 情報三頁掃描；NARA 日本大使信 | https://www.archives.gov/files/news/rg-38-entry%2081-a-4-3-earhart-2017-001_ac.jpg ；https://www.archives.gov/files/news/earhart-japanese-ambassador.jpg | ✅ |
| 54 | eh146、ch7-open.sub、說明欄：俘虜說「拿不出證據」「查到的紀錄裡沒有證據」 | CHANGED：eh146、ch7-open、youtube.description，見備註 I（比 eh101 的範圍更強、沒有限定，且 eh093 自己說有目擊故事） | 瓶中信與目擊者都存在；「could find no supporting evidence or corroborating witnesses」；「a long list of names of witnesses」 | NARA；TIGHAR Overview | 同 #53、#48 | ✅ |
| 55 | eh141「五年前那棵椰子樹」 | CHANGED：eh141，見備註 J（**算錯**：eh127 自己寫 2020 年，到 2026 年是六年；五年前是 TIGHAR Tracks 的出刊年） | 「in September 2020」；美聯社稿「first seen in the satellite imagery six years ago」 | TIGHAR Tracks 37(2) 第 11 頁；美聯社稿（ABC30 轉載） | https://tighar.org/Publications/TTracks/2021Vol_37/TIGHARTracks37_02_June_2021.pdf ；https://abc30.com/story/expedition-remote-pacific-island-fails-find-fresh-clues-hunt-amelia-earharts-plane/19955590/ | ✅ |
| 56 | eh127–eh131 網友、機翼、兩週五十多則、椰子樹 | CONFIRMED | 「might be a wing」；「two weeks and more than 50 posts」；「a coconut tree」；「Mr. Ashmore did not agree」 | TIGHAR Tracks 37(2) | 同 #55 | ✅ |
| 57 | eh123–eh126 聲納、1,100 萬、岩石、上衣 | CONFIRMED（提示詞另見 #64） | 「believed to be found」；「cross-shaped」；「the Nov. 6 post」；「just a natural rock formation」；「$11 million」「selling off his commercial real estate」；「We find rocks」 | NBC；CBS／AFP | https://www.nbcnews.com/news/us-news/image-believed-show-amelia-earharts-plane-was-rock-formation-not-crash-rcna181578 ；https://www.cbsnews.com/news/sonar-not-amelia-earhart-plane-rock-formation-exploration-team/ | ✅ |
| 58 | eh132–eh133、eh144 三十張衛星圖、大概會確認、不是飛機也算成功 | CONFIRMED | 「26 additional」＋「three more」＋「another」＝30；「probably will be the confirmation」；「would still be a successful test」 | ALI | https://www.archaeologychannel.org/taraia/ | ✅ |
| 59 | eh007、eh134–eh137 17 人、普渡基金會出錢、炸出來的水道、太早下結論、連三天 | CONFIRMED（船上還有 17 名船員，eh007 的「十七個人」改「十七人的考察隊」更準，非必要） | 「17-person … supported by a 17-person boat crew」；「funded Earhart's Lockheed Electra」；「blasted channel」；「too early to reach conclusions」；「third straight day」 | Purdue 10-12、10-14、10-16 | 同 #26、#47；https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/ | ✅ |
| 60 | eh138–eh140、eh143、eh145、ch7-trees 很可能是大樹、Y 形一段、碳酸鹽、鋼管、仍相信（撰稿者疑點 1） | CONFIRMED（每個強度都貼原文，「很可能」保留。**現場判斷確實只有考察隊一個來源**；美聯社、Newsweek、Sky 都有報導，但都轉述這份公告，沒有獨立驗證。美聯社有獨立評論：前史密森尼策展人 Cochrane 說島已搜過 15 次以上。卡片標了考察隊公告；建議 eh138 旁白也標，見備註 K，非必要） | 「no conclusive evidence」；「likely a collection of large trees deposited along the peninsula's sandspit」；「a single Y-shaped segment」；「carbonate veneer」；「a steel tube about 30 inches long」；Cochrane：「searched more than 15 times, to no avail」 | Purdue 10-18；美聯社稿 | 同 #1、#55 | ✅ |
| 61 | eh142「它差不多是對的」（撰稿者疑點 1） | CHANGED：eh142，見備註 J（意見沒標成意見；公告只說 large trees 沒說椰子樹，論壇講的是一棵，公告是一堆） | 「a coconut tree」對「a collection of large trees」；「traveled five days by sea」 | TIGHAR Tracks；Purdue 10-18 | 同 #55、#1 | ✅ |
| 62 | ch6-girl、ch6-girl-b、ch6-norwich 畫出那個十五歲女孩 | CHANGED：三個提示詞，見備註 L（**違反真實人物規則**：她是具名的真人 Betty Klenck，過世未滿 70 年；說明欄也承諾這類人物不入畫） | TIGHAR wiki：1922–2014（據搜尋摘要）；Purdue 10-16 具名 | TIGHAR wiki；Purdue 10-16 | https://tighar.org/wiki/Betty | △ |
| 63 | ch7-ali-b、ch5-blogger、ch5-30min、ch7-sat 在世者的替身有臉 | CHANGED：四個提示詞，見備註 L（「field director」只對應帶隊的 Pettigrew；部落客 Yamano、網友 Ashmore 雖寫 anonymous，旁白正在講本人） | 「Rick Pettigrew, ALI, project director」；「Kota Yamano」；「Michael Ashmore」 | Purdue 10-18；National Geographic；TIGHAR Tracks | 同 #1、#50、#55 | ✅ |
| 64 | ch7-rock 與 ch7-rock-b 的畫面對調；ch4-shake 拿的東西不對 | CHANGED：三個提示詞，見備註 M（eh125 講岩石卻畫上衣、eh126 講上衣卻畫岩石；eh063 講六分儀盒卻畫鞋底） | 見左 | video.json | 無 | ✅ |
| 65 | 遺骸與骨頭不畫；詹茲、胡德勒斯、Isaac 不入畫 | CONFIRMED（全部提示詞搜 bone、skull、skeleton、remains 無命中；ch6-prof、ch6-prof-b、ch6-wire、ch6-rival-b 都只有手。遠征隊的 woman field researcher、TIGHAR 的 researcher 是不指名的通用角色，沒有對應單一個人，可留。ch7-purdue 的 elderly professor 若要對應當年校長就要換，目前未指名） | 無命中 | video.json | 無 | ✅ |
| 66 | eh005、eh025、eh063、eh113、eh117、eh122 意見與推論 | OUT OF SCOPE（都標得出是旁白反應；eh005「人應該不遠」是推論，有 reception excellent 撐） | 無 | 無 | 無 | ✅ |
| 67 | eh147 至今沒有確認的殘骸；說明欄其餘文字 | CONFIRMED（到 10-31 amelia.prf.org 最新公告仍是 10-18；鋼管仍在研究，上架前要再查） | 「did not find the wreckage」；Cochrane「have not found bona fide evidence」 | Purdue 10-18；美聯社稿 | https://amelia.prf.org/ | ✅ |

## CHANGED 的備註與建議改法

**A. eh029**：「所以他往北、往西北找，那條線東南那一頭，暫時沒有人去。」實際搜索扇形是 337° 到 45°，以正北為主；只有電報寫 north west quadrant。

**B. eh047**：「帶隊飛行員一週後交給航空局的週報，據研究團體抄錄，卻說島上清楚看得到最近有人住過的痕跡。」「信」是 Weekly News Letter 的誤讀，收件人是海軍航空局，不是私信。`claims.md` S15 與 `NOTES.md` 一起改。

**C. eh051**：「海軍最後是照這個假設找的：飛機很可能落在豪蘭島兩百英里內的海面。報告的結語是，人已經不在水面上了。」

**D. eh070**：「一九四一年二月，箱子跟著殖民地的船到了塔拉瓦，就出事了，出什麼事？」

**E. eh108、eh109、ch6-tailor、ch6-tailor-b**（必改）：
- eh108：「來自普渡大學收藏的她的一條褲子：二〇一七年，一位舊衣裁縫替研究量了褲長。」
- eh109：「你衣櫃裡一條舊褲子的長度，八十年後變成法醫證據，想想也是有點毛。」
- ch6-tailor：改成手的特寫，戴手套的手拿布尺量平放在檔案桌上的舊長褲，不畫裁縫的臉（Paula Guernsey 是具名的當代人物）。
- ch6-tailor-b：把 newly hemmed trousers 改成 old trousers。
- `claims.md` D02 與 `NOTES.md` 第 11 點要改，並把 D01／D02 的「全文付費」改成「TIGHAR 掛有全文 PDF」。

**F. eh113 之後可加（非必要）**：「他自己也寫，這個數字還不夠資格算正式認定。」

**G. eh097**：「節目首播那天，一位日本軍事史部落客貼文：他到日本國會圖書館的網站，輸入那座環礁的名字。」

**H. eh101**（建議兩句，拆鏡頭）：「我翻到最接近的一份，是一九三九年海軍情報裡的一封瓶中信，沒有署名，也沒有人證實。除此之外，這些紀錄裡沒有一份能把她放到日本人手裡。」要短一點就只留第一句加「這種東西，放不了她進日本人手裡」。`claims.md` 的 UNOPENED 列可以刪掉這份與大使信，並補來源。

**I. eh146、ch7-open、說明欄**：eh146「海軍推測在海裡，回收小組相信在島上，日本俘虜那一說只有查不實的故事。」ch7-open.sub「海裡、島上都有人信；俘虜說查不實」。說明欄「查到的紀錄裡沒有查得實的證據」。

**J. eh141、eh142**：「還記得六年前那棵椰子樹嗎？」「我覺得它方向差不多是對的，是樹，只是不只一棵，而且這次有人真的坐了五天船去看。」

**K. eh138（非必要）**：「十月十九日，考察隊公告：沒有確切證據，那個影像很可能是一堆沖上沙嘴的大樹。」

**L. 真實人物**：
- ch6-girl、ch6-girl-b、ch6-norwich：不要人。例如「一台大短波收音機與一本空白小筆記本放在窗邊桌上」「佛州小街黃昏，屋頂上的天線，窗裡亮著燈，沒有人影」「手指停在收音機旋鈕上」。
- ch7-ali-b：改成器材箱與碼頭，只留手。
- ch5-blogger、ch5-30min、ch7-sat：只留手與空白螢幕。

**M. 畫面**：ch7-rock 與 ch7-rock-b 的 prompt 對調；ch4-shake 的鞋底改成六分儀盒。

## 開不到或沒讀到的來源

| 來源 | 狀況 |
| --- | --- |
| 國立國會圖書館數位典藏的書頁（第 44 頁，TIGHAR 連結 pid/1223403/99） | 工具只拿到網站外殼；書目靠 CiNii，對應靠 NatGeo 與 TIGHAR |
| Cross & Wright 2015 全文 | 付費；只讀 TIGHAR 頁上的摘要與 Jantz 的轉述 |
| Lambrecht 週報原頁 | 內容靠 TIGHAR Colorado Search 抄錄；文件主旨只看到搜尋摘要，沒有直接開 Research Document #6 |
| Betty Klenck 生卒年 | 只看到 TIGHAR wiki 的搜尋摘要 |
| 「碼頭 1936 年才蓋好」的部落格、TIGHAR 論壇討論串 | 找不到，論壇頁回 404，只有搜尋摘要 |
| 《國家地理》2026 年 Taraia 報導 | 只看到標題，猜的網址回 404 |
| Deep Sea Vision Instagram、Smith's Weekly 原報、2017 年節目本身、Guardian 的 Yamano 訪談 | 沒開，靠 NBC、CBS、TIGHAR、NatGeo 轉述 |
| 海軍報告第 9 頁 TOTAL 那一格的原圖 | 沒有工具轉圖；262,281 是兩列加總 |
