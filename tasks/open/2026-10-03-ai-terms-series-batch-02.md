---
id: 2026-10-03-ai-terms-series-batch-02
title: AI 名詞系列第二批：14 個新詞專文並接上總索引
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-ai-terms-02
claimed_at: 2026-10-03T09:38:23Z
created_at: 2026-10-03T09:38:22Z
completed_at:
branch: claude/sweet-ramanujan-1v06fx
depends_on: []
scope:
  - docs/ai-terms-series/batch-02
  - apps/api/app/guides/content/ai-terms-index.json
  - apps/web/public/guides/ai-terms-index
  - apps/api/app/guides/content/ai-glossary-50-terms.json
  - apps/api/app/guides/content/ai-term-neural-network.json
  - apps/web/public/guides/ai-term-neural-network
  - apps/api/app/guides/content/ai-term-attention-mechanism.json
  - apps/web/public/guides/ai-term-attention-mechanism
  - apps/api/app/guides/content/ai-term-inference.json
  - apps/web/public/guides/ai-term-inference
  - apps/api/app/guides/content/ai-term-temperature.json
  - apps/web/public/guides/ai-term-temperature
  - apps/api/app/guides/content/ai-term-knowledge-cutoff.json
  - apps/web/public/guides/ai-term-knowledge-cutoff
  - apps/api/app/guides/content/ai-term-chain-of-thought.json
  - apps/web/public/guides/ai-term-chain-of-thought
  - apps/api/app/guides/content/ai-term-structured-outputs.json
  - apps/web/public/guides/ai-term-structured-outputs
  - apps/api/app/guides/content/ai-term-grounding.json
  - apps/web/public/guides/ai-term-grounding
  - apps/api/app/guides/content/ai-term-ai-alignment.json
  - apps/web/public/guides/ai-term-ai-alignment
  - apps/api/app/guides/content/ai-term-synthetic-data.json
  - apps/web/public/guides/ai-term-synthetic-data
  - apps/api/app/guides/content/ai-term-scaling-laws.json
  - apps/web/public/guides/ai-term-scaling-laws
  - apps/api/app/guides/content/ai-term-sycophancy.json
  - apps/web/public/guides/ai-term-sycophancy
  - apps/api/app/guides/content/ai-term-agi.json
  - apps/web/public/guides/ai-term-agi
  - apps/api/app/guides/content/ai-term-computer-use.json
  - apps/web/public/guides/ai-term-computer-use
---

# AI 名詞系列第二批：14 個新詞專文並接上總索引

## Why

第一批 81 篇 AI 名詞專文（`2026-09-14-ai-terms-series`）上線後，站主要求繼續補這個系列。
盤點後仍沒有專文的詞分兩類：50 詞速查只給一句話的（temperature、知識截止日、電腦操作），
以及總索引沒有收、但讀者讀其他專文時一定會撞到的基礎詞（神經網路、注意力機制、推論、
思維鏈、結構化輸出、接地、對齊、合成資料、縮放定律、迎合、AGI）。
站上已有的產品篇（例如 `claude-computer-use-explained`、`gemini-api-search-grounding-citations`）
講的是某個產品怎麼用，不是名詞本身，這批連過去但不重寫它們。

規格與撰稿指令在 [`docs/ai-terms-series/batch-02/`](../../docs/ai-terms-series/batch-02/brief.md)。

## Definition of done

- [x] 14 個內容包落在 `apps/api/app/guides/content/ai-term-*.json`，各自有 `hero.svg`、`hero.jpg`、`diagram-1.svg`。
- [x] 每篇正文 1,800–3,000 字、≥5 個 H2、恰好一個表、≥1 個 callout、≥3 個一手來源且 `checked_on` 是實際查證日。
- [x] 每篇經過一輪獨立查核（換人），改超過三個事實的再查第二輪。
- [x] `ai-terms-index` 把 14 篇分進既有分組；`ai-glossary-50-terms` 的 temperature、知識截止日、電腦操作三條連到新專文。
- [x] `pack_cli lint --kind life` 對這 16 個 slug 零 error，warning 只剩 `no_summary`；`intake_check.py --from-content` 零 FAIL。
- [x] 28 張圖（14 張 hero.jpg、14 張 diagram-1.svg）渲染後逐張目視過。
- [x] `uv run pytest tests/test_guides_content_pack.py` 通過；`npm run check:tasks` 通過。
- [ ] 部署後 14 篇先發布、總索引與速查最後更新（要站主同意，不在本票的 PR 裡）。

## Steps

- [x] 盤點既有 81 篇、50 詞速查與全站 slug，挑出 14 個詞，寫 `brief.md` 與 `catalogue.json`。
- [x] 撰稿：一篇一個代理，只寫 `docs/ai-terms-series/batch-02/staging/<slug>/`。
- [x] 查核：換人逐篇查來源與主張，修正清單寫在 `staging/<slug>/verify-1.md`；第一輪改超過三處的 11 篇再換人查第二輪（`verify-2.md`）。
- [x] 收件：`pack_cli ingest`、`intake_check.py`、`pack_cli lint`、目視 SVG。
- [x] 更新總索引與 50 詞速查的連結。
- [x] commit、push。
- [ ] 開 PR、合併。

## How to verify

```bash
cd apps/api
S="--slug ai-term-neural-network --slug ai-term-attention-mechanism --slug ai-term-inference \
   --slug ai-term-temperature --slug ai-term-knowledge-cutoff --slug ai-term-chain-of-thought \
   --slug ai-term-structured-outputs --slug ai-term-grounding --slug ai-term-ai-alignment \
   --slug ai-term-synthetic-data --slug ai-term-scaling-laws --slug ai-term-sycophancy \
   --slug ai-term-agi --slug ai-term-computer-use --slug ai-terms-index --slug ai-glossary-50-terms"
uv run python -m app.guides.pack_cli lint --kind life $S --warnings
uv run pytest tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q
npm run check:tasks
```

部署後（站主同意後）在主機：先 `guides-import --dry-run` 帶 14 個 slug，確認後 `--publish`，
最後才帶 `ai-terms-index` 與 `ai-glossary-50-terms` 發布。

## Follow-ups found while checking (not this ticket's scope)

- `gemini-api-search-grounding-citations` 寫引用位移是「UTF-8 位元組」。2026-10-03 查核：Interactions API 參考（2026-10-02 更新）說
  UrlCitation 的 `start_index` 是 "measured in bytes"，但沒有一頁寫 UTF-8；Google Search 指南沒寫單位，範例 Go 切位元組、Python/JS/Java 切字元。要開票複查。
- `render_svg` 在 `CHROMIUM_BIN` 指到完整版 `chromium-*/chrome-linux/chrome` 時，截圖底部約 88 px 變白邊（`--window-size` 含視窗外框）。
  預設的 headless shell 沒問題，所以不影響 ingest；但有人照舊指令設了 `CHROMIUM_BIN` 就會產出被截的 hero.jpg。可以開票讓 `render_svg` 偵測或改用 `--screenshot` 前先設 viewport。
- `claude-computer-use-explained`（2026-09-14）可能落後一個版本：Anthropic 文件現在是分版本的 computer use 工具組，較早版本仍標 beta。要開票複查工具名與 beta 字樣。

## Notes

- 撰稿指令刻意禁止寫模型型號、價格、截止日期與排行榜分數：這批是名詞，不是產品快照，不想再開回填票。
- **不加 `summary` 區塊。** `SummaryBlock` 的 docstring 記著站主 2026-09-16 的決定：模型寫的摘要要站主逐批讀過，再由 `pack_cli summarize --from` 套用。第一批 76 篇也都沒有，`no_summary` 警告是這個系列共通的待辦，不是這批的缺漏。
- **渲染：** 不要設 `CHROMIUM_BIN` 指到完整版 `chromium-*/chrome-linux/chrome`，它的 `--window-size=1600,900` 含視窗外框，截圖底部約 88 px 變白邊；`render_svg` 預設會挑 `chromium_headless_shell`，那個是完整 1600×900。
- **字數：** `_body_length` 會算進 `rich_paragraph` 裡連結的文字，brief 寫的「不含連結文字」是指 `link` 區塊。
- **總索引快滿了。** `ai-terms-index` 正文 5,910 字，life 類上限 6,000。第三批加詞前要先改索引結構，不然 lint 會報 `text_length`。
- **查核數字。** 14 篇第一輪共改 69 處事實，11 篇超過三處進第二輪，第二輪又改 20 處（其中不少是協調者指定要修的地方）。
  逐篇數字與協調者收件時另改的地方在 [`ARTICLES.md`](../../docs/ai-terms-series/batch-02/ARTICLES.md)。
- **平行查核者共用 scratchpad 會互相覆寫。** 兩位查核者回報暫存檔被別人蓋掉（各自的 pack.json 沒受影響）。下次在提示裡要求每人用 `scratchpad/<slug>/` 子目錄。
- 還沒做、可以當第三批的候選：強化學習、KV 快取、過擬合、可解釋性、資料投毒、世界模型、
  視覺語言模型、獎勵駭客（reward hacking）、本機推論、速率限制。
