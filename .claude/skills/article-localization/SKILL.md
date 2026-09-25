---
name: article-localization
description: 把已經上線的 Mokaair 文章成批補上 en、ja、ko、zh-CN：兩條路線（Codex CLI 驅動的 tools/article-localization 產線加 docs/article-localization 的 baseline、assemble、install、publish_bundle、report_progress；或 Claude 代理翻譯、逐語審稿、直接併入內容包再用 guides-import 發布），含正式站快照與來源雜湊、續跑與失敗處理（STOP 檔、running.lock、額度不重試、reset、materialize）、artifact 綁定、雜湊綁定的獨立審稿、原文修正收據、releases 目錄的發布紀錄，以及 localize 與 release-localized 兩張票怎麼分工。要補語系、接手翻到一半的批次、組或安裝 bundle、發布翻譯、寫發布紀錄、或翻譯時發現原文有錯時，先讀這個 skill。寫新文章走 content-pipeline，部署走 deploy，開票與合併走 task-board。Batch-translate published Mokaair articles into four more locales, review each locale, and release them with hash-bound evidence.
metadata:
  short-description: 既有文章補四語：翻譯、審稿、組包、發布、紀錄
---

# 既有文章補語系（article-localization）

對象是**已經在正式站**的文章（通常只有 zh-TW），要補 en、ja、ko、zh-CN 四語並上線。寫新文章、新聞批次的五語翻譯走 skill `content-pipeline`；部署本身走 skill `deploy`；票與 PR 的循環走 skill `task-board`。規則全文在 `tools/article-localization/README.md`，這裡只放流程、關卡、指令與去哪裡讀。`<ROOT>` 是 repo（或 worktree）根目錄，`<WORK>` 是 repo 外的持久工作目錄，`<SSH>` 是你自己開到主機 root shell 的前綴。`<BASELINE>` 與 `<JOBS>` 是 `pipeline.py` 的預設值：`docs/article-localization/` 底下的 `baseline.json` 與 `work/`。

## 先選路線

| | 路線 A：產線＋bundle | 路線 B：代理＋guides-import |
| --- | --- | --- |
| 誰用過 | Codex，batch007–025（每批一到四篇） | Claude，2026-09-24 desk-cable 一篇 |
| 翻譯 | `pipeline.py` 呼叫 ChatGPT 登入的 Codex CLI | 每語一位翻譯代理，另一位審稿代理只交修正清單 |
| 來源基準 | `export_snapshot.py` 從正式站容器匯出，`build_baseline.py` 釘雜湊 | 公開 API 的 zh-TW 文件正規化後的雜湊 |
| 發布 | `publish_bundle.py` 四個階段＋ durable journal | `app.cli guides-import --slug --locale ... --publish` |
| 限制 | 要把腳本灌進正式站容器；auto 模式分類器會擋 | 沒有 journal，逐語 dry-run 與站主同意就是關卡 |

Claude session 預設走 B；有人已經用 A 開了批次（`<WORK>` 裡有 `receipt.json`、票上寫了 baseline 雜湊）就照 A 接手，不要換路線。

## 不變的規矩

1. **原文一個位元組都不動。** 只加四個 locale；zh-TW 的正規化 `document_hash` 前後相同，寫進票裡當證據。
2. **翻譯前先驗原文。** 翻譯與審稿常挖出原文的事實錯或站內連結連錯（desk-cable 的「標記」連到 AI Token 文章；batch009 被獨立審稿退三次）。先開原文修正、發布、再以新版本為基準翻，或走 `source_correction.py` 收據；不要在譯文裡悄悄修。
3. **審稿者不是翻譯者**，只交修正清單，由第三方套用；審稿要綁到確切的文件與圖檔雜湊。`translated`／`rendered` 狀態不是審稿通過。
4. **額度與登入失敗不自動重試**；要停就建 STOP 檔，不殺行程。刪 `running.lock` 前先確認裡面的 PID 真的不在了。
5. **正式站一律先 dry-run，站主用有選項的提問同意，先 `pg_dump` 再寫。** 只帶自己的 `--slug` 與四個 `--locale`。
6. **工作檔與證據放 repo 外。** `docs/article-localization/` 底下產生的 `work/`、`baseline.json`、`production-baseline.json`、`source-differences.json` 都沒被 git 忽略，別 commit；repo 裡只留 `releases/<batch>/README.md` 與 `evidence.json`，不寫機器路徑、主機 IP、資料庫 ID、actor ID。
7. 譯文太長觸發 `text_length` 警告不刪字；留紀錄就好。

## 主幹

| # | 階段 | 路線 A | 路線 B | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 開票 | `localize-...-batchNNN`，scope 是每篇的內容包與 `apps/web/public/guides/<slug>` | 同左 | claim 成功，沒有別人碰同一批 slug |
| 2 | 釘來源 | 快照→`build_baseline.py`→讀 `source-differences.json` | 抓公開 API，正規化算雜湊 | 正式站與 repo 內容包一致，或差異已說明 |
| 3 | 翻譯 | `pipeline.py prepare`→`run`→`status`，`render.mjs` 每個 job | 每語一位翻譯代理，SVG 自己渲染看過 | 每個 job `rendered`／每語文件過 `GuideDocument` |
| 4 | 審稿 | 獨立審稿寫 `review.json`（綁 artifact manifest） | 每語一位審稿代理→套用→重新渲染 | 修正全套用或有退回理由 |
| 5 | 併入 | `assemble_bundle.py`→記下 manifest SHA→`install_bundle.py` | 只在 zh-TW 之後加四個 locale，SVG 放進 public | zh-TW 雜湊不變 |
| 6 | 檢查、PR | `pack_cli lint`、內容包 pytest、`translation_checks.py`、產線測試 | 同左 | CI 綠（含 `article-localization.yml` 的 release-safety） |
| 7 | 開發布票 | `release-localized-...-batchNNN`，scope 只有 `docs/article-localization/releases/<batch>`，depends_on 翻譯票 | 同左 | 翻譯票 done、開票不認領 |
| 8 | 部署 | skill `deploy`；已有含該 PR 的部署就不必 | 同左 | live HEAD 包含內容 PR |
| 9 | 發布 | 新快照再比一次→`publish_bundle.py` dry-run→drafts→publish-articles→publish-hubs | `guides-import` dry-run→同意→`pg_dump`→`--publish`→links rebuild／check→再 dry-run 全 `unchanged` | journal 無 pending／計畫與實際一致 |
| 10 | 驗證與紀錄 | `report_progress.py`、瀏覽器五語桌面＋手機 | `verify_public.py` 五語 | `releases/<batch>/` 兩個檔，票 done |

## 指令

```bash
# 路線 A：從 <ROOT> 跑（API 的 Python 環境才有 GuideDocument）
uv run --project apps/api python docs/article-localization/build_baseline.py
uv run --project apps/api python tools/article-localization/pipeline.py prepare --batch batch-001 --include-existing
uv run --project apps/api python tools/article-localization/pipeline.py run --batch batch-001 --include-existing --workers 3
uv run --project apps/api python tools/article-localization/pipeline.py status --batch batch-001 --include-existing
node tools/article-localization/render.mjs --job <JOBS>/<slug>/<locale>
uv run --project apps/api python docs/article-localization/assemble_bundle.py --baseline <BASELINE> --work <JOBS> --slug <S1> --slug <S2> --output <WORK>/bundle
uv run --project apps/api python docs/article-localization/install_bundle.py --bundle <WORK>/bundle --baseline <BASELINE> --manifest-sha256 <SHA> --work <JOBS>

# 路線 B：從 <ROOT>/apps/api 跑，<PY> 是 worktree 的 venv python
<PY> -m app.guides.pack_cli lint --kind life
<PY> -m pytest tests/test_guides_content_pack.py -q
PYTHONUTF8=1 <PY> ../../docs/news-2026-batch-4/translation_checks.py <prefix> <slug>
<PY> <ROOT>/.agents/skills/content-pipeline/scripts/verify_public.py --slug <slug> --kind life --locale en --locale ja --locale ko --locale zh-CN --sitemap

# 路線 B 的正式站（主機 /root/travel_scanner，站主同意後）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <slug> --locale en --locale ja --locale ko --locale zh-CN --dry-run
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <slug> --locale en --locale ja --locale ko --locale zh-CN --publish --actor-email <ACTOR_EMAIL>
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-rebuild
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-check --locale en
```

`<ACTOR_EMAIL>` 是容器 `ADMIN_EMAILS` 的第一個。路線 A 發布、續跑、原文修正的完整指令在 `bundle-release.md`。

## 去哪裡讀

| 問題 | 讀 |
| --- | --- |
| 產線的 job 目錄、續跑、STOP、lock、reset、materialize、migrate-prepared、artifact 綁定 | `.agents/skills/article-localization/references/pipeline.md`；全文 `tools/article-localization/README.md` |
| 快照、baseline、assemble、install、publish_bundle 四階段、report_progress、原文修正與保留收據、hub | `.agents/skills/article-localization/references/bundle-release.md` |
| 路線 B 的代理分工、併入內容包、公開 API 的正規化雜湊 | `.agents/skills/article-localization/references/agent-route.md` |
| 兩張票怎麼寫、`releases/<batch>/` 的 README 範本 | `.agents/skills/article-localization/references/tickets-and-records.md` |
| 踩過的坑 | `.agents/skills/article-localization/references/pitfalls.md` |
| 內容包、`guides-import`、`verify_public.py` 的共通規則 | skill `content-pipeline` 的 `publish-runbook.md` |
| 部署、暫停檔、分階段發布 | skill `deploy`、`ops/release/README.md` |

## 這個 skill 的檔案

- `references/`：`pipeline.md`、`bundle-release.md`、`agent-route.md`、`tickets-and-records.md`、`pitfalls.md`。
- `.claude/skills/article-localization/` 是這個目錄的逐字複本，`npm run test:tools` 會比對 SKILL.md。
