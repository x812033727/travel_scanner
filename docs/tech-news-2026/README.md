# 工作區：科技新聞 2026（非 AI）（新聞批次 4）

批次 4 三個垂直之一：非 AI 的科技新聞——硬體、作業系統、網路與電信、平台法遵，
五語（zh-TW、en、ja、ko、zh-CN），每篇一張原創主圖與一張 2×2 圖解。

> **現況（2026-09-18）**：見 [`docs/news-2026-batch-4/HANDOVER.md`](../news-2026-batch-4/HANDOVER.md) 第 1b 節。
> 十三篇加索引都是五語、都經過兩輪獨立查核與逐語審稿，圖檔、`manifest.json`、contact sheet、`related` 與 relink 都做完了；
> **還沒合併、還沒匯入發布，等站主驗收與指示。** 發布前要重開的活頁面也列在那一節。
> 固定值：`topics` 是 `["tech", "tech-news"]`（需要時加 `gadgets`／`software`），主色 BLUE，眉標 `MOKAAIR  /  TECH NEWS`，
> `display_order` 十三篇 300–312、索引 299；**沒有免責 callout**。索引用 [`build_tech_index.py`](../news-2026-batch-4/build_tech_index.py) 產生 zh-TW。

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
2. [`docs/news-2026-batch-4/tech.md`](../news-2026-batch-4/tech.md)
   — 這個垂直存在的理由、可以寫／不可以寫的界線（與 AI 垂直怎麼分）、一手來源，
     以及這個垂直**不帶**免責 callout。
3. [`docs/news-2026-batch-4/corrections-tech.md`](../news-2026-batch-4/corrections-tech.md)
   — **對本垂直的撰稿代理具有拘束力**。每篇都是「紀錄寫了 X／X 錯在哪／改寫成 Z」，照著改；
     寫「不要寫這一句」的就整句刪掉，不要改寫成比較婉轉的版本。

## 工具

六個腳本都在 [`docs/news-2026-batch-4/`](../news-2026-batch-4)，都從 `apps/api` 用 API 虛擬環境跑：

```bash
cd apps/api
uv run python ../../docs/news-2026-batch-4/check_article.py <slug> --full --assets
uv run python ../../docs/news-2026-batch-4/build_assets.py tech [--svg-only]
uv run python ../../docs/news-2026-batch-4/merge_locale.py <slug> <en|ja|ko|zh-CN> <document.json>
uv run python ../../docs/news-2026-batch-4/apply_corrections.py <corrections.json>...
uv run python ../../docs/news-2026-batch-4/update_index.py tech
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
| slug 前綴 | `tech-news-`（`<vertical>-news-<topic>-<YYYYMMDD>`，日期是事件日） |
| `topics` | `["tech", "tech-news"]`，可再加 `gadgets`／`software` |
| 索引 | `tech-news-2026-index`（兩個 link 的第一個指向它） |
| hero 眉標 | `MOKAAIR  /  TECH NEWS` |
| 主色 | `#2F6F9F`（BLUE，畫冊六色之一） |
| `display_order` | 還沒指定號段；`check_article.py` 只要求不是預設的 100 |
| 免責 callout | 沒有。一篇只有它自己的提醒 `callout`（`tech.md`） |


## 票

[`tasks/open/2026-09-16-news-batch-4-2-non-ai.md`](../../tasks/open/2026-09-16-news-batch-4-2-non-ai.md)（重要新聞）與
[`tasks/open/2026-09-16-news-batch-4-4-the-8.md`](../../tasks/open/2026-09-16-news-batch-4-4-the-8.md)（8/1 起的次要新聞）。
