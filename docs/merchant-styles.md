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

4 家新候選尚缺精準地圖識別、可永久保存的座標及店家發布審核。FAbULOUS 保留原狀態，
以部署時資料重新檢查。未核實商圈不猜測，4 家新店暫留未分區。
未納入：Fika Fika 伊通店官網英文街名與中文不一致，本輪空間風格證據也不足；
ASW 僅找到較舊觀光介紹，不把頁面仍可讀當成近期營業確認。

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

本批未自動匯入正式資料庫、未修改正式站公開狀態、未啟動付費 Gemini／Places 批次。
合併與部署仍待擁有者授權；來源資料已整理不代表正式上架已完成。
