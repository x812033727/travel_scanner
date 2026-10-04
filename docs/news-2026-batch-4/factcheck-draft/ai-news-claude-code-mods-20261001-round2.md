# 第二輪獨立查核：ai-news-claude-code-mods-20261001

## 第二輪

- 查核者：獨立查核代理（第二輪，opus；沒有參與撰稿與第一輪），2026-10-04（台北）
- 規格：`agents/ai/SECOND-ROUND.md`、`agents/ai/FACTCHECK.md`（路徑改 Linux；沒有 corrections-ai.md）、`agents/DELTA-4-11.md` 第 4 節與第 6a 節
- 改動的檔案：內容包（zh-TW 正文 7 處、summary 1 處、FAQ 3 題）、研究紀錄（只加 `factcheck.second_round`；`title`、`diagram` 沒動）、本報告（加這一節）
- 暫存：`/root/news411/agents/fc2/`（`raw/`、`fetch-log.tsv`、`check_quotes.py`／`check_quotes.log`、`norm-*.A.txt`、`edit_pack.py`、`edit_research.py`、`pack.before.json`、`research.before.json`、`pack.diff`、`check.log`、`pg/`）

### 重抓（2026-10-03 UTC 19:02，台北 10-04 03:02）

UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`（只有網站與站方信箱，沒有任何人的姓名、email 或個資；標頭、查詢字串也沒有），`curl -sSL --compressed --max-time 60`，間隔 1.3 秒。

| 網址 | HTTP | 傳輸 bytes | 落地 bytes | md5 與第一輪 | 正文？ |
| --- | --- | --- | --- | --- | --- |
| claude.com/blog/claude-code-mods | 200，0 次轉址 | 99,345 | 532,059 | 相同 | 是 |
| …/plugins/mods/overview | 200，0 | 90,469 | 526,328 | 相同 | 是 |
| …/plugins/mods/create | 200，0 | 97,080 | 656,741 | 相同 | 是 |
| …/plugins/mods/admin | 200，0 | 98,950 | 646,270 | 相同 | 是 |
| 三頁 `.md` 版 | 200，0 | 8,160／8,709／10,645 | 23,225／25,270／33,874 | — | 是（讀表用） |

`git clone --depth 1 --filter=blob:none --no-checkout` `anthropics/claude-code-playground`：HEAD `569c528`（2026-10-01T09:11:57-07:00），`claude-code/mods/` 有 `token-weather`、`blast-radius`、`replay-theater`、`.claude-plugin`。

`verbatim_quote` 程式比對（`check_quotes.log`）：刪註解與 script／style／noscript／svg／template 後做 A（行內標籤→無、其他→空格）、B、C、RAW 四種正規化，**94/94 為連續子字串**，`url` 全在 `sources[]`；沒有任何一條含 `...`、`…` 或 ` | `，不必逐片段拆看。

### 覆核第一輪的 19 處與新寫的句子

逐子句回原文，約 60 條。第一輪的 19 處**全部站得住**；下列幾處原文對照特別看過：

- Where mods run 每一列對 overview 表：WSL `No, because plugins aren't available in WSL sessions`／`No`（連事件函式都不跑）✔；Remote Control `Yes, in the session on your machine`／`In the terminal on your machine` ✔；VS Code 聊天面板、`claude -p` 與 Agent SDK `Yes`／`No` ✔；雲端 `Yes, for a plugin that reaches the cloud session`／`No` ✔；Code 分頁 `except elements the elements table marks terminal-only` ✔。
- `sec-default`：載入條件 `The machine has managed settings`／`signed in to Claude Code with a Team or Enterprise plan`，API key、Bedrock、`Google Cloud's Agent Platform`、Foundry `gets the guard only on a machine that has managed settings` ✔；`Both apply to Claude's tool calls. Neither applies to a mod's own $.fs and $.process calls` ✔（正文「核准 deny 規則拒絕的工具呼叫」「deny 規則也管不到 mod 自己的 $.fs 與 $.process 呼叫」）；`Everything else is allowed` ✔。
- 內建 mods 表六列（agents-md、diff、plugin-authoring、sec-default、telemetry、you-should-know）；you-should-know `Disabled by default. Listed in /plugin -> Installed -> Show disabled if available for your org` ✔；`/diff stays, and Claude Code's built-in version of the command answers it` ✔。
- `disableSideloadFlags` `keeps mods Claude writes during a session from loading` ✔；managed `disableAllHooks` `stops the mods in every installed plugin, yours included, and turns off every hook in settings files` ✔；個人 `What your organization manages keeps running` ✔；`a process that a mod starts runs outside it` ✔；`including an API key you keep in either` ✔。
- 第一輪為字數刪的五句（第 1 段讀者定位與重複版本門檻、第 2 段「也不是訂閱或購買建議」、第 4 節「Claude 可以寫 TypeScript 並熱重載」、「用詞先分開：」）：都是敘述或重複，**沒有帶走但書、限定詞或歸因**；請 Claude 寫 mod 的那段仍以「文件說」歸因（DELTA 第 13 條）。

### 這一輪又改的 8 處（原文 → 改成，依據）

1. **第三節內建 mods 指錯節**：「與見下一節的 cc-plugin-sec-default」→「與最後一節的 cc-plugin-sec-default」。下一節是「怎麼開始用」，sec-default 在第五節「安全與企業管控」。
2. **第一節 hook 兩義的位置**：定義段排在 register(on) 段之後，而 register(on) 段已經寫了「用 on 註冊事件函式」。把定義段移到 register(on) 段之前，「把兩種都叫 hooks。設定檔裡的……」→「把兩種都叫 hooks：設定檔裡的……」（O Note：`Claude Code calls both kinds hooks`）。全文之後只用「設定檔 Hook」與「（mod 的）事件函式」，單獨的 Hook／hook 只出現在檔名、`disableAllHooks` 與這一句。
3. **第四節 Where mods run 少主詞**：「文件寫，終端機與 Desktop app 的 Code 分頁會畫（」→「文件寫，mod 的介面畫在終端機與 Desktop app 的 Code 分頁（」（O：`only the terminal and the Desktop app show a mod's panes, bands, and replaced rows`）。
4. **第五節 --safe-mode 的副作用**：「以 --safe-mode 停掉一個 session 的已安裝 mods，」→「……mods（其他自訂也停），」（O：`start Claude Code with --safe-mode, which also disables your other customizations`）。同段 disableAllHooks 已寫副作用，這條漏了；FAQ 4 同步。
5. **summary 第 5 點**：「會隨版本更新」→「可能隨版本變動」（C：`can change between releases`），與第一輪改過的 callout 同一個強度。
6. **FAQ 5 的否定句**：「沒有逐一寫各個方案能不能用，官方未說明。」→「這裡引用的部落格與三頁文件，到查核日 2026 年 10 月 4 日都沒有逐一寫各個方案能不能用。」（限縮到這幾頁、查核日；研究紀錄 `not_said` 第 1 條）。
7. **FAQ ⊆ 正文**：FAQ 1 刪「太舊就更新」與「部落格沒有寫版本門檻」（後者見第 8 處）；FAQ 4 刪「所有 session」（正文沒寫），補「組織管理的照常」（正文有）。
8. **騰字**（補第 3、4 處要 15 字）：刪第四節第一段「；部落格沒有寫版本門檻」（版本門檻仍以「文件寫」歸因，DELTA 第 4 節第 6 條要的是歸因到文件）；「只在有 managed settings 的電腦上才有」→「電腦才有」；「後兩者不會停掉內建 mods」→「後兩者不停內建 mods」。**沒有刪任何但書、限定詞或歸因。** 段落 2,999 → 3,000。

### summary、FAQ、圖解、界線

- summary 五點每個子句都在正文（「Anthropic 說 mods 能……畫窗格與按鈕、加指令」對第二節第一段；第 3 點的載入條件與「工具呼叫」對第五節第二段）；數字（2026、10、1、2.1.287、4）都在正文，自檢通過。
- FAQ 六題答案的事實都在正文（FAQ 5 的否定句是範圍限縮後的「這幾頁沒有寫」）；FAQ 沒有網址。
- 圖解 caption 與研究紀錄 `diagram.caption` 相同；四格「事件／工具呼叫、提示、畫面」「函式／觀察、改寫或接手」「介面／窗格、按鈕、指令」「管控／先載 sec-default」與 hero_label「mods：改行為也改介面」的字都對得上正文或 caption（sec-default 先載入的條件寫在 caption）。
- 界線：topics `["ai", "software", "ai-news"]`，沒有 `finance`；callout 一個（info）；價格、免費、訂閱、購買、升級、值得、台灣 0 次；廠商說法都有「Anthropic 說／部落格說／文件寫」；「本文」0 次、「這一篇」1 次；正文沒有網址（6 個網址都在 sources 與兩個結尾連結）；`checked_on` 四處 2026-10-04 沒動；兩個結尾連結沒動。
- 既有教學：`claude-code-plugins-guide`（Plugins 安裝與管理；描述把 Hooks 列為 plugin 可打包的內容）與 `claude-code-hooks-getting-started`（建立第一個 Hook；PostToolUse）寫的都是設定檔 Hook 與一般 plugin。本篇寫「設定檔 Hook 照舊執行，沒有任何一項被淘汰」，與兩篇不矛盾；用詞「Hook」對應「設定檔 Hook」。

### 協調者點名的疑點

| 疑點 | 結果 |
| --- | --- |
| hook 兩義 | 第一節講清楚，並移到第一次用「事件函式」之前（第 2 處） |
| Where mods run 各列 | 全對 overview 表；補主詞（第 3 處） |
| sec-default 載入條件、deny 規則只管 Claude 的工具呼叫 | 對 admin 頁 ✔，沒改 |
| 內建 mods 六列、you-should-know 預設關閉與 if available for your org | 表是六列；正文以「例如」列三個，兩個條件都在 ✔；修了指錯節（第 1 處） |
| Google Cloud 全名 | 沒改：`Google Cloud's Agent Platform` 要多 17 字，正文已 3,000 |
| `claude plugin test` | 沒補：約 35 字，找不到可刪的重複敘述而不動但書；留給站主（DELTA 第 7 節的教學課會教） |
| GitHub 徵求設計意見 | 照指示不補 |
| repo 連結 | 正文沒有網址 ✔ |

### 留給站主的事

1. `claude plugin test`（`verified_facts` 第 72 條）與 `Google Cloud's Agent Platform` 全名：兩者都只差字數；要補就得放寬 3,000 字上限，或接受刪掉第二節「下表四者中只有 mod 能畫介面」這類半重複的句子（這一輪判斷那句仍有資訊：表格沒有「能不能畫介面」那一欄）。
2. 內建 mods 只列了三個名稱，其他三個（agents-md、telemetry、plugin-authoring）沒列；不影響正確性。
3. 四個文件頁是活頁面，發布當天重讀，特別看 Where mods run 表與內建 mods 表。

### 自檢

```
exit=0
OK ai-news-claude-code-mods-20261001 zh-TW paragraphs 3000
```

### 結論

`ok`：第一輪的 19 處都對；這一輪 8 處都是措辭、範圍、指錯節與 FAQ ⊆ 正文，沒有動到骨幹論述，沒有刪但書。
