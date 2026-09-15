---
id: 2026-09-15-content-summary-howto-and-life
title: 編輯為攻略與生活文章加入重點摘要（summary）與真實 FAQ
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-15T13:57:48Z
completed_at:
branch:
depends_on:
  - 2026-09-15-summary-faq-definedterm-jsonld-web
scope:
  - apps/api/app/guides/content
---

# 編輯為攻略與生活文章加入重點摘要（summary）與真實 FAQ

## Why

有了區塊之後，內容要由人寫：摘要從文章首段與表格提煉，不新增事實；FAQ 只在文章本來就有 ≥2 個真實問答時加。

## Definition of done

- [ ] howto 與 life 每批加 summary，`pack_cli lint --warnings` 的 `no_summary` 數逐批下降；不用任何自動生成。

## Steps

- [ ] 依前綴分批；與 `2026-09-14-answer-first-howto-descriptions` 同一輪處理 howto。
- [ ] 每批 lint、內容包測試、部署後匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto --warnings
```

## Notes

**不自動生成**：一句錯的票價會被答案引擎快取。
