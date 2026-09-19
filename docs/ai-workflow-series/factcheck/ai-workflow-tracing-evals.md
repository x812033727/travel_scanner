# 獨立查核：ai-workflow-tracing-evals

查核代理：未參與撰稿。查核日 **2026-09-19**。
草稿的 `checked_on` 原本是 2026-09-18、七處一致；**本輪依今天的頁面改了數字**
（OpenTelemetry 屬性登錄檔的屬性數與穩定性計數）**並新增了一條 source**，
依規格把內容包七條 source 與研究紀錄的 `checked_on` 一起對齊到 **2026-09-19**。
表格與圖解 caption 的「2026 年 9 月查證」、正文第二段的「查證於 2026 年 9 月」不受影響。

查核方式：`sources[]` 全部以 `curl -sL -A "Mokaair-editorial"` 今天重抓並讀 body；
正文每一句、summary 四句、FAQ 六題答句、callout、表格十八格與兩個 caption、
圖解四格、title、description 逐條回貼原文；
OpenTelemetry 登錄檔的 Stability 欄位**用程式逐列解析計數**，不靠人工瀏覽；
兩個 `code` 區塊抽到暫存目錄 `python3 -m py_compile` 並**實際離線執行一次**，
每個匯入模組、函式簽名與關鍵字參數逐一對 `docs.python.org` 比對；
研究紀錄 30 條 `verbatim_quote` 用程式做連續字串比對（HTML 標籤去除、空白正規化）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**。

檢查的主張：**95 條**（正文 46 句／子句、summary 4 句、清單 6 項、FAQ 6 題答句、
callout 3 項、表格 18 格、兩個 caption、圖解 4 組節點、title、description），
外加程式範例 **213 個識別字**與研究紀錄 30 條引文。
**改了 11 類共 19 個編輯點**，另有 3 件留給站主。

## 重抓結果：七條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `docs.python.org/3/library/logging.html` | 200 | 191,662 | **是**。`<title>` 為「logging — Logging facility for Python — Python 3.14.7 documentation」，去標籤後 56,939 字；四條引文全部命中 |
| `docs.python.org/3/library/functools.html`（本輪新增） | 200 | 116,649 | **是**。`functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)` 與其後的範例、`WRAPPER_ASSIGNMENTS` 說明都在 |
| `opentelemetry.io/docs/specs/semconv/gen-ai/` | 200 | 172,981 | **是**。`<title>` 今天是「**Moved: Generative AI semantic conventions** \| OpenTelemetry」；`<main>` 內只剩搬遷公告與十一個同名子頁連結 |
| `raw.githubusercontent.com/...semantic-conventions-genai/main/docs/registry/attributes/gen-ai.md` | 200 | 52,759 | **是**。Markdown 原始檔，`# Gen AI` 一節的屬性表完整 |
| `raw.githubusercontent.com/...semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md` | 200 | 122,353 | **是**。Inference／Embeddings／Retrievals／Fetch response／Memory／Execute tool 六種 span 全在 |
| `developers.openai.com/api/docs/guides/evals` | 200 | 729,709 | **是**。`og:title` 與 `<h1>` 皆為「Working with evals」，去標籤後 47,947 字 |
| `platform.claude.com/docs/en/test-and-evaluate/develop-tests` | 200 | 1,934,869 | **是**。`<title>` 為「Define success criteria and build evaluations - Claude Platform Docs」，去標籤後 26,208 字 |

## 程式範例重驗

| 區塊 | 行數 | `py_compile` | 離線實跑 | 比對過的簽名／參數與文件網址 |
| --- | --- | --- | --- | --- |
| `tracer.py：JSONL 追蹤裝飾器（純標準函式庫）` | 64（與研究紀錄一致） | **通過** | **跑得動**，印出一行 JSON：`{"ts": …, "step": "summarize", "model": "claude-sonnet-5", "input_hash": "556085367d642148", "input_tokens_est": 25, "output_tokens_est": 5, "latency_ms": 0.0, "status": "ok"}` | `functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)`（functools.html）、`hashlib.sha256(...)` 與 `hash.hexdigest()`（hashlib.html）、`json.dumps(obj, *, …, ensure_ascii=True, …, default=None, sort_keys=False, **kw)`（json.html，三個關鍵字參數全部存在且拼法相同）、`time.perf_counter()` 與 `time.time()`（time.html）、`Path.open(mode='r', buffering=-1, encoding=None, …)` 與 `Path.read_text(encoding=None, …)`（pathlib.html）、`Logger.addHandler`／`extra`（logging.html） |
| `eval_compare.py：離線評測集跑分與版本比較（純標準函式庫）` | 43（與研究紀錄一致） | **通過** | **跑得動**，印出 `{'score_a': 0.75, 'score_b': 0.5, 'regressions': ['ascii-upper', 'digits']}` | `time.perf_counter()`（time.html）、`str.isascii()`（stdtypes.html：「Return True if the string is empty or all characters in the string are ASCII」——`empty` 那一題兩版都通過就是因為這一句）、`str.upper()`（stdtypes.html） |

兩塊都是純標準函式庫、無網路呼叫，因此依規格實際執行了一次。
沒有字面金鑰、`<YOUR_KEY>` 佔位、`eval(` 或刪檔命令；唯一的模型 id `claude-sonnet-5`
在 `models-seen.json` 內（本輪**沒有新增**任何模型 id）。
`checked_against` 原本只掛著 `logging.html`——那正是範例**刻意不用**的模組——已改成上表這些實際比對過的頁面。

## 改掉的 11 類（19 個編輯點）

### 協調者點名的三段

1. **「幾乎所有 gen_ai. 屬性都是 development」是人工瀏覽的印象，本輪改成數得出來的說法。**
   今天把 `docs/registry/attributes/gen-ai.md` 的屬性表用程式逐列解析：
   **72 列，全部是 `gen_ai.` 開頭，Stability 欄位 72 列全是 `Development`，`Stable` 0 列**。
   原本是「幾乎所有」（正文一處、summary 第 4 句、FAQ 第 6 題），
   都改成「本文查證當天……列出的 72 個 `gen_ai.` 屬性全部標示為 Development，沒有一個標成 Stable」。
   同一段的「列出**數十個** gen_ai. 開頭的欄位」也改成「列出 **72 個**」。
2. **`latency_ms`「不是獨立屬性，由 span 起訖時間表示」——前半是推論，後半其實找得到原文，本輪拆開處理。**
   登錄檔那 72 個屬性裡**沒有**整體延遲欄位，但**有** `gen_ai.response.time_to_first_chunk`
   （原文 `Time to first chunk in a streaming response, measured from request issuance, in seconds.`），
   所以原本的全稱否定不成立。
   而 spans 頁自己寫著 `They SHOULD cover the duration of the operation, starting when it is
   initiated and ending when the response is fully received or the operation is terminated due to
   an error or cancellation.`——「由 span 起訖時間表示」有依據。
   表格那一格已改成「那 72 個屬性裡沒有整體延遲的欄位，只有串流首個區塊的
   `gen_ai.response.time_to_first_chunk`；spans 頁則寫 span 本身要涵蓋整個操作的時間長度」，
   穩定性欄改成「development（time_to_first_chunk）」（原本寫「不適用」）；
   正文第五節第三段補一句把 spans 頁那句原文的內容寫進去，讓表格的說法在正文有落點。
3. **「頁面已標示搬遷」照今天的原文重寫。**
   今天該頁 `<title>` 是 `Moved: Generative AI semantic conventions | OpenTelemetry`，
   正文寫著 `GenAI semantic conventions have moved to the OpenTelemetry GenAI semantic conventions
   repository.` 與 `This page has moved and is no longer maintained in this repository.`
   已把「標成已搬遷」改成照原文的三件事：標題改成 Moved、已搬到 GenAI 語意慣例儲存庫、
   不再於原本的儲存庫維護。
   **新位置確認是官方頁**：該頁 `<main>` 裡唯一的外部連結是
   `https://github.com/open-telemetry/semantic-conventions-genai`（open-telemetry 組織），
   而本文 sources 第 4、5 條正是該儲存庫 `main` 分支 `docs/` 底下的檔案，指向一致。
   source 標題同步改成「OpenTelemetry：Moved: Generative AI semantic conventions（原規格站的 GenAI 語意慣例頁）」。

### 最重的一處：範例的實際輸出與正文描述不符

4. **`eval_compare.py` 實跑有兩題退步，正文只寫一題，而且對總分的結論剛好相反。**
   原文：「版本 B ……**卻讓原本會把 ASCII 轉大寫的那一題失敗**。
   **這種結果沒辦法只靠一個總分判斷哪一版更好**……」
   實際執行（本代理在暫存目錄跑過）：`{'score_a': 0.75, 'score_b': 0.5,
   'regressions': ['ascii-upper', 'digits']}`——A 通過三題、B 通過兩題，
   退步的是 **`ascii-upper` 與 `digits` 兩題**（`"42".upper()` 仍是 `"42"`，A 通過；B 加了標籤就失敗）。
   而且總分 0.75 對 0.5，**總分本身就判得出 A 較高**，原文「沒辦法只靠總分判斷」與範例的實際結果相反。
   已改寫成：「四題固定案例跑下來，版本 A 通過三題、版本 B 通過兩題……
   卻讓 ascii-upper 與 digits 兩題從通過變成失敗，退步清單列出的就是這兩題。
   總分只告訴你 B 比較低，看不出它在某一類輸入上其實變好了，所以要逐題把退步的題目列出來、人工看過」。
   研究紀錄加一條 `must_not_write` 擋住翻譯階段再寫回「只有一題退步」。

### 兩條供應商引文被升級

5. **Anthropic 的 `extremely scalable` 被寫成最高級。** 原文
   `Code-based grading: Fastest and most reliable, extremely scalable, but also lacks nuance for
   more complex judgments that require less rule-based rigidity.`
   `Fastest`／`most reliable` 是最高級，`extremely scalable` **不是**。
   草稿寫「程式評分最快、最穩定，也**最容易大量重複執行**」，已改成「**極易擴大規模**」。
   研究紀錄同一條事實也是「最容易擴大規模」，一併更正。
6. **`high quality` 被寫成「品質最高」。** 原文
   `Human grading: Most flexible and high quality, but slow and expensive. Avoid if possible.`
   ——`Most` 只修飾 `flexible`。研究紀錄那一條同步改成「品質高」。

### 與必連文章的分工

7. **Anthropic 三種評分方式整段重講，與 `ai-term-evals` 重疊。**
   `ai-term-evals` 已經用一整節加一張表比較程式評分／模型評審／外部狀態查核，
   它的 description 就寫著「比較程式、人類與模型評分」；
   而本篇自己在前一段才說「裡面已經完整說明怎麼設計案例、**選評分器**、判斷通過與否」，
   下一段卻把三種評分方式重講一次——自相矛盾，也違反「不可整段重講」。
   已壓成一段：只寫本篇範例用到的程式評分，並補上 Anthropic 頁面
   `Exact match: output == golden_answer` 這個原文例子（本篇的判分正是 `actual == expected`），
   其餘兩種只用一句「那一篇已經比較過，本篇不重複」帶過。
   研究紀錄的 `must_not_write` 與 `editorial_brief` 同步寫清楚這條界線。
   （`ai-term-agentops` 與 `claude-code-workflow-evaluation-cost` 各只被一句帶過，
   查核後與兩篇內容一致，未動。）

### 範圍過大的否定句與缺漏的限定

8. **「離線環境沒有正式的 tokenizer」超出可查證範圍。** 離線可用的 tokenizer 套件是存在的，
   本文的前提其實是「不裝任何套件」。FAQ 第 2 題已改成
   「本文的範例只用標準函式庫、不裝任何套件，所以既沒有呼叫供應商的計數工具，
   也沒有引入任何 tokenizer 套件」；正文第二節同一句也從「離線環境」改成
   「離線、不安裝任何套件的前提下」。
9. **表格 `input_hash` 那格的「改記完整的 gen_ai.input.messages」沒有依據，而且漏了警語。**
   登錄檔沒有雜湊欄位（72 個屬性逐一確認），最接近的 `gen_ai.input.messages` 是
   `The chat history provided to the model as an input.`，同頁另有警告
   `This attribute is likely to contain sensitive information including user/PII data.`
   ——正好支撐本文「只存雜湊、不存原文」的理由。已改寫成這兩件事，「完整的」拿掉。
10. **`gen_ai.operation.name` 的「一組建議值」比原文弱。** 登錄檔寫的是
    ``gen_ai.operation.name` has the following list of well-known values. If one of them applies,
    then the respective value MUST be used; otherwise, a custom value MAY be used.`
    已改成「列了一組常用值（well-known values）……其中一個適用時就必須用該值、否則才可以自訂」。
11. **「不必透過 API 上傳資料」比來源強。** OpenAI 那一頁寫的是
    `There are several ways to provide test data for eval runs, but it may be convenient to upload a
    JSONL file…` 與 `Next, let’s upload our test data file to the OpenAI platform so we can reference
    it later.`——上傳是**其中一種**方式，且可用儀表板或 API。
    已改成「不必**先把測試資料上傳到平台**」。

### 其餘小修

12. **summary 第 2 句漏列 `pathlib`。** 追蹤器實際 `from pathlib import Path`，
    而導言第二段也列了 pathlib——summary 說「**只用** hashlib、json、time 與 functools」是不成立的全稱句，已補。
13. **JSONL 的定義句改成本文的寫法。** 「JSON Lines（JSONL）**是**一行一個獨立的 JSON 物件」
    在 `sources[]` 裡沒有出處，改成「**本文採用的** JSON Lines（JSONL）寫法是……」，
    與範例實際寫檔方式（`json.dumps(...) + "\n"` 逐行附加）一致。
14. **`functools` 補上一手來源與歸屬。** 正文原本只寫「functools 讓包裝過的函式保留原本的名字與說明文字」，
    沒有任何來源；已改寫成 `functools.wraps`，並補上官方文件的說法
    （`Without the use of this decorator factory, the name of the example function would have been
    'wrapper', and the docstring of the original example() would have been lost.`），
    `time` 也改成實際用的 `time.perf_counter`。
    **`sources[]` 因此從六條增為七條**，新增 `docs.python.org/3/library/functools.html`。
15. **表格 caption。** `error.type` 那一列來自 GenAI spans 頁、不是屬性登錄檔，
    caption 從「逐字取自官方登錄檔」改成「取自官方屬性登錄檔與 GenAI spans 頁」。

## 查過而且正確的部分（沒有動）

- **OpenTelemetry 四個屬性名稱逐字無誤**：`gen_ai.operation.name`
  （`The name of the operation being performed.`）、`gen_ai.request.model`
  （`The name of the GenAI model a request is being made to.`）、
  `gen_ai.usage.input_tokens`（`The number of tokens used in the GenAI input (prompt).`）、
  `gen_ai.usage.output_tokens`（`The number of tokens used in the GenAI response (completion).`），
  拼法、底線與命名空間全部對得上，四列的 Stability 都是 Development。
- **span 命名慣例成立**：`SHOULD be `{gen_ai.operation.name} {gen_ai.request.model}`.`；
  常用值清單確實含 `chat`、`generate_content`、`text_completion`（共 18 個操作值）。
- **`error.type` 是 Stable、且是條件必要**：spans 頁六個 span 的屬性表都印著
  `![Stable](…) | `Conditionally Required` If the operation ended in an error. | string |
  Describes a class of error the operation ended with.`，
  而且該欄連回的是 **OpenTelemetry 通用語意慣例 v1.44.0 的 `error.md`**，不是 GenAI 儲存庫
  ——草稿「繼承自更通用的規範」的說法成立（本輪把它改寫成可查證的「該頁把它連回……」）。
- **四條 Python logging 引文全部命中**，包含
  `The keys in the dictionary passed in extra should not clash with the keys used by the logging
  system.` 與 `Adds the specified handler hdlr to this logger.`；
  `extra` 確實是 logging 呼叫的第四個關鍵字參數。
  正文「本文的範例**不依賴** logging，直接開檔案寫入」與程式一致
  （`tracer.py` 沒有 `import logging`，用的是 `TRACE_PATH.open("a", …)`）——
  協調者擔心的「正文說用 logging、程式用 open()」**沒有發生**。
- **OpenAI 三條引文成立**：`An eval needs two key ingredients:`、
  `A schema for the test data you will use along with the eval.`、
  `testing_criteria: The graders that determine if the model output is correct.`、
  `Your eval run has now been queued, and it will execute asynchronously as it processes every row
  in your data set…`。
  **「回歸比較」不是 OpenAI 的方法**：那一頁只在頁尾「Next steps」放了兩個 Cookbook 連結
  （`Detecting prompt regressions`、`test for prompt regressions`），本身沒有描述做法；
  本文把「兩版跑同一批題目、列退步清單」寫成**本篇的做法**，沒有歸給供應商，成立。
  同理 Anthropic 頁面的 `A/B testing: Compare performance against a baseline model or earlier
  version.` 也沒有被本文寫成「Anthropic 教你這樣做回歸比較」。
- **30 條 `verbatim_quote` 全部通過連續字串比對**（HTML 標籤去除、空白正規化後，每條都綁回它自己的 `url`）。
- **`code_samples` 的 `lines`（64、43）與內容包 code 區塊行數一致**，`label` 也一致。
- **界線檢查全部通過**：沒有訂閱、購買、升級或投資建議；沒有價格、額度或速率限制；
  沒有推薦式比價，沒有本站沒實測的排名或快慢宣稱；廠商宣稱全部有歸屬
  （「Anthropic 的文件」「OpenAI 的 Evals 文件」「登錄檔／spans 頁寫」）；
  規格狀態（Development／Stable）都寫出來了；只有**一個** `warning` callout、**沒有**免責段落；
  沒有寫「台灣可用」；`topics` 是規定的三個。
- **圖解四格與 `hero_label`** 未動；四格沒有數字，不受 72 這個新數字影響。
- **`hero.alt`** 依規格未查未改。

## 留給站主的事

1. **callout「只看總分會蓋住退步的題目」與 `ai-term-evals` 概念相近**
   （那篇寫「整體表現提高，可能同時伴隨少見但重要的請假條件退步」）。
   本輪判定**可留**：它綁的是本篇程式印出的 `regressions` 清單，不是評測案例設計方法論，
   而且是本篇唯一的 callout。若站主仍覺得重疊，可改寫成只講 `eval_compare.py` 的輸出怎麼讀。
2. **`sources[]` 由六條增為七條。** 新增 `docs.python.org/3/library/functools.html`，
   理由是 `functools.wraps` 是這支追蹤器的核心機制卻沒有一手來源，
   而原本掛著的 `logging.html` 是範例**刻意不用**的模組。
   若站主希望維持六條，替代做法是拿掉 `logging.html` 並刪掉正文談 logging 的那一段；
   本輪選擇保留，因為那一段有四條引文支撐。
3. **OpenTelemetry 的 GenAI 語意慣例仍在搬遷後的獨立儲存庫、屬性全數 Development。**
   72 這個數字與穩定性隨時可能變，正文、summary 與 FAQ 都已寫成「本文查證當天」；
   日後重查若數字不同，是規格變了，不是本文寫錯，**不要**把限定詞拿掉改寫成通則。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-tracing-evals paragraphs 2874 code_blocks 2 sources 7
```

`OK`，沒有 FAIL。唯一的 WARN 是結尾兩個純 link 尚未 relink，屬協調者的工作。
段落字數 **2,874**（1,800–3,000，改前 2,605），code 區塊 2 塊、7 條 sources。

## 結論

`needs_second_round`。改了 11 類共 19 個編輯點，其中兩處動到骨幹：
範例段落對 `eval_compare.py` 結果的描述整段重寫（原描述與程式實際輸出不符，且對總分的結論相反），
以及 Anthropic 三種評分方式那一段因與必連文章重疊而壓縮重寫。
另外 `sources[]` 增加一條、七條 `checked_on` 全部改期。
文章現在可刊，但依規格，改到骨幹敘述就該再走一輪：
第二輪只需逐句回來源查**本輪新寫進去的每一句**
（第四節第 2 段、範例後那一段、第五節三段全部、表格第 2、5 列與 caption、
summary 第 2、4 句、FAQ 第 2、6 題、正文第三節第 2 段的 functools 括號），
並重跑一次 `eval_compare.py` 確認退步清單仍是兩題。

## 第二輪

查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-19**（與第一輪同日重查）。

查核範圍是第一輪**改動過的每一段**與**新寫進去的每一句**，外加全篇的界線與一致性回掃。
檢查的主張 **126 條**（正文 47 句／子句、summary 4 句、清單 6 項、FAQ 6 題答句、
callout 標題與句 3、表格 21 格含表頭、表格與圖解 caption 2、title 與 description 2、
圖解 nodes 4，外加研究紀錄 31 條 `verbatim_quote`），程式範例另比對
**185 個相異識別字**（共 424 次出現）。**改了 4 處**（內容包 2 處、研究紀錄 2 處），
1 件連續兩輪留給站主。

**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料。**

### 重抓結果：七條 sources 今天全部讀到正文

| source | HTTP | bytes | 去標籤後字數 | body 是正文嗎 |
| --- | --- | --- | --- | --- |
| `docs.python.org/3/library/logging.html` | 200 | 191,662 | 57,801 | **是**。`<title>`「logging — Logging facility for Python — Python 3.14.7 documentation」 |
| `docs.python.org/3/library/functools.html` | 200 | 116,649 | 28,476 | **是**。`<title>`「functools — Higher-order functions and operations on callable objects …」 |
| `opentelemetry.io/docs/specs/semconv/gen-ai/` | 200 | 172,981 | 4,737 | **是**（正文只剩搬遷公告與子頁清單）。`<title>`「Moved: Generative AI semantic conventions \| OpenTelemetry」 |
| `raw.githubusercontent.com/…/registry/attributes/gen-ai.md` | 200 | 52,759 | 52,630 | **是**。Markdown 原始檔，`# Gen AI` 屬性表完整 |
| `raw.githubusercontent.com/…/gen-ai/gen-ai-spans.md` | 200 | 122,353 | 121,916 | **是**。六種 span 的屬性表都在 |
| `developers.openai.com/api/docs/guides/evals` | 200 | 729,709 | 44,844 | **是**。`<title>`「Working with evals \| OpenAI API」 |
| `platform.claude.com/docs/en/test-and-evaluate/develop-tests` | 200 | 1,935,079 | 25,427 | **是**。`<title>`「Define success criteria and build evaluations - Claude Platform Docs」 |

另外重抓了 `code_samples.checked_against` 掛的五個模組頁（`hashlib`、`json`、`time`、
`pathlib`、`stdtypes`），全部 200 且讀到正文；它們不在 `sources[]`，只用來驗程式簽名，
沒有拿來撐正文任何一句。

### 第一輪的三個關鍵結論全部可重現

1. **OpenTelemetry 屬性登錄檔的 72／全部 Development／0 個 Stable。**
   以程式重新解析主屬性表（`| Key | Stability | Value Type | Description | Example Values |`
   這張表）：**72 列資料列，鍵值不重複，全部 `gen_ai.` 開頭，Stability 欄位 72 列全是
   `Development`，`Stable` 0 列**。同檔後面還有 46 列帶反引號的列，但那些是
   `gen_ai.operation.name`、輸出型別、供應商名稱、結束原因、token 型別的**列舉值表**，
   不是屬性，第一輪沒有把它們算進來是對的。
   表中**沒有**任何含 `latency`／`duration`／`hash` 的鍵，唯一與時間有關的是
   `gen_ai.response.time_to_first_chunk`（Development）——表格第 2、5 列的兩個範圍句成立。
2. **`eval_compare.py` 的退步清單仍是兩題。** 見下方實跑輸出。
3. **31 條 `verbatim_quote` 全部通過連續字串比對。**
   這裡有一個**方法上的修正**值得記下來：第一輪那種「把每個標籤一律換成空白」的去標籤法，
   會在 `<code>`、`<em>` 這種行內元素的邊界製造出頁面上根本不存在的空白，
   於是 `logging.getLogger`、`functools.wraps` 簽名、`testing_criteria:` 三條引文會被誤判成不符。
   改用「行內標籤不插空白、只有區塊標籤換行」的還原式去標籤器重跑，**31 條 0 個不符**。
   三條引文本身沒有問題，不需要換片段，也沒有任何一條事實需要刪。

### 程式範例重驗（抽到暫存目錄，純標準函式庫、離線）

| 區塊 | 行數 | `py_compile` | 離線實跑輸出（原樣） |
| --- | --- | --- | --- |
| `tracer.py：JSONL 追蹤裝飾器（純標準函式庫）` | 64 | **通過** | `{"ts": 1789779364.05, "step": "summarize", "model": "claude-sonnet-5", "input_hash": "556085367d642148", "input_tokens_est": 25, "output_tokens_est": 5, "latency_ms": 0.0, "status": "ok"}`（再跑一次會附加成第二行，不是覆寫） |
| `eval_compare.py：離線評測集跑分與版本比較（純標準函式庫）` | 43 | **通過** | `{'score_a': 0.75, 'score_b': 0.5, 'regressions': ['ascii-upper', 'digits']}`（連跑兩次都一樣） |

行數用檢查器自己的算法（`code.count("\n") + 1`）算出 64 與 43，與研究紀錄一致。

`eval_compare.py` 逐題對照（本代理實跑）：

| 案例 | input | expected | 版本 A 輸出 | A | 版本 B 輸出 | B |
| --- | --- | --- | --- | --- | --- | --- |
| `ascii-upper` | `'hello'` | `'HELLO'` | `'HELLO'` | 通過 | `'hello[v2]'` | 失敗 |
| `zh-tag` | `'你好'` | `'你好[v2]'` | `'你好'` | 失敗 | `'你好[v2]'` | 通過 |
| `empty` | `''` | `''` | `''` | 通過 | `''` | 通過 |
| `digits` | `'42'` | `'42'` | `'42'` | 通過 | `'42[v2]'` | 失敗 |

A 通過三題（`score_a` 0.75）、B 通過兩題（`score_b` 0.5），退步的是 `ascii-upper` 與
`digits`，變好的是 `zh-tag`——**與正文「版本 A 通過三題、版本 B 通過兩題」「退步清單列出的
就是這兩題」「看不出它在某一類輸入上其實變好了」逐字相符**。正文沒有寫出 0.75／0.5 這兩個
小數，寫的是「三題」「兩題」「四題」，與表格、summary、FAQ 都一致，沒有互相打架的數字。
`empty` 那題兩版都通過，是因為 `str.isascii()` 的文件寫著
`Return True if the string is empty or all characters in the string are ASCII`。

今天重新比對過的簽名與關鍵字參數（全部命中）：
`functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)`（頁面上這行
前面還有 `@`，引文是它的連續子字串）、`hashlib.sha256(` 與 `hash.hexdigest()`、
`json.dumps(obj, *, skipkeys=False, ensure_ascii=True, …, default=None, sort_keys=False, …)`、
`time.perf_counter()` 與 `time.time()`、
`Path.open(mode='r', buffering=-1, encoding=None, …)` 與 `Path.read_text(encoding=None, …)`、
`str.isascii()`、`str.upper()`。
兩塊都沒有字面金鑰、`<YOUR_KEY>` 佔位、`eval(` 或刪檔命令，也沒有任何網路呼叫；
唯一的模型 id `claude-sonnet-5` 在 `models-seen.json` 內，本輪**沒有新增**任何模型 id。

### 改掉的 4 處

1. **正文第五節第一段：「標題已經改成 Moved」不是頁面用語，而且沒交代本文實際讀的是搬遷後的哪一頁。**
   - 原文：「現在那一頁的標題**已經改成 Moved**，頁面寫著 GenAI 語意慣例已經搬到 OpenTelemetry 的
     GenAI 語意慣例儲存庫，這一頁不再於原本的儲存庫維護；**搬過去的屬性登錄檔**，本文查證當天
     列出 72 個 `gen_ai.` 開頭的欄位……」
   - 改成：「現在那一頁的標題是 **Moved: Generative AI semantic conventions**，內文寫著 GenAI
     語意慣例已經搬到 OpenTelemetry 的 GenAI 語意慣例儲存庫、這一頁不再於原本的儲存庫維護，
     **連過去的是 open-telemetry 底下的 semantic-conventions-genai；本文實際讀的就是該儲存庫
     main 分支 docs 目錄裡的兩份檔案：屬性登錄檔與 GenAI spans 頁。**本文查證當天，屬性登錄檔
     列出 72 個 `gen_ai.` 開頭的欄位……」
   - 依據：該頁 `<title>` 今天是 `Moved: Generative AI semantic conventions | OpenTelemetry`、
     `<h1>` 是同一句去掉站名；警示框原文是
     `GenAI semantic conventions have moved to the OpenTelemetry GenAI semantic conventions repository.`
     與 `This page has moved and is no longer maintained in this repository.`；
     框內那個連結的 `href` 是 `https://github.com/open-telemetry/semantic-conventions-genai`
     （屬性未加引號，第一輪報告寫的「唯一的外部連結」查核後成立）。
     本文 `sources[]` 第 4、5 條正是該儲存庫 `main` 分支 `docs/registry/attributes/gen-ai.md`
     與 `docs/gen-ai/gen-ai-spans.md`。
   - 為什麼：原文只說「搬過去的屬性登錄檔」，讀者無從知道本文引的是搬遷後的哪一頁，
     spans 頁（正文第三段與表格第 5、6 列都靠它）在這段完全沒有落點；
     「標題已經改成 Moved」也把一個完整標題縮成一個單字，不是頁面用語。
2. **`eval_compare.py` 裡 `pipeline_b` 的註解仍寫單數。**
   - 原文：`# Version B: appends a version tag unless the input is empty; regresses the ASCII case.`
   - 改成：`# Version B: appends a version tag unless the input is empty; regresses the two ASCII cases.`
   - 依據：實跑退步的是 `ascii-upper` 與 `digits` **兩題**，兩者的輸入都是 ASCII。
   - 為什麼：第一輪把正文從「只有一題退步」改成「兩題」，但程式碼裡的註解沒有跟著改，
     留著一個會把讀者與翻譯階段帶回舊說法的單數。行數不變（43），`py_compile` 通過、輸出不變。
3. **研究紀錄新增一條 `verified_fact`：頁面標題。**
   正文現在逐字引了 `Moved: Generative AI semantic conventions`，而原本第 8 條的
   `verbatim_quote` 只涵蓋搬遷句、不涵蓋標題。新增一條以 `<title>` 原文
   `Moved: Generative AI semantic conventions | OpenTelemetry` 為 `verbatim_quote` 的事實
   （`url` 仍是 `sources[]` 第 3 條）。`verified_facts` 由 30 條增為 **31 條**，全部通過比對。
4. **研究紀錄 `must_not_write` 新增兩條。**
   一條把「`pipeline_b` 的註解要維持複數」寫進擋翻譯回退的清單（與既有那條「不可以寫成只有一題
   退步」同一個位置）；一條規定談搬遷時必須寫出頁面標題原文，並交代本文實際讀的是搬遷後的哪兩頁。

### 查過而且正確的部分（沒有動）

- **`checked_on` 一致**：內容包七條 source、研究紀錄頂層與 `code_samples.compiled_on`
  全部是 `2026-09-19`；表格 caption、圖解 caption、正文第二段的「2026 年 9 月查證」是年月層級，
  與 `2026-09-19` 相容。本輪**沒有依今天的頁面改動任何數字**，因此依規格**未動任何
  `checked_on`**（第 1、2 處改的是用語與註解，不是數字）。
- **第一輪動到骨幹的兩處覆核後成立**。範例輸出段逐題對得上實跑（見上表）。
  Anthropic 那一段壓縮後仍保有歸屬（「Anthropic 的文件」）與但書（「遇到需要較少規則式判斷的
  複雜情況就不夠細緻」）；`extremely scalable` 譯成「極易擴大規模」、`high quality` 譯成
  「品質高」都沒有被升級成最高級；`Exact match: output == golden_answer` 今天確認就列在該頁
  `Code-based grading:` 那一段底下，不是別的評分方式的例子。
- **沒有為了字數刪掉但書、限定詞或歸因**。72 這個數字出現的四處（summary 第 4 句、
  正文第五節第一段與第二段、FAQ 第 6 題）都帶「本文查證當天」；表格兩格的否定句都限縮成
  「那 72 個屬性裡」；範例段仍保有「只是示意」「固定案例只有四題，只夠驗證程式怎麼跑」
  「數量也要夠多，結論才站得住」；FAQ 第 2 題仍限縮在「本文的範例只用標準函式庫、不裝任何套件」。
- **`summary` ⊆ 正文、FAQ 答案 ⊆ 正文、圖解四格無數字**；檢查器的 summary 數字比對與
  diagram 數字比對都通過。
- **界線**：只有一個 `warning` callout、沒有免責段落；沒有訂閱、購買、升級或投資建議；
  沒有價格、額度、速率限制，也沒有本站未實測的排名或快慢宣稱；廠商宣稱全部有歸屬
  （「Anthropic 的文件」「OpenAI 的 Evals 文件」「Python 官方文件說」「官方文件特別提醒」
  「登錄檔寫的是」「GenAI spans 頁另外寫著」）；沒有寫「台灣可用」。
- **結尾兩個 link**：第一個 text 逐字是「多模型 AI 工作流教學：從拆任務到串接不同模型」，
  第二個指向 `ai-term-evals`、text 逐字是「模型與代理評測（Evals）是什麼」，
  與該內容包的 zh-TW `title` 逐字相同。正文中間沒有 link 區塊。
- **與必連三篇無矛盾、無整段重講**。`ai-term-evals` 確實用一節加一張表比較程式／人類／模型評分
  （本篇只寫自己用到的程式評分，其餘一句帶過）；`ai-term-agentops` 確實把「只監測最後一句回答
  或模型 API 是否成功，往往不夠」與工具實際結果分開講，其 description 也寫著「區分回答成功和
  操作成功」；`claude-code-workflow-evaluation-cost` 的 description 確實寫「用固定案例、原始紀錄
  和一致判準」。三篇在正文裡被點名時用的都是它們**現在**的 zh-TW title。
- **系列兄弟篇的標題**：`ai-workflow-cost-quality-latency`、`ai-workflow-cross-review-judge`、
  `ai-workflow-failures-and-guardrails` 在本篇正文**完全沒有被點名**（逐塊掃過正文、summary、
  清單、FAQ、表格、callout、caption），所以沒有舊標題殘留的問題，本輪不需要改。
- **logging 那一段成立**：`info(msg, *args, **kwargs)` 頁面寫
  `Logs a message with level INFO on this logger. The arguments are interpreted as for debug().`，
  而 `debug()` 底下寫 `The fourth keyword argument is extra which can be used to pass a dictionary
  which is used to populate the __dict__ of the LogRecord created for the logging event with
  user-defined attributes.`——「用 `info()` 的 `extra` 參數」成立；
  `addHandler` 是 `Adds the specified handler hdlr to this logger.`；
  正文「本文的範例不依賴 logging，直接開檔案寫入」與 `tracer.py` 一致（沒有 `import logging`）。
- **`error.type`**：GenAI spans 頁 18 列 `error.type` 全部印著
  `![Stable](…) | `Conditionally Required` If the operation ended in an error.`，
  連回的是 `open-telemetry/semantic-conventions` **v1.44.0** 的
  `docs/registry/attributes/error.md`（通用語意慣例，不是 GenAI 儲存庫），
  而 `error.type` 確實不在 gen_ai 登錄檔那 72 列裡——表格最後一列與正文第五節第二段成立。
- **`gen_ai.input.messages`**：描述是 `The chat history provided to the model as an input.`，
  註 [6] 底下就是 `> [!Warning] > This attribute is likely to contain sensitive information
  including user/PII data.`——表格第 2 列成立。
- **span 命名與常用值**：`**Span name** SHOULD be `{gen_ai.operation.name} {gen_ai.request.model}`.`；
  登錄檔 `gen_ai.operation.name` 的 Example Values 就是 `chat`; `generate_content`;
  `text_completion`，並寫著 `If one of them applies, then the respective value MUST be used;
  otherwise, a custom value MAY be used.`；
  spans 頁 `## Spans` 底下寫 `GenAI spans represent logical operations as observed by the caller.
  They SHOULD cover the duration of the operation, starting when it is initiated and ending when
  the response is fully received or the operation is terminated due to an error or cancellation.`
  ——正文第五節第三段三句全部成立。
- **OpenAI 三處成立**：`An eval needs two key ingredients:` 底下就是
  `data_source_config: A schema for the test data you will use along with the eval.` 與
  `testing_criteria: The graders that determine if the model output is correct.`；
  `There are several ways to provide test data for eval runs, but it may be convenient to upload a
  JSONL file…` 與 `Next, let's upload our test data file to the OpenAI platform so we can reference
  it later. You can upload files in the dashboard here, but it's possible to upload files via API as
  well.`——「不必先把測試資料上傳到平台」成立；
  `Your eval run has now been queued, and it will execute asynchronously…`——「不必排隊等待非同步的
  執行結果」成立。
- **`code_samples`** 的 `lines`（64、43）與 `label` 與內容包一致；`hero.alt` 依規格未查未改；
  `hero_label` 與圖解四格未動。

### 留給站主的事

1. **callout「只看總分會蓋住退步的題目」與 `ai-term-evals`「整體表現提高，可能同時伴隨少見但重要的
   請假條件退步」概念仍然相近。** 本輪同意第一輪的判定：**可留**——它綁的是本篇程式印出的
   `regressions` 清單，不是評測案例設計方法論，而且是全篇唯一的 callout。
   這一條連續兩輪都留給站主；若站主要收掉，最小改法是把 callout 改寫成只講
   `eval_compare.py` 的輸出怎麼讀，不要碰它與 `ai-term-evals` 的分工。
2. **`sources[]` 維持第一輪的七條。** 本輪覆核後同意保留新增的 `functools.html`：
   `functools.wraps` 是這支追蹤器的核心機制，正文那句括號引的就是該頁原文；
   `logging.html` 雖然是範例刻意不用的模組，但正文那一段有四條引文撐著，不建議拿掉。
3. **72 這個數字與「全部 Development」隨時可能變。** 本輪重數仍是 72／全部 Development／
   0 個 Stable；正文、summary 與 FAQ 都寫成「本文查證當天」。日後重查若數字不同，
   是規格變了，不是本文寫錯，**不要**把限定詞拿掉改寫成通則。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-tracing-evals paragraphs 2964 code_blocks 2 sources 7
```

`OK`，沒有 FAIL。唯一的 WARN 是結尾兩個純 link 尚未 relink，屬協調者的工作。
段落字數 **2,964**（1,800–3,000，第一輪後 2,874；本輪只增不刪，增量全在第五節第一段
補上的「本文實際讀的是搬遷後的哪兩頁」）。code 區塊 2 塊、7 條 sources。

### 結論

`ok`。第一輪那兩處骨幹改動（範例輸出段、Anthropic 評分方式壓縮）覆核後都站得住，
72／全部 Development／0 個 Stable 與 `eval_compare.py` 的兩題退步都完全可重現，
31 條引文 0 個不符。本輪只改了 4 處，其中只有一處動到正文（把搬遷敘述改成頁面用語，
並補上本文實際讀的是搬遷後哪兩頁），沒有動到任何事實數字，也沒有動任何 `checked_on`。
文章可刊。
