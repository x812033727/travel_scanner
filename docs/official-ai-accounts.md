# AI 公司的官方 X 帳號與對應的官網頁面

Last verified: 2026-10-10

**沒有任何程式讀 x.com。** 這份清單是給人追蹤用的；新聞自動化與影片選題只讀「官網頁面」那一欄，
也就是 [`sources.json`](../apps/api/app/news_automation/sources.json) 裡的來源
（流程見 [`news-automation.md`](news-automation.md)）。站主 2026-09-30 決定不把 X 當來源，
2026-10-10 看過付費 API 的價格後維持這個決定，細節在本頁最後一節。

## 怎麼讀這份表

- **查證依據**：該公司自己的網站、說明中心或官方組織頁有連到這個帳號。查證時沒有打開 x.com
  看帳號本身，所以「已查證」的意思是「官方頁面指向它」。
- **掃描器狀態**有四種：
  - 來源名稱（例如 `Anthropic news`）：已經在 `sources.json` 裡。
  - `候選`：票 `2026-10-10-add-official-changelog-and-developer-update` 要測試後加入。
  - `讀不到：原因`：測過，掃描器現在的讀法吃不了。
  - `未測`：還沒人用掃描器的解析器測過。
- 個別列的查證日期與檔頭不同時，寫在備註。

## 兩條規則

1. 查證依據不是官方頁面的列（只有第三方、未查證、互相矛盾），不得在文章或影片卡上當成官方帳號引用。
2. 整份每季重查一次；某一列第一次被引用前，先重查那一列。帳號改名很常見（見 xAI、Copilot）。

## 清單

### Anthropic

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@AnthropicAI`](https://x.com/AnthropicAI) | 公司消息、研究、模型發布 | <https://www.anthropic.com/> 頁尾 | <https://www.anthropic.com/news> | `Anthropic news` |
| [`@claudeai`](https://x.com/claudeai) | Claude 產品更新 | <https://claude.com/> 頁尾 | <https://claude.com/resources/articles> | `Claude blog`（網址待修，見備註） |
| [`@ClaudeDevs`](https://x.com/ClaudeDevs) | 開發者更新、Claude Code 更新紀錄 | 只有第三方：<https://awesomeagents.ai/news/anthropic-claudedevs-x-account-launch/> | <https://claude.dev/>、<https://code.claude.com/docs/en/changelog>、<https://platform.claude.com/docs/en/release-notes/feed.xml> | `Claude Platform release notes`；其餘兩個是`候選` |

備註：

- `claude.com/blog` 在 2026-10 轉址到 `claude.com/resources/articles`，文章路徑從 `/blog/<slug>` 變成
  `/resources/articles/<slug>`。`Claude blog` 這一列的設定還只收 `/blog/`，照設定現在讀不到任何一篇。
- Claude Code 沒有自己的官方帳號，產品頁只連到 `@claudeai`。
- Claude 各 App 的更新紀錄 <https://support.claude.com/en/articles/12138966-release-notes>
  `讀不到：整份是一頁、按日期分段，每一則沒有自己的網址`。大的項目在 `Claude blog` 與
  `Anthropic news` 都有對應文章；只寫在這頁的小更新（2026-10 的例子：Smart reports、
  Monthly API credits for Max and Team plans）目前拿不到。

### OpenAI

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@OpenAI`](https://x.com/OpenAI) | 公司消息、模型發布 | <https://help.openai.com/en/articles/11725090-verifying-communications-from-openai> | <https://openai.com/news/> | `OpenAI News`（文章頁回 403，多半只有摘要線索） |
| [`@ChatGPTapp`](https://x.com/ChatGPTapp) | ChatGPT 產品更新 | 同上 | ChatGPT 更新紀錄 | `讀不到：一頁到底，每一則沒有自己的網址` |
| [`@OpenAIDevs`](https://x.com/OpenAIDevs) | API、Codex 開發者更新 | 同上 | OpenAI API 與 Codex 更新紀錄 | `讀不到：一頁到底，每一則沒有自己的網址` |
| [`@OpenAINewsroom`](https://x.com/OpenAINewsroom) | 新聞稿 | 同上 | <https://openai.com/news/> | `OpenAI News` |

備註：

- OpenAI 的說明頁直接抓會回 403，四個帳號是從它各語言版本的搜尋結果讀到的。
- Sora 與 Codex 沒有找到官方 X 帳號；Codex 的消息發在 `@OpenAIDevs`。
- `@OpenAINewsroom` 在 2024-09 被盜用過發加密貨幣貼文，看到異常貼文先對照官網。

### Google

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@GoogleDeepMind`](https://x.com/GoogleDeepMind) | 研究、模型發布 | <https://deepmind.google/> | <https://deepmind.google/blog/> | `Google DeepMind blog` |
| [`@GeminiApp`](https://x.com/GeminiApp) | Gemini App 更新 | <https://gemini.google/about/> 頁尾 | <https://blog.google/>；Gemini App 更新紀錄 | `Google Keyword blog`；更新紀錄`讀不到：一頁到底` |
| [`@GoogleAI`](https://x.com/GoogleAI) | Google AI 消息 | <https://ai.google/> 頁尾 | <https://blog.google/technology/ai/> | `Google AI blog` |
| [`@googleaidevs`](https://x.com/googleaidevs) | Gemini API 開發者更新 | <https://github.com/google-gemini> 組織頁 | Gemini API 更新紀錄 | `讀不到：一頁到底` |
| [`@GoogleLabs`](https://x.com/GoogleLabs) | 實驗產品 | <https://labs.google/> | <https://labs.google/> | `未測` |
| [`@googledevs`](https://x.com/googledevs) | 開發者消息 | <https://developers.googleblog.com/> 頁尾 | <https://developers.googleblog.com/> | `讀不到：robots.txt 回轉址，掃描器視為拒絕` |
| [`@Gemini_Notebook`](https://x.com/Gemini_Notebook) | Gemini Notebook（原 NotebookLM）更新 | 只有第三方：<https://www.freepressjournal.in/tech/google-rebrands-notebooklm-as-gemini-notebook-heres-why> | <https://blog.google/> | `Google Keyword blog` |
| `@GoogleAIStudio` | AI Studio 更新 | 未查證：沒有官方頁面連到 | — | — |

備註：NotebookLM 在 2026-07-16 改名 Gemini Notebook（改名本身有官方公告：
<https://workspaceupdates.googleblog.com/2026/07/notebooklm-now-gemini-notebook.html>）。
舊的 `@NotebookLM` 是改名還是棄用，沒有查到。

### xAI、Meta、Microsoft、GitHub

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@SpaceXAI`](https://x.com/SpaceXAI) | xAI 公司與 Grok 消息 | <https://github.com/xai-org> 組織頁 | xAI 官網 | `讀不到：回 403` |
| [`@grok`](https://x.com/grok) | Grok 助理帳號 | <https://github.com/xai-org/grok-prompts> 的說明文字 | xAI 官網 | `讀不到：回 403` |
| [`@AIatMeta`](https://x.com/AIatMeta) | 研究、模型 | <https://ai.meta.com/blog/> | <https://ai.meta.com/blog/> | `讀不到：頁面要跑 JavaScript`；公司消息走 `Meta Newsroom` |
| `@MetaAI` | Meta AI 產品 | 未查證：沒有官方頁面連到 | — | — |
| [`@MSFTCopilot`](https://x.com/MSFTCopilot) | Copilot 更新 | <https://www.microsoft.com/en-us/microsoft-copilot/for-individuals> 頁尾 | Microsoft Copilot blog；<https://blogs.microsoft.com/> | `讀不到：回 403`；公司消息走 `Microsoft official blog` |
| [`@MSFTResearch`](https://x.com/MSFTResearch) | 研究 | <https://www.microsoft.com/en-us/research/> 頁尾 | <https://www.microsoft.com/en-us/research/> | `Microsoft Research blog` |
| [`@code`](https://x.com/code) | VS Code 更新 | <https://code.visualstudio.com/> 頁尾 | <https://code.visualstudio.com/> | `讀不到：feed 會列出日期在未來的 Insiders 版` |
| [`@github`](https://x.com/github) | GitHub 與 Copilot 更新 | <https://github.com/features/copilot> 頁尾 | <https://github.blog/>；<https://github.blog/changelog/> | `GitHub blog`；Changelog 是`候選` |
| `@GitHubCopilot` | Copilot | 未查證：GitHub 的 Copilot 頁只連到 `@github` | — | — |

備註：

- **xAI 改名**：第三方報導（<https://gigazine.net/gsc_news/en/20260707-xai-change-spacexai>）說
  `@xai` 在 2026-07-06 改成 `@SpaceXAI`。xAI 在 Hugging Face 的頁面還寫 `@xai`，把舊帳號當成過期。
- **Copilot**：微軟官網連的是 `@MSFTCopilot`。2026-09-25 有報導說另一個 Copilot 專用帳號被關掉、
  貼文移除，沒有寫明是哪個帳號；不要追蹤 `@Copilot`，除非自己對過。

### 其他模型公司

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@MistralAI`](https://x.com/MistralAI) | 公司與產品消息 | <https://mistral.ai/> 頁尾 | <https://mistral.ai/news> | `Mistral AI news` |
| [`@perplexity_ai`](https://x.com/perplexity_ai) | 產品更新 | <https://github.com/perplexityai> 組織頁 | Perplexity 官網 | `讀不到：回 403` |
| [`@deepseek_ai`](https://x.com/deepseek_ai) | 模型發布 | <https://api-docs.deepseek.com/> 頁尾 | <https://api-docs.deepseek.com/> | `讀不到：沒有文章列表，robots.txt 回的是網頁` |
| [`@Alibaba_Qwen`](https://x.com/Alibaba_Qwen) | 模型發布 | <https://github.com/QwenLM> 組織頁 | Qwen 官網 | `讀不到：頁面要跑 JavaScript` |
| [`@Kimi_Moonshot`](https://x.com/Kimi_Moonshot) | 產品更新 | <https://www.moonshot.ai/> 頁尾 | <https://www.moonshot.ai/> | `讀不到：robots.txt 回 404，掃描器視為拒絕` |
| [`@Zai_org`](https://x.com/Zai_org) | 模型發布 | <https://github.com/zai-org> 組織頁 | Z.ai（智譜）官網 | `讀不到：頁面要跑 JavaScript` |
| [`@MiniMax_AI`](https://x.com/MiniMax_AI) | 公司消息、模型發布 | <https://github.com/MiniMax-AI>、<https://huggingface.co/MiniMaxAI> | MiniMax 官網 | `未測` |
| [`@Hailuo_AI`](https://x.com/Hailuo_AI) | 海螺產品更新 | 只有第三方：<https://yespress.io/products/hailuo-ai.md> | 海螺官網 | `未測` |
| [`@Kling_ai`](https://x.com/Kling_ai) | 可靈產品更新 | <https://kling.ai/> 頁尾 | <https://kling.ai/> | `未測` |

備註：MiniMax 是**一個底線**的 `@MiniMax_AI`，兩個官方頁面都這樣寫。差一個字元是常見的冒名手法，
追蹤時用眼睛對一次。

### 開發工具與平台

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@cursor_ai`](https://x.com/cursor_ai) | 產品更新 | <https://cursor.com/> 頁尾 | <https://cursor.com/blog>；<https://cursor.com/changelog> | `Cursor blog`；Changelog 是`候選` |
| [`@cognition`](https://x.com/cognition) | Devin 與公司消息 | <https://cognition.com/> 頁尾 | <https://cognition.com/blog> | `Cognition blog` |
| [`@huggingface`](https://x.com/huggingface) | 公司與社群消息 | <https://huggingface.co/> 頁尾 | <https://huggingface.co/blog> | `Hugging Face blog` |
| [`@NVIDIAAI`](https://x.com/NVIDIAAI) | AI 相關消息 | <https://www.nvidia.com/en-us/ai/> 頁尾 | <https://blogs.nvidia.com/> | `NVIDIA blog` |
| [`@openrouter`](https://x.com/openrouter) | 模型上架、產品更新 | <https://openrouter.ai/about> 頁尾 | <https://openrouter.ai/blog/> | `候選` |
| [`@ollama`](https://x.com/ollama) | 產品更新 | <https://ollama.com/> 頁尾 | <https://ollama.com/blog> | `候選` |

備註：Windsurf 在 2026-06-02 改成 Devin Desktop，`windsurf.com` 轉到 `devin.ai/desktop`。`@windsurf`
之後怎麼了、有沒有 Devin 專用帳號，都沒有查到；只有 `@cognition` 確認過。

### 影像、影片、聲音

| X 帳號 | 發什麼 | 查證依據 | 官網頁面 | 掃描器狀態 |
| --- | --- | --- | --- | --- |
| [`@midjourney`](https://x.com/midjourney) | 產品更新 | <https://github.com/midjourney> 組織頁 | Midjourney 官網 | `讀不到：頁面要跑 JavaScript` |
| [`@runwayml`](https://x.com/runwayml) | 產品更新 | <https://runway.com/> 頁尾 | <https://runway.com/> | `讀不到：頁面要跑 JavaScript` |
| [`@LumaLabsAI`](https://x.com/LumaLabsAI) | 產品更新 | <https://github.com/lumalabs> 組織頁 | Luma 官網 | `未測` |
| [`@suno`](https://x.com/suno) | 產品更新 | <https://suno.com/about> 頁尾 | <https://suno.com/> | `未測` |
| `@ElevenLabs` 或 `@elevenlabsio` | 產品更新 | 互相矛盾：<https://github.com/elevenlabs> 寫 `@elevenlabs`，<https://huggingface.co/elevenlabs> 寫 `@elevenlabsio` | <https://elevenlabs.io/blog> | `ElevenLabs blog` |

## 為什麼不讀 X

- 2026-09-30 的決定：X 的 API 要付費、服務條款限制、x.com 擋爬蟲，而且一則貼文照
  `docs/news-2026-batch-4/BRIEF.md` 的規則不算查證依據，只能當線索。
- 2026-10-10 查到的價格（<https://docs.x.com/x-api/getting-started/pricing>）：只有按用量計費，
  讀一則貼文 0.005 美元、讀一筆帳號資料 0.010 美元，每個計費週期最多讀 300 萬則，沒有免費層。
  站主看過後決定不用。
- 官方帳號貼的公告多半連回自家的部落格或更新紀錄，那些頁面掃描器讀得到，也能當第一方證據。
  所以要補的是「官網頁面」那一欄裡還讀不到的列，不是 X。
