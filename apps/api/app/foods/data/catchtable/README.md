# CatchTable 榜單批次：目錄佈局與候選檔欄位

一批一個目錄 `<batch-id>/`，四個檔：

| 檔 | 誰寫 | 用途 |
| --- | --- | --- |
| `rankings.json` | 本機瀏覽器片段 | 榜頁抄下來的 alias 清單，原樣保存，當證據 |
| `candidates.json` | 研究者（人或代理） | 每家店的查證結果；**這是交接檔**，每寫完一家就存 |
| `merchants.json` | `tools/catchtable_build_batches.py` | `import-trend-merchants --file` 的輸入 |
| `platform-reviews.json` | `tools/catchtable_build_batches.py`（要先有 worklist） | `apply-food-platform-reviews --file` 的輸入 |

一批跨兩個目的地時（第二批是首爾第 21–40 名加釜山第 1–20 名），`rankings.json` 仍是一份、兩頁都放進去，其餘三個檔以目的地分開：
`candidates-<destination>.json`、`merchants-<destination>.json`、`platform-reviews-<destination>.json`，各自的 `batch_id` 是
`<batch-id>-<destination>`；轉檔腳本一次只吃一個目的地，兩個目的地各跑一次。

沒有任何程式會自動掃這個目錄；兩支匯入指令都要明確帶 `--file`，而且先 dry-run。設計、邊界與操作
步驟在 `docs/catchtable-ranking-discovery.md`。名次只留在 `candidates.json` 的 `ranking_evidence`，
不落地、不公開。

腳本只擋「會讓整個匯入檔被拒」的錯；真正的規則在 `app/foods/trend_import.py` 與
`app/foods/platform_review_import.py`，兩邊都是一筆壞掉整檔拒收。

## 檔頭

```json
{
  "schema_version": 1,
  "batch_id": "2026-10-catchtable-seoul-1",
  "destination": "seoul",
  "collected_at": "2026-10-01T02:00:00+00:00",
  "researched_by": "本機 Claude Code session（模型名）",
  "method": "本機瀏覽器開榜頁與店頁；官方頁用 curl -sSL 抓；沒有送出任何訂位、沒有登入。",
  "rankings": [
    {
      "page": "https://www.catchtable.net/zh-TW/ranking/location/location-all",
      "captured_at": "2026-10-01T02:00:00+00:00",
      "entries": [
        { "rank": 1, "alias": "koreahouse", "label": "韓國之家 · 韓式料理 · 忠武路" }
      ]
    }
  ],
  "records": []
}
```

- `destination` 是 `app/destinations/catalog.py` 的 id（`seoul`、`busan`、`jeju`、`daegu`、`gyeongju`、
  `jeonju`）；一批一個城市，商圈與 slug 前綴都跟著它。
- 時間一律帶時區（`+00:00` 或 `Z`）。
- `rankings[].entries[].rank` 是**畫面上的名次**；片段抄的是 DOM 順序，要對過眼。

## 一筆 record

```json
{
  "alias": "daelimchanggobar",
  "outcome": "import",
  "checked_at": "2026-10-01T03:12:00+00:00",
  "ranking_evidence": [
    { "page": "https://www.catchtable.net/zh-TW/ranking/location/location-all", "rank": 3, "captured_at": "2026-10-01T02:00:00+00:00" }
  ],
  "catchtable": {
    "listed_name": "대림창고 다이닝 & 바",
    "listed_address": "서울 성동구 성수이로 78",
    "listed_cuisine": "餐酒館",
    "listed_area": "聖水",
    "localized_urls": {
      "zh-TW": "https://www.catchtable.net/zh-TW/shop/daelimchanggobar",
      "zh-CN": "https://www.catchtable.net/zh-CN/shop/daelimchanggobar",
      "ja": "https://www.catchtable.net/ja-JP/shop/daelimchanggobar"
    },
    "booking": "reservation",
    "booking_observation": "2026-10-01 渲染 zh-TW 店頁：有「預訂」與日期、人數選擇，沒有 data-testid dock-waiting-btn。"
  },
  "merchant": {
    "slug": "seoul-daelim-changgo-dining-bar",
    "district_key": null,
    "name_zh": "大林倉庫餐酒館",
    "name_en": "Daelim Changgo Dining & Bar",
    "local_name": "대림창고 다이닝 & 바",
    "address_local": "서울특별시 성동구 성수이로 78",
    "category_slugs": ["izakaya-bar"],
    "source": {
      "url": "https://example-official-site.kr/about",
      "title": "官方頁的真正頁名",
      "kind": "merchant_official",
      "quote": "官方頁上逐字看得到、含店名與地址的一句"
    }
  },
  "notes": "站主 2026-09-21 裁示：與目錄的 seoul-daerimcanggo（同園區藝廊咖啡店）是兩家店，各自獨立。"
}
```

### `outcome`

| 值 | 意思 | 會產出什麼 |
| --- | --- | --- |
| `import` | 不在目錄裡，而且有官方來源 | `merchants.json` 一筆；套用後 `platform-reviews.json` 一筆 |
| `duplicate` | 目錄裡已有這家店（`duplicate_of` 填目錄 slug） | 只產 `platform-reviews.json` 一筆，掛在既有店家上（補訂位連結） |
| `no_official_source` | 店在 CatchTable 上，但找不到官網或觀光局講這家分店的頁 | 什麼都不產；留在候選檔等來源 |
| `not_a_restaurant` | 榜上但不是餐飲店（酒吧以外的場館、快閃、已歇業） | 什麼都不產 |
| `unclear` | 店頁看不到控制項（公休）或身分對不上，改天再開 | 什麼都不產；下一批再看 |

### `catchtable`

- `localized_urls` 抄店頁 `hreflang`：鍵只能是 `zh-TW`、`zh-CN`、`ja`，路徑分別是 `/zh-TW/`、`/zh-CN/`、
  `/ja-JP/`；`booking` 是 `reservation` 時三個都要有。**沒有 `ko`。** 無前綴的網址是 canonical，
  腳本自己生。
- `booking`：`reservation`（有本店的訂位控制項）→ 平台列 `verified`；`waiting_only`（只有
  `dock-waiting-btn`）與 `none`（沒有任何控制項）→ `disabled`；`unclear` 不產列。
- `booking_observation` 要寫日期、開的是哪個語言的店頁、看到哪個控制項、沒看到哪個。它會逐字進
  平台列的 evidence。
- `listed_address` 只用來核對同店與找官方頁，**不會**寫進店家。

### `merchant`（`outcome` 是 `import` 時必填）

| 欄位 | 規則 |
| --- | --- |
| `slug` | 小寫 kebab、以 `<destination>-` 開頭；省略時腳本用 alias 生一個並印出來。曾經撞過的坑：與精選目錄同 slug 但不同店會被匯入器整檔拒收（`trend_import.py` 的 `stolen`），改 slug 就好 |
| `district_key` | 該城市 `app/foods/area_catalog.py` 的 `key`（例：`myeongdong`、`hongdae`、`dongdaemun`、`gangnam`）；對不到就 `null`，匯入器遇到不存在的商圈會整筆跳過 |
| `name_zh` | 官方頁有中文名才用官方的；沒有就寫「韓文店名」本身，不猜漢字 |
| `name_en` | 拉丁字母；沒有就省略 |
| `local_name` | 韓文店名，含分店名（`본점`、`성수점`） |
| `address_local` | 只在來源頁印了地址時填；否則省略 |
| `category_slugs` | 1 到 3 個，`app/foods/category_catalog.py` 的 slug；第一個是主分類 |
| `source.kind` | `merchant_official`（店家自己的站）或 `official_tourism`（觀光局／政府講這家分店的頁）；Instagram、Naver 部落格、CatchTable 本身都不算 |
| `source.quote` | 逐字、看得到、300 字內 |

## 腳本怎麼轉

`merchants.json`（`import-trend-merchants` 的清單格式）每筆：`destination`、`district_key`、`name_zh`、
`name_en`、`local_name`、`address_local`、`category_slugs`、`source_url`、`source_title`、
`source_kind`、`note`（榜名與名次、引文；匯入器不存 note，它只是給人看的）、`confidence`、`slug`。

`platform-reviews.json`（`apply-food-platform-reviews` 的批次格式）每筆：`merchant_id`（從 worklist
以 slug 對到）、`slug`、`name`、`country_code`、`provider: catchtable_global`、`status`、`canonical_url`、
`localized_urls`、`review_note`、`booking_observation`、`evidence`（店頁、日文變體、榜頁各一筆）。
不帶 `expected_checked_at`：新店家的列是新建；`duplicate` 掛到既有店家時，若那一列是管理員在後台
審過的，套用會 `skipped_admin_reviewed`，那一筆改由後台手動處理，報告要記。

worklist 用主機的 `export-food-merchant-worklist --status all --destination <destination> --out …`
匯出；腳本只讀它的 `id` 與 `slug`。
