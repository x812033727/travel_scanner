# 獨立查核：ai-workflow-agent-local-batch-script

查核代理：未參與撰稿。查核日 **2026-10-04**（台北時間；重抓時 UTC 仍是 2026-10-03）。
文章原本的 `checked_on` 是 2026-10-03，內容包八條 source、研究紀錄、表格 caption、圖解 caption 一致。
今天重抓沒有任何數字或用詞變動，**不改**。補進的三條 source 也寫 2026-10-03：撰稿者 10-03 讀過 CLI reference
與 Codex 非互動頁（見研究紀錄 `fetch_log`），Ollama Cloud 頁是本代理在 UTC 2026-10-03 讀的（BRIEF 規定用 `date -u +%F`）。

查核方式：`sources[]` 全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，有官方 `.md` 匯出的另抓 `.md` 對照。
把 title、description、導言、summary、正文每一句、表格每一格與 caption、callout、清單、FAQ 答句、
圖解 caption 與研究紀錄 `diagram` 格子、`hero_label`、四個 code 區塊的每一個識別字拆開，逐條對回原文。
`verbatim_quote` 一律綁回**它自己的 `url`** 做連續字串比對（HTML 標籤刪成空字串、實體還原、空白正規化；
`.md` 另去反引號與跳脫字元）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email、姓名或任何個人資料。**
這台電腦沒有 Ollama、Codex，沒有安裝任何東西，沒有改任何環境變數或 Claude Code 設定；Python 範例只用假的 `urlopen` 離線跑。

檢查的主張：**約 170 條**（title、description 3 句、導言 8 句、summary 5 句、正文約 70 句／子句、表格 25 格與 caption、
callout 5 句、清單 3 項、FAQ 6 題答句、圖解 caption 與 4 組節點、`hero_label`、code 約 45 個識別字），
外加研究紀錄 77 條 `verified_facts` 引文與 21 條 `code_checks`。
**改了 17 處**：事實性 8 處（4 處是同一件事：「是不是本機」只看標籤），限定詞與歸因 9 處（5 處是同一件事：沙盒的範圍）；
另補三條 source、更新一條 source 網址、檔案改成 LF。

## 重抓結果：全部讀到正文

| source | HTTP | bytes（HTML／.md） | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.ollama.com/api/chat` | 200 | 396,621／20,480 | **是**。`.md` 是完整 OpenAPI：`servers: - url: http://localhost:11434`、`security: []`、`ChatRequest` 的 `required: - model - messages`、`format`、`stream`（`default: true`）、`think`、`ModelOptions`（`temperature`、`num_ctx`）、回應的 `message.content`、`message.thinking` |
| `docs.ollama.com/capabilities/structured-outputs` | 200 | 359,838／5,328 | **是**。最上方 Note `Ollama's Cloud currently does not support structured outputs.`、schema 放 `format`、schema 也放進提示詞的 Note、`Lower the temperature (e.g., set it to 0)` |
| `docs.ollama.com/cloud`（**新增**） | 200 | 286,733／2,731 | **是**。`Run models in Ollama's cloud…`、`For API requests to ollama.com, use the name returned by this list, such as gemma4:31b. In the Ollama app or CLI, use gemma4:cloud.`、`Ollama processes cloud prompts and responses…` |
| `ollama.com/library/qwen3.5/tags` | 200 | 244,976／— | **是**。能力列 `vision tools thinking`；`4b` 3.4GB、`9b` latest 6.6GB，全部 256K；**沒有任何 cloud 標籤**。標籤數今天是 65（撰稿當天 64，頁面「29 minutes ago」剛加了 `0.8b-mtp-q8_0`），正文不寫總數 |
| `ollama.com/library/glm-4.7-flash/tags` | 200 | 33,205／— | **是**。`tools thinking`，4 個標籤：latest／q4_K_M 19GB、q8_0 32GB、bf16 60GB，198K；沒有 cloud 標籤 |
| `ollama.com/library/deepseek-r1/tags` | 200 | 137,194／— | **是**。`tools thinking`；`7b` 4.7GB、`8b` latest 5.2GB，128K；`1.5b`、`14b`、`32b`、`70b`、`671b` 都在；沒有 cloud 標籤 |
| `code.claude.com/docs/en/permissions` | 200 | 788,677／78,480 | **是**。Read deny 範圍、沙盒、信任表格、Bash 規則語法、唯讀指令清單都在 |
| `code.claude.com/docs/en/tools-reference` | 200 | 704,390／76,884 | **是**。`Timeout and output limits`、`Foreground commands that move to the background`、`When a background command stops` 三節都在 |
| `code.claude.com/docs/en/cli-reference`（**新增**） | 200 | 533,640／46,824 | **是**。`claude -p "query"`、`--print, -p`、`--allowedTools` 三列 |
| `learn.chatgpt.com/docs/permissions`（**網址更新**） | 200 | 451,787／38,356 | **是**。原網址 `developers.openai.com/codex/permissions` 今天回 `308 Permanent Redirect` 到這裡；頁首 `Beta. Permission profiles are under active development and may change.` |
| `learn.chatgpt.com/docs/non-interactive-mode`（**新增**） | 200 | 425,082／14,843 | **是**。`Pass a task prompt as a single argument:`、`-o <path>`、`By default, codex exec runs in a read-only sandbox.`、`Git repository required` 一節 |

## 程式範例重驗

| 區塊 | 語言 | 行數 | 編譯 | 比對過的識別字 | 文件 |
| --- | --- | --- | --- | --- | --- |
| `local_batch.py` | python | 78 → **79** | `compile()` ok（暫存路徑過長，`py_compile` 寫不出 `__pycache__`，改用它內部同一步的 `compile()`；檢查器的 `py_compile` 也過） | `/api/chat`、`model`、`messages`（`system`／`user`）、`stream`、`format`（schema 物件）、`options.temperature`、回應 `message.content`；`urllib.request.Request(url, data, headers, method)`、`urlopen(…, timeout=)`、`json.load`（二進位檔案物件）、`json.loads`、`json.dumps(ensure_ascii=False)`、`Path.glob`／`mkdir(exist_ok)`／`exists`／`read_text`／`write_text`／`open`／`stem`、`urllib.parse.urlparse(...).hostname`（小寫）、`sys.exit(str)` 結束碼 1；例外 `URLError`、`HTTPError` ⊂ `OSError`、`socket.timeout` = `TimeoutError` ⊂ `OSError`、`JSONDecodeError`、`UnicodeError` ⊂ `ValueError` | docs.ollama.com/api/chat、/capabilities/structured-outputs、/cloud；docs.python.org 的 urllib.request、urllib.error、urllib.parse、json、pathlib、exceptions、socket、sys |
| `.claude/settings.json` | json | 7 | `json.loads` ok | `permissions.deny`、`Read(./inbox/**)`（`./path` 相對於目前目錄，範例同型 `Read(./secrets/**)`） | code.claude.com/docs/en/permissions |
| Codex `config.toml` | toml | 7 | `tomllib` ok | `default_permissions`、`[permissions.reader]`、`extends = ":read-only"`、`[permissions.reader.filesystem.":workspace_roots"]`、`"inbox" = "deny"`（同型 `"generated" = "deny"`） | learn.chatgpt.com/docs/permissions |
| 兩個代理的呼叫指令 | bash | 6 | `bash -n` ok | `claude -p "…"`、`--allowedTools "Bash(python local_batch.py *)"`、`> report.md`；`LOCAL_MODEL=qwen3.5:9b python local_batch.py 20`；`codex exec "…"`、`-o report.md`、沒有 `--sandbox` | cli-reference、headless（研究紀錄 code_checks）、permissions（規則語法）、non-interactive-mode、developer-commands（`--output-last-message, -o`） |

模型 id：code 用 `qwen3.5:4b`、`qwen3.5:9b`，正文與表格用 `glm-4.7-flash`、`deepseek-r1` 系列，都在 `models-seen.json`，**沒有新增**。
沒有金鑰、沒有字面密碼、沒有刪檔、沒有 `eval`、網路呼叫有 `timeout`、沒有貼執行輸出。

**離線實跑（假的 `urlopen`，十封虛構信，沒有任何網路請求）**，正文描述的行為全部成立：

- `python local_batch.py 3`：處理 a、b、c；c 兩次都連不上 → `failed.txt` 記 `c.txt`；印 `done=2 failed=1 left=7`。
- 不帶參數再跑：跳過已有結果檔的 a、b 與名單上的 c；d（第一次不是 JSON）、f（列舉值不合）、i（回應沒有 `message`）重試一次成功；
  e（兩次逾時）、g（多一個欄位）、h（HTTP 500 後空白摘要）、j（回應是數字）兩次都失敗 → 寫進 `failed.txt`；印 `done=3 failed=4 left=0`。
- 第三次跑：沒有呼叫，印 `done=0 failed=0 left=0`。
- 請求：`POST http://localhost:11434/api/chat`、`timeout=120`、`Content-Type: application/json`，body 只有 `model`、`messages`、`stream: false`、`format`、`options: {temperature: 0}`；
  系統提示詞裡有同一份 schema；結果檔是 `out/<檔名不含副檔名>.json`、中文不跳脫。
- **協調者交辦的主機漏洞：草稿確實有。** `OLLAMA_URL=https://ollama.com`、`LOCAL_MODEL=glm-5.3-flash`（不帶 cloud）時，
  草稿的檢查放行，虛構信的內容被送到 `https://ollama.com/api/chat`（假 `urlopen` 收到）。修正後的腳本在送出前就結束，什麼都沒送出；
  `127.0.0.1:11500`、`LOCALHOST` 放行，`192.168.1.20`、`localhost.example.com`、cloud 標籤都拒絕，結束碼 1。

## 改掉的 17 處

### 事實性（8 處）

1. **「是不是本機」只看標籤（code，與第 16 篇對齊）。** 草稿只檢查 `MODEL.endswith("cloud")`。Ollama 的 Cloud 頁寫
   `For API requests to ollama.com, use the name returned by this list, such as gemma4:31b. In the Ollama app or CLI, use gemma4:cloud.`
   ——直接打 ollama.com 時名字不帶 cloud。離線實證見上。已照第 16 篇的寫法加上
   `urlparse(URL).hostname not in ("localhost", "127.0.0.1")`（新增一行 `from urllib.parse import urlparse`），
   錯誤訊息改成 `OLLAMA_URL 要是本機位址，LOCAL_MODEL 要是本機標籤`，註解寫明「範例自己的檢查」。78 → 79 行，逾時、重試、`failed.txt` 都沒動。
2. **summary 第 2 句**「所以腳本遇到 cloud 標籤會直接停下」→「範例因此自己加了一道粗略檢查：連的是本機位址，而且標籤不帶 cloud，才往下跑」。
3. **換模型那一段**：原「腳本一開始就檢查標籤……所以這支腳本只對本機標籤成立」與「指到別台機器……本文不討論」→
   寫明兩個條件、引 Ollama 雲端文件（App 或命令列用帶 cloud 的名字，直接呼叫 ollama.com 的 API 卻用不帶 cloud 的名字，雲端會處理送去的提示詞），
   並寫「這道檢查只是防呆，不是官方的判定方法」；「下表只抄標籤頁的本機標籤」→「標籤頁上有檔案大小的本機標籤」。
   原句「帶 cloud 的標籤在 Ollama 的雲端執行」在原本八條 source 裡**找不到支撐**（結構化輸出頁只說雲端不支援結構化輸出，三個標籤頁沒有 cloud 標籤），
   所以補進 `docs.ollama.com/cloud`（finding：骨幹句缺來源）。
4. **FAQ 第 2 題**同步改成兩個條件，答句的歸因改成 Ollama 雲端文件，並補一句「直接呼叫 ollama.com 的 API 時，模型名字不帶 cloud，所以位址也要一起看」。
5. **呼叫指令那一段的推理接錯（撰稿者沒點到）。** 原「官方說結尾的空格加星號也比對不帶參數的指令，**所以帶批次數字的呼叫放行得了**」。
   權限頁那一句講的是 `Bash(ls *)` 也比對 `ls`；帶參數放行得了是因為 `Bash rules match the whole command text, with * standing in for any text.`
   → 「官方說規則裡的星號代表任何文字，結尾的空格加星號也比對不帶參數的指令，所以帶不帶批次數字都放行得了」。
6. **`codex exec` 要在 Git 儲存庫裡執行（漏寫）。** 非互動頁 `Codex requires commands to run inside a Git repository to prevent destructive changes.`
   讀者照文章開一個新資料夾，第二行就會失敗。已在呼叫指令那一段補一句，並寫出 `-o` 是把最後的回答寫成檔案（`If you only need the final message, write it to a file with -o <path>`）。
   Git 怎麼滿足留給《codex exec 與腳本整合》（那篇用 `git init`）。
7. **Codex 清單第 2 項漏掉設定檔那一半。** 原文 `If sandbox_mode appears in any loaded config file, you pass --sandbox, or the selected config profile sets sandbox_mode, Codex uses those older sandbox settings instead of default_permissions.`
   草稿只寫「只要帶了 --sandbox」。→ 補「或任何載入的設定檔裡有 sandbox_mode」「設定檔裡也不要留 sandbox_mode」。
8. **FAQ 第 5 題的重試說法與程式不符。** 原「也可以先改 LOCAL_MODEL 換一個本機標籤再試」；但腳本會跳過 `failed.txt` 名單上的信，
   只換模型不會重試（離線實跑確認）。→「把那幾行從 failed.txt 刪掉，改 LOCAL_MODEL 換一個本機標籤再跑；不刪的話，腳本換了模型仍會跳過它們」。

### 限定詞與歸因（9 處）

9–13. **沙盒「會一起擋住腳本」寫成無條件（撰稿者請查的 a、b）。** 權限頁寫沙盒 `It applies only to Bash, PowerShell, and Monitor commands and their child processes.`，
   同頁也寫 `Commands that won't run sandboxed, such as excluded commands, respect the bare Bash ask rule as usual.`。
   所以「會一起被擋」只對在沙盒裡執行的腳本成立。summary 第 3 句、權限範圍那一段、callout 都改成「代理在沙盒裡執行的腳本」；
   Codex 一側（清單第 1 項、FAQ 第 6 題）同理改成「由 Codex 在沙盒裡執行的腳本」，依據是 `Permission profiles govern sandboxed commands that run on your machine.`
   與 `Denies both reads and writes under the path.`，另有 `approved escalations use their own controls`。權限範圍那一段的導讀另補「哪些系統能用」，指向沙盒實驗那篇。
14. **temperature**：原「頁面也建議把 temperature 設成 0」，原文 `Lower the temperature (e.g., set it to 0)` → 「建議調低 temperature，例如設成 0」。
15. **description 缺 beta**：「Codex 的 permission profile」→「Codex 的 permission profile（beta）」。正文本來就寫了 beta。
16–17. **「代理的 Bash 工具」**（summary 第 5 句、逾時那一段）→「Claude Code 的 Bash 工具」。兩分鐘與十分鐘只有 Claude Code 的文件寫，Codex 這條路由你自己跑腳本。

### 其他

- **補三條 source（協調者交辦）**：`code.claude.com/docs/en/cli-reference`（`-p`、`--allowedTools`）、`learn.chatgpt.com/docs/non-interactive-mode`（`codex exec`、`-o`、Git）、
  `docs.ollama.com/cloud`（上面第 3 處）。對應引文從 `code_checks` 移進 `verified_facts`，另加 Ollama Cloud 三條、權限頁兩條（子行程、被排除的指令）、非互動頁四條。
  headless 頁兩條仍留在 `code_checks`（只是重新導向的旁證，不需要成為來源）。內容包與研究紀錄的 `sources` 順序與 `checked_on` 一致，共 11 條。
- **Codex Permissions 網址**：`developers.openai.com/codex/permissions` 今天回 308 到 `learn.chatgpt.com/docs/permissions`，兩個檔都換成新網址（同組第 13、16 篇也用 learn.chatgpt.com）。
- **研究紀錄 qwen3.5 能力列那一條**：引文 `… 122b Name 64 models` 今天找不到（頁面變 65），已截到穩定的 `… 122b Name`，事實文字說明數字變動。
- **騰字**（2,941 → 改完 3,076 → 2,996，沒有刪任何但書或限定詞）：導言第二段「個資都是假的」（前面已寫「虛構」）、「最後一件事：」、
  呼叫指令那一段的開頭句「下面的區塊是兩個工具的呼叫」、「不倚賴這個檔案」、幾處「頁面寫的是」「固定如下」之類的贅字。
- **內容包原本是 CRLF**，依規格改成 LF（內容不變）。

研究紀錄同步：`sources`、`verified_facts`（65 → 77 條）、`code_checks`（24 → 21 條，CLI 六條移走、加 `urlparse`／`hostname`／`sys.exit` 三條）、
`code_samples`（python 79 行、`checked_against` 換新網址並加 Ollama Cloud、urllib.parse、sys）、`unverified_or_excluded`、`must_not_write`（加兩條）、`editorial_brief`，加上 `factcheck` 欄位。

## 撰稿者交辦的三件事：今天官方頁上的原句

1. **`Read` deny 對 Bash 的範圍**：正文每一子句都有原句，沒有說得比文件滿。
   `Read and Edit deny rules apply to Claude's built-in file tools, to file commands Claude Code recognizes in Bash, such as cat, head, tail, sed, and tee, and to the targets of Bash redirections such as > file and < file. They don't apply to a command that reads files without naming them, such as grep -r pattern . run from the directory that holds the file, or to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself.`
   callout 的「grep 在免詢問唯讀指令裡」對 `The set includes ls, cat, echo, pwd, head, tail, grep, find, …`。
2. **Bash 逾時**：`BASH_DEFAULT_TIMEOUT_MS — the default when Claude passes no timeout; two minutes out of the box`；
   `BASH_MAX_TIMEOUT_MS — … the effective ceiling is the larger of the two, ten minutes out of the box`；
   `When a foreground command reaches its timeout without finishing, Claude Code moves it to the background instead of stopping it, unless the command starts with sleep.`；
   `In non-interactive mode with the -p flag, background commands end shortly after the run's final result.` 正文與 FAQ 第 4 題一致。
3. **Codex Permissions**：頁首 `Beta.`（正文與 summary、toml label、現在的 description 都寫了 beta）；`deny` 對 `Denies both reads and writes under the path.`；
   管沙盒裡的指令對 `Permission profiles govern sandboxed commands that run on your machine.`；不能併用對 `Permission profiles do not compose with the older sandbox settings.`；
   Windows 對 `unelevated sandboxing is a fallback with weaker network isolation and cannot enforce every split read/write carveout, so unsupported policies are refused. Use WSL when you need the Linux sandbox model.`；
   toml 每個鍵都在頁面上（見程式範例表）。「你先自己跑腳本，codex exec 只讀 out」這個安排成立。

## 查過而且正確的部分（沒有動）

- **撰稿者請查的 c**：權限頁表格 `claude -p or the SDK, folder never trusted` 欄、`permissions.allow rules and additionalDirectories in .claude/settings.json` 列寫 `Not used.`；
  `deny and ask rules aren't affected, since they only restrict.`；`A claude -p run or an SDK session never shows it`。正文與 FAQ 第 3 題成立。
- **撰稿者請查的 d**：`/api/chat` 與 Structured Outputs 兩頁都沒有提到 thinking 與 `format` 一起用的行為（不在 sources 的 Thinking 頁也沒有）。「這兩頁文件沒有寫」成立。
- **撰稿者請查的 e**：結果檔 `out/<stem>.json`，與第 16 篇 `…stem}.json` 一致。
- **表格 25 格**：五個標籤的大小、上下文、輸入、能力列逐格對今天的標籤頁；只列有檔案大小的本機標籤，沒有 `:cloud`。
- **Ollama API**：伺服器位址、`security: []`、必填欄位、`stream` 預設、`format` 可以是 `json` 或 schema、`num_ctx` 單位是 token、`message.thinking`／`message.content` 分欄。
- **結構化輸出**：schema 放 `format`、schema 也放進提示詞（`It is ideal to also pass the JSON schema as a string in the prompt to ground the model's response.`）、
  「能強制回應符合 schema」有歸因（`Structured outputs let you enforce a JSON schema on model responses…`），腳本自己再驗是「本文的做法」。
- **不實測規則**：「本站沒有實測」只在導言第二段一次；title 與 description 沒有「實測」；沒有速度、品質、哪種硬體跑得動的結論；沒有貼執行輸出；
  120 秒與每批 20 封都寫明是本文自己選的數字。
- **必連六篇**：與《本機去識別化、雲端收尾》（網址＋標籤一起釘死）現在完全一致，原本只看標籤的寫法反而比那篇弱；
  《codex exec 與腳本整合》用 `--sandbox read-only`，本文因 profile 不加 `--sandbox`，段落有說原因，不算矛盾；
  《Claude Code｜非互動執行與 JSON 輸出》《權限與 Sandbox 邊界實驗》《模型之間交接資料》《Ollama 入門》都只一句帶過，沒有整段重講。
  第二個結尾連結 text 與 `ai-workflow-local-and-cloud-mix` 的 title 逐字相同。
- **界線**：沒有購買、訂閱、價格或方案比較，沒有推薦式比價；只有一個 callout、沒有免責段落；沒有教把 Ollama 開到區域網路（現在程式直接拒絕非本機位址）。
- 圖解四格與 caption 沒有數字，與指派一致；`checked_on` 全篇一致 2026-10-03。

## 留給站主的事

1. **Claude Code 的沙盒不在原生 Windows 上執行。** Sandboxing 頁寫 `The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed.`
   本文對 Codex 寫了 Windows 的限制，對 Claude Code 只寫「沙盒怎麼開、哪些系統能用，見《Claude Code｜權限與 Sandbox 邊界實驗》」（那篇寫了原生 Windows 不在支援範圍）。
   來源上限 11 條已用完，沒有把 Sandboxing 頁補進來。要在本文直接寫，得換掉一條 source。
2. **Sandboxing 頁有一個用 `excludedCommands` 讓單一 Python 腳本在沙盒外執行的範例。** 套到本文，就是 Claude Code 開沙盒擋 inbox、只讓 `local_batch.py` 不進沙盒，
   代理就能自己跑腳本而其他指令讀不到 inbox。這是設計選擇，而且那頁不在 sources，本輪沒有寫。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-batch-script paragraphs 2996 code_blocks 4 sources 11
```

`raw_internal_url` 的 WARN 是預期的（協調者之後跑 relink）。段落字數 2,941 → **2,996**（1,800–3,000）。

## 結論

`ok`。改了 17 處：事實性 8 處（其中 4 處是同一件事），限定詞與歸因 9 處（其中 5 處是同一件事），沒有超過十處事實。
**骨幹沒有動**（代理跑腳本、Claude Code 的 deny 是護欄、Codex 改成你先跑腳本）。程式範例沒有換掉，只在既有的 cloud 檢查旁加一個主機檢查（與第 16 篇同一寫法）。
若協調者要第二輪，只需要看本輪新寫的句子：換模型那一段、FAQ 第 2 與第 5 題、呼叫指令那一段，以及 `local_batch.py` 的那一行檢查。

## 第二輪

查核代理：未參與撰稿與第一輪。查核日 **2026-10-04**（台北；重抓時 UTC 2026-10-03）。範圍照協調者的指派：第一輪新寫或改寫的每一句重讀原頁、
從第一輪「查過而且正確」隨機抽三分之一、Python 範例重驗與離線實跑、第一輪留下的三件事照協調者的決定處理。
`checked_on` 全篇仍是 2026-10-03（補進的 Sandboxing 頁也是 UTC 2026-10-03 讀的，BRIEF 規定 `date -u +%F`），沒有改。
**任何請求都沒有放入 email、姓名或個人資料**；沒有安裝任何東西，沒有改這台電腦或 repo 的 Claude Code 設定、權限、沙盒或環境變數；Python 範例只用假的 `urlopen`。

### 重抓結果（十二條，含新補的一條）

| source | HTTP | bytes（HTML／.md） | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.ollama.com/api/chat` | 200 | 396,621／20,480 | 是（OpenAPI 全文） |
| `docs.ollama.com/capabilities/structured-outputs` | 200 | 359,838／5,328 | 是 |
| `docs.ollama.com/cloud` | 200 | 286,733／2,731 | 是；第 77 行原句 `For API requests to ollama.com, use the name returned by this list, such as gemma4:31b. In the Ollama app or CLI, use gemma4:cloud.` 還在 |
| `ollama.com/library/qwen3.5/tags` | 200 | 248,279／— | 是；標籤數今天 66（正文不寫），4b、9b 兩列不變，沒有 cloud 字樣 |
| `ollama.com/library/glm-4.7-flash/tags` | 200 | 33,205／— | 是；4 個標籤不變 |
| `ollama.com/library/deepseek-r1/tags` | 200 | 137,194／— | 是；7b、8b 兩列不變 |
| `code.claude.com/docs/en/permissions` | 200 | 788,677／78,480 | 是 |
| `code.claude.com/docs/en/tools-reference` | 200 | 704,390／76,884 | 是（含 PowerShell tool 一節） |
| `code.claude.com/docs/en/cli-reference` | 200 | 533,640／46,824 | 是 |
| `learn.chatgpt.com/docs/permissions` | 200 | 451,787／38,356 | 是；頁首 `Beta.` 還在 |
| `learn.chatgpt.com/docs/non-interactive-mode` | 200 | 425,082／14,843 | 是 |
| `code.claude.com/docs/en/sandboxing`（**第二輪新增**） | 200 | 1,004,681／92,057 | 是；第 13 行平台句、權限規則對照表、連 localhost 一節都在 |

研究紀錄 89 條 `verbatim_quote`（第一輪 77 條、本輪新增 12 條）全部在它自己的 `url` 找到；比對法照 FACTCHECK 第 1 節第 8 點（標籤刪成空字串、實體還原、空白正規化；`.md` 去反引號與跳脫）。
另讀 `docs.python.org/3/library/http.client.html`（200，98,890 bytes）供程式範例的例外比對，只進 `code_samples.checked_against` 與 `code_checks`，不進 `sources`。

### 第一輪新寫的句子：逐句重讀的結果

| 句子 | 原頁怎麼寫 | 結果 |
| --- | --- | --- |
| summary 2、換模型那一段、FAQ 2「連的是本機位址，而且標籤不帶 cloud」 | Cloud 頁：直接呼叫 ollama.com 用不帶 cloud 的名字、App 或 CLI 用 `gemma4:cloud`；`Ollama processes cloud prompts and responses to answer your requests.` | 文件那一半成立。**程式那一半不一致**：程式查的是 `MODEL.endswith("cloud")`，正文寫「不帶 cloud」。離線實證 `qwen3.5:cloud-experimental` 會被放行。見改動 2 |
| 同上的「範例自己的粗略檢查」「只是防呆，不是官方的判定方法」 | — | 正文三處與程式註解 `# 範例自己的檢查` 都寫了，成立 |
| 五處「在沙盒裡執行的腳本」 | 權限頁 `It applies only to Bash, PowerShell, and Monitor commands and their child processes.`；`Commands that won't run sandboxed, such as excluded commands, respect the bare Bash ask rule as usual.`；Codex 頁 `Permission profiles govern sandboxed commands that run on your machine.` | 五處都撐得住。但「哪些系統能用」沒寫：Sandboxing 頁 `The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed.` 見改動 4、5。呼叫指令那一段的前提「沒有用沙盒擋住 inbox」另有問題，見改動 6 |
| 「規則裡的星號代表任何文字」 | `Bash rules match the whole command text, with * standing in for any text.`；`A * in a Bash rule matches any text, including spaces` | 成立（後一句補進 verified_facts） |
| 「官方也寫 codex exec 要在 Git 儲存庫裡執行」 | `Codex requires commands to run inside a Git repository to prevent destructive changes. Override this check with codex exec --skip-git-repo-check if you're sure the environment is safe.` | **比文件說得滿**：文件給了略過方式。見改動 8 |
| 「-o 把最後的回答寫成檔案」 | `If you only need the final message, write it to a file with -o <path>/--output-last-message <path>.` | 成立 |
| FAQ 5「先把那幾行從 failed.txt 刪掉，再換 LOCAL_MODEL」 | （程式行為） | 離線實證成立：只換模型 `done=0 failed=0 left=0`；刪掉 `c.txt` 那一行再換模型，`done=1`、`c.json` 出現 |
| description「permission profile（beta）」 | Codex Permissions 頁頁首 `Beta. Permission profiles are under active development and may change.` | 成立；全篇其他功能（Claude Code 沙盒、CLI 旗標）原頁沒有 beta／preview 標示。本輪新提到的 PowerShell 工具原頁標 preview，正文與註解都寫了「預覽」 |
| temperature「建議調低，例如設成 0」 | `Lower the temperature (e.g., set it to 0) for more deterministic completions.` | 成立 |
| 「Claude Code 的 Bash 工具」兩分鐘、十分鐘、移到背景 | Tools reference 第 160、161、210 行 | 成立 |
| 第一輪從 `code_checks` 移進 `verified_facts` 的 CLI 引文 | `claude -p "query"`、`--print, -p`、`--allowedTools`（cli-reference）；`Pass a task prompt as a single argument:`、`-o <path>`、Git（non-interactive-mode） | 六條都在各自的頁面。bash 區塊的每個旗標都有一條：`-p`、`--allowedTools`（多個規則以空白分開，對 cli-reference 範例 `"Bash(git log *)" "Bash(git diff *)" "Read"`）、Bash 與 PowerShell 規則、`codex exec` 的單一提示詞、`-o`；`> report.md` 是 shell 重新導向（headless 頁旁證仍在 `code_checks`） |

### 抽查（第一輪「查過而且正確」12 項，固定種子抽 4 項）

1. **Bash 逾時與移到背景**：Tools reference 第 160–161 行（兩分鐘、十分鐘）、第 210 行（移到背景，sleep 開頭除外）、第 186 行（`-p` 的背景指令在最後結果後不久結束）。成立。
2. **表格 25 格**：五列的大小、上下文、輸入、能力列逐格對今天三個標籤頁，全部相同；三頁都沒有 cloud 字樣。成立。
3. **`out/<stem>.json` 與第 16 篇一致**：第 16 篇 `target = OUT / f"{source.stem}.json"`。成立。
4. **必連六篇不矛盾**：六篇的 zh-TW title 與正文點名一致；《codex exec 與腳本整合》用 `--sandbox read-only` 與 `git init`，本文說了不加 `--sandbox` 的原因；《Claude Code｜權限與 Sandbox 邊界實驗》寫原生 Windows 不在沙盒支援範圍，與本輪補的平台句一致。成立。

抽查沒有發現錯誤。

### 程式範例重驗

| 區塊 | 行數 | 編譯 | 本輪比對 |
| --- | --- | --- | --- |
| `local_batch.py` | 79 → **78** | `compile()` 與 `py_compile` 都過（檢查器的 `py_compile` 也過） | 新增 `http.client.HTTPException`（docs.python.org：`The base class of the other exceptions in this module. It is a subclass of Exception.`；`IncompleteRead` 與 `BadStatusLine` 是它的子類別；`RemoteDisconnected` 是 `A subclass of ConnectionResetError and BadStatusLine.`） |
| `.claude/settings.json` | 7 | `json.loads` ok | 不變 |
| Codex `config.toml` | 7 | `tomllib` ok | 不變 |
| 兩個代理的呼叫指令 | 6 | `bash -n` ok | 新增 `"PowerShell(python local_batch.py *)"`（權限頁 `PowerShell permission rules use the same shape as Bash rules.`） |

**離線實跑**（假的 `urlopen`，虛構信，沒有任何網路請求；腳本是改完的版本，另用改前的版本跑同一組以作對照）：

- **主機與標籤檢查**：預設 `http://localhost:11434`、`http://127.0.0.1:11500`、`http://LOCALHOST:11434` 放行；`192.168.1.20`、`https://ollama.com`（配 `glm-5.3-flash`）、`localhost.example.com`、`http://localhost:11434@ollama.com` 拒絕；`glm-5.3:cloud`、`gpt-oss:120b-cloud` 拒絕。拒絕時結束碼 1、`urlopen` 一次都沒被呼叫。`qwen3.5:cloud-experimental`：改前放行、改後拒絕。
- **跳過、重試、failed.txt、每批上限、統計**（十封，`out/b.json` 預先存在）：`python local_batch.py 4` → 處理 a、c、d、e，`done=2 failed=2 left=5`；不帶參數 → f（列舉值不合後重試成功）、g（兩次 HTTP 500）、h（`RemoteDisconnected` 後重試成功）、i、j，`done=4 failed=1 left=0`；第三次 `done=0 failed=0 left=0`。`failed.txt` 是 c、e、g；`b.json` 沒被動過；重試過的信各呼叫兩次、其他一次。請求是 `POST http://localhost:11434/api/chat`、`timeout=120`，body 只有 `format`、`messages`、`model`、`options`、`stream`。
- **連線中途斷掉**（協調者交辦）：**改前**，回應本文讀到一半丟 `http.client.IncompleteRead`，或 `getresponse()` 丟 `BadStatusLine`，腳本以 traceback 中止（結束碼 1），沒有寫 `failed.txt`，後面兩封沒處理。`RemoteDisconnected` 本來就被 `except OSError` 接住。**改後**，三種都是重試一次、寫進 `failed.txt`、後面兩封照常處理，`done=2 failed=1 left=0`。
- **兩個批次同時跑**（協調者交辦）：七封（一封永遠逾時），兩個行程相隔 0.1 秒啟動、每次假呼叫 0.4 秒。每封信都被**兩個行程各問一次**（共 16 次呼叫，正常是 8 次）；兩個行程**各自印 `done=6 failed=1 left=0`**；`failed.txt` 出現**兩行 `z.txt`**；六個結果檔都能解析（後寫的蓋掉先寫的）；再跑一次 `done=0`。結論：重複處理與統計失真有實證，結果檔寫壞**沒有**實證，所以正文只寫「否則會重複處理同一封信」。

### 改了 13 處

1. **`local_batch.py` 接住連線中途斷掉（協調者交辦）。** `except (OSError, ValueError, KeyError, TypeError)` → 加上 `http.client.HTTPException`，開頭加 `import http.client`。
   文件：`HTTPException` 是 `a subclass of Exception`，不是 `OSError`；`IncompleteRead`、`BadStatusLine` 是它的子類別。為什麼：正文說兩次都失敗就記進 `failed.txt`，改前這兩種例外會讓腳本中止（實證見上）。
2. **`local_batch.py` 的標籤檢查與正文一致。** `MODEL.endswith("cloud")` → `"cloud" in MODEL`。為什麼：summary 2、換模型那一段、FAQ 2 都寫「標籤不帶 cloud」，程式只看結尾；改程式一處比改正文三處少動，而且只會更嚴。第 16 篇仍是 `endswith`，見「懷疑但沒動」。
3. **`local_batch.py` 行數。** `urllib.request.Request(...)` 四行併成兩行，`MODEL =os` 補空白。79 → 78 行。為什麼：多了一行 import，description 與導言寫「不到 80 行」，要維持成立。研究紀錄 `code_samples.lines` 同步為 78。
4. **補第 12 條 source 與平台句（協調者交辦）。** 權限範圍那一段「沙盒怎麼開、哪些系統能用，見《Claude Code｜權限與 Sandbox 邊界實驗》」→「官方沙盒頁寫它在 macOS、Linux 與 WSL2 上執行，原生 Windows 上指令不經沙盒；怎麼開見《Claude Code｜權限與 Sandbox 邊界實驗》」。
   文件：`The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed. To use the sandbox on a Windows machine, run Claude Code inside a WSL2 distribution.`
5. **summary 3 讓 Windows 讀者知道。**「要硬擋得靠沙盒，」→「要硬擋得靠沙盒（官方寫原生 Windows 上指令不經沙盒），」。依據同上。
6. **呼叫指令那一段的前提。**「讓代理自己執行腳本，前提是沒有用沙盒擋住 inbox」→「前提是腳本不在沙盒裡執行」。
   文件：權限頁 `Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration.`；沙盒頁對照表 `Read and Edit deny rules | Block access to specific files or directories`。為什麼：讀者照本文放了 `Read(./inbox/**)`，一開沙盒這條就併進沙盒設定，等於「用沙盒擋住了 inbox」，原寫法會讓人以為沒設 `denyRead` 就沒事。
7. **callout 的沙盒句。**「但用它擋住 inbox，代理在沙盒裡執行的 local_batch.py 也會一起被擋」→「但權限頁也寫權限規則的路徑會併進沙盒設定，所以開了沙盒，上面那條 deny 連代理在沙盒裡執行的 local_batch.py 也會擋」，兩步安排的結尾補「原生 Windows 上指令不經沙盒，這一步只靠 deny 就只是護欄」。依據同 4、6。
8. **`codex exec` 的 Git 檢查不要說得比文件滿。**「官方也寫 codex exec 要在 Git 儲存庫裡執行」→「預設要在 Git 儲存庫裡執行」。文件見上表。旗標本身沒寫進正文（字數已到上限；研究紀錄有引文）。
9. **Windows 上的 PowerShell 工具（本輪自己發現）。** 呼叫指令那一段補「Windows 上 Claude 可能改用預覽中的 PowerShell 工具，所以也放行同樣的規則」；bash 區塊的 `--allowedTools` 多一條 `"PowerShell(python local_batch.py *)"`，註解寫「Windows 上 PowerShell 工具（預覽）多半預設開啟，所以兩種規則都放行」。
   文件：Tools reference `the tool is on by default for claude.ai and Console accounts`、`When the tool is enabled, Claude treats PowerShell as the primary shell.`、`The PowerShell tool has the following known limitations during the preview:`；權限頁 `PowerShell permission rules use the same shape as Bash rules.`
   為什麼：讀者多半用 Windows；只放行 `Bash(...)` 時，Claude 若用 PowerShell 工具執行腳本，`claude -p` 不會出現詢問，這次呼叫就沒有被預先放行。
10. **同一時間只跑一批（協調者交辦）。** 逾時那一段「被切斷或重跑都能接續。」→「被切斷或重跑都能接續，但同一時間只跑一批（本文的建議），否則會重複處理同一封信。」；FAQ 4「直接再跑一次。」→「先確定上一批已經結束再跑。……前景指令到了逾時會被移到背景而不是終止，上一批可能還在跑；同一時間只跑一批是本文的建議。」；`claude -p` 的提示詞加「上一次結束才跑下一次」。
    依據：Tools reference `Claude Code moves it to the background instead of stopping it`，加上本輪離線實證（重複處理、統計失真）。
11. **否定句超出讀過的頁面。**「設 120 秒，這是本文自己選的數字，官方沒有建議值」→「設 120 秒，這只是本文選的例子」。為什麼：「官方沒有建議值」是讀過的頁面以外也成立的說法，撐不住；指派要求自選數值標明只是例子。
12. **Codex 清單第 3 項補 elevated。**「頁面寫原生 Windows 的 unelevated 沙盒無法強制所有讀寫例外」→「頁面寫原生 Windows 上 elevated 沙盒最強；備援的 unelevated 沙盒無法強制所有讀寫例外」。
    文件：`On native Windows, elevated sandboxing is strongest because it can use dedicated lower-privilege sandbox users, filesystem permission boundaries, and firewall rules. unelevated sandboxing is a fallback…`。為什麼：原寫法讓人以為 Windows 上只有 unelevated。
13. **glm-4.7-flash 的其他量化。**「另有 q4_K_M、q8_0、bf16 三種量化，大小是 19GB、32GB 與 60GB」→「另有 q8_0 與 bf16 兩種量化，大小是 32GB 與 60GB」。為什麼：標籤頁上 `q4_K_M` 與 `latest` 是同一個識別碼 `4475827791a2`，表格已列，「另有」不準；也騰出字數。

**騰字**（段落 2,996 → **2,986**；正文總字元也壓回 lint 的 6,000 以內，沒有刪任何但書或限定詞）：結構化輸出那一段重複的「答案在回應的 message.content，腳本讀出來再 json.loads」（思考那一段已寫）、逾時那一段重複的「第一個命令列參數是每次最多處理幾封」（下一節已寫）、「deny 的優先順序高於 allow，allow 不能替它開例外」併成「allow 不能替 deny 開例外」、重複的「在 claude -p 下」、兩個轉場句（「後面兩節就是在處理這個『只要』」「下面的設定就是這樣寫」）、FAQ 2 的「否則直接結束」與「這個做法」。

研究紀錄同步：`sources` 加第 12 條（順序、`checked_on` 與內容包一致）；`verified_facts` 77 → 89 條（Sandboxing 頁三條、權限頁三條、Tools reference 四條、Codex 兩頁各一條）；`code_checks` 加 `http.client` 三條；`code_samples` 的 python `lines` 78、`checked_against` 加 http.client；`unverified_or_excluded` 更新沙盒與 `codex exec` 兩條、新增三條（兩批同時跑、PowerShell 工具、代理伺服器）；`must_not_write` 加三條（`excludedCommands`、沙盒對 Windows 讀者、結果檔寫壞）；`fetch_log` 加兩頁；`factcheck.second_round`。

### 協調者交辦的四件事：處理結果

1. **`http.client.HTTPException`**：實證會中止，已改（改動 1），行數靠合併 `Request(...)` 壓到 78。
2. **背景後再啟一個批次**：實證會重複處理同一封、兩邊統計都失真、`failed.txt` 重複一行；結果檔沒有寫壞。正文補半句並標明是本文的建議（改動 10）。
3. **Claude Code 沙盒的平台**：Sandboxing 頁補成第 12 條，平台句照原文寫進權限範圍那一段（改動 4），summary 3、callout 都讓 Windows 讀者看得到（改動 5、7）；設定步驟仍留給《Claude Code｜權限與 Sandbox 邊界實驗》。
4. **`excludedCommands`**：照決定不採用、不寫（研究紀錄 `must_not_write` 記了）。

### 界線

「本站沒有實測」仍只在導言第二段一次；title 與 description 沒有「實測」；沒有速度、品質或「跑得動」的結論，沒有執行輸出；120 秒與 20 封都標明只是例子；表格只有標籤頁上有檔案大小的本機標籤；否定句（「這兩頁文件沒有寫」）限定在讀過的頁面；範例與文章沒有真實個資（離線實跑用的虛構信只在暫存目錄）。只有一個 callout，沒有免責段落。

### 懷疑但沒動

1. **第 16 篇的標籤檢查仍是 `MODEL.endswith("cloud")`**，本篇改成 `"cloud" in MODEL`。兩篇正文是否都寫「不帶 cloud」、要不要對齊，留給協調者（不在本輪 scope）。
2. **代理伺服器**：`urllib` 會依 `HTTP_PROXY` 等環境變數走代理，沒設 `NO_PROXY` 時連 localhost 的請求也可能送到代理。範例的主機檢查管不到這件事；sources 沒有一頁寫，正文已寫明是粗略防呆，沒有另寫。
3. **Ollama 沒開時**，每封信都會連不上兩次、整批進 `failed.txt`，之後要手動清名單。這是範例的設計，正文寫的「連不上就記進 failed.txt」與程式一致，沒有改。
4. **bash 區塊是 bash 語法**（`LOCAL_MODEL=qwen3.5:9b python …`），原生 Windows 的 PowerShell 不能照打；label 寫明是 bash，沒有改。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-agent-local-batch-script paragraphs 2986 code_blocks 4 sources 12
```

### 結論

`ok`。改了 13 處，其中程式 3 處（接住 `HTTPException`、標籤檢查與正文一致、行數），事實與限定詞 10 處；骨幹（代理跑腳本、Claude Code 的 deny 是護欄、Codex 改成你先跑腳本）沒有動，程式範例沒有換掉。
