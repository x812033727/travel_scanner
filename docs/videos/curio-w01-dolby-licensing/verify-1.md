# curio-w01-dolby-licensing 查核第一輪

- 查核者：獨立查核代理（Claude Opus 5.5，沒有參與寫稿），日期 2026-10-31。逐句讀 `video.json` 的旁白、字卡、標題、說明欄與縮圖字，對原始來源，撰稿者的查核表只當線索。
- 親自打開並全文搜尋的原件：Dolby 2025 財年 10-K 本文與 R5、R13、R56；FCC 96-493 第四號報告與命令全文；史丹佛 Ray Dolby papers 典藏說明（OAC）；IEEE Spectrum 2013 轉載的 1988 年專訪；ETHW；47 CFR §73.682 與 §15.117（Cornell LII）；ATSC A/52 頁；Apple Newsroom；MediaTek 新聞稿；杜比 2026-10-12 新聞稿（Finviz 轉載）；Guinness；Wikipedia Dolby Stereo、Dolby Laboratories。
- 撰稿者沒開、這輪新開的：杜比 1998 年自編年表 *A Chronology of Dolby Laboratories*（Film-Tech 存檔，下稱「年表」）；Google Patents 上的 US3631365A 與 GB1120541A；Stereo Review 1977-03 Hirsch 專欄（存檔）；Electronic Design；Brunswick Review；encyclopedia.com 公司史；GoodWhale；Screen Rant。
- 打不開：Mix（403）、Cineworld（403），都不是必要來源。熱門影片的說明欄沒開（`brand-story` 定案不讀對方逐字稿）。旁白沒用的列（#27、#28、#39、#56）這輪不列。
- 列號與 `../history-curiosity/topic-checks/W01.md` 相同；#60–#65 是這輪新增。

## 這輪改了什麼

| 行 | 問題 | 改法 |
|---|---|---|
| t130–t132 | 10-K 同時寫產能主要靠代工廠（#60）；「它自己製造」「它造的」用來反駁「不造硬體」，過強 | 「設計是它的，產線主要交給代工廠」「它賣的」「都對不上：它一直在賣自己的硬體」 |
| t069 | 「第一部是 1976《星夢淚痕》」與杜比自己的年表不符（#29） | 第一部在 1975；第一部帶環繞的才是《星夢淚痕》 |
| t054 | 「多到幾倍？紀錄沒講」：年表有家數（#64） | 那年九月第五家，隔年底三十家 |
| t055–t057 | 專利日期對，但專利全文引更早的申請，英國 1965 年就有申請（#63）；舊句暗示「那封信拖到 1969 才申請」 | 標明「典藏說明寫」，少一個「才」，補「雖然它前面還有更早的申請」 |
| t063、說明欄 | 「庫柏力克讓杜比立體聲一炮而紅」找不到任何文字出處（#58） | 流傳的版本改成查得到的「第一部就是庫柏力克的片」 |
| t119、第 9 章章名 | 「你看出方向了嗎」「手機追上來」：年報列的原因是收購與合約入帳時間（#61） | 講原因；章名改「手機排第二」 |
| t098 | 「手機的錢，跟電視走同一條管子」年報沒這樣寫，且另有直接授權（#43） | 「年報寫的收法，通常分兩段」 |
| t094 | 只講發射端，觀眾會以為電視端完全沒規定（#62） | 補「能收無線訊號的電視也要收得到」 |
| t047、t046、第 4 章章名、說明欄 | 「賣不動」「大家不想碰」「機器很好」都比來源強（#21） | 「一般家庭不買單的格式」「性能很好」「進不了一般家庭」 |
| t003、t007、第 1 章章名、說明欄 | 來源只說途中在阿富汗停留，沒有「路邊」（#5）；t007 是為了維持開場長度刪字 | 「開車回英國途中，在阿富汗」「半路」 |
| t025 | 年表寫 1965 年夏天影音原型同時做（#14） | 標明「典藏說明寫」 |
| `london-money` 字卡 | 「他自己的說法」：原文是記者敘述，不是直接引句（#13） | 「1988 年專訪的說法」 |

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | 2025 財年總營收 | CONFIRMED | 12 Months Ended Sep. 26, 2025：$ 1,349,130（千美元） | 10-K R5、R56 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R5.htm | ✅ |
| 2 | 授權 93%、產品與服務 7% | CONFIRMED（四捨五入） | Licensing $ 1,248,017、93.00%；Products and services $ 101,113、7.00%；實算 92.505% | 10-K R56 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R56.htm | ✅ |
| 3 | 2026 財年還沒公布 | CONFIRMED | 全年財報「Tuesday, November 17, 2026」；旁白全片無「去年」 | 杜比新聞稿（Finviz 轉載） | https://finviz.com/news/401219/dolby-laboratories-announces-conference-call-and-webcast-for-q4-fiscal-2026-financial-results | ✅ |
| 4 | 通常每賣一台付一筆 | CONFIRMED | 「typically enter into a per unit royalty arrangement」；另有最低量與 occasional fixed fee | 10-K 本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 5 | 途中在阿富汗寄給專利律師 | CHANGED | 兩個月陸路開回英國，「a stop in Afghanistan」；沒寫路邊。「信」是合理轉述（write up … and send），來源沒用 letter 這個字 | OAC | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 6 | 印度技術顧問、劍橋物理 | CONFIRMED | 1963 UNESCO technical adviser；1961 PhD in physics | OAC | 同上 | ✅ |
| 7 | 那份美國專利的日期 | CHANGED | 專利首頁 Filed Oct. 20, 1969、Patented Dec. 28, 1971，與 OAC 一致；「它變成」只有 OAC 這樣說，見 #63 | OAC；US3631365A | https://patents.google.com/patent/US3631365A/en | ✅ 日期／△ 關聯 |
| 8 | 1965 年 5 月在倫敦開公司 | CONFIRMED | 「May 1965」；年表同 | OAC；年表；10-K | https://www.film-tech.com/warehouse/manuals/dolbychronology.pdf | ✅ |
| 9 | 16 歲高中生偶遇、進 Ampex | CONFIRMED | 「chance encounter」；IEEE 寫週末與假日工作 | OAC；IEEE | https://spectrum.ieee.org/remembering-ray-dolby | ✅ |
| 10 | 錄影機的電子部分 | CONFIRMED | 1952–57「mainly responsible」「world's first practical」 | OAC | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 11 | 嗜好、既有設備失真更多 | CONFIRMED | 錄當地現場音樂；companders「added more distortion than they reduced noise」 | OAC | 同上 | ✅ |
| 12 | 只處理小聲的部分 | CONFIRMED | 「only audible on quiet passages」 | OAC | 同上 | ✅ |
| 13 | 成衣工廠、2.5 萬美元、四名員工 | CHANGED（字卡） | IEEE 專訪稿的敘述，非直接引句；四名員工年表也有（「staff of four」）；工廠一角與金額只有 IEEE。旁白已標明是 1988 年專訪 | IEEE；年表 | https://spectrum.ieee.org/remembering-ray-dolby | △ |
| 14 | 先做黑白影像降噪，BBC 沒要 | CHANGED（標出處） | OAC「first developed a monochrome video」；年表寫同時做音訊與影像原型 | OAC；年表 | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅／△ 先後 |
| 15 | A 型金屬盒，自己造，賣給英美錄音室 | CONFIRMED | ETHW「manufactured Dolby A units」；年表記 A301 生產與交貨 | ETHW；年表 | https://ethw.org/Dolby_Laboratories | ✅ |
| 16 | 迪卡第一個客戶、九台、三個月獨家 | CONFIRMED | OAC 同；年表 January 1966 訂九台 | OAC；年表 | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 17 | 訊噪比伸展器、被叫成杜比 | CONFIRMED | 「S/N (signal-to-noise) Stretchers」；「much to his surprise」 | IEEE | https://spectrum.ieee.org/remembering-ray-dolby | △ |
| 18 | 品牌也在收費項目裡 | CONFIRMED | 「licensing technology, our brand, and patents」 | 10-K 本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 19 | 1967 年克洛斯催做家用版 | CONFIRMED | OAC「at the urging of」；年表 April 1967 | OAC；年表 | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 20 | 不造家用機，把設計賣給廠商 | CONFIRMED | ETHW「sold the plans」；Electronic Design「manufacture only professional products」；決定時間見 #65。「賣設計」的字眼只有 ETHW | ETHW；Electronic Design；年表 | https://www.electronicdesign.com/technologies/components/article/21795627/ray-dolby-a-breaker-of-sound-barriers | ✅ |
| 21 | KLH 1968 開盤機、獨家到 1970、不普及 | CHANGED | 年表 June 1968 與 ETHW 一致；Stereo Review 記成 1970 年，並說 KLH 40 後來被召回；開盤格式「never enjoyed wide consumer acceptance」。沒有銷售數字，「賣不動」拿掉 | 年表；ETHW；Stereo Review | https://gammaelectronics.xyz/sr_1977-03_tech.html | ✅ 授權／△ 銷售 |
| 22 | 紀錄沒寫他為什麼不自己造 | CONFIRMED（反面，只到讀過的範圍） | OAC、IEEE、ETHW、年表、Electronic Design、Brunswick、公司史都開過：只有做法或事後評語。口述歷史沒找到。旁白說「我讀到的紀錄」，站得住 | 同列 | https://review.brunswickgroup.com/article/dolby-andy-sherman/ | ⚠ |
| 23 | 卡帶被看不起、可比黑膠 | CONFIRMED | ETHW 兩點都有；Stereo Review 記 1968 年業界還沒把卡帶當真。「八軌」「黑膠」只有 ETHW，旁白有標出處 | ETHW；Stereo Review | https://ethw.org/Dolby_Laboratories | ✅／△ 細節 |
| 24 | 1970 年卡帶機、授權大增 | CHANGED | OAC「became popular immediately」；「紀錄沒講幾倍」拿掉，見 #64 | OAC；年表 | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 25 | 1988 年幾乎每家都授權 | CONFIRMED | 「Just about every manufacturer」 | IEEE | https://spectrum.ieee.org/remembering-ray-dolby | ✅ |
| 26 | 《發條橘子》只在混音與母帶 | CONFIRMED | OAC、Guinness、年表三處一致；年表記 December 1971 | OAC；Guinness；年表 | https://www.guinnessworldrecords.com/world-records/first-film-with-dolby-sound | ✅ |
| 29 | 第一部杜比立體聲電影 | CHANGED | 年表 September 1975 Lisztomania；Spring 1976 A Star Is Born 是第一部帶環繞；ETHW 寫 1975；Wikipedia 寫 1976 才掛名 | 年表；ETHW；OAC；Wikipedia | https://www.film-tech.com/warehouse/manuals/dolbychronology.pdf | ✅ 年表／⚠ 來源有出入 |
| 30 | 《星際大戰》讓小戲院裝立體聲 | CONFIRMED | Wikipedia「smaller theaters」；ETHW 同方向；年表 46 家戲院，並把帶動裝機也歸給《第三類接觸》。旁白沒說唯一 | Wikipedia；ETHW；年表 | https://en.wikipedia.org/wiki/Dolby_Stereo | △ |
| 31 | 戲院要加杜比機器與新喇叭 | CONFIRMED | 「a Dolby unit and new loudspeakers」 | ETHW | https://ethw.org/Dolby_Laboratories | △ |
| 32 | 不到十年 6,000 家 | CONFIRMED | 「fewer than ten years, 6,000 cinemas worldwide」 | OAC | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 33 | 1992 數位環繞、5+1、AC-3 | CONFIRMED | OAC；年表 June 1992；Wikipedia「also known as AC-3」 | OAC；年表；Wikipedia | https://en.wikipedia.org/wiki/Dolby_Laboratories | ✅ |
| 34 | FCC 命令日期 | CONFIRMED | Adopted December 24, 1996；Released December 27, 1996 | FCC 96-493 | https://transition.fcc.gov/Bureaus/Mass_Media/Orders/1996/fcc96493.txt | ✅ |
| 35 | DTS 與杜比的爭論 | CONFIRMED | ¶23；標準文件 A/52 是 AC-3（¶22、¶50） | FCC 96-493 | 同上 | ✅ |
| 36 | 不採 DTS 的三個理由 | CONFIRMED | ¶51：沒經過測試、沒有獨立測試、可能拖延、多花成本 | FCC 96-493 | 同上 | ✅ |
| 37 | DTS 可當附加資料 | CONFIRMED | ¶53「as ancillary data」 | FCC 96-493 | 同上 | ✅ |
| 38 | 合理、非歧視是前提 | CONFIRMED | ¶55「premised on reasonable and nondiscriminatory licensing」 | FCC 96-493 | 同上 | ✅ |
| 40 | 寫進標準會限制費率與對象 | CONFIRMED | 「must often limit the royalty rates」「may be unable to limit to whom」 | 10-K 風險因素 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 41 | 電視台發射訊號要符合 A/52 | CONFIRMED | §73.682(d)(1)(i)；ATSC 頁 A/52:2018 | Cornell LII；ATSC | https://www.law.cornell.edu/cfr/text/47/73.682 | ✅ |
| 42 | 只管美國地面數位電視；沒寫手機、全世界、付錢 | CONFIRMED（全文搜過） | royalt 0 處；pay 2 處都無關；mobile、cellular、handset 0 處，telephone 1 處無關；只講這份命令，接收端見 #62 | FCC 96-493；10-K | https://transition.fcc.gov/Bureaus/Mass_Media/Orders/1996/fcc96493.txt | ✅ |
| 43 | 兩段授權 | CHANGED | 「usually occurs in two stages」；R13「only pay us a nominal initial fee」（t100 的「只有」站得住）；「license directly to integrated chip and device makers」；沒寫手機與電視同一路 | 10-K；R13 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R13.htm | ✅ |
| 44 | 約 1,000 家 | CONFIRMED | 「approximately 1,000 consumer electronics manufacturers」 | 10-K 本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 45 | 聯發科晶片支援 | CONFIRMED（只到晶片支援） | 2021-11-19 Pentonic 2000「supports」Dolby Vision、Atmos；TWSE: 2454 | MediaTek | https://www.mediatek.com/press-room/mediatek-announces-new-pentonic-smart-tv-family-with-new-pentonic-2000-for-flagship-8k-120hz-tvs | ✅ |
| 46 | 年報沒有單台金額 | CONFIRMED（全文搜過） | 搜 $／unit、$／device、cents、royalty rates of：0 處金額；只有相對說法與 ARPU | 10-K 全文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 47 | 汽車 > 電視 > 手機；銷量 | CONFIRMED | 「ARPU for cars is higher than ARPU for TVs」；2024 年十億以上、約 2 億、約 9,000 萬（Wards） | 10-K 本文 | 同上 | ✅ |
| 48 | 專利池不掛杜比品牌 | CONFIRMED | 「patent licensing solutions are not Dolby-branded」；AAC、AVC、HEVC。沒有占比，旁白說「一部分」 | 10-K 本文 | 同上 | ✅ |
| 49 | 授權收入依市場 | CONFIRMED | Broadcast 34%（Televisions and STBs）、Mobile 22%（Smartphones and Tablets）、CE 12%、PC 12%、Other 20% | 10-K R56、本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R56.htm | ✅ |
| 50 | 2023 財年對照 | CONFIRMED | 38%、20%；2024 財年 35%、20% | 10-K R56 | 同上 | ✅ |
| 51 | 廣播標準重要性下降 | CONFIRMED | 「gradually diminishing over the recent years」 | 10-K 風險因素 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 52 | 手機要一直說服、較易拿掉 | CONFIRMED | 「usually are not mandated」「must continually convince」「easier … to add or remove」 | 10-K 風險因素 | 同上 | ✅ |
| 53 | 先讓內容用它 | CONFIRMED | 風險因素直接寫目的是提高 OEM 需求；「worked with online and mobile media content service providers」 | 10-K | 同上 | ✅ |
| 54 | Apple Music 2021 | CONFIRMED | Apple：June 2021。**年報有點名**（MD&A Mobile Highlights：Dolby Atmos「is included in Apple Music」），撰稿者「年報沒點名」是錯的。年報沒說這是說服手段；旁白用「比如」、沒說年報這樣講，站得住 | Apple；10-K MD&A | https://www.apple.com/newsroom/2021/05/apple-music-announces-spatial-audio-and-lossless-audio/ | ✅ |
| 55 | 7% 主要是戲院硬體與服務 | CHANGED | 「primarily for the cinema」；servers、processors、amplifiers、loudspeakers；生產見 #60 | 10-K 本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 57 | 流傳：不造硬體只賣專利 | LEGEND | 有文字出處：GoodWhale「doesn't manufacture a single chip, speaker, or TV」；Brunswick「Rather than building gadgets」。「你可能聽過」站得住；與 #15、#31、#55 不符 | GoodWhale；Brunswick | https://goodwhale.com/is-dolby-labs-an-overlooked-tech-stock | ⚠ |
| 58 | 流傳：第一部就是庫柏力克的片 | CHANGED（仍標流傳） | 「讓杜比立體聲一炮而紅」查無文字。Screen Rant「the first film to employ Dolby Sound」、Guinness 同名紀錄查得到，旁白改講這個 | Screen Rant；Guinness | https://screenrant.com/clockwork-orange-stanley-kubrick-trivia-facts/ | ⚠ |
| 59 | Ray Dolby 卒年（畫面規則） | CONFIRMED | 1933–2013，未滿 70 年，不畫本人 | OAC | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ | ✅ |
| 60 | 硬體主要由代工廠生產 | CONFIRMED（新增） | 「rely primarily upon contract manufacturers for the majority of our production capacity」 | 10-K 本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm | ✅ |
| 61 | 手機占比上升的原因 | CONFIRMED（新增） | MD&A：GE Licensing 收購帶來影像專利收入、音訊專利最低量合約的入帳時間 | 10-K MD&A | 同上 | ✅ |
| 62 | 接收端也有規定 | CONFIRMED（新增） | §15.117(b)：receivers「shall be capable of adequately receiving」§73.682(d) 標準的頻道 | Cornell LII | https://www.law.cornell.edu/cfr/text/47/15.117 | ✅ |
| 63 | 那份專利前面還有更早的申請 | CONFIRMED（新增） | US3631365 全文引 copending Ser. No. 569,615 等，自稱進一步改良；GB1120541（R. M. Dolby）11 Aug. 1965 起申請、1968-07-17 公開 | Google Patents | https://patents.google.com/patent/GB1120541A/en | ✅ |
| 64 | 授權家數 | CONFIRMED（新增，公司自述） | September 1970「Fifth company」；1971「30 licensees by end of year」 | 年表 | https://www.film-tech.com/warehouse/manuals/dolbychronology.pdf | ✅ |
| 65 | 1967 年談的就是授權 | CONFIRMED（新增，公司自述） | April 1967「Negotiations begun on licensing」，對象 Henry Kloss of KLH | 年表 | 同上 | ✅ |

## 其他判定

- **標題**「憑什麼 93% 的錢都是授權費」：沒過頭。年報列 93.00%，「的錢」指營收，片中 t107、t108 講清楚不是每台抽成。
- **縮圖**「杜比／93% 授權／不造電視也不造手機」：不算錯，但「93% 授權」沒有分母，正是片中 t107 叫人別聽錯的說法。試過「93% 營收靠授權」（超過 6 字）、「93% 靠授權」（手機上字太小），lint 都擋，所以維持原字，由站主決定要不要換版面。
- **「不造電視也不造手機」**：年報的收入來源、生產段落與「We do not manufacture these ICs」都相符；沒有一句逐字寫不造電視與手機，屬於合理歸納。
- **t135「不是憑一條法律」**：標成作者解讀的結論前一句。美國地面電視有 §73.682 與 §15.117，但手機與全球市場不靠這些（10-K 兩處），所以「不是憑一條」站得住。
- **t058、t059「不只是那張專利」「設計圖，加上那個名字」**：標成「我覺得」。品牌收費是 2025 年的年報寫的，1970 年的授權合約有沒有包含名字，這輪沒有原件。
- **提示詞**：腳本掃過全部 `scenes[].data.prompt`，沒有公司、產品、片名或人名；真實人物都是不指認的一般人物。
- **風險**：沒有暗示違法；DTS 與杜比的立場都出自 FCC 命令 ¶23。
- **上架日期**：2026-11-17 之後若才上架，要站主決定是否改用 2026 財年數字（`brief.md` 已寫）。

## 仍只有單一或公司自述來源

成衣工廠一角與 2.5 萬美元（IEEE）；「訊噪比伸展器」與連他自己都意外（IEEE）；卡帶比八軌差、可比黑膠（ETHW）；小戲院第一次裝立體聲（Wikipedia）；戲院加機器與喇叭（ETHW）；授權家數與 1967 年談授權（杜比自編年表）。
