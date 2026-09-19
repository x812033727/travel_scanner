# 獨立查核：ai-workflow-coding-agents-division

查核代理：未參與撰稿。查核日 **2026-09-19**。文章的 `checked_on` 是 **2026-09-18**，
在內容包八條 source、研究紀錄、表格 caption 與圖解 caption 上一致，
今天重讀八個頁面後**沒有任何被引用的數字或句子改變**，依規格**不改**；
本輪新引的句子全部來自同樣那八頁，重讀日期記在研究紀錄 `factcheck.checked_on`。

查核方式：`sources[]` 八條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body
（learn.chatgpt.com 兩頁另抓官方提供的 `.md` 版交叉比對，去掉 HTML 去標籤造成的空白假陽性）；
逐句把 title、description、summary 四句、正文十二段、表格 20 格與 caption、callout、
圖解 caption 與四組節點、FAQ 六題答句、兩個 `code` 區塊的每一個 CLI 旗標對回原文；
研究紀錄原有 41 條 `verbatim_quote` 用程式做連續字串比對。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

檢查的主張：**119 條**（正文 52 句／子句、summary 4 句、FAQ 6 題答句、callout 6 項、
表格 20 格、兩個 caption、圖解 4 組節點、`hero_label`、title、description、
`code` 區塊裡 23 個識別字），外加研究紀錄 41 條引文。
**改了 12 條（29 個編輯點）**，研究紀錄新增 15 條 `verbatim_quote`，另有 4 件留給站主。

## 重抓結果：八條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `code.claude.com/docs/en/cli-reference` | 200 | 484,883 | **是**。`<title>` 為「CLI reference - Claude Code Docs」；CLI commands 表與 CLI flags 表完整渲染在 HTML 裡（不是 JS 空殼），`--output-format`／`--json-schema`／`--permission-mode`／`--permission-prompt-tool`／`--permission-prompts` 全部讀得到 |
| `learn.chatgpt.com/docs/non-interactive-mode` | 200 | 411,611 | **是**。`og:site_name` 為 `ChatGPT Learn`、canonical 指回自己；正文十節（Basic usage、Permissions and safety、Make output machine-readable、Create structured outputs with a schema、Git repository required…）齊全 |
| `learn.chatgpt.com/docs/developer-commands` | 200 | 1,087,615 | **是**。`codex exec` 的旗標表是伺服器端渲染的 `<table>`，20 個旗標逐列讀得到；Global flags 表也在 |
| `raw.githubusercontent.com/.../README.md` | 200 | 13,489 | **是**。原始 Markdown，`Non-interactive mode for scripts` 一節與兩個 `--output-format` 範例都在 |
| `raw.githubusercontent.com/.../docs/cli/headless.md` | 200 | 1,578 | **是**。整份就是這 1.5 KB：Output formats、JSON schema 三欄位、Streaming JSON 事件型別、Exit codes 四個 |
| `raw.githubusercontent.com/.../docs/cli/cli-reference.md` | 200 | 16,563 | **是**。CLI Options 表 25 列齊全 |
| `code.claude.com/docs/en/permission-modes` | 200 | 678,995 | **是**。Available modes 表、plan mode 一節、dontAsk 一節、Common setups 表都讀得到 |
| `raw.githubusercontent.com/.../docs/cli/plan-mode.md` | 200 | 19,587 | **是**。Tool Restrictions 一節（含 Planning (Write) 白名單）與 How to use Plan Mode 都在 |

**協調者交辦的轉址確認**：種子 `https://developers.openai.com/codex/cli/` 今天
`curl -sL` 的落地頁是 `https://learn.chatgpt.com/docs/codex/cli`，HTTP 200。
落地站台的 `og:site_name` 是 `ChatGPT Learn`，導覽列有 `API Dashboard`、`OpenAI Crawlers`、
`Cookbook`（「Notebook examples for building with OpenAI models」），
**確認仍是 OpenAI 官方文件站，內容確實是 Codex CLI 參考**。
內容包與研究紀錄的 sources 都已經是落地頁（撰稿者本來就換掉了），兩邊逐字一致，不需要再改。

## 程式範例重驗

| # | label | 語言 | 行數 | 編譯 | 比對過的旗標／識別字 |
| --- | --- | --- | --- | --- | --- |
| 1 | `workflow.sh` | bash | 61 → **67** | `bash -n` **通過**；內嵌 heredoc 的 Python 抽出來 `py_compile` **通過** | `claude -p`、`--output-format text`、`--permission-mode plan`（[cli-reference](https://code.claude.com/docs/en/cli-reference)、[permission-modes](https://code.claude.com/docs/en/permission-modes)）；`codex exec`、`--sandbox workspace-write`、`--output-last-message`、~~`--skip-git-repo-check`~~（[developer-commands](https://learn.chatgpt.com/docs/developer-commands)、[non-interactive-mode](https://learn.chatgpt.com/docs/non-interactive-mode)）；`gemini -p`、`--approval-mode=plan`、`--output-format json`（[cli-reference.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/cli-reference.md)、[plan-mode.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/plan-mode.md)、[headless.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/headless.md)）；`git add -N`／`git diff`（[non-interactive-mode](https://learn.chatgpt.com/docs/non-interactive-mode) 的 CI 範例） |
| 2 | `review.json` | json | 18 | `json.loads` **通過** | 純資料，欄位全部是本站自訂，沒有可對的官方簽名 |

額外做了一次**離線行為驗證**：在暫存目錄的拋棄式 Git 儲存庫裡放三支假的 `claude`／`codex`／`gemini`
（各自只回一行固定輸出），完整跑過 `workflow.sh`。結果：`plan.md`、`change.patch`、
`raw-response.json`、`review.json` 四個交接檔都產生，patch 同時含**新建檔案**與既有檔案的修改，
交接目錄本身沒有被寫進 patch，`verdict` 為 `approve` 時退出碼 0。
**沒有執行真正的 claude／codex／gemini**（依指派）。

檢查過而且通過的安全條件：`set -euo pipefail` 在第 6 行；沒有刪檔命令、沒有 `eval`、
沒有字面金鑰也沒有 `<YOUR_KEY>`；三支 CLI 呼叫都包 `timeout`；金鑰完全不出現（三支都假設已登入）。

## 改掉的 12 條

### 最重的五處

**1. callout 把三支 CLI 的核准機制合寫成「會卡住」，而 Claude Code 的文件寫的相反。**
原 callout 標題是「沒設核准旗標，非互動呼叫可能卡住」，內文結論是
「輕則卡到 timeout 逾時，重則因為找不到人核准直接失敗」。
今天的 Claude Code 文件明寫**不會卡住**：

- `--permission-prompts`：`Pass none when nobody can answer, and Claude Code denies them instead.`
- dontAsk：`anything that would prompt is denied`、
  `Use this mode for CI pipelines or restricted environments where you pre-define what Claude
  may do; the session never waits for input.`
- `-p` 搭 `--dangerously-skip-permissions`：`In this -p run, the few calls that would still
  prompt are denied instead`
- 自動模式退場：`a non-interactive -p run without a --permission-prompt-tool has no prompt to
  fall back to. When repeated blocks reach a threshold, the action doesn't run and Claude keeps
  working.` … `Claude Code doesn't stop the run in either case.`

callout 已整段重寫成**每一支各自引用自己的文件**：Claude Code 引 `--permission-prompt-tool`
（`Specify an MCP tool to handle permission prompts in non-interactive mode.`）與上面兩句；
Codex 引全域旗標 `--ask-for-approval, -a on-request | never Control when Codex pauses for
human approval before running a command.`，加上 `codex exec` 自己的定位
`for scripted or CI-style runs that should finish without human interaction.`；
Gemini CLI 引 Plan Mode 的 `Gemini CLI will stop and wait for your confirmation`。
標題改成「核准提示沒人回答時，三家文件寫的不一樣」，結尾補「本站沒有實測」。
FAQ 第 4 題同一句判斷同步改寫。

**2. 程式範例的 `--skip-git-repo-check` 是錯的，而且少了 `git add -N`。**
原腳本第 21 行加了 `--skip-git-repo-check`，第 24 行卻用 `git diff` 取變更——
`git diff` 本來就需要 Git 儲存庫，等於**關掉一個安全檢查卻沒有任何用處**。
文件寫這個檢查存在的理由是
`Codex requires commands to run inside a Git repository to prevent destructive changes.`
（覆寫它的條件是 `if you're sure the environment is safe`）。已移除該旗標，
改在註解寫明本例需要 Git 儲存庫。
另外原本只有 `git diff`，**Codex 新建的檔案不會出現在 patch 裡**；
Codex 自己的 CI 範例做法是 `git add -N .` 之後 `git diff --binary HEAD > codex.patch`。
已補上 `git add -N`，並用 `:(exclude)$out` 讓交接目錄不進 patch（實測確認）。
正文與表格「跑完用 git diff 存成 patch」同步改成「先 git add -N 再 git diff」。

**3.「Gemini CLI 的 --output-format json 只保證外層有 response、stats、error 三個欄位」
兩個地方都不對。** `error` 在文件上是**選用**的：
`error: (object, optional) Error details if the request failed.`；
而「不驗證 response 內容」是從「沒查到對應旗標」推論的。
summary 第 3 句、表格 Gemini 列、正文表格後那段、FAQ 第 2 題**四處**全部改寫成
「無頭模式文件列出 response、stats 與**選用的** error 三個外層欄位；
**本文查證當天沒有在那幾頁看到對應的 schema 驗證旗標**」。

**4.「Gemini CLI 的文件列出完整的結束代碼對照表」「Claude Code 與 Codex 沒有列出同樣完整的對照表」
兩邊都要收範圍。** `headless.md` 寫的是
`The CLI returns standard exit codes to indicate the result of the headless execution`，
並列出四個（0／1／42／53），**沒有自稱完整**。Claude Code 與 Codex 那半句原本是對「文件」的全稱否定。
summary 第 4 句、正文末段、FAQ 第 5 題**三處**改成
「Gemini CLI 的無頭模式文件列出四個結束代碼」與
「**本文這次讀到的** Claude Code 與 Codex **頁面**沒有列出這樣的數字對照」。
（今天實查：Codex 兩頁只有 `codex login status exits with 0 when credentials are present`
與 `--oss` 的 `exits with an error`；Claude Code 兩頁只有 `--max-turns`
`Exits with an error when the limit is reached.` 與 `--json-schema` 的
`exits with an error on an invalid schema`——都是個別旗標，不是對照表。）

**5. 用 Gemini CLI 的 Plan Mode 做「審查」沒有標成延伸用法，也漏了它能寫檔。**
`plan-mode.md` 對 Plan Mode 的定位是
`Plan Mode is a read-only environment for architecting robust solutions before implementation.`
——**是給實作前設計解法用的**，不是審查。而且它並非完全不寫檔：
`write_file` 與 `replace` `only allowed for .md files in the
~/.gemini/tmp/<project>/<session-id>/plans/ directory or your` 自訂計畫目錄，
流程上 `Gemini CLI creates a detailed implementation plan as a Markdown file in your plans
directory.`。正文已補一句明寫「把 Plan Mode 拿來審查是本文的延伸用法：官方文件說它是給實作前
設計解法用的唯讀環境，只準在計畫目錄裡寫 .md 檔」，程式註解同步標明。

### 其餘七條

**6. Claude Code 的 `--json-schema` 被寫成吃檔案，而且「不合法」指錯對象。**
原文（表格與正文）：「都會把一份 JSON Schema 檔交給 CLI 驗證最終回應」。
官方範例是**行內字串**：`claude -p --json-schema '{"type":"object","properties":{…`，
而 Codex 的 `--output-schema` 型別才是 `path`。另外文件寫的是
`Claude Code exits with an error on an invalid schema`——**schema 本身**不合法才以錯誤結束，
不是輸出不合法。兩處都已分開改寫，並在表格補上同一句後半段的限定：
`accepts the format keyword as an annotation without client-side validation`
（format 關鍵字只當註解、不做用戶端驗證）。

**7. Codex 的 `--output-last-message` 不是「只存」。**
文件寫 `This writes the final message to the file and still prints it to stdout`。
表格「另有 --output-last-message 只存最後一則訊息」已改成
「另外把最後一則訊息寫成檔案，stdout 仍會印出」。同一格的 `--output-schema` 說明也改用文件用語
`Codex validates tool output against it`（驗證工具輸出），不再寫成「驗證最終回應」。

**8. summary 第 1 句與正文自相矛盾。**
原句「決定核准與輸出格式的旗標名稱**三家都不同**」，但同一篇正文寫著
「Claude Code 與 Gemini CLI **同名都叫 --output-format**」。
已改成「核准旗標三家各叫各的名字，輸出格式旗標只有 Claude Code 與 Gemini CLI 同名」，
導言第一段同一個說法同步改。

**9. Gemini CLI 位置引數掉了限定詞「在 TTY 裡」。**
原文「官方文件寫這個位置引數預設會進互動模式」。文件是
`Positional prompt. Defaults to interactive mode in a TTY.`，
而且 `headless.md` 另寫 `Headless mode is triggered when the CLI is run in a non-TTY
environment or when providing a query with the -p (or --prompt) flag.`——
在非 TTY 環境（例如排程）裡，位置引數本來就是無頭模式。已補回「在 TTY 裡」。

**10. 三處「三家都沒有共通規格／都沒有定義這三個檔名」是全稱否定。**
導言第一段、交接檔那一節第一段、FAQ 第 3 題，都改成
「**本文查證的三家文件**都沒有定義工具之間的交接格式」。
`description` 的「不是官方提供的整合功能」同樣改成「本文查證的文件沒有跨工具的整合功能」。

**11. `description` 末句語意不通。**
原句「不需要另外寫 Python 以外的程式」——但讀者要寫的就是 bash。
已改成「腳本只用 bash 與 Python 內建的 json 模組」（改後 196 units，仍在 120–200）。

**12. 退出碼那段在正文出現三次。**
程式後那一段、正文末段、FAQ 第 5 題原本幾乎逐句重複，而且退出碼細節是
《Claude Code｜非互動執行與 JSON 輸出》講過的事。程式後那一段改寫成這支腳本自己的行為
（`set -euo pipefail` 任何一支回非零就停），數字與意義只留在正文末段一處。

## 查過而且正確的部分（沒有動）

- **逐字核對過的 CLI 旗標，全部與今天的官方頁面相符，沒有一個是杜撰的**：
  `claude` 的 `-p`／`--print`、`--output-format`（`text , json , stream-json`）、
  `--input-format`、`--json-schema`、`--max-turns`、`--permission-mode`（含 `plan`）、
  `--permission-prompt-tool`、`--permission-prompts`；
  `codex exec` 的 `--json`／`--experimental-json`、`--output-schema`、
  `--output-last-message`／`-o`、`--sandbox`／`-s`
  （`read-only | workspace-write | danger-full-access`）、`--skip-git-repo-check`、
  全域 `--ask-for-approval`／`-a`、`--cd`／`-C`；
  `gemini` 的 `-p`／`--prompt`、`--output-format`／`-o`（`text, json, stream-json`）、
  `--approval-mode`（`default, auto_edit, yolo, plan`）、`--yolo`（**Deprecated**）。
- **`-o` 的一字兩義成立**：Codex 的 `-o` 是 `--output-last-message`，
  Gemini CLI 的 `-o` 是 `--output-format`，兩張表都確認過。
- **`codex exec` 的 Stable 標示成立**：`codex exec Stable Run Codex non-interactively. Alias: codex e .`
- **Codex 的 stdout／stderr 分工成立**：`While codex exec runs, Codex streams progress to stderr
  and prints only the final agent message to stdout.`（HTML 去標籤版在 `stdout` 後多一個空格，
  是標籤造成的假陽性；官方 `.md` 版逐字相符，研究紀錄第 10 條未動。）
- **Claude Code 的 plan 模式在 `-p` 下成立**，而且今天找到更硬的一句已補進研究紀錄：
  `Plan mode keeps its blocks wherever Claude Code runs without an interactive terminal,
  including non-interactive runs with -p`。
- **Gemini CLI 四個結束代碼 0／1／42／53 與各自意義**與今天的 `headless.md` 逐字相符。
- **三種非互動模式的官方稱呼**（print mode／non-interactive mode／headless mode）
  與各自說明句都找得到，而且正文每一句都有歸屬（「Anthropic 的 Claude Code 文件」
  「OpenAI 的 Codex 文件」「Google 的 Gemini CLI 文件」）。
- **研究紀錄原有 41 條 `verbatim_quote` 全部通過連續字串比對**（HTML 去標籤、
  Markdown 去反引號與星號、空白正規化後）；`url` 也全部在 `sources[]` 裡。
- **界線檢查全部通過**：沒有訂閱、購買或投資建議；沒有推薦式比價，也沒有速度／品質排名；
  沒有「台灣可用」；沒有把預告寫成已推出；沒有任何模型 id（`models-seen.json` **不需要新增**）；
  只有一個 callout 且不是免責聲明；正文中間沒有 `link` 區塊。
- **必連四篇沒有被重講**：《Claude Code｜非互動執行與 JSON 輸出》《codex exec 與腳本整合》
  《CLI 寫程式：理解、規劃、修改與測試》《Claude Code｜Agent Teams 協作》都只在同一段裡各一句點名；
  `claude -p`／`--output-format json`／`--json-schema`／退出碼在本篇只出現在「三支比較」的脈絡，
  沒有重寫那篇的教學步驟，也沒有與它的「成功退出碼應為零，失敗為非零」矛盾。
  結尾第二個 link 的 text「Claude Code｜非互動執行與 JSON 輸出」與該內容包的 zh-TW `title` 逐字相同。
- **正文以文字點名的另兩篇標題逐字正確**：
  《模型之間交接資料：JSON Schema 與結構化輸出》（`ai-workflow-structured-handoff`）、
  《失敗案例與防護：迴圈、費用爆炸與代理間注入》（`ai-workflow-failures-and-guardrails`）。
- **`checked_on` 2026-09-18** 在八條 source、研究紀錄、表格 caption、圖解 caption 上一致，未更動。

## 留給站主的事

1. **Plan Mode 用在審查步驟仍有殘餘風險。** `plan-mode.md` 寫 Plan Mode 允許 `ask_user`、
   `web_fetch (requires explicit confirmation)`，而且
   `Gemini CLI will stop and wait for your confirmation` 之後才寫正式計畫。
   本文已標明是延伸用法並包了 `timeout`，但若要把這支腳本放進正式排程，
   建議先實測一次 `gemini --approval-mode=plan` 在無頭環境下的行為，或改用預設核准模式。
2. **`git add -N` 會動到使用者的索引（intent-to-add）。** 本文用 `:(exclude)` 把交接目錄排除，
   但若不希望腳本碰索引，可以改成在拋棄式 worktree 裡跑。這是取捨，不是錯誤。
3. **內文長度剛好卡在 life 類 6,000 字元的建議上限**（目前 6,000；段落字數 2,944／上限 3,000）。
   本輪補限定詞的空間是從 FAQ 與 summary 的重複敘述換來的；之後要再補，請同樣從重複處精簡，
   **不要刪掉查證過的限定條件**。
4. **兩個結尾純 link 由協調者 `relink`**，自檢剩下的 `raw_internal_url` WARN 就是它造成的；
   第一個指向尚未發布的系列目錄 `ai-workflow-tutorials`。依規格本代理沒有動那兩個區塊。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-coding-agents-division paragraphs 2944 code_blocks 2 sources 8
```

沒有 FAIL；只剩協調者會處理的 `raw_internal_url` WARN。
段落字數 **2,944**（1,800–3,000），title 28 units，description 196 units，
`code` 區塊兩個（bash 67 行、json 18 行，都 ≤ 80）。

## 結論

`needs_second_round`。改了 12 條、29 個編輯點，其中一處動到骨幹論述
（callout 的核心判斷「非互動呼叫會卡住」被官方文件推翻，整段重寫），
另一處動到程式範例的行為（移除 `--skip-git-repo-check`、補 `git add -N` 與 `:(exclude)`）。
文章現在可刊，但依規格，改到骨幹論述與程式範例就該再走一輪：
第二輪只需要逐句回來源查**本輪新寫進去的每一句**——callout 全文、
正文「實作」那一段的 Plan Mode 三句、表格三格的「結構化輸出驗證」欄、
summary 第 1、3、4 句、FAQ 第 2、4、5 題，以及研究紀錄新增的 15 條 `verbatim_quote`——
外加在一個真的 Git 儲存庫裡重跑一次 `workflow.sh` 的 `git add -N` 行為。

## 第二輪

第二輪查核代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-19**（與第一輪同日，不同代理）。
範圍是第一輪改動過的每一段與新寫進去的每一句，不是整篇重做。
文章的 `checked_on` 仍是 **2026-09-18**：八個頁面今天自己重抓一次，
被引用的句子與數字**全部沒有改變**，bytes 也與第一輪記的完全相同，依規格**不改**。

查核方式：`sources[]` 八條全部自己重抓（`curl -sL -A "Mokaair-editorial"`；
四個 HTML 文件頁另抓官方提供的 `.md` 版交叉比對，去掉去標籤造成的空白假陽性）；
研究紀錄的 `verbatim_quote` 用程式做連續字串比對（改動前 55 條 55/55 通過、改動後 57 條 57/57 通過），
並逐條檢查每句引文**是不是真的撐得起它掛的那條 `fact`**——本輪兩處問題都是這樣找出來的。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

檢查的主張：**139 條**（callout 9 項、導言兩段 7 句、summary 4 句共 10 項、
正文八段 33 句／子句、表格 20 格與 caption、圖解 caption 與四組節點、`hero_label`、
FAQ 六題答句 14 項、`code` 區塊 23 個識別字、title、六個被點名的系列文章標題與兩個結尾 link text），
外加研究紀錄 57 條引文。**改了 4 處內容包、5 處研究紀錄**，**沒有改程式碼**。

### 重抓結果：八條 sources 今天仍然讀得到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `code.claude.com/docs/en/cli-reference` | 200 | 484,883 | **是**。CLI flags 表伺服器端渲染；另抓 `.md` 版 118,548 bytes 交叉比對 |
| `learn.chatgpt.com/docs/non-interactive-mode` | 200 | 411,611 | **是**。另抓 `.md` 版 14,843 bytes，Git repository required 與 CI 範例齊全 |
| `learn.chatgpt.com/docs/developer-commands` | 200 | 1,087,615 | **是**。旗標表在 HTML 裡（`.md` 版把表換成 `<ConfigTable>` 佔位，所以旗標一律以 HTML 為準） |
| `raw.githubusercontent.com/.../README.md` | 200 | 13,489 | **是**。原始 Markdown |
| `raw.githubusercontent.com/.../docs/cli/headless.md` | 200 | 1,578 | **是**。整份 1.5 KB，Schema 三欄位與四個結束代碼都在 |
| `raw.githubusercontent.com/.../docs/cli/cli-reference.md` | 200 | 16,563 | **是**。CLI Options 表齊全 |
| `code.claude.com/docs/en/permission-modes` | 200 | 678,995 | **是**。dontAsk 與 plan mode 兩節都在；另抓 `.md` 版 82,759 bytes |
| `raw.githubusercontent.com/.../docs/cli/plan-mode.md` | 200 | 19,587 | **是**。Tool Restrictions 與 How to use Plan Mode 都在 |

八條 bytes 與第一輪記的一字不差，可以確認頁面這一天之內沒有改版。

### 程式範例第二次重驗

| # | label | 語言 | 行數 | 重驗 |
| --- | --- | --- | --- | --- |
| 1 | `workflow.sh` | bash | 67 | `bash -n` **通過**；heredoc 裡 16 行 Python 抽出來 `python -m py_compile` **通過** |
| 2 | `review.json` | json | 18 | `json.loads` **通過** |

`code_samples` 的 `lines`（67／18）與內容包相符，本輪沒有改 code，所以沒有同步修改。

**拋棄式 Git 儲存庫實跑**（暫存目錄裡新建，三支假的 CLI 各寫成獨立小腳本掛在 `PATH` 前面；
**沒有執行真正的 `claude`／`codex`／`gemini`，也沒有刪任何檔**），跑了六種情境：

1. **四個交接檔都產生**：`plan.md`、`change.patch`、`raw-response.json`、`review.json`
   （另有 `-o` 指定的 `codex-final.txt`）。三支假 CLI 收到的旗標逐字是
   `-p … --output-format text --permission-mode plan`、
   `exec --sandbox workspace-write --output-last-message .handoff/codex-final.txt`、
   `-p … --approval-mode=plan --output-format json`。
2. **Codex 新建的檔案進 patch**：假 Codex 新建的 `app/new_module.py` 以
   `new file mode 100644` 出現在 `change.patch` 裡，既有檔案的修改也在。
3. **交接目錄不進 patch**：假 Codex 故意往 `.handoff/` 寫了一個檔，
   patch 裡沒有它，`git status` 仍是 `?? .handoff/`——`:(exclude)$out` 有效。
4. **對照組**：同一個工作樹 `git reset` 之後只跑 `git diff`，`new_module` **0 次命中**；
   再 `git add -N` 後 **2 次命中**。正文與程式註解說的「`git add -N` 才讓 Codex 新建的檔案
   出現在 `git diff`」**成立**（見「留給站主的事」第 3 點：這半句是實測，不是文件原句）。
5. **退出碼與正文一致**：`verdict` 為 `approve` 時 0；`changes_requested` 時 1、訊息走 stderr；
   審查回傳的 `response` 不是 JSON 時落到 fallback（`changes_requested`／
   `reviewer did not return valid JSON`）後一樣 1；三支 CLI 分別回 3／7／42 時，
   `set -euo pipefail` 讓腳本停在那一步並原樣傳回 3／7／42——
   與正文「任何一支回非零，管線就停在那一步，不會拿半成品往下走」相符。
6. **不在 Git 儲存庫裡**跑會停在 `git add -N`（128），與腳本註解「本例需要 Git 儲存庫」一致。

每個旗標今天再逐字對過文件：`claude` 的 `-p`／`--print`、`--output-format`、`--json-schema`、
`--permission-mode plan`、`--permission-prompt-tool`、`--permission-prompts`；
`codex exec` 與 `--sandbox workspace-write`、`--output-last-message`／`-o`、`--output-schema`、
`--json`／`--experimental-json`、全域 `--ask-for-approval`；
`gemini` 的 `-p`／`--prompt`、`--output-format json`、`--approval-mode=plan`。全部相符。
`git add -N .` 與 `git diff --binary HEAD > codex.patch` 兩行也逐字對回
[non-interactive-mode](https://learn.chatgpt.com/docs/non-interactive-mode) 的 CI 範例。
另確認 Codex 兩頁沒有 `--output-format`、Claude Code 與 Gemini CLI 兩邊都沒有對方的核准旗標名，
正文「輸出格式旗標只有 Claude Code 與 Gemini CLI 同名」成立。

### 改掉的 9 處

**內容包 4 處**

**1.（最重）callout 漏掉 `--permission-prompts` 的版本下限。**
第一輪把 callout 整段重寫成三支各引自己的文件，引 `--permission-prompts` 時漏了同一列結尾那句
`Requires Claude Code v2.1.259 or later`——這是規格點名要盯的「限定詞被刪」那一類。
（今天查過：`cli-reference` 整頁這個字串只出現一次，就在這一列；本文引用的其他旗標都沒有版本下限。）
已改成「`--permission-prompts`（文件註明要 v2.1.259 以上）傳 none 表示沒人能回答、
Claude Code 改成拒絕」，並新增一條研究紀錄事實掛這句原文。

**2. callout 的「`--ask-for-approval` 只有 on-request 與 never」是全稱否定。**
文件的值欄位寫的是 `--ask-for-approval, -a on-request | never`——那是一份**列舉**，
不是「這個旗標只有兩個值」的宣告。已改成「`--ask-for-approval`，**文件只列出** on-request 與 never」。
（順帶查過：`developer-commands` 與 `non-interactive-mode` 兩頁都沒有出現 `untrusted`、
`on-failure`、`approval_policy` 之類的其他取值。）

**3. callout 裡與正文重複的「預設沙盒唯讀」六個字刪掉，但書保留。**
正文「實作」那段已經寫「官方文件寫預設沙盒是唯讀」。刪的是重複敘述，
文件上的但書「自動化要自己指定需要的最小權限」（`In automation, set the least permissions
needed for the workflow`）**原封不動留著**。這是換給第 1 處的字數。

**4. 導言第二段三次講「登入」，合併成一次；`或金鑰設定`這個限定詞保住。**
原句「已經安裝並各自**登入**……並且三支 CLI 都已經完成官方要求的**登入或金鑰設定**；
這篇不重講怎麼安裝或**登入**」。第一輪把 `description` 的「並各自完成登入或金鑰設定」
改短成「並各自登入」，所以「或金鑰設定」全篇只剩導言這一處——**不能連這裡也刪**。
已合併成「已經裝好……而且三支都完成官方要求的登入或金鑰設定」。
段落字數 2,944 → **2,933**，內文長度維持 **6,000**（與第 1～3 處相抵剛好 0）。

**研究紀錄 5 處**

**5.（最重）第 47 條事實與文章、與 `must_not_write` 自相矛盾。**
`fact` 寫「Gemini CLI 的文件列出**完整**結束代碼對照表」，但它掛的引文是
`The CLI returns standard exit codes to indicate the result of the headless execution`
——**沒有「完整」的意思**；`must_not_write` 第 7 條也明寫不准這樣講。
第一輪改了正文三處卻漏了這條紀錄。已改成
「文件寫它回傳標準的結束代碼，底下列出四個；文件沒有自稱這份對照是完整的」。

**6.（最重）第 21 條事實的引文撐不起它自己。**
`fact` 寫「先 `git add -N .` 再 `git diff` 產出 patch，新建檔案才會進到 patch」，
`verbatim_quote` 卻只有 `git diff --binary HEAD > codex.patch` 一行——
`git add -N` 那半句沒有引文，「新建檔案才會進 patch」更是文件沒有說的推論。
已拆成兩條，各掛自己找得到的連續字串（`git add -N .`／
`git diff --binary HEAD > codex.patch`）；「`git add -N` 讓新建檔案出現在 `git diff`」
改由拋棄式儲存庫的對照實測支撐，並寫進「留給站主的事」。

**7. 新增一條事實**：`--permission-prompts` 的版本下限，引文
`Requires Claude Code v2.1.259 or later`（對應第 1 處）。

**8. `unverified_or_excluded` 有一條已經不符合文章。**
它寫「這篇只在 callout 提一句 Gemini CLI 的 `--yolo` 已標 Deprecated」，
但第一輪重寫 callout 之後正文已經沒有 `--yolo`。已改成正文不再提、研究紀錄保留原句備查。

**9. `left_for_the_owner` 的字數提醒**：2,944 更新為 2,933，並寫明第二輪的字數是從哪兩處
重複敘述換來的。

### 覆核過而且正確的部分（沒有動）

- **第一輪重寫的 callout 三句，每一句都回得到自己那家的原句**：
  Claude Code 的 `--permission-prompt-tool`（`Specify an MCP tool to handle permission prompts
  in non-interactive mode.`）、`--permission-prompts none`（`Pass none when nobody can answer,
  and Claude Code denies them instead.`）、dontAsk（`anything that would prompt is denied`、
  `the session never waits for input`）、`-p` 的預設模式（`For -p , that's default when nothing
  is configured`）；Codex 的 `--ask-for-approval`（`Control when Codex pauses for human approval
  before running a command.`）與 `codex exec` 的定位（`for scripted or CI-style runs that should
  finish without human interaction.`）；Gemini CLI 的 Plan Mode
  （`Gemini CLI will stop and wait for your confirmation`，原文在「討論並取得共識」那一步，
  **確實是寫在「才寫正式計畫」之前**）。
  **callout 沒有把本站的延伸用法寫成官方建議**，結尾仍有「本站沒有實測」。
- **Plan Mode 當審查是本站延伸用法**，正文與程式註解都標明了，引的也是文件原句
  （`Plan Mode is a read-only environment for architecting robust solutions before
  implementation.`、`write_file` 與 `replace` `only allowed for .md files in the …/plans/
  directory`）。
- **第一輪新寫的其餘句子**全部回得到原文：summary 第 1／3／4 句、
  表格三格的「結構化輸出驗證」欄與 Codex 角色格、正文表格後那段、
  「實作」那段的 Plan Mode 三句、正文末段、FAQ 第 2／3／4／5 題。
- **Gemini CLI 沒有 schema 驗證旗標這句的範圍是對的**：今天在 README、headless.md、
  cli-reference.md、plan-mode.md 四頁搜尋 `schema`，只有 headless.md 的 `**Schema:**` 小標
  與 plan-mode.md 的 `postgres_read_schema` 範例，沒有任何驗證旗標。
- **summary ⊆ 正文、FAQ 答案 ⊆ 正文**，表格 20 格、兩個 caption、圖解四組節點與 `hero_label`
  逐格對過，沒有正文以外的數字；FAQ 答案沒有網址。
- **界線**：只有一個 callout 且不是免責聲明；沒有訂閱／購買／投資建議、沒有推薦式比價、
  沒有速度或品質排名、沒有「台灣可用」、沒有把預告寫成已推出；三家的宣稱都有歸屬
  （「Anthropic 的 Claude Code 文件」「OpenAI 的 Codex 文件」「Google 的 Gemini CLI 文件」）；
  沒有任何模型 id，**`models-seen.json` 不需要新增**；正文中間沒有 `link` 區塊。
- **系列兄弟篇的標題今天逐字對過各自的內容包，六篇全部相符**：
  《Claude Code｜非互動執行與 JSON 輸出》《codex exec 與腳本整合》
  《CLI 寫程式：理解、規劃、修改與測試》《Claude Code｜Agent Teams 協作》
  《模型之間交接資料：JSON Schema 與結構化輸出》（`ai-workflow-structured-handoff`）、
  《失敗案例與防護：迴圈、費用爆炸與代理間注入》（`ai-workflow-failures-and-guardrails`）。
  協調者另外點名的 `ai-workflow-mcp-shared-tools`（〈一個 MCP 伺服器，同時接上 Claude Code、
  Codex、Gemini CLI 三個客戶端〉）與 `ai-workflow-cross-review-judge`
  （〈多模型互審：LLM 當評審、投票與集成怎麼做〉）**本文沒有點名**，所以沒有標題要對。
- **結尾兩個 link**：第一個 text 逐字是「多模型 AI 工作流教學：從拆任務到串接不同模型」
  （也正好等於 `ai-workflow-tutorials` 現在的 title，所以自檢沒有那個 FAIL）；
  第二個指向 `claude-code-headless-json`、text 逐字是「Claude Code｜非互動執行與 JSON 輸出」。
- **與必連四篇沒有矛盾也沒有重講**：`claude-code-headless-json` 寫「成功退出碼應為零，失敗為非零」，
  與本篇「只能用『退出碼是不是 0』判斷成敗」一致；本篇沒有重寫那幾篇的教學步驟。
- **`checked_on` 2026-09-18 未更動**，在八條 source、研究紀錄、表格 caption 與圖解 caption 上仍然一致。

### 留給站主的事

1. **第一輪留下的四件事都還在**（Plan Mode 用在無頭審查的殘餘風險、`git add -N` 會動到使用者索引、
   兩個結尾純 link 等協調者 `relink`、內文長度卡在 6,000）。第二輪沒有推翻其中任何一件，只更新了字數。
2. **callout 現在寫的版本下限只適用 `--permission-prompts`。** 若日後把 `--permission-prompt-tool`
   的 MCP 限制（文件另註明要 v2.1.199 以上）也寫進正文，記得一併帶上那個版本。
3. **「`git add -N` 讓 Codex 新建的檔案出現在 `git diff`」這半句是實測，不是文件原句。**
   Codex 的文件只示範了這個順序，沒有解釋原因；本輪在拋棄式儲存庫做了對照實測確認。
   若站主希望正文每一句都只靠文件撐，可以把程式註解那半句改寫成「照 Codex 官方 CI 範例的順序」。
4. **內文長度已經沒有餘裕**：`_body_length` 剛好 6,000（上限也是 6,000），
   本輪補一句限定詞就得在別處精簡同樣多的字。下一次要再補，請同樣從重複敘述換，
   不要動查證過的限定條件。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-coding-agents-division paragraphs 2933 code_blocks 2 sources 8
```

沒有 FAIL；只剩協調者會處理的 `raw_internal_url` WARN。
段落字數 **2,933**（1,800–3,000），內文長度 **6,000**（life 類建議上限 6,000，沒有新 WARN），
title 28 units，description 196 units，`code` 區塊兩個（bash 67 行、json 18 行，都 ≤ 80）。

### 結論

`ok`。第二輪改的 9 處都是限定詞與引文層級的收尾——沒有動骨幹論述，
也沒有改任何一行程式碼（`workflow.sh` 與 `review.json` 只是重驗，md5 與第一輪相同）。
第一輪重寫的 callout、移除 `--skip-git-repo-check`、補 `git add -N` 與 `:(exclude)` 這三項骨幹改動，
本輪逐句回原文並在拋棄式 Git 儲存庫實跑六種情境後**全部確認成立**。文章可刊。
