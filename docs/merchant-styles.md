# 網美與文青店家：分類、查核與上架

## 功能與審核

`/{locale}/foods` 新增「店家風格」，可與城市、商圈、餐飲分類及關鍵字交叉篩選。
`instagrammable`（網美店）與 `artsy`（文青店）不是料理分類，同店可有兩種風格。
五語系共用機器代碼；只有核准標籤才出現在公開卡片、篩選結果及計數，卡片附來源與查核日期。

- 網美：具體分店的空間設計、陳列、花藝或視覺特色；不是人氣排名、性別或拍照許可。
- 文青：書籍、藝術、音樂、設計、選物或地方文化的具體內容。只供應咖啡不構成充分依據。
- 標籤是有來源的編輯判斷，不宣稱店家自稱或授予認證，不複製未授權照片、評論。

後台 `/admin/foods` 店家清單可依風格及待審／核准／拒絕篩選。
編輯店家，展開「風格新增與審核」後逐項處理；新店先儲存基本資料。
每次須填 HTTPS 來源、標題、查核日期、至少 10 字元的判定依據及審核原因。
切換風格保留草稿；重新載入會捨棄草稿。風格與店家基本資料分開儲存。
已核准標籤可退回待審或拒絕，立即停止公開該標籤，不刪店家、行程或審核歷史。

**核准風格不等於發布店家。** 原有 approved + active + 精準地圖識別 + 可永久保存的座標 +
目前有效來源等條件不變；韓國仍須 Naver 精準地點頁。

## API 與資料

- `GET /api/v1/foods/merchants?style=instagrammable`：支援既有篩選、游標分頁。
- `GET /api/v1/foods/categories?style=artsy`：以風格篩選餐飲分類數量。
- `GET /api/v1/admin/foods/merchants?style=artsy&style_status=pending`：管理待審標籤。
- `GET /api/v1/admin/foods/merchants/{id}/styles`：讀取證據與版本時間。
- `PUT /api/v1/admin/foods/merchants/{id}/styles`：提交 `reason`、`expected_updated_at` 與單一 `review`。

管理端沿用有效管理員授權。新增 `0061_merchant_styles` 遷移，每店每風格有唯一約束，預設待審；
遷移不替舊店家分類或上架。更新以店家列鎖序列化，過期版本回傳 `409 merchant_style_changed`。
`food_merchant_style_reviewed` 稽核保存操作者、原因、目標及異動前後資料。
公開回應不含內部判定理由或審核人 ID。

## 首批來源查核：2026-09-08

資料檔：`apps/api/app/foods/data/style_merchants_2026_09.json`。
**4 家新候選 + 1 家既有店家補風格**，不是 5 家已公開店家。
以下是本次閱讀原始來源後的編輯判定，不代表親自到訪或保證當日營業；
正式資料庫的風格核准須透過管理 API 記錄操作人。

| 店家 | 本輪來源審核 |
| --- | --- |
| 東京 Aoyama Flower Market GREEN HOUSE 南青山 | 網美：官方描述花卉溫室及陳列。採現址 5-4-41，不採舊文章 5-1-2。[現行分店頁](https://www.afm-teahouse.com/aoyama)、[品牌空間介紹](https://foreign.aoyamaflowermarket.com/foreign/teahouse/pc/) |
| 台北 SIDOLI RADIO 小島裡 | 文青：錄音、唱片、選物及地方聲音故事。僅取官網街道門牌，不複製與行政區不一致的郵遞區號。[介紹](https://sidoli.tw/about)、[地址](https://sidoli.tw/contact) |
| 台北 CBC SPACE 景美咖啡圖書館 | 文青：官網明列二樓 boven 紙本雜誌與設計閱讀空間；與復興南路本店分開，不匯入歷史優惠。[分館頁](https://cbcspace.com/zh-tw/jmcoffee) |
| 台北 CAFE ACME 北美館 | 文青候選：品牌說明此分店的藝術生活定位與地址。未憑第三方爆紅文章加網美標籤；審核者可要求更具體的店內藝術活動證據。[分店頁](https://acmetaipei.com/zh/pages/cafe-acme-taipei-fine-arts-museum_) |
| 札幌 FAbULOUS | 文青：當期藝術展、家具服飾選物及咖啡業態，同址既有候選只補缺少標籤，不重建店家。[官網](https://www.rounduptrading.com/) |

4 家新候選尚缺精準地圖識別、可永久保存的座標及店家發布審核。部署匯入時確認 FAbULOUS
原有 approved/active/verified 狀態保持不變，只補待審風格。未核實商圈不猜測，4 家新店暫留未分區。
未納入：Fika Fika 伊通店官網英文街名與中文不一致，本輪空間風格證據也不足；
ASW 僅找到較舊觀光介紹，不把頁面仍可讀當成近期營業確認。

## 第二批來源查核：2026-09-08

資料檔：`apps/api/app/foods/data/style_merchants_2026_09_batch_02.json`。
本批 **8 家新候選、9 個待審風格（網美 5、文青 4）**，京都沿用 `osaka-kyoto` 目的地。
所有判定都是根據原始來源的編輯提案，並非親訪、人氣排名或當日營業保證。

| 店家／城市 | 判定依據與分店限制 |
| --- | --- |
| 宮原眼科／台中 | 網美：紅磚外牆、挑高圖書館式陳列；造景不等於閱讀服務。[市府介紹](https://travel.taichung.gov.tw/ja/Attractions/Intro/1211)；[官方地址與拍攝／寵物規則](https://www.dawncake.com.tw/en/pages/store-information)。不與二樓醉月樓混合。 |
| 第四信用合作社／台中 | 網美：舊建築再利用與金庫外觀。[市府專題](https://travel.taichung.gov.tw/zh-tw/Experience/Painted)；[日出現行門市頁](https://www.dawncake.com.tw/en/pages/store-information)確認中山路72號，與宮原眼科20號分開。 |
| 喫茶ソワレ／京都 | 網美＋文青：青色照明、藝術家參與的家具與杯具設計、彩繪玻璃；真町95號。[官網與9月營業日公告入口](https://www.soiree-kyoto.com/) |
| フランソア喫茶室／京都 | 僅文青：延續的古典音樂、繪畫及藝術家設計的彩繪玻璃。[文化內容](https://francois1934.com/concept/)；[地址](https://francois1934.com/access/)；[拍攝限制](https://francois1934.com/20260127/)要求避免座位餐飲留念以外的室內拍攝，不加網美提案。 |
| BUNDAN COFFEE & BEER／東京 | 文青：文學館內實際可閱覽的藏書，不只是館址借名。[閱讀內容](https://bundan.net/about/)；[地址及近期營業調整](https://bundan.net/)。日常打烊文字不是永久歇業。 |
| The Book Cafe／新加坡 | 文青：現行介紹仍提供書籍、雜誌及閱讀座位；採Martin Road，不使用早期Stamford Road地址。[店家介紹與地址](https://www.thebookcafesg.com/about) |
| Knots Cafe and Living Paya Lebar／新加坡 | 網美：花藝與家具陳列。[品牌介紹與FAQ](https://www.knotscafeandliving.com/)；[指定分店](https://www.knotscafeandliving.com/paya-lebar)。不混入Pasir Panjang分店；官方明示不接待寵物。 |
| Patom Organic Café Bangkok Flagship Store／曼谷 | 網美：Thonglor花園中的玻璃與再利用木材空間。[分店設計](https://www.patom.com/cafe)；[曼谷地址](https://www.patom.com/contact)。不挪用Sampran農場、週末市集等另一分店資料。 |

未納入 VVG 華山舊店，因[官方歇業公告](https://vvg.com.tw/news-post/406)；品牌其他近年文章不是舊址復業證據。
% Arabica 嵐山的官方頁本輪無法完整取得，不用第三方地址補成高信心候選。
第四信用合作社舊建築手札的年代敘述不一致，改採目前市府專題與商家地址，不複製年代或文化資產登錄主張。
本批不寫入寵物正式條件、不搬運店家照片、不生成地圖 ID 或座標；全部暫留未分區。

## 第三批來源查核：2026-09-08

資料檔：`apps/api/app/foods/data/style_merchants_2026_09_batch_03.json`。
本批 **7 家新候選、7 個待審風格（網美 3、文青 4）**，涵蓋台北、台中、香港、東京、首爾與新加坡。
仍是根據來源的編輯提案，不代表親訪、當日營業保證或風格核准。

| 店家／城市 | 來源與判定界線 |
| --- | --- |
| 青田七六／台北 | 文青：老屋導覽、文化體驗與岩石標本教育結合餐飲。[文化與餐飲介紹](https://www.qingtian76.tw/)；[地址與穿襪規範](https://www.qingtian76.tw/營業與交通資訊/)。不沿用舊宣傳的建物年齡或跨語系不一致的開放時段。 |
| 中央書局／台中 | 文青：二樓書食與三樓書飲文化交流。[官方樓層及地址](https://www.centralbook.migos.com.tw/)。不將2020年舊活動描述成近期展覽，也不將整棟樓都當成餐飲座位。 |
| kubrick 油麻地／香港 | 文青：同址書店、咖啡與電影文化選書。[指定店址及業態](https://kubrick.com.hk/hk-shops-and-contacts)。油麻地H2與太古城House by kubrick不同，不挪用後者的活動。 |
| 森の図書室／東京 | 文青：閱讀空間、書中食物主題餐飲與近期讀書會。[官網](https://morinotosyoshitsu.com/)。採2021年遷入的宇田川町23-3八樓；非會員亦可使用，但不宣稱免費或不限時。 |
| Onion 安國店／首爾 | 網美：保留韓屋木地板與庭院。[韓國觀光公社](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=191156)與[店家分店頁](https://m.onionkr.com/artfinger/offline.html?cate_no=26)交叉核對계동길5；不混用聖水工廠設計或公司地址。Naver地點仍待精準核實。 |
| PS.Cafe One Fullerton／新加坡 | 網美：航海主題與濱海景觀。[二樓分店頁](https://www.pscafe.com/pscafe-one-fullerton)。店號#02-03B/04，不保證所有座位視野相同。 |
| Jypsy One Fullerton／新加坡 | 網美：波希米亞海岸風格。[一樓分店頁](https://www.pscafe.com/jypsy-one-fullerton)。店號#01-02/03，與PS.Cafe及既有Palm Beach Seafood分開；[官方2026年餐飲文章](https://www.pscafe.com/blog/2026/1/23/the-modern-hosts-guide-to-stylish-canapes-and-effortless-entertaining)支持壽司分類，不保存舊菜單價格。 |

本批排除：

- 紫藤廬：[店家官網](https://www.wistariateahouse.com/)與[台北市文化局2026-09-01更新](https://culture.gov.taipei/cp.aspx?n=6D8D9BF9A2E55CCC)仍明示閉館修繕、不供餐茶。
- PS.Cafe Harding Road：[分店頁](https://www.pscafe.com/pscafe-at-harding-road)公告8月23日起整修，不能以仍列有一般營業時間就推定復業。
- Anthracite合井：找到官方搜尋摘要，但原頁受讀取限制，未使用繞過方式；保留待下次完整核實，不靠摘要強行加入。
- 林百貨HAYASHI Café：已確認五樓有餐飲，但目前查核內容不足以將咖啡廳本身評為文青或網美；不借用四樓藝文空間的內容作風格證據。

所有新候選保持未分區、未核准地圖與座標；沒有將風格提案轉為寵物正式條件或發布認證。

## 第四批來源查核：2026-09-08

資料檔：`apps/api/app/foods/data/style_merchants_2026_09_batch_04.json`。
本批 **5 家新候選、1 家既有店家補風格，共6個待審提案（網美3、文青3）**。
店家風格仍是有來源的編輯提案，不是親訪、即時營業保證或核准發布。

| 店家／城市 | 來源與判定界線 |
| --- | --- |
| 神保町ブックセンター／東京 | 文青：[官方喫茶中心](https://www.jimbocho-book.jp/cafe/)明列購書、閱讀、餐飲。館址同列1至3樓，不把辦公／會議室都描述成咖啡座，也不把辦公參觀預約要求套到一般用餐；不採舊PDF菜單價格。 |
| 本と珈琲 梟書茶房／東京 | 文青：[官方選書概念](https://www.doutor.co.jp/fukuro/)以推薦文字與編號引導閱讀；[現行店鋪頁](https://shop.doutor.co.jp/doutor/spot/detail?code=6010001)確認Esola池袋四樓。昔日限定套組不是當期供應保證。 |
| 文喫 福岡天神／福岡 | 文青：[分店地址與設施](https://tenjin.bunkitsu.jp/)、[閱讀與喫茶規則](https://tenjin.bunkitsu.jp/about/)。位於岩田屋本館七樓，喫茶室為付費區；同頁140／170席數不一致，本批不記席數及費率，不套用其他文喫分店資訊。 |
| Brown Hands Baekje／釜山 | 網美：[釜山市韓文店家頁](https://www.visitbusan.net/index.do?lang_cd=ko&menuCd=DOM_000000201001001000&uc_seq=231)確認店名、地址與改造設計；[官方建物介紹](https://www.visitbusan.net/index.do?lang_cd=en&menuCd=DOM_000000301001001000&uc_seq=266)區分一樓咖啡店與三樓Gallery EB9。不挪用藝廊作文青證據；官方頁間年代／時段不同，不記這些數字或登錄編號。品牌站本輪無法讀取，不宣稱取得品牌確認。 |
| TERAROSA 水營店／釜山 | 網美：[品牌指定分店](https://www.terarosa.com/store/detail/?id=14)確認F1963內地址，[釜山市專題](https://www.visitbusan.net/index.do?lang_cd=en&menuCd=DOM_000000302002001000&uc_seq=2414)具體描述咖啡店鐵板桌面與鋼線裝置。不誤用頁尾江陵公司地址，也不把園區其他書店、圖書館及畫廊算作本店服務。 |
| Walden Woods Kyoto／京都 | 僅補既有店家的網美提案：[官網白色森林概念](https://www.walden-woods.com/)、[現行可讀的地址頁](https://www.walden-woods.com/lp02/)與既有同址資料吻合。文學命名不等於閱讀服務，2021年甜點消息不當作2026年新品。 |

文房具カフェ本輪暫不納入風格提案：已確認[現行活動](https://www.bun-cafe.com/)，但可自由使用文具的FAQ多屬舊活動；不將舊體驗規則直接當成目前常態服務，也不把未納入描述成歇業。
兩家韓國新店仍須精準Naver識別，不新增Google替代連結；所有新候選地圖、耐久座標與商圈留空。
Walden Woods的既有approved/active/verified狀態、地圖、座標、來源及分類保持原狀。

## 第五批來源查核：2026-09-08

資料檔：`apps/api/app/foods/data/style_merchants_2026_09_batch_05.json`。
本批 **5 家新候選、5 個待審提案（網美2、文青3）**；沒有替既有店家改名、改址或核准風格。
查核日期表示本輪閱讀來源的日期，不是親訪或保證每項舊描述今天仍然有效。

| 店家／城市 | 來源與判定界線 |
| --- | --- |
| 現流冊店／台北 | 文青：[官網](https://hianlaubookshop.com/)確認文化選書、咖啡、咖哩及重慶北路二段70巷15號1樓。保留中文原名，不把官網異常羅馬字自行改寫為英文品牌，也不使用舊址建立重複店家。 |
| 浮光書店／台北 | 文青：[品牌店舖一覽](https://athenabooks.com.tw/contact/)與[文化部消費點](https://twcp.moc.gov.tw/prec-u/project/content/1317fab9f3c6480884f287d903c23047)確認赤峰街47巷16號2樓；[品牌介紹](https://athenabooks.com.tw/about/)列選書、講座及閱讀餐飲。與春秋、風景、銀月各店分開；動物友善概述不足以建立完整寵物條件。 |
| ONIBUS COFFEE 中目黒駅前店／東京 | 網美：[現行分店頁](https://onibuscoffee.com/pages/locations/nakameguro)確認上目黒2-14-1；[2022年品牌介紹](https://onibuscoffee.com/en/blogs/news/114)記載大谷石、常滑燒磁磚與手繪設計。不是中目黒三丁目店；焙煎設備已移走，不沿用舊菜單、人氣、攝影或寵物規則。 |
| Cafe Bibliotic Hello!／京都 | 文青：[品牌地址](https://cafe-hello.jp/)與[京都市京都館](https://www.kyotokan.jp/read/my-local-guide-kyoto-16-03/)一致，後者描述書牆與咖啡文化空間。品牌展覽資訊仍停在2017年，官方時段亦不一致，信心記為medium、營運細節待複核；不把Halo Galo的展覽當作現行咖啡店服務。 |
| The Coastal Settlement／新加坡 | 網美：[官網](https://www.thecoastalsettlement.com/)確認Changi的200 Netheravon Road店址及綠意、古董家具與復古物件。只採本店空間設計，不用早期手冊菜單、不保證海景或拍攝許可，也不自動核准頁上訂位平台。 |

浮光的Facebook及部分台北旅遊網頁本輪讀取受限，未繞過；採可完整讀取的品牌與文化部頁面。
Halfway Coffee本輪未完成足夠的官方分店證據閱讀，暫不加入，不等於判定歇業。
所有新候選仍須補精準地圖、耐久座標、商圈與管理員審核；沒有複製店家照片、啟動付費服務或建立寵物正式規則。

## 第六批來源查核：2026-09-08

資料檔：`apps/api/app/foods/data/style_merchants_2026_09_batch_06.json`。
本批 **4 家新候選、4 個待審提案（網美3、文青1）**；涵蓋高雄、札幌與名古屋。
查核為閱讀官方來源後的編輯判定，不是親訪、即時營業保證、攝影許可或風格核准。

| 店家／城市 | 來源與判定界線 |
| --- | --- |
| 三餘書店／高雄 | 文青：[品牌簡介](https://www.takaobooks.tw/html/about)確認人文選書、二樓咖啡與中正二路214號。三樓講座與地下藝廊分開描述；不挪用書市集文章中其他書店的地址或搬遷消息，不沿用歷史優惠。 |
| 森彦／札幌 | 網美：[本店介紹](https://www.morihico.com/shop/morihico/)記載紅屋頂、蔓藤、木造挑空與古物陳設。與ATELIER／藝術劇場／機場等分店分開；官網限四人且不接受預約，不宣稱有團體訂位。頁上7月23日臨休未標年份，不解讀為永久歇業。 |
| 喫茶七番／名古屋 | 網美：[官網](https://www.kissa7ban.com/)明列中央黃色圓形櫃檯、餐飲與1-A地址。2-A為另外的租借空間，不將其活動或租借規則套用到一樓咖啡店；不以活動回顧保證每日有活動。 |
| 喫茶ニューポピー／名古屋 | 網美：[品牌店鋪頁](https://b-bitou.com/shop/)記載新建藏造空間、中央挑空與塔狀閣樓座位，地址為那古野一丁目36番52号。不是江戶古蹟改造，也不混用同址焙煎室或不同地址談話室；只採現行頁明列的咖啡、咖哩與甜點業態。 |

本輪未納入烏邦圖：總圖店品牌頁可讀，但地址的一手頁面尚未完成核對；不把環河店舊活動或過期優惠當作總圖店現況。
Dragonfly的大館及香港會展旅遊頁讀取受限，未繞過限制，也不靠搜尋摘要建立候選；這些排除不代表判定歇業。
四家均未與既有店家同名／同址重複；地圖、耐久座標與商圈仍須另行核實。未複製照片、啟動付費服務或推導寵物條件。

## 部署與匯入

部署同版本 API、Web、worker 並執行 `alembic upgrade head`。
環境需先有既有 food categories；先預覽，確認目標環境與結果後才寫入：

```sh
python -m app.cli import-trend-merchants --file app/foods/data/style_merchants_2026_09.json
python -m app.cli import-trend-merchants --file app/foods/data/style_merchants_2026_09.json --apply
```

匯入建立 pending、inactive、unverified 店家及 pending 風格，JSON 不能指定 approved。
同 slug 需同目的地及原文店名才補缺少的風格；同城同名亦去重。
不覆寫既有 pending／approved／rejected 風格。重跑不新增重複資料或稽核。
新增風格批次記錄 `food_merchant_styles_proposed`，店家新增沿用既有稽核。
確認來源後在後台記錄風格核准，補完地圖與座標後另走店家發布流程。

第二批使用相同命令，將 `--file` 換為 `app/foods/data/style_merchants_2026_09_batch_02.json`。
第三批則為 `app/foods/data/style_merchants_2026_09_batch_03.json`。
第四批則為 `app/foods/data/style_merchants_2026_09_batch_04.json`。
第五批則為 `app/foods/data/style_merchants_2026_09_batch_05.json`。
第六批則為 `app/foods/data/style_merchants_2026_09_batch_06.json`。
既有部署可將新 JSON 送入受控暫存路徑後傳給 `--file`；資料補充不需重建服務或執行新遷移。

### 實際執行記錄

- PR [#345](https://github.com/x812033727/travel_scanner/pull/345) 已依授權合併，2026-09-08 部署
  `b3e49a325edcc41e167653e9fe13619403248507`；main CI 全綠，資料庫為 `0061_merchant_styles`。
- 首批備份後預覽、套用與重播完成：4 家新候選、1 家既有店家補風格、5 個 pending 風格；重播零新增。
- 第二批於使用者「繼續新增」要求下補充候選；正式寫入前核對現行映像、名稱／地址去重、兩個部署鎖、
  JSON SHA-256、custom-format 資料庫備份及 `pg_restore --list` 可讀性。此操作不是管理員風格核准。
- 第二批正式匯入已完成：8 家均為 pending/inactive/unverified，9 個風格均為 pending，
  精準地圖／座標／商圈欄位留空；`food_merchant_created` 與 `food_merchant_styles_proposed` 各一筆，
  actor 為系統匯入而非冒用管理員。再次預覽為零新增、零風格提案。
- 第二批備份 7,050,608 bytes、權限 600、目錄可讀；資料檔 SHA-256 為
  `d02716eb0c516d6c8acd8f7f7e4185df502ae84418306502ff1df09e67f2fc3b`。
  兩批合計 12 家新候選及 1 家既有店家補風格，共 14 個待審標籤；公開兩種風格查詢仍為零，
  `/ready` 的 database/redis/schema 正常、前台美食頁 HTTP 200。
- 不變更公開發布狀態、不啟動付費 Gemini／Places 批次。完成來源資料及待審匯入，不代表完成公開上架。
- PR [#346](https://github.com/x812033727/travel_scanner/pull/346) 於2026-09-08依授權合併，
  以 exact-head guard 鎖定 `49748e84c405485180aac86276cf32c68371ed7f`；merge commit
  `b06022771c90a834180ac2607c0fe223db79eadb` 已在main，合併後CI `34175624475` 全綠。
  此PR僅資料、測試及交接文件，第二批已匯入，因此未重建現有服務或重跑遷移。
- 第三批正式匯入：7 家 pending/inactive/unverified、7 個 pending 風格（3網美／4文青），
  地圖／座標／商圈保持空白；建立店家及風格提案的系統稽核各一筆。再次預覽0店／0標籤。
  備份7,055,257 bytes、權限600且目錄可讀；資料檔SHA-256為
  `9ea9548218b19cd8ab2440e19d0034c4d297f6290b90eb84dba05ec78d16a0c8`。
  三批合計19家新候選、1家既有店家補風格，共21個pending標籤（網美9／文青12）；
  readiness正常，候選仍未公開。
- PR [#347](https://github.com/x812033727/travel_scanner/pull/347) 於2026-09-08依授權合併；
  exact-head guard鎖定 `744262e31b12ff48edda9fff02f03ea1ca6b1f4e`，merge commit
  `67234d9bd56a1a037b62daf6439275339e3ae1d3` 已在main，post-merge CI `34179094453` 全綠。
  第三批此前已匯入，本輪合併未重建應用服務或新增遷移。
- 第四批查重、JSON checksum、兩個部署鎖、私人備份及restore目錄驗證完成後正式套用：
  5家新店pending/inactive/unverified、6個pending風格（3網美／3文青）；再次預覽0店／0標籤。
  店家建立與風格提案各一筆系統稽核，actor=NULL。Walden Woods店家、來源及分類資料的前後完整快照相同。
  備份7,060,901 bytes、權限600；資料SHA-256為
  `99954c26fb93226577a083c4aca6fabaf32c56d672131ecf89e38acf7bd8aecd`。
  四批合計24家新候選、2家既有店家補風格，共27個pending標籤（網美12／文青15）。
  公開風格查詢仍0；readiness正常，前台美食頁HTTP 200。未呼叫核准、發布、付費地圖或模型API。
- PR [#350](https://github.com/x812033727/travel_scanner/pull/350) 於2026-09-08依授權合併。
  同步main的#349與#352後，exact-head guard鎖定 `240178b6daff4607b8db1e4be027d4aefc70fcd3`，
  八項checks全綠；merge commit `7b19c2f5717a1becdb6f93249bb0fc9d5c4ae598` 已確認在main。
- 第五批於該main建立獨立分支；正式環境已另行更新至
  `aaa33f008c82c56e5c541dede8205097102193e1`、schema `0062_merchant_platform_links`。
  本批只使用現行importer，不重建服務、不執行遷移，也不核准新的預約連結。
- 第五批取得兩個部署鎖、核對本機／伺服器／容器JSON checksum、鎖內再預覽與備份驗證後，
  新增5家pending/inactive/unverified店家及5個pending風格（2網美／3文青）；再次預覽0／0。
  兩筆稽核分別記錄建立5店、提案5風格，actor=NULL系統匯入；地圖、座標、商圈及審核人員欄位未填入。
  備份7,087,794 bytes、權限600、`pg_restore --list`可讀，JSON SHA-256為
  `b1509b953e5362d3be6f1220a2ea67ede2196a8344c8e2694c20c15d8eaba957`。
  五批合計29家新候選、2家既有補風格，共32個pending標籤（網美14／文青18）；公開風格仍0，
  readiness正常，前台美食頁HTTP 200。來源、預覽、套用及重播收據與私人備份皆保留。
- PR [#354](https://github.com/x812033727/travel_scanner/pull/354) 於2026-09-08依授權合併。
  無衝突同步main的#353後，八項checks全綠、CLEAN／MERGEABLE，exact-head guard鎖定
  `bab1e5af71652711237470cca49e4e39d66d20bc`，合併為 `88eb4b15b99619782d60e78c29ab12f5c9e35c68`，已fetch確認在main。
- 第六批先核對現行API映像、名稱／地址查重、本機／伺服器／容器checksum、兩個部署鎖與鎖內預覽，
  留存可讀的custom-format備份後套用4新店／4風格；重播預覽0／0。來源皆為店家官方頁。
  店家皆pending/inactive/unverified，地圖／座標／商圈留空，風格pending且無審核人；系統稽核恰為2筆。
  備份7,092,975 bytes、權限600，JSON SHA-256為
  `58fe1bd9cc60cc351d40f1a3b1f0ede8697085352b9b9d2ad4c42ec2026c17db`。
  六批合計33家新候選、2家既有補風格，共36個pending標籤（網美17／文青19）。
  公開風格查詢前後完全一致、仍為0，readiness正常、foods頁HTTP 200。未重建服務、執行遷移、核准風格或發布店家。
