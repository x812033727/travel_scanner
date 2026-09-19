# 獨立查核：ai-workflow-basics

查核代理：未參與撰稿。查核日 **2026-09-19**。
文章的 `checked_on` 是 **2026-09-18**，三條 source 與研究紀錄四處本來就一致，
今天重抓的三個頁面沒有一句本文引用的內容改過、也沒有任何數字被改寫，
依規格**不因重查而改**（新補進正文的「2024 年 12 月」是那篇文章的發表日，不是會變動的值）。

查核方式：`sources[]` 三條今天全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
把正文每一句、summary 四句、FAQ 五題問答、callout、表格每一格與 caption、圖解節點、
`hero_label`、title、description 逐條回貼來源原文（`hero.alt` 未查，主圖由協調者繪製）；
研究紀錄每條 `verbatim_quote` **綁回它自己的 `url`** 做連續字串比對（HTML 標籤剝除後）；
三篇必連文章與五篇同系列既有文章的內容包逐段讀過做分工比對。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

檢查的主張：**96 條**（正文 39 句／子句、summary 4 句、FAQ 5 題問答共 10 項、callout 3 項、
表格 21 格、表格與圖解 caption、圖解 3 組節點、`hero_label`、title、description 3 句、結尾兩個 link），
外加研究紀錄 14 條引文。**改了 13 處**，另有 4 件留給站主。

## 重抓結果：三條 sources 今天都讀到正文，不是空殼

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `anthropic.com/engineering/building-effective-agents` | 200 | 211,506 | **是**。`<title>` 為「Building Effective AI Agents \ Anthropic」，但頁面自己印的文章標題是 **Building effective agents**、下方 `Published Dec 19, 2024`；workflow／agent 兩句定義、When (and when not) to use agents、六種 pattern、兩個附錄全文都在；`Access Denied`／`Request Access`／`http-equiv="refresh"` 各 **0** 次 |
| `openai.github.io/openai-agents-python/` | 200 | 76,263 | **是**。渲染後 7,608 字，含 `Why use the Agents SDK` 全部條目與 `Agents SDK or Responses API?` 兩組 bullet、`pip install openai-agents`、hello world |
| `docs.langchain.com/oss/python/langgraph/overview` | 200 | 852,166 | **是**（JS 站，但正文在 HTML 裡）。渲染後 7,118 字，含開頭定位段、`Core benefits` 六項、`Install` 與 hello world 圖 |

三頁的 14 條 `verbatim_quote` 今天**全部**以連續字串比對通過。
Anthropic 那兩句定義在原始 HTML 裡被 `<strong>` 切開（`<li><strong>Workflows</strong> are systems…`），
**剝除標籤後是連續字串**，符合規格對 verbatim 的定義，未更動。

## 程式範例

**本篇是入門篇，`code` 區塊 0 個**（`code_samples: []`），與 BRIEF「入門篇可以零個或一個」相符，
自檢也確認 `code_blocks 0`。沒有可重驗的編譯項；正文與 FAQ 全篇**沒有出現任何模型 id**
（自檢的 prose 模型掃描無 WARN），因此 `models-seen.json` **沒有新增**任何條目。
比對過的官方識別字共 9 個，全部在散文裡被點名而非在程式裡：
`tool dispatch`、`turns`、`tool execution`、`guardrails`、`handoffs`、`sessions`（以上 OpenAI Agents SDK 首頁）、
`Responses API`、`deterministic, hand-coded steps`／`LLM-driven agentic steps`（LangGraph overview）。

## 改掉的 13 處

### 協調者點名的三段

1. **Anthropic 代理定義裡的 `their own processes` 被譯成「流程」，和本文自己的譯名對撞（最重的一處）。**
   原文：`Agents, on the other hand, are systems where LLMs dynamically direct their own processes and
   tool usage, maintaining control over how they accomplish tasks.`
   草稿寫「LLM 自己**動態指揮流程**與工具使用」——但本文從上一節開始就把 **workflow 譯成「流程」**，
   而 workflow 在原文正是與 agent **對立**的那一類。照字面讀會變成「代理去指揮流程」，
   定義的分界線就翻過去了。原文的 `their own processes` 是模型**自己的處理過程**。
   已改成「LLM 自己動態**主導自己的處理過程**與工具使用」，並在 `must_not_write` 擋住翻譯階段再犯。
2. **「調度」與「主控權」兩個譯詞：都在原意範圍內，沒有改。**
   - `orchestrated through predefined code paths` →「依照預先寫定的程式路徑**被調度**」：
     被動、由外部安排，與原文一致，沒有加進原文沒有的主動性。
   - `maintaining control over how they accomplish tasks` →「**對怎麼完成任務**保有**主控權**」：
     原文的限定範圍（`over how they accomplish tasks`）草稿有完整保留，沒有擴大成「對整個系統的主導」；
     而「主」字對得上這一段的對照關係——workflow 是程式路徑在控制，agent 是模型在控制。
     兩詞維持原樣。（附帶發現：`orchestration` 的譯名站上三篇不一致，見「留給站主的事」。）
3. **三層比較表「代理」欄語氣中立，沒有改。** 四格分別是「模型，邊做邊自己判斷」「不固定，由模型決定要不要換路徑」
   「模型自己決定要不要回頭問、要不要跳過」「模型判斷待辦欄位含糊時要不要先回頭問你」——
   全是**描述誰決定什麼**，沒有一格出現「更好」「更聰明」「進階」這類詞，也沒有把「回頭問人」寫成優點。
   「回頭問、跳過」有來源撐：`potentially returning to the human for further information or judgement`、
   `Agents can then pause for human feedback at checkpoints or when encountering blockers`。
   同一篇的 callout 反向提醒「多一層不會自動變準」，表與 callout 沒有互相矛盾，
   FAQ 第 4 題也明寫「不是每個流程最後都要變成代理」。**不需要調整。**

### 兩條來源被引用的每一句：有兩處寫進了頁面沒說的意思

4. **`tool dispatch` 被譯成「工具呼叫**順序**」。** 原文是
   `you want to own the loop, tool dispatch, and state handling yourself`——
   dispatch 是**把工具呼叫派送出去**這件事，不是呼叫的先後順序，頁面通篇沒有談順序。
   站上既有文章「Agent 框架入門」同一句用的就是「**工具派送**」。已改成「工具派送」。
5. **「二選一」的框架是草稿加的，官方下一句就否掉了。** 草稿寫成
   「想自己掌控…就直接用底層的 API；想讓執行環境…才用現成的代理框架」，
   但頁面在兩組 bullet 之後緊接著寫
   `You do not need to choose one globally. Many applications use the SDK for managed workflows and
   call the Responses API directly for lower-level paths.`
   已補上「文件寫明這不是全域二選一，同一個應用可以兩種混用」，並把「底層的 API／現成的代理框架」
   這種泛稱收回成一條分界線的描述（頁面點名的是 Responses API 與 Agents SDK 本身，不是「框架」這一類）。
6. **LangGraph 那段沒有寫進頁面沒說的功能**（`low-level orchestration framework and runtime`、
   `long-running, stateful agents`、`mix deterministic, hand-coded steps with LLM-driven agentic steps
   in the same graph` 逐項對得上），但**整段與必連文章重複**，見第 8 條。

### 界線與分工：兩段在重講必連文章

7. **Agents SDK／Responses API 的取捨整段與「Agent 框架入門」幾乎同義。**
   該文已經寫著：「OpenAI 的文件就直說：想自己掌握迴圈、工具派送與狀態，流程又短，那直接呼叫
   Responses API 就好；要交給執行環境管回合、工具執行、護欄、交接或 session，才輪到 Agents SDK。」
   指派寫明必連文章「只能一句帶過、不得整段重講」。已收成一句
   （「把『迴圈、工具派送與狀態由誰管』當成要不要交給執行環境的分界」）＋第 5 條補的那個限定詞。
8. **LangGraph 的官方定位整段也是。** 該文已經寫著：「LangGraph 的官方定位是低階的協調框架與執行環境，
   用來跑長時間、有狀態的代理……官方特別強調同一張圖裡可以混搭寫死的步驟與交給模型判斷的步驟。」
   草稿等於把同一段再寫一次（連「用來蓋、管理與部署長時間執行、有狀態的代理」都照抄定位句）。
   已刪掉定位句，只留**對本篇論點有用的那一句**——同一張圖可以混用兩種步驟，
   所以「流程與代理不是二選一」——並把框架各自的定位一併推回那篇。

### 來源支撐不住或名字不對的五處

9. **上下文視窗那句沒有任何來源撐。** 草稿寫「一次對話能放進去的內容也有限，話題一多、來回一多，
   最早提到的內容可能被擠到看不見的地方」——這是關於模型行為的技術主張，
   但三條 sources 的任何一頁都**沒有**談上下文長度或訊息被擠出（`context window` 在三頁皆 0 次），
   而規格禁止用 `sources[]` 以外的網址補證。整句改寫成不含這個機制的說法
   （「步驟沒有寫下來，前情每次都得從頭交代」），沒有削弱原本的論點。
10. **`Agentic systems` 被換成「把系統疊得更複雜」。** 原文
    `Agentic systems often trade latency and cost for better task performance`——
    主詞是**代理式系統**這一類，不是泛指「系統變複雜」。已改回並標出英文原詞。
11. **`usually` 被刪掉。** 原文 `optimizing single LLM calls with retrieval and in-context examples is
    usually enough`，草稿寫「搭配檢索與範例**就夠**」。已改成「**通常**就夠了」。
12. **文章名字寫錯。** 草稿寫《Building Effective AI Agents》——那是**瀏覽器分頁標題**
    （`<title>Building Effective AI Agents \ Anthropic</title>`）；頁面印在作者列上方的文章標題是
    **Building effective agents**，站上另外六篇（含同系列 `ai-workflow-split-tasks-across-models`）
    引用同一頁時用的也都是後者。正文與 `sources[0].title` 都已改，研究紀錄同步。
    同時補上發表年月「2024 年 12 月」——這是一篇兩年前的文章，而本文的骨幹定義整個來自它。
13. **兩個站內文章的名字：一個縮寫、一個描述了還不存在的內容。**
    「一件事拆給多個模型：**四種切法**」是縮寫，真正的 zh-TW title 是
    「一件事拆給多個模型：**依步驟、能力、風險、資料敏感度**四種切法」，已補全（`autolink` 要靠它比對）。
    「成本、品質、延遲：多模型流程怎麼取捨」草稿寫它「**有估算表**」——查核開始時那篇的內容包
    還不存在，不能描述一篇還沒寫的文章有什麼。已改成「會處理」。（標題本身保留：同系列
    `ai-workflow-split-tasks-across-models` 正文也用同一個標題，且查核途中該篇已被另一個代理寫出來，
    title 逐字相同，見「留給站主的事」。）

**另補兩句有來源的話**（都在第 5 節，回填草稿原本沒有歸屬的判斷）：
Anthropic 何時用流程、何時用代理那一句，含原文兩個限定詞
（`When more complexity is warranted`、`needed at scale`）；
以及 `Agents can be used for open-ended problems where it’s difficult or impossible to predict the
required number of steps, and where you can’t hardcode a fixed path.`
研究紀錄相應新增 6 條 `verified_facts`（今天逐條做過連續字串比對）、
4 條 `unverified_or_excluded`、5 條 `must_not_write`。

## 查過而且正確的部分（沒有動）

- **Anthropic 的兩句定義本身**：`Workflows are systems where LLMs and tools are orchestrated through
  predefined code paths.` 與代理那句，中譯除第 1 條的 `their own processes` 外逐項對得上，沒有增減條件。
- **OpenAI Agents SDK 被引用的其餘每一句都找得到原句**：
  `Sessions: A persistent memory layer for maintaining working context within an agent loop.`
  （撐正文「記憶都先寫好」）、`you want the runtime to manage turns, tool execution, guardrails,
  handoffs, or sessions`。**沒有寫進頁面沒說的功能**：正文沒有提到 Sandbox agents、Realtime、Voice、
  Tracing、MCP 這些頁面上有但本文用不到的東西，也沒有替 SDK 宣稱任何效能或品質。
- **LangGraph 被引用的那一句**逐字對得上 `mix deterministic, hand-coded steps with LLM-driven agentic
  steps in the same graph`；正文沒有提到 durable execution、persistence、LangSmith 這些頁面上有、
  但本文沒有查證需求的功能，也沒有把 LangGraph 說成必要或最好。
- **Claude Agent SDK 被歸類成代理框架有來源**：Anthropic 該頁 frameworks 清單第一項就是 `The Claude Agent SDK`。
- **必連文章的三個標題逐字相符**（「提示詞串接（Prompt Chaining）是什麼」「代理迴圈（Agent Loop）是什麼：
  判斷、操作與回饋」「Agent 框架入門：OpenAI Agents SDK、Claude Agent SDK、LangGraph」），
  正文對三篇都只有一句帶過，**沒有與它們矛盾**：提示詞串接的一句話定義、代理迴圈的「判斷、行動、讀回饋」
  三段式，都與那兩篇自己的寫法一致。結尾第二個 link 指向 `ai-term-prompt-chaining`、
  text 等於它的 zh-TW title；第一個 link text 是指定的目錄篇標題（自檢逐字比對通過）。
- **其他系列篇的分工守住了**：正文明寫不談「每一步該換哪個模型」（拆法）、不談成本延遲的估算、
  不談契約怎麼寫成正式規格，也沒有出現路由、級聯、統一 API 層、防護、追蹤評測這些他篇的主題。
- **界線全部通過**：沒有訂閱、購買、升級或投資建議；沒有推薦式比價，也沒有任何價格；
  沒有「台灣可用」；沒有把預告寫成已推出；**只有一個** `warning` callout、**沒有**免責段落；
  廠商宣稱全部帶歸屬（「Anthropic 把…定義成」「OpenAI 的 Agents SDK 文件」「LangGraph 的官方文件也寫」）；
  沒有本站沒實測的排名、快慢或品質高低。
- **summary 四句都 ⊆ 正文**，圖解三格與 `hero_label` 不含數字，表格 caption 與圖解 caption 都帶查證年月且
  與研究紀錄 `diagram.caption` 逐字相同；`display_order` 400、`kind`／`topics`／`news_date` 都照規格。
- **`checked_on` 2026-09-18** 在三條 source 與研究紀錄四處一致，未更動。

## 留給站主的事

1. **Anthropic 那頁頂端有一則編按**：`Note: Much of the tooling landscape described in this post has
   changed since December 2024.`，並指向 Claude Managed Agents。本文引用的是它的**定義與取捨建議**
   （不在編按的射程內），本輪只補上發表年月。若站主要更保守，可在第 1 節再加半句點出這則編按；
   **但不要**去追編按連出去的新頁面，那些網址不在 `sources[]` 裡。
2. **同一個「社團會議紀錄 → 待辦 → 通知」情境，必連文「提示詞串接（Prompt Chaining）是什麼」也在用。**
   這是指派指定給本篇的例子，本輪沒有改。兩篇並排時讀者可能覺得重複，要區隔就得換掉其中一篇的情境。
3. **`orchestration` 的譯名站上三套並存**：本篇「流程調度」、「Agent 框架入門」「協調框架」、
   另有「代理協調（Agent Orchestration）」。本輪只在本篇內部保持一致，沒有跨篇統一——這要站主決定。
4. **「成本、品質、延遲：多模型流程怎麼取捨」在本輪查核途中才被另一個代理寫出來**
   （`apps/api/app/guides/content/ai-workflow-cost-quality-latency.json`，本代理沒有動它）。
   它的 zh-TW title 與本篇、與 `ai-workflow-split-tasks-across-models` 正文寫的逐字相同，
   而且它確實帶一張成本估算表。本篇保守寫成「會處理」；等那個檔落地之後，
   站主若要把「有估算表」寫回來，是成立的。
5. **結尾兩個純 link 的 `raw_internal_url` WARN 由協調者 `pack_cli relink` 處理**，本代理沒有動。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-basics paragraphs 2136 code_blocks 0 sources 3
```

`OK`，沒有 FAIL。段落字數 **2,136**（1,800–3,000，原本 2,015），title 21 字，description 198 字（上限 200，很緊），
code 區塊 0，sources 3。`models-seen.json` 未新增（全篇沒有模型 id）。

## 結論

`needs_second_round`。改了 13 處，其中兩處動到骨幹：代理定義的 `their own processes` 譯法
（原譯會把 workflow／agent 的分界翻過去），以及第 3 節第 2、3 段因為與必連文章「Agent 框架入門」
整段重複而各收成一句。文章現在可刊，但依規格，改到骨幹論述就該再走一輪。
第二輪只需要逐句回來源查**本輪新寫進去的每一句**：
第 1 節第 2 段、第 3 節第 1 段的代理定義、第 3 節第 2 段與第 3 段的第一句、
第 5 節第 1 段的站內文章名、第 5 節第 2 段整段，以及研究紀錄新增的 6 條 `verified_facts`。
