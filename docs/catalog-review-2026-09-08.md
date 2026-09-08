# 2026-09-08 全旅遊目錄審核紀錄

狀態：本輪全部評估、決策套用與最終更正完成（2026-09-08 08:28 UTC）。使用者授權範圍為所有未審景點、店家與風格，允許使用既有 Gemini 額度與瀏覽器。評估完成不代表全部達到發布條件；資料不足的項目仍保留待審。

## 最終結果

| 起始待審類別 | 本輪筆數 | 核准 | 拒絕／退回 | 保留待確認 |
| --- | ---: | ---: | ---: | ---: |
| 景點 | 2,215 | 0 | 435 | 1,780 |
| 店家 | 167 | 4 | 0 | 163 |
| 風格提案 | 44 | 43 | 0 | 1 |
| 合計 | 2,426 | 47 | 435 | 1,944 |

2,382 個目錄實體全部有評估與明確決策，漏評 0、未套用 0；44 個風格另外逐項處理。保留項目主要缺精準地圖、獨立定位或直接來源，另有行政區、改名／分店、建物及分類待釐清。待審不是核准，也不是斷言該場所不存在。

四個 Gemini 工作共使用 318 次既有平台呼叫，沒有調高／重設上限，也未扣會員次數。708 個模型拒絕建議均逐筆讀取引文及來源後複核，其中 273 個改為保留待確認；原模型歷史不改寫。

## 範圍與保護

- 起始待審：景點 2,215、店家 167、風格 44；美食條目無待審。
- 正式資料庫已在任何審核寫入前以 pg_dump 備份並驗證索引；備份位於伺服器私有目錄，不放入 Git。
- Gemini 使用既有 gemini-3.8-flash，每工作最多 80 次、既有每日上限 1,000 次；不調高、不重設額度、不扣會員次數。
- 根工作：`5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a`，由實際登入的管理員在 UI 建立。所有寫入重新檢查有效管理權限，使用既有樂觀版本／冪等／稽核服務。
- 本輪只處理起始 2,382 個目錄快照，不新增候選。後續工作只接續尚未評估項目，保留舊工作與計費記錄。
- 模型建議不是發布許可。不填造地圖 ID、座標、驗證日期；韓國精準地圖仍須 Naver，其餘仍須 Google Place ID。
- 缺少資料、來源讀取失敗、區域型記錄、別名／改建後身分不清楚，保留待審；一般學校、醫療／行政機構、住宅、可移動館藏、歷史事件等與獨立現行景點不符的資料，須有可核對來源才拒絕。
- 風格核准不等於店家核准，不連帶修改店家發布狀態。後續店家需獨立完成來源與發布條件核對。沒有實體刪除資料。

## 已完成的風格複核

44 個風格提案已使用公開來源與必要的瀏覽器回退逐項複核：43 核准，1 保留待審。44 筆均已寫入既有 `food_merchant_style_reviewed` 稽核，保留操作者與理由。

ACME 北美館店的泛用品牌定位與所在美術館，不足以證明店內具體文化活動，保留待審。Walden 與喫茶ソワレ的證據連結已改指向實際介紹頁。既有公開店家的 FAbULOUS 與 Walden Woods Kyoto 風格可顯示；其餘核准風格不改變店家待審狀態。

補查 [CAFE ACME 品牌故事](https://www.cafeacme.com/pages/about-us) 提到的展演空間是 MAISON ACME 圓山別邸，不能直接套用到北美館咖啡店；維持此店文青標籤待審。

| 店家 | 風格 | 結果 | 本次來源與理由 |
| --- | --- | --- | --- |
| Aoyama Flower Market GREEN HOUSE | 網美 | 核准 | [來源](https://foreign.aoyamaflowermarket.com/foreign/teahouse/pc/)：已核對南青山官方地址與花卉溫室、花藝陳列介紹，支持網美風格；不代表人氣排名或攝影許可。 |
| BUNDAN COFFEE & BEER | 文青 | 核准 | [來源](https://bundan.net/about/)：瀏覽器核對官網，館內提供文學藏書閱覽並供應咖啡，支持文青風格；不把未排定活動當成現行展演。 |
| BUNKITSU TENJIN | 文青 | 核准 | [來源](https://tenjin.bunkitsu.jp/about/)：官網明列策選書籍、閱覽室與喫茶室，支持文青風格；閱讀及喫茶屬付費區域。 |
| Brown Hands Baekje | 網美 | 核准 | [來源](https://www.visitbusan.net/index.do?lang_cd=ko&menuCd=DOM_000000201001001000&uc_seq=231)：釜山市官方指定店家頁描述舊醫院建築改造與保留年代感的室內設計，支持網美風格；不挪用其他樓層藝廊。 |
| CAFE ACME Taipei Fine Arts Museum | 文青 | 待審 | [來源](https://acmetaipei.com/zh/pages/cafe-acme-taipei-fine-arts-museum_)：官網確認此店與藝術生活的品牌定位，但未列具體店內藝術展示、閱讀、策展或文化活動；不能只因鄰近美術館核准文青風格，待補直接證據。 |
| CBC SPACE Jingmei Cafe Library | 文青 | 核准 | [來源](https://cbcspace.com/zh-tw/jmcoffee)：官網確認景美分館結合咖啡與二樓 boven 雜誌閱讀，涵蓋設計和生活內容，支持文青风格；舊優惠不視為現行價格。 |
| Cafe Bibliotic Hello! | 文青 | 核准 | [來源](https://www.kyotokan.jp/read/my-local-guide-kyoto-16-03/)：京都市京都館的指定店家介紹載明整面書牆與音樂餐飲空間，支持文青風格；不推論借閱權限。 |
| FAbULOUS | 文青 | 核准 | [來源](https://www.rounduptrading.com/)：官網核實札幌同址咖啡與家具服飾選物，並列出延續至2026年9月的藝術展示，支持文青風格；已結束快閃不描述成當期活動。 |
| FUKUROSHOSABO | 文青 | 核准 | [來源](https://www.doutor.co.jp/fukuro/)：官網介紹以推薦文字及編號引導選書並結合咖啡的書茶房，支持文青風格；不延用往年限定套餐。 |
| Jypsy One Fullerton | 網美 | 核准 | [來源](https://www.pscafe.com/jypsy-one-fullerton)：官方指定分店頁明述波希米亞海岸風格的餐飲空間，支持網美風格；與同棟 PS.Cafe 分店分開。 |
| Knots Cafe and Living Paya Lebar | 網美 | 核准 | [來源](https://www.knotscafeandliving.com/)：官網描述花藝、手作家具與餐飲的空間組合並列出 Paya Lebar 分店，支持網美風格；不推論寵物接待或拍照權限。 |
| MORI NO TOSHO SHITSU | 文青 | 核准 | [來源](https://morinotosyoshitsu.com/)：官網明列可邊飲食邊閱讀的書籍空間與書中食物主題菜單，支持文青風格；不宣稱免費使用。 |
| Merci Marcel Orchard | 網美 | 核准 | [來源](https://mercimarcelgroup.com/merci-marcel/orchard-singapore/)：瀏覽器核對 Orchard 官方分店頁，明列 Bauhaus 靈感、熱帶元素及復古現代家具搭配，支持網美風格。 |
| NOC Cityplaza | 網美 | 核准 | [來源](https://noc.coffee/rediscover-urban-serenity-introducing-noc-cityplaza/)：品牌指定分店文章列明石材立面、木材與混凝土、再利用樹幹融入桌面，支持網美風格；不借用其他分店特色。 |
| New Poppy | 網美 | 核准 | [來源](https://b-bitou.com/shop/)：瀏覽器核對品牌頁的蔵造空間、中央挑空及塔狀閣樓座席，支持網美風格；官方明示新建，不稱古蹟。 |
| ONIBUS COFFEE 中目黒駅前店 | 網美 | 核准 | [來源](https://onibuscoffee.com/en/blogs/news/114)：瀏覽器核對中目黒店介紹，明列大谷石外牆、常滑燒磁磚及手繪牆窗，支持網美風格；不採用同文奥沢店特色。 |
| Onion Anguk | 網美 | 核准 | [來源](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=191156)：韓國觀光公社的安國分店介紹確認韓屋改造及保留大廳與庭院，支持網美風格；地圖另待 Naver 核實。 |
| PS.Cafe One Fullerton | 網美 | 核准 | [來源](https://www.pscafe.com/pscafe-one-fullerton)：官方二樓分店頁確認航海主題、明亮開闊空間及濱海視野，支持網美風格；不保證每個座位的視野。 |
| Patom Organic Café Bangkok Flagship Store | 網美 | 核准 | [來源](https://www.patom.com/cafe)：官方 Thonglor 曼谷旗艦店段落明列花園、玻璃與再利用木材建築，支持網美風格；不混用 Sampran 農場分店。 |
| RBL CAFE | 文青 | 核准 | [來源](https://rblcafe.jp/)：瀏覽器核對官網提供可閱讀的參考圖書、書牆及手沖咖啡，支持文青風格；目前無排定活動，不宣稱現行展演。 |
| SIDOLI RADIO | 文青 | 核准 | [來源](https://sidoli.tw/about)：官網確認大稻埕同一場域結合录音、唱片、選物、咖啡及地方聲音故事，支持文青風格。 |
| TERAROSA 水營店 | 網美 | 核准 | [來源](https://www.visitbusan.net/index.do?lang_cd=en&menuCd=DOM_000000302002001000&uc_seq=2414)：釜山市官方 F1963 專題明確把鐵板桌面及入口鋼線裝置歸於 Terarosa 咖啡空間，支持網美風格；不挪用鄰近展館服務。 |
| TaKaoBooks | 文青 | 核准 | [來源](https://www.takaobooks.tw/html/about)：瀏覽器核對官網的人文選書與文化交流內容，日文介紹明列二樓咖啡、三樓講座及地下藝廊，支持文青風格。 |
| The Book Cafe | 文青 | 核准 | [來源](https://www.thebookcafesg.com/about)：現行官網列出供閱讀的書籍雜誌與沙發休憩空間，支持文青風格；採 Martin Road 店而非早期地址。 |
| The Coastal Settlement | 網美 | 核准 | [來源](https://www.thecoastalsettlement.com/)：官網明列綠意環繞與古董家具、復古收藏的餐飲空間，支持網美風格；不推論海景或商業拍攝許可。 |
| Walden Woods Kyoto | 網美 | 核准 | [來源](https://www.walden-woods.com/lp03/)：瀏覽器核對品牌 Greeting 頁的白色森林與白色空間設計，支持網美風格；文學命名不等於借閱服務。 |
| café & books bibliothèque Fukuoka Tenjin | 文青 | 核准 | [來源](https://vioro.jp/shop/bibliothequecafe/)：瀏覽器核對 VIORO 指定店家頁，明列書籍、藝術資訊與咖啡文化交流業態，支持文青風格；不挪用推薦鄰店特色。 |
| kubrick | 文青 | 核准 | [來源](https://kubrick.com.hk/hk-shops-and-contacts)：瀏覽器核對油麻地 H2 店址，同頁確認書店、咖啡與影碟服務，支持文青風格；不混用太古城藝術空間。 |
| フランソア喫茶室 | 文青 | 核准 | [來源](https://francois1934.com/concept/)：官網確認現存創辦人畫作、古典音樂與藝術文化交流定位，支持文青風格；不加上網美或不受限攝影主張。 |
| 中央書局 | 文青 | 核准 | [來源](https://www.centralbook.migos.com.tw/)：瀏覽器核對官方的選書、好書好食及書飲文化交流空間，支持文青風格；不把2020年活動當成現行展覽。 |
| 喫茶ソワレ | 文青 | 核准 | [來源](https://www.soiree-kyoto.com/about/)：瀏覽器核對官網 About 頁，確認店內原畫收藏、雕刻家木雕及專屬杯具線畫，支持文青風格；不推論現場音樂演出。 |
| 喫茶ソワレ | 網美 | 核准 | [來源](https://www.soiree-kyoto.com/about/)：瀏覽器核對官網 About 頁，確認青色照明與多色果凍的視覺設計，支持網美風格；不代表任意攝影許可。 |
| 喫茶七番 | 網美 | 核准 | [來源](https://www.kissa7ban.com/)：瀏覽器核對官網，店內中央黃色圓形點餐櫃檯為本店具體設計，支持網美風格；不移用二樓租借空間。 |
| 宮原眼科 | 網美 | 核准 | [來源](https://travel.taichung.gov.tw/ja/Attractions/Intro/1211)：瀏覽器核對台中觀光局指定景點頁，確認紅磚外牆與挑高圖書館式內裝，支持網美風格；造景不等於書籍閱覽。 |
| 文喫 六本木 | 文青 | 核准 | [來源](https://roppongi.bunkitsu.jp/store/)：分店官網明列藝術設計等選書室、閱覽室及喫茶室，支持文青風格；不宣稱全館免費。 |
| 本屋 B&B | 文青 | 核准 | [來源](https://bookandbeer.com/about/)：官網確認逐本選書、作者編輯交流及飲品服务，支持文青風格；需預約的活動與一般購書分開。 |
| 森彦 | 網美 | 核准 | [來源](https://www.morihico.com/shop/morihico/)：官方本店頁確認紅屋頂、蔓藤、木造二樓挑空及古時計桌椅，支持網美風格；不推論所有座席視野或文化活動。 |
| 浮光書店 | 文青 | 核准 | [來源](https://athenabooks.com.tw/about/)：官網明列浮光書店的藝術文哲、攝影電影選書、閱讀座區與咖啡茶飲，支持文青風格；不保證當日講座。 |
| 現流冊店 | 文青 | 核准 | [來源](https://hianlaubookshop.com/)：官網確認以台灣文學、歷史、音樂、電影及公共議題選書的獨立文化書店，支持文青風格；不只依店名判斷。 |
| 神保町ブックセンター | 文青 | 核准 | [來源](https://www.jimbocho-book.jp/cafe/)：瀏覽器核對現行官方 CAFE 頁，明列可購書閱讀的喫茶店與書籍餐飲空間，支持文青風格；辦公參觀規則不套用一般用餐。 |
| 第四信用合作社 | 網美 | 核准 | [來源](https://travel.taichung.gov.tw/zh-tw/Experience/Painted)：瀏覽器核對台中市觀光局專題，確認老建築再利用、保留金庫外觀與新設備組合，支持網美風格；不採用矛盾年代資料。 |
| 華山青鳥 | 文青 | 核准 | [來源](https://www.huashan1914.com/w/huashan1914/CustomShops_17081617223586642)：華山園區指定店家頁明列人文主題選書、書籍跨界活動及咖啡輕食，支持文青風格；不把過去活動視為當期節目。 |
| 青田七六 | 文青 | 核准 | [來源](https://www.qingtian76.tw/)：官網明列老屋餐飲、街區文化導覽、文化體驗及岩石標本科普內容，支持文青風格；不僅根據老屋外觀。 |
| 오설록 티하우스 북촌점 | 網美 | 核准 | [來源](https://www.osulloc.com/kr/ko/store-introduction/312)：品牌北村分店頁確認住宅的現代改造與茶香展示、茶廳及茶吧的樓層設計，支持網美風格；不套用濟州茶園景觀。 |

## 批次進度

- 第一批：632 筆已評估，8 筆失敗，80 次額度用盡；未評估項目由後續工作接續。
- 第一批的 194 筆模型拒絕建議已逐筆讀取證據：131 筆維持拒絕，63 筆改保留待審。加上 438 筆模型與發布規則均要求保留的項目，共套用 632 筆，131 拒絕、501 保留待審。
- 每筆套用均保留原 Gemini 理由，另外記錄本次編輯決策。正常套用稽核及編輯決策稽核各 632 筆；相同決策清單重播回傳一致結果，未重複增加稽核。
- 第一批 438 個模型待審項目中，426 缺精準地圖、430 未獨立驗圖、165 缺可核對引用、94 信心不足、37 缺永久來源座標與座標驗證；缺項可重疊。
- 第二批：`feab40cb-27b9-4f91-aedd-4e7ecb55b0ed`，640 個起始範圍內未評估快照。
- 第二批完成 576 筆評估、48 筆回應截斷失敗、16 筆未評估，80 次上限不變。194 個拒絕建議逐筆複核後，114 筆拒絕、80 筆保留；另 382 筆依缺項保留，共套用 576 筆。正常套用與編輯決策稽核各 576 筆。
- 第二批模型待審的 382 筆均缺精準地圖身分與獨立驗圖，其中 105 缺可核對引用、60 信心不足、20 缺 Wikidata 身分及永久座標；缺項可重疊。
- 本川公眾廁所來源明記被爆建物，不因目前用途就拒絕；國立民俗博物館及板頭村為城市／座標錯配，先待修正，不認定場所不存在。
- 第三批：`e4cf0849-3877-4065-8571-61c1a6f837d0`，07:30 UTC 開始處理後續 640 筆。前兩批已有 1,208 個不同實體完成評估與套用，餘 1,174 未評估。
- 第三批於 07:53 UTC 完成 576 筆評估、16 筆回應截斷失敗，達 80 次上限。203 個模型拒絕建議逐筆複核後，113 拒絕、90 保留；另 373 筆依發布缺項保留，合計套用 576 筆（113 拒絕、463 保留）。三批共 1,784 個不同實體已套用，歷史決策為 358 拒絕、1,426 保留；另有下述 2 間店人工補核後核准。
- 第三批的 373 筆模型待審均缺精準地圖與獨立驗圖，123 缺可核對引用、78 信心不足、15 缺 Wikidata 身分及永久座標。天神商圈、堂島歷史辦公建築、寺內佛畫等不因類型或資料不足直接拒絕。
- 第四批：`4930c6ea-6e4d-4526-91be-f58fb14e706f`，07:54 UTC 開始處理剩餘 598 個未評估實體（467 景點、131 店家）。
- 第四批於 75 次呼叫後有 24 筆截斷，使用正常續跑服務補足 3 次呼叫，08:11 UTC 完成全部 598 筆、失敗 0。117 個模型拒絕建議複核為 77 拒絕、40 保留，加上 481 筆模型待審，共套用 77 拒絕、521 保留。四批正常套用與編輯決策稽核各 2,382 筆。
- 四批歷史套用為 435 拒絕、1,947 保留；後續曾有 5 間店人工來源核准，其中 Mak's Noodle 因最終發現混店而撤回，最終淨核准 4 間，目前目錄保留數為 1,943。模型歷史不回寫成核准。前三個工作保留原本達上限的 partial 歷史，整體覆蓋由四批初始實體 ID 聯集核對，不能只看根工作狀態。
- 07:06 UTC 正式服務被其他部署替換，第二批於 80 筆時中斷。租約過期後使用既有續跑服務恢復；已用 11 次呼叫與完成內容保留，並確認後台重新顯示評估進度。

## 追蹤與驗證

### 官方分店來源人工補核

Gemini 抓取／引用失敗的兩間店，另以公開官方分店頁人工核對；當時資料庫的地圖、座標、直接來源及分類欄位完整，完整快照與起始版本一致且程式發布缺項為零，曾透過既有管理服務核准。最終複核證明 Mak's Noodle 的既有地圖雖標記 verified，實際仍混用另一家店，已撤回其核准（見下節）：

- [山本屋本店門市指南](https://yamamotoyahonten.co.jp/storeguidance/)：栄本町通店，名古屋市中区栄2-14-5。
- [Mak's Noodle 官方分店頁](https://www.maksnoodle.com/en/%E5%88%86%E5%BA%97%E8%B3%87%E6%96%99)：Main Branch，中環威靈頓街 77 號地下。

只變更核准／啟用狀態；原有地圖及座標驗證時間仍為 2026-09-07，沒有藉來源複核刷新定位驗證。新增兩筆既有批次店家稽核及兩筆獨立人工來源複核稽核；原 Gemini 待審評估保持不變。公開 BFF 各查到一間對應店家，五語系既有店名正常沿用。

此階段先前 963 筆保留待審決策中有 2 間店後續人工核准；歷史批次數字不回寫成模型核准。當時店家為 271 核准／165 待審／3 拒絕。

第四批完成後再核准下列 3 間，全部通過完整起始快照一致、當前發布缺項為零及有效管理員檢查，只執行普通 approve，不執行 verify／verify_activate：

- [Ukishima Brewing Tap Room](https://www.ukishimabrewing.com/tap-room.html)：沖繩牧志 3-3-1 水上店舗第二街區 3F；觀光局與店家頁地址一致，確認餐食與精釀啤酒。
- [Gecko – Huế Cuisine & Craft Beer](https://www.facebook.com/geckohuecuisine/)：瀏覽器確認順化 09 Pham Ngu Lao 店址、餐飲服務及店家發文，不套用其他同名店。
- [Kanomwan Chang Moi](https://www.facebook.com/Thaidessertcnx)：瀏覽器確認清邁 169 Chang Moi 店址與泰式甜點。完整閱讀品質客訴與訊息漏回公告，非停業通知；此次為身分／目錄核准，不作食品安全或品質背書。

5 次人工核准皆另留 `catalog_review_browser_override` 與既有店家批次稽核；其中 1 次已更正撤回，歷史不刪除。最終仍核准的 4 間店，地圖及座標查核時間維持 2026-09-07，沒有刷新。最終全資料庫店家為 273 核准／163 待審／3 拒絕；景點為 1,049 核准／1,780 待審／1,060 拒絕／5 停用，原已核准／停用景點不變。

未解決缺項仍保留於逐筆決策清單及後台：歷史保留決策中 1,880 缺精準地圖、1,898 未獨立驗圖、611 缺可核對引用、399 信心不足、151 缺永久座標與查核、76 缺直接店家來源、65 缺 Wikidata 身分；缺項可重疊，後續人工核准與撤回均不回寫清除模型歷史缺項。

### 最終混店更正：Mak's Noodle Central

前台顯示的中文名稱是「麥奀記忠記傳統雲吞麵家」，不是所引用官方來源的「麥奀雲吞麵世家」。[香港旅遊發展局的指定店家頁](https://www.discoverhongkong.com/tc/place-to-go/travel.guide-mak-s-noodle.html)確認後者位於威靈頓街 77 號；[國泰的香港美食介紹](https://www.cathaypacific.com/cx/zh_TW/inspiration/dining/must-try-hong-kong-food.html)則把麥奀記（忠記）麵家列於永吉街 37 號。瀏覽器開啟既有精準 Google Place ID `ChIJx7wp6HwABDQRcl6W0a4eJL8`，也確認指向後者，不能當作前者的定位證據。

本次先前核准只檢查來源與既有 verified 欄位，漏掉名稱／定位的語意衝突，因此已透過既有更新服務撤回自己的核准：`review_status=pending`、`is_active=false`、`map_match_status=ambiguous`，清除原地圖 verified_at／verified_by。原 ID、座標與座標查核時間保留，沒有編造新 ID 或直接改名。新增 `catalog_review_identity_correction`（含原核准稽核 ID、原因、來源及前後值）與正常 `food_merchant_updated`；原核准及模型紀錄保留。

更正前只允許與本次核准一致的狀態與精確 updated_at，其餘完整快照必須仍與初始相同；更正重播不重複寫入。公開 BFF 再查此店回傳 0，其他 4 間核准店各回傳 1。此例也說明「程式發布缺項為零」不能代替實際的名稱、分店與地圖交叉核對。

### 第四批額外來源檢查

- [BIOTOP 官方店舖資訊](https://www.biotop.jp/about/)確認大阪地址，但 1F 咖啡站與 4F CUBIERTA 是不同空間；現有名稱／slug 指向不一致，保留待釐清，不用整棟地址替代分店身分。
- [新宿つな八現行分店頁](https://www.tunahachi.co.jp/store/53.html)指向新宿 3-28-4 的總本店別館；候選名稱仍為總本店，須先核對精準地圖，未直接核准。
- [少爺啤聯絡頁](https://youngmasterales.com/pages/contact-us)明示黃竹坑工廠不對一般公眾開放；[中環 Taproom](https://youngmasterales.com/pages/young-master-central)是 BaseHall 01 的另一處場所。保留待確認工廠預約參訪／門市身分，不混用地址。
- [Wattana Panich 既有 Facebook 來源](https://www.facebook.com/profile.php?id=188502191167176)在瀏覽器明示「非官方粉絲專頁」，雖地址相符，也不能當成官方來源；保留待補真正直接來源。People & Life.Cafe 的 Facebook 及 Hong Sieng Kong 的 Instagram 讀取受阻，未繞過限制，也不當作停業證據。
- [沖繩觀光局浮島 Tap Room 頁](https://www.okinawastory.jp/gourmet/600010867)與[店家 Tap Room 官網](https://www.ukishimabrewing.com/tap-room.html)共同確認牧志 3-3-1 的三樓餐飲店及精釀啤酒；官網較觀光頁多列一個休息日，因此不將舊營業時間當成最新資訊。
- Here Hai 公開頁可確認品牌與餐飲，未提供現有候選門牌；關於頁目前無法顯示。So Heng Tai 顯示歷史宅院與潛水課程，但街巷文字和餐飲類別仍待確認。Som Tam Udon 指定觀光頁只讀到框架，不使用觀光局頁尾地址作店址；以上均保留待確認。

## 最終驗證與保留資料

- 初始範圍 2,382 個實體全部 assessed／applied；最後 SQL 確認無本輪以外新增待審景點或店家。
- 29 組明確決策清單完整重播，輸出與首次套用逐位元相同；當時 5 間人工核准重播均為 replayed，2,382 + 2,382 + 5 筆相關稽核數量不增加。另有 44 筆正常風格稽核、5 筆正常店家批次核准稽核。最終再新增 1 筆身分更正及 1 筆正常店家更新；更正重播不增加紀錄。
- 最終公開 BFF 對 4 間核准店各回傳 1 個精準對應結果；撤回的 Mak's Noodle、Wattana Panich、Young Master Brewery、ACME 北美館店均為 0，不洩漏待審店家。文青／網美公開篩選仍各只有 FAbULOUS／Walden Woods Kyoto，風格核准不會單獨發布店家。
- 正式 `/ready` 回傳 database／redis ok，schema `0063_destination_offers`。本任務未部署、未改 schema，也未修改會員、帳務、API 金鑰或額度設定。
- 審核前後均有 mode 600 的私有 PostgreSQL 備份與有效 pg_restore 索引。08:16 的 after.dump 保留不覆寫；08:28 更正後另存 final-after-correction.dump（12,415,953 bytes）及索引。操作輸出、coverage／status 與重播紀錄保留在同一伺服器私有目錄；不將資料庫備份或憑證提交 Git。
- 一次性操作腳本通過 Ruff check／format 及正式容器 py_compile；任務板檢查、JSON 解析與 git diff --check 通過。沒有修改應用程式，因此未宣稱跑過全套 API／Web CI。
- 可追溯的逐筆清單：`ops/catalog_review_20260908_decisions.json`、`ops/catalog_review_20260908_styles.json`；原始模型來源與引用保留在既有後台工作紀錄。

已驗證正式公開 API 與 BFF 的風格篩選：文青 1 間 FAbULOUS、網美 1 間 Walden Woods Kyoto。瀏覽器前台文青篩選顯示 FAbULOUS、2026-09-08 查核日期與來源連結。風格操作當時店家仍為 269 核准／167 待審／3 拒絕；其後 2 間來源補核核准的異動另計。

操作程式與明確決策清單位於 `ops/catalog_review_20260908*`。它們是本次有範圍／時效限制的操作紀錄，不是排程或通用自動核准功能。
