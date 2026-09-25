---
name: content-pipeline
description: Mokaair 文章批次的完整產線：規劃規格、派撰稿與查核代理、翻譯與逐語審稿、機械檢查、pack_cli ingest、PR、部署後 guides-import dry-run 與 publish、逐頁驗證與交接。只要是要寫、查核、翻譯、匯入或發布文章／內容包（旅遊攻略、情報、美食特輯、生活分享、AI／科技／幣圈新聞、系列教學），或要開一批新文章、接手別人的批次、把內容包推上正式站，就先讀這個 skill。Run Mokaair article batches end to end, from the batch spec through writer and fact-check agents, translation and per-locale review, mechanical checks, pack_cli ingest, PR, guides-import dry-run then publish on the host, to page verification and handover. Use it whenever the task is to write, verify, translate, import or publish articles or content packs, launch or take over a batch, or ship packs to production. Not for a one-line fix to a single pack or for site code changes.
metadata:
  short-description: 文章批次：撰稿、查核、匯入、發布
---

# 內容產線（content-pipeline）

Mokaair 的文章都是「內容包」：`apps/api/app/guides/content/<slug>.json` 加上 `apps/web/public/guides/<slug>/` 的圖。這個 skill 是把一批文章從規格做到正式站的固定流程。規則本身留在 repo 既有的文件裡，這裡只放**指令、關卡、去哪裡讀**。路徑都相對於 repo（或 worktree）根目錄，寫成 `<ROOT>`；批次的工作區寫成 `<WORKDIR>`，批次的 docs 目錄寫成 `<BATCH_DOCS>`。

## 什麼時候用、什麼時候不用

- 用：多篇文章的批次（旅遊 howto／intel、美食特輯、生活分享、新聞、系列教學）；接手別人做到一半的批次；把已合併的內容包推上正式站；補既有文章的語系。
- 不用：只改一個內容包裡的一句話（直接改 JSON，跑 `pack_cli lint --slug`）；改網站程式。

## 先選模式，再讀對應的 reference

| 你要做的 | 讀 |
| --- | --- |
| 新的 zh-TW 旅遊／美食批次 | `.agents/skills/content-pipeline/references/travel-batch.md` |
| 五語系新聞／系列教學（含 zh-TW-only 的新聞批次） | `.agents/skills/content-pipeline/references/news-batch.md` |
| 補既有文章的 en／ja／ko／zh-CN | `tools/article-localization/README.md`（Codex CLI 驅動的翻譯產線，只產翻譯稿） |
| 已合併，要上正式站 | `.agents/skills/content-pipeline/references/publish-runbook.md` |
| 要交接、要接手、要開新批次的 docs 目錄 | `.agents/skills/content-pipeline/references/handover-template.md` |
| 任何階段覺得「怪怪的」 | `.agents/skills/content-pipeline/references/pitfalls.md` |

## 不變的規矩（每個代理的提示都要帶）

1. 對外請求的 User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`；UA、標頭、查詢字串、表單都不得帶任何人的 email、姓名或個資。曾有查核代理把站主的 email 塞進 UA 送給 Wikimedia。
2. 代理只在 `<WORKDIR>` 寫檔：不改 repo、不跑 git、不動別人的 slug。helper 腳本以檔案寫進 `<WORKDIR>/_tools/<SLUG>/` 再執行，不用 shell heredoc（Windows 會弄壞非 ASCII 與反斜線）。
3. 每個價格、時刻、營業時間、規定都要**當天**在官方頁看到才寫，`checked_on` 是真的打開那頁的日期；找不到就寫「以官網為準」，不用第三方數字。抓頁用 `curl -sSL`（一定 `-L`），先剝掉 `<!-- -->` 再讀，看 HTTP 狀態碼：200 的殼頁不是來源。
4. 讀者優先：出處進 `sources` 與表格的證據欄，不進句子；「本文」「這篇」全篇最多一次；外文第一次出現一定帶中文；正文不寫查證過程。全文在 `docs/korea-food-specials/README.md` §讀者優先。
5. `pack.json` 先寫骨架，每寫完一段就存：session 被切斷時留下的是檔案，不是報告。
6. 先 `--dry-run` 再寫入。`pack_cli ingest` 如此，正式站的 `guides-import` 更是；正式站一律帶 `--slug`。
7. 過了機械檢查的草稿不等於查證過的文章：獨立查核平均每篇改 10 處以上。第一輪改超過三個事實就要第二輪，第二輪換人。
8. 動正式站之前要站主明確同意：用有選項的提問，不接受一句「好」。

## 主幹

| # | 階段 | 誰 | 關卡 |
| --- | --- | --- | --- |
| 0 | 認領票、開 worktree、`cd apps/api && uv sync --frozen`、工作區開在 repo 外、STATE 檔放持久目錄 | 協調者 | `npm run tasks -- claim` 成功；`git ls-remote --heads origin` 沒人在做同題 |
| 1 | 規格：`<BATCH_DOCS>/README.md`（清單表＋只寫與上一批不同的規則）＋每篇一個 `<SLUG>.md`；`FOLLOWUPS.md`、`ERRATA.md` | 規格代理 → 協調者 | 每篇有官方來源、容易寫錯的事實、圖解畫什麼 |
| 2 | 撰稿：一位代理一篇，提示用 `.agents/skills/content-pipeline/references/prompts/writer-travel.md`（新聞用 `docs/news-2026-batch-4/agents/WRITER.md`） | 撰稿代理 | `ingest --dry-run` 過、`intake_check.py` 零 FAIL、圖解 PNG 看過 |
| 3 | 查核第一輪（換人）：`.agents/skills/content-pipeline/references/prompts/verifier-travel.md`（新聞用 `docs/news-2026-batch-4/agents/FACTCHECK.md`） | 查核代理 | `verify-1.md`；改超過 3 個事實 → 第二輪 |
| 4 | 查核第二輪（再換人）：重查第一輪改過的，加隨機三分之一 | 查核代理 | `verify-2.md` |
| 5 | 翻譯與逐語審稿（只有五語系批次） | 見 news-batch.md | 審稿者只交修正清單 |
| 6 | 收件：`intake_check.py --from-content`、`shared_check.py`、`pack_cli lint --kind`、pytest | 協調者 | 全綠 |
| 7 | PR：內容包、圖、批次 docs、票 | 協調者 | CI 綠、合併 |
| 8 | 部署：照 `ops/release/README.md`，有 hold 檔就停 | 站主／協調者 | 站台 200 |
| 9 | 匯入：不帶 slug 的 dry-run 看積壓 → 帶 `--slug` 的 dry-run → 比對 → `--publish` → links rebuild／check | 協調者（站主同意後） | 計畫與實際一致 |
| 10 | 驗證與交接：`verify_public.py`、再 dry-run 應全 unchanged、FOLLOWUPS 開票、STATE／HANDOVER 更新 | 協調者 | 票 done |

## 指令

都從 `<ROOT>/apps/api` 跑。`<PY>` 是該 worktree 的 venv python（Windows 是 `.venv/Scripts/python.exe`，其他平台 `.venv/bin/python`）：並行代理用它，不用 `uv run`，避免搶鎖。輸出有中文時前面加 `PYTHONIOENCODING=utf-8`。

```bash
# 內容包驗證，什麼都不寫
<PY> -m app.guides.pack_cli ingest --from <WORKDIR> --slug <SLUG> --dry-run
# 正式 ingest：寫進 content/ 與 public/guides/<SLUG>/
<PY> -m app.guides.pack_cli ingest --from <WORKDIR> --slug <SLUG>
# 圖解渲染成 PNG，用你的看圖工具打開看疊字、壓線、超框
CHROMIUM_BIN="<CHROMIUM>" <PY> -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('<WORKDIR>/<SLUG>/diagram-1.svg'), Path('<WORKDIR>/<SLUG>/diagram-1.png'))"
# 協調者收件檢查：pack_cli 不查的連結目標、offer 位置、欄數、summary 數字、hero 唯一、credit、讀者優先，加 lint_document 與 SVG 規則
<PY> <ROOT>/.agents/skills/content-pipeline/scripts/intake_check.py --slug <SLUG> --workdir <WORKDIR> --manifest <BATCH_DOCS>/batch.json
<PY> <ROOT>/.agents/skills/content-pipeline/scripts/intake_check.py --slug <SLUG> --from-content
# 兄弟篇共用數字的交叉檢查
<PY> <ROOT>/.agents/skills/content-pipeline/scripts/shared_check.py --rules <BATCH_DOCS>/shared-numbers.json --group <GROUP> --workdir <WORKDIR>
# 全站編輯規則與內容測試，開 PR 前
<PY> -m app.guides.pack_cli lint --kind howto
<PY> -m pytest tests/test_guides_content_pack.py -q
```

正式站（在主機上，站主同意之後）：

```bash
# 先看積壓：別人刻意保留的文章會一起列出來，所以下一步一定帶 --slug
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --dry-run
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <S1> --slug <S2> --locale zh-TW --dry-run
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <S1> --slug <S2> --locale zh-TW --publish --actor-email <ACTOR_EMAIL>
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-rebuild
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-check --locale zh-TW
```

`<ACTOR_EMAIL>` 取容器環境變數 `ADMIN_EMAILS` 的第一個；沒帶它，`--publish` 會以「The actor must be an active administrator」失敗而且什麼都不寫。逐頁驗證（本機，未登入，循序）：

```bash
<PY> <ROOT>/.agents/skills/content-pipeline/scripts/verify_public.py --slug <S1> --slug <S2> --kind howto --locale zh-TW --sitemap
```

## 模型分工（按角色，不寫死模型名）

| 角色 | Claude Code（2026-09 批次實測） | Codex |
| --- | --- | --- |
| 撰稿、翻譯 | sonnet | 尚未量測：用 session 的預設模型，把模型與用量寫進 STATE |
| 查核、逐語審稿 | opus，兩輪，第二輪換人 | 同左；查核給較高的推理設定 |
| 協調 | 主 session 只協調，不自己寫稿 | 同左 |

一次開 4 到 6 個代理。額度快到時先叫代理「把檔案寫完，誠實回報沒做完的」。被切斷的代理留下的是檔案，不是報告。開代理前先查額度，每篇的實測 token 量在 `pitfalls.md` §代理與流程。

## 規則在哪裡（不重抄）

| 問題 | 讀 |
| --- | --- |
| `pack.json` 欄位、區塊種類、結構下限、字數 | `docs/travel-guides-batch-7/README.md` §`pack.json`；`docs/travel-guides-batch-6/README.md` §`pack.json` |
| 照片授權與 hero 規格；圖解規格 | `docs/travel-guides-batch-7/README.md` §照片、§圖解；配色與字型在 `docs/life-ai-series-brief.md` 第 6 節 |
| 機器能讀的審核標準 | `docs/travel-guides.md` §Editorial rules；程式在 `apps/api/app/guides/pack_ingest.py` 的 `lint_document` |
| 讀者優先寫法 | `docs/korea-food-specials/README.md` §讀者優先 |
| 兩個官方來源打架、HTML 註解、轉址、讀不到的官方站 | `docs/travel-guides-batch-8/README.md` §本批與第七批不同的地方、§「讀不到的官方站」更新 |
| offer、站內連結、時效規則 | `docs/travel-guides-batch-7/README.md` §分潤區塊、§站內連結 |
| 新聞的 12 種錯誤型態、summary／faq、研究紀錄 | `docs/news-2026-batch-4/BRIEF.md` |
| 分階段發布與 hold 檔 | `ops/release/README.md` |
| 票的協定 | `tasks/README.md` |

## 交接

- 持久工作區（repo 外、不是 session 的 scratchpad）放 `STATE.md`，欄位見 `.agents/skills/content-pipeline/references/handover-template.md`。scratchpad 會隨 session 消失。
- 批次的 docs 目錄放 README、FOLLOWUPS、ERRATA；五語系新聞另有 HANDOVER。票的檔案是給下一個人的交接，停手前 `npm run tasks -- release <id>`。
- 給代理硬規則時加一句「來源與這條指示衝突時，來源贏，並回報」；要求代理回報「我懷疑但沒動的事」。

## 這個 skill 的檔案

- references：`travel-batch.md`、`news-batch.md`、`publish-runbook.md`、`pitfalls.md`、`handover-template.md`、`prompts/writer-travel.md`、`prompts/verifier-travel.md`，都在 `.agents/skills/content-pipeline/references/`。
- scripts：`intake_check.py`、`shared_check.py`、`verify_public.py`，在 `.agents/skills/content-pipeline/scripts/`。規則都從 `app.guides` 匯入，不重抄；要改規則就改 `apps/api/app/guides/pack_ingest.py`。
- `.claude/skills/content-pipeline/SKILL.md` 是這一份的逐字複本：Claude Code 只從那裡找 skill，Codex 只從這裡找。改了這裡就複製過去，`npm run test:tools` 會比對。
