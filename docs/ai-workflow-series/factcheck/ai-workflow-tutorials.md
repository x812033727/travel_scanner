# 獨立查核：ai-workflow-tutorials（系列目錄篇）

查核代理：未參與撰稿。查核日 **2026-09-19**（內容包六條 source 與研究紀錄的 `checked_on`
本來就是 2026-09-19、七處一致，而且確實是撰稿者與本代理都讀到來源的那一天，**不改**；
本輪沒有依今天的頁面改任何數字，所以沒有任何一條 source 的 `checked_on` 需要動）。

查核方式：`sources[]` 六條全部以 `curl -sL -A "Mokaair-editorial"` 今天重抓並讀 body；
研究紀錄六條 `verbatim_quote` **逐條綁回它自己的 `url`** 再做連續字串比對（不跨來源搜尋）；
十二篇的內容包逐一打開，把目錄篇 `article` inline 的 `text` 與各篇**當下**的 zh-TW `title`
逐字比對，再把表格那一列與路線段落裡對它的描述回貼各篇的 `description`、`summary` 與正文核對；
全篇（含 summary、表格、FAQ、callout、caption、description）以正規表示式掃過篇數與課序寫法。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

檢查的主張：**132 條**（title 1、description 1、導言兩段 6 句、summary 4 句、
四段路線 23 句／子句、表格 36 格＋表頭 3＋caption 1、callout 4 項、FAQ 3 題共 6 句、
圖解 alt 與 caption 2＋diagram 四格 8＋`hero_label` 1、十二篇 inline 逐字比對 12＋
十二列篇名逐字比對 12），外加研究紀錄 6 條事實與 6 條引文。
**改了 7 條**（內容包 12 個編輯點，研究紀錄 `diagram` 5 個），另有 3 件留給站主。

## 重抓結果：六條 sources 今天都讀到正文，不是擋阻頁

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `anthropic.com/engineering/building-effective-agents` | 200 | 211,506 | **是**。`<title>` 為「Building Effective AI Agents \ Anthropic」，`Workflows are systems where LLMs and tools are orchestrated through predefined code paths.`、`Prompt chaining`、`Orchestrator-workers` 都在；擋阻字串（`Access Denied`／`Request Access`／`Just a moment`）**0** 次 |
| `openai.github.io/openai-agents-python/` | 200 | 76,263 | **是**。`<title>` 為「OpenAI Agents SDK」，`lightweight, easy-to-use package with very few abstractions`、`Handoffs`、`Guardrails`、`Sessions` 都在；擋阻字串 **0** 次 |
| `modelcontextprotocol.io/docs/getting-started/intro` | 200 | 290,696 | **是**。`curl -L` 最終落在 `modelcontextprotocol.io/docs/2026-07-28/getting-started/intro`；`<title>` 為「What is the Model Context Protocol (MCP)? - Model Context Protocol」，`MCP is an open protocol supported across a wide range of clients and servers.` 在頁面上；擋阻字串 **0** 次 |
| `platform.openai.com/docs/guides/structured-outputs` | 200 | 3,253,904 | **是**。轉址到 `developers.openai.com/api/docs/guides/structured-outputs`；`<title>` 為「Structured model outputs \| OpenAI API」，`Structured Outputs is a feature that ensures…`、`json_schema`、`response_format`、`Supported models` 都在；擋阻字串 **0** 次 |
| `docs.litellm.ai/docs/` | 200 | 106,555 | **是**。`<title>` 為「Getting Started \| liteLLM」，`LiteLLM is an open-source library that gives you a single, unified interface to call 100+ LLMs…`、`completion(`、`LiteLLM Proxy` 都在；擋阻字串 **0** 次 |
| `platform.openai.com/docs/guides/evals` | 200 | 729,709 | **是**。轉址到 `developers.openai.com/api/docs/guides/evals`；`<title>` 為「Working with evals \| OpenAI API」，`Evaluations (often called <strong>evals</strong>) test model outputs…`、`graders`、`dataset` 都在；擋阻字串 **0** 次 |

**MCP intro 的轉址（協調者點名的一項）**：入口網址 `…/docs/getting-started/intro` 今天 302 到
帶日期的 `…/docs/2026-07-28/getting-started/intro`。內容包與研究紀錄**都記入口網址、兩邊一致**，
落地頁 HTTP 200 且有正文，符合指派給的兩種寫法之一，**不改**。
（兩條 OpenAI 文件同理：`platform.openai.com` 轉到 `developers.openai.com`，記的是原始入口。）

**六條 `verbatim_quote` 全部通過連續字串比對。** 其中 `Evaluations (often called evals) test model
outputs to ensure they meet style and content criteria that you specify.` 在原始 HTML 裡被
`<strong>evals</strong>` 切開，**渲染後的可見文字逐字相同**，是可搜尋到的連續字串，**不是拼裝品**，
不需要更動。

## 程式範例重驗

**無 code。** 目錄篇沒有 `code` 區塊（檢查器對 hub 也不要求），研究紀錄 `code_samples` 為 `[]`，
`factcheck.code_recompiled` 亦為 `[]`。全篇沒有可編譯的識別字、參數名、旗標或端點需要比對。

## 改掉的 7 條

### 與各篇對不上的三處（最重的三處）

1. **路線一把《一件事拆給多個模型》擺在「已經決定要拆」之後，與那篇和本篇自己的表格都矛盾。**
   原文：「…才看得出一件事目前卡在哪一層。**決定要拆之後**，《一件事拆給多個模型：依步驟、能力、
   風險、資料敏感度四種切法》整理出…四種切法，讓你照工作本身的性質**挑切法**，而不是憑感覺亂拆。」
   但那篇的 `description` 寫「重點是**先想清楚不拆會怎樣**，能一個模型做完的步驟就不必拆」，
   `summary` 第一句也寫「拆法也要看依據，**不是拆得越細越好**」；
   **本篇表格同一列**更是寫著「用…四種依據，**決定要不要拆**、怎麼拆給不同模型」——
   同一篇文章的表格與段落互相打架。
   （另外「決定要拆之後」在下一段開頭**原樣再出現一次**，是重複句。）
   已改成「**接著要判斷該不該拆、又該怎麼拆**，《…》整理出…四種切法，讓你照工作本身的性質
   **決定要不要拆、又該挑哪一種切法**，而不是憑感覺亂拆。」
2. **「只換 base_url 與 model 字串」漏掉金鑰（兩處）。**
   路線二原文：「《統一 API 層：OpenRouter 與 LiteLLM 換模型不改程式》示範同一段程式**只換**
   base_url 與 model 字串，就能連到別家模型。」表格第四列同樣寫「靠換 base_url 與 model 字串」。
   但那篇的 `description` 逐字寫的是「程式只要換 **base_url、金鑰與 model 字串**就能連到別家模型」，
   `summary` 第四句也寫「換供應商時，**金鑰要放的環境變數名稱**與 model 字串的寫法都不同」，
   正文那段更直接寫「只有 base_url、**金鑰讀的環境變數**，以及 model 字串**三個地方**不一樣」。
   目錄篇的「只」把三件事寫成兩件。已改成「示範同一段程式**換掉 base_url、金鑰與 model 字串**，
   就能連到別家模型」，表格那一格同步補上金鑰。
3. **summary 第三句誤述《本機去識別化、雲端收尾》。**
   原文：「…以及同一支 MCP 伺服器**與同一套去識別化流程**怎麼同時給多個客戶端**或本機與雲端共用**。」
   那篇根本不是「本機與雲端共用同一套去識別化流程」，而是**把碰到原始個資的那一步留在本機**、
   換成代號的乾淨文字**才送進雲端模型收尾**（該篇 `summary` 第一句與本篇正文路線三都這樣寫）。
   「共用」在那篇裡會讀成原始個資兩邊都碰得到，正好是那篇要避免的事。
   已改寫成「…同一支 MCP 伺服器怎麼同時給多個客戶端共用，以及同一支程式怎麼把會碰到原始個資的
   步驟留在本機、乾淨的文字才交給雲端模型收尾。」（summary ⊆ 正文，逐句取自路線三那一段。）

### 其餘四條

4. **路線四把三種防護一律說成「會停下流程」。**
   原文：「…各自配一種對應的防護，**讓流程在還在跑的時候就先停下來**。」
   《失敗案例與防護》的第三種防護是**把上游輸出包成明確標示的資料再交下游**，
   那篇 `summary` 最後一句還特別寫「三個防護各自擋不同的失效模式」——包成資料並不會停住流程。
   已改成「**讓流程在失控之前就先擋下來**」。
5. **FAQ 第三題與 callout 高度重疊，而且答案不在正文裡（協調者點名的一項）。**
   原問句「這個系列的價格、模型 id 這些資訊，多久更新一次？」，答句「每一篇文章都在文中自己標好
   查證日期，價格、免費額度、速率限制與模型 id 都以那篇當天讀到的官方頁面為準…」，
   與 callout 第一句「這系列每一篇文章都自己在文中標好查證日期，價格、免費額度、速率限制與模型 id
   都以那篇當天讀到的官方頁面為準」**幾乎逐字相同**；而且這件事**只出現在 callout**，
   正文四段路線與兩段導言都沒有寫，違反「FAQ 答案 ⊆ 正文」，
   也踩到研究紀錄 `must_not_write` 第五條的「免責聲明式的重複提醒」。
   選擇**改寫而不是刪**（hub 的 faq 下限是 2 題，刪掉只剩 2 題會讓導覽變薄）：
   換成「接線的幾篇和協作與工具的幾篇，差別在哪裡？」，答案逐句取自正文路線二與路線三兩段
   （換 base_url、金鑰與 model 字串／路由與級聯／JSON Schema 驗證；規劃、執行、審查三個角色／
   同一支 MCP 伺服器登記進多個客戶端／哪一段留在自己的電腦上）。查證日期那件事仍留在 callout，
   全篇只講一次。
6. **兩個 h2 標題把該路線的文章數寫死在標題裡（協調者點名的一項）。**
   原本是「先懂**三個**觀念：拆解、切法與取捨」與「接線**三步**：統一介面、路由級聯、交接資料」。
   這兩節各自正好涵蓋三篇，「三個」「三步」實際上就是該路線的篇數；
   指派寫的是**不寫篇數、不寫課序（目錄由 SeriesHub 依 `display_order` 自動列）**，
   研究紀錄 `unverified_or_excluded` 第二條也自陳「正文刻意不寫篇數與課序編號」——
   日後這條路線多一篇，標題就變成錯的。
   已改成「**先懂觀念**：拆解、切法與取捨」「**接線**：統一介面、路由級聯、交接資料」。
   改完四個 h2 的開頭字詞是**觀念／接線／協作與工具／營運**，與表格「路線」欄的四個值完全一致
   （協調者問的「h2 要與路線欄一致」現在成立，而且不是靠語意近似，是同一組字）。
7. **圖解自成一套四格名稱，與表格「路線」欄對不上。**
   原本的 caption 與 alt 是「拆解任務、接線交接、協作與工具、追蹤防護**四個階段**」，
   研究紀錄 `diagram.nodes` 也是這四個名字。但表格「路線」欄是**觀念、接線、協作與工具、營運**，
   四個裡只有「協作與工具」相同——讀者無從判斷「階段」與「路線」是不是兩回事，
   而看起來只是同一組東西被取了兩次名字（主圖說明用的又是路線那一組）。
   已把節點小標換成四條路線的名字，第四格說明順帶補上**互審**
   （營運路線含《多模型互審：LLM 當評審、投票與集成怎麼做》，原本的「找錯誤、擋風險」只涵蓋
   追蹤與防護兩篇）：
   `[["觀念","看依據、算代價"],["接線","換供應商、串格式"],["協作與工具","代理分工、共用工具"],["營運","互審、追蹤、擋失敗"]]`。
   caption 與 alt 同步改成「觀念、接線、協作與工具、營運四條路線各自要解決的問題（查證：2026 年 9 月）」，
   研究紀錄的 `diagram.title`（「系列四個階段」→「系列四條路線」）與 `diagram.caption` 一併更新。
   四格裡**沒有任何數字**，不影響「圖上的數字都要在正文」這條。
   資產尚未產出（`apps/web/public/guides/ai-workflow-tutorials/` 不存在），研究紀錄仍是繪圖的依據。

## 查過而且正確的部分（沒有動）

- **十二篇的 inline text 逐字等於各篇當下的 zh-TW `title`**，十二列表格的「篇名」欄同樣逐字相同，
  十二個 slug 一個不漏、沒有多餘的。本輪在開工與收工各比對一次
  （期間 `ai-workflow-unified-api-layer.json` 被別的代理改過，但動的是正文與 FAQ，
  `title` 與 `description` 沒變，目錄篇不受影響）。
- **路線歸屬與 `ASSIGNMENTS.md` 完全相同**：1、2、3 觀念；4、5、6 接線；7、11、12 營運；
  8、9、10 協作與工具。表格十二列的排序也照這個分組，段落點名的順序與表格一致。
- **每篇的一句話回貼各篇 `description`、`summary` 與正文都對得上**，
  而且**沒有宣稱任何一篇沒有的東西**：沒有替任何一篇說有價目表、有某段範例、有官方規格。
  逐一確認過幾個容易出錯的：
  - 《Claude Code、Codex、Gemini CLI 分工》那句「靠檔案交接**而不是共用對話紀錄**」——
    那篇正文寫「三個階段互相看不到對方的對話紀錄，只能靠檔案交換結果」「彼此不共用登入」，成立。
  - 《一個 MCP 伺服器…》那句「不必改程式…只是每邊的設定檔與**白名單**要分開設定」——
    那篇正文寫「伺服器端完全不用改」，callout 標題就是「三邊的白名單要分開設定」，用字相同，成立。
  - 《多模型互審》那句「依照**寫死的**評分準則…**逐條**打分」——
    那篇第一段逐字是「依照寫死的評分準則，對另外一到多個模型的答案逐條檢查」，成立。
  - 《追蹤、評測與可觀測性》那句「**只用 Python 標準函式庫**自寫一支追蹤器」——
    那篇 `summary` 第二句列出 hashlib、json、time、functools、pathlib，成立。
- **callout 的「這系列每一篇文章都自己在文中標好查證日期」成立**：
  十二篇的表格或圖解 caption 都寫了查證年月（《成本、品質、延遲》寫到日：2026 年 9 月 18 日）。
- **全篇掃不到篇數與課序**：以 `[一二三四五六七八九十百0-9]+\s*篇`、`第\s*[一二三四五六七八九十0-9]+\s*[篇課章節步個]`、
  `十二`、`12` 掃過 title、description、導言、summary、四段路線、表格每一格與 caption、
  callout、FAQ、圖解 caption，命中的只有「一篇一篇拆開講清楚」「每一篇文章」這種不帶數量的說法，
  以及 caption 裡的年月 `2026 年 9 月`。改掉第 6 條之後，連隱含篇數的標題也沒有了。
- **界線檢查全部通過**：沒有訂閱、購買、升級或投資建議；沒有推薦式比價，全篇不出現任何價格與額度；
  沒有對 Claude Code、Codex、Gemini CLI、OpenRouter、LiteLLM、Ollama 任何一方做優劣評比或人身式褒貶；
  **沒有沒歸屬的廠商宣稱**——對供應商與協定的陳述一律寫成「《某篇》示範／講的是…」，
  由那一篇自己的來源負責；沒有把預告寫成已推出；沒有寫「台灣可用」。
- **只有一個 `callout`（`tip`）、沒有免責段落**；`topics` 是規定的三個；`news_date` 為 null；
  `display_order` 399；只有 zh-TW；**沒有 `link` 區塊**（hub 靠 inline article 連出去，符合檢查器）。
- **用語照 BRIEF 第 4 節**：路由、級聯、結構化輸出、代理（Agent）、追蹤、評測、防護、JSON Schema、
  fan-out 的寫法與十二篇一致；沒有出現「詞元」等非本系列用語；簡體字檢查由自檢通過。
- **summary ⊆ 正文**：四句每一句的說法都能在導言或四段路線裡找到（第三句改寫後才成立，見上）；
  summary 與圖解四格都不含數字，沒有「圖上有、正文沒有」的問題。
- **研究紀錄與內容包一致**：`title`、`sources`（六條的順序與內容）、`diagram.caption` 三處相同；
  六條 `verified_facts` 的 `url` 全在 `sources[]` 裡；`unverified_or_excluded` 四條、
  `must_not_write` 五條都不空；`hero_label`「四條路線導讀」6 字（上限 12）。
- **`checked_on` 2026-09-19** 在六條 source 與研究紀錄共七處一致，未更動。

## 留給站主的事

1. **《統一 API 層》自己的 `summary` 第一句仍寫「只換 base_url **或** model 字串」**，
   與同篇 `description`、`summary` 第四句與正文的「base_url、金鑰與 model 字串三個地方」鬆緊不同。
   目錄篇本輪已照那篇的 `description` 寫（補上金鑰）；**那篇內部要不要一致，屬於該篇查核代理的範圍**，
   本代理依規格沒有動十二篇的任何一個字。
2. **目錄篇帶六條 `sources`，但正文只做導讀、沒有直接引用它們。**
   撐住它們的是研究紀錄的六條 `verified_facts`（六條引文今天都重驗過）。
   檢查器要求 3–8 條，數量合法，所以沒有動；若站主希望目錄篇的來源與正文有更直接的對應，
   要改的是正文的寫法，不是刪來源。
3. **四條路線的用字**：本篇全篇統一用「協作與工具」，`ASSIGNMENTS.md` 的分組寫法是「協作／工具」，
   語意相同、只差一個連接符號。本輪把表格「路線」欄、四個 h2、summary、圖解四格與 caption
   都收斂到同一組字（觀念／接線／協作與工具／營運）。
   若站主要改用斜線寫法，這五個地方連同主圖的 `hero.alt` 要一起改
   （`hero.alt` 依規格不由查核代理動，目前寫的已經是「觀念、接線、協作與工具、營運」這一組）。

## 自檢

```
OK ai-workflow-tutorials paragraphs 1516 code_blocks 0 sources 6
```

無 FAIL、無 WARN。段落字數 **1,516**（hub 的範圍是 900–3,000；改動前 1,495），
title 22.2 單位（上限 60），description 183.4 單位（120–200），`sources` 6 條，`code` 0 塊，
表格 1、callout 1、圖解 1、FAQ 3 題（hub 允許 2–10）。

## 結論

`ok`。改了 7 條、內容包 12 個編輯點加研究紀錄 `diagram` 5 個，
其中三條是目錄篇對各篇的描述與那篇自己的 `description`／`summary`（或與本篇表格）對不上，
四條是內部一致性與規格（篇數寫法、FAQ 與 callout 重複、圖解自成一套名稱、防護以偏概全）。
**沒有換掉骨幹論述**：四條路線的分法、十二篇的歸屬與順序、每篇的定位都維持撰稿者原樣，
改的是把描述收回各篇撐得住的範圍，以及把四條路線的名字在表格、標題、圖解之間統一。
`models-seen.json` 未新增（目錄篇沒有模型 id）。不需要第二輪。
