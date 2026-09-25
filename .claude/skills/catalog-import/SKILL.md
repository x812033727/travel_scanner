---
name: catalog-import
description: travel_scanner 主機端資料 CLI 的用法，涵蓋 apps/api/app/cli.py 約 30 個子指令與 foods、hotspots、guides、catalog_review 底下的 *_cli：每個子指令做什麼、dry-run 與 --apply、檔案從 stdin 餵還是放容器路徑，以及固定順序——店家（seed-foods → import-trend-merchants → 座標 → Place ID → 補資料 → 後台核准）、景點候選、假日、backfill、文章索引與連結維護、非韓國的訂位平台連結（白名單、分辨本店訂位鈕與鄰店廣告、哪些網域讀得到）。文章包匯入發布（content-pipeline）、CatchTable 批次（catchtable-discovery）、審核佇列與 Place ID（hotspot-review）、部署本身（deploy）不在這裡。要跑 python -m app.cli、匯入或補齊店家與景點、套用訂位平台檔、更新假日、重建文章索引或連結時，先讀這個 skill。Run the host-side data CLIs for merchants, hotspots, holidays, backfills, guide maintenance and reservation-platform links in the right order.
metadata:
  short-description: 主機資料 CLI：店家、景點、假日、backfill、文章維護、訂位連結
---

# 主機端資料 CLI（catalog-import）

> 本文提到的 `references/…`、`scripts/…` 都在 `.agents/skills/catalog-import/` 底下；`.claude/skills/catalog-import/` 只放這份 SKILL.md 的逐字複本。

`python -m app.cli` 有 30 個子指令，另有幾個模組自己帶 `__main__`。這個 skill 只放順序、關卡與去哪裡讀；每個子指令的旗標在 `.agents/skills/catalog-import/references/commands.md`，別再從頭讀 58 KB 的 `apps/api/app/cli.py`。旗標以 `argparse` 為準：懷疑時跑 `python -m app.cli <子指令> --help`。

佔位符：`<SSH>` 是你自己開到主機 root shell 的前綴（連線方式不進 repo，見 skill `deploy`）；`<API>` 是 `cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.cli`；`<PY>` 是從 `apps/api` 跑的 repo python（`uv run python` 或 venv）。

## 不變的規矩

1. **先 dry-run 再寫入。** 多數寫資料庫的指令不帶 `--apply` 只報告；少數是反過來的 `--dry-run`（清單在 commands.md 最上面）。dry-run 的報告給站主看、在對話裡同意後才 `--apply`；分類器擋就停，不換寫法重試（skill `deploy` 的 pitfalls）。
2. **批次永遠不寫座標以外的審核狀態，也不發布。** 匯入的店家一律 `pending`、`is_active=false`、`map_match_status=unverified`；補資料只填空欄位；公開要後台核准，核准要耐久座標加精準地圖身分（commands.md 的「公開閘門」）。
3. **容器裡只有 `apps/api`**（映像的 `/app`）：`docs/`、repo 根目錄的 `candidates/` 都不在，寫到容器 `/tmp` 或 `/app` 的檔案下次部署就沒了。檔案三種給法：已 commit 並部署的用相對路徑 `app/foods/data/...`；沒部署的用 `--file /dev/stdin` 從本機餵（`exec -T` 才接得到 stdin）；要讀多個檔的先 `exec -T api sh -c 'cat > /tmp/x.json' < x.json`。只餵資料檔，不要餵腳本。
4. **金鑰在後台資料庫。** 要打 Google、Gemini、AI vendor 的指令（`match-*-places`、`generate-hotspot-candidates`、`import-hotspot-candidates`、`enrich-food-merchants`、`review-pending-guides`、`fill-simplified-names`）只能在正式站跑；改 repo 檔的指令（`fill-hotspot-labels`、`refresh-holidays`、`fill-simplified-names --from-mapping`）在本機跑、結果走 PR。
5. **帳單。** Place ID 比對與景點候選匯入每筆一次 Google Text Search Pro；`review-pending-guides` 預設 `--max-calls 200`；店家補資料受後台 `catalog_review_max_calls`（預設 80）限制。跑全量前先算筆數。
6. **平台頁只當發現，不當來源。** 食べログ、ぐるなび、ホットペッパー、OpenRice、CatchTable、社群都不能當店家來源（`PLATFORM_HOSTS`）；訂位連結是另一張表，走 `apply-food-platform-reviews`。

## 主幹：店家

| # | 指令 | 做什麼 | 關卡 |
| --- | --- | --- | --- |
| 1 | `seed-foods` | upsert 精選目錄、商圈、分類，印計數；只補空、不動管理員設的 | 部署帶來分類資料後跑一次 |
| 2 | `import-trend-merchants --file …` | JSON 清單建 pending 店家、一個來源、至多 3 分類；slug 或 `(destination, local_name)` 撞到就跳過 | dry-run 的 `would_create` 對得上；重跑全是 `skipped_existing_slug` |
| 3 | `fill-food-merchant-coordinates` | 只讀店家自己引用的官網／觀光局頁的 JSON-LD 與 geo meta，存耐久座標 | 報告的 `ambiguous` 留給人 |
| 4 | `match-food-merchant-places` | 只寫 Google Place ID（KR 跳過） | 分店對不對要人看；佇列與挑選走 skill `hotspot-review` |
| 5 | `enrich-food-merchants` 或 `export-food-merchant-worklist` → 研究 → `apply-food-merchant-enrichment` | 補官網、觀光局頁、地址、商圈、分類 | `--check` 本機驗檔 → 正式站 dry-run → `--apply` → 再 dry-run 只剩 `unchanged`／`already_noted` |
| 6 | `apply-food-platform-reviews --file …` | 訂位平台列；不覆寫管理員審過的列 | 重跑全是 `unchanged` |
| 7 | 後台 `/admin/foods` | 驗證地點＋核准＋啟用 | 公開 API 的家數對得上 |

細節、檔案格式、研究批次的做法在 `.agents/skills/catalog-import/references/merchants.md`；訂位平台在 `.agents/skills/catalog-import/references/reservation-links.md`。

## 其他資料線

| 線 | 順序 | 讀 |
| --- | --- | --- |
| 景點候選 | `generate-hotspot-candidates --city <CODE> --dry-run`（主機，取 `document`）→ 本機存檔 → `import-hotspot-candidates --file /dev/stdin` → `--apply` | `references/other-data.md` |
| 假日 | 本機 `refresh-holidays --country jp --year …`（`tw` 要 `--file` 手動下載的 CSV）→ `--apply` → PR | `references/other-data.md`、`docs/public-holidays.md` |
| backfill | `backfill-trip-item-names`、`backfill-merchant-english-names`、`fill-simplified-names`、`fill-hotspot-labels`，各自 dry-run 先 | `references/other-data.md` |
| 文章維護 | 大量發布或 migration 後 `guides-search-reindex`、`guides-links-rebuild`、`guides-aliases-seed`，再 `guides-links-check`；景點攻略待審 `review-pending-guides`、誤配國家 `guides-foreign-place-scan` | `references/other-data.md` |

## 指令

```bash
# 店家匯入：未部署的檔從 stdin 做 dry-run；已部署的用容器內路徑，一致再 --apply
<SSH> "<API> import-trend-merchants --file /dev/stdin" < apps/api/app/foods/data/trend_merchants.json
<SSH> "<API> import-trend-merchants --file app/foods/data/<batch>.json --apply"
# 座標與 Place ID（都可 --destination 重複、--limit）
<SSH> "<API> fill-food-merchant-coordinates --destination tokyo"
<SSH> "<API> match-food-merchant-places --destination tokyo --limit 20"
# 研究批次：worklist 直接讀 stdout（--out 會落在容器裡）
<SSH> "<API> export-food-merchant-worklist --status pending" > worklist.json
<PY> -m app.cli apply-food-merchant-enrichment --file app/foods/data/enrichment/<file>.json --check
<SSH> "<API> apply-food-merchant-enrichment --file /dev/stdin [--apply --limit 30]" < apps/api/app/foods/data/enrichment/<file>.json
# 訂位平台列
<SSH> "<API> apply-food-platform-reviews --file /dev/stdin [--apply]" < apps/api/app/foods/data/platform_reviews/<file>.json
# 文章維護（都有 --dry-run；links-check 有發現時 exit 1）
<SSH> "<API> guides-search-reindex --dry-run"
<SSH> "<API> guides-links-rebuild && <API> guides-links-check --locale zh-TW"
```

平台列逐筆結果印在 stderr、JSON 摘要在 stdout；要存檔時兩者分開接。

## 不在這個 skill

| 要做的事 | 去哪裡 |
| --- | --- |
| 文章內容包 `guides-import`（含 `--publish`）、`pack_cli` | skill `content-pipeline`（`.agents/skills/content-pipeline/references/publish-runbook.md`） |
| CatchTable 榜單反推韓國店家、`catchtable_build_batches.py` | skill `catchtable-discovery` |
| 景點與店家的審核佇列、Place ID 挑選與核准、`match-hotspot-places --approve` | skill `hotspot-review` |
| 部署、主機預檢、暫停檔 | skill `deploy` |

## 這個 skill 的檔案

- `.agents/skills/catalog-import/references/commands.md`：全部子指令一張表（做什麼、寫不寫、dry-run 旗標、在哪跑、檔案），加上公開閘門與報告裡的動作名。
- `.agents/skills/catalog-import/references/merchants.md`：店家主幹的每一步、匯入與補資料檔的格式、研究批次、核准。
- `.agents/skills/catalog-import/references/reservation-links.md`：平台白名單、各平台「本店真的能訂」的判定、哪些網域讀得到、平台檔格式與套用。
- `.agents/skills/catalog-import/references/other-data.md`：景點候選、假日、backfill、文章維護、其他 `-m` 入口。
- `.claude/skills/catalog-import/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
