# 工作區：「多模型 AI 工作流」教學系列（12 篇＋hub，zh-TW）

> **現況（2026-09-18）**：工作區、規格、檢查器、出圖與模型白名單就緒，**文章還沒寫**——撰稿與查核代理要等週額度重置後開工
> （票 `tasks/open/2026-09-18-ai-workflow-tutorial-series.md`）。計畫來源：站主 2026-09-18 要求「新增幾篇 workflow 相關的教學與介紹，
> 可以介紹比較高技術面的串不同的 model」，定案為 12 篇＋一個系列 hub、只做 zh-TW、登記為獨立系列 `ai-workflow`（topic `ai-coding`）。

## 這個目錄放什麼

| 檔案 | 用途 |
| --- | --- |
| [`BRIEF.md`](BRIEF.md) | 撰稿規格（內容包形狀、區塊骨架、程式範例規則、用語、研究紀錄格式、回報格式）。撰稿代理只讀這一份加指派。 |
| [`agents/ASSIGNMENTS.md`](agents/ASSIGNMENTS.md) | 12 篇＋hub 的指派表：slug、display_order、程度、切角、必連且不可重寫的既有文章、來源種子、系列內 `related`。 |
| [`agents/FACTCHECK.md`](agents/FACTCHECK.md) | 查核代理規格：重抓來源、逐句核對、**每個 code 區塊重編譯並對官方文件比對簽名／旗標／端點**、模型 id 對白名單；改 >10 處才第二輪。 |
| [`series.py`](series.py) | 固定值：`SLUGS`（順序＝display_order 400–411）、`HUB`（399）、`TOPICS`、`EYEBROW`、`load()`。 |
| [`check_article.py`](check_article.py) | `check_article.py <slug> [--assets]`：schema、topics、order、字數、簡體字、lint、summary／FAQ、sources 與研究紀錄一致、**code 區塊編譯（py_compile／bash -n／json／yaml）、秘密 regex、模型 id 白名單**、圖檔。 |
| [`build_assets.py`](build_assets.py) | `build_assets.py [--svg-only] [--slug=…]`：hero（無日期）與 `diagram-1.svg`（`flow` 三到五步或 `grid` 2×2），`_DRAWINGS` 每篇一個，等文章寫好再填。 |
| [`models-seen.json`](models-seen.json) | 模型 id 白名單（id、官方頁 url、逐字、checked_on）；撰稿與查核只能新增、不能憑記憶寫 id。 |
| `research/<slug>.json` | 各篇研究紀錄（撰稿產出，含 `code_samples`、`diagram`、`hero_label`；查核加 `factcheck`）。 |
| `factcheck/<slug>.md` | 查核報告。 |
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
