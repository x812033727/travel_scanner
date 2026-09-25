# 景點候選、假日、backfill、文章維護

`<SSH>`、`<API>`、`<PY>` 的意思同 SKILL.md。

## 景點候選

設計與三方比對的理由在 `apps/api/app/hotspots/candidates.py` 的模組說明；排行、collector 與來源政策在 `docs/hotspot-intelligence.md`。

1. **產生**（主機，Gemini 金鑰在後台）：`<SSH> "<API> generate-hotspot-candidates --city TNN --count 40 --dry-run" > gen.json`，從輸出的 `document` 存成本機 `candidates/TNN.json`（格式 `{"city_code": "TNN", "candidates": [{"name": "赤崁樓", "district": "中西區"}]}`）。不帶 `--dry-run` 會寫到容器裡的 `candidates/`，下次部署就消失。`--count` 預設是該城市的目標數、上限 150；先 40–50 個，補量時用 `--avoid <舊檔>` 避開重複（`--avoid` 的檔也要在容器裡）。`city_code` 要在 `app/hotspots/cities.py`。
2. **看過名單**：候選名是不可信輸入，先刪掉明顯不是景點的。
3. **匯入 dry-run**：`<SSH> "<API> import-hotspot-candidates --file /dev/stdin" < candidates/TNN.json`。每筆一次 Text Search Pro（這個 SKU 每月有上限，別空跑）。
4. **`--apply`**：三方都對上（Google 身分、1 km 內的維基條目、Wikidata 名稱與 P31 類型）才建列，slug 是 `wikidata-<qid>`、座標取自維基；以前被駁回或停用的 Wikidata 項目回 `skipped:previously_rejected`，已驗證的回 `skipped:already_verified`；Place ID 被別列佔用只報告不寫。
5. 建出的列進審核佇列，後續走 skill `hotspot-review`。

`collect-hotspots` 手動跑一輪 collector（種子、Wikimedia 30 天瀏覽量、排行快照）；正式站平常由 `hotspots` compose profile 的 collector 每 6 小時跑，核准後的排行最多要等一輪。

## 假日（`refresh-holidays`）

資料是 repo 裡 vendored 的 JSON，所以**在本機跑、結果走 PR**。來源、授權與每國的坑在 `docs/public-holidays.md`。

```bash
<PY> -m app.cli refresh-holidays --country jp --year 2027
curl -sS -o <tmp>/tw2027.csv "<data.gov.tw 目錄裡的 resourceDownloadUrl>"
<PY> -m app.cli refresh-holidays --country tw --year 2027 --file <tmp>/tw2027.csv
```

- 不帶 `--apply` 只印差異；`--apply` 寫回並保留手寫的 `names`，新節日沒翻譯會被拒。
- 台灣一定要 `--file`：人事總處的憑證鏈 Python 不收（本機與容器都一樣），curl 可以；下載網址每次從目錄 API 讀，不寫死。編碼要嗅探。
- 韓國沒有機讀來源，手寫，指令會拒絕。
- 時機：政府公布新年度時跑，每年秋天再跑一次抓修訂（台灣曾在年中改過三天）。日本隔年的檔每年 2 月才出。

## Backfill

| 指令 | 什麼時候 | 跑哪裡 |
| --- | --- | --- |
| `backfill-trip-item-names [--dry-run]` | migration 0039 前的行程項目沒有五語系名時；旅客改過名的不動 | 主機，預設就寫 |
| `backfill-merchant-english-names [--apply] [--reset-drifted]` | `trend_merchants.json` 補了 `name_en` 之後；已匯入的列不會自己更新 | 主機；`--reset-drifted` 會把管理員改過的名字也拉回，先讀 dry-run |
| `fill-simplified-names [--source seeds] [--apply]` | 景點種子缺 zh-CN 時 | AI 金鑰在後台，所以主機跑產 mapping（不帶 `--apply`），本機 `--from-mapping <file> --apply` 改 bootstrap 檔、PR；`--source areas` 只產 mapping，手寫進 `app/hotspots/areas.py` |
| `fill-hotspot-labels [--file NAME] [--overwrite-original] [--dry-run]` | 景點 bootstrap 缺原文名或語系名時 | 本機（要連 Wikidata），看 diff 後 PR；`--overwrite-original` 會蓋掉審過的 `local_name` |
| `python -m app.hotspots.themes` | 不等 collector 就同步主題種子 | 主機（`docs/hotspot-themes.md`） |

## 文章維護

內容包的匯入與發布是 skill `content-pipeline` 的事；這裡是索引與圖的維護。規則在 `docs/article-architecture.md`、`docs/travel-guides.md`。

- `guides-search-reindex`：搜尋索引只在發布時寫。migration 0077 後、或任何繞過後台寫入路徑的大量發布後，跑一次（先 `--dry-run`）；不跑搜尋是空的。
- `guides-links-rebuild`：連結圖只在發布時寫。migration 0078 後、大量發布後跑；不跑「引用本文的文章」全空。
- `guides-aliases-seed`：只加不改。容器裡沒有 `docs/`，不帶檔案只會種系列關鍵字；要 AI 名詞別名就先把 `docs/ai-terms-series/aliases.json` 與 `docs/ai-suffix-keywords.md` 送進容器 `/tmp`（`exec -T api sh -c 'cat > /tmp/aliases.json' < …`），再 `--terms-file /tmp/aliases.json --keywords-file /tmp/ai-suffix-keywords.md --dry-run`。
- `guides-links-check [--locale zh-TW]`：列壞連結，有發現 exit 1；暫緩發布的批次會留下已知的發現，對照交接再判斷。

### 景點攻略（hotspot guides）

- `review-pending-guides`：Brave／YouTube 找到的攻略直接進 `pending`，這個指令用設定好的 AI vendor 評分（`--min-relevance 60`、`--min-quality 40`），先過 `foreign_place`（講別國且沒講本景點就駁回）。先不帶 `--apply` 看分佈；`--max-calls`（預設 200）是硬上限，每次呼叫 20 筆。
- `guides-foreign-place-scan`：掃**已核准**的攻略找誤配國家的；`--apply` 要 `--actor-email`，逐筆駁回並寫 `hotspot_guides_reviewed` 稽核。規則會誤判，所以 skip 名單（例：`docs/catalog-content-reviews/2026-09-19-foreign-guides-keep-ids.txt`）與 reject 名單每次都要帶；檔案不在容器裡，用 `--skip-ids-file /dev/stdin` 或先送進 `/tmp`。
- `jev-shadow-report`：唯讀，讀 Jev shadow 的一致率與分歧，改門檻前看。
