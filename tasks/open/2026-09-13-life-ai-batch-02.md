---
id: 2026-09-13-life-ai-batch-02
title: 生活分享 AI 系列批次 02：ChatGPT 教學（20 篇）
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T13:06:09Z
created_at: 2026-09-13T11:55:59Z
completed_at:
branch: claude/festive-brown-6nsxfm
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/chatgpt-plans-plus-pro-2026.json
  - apps/api/app/guides/content/chatgpt-projects-guide.json
  - apps/api/app/guides/content/chatgpt-custom-instructions-memory.json
  - apps/api/app/guides/content/chatgpt-voice-mode-guide.json
  - apps/api/app/guides/content/chatgpt-deep-research-guide.json
  - apps/api/app/guides/content/chatgpt-file-upload-analysis.json
  - apps/api/app/guides/content/chatgpt-image-generation-guide.json
  - apps/api/app/guides/content/chatgpt-canvas-writing.json
  - apps/api/app/guides/content/chatgpt-custom-gpts-build.json
  - apps/api/app/guides/content/chatgpt-search-vs-google.json
  - apps/api/app/guides/content/chatgpt-agent-mode-guide.json
  - apps/api/app/guides/content/chatgpt-mobile-app-tips.json
  - apps/api/app/guides/content/chatgpt-for-email-writing.json
  - apps/api/app/guides/content/chatgpt-for-excel-formulas.json
  - apps/api/app/guides/content/chatgpt-for-english-learning.json
  - apps/api/app/guides/content/chatgpt-for-resume-cover-letter.json
  - apps/api/app/guides/content/chatgpt-data-analysis-csv.json
  - apps/api/app/guides/content/chatgpt-shared-links-privacy.json
  - apps/api/app/guides/content/chatgpt-troubleshooting-common-errors.json
  - apps/api/app/guides/content/chatgpt-team-for-small-business.json
  - apps/web/public/guides/chatgpt-plans-plus-pro-2026
  - apps/web/public/guides/chatgpt-projects-guide
  - apps/web/public/guides/chatgpt-custom-instructions-memory
  - apps/web/public/guides/chatgpt-voice-mode-guide
  - apps/web/public/guides/chatgpt-deep-research-guide
  - apps/web/public/guides/chatgpt-file-upload-analysis
  - apps/web/public/guides/chatgpt-image-generation-guide
  - apps/web/public/guides/chatgpt-canvas-writing
  - apps/web/public/guides/chatgpt-custom-gpts-build
  - apps/web/public/guides/chatgpt-search-vs-google
  - apps/web/public/guides/chatgpt-agent-mode-guide
  - apps/web/public/guides/chatgpt-mobile-app-tips
  - apps/web/public/guides/chatgpt-for-email-writing
  - apps/web/public/guides/chatgpt-for-excel-formulas
  - apps/web/public/guides/chatgpt-for-english-learning
  - apps/web/public/guides/chatgpt-for-resume-cover-letter
  - apps/web/public/guides/chatgpt-data-analysis-csv
  - apps/web/public/guides/chatgpt-shared-links-privacy
  - apps/web/public/guides/chatgpt-troubleshooting-common-errors
  - apps/web/public/guides/chatgpt-team-for-small-business
---

# 生活分享 AI 系列批次 02：ChatGPT 教學（20 篇）

## Why

`docs/life-ai-series.md` 的批次 02。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
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

1. `chatgpt-plans-plus-pro-2026` · ChatGPT Plus、Pro 與其他方案差在哪：2026 年怎麼選 · ai, software · 圖：插 · 易變
2. `chatgpt-projects-guide` · ChatGPT Projects：把檔案、指令與對話收在一個工作區 · ai, tutorial · 圖：插
3. `chatgpt-custom-instructions-memory` · 自訂指令與記憶功能：讓 ChatGPT 記住你的偏好 · ai, tutorial · 圖：插
4. `chatgpt-voice-mode-guide` · ChatGPT 語音模式：練英文、口說翻譯與免手打 · ai, tutorial · 圖：照
5. `chatgpt-deep-research-guide` · ChatGPT Deep Research：讓 AI 花十分鐘幫你做一份完整研究 · ai, productivity · 圖：插 · 易變
6. `chatgpt-file-upload-analysis` · 上傳 PDF、Excel 給 ChatGPT：分析、摘要與抓重點 · ai, tutorial · 圖：插
7. `chatgpt-image-generation-guide` · ChatGPT 畫圖教學：圖片生成、修圖與風格提示 · ai, tutorial · 圖：插 · 易變
8. `chatgpt-canvas-writing` · ChatGPT Canvas：和 AI 並排改文章、改程式 · ai, tutorial · 圖：插
9. `chatgpt-custom-gpts-build` · 自製 GPT：不用寫程式做出自己的專用助手 · ai, tutorial · 圖：插
10. `chatgpt-search-vs-google` · ChatGPT 搜尋 vs Google：什麼時候該用哪一個 · ai, productivity · 圖：插
11. `chatgpt-agent-mode-guide` · ChatGPT 代理模式：讓它替你上網比價、填表、訂位 · ai, tutorial · 圖：插 · 易變
12. `chatgpt-mobile-app-tips` · ChatGPT 手機 App 十個技巧：拍照提問、捷徑與小工具 · ai, daily · 圖：照
13. `chatgpt-for-email-writing` · 用 ChatGPT 寫 Email：中英文商務信件範本與提示詞 · ai, productivity · 圖：插
14. `chatgpt-for-excel-formulas` · 用 ChatGPT 寫 Excel 公式與 VBA：從問題描述到可貼上的公式 · ai, productivity · 圖：插
15. `chatgpt-for-english-learning` · 用 ChatGPT 學英文：對話練習、糾錯與單字卡 · ai, daily · 圖：插
16. `chatgpt-for-resume-cover-letter` · 用 ChatGPT 改履歷與求職信：改得像自己寫的做法 · ai, productivity · 圖：插
17. `chatgpt-data-analysis-csv` · ChatGPT 資料分析：上傳 CSV 讓它跑程式畫圖表 · ai, tutorial · 圖：插
18. `chatgpt-shared-links-privacy` · ChatGPT 分享連結與隱私：哪些對話可能被搜尋到 · ai, misc · 圖：插
19. `chatgpt-troubleshooting-common-errors` · ChatGPT 常見問題排解：登不進、額度用完、回應中斷 · ai, tutorial · 圖：插 · 易變
20. `chatgpt-team-for-small-business` · 小公司要不要買 ChatGPT Team：資料不訓練、共用 GPT 與管理 · ai, software · 圖：插 · 易變

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
