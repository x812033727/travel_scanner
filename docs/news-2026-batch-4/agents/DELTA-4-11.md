# 批次 4.11（Claude Code mods，一篇，五語）：對既有規格的差異

批次 4.11 照 [`DELTA-4-10.md`](DELTA-4-10.md) → [`DELTA-4-9.md`](DELTA-4-9.md) 的做法走：沿用它們引用的所有規則，
路徑、代理分工、研究紀錄 schema、查核報告的格式都一樣。下面只寫不同的地方。
**這份文件的規則優先於 DELTA-4-10、DELTA-4-9 與它們引用的各份規格裡與它衝突的句子。**

## 1. 為什麼有這一批

- Anthropic 在 2026-10-01 於 `claude.com/blog` 發表「Customize Claude Code with mods in TypeScript」：
  mods 是裝在 plugin 裡、在 Claude Code 自己的行程內執行的 TypeScript／JavaScript 函式，
  可以改寫提示、攔截工具呼叫、核准或拒絕權限、畫新的介面、取代內建功能。
- 每小時的自動化看不到 `claude.com/blog`（候選清單 4.8 已指出自動化不收 `openai.com`、`anthropic.com`、`claude.com`），
  站上到 2026-10-03 沒有任何一篇寫 plugins、marketplace 或 mods 的新聞。
- 站主 2026-10-03 要求規劃一篇，要回答四個問題：**mods 是什麼、能做什麼、用在哪、怎麼開始用**。

| slug | order | 事件日（台北） | 日期依據 |
| --- | --- | --- | --- |
| `ai-news-claude-code-mods-20261001` | 192 | 2026-10-01 | 部落格頁只印日期（October 1, 2026），沒有時刻。照 Opus 5.5 的判例（DELTA-4-8 第 4 條）照印、不換算；研究代理若在一手頁找到時刻，照 DELTA-4-5 第 6 條換算台北時間並回報 |

`display_order` 由 `check_article.py` 的 `RELATED`（`# 4.11` 區）決定。`topics` 是 `["ai", "software", "ai-news"]`。

## 2. 來源只用 Anthropic 自己的頁面

協調者 2026-10-03 用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 讀過下列頁面，
全部 HTTP 200、有正文；研究代理當天**要再讀一次**，`checked_on` 寫自己打開的那天。

- 公告：`https://claude.com/blog/claude-code-mods`（Product announcements，Reading time 5 min）。
- 文件（`https://code.claude.com/docs/en/plugins/mods/` 底下）：
  `overview`（定義、能做什麼、與 settings hooks／skills／MCP 的比較表、內建 mods 表、哪些地方會畫介面）、
  `create`（請 Claude 寫一個 mod、自己寫 first-mod 的三個檔案、`claude plugin validate`、`claude plugin test`、怎麼分享）、
  `reference`（事件、mods API、render sites、限制、設定與環境變數、指令）、
  `admin`（`sec-default`、`allowManagedModsOnly`、`prependPlugins`、`disableSideloadFlags`、政策 mod 範例）。
  其餘頁（`interface`、`events`、`api`、`test`、`troubleshoot`、`gallery`）可以讀，需要才引用。
- GitHub 上 Anthropic 自己的檔案：`anthropics/claude-code` 的 `mods/` 目錄（`sec-default`、`diff`、`agents-md`、`telemetry` 的源碼）
  與 `mods/types/claude-code.d.ts`；`anthropics/claude-code-playground` 的 `claude-code/mods`
  （`token-weather`、`blast-radius`、`replay-theater` 三個範例）。**要真的打開那個 repo 頁面、看到目錄存在才可以寫**；
  文件說範例「shared as they are, without support」，要照寫。
- 部落格說 Anthropic「在發表前把 mods 的設計放上 GitHub 徵求意見」。找不到那則 issue／discussion 的真實網址就只寫
  「Anthropic 表示」，**不猜網址、不猜編號**（BRIEF「猜識別碼、猜網址都屬於捏造」）。
- `sources` 最多 4 條，建議：部落格、`overview`、`create`、`admin`（企業段落用到 `reference` 的設定表再換）。
- 下列只能當線索、**不能**當來源，正文也不可以轉述它們獨有的說法：`smartscope.blog`、`aitmpl.com`、`digitalapplied.com`、
  `neurycode.com`、`blog.4sapi.com`、`KilimcininKorOglu/claude-code-mods`，以及任何媒體、整合站與使用者心得。
  其中有幾篇還在教讀者設 `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`，那是 early access 的做法，現在的文件明寫這個變數已被忽略。

## 3. 文章要回答的四個問題，與五節的建議

開頭兩段照 BRIEF：第一段寫 2026 年 10 月 1 日發生了什麼；第二段寫查核日，並交代**本站沒有安裝或執行任何 mod，
以下全部來自 Anthropic 的公告與文件**。`summary` 接在後面、第一個 heading 之前。

| # | 小節（撰稿者可改字，不可改範圍） | 回答哪個問題 | 必須寫到的事 |
| --- | --- | --- | --- |
| 1 | mods 是什麼：裝在 plugin 裡、在 Claude Code 行程內跑的函式 | 是什麼 | 一個 mod 是一個 plugin 加一個 hooks module（`.claude-plugin/plugin.json`、`hooks/hooks.json` 的 `modules`、`hooks/register.js`）；`register(on)` 註冊事件處理函式；每個函式拿到 `$`（mods API）、`e`（事件）、`next`；三種處理方式：觀察、改寫、接手。文件把設定檔裡的舊式 hook 叫 settings hook，兩者都叫 hook，**這一節要一次講清楚** |
| 2 | 能做什麼：改提示、管工具呼叫、畫介面、加指令、取代內建功能 | 能做什麼 | 部落格列的能力：改寫提示、擋／改／重試工具呼叫、核准或拒絕權限、遮掉工具輸出裡的機密、改或換介面元素、加按鈕與輸入框；多個 mod 依載入順序疊加；`/diff` 已改成 mod，可關可換。**本節結尾放表**：mod、settings hook、skill、MCP server 四欄，列「是什麼／能改什麼／能不能畫介面／寫什麼」，照 `overview` 的比較表逐欄對、儲存格要短 |
| 3 | 用在哪：個人的小工具與團隊的管控 | 應用在哪 | 部落格的三個團隊例子（CI/CD 狀態窗格、碰 production 設定前要確認、載入最前面的稽核 mod）；文件的範例 mod（三個）；內建 mods（`cc-plugin-diff`、`cc-plugin-agents-md`、`cc-plugin-sec-default`、`cc-plugin-telemetry`、預設關閉的 `cc-plugin-you-should-know`）名稱照 `/plugin` 顯示。生活化情境要標明是編輯設計的例子。**本節結尾放圖解** |
| 4 | 怎麼開始用：版本、安裝、請 Claude 寫、自己寫 | 怎麼用 | Claude Code v2.1.287 以上（文件寫，部落格沒寫，歸因到文件）；`/plugin install <name>@<marketplace>`；`claude --plugin-dir <dir>` 載入一個目錄、存檔即熱重載；在 session 裡請 Claude 寫（內建 `plugin-authoring` skill，寫到 `~/.claude/dev-mods/<session id>/`，要你核准才載入，`cleanupPeriodDays` 到了會刪）；`claude plugin validate` 列出它處理的事件與呼叫的方法；`claude plugin test`；哪裡會畫、哪裡只跑不畫（見第 4 節第 7 條） |
| 5 | 安全與企業管控 | 用在哪／怎麼用 | 不是沙盒、與使用者同等權限、能讀環境變數與設定、能在你被問之前核准工具呼叫、能用你的方案呼叫模型；**改不了權限提示本身**；`sec-default` 的載入條件與它守的東西；管理者的四個開關（`allowManagedModsOnly`、`disableSideloadFlags`、`prependPlugins`／`appendPlugins`、`disableAllHooks`）；個人關掉的方法（`/plugin` 停用、`--safe-mode`、`disableAllHooks`） |

`faq` 候選（挑 4–6 題，答案只能是正文寫過的）：要什麼版本、要不要 Node.js 或 build step（文件：不用）、
settings hooks 會不會被淘汰（文件：「Nothing about them is deprecated」）、怎麼整個關掉、
個人的 Free／Pro／Max 帳號能不能用（部落格只說 CLI 與 desktop app 都能用，**方案沒寫，就寫「官方未說明」**）、
雲端 session 與 VS Code 外掛能不能用（文件：hooks 跑、不畫）。

一般 `callout` 一個：本站沒有實測；mod 與你同權限、只裝信得過的來源（照部落格那句歸因）。**不掛 `finance`、沒有免責 callout**（同 `ai.md`）。

圖解 2×2（研究紀錄的 `diagram.nodes`，小標 ≤ 8 字、說明 ≤ 14 字）建議骨架：
左上「事件」（工具呼叫、提示、畫面）→ 右上「函式」（事件前、後或取代）→ 左下「介面」（窗格、按鈕、指令）→ 右下「管控」（sec-default 先載入）。
圖上不畫任何商標、字標或介面截圖，產品名用純文字。

## 4. 容易寫錯的事實（對撰稿與查核都有拘束力）

1. **「hook」有兩個意思。** mod 的事件處理函式叫 hook，設定檔裡的 `PreToolUse`／`PostToolUse` 那種文件叫 settings hook。
   正文第一節講清楚之後，固定用兩個不同的中文詞（例如「設定檔 Hook」與「mod 的事件函式」），不可以混用。
   站上既有的 `claude-code-hooks-*` 教學寫的都是 settings hooks。
2. **不要寫 mods 取代 hooks。** 文件明寫 settings hooks 照常運作、沒有被淘汰；部落格說的是「hooks 做不到的，mods 做得到」。
3. **不要寫 mods 是沙盒、或有任何隔離。** 部落格與文件都說不是；開了 sandboxing 也只隔離 Claude 跑的 Bash 命令，mod 自己啟動的程式在外面。
4. **`sec-default` 的載入條件照文件：** 機器有 managed settings，**或**使用者以 Team／Enterprise 方案登入。
   用 API key、Bedrock、Google Cloud、Microsoft Foundry 登入的人，只在有 managed settings 的機器才有。
   部落格那句「Team and Enterprise plans, and any machine with managed settings」是同一件事，不要寫成「企業版才有」。
5. **它守的範圍也照文件：** 擋使用者的 mod 改管理者管的東西（managed hooks 收到與決定的事、系統提示、managed `CLAUDE.md` 與其他受管指示、任何 mod 讀到的 settings、managed MCP 伺服器的工具與描述），
   以及擋使用者的 mod 核准 `deny` 規則拒絕的呼叫。**其他都不擋**：使用者的 mod 照樣能讀寫檔案、起程式、連網路、改寫提示。
   `deny` 規則與 managed hooks 只管 Claude 的工具呼叫，管不到 mod 自己的 `$.fs`／`$.process` 呼叫（admin 頁明寫 `Read(.env)` 被拒時 mod 仍能用 `$.fs.read` 讀），不可寫成「deny 規則擋得住 mod」。
6. **版本門檻 v2.1.287** 只在文件；`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` 是 early access 的變數，現在設成任何值都被忽略，**不寫成啟用方法**。
7. **哪裡會畫介面，照 `overview` 的表：** 終端機（含編輯器內建終端、JetBrains 外掛）與 Desktop app 的 Code 分頁會畫；
   Desktop 的 WSL session 連 hooks 都不跑；VS Code 外掛的聊天面板、`claude -p`、Agent SDK、雲端 session 是「hooks 跑、不畫」；
   Remote Control 是「hooks 在你電腦上的 session 跑、畫在你電腦的終端機」，不是「不畫」（研究代理 2026-10-04 依 overview 的表修正）。
   不可以寫「所有地方都能用」，也不可以把「不畫」寫成「不能用」。
8. **內建 mods 的名稱**照 `/plugin` 顯示（overview 的表有六列：`cc-plugin-agents-md`、`cc-plugin-diff`、`cc-plugin-plugin-authoring`、`cc-plugin-sec-default`、`cc-plugin-telemetry`、`cc-plugin-you-should-know`；第 3 節的小節表少列了 `cc-plugin-plugin-authoring`，以六列為準）；關掉 `cc-plugin-diff` 之後 `/diff` 命令還在，由內建版本回答。
   `cc-plugin-you-should-know` 預設關閉、且文件說「if available for your org」，不可寫成人人都有。
9. **`/plugin install token-chart@your-org`** 是文件範例裡的假名字，不是真的外掛；要舉例就寫明是文件的範例，或改用三個真的範例 mod。
10. **三個範例 mod 的名字與功能照 `overview`**：`token-weather` 畫 context window 預報、`blast-radius` 攔下 `rm -rf` 或 force push 這類命令並顯示影響、
    `replay-theater` 加 `/replay` 命令重播上一輪的檔案修改。寫它們之前要打開 repo 看到目錄。
11. **限制數字**（一個 hook 10 秒、`$.store` 4 MiB、`$.ui.toast` 4 秒之類）要寫就在 `reference` 頁逐字對過，而且頂多挑兩三個；不要把整張表抄進來。
12. **「Claude directory」與「Anthropic's directory」**：部落格用前者、文件用後者，各自逐字；不要寫成「Claude Marketplace」——那是 9 月 23 日另一個產品（合作夥伴的 plugins、agents 與 services），一手頁沒有把兩者連起來就不要連。
13. **部落格說 mods 可以「用 Claude Code 寫 Claude Code 的 mod」**：寫成 Anthropic 說明的功能，不寫成本站試過。
14. **不寫價格、不寫用量比較。** 唯一可寫的用量事實是文件說 `$.model.complete` 會用使用者的方案或 API key，照寫、歸因。
15. **「Code with mods」**是站主的口語，不是官方名稱。正文用小寫 `mods`；外文第一次出現要帶中文說明（例如「mods（改寫 Claude Code 行為與介面的小型程式）」），之後直接寫 mods。
16. 官方頁的原文引用照 BRIEF 第 1 條：`verbatim_quote` 只能是來源頁原樣搜尋得到的連續字串，部落格裡的彎引號（’）與 `·` 照抄。

## 5. 兩個結尾連結與 `related`

- 第一個：AI 索引，標題不改：`2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用`，網址 `https://mokaair.com/zh-TW/life/ai-news-2026-january-september-index`。
- 第二個：`ai-news-claude-sonnet-55-20260928`，text 逐字為 `Claude Sonnet 5.5 推出：牌價與 Sonnet 5 相同，API、雲端平台與 Claude.ai 都能用`，
  網址 `https://mokaair.com/zh-TW/life/ai-news-claude-sonnet-55-20260928`。這篇五語齊全；站上沒有五語的 plugins 或 hooks 新聞可指。
- `related` 放 `ai-news-claude-sonnet-55-20260928` 與 `ai-news-claude-opus-55-20260922`，兩篇都五語齊全。
- zh-TW 正文定稿後跑 `pack_cli autolink`，可以掛上教學系列的 `claude-code-plugins-guide`（`Claude Code｜Plugins 安裝與管理`）與
  `claude-code-hooks-getting-started`（`Claude Code｜建立第一個 Hook`）。這兩篇只有 zh-TW，**其他四語不掛**（`--full` 會查連結目標的語系）。

## 6. 索引、活頁面、查核報告

- 索引由協調者在同一個 PR 用 `update_index.py ai` 五語一起補，先 `--dry-run`；撰稿與翻譯代理不碰索引。
  索引標題「1 月至 9 月」在 10 月的文章進來後會過期：**本票不改標題**（改了會波及 30 個內容包的連結文字，見 `ai.md`），開一張後續票決定怎麼改。
- **活頁面**：`reference` 標「as of v2.1.287」，其他三頁寫「v2.1.287 or later」，內建 mods 表、限制表、設定表每個版本都會變；GitHub 上的 `claude-code.d.ts` 第一行寫它的版本。
  研究紀錄的 `live_data_warnings` 要列出來，正文寫「截至查核日的文件版本」，發布當天由協調者重讀四頁。
- 查核報告：`factcheck-draft/ai-news-claude-code-mods-20261001-round1.md`、`-round2.md`。兩輪由不同的 opus 代理做，第二輪逐句回一手來源。

## 6a. 研究後的裁決（協調者 2026-10-04）

- 限制數字（hook 10 秒、`$.store` 4 MiB 等）**不寫**：它們只在 `reference` 頁，換進 `sources[]` 會擠掉 `admin` 或 `create`，而且對讀者不是重點。
- 部落格提到的 GitHub 設計討論：連結在部落格頁上，但本環境打不開那個 issue，正文只寫「Anthropic 表示發表前把設計放上 GitHub 徵求意見」，**不放網址、不寫編號**。
- 管理者開關只寫 `allowManagedModsOnly`、`disableSideloadFlags`、`prependPlugins`／`appendPlugins`、`disableAllHooks` 與 `--safe-mode`；`allowManagedHooksOnly`、`allowModsToOverrideDenyRules` 不寫（admin 頁有，但本篇不是管理手冊）。
- 研究紀錄 `verified_facts` 有 94 條、逐字比對全過；撰稿只能用那 94 條撐事實。

## 7. 不在本票範圍、要另開票的事

- 教學系列（`docs/claude-code-series`，zh-TW）加一課「建立第一個 mod」：照文件的 first-mod 做（計數工具呼叫、spinner 顯示、`/tally` 命令、`claude plugin validate`、`claude plugin test`），接在 `claude-code-plugins-guide` 與 `claude-code-plugin-team-distribution` 之後。這篇新聞只講概念與入口，不教寫。
- 新聞自動化加掛 `claude.com/blog` 來源（4.8 候選清單第 1 條只提了 OpenAI 的 feed）。
- AI 索引標題的月份範圍怎麼跟著 10 月走。
