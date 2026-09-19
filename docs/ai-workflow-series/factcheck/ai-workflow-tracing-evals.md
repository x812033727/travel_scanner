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
