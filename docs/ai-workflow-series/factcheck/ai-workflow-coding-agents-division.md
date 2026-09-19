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
