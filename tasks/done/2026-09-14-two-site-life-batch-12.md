---
id: 2026-09-14-two-site-life-batch-12
title: 兩站原創生活分享批次 12（12 篇）
status: done
priority: P2
area: docs
owner: codex-two-site-life
claimed_at: 2026-09-14T12:27:17Z
created_at: 2026-09-14T02:26:22Z
completed_at: 2026-09-14T12:59:37Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/envato-music-license.json
  - apps/web/public/guides/envato-music-license
  - .codex/two-site-life/work/envato-music-license
  - apps/api/app/guides/content/wise-transfer-checklist.json
  - apps/web/public/guides/wise-transfer-checklist
  - .codex/two-site-life/work/wise-transfer-checklist
  - apps/api/app/guides/content/saas-paas-iaas-responsibility.json
  - apps/web/public/guides/saas-paas-iaas-responsibility
  - .codex/two-site-life/work/saas-paas-iaas-responsibility
  - apps/api/app/guides/content/small-language-models.json
  - apps/web/public/guides/small-language-models
  - .codex/two-site-life/work/small-language-models
  - apps/api/app/guides/content/rag-retrieval-explained.json
  - apps/web/public/guides/rag-retrieval-explained
  - .codex/two-site-life/work/rag-retrieval-explained
  - apps/api/app/guides/content/generative-ai-basics.json
  - apps/web/public/guides/generative-ai-basics
  - .codex/two-site-life/work/generative-ai-basics
  - apps/api/app/guides/content/agent-service-evaluation.json
  - apps/web/public/guides/agent-service-evaluation
  - .codex/two-site-life/work/agent-service-evaluation
  - apps/api/app/guides/content/claude-cowork-evaluation.json
  - apps/web/public/guides/claude-cowork-evaluation
  - .codex/two-site-life/work/claude-cowork-evaluation
  - apps/api/app/guides/content/claude-design-evaluation.json
  - apps/web/public/guides/claude-design-evaluation
  - .codex/two-site-life/work/claude-design-evaluation
  - apps/api/app/guides/content/claude-code-plugin-management.json
  - apps/web/public/guides/claude-code-plugin-management
  - .codex/two-site-life/work/claude-code-plugin-management
  - apps/api/app/guides/content/four-hour-workweek-reflection.json
  - apps/web/public/guides/four-hour-workweek-reflection
  - .codex/two-site-life/work/four-hour-workweek-reflection
  - apps/api/app/guides/content/woocommerce-catalog-mode.json
  - apps/web/public/guides/woocommerce-catalog-mode
  - .codex/two-site-life/work/woocommerce-catalog-mode
---

# 兩站原創生活分享批次 12

## Why

依使用者核定的兩站標題盤點計畫，製作全部不重複主題。總表：`docs/content-research/two-site-life/catalogue.json`。

## Definition of done

- [x] 本批每篇都有原創正文、1600×900 封面、SVG 圖解、官方來源及查證日。
- [x] ingest、限定 slug lint、逐張圖片 QA 與相關測試通過。
- [x] 交付可匯入內容包；未執行正式站匯入、發布或部署。

## Steps

- [x] `envato-music-license` — Envato 音樂素材怎麼用：專案授權與上傳後申訴。必寫：授權登錄、素材修改、平台權利聲明。
- [x] `wise-transfer-checklist` — Wise 匯款前要確認什麼：地區、費用與收款資料。必寫：台灣可用性、報價與收款、交易查核。
- [x] `saas-paas-iaas-responsibility` — SaaS、PaaS 與 IaaS：你使用服務，也接下哪些責任。必寫：服務分層、資料與維運、退出成本。
- [x] `small-language-models` — 小型語言模型適合什麼：任務、裝置與準確度取捨。必寫：規模與用途、部署條件、評估方法。
- [x] `rag-retrieval-explained` — RAG 怎麼讓 AI 使用文件：檢索、引用與更新流程。必寫：檢索生成流程、權限與資料、答案驗證。
- [x] `generative-ai-basics` — 生成式 AI 的工作方式：文字、圖片與使用界線。必寫：生成與辨識、工具用途、查證與責任。
- [x] `agent-service-evaluation` — AI 代理服務怎麼評估：AaaS 的任務、權限與計費。必寫：服務定義、人工確認、成效與成本。
- [x] `claude-cowork-evaluation` — Claude Cowork 使用前：工作範圍、檔案權限與確認流程。必寫：官方功能與供應狀態、與Chat Code分工、檔案操作驗收。
- [x] `claude-design-evaluation` — Claude Design 怎麼評估：原型、簡報與設計交接。必寫：功能供應查證、設計輸入、交付與限制。
- [x] `claude-code-plugin-management` — Claude Code 外掛怎麼管理：來源、安裝與更新檢查。必寫：外掛與Skills分界、來源權限、驗收與移除。
- [x] `four-hour-workweek-reflection` — 重讀一週工作四小時的提問：委派、時間與生活選擇。必寫：書籍版本與出版資料、觀點檢視、個人適用界線。
- [x] `woocommerce-catalog-mode` — WooCommerce 型錄模式：展示商品而不直接結帳。必寫：價格與購物車顯示、YITH Catalog Mode、詢問流程。

## How to verify

`uv run python -m app.guides.pack_cli lint --kind life --slug <本批 slug> --render-dir <QA目錄>`

`uv run pytest tests/test_guides_content_pack.py -q`

`npm run check:tasks`

## Notes

來源原文只收標題與網址。不得將指派、通過 schema 或 AI 摘要視為完整文章。每篇 1,800–3,000 字並自行查證；協調者文件保存研究記錄。

2026-09-14：12 篇完整正文與 24 張圖片 QA 逐張檢視完成；ingest、限定 12 slug lint、字數與來源、50 字以上段落重複及站內連結驗收通過。內容包測試 9 passed、5 skipped（缺 PostgreSQL 測試環境），26.85 秒。核對 342 本機內容包、220 AI 題目與 46 文章任務，未有新增未對照主題。詳見 docs/content-research/two-site-life/batch-12-review.md 與證據檔。
