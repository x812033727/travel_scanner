---
id: 2026-09-13-life-ai-batch-10
title: 生活分享 AI 系列批次 10：比較、費用、資安與法律（20 篇）
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-15T06:20:43Z
created_at: 2026-09-13T11:56:00Z
completed_at: 2026-09-15T08:53:43Z
branch:
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/ai-subscription-which-to-pay-2026.json
  - apps/api/app/guides/content/ai-benchmarks-explained.json
  - apps/api/app/guides/content/ai-model-release-timeline-2026.json
  - apps/api/app/guides/content/ai-api-pricing-comparison-2026.json
  - apps/api/app/guides/content/ai-scams-deepfake-taiwan.json
  - apps/api/app/guides/content/ai-account-security-2fa-api-keys.json
  - apps/api/app/guides/content/ai-and-copyright-law-taiwan.json
  - apps/api/app/guides/content/ai-at-work-policy-checklist.json
  - apps/api/app/guides/content/ai-detection-tools-reliability.json
  - apps/api/app/guides/content/ai-energy-water-footprint.json
  - apps/api/app/guides/content/ai-for-kids-parent-guide.json
  - apps/api/app/guides/content/ai-regulation-eu-act-taiwan.json
  - apps/api/app/guides/content/ai-prompt-injection-explained.json
  - apps/api/app/guides/content/ai-chat-history-export-delete.json
  - apps/api/app/guides/content/ai-token-cost-estimation.json
  - apps/api/app/guides/content/ai-open-vs-closed-models.json
  - apps/api/app/guides/content/ai-taiwan-local-models-taide.json
  - apps/api/app/guides/content/ai-companion-mental-health-caution.json
  - apps/api/app/guides/content/ai-news-sources-to-follow.json
  - apps/api/app/guides/content/ai-hype-vs-reality-2026.json
  - apps/web/public/guides/ai-subscription-which-to-pay-2026
  - apps/web/public/guides/ai-benchmarks-explained
  - apps/web/public/guides/ai-model-release-timeline-2026
  - apps/web/public/guides/ai-api-pricing-comparison-2026
  - apps/web/public/guides/ai-scams-deepfake-taiwan
  - apps/web/public/guides/ai-account-security-2fa-api-keys
  - apps/web/public/guides/ai-and-copyright-law-taiwan
  - apps/web/public/guides/ai-at-work-policy-checklist
  - apps/web/public/guides/ai-detection-tools-reliability
  - apps/web/public/guides/ai-energy-water-footprint
  - apps/web/public/guides/ai-for-kids-parent-guide
  - apps/web/public/guides/ai-regulation-eu-act-taiwan
  - apps/web/public/guides/ai-prompt-injection-explained
  - apps/web/public/guides/ai-chat-history-export-delete
  - apps/web/public/guides/ai-token-cost-estimation
  - apps/web/public/guides/ai-open-vs-closed-models
  - apps/web/public/guides/ai-taiwan-local-models-taide
  - apps/web/public/guides/ai-companion-mental-health-caution
  - apps/web/public/guides/ai-news-sources-to-follow
  - apps/web/public/guides/ai-hype-vs-reality-2026
---

# 生活分享 AI 系列批次 10：比較、費用、資安與法律（20 篇）

## Why

`docs/life-ai-series.md` 的批次 10。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
分十一批產出；這張票是其中一批，scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

開工前先讀 `docs/life-ai-series.md` 的「經驗記錄」與批次 01 票的 Outcome。

## Definition of done

- [x] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [x] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [x] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [x] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 合作 · 易變）：

1. `ai-subscription-which-to-pay-2026` · 只能訂一個的話訂哪個：ChatGPT、Claude、Gemini · ai, software · 圖：插 · 易變
2. `ai-benchmarks-explained` · 模型跑分怎麼看：LMArena、SWE-bench 與陷阱 · ai · 圖：插 · 易變
3. `ai-model-release-timeline-2026` · 2026 年 AI 模型大事記 · ai, misc · 圖：插 · 易變
4. `ai-api-pricing-comparison-2026` · API 價格比較：每百萬 token 各家多少 · ai, software · 圖：插 · 易變
5. `ai-scams-deepfake-taiwan` · AI 詐騙與 Deepfake：台灣案例與防範 · ai, daily · 圖：插
6. `ai-account-security-2fa-api-keys` · 保護你的 AI 帳號：兩步驟驗證與金鑰外洩 · ai, tutorial · 圖：插
7. `ai-and-copyright-law-taiwan` · AI 與著作權：台灣法規與判決整理 · ai, misc · 圖：插
8. `ai-at-work-policy-checklist` · 公司裡用 AI 的規範：資料外流與合規 · ai, productivity · 圖：插
9. `ai-detection-tools-reliability` · AI 偵測工具準不準 · ai, misc · 圖：插
10. `ai-energy-water-footprint` · AI 的用電與用水：一次對話的成本 · ai, misc · 圖：插
11. `ai-for-kids-parent-guide` · 家長指南：孩子用 AI 的年齡限制與設定 · ai, daily · 圖：照 · 易變
12. `ai-regulation-eu-act-taiwan` · 歐盟 AI 法案與台灣 AI 基本法：對使用者的影響 · ai, misc · 圖：插 · 易變
13. `ai-prompt-injection-explained` · 提示詞注入是什麼：使用者該懂的攻擊 · ai, tutorial · 圖：插
14. `ai-chat-history-export-delete` · 匯出與刪除你的 AI 對話記錄 · ai, tutorial · 圖：插 · 易變
15. `ai-token-cost-estimation` · token 計算與費用估算 · ai, tutorial · 圖：插 · 易變
16. `ai-open-vs-closed-models` · 開源 vs 閉源模型：對使用者的差別 · ai · 圖：插
17. `ai-taiwan-local-models-taide` · 台灣的本土模型：TAIDE 與繁中表現 · ai · 圖：插 · 易變
18. `ai-companion-mental-health-caution` · AI 陪伴與心理健康：可以與不可以 · ai, daily · 圖：插
19. `ai-news-sources-to-follow` · 追 AI 新聞的來源清單 · ai, misc · 圖：插
20. `ai-hype-vs-reality-2026` · AI 能與不能：2026 年的誠實盤點 · ai, misc · 圖：插 · 易變

- [x] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [x] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [x] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。

## Outcome (2026-09-15)

- 二十篇全部落地：`apps/api/app/guides/content/<slug>.json` 與 `apps/web/public/guides/<slug>/{hero.jpg,hero.svg,diagram-1.svg}`，slug 照 scope 清單；每篇一張自繪 hero（jpg 最大 72 KB）與一張 1600×900 自繪圖解，全部渲染成 PNG 人工看過。總表唯一標「照」的家長指南一律改自繪；沒有任何 logo、字標或介面截圖。
- 檢查：`pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md` 0 error（warning 只有既有的 `pack_not_in_catalogue`、舊批次的 `text_length`、尚未寫的批次 11–12 `catalogue_missing_pack`，以及 `sitemap_budget`：本批落地後 repo 內 (article, locale) 列數 1,037，仍超過共用 sitemap 的 1,000 列上限，由 `2026-09-14-sitemap-split-before-1000-rows`／`2026-09-14-guide-sitemap-capacity` 處理）；`test_guides_content_pack.py` 與 `test_guide_partner_links.py` 全綠；`npm run check:tasks` 通過。
- 來源：每篇 12–20 筆、共 378 筆，`checked_on` 全為 2026-09-15，只用廠商定價頁與說明中心、系統卡／模型卡 PDF、官方 RSS、法規資料庫（全國法規資料庫、EUR-Lex 條號經執委會 AI Act Service Desk）、智財局函釋、裁判書系統、警政署／刑事局／衛福部／教育部官方頁；沒有任何合作連結。法律與心理健康兩類只引原文、不下法律或醫療結論，危機情境一律導向 1925／1995／110／119。
- 審稿：每篇跑 `life_links`、dry-run、文字 dump、圖解與 hero 目視，再用 curl／WebFetch／pypdf 逐篇抽查 8–20 個數字與引文；二十篇全部一次通過，沒有退回寫手。審稿只改三處小字：歐盟法案表格 caption「EUR-Lex 條號」→「Regulation (EU) 2024/1689 條號」（當天 EUR-Lex 讀不到）、TAIDE 組織頁那句改為「這 9 個在組織頁上都找得到，另有幾個以代號命名的倉庫」（HF API 另列 4 個 gated=manual 的代號倉庫）、AI 陪伴篇 OpenAI 使用政策句加「現行條文以官網為準」（原文取自 Wayback 2026-07-01 快照）。審稿記錄在 session scratchpad 的 `life10/review-log.md`。
- 與指派不同、寫手照當天官網改寫的事實（重點）：ChatGPT 代理模式已「no longer available」（改寫成 ChatGPT Work）、Sora 2026-04-26 停止服務／API 2026-09-24；ChatGPT Go 美國 8 美元只能由 Wayback 2026-09-03 快照覆核；LMArena 網域改為 arena.ai、政策頁 2026-09-01 更新；OpenAI AI 文字分類器頁 2023-07-20 下架（Wayback 2026-08-19 快照）；Gemini API 2026-05-07 起封鎖閒置金鑰、2026 年 9 月起拒絕標準金鑰；Grok 官方文件自稱「SpaceXAI」；DeepSeek V4-Flash 退場；人工智慧基本法 115-01-14 公布（全文無「著作」二字）、個資法 114-11-11 修正尚未生效；Character.AI 未滿 18 歲開放式聊天 2025-11-24 起在美國關閉，台灣時程官方沒寫。五篇標題依內容改寫（跑分、大事記、偵測工具、token 費用、新聞來源），總表已同步。
- 讀法：openai.com／platform.openai.com 全站 403，改讀 help.openai.com 的 `<id>-<slug>.json`、developers.openai.com 的 `.md`、`openai.com/news/rss.xml`、deploymentsafety.openai.com 與 Wayback（`web.archive.org/web/<ts>id_/`，連線常被 reset 要重試）；iea.org 403 走 Wayback；EUR-Lex 只回 202 空頁，條文改讀 ai-act-service-desk.ec.europa.eu；opensource.org 與 perplexity.ai 403（後者未引用）；taide.tw 302 到 taide.stpi.niar.org.tw；judicial.gov.tw 裁判書用 `FJUD/data.aspx?ty=JD&id=…` 直讀；law.moj.gov.tw 偶發「Unreachable Server」、taipower.com.tw 連線 reset 要重試；Character.AI 說明中心走 Zendesk API `.json`；Meta 條款用 WebFetch；教育部 pads.moe.edu.tw 的 PDF 要補 TWCA 中繼憑證；HF gated 倉庫用 `huggingface.co/api/models/<repo>` 讀授權與 extra_gated_prompt；PDF 用 `uv run --no-project --isolated --with pypdf` 讀。sources 一律記轉址後網址。
- 撰稿代理：20 個 Opus 代理、一篇一個、同時最多七個，每個 20–40 分鐘、20 萬–34 萬 token；本批沒有撞到額度。兩個代理把 `_raw/` 留在交件目錄、一個代理短暫把暫存 HTML 寫進 repo 根目錄，都在審稿時清掉，`git status` 只含這二十篇。
- 部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，確認後再 `--publish`；發布前先處理 sitemap 拆分。
