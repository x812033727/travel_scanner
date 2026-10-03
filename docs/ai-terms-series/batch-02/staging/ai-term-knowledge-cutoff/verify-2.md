# 查核紀錄 2：ai-term-knowledge-cutoff

查核者：第二輪獨立查核（不是撰稿者，也不是第一輪查核者），2026-10-03。13 筆來源今天以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新開啟，全部 200 且不是空殼頁；三篇 arXiv 另讀 `arxiv.org/html/<id>` 全文。另外開了：已棄用的 Gemini 3 指南、Gemini 模型索引與 3.5 Flash、3.1 Pro Preview、2.5 Pro 模型頁、OpenAI 比較頁、COLM 2024 Accepted Papers、arXiv:2402.16797、arXiv:2202.05262。我沒有沿用前兩人的抓頁結果。

## 修改（每處一行：原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

1. 「不重新訓練模型的話，補上截止日之後的資訊只有一條路」→「不更動模型本身（例如重新訓練或微調）的話，要補上截止日之後的資訊只有一條路」；圖說「不重新訓練的話，補救只能……」→「不更動模型本身的話，補救只能……」；diagram-1.svg 小標「不重新訓練的話，截止日之後的內容只能放進上下文視窗」→「不更動模型本身的話，……」，`<desc>`「不重新訓練模型時」→「不更動模型本身時」｜**事實（計入）**：第一輪補上的「不重新訓練」仍然太絕對。知識編輯（knowledge editing）不重新訓練也能直接改權重、寫入特定事實，所以「不重新訓練就只剩上下文」不成立；「不更動模型本身」才是「只剩上下文」真正的前提。ROME 只作查核依據，沒有列入 sources｜https://arxiv.org/abs/2202.05262 （NeurIPS 2022：「we modify feed-forward weights to update specific factual associations」）；https://arxiv.org/html/2511.12116 （Introduction：「continually pretrained … and further finetuned」）
2. 「Daily Oracle 每天用新聞出真假題與選擇題，在不提供資料的設定下測多個模型。在幾個模型上，……」→「Daily Oracle 每天從新聞自動出預測題（真假題與選擇題），問某件事在某天前會不會發生、結果如何；答案在截止日之前就揭曉的題目，等於考模型記不記得已發生的事。在不提供資料的設定下，幾個模型……；截止日之後題目才真正要靠預測，……」｜**事實（計入）**：這套基準是預測題（「a continuously updated QA benchmark of forecasting questions」，例題都是「Will … by March 2024?」「What will be …」）。原句讀起來像在考新聞事實。論文用 resolution date 和知識截止日的先後分兩類：截止日前的題「testing the model’s understanding of past events」，截止日後的題才「requiring models to predict future events」。不說清楚這點，讀者會誤解截止日後下滑的原因｜https://arxiv.org/html/2411.08324 （Section 3、Table 2、Section 4.1 Closed-Book Setting）
3. 「它的透明度頁面把前者解釋為模型知識『最廣泛也最可靠』所及的日期，並寫明……」→「它的透明度頁面在部分模型條目裡，把前者解釋為……，也有條目寫明訓練資料截止日比可靠知識截止日晚」；sources 標題「（各模型的 Knowledge Cutoff Date 說明）」→「（部分模型條目的 Knowledge Cutoff Date 說明與定義句）」｜**事實（計入）**：Transparency Hub（Model Report，標示 October 2, 2026）的選單列出 19 個條目。只有 13 則有「Knowledge Cutoff Date」段落，其中 12 則有「most extensive and reliable」定義句。最新的 Sonnet 5.5、Opus 5.5、Fable 5.1、Mythos 5.1 條目都沒有這段。原句寫成整個頁面的說法並不準確。「訓練資料截止日較晚」那句出自 Opus 4／Sonnet 4 的條目｜https://www.anthropic.com/transparency
4. 「三家文件的標法並不一致。Anthropic 的模型總覽頁把……分成兩列」→「各家標示截止日的名稱與定義並不一致。Anthropic 的文件區分『可靠知識截止日』與『訓練資料截止日』，兩者不一定是同一天」｜耐久措辭（不計）：「總覽頁分成兩列」是版面快照，換成兩種日期的區分本身。總覽頁今天仍並列兩列，其中一個現行模型兩列不同｜https://platform.claude.com/docs/en/models/overview
5. 「OpenAI 的模型頁只有一個『Knowledge cutoff』欄位加一個日期……Google 的 Gemini API 文件把截止日寫在部分模型頁的欄位，或開發指南的常見問題裡，並補一句……；但不是每個模型頁都有這個欄位」→「OpenAI 與 Google 的開發者文件多半只寫一個『knowledge cutoff』加日期，查證時讀到的頁面沒有說明它指訓練資料還是可靠知識；Google 在說明截止日時，也建議需要更新的資訊改用搜尋接地工具。放的位置也不固定：可能在模型頁的欄位、比較表、常見問題或透明度頁面，有些模型頁則完全不列，找不到就翻官方文件的其他頁面」｜耐久措辭（不計）：改寫成通則，不再寫哪個供應商的哪幾頁有或沒有欄位。今天逐項核對：OpenAI 清單頁與比較頁都只有 Knowledge cutoff 欄位、沒有定義；Gemini 2.5 Flash／2.5 Pro 模型頁有欄位，3.8 Flash、3.5 Flash、3.1 Pro Preview 模型頁與模型索引頁全文沒有 cutoff；3.5 指南的常見問題寫出截止日並說「For more recent information, use the Search Grounding tool」；Anthropic 把截止日放在總覽比較表與 Transparency Hub｜https://developers.openai.com/api/docs/models ；https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 ；https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ；https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash
6. LLMLagBench 段：「Pęzik 等人（2025 預印本）的 LLMLagBench 用 1,713 題新聞問答，另請一個模型當評審……。有的模型不只一個『部分截止點』；在某些模型上，……」→「模型自己說的截止日準不準，有一篇預印本做了直接比對，尚未經同儕審查：Pęzik 等人 2025 年的 LLMLagBench 用 1,713 題新聞問答，交給另一個模型評分……。在其中某些模型上，……。這是單一預印本的結果，還待其他研究驗證」｜來源處理（不計）：依指示，能換成同儕審查來源的就換。「一個模型不只一條截止線」改由前一段 Cheng 等人（COLM 2024）的有效截止日支持（「applies separately to sub-resources and topics」），所以刪掉只靠預印本的「部分截止點」。模型自述截止日的落差找不到同儕審查的替代來源（見下方「懷疑」第 1 點），所以保留，並在正文寫明是未經同儕審查的預印本、由模型評分、是單一研究｜https://arxiv.org/abs/2511.12116 ；https://arxiv.org/abs/2403.12958
7. callout「模型自述的日期可能比實際保守，也可能是錯的。」→「……也可能是錯的，上文的預印本就記錄過這種情形。」｜來源處理（不計）：讓讀者知道這句警告的實證來自預印本｜https://arxiv.org/html/2511.12116 （Section 4.1、4.3）
8. 「所以標示的日期比較像『大約到這附近』……」從 LLMLagBench 段尾移到 Daily Oracle 段尾，改成「兩篇研究合起來看，標示的日期比較像……」｜措辭（不計）：這個結論來自 Cheng 與 Dai 兩篇經同儕審查的論文，不該接在預印本後面｜—
9. 「Cheng 等人 2024 年的論文」→「Cheng 等人在 COLM 2024 發表的論文」；sources 標題加「COLM 2024」；「其中一個甚至早了以年計」→「其中一個的差距甚至以年計」｜來源補註與措辭（不計）：寫出發表場合，和預印本對照；COLM 2024 Accepted Papers 頁把它列為 Outstanding Paper Award。後半是修語病｜http://2024.colmweb.org/AcceptedPapers.html （https 憑證與主機名不符，改用 http 讀）
10. 導言「官方文件與三篇研究論文」→「官方文件與三篇研究（其中一篇是預印本）」｜措辭（不計）：一開始就交代來源性質｜—
11. 「補上截止日之後的資訊只有一條路」前後語序、「交給另一個模型評分」等幾處｜措辭（不計）：可讀性｜—
12. sources 標題：OpenAI →「模型清單的 Knowledge cutoff 欄位，頁面未另外定義」；Google 3.5 指南「目前的開發指南」→「查證時的開發指南」；LLMLagBench →「v1 預印本，未經同儕審查」｜措辭（不計）：拿掉會過期的「目前」，寫明來源性質｜同上各網址

改後 `_body_length` 為 2,722 字（含連結文字 69 字），第一輪是 2,547。結構不變：6 個 H2、1 個表、1 個 callout，指派的 4 個站內連結與總索引都在，全文沒有「推論」或「推理」。dry-run 結果：`dry run: nothing written`，exit 0，只有一個 warning `no_summary`（第一輪就有）。diagram-1.svg 用預設 `render_svg` 渲染到 `/tmp/ai-term-knowledge-cutoff-d1.png` 看過：新小標沒有壓線、超框或疊字，頁尾版權行完整可見；圖上唯一的數字仍是 2026。notes.md 與 research.json 已同步：換掉 Gemini 3 指南，更新 Hub、Daily Oracle、LLMLagBench 的說明與字數，research.json 的 sources 順序與 pack.json 一致。

## 第一輪 6 處事實修改，今天重查

1. **Google 模型頁與開發指南**：成立。Gemini 3 指南頂端仍是「This page is deprecated and will be removed」；What's new in Gemini 3.5 Flash 的常見問題寫出截止日並建議用 Search Grounding；3.8 Flash 頁沒有 cutoff，2.5 Flash 頁有。不過這句仍然取決於「哪幾頁有欄位」，所以按第 5 條改成通則。
2. **「不重新訓練」**：方向對，但還是太絕對，按第 1 條改成「不更動模型本身」。
3. **Dai 等人的推測措辭**：成立。原文是「likely due to a lack of representation of recent news in the training data」，觀察到的是三個模型。正文寫「作者推測」，圖上與 alt 寫「可能較少」，都對。
4. **Daily Oracle 的條件**：成立。原文是「Llama-3-8B may perform worse than the closed-book setting when the RAG cutoff is prior to the knowledge cutoff dates」，這裡的知識截止日是 Table 3 的 K-Cutoff，也就是供應商標示的日期。正文「只到它標示的知識截止日之前」正確。
5. **LLMLagBench 的措辭**：成立。原文「they may declare overly conservative cutoff dates while simultaneously hallucinating about events far beyond their actual training period」在 Introduction，是作者的整體陳述，附註指向 Table 3，不是某一節量出的數字，所以正文用「作者也指出」是對的。Grok 案例是「more than a year earlier」，GPT-OSS 案例是「approximately two years off」，「早了一年以上」成立。
6. **示例**：成立。型態二改成「可以追問……但模型回答的年份本身也要核對」，不構成保證。三種型態都標了虛構、未實測，也沒有寫成觀察到的結果。

## 隨機抽查三分之一的其餘主張（以 seed 20261003 從 22 條抽 8 條）

- A Anthropic 總覽頁兩列：成立。並列四個現行模型，其中一個兩列不同；頁上寫「for the reliable-knowledge and training-data cutoffs behind each model, see Anthropic's Transparency Hub」。https://platform.claude.com/docs/en/models/overview
- E Cheng 等人的設定：成立。以 WikiSpan（也有 NewsSpan）的各月版本量困惑度，取最小值為有效截止日，分析的是開放或有描述的預訓練資料集。https://arxiv.org/html/2403.12958
- I Dai 等人 ICML 2025、每天從新聞產生真假題與選擇題：成立（Comments：ICML 2025）。另外補了預測題框架，見修改第 2 條。https://arxiv.org/abs/2411.08324
- J 截止日後選擇題下滑加快：成立（「sharp performance drops are observed in several models in MC questions」）。
- K LLMLagBench 1,713 題、由模型評分：成立（「As of October 2025, the benchmark comprises 1,713 questions」，評分模型是 DeepSeek-V3-0324）。
- P OpenAI 來源清單多於引用：成立（「The number of sources is often greater than the number of citations」）。https://developers.openai.com/api/docs/guides/tools-web-search
- T Anthropic 系統提示詞提供日期、不適用於 API：成立（「use a system prompt to provide up-to-date information, such as the current date … These system prompt updates do not apply to the Claude API」）。https://platform.claude.com/docs/en/release-notes/system-prompts/overview
- V 補救對照表：屬於概念整理，和 Daily Oracle 的檢索結果、三家搜尋文件一致，沒有超出來源的說法。

順帶也重看了 8 條：三家都寫由模型判斷搜不搜（Anthropic「Claude determines when to search based on the prompt」、Google「determines if a Google Search can improve the answer」、OpenAI「the model can choose to search the web or not」，並註明 Chat Completions 的搜尋模型一律先搜）；Anthropic 的空結果回傳空列表、不是錯誤；OpenAI 的 `external_web_access: false` 是 offline/cache-only 模式；BM25 取前 5 篇、每篇最多 512 words；RAG 截止日之後立刻下滑；給 gold article 時「most of the models still show declining trends」。都成立。

## 我懷疑但沒改的事

1. **模型自述截止日這一點，仍然只有預印本支持。** 我找過同儕審查的替代來源。Cheng 等人（COLM 2024）只比較有效截止日和供應商標示，沒有問模型。Zhao 等人「Set the Clock」（Findings of ACL 2024，arXiv:2402.16797）量的是模型預設用哪一年的知識回答（例如 2022 年截止的模型多半用 2019 年的知識作答），題目是時間對齊，不是自述截止日，所以沒有拿來替換，以免張冠李戴。現在正文與 callout 都寫明這是單一、未經同儕審查、由模型評分的預印本。如果主編只收同儕審查來源，就刪掉 LLMLagBench 段，callout 只留「要查截止日，看供應商的官方文件」。指派切角「模型常說不準自己的截止日」那一項，也就沒有研究可引。
2. **Transparency Hub 的定義句只剩較舊的條目有。** 總覽頁說各模型的截止日要到 Hub 看，但最新的四則條目今天都沒有這段。正文已改成「部分模型條目」，Hub 下架舊條目時，這句要重查。
3. **Google 的兩個模型頁來源最容易失效。** 2.5 Flash 頁可能隨模型停用而下架，3.8 Flash 頁之後可能補上欄位。正文已經不靠哪一頁有欄位，但下次查核時 sources 可能要換頁。來源標題裡的型號是頁面標題，正文沒有型號。
4. 字數 2,722：在 1,800–3,000 之內，但超過 brief 的目標 2,100–2,500。增加的字數主要是預印本的說明與 Daily Oracle 的預測題框架，這兩項都是這一輪要求補的，所以沒有為了壓字數刪事實。
5. 「三家的文件都寫明由模型依提示詞判斷搜不搜」符合今天的文件，但這類工具行為可能改版，例如加入強制搜尋的選項。目前三頁都沒有提到強制搜尋（OpenAI 另有一律先搜的 Chat Completions 搜尋模型，正文已用「Responses API」限定）。
6. 正文的「比較表」由 Anthropic 總覽頁（Compare models）支持，sources 裡有這頁。OpenAI 的比較頁今天也有 Knowledge cutoff 欄位，但沒有另列入 sources。
7. dry-run 的 `no_summary` warning 照舊：brief 沒有要求，也不在查核範圍。
8. COLM 2024 的 https 憑證和主機名不符，那頁是用 http 讀的。arXiv 頁本身沒有寫會議，正文的「COLM 2024」靠的是那一頁，加上作者首頁 PDF 的檔名 `2024_COLM_DatedData.pdf`。

facts_changed: 3
