# 工作區：AI 新聞 9 月下旬與 1 月起補漏（新聞批次 4）

批次 4 三個垂直之一，接在 `docs/ai-news-2026-09`、`docs/ai-news-2026-ytd`、
`docs/ai-news-2026-09-mid` 之後：補到 9/16，並補回 1/1 起漏掉的重要新聞。
五語（zh-TW、en、ja、ko、zh-CN），每篇一張原創主圖與一張 2×2 圖解。

> **現況（2026-09-18）**：見 [`docs/news-2026-batch-4/HANDOVER.md`](../news-2026-batch-4/HANDOVER.md) 第 1c 節。
> 十二篇都是五語、都經過兩輪獨立查核與逐語審稿，圖檔、`manifest.json`、contact sheet、`related` 與 relink 都做完了；
> 既有索引 `ai-news-2026-january-september-index` 已原地改版（拿掉篇數、加 12 篇連結）。
> **批次 4.5（2026-09-16 起的新消息）**：本工作區再加六篇（`ai-news-chatgpt-sponsored-agents-20260916`、`ai-news-firefox-smart-window-mistral-20260916`、`ai-news-openai-misalignment-reports-20260917`、`ai-news-anthropic-pace-metrics-20260917`、`ai-news-astra-for-law-20260917`、`ai-news-google-cc-family-agent-20260918`，display_order 161–166），研究紀錄直接寫在 `research/`，索引原地增補；現況見 HANDOVER 第 1d 節。
>
> **批次 4.6（2026-09-19，待發布）**：本工作區再加兩篇 9 月 18 日的 AI 公告
> （`ai-news-anthropic-accenture-evaluation-20260918`、`ai-news-google-flow-fashion-20260918`，
> display_order 167–168），研究紀錄在 `research/`，既有索引已原地增補（五語各兩個連結、日期句改到 9 月 19 日）。
> 票在 `tasks/open/2026-09-19-ai-news-batch-4-6-since.md`，那張票記著 OpenAI 同日那則為什麼沒寫、
> 索引來源為什麼只引用一篇、`update_index.py` 這次改了哪幾張表，
> 以及**這一輪沒有獨立查核、`factcheck/` 沒有這兩篇**這件事。
>
> **PR #548 已於 2026-09-18 合併、部署並匯入發布**（12 篇＋索引＋30 個只改了連結文字的既有包同一次 `--slug` 匯入；清單在 HANDOVER 第 2.4 節）。
> 固定值：`topics` 是 `["ai", "ai-news"]`（需要時加 `software`／`gadgets`），主色 TEAL，眉標 `MOKAAIR  /  AI NEWS`，
> `display_order` 十二篇 149–160；**沒有免責 callout**（含 B8 金融服務那篇，理由見 `ai.md`）。
> 實際發給代理的六份規格在 [`docs/news-2026-batch-4/agents/ai/`](../news-2026-batch-4/agents/ai)。

## 這個目錄放什麼

| 路徑 | 內容 | 誰寫的 |
| --- | --- | --- |
| `research/<slug>.json` | 每篇的研究紀錄：`verified_facts`、`unverified_or_excluded`、`hero_label`、2×2 圖解的四格文字。格式見 `BRIEF.md` 的「研究紀錄」。 | 撰稿代理，動筆前 |
| `manifest.json` | 本垂直已產圖的篇目與五語網址。 | `build_assets.py` |
| `renders/` | SVG 轉出的 PNG 中間檔，每次重跑都覆寫。git 忽略——`.gitignore` 由 `build_assets.py` 寫，內容是 `renders/` 與 `__pycache__/`。 | `build_assets.py` |
| `hero-sheet-N-<locale>.jpg`、`diagram-1-sheet-N-<locale>.jpg` | contact sheet，四篇一張。代理看不到自己畫的圖，所以出刊前要由人逐張看過（`BRIEF.md`「圖像」）。 | `build_assets.py` |

不放在這裡的兩樣東西：**內容包**在 `apps/api/app/guides/content/<slug>.json`，
**上線圖檔**在 `apps/web/public/guides/<slug>/`。

批次共用的前期研究與獨立查核（撰稿前就做好的那一批）留在
[`docs/news-2026-batch-4/research/`](../news-2026-batch-4/research) 與
[`docs/news-2026-batch-4/factcheck/`](../news-2026-batch-4/factcheck)。
本目錄的 `research/<slug>.json` 是**套用修正清單之後**、工具真正讀的那一份：
`check_article.py` 與 `build_assets.py` 都用 slug 前綴決定工作區，見
[`verticals.py`](../news-2026-batch-4/verticals.py)。

## 動筆前必讀的三份文件

1. [`docs/news-2026-batch-4/BRIEF.md`](../news-2026-batch-4/BRIEF.md)
   — 三個垂直共同的查證規則、內容包格式、`blocks` 順序、篇幅、`summary`／`faq`、翻譯與流程。
2. [`docs/news-2026-batch-4/ai.md`](../news-2026-batch-4/ai.md)
   — 補漏範圍、既有篇目表（動筆前逐一比對，不要重寫講過的事），
     以及改索引標題的三個陷阱。
3. [`docs/news-2026-batch-4/corrections-ai.md`](../news-2026-batch-4/corrections-ai.md)
   — **對本垂直的撰稿代理具有拘束力**。每篇都是「紀錄寫了 X／X 錯在哪／改寫成 Z」，照著改；
     引用事實時一律用 `verified_facts` 陣列的 1-based 位置。

## 工具

六個腳本都在 [`docs/news-2026-batch-4/`](../news-2026-batch-4)，都從 `apps/api` 用 API 虛擬環境跑：

```bash
cd apps/api
uv run python ../../docs/news-2026-batch-4/check_article.py <slug> --full --assets
uv run python ../../docs/news-2026-batch-4/build_assets.py ai [--svg-only]
uv run python ../../docs/news-2026-batch-4/merge_locale.py <slug> <en|ja|ko|zh-CN> <document.json>
uv run python ../../docs/news-2026-batch-4/apply_corrections.py <corrections.json>...
uv run python ../../docs/news-2026-batch-4/update_index.py ai
```

`check_article.py` 要印出 `OK` 才算完成。`WARN` 行是可以出刊、但值得看一眼的事——
例如 hero 超過 200 KB 的編輯準則卻仍在 300 KB 硬上限之內，與站上 `pack_ingest` 的分級一致。
移植時的取捨與還沒驗證的事記在 [`PORT-NOTES.md`](../news-2026-batch-4/PORT-NOTES.md)。

渲染要瀏覽器：`build_assets.py` 走 `pack_ingest.chromium_binary()`，這個容器上實測找到
`/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`；
`--svg-only` 只寫 SVG，不需要瀏覽器。

## 本垂直的固定值（來自 `verticals.py`，不要在別處重打一遍）

| | |
| --- | --- |
| slug 前綴 | `ai-news-`（`<vertical>-news-<topic>-<YYYYMMDD>`，日期是事件日） |
| `topics` | `["ai", <橫向主題>, "ai-news"]` |
| 索引 | `ai-news-2026-january-september-index`，既有索引，**slug 永遠不改**，只原地改標題 |
| hero 眉標 | `MOKAAIR  /  AI NEWS` |
| 主色 | `#0D6B68`（TEAL，畫冊六色之一，也是前三批的顏色，所以圖解與批次 3 逐位元組相同） |
| `display_order` | 從 149 起算，接在 `ai-news-siri-ai-ios-27-20260914` 的 148 之後 |
| 免責 callout | 原則上沒有；但帶 `finance` 的文章一定要，見下方 |


索引改標題會波及既有文章的連結文字（`article` inline 的 `text` 是凍進內容包的）。
`update_index.py` 的 `retitle()` 走每個內容包的 JSON 結構，只改 `slug` 等於索引的 inline，
**不要用正規表示式**——各批次的欄位順序不一致。細節見 `ai.md` 的三個陷阱。

## 票

[`tasks/done/2026-09-16-news-batch-4-3-ai-news.md`](../../tasks/done/2026-09-16-news-batch-4-3-ai-news.md)（重要新聞，2026-09-18 發布後結案）與
[`tasks/open/2026-09-16-news-batch-4-4-the-8.md`](../../tasks/open/2026-09-16-news-batch-4-4-the-8.md)（8/1 起的次要新聞）。

B8（`ai-news-chatgpt-financial-services-20260910`）**不帶 `finance`、沒有投資免責 callout**，照 `ai.md` 的決定發布；它的一般 callout 明講「不是理財建議」。
