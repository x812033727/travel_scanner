---
name: catchtable-discovery
description: 用 CatchTable 的排行榜反推新的韓國美食店家並補上訂位連結：抄榜單、對正式站目錄去重、逐店查證店頁與官方來源、轉成既有匯入指令的檔案、部署後套用，再在後台補座標、Naver 精準頁與核准。要開新一批（首爾、釜山、濟州、大邱的最佳餐廳榜或候位榜）、接手別人的批次、把候選檔轉成匯入檔、在正式站套用店家與平台列、或處理「建成 pending 之後怎麼公開」時，先讀這個 skill。Turn CatchTable rankings into new Korean food merchants and reservation links for travel_scanner. Covers capturing a ranking page, dedup against the production catalog, per-shop verification of the shop page and an official source, converting the candidate file into the files the existing importers accept, applying them on the host after a deploy, and the admin steps that make a Korean merchant public. Use it to start or take over a batch, convert or apply a batch, or publish pending merchants. Not for writing articles (content-pipeline) and not for the deploy itself (deploy).
metadata:
  short-description: CatchTable 榜單反推店家：收集、查證、匯入、公開
---

# CatchTable 榜單反推店家（catchtable-discovery）

規則與邊界的全文在 `docs/catchtable-ranking-discovery.md`（平台只當發現、名次不落地、批次不寫座標與地圖身分、來源要講這家分店），
候選檔的欄位在 `apps/api/app/foods/data/catchtable/README.md`，第一批的做法與數字在 `docs/catalog-content-reviews/catchtable-seoul-batch-1.md`。
這個 skill 只放指令、關卡、去哪裡讀；`<PY>` 是 repo 的 venv python（從 `apps/api` 跑）、`<BATCH>` 是 `app/foods/data/catchtable/<batch-id>`、
`<SSH>` 是你自己開到主機 root shell 的前綴。

## 不變的規矩

1. **CatchTable、Naver、Google、Instagram 只當發現與定位，永不當來源；名次只留在候選檔。** 進目錄要有官方頁（觀光局／政府／店家官網）講這家分店。
2. **只有渲染後看到店家自己的訂位控制項才算可訂位**（`service-tab-DINING` 點開有日期選擇），候位、優先入場都存 `disabled`。
3. **兩個瀏覽器都開不了 Naver**（Anthropic 端安全政策，內建瀏覽器與 Chrome 同樣拒絕），不繞道 curl；Naver 精準頁由站主在自己的 Naver 地圖依地址挑選、
   貼短網址，session 只讀 `naver.me` 的轉址標頭取 id。經營者官網自己放的 Naver 短網址可以直接用。
4. **座標只用耐久來源**：官方頁 JSON-LD 的 `GeoCoordinates`（`official_tourism`）或 OpenStreetMap 上店家或同門牌建物的節點（`admin_verified`，來源網址是節點永久連結）。
   座標佇列自 2026-09-19 起不寫座標，Google 候選只作比對。
5. **正式站每一步先 dry-run、站主在對話裡同意後才 `--apply`；後台的連續寫入與核准在 auto 模式會被分類器擋**，用有選項的提問列出動作，站主同意後同一動作放行，
   或先切 Manual。被擋不要換寫法重試。
6. 抓官方頁用固定 UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，任何請求不帶任何人的個資。

## 主幹

| # | 階段 | 做什麼 | 關卡 |
| --- | --- | --- | --- |
| 0 | 開票 | `npm run tasks -- new … --scope apps/api/app/foods/data/catchtable,docs/catalog-content-reviews/<report>.md,docs/catchtable-ranking-discovery.md`，claim，建 `<BATCH>/` | 站主點頭範圍（哪個榜、哪個城市、第幾名到第幾名） |
| 1 | 收集 | 內建瀏覽器開榜頁，照 `.agents/skills/catchtable-discovery/references/browser.md` 的累積片段用滾輪逐步捲、名次讀徽章，存 `rankings.json` | 名次連續無缺、`conflicts` 為空 |
| 2 | 去重 | 主機匯出 worklist（下方指令）＋ repo 內 `apps/api/app/foods/data/platform_reviews/*.json` 的 CatchTable alias；疑似同店列給人判 | 每個 alias 標 `new` 或 `duplicate_of` |
| 3 | 逐店查證 | 研究代理各一個分頁、各 10 家：店頁（身分、hreflang、訂位判定）→ `/info` 分頁（韓文地址、網站）→ 官方來源；每家寫完就存分片檔；另一個代理抽三分之一複核 | 每筆 `import` 有 https 官方來源與逐字引文；訂位判定有「區塊本體」證據 |
| 4 | 轉檔 | `catchtable_build_batches.py --check` → `--merchants-out`；本機用 `load_trend_merchants` 再驗 | 零錯誤 |
| 5 | PR 一 | 候選檔、`merchants.json`、報告初稿、票的 Notes；`merge-when-green` | CI 綠 |
| 6 | 正式站 | 部署（skill `deploy`）→ 店家 dry-run 對報告 → `--apply` → 再匯出 worklist → `--platform-out` → 平台列以 stdin 餵入 dry-run → `--apply` | 再跑一次分別是 `skipped_existing_slug`／`unchanged` |
| 7 | 公開 | 後台逐家：座標 → Naver 精準頁（站主貼）→ 一次儲存「已驗證＋核准＋啟用」→ 公開 API 驗證；細節在 `.agents/skills/catchtable-discovery/references/admin.md` | 公開 API 家數與按鈕數對得上報告 |
| 8 | 收尾 | PR 二（平台列檔、報告數字、`done`）；報告寫三個比例（有官方來源、能訂位、與目錄重複）與未公開的原因 | 票在 done、數字在報告 |

## 指令

```bash
# 去重快照（主機；不帶 --out，直接讀 stdout；--out 會落在容器裡的 /tmp）
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  export-food-merchant-worklist --status all --destination seoul --destination busan --include-researched" > worklist.json

# 候選檔檢查與轉檔（任何機器，只用標準函式庫）
<PY> ../../tools/catchtable_build_batches.py --candidates <BATCH>/candidates.json --check
<PY> ../../tools/catchtable_build_batches.py --candidates <BATCH>/candidates.json --merchants-out <BATCH>/merchants.json
<PY> -c "from pathlib import Path; from app.foods.trend_import import load_trend_merchants; print(len(load_trend_merchants(Path('<BATCH>/merchants.json'))))"

# 正式站店家：部署前可先從 stdin 餵檔做唯讀 dry-run；部署後用主機上的檔案 dry-run，一致再 --apply
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.cli import-trend-merchants --file /dev/stdin" < <BATCH>/merchants.json
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.cli import-trend-merchants --file <BATCH>/merchants.json [--apply]"

# 平台列：套用後的 worklist 補 merchant_id，檔案不必部署，從 stdin 餵入
<PY> ../../tools/catchtable_build_batches.py --candidates <BATCH>/candidates.json --worklist worklist-after.json --platform-out <BATCH>/platform-reviews.json
<PY> -c "from pathlib import Path; from app.foods.platform_review_import import load_review_file; print(len(load_review_file(Path('<BATCH>/platform-reviews.json')).records))"
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews --file /dev/stdin [--apply]" < <BATCH>/platform-reviews.json

# 公開 API 驗證（X-Travel-Locale 只吃 en/ja/ko/zh-TW/zh-CN；limit 上限低於 100）
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=seoul&limit=50" | python -m json.tool | grep -c catchtable_global
```

## 會踩到的點

- 榜頁是虛擬化清單：捲到底再抓會漏掉榜首；`scrollTo` 跳著捲會撞到回收卡片；候位榜第 1–4 名首次渲染沒有 `href`。
- 店頁服務區塊是 lazy section，**面板隱藏或分頁在背景時永遠不掛載**，看到的「只有候位鈕」不算證據；正面證據可信、缺席不可信。做法在 references/browser.md。
- `naver.me` 短網址後台會退 422，要先解成 `https://map.naver.com/p/entry/place/<id>`；同一個 Naver id 不能給兩家店（園區內的第二間餐飲要有自己的條目）。
- 來源網址只收 https（只有 http 的官網不算）；`notes` 1000 字、`quote` 300 字、分類至多 3 個，轉檔腳本會擋。
- 匯入器的第二把去重鑰匙是 `(destination, local_name)`：分店名要寫進 `local_name`。
- 轉檔腳本一個候選檔只吃一個 `destination`：一批跨兩個城市就寫 `candidates-<destination>.json` 各一份、轉檔與匯入各跑一次（佈局在 `apps/api/app/foods/data/catchtable/README.md`）。
- 後台編輯器是 React 表單：文字欄用原生 value setter 加 `input`／`change` 事件、勾選框真點；關舊視窗與開新視窗之間等一秒。

## 這個 skill 的檔案

- `.agents/skills/catchtable-discovery/references/browser.md`：榜頁累積片段、店頁訂位判定片段（含 IntersectionObserver 包裝）、`/info` 分頁片段、代理提示要帶的規則。
- `.agents/skills/catchtable-discovery/references/admin.md`：後台欄位、每家的儲存順序、座標來源怎麼找、Naver 分工、驗證與分類器的處置。
- `.claude/skills/catchtable-discovery/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
