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
