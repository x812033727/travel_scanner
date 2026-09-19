# 獨立查核：ai-workflow-failures-and-guardrails

查核代理：未參與撰稿。查核日 **2026-09-19**。
草稿原本六條 source 與研究紀錄都寫 2026-09-18、彼此一致；本輪**依今天的頁面換掉了一條 source 的網址**
（MCP 規格轉到新版，見下面第 1 條），依規格那一條要改成今天，而檢查器要求每條 source 的
`checked_on` 等於研究紀錄的 `checked_on`，所以六條與研究紀錄**一起對齊到 2026-09-19**。
兩個 caption 的「2026 年 9 月查證」不受影響。

查核方式：`sources[]` 六條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
逐句把 title、description、正文十六段、摘要五句、FAQ 六題、callout、表格十二格、
兩個 caption、圖解三組節點對回原文；兩個 `code` 區塊抽到暫存目錄跑 `python3 -m py_compile`、
實際各執行一次，另用一支探針腳本走過步數上限與預算上限兩條路徑；
研究紀錄每條 `verbatim_quote` **綁回它自己的 `url`** 做連續字串比對。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料。**
為了反駁而讀的其他官方頁（`platform.openai.com` 舊網址、`modelcontextprotocol.io/specification/latest`、
MCP 2025-11-25 舊版頁、`docs.python.org` 兩頁）只寫進本報告，沒有拿去替文章補事實——
唯一的例外是判定 `sources[]` 自己該換的那一條（規格允許，並在下面說明）。

檢查的主張：**86 條**（title 1、description 2 句、正文 48 句／子句、摘要 5 句、清單 4 項、
FAQ 6 題答句、callout 5 項、表格 12 格、兩個 caption、圖解 alt），外加研究紀錄 **17 條引文**
與兩個範例的 10 個識別字。**改了 15 條（27 個編輯點）**，另有 5 件留給站主。

## 重抓結果：六條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `genai.owasp.org/llmrisk/llm102025-unbounded-consumption/` | 200 | 362,405 | **是**。定義段、7 個 Common Examples of Vulnerability、15 條 Prevention and Mitigation Strategies、6 個 Example Attack Scenarios、Reference Links 全在 |
| `genai.owasp.org/llmrisk/llm052025-improper-output-handling/` | 200 | 350,704 | **是**。定義段、5 個弱點例子、7 條緩解建議、6 個 Attack Scenario 全在 |
| `genai.owasp.org/llm-top-10/` | 200 | 913,376 | **是**。`LLM01:2025` 到 `LLM10:2025` 十個條目名稱逐一印出 |
| `developers.openai.com/api/docs/guides/safety-best-practices` | 200 | 396,143 | **是**。Moderation API、Adversarial testing、HITL、Prompt engineering、KYC、Constrain user input、safety_identifier 等九節全在（`platform.openai.com/docs/guides/safety-best-practices` 今天 **301** 到這個網址，source 的「轉址後網址」成立） |
| `modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices` | 200 | 560,645 | **是**。頁首標 `Version 2026-07-28 (latest)`，Confused Deputy、Token Passthrough、SSRF、State Handle Hijacking、Local MCP Server Compromise 等節全在 |
| `platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks` | 200 | 408,985 | **是**。直接注入與間接注入兩節、JSON-encode untrusted content、Screen tool outputs、Chain safeguards 全在 |

## 程式範例重驗

| 區塊 | 語言／行數 | 編譯 | 實際執行 | 比對過的識別字與文件 |
| --- | --- | --- | --- | --- |
| `budget_guard.py：預算計數器與步數上限（純 Python，可離線跑）` | python／54 | `python3 -m py_compile` **通過**（Python 3.11.15） | **跑過**。印出 `guard stopped the loop: stopped after 6 steps: the cap is 6` | `@dataclass` 對 `docs.python.org/3/library/dataclasses.html` 的 `@dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=…)`；`RuntimeError` 對 `docs.python.org/3/library/exceptions.html`。無外部套件、無網路呼叫、無金鑰、無 `eval`、無刪檔命令 |
| `handoff_envelope.py：把模型輸出包成資料再交下游（純 Python，可離線跑）` | python／69 | `python3 -m py_compile` **通過** | **跑過**。印出啟發式旗標與包好的提示詞 | `json.dumps(..., ensure_ascii=False)` 對 `docs.python.org/3/library/json.html` 的 `json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=…)`；`@dataclass` 同上。模型 id `gpt-5.6-sol`、`claude-sonnet-5` 都在 `models-seen.json`（只當字串常數用，沒有真的呼叫） |

**協調者交辦的行為確認（第 6 項）**，用一支探針腳本走完兩條路徑：

- 出貨參數 `max_steps=6`、`max_cost_usd=0.05`、每步 `0.004`，**先撞的是步數上限**，
  停在第 6 步、只花到 `$0.024`——示範跑出來的那一行只驗證了步數這一道。
- 把 `max_steps` 放大後，第 13 次 `record()` 撞預算上限，訊息是
  `stopped after 12 steps: spending $0.052 would cross the $0.050 cap`。
- 兩條路徑都是**拋出 `BudgetExceeded`**（`class BudgetExceeded(RuntimeError)`），**不是回傳旗標**。
  草稿正文原本沒有寫是哪一種，本輪在 §2 第 3 段補上一句照實描述（見下面第 14 條），
  FAQ 第 6 題「示範的是步數與預算的計數邏輯」與程式一致，未動。
- `handoff_envelope.py` 的 docstring 宣稱「引號或換行不能關掉資料區塊」——用含
  `"`、換行與 `</instructions>` 的字串探過，`json.dumps` 逐一逸出，資料區塊仍是單行，**宣稱成立**。
  （但字面上的 `</upstream_data>` 不在 `json.dumps` 的逸出範圍；docstring 只講引號與換行，沒有寫過頭。）

## 改掉的 15 條

### 協調者點名的七項

1. **MCP 來源指向舊版（最重的一處，也是唯一換掉的 source）。**
   今天實抓轉址鏈：
   `/specification/2025-06-18/basic/security_best_practices` → **308** →
   `/docs/2025-11-25/tutorials/security/security_best_practices`（頁首 `Version 2025-11-25`），
   這正是草稿寫進 `sources[]` 的網址；
   而 `/specification/latest/basic/security_best_practices` → **307** →
   `/specification/2026-07-28/basic/security_best_practices` → **308** →
   `/docs/2026-07-28/tutorials/security/security_best_practices`，頁首 `Version 2026-07-28 (latest)`
   （`/specification/latest` 本身也落在 `/specification/2026-07-28`）。
   **現行版本是 2026-07-28**，站內另一篇引用的版本才是對的。
   內容包與研究紀錄的 source 網址、標題同步改成 2026-07-28 版，
   `checked_on` 六條一起對齊 2026-09-19。撐著這條 source 的那句引文
   （`This document identifies security risks, attack vectors, and best practices specific to MCP implementations.`）
   兩個版本都有，**換版本不影響任何引文**。
   附帶查到：2026-07-28 版把 2025-11-25 版的 **Session Hijack Prompt Injection 整節移除**，
   現行版本全文已經沒有 `prompt injection` 這個詞（只剩兩處 `untrusted`，都在 OAuth／CSP 脈絡）。
2. **正文從頭到尾沒有引用 MCP 那份文件的任何一句，description 與圖解 caption 卻把它列進「逐字引用歸因」的名單。**
   逐處確認：MCP 只出現在 description、`image.caption`、§5 第 2 段三個**列舉**裡，
   沒有任何一句話引自那一頁。加上第 1 條查到的「現行版本沒有 prompt injection 內容」，
   這個列舉撐不住。description 與 caption（含研究紀錄 `diagram.caption`）都改成
   **OWASP、OpenAI 與 Anthropic**；§5 第 2 段整句改寫（見第 4 條）。
   這條 source 本身**保留**（協調者交辦的是更新版本不是刪除），
   但研究紀錄已明記它只作為協定層級的對照，`must_not_write` 也加了一條擋住日後回填。
3. **Denial of Wallet 的延伸掛在 OWASP 名下。**
   OWASP 原文（`Common Examples of Vulnerability` 第 **2** 條，條目是 **LLM10:2025**，
   另外 `Example Attack Scenarios` 的 Scenario #4 也叫同一個名字）是：
   「`By initiating a high volume of operations, attackers exploit the cost-per-use model of
   cloud-based AI services, leading to unsustainable financial burdens on the provider and
   risking financial ruin.`」
   草稿寫「條目裡把攻擊者藉高頻操作榨乾……稱為「Denial of Wallet (DoW)」**——不必是攻擊者，
   自己的重試邏輯出錯，一樣會製造同一種後果**」，破折號後面那半句沒有歸屬，讀起來像 OWASP 說的。
   而且「**同一種後果**」不成立：OWASP 那一句寫的受害者是 **the provider**（服務供應者），
   重試迴圈爆掉時帳單落在**呼叫方**自己身上。
   已改成：「……讓服務供應者背上難以承受的費用。OWASP 這一條寫的是攻擊者；自己的重試邏輯出錯、
   帳單落在呼叫方身上，**是本站的延伸觀察**，這個條目沒有寫非惡意的情況。」
   研究紀錄第 2 條事實同步補上歸屬，`must_not_write` 加了一條。
4. **「四份官方文件都用降低風險而不是消除風險的語氣」不成立。**
   §5 第 2 段原文：「OWASP、OpenAI、MCP 與 Anthropic 的官方文件都把自己列出的做法寫成
   降低風險而不是消除風險的語氣」。逐頁對過：
   OWASP 的段落標題是 `Prevention and Mitigation Strategies`（帶 prevention）；
   MCP 那份通篇是 RFC 式的 `MUST`／`MUST NOT`／`SHOULD` 規範語；
   Anthropic 那頁結尾寫的是「`By layering these strategies, you create a robust defense against
   jailbreaking and prompt injections, ensuring your Claude-powered applications maintain the
   highest standards of safety and compliance.`」——`ensuring` 不是「降低風險」的語氣。
   整句已改成本站自己的看法，並補上「本站也沒有實測過任何一種防護的攔截率」。
5. **案例三把未經文件支撐的行為掛在三支 CLI 上。**
   草稿寫「用 Claude Code、Codex、Gemini CLI 這類可以無人值守執行的工具接起……
   **執行步驟只要把這段輸出直接接成自己提示詞的一部分**，就可能把那句話當成新的指令去執行」。
   三家文件都沒有寫「會把上游輸出原樣塞進提示詞」；站內
   《Claude Code、Codex、Gemini CLI 分工：規劃、執行、審查》寫的也是**使用者自己的腳本**
   用 `plan.md`／`patch`／`review.json` 三個檔交接（那篇明寫這三個檔名是本站自訂、不是任何一家的規格）。
   已改成「你寫一支腳本，讓**一個可以無人值守執行的命令列代理（Agent）**做「規劃」、另一個做「執行」」，
   並在段末加一句「**會不會直接串接由腳本的寫法決定，不是哪一支工具的既定行為**」。
   三支工具的名字只留在那句站內文章的引用裡，沒有再被賦予任何行為。
6. **FAQ 第 4 題的「原因就是它們是不同的失效模式」是推論。**
   OWASP 清單頁只印條目名稱與各自的一句摘要，**沒有寫為什麼分開列**。
   已改成「本站把它們讀成兩種不同的失效模式，至於為什麼分開列，清單上沒有寫」。
7. **Anthropic 與 OpenAI 的引文各掉一個限定詞。**
   Anthropic 原文是「**Where possible,** wrap third-party strings in a JSON object rather than
   concatenating them into free-form text.」，草稿的引號從 `wrap` 開始，把「在可行時」吃掉了；
   已在正文與 FAQ 第 3 題補回。
   OpenAI 原文句首是大寫的「**N**arrowing the ranges of inputs or outputs」，
   草稿引號裡寫小寫 `narrowing`，照該頁在頁面上搜尋不到；已改成大寫。
   （研究紀錄第 12 條的引文本來就是完整正確的整句，含 `especially drawn from trusted sources`；
   本輪在 `fact` 文字裡把這個條件標出來。）

### 其餘八條

8. **LLM05 的攻擊情境張冠李戴。**
   草稿寫「條目裡的攻擊情境之一，就是一個模型的回答未經輸出驗證就**直接交給另一個有權限的模型**」。
   原文 Attack Scenario #1 是：「`An application utilizes an LLM extension to generate responses for a
   chatbot feature. The extension also offers a number of administrative functions accessible to
   another privileged LLM. The general purpose LLM directly passes its response, without proper
   output validation, **to the extension** causing the extension to shut down for maintenance.`」
   下游是**擴充功能**；那個「有權限的模型」是可以呼叫擴充功能管理介面的另一方，不是收下這份回答的人。
   這是本篇「模型交給模型」骨幹的支撐句，已照原文改寫，並明寫「本篇借的是『輸出沒驗證就往下游送』這個形狀」。
   研究紀錄第 10 條事實同步更正，`must_not_write` 加了一條。
9. **OWASP 第十條緩解措施的標題被截短後放進引號。**
   草稿寫「以及限制排隊與總動作數量的「**Limit Queued Actions**」」，
   頁面上的標題是「**Limit Queued Actions and Scale Robustly**」。已補全。
   同段另外補上「這個條目下列了**十五**條因應做法」與「**本篇挑**跟這個情境最接近的三條」，
   讓「最相關」是本站的選取而不是 OWASP 的排序。
10. **案例二把自家算錯歸進 OWASP 的 LLM10。**
    草稿寫「這種放大方式**一樣屬於** OWASP「LLM10:2025 Unbounded Consumption」談的風險」。
    LLM10 的定義句寫的是「`allows **users** to conduct excessive and uncontrolled inferences`」，
    七個弱點例子與六個攻擊情境**全部**是攻擊者或使用者送進過量請求，沒有一個是應用自己的規劃步驟算錯數量。
    已改成「成因不是 OWASP……寫的使用者過量請求，而是自家規劃步驟把數量寫錯，**放在一起談是本站的歸類**」。
11. **兩處 superlative 沒有依據。**
    description 第 1 句與摘要第 1 句都寫「多模型工作流**最容易失控**的三種情況」——
    沒有任何來源排序過失控頻率，本站也沒有實測。兩處都改成「**常見的**三種」，
    與正文「這篇挑三個具體的失控情境」一致。
    callout 的「**常見的**坑」也改成「一個容易踩的坑」。
12. **OpenAI 那條 source 的標題宣稱頁面上沒有的東西。**
    標題寫「輸入輸出範圍限縮、human in the loop、**rate limit 相關指引**」。
    今天以該頁**正文段落**比對，`rate limit` 出現 **0** 次；`Rate limits` 的 4 次命中
    全落在左側導覽（`Rate limits and spend`、`Operations > Rate limits`）。
    正文相關的一節叫 `Constrain user input and limit output tokens`。
    標題已改成「限制輸入長度與輸出 token 數」。
13. **研究紀錄第 1 條的引文撐不起它自己的 fact。**
    `fact` 寫「OWASP 把 Unbounded Consumption 定義為 LLM 應用允許使用者進行過度且不受控的推論」，
    `verbatim_quote` 卻是「`Unbounded Consumption refers to the process where a Large Language Model
    (LLM) generates outputs based on input queries or prompts.`」——那句講的是推論這個動作本身，
    沒有「允許使用者過度且不受控」這件事。已換成頁面上真正這樣寫的那一句
    （`Unbounded Consumption occurs when a Large Language Model (LLM) application allows users to
    conduct excessive and uncontrolled inferences, leading to risks such as denial of service (DoS),
    economic losses, model theft, and service degradation.`），並把後果四項補進 `fact`。
14. **正文補上程式的實際行為。**
    §2 第 3 段加「超過上限時它**拋出自訂例外中斷迴圈**，不是回傳旗標讓呼叫端自己判斷」，
    與 `BudgetExceeded(RuntimeError)` 一致（見上面的程式重驗表）。
15. **FAQ 第 1 題的否定句超出查到的範圍。**
    「**官方文件不會給單一數字**」是對所有官方文件的全稱否定；
    已限縮成「**本篇查的官方文件都沒有給單一數字**」，並把「照自己的流程回推、不要照抄樣板數字」
    標成本站的建議。
    另外，FAQ 第 3 題原本寫「Anthropic 官方文件把 JSON 編碼寫成讓攻擊者**不容易**「跳出」資料範圍」——
    原文其實比這個強（`so an attacker **cannot** close a quote or tag to "break out" into an
    instruction context`），但那句話管的是**分隔機制本身**，不是「下游模型不會被誤導」。
    已改成照原文寫分隔機制，並把「降低機率而不是歸零」標成本站的看法。

**騰字**：本輪補進去的歸屬與限定詞（§2 第 2、3 段 +78、§3 第 2 段 +27、§4 第 1、2 段 +67）
全部靠精簡**重複敘述**騰出來——
§1 第 1 段與第 3 段的鋪陳（「一個模型的錯誤通常會馬上被你看到：它答錯了，你就換個問法，或者乾脆自己動手」
→「模型答錯你會馬上看到，換個問法或自己動手就好」）、§2／§3 情境段的贅詞、
§3 末段與 §5 第 2 段的重述。**沒有刪掉任何但書或限定詞。**
段落字數 2,971 → **2,985**。

## 查過而且正確的部分（沒有動）

- **研究紀錄 17 條 `verbatim_quote` 全部通過**——每條**綁回它自己的 `url`** 做連續字串比對
  （不是跨來源搜尋），含本輪新增的四條（`Automated MLOps Deployment`、
  `Version 2026-07-28 (latest)`、`Where possible, wrap third-party strings…`、
  以及換掉的第 1 條）。`classifier's` 那條確認頁面用的是 **ASCII 直撇**，原樣正確。
- **OWASP 三個條目編號與排序成立**：清單頁逐字印出 `LLM01:2025` 到 `LLM10:2025`，
  `LLM05:2025 Improper Output Handling` 與 `LLM10:2025 Unbounded Consumption` 是兩個獨立項目。
  §1 第 3 段「兩者是分開的項目，不是同一件事的兩種說法」成立。
- **三條緩解措施的內容逐字吻合**：`Apply rate limiting and user quotas to restrict the number of
  requests a single source entity can make in a given time period.`、
  `Set timeouts and throttle processing for resource-intensive operations to prevent prolonged
  resource consumption.`、`Implement restrictions on the number of queued actions and total
  actions, while incorporating dynamic scaling and load balancing…`；十五條的數目也對
  （第 15 條是 `Automated MLOps Deployment`）。
- **`Treat the model as any other user, adopting a zero-trust approach` 與
  `JSON escaping provides unambiguous delimiters between the untrusted payload and the surrounding
  structure` 逐字無誤**，歸屬（OWASP／Anthropic）也對。
- **必連的三篇沒有被重講也沒有被矛盾**：《提示詞注入是什麼：使用者該懂的攻擊》
  《安全防護機制（Guardrails）是什麼》《Claude Code｜MCP 回傳含有指令時：資料與操作權限分開》
  三篇的 zh-TW title 逐字對過，本篇各用**一句**帶過，定義與操作步驟都沒有重寫。
  《Claude Code、Codex、Gemini CLI 分工：規劃、執行、審查》那篇本身就把
  「重試、人工通知與總花費上限」指向本篇，兩篇**互相銜接、不衝突**；
  schema 驗證迴圈的細節留給《模型之間交接資料：JSON Schema 與結構化輸出》、
  事後追查留給《追蹤、評測與可觀測性：知道流程哪一步出錯》，兩處都只有一句轉介。
- **結尾兩個 `link` 的 text 逐字正確**：第一個「多模型 AI 工作流教學：從拆任務到串接不同模型」，
  第二個「提示詞注入是什麼：使用者該懂的攻擊」＝ `ai-prompt-injection-explained` 的 zh-TW title。
  正文中間沒有 `link` 區塊。
- **用語照 BRIEF 統一**：全篇用「防護」（沿用站內 `ai-term-guardrails` 的
  「安全防護機制（Guardrails）」），**沒有出現「護欄」「防護欄」「安全圍欄」**；
  token、提示詞、結構化輸出、代理（Agent）、追蹤、評測都照系列寫法，沒有簡體字。
- **界線全部通過**：沒有訂閱、購買、升級或投資建議，沒有任何價格與推薦式比價，
  沒有「台灣可用」，沒有把預覽或 beta 寫成已推出（本篇沒有引用任何功能狀態），
  只有**一個** `warning` callout、**沒有**免責段落，`topics` 是 `ai`／`tutorial`／`ai-coding`。
  改完之後，每一條廠商宣稱都帶歸屬（OWASP 寫／OpenAI 的官方安全文件寫／Anthropic 的官方文件建議），
  本站自己的判斷一律標「本站」。
- **摘要五句都在正文找得到**；圖解三組節點與表格十二格沒有需要回正文比對的數字；
  兩個 caption 的「2026 年 9 月查證」本輪重查後仍成立。
- **`models-seen.json` 不需要新增**：正文沒有出現任何模型 id，
  兩個範例裡的 `gpt-5.6-sol` 與 `claude-sonnet-5` 都已在清單裡，且只是字串常數。

## 留給站主的事

1. **Anthropic 那一頁在 JSON 包裝之前還有一條更強的建議**：
   「`Put untrusted content only in tool results. Deliver third-party content to Claude inside
   tool_result blocks, never in system prompts or plain user text blocks.`」
   本篇的 `handoff_envelope.py` 是不綁廠商的提示詞字串組裝，**做不到那一條**。
   正文沒有宣稱本篇範例符合 Anthropic 的全部建議（研究紀錄 `unverified_or_excluded` 也記了），
   但日後若要把範例改成 Claude Messages API 的寫法，這條要一起補。
2. **MCP 那條 source 現在一句都沒有被引用。** 本代理依協調者指示把它更新到現行版本而不是刪除；
   如果站主覺得完全沒被引用的來源不該留在名單裡，可以整條拿掉（`sources` 會剩五條，仍在 3–8 內），
   description、caption 與 §5 都已經不再提到它，拿掉不需要再改正文。
3. **MCP 的 `latest` 還會再前進。** 今天 `/specification/latest` 指向 2026-07-28；
   日後重查若又換版，要連同站內其他引用一起更新，並注意 2026-07-28 版已把
   Session Hijack Prompt Injection 整節移除，舊版連結不再等價。
4. **title 的「代理間注入」是本站的框架用語。** 三份來源都沒有這個詞
   （最接近的是 OWASP LLM01 的 indirect prompt injection，不在本篇 `sources` 裡）。
   若希望標題只用來源有的詞，需要重擬 title 並連動研究紀錄的 `title`。
5. **段落字數 2,985，離 3,000 只剩 15 個字。** 翻譯或後續編修要再加句子之前得先騰字，
   **不可以拿限定詞或歸屬來湊**。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-failures-and-guardrails paragraphs 2985 code_blocks 2 sources 6
```

`OK`，沒有 FAIL；那個 WARN 是結尾兩個純 `link` 尚未 relink，由協調者處理。
段落字數 **2,985**（1,800–3,000），title 21 單位，description 184 單位（120–200），
`code` 區塊 2 塊、54 與 69 行（與研究紀錄 `code_samples` 的 `lines` 一致）。

## 結論

`needs_second_round`。改了 15 條、27 個編輯點，其中**兩處動到骨幹**：
案例三支撐「模型交給模型」的那個 OWASP 攻擊情境其實寫的是擴充功能（第 8 條），
以及案例二被歸進 LLM10 的歸屬（第 10 條）；另有一條 source 換掉（第 1 條）。
文章本身現在可刊，但依規格，改到骨幹論述就該再走一輪。
第二輪只需要逐句回來源查**本輪新寫進去的每一句**：
§1 第 1、2、3 段，§2 第 2、3 段，§3 第 1、2 段，§4 第 1、2、3 段，§5 第 1、2 段，
FAQ 第 1、3、4 題，callout，description 與摘要第 1 句，
以及研究紀錄新增的四條引文與 `factcheck` 欄位。
