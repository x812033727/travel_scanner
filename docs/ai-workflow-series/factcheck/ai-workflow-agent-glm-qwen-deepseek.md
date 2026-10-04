# 獨立查核：ai-workflow-agent-glm-qwen-deepseek

查核代理：未參與撰稿。查核日 **2026-10-04**（台北時間；重抓時 UTC 是 2026-10-03）。
文章的 `checked_on` 是 2026-10-03，內容包 sources、研究紀錄、表格 caption、圖解 caption 一致，
重抓沒有任何數字變動，**不改**。新補的第 13 條 source 也記 2026-10-03（UTC 當天，與檢查器要求的全篇一致）。

查核方式：`sources[]` 12 條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
Z.ai 兩頁與 Claude Code gateway 頁另抓官方 `.md` 版對照。依協調者要求，把 Codex 官方設定參考頁補進 sources（第 13 條）並自己重讀。
為了反駁（**不當文章依據**）另讀了：Ollama 五個家族的 `/tags` 頁、Codex `config-advanced`／`config-basic` 的 `.md`、
Claude Code `env-vars`／`model-config` 的 `.md`。
title、description、導言、summary、正文每一句、三個 list 項、callout、表格每格與 caption、FAQ 五題答句、
圖解 caption 與研究紀錄 `diagram` 的格子、`hero_label`、四個 `code` 區塊的每個識別字，逐條對回原文。
`verbatim_quote` 一律綁回**它自己的 `url`** 做連續字串比對（HTML 標籤刪成空字串、實體還原、空白正規化；`.md` 版另試去反引號）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email、姓名或任何個人資料**；沒有安裝任何軟體、沒有呼叫任何供應商 API、沒有改任何環境變數或設定。

檢查的主張：**約 150 條**（title、description 2 句、導言 7 句、summary 4 句約 8 個子句、正文 17 段約 60 句、
list 3 項約 20 句、callout 標題與 5 句、表格 18 格與 caption、FAQ 5 題約 12 句、圖解 caption 與 4 格、`hero_label`），
外加 code 區塊 **66 個識別字與值**、研究紀錄原有 **132 條**引文（查核後 163 條）。
**改了 14 處**：事實 9 處，歸因、改寫揭露與小修 5 處。

## 重抓結果：12 條都讀到正文，補進第 13 條

| # | source | HTTP | bytes（HTML／.md） | body 是正文嗎 |
| --- | --- | --- | --- | --- |
| 1 | `docs.z.ai/devpack/tool/claude` | 200 | 322,998／6,824 | **是**。副標 Methods for Using the GLM Coding Plan in Claude Code；預設對照三行、自動腳本與手動設定兩個 JSON 都在 |
| 2 | `docs.z.ai/devpack/tool/codex` | 200 | 329,994／7,573 | **是**。Warning 框的 Responses 端點、models.json 全文、config.toml、Note 三點都在 |
| 3 | `api-docs.deepseek.com/quick_start/agent_integrations/claude_code` | 200（轉到尾斜線） | 38,642 | **是**。兩組 export、Model Mapping 一節都在 |
| 4 | `api-docs.deepseek.com/quick_start/agent_integrations/codex` | 200（轉到尾斜線） | 129,666 | **是**。一鍵腳本、Option 2、config.toml、Field Reference 表都在 |
| 5 | `www.alibabacloud.com/help/en/model-studio/claude-code` | 200 | 39,383 | **是**。Last Updated Sep 28, 2026；四種方案的 settings.json、疑難排解表都在 |
| 6 | `www.alibabacloud.com/help/en/model-studio/codex` | 200 | 103,999 | **是**。Last Updated Sep 28, 2026；各方案 Responses／Chat 兩種寫法、FAQ 都在 |
| 7 | `code.claude.com/docs/en/llm-gateway` | 200 | 400,069／7,105 | **是**。不支援接非 Claude 模型一句、Subscriptions and gateways 一節都在 |
| 8 | `ollama.com/library/qwen3.5` | 200 | 196,547 | **是**。標籤表寫 65 models（頁面列 14 列），Applications 區四個指令；頁面標 Updated 27 minutes ago，七個尺寸標籤的數字沒變 |
| 9 | `ollama.com/library/glm-4.7-flash` | 200 | 81,820 | **是**。4 models，大小與上下文逐列相符 |
| 10 | `ollama.com/library/glm-5.3-flash` | 200 | 88,658 | **是**。1 model（`:cloud`，大小欄「-」）、託管地點句、MIT Licensed |
| 11 | `ollama.com/library/deepseek-r1` | 200 | 94,678 | **是**。35 models（頁面列 8 列），Models／Distilled models／License 三段都在 |
| 12 | `ollama.com/library/deepseek-v4.1-flash` | 200 | 89,278 | **是**。1 model（`:cloud`，大小欄「-」），沒有託管句、沒有授權字樣 |
| 13（新增） | `learn.chatgpt.com/docs/config-file/config-reference` | 200 | 1,401,588／131,163 | **是**。伺服器端渲染，canonical 指向自己；`developers.openai.com/codex/config-reference` 今天轉到這裡。`model_providers.<id>.*` 各鍵的說明都在 |

## 程式範例重驗

| 區塊 | 語言 | 行數（改前→改後） | 編譯 | 比對過的識別字 | 文件 |
| --- | --- | --- | --- | --- | --- |
| `ollama-launch-tags.sh` | bash | 11→11 | `bash -n` ok | `ollama launch claude --model` 加五個標籤，逐字對各頁 Applications 區；只改註解（「大小欄」→「Size / Usage 欄」） | ollama.com/library 五頁 |
| `use-endpoint.sh` | bash | 45→45 | `bash -n` ok | 9 個 Claude Code 變數（`ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_MODEL`、`API_TIMEOUT_MS`、三個 `ANTHROPIC_DEFAULT_*_MODEL`、`CLAUDE_CODE_SUBAGENT_MODEL`、`CLAUDE_CODE_MAX_CONTEXT_TOKENS`）、3 個端點網址、12 個值，逐字對三家頁面；變數名另在 Claude Code env-vars 頁確認都存在。只改註解（settings.json→export 的揭露、金鑰變數名是本篇取的） | Z.ai claude、DeepSeek claude_code、阿里雲 claude-code、Claude Code llm-gateway |
| `~/.codex/config.toml`（Z.ai） | toml | 15→15 | `tomllib` ok | `model_provider`、`model`、`model_reasoning_effort`、`model_catalog_json`、`[model_providers.ZAI]` 的 `name`／`base_url`／`env_key`／`wire_api`：值逐字對 Z.ai 頁，鍵逐一對 Codex 設定參考頁；`env_key` 取代頁面的 `experimental_bearer_token`（參考頁：discouraged; use env_key） | Z.ai codex、阿里雲 codex、Codex config-reference |
| `~/.codex/config.toml`（DeepSeek） | toml | 22→22 | `tomllib` ok | 同上，另 `forced_login_method`（參考頁型別 `chatgpt \| api`）、`web_search`（`disabled` 會拿掉工具）、`show_raw_agent_reasoning`；**拿掉 `preferred_auth_method`**（Codex 參考頁、進階頁、基本頁都沒有這個鍵），註解交代，並註明 `[desktop]` 區段不放 | DeepSeek codex、阿里雲 codex、Codex config-reference |

沒有字面金鑰、沒有 `YOUR_API_KEY` 類佔位（頁面上的 `your_zai_api_key`、`<your DeepSeek API Key>`、`YOUR_API_KEY` 都已改成讀環境變數），沒有刪檔、沒有 `eval`、沒有網路呼叫、沒有執行輸出。
code 裡的模型 id（`qwen3.5`、`glm-4.7-flash`、`deepseek-r1`、`glm-5.3-flash:cloud`、`deepseek-v4.1-flash:cloud`、`deepseek-flash`、`qwen3.6-flash`、`qwen3.8-flash`、`qwen3.8-max`、`glm-5.3`）都在 `models-seen.json`。
正文新寫入的 `DeepSeek-R1-0528-Qwen3-8B` 不在清單，已依 Ollama deepseek-r1 頁的原文用 Edit 加在陣列尾端。

## 改掉的 14 處

### 事實（9 處）

1. **判斷「是不是本機」的方法經不起反例（協調者點名的核心）。**
   原 callout：「標籤表的大小欄是 GB 數字的，才是下載到自己電腦的權重；大小欄寫「-」、能力列多一個 cloud 的，是 Ollama 的雲端」。
   glm-5.3-flash 與 deepseek-v4.1-flash 兩頁的 curl 範例是
   `curl http://localhost:11434/api/chat \ -d '{ "model": "glm-5.3-flash:cloud"`——**位址是本機，模型在雲端**；
   反過來，網址不是本機時，名字有沒有 cloud 都一樣送到別人的伺服器。
   另外「大小欄寫「-」」只在模型頁成立，`/tags` 頁同一欄（欄名 `Size / Usage`）寫的是 `Medium Usage`。
   → callout 改成「兩件事同時成立才是本機：連的是自己電腦的位址，而且標籤不帶 cloud、Size / Usage 欄是 GB 數字（本篇讀的雲端標籤在這一欄寫「-」）」，
   並寫進 curl 反例；第 1 節第 1 段、FAQ 1、code 1 註解、研究紀錄圖解第 4 格（「看位址、標籤與大小欄」）同步。
2. **「Ollama 上下載得到的是…」超出讀過的範圍。** summary 2 原寫「Ollama 上下載得到的是 qwen3.5（1.0GB 到 81GB）…deepseek-r1（1.1GB 到 404GB）」。
   本篇只讀了五個模型頁；qwen3.5 頁寫 65 models、deepseek-r1 頁寫 35 models，deepseek-r1 的量化標籤最大到 1.3TB（671b fp16，/tags 頁）。
   → 限定為「本篇讀的五個 Ollama 模型頁裡」「七個尺寸標籤」；第 2 節 GLM、DeepSeek 段與 FAQ 2 同步加「本篇讀的…頁裡」。
3. **models.json 的說法錯了。** 原「Z.ai 的頁面要你自己建立，DeepSeek 的頁面列出完整內容」。
   Z.ai Codex 頁：`Copy the following content entirely into ~/.codex/models.json`，下面就是整份 JSON（slug `glm-5.3`）。
   → 「兩家頁面都列出完整內容，內容卻不同：Z.ai 宣告 glm-5.3，DeepSeek 宣告 deepseek-flash 與 deepseek-v4-pro」；
   「照著做一次只能留一家」改成可驗證的「照兩家頁面原樣貼上，後貼的會蓋掉先貼的；兩家頁面都沒有寫怎麼同時保留」。
4. **DeepSeek toml 的 `preferred_auth_method` 在 Codex 官方文件查不到。**
   Codex 設定參考頁（HTML 與 `.md`）、進階設定頁、基本設定頁都沒有這個鍵；`forced_login_method` 有（`chatgpt | api`，`Restrict Codex to a specific authentication method.`）。
   依規格「官方文件沒有的參數就是錯」，從 toml 拿掉，註解寫明「頁面另有 preferred_auth_method = "apikey"，Codex 的設定參考頁沒有這個鍵，這裡不放」。
   行數不變（同時把 `[desktop]` 區段不放的原因寫進註解）。
5. **`wire_api` 與 Coding Plan（協調者點名第 2 項）。** 原文只寫「Coding Plan 頁面寫它只支援 Chat/Completions API…疑難排解又寫新版 Codex 已不再支援 wire_api 設成 chat」。
   今天的頁面：Coding Plan 那一節還寫 `Coding Plan does not support the Responses API (Chat/Completions API only)`，設定用 `wire_api = "chat"`；
   FAQ 對 `wire_api = "chat" is no longer supported` 的解法是 `Change wire_api to responses and verify that base_url is correct.`；
   Codex 參考頁：`Protocol used by the provider. responses is the only supported value, and it is the default when omitted.`
   → 第 5 節第 2 段把三件事照實並列（不替阿里雲選），第 4 節第 1 段補 Codex 參考頁那一句；「Coding Plan 頁面」改「那一節」（同一頁），FAQ 4 同步。
6. **阿里雲 Claude Code 頁同頁不一致，草稿沒寫。** 設定那一節是四種方案、國際站網址；疑難排解（401 invalid_api_key）卻寫
   `Model Studio provides three access methods, and each access method uses a different base URL and a dedicated API key.`，
   列的是 `https://dashscope.aliyuncs.com/apps/anthropic`、`https://coding.dashscope.aliyuncs.com/apps/anthropic`、`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。
   → list 第 3 項補「同一頁的疑難排解表另列了三組不同的網址，例如 Pay-as-you-go 寫 https://dashscope.aliyuncs.com/apps/anthropic，和設定那一節不一樣；函式照設定那一節，以官網為準」；
   「Token Plan 的兩個版本共用一個網址」限定為「設定那一節裡」。
7. **授權段落漏了一句，而且 latest 標籤不在授權段落裡（協調者點名第 5 項）。**
   頁面授權段落有三句 Please note：Qwen 蒸餾版源自 Apache 2.0 的 Qwen-2.5、**Llama 8B 源自 Llama3.1-8B-Base（llama3.1 license）**、Llama 70B 源自 Llama3.3-70B-Instruct（llama3.3 license）；草稿漏了中間那句。
   同一頁卻把 `deepseek-r1:8b`（也是 latest）標成 `DeepSeek-R1-0528-Qwen3-8B`，授權段落沒有提到 Qwen3。
   → 正文補 Llama 8B 一句與「同一頁把 8b（也就是 latest）標成 DeepSeek-R1-0528-Qwen3-8B，授權段落沒有提到 Qwen3」；
   表格 DeepSeek 兩格：「除 671b 外是蒸餾模型」→「頁面把 671b 標成 DeepSeek-R1，其餘六個列為蒸餾模型」，
   「但蒸餾版源自別的授權」→「同段寫 Qwen、Llama 蒸餾版源自原本另有授權的模型」。與必連的 `deepseek-local-with-ollama`（llama3.1 與 llama3.3）現在一致。
8. **導言「一組讓 Claude Code 指到供應商端點的環境變數」**：程式有三個函式、標題寫「三組環境變數」→ 改成三家。
9. **「資料去向看表格裡的標示就夠了：…標「本機」的才在自己電腦上處理」**：表格標的是標籤，不是連線；依第 1 處的反例，
   → 「標「本機」的標籤，要由自己電腦上的 Ollama 執行才留在本機」。

### 歸因、改寫揭露與小修（5 處）

10. **閘道類比（協調者點名第 4 項）。** 原「下面三家的端點做法上也是把請求網址指到別處、由非 Claude 模型回答；這句話涵蓋哪些情形以 Anthropic 的文件為準」。
    gateway 頁沒有提到供應商端點，三家頁面也沒有自稱閘道，類比撐不住。
    → 只並列兩邊原文：gateway 頁 `ANTHROPIC_BASE_URL is the variable that points Claude Code at the gateway.`；三家頁面也用 `ANTHROPIC_BASE_URL`、回答的是自家模型；「供應商端點算不算這一頁說的閘道，兩邊頁面都沒有寫」。
11. **`env_key` 的出處（協調者點名第 1 項）。** 原本只有阿里雲範例撐。Codex 參考頁：`model_providers.<id>.env_key` = `Environment variable supplying the provider API key.`；
    `experimental_bearer_token` = `Direct bearer token for the provider (discouraged; use env_key).`。
    → 補進第 4 節第 2 段、summary 4、FAQ 5，sources 加第 13 條，`verified_facts` 加 12 條 Codex 鍵的原句；
    並寫明 `ZAI_API_KEY`、`DEEPSEEK_API_KEY` 這些變數名是本篇取的。
    「三家頁面的 Responses 寫法用同一個模式」本身成立：Z.ai、DeepSeek、阿里雲 Token Plan 與 Pay-as-you-go 的 Responses 寫法都有 `[model_providers.X]`＋`base_url`＋`wire_api = "responses"`＋`model_provider`＋`model_catalog_json`，沒有改。
12. **Z.ai 別名（協調者點名第 3 項）。** 原「兩處不一致，所以函式不設別名」。頁面一處是 `with the default configuration as follows`（三個都是 GLM-5.3-Flash），
    一處是手動設定範例（haiku `glm-5.3-flash[1m]`、sonnet 與 opus `glm-5.3[1m]`），頁首另有 `To use the latest GLM-5.3 model, see How to Switch the Model in Use`——
    「不一致」是本篇的判斷。→ 改成並列兩種寫法；函式照**自動腳本**那一組（頁面寫進 settings.json 的只有 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、`API_TIMEOUT_MS`），不設別名，以官網為準。
13. **settings.json 改寫成 export 沒有揭露。** Z.ai（`The script will automatically modify ~/.claude/settings.json…`）與阿里雲（`Create ~/.claude/settings.json`）都寫進設定檔的 `env`，只有 DeepSeek 用 export。
    → 第 3 節第 2 段與 code 2 兩個函式的「來源」註解補上「頁面寫進 settings.json，這裡改成 export」。
14. **小修**：code 2 註解「不寫進任何檔案」→「不寫進這支腳本」（阿里雲自己就叫你把 export 寫進 ~/.zshrc）、「清掉這幾個變數，再開一個新的終端機視窗」→「或」；
    DeepSeek 對照的主詞照原文 `the Claude model names you pass in` 改成「傳入的模型名」；
    刪掉重講蒸餾定義的半句（必連的 `deepseek-local-with-ollama` 已整段講過），改成一句帶過並指向那篇。
    其餘為騰字：段落字數加了上述內容後到 3,206，只刪轉場與重複（「先分清楚三種跑法」「先交代 Anthropic 的立場」「所以不同尺寸的授權文字不只一份」、model_provider 的重複解釋、「兩處怎麼搭配，頁面沒有放在一起說明」等），**沒有刪任何但書、限定詞或「不是本機」的標示**，回到 2,999。

研究紀錄同步：`sources` 加第 13 條（順序、`checked_on` 與內容包一致）；`verified_facts` 新增 31 條（全部綁回自己的 url 比對通過），
改述 2 條（`preferred_auth_method` 那條註明本篇不放；`Model_Studio_Token_Plan` 那條原寫成 Token Plan 通稱，其實是 Team Edition，Personal 是 `Model_Studio_Token_Plan_Personal`）；
`unverified_or_excluded` 改 2 條、加 4 條；`must_not_write` 加 4 條；`code_samples` 兩份 toml 的 `checked_against` 加 Codex 參考頁；`diagram` 第 4 格；加 `factcheck` 欄位。
內容包原本是 CRLF，改成 LF（內容不變，與同系列檔案和 `.gitattributes` 的 `eol=lf` 一致）。

## 查過而且正確的部分（沒有動）

- **端點、模型名、環境變數逐字相符**：`https://api.z.ai/api/anthropic`、`https://api.z.ai/api/v1`、`https://api.deepseek.com/anthropic`、`https://api.deepseek.com/`、
  `https://token-plan.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` 與 `/compatible-mode/v1`、`https://coding-intl.dashscope.aliyuncs.com/apps/anthropic`、
  北京／新加坡／維吉尼亞三個 `{WorkspaceId}` 網址；`API_TIMEOUT_MS` 3000000、`CLAUDE_CODE_MAX_CONTEXT_TOKENS` 983616、Token Plan 別名 `qwen3.6-flash`／`qwen3.8-flash`／`qwen3.8-max`、`auto`。
- **DeepSeek 對照與範例照實並列**：`Models starting with claude-opus are mapped to deepseek-v4-pro`、`…claude-haiku or claude-sonnet are mapped to deepseek-flash`、`billed at the V4 Pro price`；範例三個別名都是 deepseek-flash。價格只寫「以官網為準」。
- **Claude Code 一側的變數**：`ANTHROPIC_AUTH_TOKEN`、`API_TIMEOUT_MS`（預設 600000）、`CLAUDE_CODE_MAX_CONTEXT_TOKENS`、`CLAUDE_CODE_SUBAGENT_MODEL`、`ANTHROPIC_DEFAULT_*_MODEL`、`ANTHROPIC_MODEL` 在 Claude Code env-vars 頁都存在（該頁不進 sources，只用來反駁）。
- **Ollama 五頁**：標籤、大小、上下文、能力列逐列相符；Applications 區五頁都只有 claude、opencode、hermes、openclaw 四個 `ollama launch`，沒有 Codex。
  qwen3.5 的 65 個標籤（/tags 頁）沒有一個帶 cloud，草稿「qwen3.5 頁沒有列；其他 Qwen 檔案庫本篇沒讀」成立。
- **託管與授權字樣**：glm-5.3-flash 頁 `This model is hosted in the United States and Europe. Like all other models on Ollama’s cloud, this model follows Ollama’s privacy policy with zero data retention.` 與 `MIT Licensed`；
  deepseek-v4.1-flash、qwen3.5、glm-4.7-flash 三頁 `licen`／`MIT`／`Apache`／`commercial` 都是 0 次，「頁面沒有寫」成立；沒有一處寫成「可以商用」，deepseek-r1 的 `support commercial use` 寫成該頁的說法。
- **歸因**：「Anthropic 的文件寫不支援透過任何閘道把 Claude Code 導到非 Claude 模型」出現並歸因（summary 3、第 3 節），沒有寫成違反條款；只設網址時 `a saved claude.ai login remains the active credential, so its usage limits and billing apply` 轉述正確。
- **本機與雲端標示**：表格每格都標「本機」或「雲端」，正文每次提到 `:cloud` 標籤或供應商端點都講明去向；第 3、4 節與三個 code 註解都寫「不是本機」。
- **不實測規則**：沒有速度、品質、跑得動／跑不動的結論；沒有執行輸出；「本站沒有實測」只在第二段導言出現一次；title 與 description 沒有「實測」。
- **必連六篇**：title 逐字相符（結尾連結與文中書名號）；`deepseek-local-with-ollama`（六個蒸餾版、8b=Qwen3、llama3.1／llama3.3）、`ollama-getting-started`（大小欄「-」、OLLAMA_NO_CLOUD）、兩篇 Qwen（授權分三種）、`chinese-ai-models-comparison`、`deepseek-privacy-and-data-flow` 都沒有矛盾，各一句帶過。
- **界線**：沒有購買、訂閱或方案建議，沒有價格數字，沒有推薦式比價；方案名（Coding Plan、Token Plan、Pay-as-you-go）只用來區分網址；只有一個 callout、沒有免責段落；沒有教把 Ollama 開到區域網路，沒有教第三方路由器。
- **引文**：原 132 條全部綁回自己的 url 找到；llm-gateway 兩條直引號版只在 `.md` 找得到（HTML 是彎引號 `doesn’t`），Z.ai Codex 三條帶反引號的在 HTML 去反引號後找得到，內容相同，未改。

## 留給站主的事

1. **站內 `qwen-local-deployment`（09-14 查證）舉 `qwen3.5:cloud` 當雲端標籤的例子**；今天 qwen3.5 的 65 個標籤沒有一個帶 cloud。那是另一篇，本輪沒有動，要不要改由站主或協調者決定。
2. **`text_length` 軟性警告 7,606 字**（撰稿時 6,890；生活類指引 1,500–6,000）。增加的是判斷方法的反例、阿里雲同頁不一致、settings.json 改寫揭露與 Codex 參考頁依據，都屬不可刪的但書；壓不到 6,000。
3. **給同組其他篇**：Ollama 雲端標籤的大小欄在模型頁寫「-」、在 /tags 頁寫 `Medium Usage`；本篇改用欄名 `Size / Usage` 說「是不是 GB 數字」。其他篇若寫「大小欄是「-」」，要寫明是哪一頁。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
WARN - lint text_length: 7606 characters of body text; the guideline for life is 1500–6000
OK ai-workflow-agent-glm-qwen-deepseek paragraphs 2999 code_blocks 4 sources 13
```

`raw_internal_url` 的 WARN 是預期的（協調者之後跑 relink）。段落字數 2,834 → **2,999**（1,800–3,000）。

## 結論

`ok`。改了 14 處，事實性 9 處（未超過十處）：判斷本機的方法補上位址條件與反例、「能下載」的範圍、models.json 說錯、
一個 Codex 文件沒有的設定鍵、Coding Plan 與 wire_api 的並列、阿里雲同頁另一組網址、授權段落漏句與 latest 標籤、兩處用詞。
**沒有動到骨幹**（三種跑法、三家逐家寫、金鑰一律讀環境變數都撐得住），程式範例只拿掉 DeepSeek toml 的一個鍵並改註解，沒有換掉任何範例。

## 第二輪

查核代理：另一位，未參與撰稿與第一輪。查核日 **2026-10-04**（台北時間 01:20；UTC 是 2026-10-03）。
沒有任何數字因今天的頁面而改，所以 `checked_on` 一律**不改**。
任何請求的 UA、標頭、查詢字串都沒有放入 email、姓名或個人資料；沒有安裝軟體、沒有呼叫供應商 API、沒有改環境變數或設定。

### 重抓結果

13 條 sources 以 `curl -sL -A "Mokaair-editorial"` 重抓，全部 HTTP 200、body 是正文，bytes 與第一輪幾乎一樣：
Z.ai claude 322,998（.md 6,824）、Z.ai codex 329,994（.md 7,573）、DeepSeek claude_code 38,642、DeepSeek codex 129,666、
阿里雲 claude-code 39,383、阿里雲 codex 103,994（Last Updated 仍是 Sep 28, 2026）、llm-gateway 400,069（.md 7,105）、
qwen3.5 196,546、glm-4.7-flash 81,820、glm-5.3-flash 88,658、deepseek-r1 94,678、deepseek-v4.1-flash 89,278、Codex config-reference 1,401,588（.md 131,163）。
唯一的變動：qwen3.5 模型頁今天寫 **66 models**（第一輪 65），`/tags` 頁 66 個標籤沒有一個帶 cloud；正文只寫七個尺寸標籤，數字沒變，不受影響。
為了反駁另讀（不當依據）：Ollama 五個 `/tags` 頁、Claude Code `env-vars.md`。

### 第一輪新寫或改寫的句子：逐句重查

| 句子 | 原文在哪、怎麼寫 | 結果 |
| --- | --- | --- |
| callout 的判斷法與反例 | glm-5.3-flash、deepseek-v4.1-flash 兩個**模型頁**的 cURL 分頁：`curl http://localhost:11434/api/chat \ -d '{ "model": "glm-5.3-flash:cloud"`（另一頁是 `deepseek-v4.1-flash:cloud`）。模型頁標籤表 `Name 1 model Size / Usage Context Input`，雲端那一列 `glm-5.3-flash:cloud - · 1M context window`；`/tags` 頁欄名相同、那一格寫 `Medium Usage` | 反例逐字成立；括號原寫「本篇讀的雲端標籤在這一欄寫「-」」沒說是哪一頁，**改**（第 2 處） |
| 阿里雲疑難排解表三組網址 | Claude Code 頁 `Requests return 401 invalid_api_key`：`Model Studio provides three access methods, and each access method uses a different base URL and a dedicated API key.`，表列 `https://dashscope.aliyuncs.com/apps/anthropic`、`https://coding.dashscope.aliyuncs.com/apps/anthropic`、`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；設定那一節是 `coding-intl`、`token-plan.ap-southeast-1` 與三個 `{WorkspaceId}` 網址 | 正文舉的 Pay-as-you-go 網址逐字對；只陳述兩處各怎麼寫，成立 |
| Coding Plan／wire_api／Codex 參考頁 | 阿里雲 Codex 頁 `Coding Plan only supports the Chat/Completions API. Install an older version of Codex, such as 0.80.0:`、`Coding Plan does not support the Responses API (Chat/Completions API only)`；FAQ `Newer versions of Codex no longer support wire_api = "chat".`、`Change wire_api to responses and verify that base_url is correct.`；Codex 參考頁 `` `responses` is the only supported value, and it is the default when omitted. `` | 三處都在，版本號 0.80.0 逐字，成立 |
| deepseek-r1 授權段落新補的句子 | `The Llama 8B distilled model is derived from Llama3.1-8B-Base and is originally licensed under llama3.1 license.`；Distilled models 下 `DeepSeek-R1-0528-Qwen3-8B` / `ollama run deepseek-r1:8b`，標籤表 `deepseek-r1:8b latest 5.2GB`；授權段落只提 Qwen-2.5 與兩個 Llama | 成立；「沒有提到 Qwen3」限定在授權段落 |
| `env_key`、`experimental_bearer_token` 原句 | Codex 參考頁 `Environment variable supplying the provider API key.`、`` Direct bearer token for the provider (discouraged; use `env_key`). `` | 逐字成立 |
| 閘道那一句 | gateway 頁 `ANTHROPIC_BASE_URL is the variable that points Claude Code at the gateway.` | 前半成立；後半「回答的是各家自己的模型」撐不住，**改**（第 1 處） |
| code 2 的揭露註解 | Z.ai 自動腳本 `The script will automatically modify ~/.claude/settings.json…`、手動設定也寫進 settings.json；阿里雲 `Create ~/.claude/settings.json`；DeepSeek 用 `export`（Windows 用 `$env:`）；三家都沒有指定金鑰變數名 | 成立 |
| DeepSeek toml 的 `forced_login_method` | DeepSeek Codex 頁範例逐字 `forced_login_method = "api"`；Codex 參考頁 `config.toml` 一節 `forced_login_method`，型別 `chatgpt \| api`，`Restrict Codex to a specific authentication method.` | 兩者都有，**保留**，註解改寫明出處（第 6 處）；配 `env_key` 行不行，文件沒寫，本篇沒寫 |
| Z.ai 頁首指向另一頁 | `To use the latest GLM-5.3 model, see How to Switch the Model in Use` | 正文只說頁首指向另一頁，沒有句子依賴那一頁的內容，不動 |
| `models-seen.json` 的 `DeepSeek-R1-0528-Qwen3-8B` | verbatim `DeepSeek-R1-0528-Qwen3-8B ollama run deepseek-r1:8b` | 在 deepseek-r1 頁去標籤後找得到，成立 |

其餘第一輪改寫的句子（「本篇讀的五個模型頁裡」的範圍、models.json 兩家都列完整內容、DeepSeek 一鍵腳本備份、Z.ai 兩種別名並列、
`/status` 一句、「標「本機」的標籤要由自己電腦上的 Ollama 執行才留在本機」、FAQ 1／2／4／5）逐句對回原文，都成立。

### 改掉的 7 處

1. **閘道段「回答的是各家自己的模型」（事實）。**
   原文：「下面三家的頁面用的也是 ANTHROPIC_BASE_URL，回答的是各家自己的模型。」→「…回答的是各家頁面設定的模型。」
   文件：阿里雲 Claude Code 頁 Token Plan 範例 `"ANTHROPIC_MODEL": "auto"`、`"CLAUDE_CODE_SUBAGENT_MODEL": "auto"`，頁面沒有寫 auto 是哪個模型；
   阿里雲 Codex 頁 Token Plan 的模型目錄除 Qwen 外列了 `glm-5.3`、`deepseek-v4-pro`（Team 另有 `kimi-k2.6`、`MiniMax-M2.5` 等）。
   為什麼：本篇的阿里雲函式就是 Token Plan 配 auto，「各家自己的模型」沒有頁面撐。
2. **callout 的欄位寫法（事實）。**
   原文：「標籤表 Size / Usage 欄是 GB 數字（本篇讀的雲端標籤在這一欄寫「-」）」→「標籤表 Size / Usage 欄是檔案大小（本篇讀的模型頁上，雲端標籤這一格寫「-」）」。
   文件：模型頁那一格是 `-`，`/tags` 頁同一格是 `Medium Usage`。為什麼：判斷法引用的是模型頁，限定到模型頁才對得上；
   「GB 數字」改成與第 1 節、FAQ 1、code 1 註解一致的「檔案大小」，規則不會把小於 1GB 的本機標籤排除。
3. **表格 GLM、DeepSeek 的 :cloud 欄（事實，範圍）。**
   原文：「雲端：glm-5.3-flash:cloud，只有這一個標籤；1M」→「雲端：glm-5.3-flash:cloud，該頁只有這一個標籤；1M；其他 GLM 檔案庫本篇沒讀」；DeepSeek 那一格同樣改。
   為什麼：這一欄是家族層級，本篇只讀了 glm-5.3-flash、deepseek-v4.1-flash 兩頁；照 Qwen 那一格「其他 Qwen 檔案庫本篇沒讀」的寫法限定，同組其他篇沿用這張表。
4. **「金鑰的寫法三家不同」→「金鑰有兩種寫法」。** Z.ai 與 DeepSeek 都用 `experimental_bearer_token`，只有阿里雲用 `env_key`。
5. **summary 第 4 句「各有一組模型別名對照」→「都寫了模型別名對照」。** Z.ai 頁有預設對照（`with the default configuration as follows`）與手動範例兩種寫法，正文也是並列兩種。
6. **DeepSeek toml 註解。** 「比 Z.ai 多的幾行照 DeepSeek 頁抄：forced_login_method 是…」→「比 Z.ai 多的幾行是 DeepSeek 頁面的範例寫法；頁面說明 forced_login_method 是…」。
   依協調者決定明寫出處；DeepSeek 欄位說明原文是 `preferred_auth_method , forced_login_method` 共用 `Authenticate with an API Key, skipping the ChatGPT account login`。行數不變（22 行），研究紀錄 `lines` 不用改。
7. **騰字與主詞。** 第 5 節第 1 段刪「檔案很長，本篇不重貼。」（兩份 toml 的註解都已寫「本篇不重貼」），下一句補主詞成「models.json 照兩家頁面原樣貼上」，免得讀成 config.toml。

試過但撤回：把授權段落改成頁面的拼法（`Qwen-2.5`、`llama3.1 license`）會讓檢查器把它們當模型 id 警告；原句「源自 Llama 3.1 與 Llama 3.3 授權的模型」是頁面意思的正確轉述，維持原樣。

### 抽查與表格重對

- **抽查**：第一輪 `checked_and_correct` 9 條全部重查（超過三分之一）：三家端點與值、DeepSeek 對照與範例、Claude Code 九個變數在 `env-vars.md` 都存在、Ollama 五頁的標籤／大小／上下文／能力列／Applications 區、託管句與 MIT Licensed、Anthropic 歸因、不實測規則、必連六篇 title 逐字相符且 `deepseek-local-with-ollama`（llama3.1／llama3.3、8b=Qwen3）與 `ollama-getting-started`（大小欄「-」）沒有矛盾、163 條引文。全部成立。
- **引文**：163 條 `verbatim_quote` 綁回自己的 url，HTML 標籤刪成空字串、實體還原、空白正規化：155 條在 HTML 找到，3 條 Z.ai Codex 與 2 條 llm-gateway 只在 `.md`，3 條 Z.ai Claude 在含 script 的去標籤全文與 `.md` 找到；**0 條找不到**。
- **表格 18 格重對**：

| 家族 | 本機標籤與大小 | :cloud | Claude Code | Codex | 授權 |
| --- | --- | --- | --- | --- | --- |
| Qwen | qwen3.5 0.8b 1.0GB、2b 2.7GB、4b 3.4GB、9b 6.6GB（latest）、27b 17GB、35b 24GB、122b 81GB；256K ✓ | 頁上沒有 ✓ | Token Plan 網址逐字 ✓ | `compatible-mode/v1`、responses；Coding Plan 只 Chat ✓ | 頁面沒寫 ✓ |
| GLM | glm-4.7-flash latest／q4_K_M 19GB、q8_0 32GB、bf16 60GB；198K ✓ | glm-5.3-flash:cloud，1M ✓（範圍改） | `api.z.ai/api/anthropic` ✓ | `api.z.ai/api/v1` ✓ | MIT Licensed／沒寫 ✓ |
| DeepSeek | deepseek-r1 1.5b 1.1GB、7b 4.7GB、8b 5.2GB（latest）、14b 9.0GB、32b 20GB、70b 43GB、671b 404GB；128K，671b 160K ✓ | deepseek-v4.1-flash:cloud，1M ✓（範圍改） | `api.deepseek.com/anthropic` ✓ | `api.deepseek.com/` ✓ | MIT、蒸餾版另有原授權／沒寫 ✓ |

### 程式範例

| 區塊 | 行數 | 檢查 | 識別字 |
| --- | --- | --- | --- |
| `ollama-launch-tags.sh` | 11 | `bash -n` ok | 五個 `ollama launch claude --model` 標籤逐字在各頁 Applications 區 |
| `use-endpoint.sh` | 45 | `bash -n` ok | 9 個變數、3 個端點、12 個值逐字在各自的供應商頁；金鑰都是 `$ZAI_API_KEY` 等環境變數，沒有佔位字 |
| `config.toml`（Z.ai） | 15 | `tomllib` ok | 8 個鍵；值對 Z.ai 頁，鍵都在 Codex 參考頁 `config.toml` 一節 |
| `config.toml`（DeepSeek） | 22 | `tomllib` ok | 11 個鍵（多 `forced_login_method`、`web_search`、`show_raw_agent_reasoning`）都在 Codex 參考頁；`preferred_auth_method` 在參考頁 `.md` 與 HTML 都搜不到，維持拿掉；沒有別的查不到的鍵 |

研究紀錄 `code_samples` 四條的 `label` 與 `lines` 與內容包一致。

### 界線

三種跑法每次出現都標得出是哪一種（表格兩格補了範圍）；沒有速度、品質、「跑得動」，沒有執行輸出；「本站沒有實測」只在第二段導言；title 與 description 沒有「實測」；
沒有價格數字、方案比較或訂閱建議；授權只用頁面上的字；「Anthropic 的文件寫不支援」在正文出現一次並歸因（summary 照正文重述），沒有寫成違反條款；否定句都限定在讀過的頁面。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
WARN - lint text_length: 7644 characters of body text; the guideline for life is 1500–6000
OK ai-workflow-agent-glm-qwen-deepseek paragraphs 2994 code_blocks 4 sources 13
```

段落字數 2,999 → 2,994。`text_length` 7,606 → 7,644：增加的是 callout 與表格兩格的範圍限定，屬不可刪的但書，壓不到 6,000。

### 懷疑但沒動

- 第 5 節「後貼的會蓋掉先貼的」是從 Z.ai 的 `Copy the following content entirely into ~/.codex/models.json` 與 DeepSeek「建立這個檔案、內容如下」推出來的，兩家頁面沒有逐字這樣寫；推論單純，沒改。
- 阿里雲 Codex 頁 FAQ 把 Model Studio 稱為 `the Model Studio gateway`，但沒有說它算不算 Anthropic 文件說的閘道，第 3 節「兩邊頁面都沒有寫」仍成立。

### 結論

`ok`。改了 7 處，事實 3 處（閘道段的「各家自己的模型」、callout 的欄位寫法、表格兩格的範圍），其餘是用詞、出處揭露與騰字。
第一輪改寫的句子除上述外逐句對得上今天的原文；`forced_login_method` 兩個條件都成立而保留；四個 code 區塊語法與識別字都成立，骨幹不變。
