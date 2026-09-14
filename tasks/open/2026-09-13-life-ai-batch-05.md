---
id: 2026-09-13-life-ai-batch-05
title: 生活分享 AI 系列批次 05：Gemini 與 Google 生態（20 篇）
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
  - apps/api/app/guides/content/gemini-plans-ai-pro-ultra-2026.json
  - apps/api/app/guides/content/gemini-in-gmail-docs-sheets.json
  - apps/api/app/guides/content/gemini-gems-custom-assistants.json
  - apps/api/app/guides/content/gemini-deep-research-guide.json
  - apps/api/app/guides/content/gemini-live-voice-camera.json
  - apps/api/app/guides/content/notebooklm-guide.json
  - apps/api/app/guides/content/notebooklm-for-study-notes.json
  - apps/api/app/guides/content/nano-banana-image-editing.json
  - apps/api/app/guides/content/veo-video-generation-guide.json
  - apps/api/app/guides/content/gemini-on-android-assistant.json
  - apps/api/app/guides/content/gemini-in-chrome-guide.json
  - apps/api/app/guides/content/google-ai-mode-search.json
  - apps/api/app/guides/content/gemini-for-google-sheets-formulas.json
  - apps/api/app/guides/content/gemini-api-ai-studio-first-call.json
  - apps/api/app/guides/content/gemini-vs-chatgpt-vs-claude-daily.json
  - apps/api/app/guides/content/gemini-for-travel-planning.json
  - apps/api/app/guides/content/google-workspace-ai-for-small-business.json
  - apps/api/app/guides/content/gemini-privacy-activity-settings.json
  - apps/api/app/guides/content/google-ai-overviews-for-site-owners.json
  - apps/api/app/guides/content/gemini-model-lineup-flash-pro.json
  - apps/web/public/guides/gemini-plans-ai-pro-ultra-2026
  - apps/web/public/guides/gemini-in-gmail-docs-sheets
  - apps/web/public/guides/gemini-gems-custom-assistants
  - apps/web/public/guides/gemini-deep-research-guide
  - apps/web/public/guides/gemini-live-voice-camera
  - apps/web/public/guides/notebooklm-guide
  - apps/web/public/guides/notebooklm-for-study-notes
  - apps/web/public/guides/nano-banana-image-editing
  - apps/web/public/guides/veo-video-generation-guide
  - apps/web/public/guides/gemini-on-android-assistant
  - apps/web/public/guides/gemini-in-chrome-guide
  - apps/web/public/guides/google-ai-mode-search
  - apps/web/public/guides/gemini-for-google-sheets-formulas
  - apps/web/public/guides/gemini-api-ai-studio-first-call
  - apps/web/public/guides/gemini-vs-chatgpt-vs-claude-daily
  - apps/web/public/guides/gemini-for-travel-planning
  - apps/web/public/guides/google-workspace-ai-for-small-business
  - apps/web/public/guides/gemini-privacy-activity-settings
  - apps/web/public/guides/google-ai-overviews-for-site-owners
  - apps/web/public/guides/gemini-model-lineup-flash-pro
---

# 生活分享 AI 系列批次 05：Gemini 與 Google 生態（20 篇）

## Why

`docs/life-ai-series.md` 的批次 05。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
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

1. `gemini-plans-ai-pro-ultra-2026` · Google AI Pro 與 Ultra 方案：包了什麼、和 One 的關係 · ai, software · 圖：插 · 易變
2. `gemini-in-gmail-docs-sheets` · Gemini 在 Gmail、Docs、Sheets 裡怎麼用 · ai, productivity · 圖：插
3. `gemini-gems-custom-assistants` · Gemini Gems：自訂助手教學 · ai, tutorial · 圖：插
4. `gemini-deep-research-guide` · Gemini Deep Research：研究報告怎麼下指令、怎麼驗證 · ai, productivity · 圖：插
5. `gemini-live-voice-camera` · Gemini Live：語音對話與開鏡頭問問題 · ai, daily · 圖：照
6. `notebooklm-guide` · NotebookLM 入門：把資料丟進去，生成摘要與語音導覽 · ai, productivity · 圖：插
7. `notebooklm-for-study-notes` · 用 NotebookLM 讀書：考試筆記與問答 · ai, daily · 圖：插
8. `nano-banana-image-editing` · Nano Banana 修圖教學：Gemini 的圖片生成與編輯 · ai, tutorial · 圖：插 · 易變
9. `veo-video-generation-guide` · Veo 影片生成入門：提示、長度與費用 · ai, tutorial · 圖：插 · 易變
10. `gemini-on-android-assistant` · Android 手機上的 Gemini：取代 Google 助理後怎麼用 · ai, gadgets · 圖：照
11. `gemini-in-chrome-guide` · Chrome 裡的 Gemini：整理分頁、摘要網頁 · ai, software · 圖：插 · 易變
12. `google-ai-mode-search` · Google 搜尋的 AI 模式與 AI 摘要：怎麼用、怎麼關 · ai, daily · 圖：插 · 易變
13. `gemini-for-google-sheets-formulas` · 用 Gemini 寫 Sheets 公式與整理資料 · ai, productivity · 圖：插
14. `gemini-api-ai-studio-first-call` · Google AI Studio 與 Gemini API：免費額度與第一次呼叫 · ai, tutorial · 圖：插 · 易變
15. `gemini-vs-chatgpt-vs-claude-daily` · 三大助手日常任務實測：Gemini、ChatGPT、Claude · ai · 圖：插 · 易變
16. `gemini-for-travel-planning` · 用 Gemini 規劃旅行：地圖、航班與行程整合 · ai, daily · 圖：插
17. `google-workspace-ai-for-small-business` · 小公司的 Google Workspace AI：值不值得升級 · ai, software · 圖：插 · 易變
18. `gemini-privacy-activity-settings` · Gemini 的活動記錄與隱私設定 · ai, misc · 圖：插
19. `google-ai-overviews-for-site-owners` · AI 摘要對網站流量的影響：站長該怎麼做 · ai, misc · 圖：插
20. `gemini-model-lineup-flash-pro` · Gemini 模型家族：Flash、Pro、Nano 怎麼分 · ai · 圖：插 · 易變

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
