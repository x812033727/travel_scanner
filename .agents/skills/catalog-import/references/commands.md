# 子指令一覽

以 `apps/api/app/cli.py` 的 `argparse` 與各 `*_cli` 模組為準（2026-09-25 核對）。`--destination` 都是 destination id（`tokyo`、`seoul`），可重複；`--limit` 都是「處理到第 N 筆就停」。

**寫入旗標是哪一種**：不帶 `--apply` 只報告的是預設；**反過來預設就寫、要自己加 `--dry-run` 的**是 `seed-foods`（沒有 dry-run）、`collect-hotspots`（沒有）、`backfill-trip-item-names`、`guides-search-reindex`、`guides-aliases-seed`、`guides-links-rebuild`、`fill-hotspot-labels`、`match-hotspot-places`、`guides-import`、`python -m app.hotspots.themes`（沒有）。

「跑哪裡」：主機＝要後台資料庫裡的金鑰或正式資料；本機＝改 repo 裡的檔案、結果走 PR。

## 店家與訂位（foods）

| 子指令 | 做什麼 | 寫入 | 跑哪裡／檔案 |
| --- | --- | --- | --- |
| `seed-foods` | upsert 精選菜色、店家、商圈、分類，印計數；只補空、不改管理員設過的；平台列只建不改 | 直接寫 | 主機；部署帶來分類資料後跑一次 |
| `import-trend-merchants [--file F] [--limit N] [--apply]` | JSON 清單建 pending 店家（一個來源、至多 3 分類、`area_source=admin`） | `--apply` | 預設檔 `app/foods/data/trend_merchants.json`；風格店家批次是 `app/foods/data/style_merchants_2026_09*.json`（`docs/merchant-styles.md`） |
| `fill-food-merchant-coordinates [--destination D] [--limit N] [--apply]` | 讀店家自己的 `merchant_website`／`merchant_listing` 來源頁的 JSON-LD 與 geo meta，存耐久座標；不讀內嵌 Google 地圖；多地點頁名稱對不上報 `ambiguous` | `--apply` | 主機（抓外部網頁；只收 https、擋私有位址） |
| `match-food-merchant-places [--destination D] [--limit N] [--apply]` | 對沒有 Place ID 的店家做 Text Search，只寫 `google_place_id`；KR 跳過 | `--apply` | 主機；每筆一次 Text Search Pro |
| `enrich-food-merchants --actor-email A [--destination D] [--limit N] [--max-calls N] [--no-identify] [--dry-run] [--idempotency-key K]` | 在容器內直接跑 catalog review 的 `enrich_merchants` 模式：Place ID → Gemini 找官網／觀光局頁／地址／商圈／分類，產出待後台套用的修正 | 建 run；修正仍要在後台 `/admin/catalog-review` 套用 | 主機；`--dry-run` 只列待補清單；同一天同參數重跑會接續同一個 run |
| `export-food-merchant-worklist [--status pending\|approved\|all] [--destination D] [--include-researched] [--out P]` | 印要研究的店家 JSON，含該城市商圈與啟用分類；已被 committed 補資料檔結案的預設略過 | 唯讀 | 主機；直接讀 stdout（`--out` 寫在容器裡） |
| `apply-food-merchant-enrichment [--file F] [--slug S] [--limit N] [--check] [--apply]` | 套用研究檔：只填空的地址／官網／商圈／Place ID，來源以網址 upsert，分類只增 | `--apply`；`--check` 不開資料庫 | `--check` 本機；套用在主機，未部署用 `--file /dev/stdin` |
| `apply-food-platform-reviews [--file F] [--limit N] [--apply]` | 套用訂位平台審查檔；不覆寫有審核者的列（除非帶一致的 `expected_checked_at`） | `--apply` | 主機；逐筆結果在 stderr |
| `backfill-merchant-english-names [--apply] [--reset-drifted]` | 讓已匯入的潮流店家拿到 `trend_merchants.json` 後來補的英文名 | `--apply` | 主機；`--reset-drifted` 分不出管理員改名，先讀 dry-run |

## 景點（hotspots）

| 子指令 | 做什麼 | 寫入 | 跑哪裡／檔案 |
| --- | --- | --- | --- |
| `collect-hotspots` | 手動跑一輪 hotspot collector（種子、Wikimedia 瀏覽量、排行快照） | 直接寫 | 主機；平常由 `hotspots` profile 的 collector 每 6 小時跑 |
| `generate-hotspot-candidates --city C [--count N] [--out P] [--model M] [--avoid F]... [--dry-run] [--force]` | 請 Gemini 列一個城市的景點名，寫候選 JSON | 寫檔（非資料庫） | 主機要 `--dry-run`，從輸出取 `document`；預設檔 `candidates/<CODE>.json` 在容器裡會消失；上限 150 |
| `import-hotspot-candidates --file F [--limit N] [--apply]` | Google 身分 × 1 km 內維基條目 × Wikidata 名稱與類型三方對上才建列；座標取自維基 | `--apply` | 主機；`--file /dev/stdin`；每筆一次 Text Search Pro |
| `match-hotspot-places [--destination D] [--slug-prefix P] [--limit N] [--dry-run] [--approve SLUG]...` | 替公開景點補 Place ID；`--approve` 把存著的候選升為正式 | 直接寫（`--dry-run` 不打 Google） | 主機；屬 skill `hotspot-review` |
| `fill-hotspot-labels [--file NAME]... [--overwrite-original] [--dry-run]` | 從 Wikidata 補 bootstrap 檔的原文名與各語系名 | 改 repo 檔 | 本機（要網路），看 diff 後 PR |
| `fill-simplified-names [--provider P] [--source seeds\|areas] [--max-output-tokens N] [--from-mapping F] [--apply]` | 由繁體名轉 zh-CN，逐字核對不是純轉換的丟掉 | `--apply` 改 bootstrap 檔 | 主機產 mapping、本機 `--from-mapping` 套用；`areas` 只產 mapping，手寫進 `areas.py` |
| `jev-shadow-report [--limit N] [--examples N]` | 讀 Jev shadow 的一致率（分語言）與分歧清單 | 唯讀 | 主機 |

## 文章（guides）

| 子指令 | 做什麼 | 寫入 | 跑哪裡 |
| --- | --- | --- | --- |
| `guides-import …` | 匯入／發布內容包 | — | skill `content-pipeline`，這裡不講 |
| `guides-search-reindex [--dry-run]` | 從已發布版本重建搜尋索引 | 直接寫 | 主機；migration 0077 後、繞過後台寫入路徑的大量發布後 |
| `guides-aliases-seed [--terms-file F] [--keywords-file F] [--dry-run]` | 從 AI 名詞別名與系列目錄補別名，只加不改 | 直接寫 | 主機；容器沒有 `docs/`，不帶檔只會種系列關鍵字，要別名表就把檔先放進容器 `/tmp` |
| `guides-links-rebuild [--dry-run]` | 從已發布版本重建文章連結圖 | 直接寫 | 主機；migration 0078 後、大量發布後 |
| `guides-links-check [--locale L]` | 列出指向不存在、類型錯、未發布、隱藏、過期文章的內文連結與裸網址 | 唯讀；有發現 exit 1 | 主機 |
| `review-pending-guides [--provider P] [--locale L]... [--limit N] [--min-relevance 60] [--min-quality 40] [--max-calls 200] [--batch-size 20] [--max-output-tokens N] [--apply] [--verbose]` | 用 AI 評分景點攻略待審佇列並記 approve／reject；先過 `foreign_place` | `--apply` | 主機；一次 AI 呼叫 20 筆 |
| `guides-foreign-place-scan [--locale L]... [--status S]... [--limit N] [--skip-id ID]... [--skip-ids-file F] [--reject-id ID]... [--reject-ids-file F] [--apply --actor-email A] [--verbose]` | 找已核准、標題摘要講別國而沒講本景點的攻略；`--apply` 駁回並寫稽核 | `--apply`（要 `--actor-email`） | 主機；skip／reject 名單要帶著走 |

## 帳號、驗證與其他

| 子指令 | 做什麼 | 備註 |
| --- | --- | --- |
| `set-admin --email E [--revoke]` | 授予或撤銷舊式管理員（對應 support、content、operations 能力；不含部署與資料庫） | `--revoke` 只撤這一個舊授權 |
| `create-admin --email E [--password-stdin]` | 不經公開註冊建立管理員 | `ADMIN_EMAILS` 等清單上的地址不能自助註冊，要用這個 |
| `add-usage-package --email E --package CODE --reference R` | 手動發用量包 | `TRIAL_3` 不能用 |
| `verify-airline-crawlers`、`verify-live-provider [--origin TPE] [--destination NRT] [--strict]`、`verify-naver-maps [--strict]` | 對外部來源做一次連線驗證 | `--strict` 失敗時 exit 1 |
| `backfill-trip-item-names [--dry-run]` | migration 0039 前存的行程項目補五語系名，旅客改過的不動 | 預設就寫 |

## 不在 app.cli 的入口

| 入口 | 做什麼 | 讀 |
| --- | --- | --- |
| `python -m app.hotspots.themes` | 不等 collector，單次同步主題種子 | `docs/hotspot-themes.md` |
| `python -m app.travel_services.klook_catalog --manifest P [--apply]` | Klook 商品只增、待審匯入 | `docs/klook-integration.md` |
| `python -m app.news_automation.sources_cli [--file F] [--apply --actor-email A]`、`python -m app.news_automation.settings_cli …` | 新聞來源載入、自動新聞開關 | `docs/news-automation.md` |
| `python -m app.guides.pack_cli …` | 內容包 ingest | skill `content-pipeline` |

## 公開閘門（店家）

後台核准（`/admin/foods` 的核准、`verify_activate`）會檢查：`map_match_status=verified`；精準地圖身分（KR 是 Naver 精準頁 `naver_map_url`，其他國家是 Google Place ID）；成對的 WGS84 座標；`coordinate_source_type` 屬耐久來源且 `coordinate_source_url` 是 https；至少一個分類。缺一個就是 422（`exact_map_identity_required`、`permanent_coordinates_required`、`coordinate_source_required`、`map_verification_required`）。Google 的座標不是耐久來源。

## 報告裡的動作名

| 指令 | 會看到 |
| --- | --- |
| `import-trend-merchants` | `would_create`／`created`、`skipped_existing_slug`、`skipped_same_name` |
| `apply-food-merchant-enrichment` | `would_enrich`／`would_note`、`unchanged`、`already_noted`、`skipped_missing_merchant`、`skipped_slug_mismatch`、`skipped_conflict`、`skipped_taxonomy`、`skipped_not_enrichable` |
| `apply-food-platform-reviews` | `would_create`／`would_update`、`created`／`updated`、`unchanged`、`skipped_admin_reviewed`、`skipped_changed_since_research`、`skipped_branch_conflict`、`skipped_missing_merchant`、`skipped_slug_mismatch` |
| `fill-food-merchant-coordinates` | `would_fill`、`already_filled`、`ambiguous` 等 |
| `match-food-merchant-places` | `would_match`、`already_matched` 等 |
