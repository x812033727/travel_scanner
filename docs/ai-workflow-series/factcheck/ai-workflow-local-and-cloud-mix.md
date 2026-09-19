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

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-19**（與第一輪同一天）。
文章的 `checked_on` 仍是 **2026-09-18**：本輪同樣**沒有依今天的頁面改掉任何一個數字**
（七頁逐列重抄，全部與第一輪相同），依規格**不改這個日期**。

範圍：只覆核第一輪改動過的每一段與新寫進去的每一句（第一輪報告結尾那份清單），
加上研究紀錄 31 條 `verbatim_quote`、三個 code 區塊、界線七項與兄弟篇標題。
**檢查了約 95 條主張，改了 11 處**（內容包 10 處、程式 2 塊；研究紀錄另外 6 處）。
沒有打任何需要金鑰的 API，沒有用 `sources[]` 以外的網址替文章補事實，
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**。

### 重抓結果：七條今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.ollama.com/api/openai-compatibility` | 200 | 499,325 | **是**（`<title>` OpenAI compatibility - Ollama；Direct cloud access／Local server usage／Endpoints／Supported request fields／Models 齊全） |
| `docs.ollama.com/api` | 200 | 252,306 | **是**（Introduction - Ollama；Base URLs 表三列、Ollama API example 都在） |
| `docs.ollama.com/cloud` | 200 | 277,581 | **是**（Cloud - Ollama；API Key／Models／Retirements／Data handling 六節齊全） |
| `docs.ollama.com/faq` | 200 | 485,466 | **是**（FAQ - Ollama；三題隱私／綁定／停用雲端都讀得到） |
| `ollama.com/library/gemma4` | 200 | 121,046 | **是**（50 個標籤、讀我檔、兩張表都在） |
| `ollama.com/library/qwen3.6` | 200 | 84,737 | **是**（35 個標籤、讀我檔在；全份 HTML `cloud` **0 次**） |
| `ollama.com/library/gpt-oss` | 200 | 88,805 | **是**（5 個標籤、MXFP4 一節在） |

bytes 與第一輪完全相同，沒有一頁是 JS 空殼。

### 研究紀錄的 `verbatim_quote`：程式比對，31 條全過

用腳本把每條引文**綁回它自己的 `url`**，對「HTML 標籤去掉」的正文做連續字串比對
（同時試原樣與空白收斂兩種）：**第一輪的 31 條今天全部命中，一條都不用換**。
本輪另外**新增 3 條**（gemma4:31b-cloud 那一列、讀我檔「Ollama’s cloud」一節、模型庫頁四個分頁），
重跑後 **34 條全過**。

### 程式範例重驗

| # | label | `py_compile` | 行數 | 本輪比對／改動 |
| --- | --- | --- | --- | --- |
| 1 | `hybrid_client.py` | **ok** | 43 → **49** | 新增 `ensure_local_tag()`；`OpenAI(base_url=, api_key=, timeout=30.0)`、`chat.completions.create(model=, messages=)`、`os.environ["OLLAMA_API_KEY"]` 逐字對讀我檔與 Ollama 兩頁 |
| 2 | `redact_locally.py` | **ok** | 24 → **25** | 補上 `ensure_local_tag(model)`；`client.with_options(timeout=60.0)`、`response_format={"type": "json_object"}` |
| 3 | `finish_in_cloud.py` | **ok** | 29 | 未動；`with_options(timeout=60.0)`、`gemma4:31b`、`str.replace`、`dict[str, str]` |

- `OpenAI(timeout=…)` 與 `client.with_options(timeout=…).chat.completions.create(…)` 兩種寫法，
  今天重讀 `https://raw.githubusercontent.com/openai/openai-python/main/README.md`（200、41,584 bytes）
  的 Timeouts 一節，原文仍是
  「`# Configure the default for all requests: client = OpenAI(timeout=20.0,)`」與
  「`# Override per-request: client.with_options(timeout=5.0).chat.completions.create(...)`」——**文章寫對了**。
  `create()` 沒有 `timeout` 關鍵字這件事也仍然成立。
- `response_format` 這個關鍵字本輪另外拉了套件原始碼核簽名
  （`openai-python/src/openai/resources/chat/completions/completions.py`，200、182,333 bytes）：
  `response_format: completion_create_params.ResponseFormat | Omit = omit`，
  文件字串寫「Setting to `{ "type": "json_object" }` enables the older JSON mode」——拼法與值的形狀都對。
- `base_url` 兩種字面、`api_key='ollama'`（`# required but ignored`）今天原文未變，維持不動。
- 三塊都沒有字面金鑰、沒有 `<YOUR_KEY>`、沒有 `eval`、沒有刪檔命令；
  雲端金鑰只從 `os.environ["OLLAMA_API_KEY"]` 讀。
- **白名單邏輯離線實跑**（用假的 `OpenAI` 用戶端，沒有連網）：
  `gemma4:cloud`、`gemma4:31b-cloud`、`gpt-oss:20b-cloud` 在 `ask("local", …)` 與
  `redact_locally(model=…)` 兩處都擋下來，錯誤訊息 `… is not a downloaded local tag`；
  `get_client("local")` 回 `http://localhost:11434/v1` / `'ollama'` / `30.0`，
  `get_client("cloud")` 回 `https://ollama.com/v1` / 環境變數金鑰 / `30.0`。

### 改掉的 11 處

1. **骨幹的反向錯誤（最重的一處）。** 第三節第一段第一輪改寫後寫成
   「要判斷一個標籤到底在自己機器上跑還是送到 Ollama 的雲端，**看的是下面這張表最後一欄**，不是呼叫方式」——
   把「標籤」單獨當成判準，正好是第一輪骨幹修正的**反面**，而且和本篇自己的程式打架
   （第三塊 code 把**不帶 cloud** 的 `gemma4:31b` 當雲端模型送到 `https://ollama.com/v1`）。
   `sources[2]` 的 Models 一節原文是
   「`For API requests to ollama.com, use the name returned by this list, such as gemma4:31b.`」
   ——不帶 cloud 的名稱送到 ollama.com 一樣跑在雲端。
   已改成「看的**不是呼叫方式，而是網址加標籤**：這張表最後一欄只管標籤這一半，
   雲端頁寫對 ollama.com 送請求用的正是 gemma4:31b 這種不帶 cloud 的名稱」。
2. **第二節的 h2 標題也還停在舊骨幹上。** 「同一支 Python：**base_url 決定資料去哪裡**」
   與第一輪的結論（base_url 一件事決定不了）矛盾，已改成「**base_url 和標籤**決定資料去哪裡」。
3. **表格 `gemma4:31b` 那一格自相矛盾。** 欄名是「跑在哪裡」，格子卻寫
   「**本機**；也是官方直接雲端存取範例寫的模型名稱」。依 `sources[2]` 上面那句原文，
   已改成「下載後在本機；雲端頁寫對 ollama.com 送 API 請求也用這個名稱，那一種就跑在雲端」。
4. **表格 cloud 那一格超出原文。** 原本寫兩個標籤都「讀我檔列在「Ollama’s cloud」底下」，
   但 `sources[4]` 讀我檔那一節底下只有一行 `ollama run gemma4:31b-cloud`，
   `gemma4:cloud` 只出現在上面的標籤清單。已改成
   「讀我檔的「Ollama’s cloud」一節寫 ollama run gemma4:31b-cloud」。
5. **程式：白名單擋不到真正碰個資的那支函式。** 第一輪新增的 `LOCAL_MODELS` 檢查只寫在 `ask()` 裡，
   但 `redact_locally()` 自己收一個 `model` 參數、直接呼叫 `get_client("local")`，**完全繞過檢查**——
   與正文和 callout 講的「去識別化那支函式要同時釘死網址與標籤」不一致。
   已把檢查抽成 `ensure_local_tag()`，`ask()` 與 `redact_locally()` 進本機那一步之前都跑一次；
   第二塊的 `label` 同步改成「延續 hybrid_client.py 的 get_client 與 ensure_local_tag」，
   第四節第二段與第三段的敘述一併改。行數 43→49、24→25，三塊 `py_compile` 全過。
6. **導言末句與第二節、FAQ 第一題打架。** 導言寫「程式上本機與雲端**只差 base_url 那一行**」，
   但第一輪已經把第二節與 FAQ 第一題改成「差別只有兩處：`base_url`、`api_key` 與 `model`」，
   程式本身也是換三個值。已改成「差的只有 base_url、api_key 和 model」。
7. **Base URLs 表的歸屬放錯頁。** 正文第二節第一段與摘要第二句都寫成「**OpenAI 相容端點**文件」的表，
   但那張表在 `sources[1]`（`docs.ollama.com/api`，API 介紹頁），
   「OpenAI compatibility」只是表裡的一列；`sources[0]` 那一頁沒有這張表。
   兩處都改成「Ollama 的 **API 文件**……同一張 **Base URLs 表**裡，OpenAI 相容那一列」。
8. **兩處否定句超出「本文引用的這幾頁」。** 第五節第一段「**沒有一頁**公開本機和雲端實際回覆要等多久」
   與 FAQ 第五題「因為**沒有一份官方頁**公開這個數字」是對所有官方頁的全稱否定，
   我們只讀了七頁。兩處都改成「**本文引用的官方頁**沒有公開……」。
9. **一個沒有來源的最高級。** 第四節第一段「這裡示範**最常見**的敏感步驟」改成「一個**典型**的敏感步驟」。
10. **研究紀錄：一條引文的涵蓋範圍寫寬了。** 第 21 條說「gemma4:cloud 與 gemma4:31b-cloud 那兩列」，
    但引文 `- · 256K context window · Text, Image · 2 months ago` 只是 gemma4:cloud 那一列
    （31b-cloud 那一列是 `5 months ago`）。已把 `fact` 寫精確，並補上 31b-cloud 那一列自己的引文。
    另補兩條（「Ollama’s cloud」一節、模型庫頁的四個分頁），`must_not_write` 新增兩條
    （反向的單一條件、只在 `ask` 擋標籤）。
11. **字數。** 為了容納上面的修正，刪掉兩句**同段已經講過**的贅述——
    第四節第一段的「這樣走一趟，送出去的就只有代號版本的文字」與
    第五節第一段的「能確定的只有上面那張表裡的規格數字」。
    **沒有刪掉任何但書、限定詞或歸屬**（本輪反而補回兩個限定詞，見第 8 條）。
    段落字數 2,913 → **2,955**。

### 查過而且正確、本輪沒有動的部分

- **第一輪的骨幹修正站得住。** `sources[0]`「`Through a signed-in local server, select a cloud model such as gemma4:cloud.`」
  與 `sources[1]`「`To use cloud models through your local server, sign in to Ollama.`」今天逐字未變，
  第一節第二段、callout、FAQ 第 2／第 4 題、摘要第 4 句的新寫法全部撐得住。
- **callout 全段重驗通過**：大小欄「-」、`Cloud models do not need to be downloaded.`、
  已登入本機伺服器選 `gemma4:cloud`、`Ollama can run in local only mode by disabling Ollama’s cloud features.`
  四項都有原文，停用雲端的**設定方式**確實只用一句帶過並指向「Ollama 入門」，沒有重講。
- **雲端範例模型 `gemma4:31b` 正確。** `ollama.com/library/gemma4` 的標籤清單上有
  `gemma4:31b 20GB · 256K context window · Text, Image`（全頁 1 次），
  `sources[0]` 的 Direct cloud access 範例寫 `model="gemma4:31b"`，
  `sources[2]` 的 Models 一節也寫 `such as gemma4:31b`——**「31b 這個標籤存在」與「官方拿它當雲端範例」兩件事都有原文**。
- **`:cloud` 跑在 Ollama 雲端、不帶 cloud 的標籤跑本機**：前半有原文（`sources[0]` 稱 `gemma4:cloud` 為 cloud model、
  `sources[2]` 寫 App/CLI 用 `gemma4:cloud`、雲端模型不用下載）；
  **後半只在「已下載的標籤在本機跑」這個範圍內成立**，不能反過來當成單一判準（見改動第 1、3 條）。
- **「三頁四個分頁」今天逐頁確認**：gemma4／qwen3.6／gpt-oss 上方都是 `CLI cURL Python JavaScript`，
  cURL 分頁印的都是 `curl http://localhost:11434/api/chat`。
- **qwen3.6 的限縮寫法仍然正確**：今天整份 HTML 搜尋 `cloud` **0 次**，
  文章寫的是「查證當天那一頁沒有列出」，不是「沒有雲端版本」。
- **標籤與規格逐列重抄全部相同**（7.2GB／9.6GB／7.6GB／19GB／20GB／18GB／23GB／14GB／65GB 與各列上下文視窗），
  `26B (Mixture of Experts model with 4B active parameters)`、MXFP4 的 16GB／80GB、
  `lower latency, local, or specialized use-cases.`、退場與資料處理兩段、常見問答三句，今天原文全部未變。
- **界線重掃全部通過**：全篇 `個資法`／`法規`／`合規`／`GDPR` 各 **0** 次；沒有購買、訂閱或投資建議；
  沒有推薦式比價、沒有價格數字；廠商宣稱全部帶歸屬（官方／讀我檔／雲端頁／常見問答）；
  沒有 beta／預覽被寫成已推出；沒有「台灣可用」；只有**一個** `warning` callout、**沒有**免責段落；
  沒有驚嘆號、沒有簡體字（檢查器已驗）。「本站沒有實測」在正文、摘要、FAQ 共 4 處。
- **`summary` ⊆ 正文、FAQ 答案 ⊆ 正文、表格每一格與圖解四格的數字**都在正文或表格裡（檢查器的 summary／diagram 數字規則通過）；
  `diagram.caption` 與內容包一致，`hero_label` 未動。
- **結尾兩個 link 逐字正確**：第一個 `多模型 AI 工作流教學：從拆任務到串接不同模型` → hub；
  第二個 → `ollama-getting-started`，text 逐字等於那篇的 zh-TW title
  `Ollama 入門：Windows、Mac 安裝與第一個模型`。
- **正文點名的六個站內標題今天逐字比對全部相同**：
  `一件事拆給多個模型：依步驟、能力、風險、資料敏感度四種切法`、
  `統一 API 層：OpenRouter 與 LiteLLM 換模型不改程式`、
  `模型之間交接資料：JSON Schema 與結構化輸出`（`ai-workflow-structured-handoff`）、
  `Ollama 入門：Windows、Mac 安裝與第一個模型`、
  `本機 vs 雲端 AI 成本試算：訂閱、API 與電費怎麼算`、`本機 RAG：跟自己的文件聊天`。
  協調者另外點名的 `失敗案例與防護：迴圈、費用爆炸與代理間注入` 與
  `一個 MCP 伺服器，同時接上 Claude Code、Codex、Gemini CLI 三個客戶端` 本篇沒有點名，不需要處理。
- **與三篇必連文的分工**：本篇沒有與它們矛盾的句子；第一輪換掉表格第五欄與 FAQ 第六題之後，
  剩下的重複只有 gemma4 五列的**數字**（數字只有一種寫法）與「11434 埠預設綁定」一句，
  兩者都是一句帶過，沒有整段重講；安裝、成本試算、RAG 三個主題各一句並指名文章。
- **`models-seen.json`**：本輪**沒有新增也沒有修改**（清單目前 31 筆，其他代理另外加過 2 筆）。
  第一輪新增的四筆今天重驗，`gemma4:cloud`、`gemma4:31b-cloud`、`gpt-oss:20b-cloud`、`gpt-oss:120b-cloud`
  的 verbatim 在各自的模型庫頁上都搜尋得到；本輪沒有引入任何清單外的模型 id。

### 留給站主的事

1. **第一輪那四件事本輪都沒有改變**：`base_url` 帶不帶結尾斜線、與「Ollama 入門」重複的 gemma4 數字、
   雲端收尾要不要寫回 `gpt-oss:120b`（要寫回就得先把 `https://ollama.com/api/tags` 加進 `sources[]`）、
   `openai` 套件沒裝在本 repo 的 venv 裡（`with_options` 與 `OpenAI(timeout=…)` 只核對簽名、沒有實跑真請求）。
2. **必連文章「Ollama 入門」有一句看起來過時了。** 那篇寫「相容到什麼程度官方逐項列了：……**不支援 `tool_choice`**」，
   但 `https://docs.ollama.com/api/openai-compatibility` 今天的 `/v1/chat/completions`
   「Supported request fields」清單裡**有 `tool_choice`**。本篇沒有提 `tool_choice`，所以不構成矛盾，
   本輪也不能動那個檔；建議站主替那一篇排一次重查。
3. **表格「跑在哪裡」這一欄的語意**本輪只修到與來源一致（標籤這一半），
   若站主覺得欄名仍容易被讀成單一判準，可以把欄名改成「標籤這一半：本機還是雲端」。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-local-and-cloud-mix paragraphs 2955 code_blocks 3 sources 7
```

`OK`，沒有 FAIL。`raw_internal_url` 這個 WARN 是預期的。
段落字數 **2,955**（1,800–3,000），code 區塊 3 塊（49／25／29 行），sources 7 條。

### 第二輪結論

`ok`。改的 11 處裡有 4 處（第 1、2、3、5 條）是第一輪骨幹修正**沒有改乾淨的殘留**：
正文、h2 標題與表格仍把「標籤」當成單一判準，而白名單也還沒擋到真正碰個資的那支函式。
補完之後，正文、標題、表格、callout、FAQ 與三塊程式對「資料往哪裡走」的說法已經一致，
每一句都回得到 `sources[]` 的原文。沒有換掉任何程式範例，沒有動到查證過的數字與日期。
