# AI 字尾關鍵字：「〇〇 AI」搜尋詞對照表

台灣使用者找 AI 工具時，很常把 AI 放在**字尾**打：「翻譯 AI」「簡報 AI」「去背 AI」「履歷 AI」。
生活分享專區的文章標題與描述幾乎全用字首型（「AI 翻譯」「AI 做簡報」），字尾型只出現在
「生成式 AI」「開源 AI」這幾個概念詞裡。這份文件把字尾型搜尋詞列出來，逐一對到站上的文章：
已經寫了的補進描述與導言，總表裡排了還沒寫的交給該批次帶進去，哪裡都沒有的排成批次 12。

規格本身在 [`docs/travel-guides.md`](travel-guides.md)，撰稿指令在
[`docs/life-ai-series-brief.md`](life-ai-series-brief.md)，系列總表在 [`docs/life-ai-series.md`](life-ai-series.md)。

## 目的與讀者

- 讀者是台灣的一般使用者，搜的是「我要做某件事，有沒有 AI 可以用」：動作或物件加 AI，後面常再接
  「推薦」「免費」「App」「教學」。
- 目的不是塞關鍵字。每篇只在 `description` 第一句與導言第一段各出現一次字尾詞，h2 與正文其餘部分不重複；
  `docs/gemini-series/lessons/28.md` 的反塞字立場照舊。
- 「旅遊 AI」「行程 AI」這一組直接對到站的核心產品，總表標 P1：落點文章要帶讀者到站內的攻略與規劃工具。

## 資料來源聲明

- 這份清單**沒有搜尋量、難度或成效數字**：候選詞是編輯依台灣使用者常見的搜尋型態列出來的判斷，
  不是任何工具的匯出。`docs/content-research/two-site-life/batch-05-review.md` 的規則在這裡照用：
  關鍵字工具的競爭度不當排名難度，Trends 指數不當搜尋次數，沒有查過的數字不寫。
- 總表留了「實際查詢」與「曝光」兩欄，全部空白。等 Search Console 有資料再回填：成效 → 查詢 →
  篩選「查詢包含 ai」→ 匯出，把查詢字串貼進「實際查詢」、曝光數貼進「曝光」，並在「經驗記錄」寫下匯出日期。
  在那之前，不要因為這份清單改任何標題。

## 寫法規則

- 用字統一「〇〇 AI」：中文後留一個半形空格再接大寫 AI，和站上「生成式 AI」一致。
- 已寫的文章：`description` 第一句自然帶出字尾詞一次（改寫，不是在句尾附加），長度維持 120–200 字；
  導言第一段加一句含字尾詞的話；標題不改（h1、站內連結文字與兩個系列的目錄都抄自標題，沒有工具會同步）。
  Gemini 51 頁系列的成員（`apps/web/lib/guide-series.json`）正文有 3,000 字硬上限，導言只加一句。
- 新文章：標題以字尾詞開頭（「圖片轉文字 AI：…」），description 第一句與導言各用一次，h2 不重複。
  指派給撰稿代理時把字尾詞寫在指派裡（brief 第 4 節）。
- 一個詞只對一個主要落點；備選落點列在同一列，只在主要落點還沒寫時才由備選承接。

## 狀態怎麼看

- **已寫**：`apps/api/app/guides/content/<slug>.json` 存在，且屬於 `docs/life-ai-series.md` 的系列。
- **已寫（系列外）**：內容包存在，但來自 two-site-life 或 AI 名詞系列，不在 life-ai 總表裡。
- **待批次 NN**：`docs/life-ai-series.md` 排了、內容包還沒有；字尾詞由該批次的指派帶進去。
- **批次 12**：哪裡都沒有，排進 `docs/life-ai-series.md` 的批次 12（本文最後一節）。

已寫落點有沒有真的補到，用這段檢查（在 repo 根目錄）：

```bash
python3 - <<'PY'
import json, re
rows = re.findall(r"^\| ([^|]+?) \|[^|]*\|[^|]*\| `([a-z0-9-]+)` \| 已寫", open("docs/ai-suffix-keywords.md", encoding="utf-8").read(), re.M)
for keyword, slug in rows:
    doc = json.load(open(f"apps/api/app/guides/content/{slug}.json", encoding="utf-8"))["locales"]["zh-TW"]
    first = doc["blocks"][0]["text"]
    ok = keyword in doc["description"] and keyword in first and 120 <= len(doc["description"]) <= 200
    print("ok " if ok else "MISS", slug, keyword, len(doc["description"]))
PY
```

## 對照總表

欄位：關鍵字｜變體｜讀者要做的事｜對應 slug（第一個是主要落點）｜狀態｜動作｜實際查詢｜曝光。
「動作」：補描述＝已寫落點的 description 與導言已補；帶入＝寫進該批次指派；批次 12＝新文章。

### 文字與工作

| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 | 動作 | 實際查詢 | 曝光 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 翻譯 AI | 日文翻譯 AI、英文翻譯 AI | 把信件、文件翻成道地中文 | `claude-for-translation-zh-tw` | 已寫 | 補描述 |  |  |
| 網頁翻譯 AI | 翻譯外掛 AI | 讀外文網頁、PDF、字幕 | `immersive-translate-guide` | 已寫（系列外） | 補描述 |  |  |
| 旅行翻譯 AI | 出國翻譯 AI | 出國即時對話翻譯 | `ai-translation-apps-travel` | 待批次 11 | 帶入 |  |  |
| 寫作 AI | 文章 AI、潤稿 AI | 寫出像自己寫的長文 | `claude-writing-style-guide` | 已寫 | 補描述 |  |  |
| 文案 AI | 貼文 AI | 寫商品文案與社群貼文 | `ai-for-social-media-content`；備 `claude-writing-style-guide` | 待批次 09 | 帶入 |  |  |
| 簡報 AI | PPT AI | 把內容做成簡報 | `ai-slides-generation-tools`；備 `gemini-canvas-guide` | 待批次 08 | 帶入（備選已補描述） |  |  |
| 履歷 AI | 求職信 AI | 改履歷與求職信 | `chatgpt-for-resume-cover-letter` | 已寫 | 補描述 |  |  |
| 面試 AI | 模擬面試 AI | 練面試 | `ai-job-interview-practice` | 待批次 11 | 帶入 |  |  |
| Email AI | 寫信 AI | 寫商務信 | `chatgpt-for-email-writing`；`ai-email-management` | 已寫 | 補描述 |  |  |
| Excel AI | 公式 AI | 寫 Excel 公式與巨集 | `chatgpt-for-excel-formulas` | 已寫 | 補描述 |  |  |
| 試算表 AI | Sheets AI | 在 Google Sheets 裡用 AI | `gemini-for-google-sheets-formulas`；`ai-spreadsheet-automation` | 已寫 | 補描述 |  |  |
| Office AI | Word AI、Windows AI | Office 裡的 Copilot | `microsoft-copilot-windows-office` | 已寫 | 補描述 |  |  |
| PDF AI | 讀 PDF AI | 讓 AI 讀 PDF、抓數字 | `ai-pdf-tools-summarize-translate`；備 `chatgpt-file-upload-analysis`、`claude-file-analysis-pdf-excel` | 待批次 09 | 帶入（備選已補描述） |  |  |
| 論文 AI | 摘要 AI、讀論文 AI | 讀論文與長報告 | `claude-for-research-summaries` | 已寫 | 補描述 |  |  |
| 研究 AI | 報告 AI | 做一份附引用的研究 | `chatgpt-deep-research-guide`；`gemini-deep-research-guide` | 已寫 | 補描述 |  |  |
| 筆記 AI | 整理筆記 AI | 把資料整理成筆記 | `ai-note-taking-workflow`；備 `notebooklm-guide` | 待批次 09 | 帶入（備選已補描述） |  |  |
| 讀書 AI | 家教 AI、複習 AI | 用 AI 讀書複習 | `notebooklm-for-study-notes` | 已寫 | 補描述 |  |  |
| 會議記錄 AI | 會議 AI | 會議轉錄與摘要 | `ai-meeting-notes-tools` | 待批次 09 | 帶入 |  |  |
| 逐字稿 AI | 錄音轉文字 AI | 錄音變文字 | `transcription-desktop-tools`；`whisper-local-transcription` | 已寫（系列外） | 補描述（兩篇） |  |  |
| 語音轉文字 AI | 聽打 AI | 了解語音辨識在做什麼 | `ai-term-automatic-speech-recognition` | 已寫（系列外） | 補描述 |  |  |
| 字幕 AI | 上字幕 AI | 替影片上字幕與翻譯 | `ai-video-subtitles-translation` | 待批次 08 | 帶入 |  |  |
| 學英文 AI | 英文 AI、口說 AI | 用 AI 練英文 | `chatgpt-for-english-learning`；`chatgpt-voice-mode-guide`；`ai-language-learning-apps` | 已寫 | 補描述 |  |  |
| 口說 AI | 口譯 AI | 用語音模式練口說、出國口譯 | `chatgpt-voice-mode-guide` | 已寫 | 補描述 |  |  |
| Gmail AI | 文件 AI | 在 Gmail、Docs 裡用 AI | `gemini-in-gmail-docs-sheets` | 已寫 | 補描述 |  |  |

### 圖片、影片、聲音

| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 | 動作 | 實際查詢 | 曝光 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 生圖 AI | 繪圖 AI、畫圖 AI | 用文字生成圖片 | `ai-image-tools-overview-2026`；備 `chatgpt-image-generation-guide`、`ai-term-text-to-image` | 待批次 08 | 帶入（備選已補描述） |  |  |
| 畫圖 AI | ChatGPT 畫圖 | 用 ChatGPT 畫圖 | `chatgpt-image-generation-guide` | 已寫 | 補描述 |  |  |
| 修圖 AI | 改圖 AI | 局部修改照片 | `nano-banana-image-editing` | 已寫 | 補描述 |  |  |
| 去背 AI | 圖片放大 AI | 去背與放大 | `ai-remove-background-upscale` | 待批次 08 | 帶入 |  |  |
| 老照片 AI | 照片修復 AI | 修復老照片 | `ai-photo-restoration-old-photos` | 待批次 08 | 帶入 |  |  |
| 商品圖 AI | 商品照 AI | 做商品圖 | `ai-product-photo-for-sellers` | 待批次 08 | 帶入 |  |  |
| Logo AI | 標誌 AI | 做 Logo | `logo-design-tools-budget` | 已寫（系列外） | 補描述 |  |  |
| 影片 AI | 生成影片 AI | 用文字生成影片 | `ai-video-tools-compared`；備 `veo-video-generation-guide` | 待批次 08 | 帶入（備選已補描述） |  |  |
| 影片生成 AI | 文字生影片 AI | 了解影片生成在做什麼 | `ai-term-text-to-video` | 已寫（系列外） | 補描述 |  |  |
| 動畫 AI | 動漫 AI | 生成動畫風格圖 | `ai-art-prompt-styles-reference` | 待批次 08 | 帶入 |  |  |
| 虛擬主播 AI | 數位人 AI | 做虛擬主播影片 | `ai-avatar-video-tools` | 待批次 08 | 帶入 |  |  |
| 配音 AI | 文字轉語音 AI | 把文字變成聲音 | `minimax-speech-tts-guide`；備 `ai-term-text-to-speech` | 已寫 | 補描述（兩篇） |  |  |
| 翻唱 AI | 聲音克隆 AI | 複製聲音 | `ai-voice-cloning-elevenlabs` | 待批次 08 | 帶入 |  |  |
| 作曲 AI | 音樂 AI、做歌 AI | 生成音樂 | `suno-music-generation-guide`；備 `minimax-music-generation` | 待批次 08 | 帶入（備選已補描述） |  |  |
| 3D AI | 3D 模型 AI | 生成 3D 模型 | `ai-3d-model-generation` | 待批次 08 | 帶入 |  |  |
| 換臉 AI | 深偽 AI | 辨識與防範換臉 | `ai-term-deepfake`；`ai-scams-deepfake-taiwan` | 已寫（系列外） | 補描述 |  |  |
| 設計 AI | UI AI | 用 AI 做介面設計 | `ai-design-prompt-workflow` | 已寫（系列外） | 補描述 |  |  |
| Canva AI | Canva 魔法 AI | Canva 裡的 AI 功能 | `canva-ai-features-guide` | 待批次 08 | 帶入 |  |  |

### 程式與網站

| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 | 動作 | 實際查詢 | 曝光 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 寫程式 AI | 程式 AI、coding AI | 選一個寫程式工具 | `ai-coding-tools-overview-2026` | 已寫 | 補描述 |  |  |
| 做網站 AI | 架站 AI | 不會寫程式做網站 | `vibe-coding-first-website`；`lovable-first-project` | 已寫 | 補描述 |  |  |
| 架站 AI | 網站產生 AI | 用 Lovable 做網站 | `lovable-first-project` | 已寫（系列外） | 補描述 |  |  |
| 客服 AI | 聊天機器人 AI | 做客服機器人 | `ai-customer-service-line-bot`；備 `social-chatbot-workflow` | 待批次 09 | 帶入（備選已補描述） |  |  |
| LINE 機器人 AI | LINE bot AI | 做 LINE 機器人 | `ai-build-line-bot-tutorial` | 已寫 | 補描述 |  |  |
| 網站搜尋 AI | 站內搜尋 AI | 替網站加 AI 搜尋 | `ai-site-search-design` | 已寫（系列外） | 補描述 |  |  |

### 生活與裝置

| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 | 動作 | 實際查詢 | 曝光 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **旅遊 AI** | 旅行 AI、行程 AI、旅行規劃 AI | 用 AI 排行程（P1：站的核心產品） | `ai-travel-planning-tools`；備 `gemini-for-travel-planning` | 待批次 11 | 帶入，指派加必寫「站內規劃器入口」（備選已補描述與站內連結） |  |  |
| 記帳 AI | 理財 AI | 用 AI 記帳 | `ai-personal-finance-budgeting` | 待批次 11 | 帶入 |  |  |
| 食譜 AI | 菜單 AI | 排菜單與食譜 | `ai-cooking-recipes-meal-planning` | 待批次 11 | 帶入 |  |  |
| 健身 AI | 減肥 AI、健康 AI | 健身計畫與手錶數據 | `ai-fitness-health-tracking` | 待批次 11 | 帶入 |  |  |
| 購物 AI | 比價 AI | 購物比價 | `ai-shopping-assistant-price-compare` | 待批次 11 | 帶入 |  |  |
| 相簿 AI | 照片整理 AI | 整理相片 | `ai-photo-organizing-apps` | 待批次 11 | 帶入 |  |  |
| 婚禮 AI | 活動 AI | 辦活動 | `ai-event-planning-wedding` | 待批次 11 | 帶入 |  |  |
| 長照 AI | 提醒 AI | 長照提醒與陪伴 | `ai-elderly-care-reminders` | 待批次 11 | 帶入 |  |  |
| 手機 AI | Android AI、iPhone AI | 手機內建 AI | `ai-phone-features-compared`；備 `gemini-on-android-assistant`、`apple-intelligence-guide` | 待批次 11 | 帶入（備選已補描述） |  |  |
| 眼鏡 AI | AI 眼鏡 | 買 AI 眼鏡 | `ai-smart-glasses-2026` | 待批次 11 | 帶入 |  |  |
| 耳機 AI | 翻譯耳機 AI | 即時翻譯耳機 | `ai-earbuds-live-translation` | 待批次 11 | 帶入 |  |  |
| 電腦 AI | 筆電 AI、AI PC | 買 AI 電腦 | `ai-pc-npu-copilot-plus`；`ai-mac-vs-windows` | 待批次 11 | 帶入 |  |  |
| 平板 AI | 筆記平板 AI | 平板加 AI 筆記 | `ai-tablet-note-taking` | 待批次 11 | 帶入 |  |  |
| 顯卡 AI | 顯示卡 AI | 為 AI 選顯卡 | `local-ai-gpu-buying-guide` | 已寫 | 補描述 |  |  |
| 本機 AI | 離線 AI、自架 AI | 在自己電腦跑 AI | `local-llm-why-and-when`；`ollama-getting-started`；`self-host-ai-on-vps` | 已寫 | 補描述（三篇，自架篇用「自架 AI」） |  |  |
| 智慧家庭 AI | 語音助理 AI | 家裡的語音助理 | `ai-smart-home-assistants` | 待批次 11 | 帶入 |  |  |
| LINE AI | LINE 翻譯 AI | LINE 裡的 AI | `line-ai-features-taiwan` | 已寫 | 補描述 |  |  |

### 人群、比較、安全

| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 | 動作 | 實際查詢 | 曝光 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 長輩 AI | 老人 AI | 教爸媽用 AI | `ai-for-seniors-first-steps` | 已寫 | 補描述 |  |  |
| 學生 AI | 作業 AI、作文 AI | 學生怎麼用不踩線 | `ai-for-students-honest-use` | 已寫 | 補描述 |  |  |
| 老師 AI | 教學 AI | 老師備課出題 | `claude-for-teachers-lesson-plans` | 已寫 | 補描述 |  |  |
| 小孩 AI | 兒童 AI | 孩子用 AI 的設定 | `ai-for-kids-parent-guide` | 待批次 10 | 帶入 |  |  |
| 陪伴 AI | 心理 AI、聊天陪伴 AI | AI 陪伴的界線 | `ai-companion-mental-health-caution` | 待批次 10 | 帶入 |  |  |
| 偵測 AI | AI 偵測 | 辨識 AI 生成內容 | `ai-detection-tools-reliability` | 待批次 10 | 帶入 |  |  |
| 詐騙 AI | 假聲音 AI | 防 AI 詐騙 | `ai-scams-deepfake-taiwan`；備 `ai-for-seniors-first-steps` | 待批次 10 | 帶入 |  |  |
| 台灣 AI | 繁中 AI | 台灣本土模型 | `ai-taiwan-local-models-taide` | 待批次 10 | 帶入 |  |  |
| 中國 AI | 中國系 AI | 中國系模型比較 | `chinese-ai-models-comparison` | 已寫 | 補描述 |  |  |
| 小店 AI | 店家 AI | 小店用 AI | `ai-for-small-business-taiwan` | 待批次 09 | 帶入 |  |  |
| 小公司 AI | 企業 AI、公司 AI | 公司買哪個方案 | `chatgpt-team-for-small-business`；`google-workspace-ai-for-small-business` | 已寫 | 補描述 |  |  |
| YouTube AI | 影片創作 AI | YouTuber 工作流 | `ai-for-youtube-creators` | 待批次 09 | 帶入 |  |  |
| 社群 AI | 貼文 AI、IG AI | 做社群貼文 | `ai-for-social-media-content` | 待批次 09 | 帶入 |  |  |
| 免費 AI | 免費 AI 工具 | 免費版夠不夠用 | `ai-free-vs-paid-plans-2026` | 已寫 | 補描述 |  |  |
| 聊天 AI | 對話 AI | 第一次用聊天式 AI | `chatgpt-beginner-guide` | 已寫 | 補描述 |  |  |
| 搜尋 AI | AI 搜尋引擎 | 用 AI 搜尋 | `perplexity-ai-search-guide`；備 `google-ai-mode-search`、`chatgpt-search-vs-google` | 已寫 | 補描述（三篇） |  |  |
| 瀏覽器 AI | Chrome AI | 瀏覽器裡的 AI | `ai-browsers-guide`；備 `claude-in-chrome-browser-agent`、`gemini-in-chrome-guide` | 待批次 09 | 帶入（備選已補描述） |  |  |
| 語音 AI | 講話 AI | 用講的跟 AI 對話 | `gemini-live-voice-camera` | 已寫 | 補描述 |  |  |
| 版權 AI | 著作權 AI | AI 生成內容的版權 | `ai-image-copyright-taiwan`；`ai-and-copyright-law-taiwan` | 待批次 08 | 帶入 |  |  |
| 開源 AI | 開放權重 AI | 開源模型 | `ai-term-open-source-ai`；`ai-open-vs-closed-models` | 已寫（系列外） | 已在標題，不動 |  |  |
| 生成式 AI | 生成 AI | 生成式 AI 是什麼 | `ai-term-generative-ai` | 已寫（系列外） | 已在標題，不動 |  |  |

## 批次 12｜字尾關鍵字補位（11 篇）

哪裡都沒有的字尾詞排成新文章，slug 已對過 `apps/api/app/guides/content`、`docs/life-ai-series.md` 與
`docs/content-research/two-site-life/catalogue.md`。任務票：`2026-09-14-life-ai-batch-12-suffix-keywords`；
總表列在 `docs/life-ai-series.md` 的「批次 12」。

| # | slug | 標題 | 關鍵字 | topics | 圖 | 備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 250 | `ai-tools-by-search-term` | 〇〇 AI 怎麼找：從你會搜的字找到對的工具與教學 | 翻譯 AI、簡報 AI… | ai, misc | 插 | 字尾詞索引 hub，`featured: false`、`display_order: 100`（比照 `ai-terms-index`）；只連已寫的篇 |
| 251 | `ai-image-to-text-ocr` | 圖片轉文字 AI：截圖、掃描件與手寫筆記變成可編輯文字 | 圖片轉文字 AI | ai, tutorial | 插 | 含辨識後核對數字、民國年、個資 |
| 252 | `ai-taiwanese-hokkien-hakka-tools` | 台語 AI 與客語 AI：語音辨識、合成與翻譯工具有哪些、準不準 | 台語 AI | ai, daily | 照 | 只寫查得到官方頁的工具 |
| 253 | `ai-line-sticker-creation` | 貼圖 AI：用 AI 做 LINE 貼圖的生成、去背、審核規則與版權 | 貼圖 AI | ai, daily | 插 | LINE Creators Market 規則以官方頁為準 |
| 254 | `ai-interior-design-visualization` | 裝潢 AI：把房間照片變成設計提案，哪些不能靠 AI | 裝潢 AI | ai, daily | 照 | 尺寸、施工、法規不靠 AI |
| 255 | `ai-id-photo-rules-taiwan` | 證件照 AI：AI 修圖或生成的證件照能不能用，護照與身分證規定 | 證件照 AI | ai, daily | 插 | 來源：外交部領事事務局、內政部 |
| 256 | `ai-naming-brainstorm-checks` | 取名 AI：品牌、公司與商品名的提示詞，以及預查與商標檢索 | 取名 AI | ai, daily | 插 | 經濟部公司名稱預查、智慧局商標檢索 |
| 257 | `ai-fortune-telling-apps-caution` | 算命 AI 在做什麼：生成式回答的原理、個資流向與付費陷阱 | 算命 AI | ai, daily | 插 | 敏感題，待拍板 |
| 258 | `ai-stock-research-boundaries` | 投資 AI 能幫什麼：整理財報與新聞、不能預測漲跌、金管會怎麼管 | 投資 AI | ai, daily | 插 | YMYL，待拍板 |
| 259 | `ai-legal-questions-boundaries` | 法律 AI：法律問題問 AI 能整理什麼、什麼要找律師 | 法律 AI | ai, daily | 插 | YMYL，待拍板 |
| 260 | `ai-health-questions-boundaries` | 健康 AI：症狀整理、看診前準備與它不能取代的事 | 健康 AI | ai, daily | 插 | YMYL，待拍板；與 `ai-news-chatgpt-health-20260107` 是新聞／教學之別 |

257–260 四篇是敏感或 YMYL 題，先列著等站主拍板；不寫就從兩份總表刪掉，不要留 `catalogue_missing_pack`。
其他候選折進既有篇：作文 AI→學生篇、手寫辨識 AI→OCR 篇、聽打 AI→逐字稿篇、減肥 AI→健身篇、頭貼 AI→證件照篇。

## 不做的詞

- 穿搭 AI、試衣 AI：功能地區限制多、查證困難。
- 遊戲 AI、簡訊 AI：沒有讀者任務可寫。
- 隱私 AI、代理 AI、推理 AI：字尾型不自然，讀者用字首型（AI 隱私、AI 代理）；這些主題已有文章。

## 驗證

```bash
npm run check:tasks
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_gemini_series.py -q
npm run test:tools
```

加上「狀態怎麼看」那段檢查。部署後在主機以 slug 限定匯入，不要整批發布：
`python -m app.cli guides-import --actor-email <admin> --locale zh-TW --slug <slug> … --dry-run`，再 `--publish`。

## 經驗記錄

- 2026-09-14：總表建立，61 篇已寫落點補了描述與導言（`tasks/open/2026-09-14-ai-suffix-keywords-backfill.md`）；
  其中 12 篇是批次 06、07 在同一天併入 main 後補的。沒有搜尋量資料；Search Console 匯出日期待記。
