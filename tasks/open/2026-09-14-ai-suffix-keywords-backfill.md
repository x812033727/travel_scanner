---
id: 2026-09-14-ai-suffix-keywords-backfill
title: 字尾關鍵字補進 61 篇既有 AI 文章的 description 與導言
status: review
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-14T23:06:59Z
created_at: 2026-09-14T23:06:58Z
completed_at:
branch: claude/ai-suffix-keyword-planning-76gn21
depends_on: []
scope:
  - apps/api/app/guides/content/ai-tools-choose-by-task.json
  - apps/api/app/guides/content/claude-for-translation-zh-tw.json
  - apps/api/app/guides/content/immersive-translate-guide.json
  - apps/api/app/guides/content/claude-writing-style-guide.json
  - apps/api/app/guides/content/chatgpt-for-resume-cover-letter.json
  - apps/api/app/guides/content/chatgpt-for-email-writing.json
  - apps/api/app/guides/content/chatgpt-for-excel-formulas.json
  - apps/api/app/guides/content/gemini-for-google-sheets-formulas.json
  - apps/api/app/guides/content/chatgpt-file-upload-analysis.json
  - apps/api/app/guides/content/claude-file-analysis-pdf-excel.json
  - apps/api/app/guides/content/claude-for-research-summaries.json
  - apps/api/app/guides/content/chatgpt-deep-research-guide.json
  - apps/api/app/guides/content/gemini-deep-research-guide.json
  - apps/api/app/guides/content/notebooklm-guide.json
  - apps/api/app/guides/content/notebooklm-for-study-notes.json
  - apps/api/app/guides/content/transcription-desktop-tools.json
  - apps/api/app/guides/content/ai-term-automatic-speech-recognition.json
  - apps/api/app/guides/content/ai-term-text-to-speech.json
  - apps/api/app/guides/content/chatgpt-for-english-learning.json
  - apps/api/app/guides/content/chatgpt-voice-mode-guide.json
  - apps/api/app/guides/content/chatgpt-image-generation-guide.json
  - apps/api/app/guides/content/nano-banana-image-editing.json
  - apps/api/app/guides/content/veo-video-generation-guide.json
  - apps/api/app/guides/content/ai-term-text-to-image.json
  - apps/api/app/guides/content/ai-term-text-to-video.json
  - apps/api/app/guides/content/ai-term-deepfake.json
  - apps/api/app/guides/content/logo-design-tools-budget.json
  - apps/api/app/guides/content/ai-design-prompt-workflow.json
  - apps/api/app/guides/content/ai-coding-tools-overview-2026.json
  - apps/api/app/guides/content/vibe-coding-first-website.json
  - apps/api/app/guides/content/lovable-first-project.json
  - apps/api/app/guides/content/ai-build-line-bot-tutorial.json
  - apps/api/app/guides/content/social-chatbot-workflow.json
  - apps/api/app/guides/content/ai-site-search-design.json
  - apps/api/app/guides/content/gemini-for-travel-planning.json
  - apps/api/app/guides/content/ai-for-seniors-first-steps.json
  - apps/api/app/guides/content/ai-for-students-honest-use.json
  - apps/api/app/guides/content/claude-for-teachers-lesson-plans.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/api/app/guides/content/chatgpt-beginner-guide.json
  - apps/api/app/guides/content/google-ai-mode-search.json
  - apps/api/app/guides/content/chatgpt-search-vs-google.json
  - apps/api/app/guides/content/claude-in-chrome-browser-agent.json
  - apps/api/app/guides/content/gemini-in-chrome-guide.json
  - apps/api/app/guides/content/gemini-on-android-assistant.json
  - apps/api/app/guides/content/gemini-live-voice-camera.json
  - apps/api/app/guides/content/gemini-in-gmail-docs-sheets.json
  - apps/api/app/guides/content/gemini-canvas-guide.json
  - apps/api/app/guides/content/chatgpt-team-for-small-business.json
  - apps/api/app/guides/content/microsoft-copilot-windows-office.json
  - apps/api/app/guides/content/minimax-speech-tts-guide.json
  - apps/api/app/guides/content/minimax-music-generation.json
  - apps/api/app/guides/content/apple-intelligence-guide.json
  - apps/api/app/guides/content/line-ai-features-taiwan.json
  - apps/api/app/guides/content/chinese-ai-models-comparison.json
  - apps/api/app/guides/content/perplexity-ai-search-guide.json
  - apps/api/app/guides/content/whisper-local-transcription.json
  - apps/api/app/guides/content/local-ai-gpu-buying-guide.json
  - apps/api/app/guides/content/local-llm-why-and-when.json
  - apps/api/app/guides/content/ollama-getting-started.json
  - apps/api/app/guides/content/self-host-ai-on-vps.json
---

# 字尾關鍵字補進 61 篇既有 AI 文章的 description 與導言

## Why

`docs/ai-suffix-keywords.md` 對照出 49 篇已經寫好的文章（同日批次 06、07 併入 main 後再加 12 篇，共 61 篇）是「〇〇 AI」字尾詞的落點，但它們的 description 與導言
只有字首型（「AI 翻譯」），搜尋摘要裡看不到讀者實際打的字。這張票把字尾詞補進去：description 第一句改寫成
自然帶出字尾詞一次並落在 120–200 字，導言第一段加一句；標題不動。`ai-search-geo-content` 原本也在清單裡，
但它沒有自然的字尾型搜尋詞（讀者打的是「AI SEO」「GEO」），拿掉了。

## Definition of done

- [x] 61 篇的 `description` 含該篇字尾詞、120–200 字；導言第一段含該詞；`docs/ai-suffix-keywords.md`「狀態怎麼看」那段檢查全部 `ok`。
- [x] 沒有改任何標題、圖片、sources、topics；唯一加區塊的是 `gemini-for-travel-planning`（一個 `link` 到 `https://mokaair.com/zh-TW/guides`）。
- [x] `guides-pack lint --kind life` 沒有 error；`pytest tests/test_guides_content_pack.py tests/test_gemini_series.py` 與 `npm run test:tools` 綠。

## Steps

主要落點先、備選後；改一篇勾一篇：

- [x] 文字與工作：claude-for-translation-zh-tw、claude-writing-style-guide、chatgpt-for-resume-cover-letter、chatgpt-for-email-writing、chatgpt-for-excel-formulas、claude-for-research-summaries、chatgpt-deep-research-guide、chatgpt-for-english-learning、chatgpt-voice-mode-guide、transcription-desktop-tools、notebooklm-for-study-notes、gemini-in-gmail-docs-sheets、gemini-for-google-sheets-formulas、immersive-translate-guide、ai-term-automatic-speech-recognition、gemini-deep-research-guide、notebooklm-guide、chatgpt-file-upload-analysis、claude-file-analysis-pdf-excel、gemini-canvas-guide
- [x] 圖片、影片、聲音：chatgpt-image-generation-guide、nano-banana-image-editing、logo-design-tools-budget、ai-design-prompt-workflow、ai-term-text-to-image、ai-term-text-to-video、ai-term-deepfake、ai-term-text-to-speech、veo-video-generation-guide
- [x] 程式與網站：ai-coding-tools-overview-2026、vibe-coding-first-website、lovable-first-project、ai-build-line-bot-tutorial、social-chatbot-workflow、ai-site-search-design
- [x] 批次 06、07 併入後補的 12 篇：microsoft-copilot-windows-office、minimax-speech-tts-guide、minimax-music-generation、apple-intelligence-guide、line-ai-features-taiwan、chinese-ai-models-comparison、perplexity-ai-search-guide、whisper-local-transcription、local-ai-gpu-buying-guide、local-llm-why-and-when、ollama-getting-started、self-host-ai-on-vps
- [x] 生活、人群、比較：gemini-for-travel-planning（加站內連結）、ai-for-seniors-first-steps、ai-for-students-honest-use、claude-for-teachers-lesson-plans、ai-free-vs-paid-plans-2026、chatgpt-beginner-guide、google-ai-mode-search、chatgpt-search-vs-google、claude-in-chrome-browser-agent、gemini-in-chrome-guide、gemini-on-android-assistant、gemini-live-voice-camera、chatgpt-team-for-small-business、ai-tools-choose-by-task

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_gemini_series.py -q
npm run test:tools && npm run check:tasks
```

加 `docs/ai-suffix-keywords.md`「狀態怎麼看」的 python 檢查。部署後在主機以 `--slug` 限定這 61 篇匯入：
`python -m app.cli guides-import --actor-email <admin> --locale zh-TW --slug … --dry-run`，再 `--publish`；不加 `--slug`
會把批次 06、ai-news 等已合併未發布的一起發出去。

## Notes

- 13 篇是 Gemini 51 頁系列成員（`apps/web/lib/guide-series.json`）：`tools/gemini-series.mjs` 硬性要求正文 1,800–3,000 字，導言只加一句。
  `docs/gemini-series/reviewed-files.json`、`publication-receipt.json`、`public-browser.json` 記的是發布當時的檔案雜湊，自此是歷史紀錄，不重產。
- 5 篇 `ai-term-*` 同理：`docs/ai-terms-series/release-manifest.json` 的 SHA256 是發布當時的紀錄；沒有測試或 CI 讀它。
- two-site-life 的 `docs/content-research/two-site-life/catalogue.md` 稽核列指的是舊描述，不改它。
- 現在超過 200 字的六篇（chatgpt-search-vs-google 257、chatgpt-image-generation-guide 226、claude-file-analysis-pdf-excel 212、chatgpt-beginner-guide 209、chatgpt-file-upload-analysis 203、chatgpt-for-english-learning 201）順手縮回；不到 120 的六篇（gemini-for-travel-planning 110、gemini-on-android-assistant 116、veo-video-generation-guide 117、notebooklm-for-study-notes 118、nano-banana-image-editing 119、google-ai-mode-search 119）補到範圍內。

## Outcome (2026-09-14)

- 61 篇的 description 改寫成第一句帶字尾詞、120–200 字（其中 12 篇是批次 06、07 併入 main 之後補的）；導言各加一句（`chatgpt-for-excel-formulas` 改成把字尾詞寫進原句，
  因為加一句會讓正文超過 6,000 字的 lint 警戒線）。`gemini-for-travel-planning` 多一個 `link` 到 `/zh-TW/guides`。
- 檢查：61 篇 description 與導言都含該篇字尾詞；`guides-pack lint --kind life --catalogue` exit 0，warning 與改前相同
  （text_length 不變、pack_not_in_catalogue 不變、sitemap_budget 926）；`pytest tests/test_guides_content_pack.py tests/test_gemini_series.py`
  綠；`npm run test:tools` 52 個全過；`npm run check:tasks` 只剩既有警告。
- 部署後在主機用 `--slug` 限定這 61 篇 `guides-import --dry-run`，再 `--publish`。
