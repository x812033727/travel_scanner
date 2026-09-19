# 獨立查核：ai-workflow-local-and-cloud-mix

查核代理：未參與撰稿。查核日 **2026-09-19**。
文章的 `checked_on` 是 **2026-09-18**，七條 source 與研究紀錄八處一致，
而且本輪**沒有依今天的頁面改掉任何一個數字**（逐列重抄，全部相同），依規格**不改這個日期**。

查核方式：`sources[]` 七條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
正文每一句、摘要五句、FAQ 七題答句、callout、表格 55 格、兩個 caption、
圖解四組節點、`hero_label`、title、description 逐條回原文比對；
三個 `code` 區塊抽出重跑 `python -m py_compile`，每一個匯入、函式、關鍵字參數、
端點與模型 id 對官方文件核對；研究紀錄每一條 `verbatim_quote` **綁回它自己的 `url`**、
以「HTML 標籤去掉」的連續字串比對。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**；
**沒有使用 `sources[]` 以外的網址替文章補任何事實**（為了反駁而讀的兩個官方頁見文末）。
沒有打任何需要金鑰的 API。

檢查的主張：**126 條**（正文 44 句／子句、摘要 5、FAQ 7、callout 6、表格 55 格、
caption 2、圖解 4 組節點、title／description／`hero_label`），
外加三個 code 區塊約 112 個不重複識別字與研究紀錄的引文。
**改了 14 條（22 個編輯點）**，其中一處動到骨幹論述；另有 4 件留給站主。

## 重抓結果：七條今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.ollama.com/api/openai-compatibility` | 200 | 499,325 | **是**。`<title>` 為「OpenAI compatibility - Ollama」；Direct cloud access、Local server usage、Endpoints、Supported request fields（8 處）、Responses API、Models 各節齊全 |
| `docs.ollama.com/api` | 200 | 252,306 | **是**。「Introduction - Ollama」；Base URLs 表三列、Ollama API example、Libraries、Versioning 都在 |
| `docs.ollama.com/cloud` | 200 | 277,581 | **是**。「Cloud - Ollama」；API Key、Ollama App or CLI、Models、Usage、Retirements、Data handling 六節齊全 |
| `docs.ollama.com/faq` | 200 | 485,466 | **是**。「FAQ - Ollama」；隱私、停用雲端、`binds 127.0.0.1` 三題都讀得到 |
| `ollama.com/library/gemma4` | 200 | 121,046 | **是**。50 個標籤的清單、讀我檔、Benchmark 與 Model information 兩張表都在 |
| `ollama.com/library/qwen3.6` | 200 | 84,737 | **是**。35 個標籤、讀我檔 Qwen3.6 Highlights 在 |
| `ollama.com/library/gpt-oss` | 200 | 88,805 | **是**。5 個標籤、讀我檔 MXFP4 一節（6 處命中）在 |

模型庫的標籤清單另外抓了 `/library/<name>/tags` 三頁做完整比對（gemma4 50 個、qwen3.6 35 個、gpt-oss 5 個），
只用來核對「這一頁上有沒有這個標籤」，沒有進 `sources[]`。

## 程式範例重驗

| # | label | 語言 | 行數 | `py_compile` | 比對過的簽名／參數／端點 |
| --- | --- | --- | --- | --- | --- |
| 1 | `hybrid_client.py` | python | 34 → **43** | **ok** | `OpenAI(base_url=…, api_key=…, timeout=…)`、`chat.completions.create(model=, messages=)`、`os.environ["OLLAMA_API_KEY"]`、`http://localhost:11434/v1`、`https://ollama.com/v1`、`gpt-oss:20b` |
| 2 | `redact_locally.py` | python | 24 | **ok** | `client.with_options(timeout=…)`、`response_format={"type": "json_object"}`、`qwen3.6:35b` |
| 3 | `finish_in_cloud.py` | python | 27 → **29** | **ok** | `client.with_options(timeout=…)`、`gemma4:31b`、`str.replace`、`dict[str, str]` |

比對的文件：
`https://docs.ollama.com/api/openai-compatibility`（本機／雲端範例、Supported request fields）、
`https://docs.ollama.com/api`（Base URLs 表）、
`https://docs.ollama.com/cloud`（雲端模型命名）、
`https://raw.githubusercontent.com/openai/openai-python/main/README.md`（openai 套件官方讀我檔，HTTP 200、41,584 bytes）。

三塊都沒有字面金鑰、沒有 `<YOUR_KEY>`、沒有 `eval`、沒有刪檔命令，金鑰只從環境變數讀。

## 改掉的 14 條

### 協調者點名的七項

1. **骨幹更正：「呼叫本機端點」不等於「資料留在本機」（最重的一處）。**
   草稿第一節第二段寫「只要本機那一步真的呼叫的是本機端點，資料在離開這台機器之前，
   官方講的隱私承諾都還沒輪到要不要相信的問題——**資料根本沒有送出去**」，
   callout 的第一個「保險做法」也寫「去識別化那支函式**固定寫死** `base_url="http://localhost:11434/v1"`，不讓變數決定」。
   但同一份 `sources[0]` 的 Models 一節原文是：
   「`Direct cloud requests use the identifiers from https://ollama.com/api/tags and do not require a pull.
   Through a signed-in local server, select a cloud model such as gemma4:cloud.`」
   `sources[1]` 的 Base URLs 段落也寫「`To use cloud models through your local server, sign in to Ollama.`」
   ——**已登入的本機伺服器一樣送得出雲端請求**，網址釘死在 localhost 並不保證資料不出機。
   已把第一節第二段、callout、FAQ 第 2 與第 4 題、摘要第 4 句全部改成
   「網址指到本機」**與**「模型用已經下載下來的本機標籤」兩件事都要成立，
   並在 `must_not_write` 加一條擋住翻譯階段寫回去。
2. **callout 整段重寫。** 原本的補救辦法被同一份官方文件推翻（見第 1 條），
   標題也從「去識別化那一步選到 cloud 標籤，等於沒做」改成「去識別化那一步，網址和標籤要一起釘死」。
   另外，停用雲端功能的**設定方式**是必連文章「Ollama 入門」已經寫完的東西
   （那篇的 callout 就寫著 `disable_ollama_cloud` 與 `OLLAMA_NO_CLOUD=1`），
   本篇改成一句帶過並指名那一篇，不重複設定步驟。
3. **`-cloud 後綴` 這個說法不成立。** 草稿寫「只有在 Ollama 的 App 或 CLI 裡**才需要加上 -cloud 後綴**，
   例如 `gemma4:cloud`」——同一句自己就矛盾：`gemma4:cloud` 的 cloud 接在**冒號**後面。
   `sources[2]` 原文是「`For API requests to ollama.com, use the name returned by this list, such as gemma4:31b.
   In the Ollama app or CLI, use gemma4:cloud. Cloud models do not need to be downloaded.`」
   而且「只有在 App 或 CLI」漏掉 `sources[0]` 寫的第三種情況（已登入的本機伺服器）。
   已照原文改寫三種情況並列，並說明 `gemma4:31b-cloud`、`gpt-oss:20b-cloud` 那種是標籤清單上另外的寫法。
4. **`gpt-oss:120b` 不該當雲端範例的模型名稱。** `sources[]` 七頁沒有任何一頁把 `gpt-oss:120b`
   寫成 ollama.com 的雲端模型名稱；官方**兩頁**的直接雲端存取範例寫的都是 `gemma4:31b`
   （`sources[0]` 的 `model="gemma4:31b"`、`sources[2]` 的 curl 範例）。
   第三個 code 區塊的預設模型已改成 `gemma4:31b`，正文同步。
   （為了反駁另外讀了 `https://ollama.com/api/tags`：今天回 20 個名字，`gpt-oss:120b` 與 `gpt-oss:20b`
   **確實在裡面**，所以草稿的寫法不是錯的，是 `sources[]` 撐不住；那個網址不在 `sources[]`，
   依規格不拿它替文章補事實。要寫回去就得先把它加進 `sources[]`——留給站主。）
5. **`timeout` 傳錯位置。** 三塊程式原本都寫 `client.chat.completions.create(..., timeout=30)`。
   openai 套件的官方讀我檔 Timeouts 一節只記載兩種寫法：
   「`# Configure the default for all requests: client = OpenAI(timeout=20.0,)`」與
   「`# Override per-request: client.with_options(timeout=5.0).chat.completions.create(...)`」。
   已改成 `OpenAI(..., timeout=30.0)` 設全域預設、`client.with_options(timeout=60.0).chat.completions.create(...)`
   做單次覆寫，`create()` 不再吃 `timeout` 關鍵字；正文加一句說明，`must_not_write` 加一條。
6. **`base_url` 字面：兩種寫法都在官方頁上，文章沒有錯。**
   `sources[0]` 的本機範例**全部 11 處**寫 `http://localhost:11434/v1/`（**帶**結尾斜線），
   雲端那支寫 `base_url="https://ollama.com/v1"`（**不帶**）；
   `sources[1]` 的 Base URLs 表則是 `http://localhost:11434/v1` 與 `https://ollama.com/v1`（都不帶）。
   文章用的是 Base URLs 表那一種，**維持不動**；研究紀錄第 1 條原本只寫帶斜線那種，已補齊兩種並加一條 Base URLs 表的事實。
   `api_key='ollama'` 是官方本機範例自己寫的必填佔位（原文註解 `# required but ignored`），不是真金鑰，維持不動。
7. **`gemma4:26b` 的 MoE 寫法今天仍然成立，但「只有」是草稿加的。**
   讀我檔原文是「`26B (Mixture of Experts model with 4B active parameters)`」，
   沒有「只有」；而且同一頁下方的 Model information 表把 Active Parameters 寫成 **3.8B**，
   官方自己在同一頁有兩個數字。這一格的說明已經拿掉（理由見第 8 條），數字爭議一併消失。

### 與必連文章的分工

8. **表格第五欄與必連的「Ollama 入門」幾乎逐字重複。**
   那篇（`ollama-getting-started`，本篇結尾第二個連結指向它）的清單原文是：
   「gemma4:e2b：7.2GB、128K……官網說 E 代表有效參數，給邊緣裝置」「gemma4:26b：19GB、256K，官網註明是 4B 活躍參數的混合專家模型」
   「gemma4:31b：20GB、256K，是密集模型」「gemma4:cloud 與 gemma4:31b-cloud：大小欄是「-」，不用下載」——
   本篇的「官方頁重點」欄寫的是同一組話。依指派「不得整段重講」，
   該欄已換成本篇自己要回答的問題：**「跑在哪裡」**（本機／Ollama 的雲端）。
   數字本身（7.2GB、9.6GB、7.6GB、19GB、20GB、18GB、23GB、14GB、65GB、各列的上下文視窗）
   今天逐列重抄，全部相同，維持不動。
9. **FAQ 第 6 題整題換掉。** 原題「本機的 Ollama 端點，預設誰連得到？」的答案
   「同一個區網的其他機器**都連不到**」超出原文 `Ollama binds 127.0.0.1 port 11434 by default.` 的範圍
   （那一題的標題是 `How can I expose Ollama on my network?`，頁面沒有寫這個全稱否定），
   內容又和「Ollama 入門」的段落重複。已換成本篇自己的題目
   「怎麼確認本機那一步真的沒有把資料送出去？」。
   正文第一節第二段同一句的「等於連同一個區網的其他機器都連不到」也一併收斂成原文的說法。
10. **正文點名的系列文章標題寫錯。** 草稿寫「一件事拆給多個模型：**四種切法**」，
    但 `ai-workflow-split-tasks-across-models` 的 zh-TW title 是
    「一件事拆給多個模型：**依步驟、能力、風險、資料敏感度**四種切法」。已照抄改正。
    （另外兩個點名的標題「統一 API 層：OpenRouter 與 LiteLLM 換模型不改程式」與
    「模型之間交接資料：JSON Schema 與結構化輸出」逐字無誤。）

### 其餘四條

11. **qwen3.6 的全稱否定。** 草稿寫「qwen3.6 目前的模型庫頁沒有列出帶 cloud 字樣的標籤，
    **等於它只能在本機跑，沒有 Ollama 自己雲端的版本**」。
    查證：今天把 `/library/qwen3.6/tags` 的 35 個標籤全數列出，`cloud` 在整份 HTML **0 次**，
    所以「這一頁沒有列」成立，但「沒有雲端版本」是官方沒說過的推論。
    已改成「qwen3.6 那一頁在本文查證當天沒有列出任何帶 cloud 字樣的標籤——
    這是當天那一頁的狀態，不是官方宣告過它不會有雲端版本」。
    順帶：草稿原本要拿「能力列只有 vision、tools、thinking」佐證，但那一排字在頁面上是**各自獨立的元素**，
    沒有可逐字搜尋到的連續字串，已改引讀我檔的「Ollama’s cloud」一節與標籤清單的「-」大小欄。
12. **「無論用哪一種呼叫方式都是 11434 埠」與「三種呼叫方式」都不對。**
    三頁上方實際是 **CLI／cURL／Python／JavaScript 四個**分頁；
    而且只有 cURL 那個分頁印出 `http://localhost:11434/api/chat`，CLI 分頁只印 `ollama run gemma4`，
    頁面沒有寫「每一種都走 11434 埠」，帶 cloud 的標籤更不成立。已照頁面改寫。
13. **界線：把「不會」改成描述，並補上遮蔽會漏的但書。**
    FAQ 第 2 題原本以「**不會**」開頭保證雲端看不到姓名電話。
    全篇沒有法規、合規或個資法字樣（`個資法`／`法規`／`合規`／`GDPR`／`符合` 各 **0** 次，本輪也沒有加），
    但「不會」是對一段由模型執行的遮蔽下保證。已改成描述這套流程送出去的是什麼，
    加上前提（網址與標籤都要對）與但書（遮蔽由模型判斷，要自己拿真實樣本驗過），第四節第一段同步。
14. **五個小修。**
    摘要第 2 句「本機預設**只**綁定 127.0.0.1」→「預設綁定」；
    表格與摘要第 3 句的「**官方**寫最低 16GB」→「**讀我檔**寫量化後最低 16GB」（那是 gpt-oss 讀我檔，不是泛稱的官方頁），
    第三節第二段照原文改成 `as little as 16GB memory`／`fit on a single 80GB GPU` 的直譯；
    「差的只有 OpenAI() 建構子**那三行**：base_url、api_key、**model**」——`model` 不是建構子參數，
    已改成「建構子裡的 base_url 與 api_key，以及呼叫時填的 model」（FAQ 第 1 題同步）；
    最後一節刪掉第二次重述的 14GB／16GB／65GB／80GB，以及
    「買一張 80GB 顯示卡不是每個開發者的選項，Ollama 自己的雲端剛好補上這一段」這句帶推薦語氣的話；
    表格 caption 補上新增的「執行的位置」欄。段落字數 2,515 → **2,913**。

## 研究紀錄的修正

- **三條 `verbatim_quote` 是拼裝品。** 第 11、13、14 條寫成
  `gemma4:e2b 7.2GB · 128K context window · Text, Image · 5 months ago` 這種「標籤名＋規格」的字串，
  但模型庫的每一列把標籤名和規格放在**兩個不同的元素**裡，這個字串在頁面上搜尋不到。
  已改成頁面上真的連續的那一段（`7.2GB · 128K context window · Text, Image · 5 months ago`），
  標籤名寫進 `fact` 欄並註明原因。
- **`verified_facts` 從 16 條擴到 31 條**：表格每一列的大小與上下文視窗、兩組 cloud 標籤、
  Base URLs 表、`response_format`、直接雲端存取範例的 `model="gemma4:31b"`、
  以及第 1 條那兩句關鍵限制，都各自補上自己的連續引文。
  改完重跑，**31 條全部通過「綁回自己的 `url`」的連續字串比對**。
- `code_samples` 的 `lines` 更新為 43／24／29，`compiled_on` 改成 2026-09-19，
  `checked_against` 加上 openai 套件讀我檔。
- `must_not_write` 新增 5 條（base_url 迷思、`-cloud 後綴`、qwen3.6 全稱否定、合規保證、`timeout` 位置），
  `unverified_or_excluded` 新增 3 條（`ollama.com/api/tags`、能力標籤列、Ollama 雲端價格）。
- 新增 `factcheck` 欄位。

## 查過而且正確的部分（沒有動）

- **`sources[0]` 的四段程式原文逐字吻合**：
  `These examples connect to your local Ollama server. The client requires an API key value, but Ollama ignores it.`、
  `api_key='ollama',  # required but ignored`、`base_url="https://ollama.com/v1"`、`model="gemma4:31b"`。
- **`response_format` 確實列在 `/v1/chat/completions` 的 Supported request fields**（全頁只出現這一次），
  `JSON mode` 也列在 Supported features；值的寫法 `{"type": "json_object"}` 在 Ollama 頁上沒有印出來，
  openai 套件讀我檔的 Nested params 一節印的是 `text={"format": {"type": "json_object"}}`，
  兩者合起來足以支撐這個寫法——正文只說「支援 response_format 這個欄位」，沒有超寫。
- **常見問答三句原文今天逐字相符**：
  `Ollama runs locally. We don’t see your prompts or data when you run locally.`（`don’t` 是 U+2019）、
  `Ollama binds 127.0.0.1 port 11434 by default. Change the bind address with the OLLAMA_HOST environment variable.`、
  `Ollama can run in local only mode by disabling Ollama’s cloud features.`
- **雲端頁的退場與資料處理**：
  `Usage settings show upcoming retirements for models you’ve recently used. Switch models before the retirement date.
  Downloaded local models are not affected.` 與
  `Ollama processes cloud prompts and responses to answer your requests. We do not use them to train models.`
- **gpt-oss 讀我檔的硬體門檻**：
  `enables the smaller model to run on systems with as little as 16GB memory, and the larger model to fit on a single 80GB GPU`
  與 `gpt-oss-20b model is designed for lower latency, local, or specialized use-cases.` 今天原文未變，
  MXFP4 這個前提條件文章有寫，沒有被刪。
- **標籤與規格逐列重抄全部相同**：gemma4 `e2b 7.2GB/128K`、`e4b(latest) 9.6GB/128K`、`12b 7.6GB/256K`、
  `26b 19GB/256K`、`31b 20GB/256K`、`cloud` 與 `31b-cloud` 大小欄 `-`/256K；
  qwen3.6 `27b 18GB/256K`、`35b(latest) 23GB/256K`；
  gpt-oss `20b(latest) 14GB/128K`、`120b 65GB/128K`、`20b-cloud` 與 `120b-cloud` 大小欄 `-`/128K。
- **界線重掃全部通過**：沒有購買、訂閱或投資建議，沒有推薦式比價，全篇沒有價格數字；
  廠商宣稱全部帶歸屬（「官方文件寫」「讀我檔寫」「雲端頁寫」）；
  沒有把預告寫成已推出（沒有 beta／preview 相關內容）；沒有寫「台灣可用」；
  只有**一個** `warning` callout、**沒有**免責段落；「本站沒有實測」在正文、摘要、FAQ 共 4 處；
  沒有驚嘆號、沒有簡體字（檢查器已驗）。
- **摘要五句仍 ⊆ 正文**，圖解四格與 `hero_label` 未動，`diagram.caption` 與內容包一致。
- **`checked_on` 2026-09-18** 在七條 source 與研究紀錄一致，未更動。

## 留給站主的事

1. **本機 `base_url` 的兩種寫法要不要統一。** 本篇用 `http://localhost:11434/v1`（Base URLs 表），
   既有的「Ollama 入門」用 `http://localhost:11434/v1/`（OpenAI 相容性頁範例，那一頁 11 處都帶斜線）。
   兩種都是官方頁上的字，本輪不動；兩篇並排時讀者會注意到。
2. **與「Ollama 入門」的分工還沒完全乾淨。** 本輪換掉了重複最重的表格第五欄與 FAQ 第 6 題，
   但 gemma4 那五列的**數字**仍與那篇相同（數字只有一種寫法）。
   若站主想更乾淨，可以把 gemma4 的本機列縮成一句話，整段指向那篇。
3. **雲端收尾要不要寫回 `gpt-oss:120b`。** 本輪改成官方範例寫的 `gemma4:31b`。
   查核當天讀 `https://ollama.com/api/tags` 確實看得到 `gpt-oss:120b` 與 `gpt-oss:20b`，
   要寫回去就得先把那個網址加進 `sources[]`（目前 7 條，上限 8 條）。
4. **`openai` 套件沒有裝在本 repo 的 venv 裡**，所以 `with_options()` 與 `OpenAI(timeout=…)`
   只對官方讀我檔核對過簽名，沒有實際執行；`response_format={"type": "json_object"}` 同理。

## `models-seen.json`

新增 **4 筆**（只新增，沒有動別人的條目）：`gemma4:cloud`、`gemma4:31b-cloud`、
`gpt-oss:20b-cloud`、`gpt-oss:120b-cloud`，各自帶今天在模型庫頁讀到的連續引文、
url 與 `checked_on: 2026-09-19`。原本清單只有 `gemma4`／`qwen3.6`／`gpt-oss` 三個基底 id，
而這篇的正文與 callout 逐字寫出這四個雲端標籤。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-local-and-cloud-mix paragraphs 2913 code_blocks 3 sources 7
```

`OK`，沒有 FAIL。`raw_internal_url` 這個 WARN 是預期的（結尾兩個純 link 由協調者 `relink`）。
段落字數 **2,913**（1,800–3,000），title 39 字，description 175 字，code 區塊 3 塊（43／24／29 行）。

## 結論

`needs_second_round`。改了 14 條、22 個編輯點，其中**第 1 條動到骨幹論述**
（「呼叫本機端點就等於資料不出機」被同一份官方文件推翻，第一節第二段、callout、
FAQ 第 2 與第 4 題、摘要第 4 句全部重寫），第 2 條整段重寫了唯一的 callout，
第 4、5 條換掉了程式範例的模型名稱與 `timeout` 寫法。文章現在可刊，但依規格該再走一輪。

第二輪只需要逐句回來源查**本輪新寫進去的每一句**：
第一節第二段後半、第二節第一段與第二段、第三節第一段與第二段後半、
第四節第一段末與第三段、callout 全段、表格第五欄十一格、
FAQ 第 1、2、4、6 題、摘要第 1 與第 4 句、導言第一段末句，
以及三個 code 區塊改動過的行（`LOCAL_MODELS`、兩處 `with_options`、`OpenAI(timeout=…)`、`gemma4:31b`）。
