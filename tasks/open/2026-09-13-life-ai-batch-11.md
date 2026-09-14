---
id: 2026-09-13-life-ai-batch-11
title: 生活分享 AI 系列批次 11：生活應用、3C 與旅途中的 AI（20 篇）
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
  - apps/api/app/guides/content/ai-travel-planning-tools.json
  - apps/api/app/guides/content/ai-translation-apps-travel.json
  - apps/api/app/guides/content/ai-photo-organizing-apps.json
  - apps/api/app/guides/content/ai-cooking-recipes-meal-planning.json
  - apps/api/app/guides/content/ai-fitness-health-tracking.json
  - apps/api/app/guides/content/ai-personal-finance-budgeting.json
  - apps/api/app/guides/content/ai-smart-home-assistants.json
  - apps/api/app/guides/content/ai-smart-glasses-2026.json
  - apps/api/app/guides/content/ai-earbuds-live-translation.json
  - apps/api/app/guides/content/ai-phone-features-compared.json
  - apps/api/app/guides/content/ai-pc-npu-copilot-plus.json
  - apps/api/app/guides/content/ai-mac-vs-windows.json
  - apps/api/app/guides/content/ai-tablet-note-taking.json
  - apps/api/app/guides/content/ai-language-learning-apps.json
  - apps/api/app/guides/content/ai-job-interview-practice.json
  - apps/api/app/guides/content/ai-event-planning-wedding.json
  - apps/api/app/guides/content/ai-shopping-assistant-price-compare.json
  - apps/api/app/guides/content/ai-elderly-care-reminders.json
  - apps/api/app/guides/content/ai-writing-traditional-chinese-tips.json
  - apps/api/app/guides/content/ai-daily-habits-30-day-challenge.json
  - apps/web/public/guides/ai-travel-planning-tools
  - apps/web/public/guides/ai-translation-apps-travel
  - apps/web/public/guides/ai-photo-organizing-apps
  - apps/web/public/guides/ai-cooking-recipes-meal-planning
  - apps/web/public/guides/ai-fitness-health-tracking
  - apps/web/public/guides/ai-personal-finance-budgeting
  - apps/web/public/guides/ai-smart-home-assistants
  - apps/web/public/guides/ai-smart-glasses-2026
  - apps/web/public/guides/ai-earbuds-live-translation
  - apps/web/public/guides/ai-phone-features-compared
  - apps/web/public/guides/ai-pc-npu-copilot-plus
  - apps/web/public/guides/ai-mac-vs-windows
  - apps/web/public/guides/ai-tablet-note-taking
  - apps/web/public/guides/ai-language-learning-apps
  - apps/web/public/guides/ai-job-interview-practice
  - apps/web/public/guides/ai-event-planning-wedding
  - apps/web/public/guides/ai-shopping-assistant-price-compare
  - apps/web/public/guides/ai-elderly-care-reminders
  - apps/web/public/guides/ai-writing-traditional-chinese-tips
  - apps/web/public/guides/ai-daily-habits-30-day-challenge
---

# 生活分享 AI 系列批次 11：生活應用、3C 與旅途中的 AI（20 篇）

## Why

`docs/life-ai-series.md` 的批次 11。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
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

1. `ai-travel-planning-tools` · 用 AI 規劃旅行：行程、比價與注意事項 · ai, daily · 圖：照
2. `ai-translation-apps-travel` · 旅行翻譯 App：Google 翻譯、ChatGPT 語音、Gemini Live · ai, daily · 圖：照
3. `ai-photo-organizing-apps` · AI 整理相片：Google 相簿、Apple 照片 · ai, daily · 圖：照
4. `ai-cooking-recipes-meal-planning` · AI 幫你排菜單與食譜 · ai, daily · 圖：照
5. `ai-fitness-health-tracking` · AI 與健康：手錶數據、健身計畫 · ai, gadgets · 圖：照
6. `ai-personal-finance-budgeting` · AI 記帳與理財：注意事項 · ai, daily · 圖：插
7. `ai-smart-home-assistants` · AI 智慧家庭：Home Assistant 與語音助理 · gadgets, ai · 圖：照
8. `ai-smart-glasses-2026` · AI 眼鏡：能做什麼、台灣買得到嗎 · gadgets, ai · 圖：照 · 易變
9. `ai-earbuds-live-translation` · 即時翻譯耳機實測 · gadgets, ai · 圖：照 · 易變
10. `ai-phone-features-compared` · 手機的 AI 功能：Pixel、Galaxy、iPhone · gadgets, ai · 圖：照 · 易變
11. `ai-pc-npu-copilot-plus` · AI PC 與 NPU：Copilot+ PC 值得買嗎 · gadgets, ai · 圖：照 · 易變
12. `ai-mac-vs-windows` · Mac 或 Windows 跑 AI：怎麼選 · gadgets, ai · 圖：照
13. `ai-tablet-note-taking` · 平板＋AI 筆記：Goodnotes、Notability · gadgets, productivity · 圖：照
14. `ai-language-learning-apps` · AI 語言學習 App：Duolingo、Speak · ai, daily · 圖：插 · 易變
15. `ai-job-interview-practice` · AI 模擬面試 · ai, daily · 圖：插
16. `ai-event-planning-wedding` · 用 AI 辦活動：婚禮、生日 · ai, daily · 圖：照
17. `ai-shopping-assistant-price-compare` · AI 購物助理與比價 · ai, daily · 圖：插 · 易變
18. `ai-elderly-care-reminders` · 長照與 AI：提醒、陪伴 · ai, daily · 圖：照
19. `ai-writing-traditional-chinese-tips` · 讓 AI 寫出道地繁體中文：避免簡體用語 · ai, tutorial · 圖：插
20. `ai-daily-habits-30-day-challenge` · 30 天 AI 習慣挑戰 · ai, daily · 圖：插

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
