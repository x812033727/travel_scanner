# AI 名詞系列第三批：撰稿指令

第三批 10 個詞，指派在同目錄的 [`catalogue.json`](catalogue.json)。規則沿用第二批：
**先讀 [`../batch-02/brief.md`](../batch-02/brief.md) 全文，以及它要你讀的三份文件**，全部照用。
這份只寫第二批收件時才發現、這批要一開始就做對的事；衝突時以這份為準。

## 和第二批不同的地方

- **工作區**：`docs/ai-terms-series/batch-03/staging/<slug>/`。只寫自己的目錄，不碰 `apps/`、別人的目錄、`catalogue.json`、任務票，不跑 git（連唯讀的 `git status` 也不要跑）。
- **暫存檔**：helper 腳本與下載檔放 `docs/ai-terms-series/batch-03/staging/<slug>/_tools/`，交件前刪掉。不要用 session 的共用 scratchpad：第二批有平行代理在那裡互相蓋掉檔案。
- **topics 是 `["ai", "tutorial", "ai-terms"]`**。`ai-terms` 讓文章出現在 AI 名詞系列裡、連回總索引；第二批漏了它。
- **「本文」「這篇」全篇（含 description）最多出現一次。** 說明範圍可以寫「以下」「這裡」「內容」。
- **正文不寫查證過程**：不寫「查證日」「查證時」「我們查不到」。日期範圍寫成「資料截至 2026 年 10 月」。
- **字數**：`_body_length` 會把 `rich_paragraph` 裡連結的文字也算進去。目標 2,200–2,600，上限 3,000。
- **台灣用語**：術語先查台灣通行譯名（Google 繁中機器學習詞彙表、國家教育研究院雙語詞彙），避免中國用語（例如 activation function 寫「活化函數」，不寫「激活函數」；不寫「信息」「默認」「優化」當 optimize 的意思時寫「最佳化」）。譯名不統一的詞，第一段說明採用哪個與理由。
- **連結**：只連指派 `links` 列出的 slug，每個至少一次，加上 `ai-terms-index`。用 `rich_paragraph` 的 `article` inline。
- **既有實作篇**：`local-llm-why-and-when`、`local-llm-hardware-requirements`、`gemini-api-cost-errors-guide` 是操作教學；概念篇第一段就寫明「操作步驟見⋯⋯」並連過去，不重寫它們。

## 渲染

`render_svg` 不要設 `CHROMIUM_BIN`（預設的 headless shell 才會給完整 1600×900）：

```bash
cd apps/api && .venv/bin/python -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('../../docs/ai-terms-series/batch-03/staging/<slug>/diagram-1.svg'), Path('../../docs/ai-terms-series/batch-03/staging/<slug>/_tools/d1.png'))"
```

自驗：

```bash
cd apps/api && .venv/bin/python -m app.guides.pack_cli ingest \
  --from ../../docs/ai-terms-series/batch-03/staging --slug <slug> --dry-run
```

`no_summary` 警告不用處理：摘要由協調者在查核後另外加。
