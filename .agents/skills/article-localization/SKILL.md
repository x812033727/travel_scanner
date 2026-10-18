---
name: article-localization
description: 把已經上線的 Mokaair 文章成批補上 en、ja、ko、zh-CN：兩條路線（Codex CLI 驅動的 tools/article-localization 產線加 docs/article-localization 的 baseline、assemble、install、publish_bundle、report_progress；或 Claude 代理翻譯、逐語審稿、併入內容包，再用 prepare_route_b_bundle 把審過的一波編成同一種 bundle 交給 publish_bundle），含正式站快照與來源雜湊、續跑與失敗處理（STOP 檔、running.lock、額度不重試、reset、materialize）、artifact 綁定、雜湊綁定的獨立審稿、原文修正收據、releases 目錄的發布紀錄，以及 localize 與 release-localized 兩張票怎麼分工。要補語系、接手翻到一半的批次、組或安裝 bundle、發布翻譯、寫發布紀錄、或翻譯時發現原文有錯時，先讀這個 skill。寫新文章走 content-pipeline，部署走 deploy，開票與合併走 task-board。Batch-translate published Mokaair articles into four more locales, review each locale, and release them with hash-bound evidence.
metadata:
  short-description: 既有文章補四語：翻譯、審稿、組包、發布、紀錄
---

# 既有文章補語系（article-localization）

> 本文提到的 `references/…`、`scripts/…` 都在 `.agents/skills/article-localization/` 底下；`.claude/skills/article-localization/` 只放這份 SKILL.md 的逐字複本。

對象是**已經在正式站**的文章（通常只有 zh-TW），要補 en、ja、ko、zh-CN 四語並上線。寫新文章、新聞批次的五語翻譯走 skill `content-pipeline`；部署本身走 skill `deploy`；票與 PR 的循環走 skill `task-board`。規則全文在 `tools/article-localization/README.md`，這裡只放流程、關卡、指令與去哪裡讀。`<ROOT>` 是 repo（或 worktree）根目錄，`<WORK>` 是 repo 外的持久工作目錄，`<SSH>` 是你自己開到主機 root shell 的前綴。`<BASELINE>` 與 `<JOBS>` 是 `pipeline.py` 的預設值：`docs/article-localization/` 底下的 `baseline.json` 與 `work/`。

## 先選路線

| | 路線 A：產線＋bundle | 路線 B：代理＋內容包＋編譯 |
| --- | --- | --- |
| 誰用過 | Codex，batch007–025（每批一到四篇） | Claude，2026-09-24 desk-cable 一篇（那時還沒有編譯器，用裸 `guides-import` 發布） |
| 翻譯 | `pipeline.py` 呼叫 ChatGPT 登入的 Codex CLI | 每語一位翻譯代理，另一位審稿代理只交修正清單 |
| 來源基準 | `export_snapshot.py` 從正式站容器匯出，`build_baseline.py` 釘雜湊 | 翻譯時：公開 API 的 zh-TW 文件正規化後的雜湊；發布前：同左的快照與 baseline |
| 審稿證據 | 每個 job 的 `review.json`，綁 artifact manifest | 一份 `route-b-review-v1` 收據，逐語綁譯者、審稿者、來源與文件雜湊、圖 |
| 發布 | `assemble_bundle.py`→`publish_bundle.py` 四個階段＋ durable journal | `prepare_route_b_bundle.py` 編成同一種 bundle→同一個 `publish_bundle.py` 四階段＋ journal |
| 限制 | 要把腳本灌進正式站容器；auto 模式分類器會擋 | 翻譯到內容 PR 都不碰正式站；發布前的快照與 publisher 同左，要灌腳本進容器；編譯器 v1 的範圍見下 |

Claude session 預設走 B；有人已經用 A 開了批次（`<WORK>` 裡有 `receipt.json`、票上寫了 baseline 雜湊）就照 A 接手，不要換路線。

路線 B 的編譯器 `docs/article-localization/prepare_route_b_bundle.py`（v1）只做一件事：替**公開、沒過期、不在 `apps/api/app/guides/publish_holds.json`** 的文章，建立 baseline 裡還沒有資料庫列的語系，一波最多 20 篇，內容包要完整五語。下面這些它一律拒絕，選路線時就分出去：

- 改已公開的文字（原文或已上線的譯文）：走 `docs/article-localization/source_correction.py` 與路線 A。
- hub（`gemini-guide`、`claude-code-tutorials`、`ai-terms-index`）：要路線 A 的依賴釘選。
- 來源語系，或 baseline 裡已有資料庫列（草稿或已發布）的語系。
- 內容包替選到的語系設了 `aliases`：publisher 只寫文件，別名不會上線。

裸 `guides-import --publish` 不再是路線 B 的預設，只留給編譯器與路線 A 都不收的情況（例如選到的語系要帶 `aliases` 上線）：發布票先寫明為什麼不走編譯器、站主看過，其餘照舊逐語 dry-run、站主用有選項的提問同意、先 `pg_dump`。它沒有 journal，擋不住 dry-run 與 `--publish` 之間的來源變動。編譯路線第一次寫正式站之前，要先在部署用的 API 映像上隔離排演（票 `2026-10-05-rehearse-a-compiled-route-b-wave`）。

## 不變的規矩

1. **原文一個位元組都不動。** 只加四個 locale；zh-TW 的正規化 `document_hash` 前後相同，寫進票裡當證據。
2. **翻譯前先驗原文。** 翻譯與審稿常挖出原文的事實錯或站內連結連錯（desk-cable 的「標記」連到 AI Token 文章；batch009 被獨立審稿退三次）。先開原文修正、發布、再以新版本為基準翻，或走 `source_correction.py` 收據；不要在譯文裡悄悄修。
3. **審稿者不是翻譯者**，只交修正清單，由第三方套用；審稿要綁到確切的文件與圖檔雜湊。`translated`／`rendered` 狀態不是審稿通過。
4. **額度與登入失敗不自動重試**；要停就建 STOP 檔，不殺行程。刪 `running.lock` 前先確認裡面的 PID 真的不在了。
5. **正式站一律先 dry-run，站主用有選項的提問同意，先 `pg_dump` 再寫。** 只帶自己的 `--slug` 與四個 `--locale`。
6. **工作檔與證據放 repo 外。** `docs/article-localization/` 底下產生的 `work/`、`baseline.json`、`production-baseline.json`、`source-differences.json` 都沒被 git 忽略，別 commit；repo 裡只留 `releases/<batch>/README.md` 與 `evidence.json`，不寫機器路徑、主機 IP、資料庫 ID、actor ID。
7. 譯文太長觸發 `text_length` 警告不刪字；留紀錄就好。

站內連結只機械替換已驗證路由的語系；帶 query 的網址目前只收完整相同的 `/foods?city=hong-kong`，不接受額外或重複參數、改編碼或片段；同站網址含 ASCII 控制字元或前後空白也拒絕。公開路由與篩選證據見 `.agents/skills/article-localization/references/pipeline.md`；發布前仍要重新確認。

## 主幹

| # | 階段 | 路線 A | 路線 B | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 開票 | `localize-...-batchNNN`，scope 是每篇的內容包與 `apps/web/public/guides/<slug>` | 同左 | claim 成功，沒有別人碰同一批 slug |
| 2 | 釘來源 | 快照→`build_baseline.py`→讀 `source-differences.json` | 抓公開 API，正規化算雜湊（收據的 `source_sha256`） | 正式站與 repo 內容包一致，或差異已說明 |
| 3 | 翻譯 | `pipeline.py prepare`→`run`→`status`，`render.mjs` 每個 job | 每語一位翻譯代理，SVG 自己渲染看過 | 每個 job `rendered`／每語文件過 `GuideDocument` |
| 4 | 審稿 | 獨立審稿寫 `review.json`（綁 artifact manifest） | 每語一位審稿代理→套用→重新渲染→寫 `route-b-review-v1` 收據 | 修正全套用或有退回理由；收據每列 `PASS`、`open_findings` 0 |
| 5 | 併入 | `assemble_bundle.py`→記下 manifest SHA→`install_bundle.py` | 只在 zh-TW 之後加四個 locale，SVG 放進 public | zh-TW 雜湊不變 |
| 6 | 檢查、PR | `pack_cli lint`、內容包 pytest、`translation_checks.py`、產線測試 | 同左 | CI 綠（含 `article-localization.yml` 的 release-safety） |
| 7 | 開發布票 | `release-localized-...-batchNNN`，scope 只有 `docs/article-localization/releases/<batch>`，depends_on 翻譯票 | 同左 | 翻譯票 done、開票不認領 |
| 8 | 部署 | skill `deploy`；已有含該 PR 的部署就不必 | 同左 | live HEAD 包含內容 PR |
| 9 | 發布 | 新快照再比一次→`publish_bundle.py` dry-run→drafts→publish-articles→publish-hubs | 從合併提交的 Git blob 凍結 candidate→部署後新快照與 `build_baseline.py`→`prepare_route_b_bundle.py`→審 manifest 與 `route-b-provenance.json`→同意→`pg_dump`→同左的 `publish_bundle.py` 四階段→links rebuild／check | journal 無 pending；重跑什麼都不寫 |
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

# 路線 B 的編譯：從 <ROOT> 跑，不碰正式站。三個輸入的 SHA-256 在檔外算好再傳；<BASELINE> 是內容 PR 部署之後的新快照建的
uv run --project apps/api python docs/article-localization/prepare_route_b_bundle.py --candidate <CANDIDATE>/candidate-manifest.json --candidate-sha256 <CANDIDATE_SHA> --review <WORK>/review.json --review-sha256 <REVIEW_SHA> --baseline <BASELINE> --baseline-sha256 <BASELINE_SHA> --slug <S1> --slug <S2> --locale en --locale ja --locale ko --locale zh-CN --output <WORK>/bundle-<wave>
# 成功印 {"status": "compiled", "manifest_sha256": ...}；拒絕把 {"status": "refused", "reason": ...} 印到 stderr、exit 1、不留 manifest
# 接著在正式站 API 環境跑 publish_bundle.py dry-run→drafts→publish-articles→publish-hubs（站主同意、pg_dump 之後）

# 兩條路線發布之後（主機 /root/travel_scanner，站主同意後）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-rebuild
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-check --locale en

# 裸 guides-import：只在編譯器與路線 A 都不收、站主看過理由之後
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <slug> --locale en --locale ja --locale ko --locale zh-CN --dry-run
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <slug> --locale en --locale ja --locale ko --locale zh-CN --publish --actor-email <ACTOR_EMAIL>
```

`<ACTOR_EMAIL>` 是容器 `ADMIN_EMAILS` 的第一個。`publish_bundle.py` 四階段（兩條路線共用）、續跑、原文修正的完整指令在 `.agents/skills/article-localization/references/bundle-release.md`；路線 B 從編譯到交給 publisher 的步驟在 `.agents/skills/article-localization/references/agent-route.md`；編譯器的輸入格式、輸出與拒絕表在 `docs/article-localization/route-b-bundle.md`。

## 去哪裡讀

| 問題 | 讀 |
| --- | --- |
| 產線的 job 目錄、續跑、STOP、lock、reset、materialize、migrate-prepared、artifact 綁定 | `.agents/skills/article-localization/references/pipeline.md`；全文 `tools/article-localization/README.md` |
| 快照、baseline、assemble、install、publish_bundle 四階段（路線 B 從 §5 接入）、report_progress、原文修正與保留收據、hub | `.agents/skills/article-localization/references/bundle-release.md` |
| 路線 B 的代理分工、公開 API 的正規化雜湊、審稿收據、併入內容包、凍結 candidate、編譯與發布 | `.agents/skills/article-localization/references/agent-route.md` |
| 編譯器的三個輸入 schema、輸出、拒絕表、交給 publisher | `docs/article-localization/route-b-bundle.md`；`docs/article-localization/prepare_route_b_bundle.py` 的 docstring |
| 兩張票怎麼寫、`releases/<batch>/` 的 README 範本 | `.agents/skills/article-localization/references/tickets-and-records.md` |
| 踩過的坑 | `.agents/skills/article-localization/references/pitfalls.md` |
| 內容包、`guides-import`、`verify_public.py` 的共通規則 | skill `content-pipeline` 的 `publish-runbook.md` |
| 部署、暫停檔、分階段發布 | skill `deploy`、`ops/release/README.md` |

## 這個 skill 的檔案

- `references/`：`pipeline.md`、`bundle-release.md`、`agent-route.md`、`tickets-and-records.md`、`pitfalls.md`。
- `.claude/skills/article-localization/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對；`references/` 只在 `.agents/` 這邊。
