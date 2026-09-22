---
name: catchtable-discovery
description: 用 CatchTable 的排行榜（候位榜、最佳餐廳榜）反推韓國新店家並補訂位連結：本機瀏覽器收集與逐店查證、對目錄去重、找官方來源、產出 import-trend-merchants 與 apply-food-platform-reviews 的匯入檔、dry-run、PR、正式站套用與交接；第二階段以 Jev 判同店、分類、商圈與本店確認。只要是要從 CatchTable（或其他訂位平台的榜單）找韓國新店家、補韓國店家的 CatchTable 訂位連結、接手這類批次或套用其結果，就先讀這個 skill。Discover new Korean food merchants from CatchTable rankings and fill their reservation links, from browser collection and per-shop verification through dedupe, official-source research, importer files, dry-run, PR and production apply, with Jev decisions in phase two. Not for adding a single reservation link by hand in the admin editor, and not for platforms outside Korea.
metadata:
  short-description: CatchTable 榜單：找韓國新店家、補訂位連結
---

# CatchTable 榜單反推店家（catchtable-discovery）

排行榜只當**發現清單**：每家店仍要找到官方來源才進目錄，訂位連結仍要親眼看到店家自己的
訂位控制項才公開。規則本身在 `docs/catchtable-ranking-discovery.md`；這裡只放指令、關卡、去哪裡讀。
路徑相對於 repo 根目錄，寫成 `<ROOT>`；批次目錄寫成 `<BATCH>`，也就是
`apps/api/app/foods/data/catchtable/<batch-id>/`。

## 什麼時候用、什麼時候不用

- 用：從 CatchTable 榜單開一批韓國新店家；為一批韓國店家補 CatchTable 訂位連結；接手別人做到一半
  的批次；把已合併的批次套上正式站。
- 不用：後台改一家店的訂位連結（直接在 `/admin/foods` 的訂位平台編輯器做）；韓國以外的平台（走
  `docs/catalog-content-reviews/2026-09-13-non-japan-platforms.md` 那一套）。

## 先分清楚在哪裡跑

| 步驟 | 雲端 session | 本機（站主的瀏覽器，或本機的 Claude Code／Codex） |
| --- | --- | --- |
| 開榜頁、開店頁、判斷訂位控制項、找官方頁 | 不行：`api.catchtable.net` 被 Cloudflare 擋，headless Chromium 卡代理憑證 | 可以（2026-09-21 那批就是這樣做的） |
| 去重、轉檔、PR、票、文件 | 可以 | 可以 |
| 正式站 dry-run 與套用 | 站主同意後在主機 | 同左 |

## 不變的規矩（每個代理的提示都要帶）

1. CatchTable、Naver、Google、Instagram 只當發現與定位，**永不當來源**；來源只能是店家官網
   （`merchant_official`）或觀光局／政府講**這家分店**的頁（`official_tourism`）。找不到就
   `no_official_source`，不建店家。
2. 只有渲染後看到店家自己的控制項（「預訂」、日期與人數、「尋找可用時間」）才是可訂位；只有
   `dock-waiting-btn`「登記遠端候位」是候位，存 `disabled`。不整頁搜關鍵字：頁尾「如果您喜歡」
   會列別家店。「今日公休」看不到控制項就改天再開，不硬判。
3. 不逆向 API、不繞過封鎖（Cloudflare、Naver 地圖）、不解驗證碼、不登入、不送任何訂位表單。
4. 名次不寫進資料庫、不公開；只留在候選檔的 `ranking_evidence`。
5. 地址只從官方頁抄；CatchTable 的地址只用來核對「同一家店」。座標、Naver 網址、審核狀態批次一律不寫。
6. 店頁語言網址照 `hreflang`：`/zh-TW/`、`/zh-CN/`、`/ja-JP/`、無前綴。**沒有 `/ko/`，不要生一個。**
7. 漢字店名不猜；官方頁自己寫了中文名才用；英文名要是拉丁字母。
8. 抓官方頁的 UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，
   不帶任何人的 email 或個資；`curl -sSL`，先剝 `<!-- -->` 再讀，200 的殼頁不是來源。
9. 先 `--dry-run` 再寫；動正式站之前要站主明確同意（有選項的提問，不接受一句「好」）。

## 主幹

| # | 階段 | 誰 | 關卡 |
| --- | --- | --- | --- |
| 0 | 認領票（`2026-09-22-catchtable-ranking-discovery-batch-1` 或後續批次票）、和站主定這批的榜、城市、家數；建 `<BATCH>/` | 協調者 | `npm run tasks -- claim` 成功 |
| 1 | 收集：本機開榜頁，貼 `references/collect-in-browser.md` 的片段，存成 `<BATCH>/rankings.json` | 本機 | alias 數與畫面家數一致 |
| 2 | 去重：主機匯出 worklist（`--status all --destination seoul`），加 repo 內既有 platform_reviews 的 CatchTable 網址；每個 alias 標 `new` 或 `duplicate_of` | 協調者 | 疑似同店的列成清單給人判 |
| 3 | 逐店查證：本機開店頁與官方頁，照 `references/candidate-file.md` 填 `<BATCH>/candidates.json`，每寫完一家就存 | 本機 | 每筆 `import` 都有 https 官方來源與逐字引文 |
| 4 | 轉檔：`build_batches.py` 產 `merchants.json`；主機 dry-run；套用後匯出 worklist 拿 merchant_id，再產 `platform-reviews.json` | 協調者 | 腳本零錯誤；dry-run 計畫與報告數字一致 |
| 5 | PR：候選檔、兩個匯入檔、報告（`docs/catalog-content-reviews/` 一篇）、票 | 協調者 | CI 綠、合併 |
| 6 | 正式站：兩支指令各自 dry-run，站主同意後 `--apply` | 站主／協調者 | 計畫與實際一致 |
| 7 | 站主：後台貼 Naver 精準頁、座標佇列、核准 | 站主 | 公開 API 查得到 |
| 8 | 交接：報告補數字（幾家 pending、幾家可訂位、幾家等 Naver、幾家沒來源）、開後續票、`release` 或 `done` | 協調者 | 票更新 |

第一批做到第 6 步就算完成；第 7 步是站主的。

## 指令

主機上的指令都在 `docker compose -f docker-compose.prod.yml exec -T api python -m app.cli …` 後面；
本機檢查用 repo 的 venv python（`<PY>`），從 `<ROOT>/apps/api` 跑。

```bash
# 去重用的目錄快照（主機；含 approved，因為重複最常發生在已公開的店）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  export-food-merchant-worklist --status all --destination seoul --out /tmp/seoul-all.json

# 候選檔檢查與轉檔（任何機器，只用標準函式庫）
<PY> <ROOT>/.agents/skills/catchtable-discovery/scripts/build_batches.py \
  --candidates <BATCH>/candidates.json --merchants-out <BATCH>/merchants.json
# 店家套用後，用 worklist 補 merchant_id，再產平台列
<PY> <ROOT>/.agents/skills/catchtable-discovery/scripts/build_batches.py \
  --candidates <BATCH>/candidates.json --worklist /tmp/seoul-all.json \
  --platform-out <BATCH>/platform-reviews.json

# 本機用 repo 的解析器再驗一次匯入檔（不碰資料庫）
<PY> -c "from pathlib import Path; from app.foods.trend_import import load_trend_merchants; print(len(load_trend_merchants(Path('<BATCH>/merchants.json'))))"
<PY> -c "from pathlib import Path; from app.foods.platform_review_import import load_review_file; print(len(load_review_file(Path('<BATCH>/platform-reviews.json')).records))"

# 正式站：店家（先 dry-run，看 would_create 與 skipped 的理由）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  import-trend-merchants --file app/foods/data/catchtable/<batch-id>/merchants.json
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  import-trend-merchants --file app/foods/data/catchtable/<batch-id>/merchants.json --apply
# 正式站：平台列（同樣先 dry-run）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  apply-food-platform-reviews --file app/foods/data/catchtable/<batch-id>/platform-reviews.json
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  apply-food-platform-reviews --file app/foods/data/catchtable/<batch-id>/platform-reviews.json --apply
```

`import-trend-merchants` 的稽核來源會標成 `trend-merchant-sweep`（它是為潮流街區寫的，檔案格式通用）；
第二階段的專用匯入器落地後改用它。平台列的 `verified` 與 `disabled` 都**強制要有 `evidence`**；
一筆壞掉整個檔案被拒，不是跳過那一筆；管理員在後台審過的列會被跳過，除非帶精確的 `expected_checked_at`。

## 驗證（正式站）

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  export-food-merchant-worklist --status pending --destination seoul --out /tmp/seoul-pending.json
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=seoul&limit=50" \
  | python -m json.tool | grep -A3 catchtable_global
```

`X-Travel-Locale` 只吃 `en / ja / ko / zh-TW / zh-CN`；`limit` 上限低於 100。pending 店家不會出現在
公開 API，看後台或 worklist。

## Jev（第二階段）

四題、state 形狀、門檻與影子量測的做法在 `references/jev-questions.md`。程式落點是票
`2026-09-22-catchtable-import-and-jev`；在它落地前，第一批用人判，並把候選檔保留成之後影子
量測的基準。不要自己寫一個呼叫 Jev 的一次性腳本去改判定：CJK 自動駕駛關著，Jev 現階段只排序與標旗。

## 模型分工

| 角色 | 建議 |
| --- | --- |
| 本機瀏覽器逐店查證 | 一位代理一次 10 家，每家寫完就存候選檔；被切斷時留下的是檔案 |
| 去重、轉檔、PR、票 | 主 session（雲端可） |
| 第二輪抽查 | 換人，抽三分之一的 `import` 重開店頁與官方頁 |

## 規則在哪裡（不重抄）

| 問題 | 讀 |
| --- | --- |
| 設計、邊界、漏斗預期、站主待決事項 | `docs/catchtable-ranking-discovery.md` |
| 候選檔欄位與兩個匯入檔的對應 | `.agents/skills/catchtable-discovery/references/candidate-file.md` |
| 榜頁收集片段、店頁怎麼看、官方來源去哪找 | `.agents/skills/catchtable-discovery/references/collect-in-browser.md` |
| Jev 四題、門檻、影子量測 | `.agents/skills/catchtable-discovery/references/jev-questions.md` |
| 平台網址規則、語言網址 | `apps/api/app/foods/platform_links.py`、`docs/food-reservation-platforms.md` |
| 店家匯入格式與去重規則 | `apps/api/app/foods/trend_import.py` 開頭的 docstring |
| 平台列匯入的保護 | `apps/api/app/foods/platform_review_import.py` 開頭的 docstring |
| 來源等級、店名不猜、韓文一定有中文 | `docs/korea-food-specials/README.md` |
| 2026-09-21 那批的實測筆記 | 票 `2026-09-21-catchtable-apply-and-daerim`、`apps/api/app/foods/data/platform_reviews/2026-09-21-korea-catchtable.json` |
| 票的協定 | `tasks/README.md` |

## 交接

- 候選檔就是交接：每家寫完就存，`outcome` 與 `notes` 要能讓下一個人不重開同一頁。
- 報告放 `docs/catalog-content-reviews/`，寫前後計數；票的 Notes 寫「懷疑但沒動的事」；停手前
  `npm run tasks -- release <id>`。

## 這個 skill 的檔案

- references：`candidate-file.md`、`collect-in-browser.md`、`jev-questions.md`，在
  `.agents/skills/catchtable-discovery/references/`。
- scripts：`build_batches.py`，在 `.agents/skills/catchtable-discovery/scripts/`；只用標準函式庫，
  本機 Windows 也能跑。真正的驗證規則在 `app.foods.trend_import` 與 `app.foods.platform_review_import`，
  腳本只擋掉會讓整個檔案被拒的錯。
- `.claude/skills/catchtable-discovery/SKILL.md` 是這一份的逐字複本：改了這裡就複製過去，
  `npm run test:tools` 會比對。
