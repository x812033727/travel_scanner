# AI 名詞系列第二批：撰稿指令

第一批 81 個概念已於 2026-09-14 上線（[`../ARTICLES.md`](../ARTICLES.md)）。這一批補 14 個仍沒有專文的詞，
其中 temperature、知識截止日、電腦操作三個已經在 `ai-glossary-50-terms` 有一句話定義，這裡寫完整專文。
指派在同目錄的 [`catalogue.json`](catalogue.json)。

**先讀這三份，全部規則照用**，這份只寫差異，衝突時以這份為準：

1. [`docs/life-ai-series-brief.md`](../../life-ai-series-brief.md)：`pack.json` 形狀、SVG 配色與尺寸、台灣用語、交出前自查。
2. [`docs/ai-terms-series/brief.md`](../brief.md)：第一批的編輯要求（1,800–3,000 字、假設案例、不憑記憶、新興詞標明誰的定義）。
3. 範本：`docs/ai-terms-series/staging/ai-term-sandbox/`（pack.json、research.json、兩張 SVG）。看形狀與口吻，不要抄句子。

## 與第一批不同的地方

- **工作區**：`docs/ai-terms-series/batch-02/staging/<slug>/`。只准寫自己的目錄，不准碰 `apps/`、別人的目錄、`catalogue.json`、任務票，不跑 git。
- **查證日**：`checked_on` 寫你真的打開那頁的日期（本批開工日 2026-10-03）。不要抄別篇日期。
- **站內連結用 `rich_paragraph` 的 `article` inline**，放進相關段落或段落後：
  `{"type":"rich_paragraph","inlines":[{"type":"text","text":"……"},{"type":"article","text":"連結文字","kind":"life","slug":"ai-term-xxx"}]}`。
  **只連指派 `links` 列出的 slug**，每個至少一次；加上總索引 `ai-terms-index`。不要用 `link` 區塊寫死網域。
- **結構**：≥5 個 level-2 heading；恰好一個比較表（2–3 欄）；≥1 個 callout；`diagram-1.svg` 一張；`hero.svg` 一張。
- **正文 1,800–3,000 字，目標 2,100–2,500**，算法同 `_body_length`（段落、rich_paragraph 的文字、清單項、表格格子、callout 標題與內文；不含 heading、圖說、連結文字、來源）。自己數，寫進 `research.json` 的 `running_text_characters`。
- **中文的「推論」與「推理」**：本系列 inference＝推論、reasoning＝推理。兩個詞同時出現時第一次附英文。
- **模型名、價格、截止日期、排行榜分數一律不寫**，除非指派明說需要且你今天在官方頁看到。寫機制，不寫產品快照。
- **一手來源**：原始論文（arXiv、期刊、會議頁）、官方開發者文件、標準原文。新聞、部落格轉述、內容農場不收。每篇 ≥3 個獨立一手來源；定義有分歧的詞，兩邊都要列。
- **假設案例**一律標「示例」並寫明未實測；不可把想像的模型輸出寫成觀察到的結果。
- **論文的數字**只寫「該論文在它的設定下」量到什麼，並寫出設定；不推廣成通則。
- **不承諾**：不寫「用了就不會幻覺」「設成 0 就固定」「有引用就正確」這類保證。

## 抓頁

- User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`；不得帶任何人的 email 或個資。
- `curl -sSL`（一定 `-L`），看狀態碼；200 的空殼頁不是來源。arXiv 讀 `https://arxiv.org/abs/<id>`。
- 讀不到的官方頁用 Wayback（CDX 查 `statuscode:200` 再抓 `web/<時間戳>id_/<網址>`）；`sources` 寫原網址，讀法記進 `notes.md`。
- helper 腳本寫成檔案放 `docs/ai-terms-series/batch-02/staging/<slug>/_tools/` 再執行（交件前刪掉 `_tools/`）。

## 自驗（只能 dry-run）

```bash
cd apps/api && .venv/bin/python -m app.guides.pack_cli ingest \
  --from ../../docs/ai-terms-series/batch-02/staging --slug <slug> --dry-run
```

SVG 渲染看圖（字壓線、超框、疊字）：

```bash
cd apps/api && .venv/bin/python -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('../../docs/ai-terms-series/batch-02/staging/<slug>/diagram-1.svg'), Path('/tmp/<slug>-d1.png'))"
```

PNG 放 `/tmp`，不要放進工作區。不要設 `CHROMIUM_BIN` 指到完整版 `chrome`：它會把 PNG 底部約 88 px 截成白邊；預設的 headless shell 才是完整 1600×900。

## 交付順序

`pack.json`（先寫骨架，每寫完一節存一次）→ `diagram-1.svg` → `hero.svg` → `notes.md`（`主張｜來源網址｜查證日｜讀取方式`）→ `research.json`。
最後回報一行：完成與否、字數、你懷疑但沒改的事。不要貼文章內容。
