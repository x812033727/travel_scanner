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

## 2026-10 更新的查核

查核代理：未參與撰稿，也沒有參與九月那一輪。查核日 **2026-10-04**。
這次查的是撰稿者加進目錄篇的「搭本機模型」一節（E 組六篇）、表格六列、導言／`description`／summary／FAQ 的補句、
五格圖解，以及六條 `sources` 的重讀與兩條 OpenAI 網址的更換。

**`checked_on` 2026-10-03 不改**：內容包六條 source、研究紀錄的 `checked_on` 與它的六條 source、
表格 caption、圖解 caption（2026 年 10 月）與研究紀錄 `diagram.caption` 全部一致；
本代理 10-04 重抓的六頁內容與撰稿者記下的一致，本輪沒有依今天的頁面改任何外部事實，所以照規格不動日期。

查核方式：`sources[]` 六條以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；兩條舊的 OpenAI 網址與 MCP 入口另以不跟轉址的請求看狀態碼；
研究紀錄六條 `verbatim_quote` 照 FACTCHECK.md 第 1 節第 8 點的固定方法（刪掉 `<script>`／`<style>`、其餘標籤刪成**空字串**、
HTML 實體還原、空白正規化成一個空格後做子字串搜尋）**綁回各自的 url** 比對；
十八篇的 zh-TW `title` 與目錄篇的 `article` inline、表格「篇名」欄用腳本逐字比對；
E 組六篇逐句對回各篇的 `description`、summary、正文、表格與 FAQ；既有十二篇抽查三分之一
（《成本、品質、延遲》——九月之後 09-24 改過旗艦價、《本機去識別化、雲端收尾》、《一個 MCP 伺服器…》、《失敗案例與防護》）；
讀者看得到的每個欄位（title、description、段落、h2、summary、表格每列與 caption、callout、FAQ、圖解 alt 與 caption，
外加研究紀錄的 `hero_label`、`diagram`）用正規表示式掃篇數、路線數、組數、第 N 篇、中文與阿拉伯數字，以及「實測」。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**；沒有用 `sources[]` 以外的網址替文章補事實
（為了反駁而讀的兩頁見下，只寫進報告）。

檢查的主張：**119 條**（`description` 補句 1、導言補句 2、summary 第五句 5、新 h2 1、新一節的導句 2 與六篇描述 23、
新六列表格 18 格＋caption 1、新 FAQ 問句 1 與答句 5、圖解 alt 與 caption 2、`diagram` 五格 10＋title 1＋`hero_label` 1＋
`editorial_brief`／`must_not_write` 2、十八篇 inline 與表格篇名逐字 36、抽查既有四篇的段落描述與表格列 8），
外加六條來源重抓與六條引文。**改了 6 處**（內容包 6 個編輯點，研究紀錄另加 `factcheck.update_2026_10`），另有 4 件留給協調者或站主。

### 重抓結果：六條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `anthropic.com/engineering/building-effective-agents` | 200 | 173,726 | **是**。`<title>`「Building Effective AI Agents \ Anthropic」，可見文字約 19,800 字元；擋阻字串 0 次。比九月的 211,506 bytes 小，但引文與上下文都在 |
| `openai.github.io/openai-agents-python/` | 200 | 76,263 | **是**。`<title>`「OpenAI Agents SDK」；擋阻字串 0 次 |
| `modelcontextprotocol.io/docs/getting-started/intro` | 200 | 310,416 | **是**。入口今天 **307** 到 `/docs/2026-07-28/getting-started/intro`（九月記的是 302），落地頁 `<title>`「What is the Model Context Protocol (MCP)? - Model Context Protocol」；擋阻字串 0 次 |
| `developers.openai.com/api/docs/guides/structured-outputs` | 200 | 3,275,351 | **是**。直接 200、沒有再轉址；`<title>`「Structured model outputs \| OpenAI API」；擋阻字串 0 次 |
| `docs.litellm.ai/docs/` | 200 | 117,514 | **是**。`<title>`「Getting Started \| liteLLM」；擋阻字串 0 次 |
| `developers.openai.com/api/docs/guides/evals` | 200 | 746,824 | **是**。直接 200；`<title>`「Working with evals \| OpenAI API」；擋阻字串 0 次 |

**兩條換了網址的 OpenAI 頁面**：`platform.openai.com/docs/guides/structured-outputs` 與 `…/evals` 今天不跟轉址各回
**301**，`Location` 分別是 `https://developers.openai.com/api/docs/guides/structured-outputs` 與 `…/evals`；
新網址本身回 200、不再轉址，是 OpenAI 自己的開發者文件網域，`<title>` 都帶「OpenAI API」，正文讀得到。
換成最終網址成立；研究紀錄 `unverified_or_excluded` 對這件事的記載（301、MCP 307 仍記入口網址）與今天的觀察一致。

**六條 `verbatim_quote` 全部 FOUND**（各自只在自己的 url 上搜尋）。evals 那條在原始 HTML 裡被 `<strong>evals</strong>` 切開，
標籤刪成空字串後是連續字串，與九月的結論相同。

### 十八篇標題逐字比對（腳本）

- `article` inline：十八個系列 slug 各出現一次，**18／18 逐字等於**各篇當下的 zh-TW `title`，沒有缺、沒有重複。
  另外兩個非系列 inline（「MCP」→ `ai-term-model-context-protocol`、「評測」→ `ai-term-evals`）的內容包都存在。
- 表格「篇名」欄：**18／18 逐字相同**。表格與段落的排序依路線分組（營運在協作與工具之後、搭本機模型最後），
  不是 `display_order`，與九月相同。
- 《Claude Code、Codex 搭本機模型的注意事項：開工前的檢查清單》第一輪查核的結論是 `needs_second_round`；
  本代理開工與收工各比對一次，title 都沒變。

### 改掉的 6 處（內容包）

1. **批次腳本那一句把 Codex 路寫成「讓代理執行」，也拿掉了 beta。**
   原文：「《讓 Claude Code、Codex 把大量雜務交給本機模型：一支 Python 腳本》**示範讓代理去執行**一支 Python 腳本，由腳本逐封問…，
   也寫了 **Claude Code 與 Codex 各自擋得住原始檔到什麼程度**…」。
   那篇的 summary 第四句與 FAQ 寫，Codex 的 permission profile 連沙盒裡執行的腳本也擋，所以「Codex 這一條路是**先由你跑腳本**，
   再讓 codex exec 只讀 out」；擋原始檔的分別是 Claude Code 的 Read deny 規則（那篇稱它「是護欄，不是邊界」）與
   Codex 的 permission profile，後者那篇寫「官方 Permissions 頁標示它是 beta」——本代理今天另讀 Codex 的 Permissions 頁，
   原文是「Beta. Permission profiles are under active development and may change.」（只寫進報告，不是目錄篇的來源）。
   已改成「示範**把一批文字檔交給一支 Python 腳本**，由腳本逐檔問本機的 Ollama 模型…，也寫了 **Claude Code 的 deny 規則與
   Codex 的 permission profile（文件標示為 beta）**各擋得住原始檔到什麼程度…」。
2. **表格同一篇那一列**「寫一支…Python 腳本**讓代理執行**」同理改成「…Python 腳本**逐檔問本機模型、代理只讀結果**」。
3. **整個換成本機那一句的「官方給的上下文門檻」與「怎麼確認現在連到的是誰」。**
   兩種接法那一篇明寫「64k 是 Ollama 給代理的建議值，不是 Claude Code 或 Codex 規定的門檻」，LM Studio 寫的是超過約 25k；
   目錄篇不帶歸因寫「官方給的門檻」，讀起來像代理工具本身的規定。同一句的確認方法，那篇正文寫
   「Codex 這邊，兩份文件都沒寫對應的確認指令」，只有 Claude Code 的 /status。
   已改成「寫出 Ollama 與 LM Studio 的指令、**這兩家文件建議的上下文長度**、**怎麼用 /status 確認 Claude Code** 現在連到的是誰，以及用完怎麼還原」。
4. **表格同一篇那一列**「確認上下文與現在連到誰」同理改成「確認上下文與 **Claude Code** 現在連到誰」。
5. **MCP 工具那一句「列出兩邊逾時與輸出量的官方預設值差在哪裡」。**
   那篇表格的輸出量一列，Codex 那格寫「tools 底下單一工具的 output_token_limit（token 預算）；本文查證的那一頁**沒有寫預設的數字**」；
   兩邊都有預設值的只有逾時。已改成「並列出兩邊**逾時**的官方預設值差在哪裡、**輸出量又各怎麼管**」。
6. **三個家族那一句「讓你不會把雲端端點誤當成本機」把兩種雲端併成一個詞。**
   那篇的骨幹是三種跑法分開：權重在自己電腦、Ollama 的 `:cloud` 標籤、供應商自己的端點；它的 callout 最強調的陷阱
   正是「這兩個雲端模型頁的 curl 範例，連的就是 http://localhost:11434，模型卻是帶 cloud 的標籤」——那不是「端點」。
   已改成「讓你不會把 **:cloud 標籤或供應商端點**誤當成本機」。

六處都只動描述的範圍，沒有改路線分法、篇目歸屬或任何一篇的定位；正文 2,456 → 2,515 字，沒有刪任何但書或限定詞。

### 撰稿者請優先重看的三件

- **兩種接法那一句的 Anthropic 說法：成立，不改。** 目錄篇只寫那篇「對照 Anthropic、Ollama、LM Studio 與 OpenAI 的官方文件怎麼寫，
  包括 **Anthropic 的文件對把 Claude Code 接到非 Claude 模型的說法**」——只點出那篇有這一段，沒有轉述內容、沒有下結論、
  沒有「違反條款」或「不合法」這類字。那篇正文與 FAQ 都寫成「Claude Code 文件的 LLM gateway 頁寫，Anthropic 不支援透過任何 gateway
  把 Claude Code 接到非 Claude 模型」並加「不對條款做解讀」。本代理今天讀 `code.claude.com/docs/en/llm-gateway`，
  原文「doesn’t support routing Claude Code to non-Claude models through any gateway」仍在（只寫進報告）。
- **批次腳本那一句：改了**，見上面第 1、2 處。
- **新 FAQ 的「它不需要寫程式」：成立，不改。** 兩種接法那篇第二段導言原句是「讀完你會有一張兩種接法的對照表和三個選路的問題，
  不需要寫程式」，那篇是入門篇。它有一個 bash 區塊，但內容是照抄 Ollama 文件的入口與 `ollama ps` 指令，不是要讀者寫程式；
  FAQ 下一句隨即把要寫腳本的工作指向批次腳本與 MCP 工具那兩篇，不會讓人以為接法一不用程式。正文同一處的寫法相同，也不改。

### 查過而且正確的部分（沒有動）

- **本機與雲端沒有混淆。** 新一節與表格、summary、FAQ 提到 GLM、Qwen、DeepSeek 時，一律寫成「標籤哪些能下載到自己電腦、
  哪些只有 :cloud（或其實在雲端）」，沒有一處寫三家都能在本機跑；供應商端點只出現在「整理供應商自己的端點怎麼接…，
  每一處都標明資料會送到哪裡」，沒有暗示資料留在本機（那篇 `description` 原句就是「每一處都標明資料會送到哪裡」）。
  批次腳本、MCP 工具兩句的「本機的 Ollama 模型」與那兩篇的位址＋標籤檢查一致。研究紀錄 `must_not_write` 第二條也寫了這條界線。
- **不實測的揭露**：「本站沒有實測」全篇只出現 **1** 次（新一節的導句）；title 與 `description` 沒有「實測」；
  全篇沒有速度、品質、價格、購買或訂閱建議、沒量過的排名（callout 的「價格…以那篇當天讀到的官方頁面為準」不是價格）。
  導句「這一節各篇的步驟都來自官方文件」與六篇各自第二段導言的揭露一致（六篇都有且只有一次「本站沒有實測」）。
- **會長大的數字**：掃過所有讀者看得到的欄位，命中的只有各篇內容本身的固定數量——三個層次、四種切法、三個量、三支命令列代理、
  三個客戶端、兩版、三種常見失控、Claude Code 與 Codex「兩邊」、Ollama 與 LM Studio「這兩家」、FAQ 點名「講兩種接法怎麼選的那一篇」
  （出自那篇標題的主題），以及 caption 的「2026 年 10 月」。沒有篇數、路線數、組數或「第 N 篇」；FAQ 用「那幾篇」「這幾個家族」帶過。
  `hero.alt` 的三個「四」見留給協調者的第 1 件。研究紀錄的 `diagram.title`「系列的各條路線」、`hero_label`「各條路線導讀」、
  `editorial_brief`「這幾條路線」、`must_not_write` 第一條都已拿掉數量。
- **E 組六篇的其餘描述對得上**：兩種接法的三個判準（資料能不能出門、上下文開得夠不夠長、工作的類型）與那篇導言相同；
  三個家族那篇確實逐家寫 Ollama 標籤與 Z.ai、DeepSeek、阿里雲百鍊的端點；MCP 工具那篇是 stdio 伺服器、兩邊各登記一次、
  只回分類結果與結果檔路徑；整個換成本機那篇有 Ollama 與 LM Studio 的指令與 `ollama launch codex --restore` 還原；
  檢查清單那篇是一張表、每項一句怎麼檢查、最先查資料、憑證（現在連的是誰）、上下文與驗收四件事。
  summary 第五句、導言兩處補句、`description` 補句、新 FAQ 的答句都 ⊆ 正文。
- **既有十二篇抽查四篇**：段落描述與表格列和各篇當下的 `description`、summary、正文一致
  （《成本、品質、延遲》09-24 改的是旗艦定價，目錄篇只寫「比較單一旗艦、級聯與並行互審幾種架構的代價」，不受影響）。
- **圖解**：研究紀錄 `diagram.layout` 是 `flow`、五格；`diagram.caption` 與內容包 image 的 caption 逐字相同（自檢也比對）；
  五格小標「觀念／接線／協作與工具／營運／搭本機模型」與表格「路線」欄、五個 h2 的開頭字詞同一組字；
  第五格「選接法、分本機雲端」對得上兩種接法與三個家族兩篇，小標 5 字、說明 9 字都在上限內；五格沒有任何數字。
  image 的 alt 與 caption 已拿掉「四條路線」。
- **依賴外部事實的句子**：目錄篇正文沒有自己的外部事實句，新一節每一句都是「某篇教什麼」。其中兩處帶到外部文件的說法
  （Anthropic 對接非 Claude 模型的說法、Codex permission profile 的 beta 標示）都寫成那一篇的內容，本代理另讀官方頁確認原文仍在。
- **研究紀錄與內容包一致**：`title`、`sources`（六條的順序、標題、網址）、`diagram.caption` 相同；六條 `verified_facts` 的 url 都在 `sources[]`。
- **界線**：沒有購買、訂閱或投資建議，沒有推薦式比價，沒有沒歸因的廠商宣稱，只有一個 callout、沒有免責段落，沒有寫台灣可用。

### 留給協調者／站主

1. **`hero.alt`**（協調者）：仍寫「一張書桌中央延伸出四條路徑，分別通往觀念、接線、協作與工具、營運四個標示牌，代表這個系列的四條路線」，
   有三個「四」，也缺搭本機模型這條路線。主圖由協調者重畫與改寫，本代理依指示沒有動。
2. **兩篇自己的 `description` 比正文鬆**（各篇的查核範圍，本代理只讀）：
   《讓 Claude Code、Codex 把大量雜務交給本機模型：一支 Python 腳本》寫「可以讓 Claude Code 或 Codex 去執行」那支腳本，
   正文的 Codex 路卻是先由你跑腳本；《把 Claude Code、Codex 整個換成本機模型：Ollama 與 LM Studio 設定與還原》寫
   「官方給的上下文門檻」「確認現在連到誰的方法」，正文寫 64k 是 Ollama 的建議、Codex 兩份文件都沒寫確認指令。目錄篇已照各篇正文寫。
3. **檢查清單的第二輪**（協調者）：若第二輪改了 title，目錄篇的 inline 與表格篇名兩處要跟著改。
4. **sources 與新一節沒有對應**（站主）：六條 sources 都屬既有十二篇的主題；新一節只描述各篇、沒有外部事實句，所以不需要新來源。
   若希望來源涵蓋這一組，加進來的會是正文沒有句子靠它支撐的來源。

### 懷疑但沒動

- SeriesHub 的組別（`build_catalogue.py` 的 `GROUPS`：A 觀念、B 接線、C「協作：互審、代理分工與 MCP」、D「營運：本機混搭、追蹤與防護」、
  E「實作：代理工具搭本機模型」）按 `display_order` 每三篇一組，與目錄篇正文的路線分法（互審在營運、本機去識別化在協作與工具）不同。
  這是九月就有的差異，E 組前後兩邊都把那六篇放在一起，沒有讓它更糟；不在本代理可改的檔案裡。
- 圖解 caption 與 alt 的「各條路線各自要解決的問題」，「各」與「各自」重複，是文字問題不是事實問題；改它要同步研究紀錄，沒有動。

### 自檢

```
OK ai-workflow-tutorials paragraphs 2515 code_blocks 0 sources 6
```

無 FAIL、無 WARN。段落字數 2,515（hub 900–3,000；改動前 2,456）。

### 結論

`ok`。改了 6 處，都是目錄篇對 E 組三篇的描述說得比那一篇滿（Codex 路、beta、官方門檻、確認指令、輸出量預設值）或把兩種雲端併成一個詞；
沒有動骨幹、路線分法或篇目歸屬。十八篇標題逐字相同，六條來源今天都讀到正文、六條引文都在，`checked_on` 全篇一致。
`models-seen.json` 未新增（目錄篇沒有模型 id）。
