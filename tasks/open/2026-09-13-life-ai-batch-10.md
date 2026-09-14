---
id: 2026-09-13-life-ai-batch-10
title: 生活分享 AI 系列批次 10：比較、費用、資安與法律（20 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-13T11:56:00Z
completed_at:
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

- [ ] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [ ] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [ ] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [ ] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

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
