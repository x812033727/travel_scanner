# 獨立查核：ai-workflow-unified-api-layer

查核代理：未參與撰稿。查核日 **2026-09-19**。
文章的 `checked_on` 是 **2026-09-18**，八條 source 與研究紀錄六處一致，今天重抓的頁面與撰稿者所記相同
（沒有任何數字因今天的頁面而改），依規格**不動**。
查核方式：`sources[]` 八條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
正文每一句、摘要、FAQ 每題答句、callout、表格每一格與 caption、圖解 caption 與節點、
`hero_label`、title、description 逐條回貼原文；兩個 `code` 區塊抽到暫存目錄跑 `python3 -m py_compile`，
每個 base_url、環境變數名、HTTP 標頭、函式簽名、關鍵字參數與模型 id 逐字對官方頁；
研究紀錄的引文用連續字串比對（HTML 去標籤後「標籤換空白」與「標籤直接刪掉」兩種接法都試）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**
（為了反駁而讀的 `docs.litellm.ai/docs/providers` 與 `docs.mistral.ai/...` 只寫進本報告）。

檢查的主張：**99 條**（正文 44 句／子句、摘要 6 句、FAQ 19 句、callout 4 項、表格 16 格、
表格與圖解 caption 各 1、圖解 5 組節點、`hero_label`、title、description），
外加研究紀錄 23 條引文與程式範例約 35 個識別字。**改了 14 處（16 個編輯點）**，另有 3 件留給站主。

## 重抓結果：八條今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `openrouter.ai/docs/quickstart` | 200 | 767,035 | **是**。標題 `OpenRouter Quickstart Guide`；三種整合方式、`Using the OpenAI SDK` 的 Python／TypeScript 範例、兩個選用標頭的註解都在 |
| `openrouter.ai/docs/api-reference/overview` | 200 | 644,044 | **是**。請求 schema（135 行）、`Headers`、`Non-standard parameters`、回應 schema 與 `Finish reason` 都在 |
| `docs.litellm.ai/docs/` | 200 | 106,555 | **是**。`Installation`／`Quick Start` 六個供應商分頁、`Choose Your Path` 兩欄、`Exception Handling`、Proxy 兩步驟都在 |
| `docs.litellm.ai/docs/completion/input` | 200 | 99,698 | **是**。`Translated OpenAI params` 表、`note` 的 drop_params 段、`def completion(...)` 完整簽名都在 |
| `docs.litellm.ai/docs/providers/openrouter` | 200 | 115,205 | **是**。`Usage` 範例、`OpenRouter Completion Models` 表、`transforms/models/route` 段都在 |
| `github.com/openai/openai-python` | **403** | 378 | 否——**被本工作階段的代理擋掉**（回的是 `GitHub access to this repository is not enabled for this session`，不是 GitHub 的頁面；退回 curl 預設 UA 仍是同一個 403）。依規格改抓 `raw.githubusercontent.com/openai/openai-python/main/README.md`：**HTTP 200、41,584 bytes、是 README 全文**（`Requirements`、`Timeouts`、`Usage` 各節都在） |
| `console.groq.com/docs/openai` | 200 | 301,135 | **是**。`Configuring OpenAI to Use Groq API` 的 Python 範例、`Currently Unsupported OpenAI Features` 四個欄位清單都在 |
| `console.groq.com/docs/models` | 200 | 404,628 | **是**。`Featured Models`、`Production Models` 表（`MODEL ID` 欄）、`Preview Models`、`Get All Available Models` 都在 |

## 程式範例重驗

| 區塊 | 行數 | `python3 -m py_compile` | 比對過的識別字與文件 |
| --- | --- | --- | --- |
| `openai 套件：同一段程式換兩個 OpenAI 相容 base_url` | 34 | **ok** | `OpenAI(base_url=, api_key=, timeout=)`、`chat.completions.create(extra_headers=, model=, messages=)`、`choices[0].message.content` → `raw.githubusercontent.com/openai/openai-python/main/README.md`（`timeout=20.0` 是 README 自己的範例，另有 `with_options(timeout=...)`）；`https://openrouter.ai/api/v1`、`HTTP-Referer`、`X-OpenRouter-Title`、`Authorization: Bearer` → `openrouter.ai/docs/quickstart`（兩個標頭都標 `Optional.`）與 `openrouter.ai/docs/api-reference/overview`（`X-Title also accepted`）；`https://api.groq.com/openai/v1`、`GROQ_API_KEY` → `console.groq.com/docs/openai`；`openai/gpt-oss-120b` → `console.groq.com/docs/models` |
| `litellm 套件：completion() 換三個 model 字串` | 17 → **22** | **ok**（今天改後重編譯） | `from litellm import completion`、`completion(model=, messages=, timeout=)` → `docs.litellm.ai/docs/completion/input`（`timeout: Optional[Union[float, int]] = None,`，以秒計、預設 600 秒）；`openai/gpt-5.6-terra`、`anthropic/claude-sonnet-5`、`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`litellm.AuthenticationError` → `docs.litellm.ai/docs/`；`openrouter/` 前綴與 `OPENROUTER_API_KEY` → `docs.litellm.ai/docs/providers/openrouter` |

兩塊都沒有字面金鑰、`<YOUR_KEY>`、`eval` 或刪檔命令，網路呼叫都帶 `timeout`，沒有捏造輸出。

## 改掉的 14 處

### 協調者點名的三段

1. **Groq 那句「也是 OpenAI 自己開放權重的 gpt-oss 模型在 Groq 上跑的版本」沒有歸屬。**
   `console.groq.com/docs/models` 的 Featured 區原句是
   `GPT-OSS 120B is OpenAI's flagship open-weight language model with 120 billion parameters, built in
   browser search and code execution, and reasoning capabilities.`
   ——這一頁是官方一手頁、本來就在 `sources[]` 裡，所以**來源成立、不必換供應商**，缺的只是歸屬。
   已改成「範例裡的 `openai/gpt-oss-120b` 是 Groq 模型頁 `MODEL ID` 欄位上的代號，**那一頁把它寫成
   OpenAI 的旗艦開放權重模型**」，研究紀錄補一條事實掛這句原文。
2. **研究紀錄第 23 條引文在頁面上搜尋不到（最重的一處）。**
   原本寫 `"model": "openai/gpt-oss-120b"` 出自 `console.groq.com/docs/models`。
   今天逐字比對：這個字串**不在可讀正文裡**，只出現在頁面 Next.js flight payload 的跳脫字串中
   （`\\\"model\\\": \\\"openai/gpt-oss-120b\\\"`，而且那是 Responses API 的 `input` 範例，
   不是 Chat Completions），去標籤後兩種接法都搜不到。
   已改成表格上找得到的 `GPT OSS 120B openai/gpt-oss-120b`，事實文字改成「Production Models 表格
   `MODEL ID` 欄位上的代號」。同一條連動的 source 標題「（openai/gpt-oss-120b 模型代號與**範例請求**）」
   也不成立（該頁的範例請求是列出模型的 `/openai/v1/models`），已改成
   「（`MODEL ID` 欄位上的 openai/gpt-oss-120b、GPT-OSS 120B 的模型說明）」，內容包與研究紀錄同步。
3. **「LiteLLM 依前綴決定呼叫哪一家 API」不是文件寫的機制。**
   `sources[]` 裡三頁 LiteLLM 文件，`prefix` 一字命中 **0** 次；首頁與 Input Params 頁只給範例，
   沒有任何一句說明「前綴決定要打哪一家、該讀哪一組環境變數」。頁面真正明講的只有 OpenRouter 那一頁：
   `LiteLLM supports ALL OpenRouter models, send model=openrouter/<your-openrouter-model> to send it to
   open router.`
   已把正文「LiteLLM 認供應商的方式是看 model 字串」與 FAQ 第 4 題的機制句，改成
   「官方文件的**每個範例**都把供應商名稱寫在最前面、用斜線隔開……並**在同一段範例裡設好**對應的環境變數」
   ＋ OpenRouter 那一頁的原句。研究紀錄 `must_not_write` 加一條擋住翻譯階段寫回機制句。
4. **同一個毛病在正文另一處。** 「LiteLLM 自己會決定要打哪一家的網址、帶哪一把金鑰」同樣沒有出處，
   已改成文件寫得出來的那一半：`LiteLLM maps every provider's errors to the OpenAI exception types`
   →「官方文件寫，LiteLLM 把各家的錯誤對應成 OpenAI 的例外型別」。
5. **FAQ 第 3 題「Groq 則是照它自己模型頁列出的代號填」收斂。**
   該頁的依據是 Production Models 表的 `MODEL ID` 欄，加上
   `Hosted models are directly accessible through the GroqCloud Models API endpoint using the model IDs
   mentioned above.`
   已改成「Groq 則是填它模型頁表格 `MODEL ID` 欄位上的代號」。

### 相容範圍（協調者第 6 點）

6. **Groq 不支援欄位漏了官方清單的第四項。** 原句是
   `The following fields are currently not supported and will result in a 400 error (yikes) if they are
   supplied: logprobs / logit_bias / top_logprobs / messages[].name`。
   草稿的正文與 callout 都只寫三個，已補上 **`messages[].name`**，callout 另補回 `currently` 對應的「目前」。
   （同段的 `If N is supplied, it must be equal to 1.` 與 Audio 的 `vtt`／`srt` 不屬本篇範圍，維持不寫。）
7. **`drop_params` 的範圍限定被刪掉。** 原文 note 的最後一句是
   `This ONLY DROPS UNSUPPORTED OPENAI PARAMS . LiteLLM assumes any non-openai param is provider specific
   and passes it in as a kwarg in the request body`。
   正文與 callout 都已補上「而且（文件註明）它只會捨棄不支援的 OpenAI 參數」。
   OpenRouter 那一側本來就照原文列了 `logit_bias`（非 OpenAI 模型）與 `top_k`（OpenAI 模型），沒有動。

### 其餘

8. **自架 Proxy 那段的因果是草稿自己加的。** 「`api_key` 隨便填一個字串即可，**因為認證是自架的 Proxy
   自己在管，不是原本那些供應商在管**」——文件只有範例 `openai.OpenAI(api_key="anything",
   base_url="http://0.0.0.0:4000")` 與功能列 `Virtual keys with per-key/team/user budgets`。
   已改成「`api_key` 填的是 `anything` 這個字串，實際的存取控制由 Proxy 自己的虛擬金鑰管」。
9. **同段「OpenRouter 是別人已經架好、你付費使用的託管閘道」**——本篇 `sources[]` 沒有任何費用資訊
   （費用是《OpenRouter：一把金鑰用遍各家模型》的事），已刪掉「你付費使用」，順手把與 FAQ 第 5 題
   重複的兩句收成一句（騰出字數給第 12 點的新句子）。
10. **FAQ 第 5 題「OpenRouter……金鑰的花費上限與存取規則要照對方提供的設定做」**同樣沒有來源，
    已改成中性寫法「能設定的就是對方那一端提供的項目」，LiteLLM 那一半改成文件真的列出的項目。
11. **表格第 3 列兩格。** 「相容範圍由誰的文件定義」原本寫「LiteLLM 的 **Providers** 文件頁」，
    但 `sources[]` 裡的 Providers 頁只有 OpenRouter 一頁，真正列出各供應商支援哪些 OpenAI 參數的是
    Input Params 頁（那張 `Translated OpenAI params` 表），已改掉；model 字串那格補上「與 OpenRouter
    那一列同形不同意」。
12. **兩段程式裡同形的 `anthropic/claude-sonnet-5` 沒有講清楚是哪一家的字串（協調者第 5 點）。**
    第一段是 OpenRouter 目錄裡的完整代號，第二段是 LiteLLM 的 `anthropic/` 前綴加 Anthropic 自己的
    `claude-sonnet-5`（讀 `ANTHROPIC_API_KEY`，`docs.litellm.ai/docs/` 的 Anthropic 分頁就是這個字串）。
    正文、表格、FAQ 第 4 題各補一句點明「同形不同意」。
13. **「只需要換 base_url 與 model 字串兩個值」與文章自己的「三個地方」矛盾。**
    Groq 文件寫的是 `pass your Groq API key to the api_key parameter and change the base_url`，
    正文第 2 節與 FAQ 第 3 題也寫「base_url、金鑰讀的環境變數、model 三個地方」。
    導言、`description`、圖解節點（「換兩個值／base_url、model」）、圖解 `alt` 與 image caption
    （內容包與研究紀錄同步）全部改成 base_url、金鑰與 model 三個。
14. **兩個小修 ＋ 一段程式。**
    「設了應用程式**才會**出現在排行榜上」比原文 `Setting them allows your app to appear on the
    OpenRouter leaderboards` 強，改成「就能」；
    第 5 節「相容層不會替它補上原本沒有的功能」與同句前半重複，刪（騰字）；
    第二個 `code` 區塊 `import os` 匯入了卻沒用到，改成用它檢查三個環境變數是否設好
    （`OPENAI_API_KEY`／`ANTHROPIC_API_KEY`／`OPENROUTER_API_KEY`，金鑰仍然只從環境變數讀），
    17 → 22 行，今天重新 `py_compile` 通過，研究紀錄的 `lines` 與 `compiled_on` 同步。

## 查過而且正確的部分（沒有動）

- **兩個 base_url 逐字無誤**：`https://openrouter.ai/api/v1`（quickstart 的 OpenAI SDK 範例）與
  `https://api.groq.com/openai/v1`（Groq `base_url="https://api.groq.com/openai/v1"`），
  都含 `/v1`、都沒有結尾斜線；OpenRouter 的端點路徑 `/api/v1/chat/completions` 也對得上原文。
- **金鑰環境變數名逐字無誤**：`OPENROUTER_API_KEY`（quickstart 的 Python SDK 範例
  `os.getenv("OPENROUTER_API_KEY")`）、`GROQ_API_KEY`（Groq 範例 `os.environ.get("GROQ_API_KEY")`）、
  `OPENAI_API_KEY` 與 `ANTHROPIC_API_KEY`（LiteLLM 首頁 Quick Start 各分頁）。
- **兩個選用標頭的拼法無誤**：`HTTP-Referer` 與 `X-OpenRouter-Title`，quickstart 兩個都註 `Optional.`；
  API 參考另寫 `X-Title also accepted`、第三個 `X-OpenRouter-Categories` 本篇刻意不寫（研究紀錄已記）。
- **`timeout` 的傳法無誤**：openai-python README 的範例就是 `OpenAI(timeout=20.0)`
  （`By default requests time out after 10 minutes.`，另有 `with_options(timeout=5.0)` 可逐次覆寫），
  所以範例用 `OpenAI(timeout=30.0)` 成立；LiteLLM 的 `completion()` 簽名是
  `timeout: Optional[Union[float, int]] = None,`、以秒計。
- **LiteLLM 三個 model 字串**：`openai/gpt-5.6-terra` 與 `anthropic/claude-sonnet-5` 是文件首頁範例的
  原字串；`openrouter/google/gemini-3.8-flash` 的前綴規則出自 OpenRouter 供應商頁，
  模型半段是 `models-seen.json` 記過的 OpenRouter 代號。
- **Proxy 段逐項對得上**：`Self-hosted gateway for platform teams managing LLM access across an
  organization.`、`http://0.0.0.0:4000`、`api_key="anything"`、虛擬金鑰預算、集中記錄與快取、管理介面。
- **界線檢查全部通過**：全篇沒有價格、免費額度、購買、升級或訂閱建議，沒有推薦式比價，沒有「台灣可用」，
  沒有本站沒做過的實測宣稱；只有**一個** callout、**沒有**免責段落；廠商宣稱都有歸屬
  （「官方文件寫」「Groq 官方文件」「OpenRouter 的 API 參考」）；
  沒有把預告寫成已推出（`gpt-oss-120b` 在 Groq 是 Production 列，不是 Preview）。
- **與必連文章的分工成立**：OpenRouter 的帳號／金鑰／儲值一句帶過並指向
  《OpenRouter：一把金鑰用遍各家模型》，Claude 與 Gemini 的第一次呼叫各一句帶過，
  路由與 fallback 只有一句並指向《模型路由與級聯：便宜先試、貴的兜底》，全篇沒有提 Ollama；
  正文點名的四個站內標題與內容包逐字相同，第二個結尾 link 的 text 與
  `openrouter-multi-model-api` 的 zh-TW title 逐字相同。
- **研究紀錄引文**：原 23 條，修掉第 23 條之後全部通過連續字串比對；本輪新增 9 條（Groq 開放權重歸屬、
  Groq model IDs 那句、OpenRouter 前綴規則、`This ONLY DROPS UNSUPPORTED OPENAI PARAMS`、
  LiteLLM 的 Anthropic 字串、虛擬金鑰、Proxy 呼叫範例、`timeout` 秒數、README 的 `timeout=20.0` 註解），
  **共 32 條今天全部在各自的 `url` 上原樣搜尋得到**。
- **`checked_on` 2026-09-18** 在八條 source 與研究紀錄一致，未更動。

## 留給站主的事

1. **`models-seen.json` 的 `mistral-small-2603` 那筆（不是本篇用的 id，依規格「不改別人的條目」未動）。**
   `verbatim` 寫的是 `Click to copy: mistral-small-2603`，今天重抓
   `docs.mistral.ai/models/mistral-small-4-0-26-03`（HTTP 200、1,184,812 bytes）確認：
   那串字**只存在於徽章的 `title=` 屬性**（滑鼠移上去才看得到的提示），去標籤後搜尋不到；
   id 本身、別名 `mistral-small-latest`、`GA`、`Apache 2.0`、`v 26.03` 在頁面上都在。
   要不要把 `verbatim` 換成正文可見的字串，由站主決定。
2. **第一個 `code` 區塊的 OpenRouter 半段，與《OpenRouter：一把金鑰用遍各家模型》的 Python 範例高度相似**
   （都是 `base_url` ＋ `extra_headers` ＋ `anthropic/claude-sonnet-5`）。
   差別是本篇多了第二個用戶端、金鑰改從環境變數讀、加了 `timeout`；這是指派「同一段 Python 打兩個
   base_url」要求的形狀，本代理沒有動。若站主覺得仍嫌重複，可考慮只留 Groq 那半。
3. **openai-python 的 README 現在把 Responses API 寫成主要介面**，Chat Completions 是
   `The previous standard (supported indefinitely)`。本篇談的相容層都是 Chat Completions 形狀，
   目前沒有寫錯；日後若要補一句說明，請回 README 重查那兩行的措辭。

## `models-seen.json`

只**新增**兩筆（用「重新讀檔 → append → 寫回」，其他代理同時新增的條目未受影響，本次寫回時清單已從 25 筆長到 29 筆）：

- `openai/gpt-5.6-terra`（LiteLLM SDK 字串）— `docs.litellm.ai/docs/`，verbatim `model="openai/gpt-5.6-terra"`，`checked_on` 2026-09-19。
- `openrouter/google/gemini-3.8-flash`（LiteLLM 經 OpenRouter 的字串）— `docs.litellm.ai/docs/providers/openrouter`，
  verbatim 是該頁的前綴規則原句（這是**組合字串**，`notes` 已寫明模型半段取自清單裡的 `google/gemini-3.8-flash`），`checked_on` 2026-09-19。

`mistral-small-2603` 與 `openai/gpt-oss-120b` 兩筆是撰稿者加的，未改：後者的 `url` 與 `verbatim`
（`GPT OSS 120B openai/gpt-oss-120b`）今天在 `console.groq.com/docs/models` 去標籤後找得到，成立；
前者見「留給站主的事」第 1 點。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-unified-api-layer paragraphs 2975 code_blocks 2 sources 8
```

`OK`，沒有 FAIL；`raw_internal_url` 是結尾兩個純 link 尚未 relink 的預期警告。
段落字數 **2,975**（1,800–3,000），code 區塊 2 塊（34 行、22 行），sources 8 條。

## 結論

`ok`。改了 14 處、16 個編輯點，全部是歸屬、限定詞、來源撐不住的機制句與一條搜尋不到的引文，
**沒有動到骨幹論述，也沒有換掉任何一個程式範例**（第二塊只加了三行環境變數檢查，讓原本沒用到的
`import os` 有了用途）。不需要第二輪。

## 第二輪

第二位查核代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-19**（與第一輪同一天，
`checked_on` 仍是 **2026-09-18**，八條 source 與研究紀錄一致，今天的頁面沒有一個數字改變，依規格**不動**）。

範圍：第一輪改動過的每一段與新寫進去的每一句逐句回貼 `sources[]` 原文，其餘正文、`summary`、
FAQ、callout、表格每一格、兩個 caption、圖解節點、`hero_label`、title、description 一併複驗
（合計與第一輪同一組 **99 條主張**），外加研究紀錄 **34 條 `verbatim_quote`**（第一輪 23＋9，本輪再加 2）
與兩塊程式約 35 個識別字。來源全部自己重抓、重讀 body；
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。**改了 8 處。**

### 重抓結果：八條今天再讀一次，都是正文

| source | HTTP | bytes | body |
| --- | --- | --- | --- |
| `openrouter.ai/docs/quickstart` | 200 | 767,035 | 是（`Using the OpenAI SDK` 的 Python 範例、兩個 `Optional.` 標頭註解、`~openai/gpt-sol-latest` 的 latest alias 說明都在） |
| `openrouter.ai/docs/api-reference/overview` | 200 | 644,001 | 是（`Non-standard parameters`、`Headers`、請求 schema 的 `supported_parameters=tools` 註解都在） |
| `docs.litellm.ai/docs/` | 200 | 106,555 | 是（Quick Start 六個供應商頁籤、`Exception Handling`、Proxy 兩步驟都在） |
| `docs.litellm.ai/docs/completion/input` | 200 | 99,698 | 是（`Translated OpenAI params` 表、`note` 的 drop_params 段、`def completion(...)` 簽名都在） |
| `docs.litellm.ai/docs/providers/openrouter` | 200 | 115,205 | 是（`Usage`、`OpenRouter Completion Models` 表都在） |
| `github.com/openai/openai-python` | **403** | 378 | 否——仍被本工作階段的代理擋掉（回的是 `GitHub access to this repository is not enabled for this session`）。依規格改抓 `raw.githubusercontent.com/openai/openai-python/main/README.md`：**200、41,584 bytes、README 全文** |
| `console.groq.com/docs/openai` | 200 | 301,135 | 是（`Currently Unsupported OpenAI Features` 的四個欄位、`base_url` 範例都在） |
| `console.groq.com/docs/models` | 200 | 404,628 | 是（Featured 的 GPT-OSS 120B 說明、Production Models 表的 `MODEL ID` 欄都在） |

### 研究紀錄的引文：34 條全部通過連續字串比對

用程式比對，HTML 去標籤後試三種接法（標籤換空白、標籤直接刪、另外把 Next.js flight payload 的跳脫字串
單獨當一種），並確認**沒有任何一條只靠 payload 成立**——第一輪改掉的第 23 條現在是表格上的
`GPT OSS 120B openai/gpt-oss-120b`，在「換空白」那一種裡就找得到。八條引文只在「標籤直接刪」那一種命中，
逐一看過前後文，全部是程式碼區塊被語法高亮切成 span 的結果（例如
`os.environ["ANTHROPIC_API_KEY"] = "your-api-key"`、`timeout: Optional[Union[float, int]] = None,`），不是拼接。

### 程式範例：兩塊再編譯一次，沒有動

| 區塊 | 行數 | `python3 -m py_compile` | 本輪再對過的識別字 |
| --- | --- | --- | --- |
| `openai 套件：同一段程式換兩個 OpenAI 相容 base_url` | 34 | **ok** | `https://openrouter.ai/api/v1`／`https://api.groq.com/openai/v1`（兩頁逐字、都含 `/v1`、無結尾斜線）、`OPENROUTER_API_KEY`／`GROQ_API_KEY`／`SITE_URL`／`SITE_NAME`（前兩個是文件上的名字，後兩個是讀者自己的值，對應文件的 `<YOUR_SITE_URL>`／`<YOUR_SITE_NAME>`）、`HTTP-Referer`／`X-OpenRouter-Title`（quickstart 兩個都註 `Optional.`；API 參考另寫 `X-Title also accepted`）、`OpenAI(base_url=, api_key=, timeout=)`（README `## Timeouts`：`timeout=20.0`、`By default requests time out after 10 minutes.`，所以 `timeout=30.0` 這個 float 成立）、`extra_headers`（README `#### Undocumented request params`）、`choices[0].message.content` |
| `litellm 套件：completion() 換三個 model 字串` | 22 | **ok** | `completion(model=, messages=, timeout=)`（`timeout: Optional[Union[float, int]] = None,`、`Timeout in seconds ... (Defaults to 600 seconds)`，所以 `timeout=30` 這個 int 成立）、`openai/gpt-5.6-terra` 與 `anthropic/claude-sonnet-5`（首頁 Quick Start 原字串）、`openrouter/google/gemini-3.8-flash`（前綴規則＋目錄代號的組合，見下）、`OPENAI_API_KEY`／`ANTHROPIC_API_KEY`／`OPENROUTER_API_KEY` 的三個環境變數檢查 |

兩塊與第一輪交出來的位元組完全相同，`lines` 34／22 與研究紀錄一致（檢查器算法是 `code.count("\n") + 1`），
所以 `code_samples` 不必改。沒有字面金鑰、`<YOUR_KEY>`、`eval` 或刪檔命令，兩處網路呼叫都帶 `timeout`，沒有捏造輸出。

### 改掉的 8 處

1. **`summary` 第 1 句還留著第一輪要修掉的那個數字（最重的一處）。**
   第一輪把導言、`description`、圖解節點、圖解 `alt` 與 image caption 的「只換兩個值」統一成
   base_url、金鑰與 model 三個，但**漏了摘要**：
   「官方 openai 套件與 LiteLLM 都能**只換 base_url 或 model 字串**切換供應商」。
   正文第 2 節與 FAQ 3 寫的是「base_url、金鑰讀的環境變數，以及 model 字串三個地方」，摘要與正文互相矛盾，
   也違反「summary ⊆ 正文」。已改成
   「官方 openai 套件換 base_url、金鑰與 model 字串，LiteLLM 換 model 字串，就能切換供應商」。
2. **「官方文件的**每個**範例都把供應商名稱寫在最前面」在文件上不成立（第二重）。**
   `docs.litellm.ai/docs/` 同一頁的 `Logging & Observability` 與 `Track Costs & Usage` 範例用的是
   **沒有前綴**的 `model="gpt-5.6-terra"`（今天以連續字串確認在頁面上），Proxy 那段呼叫用的是 config 裡取的
   `model="gpt-5.6-luna"`。真正成立的是：文件**示範某一家供應商**時才帶前綴——
   `openai/`、`anthropic/`、`vertex_ai/`、`bedrock/`、`ollama/`、`azure/` 六個頁籤都是。
   正文與 FAQ 4 已收斂成「官方文件**示範每一家供應商時**，都把供應商名稱寫在最前面、用斜線隔開」，
   研究紀錄 `must_not_write` 加一條擋住翻譯階段寫回絕對句，並補一條事實
   （`os.environ["ANTHROPIC_API_KEY"] = "your-api-key"`）撐「在同一段範例裡設好對應的環境變數」。
3. **「每個模型頁也會列出它支援哪些欄位」沒有來源（第三重）。**
   本篇 `sources[]` 的兩頁 OpenRouter 文件都沒有這句話；「整份模型清單放在**公開的** API 上」的「公開」
   也沒寫（quickstart 只寫 `list every available slug programmatically via the GET /api/v1/models endpoint`）。
   頁面真的寫得出來的是 API 參考請求 schema 裡的註解
   `See models supporting tool calling: openrouter.ai/models?supported_parameters=tools`。
   整句已改成「OpenRouter 則是在 API 參考的註解裡示範，用 `supported_parameters` 篩出支援工具呼叫的模型」，
   研究紀錄補這條 verbatim，`unverified_or_excluded` 記下原本那半為什麼拿掉。
4. **「比自己一個個手動試更快」是沒有來源的比較。**
   `get_supported_openai_params()` 那一段，文件只寫
   `Use this function to get an up-to-date list of supported openai params for any model + provider.`，
   沒有任何快慢比較。已刪掉這半句（也騰出字數給第 3 點的新句子）。
5. **FAQ 3「OpenRouter 是**固定的**『供應商／模型』格式」太絕對。**
   quickstart 自己的範例就是帶 `~` 的 latest alias `~openai/gpt-sol-latest`
   （`a latest alias that always resolves to the newest model in the OpenAI GPT Sol family`）。
   已改成「OpenRouter 用的是『供應商／模型』這種格式」。
6. **「這裡用到的 `anthropic/claude-sonnet-5` 是 OpenRouter **模型頁**上的代號」的出處不對。**
   `models-seen.json` 這一筆是從 `openrouter.ai/api/v1/models` 抄的，quickstart 也只寫
   `Browse the full catalog at openrouter.ai/models`；同一篇後面本來就寫「OpenRouter **目錄**裡的代號」。
   已統一成「OpenRouter 目錄裡的代號」。
7. **圖解節點的三個值與正文不同字。** 第一輪把節點改成「換三個值／**端點**、金鑰、model」，
   但正文、image caption 與 `alt` 寫的都是 `base_url`。已把節點細項改成
   「base_url、金鑰、model」（11.15 個單位，仍在規格的 14 字以內），三處用字一致。
8. **「request 裡帶了工具呼叫」的 `request`** 依系列的台灣用語規則改成「請求」（同句的
   工具呼叫（tool calling）維持不動）。

### 查過而且正確、本輪沒有動的部分

- **第一輪最重的那三處都站得住**：Groq 的歸屬句對得上 Featured 區原文
  `GPT-OSS 120B is OpenAI's flagship open-weight language model with 120 billion parameters`；
  `GPT OSS 120B openai/gpt-oss-120b` 在 Production Models 表（不是 Preview）上找得到；
  「LiteLLM 依前綴決定呼叫哪一家」的機制句確實已經換成文件寫法，`prefix` 一字在三頁 LiteLLM 文件仍是 0 次。
- **Groq 不支援欄位四個一起寫**（`logprobs`／`logit_bias`／`top_logprobs`／`messages[].name`）、
  `currently` 對應的「目前」、`400` 這個狀態碼，正文與 callout 兩處都在。
  同段的 `If N is supplied, it must be equal to 1.` 與 Audio 的 `vtt`／`srt` 依研究紀錄維持不寫。
- **`drop_params` 的範圍限定**（`This ONLY DROPS UNSUPPORTED OPENAI PARAMS`）正文與 callout 都在；
  OpenRouter 側的 `logit_bias`（非 OpenAI 模型）與 `top_k`（OpenAI 模型）逐字對得上
  `then the parameter is ignored. The rest are forwarded to the underlying model API.`。
- **例外型別那句**對得上 `LiteLLM maps every provider's errors to the OpenAI exception types`，
  `litellm.AuthenticationError`、`litellm.RateLimitError` 都在同一段程式裡。
- **Proxy 段**逐項對得上：`Self-hosted gateway for platform teams managing LLM access across an organization.`、
  `openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")`、
  `Virtual keys with per-key/team/user budgets`、`Centralized logging, guardrails, and caching`、
  `Admin UI for monitoring and management`。
- **排行榜那句**維持第一輪改過的「就能」，對得上
  `Setting them allows your app to appear on the OpenRouter leaderboards.` 與同段的 `are optional`。
- **界線再掃一次全部通過**：只有 **1 個** callout、1 張圖解、**沒有**免責段落；全篇沒有價格、免費額度、
  手續費、購買、升級或訂閱建議，沒有推薦式比價，沒有「台灣可用」，沒有本站沒做過的實測宣稱，沒有驚嘆號；
  廠商宣稱都有歸屬。表格 16 格裡出現的三個數字（`120`、兩個 `5`，都在模型 id 裡）正文都有；
  摘要與圖解沒有任何數字。
- **與必連文章的分工**：OpenRouter 的帳號／金鑰／儲值、Claude 與 Gemini 的第一次呼叫、路由與 fallback
  都各只有一句帶過；《OpenRouter：一把金鑰用遍各家模型》談的是價格、手續費、隱私與路由，本篇一個價格數字都沒有，
  沒有矛盾也沒有整段重講。
- **正文點名的四個系列兄弟篇，標題與今天的內容包逐字相同**：
  《模型路由與級聯：便宜先試、貴的兜底》《成本、品質、延遲：多模型流程怎麼取捨》
  《第一次呼叫 Claude API：金鑰、費用與十行 Python》《AI Studio 與第一個 Gemini API 呼叫》
  （本篇沒有點名 `ai-workflow-local-and-cloud-mix` 與 `ai-workflow-structured-handoff`）。
  結尾第一個 link 的 text 與 `ai-workflow-tutorials` 的 zh-TW title
  「多模型 AI 工作流教學：從拆任務到串接不同模型」逐字相同（目錄篇已經寫好，所以連這一個 FAIL 都沒有），
  第二個指向 `openrouter-multi-model-api`、text 與它的 zh-TW title 逐字相同；正文中間沒有 link 區塊。
- **兩處「換 base_url 與 model 字串」沒有動**：第 2 節的標題與第 5 節開頭那句都只是在點名這個做法、
  **沒有宣告個數**（第一輪修掉的是「只需要換……兩個值」這種有數字的寫法），與正文的「三個地方」不衝突。

### 留給站主的事

1. **`models-seen.json` 的 `openrouter/google/gemini-3.8-flash`（第一輪新增）本輪判定成立，但它是組合字串。**
   它的 `verbatim` 是 `send model=openrouter/<your-openrouter-model> to send it to open router`——
   今天在 `docs.litellm.ai/docs/providers/openrouter` 上以連續字串確認得到，符合清單「verbatim 是那一頁上的連續字串」
   的定義；**但 id 本身沒有出現在任何頁面上**（該頁的實例是 `openrouter/google/palm-2-chat-bison`，
   `gemini-3.8-flash` 在那一頁 0 次）。id 的兩半分別有據：前綴出自這句規則，模型半段
   `google/gemini-3.8-flash` 是清單裡另一筆、抄自 `openrouter.ai/api/v1/models`。
   條目的 `notes` 已經寫明這件事，所以**沒有新增修正條目、也沒有動它**；
   若站主希望清單只收「頁面上逐字出現過的 id」，這一筆要改成註記型條目，請站主決定。
   同一輪新增的 `openai/gpt-5.6-terra` 沒有這個問題：`model="openai/gpt-5.6-terra"` 今天在首頁 Quick Start 找得到。
2. **`mistral-small-2603` 那筆仍未動**（不是本篇用的 id，依規格不改別人的條目）；第一輪已寫明它的
   `verbatim` 只存在於徽章的 `title=` 屬性。
3. **openai-python README 的主要介面是 Responses API**，Chat Completions 標成
   `The previous standard (supported indefinitely)`。本篇談的相容層都是 Chat Completions 形狀，
   目前沒寫錯；日後若要補一句狀態說明，請回 README 重查那兩行。
4. **第一個 `code` 區塊的 OpenRouter 半段與《OpenRouter：一把金鑰用遍各家模型》的 Python 範例仍然相似**
   （第一輪已列，本輪沒有動）：本篇多了第二個用戶端、金鑰從環境變數讀、加了 `timeout`。

### `models-seen.json`

**本輪沒有新增、沒有修改、沒有刪除任何條目**（今天讀到的是 31 筆）。本篇正文與兩塊程式用到的
`openai/gpt-oss-120b`、`anthropic/claude-sonnet-5`、`openai/gpt-5.6-terra`、`google/gemini-3.8-flash`、
`openrouter/google/gemini-3.8-flash` 全部在清單裡，檢查器也沒有對任何一個模型 id 發警告。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-unified-api-layer paragraphs 2968 code_blocks 2 sources 8
```

`OK`，沒有 FAIL；`raw_internal_url` 是結尾兩個純 link 尚未 relink 的預期警告。
段落字數從 **2,975** 降到 **2,968**（1,800–3,000）：本輪補的句子比刪掉的短，
**沒有為了字數刪掉任何但書、限定詞或歸因**。code 區塊 2 塊（34 行、22 行）、sources 8 條都沒有變。

### 結論

`ok`。第二輪再改 8 處：一處是第一輪漏掉的摘要數字（與正文矛盾），兩處是來源撐不住的絕對句與無出處的欄位說明，
其餘是沒有來源的比較句、出處寫錯的代號、圖解用字與一個英文詞。
**骨幹論述、章節結構與兩個程式範例都沒有動**，`checked_on` 依規格維持 2026-09-18。不需要第三輪。
