# 獨立查核：ai-workflow-split-tasks-across-models

查核代理：未參與撰稿。查核日 **2026-09-19**。文章的 `checked_on` 本來就是 2026-09-18、
四處（三條 source 與研究紀錄）一致，今天重抓三個頁面的相關段落與撰稿當日內容相同，
**沒有依今天的頁面改任何數字，所以 `checked_on` 一律不動**（FACTCHECK 第 1 節末條）。

查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
逐條把 title、description、正文 14 段 38 句、摘要 5 句、清單 5 項、表格 16 格、
兩個 caption、callout 3 句、FAQ 6 題答句、圖解 5 組節點與 `hero_label` 對回原文，
共 **83 條主張**；研究紀錄的 `verbatim_quote` 用程式做連續字串比對。
**任何請求的 UA、標頭與查詢字串都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

結果：**改了 8 條（11 個編輯點）**，另有 4 件留給站主。這是入門篇、**沒有 code 區塊**，
所以錯誤型態不是參數與旗標，而是**譯名、歸屬與沒有來源的效益宣稱**。

## 重抓結果：三條 sources 今天都讀到正文，不是空殼

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `anthropic.com/engineering/building-effective-agents` | 200 | 211,506 | **是**。純 HTML 全文（去標籤後 20,031 字元），`Published Dec 19, 2024`、五個 workflow 小節（prompt chaining／routing／parallelization／orchestrator-workers／evaluator-optimizer）、Appendix 1–2 都在；頁首的 Note 指向 Managed Agents |
| `platform.claude.com/docs/en/about-claude/models/overview` | 200 | 367,902 | **是**。雖然是文件站，去標籤後仍有 5,093 字元正文：`Compare models` 整張比較表（Pricing、Claude API ID、Context window、Max output、Comparative latency 各列都讀得到），側邊目錄含 `Specialized models`／`Legacy models` 兩個分組 |
| `platform.openai.com/docs/models` | 200 | 382,226 | **是**。去標籤後 14,811 字元，`Flagship models` 四張模型卡（id、價格、context、max output）與 `Specialized models Purpose-built for specific tasks.` 一節（Daybreak／Life sciences／Image／Realtime）都在 |

三條都是官方一手頁面、無追蹤參數、無 PDF，`checked_on` 三條都是 2026-09-18，與研究紀錄一致。

## 程式範例重驗：這一篇沒有

入門篇（指派標「入門（可零 code）」），內容包 `code` 區塊 **0 塊**，
`check_article.py` 也只對非入門篇要求兩塊，研究紀錄 `code_samples` 是空陣列，一致。
沒有可編譯的識別字，因此**沒有任何簽名、旗標、端點或環境變數需要比對**；
正文也沒有出現任何模型 id（檢查器的 `model_ids_in(prose)` 沒有 WARN），
**`models-seen.json` 沒有新增，也沒有改動任何既有條目**。

## 改掉的 8 條

### 一、最重的一處：「拆開比較快」沒有來源，而且與唯一的來源相反（4 個編輯點）

草稿在四個地方寫拆給多個模型會更快：`description`「更省錢、**更快**」、
導言第一段「通常比全部丟給同一個模型更省錢、**更快**」、摘要第一句「在成本、**速度**與抓錯上都比只用一個模型有利」、
以及第一節第三段「省下來的錢、**換來的速度**到底有多少」。

今天重讀的原文寫的是相反方向：

- prompt chaining 那一節：`The main goal is to trade off latency for higher accuracy, by making each LLM call an easier task.`
- 文章開頭的通則：`Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.`

也就是官方把拆開寫成**拿延遲去換正確率**，沒有任何一句支持「更快」；
`sources[]` 另外兩頁只有各模型自己的延遲比較，沒有比較「拆 vs 不拆」。
本站也沒有實測。依 BRIEF「沒實測就寫本站沒有實測」與 FACTCHECK 1.4，四處全部改掉：

- `description` → 「可以讓便宜的模型分擔簡單的部分，也更容易看出是哪一步出了問題，**但不保證變快**。」
- 導言 → 「通常比全部丟給同一個模型**省錢**，也更容易看出是哪一步做得不好。」
- 摘要 → 「通常在成本與抓錯上比只用一個模型有利，**速度則不一定變快**，拆法也要看依據……」
- 第一節第三段 → 「省下來的錢、**多出來的延遲**到底有多少、怎麼估算」（那篇的標題本來就是《成本、品質、延遲》）
- 並在第一節補一句依據：「Anthropic 講這種一步接一步的做法時寫的是把每一次呼叫變簡單，用延遲換取更高的正確率，**本站沒有實測過哪一種拆法比較快**。」

研究紀錄加了這條 verbatim，並在 `must_not_write` 留下擋板，避免翻譯或改稿階段再犯。

### 二、`prompt chaining` 的譯名與站內既有文章不一致（撰稿代理點名要看的句子）

草稿譯成「**提示鏈**」。全站 `content/` 只有這一篇這樣寫；
`ai-term-prompt-chaining` 的 zh-TW title 是「**提示詞串接**（Prompt Chaining）是什麼」，
`ai-workflow-basics`、`ai-term-prompt-engineering`、`ai-terms-index` 也都用提示詞串接（共 11 處）。
已改為「提示詞串接（prompt chaining）」。附帶效果：`autolink` 比對的是詞彙別名而不是標題，
改了之後這個詞才連得到既有的詞彙篇。

同一句的定義也對緊了原文：`Prompt chaining decomposes a task into a sequence of steps,
where each LLM call processes the output of the previous one.`
草稿「把任務拆成一串步驟，讓**一次**模型呼叫處理前一次呼叫的輸出」漏掉 `each` 的分配語氣，
已改成「把任務拆成一**連串**步驟，**每一次**模型呼叫都處理前一次呼叫的輸出」。

### 三、`orchestrator-workers` 被接到不是它的例子上（撰稿代理點名要看的句子）

譯名本身**沒有問題**：`orchestrator-workers` 譯「協調者與工作者」與站內
《代理協調（Agent Orchestration）是什麼》的用語一致，定義句也逐字對得上
`In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks,
delegates them to worker LLMs, and synthesizes their results.`（中樞／動態／分派／彙整四個要素都在）。

**問題在歸屬**：原文把這個工作流程的關鍵界定寫成
`subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.`，
適用情境是 `complex tasks where you can't predict the subtasks needed`。
而草稿緊接著舉的例子（一個模型讀訂房信、一個模型排版，「兩個模型同時進行，不必等誰先做完」）
是**事先就分得出來、還能同時跑**的分工——那在同一篇文章裡屬於另一個工作流程：
parallelization 底下的 `Sectioning : Breaking a task into independent subtasks run in parallel.`
已在定義句後補一句把兩者切開，並把 sectioning 那條 verbatim 寫進研究紀錄。

### 四、`worker LLMs` 被寫成「子代理就是別的模型」，與必連文章矛盾

草稿：「被分派工作的**那些模型**，則是《子代理（Subagent）是什麼》說的角色。」
`ai-term-subagent` 的前幾段寫的是「最值得注意的是**委派關係**，而不是把它想成較小或較笨的模型。
同一個模型也能在不同任務狀態下扮演主代理與子代理」，description 也寫「它**不一定使用不同模型**」。
已改成「被分派工作的**那一端**，扮演的則是《子代理……》說的角色，
那篇強調重點是委派關係，**不一定要換一個模型**」——仍是一句帶過，但不再與那篇對撞。

### 五、`Specialized models` 那一句把兩家頁面的結構講錯了（撰稿代理點名要看的句子）

譯名「專用模型」**站得住**：OpenAI 自己的一句話就是 `Specialized models Purpose-built for specific tasks.`，
專用＝為特定任務打造。已補上英文原名讓讀者對得回去。

但草稿寫「Claude 與 OpenAI 的模型文件也都把一般的**旗艦、中階、輕量**模型，跟另外列出的一組專用模型分開處理」——
兩家頁面都不是這樣分的：

- OpenAI 這一頁把 GPT-6 Astra、GPT-5.6 Sol、Terra、Luna **四個都放在 `Flagship models` 底下**，沒有三階分欄。
- Claude 這一頁的比較表是四個通用模型並列，`Specialized models` 是**側邊目錄的一個分組**（底下是 Claude Mythos 5.1 與 Claude Mythos 5），不是比較表的一欄。

旗艦／中階／輕量是本站《同一家為什麼有好幾個模型》的框架，不是這兩頁的框架。
已改寫成「把日常在用的那幾個通用模型，跟另外一組專用模型（specialized models）**分開列**」，
研究紀錄兩條相關事實也各補一句說明頁面實際長相。

### 六、`routing` 的定義漏掉 `specialized`（撰稿代理點名要看的句子）

原文：`Routing classifies an input and directs it to a specialized followup task.`
草稿：「先把輸入分類，再導向**對應的**後續處理」——`specialized` 不見了。
已改成「把一筆輸入分類，**導向專門處理它的後續任務**」。

至於「依風險切」把 easy/hard 改敘成**後果大小**：**沒有失真，維持原判斷**。
草稿是先照原文報 easy/common → 較小較省成本的模型、hard/unusual → 更強的模型，
再明講本篇的切法看的是別的東西，兩者是分開的，不是把官方例子改寫成後果。
只把接縫講得更硬：「**要提醒的是官方那個例子分的是題目難易，這篇的依風險切看的則是答錯的後果大小**」。
原例裡的舊模型名（Claude Haiku 4.5／Claude Sonnet 4.5）確實只留在研究紀錄的 `verbatim_quote`，正文沒有點名，正確。

### 七、「沒有一個模型同時是所有事情的專家」是沒有來源的全稱否定

依 FACTCHECK 1.5，全稱否定要有出處。已換成兩家官方文件自己說的話，並各補一條 verbatim：

- Claude：`If you're unsure which model to use, start with Claude Opus 5 for most workloads.`
- OpenAI：`Choose GPT-5.6 Terra to balance intelligence and cost, or GPT-5.6 Luna for cost-sensitive, high-volume workloads.`

改成「Claude 與 OpenAI 的模型文件自己就列出好幾個模型，也各自建議不同性質的工作挑不同的模型」。
同一段的「好抓錯」也補上依據：`on any intermediate steps to ensure that the process is still on track.`
（正文寫「可以在中間任何一步加上程式檢查，確認流程還在正軌上」）。

### 八、「秒答」是沒有實測的回應時間宣稱（2 個編輯點）

正文「可以讓輕量模型**秒答**」→「交給輕量模型回答就好」；
表格同一列「行程問題**秒答**」→「行程問題交輕量模型」（表格與正文同步）。
同段保留的「便宜、快的模型」有頁面依據，已補一條 verbatim：
`Claude Haiku 4.5 The fastest model with near-frontier intelligence`（價目表上最便宜的那個就是頁面上標最快的那個）。

## 查過而且正確的部分（沒有動）

- **四個 Anthropic 例子逐字對得上**：先寫文案再翻譯（`Generating Marketing copy, then translating it into a different language.`）、
  先寫大綱確認合格再寫全文（`Writing an outline of a document, checking that the outline meets certain criteria, then writing the document based on the outline.`）、
  easy/common 導向較小較省成本的模型、hard/unusual 導向更強的模型。
- **研究紀錄原有 8 條 `verbatim_quote` 今天全部命中**（連續字串比對，不是拼接）；
  新增的 7 條也各自命中後才寫入，共 15 條、0 條落空；每條 `url` 都在 `sources[]` 內。
- **界線**：沒有 API 接法、沒有成本估算表、沒有路由或級聯的實作、沒有本機模型安裝步驟——
  四件事都只用一句話點名到對應的篇目，與指派的切角一致。
- **必連三篇各只一句帶過**：`ai-model-tiers-explained`（第一節第二段）、
  `ai-term-agent-orchestration` 與 `ai-term-subagent`（第三節同一句的兩個分句），沒有整段重講；
  第二個結尾 link 的 text 逐字等於 `ai-model-tiers-explained` 的 zh-TW title，
  第一個逐字等於系列目錄標題，兩個 URL 都沒有查詢字串。
- **`ai-workflow-basics` 的銜接正確**：那篇 `display_order` 400、title 逐字就是草稿寫的
  「AI 工作流是什麼：從一次對話到可重跑的流程」，「上一篇」成立；那篇確實用對話、流程、代理三層來分，不矛盾。
- **一個 callout、沒有免責聲明**；沒有訂閱、購買或投資建議；沒有「台灣可用」；
  沒有沒歸因的廠商宣稱（每一句 Anthropic／Claude／OpenAI 的話都寫了是誰說的）。
- **資料敏感度那一節沒有替任何一家服務背書**：草稿只寫「以你要用的那個服務當下的官方頁面為準」，
  沒有斷言誰會不會拿資料訓練模型、保留多久——這正是不該寫死的部分，維持原狀。
- 圖解與表格 caption 都寫「2026 年 9 月查證」，與 `checked_on` 一致；
  圖上與摘要都沒有數字（檢查器的數字比對因此無事可對）；`hero_label` 11 字，在 12 字上限內。

## 留給站主的事

1. 正文用《…》點名了**兩篇還沒寫、標題是撰稿者自己取的**文章：
   《Claude Code、Codex、Gemini CLI 分工：規劃、執行、審查》（`ai-workflow-coding-agents-division`）與
   《本機開放權重模型與雲端模型混搭》（`ai-workflow-local-and-cloud-mix`）。
   指派只給了這兩篇的 slug、沒有給標題。那兩篇定稿若換標題，這裡要回頭改。
2. **括號體例不一致**：`ai-workflow-basics` 點名兄弟篇用「…」，這篇用《…》。
   `autolink` 比對的是詞彙別名不是標題，兩種都不影響連結，但系列讀起來會不一致，請站主定一種。
3. `ai-workflow-basics` 文末預告這篇時寫的是「一件事拆給多個模型：**四種切法**」，
   與這篇實際標題（「……依步驟、能力、風險、資料敏感度四種切法」）不同。那個檔不在本次可動範圍。
4. Claude 模型文件目錄的 `Specialized models` 底下是 Claude Mythos 5.1 與 Claude Mythos 5，
   但**這一頁沒有印出它們的 API id**，所以沒有加進 `models-seen.json`（依規定不憑記憶寫 id）。
   之後哪一篇要點名，得先開個別模型頁查 id 再補進清單。

## 自檢

```
cd apps/api && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/bin/python3 \
  ../../docs/ai-workflow-series/check_article.py ai-workflow-split-tasks-across-models

WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-split-tasks-across-models paragraphs 2806 code_blocks 0 sources 3
```

`raw_internal_url` 是預期的：結尾兩個純 link 由協調者 `relink`。
字數 2,806（改前 2,524），在 1,800–3,000 內；沒有為了湊字數刪掉任何但書或限定詞，
新增的字全部是補回來源寫過的限定條件。兩個 JSON 都是 2 格縮排、不跳脫中文、LF、檔尾一個換行。

## 結論

**needs_owner**。

事實錯誤改了 8 條 11 處，其中「拆開比較快」（4 處）與 `orchestrator-workers` 的歸屬
是會誤導讀者的兩處，其餘是譯名、限定詞與全稱否定。
骨幹論述（四種切法、決策順序、四個判斷依據）查下來站得住，沒有換掉，
也沒有動任何程式範例（本篇沒有），所以不需要第二輪。
剩下的四件事都要站主決定：兩篇未寫文章的標題、括號體例、`ai-workflow-basics` 的預告標題，
以及 Mythos 的 id 要不要補進 `models-seen.json`。
