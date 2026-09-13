---
id: 2026-09-13-life-ai-batch-03
title: 生活分享 AI 系列批次 03：Claude 教學（20 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-13T11:55:59Z
completed_at:
branch:
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/claude-plans-free-pro-max-2026.json
  - apps/api/app/guides/content/claude-projects-knowledge-base.json
  - apps/api/app/guides/content/claude-artifacts-guide.json
  - apps/api/app/guides/content/claude-extended-thinking-guide.json
  - apps/api/app/guides/content/claude-file-analysis-pdf-excel.json
  - apps/api/app/guides/content/claude-writing-style-guide.json
  - apps/api/app/guides/content/claude-for-translation-zh-tw.json
  - apps/api/app/guides/content/claude-system-prompt-basics.json
  - apps/api/app/guides/content/claude-computer-use-explained.json
  - apps/api/app/guides/content/claude-mcp-explained.json
  - apps/api/app/guides/content/claude-desktop-mobile-app-setup.json
  - apps/api/app/guides/content/claude-in-chrome-browser-agent.json
  - apps/api/app/guides/content/claude-memory-and-privacy.json
  - apps/api/app/guides/content/claude-vs-chatgpt-writing-test.json
  - apps/api/app/guides/content/claude-for-research-summaries.json
  - apps/api/app/guides/content/claude-skills-explained.json
  - apps/api/app/guides/content/claude-api-first-call.json
  - apps/api/app/guides/content/claude-api-prompt-caching-cost.json
  - apps/api/app/guides/content/claude-model-lineup-2026.json
  - apps/api/app/guides/content/claude-for-teachers-lesson-plans.json
  - apps/web/public/guides/claude-plans-free-pro-max-2026
  - apps/web/public/guides/claude-projects-knowledge-base
  - apps/web/public/guides/claude-artifacts-guide
  - apps/web/public/guides/claude-extended-thinking-guide
  - apps/web/public/guides/claude-file-analysis-pdf-excel
  - apps/web/public/guides/claude-writing-style-guide
  - apps/web/public/guides/claude-for-translation-zh-tw
  - apps/web/public/guides/claude-system-prompt-basics
  - apps/web/public/guides/claude-computer-use-explained
  - apps/web/public/guides/claude-mcp-explained
  - apps/web/public/guides/claude-desktop-mobile-app-setup
  - apps/web/public/guides/claude-in-chrome-browser-agent
  - apps/web/public/guides/claude-memory-and-privacy
  - apps/web/public/guides/claude-vs-chatgpt-writing-test
  - apps/web/public/guides/claude-for-research-summaries
  - apps/web/public/guides/claude-skills-explained
  - apps/web/public/guides/claude-api-first-call
  - apps/web/public/guides/claude-api-prompt-caching-cost
  - apps/web/public/guides/claude-model-lineup-2026
  - apps/web/public/guides/claude-for-teachers-lesson-plans
---

# 生活分享 AI 系列批次 03：Claude 教學（20 篇）

## Why

`docs/life-ai-series.md` 的批次 03。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
分十一批產出；這張票是其中一批，scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

開工前先讀 `docs/life-ai-series.md` 的「經驗記錄」與批次 01 票的 Outcome。

## Definition of done

- [ ] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [ ] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [ ] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [ ] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 合作 · 易變）：

1. `claude-plans-free-pro-max-2026` · Claude 免費、Pro、Max 方案比較：額度怎麼算、值不值得 · ai, software · 圖：插 · 易變
2. `claude-projects-knowledge-base` · Claude Projects：把資料與指令放進專案，越用越懂你 · ai, tutorial · 圖：插
3. `claude-artifacts-guide` · Claude Artifacts：在對話裡直接做出網頁、圖表與小工具 · ai, tutorial · 圖：插
4. `claude-extended-thinking-guide` · Claude 延伸思考模式：什麼題目該開、怎麼看它的推理 · ai, tutorial · 圖：插 · 易變
5. `claude-file-analysis-pdf-excel` · 給 Claude 讀 PDF 與試算表：摘要、比對與抓數字 · ai, tutorial · 圖：插
6. `claude-writing-style-guide` · 用 Claude 寫作：設定風格、長文結構與潤稿 · ai, productivity · 圖：插
7. `claude-for-translation-zh-tw` · 用 Claude 做中英日翻譯：語氣、專有名詞與術語表 · ai, productivity · 圖：插
8. `claude-system-prompt-basics` · 系統提示詞入門：讓 Claude 穩定扮演一種角色 · ai, tutorial · 圖：插
9. `claude-computer-use-explained` · Claude 操作電腦是怎麼回事：能力、限制與安全 · ai · 圖：插 · 易變
10. `claude-mcp-explained` · MCP 是什麼：讓 Claude 連上你的檔案、日曆與資料庫 · ai, tutorial · 圖：插
11. `claude-desktop-mobile-app-setup` · Claude 桌面版與手機 App：安裝、快捷鍵與語音 · ai, software · 圖：照
12. `claude-in-chrome-browser-agent` · Claude 在瀏覽器裡：Chrome 擴充功能替你操作網頁 · ai, tutorial · 圖：插 · 易變
13. `claude-memory-and-privacy` · Claude 的記憶與隱私：什麼會被記住、怎麼清除 · ai, misc · 圖：插 · 易變
14. `claude-vs-chatgpt-writing-test` · Claude 和 ChatGPT 寫作比一比：同一題目的實測 · ai · 圖：插 · 易變
15. `claude-for-research-summaries` · 用 Claude 讀論文與長報告：摘要、提問與批判 · ai, productivity · 圖：插
16. `claude-skills-explained` · Claude Skills 是什麼：把重複流程包成可重用的技能 · ai, tutorial · 圖：插 · 易變
17. `claude-api-first-call` · 第一次呼叫 Claude API：金鑰、費用與十行 Python · ai, tutorial · 圖：插 · 易變
18. `claude-api-prompt-caching-cost` · Claude API 省錢：提示快取與批次處理怎麼用 · ai, tutorial · 圖：插 · 易變
19. `claude-model-lineup-2026` · Claude 模型家族：Opus、Sonnet、Haiku 怎麼選 · ai · 圖：插 · 易變
20. `claude-for-teachers-lesson-plans` · 老師用 Claude：出題、教案與批改回饋 · ai, productivity · 圖：照

- [ ] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [ ] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [ ] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。
