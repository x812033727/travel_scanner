# 生活分享：AI 工具介紹與教學系列（260 篇總表）

這份文件是「生活分享」（`kind: "life"`，`/{locale}/life/{slug}`）AI 系列的**編輯總表**：每一篇
的 slug、標題、主題、配圖方式與合作連結在這裡定死，批次任務票的 `scope` 才能精確到檔案。
規格本身在 [`docs/travel-guides.md`](travel-guides.md)（內容包格式、圖片與文字規則、合作連結）；
撰稿代理拿到的指令在 [`docs/life-ai-series-brief.md`](life-ai-series-brief.md)。

## 目的與讀者

站主要用一批與旅遊無關、可索引的自有文章換曝光，文末再把讀者導向旅遊情報攻略與目的地頁
（`docs/travel-guides.md`「What this is」）。讀者是台灣的一般使用者：會用手機和電腦，想知道
ChatGPT、Claude、Gemini、Codex、MiniMax 這些東西是什麼、怎麼開始、要花多少錢、哪裡要小心；
工程師向的內容只到「第一次呼叫 API」和「用 AI 寫程式工具做出東西」為止。

## 政策

- **語系：只寫 zh-TW。** 五語系共用一個 1,000 列的 sitemap 額度（`docs/travel-guides.md`「Still open」），
  今天約 110 列；220 篇 zh-TW 加進去約 330 列。其他語系要等 sitemap 拆分後再議。
- **配圖：自繪插圖與 Commons 照片混用。** hero 必須是點陣圖（`HERO_SRC_PATTERN`），所以自繪 hero 由
  `guides-pack ingest` 把 `hero.svg` 渲染成 1600×900 的 `hero.jpg`；有實物可拍（鍵盤、顯示卡、手上的手機）
  時用 Wikimedia Commons 的 CC0／PD／CC BY／CC BY-SA 照片。**產品 logo、字標、圖示、吉祥物與介面截圖一律不用。**
  總表「圖」欄：插＝自繪 hero 插圖，照＝Commons 照片；每篇另有至少一張自繪 SVG 圖解。
- **合作連結：** 只有 `partner_link` 區塊、只限 `CONTENT_PARTNERS` 登錄的程式（H＝Hostinger、B＝博客來），
  只放在文章真的用到該產品的段落，每篇最多三個。總表沒標的篇不放。
- **事實：** 方案、價格、模型名、額度都在寫作當天查供應商官網並在 `sources` 記 `checked_on`；查不到的寫
  「以官網為準」。「易變」欄打勾的篇要定期回查（`valid_until` 維持 null，life 文章不走到期邏輯）。
- **主題：** 只用 life 詞彙（`ai`、`tutorial`、`software`、`gadgets`、`productivity`、`daily`、`misc`）；
  `destination_id` 一律 null。
- **字尾關鍵字：** 「翻譯 AI」「簡報 AI」這類字尾型搜尋詞的對照、寫法與批次 12 的由來見
  [`docs/ai-suffix-keywords.md`](ai-suffix-keywords.md)；已寫的篇只補 description 與導言，不改標題。

## 狀態怎麼看

總表不記錄「寫了沒」。`apps/api/app/guides/content/<slug>.json` 存在就是寫了；

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
```

會列出總表有、內容包沒有的 slug（還沒寫）與內容包有、總表沒有的 slug（該補進總表）。批次完成後不必回頭改這份檔案。

## 批次與任務票

每批 20 篇一張任務票，scope 是該批 20 個內容包檔案加 20 個圖片目錄（`tools/tasks.mjs` 的 scope 比對是
「相同或前綴」，兄弟檔案不互卡，所以兩批可以同時進行）。批次 01 是試點，02 起依賴 01：試點學到的先寫回 brief。

| 批次 | 主題 | 任務票 |
| --- | --- | --- |
| 01 | AI 入門與各工具總覽（先寫，之後每篇深入文都連回這 20 篇） | `2026-09-13-life-ai-batch-01` |
| 02 | ChatGPT 教學 | `2026-09-13-life-ai-batch-02` |
| 03 | Claude 教學 | `2026-09-13-life-ai-batch-03` |
| 04 | AI 寫程式：Claude Code、Codex、Gemini CLI、Cursor、Copilot | `2026-09-13-life-ai-batch-04` |
| 05 | Gemini 與 Google 生態 | `2026-09-13-life-ai-batch-05` |
| 06 | MiniMax、DeepSeek、Qwen、Kimi、豆包與其他家 | `2026-09-13-life-ai-batch-06` |
| 07 | 本機與開源模型 | `2026-09-13-life-ai-batch-07` |
| 08 | 圖片、影片、音樂生成 | `2026-09-13-life-ai-batch-08` |
| 09 | 工作流、效率與自動化 | `2026-09-13-life-ai-batch-09` |
| 10 | 比較、費用、資安與法律 | `2026-09-13-life-ai-batch-10` |
| 11 | 生活應用、3C 與旅途中的 AI | `2026-09-13-life-ai-batch-11` |
| 12 | 字尾關鍵字補位（11 篇，不是 20；`docs/ai-suffix-keywords.md`） | `2026-09-14-life-ai-batch-12-suffix-keywords` |

工具與 brief：`2026-09-13-life-ai-series-tooling`；這份總表：`2026-09-13-life-ai-series-catalogue`。

## 產製流程（每批）

1. 認領批次票，從總表抄出 20 筆指派。
2. 一篇一個撰稿代理（前幾批兩篇一個代理會撞到額度），每波最多七個；代理拿到 brief 全文加五行指派，
   在 scratchpad 的 `<workdir>/<slug>/` 產出 `pack.json`、`diagram-1.svg`、`hero.svg` 或 `images.json`、`notes.md`。
3. 每篇落地就 `guides-pack ingest --from <workdir> --slug <slug>`；被拒的退回該代理修。
4. 全部進來後 `guides-pack lint --kind life --render-dir <dir>`，逐張看渲染出的 PNG：壓線、出框、疊字、logo 都退回重畫。
5. `uv run pytest tests/test_guides_content_pack.py -q`、`npm run check:tasks`，更新任務票，commit。
6. 部署後在主機 `guides-import --dry-run` 再 `--publish`。

## 總表

欄位：編號｜slug｜標題｜topics｜圖（插＝自繪 hero、照＝Commons 照片）｜合作（H＝hostinger、B＝books_com_tw）｜易變。


### 批次 01｜AI 入門與各工具總覽（先寫，之後每篇深入文都連回這 20 篇）

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `ai-tools-2026-overview` | 2026 年 AI 工具全景：ChatGPT、Claude、Gemini、Codex、MiniMax 一次看懂 | ai, misc | 插 |  | ✓ |
| 2 | `what-is-a-large-language-model` | 大型語言模型是什麼：用白話解釋 token、上下文與幻覺 | ai, tutorial | 插 |  |  |
| 3 | `chatgpt-beginner-guide` | ChatGPT 新手入門：註冊、免費與付費差別、第一個對話 | ai, tutorial | 插 |  | ✓ |
| 4 | `claude-beginner-guide` | Claude 新手入門：Anthropic 的 AI 助手怎麼用、和 ChatGPT 差在哪 | ai, tutorial | 插 |  | ✓ |
| 5 | `gemini-beginner-guide` | Gemini 新手入門：有 Google 帳號就能用，Gmail、Docs 裡怎麼叫出來 | ai, tutorial | 插 |  | ✓ |
| 6 | `codex-beginner-guide` | OpenAI Codex 是什麼：從 ChatGPT 裡的寫程式代理到 Codex CLI | ai, software | 插 |  | ✓ |
| 7 | `minimax-beginner-guide` | MiniMax 是什麼：海螺 AI、影片與語音生成，台灣使用者怎麼用 | ai, software | 插 |  | ✓ |
| 8 | `deepseek-beginner-guide` | DeepSeek 是什麼：免費、開源與資料流向，用之前先知道的事 | ai, software | 插 |  | ✓ |
| 9 | `ai-chat-prompt-basics` | 提示詞入門：把問題問清楚的五個原則，改前改後對照著學 | ai, tutorial | 插 |  |  |
| 10 | `ai-hallucination-fact-check` | AI 為什麼會一本正經地胡說：幻覺的成因與查證方法 | ai, tutorial | 插 |  |  |
| 11 | `ai-context-window-explained` | 上下文視窗是什麼：為什麼聊久了 AI 會忘記前面說的話，六個做法讓它記住 | ai, tutorial | 插 |  |  |
| 12 | `ai-model-tiers-explained` | 同一家為什麼有好幾個模型：旗艦、中階、輕量怎麼選 | ai | 插 |  | ✓ |
| 13 | `ai-free-vs-paid-plans-2026` | 免費版夠不夠用：ChatGPT、Claude、Gemini 付費方案比較（2026） | ai, software | 插 |  | ✓ |
| 14 | `ai-privacy-settings-checklist` | 用 AI 前先關這些：ChatGPT、Claude、Gemini 的資料訓練與隱私設定 | ai, tutorial | 插 |  | ✓ |
| 15 | `ai-for-seniors-first-steps` | 長輩的第一堂 AI 課：用語音跟 AI 聊天、查資料、寫訊息 | ai, daily | 照 |  |  |
| 16 | `ai-for-students-honest-use` | 學生怎麼用 AI 不踩線：學習、整理筆記與學術誠信 | ai, daily | 照 |  |  |
| 17 | `ai-agents-explained` | AI 代理（Agent）是什麼：從回答問題到替你完成任務 | ai, tutorial | 插 |  |  |
| 18 | `ai-reasoning-models-explained` | 推理模型是什麼：o 系列、延伸思考、Deep Think 的差別 | ai, tutorial | 插 |  | ✓ |
| 19 | `ai-glossary-50-terms` | AI 名詞速查：50 個常見詞彙一次搞懂 | ai, misc | 插 |  |  |
| 20 | `ai-tools-choose-by-task` | 依任務選 AI 工具：寫作、翻譯、程式、圖片、研究各用哪一個 | ai, productivity | 插 |  | ✓ |

### 批次 02｜ChatGPT 教學

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 21 | `chatgpt-plans-plus-pro-2026` | ChatGPT Plus、Pro 與其他方案差在哪：2026 年怎麼選 | ai, software | 插 |  | ✓ |
| 22 | `chatgpt-projects-guide` | ChatGPT Projects：把檔案、指令與對話收在一個工作區 | ai, tutorial | 插 |  |  |
| 23 | `chatgpt-custom-instructions-memory` | ChatGPT 自訂指令與記憶功能：讓它記住你的偏好，每次都用台灣繁體中文回答 | ai, tutorial | 插 |  |  |
| 24 | `chatgpt-voice-mode-guide` | ChatGPT 語音模式：練英文、口說翻譯與免手打的完整做法 | ai, tutorial | 照 |  |  |
| 25 | `chatgpt-deep-research-guide` | ChatGPT Deep Research：讓 AI 花十分鐘幫你做一份完整研究 | ai, productivity | 插 |  | ✓ |
| 26 | `chatgpt-file-upload-analysis` | 上傳 PDF、Excel 給 ChatGPT：分析、摘要與抓重點 | ai, tutorial | 插 |  |  |
| 27 | `chatgpt-image-generation-guide` | ChatGPT 畫圖教學：圖片生成、修圖與風格提示詞怎麼寫 | ai, tutorial | 插 |  | ✓ |
| 28 | `chatgpt-canvas-writing` | ChatGPT Canvas 改版後怎麼改稿：用寫作區塊與程式區塊逐段修文章、改小腳本 | ai, tutorial | 插 |  |  |
| 29 | `chatgpt-custom-gpts-build` | 自製 GPT：不用寫程式做出自己的專用助手（2026 年誰能建、怎麼替代） | ai, tutorial | 插 |  |  |
| 30 | `chatgpt-search-vs-google` | ChatGPT 搜尋 vs Google：六類問題什麼時候該用哪一個 | ai, productivity | 插 |  |  |
| 31 | `chatgpt-agent-mode-guide` | ChatGPT 代理模式：讓它替你上網比價、填表、訂位 | ai, tutorial | 插 |  | ✓ |
| 32 | `chatgpt-mobile-app-tips` | ChatGPT 手機 App 十個技巧：拍照提問、Siri、鎖定畫面語音與排程通知 | ai, daily | 照 |  |  |
| 33 | `chatgpt-for-email-writing` | 用 ChatGPT 寫 Email：中英文商務信件範本與提示詞 | ai, productivity | 插 |  |  |
| 34 | `chatgpt-for-excel-formulas` | 用 ChatGPT 寫 Excel 公式與 VBA：從問題描述到可貼上的公式 | ai, productivity | 插 |  |  |
| 35 | `chatgpt-for-english-learning` | 用 ChatGPT 學英文：對話練習、糾錯與單字卡，每天 20 分鐘的六種練法與提示詞 | ai, daily | 插 |  |  |
| 36 | `chatgpt-for-resume-cover-letter` | 用 ChatGPT 改履歷與求職信：改得像自己寫的做法 | ai, productivity | 插 |  |  |
| 37 | `chatgpt-data-analysis-csv` | ChatGPT 資料分析：上傳 CSV 讓它跑程式畫圖表 | ai, tutorial | 插 |  |  |
| 38 | `chatgpt-shared-links-privacy` | ChatGPT 分享連結與隱私：哪些對話可能被搜尋到 | ai, misc | 插 |  |  |
| 39 | `chatgpt-troubleshooting-common-errors` | ChatGPT 常見問題排解：登不進、額度用完、回應中斷 | ai, tutorial | 插 |  | ✓ |
| 40 | `chatgpt-team-for-small-business` | 小公司要不要買 ChatGPT Business（原 Team）：資料不訓練、共用專案、集中管理 | ai, software | 插 |  | ✓ |

### 批次 03｜Claude 教學

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 41 | `claude-plans-free-pro-max-2026` | Claude 免費、Pro、Max 方案比較：額度怎麼算、值不值得 | ai, software | 插 |  | ✓ |
| 42 | `claude-projects-knowledge-base` | Claude Projects：把資料與指令放進專案，越用越懂你 | ai, tutorial | 插 |  |  |
| 43 | `claude-artifacts-guide` | Claude Artifacts 教學：不會寫程式也能在對話裡做出網頁、圖表與小工具 | ai, tutorial | 插 |  |  |
| 44 | `claude-extended-thinking-guide` | Claude 延伸思考模式：什麼題目該開、怎麼看它的推理 | ai, tutorial | 插 |  | ✓ |
| 45 | `claude-file-analysis-pdf-excel` | 給 Claude 讀 PDF 與試算表：摘要、比對與抓數字 | ai, tutorial | 插 |  |  |
| 46 | `claude-writing-style-guide` | 用 Claude 寫作：設定風格、長文結構與潤稿，寫出像自己寫的中文 | ai, productivity | 插 |  |  |
| 47 | `claude-for-translation-zh-tw` | 用 Claude 做中英日翻譯：語氣、專有名詞與術語表 | ai, productivity | 插 |  |  |
| 48 | `claude-system-prompt-basics` | 系統提示詞入門：讓 Claude 穩定扮演一種角色 | ai, tutorial | 插 |  |  |
| 49 | `claude-computer-use-explained` | Claude 操作電腦是怎麼回事：能力、限制與安全 | ai | 插 |  | ✓ |
| 50 | `claude-mcp-explained` | MCP 是什麼：讓 Claude 連上你的檔案、日曆與資料庫 | ai, tutorial | 插 |  |  |
| 51 | `claude-desktop-mobile-app-setup` | Claude 桌面版與手機 App：安裝、快捷鍵與語音 | ai, software | 照 |  |  |
| 52 | `claude-in-chrome-browser-agent` | Claude 在瀏覽器裡：Chrome 擴充功能替你操作網頁 | ai, tutorial | 插 |  | ✓ |
| 53 | `claude-memory-and-privacy` | Claude 的記憶與隱私：什麼會被記住、怎麼清除、對話會不會拿去訓練 | ai, misc | 插 |  | ✓ |
| 54 | `claude-vs-chatgpt-writing-test` | Claude 與 ChatGPT 寫作自測法：五道題、五個面向，結論自己測出來 | ai | 插 |  | ✓ |
| 55 | `claude-for-research-summaries` | 用 Claude 讀論文與長報告：摘要、提問與批判 | ai, productivity | 插 |  |  |
| 56 | `claude-skills-explained` | Claude Skills 是什麼：把重複流程包成可重用的技能 | ai, tutorial | 插 |  | ✓ |
| 57 | `claude-api-first-call` | 第一次呼叫 Claude API：金鑰、費用與十行 Python | ai, tutorial | 插 |  | ✓ |
| 58 | `claude-api-prompt-caching-cost` | Claude API 省錢：提示快取與批次處理怎麼用 | ai, tutorial | 插 |  | ✓ |
| 59 | `claude-model-lineup-2026` | Claude 模型家族：Fable、Opus、Sonnet、Haiku 怎麼選 | ai | 插 |  | ✓ |
| 60 | `claude-for-teachers-lesson-plans` | 老師用 Claude：出題、教案與批改回饋 | ai, productivity | 照 |  |  |

### 批次 04｜AI 寫程式：Claude Code、Codex、Gemini CLI、Cursor、Copilot

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 61 | `ai-coding-tools-overview-2026` | AI 寫程式工具總覽：Claude Code、Codex、Gemini CLI、Cursor、Copilot | ai, software | 插 |  | ✓ |
| 62 | `claude-code-getting-started` | Claude Code 入門：安裝、第一個專案與常用指令 | ai, tutorial | 插 |  | ✓ |
| 63 | `claude-code-claude-md-guide` | 寫好 CLAUDE.md：讓 Claude Code 記住專案規矩 | ai, tutorial | 插 |  |  |
| 64 | `claude-code-mcp-servers` | Claude Code 接 MCP：連 GitHub、資料庫與瀏覽器 | ai, tutorial | 插 |  |  |
| 65 | `claude-code-hooks-and-skills` | Claude Code 的 Hooks 與 Skills：自動化你的工作流 | ai, tutorial | 插 |  | ✓ |
| 66 | `claude-code-on-the-web` | Claude Code 網頁版與手機：在雲端跑任務、回來看結果 | ai, tutorial | 插 |  | ✓ |
| 67 | `codex-cli-getting-started` | Codex CLI 入門：在終端機裡讓 OpenAI 幫你改程式 | ai, tutorial | 插 |  | ✓ |
| 68 | `codex-cloud-tasks-github` | Codex 雲端任務：連 GitHub、平行跑多個任務、開 PR | ai, tutorial | 插 |  | ✓ |
| 69 | `gemini-cli-getting-started` | Gemini CLI 入門：免費額度、安裝與常用指令 | ai, tutorial | 插 |  | ✓ |
| 70 | `cursor-editor-guide` | Cursor 編輯器入門：Tab 補全、Chat 與代理模式 | ai, software | 插 |  | ✓ |
| 71 | `github-copilot-guide` | GitHub Copilot 入門：VS Code 裡的補全、Chat 與代理 | ai, software | 插 |  | ✓ |
| 72 | `vibe-coding-first-website` | Vibe coding：不會寫程式也能做出第一個網站 | ai, tutorial | 插 | H |  |
| 73 | `ai-coding-agents-compared` | AI 寫程式代理操作步驟比較：同一個需求在三個工具怎麼做 | ai | 插 |  | ✓ |
| 74 | `deploy-ai-built-site-to-vps` | 把 AI 幫你寫的網站放上網：VPS、網域與 HTTPS 一次搞定 | tutorial, software | 插 | H |  |
| 75 | `ai-coding-git-basics` | 用 AI 寫程式前該懂的 Git：分支、提交與還原 | tutorial, software | 插 |  |  |
| 76 | `ai-code-review-safety` | AI 寫的程式能信嗎：審查、測試與安全檢查清單 | ai, tutorial | 插 |  |  |
| 77 | `ai-coding-cost-tokens-explained` | AI 寫程式的費用怎麼算：token、訂閱與 API 額度 | ai, software | 插 |  | ✓ |
| 78 | `ai-coding-prompt-patterns` | 給程式代理的提示模式：先規劃、再實作、最後驗證 | ai, tutorial | 插 |  |  |
| 79 | `ai-build-line-bot-tutorial` | 用 AI 幫你做 LINE 機器人：從零到上線 | tutorial, software | 插 | H |  |
| 80 | `ai-build-personal-blog-tutorial` | 用 AI 做個人部落格：靜態網站產生器與部署 | tutorial, software | 插 | H |  |

### 批次 05｜Gemini 與 Google 生態

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 81 | `gemini-plans-ai-pro-ultra-2026` | Google AI Pro 與 Ultra 方案：包了什麼、和 One 的關係 | ai, software | 插 |  | ✓ |
| 82 | `gemini-in-gmail-docs-sheets` | Gemini 在 Gmail、Docs、Sheets 裡怎麼用 | ai, productivity | 插 |  |  |
| 83 | `gemini-gems-custom-assistants` | Gemini Gems：自訂助手教學 | ai, tutorial | 插 |  |  |
| 84 | `gemini-deep-research-guide` | Gemini Deep Research：研究報告怎麼下指令、怎麼驗證 | ai, productivity | 插 |  |  |
| 85 | `gemini-live-voice-camera` | Gemini Live：語音對話與開鏡頭問問題 | ai, daily | 照 |  |  |
| 86 | `notebooklm-guide` | NotebookLM 入門：把資料丟進去，生成摘要與語音導覽 | ai, productivity | 插 |  |  |
| 87 | `notebooklm-for-study-notes` | 用 NotebookLM 讀書：考試筆記與問答 | ai, daily | 插 |  |  |
| 88 | `nano-banana-image-editing` | Nano Banana 修圖教學：Gemini 的圖片生成與編輯 | ai, tutorial | 插 |  | ✓ |
| 89 | `veo-video-generation-guide` | Veo 影片生成入門：提示、長度與費用 | ai, tutorial | 插 |  | ✓ |
| 90 | `gemini-on-android-assistant` | Android 手機上的 Gemini：取代 Google 助理後怎麼用 | ai, gadgets | 照 |  |  |
| 91 | `gemini-in-chrome-guide` | Chrome 裡的 Gemini：整理分頁、摘要網頁 | ai, software | 插 |  | ✓ |
| 92 | `google-ai-mode-search` | Google 搜尋的 AI 模式與 AI 摘要：怎麼用、怎麼關 | ai, daily | 插 |  | ✓ |
| 93 | `gemini-for-google-sheets-formulas` | 用 Gemini 寫 Sheets 公式與整理資料 | ai, productivity | 插 |  |  |
| 94 | `gemini-api-ai-studio-first-call` | Google AI Studio 與 Gemini API：免費額度與第一次呼叫 | ai, tutorial | 插 |  | ✓ |
| 95 | `gemini-vs-chatgpt-vs-claude-daily` | 三大助手日常任務實測：Gemini、ChatGPT、Claude | ai | 插 |  | ✓ |
| 96 | `gemini-for-travel-planning` | 用 Gemini 規劃旅行：地圖、航班與行程整合 | ai, daily | 插 |  |  |
| 97 | `google-workspace-ai-for-small-business` | 小公司的 Google Workspace AI：值不值得升級 | ai, software | 插 |  | ✓ |
| 98 | `gemini-privacy-activity-settings` | Gemini 的活動記錄與隱私設定 | ai, misc | 插 |  |  |
| 99 | `google-ai-overviews-for-site-owners` | AI 摘要對網站流量的影響：站長該怎麼做 | ai, misc | 插 |  |  |
| 100 | `gemini-model-lineup-flash-pro` | Gemini 模型家族：Flash、Pro、Nano 怎麼分 | ai | 插 |  | ✓ |

### 批次 06｜MiniMax、DeepSeek、Qwen、Kimi、豆包與其他家

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 101 | `minimax-hailuo-video-guide` | MiniMax 海螺影片生成教學：從註冊到下載第一支 AI 影片 | ai, tutorial | 插 |  | ✓ |
| 102 | `minimax-speech-tts-guide` | MiniMax 語音合成：中文配音、有聲書與影片旁白 | ai, tutorial | 插 |  | ✓ |
| 103 | `minimax-music-generation` | MiniMax 音樂生成怎麼用：從一段描述與歌詞做出一首歌 | ai, tutorial | 插 |  | ✓ |
| 104 | `minimax-m-series-models-explained` | MiniMax M 系列模型：開放權重、授權條款與 API 價格 | ai | 插 |  | ✓ |
| 105 | `minimax-agent-guide` | MiniMax Agent 怎麼用：一句話做出網頁、報告與簡報 | ai, tutorial | 插 |  | ✓ |
| 106 | `deepseek-chat-and-reasoner` | DeepSeek 對話與深度思考：哪些題目該開推理模式 | ai, tutorial | 插 |  | ✓ |
| 107 | `deepseek-privacy-and-data-flow` | DeepSeek 資料去哪裡：隱私、審查與台灣使用者的取捨 | ai, misc | 插 |  |  |
| 108 | `deepseek-local-with-ollama` | 在自己電腦跑 DeepSeek：Ollama 蒸餾版教學 | ai, tutorial | 插 |  | ✓ |
| 109 | `qwen-alibaba-models-guide` | 通義千問 Qwen：開放權重模型家族與 Qwen Studio | ai | 插 |  | ✓ |
| 110 | `kimi-moonshot-guide` | Kimi（月之暗面）：長文件與 K 系列模型 | ai | 插 |  | ✓ |
| 111 | `doubao-bytedance-guide` | 豆包（字節跳動）：功能與台灣可用性 | ai | 插 |  | ✓ |
| 112 | `chinese-ai-models-comparison` | 中國系 AI 模型比較：DeepSeek、Qwen、Kimi、豆包、MiniMax | ai | 插 |  | ✓ |
| 113 | `chinese-ai-apps-security-checklist` | 使用中國系 AI App 前的資安檢查清單 | ai, misc | 插 |  |  |
| 114 | `mistral-le-chat-guide` | Mistral Vibe（原 Le Chat）：歐洲 AI 助手的方案、功能與資料存放 | ai | 插 |  | ✓ |
| 115 | `grok-xai-guide` | Grok（xAI）怎麼用：三個入口、方案價格與資料訓練開關 | ai | 插 |  | ✓ |
| 116 | `perplexity-ai-search-guide` | Perplexity 入門：附引用的 AI 搜尋、方案與隱私設定 | ai, productivity | 插 |  | ✓ |
| 117 | `microsoft-copilot-windows-office` | Microsoft Copilot：Windows 與 Office 裡的 AI 怎麼分、怎麼買、怎麼關 | ai, software | 插 |  | ✓ |
| 118 | `meta-ai-whatsapp-instagram` | Meta AI：WhatsApp、Instagram 裡的 AI 與隱私 | ai, daily | 插 |  | ✓ |
| 119 | `apple-intelligence-guide` | Apple Intelligence：iPhone、Mac 上的 AI 功能與中文支援 | ai, gadgets | 照 |  | ✓ |
| 120 | `line-ai-features-taiwan` | LINE 裡的 AI：聊天、翻譯與台灣可用功能 | ai, daily | 照 |  | ✓ |

### 批次 07｜本機與開源模型

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 121 | `local-llm-why-and-when` | 為什麼要在自己電腦跑 AI：隱私、離線與成本 | ai, software | 插 |  |  |
| 122 | `ollama-getting-started` | Ollama 入門：Windows、Mac 安裝與第一個模型 | ai, tutorial | 插 |  | ✓ |
| 123 | `lm-studio-getting-started` | LM Studio 入門：圖形介面跑本機模型 | ai, tutorial | 插 |  | ✓ |
| 124 | `local-llm-hardware-requirements` | 跑本機模型要什麼電腦：記憶體、顯示記憶體與 Apple Silicon | ai, gadgets | 照 |  |  |
| 125 | `llama-models-explained` | Llama 模型家族：授權與版本 | ai | 插 |  | ✓ |
| 126 | `gguf-quantization-explained` | 量化是什麼：GGUF、Q4、Q8 怎麼選 | ai, tutorial | 插 |  |  |
| 127 | `open-webui-chat-interface` | Open WebUI：給本機模型一個像 ChatGPT 的介面 | ai, tutorial | 插 |  |  |
| 128 | `ollama-with-code-editors` | 把本機模型接到編輯器：Continue、Cursor 與 Ollama | ai, tutorial | 插 |  | ✓ |
| 129 | `local-rag-chat-with-your-documents` | 本機 RAG：跟自己的文件聊天 | ai, tutorial | 插 |  |  |
| 130 | `gpt-oss-openai-open-weights` | OpenAI 的開放權重模型 gpt-oss：怎麼跑、和 ChatGPT 差在哪 | ai | 插 |  | ✓ |
| 131 | `gemma-google-open-models` | Gemma：Google 的開源模型怎麼用 | ai | 插 |  | ✓ |
| 132 | `qwen-local-deployment` | 本機跑 Qwen：中文表現與設定 | ai, tutorial | 插 |  | ✓ |
| 133 | `whisper-local-transcription` | 用 Whisper 本機轉錄逐字稿：會議與訪談的離線做法 | ai, tutorial | 照 |  |  |
| 134 | `stable-diffusion-comfyui-setup` | 本機跑 Stable Diffusion 與 Flux：ComfyUI 入門 | ai, tutorial | 插 |  | ✓ |
| 135 | `local-ai-on-mac-mini` | Mac mini 當家用 AI 伺服器：統一記憶體、售價與區網設定 | ai, gadgets | 照 |  | ✓ |
| 136 | `local-ai-gpu-buying-guide` | 為 AI 選顯示卡：顯示記憶體優先與預算配置 | gadgets, ai | 照 |  | ✓ |
| 137 | `huggingface-guide` | Hugging Face 入門：找模型、看授權、下載 | ai, tutorial | 插 |  |  |
| 138 | `self-host-ai-on-vps` | 在 VPS 上自架 AI 服務：Ollama＋Open WebUI | tutorial, software | 插 | H |  |
| 139 | `local-vs-cloud-ai-cost` | 本機 vs 雲端 AI 成本試算：訂閱、API 與電費怎麼算 | ai, software | 插 |  | ✓ |
| 140 | `openrouter-multi-model-api` | OpenRouter：一把金鑰用遍各家模型 | ai, tutorial | 插 |  | ✓ |

### 批次 08｜圖片、影片、音樂生成

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 141 | `ai-image-tools-overview-2026` | AI 圖片工具總覽：ChatGPT、Nano Banana、Midjourney、Flux 怎麼選 | ai, software | 插 |  | ✓ |
| 142 | `midjourney-getting-started` | Midjourney 入門：網頁版、參數與訂閱 | ai, tutorial | 插 |  | ✓ |
| 143 | `midjourney-prompt-guide` | Midjourney 提示詞：風格、比例、參考圖 | ai, tutorial | 插 |  |  |
| 144 | `sora-video-guide` | Sora 影片生成教學：官方已停止服務，先匯出再挑替代工具 | ai, tutorial | 插 |  | ✓ |
| 145 | `ai-video-tools-compared` | AI 影片工具比較：Veo、Sora、海螺、Kling 的方案與規格 | ai | 插 |  | ✓ |
| 146 | `kling-runway-video-tools` | Kling 與 Runway：影片生成工具介紹 | ai | 插 |  | ✓ |
| 147 | `suno-music-generation-guide` | Suno 做歌：從歌詞到成品，方案、下載與商用權怎麼算 | ai, tutorial | 插 |  | ✓ |
| 148 | `ai-voice-cloning-elevenlabs` | ElevenLabs 與語音克隆：配音、方案與同意規則怎麼看 | ai, tutorial | 插 |  | ✓ |
| 149 | `ai-image-copyright-taiwan` | AI 生成圖片的版權：台灣法規與商用注意事項 | ai, misc | 插 |  |  |
| 150 | `ai-image-watermark-c2pa` | AI 圖片的浮水印與 C2PA：怎麼標示、怎麼辨識 | ai, misc | 插 |  |  |
| 151 | `ai-remove-background-upscale` | AI 去背與放大：免費工具怎麼挑 | ai, tutorial | 照 |  |  |
| 152 | `ai-photo-restoration-old-photos` | 用 AI 修復老照片：去刮痕、放大與上色分開做，工具怎麼選 | ai, daily | 照 |  |  |
| 153 | `canva-ai-features-guide` | Canva 的 AI 功能怎麼用：免費能做什麼、額度怎麼算 | ai, software | 插 |  | ✓ |
| 154 | `ai-slides-generation-tools` | AI 做簡報：Gamma、Copilot 與 Gemini | ai, productivity | 插 |  | ✓ |
| 155 | `ai-product-photo-for-sellers` | 賣家用 AI 做商品圖：四種用法、平台規範與紅線 | ai, daily | 照 |  |  |
| 156 | `ai-video-subtitles-translation` | AI 上字幕與翻譯影片：CapCut、Whisper 與 YouTube 三條路 | ai, tutorial | 插 |  |  |
| 157 | `ai-avatar-video-tools` | AI 虛擬主播與數位分身：HeyGen 的方案、同意規則與標示怎麼看 | ai | 插 |  | ✓ |
| 158 | `ai-generated-content-disclosure` | AI 內容標示：YouTube、Meta 與台灣的規定 | ai, misc | 插 |  | ✓ |
| 159 | `ai-art-prompt-styles-reference` | AI 繪圖風格提示參考：50 種風格描述 | ai, tutorial | 插 |  |  |
| 160 | `ai-3d-model-generation` | AI 生成 3D 模型入門：從文字或圖片到能列印的檔案 | ai | 插 |  | ✓ |

### 批次 09｜工作流、效率與自動化

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 161 | `ai-note-taking-workflow` | 用 AI 做筆記：Notion AI、Obsidian 與 NotebookLM 怎麼分工 | productivity, ai | 插 |  |  |
| 162 | `notion-ai-guide` | Notion AI 入門：哪個方案才有、能做什麼、資料怎麼處理 | productivity, software | 插 |  | ✓ |
| 163 | `ai-meeting-notes-tools` | AI 會議記錄工具怎麼挑：Otter、Google Meet、Teams、Zoom 與 Notion | productivity, ai | 照 |  | ✓ |
| 164 | `n8n-ai-automation-guide` | n8n 入門：用 AI 節點做自動化工作流 | tutorial, productivity | 插 | H |  |
| 165 | `zapier-make-ai-automation` | Zapier 與 Make 的 AI 自動化：計費方式與 AI 功能對照 | productivity, software | 插 |  | ✓ |
| 166 | `mcp-servers-for-everyone` | MCP 伺服器實用清單：檔案、Google、Notion、瀏覽器 | ai, tutorial | 插 |  | ✓ |
| 167 | `ai-email-management` | 用 AI 管理 Email：分類、摘要與草稿的工作流 | productivity, ai | 插 |  |  |
| 168 | `ai-calendar-scheduling` | AI 排程與行事曆助手：找時間、排工作區塊與定時提醒 | productivity, ai | 插 |  | ✓ |
| 169 | `ai-pdf-tools-summarize-translate` | AI PDF 工具：摘要、翻譯、問答怎麼分工 | productivity, software | 插 |  |  |
| 170 | `ai-browsers-guide` | AI 瀏覽器怎麼選：Comet、Dia、Chrome 的 Gemini 與代理風險 | ai, software | 插 |  | ✓ |
| 171 | `ai-spreadsheet-automation` | 試算表 AI 自動化：Google 試算表 AI 函式與 Excel Copilot 怎麼分工 | productivity, ai | 插 |  |  |
| 172 | `ai-second-brain-obsidian` | Obsidian＋AI 打造第二大腦：外掛、程式代理與 MCP 三種接法 | productivity, software | 插 |  |  |
| 173 | `ai-prompt-library-personal` | 建立自己的提示詞庫：固定欄位、放在哪裡、怎麼管版本 | productivity, ai | 插 |  |  |
| 174 | `ai-for-social-media-content` | 用 AI 做社群貼文：IG、Threads、FB 排程 | ai, daily | 插 |  |  |
| 175 | `ai-for-youtube-creators` | YouTuber 的 AI 工作流：腳本、字幕、縮圖與標示規則 | ai, productivity | 插 |  |  |
| 176 | `ai-for-small-business-taiwan` | 台灣小店的 AI 應用：客服、菜單、廣告 | ai, daily | 照 |  |  |
| 177 | `ai-customer-service-line-bot` | 用 AI 做客服機器人：LINE 官方帳號接 AI | tutorial, software | 插 | H |  |
| 178 | `ai-agent-frameworks-explained` | Agent 框架入門：OpenAI Agents SDK、Claude Agent SDK、LangGraph | ai, tutorial | 插 |  | ✓ |
| 179 | `ai-weekly-review-templates` | AI 週回顧與目標管理範本：固定輸入、固定輸出，還能讓它自動跑 | productivity, daily | 插 |  |  |
| 180 | `ai-reading-list-books-2026` | AI 入門書單：十本值得讀的書，附繁中版出版資訊 | ai, misc | 照 | B | ✓ |

### 批次 10｜比較、費用、資安與法律

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 181 | `ai-subscription-which-to-pay-2026` | 只能訂一個的話訂哪個：ChatGPT、Claude、Gemini | ai, software | 插 |  | ✓ |
| 182 | `ai-benchmarks-explained` | 模型跑分怎麼看：LMArena、SWE-bench 與陷阱 | ai | 插 |  | ✓ |
| 183 | `ai-model-release-timeline-2026` | 2026 年 AI 模型大事記 | ai, misc | 插 |  | ✓ |
| 184 | `ai-api-pricing-comparison-2026` | API 價格比較：每百萬 token 各家多少 | ai, software | 插 |  | ✓ |
| 185 | `ai-scams-deepfake-taiwan` | AI 詐騙與 Deepfake：台灣案例與防範 | ai, daily | 插 |  |  |
| 186 | `ai-account-security-2fa-api-keys` | 保護你的 AI 帳號：兩步驟驗證與金鑰外洩 | ai, tutorial | 插 |  |  |
| 187 | `ai-and-copyright-law-taiwan` | AI 與著作權：台灣法規與判決整理 | ai, misc | 插 |  |  |
| 188 | `ai-at-work-policy-checklist` | 公司裡用 AI 的規範：資料外流與合規 | ai, productivity | 插 |  |  |
| 189 | `ai-detection-tools-reliability` | AI 偵測工具準不準 | ai, misc | 插 |  |  |
| 190 | `ai-energy-water-footprint` | AI 的用電與用水：一次對話的成本 | ai, misc | 插 |  |  |
| 191 | `ai-for-kids-parent-guide` | 家長指南：孩子用 AI 的年齡限制與設定 | ai, daily | 照 |  | ✓ |
| 192 | `ai-regulation-eu-act-taiwan` | 歐盟 AI 法案與台灣 AI 基本法：對使用者的影響 | ai, misc | 插 |  | ✓ |
| 193 | `ai-prompt-injection-explained` | 提示詞注入是什麼：使用者該懂的攻擊 | ai, tutorial | 插 |  |  |
| 194 | `ai-chat-history-export-delete` | 匯出與刪除你的 AI 對話記錄 | ai, tutorial | 插 |  | ✓ |
| 195 | `ai-token-cost-estimation` | token 計算與費用估算 | ai, tutorial | 插 |  | ✓ |
| 196 | `ai-open-vs-closed-models` | 開源 vs 閉源模型：對使用者的差別 | ai | 插 |  |  |
| 197 | `ai-taiwan-local-models-taide` | 台灣的本土模型：TAIDE 與繁中表現 | ai | 插 |  | ✓ |
| 198 | `ai-companion-mental-health-caution` | AI 陪伴與心理健康：可以與不可以 | ai, daily | 插 |  |  |
| 199 | `ai-news-sources-to-follow` | 追 AI 新聞的來源清單 | ai, misc | 插 |  |  |
| 200 | `ai-hype-vs-reality-2026` | AI 能與不能：2026 年的誠實盤點 | ai, misc | 插 |  | ✓ |

### 批次 11｜生活應用、3C 與旅途中的 AI

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 201 | `ai-travel-planning-tools` | 用 AI 規劃旅行：行程、比價與注意事項 | ai, daily | 照 |  |  |
| 202 | `ai-translation-apps-travel` | 旅行翻譯 App：Google 翻譯、ChatGPT 語音、Gemini Live | ai, daily | 照 |  |  |
| 203 | `ai-photo-organizing-apps` | AI 整理相片：Google 相簿、Apple 照片 | ai, daily | 照 |  |  |
| 204 | `ai-cooking-recipes-meal-planning` | AI 幫你排菜單與食譜 | ai, daily | 照 |  |  |
| 205 | `ai-fitness-health-tracking` | AI 與健康：手錶數據、健身計畫 | ai, gadgets | 照 |  |  |
| 206 | `ai-personal-finance-budgeting` | AI 記帳與理財：注意事項 | ai, daily | 插 |  |  |
| 207 | `ai-smart-home-assistants` | AI 智慧家庭：Home Assistant 與語音助理 | gadgets, ai | 照 |  |  |
| 208 | `ai-smart-glasses-2026` | AI 眼鏡：能做什麼、台灣買得到嗎 | gadgets, ai | 照 |  | ✓ |
| 209 | `ai-earbuds-live-translation` | 即時翻譯耳機實測 | gadgets, ai | 照 |  | ✓ |
| 210 | `ai-phone-features-compared` | 手機的 AI 功能：Pixel、Galaxy、iPhone | gadgets, ai | 照 |  | ✓ |
| 211 | `ai-pc-npu-copilot-plus` | AI PC 與 NPU：Copilot+ PC 值得買嗎 | gadgets, ai | 照 |  | ✓ |
| 212 | `ai-mac-vs-windows` | Mac 或 Windows 跑 AI：怎麼選 | gadgets, ai | 照 |  |  |
| 213 | `ai-tablet-note-taking` | 平板＋AI 筆記：Goodnotes、Notability | gadgets, productivity | 照 |  |  |
| 214 | `ai-language-learning-apps` | AI 語言學習 App：Duolingo、Speak | ai, daily | 插 |  | ✓ |
| 215 | `ai-job-interview-practice` | AI 模擬面試 | ai, daily | 插 |  |  |
| 216 | `ai-event-planning-wedding` | 用 AI 辦活動：婚禮、生日 | ai, daily | 照 |  |  |
| 217 | `ai-shopping-assistant-price-compare` | AI 購物助理與比價 | ai, daily | 插 |  | ✓ |
| 218 | `ai-elderly-care-reminders` | 長照與 AI：提醒、陪伴 | ai, daily | 照 |  |  |
| 219 | `ai-writing-traditional-chinese-tips` | 讓 AI 寫出道地繁體中文：避免簡體用語 | ai, tutorial | 插 |  |  |
| 220 | `ai-daily-habits-30-day-challenge` | 30 天 AI 習慣挑戰 | ai, daily | 插 |  |  |

## 經驗記錄

每批做完把學到的事寫在這裡（一兩行，指向任務票的 Outcome），下一批開工前先讀。

- 批次 01（2026-09-13，`tasks/done/2026-09-13-life-ai-batch-01.md`）：一篇一個代理、同時七個最穩，沒有人被額度切斷；
  代理只准 `--dry-run`，不碰 repo 檔案（有代理「清理」掉已收進去的文章）；`alt` ≤ 200 字、系列統一用語（token、上下文視窗）已寫進 brief；
  收完後把 life→life 連結文字統一成目標標題；每張圖渲染後一定要人看，字壓框機械檢查抓不到。
- 批次 02（2026-09-13，`tasks/done/2026-09-13-life-ai-batch-02.md`）：撰稿代理會繼承 session 的 plan mode——開著時代理只寫計畫檔、不寫交付物；
  `ExitPlanMode` 後用 SendMessage 讓同一個代理接著執行，查證不用重做。被額度切斷的代理留下的 `pack.json` 可由新代理接手補圖。
  官網 403 的讀法（help center 網址加 `.json`、Wayback 快照、WebSearch 限定網域）已寫進 brief 第 5 節。代理在協調者 ingest 之後還會再改檔，
  收尾前用 `find -newer` 再對一次。總表標題以實際篇名為準（本批同步了 12 列），life→life 連結文字收完後統一。
- 批次 03（2026-09-14，`tasks/done/2026-09-13-life-ai-batch-03.md`）：**指派的站內連結只能列已經寫完或同批會寫的 slug**——
  本批列了批次 04／10／11 的篇名，八篇共 13 個連結指向不存在的文章，收尾時才由 `normalise_links.py` 的 missing target 抓到並移除。
  撰稿代理會繼承 session 的 plan mode，開著時代理只寫計畫檔；`ExitPlanMode` 後用 SendMessage 讓同一個代理接著執行即可，查證不用重做。
  總表標題以實際篇名為準（本批同步 5 列，其中「兩家寫作比一比」因為我們無法真的實測，改寫成讀者自測法）。
- 批次 04（2026-09-14，`tasks/open/2026-09-13-life-ai-batch-04.md`）：教學文很需要 `code` 區塊（指令、設定檔、範例提示詞），撰稿補充要明寫可用；連結文字直接取目標文章標題（同批會寫的篇用指派給的標題，收完後再統一一次）；無法實測的「比較」題改寫成操作步驟比較與讀者自測法。官方文件會搬家（Codex 文件轉到 learn.chatgpt.com），sources 記實際生效的網址。合作連結沒有聯盟網址就不放，總表的 H 標記只是允許。
- 批次 06（2026-09-14，`tasks/open/2026-09-13-life-ai-batch-06.md`）：中國系與其他家的產品名、模型版本、授權與方案半年內幾乎全換過（Le Chat→Vibe、Qwen Chat→Qwen Studio、MiniMax Agent→Mavis、Copilot Pro 停售），指派裡的「例如」只能當起點，寫手照當天官網寫、審稿再用 curl／Hugging Face API／iTunes lookup 逐篇複核；台灣可用性用 App Store／Google Play 官方查詢，查不到就寫查不到；政府禁令只引公告原文並限定公務機關；x.ai、help.x.com、perplexity.ai、volcengine 對機房 IP 回 403，寫手改讀 .md 版文件、說明中心的 Intercom 網址或 Wayback 快照並在 notes 記讀法。一波七個 Opus 代理會撞帳號的五小時額度，撞到就等重置再重跑。
- 批次 07（2026-09-14，`tasks/open/2026-09-13-life-ai-batch-07.md`）：本機與開源模型的授權要逐版本用 Hugging Face API 的 license 標籤與 LICENSE 原文核對，不能用家族名稱推論（Gemma 4 是 Apache 2.0 但 Gemma 3 仍是 Gemma Terms；FLUX.2 klein 4B 可商用但 9B 非商用；Qwen 只有 Flash-Next 是自訂授權；SDXL Turbo 的 HF 標籤與 LICENSE 檔不一致）。官方文件自己也會前後不一致（Ollama 預設上下文、Open WebUI 向量庫數、Whisper turbo 參數），正文擇一並註明出處。openai.com 與 help.openai.com 對本環境 403，Wayback 的 `id_` 原始快照要 `--compressed`；amd.com 要 `--http1.1` 加瀏覽器 UA；developer.apple.com 走 `tutorials/data/...json`；apple.com/tw 售價在 JSON-LD。硬體與價格只抄官網當天數字、不做效能推估；sitemap 已到 926/1,000 列。
- 批次 08（2026-09-14，`tasks/open/2026-09-13-life-ai-batch-08.md`）：圖片、影片、音樂工具改版比模型更快，指派裡的產品現況要當作假設（Sora 已停止服務、Midjourney 預設 V8.2 且 `--cref` 已被 Edit Model 取代、Canva 的 Magic Studio 改名、remove.bg 將併入 Leonardo.Ai、Luma 已無 3D 產品），寫手照當天官網寫、審稿逐篇用 Zendesk／Intercom 內容 API、Wayback、WebFetch 與 iTunes lookup 複核；價格照官網幣別，但 Google 訂閱有台灣頁就寫新台幣；法規與平台規範只引 law.moj.gov.tw 與官方頁原文、不下法律結論；免費層常見的坑是「能生成、不能下載或不能商用」（Meshy、Suno、remove.bg、Photoroom、HeyGen），表格要把這件事寫成獨立欄位。docs.midjourney.com 與 help.runwayml.com 走 Zendesk API，helpx.adobe.com 要完整瀏覽器標頭，canva.com 只能讀 Wayback，Meta 頁面要用 WebFetch。
- 批次 09（2026-09-15，`tasks/open/2026-09-13-life-ai-batch-09.md`）：工作流與自動化工具半年內改名改計費的比例比模型還高（NotebookLM→Gemini Notebook、Make operations→credits、Clockwise 收攤、Atlas 停止運作、Excel COPILOT 函式停用、n8n npm 安裝淘汰、ChatGPT 個人帳號不能新建 GPT），指派裡的功能名稱只能當起點；台灣讀者最常踩的是語言清單（Meet 筆記、Sheets AI 函式、Google 商家檔案 Gemini、Acrobat AI 助理、YouTube 自動配音都沒有繁中或只能配英語），每篇都要把語言清單當獨立欄位查。文件網域大搬家（docs.claude.com→platform.claude.com／code.claude.com、langchain-ai.github.io→docs.langchain.com、adk-docs→adk.dev、help.obsidian.md→obsidian.md/help），sources 記轉址後網址。七個代理撞到 session 額度時不用重開，額度重置後 SendMessage 接續同一個代理即可。本批落地後 repo 的 sitemap 列數 1,017，已超過 1,000，發布前要先拆 sitemap。
- Commons 照片：工具的 User-Agent 要有聯絡信箱，而且請求要走 urllib（httpx 的連線被 Wikimedia 擋 403）；十個代理同時搜 Commons 會被 429，工具會退避重試。

## Gemini 完整系列補充（2026-09-14）

原批次 01 的入門篇、批次 04 的 CLI 入門及批次 05 的 Gemini 主題沿用原 slug；以下僅列新增項目，避免重複指派。完整篇序、五條路線及驗收程序以 [Gemini 系列維護說明](gemini-series/README.md) 和 `apps/web/lib/guide-series.json` 為準。發布以 51 頁整套驗收為單位，不按原批次單獨發布。

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 221 | `gemini-guide` | Gemini 完整教學：電腦、手機、CLI 與 Google AI 應用 | ai, tutorial | 插 |  | ✓ |
| 222 | `gemini-web-desktop-guide` | 電腦網頁版：Windows、檔案與瀏覽器捷徑 | ai, tutorial | 插 |  | ✓ |
| 223 | `gemini-mac-app-guide` | Mac 桌面版：安裝、快捷鍵與視窗分享 | ai, tutorial | 插 |  | ✓ |
| 224 | `gemini-ios-app-guide` | iPhone 與 iPad：安裝、語音與照片 | ai, tutorial | 插 |  | ✓ |
| 225 | `gemini-prompt-writing-guide` | 提示詞怎麼寫：目標、背景與輸出格式 | ai, tutorial | 插 |  | ✓ |
| 226 | `gemini-file-analysis-guide` | 讀 PDF、圖片與表格：摘要、比對與驗證 | ai, tutorial | 插 |  | ✓ |
| 227 | `gemini-canvas-guide` | Canvas：編輯文章、簡報與製作小工具 | ai, tutorial | 插 |  | ✓ |
| 228 | `gemini-spark-workflows-guide` | Gemini Spark：任務、排程與 Skills | ai, tutorial | 插 |  | ✓ |
| 229 | `gemini-connected-apps-guide` | Connected Apps：Drive、日曆與地圖整合 | ai, tutorial | 插 |  | ✓ |
| 230 | `gemini-cli-authentication` | CLI 認證：Google 帳號、API Key 與計費 | ai, tutorial | 插 |  | ✓ |
| 231 | `gemini-cli-command-reference` | CLI 指令總表：語法、範例與深入教學 | ai, tutorial | 插 |  | ✓ |
| 232 | `gemini-cli-files-and-shell` | CLI 檔案與命令：@、! 與路徑 | ai, tutorial | 插 |  | ✓ |
| 233 | `gemini-cli-sessions-context` | CLI 對話管理：恢復、壓縮與匯出 | ai, tutorial | 插 |  | ✓ |
| 234 | `gemini-cli-coding-workflow` | CLI 寫程式：理解、規劃、修改與測試 | ai, tutorial | 插 |  | ✓ |
| 235 | `gemini-markdown-basics` | Markdown 基礎：建立 MD、標題與程式碼 | ai, tutorial | 插 |  | ✓ |
| 236 | `gemini-cli-gemini-md` | GEMINI.md 入門：建立規則與 /init | ai, tutorial | 插 |  | ✓ |
| 237 | `gemini-cli-memory-hierarchy` | GEMINI.md 進階：範圍、匯入與 /memory | ai, tutorial | 插 |  | ✓ |
| 238 | `gemini-cli-settings` | settings.json：全域、專案與環境變數 | ai, tutorial | 插 |  | ✓ |
| 239 | `gemini-cli-permissions-sandbox` | CLI 權限：忽略檔案、可信任資料夾與沙箱 | ai, tutorial | 插 |  | ✓ |
| 240 | `gemini-cli-custom-commands` | 自訂斜線指令：TOML、參數與重新載入 | ai, tutorial | 插 |  | ✓ |
| 241 | `gemini-cli-mcp-extensions` | MCP 與 Extensions：安裝、驗證與停用 | ai, tutorial | 插 |  | ✓ |
| 242 | `gemini-cli-agent-skills` | Agent Skills：建立可重用的 SKILL.md | ai, tutorial | 插 |  | ✓ |
| 243 | `gemini-cli-hooks` | Hooks：在指定事件執行檢查 | ai, tutorial | 插 |  | ✓ |
| 244 | `gemini-cli-subagents` | Subagents：拆分任務與整合結果 | ai, tutorial | 插 |  | ✓ |
| 245 | `gemini-cli-headless-automation` | Headless 模式：批次、JSON 與腳本 | ai, tutorial | 插 |  | ✓ |
| 246 | `gemini-cli-troubleshooting` | CLI 疑難排解：登入、PATH 與設定失效 | ai, tutorial | 插 |  | ✓ |
| 247 | `gemini-api-files-structured-output` | API 檔案與 JSON：結構化輸出及驗證 | ai, tutorial | 插 |  | ✓ |
| 248 | `gemini-api-cost-errors-guide` | API 額度與錯誤：費用、重試與成本控制 | ai, tutorial | 插 |  | ✓ |
| 249 | `gemini-api-document-assistant` | 完整實作：文件摘要與資料擷取工具 | ai, tutorial | 插 |  | ✓ |

### 批次 12｜字尾關鍵字補位（11 篇）

字尾型搜尋詞（「〇〇 AI」）哪裡都對不到文章的，排在這裡；對照表、寫法與四篇待拍板的敏感題見
[`docs/ai-suffix-keywords.md`](ai-suffix-keywords.md)。第 250 篇是索引 hub，`featured: false`、`display_order: 100`，只連已寫的篇。

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 250 | `ai-tools-by-search-term` | 〇〇 AI 怎麼找：從你會搜的字找到對的工具與教學 | ai, misc | 插 |  | ✓ |
| 251 | `ai-image-to-text-ocr` | 圖片轉文字 AI：截圖、掃描件與手寫筆記變成可編輯文字 | ai, tutorial | 插 |  | ✓ |
| 252 | `ai-taiwanese-hokkien-hakka-tools` | 台語 AI 與客語 AI：語音辨識、合成與翻譯工具有哪些、準不準 | ai, daily | 照 |  | ✓ |
| 253 | `ai-line-sticker-creation` | 貼圖 AI：用 AI 做 LINE 貼圖的生成、去背、審核規則與版權 | ai, daily | 插 |  | ✓ |
| 254 | `ai-interior-design-visualization` | 裝潢 AI：把房間照片變成設計提案，哪些不能靠 AI | ai, daily | 照 |  | ✓ |
| 255 | `ai-id-photo-rules-taiwan` | 證件照 AI：AI 修圖或生成的證件照能不能用，護照與身分證規定 | ai, daily | 插 |  | ✓ |
| 256 | `ai-naming-brainstorm-checks` | 取名 AI：品牌、公司與商品名的提示詞，以及預查與商標檢索 | ai, daily | 插 |  |  |
| 257 | `ai-fortune-telling-apps-caution` | 算命 AI 在做什麼：生成式回答的原理、個資流向與付費陷阱 | ai, daily | 插 |  |  |
| 258 | `ai-stock-research-boundaries` | 投資 AI 能幫什麼：整理財報與新聞、不能預測漲跌、金管會怎麼管 | ai, daily | 插 |  | ✓ |
| 259 | `ai-legal-questions-boundaries` | 法律 AI：法律問題問 AI 能整理什麼、什麼要找律師 | ai, daily | 插 |  |  |
| 260 | `ai-health-questions-boundaries` | 健康 AI：症狀整理、看診前準備與它不能取代的事 | ai, daily | 插 |  |  |
