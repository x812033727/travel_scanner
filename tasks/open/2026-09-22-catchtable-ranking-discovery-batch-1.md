---
id: 2026-09-22-catchtable-ranking-discovery-batch-1
title: CatchTable 排行榜反推首爾新店家：第一批（本機瀏覽器路線，沿用現有匯入指令）
status: review
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-23T00:05:44Z
created_at: 2026-09-22T15:26:39Z
completed_at:
branch: claude/catchtable-ranking-discovery-batch-1-b4bef6
depends_on: []
scope:
  - apps/api/app/foods/data/catchtable
  - docs/catalog-content-reviews/catchtable-seoul-batch-1.md
  - docs/catchtable-ranking-discovery.md
  - tools/catchtable_build_batches.py
---

# CatchTable 排行榜反推首爾新店家：第一批（本機瀏覽器路線，沿用現有匯入指令）

## Why

站主 2026-09-22 給了兩個入口：CatchTable 的首爾候位榜
（`https://www.catchtable.net/zh-TW/top-list/waiting/seoul/all`）與全韓最佳餐廳榜
（`https://www.catchtable.net/zh-TW/ranking/location/location-all`），要「反推新增餐廳，並補足
訂位連結、菜單連結等資訊」。目前的方向是反的：2026-09-11 從目錄往 CatchTable 查，80 家公開韓國
店家只有 7 家能在上面訂位、60 家根本不在上面。榜上的店一定在 CatchTable 上，所以從榜出發，
訂位連結的命中率會高得多；店家本身仍要有官方來源才進目錄。

設計、邊界、操作步驟與站主待決事項都在 `docs/catchtable-ranking-discovery.md`；候選檔欄位在
`apps/api/app/foods/data/catchtable/README.md`。這張票是**第一批**：不改程式，用
`import-trend-merchants --file` 建店家、`apply-food-platform-reviews --file` 建平台列，
量出三個比例（有官方來源、能訂位、與既有目錄重複）再決定下一批怎麼切。

## Definition of done

- [ ] `apps/api/app/foods/data/catchtable/<batch-id>/` 有 `rankings.json`、`candidates.json`、
      `merchants.json`、`platform-reviews.json`，`tools/catchtable_build_batches.py --check` 零錯誤，
      兩個匯入檔各自過 repo 解析器（`load_trend_merchants`、`load_review_file`）。
- [ ] 正式站 dry-run 的 `would_create` 與 `would_create/would_update` 數字和報告一致；站主同意後
      `--apply`，新店家全部是 pending／inactive／unverified，沒有任何既有列的座標、地圖狀態、
      核准狀態被動到。
- [ ] `docs/catalog-content-reviews/catchtable-seoul-batch-1.md` 寫下：看了幾家、幾家 `import`、
      幾家 `duplicate`、幾家 `no_official_source`、幾家可訂位、幾家只能候位、幾家等站主貼 Naver。
- [ ] 大林倉庫餐酒館（`daelimchanggobar`，票 `2026-09-21-catchtable-apply-and-daerim` 的 A 項）
      是這批的第一筆候選，建成獨立店家（與 `seoul-daerimcanggo` 分開）。
- [ ] 設計文件的「漏斗」一節補上量到的三個比例，並寫下要不要跑第二批、要不要升成 skill。

## Steps

- [x] 和站主定範圍。站主 2026-09-22 定：最佳餐廳榜的首爾區前 20 家加候位榜前 10 家。
- [x] 本機瀏覽器：兩個榜頁各跑一次設計文件「本機瀏覽器」一節的片段，對過家數與名次，存 `rankings.json`（2026-09-23，見 Notes：清單是虛擬化的，片段改成邊捲邊累積）。
- [x] 主機匯出 `export-food-merchant-worklist --status all --destination seoul`，加 repo 內
      `apps/api/app/foods/data/platform_reviews/` 三個檔裡的 CatchTable 網址，標每個 alias 是 new 還是 duplicate_of。
- [x] 本機瀏覽器逐店：店頁（韓文名、地址、hreflang、訂位控制項）＋官方來源（VisitSeoul 店家頁、
      VisitKorea、區廳名錄、官網），照資料目錄 README 填 `candidates.json`，每家寫完就存。
- [ ] 換人抽三分之一的 `import` 重開店頁與官方頁。
- [ ] `catchtable_build_batches.py --merchants-out`；本機用 `load_trend_merchants` 再驗；PR 一（候選檔、merchants.json、報告初稿）。
- [ ] 合併部署後主機 dry-run → 站主同意 → `import-trend-merchants --file … --apply`。
- [ ] 主機再匯出 worklist（拿新 merchant_id）→ `catchtable_build_batches.py --worklist … --platform-out`；本機用
      `load_review_file` 再驗；PR 二（platform-reviews.json、報告補數字）。
- [ ] 主機 dry-run → 站主同意 → `apply-food-platform-reviews --file … --apply`；`skipped_admin_reviewed`
      的列記進報告交後台。
- [ ] 報告補前後計數；把「等 Naver」的清單交給站主；下一批的切法寫進 Notes；`release` 或 `done`。

## How to verify

```bash
# 本機（repo 的 venv python，從 apps/api 跑）
python ../../tools/catchtable_build_batches.py --candidates app/foods/data/catchtable/<batch-id>/candidates.json --check
python -c "from pathlib import Path; from app.foods.trend_import import load_trend_merchants; print(len(load_trend_merchants(Path('app/foods/data/catchtable/<batch-id>/merchants.json'))))"
python -c "from pathlib import Path; from app.foods.platform_review_import import load_review_file; print(len(load_review_file(Path('app/foods/data/catchtable/<batch-id>/platform-reviews.json')).records))"
npm run check:tasks
```

```bash
# 主機（先 dry-run，站主同意後才加 --apply）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli import-trend-merchants --file app/foods/data/catchtable/<batch-id>/merchants.json
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews --file app/foods/data/catchtable/<batch-id>/platform-reviews.json
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli export-food-merchant-worklist --status pending --destination seoul --out /tmp/seoul-pending.json
```

pending 店家不出現在公開 API；公開的訂位按鈕要等站主貼 Naver 精準頁並核准後才會出現。

## Notes

- 2026-09-23 第一批實作（claude-fable-5-1，本機 Claude Code，內建瀏覽器）。範圍：最佳榜首爾區 1–20 ＋ 候位榜 1–10，兩榜無重複，共 30 家。
  結果：`import` 14、`duplicate` 1（`buchonyukhoe` → 目錄裡 rejected 的 `seoul-buchon-yukhoe`）、`no_official_source` 15；
  訂位判定 30 家裡 `reservation` 22、`waiting_only` 8（最終版：全部 30 家在同一分頁用 IntersectionObserver 包裝讓 lazy 區塊掛載後重看，見報告「陷阱」）。
  主機 `import-trend-merchants --file /dev/stdin` 唯讀 dry-run：`would_create 14`、0 skipped（stdin 餵法可用，省一次部署）。
- **榜頁是虛擬化清單**：捲到底再抓會漏掉榜首；`scrollTo` 跳著捲會撞到「徽章更新了、內容還是舊的」的回收卡片。
  只用滾輪逐步捲＋每步累積＋名次讀徽章＋衝突檢查才乾淨；候位榜第 1–4 名首次渲染是沒有 href 的 `<a>`。片段已改進設計文件。
- **店頁服務區塊是 lazy section**：不往下捲就不會渲染，三個研究代理都把它當成「被擋」，四家可訂位的店先被記成 `unclear`、
  一家候位店的判定也差點漏掉分頁；全部 30 家用「每步 500px、最多 14 步、直到區塊出現」重查一次才定案。規則已寫進設計文件。
- `export-food-merchant-worklist --out /tmp/x.json` 的檔案落在 api 容器裡，主機 `cat` 不到；不帶 `--out` 直接讀 stdout，並加 `--include-researched`。
- 來源網址只收 https：`jejuoktop_bbq` 的品牌站只有 http（https 握手失敗），只能記 `no_official_source`。
- 江南區廳的 `visitgangnam.net`、首爾觀光財團的 Taste of Seoul（`*.tasteofseoul.visitseoul.net`）、母公司門市清單（`sgfco.kr`）都當過來源；
  `korean.visitkorea.or.kr` 店家頁的地址是前端動態載入、內建瀏覽器導向會被彈回，本批改用英文站或 KTO 韓文頁的替代網址。

- 2026-09-22 環境實測（claude-fable-5-1）：雲端容器 `curl` 榜頁得到 7,056 bytes 的 SPA 空殼；
  `api.catchtable.net` 的搜尋與店家 API 都是 Cloudflare 403 封鎖頁，帶完整瀏覽器標頭也一樣；
  headless Chromium 開榜頁是 `ERR_CERT_AUTHORITY_INVALID`（代理重簽憑證不在信任庫，規則是不可關驗證）。
  所以第 1、4 步一定在本機做；2026-09-21 的 9 筆就是本機做的，方法在票
  `2026-09-21-catchtable-apply-and-daerim` 的 Notes。
- 2026-09-22 站主原則：省 token 才做 skill、Jev 要真的更好才用。量過後兩者都不做，理由在設計文件
  文末兩節；第一批跑完再看要不要升 skill。
- `import-trend-merchants` 的稽核來源會標 `trend-merchant-sweep`；一次寫入的專用匯入器是
  `2026-09-22-catchtable-one-pass-importer`（P3，等這批證明會再跑）。
- 名次不落地、不公開（同 Google Places 的政策）；只在候選檔與平台列的一筆 evidence 裡當「為什麼看這家」。
- 站主待決（見設計文件）：第一批範圍；Naver 精準頁由後台逐筆貼（建議）還是候選檔帶欄位；
  只有官網來源的店要不要收（建議收）；菜單按鈕不開欄位（建議）。
- `2026-09-12-food-merchant-enrichment` 的 E 是同一條研究路線；這張票不動它的 scope。
- `tools/catchtable_build_batches.py` 已用 3 筆 fixture 驗過：產出通過 `load_trend_merchants` 與
  `load_review_file`；故意弄壞的檔（`ko` 網址、Instagram 當來源、4 個分類、缺 evidence、無時區、
  重複 alias、名次 0）會列出全部錯誤並以非零碼退出。
