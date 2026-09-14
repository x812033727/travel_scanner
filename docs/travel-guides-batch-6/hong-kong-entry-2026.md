# 13. `hong-kong-entry-2026`

2026 台灣旅客入境香港：網上預辦入境登記免費、2 個月內入境 2 次各停留 30 天，電子菸與加熱菸不能帶、公眾地方持有也罰，菸酒免稅額與 12 萬港元現金申報

| 欄位 | 值 |
| --- | --- |
| kind | `intel` |
| destination_id | `hong-kong` |
| topics | `entry` |
| valid_until | `2027-03-31` |
| featured | `true` |
| display_order | `930` |

規格 2026-09-14 定稿：兩輪查核加三輪一致性審查，已對照 main 上 #468 與第五批的文章。官方來源的數字是規劃時讀到的，
撰稿當天要再打開一次核對，`checked_on` 填實際打開那天。通用規則見 [README](README.md)。

## 切角與段落

情報文 800–1,500 字，目標 1,300–1,450 字；超過時先刪澳門 callout 的第二句，再縮短入境許可那段。用字：正文一律寫「電子菸」「加熱菸」「菸酒」，跟站上的越南入境文（vietnam-entry-2026-evisa）一致；香港的法定名稱「另類吸煙產品」和公報用字「煙彈」「煙油」「加熱煙枝」照原文寫，第一次出現加引號。港鐵中文一律寫「機場快綫」，跟香港另外兩篇一致。

區塊順序如下。

0. 開頭 paragraph（約 120 字）：直接給結論。台灣護照去香港不用簽證，但出發前要在 GovHK 免費辦「台灣居民網上預辦入境登記」，或持台胞證入境。電子菸、加熱菸不能帶進香港（2022 年 4 月 30 日起禁止輸入），2026 年 4 月 30 日起連在公眾地方持有也會被罰。帶超過 12 萬港元的現金，在機場要走紅色通道申報。最後寫明 2026 年 9 月依香港入境事務處、香港海關、衛生署控煙酒辦事處與外交部領事事務局的頁面查證。

1. 緊接一張 table「文件與規定檢查表」，欄位是項目、要準備什麼、2026 年 9 月查證的規定，caption 寫「2026 年 9 月查證」。8 列，每格精簡：預辦入境登記；台胞證；入境許可；回台證件效期（6 個月以上）；入境標籤；菸酒免稅額；電子菸與加熱菸；現金與不記名票據（超過 12 萬港元，香港國際機場走紅色通道申報）。

2. H2「出發前：三種入境方式怎麼選」
(a) 網上預辦入境登記：免費，結果即時出來；有效 2 個月，可入境 2 次，每次以訪客身分最多停留 30 天。資格照入境處原文寫全：在台灣出生，或在台灣以外出生但曾以台灣居民身分入境香港；而且除台胞證與入境處簽發的入境許可外，不持有其他地方簽發的旅行證件。直接點出「持有外國護照的雙重國籍者不符資格」。登記時與抵港時，回台證件都要有 6 個月以上效期。
(b) 持有效台胞證：可以訪客身分停留最多 30 天，轉機往返內地或單純來港都一樣。
(c) 不符資格的人（例如在台灣以外出生、又沒有以台灣居民身分入境過香港）要申請入境許可：可網上或用紙本表格申請，海外申請約四個星期；經在台灣的指定航空公司申請多次入境許可約 2 個工作天。費用寫「以入境處收費表 ID 912 為準」。
接著一個 ordered list，只寫官方頁有的四步：確認資格與回台證件效期 6 個月以上；在 GovHK 網上登記，免費、即時出結果；通知書用 A4 白紙列印並簽名；抵港時連同回台證件出示。
再放一個 warning callout，口徑比照越南入境文：搜尋結果常先出現代辦網站；登記免費，只在 gov.hk 網域辦，網址不是 gov.hk 結尾的都不是香港政府網站。
段末一句「出發當天在桃園機場報到、安檢怎麼走」，後接 link 到 guides/howto/taoyuan-airport-departure-guide。
最後放 diagram-1.svg。

3. H2「抵達香港：入境審查與入境標籤」（約 150 字）
．台灣旅客走人工櫃檯。入境處訪客 e-道頁沒有列台灣居民或台胞證持有人，只能寫「以入境處公告為準」，不能寫可以用 e-道。
．入境處不在護照上蓋章，改發入境標籤，上面有英文姓名、旅行證件號碼、抵達日期、逗留條件與准許停留期限。拿到先看清楚准許停留到哪一天；在港期間要保留入境標籤，遺失可親身到入境處延期逗留組免費補發。
．photo-1 放這一節後（機場入境大堂或海關通道的 Commons 照片）。

4. H2「海關：菸酒免稅額、電子菸與現金」
．用 list 列免稅額，只給 18 歲以上：酒精濃度 30% 以上（20°C 量度）的酒 1 公升；菸草四擇一：香菸 19 支，或雪茄 1 支或 25 克，或其他菸草製品 25 克。
．紅綠通道怎麼選，只寫海關免稅額頁原文有寫的；原文沒寫，就寫「超過免稅額或帶了應課稅品，向海關申報，以香港海關為準」。
．H3「電子菸與加熱菸：兩條禁令、兩個日期」
  ．輸入禁令：2022 年 4 月 30 日起。簡易程序定罪最高罰 50 萬港元並監禁 2 年，循公訴程序最高罰 200 萬港元並監禁 7 年，兩個一起寫。只有在香港國際機場轉機、不經入境檢查的旅客豁免。
  ．公眾地方持有禁令：2026 年 4 月 30 日起。少量（煙彈不超過 5 個、煙油不超過 5 毫升、加熱煙枝或草本煙不超過 100 支）定額罰款 3,000 港元；超過這些數量或作商業用途，最高罰 5 萬港元並監禁 6 個月。
  ．接一句 news.gov.hk 的說明：對旅客來說，入境本來就不能帶，新禁令是把規管延伸到公眾地方持有。
  ．warning callout：加熱菸不算在 19 支香菸的免稅額裡；航空規定電子菸機器只能放手提行李，那是飛航安全規定，放手提不代表可以帶進香港。
．H3「現金與不記名票據：超過 12 萬港元」：香港國際機場在《條例》附表 1 的指明管制站清單上。搭機抵港時，現金與不記名可轉讓票據合計超過 12 萬港元，要走紅色通道向海關申報，也可以填紙本申報表。首次違反可繳 2,000 港元了結，其他個案循刑事程序處理，最高罰 50 萬港元並監禁 2 年。在機場轉機、不經入境檢查的旅客不適用。
．info callout「順道去澳門」，只寫兩件事：外交部領事事務局 2026 年 7 月 23 日更新的名單列澳門免簽 30 天，名單註明以陸委會與當地規定為準；入境澳門帶總值 12 萬澳門元以上的現金或無記名票據要申報，違反可罰 1,000 至 50 萬澳門元（澳門旅遊局）。其他不寫。

5. H2「出關之後：機場交通與回台灣」（約 100–150 字）
．paragraph 1–2 句：出關後可搭機場快綫、機場巴士或計程車進市區。不寫票價、時間與班距，細節交給專文。
．link 到 guides/howto/hong-kong-airport-to-city。
．offer（transport）。
．paragraph 1 句：回台灣入境另有免稅額，肉製品、現金也有規定，不在本文展開。
．link 到 guides/howto/return-to-taiwan-customs-duty-free-guide。
．link 到 guides/howto/hong-kong-4-day-itinerary。
．同系列入境情報：link 到 guides/intel/singapore-entry-2026-sg-arrival-card、guides/intel/vietnam-entry-2026-evisa。
．結尾：destinations/hong-kong、foods?city=hong-kong。

## 官方來源

一律用 WebFetch 讀原頁；checked_on 填撰稿實際查核日。★ 表示 2026-09-14 修訂時重新讀過。

1. 香港入境事務處：台灣居民網上預辦入境登記 https://www.immd.gov.hk/eng/services/visas/pre-arrival_registration_for_taiwan_residents.html（中文版把 /eng/ 換成 /hkt/）。查免費、即時結果、有效 2 個月、入境 2 次、每次 30 天、資格全文、6 個月效期、A4 列印並簽名。頁面修訂日 2022-11-29。
2. ★香港入境事務處：Entry Arrangements for Mainland, Macao, Taiwan & Overseas Chinese Residents https://www.immd.gov.hk/eng/services/visas/overseas-chinese-entry-arrangement.html（修訂日 2026-06-02）。查台胞證 30 天。不符資格者可網上或用紙本表格 ID 78D（單次）、ID78H（多次）申請入境許可，海外申請約四個星期，經台灣指定航空公司申請多次入境許可 2 個工作天。費用這頁只連到 ID 912。
3. ★香港入境事務處：收費表 ID 912 https://www.immd.gov.hk/pdforms/id912.pdf（2025 年 9 月 8 日起生效，版次 ID 912 (4/2026)）。表上有「限用一次的入境證」「有效期 1 年／3 年的多次入境證」等多個收費項目，但沒寫台灣居民適用哪一項，所以正文不寫金額，只寫以此表為準。
4. ★香港入境事務處：Non-stamping Immigration Clearance Arrangement https://www.immd.gov.hk/eng/useful_information/non-stamping-immigration-clearance.html（修訂日 2026-08-19）。查入境標籤上的資料（英文姓名、旅行證件號碼、抵達日期、逗留條件與期限）、在港期間要保留、遺失到延期逗留組免費補發。
5. 香港入境事務處：e-Channel Services for Visitors https://www.immd.gov.hk/eng/services/echannel_visitors.html（修訂日 2026-09-02），用來確認沒有列台灣居民。
6. 香港海關：Duty-free Concessions https://www.customs.gov.hk/en/service-enforcement-information/passenger-clearance/duty-free-concessions/index.html。查 18 歲以上；酒 1 公升，酒精濃度 30% 以上、20°C 量度；香菸 19 支、雪茄 1 支或 25 克、其他菸草 25 克，四擇一。紅綠通道寫法也以此頁為準。
7. 香港海關：Alternative Smoking Products https://www.customs.gov.hk/en/service-enforcement-information/trade-facilitation/ASP/index.html。查輸入禁止、機場轉機不經入境檢查的豁免。本頁沒有罰則與日期。
8. 衛生署控煙酒辦事處：Ban on Alternative Smoking Products https://www.taco.gov.hk/t/english/legislation/legislation_asp.html。查產品定義、輸入罰則兩級、公眾地方持有罰則。
9. 香港政府新聞公報 2026-04-29 https://www.info.gov.hk/gia/general/202604/29/P2026042900589.htm。查 4 月 30 日生效，以及煙彈 5 個、煙油 5 毫升、加熱煙枝或草本煙 100 支的少量上限。
10. news.gov.hk 2026-04-30 https://www.news.gov.hk/eng/2026/04/20260430/20260430_181730_790.html。查 2022 年 4 月 30 日起旅客不得帶入、新禁令沒有增加旅客限制。
11. ★香港海關：現金類物品（中文）https://www.customs.gov.hk/tc/service-enforcement-information/passenger-clearance/currency-bearer-negotiable-instruments/index.html（英文版把 /tc/ 換成 /en/）。查指明管制站走紅通道申報、可填紙本申報表、首次違規 2,000 港元、最高罰 50 萬港元並監禁 2 年、機場過境豁免。
12. ★香港海關：指明管制站清單 https://www.customs.gov.hk/tc/service-enforcement-information/passenger-clearance/currency-bearer-negotiable-instruments/specified-control-points/index.html。15 個管制站中第 7 項是「香港國際機場」，所以搭機抵港屬申報制，不是被問才披露。
13. 澳門旅遊局：入境須知 https://www.macaotourism.gov.mo/zh-hant/travelessential/before-you-travel/entry-requirements。只查 12 萬澳門元申報與 1,000 至 50 萬澳門元罰款。
14. 外交部領事事務局：國人可以免簽證、落地簽證及電子簽證前往之國家與地區（2026.7.23）https://www.boca.gov.tw/dl-4250-bc7da479a4d2418ab92b51a6dae38019.html。只查澳門免簽 30 天。

不引用：澳門治安警察局 gov.mo ps-1474b（沒有台灣護照停留天數）；海關舊網址 .../currency-declaration/（404）；elegislation.gov.hk 第 629 章（WebFetch 只讀到載入畫面，改用上面第 12 項的清單頁）。

## 合作區塊（offer）

只放一個，位置在最後一個 H2「出關之後：機場交通與回台灣」裡：機場交通 paragraph 與 hong-kong-airport-to-city 連結之後、回台灣那句 paragraph 之前。區塊寫 {"type":"offer","module":"transport","destination_id":null,"heading":"香港機場到市區的交通票券與接送，先比價"}。文章 destination_id 已改成 hong-kong，所以 offer 的 destination_id 留 null，沿用文章值，跟 singapore-entry-2026-sg-arrival-card 同一種寫法。heading 不點名機場快綫車票或任何特定商品。香港的 transport 優惠目前還沒核准，上線時不會顯示，照放即可。entry 主題其餘段落不放 activities、hotel、connectivity。

## 站內連結

網址前綴一律是 https://mokaair.com/zh-TW/，每個連結是一個 link 區塊。

1. guides/howto/taoyuan-airport-departure-guide：放在第一個 H2「出發前：三種入境方式怎麼選」段末、diagram-1 之前，前一句寫「出發當天在桃園機場報到、安檢怎麼走」。第六批，長青。
2. guides/howto/hong-kong-airport-to-city：放在最後一個 H2 的機場交通 paragraph 之後、offer 之前。第六批，長青。
3. guides/howto/return-to-taiwan-customs-duty-free-guide：放在最後一個 H2「回台灣入境另有免稅額」那句之後。第六批，長青，取代原本的 korea-olive-young-tax-refund-shopping。
4. guides/howto/hong-kong-4-day-itinerary：接在第 3 項之後。第六批，長青；那篇行程會再連 hong-kong-ferry-tram-day 與 cheung-chau-walking-day。
5. guides/intel/singapore-entry-2026-sg-arrival-card：放在結尾同系列入境情報。第六批，valid_until 2027-03-31，跟本篇同日。
6. guides/intel/vietnam-entry-2026-evisa：接在第 5 項之後。第五批，main 上有 zh-TW，valid_until 2027-03-31。
7. destinations/hong-kong：結尾城市頁。
8. foods?city=hong-kong：結尾美食目錄，放在第 7 項之後。

刻意不連：
．japan-entry-2026-visit-japan-web、korea-entry-2026-k-eta-e-arrival、thailand-entry-2026-tdac：都 2026-12-31 到期，本篇有效到 2027-03-31。
．power-bank-flight-rules-2026：2027-01-31 到期，一樣會在本篇閱讀期內過期。電子菸只能放手提這件事，只在 callout 裡一句帶過。
．korea-olive-young-tax-refund-shopping：已由同批的回台專文取代。
．hong-kong-ferry-tram-day、cheung-chau-walking-day（#468）：跟本篇沒有重疊段落，由 hong-kong-4-day-itinerary 轉連，入境情報不再加連結。
．macau-day-trip-from-hong-kong：main 上沒有，也不在第六批。
．澳門城市頁：目的地目錄沒有 macau，不寫。

## 圖解

diagram-1.svg，1600×900，決策樹加流程圖，放在第一個 H2 段末（桃園機場連結之後）。字型用 'Noto Sans TC','Noto Sans JP','PingFang TC','Microsoft JhengHei','Hiragino Sans',system-ui,sans-serif，字級最小 15。

左半邊：起點「你用什麼入境？」分三條。
(a)「台灣出生（或曾以台灣居民身分入境香港）、沒有外國護照、回台證件效期 6 個月以上」→「網上預辦入境登記 Pre-arrival Registration：免費、有效 2 個月、入境 2 次、每次 30 天、A4 列印簽名」。
(b)「持有效台胞證」→「停留 30 天」。
(c)「不符資格」→「申請入境許可 Entry Permit：經台灣指定航空公司辦多次入境許可約 2 個工作天」。

右半邊：三條線匯到四步流程。
1.「入境審查 Immigration：人工櫃檯、領入境標籤 Landing Slip」。
2.「領行李 Baggage」。
3.「海關 Customs 紅綠通道 Red／Green Channel：18 歲以上 酒 1 公升（30% 以上）、香菸 19 支」。
4.「入境大堂 Arrival Hall」。

海關格旁邊放一個 coral #B8442D 警示框，三行：
．電子菸、加熱菸 2022 年 4 月 30 日起禁止輸入。
．2026 年 4 月 30 日起公眾地方持有，少量定額罰款 3,000 港元。
．現金與不記名票據超過 12 萬港元，紅色通道申報。

不畫 e-道，不畫機場交通，不畫澳門。圖上的數字只有 6、2、30、1、19、18、30%、2022 年 4 月 30 日、2026 年 4 月 30 日、3,000、12 萬，每一個都要在正文出現。右下角寫「© Mokaair 製圖 2026」。

## 撰稿時要小心

一、e-道：入境處訪客 e-道頁（修訂日 2026-09-02）沒有列台灣居民與台胞證持有人；Smart Departure 只限指定國家或地區的電子護照。只能寫走人工櫃檯、以入境處公告為準。

二、另類吸煙產品是兩條法規、兩個日期，不能混寫。
．輸入禁令 2022 年 4 月 30 日起：簡易程序 50 萬港元並監禁 2 年、公訴程序 200 萬港元並監禁 7 年，兩個一起寫。
．公眾地方持有禁令 2026 年 4 月 30 日起：少量定額罰款 3,000 港元，數量上限照公報寫；超量或作商業用途最高 5 萬港元並監禁 6 個月。
．海關的 ASP 頁沒有罰則與日期，罰則的 sources 要列控煙酒辦頁與公報。

三、轉機豁免只適用於在香港國際機場轉機、沒有經過入境檢查的人。過境途中出了機場就不算。電子菸和現金兩條都照這個口徑寫。

四、跟 power-bank-flight-rules-2026、taoyuan-airport-departure-guide 的口徑要一致：那兩篇寫電子菸機器是鋰電池、只能放手提行李。本篇不能讓讀者誤會「放手提就能帶進香港」，要寫明那是飛航安全規定，入境香港仍屬輸入禁令範圍。不要寫 Wh 或行動電源的規定。

五、預辦登記頁的修訂日是 2022-11-29。「A4 白紙列印並簽名」是原文；手機截圖能不能用，頁面沒寫，不要自己補。ordered list 只寫官方頁有的四步，不自己編表單欄位或畫面名稱。

六、入境許可費用：ID 912 收費表有單次入境證、1 年與 3 年多次入境證等多個金額，但沒寫台灣居民適用哪一項。正文一律不寫金額，只寫以入境處收費表為準。處理時間只寫「海外申請約四個星期；經台灣指定航空公司申請多次入境許可約 2 個工作天」。

七、預辦登記資格照原文寫全。持有外國護照的雙重國籍者不符資格，這點要點出來。台胞證 30 天只陳述入境處原文，不評論辦台胞證的政治或法律風險。

八、現金申報已確認：海關指明管制站清單第 7 項是香港國際機場。搭機抵港超過 12 萬港元要走紅色通道申報，或填紙本申報表。不要寫成「關員詢問時才披露」，那是客輪經碇泊處抵港等非指明管制站的做法，本篇不用寫。罰則寫首次違規 2,000 港元了結、最高 50 萬港元並監禁 2 年。

九、菸草免稅額是四擇一，不是 19 支香菸再加雪茄；18 歲以上才有。香港身分證持有人的 24 小時限制、跨境司機的規定都跟台灣旅客無關，不寫。酒類只寫「酒精濃度 30% 以上 1 公升免稅」，30% 以下課不課稅沒查，不寫。加熱菸不算在香菸免稅額裡。

十、入境標籤只寫入境處頁有的：上面的資料項目、在港期間要保留、遺失到延期逗留組免費補發。不要寫「出境時要交回」「背面有什麼」這類沒查到的細節。

十一、澳門只寫兩件事，都要標來源：外交部領事事務局名單列澳門免簽 30 天（名單本身註明以陸委會與當地規定為準），以及 12 萬澳門元現金申報。澳門治安警察局頁沒有台灣護照的停留天數，不能引用成「澳門官方說 30 天」。旅遊局頁的落地簽 200／300 澳門元是一般規定，絕對不能寫成台灣旅客要付。澳門的菸酒免稅額與電子菸規定沒讀到原文，不寫。

十二、香港本身不在領事局免簽名單上（歸陸委會管），不要寫「外交部列香港免簽」。

十三、回台灣的規定（免稅額、肉品、電子菸、現金）一律不寫，只用一句話連 return-to-taiwan-customs-duty-free-guide。那篇對電子菸的寫法還要看查核結果，本篇不能先下結論。

十四、跟 hong-kong-airport-to-city 不重疊：本篇不寫機場快綫、巴士、計程車的票價、時間、班距，也不寫 T2 離境大堂或市區預辦登機。

十五、用字：正文寫電子菸、加熱菸、菸酒，港鐵寫「機場快綫」；香港官方名詞（另類吸煙產品、煙彈、煙油、加熱煙枝）照原文。港幣寫「3,000 港元」「12 萬港元」，澳門幣寫「12 萬澳門元」，不換算台幣。

十六、destination_id 已改成 hong-kong，offer 的 destination_id 要留 null。這篇不要再填 null，也不要在 offer 重填 hong-kong。

十七、這是 intel，valid_until 是 2027-03-31。所有站內連結都要是長青文，或到期日不早於 2027-03-31 的 intel。不要加連 2026-12-31、2027-01-31 到期的文章。

## 上線後與交叉檢查

- 統整第六批時，確認 singapore-entry-2026-sg-arrival-card 的 destination_id 仍是 singapore、offer 的 destination_id 是 null；若那篇改回 null，本篇也要跟著改，兩篇必須一致。
- 建議 singapore-entry-2026-sg-arrival-card 的正文也把「電子煙」統一成「電子菸」（新加坡法定名詞可另註英文），港星越三篇入境文用字一致。
- 上線 PR 裡，已在 main 的 vietnam-entry-2026-evisa 文末只連了 thailand-entry-2026-tdac（2026-12-31 到期）。建議另開票在那篇加上 intel/hong-kong-entry-2026 與 intel/singapore-entry-2026-sg-arrival-card 的反向連結，並把泰國入境連結留到泰國出 2027 版時再換。
- 上線後檢查同批反向連結都有寫進去：hong-kong-4-day-itinerary 開頭段、hong-kong-airport-to-city 開頭段後、taoyuan-airport-departure-guide 的「怎麼入境」、singapore-entry-2026-sg-arrival-card 的同系列入境文，都要連回本篇。
- 2027 年 1 月中複查：入境處預辦登記頁（修訂日是否從 2022-11-29 變動）、訪客 e-道頁有沒有加入台灣居民、控煙酒辦的另類吸煙產品規定、外交部領事事務局簽證便利名單的澳門天數。有變動就先改文，並更新 sources 的 checked_on。
- 2027 年 3 月上旬決定出 2027 年版還是延長 valid_until。到期前若日本、韓國、泰國入境文已出 2027 年版且到期日較晚，可以補回同系列連結。
- power-bank-flight-rules-2026 若續出 2027 年版且到期日不早於本篇，可在電子菸 callout 那句補連；在那之前不要連。
- 第七批若寫了澳門一日遊（例如 macau-day-trip-from-hong-kong），在本篇「順道去澳門」callout 後補連；目的地目錄若新增 macau，再加澳門城市頁。
- 搭機抵港的現金申報屬指明管制站（紅色通道），這個結論也要告訴寫 hong-kong-airport-to-city 與 hong-kong-4-day-itinerary 的撰稿者：那兩篇如果提到現金，只用一句話連本篇，不要另寫一套說法。
