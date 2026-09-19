---
id: 2026-09-15-publish-held-ai-coding-content
title: 批次 04 與 Claude Code 兩系列要一起發：線上 25 個連結指向它們
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-15T12:49:32Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on:
  - 2026-09-14-sitemap-split-before-1000-rows
  - 2026-09-14-claude-advanced-live-validation
scope:
  - docs/content-publication/2026-09-15-held-ai-coding-content.md
---

# 批次 04 與 Claude Code 兩系列要一起發：線上 25 個連結指向它們

## Why

三批已經合併的內容包還沒匯入正式站，而且彼此互連，只能一起發：

- 生活分享批次 04，共 14 篇（`f2567e51` #499、`d28c09a5` #502）
- Claude Code 教學中心，共 61 篇（`35a2d258` #485）
- Claude Code 深入教學，共 36 篇（`3e7f3772` #501）

2026-09-15 以正式站 sitemap 對照 main 的內容包，已上線的頁面有 25 個站內連結指向這三批的文章。讀者點下去會看到 noindex 的「這篇文章目前看不到」。
（計算時已排除 `codex-beginner-guide`：它的內容包被 #525 改過、尚未重新匯入，線上版本和內容包不同。）

- 指向批次 04 的 15 個：
  - `ai-api-pricing-comparison-2026`、`ai-token-cost-estimation`、`local-vs-cloud-ai-cost`、`openrouter-multi-model-api`、`ollama-with-code-editors` → `ai-coding-cost-tokens-explained`
  - `ai-customer-service-line-bot`、`line-ai-features-taiwan`、`n8n-ai-automation-guide` → `ai-build-line-bot-tutorial`
  - `ai-at-work-policy-checklist` → `ai-code-review-safety`
  - `ai-benchmarks-explained`、`ollama-with-code-editors` → `ai-coding-tools-overview-2026`
  - `microsoft-copilot-windows-office`、`ollama-with-code-editors` → `github-copilot-guide`
  - `ollama-with-code-editors` → `cursor-editor-guide`
  - `self-host-ai-on-vps` → `deploy-ai-built-site-to-vps`
- 指向 #485 的 6 個：
  - `ai-agent-frameworks-explained` → `claude-code-agent-sdk`
  - `ai-calendar-scheduling`、`ai-weekly-review-templates` → `claude-code-scheduled-tasks`
  - `ai-second-brain-obsidian` → `claude-code-claude-md-guide` 與 `claude-code-files-and-context`
  - `mcp-servers-for-everyone` → `claude-code-mcp-setup-troubleshooting`
- 指向 #501 的 4 個：
  - `ai-agent-frameworks-explained` → `claude-code-agent-sdk-stateful-runner`
  - `ai-customer-service-line-bot`、`ai-prompt-injection-explained`、`mcp-servers-for-everyone` → `claude-code-mcp-untrusted-output`

三批之間的相依（main 的內容包，zh-TW）：

- 批次 04 每一篇都連到其他尚未發布的文章：
  - 12 篇一般文章連到 #485（例如 `claude-code-getting-started`、`claude-code-ide-integration`），也互相連結。
  - `ai-coding-agents-compared`、`ai-coding-prompt-patterns`、`ai-coding-tools-overview-2026` 另外連到 Codex 的 `codex-cli-getting-started`。
- 批次 04 裡的 `codex-cli-getting-started` 與 `codex-cloud-tasks-github` 被 #525 改過：
  - 多了 en、ja、ko、zh-CN 四個語系。
  - 連進 Codex 學習中心，例如 `codex-learning-hub`、`codex-first-project`。
  - Codex 學習中心的票 `2026-09-14-codex-learning-series` 是 blocked，作者明說還不能發布。
- #485 與 #501 互相大量連結：#485 有 12 個連到 #501，#501 有 85 個連到 #485。
- #501 尚有實測項目未完成（`2026-09-14-claude-advanced-live-validation`：實體手機、遠端 MCP OAuth、付費 Actions 模型；正式站沒有 `ANTHROPIC_API_KEY`）。

sitemap：2026-09-15 發布 317 篇後，線上文章共 925 個 (article, locale) 列，上限是 1,000（`SITEMAP_LIMIT`、`SITEMAP_GUIDE_ENTRY_LIMIT`）。這三批 111 篇再加進來，會變成 1,036 列。

## Definition of done

- [ ] 前置條件都成立：
  - sitemap 已拆成 index（`2026-09-14-sitemap-split-before-1000-rows`）。
  - #501 的實測票已完成，或站主明確接受照目前寫明的限制發布。
- [ ] 批次 04 的 12 篇一般文章、#485 的 61 篇、#501 的 36 篇，已用同一次 `--slug` 限定匯入並發布。
- [ ] `codex-cli-getting-started`、`codex-cloud-tasks-github` 已依站主決定處理（見 Steps）。
- [ ] 發布後，已上線頁面不再有連結指向「這篇文章目前看不到」。唯一例外是站主同意暫留、指向 Codex 學習中心的連結。
- [ ] `docs/content-publication/2026-09-15-held-ai-coding-content.md` 記下 slug 清單、dry-run 與 publish 輸出、驗證結果。

## Steps

- [x] 確認前置條件（兩張相依票的狀態，或站主的書面決定）。2026-09-19 核對：sitemap 票已 done；`2026-09-14-claude-advanced-live-validation` 仍 open（4 項未完成），要站主書面接受——決定欄在 `docs/content-publication/2026-09-15-held-ai-coding-content.md` 第 1 節。
- [x] 三批 slug 清單（14＋61＋36＝111，全部有內容包）、本機 lint／pytest、正式站現況、站內連結重算與主機指令，已寫進上述文件（2026-09-19，claude-fable-5-1）。
- [ ] 請站主決定兩篇 Codex 文章怎麼處理，三個選項：
  - (a) 等 Codex 學習中心一起發。
  - (b) 只發 zh-TW，暫時接受連進學習中心的連結是壞的。
  - (c) 先把這兩篇連進學習中心的連結拿掉再發。
- [ ] 在正式站跑不帶 slug 的 `guides-import --dry-run`，重新確認這三批仍全是 create，也沒有別人的內容混進清單。
- [ ] `--slug` 限定的 `--dry-run --publish`，核對計畫與清單完全一致，再正式 `--publish`。
- [ ] 逐頁驗證並重算站內連結（見 How to verify）。

## How to verify

```bash
# 在主機 /root/travel_scanner（actor 是站主 email）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --locale zh-TW --publish --dry-run --slug <slug> ...   # 應全部 create
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --locale zh-TW --publish --slug <slug> ...
```

- 逐頁檢查，未登入、每個請求間隔 ≥1.3 秒（nginx 每個 IP 限 5 r/s）：
  - `/zh-TW/life/<slug>` 回 200、無 noindex。
  - h1、meta description 與內容包一致，canonical 正確。
  - hero 回 200，而且在 `/sitemap.xml` 裡。
- 重算站內連結：
  - 對照 `/sitemap.xml` 取得已上線的 (locale, kind, slug)。
  - 掃每個已上線內容包的完整站內網址，以及 `{"type":"article"}` 行內引用。
  - 注意：article 行內引用的欄位順序各批不同，要走訪 JSON 結構，不能用正規表示式比對。

## Notes

- 本票的數字來自 2026-09-15 的分析：用 `git archive` 解出 main 的內容包，對照正式站 sitemap。
  - 同一天已發布：#468、#474、#506、#507，以及 #498（排除 `llms-txt-evaluation`，它和 `ai-search-llms-txt` 同題），共 317 篇。
  - 發布前 90 個審查代理比對 317 篇，沒有找到其他重複內容。
  - 那次發布修掉 160 個壞連結，另新增 9 個指向批次 04（已計入上面的 15 個）。
- `taipei-4-day-itinerary` 另有 4 個類別寫錯的連結，由 PR #526 處理，不屬本票。
- 批次 04 的作者當初寫的是「部署後 dry-run、九篇 create、總覽篇 update，再 publish」。之後 #525 改動了其中兩篇，這個步驟已經不能照原樣執行。

### 2026-09-19 準備完成（claude-fable-5-1）

不需要正式站權限的部分都做完，寫在 `docs/content-publication/2026-09-15-held-ai-coding-content.md`；票放回 open，等站主在該文件第 1 節簽兩個決定後，由站主或下一個代理 claim（相依票未完成，要 `--force`）去主機執行第 7 節、回填第 8 節。

- 前置條件：`2026-09-14-sitemap-split-before-1000-rows` 已 done；`2026-09-14-claude-advanced-live-validation` 仍 open，未完成的是第 81 篇遠端 MCP OAuth、第 90 篇真實手機、第 92 篇付費 Actions 模型 job、發布前來源複查——文件第 1 節列給站主決定。`2026-09-14-codex-learning-series` 仍 blocked。
- slug 清單從 repo 重建：批次 04 表 20 篇 − 5 篇轉入系列 − `gemini-cli-getting-started` ＝ 14（12 一般 ＋ 2 Codex）；#485 ＝ `series_data/claude-code.json` hub ＋ entries 1–60 ＝ 61；#501 ＝ entries 61–96 ＝ 36，與 `advanced/curriculum.json` 相同。111 個 slug 都有內容包、都是 `life`；`claude-code-*.json` 恰 97 個。本分支是 shallow clone，看不到 #485／#501／#499／#502 的原始 commit，改用 evidence 的 content-validation.json（61／97 頁）交叉核對。
- 內容包在合併後又被 #513（3 篇 description）、#525（2 篇 Codex）、#531（111 篇全部，完整網址→article 行內引用等）改過；最近一次部署 `deploy_20260919_032927`（#553）在這些之後，#554–#556 沒動內容包與圖檔。文件第 7.1 節給了 111 檔 sha256 合成值 `8674d468…7987f6` 讓主機核對，不需再部署。
- 本機檢查：`pack_cli lint --kind life --slug ×111` 111 entries、0 error、121 warning（119 `no_summary`、2 `text_length`）；整個 life 911 entries 0 error；`pytest tests/test_guides_content_pack.py` 9 passed／5 skipped。沒有改任何內容包。
- 正式站（06:47–06:50 UTC，9 個請求）：sitemap index 11 個子檔；`life-zh-TW.xml` 705 篇 ＋ 32 主題頁，111 個 slug 都不在；抽查三頁 200＋noindex＋title/h1「這篇文章目前看不到」；兩張 hero 已回 200。summary 端點合計 **1,270** 列（life zh-TW 705），發布後 **1,381**（(a) 1,379），子檔上限 5,000，票面「925 → 1,036」已過時。
- 站內連結重算（走訪 1,056 個內容包的 JSON）：指向 111 篇的 690 個引用全是 article 行內引用、沒有完整網址。已上線 zh-TW 來源 → 保留中文章 **29 條／21 篇**；扣掉 `codex-beginner-guide` 是 27 條／20 篇，比票面 25 多 2 條：`ai-tools-choose-by-task → ai-coding-tools-overview-2026`、`ai-workflow-coding-agents-division → claude-code-headless-json`（#553 今天上線）。批次 04 引用 `codex-cli-getting-started` 的是 4 篇（票面 3 篇之外多 `ai-coding-git-basics`）。三批之間 #485→#501 12、#501→#485 85，與票面一致。
- 限制：這個重算用 repo 內容包代表上線內容；正式站 DB 裡 #531 之前匯入的版本可能還是完整網址（真的會點進「看不到」），article 引用則在目標未發布時只顯示純文字。權威重算是主機上的 `guides-links-check --locale zh-TW`，文件第 7.5 節有指令。
- 沒有做的：站主決定、主機上的 dry-run／publish／驗證。
