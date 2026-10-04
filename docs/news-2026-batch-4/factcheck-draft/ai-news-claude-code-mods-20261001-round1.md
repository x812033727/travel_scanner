# 查核報告（第一輪）：ai-news-claude-code-mods-20261001

- 查核者：獨立查核代理（第一輪，opus），2026-10-04（台北）
- 規格：`agents/ai/FACTCHECK.md`（Windows 路徑、corrections-ai.md 與「這一批特有的事」不適用）、`agents/DELTA-4-11.md`（第 4 節十六條與第 6a 節有拘束力）、`BRIEF.md` 最後一節錯誤型態、`ai.md`
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-claude-code-mods-20261001.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-claude-code-mods-20261001.json`（只加 `factcheck`；`title`、`diagram` 不必動）
- 暫存與原始回應：`/root/news411/agents/fc1/`（`raw/`、`norm/`、`fetch.sh`、`fetch-log.tsv`、`check_quotes.py`／`check_quotes.log`、`edit_pack.py`、`edit_research.py`、`pack.diff`、`pack.before.json`、`check0.log`（改前）、`check.log`（改後）、`pg-clone/`、`cc-clone/`）

## 摘要

- 主張約 100 條：CONFIRMED 77、CHANGED 19、補寫 4（漏掉的 Remote Control 一列、內建 mods、`/diff` 停用後仍在、`disableAllHooks` 連受管設定檔 Hook 也停）。
- **內容包改了 19 處**（事實或範圍 13 處、歸因與措辭 6 處），另為了字數上限刪了 5 句不帶事實的敘述。研究紀錄加 `factcheck`。
- 最重的五處：
  1. **WSL session**：原句「終端機與 Desktop app 的 Code 分頁（WSL session 除外…）會畫」讓 WSL 看起來只是「不畫」；overview 表寫 `No, because plugins aren't available in WSL sessions`，連事件函式都不跑。Where mods run 改成獨立一段，並補上整列漏掉的 **Remote Control**（`Yes, in the session on your machine`／`In the terminal on your machine`）。
  2. **deny 規則的範圍**：原句「deny 規則也管不到 mod 自己的 $.fs」漏了 `$.process`（admin：`Neither applies to a mod's own $.fs and $.process calls`），而「核准被 deny 規則拒絕的呼叫」沒寫只限 Claude 的工具呼叫（`Both apply to Claude's tool calls`）。兩處補齊。
  3. **管理者開關收窄**：`disableSideloadFlags` 漏了「Claude 在 session 裡寫的 mods 也不能載入」；managed `disableAllHooks` 漏了「受管的 PreToolUse 等設定檔 Hook 也一起關」。對管理者這兩條正是取捨的關鍵。
  4. **內建 mods 與 `/diff`**：原文只提 diff 與 sec-default，沒有 DELTA 要求的 `cc-plugin-you-should-know`（預設關閉、`if available for your org`）；「`/diff` 可在 /plugin 關掉或換掉」把 `in /plugin` 套到換掉上，也沒寫停用 `cc-plugin-diff` 之後 `/diff` 還在、由內建版本回答。
  5. **安裝格式的歸因**：「部落格說……格式是 /plugin install 加 plugin 名稱、@ 與 marketplace 名稱」——格式是 overview 寫的，部落格沒有。改歸因到文件。
- 自檢：`OK ai-news-claude-code-mods-20261001 zh-TW paragraphs 2999`（exit 0，零 FAIL；改前 2969，加事實後一度 3,511，再精簡敘述壓回）。
- 結論：`needs_second_round`（事實改動超過十處；DELTA-4-11 第 6 節本來就要兩輪）。

## 重抓結果（2026-10-03 UTC，台北 2026-10-04）

UA：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --compressed --max-time 60`，間隔 1.3 秒；請求、標頭、查詢字串都沒有任何人的 email 或個資。

| 時間（UTC） | 網址 | HTTP | 傳輸 bytes（gzip） | 落地 bytes（解壓） | 正文？ |
| --- | --- | --- | --- | --- | --- |
| 18:47:01 | https://claude.com/blog/claude-code-mods | 200，0 次轉址 | 99,345 | 532,059（與研究代理 md5 相同） | 是：h1、Date October 1, 2026、Why we built mods → Getting started 全文 |
| 18:47:03 | https://code.claude.com/docs/en/plugins/mods/overview | 200，0 | 90,428 | 526,328（相同） | 是：定義、What a mod can reach、Turn mods on or off、Where mods run 表、比較表、內建 mods 表 |
| 18:47:05 | https://code.claude.com/docs/en/plugins/mods/create | 200，0 | 96,979 | 656,741（相同） | 是：Ask Claude for a mod、first-mod 教學、validate、test、Share |
| 18:47:06 | https://code.claude.com/docs/en/plugins/mods/admin | 200，0 | 98,953 | 646,270（相同） | 是：allowManagedModsOnly、Know what happens by default、Choose how much to allow、prependPlugins |
| 18:47:08–11 | 上面三頁的 `.md` 版 | 200，0 | 8,185／8,770／10,629 | 23,225／25,270／33,874 | 是：與 HTML 版可見文字一致，用來讀表格 |

**bytes 差異的原因**：伺服器回 `content-encoding: gzip`。撰稿者回報的「約 9–10 萬」是 curl `size_download`（線上壓縮後的傳輸量）；研究代理的 52–66 萬是 `--compressed` 解壓後的落地檔。兩者是同一份頁面：四個落地檔與研究代理的 md5 逐位元組相同（`73a0d6ed…`、`5808840c…`、`2d254322…`、`ac4549dd…`），頁首 `Last Published: Fri Oct 02 2026 18:00:44 GMT` 也一樣。沒有 403、軟性 404 或擋阻頁。

GitHub：`github.com/anthropics/claude-code-playground/tree/main/claude-code/mods` 對本環境回 403、378 bytes，body 是出口代理的訊息（`GitHub access to this repository is not enabled for this session`），不是 GitHub 拒絕。換路：`git clone --depth 1 --filter=blob:none --no-checkout` 兩個公開 repo，`git ls-tree` 列目錄：

- `anthropics/claude-code-playground`（HEAD `569c5283`，2026-10-01T09:11:57-07:00）：`claude-code/mods/token-weather`、`blast-radius`、`replay-theater`、`.claude-plugin`（marketplace 名 `claude-code-playground-mods`，描述 `Shared as-is.`）。三個 README 經 raw.githubusercontent.com 讀到（200）。
- `anthropics/claude-code`（HEAD `1c229fcd`，2026-10-02T20:19:38Z）：`mods/agents-md`、`diff`、`sec-default`、`telemetry`、`types`。

`verbatim_quote` 逐字比對：HTML 刪註解與 script／style／noscript／svg／template 後，做 A（行內標籤→無、其他→空格）、B（全部→空格）、C（全部→無）三種正規化加 RAW；**94/94 通過**，全部在 A 版命中，所有 `url` 都在 `sources[]`（`check_quotes.log`）。

## 主張逐條

來源代號：B＝部落格、O＝overview、C＝create、A＝admin。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | Claude Code 推出 mods、用 TypeScript 改寫行為與介面 | CONFIRMED | B 副標 `Change how Claude Code behaves and looks with a few lines of TypeScript.` |
| 2 | title | 裝在 plugin 裡 | CONFIRMED | B `Mods ship inside plugins` |
| 3 | description | 10/1 發表；plugin 裡、行程內的 TS 或 JS 函式 | CONFIRMED | B 日期；O `JavaScript or TypeScript event handlers`、比較表 `in its own process` |
| 4 | description | 可改寫提示、管工具呼叫、畫新介面 | CONFIRMED | B |
| 5 | description | 「CLI 與 desktop app 能用」未歸因 | **CHANGED**（歸因 Anthropic） | B `They work in the Claude Code CLI and desktop app.` |
| 6 | description | 文件寫 v2.1.287 以上；Anthropic 說沒有沙盒 | CONFIRMED | O、A；B `They aren’t sandboxed` |
| 7 | 第 1 段 | 10/1 發表、括號中文說明、TS 或 JS、plugin、行程內 | CONFIRMED | B、O |
| 8 | 第 1 段 | Anthropic 說 CLI 與 desktop app 都能用 | CONFIRMED | B |
| 9 | 第 1 段 | 「文件寫要 v2.1.287 以上」 | 刪（重複；第四節保留） | 字數 |
| 10 | 第 1 段 | 「寫工具的開發者與替團隊管設定的管理者最相關」 | 刪（編輯判斷，不帶事實） | 字數 |
| 11 | 第 2 段 | 10/4 查核、依據部落格與三頁文件 | CONFIRMED | `sources[]` 四條 `checked_on` 一致 |
| 12 | 第 2 段 | 沒有安裝或執行任何 mod、都是 Anthropic 的說法 | CONFIRMED | 編輯聲明 |
| 13 | 第 2 段 | 「也不是訂閱或購買建議」 | 刪（字數；全文沒有購買建議，不影響界線） | — |
| 14 | summary 1 | 10/1、plugin、行程內、CLI 與 desktop、v2.1.287 歸因文件 | CONFIRMED | B、O |
| 15 | summary 2 | 能力清單未歸因 | **CHANGED**（加「Anthropic 說」） | B 的能力是廠商自述 |
| 16 | summary 2 | 「文件寫兩者並行」 | **CHANGED** →「文件寫設定檔 Hook 照舊執行，沒有被淘汰」 | A `run as before, alongside mods. Nothing about them is deprecated.`；正文精簡後只留「照舊執行、沒有被淘汰」 |
| 17 | summary 3 | 沒有沙盒、同權限、只裝信得過的 | CONFIRMED | B（callout 歸因）、O |
| 18 | summary 3 | sec-default 沒寫載入條件 | **CHANGED**（補 managed settings 或 Team、Enterprise） | A `The guard loads when either of these is true` |
| 19 | summary 3 | 只擋改管理者管的東西與核准 deny 拒絕的呼叫，其他都不擋 | **CHANGED**（「呼叫」→「工具呼叫」） | A `Both apply to Claude's tool calls`、`Everything else is allowed` |
| 20 | summary 4 | 管理者四個開關；個人三種；後兩者不停內建 mods | CONFIRMED | A、O `don’t stop built-in mods` |
| 21 | summary 5 | 文件與內建 mods 表會隨版本更新 | CONFIRMED（編輯提醒） | C `can change between releases` |
| 22 | 第 1 節第 1 段 | Claude Code 每做一件事發出事件；mod 掛在事件上；之前、之後或取代 | CONFIRMED | B |
| 23 | 同上 | 三個檔案路徑 | CONFIRMED | O、C |
| 24 | 同上 | modules 欄、有它才算 mod | CONFIRMED | C `having it is what makes the plugin a mod` |
| 25 | 第 1 節第 2 段 | 載入時呼叫 register、傳入 on | CONFIRMED | C |
| 26 | 同上 | $、e、next 的定義 | CONFIRMED | C |
| 27 | 同上 | 「處理方式有三種」 | **CHANGED** →「文件列出三種處理方式」 | O 是 `It can:` 的三項；B 另有 `wrap`，不寫成封閉清單 |
| 28 | 同上 | 接手：自己處理、原本行為不執行 | CONFIRMED | O `Answer` |
| 29 | 第 1 節第 3 段 | Claude Code 把兩種都叫 hooks；設定檔 Hook／mod 的事件函式 | CONFIRMED | O Note |
| 30 | 全文 | 兩個詞固定、不混用；沒有 mods 取代 hooks | CONFIRMED | grep：單獨的 Hook／hook 只出現在檔名、`disableAllHooks` 與「Claude Code 把兩種都叫 hooks」 |
| 31 | 第 2 節第 1 段 | 部落格列的四項＋介面兩項，歸因 Anthropic | CONFIRMED | B |
| 32 | 同上 | 文件補充：窗格、提示框上方橫條、不經 Claude 回合的 /command | CONFIRMED | O |
| 33 | 第 2 節第 2 段 | 「多個 mods 依載入順序疊加」 | **CHANGED** →「掛同一個事件時依載入順序執行」 | B `When several mods hook the same event, they run in the order they load` |
| 34 | 同上 | 最先載入的最先看到事件、最後看到結果 | CONFIRMED | B |
| 35 | 同上 | 「/diff 可在 /plugin 關掉或換掉」 | **CHANGED** →「可在 /plugin 關掉，或換成自己的版本」 | B `turn it off (in /plugin) or replace it with your own version`（`in /plugin` 只掛在關掉） |
| 36 | 同上 | （漏）停用後 /diff 還在 | **補寫** | O `/diff stays, and Claude Code's built-in version of the command answers it.` |
| 37 | 同上 | Anthropic 說設定檔 Hook 不能改寫事件、畫新介面、取代功能 | CONFIRMED | B（其 Hooks 連到 docs/en/hooks，就是 settings hooks） |
| 38 | 同上 | 文件寫照舊執行、沒有任何一項被淘汰 | CONFIRMED | A |
| 39 | 同上 | 「只有 mod 能畫介面」 | **CHANGED** →「下表四者中只有 mod 能畫介面」 | O 比較表 `Yes No No No`；範圍限於表（O 開頭把 status lines 與它們並列） |
| 40–51 | 表格 12 格 | mod／設定檔 Hook／skill／MCP server 的是什麼、能改什麼、寫什麼 | CONFIRMED（逐格） | O 比較表三列；「參數與結果」是 `a tool call's arguments and result` 的省略，主詞在同格 |
| 52 | 表格 caption | 依總覽頁比較表縮短、查核日 10/4 | CONFIRMED | — |
| 53 | 第 3 節第 1 段 | 部落格三個團隊例子 | CONFIRMED | B `For example:` 三項；production 那例改照原文「指令碰到 production 設定前」 |
| 54 | 同上 | 「這些是可以這樣做的例子，不是現成的產品」 | **CHANGED** →「三個團隊可以用 mods 自己做的例子」 | 否定句超出來源；B 寫 `Teams can also use mods to build their own controls and functionality` |
| 55 | 第 3 節第 2 段 | 範例在 claude-code-playground、照原樣分享、不提供支援 | CONFIRMED | O；git ls-tree 看到三個目錄 |
| 56–58 | 同上 | token-weather／blast-radius／replay-theater 的功能 | CONFIRMED | O 三行；沒有寫 plugin.json 才有的 `git reset --hard` 等 |
| 59 | 第 3 節第 3 段 | 內建 mods 在 /plugin 的 Built-in 底下 | **CHANGED**（補 Installed 分頁） | O `go to the Installed tab, which lists them under Built-in` |
| 60 | 同上 | cc-plugin-diff 接手 /diff；sec-default 見下一節 | CONFIRMED | O 內建表 |
| 61 | 同上 | （漏）cc-plugin-you-should-know 預設關閉、if available for your org | **補寫** | O 內建表；DELTA 第 3 節必寫、第 4 節第 8 條。以「例如」列名，不寫「六個」等清點 |
| 62 | 圖解 caption | 事件、函式、介面；有受管設定的電腦或 Team／Enterprise 時 sec-default 先載入 | CONFIRMED | B、O、A；與研究紀錄 `diagram.caption` 相同 |
| 63–66 | diagram 四格 | 事件／函式／介面／管控 | CONFIRMED | 同上 |
| 67 | hero_label | mods：改行為也改介面 | CONFIRMED | B 副標 |
| 68 | 第 4 節第 1 段 | v2.1.287 或以上、預設開啟、claude --version，歸因文件；部落格沒寫 | CONFIRMED | O；B 以 `2.1` 查 0 次，詞界 `version` 1 次是 `replace it with your own version`，不是版本門檻 |
| 69 | 同上 | Claude directory 或 /plugin 安裝 | CONFIRMED | B 逐字 `Claude directory` |
| 70 | 同上 | 「部落格說……格式是 /plugin install 加名稱、@、marketplace」 | **CHANGED**（格式改歸因文件） | 格式只在 O；B 沒有 |
| 71 | 第 4 節第 2 段 | 不需要 Node.js 或 build step | CONFIRMED | C |
| 72 | 同上 | --plugin-dir 一個 session、存檔熱重載 | CONFIRMED | C |
| 73 | 同上 | 「Anthropic 說 Claude 可以寫 TypeScript 並熱重載」 | 刪（字數；同段保留文件版本，仍寫成文件說明的功能） | B |
| 74 | 同上 | plugin-authoring skill、~/.claude/dev-mods/ 的 session 資料夾、要核准、cleanupPeriodDays | CONFIRMED | C |
| 75 | 第 4 節第 3 段 | 安裝前對目錄執行 claude plugin validate，不必執行就列出事件與方法 | CONFIRMED（補「先取得 plugin 的檔案」） | O `Get the plugin’s files first` |
| 76 | 原第 4 節第 3 段 | 終端機與 Code 分頁會畫 | CONFIRMED | O 表 |
| 77 | 同上 | 「（WSL session 除外，且有些元素只限終端機）會畫」 | **CHANGED** → WSL session「不能用 plugins，事件函式不跑」；Code 分頁畫不出只限終端機的元素 | O 表 `No, because plugins aren't available in WSL sessions` |
| 78 | 同上 | VS Code 聊天面板、claude -p、Agent SDK、雲端 session（送進雲端的 plugin）跑、不畫 | CONFIRMED | O 表 |
| 79 | 同上 | （漏）Remote Control | **補寫** | O 表 `Yes, in the session on your machine`／`In the terminal on your machine`；DELTA 第 4 節第 7 條 |
| 80 | 第 5 節第 1 段 | 部落格的同權限、沒有沙盒、只裝信得過的 | 移到 callout（仍歸因部落格）；本段改用 O `Mods aren't sandboxed`、`runs with your permissions` | 字數；內容沒有減少 |
| 81 | 同上 | 「能讀環境變數與設定檔裡的 API key」 | **CHANGED** →「能讀環境變數與設定檔（包括裡面的 API key）」 | O `environment variables and settings files, including an API key you keep in either`；原句可讀成只讀 API key |
| 82 | 同上 | 被問之前核准、用你的方案或 API key 呼叫模型、改不了權限提示 | CONFIRMED | O |
| 83 | 同上 | sandboxing 只隔離 Claude 執行的 Bash | CONFIRMED，**補**「mod 啟動的程式在沙盒外」 | O `a process that a mod starts runs outside it` |
| 84 | 第 5 節第 2 段 | 載入條件：managed settings 或 Team、Enterprise | CONFIRMED | A |
| 85 | 同上 | 「用 API key 或 Bedrock、Google Cloud、Foundry 登入的人」 | **CHANGED**（「登入」→「用…的人」） | A `authenticates with an API key, or through …`；Google Cloud 照 DELTA 第 4 條簡寫（原文 Google Cloud’s Agent Platform） |
| 86 | 同上 | 「受管設定檔 Hook」 | **CHANGED** →「受管設定檔 Hook 收到與決定的事」 | A `what your managed hooks receive or decide` |
| 87 | 同上 | 核准被 deny 規則拒絕的呼叫 | **CHANGED**（→工具呼叫） | A `Both apply to Claude's tool calls` |
| 88 | 同上 | 其他都允許 | CONFIRMED | A `Everything else is allowed. The guard adds no other restrictions.` |
| 89 | 同上 | deny 規則管不到 mod 自己的 $.fs | **CHANGED**（補 $.process） | A `Neither applies to a mod's own $.fs and $.process calls` |
| 90 | 第 5 節第 3 段 | allowManagedModsOnly 讓使用者帶來的 mods 不載入 | CONFIRMED | A |
| 91 | 同上 | disableSideloadFlags 拒絕 --plugin-dir 與 --plugin-url | **CHANGED**（補 Claude 在 session 裡寫的 mods） | A `and keeps mods Claude writes during a session from loading` |
| 92 | 同上 | prependPlugins／appendPlugins 決定順序；設 prependPlugins 要列 sec-default@builtin | CONFIRMED | A `The list replaces the default` |
| 93 | 同上 | managed disableAllHooks 連組織的 mods 也停 | CONFIRMED，**補**受管的設定檔 Hook 也停 | A `turns off every hook in settings files, so a PreToolUse hook in your managed settings no longer blocks anything` |
| 94 | 第 5 節第 4 段 | /plugin 停用；--safe-mode「關掉一個 session」 | **CHANGED**（寫明停一個 session 的已安裝 mods） | O `Every installed mod, for one session` |
| 95 | 同上 | 個人 disableAllHooks 連設定檔 Hook 與 status line 也停 | CONFIRMED，**補**「組織管理的照常」 | O `What your organization manages keeps running.` |
| 96 | 同上 | 後兩者不停內建 mods | CONFIRMED | O |
| 97 | FAQ 1、2、4、5、6 | 版本、Node.js、怎麼關、方案官方未說明、VS Code 與雲端 | CONFIRMED | 正文對應句；FAQ 5 照 DELTA 第 3 節寫「官方未說明」 |
| 98 | FAQ 3 | 「和 mods 並行」 | **CHANGED**（刪，正文已不寫這三字；其餘不變） | — |
| 99 | callout | 沒有實測、部落格的同權限提醒（歸因）、截至 10/4 | CONFIRMED | B |
| 100 | callout | 「會隨版本變動」 | **CHANGED** →「可能隨版本變動」 | C `can change between releases` |
| 101 | sources／checked_on／結尾連結／related | 四條 2026-10-04 一致；兩個連結與 related 照 DELTA 第 5 節 | CONFIRMED | 自檢通過；未動 |

## 改掉的地方（原文 → 改成，依據）

1. **description**：「CLI 與 desktop app 能用，文件寫要 v2.1.287 以上，Anthropic 說 mods 沒有沙盒」→「Anthropic 說 CLI 與 desktop app 能用、mods 沒有沙盒，文件寫要 v2.1.287 以上」。B 的可用範圍歸因。
2. **summary 2**：加「Anthropic 說」；「設定檔 Hook 沒有被淘汰，文件寫兩者並行」→「文件寫設定檔 Hook 照舊執行，沒有被淘汰」。
3. **summary 3**：sec-default 前補「在有 managed settings 的電腦或以 Team、Enterprise 方案登入時載入的」；「呼叫」→「工具呼叫」。A 的載入條件與 `Both apply to Claude's tool calls`。
4. **第 1 節第 2 段**：「處理方式有三種：觀察、改寫，以及接手：……」→「文件列出三種處理方式：觀察、改寫，以及接手（自己處理，原本的行為不執行）」。
5. **第 2 節第 2 段**：「多個 mods 依載入順序疊加」→「多個 mods 掛同一個事件時依載入順序執行」（B）。
6. **第 2 節第 2 段**：「內建的 /diff 現在是 mod，可在 /plugin 關掉或換掉」→「可在 /plugin 關掉，或換成自己的版本；文件說停用後 /diff 還在，由內建版本回答」（B、O 內建表）。
7. **第 2 節第 2 段**：「下表縮短自文件的比較表，只有 mod 能畫介面」→「下表四者中只有 mod 能畫介面」（縮短的說明已在 caption）。
8. **第 3 節第 1 段**：刪「這些是可以這樣做的例子，不是現成的產品」，改成「部落格舉了三個團隊可以用 mods 自己做的例子」；「碰 production 設定前」→「指令碰到 production 設定前」（B `before any command touches production config`）。
9. **第 3 節第 3 段**（內建 mods）：「Claude Code 也內建 mods，在 /plugin 的 Built-in 底下看：cc-plugin-diff 接手 /diff，cc-plugin-sec-default 見下一節」→「內建的 mods 列在 /plugin 的 Installed 分頁 Built-in 底下，例如接手 /diff 的 cc-plugin-diff 與見下一節的 cc-plugin-sec-default；cc-plugin-you-should-know 預設關閉，文件寫「if available for your org」才會列出」（O 內建表）。
10. **第 4 節第 1 段**：「部落格說可從 Claude directory 或……安裝含 mods 的 plugin，格式是……」→「……安裝含 mods 的 plugin；文件寫格式是 /plugin install 名稱@marketplace」（格式只在 O）。
11. **第 4 節第 3 段**：validate 前補「先取得 plugin 的檔案」（O `Get the plugin’s files first`），Where mods run 拆成第 4 段。
12. **第 4 節第 4 段（新）**：「文件寫，終端機與 Desktop app 的 Code 分頁會畫（Code 分頁畫不出只限終端機的元素）；Desktop 的 WSL session 不能用 plugins，事件函式不跑；VS Code 外掛的聊天面板、claude -p、Agent SDK 與雲端 session（限送得進去的 plugin）只跑不畫；用 Remote Control 時，事件函式在你電腦上的 session 跑、畫在你電腦的終端機。」原句的 WSL 括號與漏掉的 Remote Control 一併修正（O 表）。
13. **第 5 節第 1 段**：部落格那句同權限提醒移到 callout（已在，且歸因），本段以「文件寫 mods 沒有沙盒、以你的權限執行」開頭；「能讀環境變數與設定檔裡的 API key」→「能讀環境變數與設定檔（包括裡面的 API key）」；句尾補「mod 啟動的程式在沙盒外」（O）。
14. **第 5 節第 2 段**：「登入」→「用…的人」；「受管設定檔 Hook」→「受管設定檔 Hook 收到與決定的事」；「呼叫」→「工具呼叫」；「$.fs」→「$.fs 與 $.process 呼叫」（A）。
15. **第 5 節第 3 段**：disableSideloadFlags「拒絕 --plugin-dir 與 --plugin-url」→「拒絕 --plugin-dir、--plugin-url 與 Claude 在 session 裡寫的 mods」；disableAllHooks「連組織自己的 mods 也停」→「連組織的 mods 與受管的設定檔 Hook 都停」（A）。
16. **第 5 節第 4 段**：「用 --safe-mode 關掉一個 session」→「以 --safe-mode 停掉一個 session 的已安裝 mods」；disableAllHooks 補「組織管理的照常」（O）。
17. **FAQ 3**：刪「和 mods 並行」（配合第 7 處後正文的寫法）。
18. **callout**：「會隨版本變動」→「可能隨版本變動」。
19. **研究紀錄**：加 `factcheck`。

為了字數（加上第 9、12–16 處後一度 3,511 字）另刪了五句不帶事實的敘述：第 1 段的讀者定位句與重複的版本門檻、第 2 段「也不是訂閱或購買建議」、第 4 節第 2 段部落格的「Claude 可以寫 TypeScript 並熱重載」（同段保留文件寫的版本）、第 1 節第 3 段「用詞先分開：」。**沒有刪任何但書或限定詞。**

## DELTA-4-11 第 4 節十六條逐條

1. hook 兩義：第一節講清楚，之後只用「設定檔 Hook」「mod 的事件函式」。✔
2. 沒有 mods 取代 hooks；FAQ 3 答「不會」並引 A。✔
3. 沒有沙盒或隔離的說法；sandboxing 只隔離 Bash，現在也寫了 mod 啟動的程式在外面。✔（第 13 處）
4. sec-default 載入條件照 A，正文、summary（第 3 處補上）、圖解 caption 一致；沒有「企業版才有」。✔
5. 守的範圍與不守的範圍；deny 規則管不到 `$.fs`／`$.process`。✔（第 14 處補 `$.process`）
6. v2.1.287 只歸因文件；`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` 沒出現。✔
7. Where mods run 每一列：終端機、Code 分頁（含 terminal-only 但書）、WSL（不跑）、VS Code、claude -p／Agent SDK、Remote Control、雲端。✔（第 12 處）
8. 內建 mods 名稱照 `/plugin`；`/diff` 停用後仍在；you-should-know 預設關閉且 if available for your org。✔（第 6、9 處）
9. 沒有 `token-chart`。✔
10. 三個範例的名稱與功能、`shared as they are, without support`；目錄以 git clone 看到。✔
11. 限制數字沒寫（6a 裁決）。✔
12. 只用 `Claude directory`（部落格）；沒有 Claude Marketplace。✔
13. 請 Claude 寫 mod 寫成文件說明的功能，沒有本站試用。✔
14. 沒有價格與用量比較；`$.model.complete` 那條以「用你的方案或 API key 呼叫模型」歸因文件。✔
15. 正文小寫 mods、首次帶中文說明；沒有「Code with mods」。✔
16. `verbatim_quote` 94/94 逐字。✔

## 界線檢查

- 購買建議、推薦式比價、價格：無（「價格」「免費」「訂閱」「購買」0 次）。
- 廠商宣稱：部落格的能力、動機、團隊例子都歸因 Anthropic；summary 2 與 description 補了歸因。
- 狀態：部落格寫 available today；正文沒有 beta、預覽、GA，也沒有推定台灣可用（Taiwan／台灣 0 次）。方案層級在 FAQ 5 寫「官方未說明」。
- 「本文」0 次、「這一篇」1 次（第 2 段）；只有一個 info callout；topics `["ai", "software", "ai-news"]`，沒有 finance。
- GitHub 設計討論沒有寫網址或編號（這一輪也沒寫那句，見下）。

## 留給站主的事

1. **字數上限**：改後 2,999／3,000。DELTA-4-11 第 3 節列為必寫、這一輪因上限沒有寫進正文的：`claude plugin test`（C：`with no session, sign-in, or network`）、`cc-plugin-agents-md`／`cc-plugin-telemetry`／`cc-plugin-plugin-authoring` 的列名（plugin-authoring 以 skill 名出現在第 4 節），以及部落格「發表前把設計放上 GitHub 徵求意見」那句（6a 允許、非必寫）。要補就需要放寬上限或另刪敘述；第二輪請不要為了補它們刪但書。
2. 四個文件頁是活頁面（O 的內建 mods 表與 Where mods run 表、A 的開關），發布當天重讀，特別看 Remote Control 那列與內建 mods 的列。
3. github.com 的 HTML 與 API 對本環境的出口代理回 403（代理訊息），`git clone` 走得通、目錄已確認；正文沒有 repo 連結，要不要放由協調者決定。
4. 正文把 `Google Cloud’s Agent Platform` 簡寫成 Google Cloud（照 DELTA 第 4 節第 4 條）；要不要寫全名由站主決定。
5. 圖解與 hero 沒有動；圖上四格與 caption 照研究紀錄 `diagram`。

## 結論

`needs_second_round`：事實與範圍改了 13 處（超過十處），第 4 節第 3–4 段與第 5 節三段是重寫的，而且 DELTA-4-11 第 6 節本來就要求第二輪。第二輪請逐句回原文，特別看這一輪新寫的句子：第 4 節第 4 段（Where mods run）、第 3 節第 3 段（內建 mods）、第 2 節第 2 段的 `/diff`、第 5 節第 2–4 段的補寫，以及 summary 第 2、3 點。
