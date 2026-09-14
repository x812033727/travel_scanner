---
id: 2026-09-13-life-ai-batch-06
title: 生活分享 AI 系列批次 06：MiniMax、DeepSeek、Qwen、Kimi、豆包與其他家（20 篇）
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-14T14:55:21Z
created_at: 2026-09-13T11:55:59Z
completed_at:
branch: claude/travel-guides-tutorials-59j1dv
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/minimax-hailuo-video-guide.json
  - apps/api/app/guides/content/minimax-speech-tts-guide.json
  - apps/api/app/guides/content/minimax-music-generation.json
  - apps/api/app/guides/content/minimax-m-series-models-explained.json
  - apps/api/app/guides/content/minimax-agent-guide.json
  - apps/api/app/guides/content/deepseek-chat-and-reasoner.json
  - apps/api/app/guides/content/deepseek-privacy-and-data-flow.json
  - apps/api/app/guides/content/deepseek-local-with-ollama.json
  - apps/api/app/guides/content/qwen-alibaba-models-guide.json
  - apps/api/app/guides/content/kimi-moonshot-guide.json
  - apps/api/app/guides/content/doubao-bytedance-guide.json
  - apps/api/app/guides/content/chinese-ai-models-comparison.json
  - apps/api/app/guides/content/chinese-ai-apps-security-checklist.json
  - apps/api/app/guides/content/mistral-le-chat-guide.json
  - apps/api/app/guides/content/grok-xai-guide.json
  - apps/api/app/guides/content/perplexity-ai-search-guide.json
  - apps/api/app/guides/content/microsoft-copilot-windows-office.json
  - apps/api/app/guides/content/meta-ai-whatsapp-instagram.json
  - apps/api/app/guides/content/apple-intelligence-guide.json
  - apps/api/app/guides/content/line-ai-features-taiwan.json
  - apps/web/public/guides/minimax-hailuo-video-guide
  - apps/web/public/guides/minimax-speech-tts-guide
  - apps/web/public/guides/minimax-music-generation
  - apps/web/public/guides/minimax-m-series-models-explained
  - apps/web/public/guides/minimax-agent-guide
  - apps/web/public/guides/deepseek-chat-and-reasoner
  - apps/web/public/guides/deepseek-privacy-and-data-flow
  - apps/web/public/guides/deepseek-local-with-ollama
  - apps/web/public/guides/qwen-alibaba-models-guide
  - apps/web/public/guides/kimi-moonshot-guide
  - apps/web/public/guides/doubao-bytedance-guide
  - apps/web/public/guides/chinese-ai-models-comparison
  - apps/web/public/guides/chinese-ai-apps-security-checklist
  - apps/web/public/guides/mistral-le-chat-guide
  - apps/web/public/guides/grok-xai-guide
  - apps/web/public/guides/perplexity-ai-search-guide
  - apps/web/public/guides/microsoft-copilot-windows-office
  - apps/web/public/guides/meta-ai-whatsapp-instagram
  - apps/web/public/guides/apple-intelligence-guide
  - apps/web/public/guides/line-ai-features-taiwan
---

# 生活分享 AI 系列批次 06：MiniMax、DeepSeek、Qwen、Kimi、豆包與其他家（20 篇）

## Why

`docs/life-ai-series.md` 的批次 06。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
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

1. `minimax-hailuo-video-guide` · MiniMax 海螺影片生成教學 · ai, tutorial · 圖：插 · 易變
2. `minimax-speech-tts-guide` · MiniMax 語音合成：中文配音與有聲書 · ai, tutorial · 圖：插 · 易變
3. `minimax-music-generation` · MiniMax 音樂生成怎麼用 · ai, tutorial · 圖：插 · 易變
4. `minimax-m-series-models-explained` · MiniMax M 系列模型：開源權重與 API · ai · 圖：插 · 易變
5. `minimax-agent-guide` · MiniMax Agent：一句話做出網頁與報告 · ai, tutorial · 圖：插 · 易變
6. `deepseek-chat-and-reasoner` · DeepSeek 對話與推理模式怎麼用 · ai, tutorial · 圖：插 · 易變
7. `deepseek-privacy-and-data-flow` · DeepSeek 資料去哪裡：隱私、審查與台灣使用者的取捨 · ai, misc · 圖：插
8. `deepseek-local-with-ollama` · 在自己電腦跑 DeepSeek：Ollama 蒸餾版教學 · ai, tutorial · 圖：插 · 易變
9. `qwen-alibaba-models-guide` · 通義千問 Qwen：開源模型家族與 Qwen Chat · ai · 圖：插 · 易變
10. `kimi-moonshot-guide` · Kimi（月之暗面）：長文件與 K 系列模型 · ai · 圖：插 · 易變
11. `doubao-bytedance-guide` · 豆包（字節跳動）：功能與台灣可用性 · ai · 圖：插 · 易變
12. `chinese-ai-models-comparison` · 中國系 AI 模型比較：DeepSeek、Qwen、Kimi、豆包、MiniMax · ai · 圖：插 · 易變
13. `chinese-ai-apps-security-checklist` · 使用中國系 AI App 前的資安檢查清單 · ai, misc · 圖：插
14. `mistral-le-chat-guide` · Mistral Le Chat：歐洲的 AI 助手 · ai · 圖：插 · 易變
15. `grok-xai-guide` · Grok（xAI）：X 上的 AI 助手與注意事項 · ai · 圖：插 · 易變
16. `perplexity-ai-search-guide` · Perplexity：AI 搜尋引擎入門 · ai, productivity · 圖：插 · 易變
17. `microsoft-copilot-windows-office` · Microsoft Copilot：Windows 與 Office 裡的 AI · ai, software · 圖：插 · 易變
18. `meta-ai-whatsapp-instagram` · Meta AI：WhatsApp、Instagram 裡的 AI 與隱私 · ai, daily · 圖：插 · 易變
19. `apple-intelligence-guide` · Apple Intelligence：iPhone、Mac 上的 AI 功能與中文支援 · ai, gadgets · 圖：照 · 易變
20. `line-ai-features-taiwan` · LINE 裡的 AI：聊天、翻譯與台灣可用功能 · ai, daily · 圖：照 · 易變

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
