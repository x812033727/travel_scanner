---
id: 2026-09-13-life-ai-batch-01
title: 生活分享 AI 系列批次 01：AI 入門與各工具總覽（先寫，之後每篇深入文都連回這 20 篇）（20 篇）
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T12:12:19Z
created_at: 2026-09-13T11:55:58Z
completed_at: 2026-09-13T13:04:39Z
branch: claude/festive-brown-6nsxfm
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
scope:
  - apps/api/app/guides/content/ai-tools-2026-overview.json
  - apps/api/app/guides/content/what-is-a-large-language-model.json
  - apps/api/app/guides/content/chatgpt-beginner-guide.json
  - apps/api/app/guides/content/claude-beginner-guide.json
  - apps/api/app/guides/content/gemini-beginner-guide.json
  - apps/api/app/guides/content/codex-beginner-guide.json
  - apps/api/app/guides/content/minimax-beginner-guide.json
  - apps/api/app/guides/content/deepseek-beginner-guide.json
  - apps/api/app/guides/content/ai-chat-prompt-basics.json
  - apps/api/app/guides/content/ai-hallucination-fact-check.json
  - apps/api/app/guides/content/ai-context-window-explained.json
  - apps/api/app/guides/content/ai-model-tiers-explained.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/api/app/guides/content/ai-privacy-settings-checklist.json
  - apps/api/app/guides/content/ai-for-seniors-first-steps.json
  - apps/api/app/guides/content/ai-for-students-honest-use.json
  - apps/api/app/guides/content/ai-agents-explained.json
  - apps/api/app/guides/content/ai-reasoning-models-explained.json
  - apps/api/app/guides/content/ai-glossary-50-terms.json
  - apps/api/app/guides/content/ai-tools-choose-by-task.json
  - apps/web/public/guides/ai-tools-2026-overview
  - apps/web/public/guides/what-is-a-large-language-model
  - apps/web/public/guides/chatgpt-beginner-guide
  - apps/web/public/guides/claude-beginner-guide
  - apps/web/public/guides/gemini-beginner-guide
  - apps/web/public/guides/codex-beginner-guide
  - apps/web/public/guides/minimax-beginner-guide
  - apps/web/public/guides/deepseek-beginner-guide
  - apps/web/public/guides/ai-chat-prompt-basics
  - apps/web/public/guides/ai-hallucination-fact-check
  - apps/web/public/guides/ai-context-window-explained
  - apps/web/public/guides/ai-model-tiers-explained
  - apps/web/public/guides/ai-free-vs-paid-plans-2026
  - apps/web/public/guides/ai-privacy-settings-checklist
  - apps/web/public/guides/ai-for-seniors-first-steps
  - apps/web/public/guides/ai-for-students-honest-use
  - apps/web/public/guides/ai-agents-explained
  - apps/web/public/guides/ai-reasoning-models-explained
  - apps/web/public/guides/ai-glossary-50-terms
  - apps/web/public/guides/ai-tools-choose-by-task
---

# 生活分享 AI 系列批次 01：AI 入門與各工具總覽（先寫，之後每篇深入文都連回這 20 篇）（20 篇）

## Why

`docs/life-ai-series.md` 的批次 01。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
分十一批產出；這張票是其中一批，scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

批次 01 是試點：這二十篇是各工具的入門與總覽，之後每一篇深入文都會連回來，所以先寫；做完把學到的寫回
`docs/life-ai-series-brief.md` 與總表的「經驗記錄」，02 起才開工。

## Definition of done

- [x] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [x] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [x] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [x] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 合作 · 易變）：

1. `ai-tools-2026-overview` · 2026 年 AI 工具全景：ChatGPT、Claude、Gemini、Codex、MiniMax 一次看懂 · ai, misc · 圖：插 · 易變
2. `what-is-a-large-language-model` · 大型語言模型是什麼：用白話解釋 token、上下文與幻覺 · ai, tutorial · 圖：插
3. `chatgpt-beginner-guide` · ChatGPT 新手入門：註冊、免費與付費差別、第一個對話 · ai, tutorial · 圖：插 · 易變
4. `claude-beginner-guide` · Claude 新手入門：Anthropic 的 AI 助手怎麼用、和 ChatGPT 差在哪 · ai, tutorial · 圖：插 · 易變
5. `gemini-beginner-guide` · Gemini 新手入門：有 Google 帳號就能用，Gmail、Docs 裡怎麼叫出來 · ai, tutorial · 圖：插 · 易變
6. `codex-beginner-guide` · OpenAI Codex 是什麼：從 ChatGPT 裡的寫程式代理到 Codex CLI · ai, software · 圖：插 · 易變
7. `minimax-beginner-guide` · MiniMax 是什麼：海螺 AI、影片與語音生成，台灣使用者怎麼用 · ai, software · 圖：插 · 易變
8. `deepseek-beginner-guide` · DeepSeek 是什麼：免費、開源與資料流向，用之前先知道的事 · ai, software · 圖：插 · 易變
9. `ai-chat-prompt-basics` · 提示詞入門：把問題問清楚的五個原則 · ai, tutorial · 圖：插
10. `ai-hallucination-fact-check` · AI 為什麼會一本正經地胡說：幻覺的成因與查證方法 · ai, tutorial · 圖：插
11. `ai-context-window-explained` · 上下文視窗是什麼：為什麼聊久了 AI 會忘記前面 · ai, tutorial · 圖：插
12. `ai-model-tiers-explained` · 同一家為什麼有好幾個模型：旗艦、中階、輕量怎麼選 · ai · 圖：插 · 易變
13. `ai-free-vs-paid-plans-2026` · 免費版夠不夠用：ChatGPT、Claude、Gemini 付費方案比較（2026） · ai, software · 圖：插 · 易變
14. `ai-privacy-settings-checklist` · 用 AI 前先關這些：ChatGPT、Claude、Gemini 的資料訓練與隱私設定 · ai, tutorial · 圖：插 · 易變
15. `ai-for-seniors-first-steps` · 長輩的第一堂 AI 課：用語音跟 AI 聊天、查資料、寫訊息 · ai, daily · 圖：照
16. `ai-for-students-honest-use` · 學生怎麼用 AI 不踩線：學習、整理筆記與學術誠信 · ai, daily · 圖：照
17. `ai-agents-explained` · AI 代理（Agent）是什麼：從回答問題到替你完成任務 · ai, tutorial · 圖：插
18. `ai-reasoning-models-explained` · 推理模型是什麼：o 系列、延伸思考、Deep Think 的差別 · ai, tutorial · 圖：插 · 易變
19. `ai-glossary-50-terms` · AI 名詞速查：50 個常見詞彙一次搞懂 · ai, misc · 圖：插
20. `ai-tools-choose-by-task` · 依任務選工具：寫作、翻譯、程式、圖片、研究各用哪一個 · ai, productivity · 圖：插 · 易變

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

## Outcome (2026-09-13)

- 二十篇全部進 `apps/api/app/guides/content/`，`guides-pack lint --kind life` 零 error 零 warning，`test_guides_content_pack.py` 全綠；
  每篇的 hero 與圖解都渲染成 PNG 人工看過。十八篇 hero 是自繪插圖，兩篇（長輩、學生）是 Commons CC BY 2.0 照片（無正面人臉、無 logo）。
- 產製：一篇一個撰稿代理、同時七個，每篇約 15–22 分鐘、14 萬到 28 萬 token，這次沒有代理被額度切斷；每篇 sources 10–20 筆，
  全部是供應商官網、help center、官方文件、法規或一手來源，`checked_on` 皆為 2026-09-13。
- 代理自己的 dry-run 很好用，但 Codex 那篇的代理跑了不帶 `--dry-run` 的 ingest 再「清理」，剛好刪掉協調者已收進去的檔案；
  brief 第 3 節現在明寫只准 `--dry-run`、不碰 repo 檔案。
- 三件在 brief 補上的規則：`alt` ≤ 200 字（三篇被 pydantic 擋下，用 `trim_alt.py` 截短後重收）；系列統一用語
  （一篇用了 Google 譯名「詞元」「脈絡窗口」，已改回 token、上下文視窗）；`hero.svg` 少字。
- 站內連結：收完後用腳本把 102 個 life→life 的 `link` 文字統一成目標文章的實際標題（代理寫連結時只知道總表標題）；
  下一批可考慮把這步做進 `lint`。
- 一張圖解的英文副標壓到框邊（長輩篇），渲染後才看得出來——機械檢查抓不到排版，人工看圖這步不能省。
- `npm run test:tools` 有一個既有的失敗（`airline-chrome-crawler.test.mjs` 需要 `@playwright/test`，本環境沒裝 web 的 node_modules），與本批無關。
- 部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，確認二十篇為 create，再 `--publish`；
  `/zh-TW/life` 應列出二十篇，總覽篇 `featured: true`、`display_order: 10`。
