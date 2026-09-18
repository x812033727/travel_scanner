# 工作區：幣圈新聞 2026（新聞批次 4）

批次 4 三個垂直之一：法規、技術與產業面的幣圈新聞，五語（zh-TW、en、ja、ko、zh-CN），
每篇一張原創主圖與一張 2×2 圖解。站上目前一篇幣圈文章都沒有，這是第一批。

> **現況與未完成事項（2026-09-17）**：見 [`docs/news-2026-batch-4/HANDOVER.md`](../news-2026-batch-4/HANDOVER.md)。
> 十一篇加索引都是五語、都經過獨立查核與逐語審稿，圖檔、`manifest.json`、contact sheet 與 relink 都做完了；
> **批次 4.5（2026-09-16 起的新消息）**：本工作區再加三篇（`crypto-news-fca-perimeter-guidance-20260916`、`crypto-news-cftc-passive-software-20260917`、`crypto-news-fca-p2p-crypto-crackdown-20260917`，display_order 211–213），索引新開「英國」組（`update_index.py crypto`，不重跑 `build_crypto_index.py`）；現況見 HANDOVER 第 1d 節。
>
> **2026-09-17 已匯入發布**（12 篇 × 5 語系）；日後修訂照 HANDOVER 2.1–2.3。

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
2. [`docs/news-2026-batch-4/crypto.md`](../news-2026-batch-4/crypto.md)
   — 幣圈專屬：可以寫／不可以寫的界線（站主定的，不是建議）、**每篇必帶的免責 callout**
     與五語標記字串、一手來源允許名單、用語。
3. [`docs/news-2026-batch-4/corrections-crypto.md`](../news-2026-batch-4/corrections-crypto.md)
   — **對本垂直的撰稿代理具有拘束力**。11 篇的獨立查核結論全是 `needs_fixes`，
     研究紀錄裡留著的錯誤照抄就會上線；開稿前先讀本篇 slug 那一段，再讀研究紀錄。

## 工具

腳本都在 [`docs/news-2026-batch-4/`](../news-2026-batch-4)，都從 `apps/api` 用 API 虛擬環境跑：

```bash
cd apps/api
uv run python ../../docs/news-2026-batch-4/check_article.py <slug> --full --assets
uv run python ../../docs/news-2026-batch-4/build_assets.py crypto [--svg-only]
uv run python ../../docs/news-2026-batch-4/merge_locale.py <slug> <en|ja|ko|zh-CN> <document.json>
uv run python ../../docs/news-2026-batch-4/review_dumps.py crypto <out-dir>      # 審稿代理讀的逐段對照檔
uv run python ../../docs/news-2026-batch-4/apply_corrections.py <corrections.json>...
uv run python ../../docs/news-2026-batch-4/align_links.py --apply                # 標題改過之後對齊連結文字
uv run python ../../docs/news-2026-batch-4/update_index.py crypto
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
| slug 前綴 | `crypto-news-`（`<vertical>-news-<topic>-<YYYYMMDD>`，日期是事件日） |
| `topics` | `["finance", "crypto"]`，hub 在前 |
| 索引 | `crypto-news-2026-index`（兩個 link 的第一個指向它） |
| hero 眉標 | `MOKAAIR  /  CRYPTO NEWS` |
| 主色 | `#D97A2B`（ORANGE，畫冊六色之一） |
| `display_order` | 200 起（`verticals.py` 的 `order_base`）：十一篇依 `check_article.py` 的 `RELATED` 順序是 200–210，索引是 199 |
| 免責 callout | 每篇都要，且用該語系自己的標記（zh-TW 是「不是投資建議」），不是中文那句的翻譯 |


## 票

[`tasks/done/2026-09-16-news-batch-4-1-crypto-regulation.md`](../../tasks/done/2026-09-16-news-batch-4-1-crypto-regulation.md)（重要新聞，2026-09-17 發布後結案）與
[`tasks/open/2026-09-16-news-batch-4-4-the-8.md`](../../tasks/open/2026-09-16-news-batch-4-4-the-8.md)（8/1 起的次要新聞）。

