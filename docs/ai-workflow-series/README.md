# 工作區：「多模型 AI 工作流」教學系列（12 篇＋hub，zh-TW）

> **現況（2026-09-19）**：12 篇＋目錄篇**全部寫完並查核完畢**，圖檔、`related`、relink／autolink、系列登記與測試都已完成，分支 `claude/travel-scanner-pr-552-rpq36m`，等站主決定發布（票 `tasks/open/2026-09-18-ai-workflow-tutorial-series-12-zh.md`；
> 交接見本頁最後一節）。計畫來源：站主 2026-09-18 要求「新增幾篇 workflow 相關的教學與介紹，可以介紹比較高技術面的串不同的 model」，
> 定案為 12 篇＋一個系列 hub、只做 zh-TW、登記為獨立系列 `ai-workflow`（topic `ai-coding`）。

## 這個目錄放什麼

| 檔案 | 用途 |
| --- | --- |
| [`BRIEF.md`](BRIEF.md) | 撰稿規格（內容包形狀、區塊骨架、程式範例規則、用語、研究紀錄格式、回報格式）。撰稿代理只讀這一份加指派。 |
| [`agents/ASSIGNMENTS.md`](agents/ASSIGNMENTS.md) | 12 篇＋hub 的指派表：slug、display_order、程度、切角、必連且不可重寫的既有文章、來源種子、系列內 `related`。 |
| [`agents/FACTCHECK.md`](agents/FACTCHECK.md) | 查核代理規格：重抓來源、逐句核對、**每個 code 區塊重編譯並對官方文件比對簽名／旗標／端點**、模型 id 對白名單；改 >10 處才第二輪。 |
| [`series.py`](series.py) | 固定值：`SLUGS`（順序＝display_order 400–411）、`HUB`（399）、`TOPICS`、`EYEBROW`、`load()`。 |
| [`check_article.py`](check_article.py) | `check_article.py <slug> [--assets]`：schema、topics、order、字數、簡體字、lint、summary／FAQ、sources 與研究紀錄一致、**code 區塊編譯（py_compile／bash -n／json／yaml）、秘密 regex、模型 id 白名單**、圖檔。 |
| [`build_assets.py`](build_assets.py) | `build_assets.py [--svg-only] [--slug=…]`：hero（無日期）與 `diagram-1.svg`（`flow` 三到五步或 `grid` 2×2），`_DRAWINGS` 每篇一個，等文章寫好再填。 |
| [`build_catalogue.py`](build_catalogue.py) | `build_catalogue.py [--related] [--check]`：由 12 個內容包產生 `apps/api/app/guides/series_data/ai-workflow.json`（A–D 四組、concepts／builder／operator 三條路線、每篇的 level／platforms／aliases／prerequisites／related）；`--related` 同時把 related 寫回內容包。 |
| [`prune_autolinks.py`](prune_autolinks.py) | `prune_autolinks.py <content-dir> <slug>...`：`pack_cli autolink` 之後把 AI／參數／GenAI 三種誤導連結還原成文字（本系列的「參數」多指 API 參數，不是模型參數；GenAI 出現在 OpenTelemetry 慣例名稱裡）。 |
| [`models-seen.json`](models-seen.json) | 模型 id 白名單（id、官方頁 url、逐字、checked_on）；撰稿與查核只能新增、不能憑記憶寫 id。 |
| `research/<slug>.json` | 各篇研究紀錄（撰稿產出，含 `code_samples`、`diagram`、`hero_label`；查核加 `factcheck`）。 |
| `factcheck/<slug>.md` | 查核報告；改動超過十處或動到骨幹的篇章在同一檔尾加「## 第二輪」。 |
| `manifest.json`、`hero-sheet-*.jpg`、`diagram-1-sheet-*.jpg` | `build_assets.py` 全量建置的產物：13 篇的網址清單與 contact sheet（人眼看圖用）。 |
| `renders/`（git 忽略） | 出圖中間檔。 |

## 流程（B 節，`C:\Users\x8120\.claude\plans\parsed-conjuring-dolphin.md`）

1. 撰稿（sonnet，一篇一代理，指派抄 `agents/ASSIGNMENTS.md`）→ 各自跑 `check_article.py <slug>` 到 OK。
2. 查核（opus，一篇一代理）→ 改 >10 處才第二輪。
3. 協調者通讀 13 篇（用語統一、跨篇不重複、hub 一句一篇正確）→ `_DRAWINGS` → `build_assets.py` → `related`（表在 ASSIGNMENTS）→
   `pack_cli relink --prefix ai-workflow- --apply`、`autolink --prefix ai-workflow- --dry-run` 審 diff 再 `--apply`。
4. 登記：`apps/api/app/guides/series_registry.json` 加 `ai-workflow`（source `api-series`、topic `ai-coding`、hub `ai-workflow-tutorials`）、
   `series_data/ai-workflow.json`（鏡射 `claude-code.json`：groups A 觀念 1–3／B 接線 4–6／C 協作 7–9／D 營運 10–12，paths concepts／builder／operator）、
   `tests/test_guide_series.py` 的 registry 清單加 `ai-workflow` 並新增 catalogue 測試。
5. lint、pytest、`check:tasks`、PR；站主明確選發布後：先部署（registry 進 API），再 `guides-import --slug` hub＋12 篇同一趟。

## 網路請求

任何請求 UA 一律 `Mokaair-editorial`（主機拒絕時退回 curl 預設 UA），不得帶入任何人的 email 或個人資料——每個代理 prompt 都要寫這條。

## 交接（2026-09-19，協調者）

**產出**：13 個內容包 `apps/api/app/guides/content/ai-workflow-*.json`（hub 399、文章 400–411）、13 份研究紀錄 `research/`、13 份查核報告 `factcheck/`（其中 10 份含第二輪）、13 組圖檔 `apps/web/public/guides/ai-workflow-*/`（hero.svg／hero.jpg／diagram-1.svg，hero.jpg 48–68 KB）、contact sheet 與 `manifest.json`。

**流程實際跑法**：撰稿 sonnet ×13（12 篇並行，目錄篇等 12 篇標題定案後才寫）→ 每篇一位 opus 獨立查核（每篇查 83–204 條主張、改 7–17 條）→ 改動超過十處或動到骨幹論述的 10 篇（1、3、4、5、6、8、9、10、11、12）再做第二輪（只查第一輪新寫的句子、重跑程式，第二輪各改 3–11 處，結論全部 `ok`）→ 協調者通讀（兄弟篇點名改為現題、引號統一《》）→ `build_catalogue.py --related` → `pack_cli relink --prefix ai-workflow- --apply` → `pack_cli autolink --prefix ai-workflow- --apply` 再 `prune_autolinks.py`（37 條建議保留 24 條）→ `build_assets.py` 全量重建 → 13 篇 `check_article.py <slug> --assets` 全 OK。

**檢查結果**：`pack_cli lint --kind life` 0 errors（911 entries；第 8 篇有一條 `text_length` 警告：relink 加上兩個站內連結標題後正文 6,045 字，超過 6,000 的 life 指引 45 字，僅警告）；`pytest tests/test_guide_series.py tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py tests/test_guides_content_links.py` 69 passed／24 skipped（PostgreSQL leg）；`npm run check:tasks` 綠。`test_guide_series.py` 有一處既有測試改為依 slug 取 claude-code 目錄（原本 `catalogues()[0]`，新檔案依檔名排序後變成本系列）。

**環境差異**：這一輪在 Linux 容器跑（venv python、`bash -n` 走 PATH），Chromium 沒有 CJK 字型，手動把 Noto Sans TC 裝到 `~/.fonts`；SVG 的字型堆疊仍是 JhengHei → Noto Sans TC → sans-serif，Windows 上會渲染成 JhengHei。`build_assets.py` 的輸出目錄與 flow 圖的序號兩個 bug 這一輪修掉（見 git log）。

**models-seen.json**：22 → 31 筆。新增：`gpt-4o`（只作「從 GPT-4o 起支援」的歷史句依據，未用於程式）、`mistral-small-2603`（未使用；verbatim 只在頁面 title 屬性）、`openai/gpt-oss-120b`（Groq）、`gemma4:cloud`、`gemma4:31b-cloud`、`gpt-oss:20b-cloud`、`gpt-oss:120b-cloud`、`openai/gpt-5.6-terra`、`openrouter/google/gemini-3.8-flash`（**組合字串**：LiteLLM 前綴＋OpenRouter id，頁面上沒有逐字出現，notes 已註明——要不要留給站主定奪）。

**留給站主的事**（各篇查核報告「留給站主」的彙整；沒有一件擋發布）：
- 通用：13 篇結尾連結已 relink；各篇 `checked_on` 2026-09-18 或 2026-09-19（11、12 篇與目錄篇因依頁面改數字或換來源而對齊到 19 日）；正文的價格與 API 參數請照 `2026-09-16-model-table-quarterly-recheck` 的節奏回查。
- 第 3 篇：Gemini 3.8 Flash 標準價 2027-01-01 起改為 1.50／7.50，屆時回查；表格「每萬次」的 114 與 1,004 只在表格。
- 第 4 篇：第一個範例的 OpenRouter 半段與 `openrouter-multi-model-api` 的範例形狀相近（指派要求）。
- 第 6 篇：Anthropic 結構化輸出頁只列系列名、沒有 Fable／Mythos 的 API id；「重試三次」實為整輪最多送三次（四處一致）。
- 第 7 篇：summary 與 description 的「倍增」偏強（n+m 是線性相加）；第二塊程式沿用第一塊的變數。
- 第 8 篇：Gemini CLI Plan Mode 在無頭執行下仍可能等確認，正式排程前請實測；`git add -N` 會動索引；正文長度已到 life 上限。
- 第 9 篇：Codex 的工具白名單要讀者自己貼進 `~/.codex/config.toml`，文件沒有指令可設。
- 第 10 篇：本篇寫 `localhost:11434/v1`、`ollama-getting-started` 寫 `…/v1/`（兩種都在官方頁）；另立票 `2026-09-19-ollama-getting-started-tool-choice-recheck`（該篇「不支援 tool_choice」與今天的相容性頁不符）。
- 第 12 篇：Anthropic 另有「不可信內容只放 tool_result」一條，本篇範例做不到、正文未宣稱符合；MCP 規格頁已不在 sources，日後要引用得先加回來。
- 用語：「位置偏誤／偏差」「orchestration 的三種譯名」「in-context examples」跨篇不一致，屬全站用語表的事。

**發布（站主明確選擇後）**：先部署（registry 與 `series_data/ai-workflow.json` 進 API），再 `guides-import --slug` hub＋12 篇同一趟；驗證 `https://mokaair.com/zh-TW/life/ai-workflow-tutorials` 會用 SeriesHub 列出 12 篇、`curl -s 'https://mokaair.com/api/v1/guides/series?locale=zh-TW' | grep -c ai-workflow` 為 1、13 個網址 200。
