# 查核紀錄 1：ai-term-knowledge-cutoff

查核者：獨立查核（非撰稿者），2026-10-03。所有來源今天以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新開啟，13 筆全部 200 且非空殼；arXiv 三篇另讀 `arxiv.org/html/<id>` 全文。沒有沿用撰稿者的 notes.md。

## 修改（每處一行：原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

1. 「Google 把截止日放在部分模型頁的欄位和 Gemini 3 指南的表格裡，指南還補了一句……；較新的幾個 Gemini 模型頁則沒有這個欄位」→「Google 的 Gemini API 文件把截止日寫在部分模型頁的欄位，或開發指南的常見問題裡，並補一句……；但不是每個模型頁都有這個欄位」｜事實（計入）：Gemini 3 開發指南頁今天頂端標示「This page is deprecated and will be removed」；「較新的」是會隨時間失效的說法，正文也不該出現型號。今天逐頁查了 Gemini API 模型索引連到的 40 個 gemini-* 模型頁：2.0／2.5 系列與 robotics 頁有 Knowledge cutoff 欄位，3.x 系列（含 3.1 Pro Preview、3.5／3.6／3.7／3.8 Flash）、embedding 與部分 TTS 頁沒有。目前的 3.5 指南常見問題同樣寫截止日並說「For more recent information, use the Search Grounding tool」。改後的寫法不依賴哪一頁有欄位也仍然成立｜https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 ；https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash ；https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ；https://ai.google.dev/gemini-api/docs/gemini-3
2. sources：`https://ai.google.dev/gemini-api/docs/gemini-3`（Gemini 3 developer guide）→ `https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5`（What's new in Gemini 3.5 Flash）｜隨第 1 條：舊頁已標示棄用、即將移除；新頁今天 200，常見問題支持同一句｜同上
3. callout「要查截止日，看供應商當天的模型頁」→「要查截止日，看供應商當天的官方文件」｜隨第 1 條（不另計）：Gemini 3.x 模型頁沒有這個欄位，只看模型頁會找不到｜https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
4. 「補上截止日之後的資訊只有一條路：讓內容進到上下文視窗」→「不重新訓練模型的話，補上截止日之後的資訊只有一條路……」；圖說「補救只能把內容放進上下文視窗」→「不重新訓練的話，補救只能……」；diagram-1.svg 小標「要補上截止日之後的內容，只能放進上下文視窗」→「不重新訓練的話，截止日之後的內容只能放進上下文視窗」，`<desc>` 同步｜事實（計入）：持續預訓練或微調也能加入新知識，兩篇引用論文都提到；原句是絕對說法｜https://arxiv.org/html/2511.12116 （Introduction：「LLMs can be continually pretrained on texts and further finetuned」）；https://arxiv.org/html/2411.08324 （Section 4.3：「continuous pre-training of LLMs … is still needed」）
5. 圖解 alt「接近截止日的資料稀薄且版本混雜」→「接近截止日的資料可能較少且版本混雜」｜事實（計入）：「資料較少」只是 Dai 等人的推測（「likely due to a lack of representation of recent news in the training data」），正文與圖上都寫成推測，只有 alt 寫成定論｜https://arxiv.org/html/2411.08324 （Section 4.3）
6. 「有個模型在檢索資料比自己的訓練截止日更舊時，表現可能不如不給資料」→「有個模型在檢索資料只到它標示的知識截止日之前時，表現可能不如不給資料」｜事實（計入）：論文的條件是 RAG cutoff 早於模型的 knowledge cutoff（供應商標示的那個），不是「訓練截止日」；本文自己把訓練資料截止日與知識截止日分開談，混用會誤導｜https://arxiv.org/html/2411.08324 （Section 4.2：「Llama-3-8B may perform worse than the closed-book setting when the RAG cutoff is prior to the knowledge cutoff dates」）
7. 「作者並指出模型可能自述保守，卻對更晚的事作答」→「作者並指出，模型可能自述一個偏保守的日期，同時卻對遠超出實際訓練範圍的事件編造答案」｜事實（計入）：原文是「hallucinating about events far beyond their actual training period」，重點是編造，不只是「作答」；「更晚」也沒說比什麼晚｜https://arxiv.org/html/2511.12116 （Section 1）
8. 示例型態二「追問『這是哪一年的資訊』就能攤開」→「可以追問『這是哪一年的資訊』，但模型回答的年份本身也要核對」｜事實（計入）：原句是效果保證，違反系列「不承諾」規則；模型回答的年份同樣可能出錯（LLMLagBench 就記錄了模型講錯自己的截止日）｜https://arxiv.org/html/2511.12116 （Section 4.1、4.3）
9. 「每篇截至 512 個英文單字」→「每篇最多 512 個英文單字」｜措辭：「截至」是時間用語；原文為「truncate each retrieved article to a maximum length of 512 words」｜https://arxiv.org/html/2411.08324 （Section 4.1）
10. 「我讀到的頁面沒有另外定義」→「查證時讀到的頁面沒有另外定義」｜措辭：不用第一人稱經驗口吻｜https://developers.openai.com/api/docs/models
11. sources 標題：「Gemini 3.8 Flash 模型頁（較新的模型頁，本次讀到的版本沒有此欄位）」→「（查證時沒有 Knowledge cutoff 欄位的模型頁之一）」；「Pezik et al.」→「Pęzik et al.」（與正文、arXiv 作者名一致）｜措辭｜https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ；https://arxiv.org/abs/2511.12116
12. alt 標點「可能較少、版本混雜、截止日之後」→「可能較少且版本混雜、截止日之後」｜措辭：避免三段列舉被頓號打亂｜—

改後 `_body_length` 2,547 字（原 2,500）；6 個 H2、1 個表、1 個 callout，指派的 4 個站內連結與總索引都在。diagram-1.svg 重新渲染檢查，新增的小標沒有壓線、超框；圖上仍只有版權行的 2026 一個數字。

## 查過、沒問題的主要主張

- Anthropic 模型總覽頁有「Reliable knowledge cutoff」與「Training data cutoff」兩列，並寫「for the reliable-knowledge and training-data cutoffs behind each model, see Anthropic's Transparency Hub」；今天頁上就有一個模型兩列不同（訓練資料截止日較晚）。總覽頁本身沒有定義句，這點作者標得對。https://platform.claude.com/docs/en/models/overview
- 定義句在 Transparency Hub 的 Model Report（頁面標示 October 2, 2026）：大多數條目寫「knowledge cutoff date … This means the model's knowledge base is most extensive and reliable on information and events up to …」；有一則條目寫明兩個模型的「training data cutoff date」比「reliable knowledge cutoff date」晚。正文把定義歸給透明度頁面、不是總覽頁，是對的。https://www.anthropic.com/transparency
- OpenAI 模型清單、單一模型頁、比較頁都只有「Knowledge cutoff」欄位加日期，沒有定義。https://developers.openai.com/api/docs/models
- Anthropic 搜尋工具：「Claude determines when to search based on the prompt」、穩定知識直接回答、可用系統提示詞調整；「A search that succeeds but matches no results returns an empty content list, not an error」；可回答「beyond its knowledge cutoff」並附引用。https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
- OpenAI（Responses API）：「the model can choose to search the web or not based on the content of the input prompt」；Chat Completions 的搜尋模型一律先搜，所以正文加「（Responses API）」是對的；`external_web_access: false` 為「offline/cache-only mode」；「The number of sources is often greater than the number of citations」。https://developers.openai.com/api/docs/guides/tools-web-search
- Google 接地：「The model analyzes the prompt and determines if a Google Search can improve the answer」；回應以 url_citation 標註文字片段與來源。https://ai.google.dev/gemini-api/docs/google-search
- Anthropic 系統提示詞頁：claude.ai 與手機 app「use a system prompt to provide up-to-date information, such as the current date … at the start of every conversation」，「These system prompt updates do not apply to the Claude API」。「用 API 時自己放日期比較保險」是本文建議，寫法上沒有冒充文件原句。https://platform.claude.com/docs/en/release-notes/system-prompts/overview
- Cheng 等人：effective cutoff「distinct from the LLM's reported cutoff and differs between sub-resources」；分析的是訓練資料公開或有描述的模型（閉源模型的推測放在附錄 D，不入正文，本文也沒用）；用 WikiSpan 每月版本量困惑度、取最小值；有模型（含 2023 年 Wikipedia 傾印）有效截止日落在 2019 年左右，「以年計」成立；兩個原因（去重複擋不住語意相同、字面相近的重複文件；新的 CommonCrawl 傾印含大量舊內容）；Pile 系模型與標示吻合；結論「sometimes it does align … in many cases it does not」。https://arxiv.org/abs/2403.12958
- Dai 等人：arXiv 頁 Comments 寫 ICML 2025；Daily Oracle 每天從新聞產生真假題與選擇題；closed-book 下有三個模型在截止日前幾個月緩慢下降，原因只用「likely」，正文寫「作者推測」，用詞正確；截止日之後「sharp performance drops are observed in several models in MC questions」；BM25 前 5 篇；RAG cutoff 之後成績立刻下降；gold article 設定下最高接近約 90%，但「Most of the models struggle with temporal generalization, even when provided with gold articles」。https://arxiv.org/abs/2411.08324
- LLMLagBench：「As of October 2025, the benchmark comprises 1,713 questions」；用 DeepSeek-V3 當評審；PELT 變點偵測；「several LLMs exhibit multiple partial cutoff points」；Section 4.1 有一個模型自述比量到的邊界早一年以上，4.3 另一個約早兩年，所以「某些模型……早了一年以上」成立。今天 arXiv 只有 v1（2025-11-15），沒有期刊或會議標示，「預印本」標得對。https://arxiv.org/abs/2511.12116
- 系列規矩：正文與圖上都沒有型號、截止日期、價格、排行榜分數（論文中的模型名都已略去）；示例標明虛構、未實測，三種回答型態都寫成假設、沒有寫成觀察；全文沒有用到「推論」或「推理」，所以不涉及兩者混用；有台灣用語；圖上唯一的數字是版權行的 2026。

## 我懷疑但沒改的事

- LLMLagBench 值不值得留：我留下了。它是本文唯一支持「模型自述的截止日不可靠」與「部分截止點」的一手來源，這兩點也正是指派切角要的（「模型常說不準自己的截止日」）。正文已標「2025 預印本」，用「作者指出」「可能」措辭，沒有引用它的數字。它的弱點是 v1 預印本、評分靠另一個模型、作者自己也寫指令微調後的拒答會干擾偵測。如果主編要求只用經同儕審查的來源，就刪掉 [8] 段的後半與 callout 第一句的依據，改成只說「模型自述的日期不一定可靠」，不附研究。
- Daily Oracle 的題目原本是「預測」形式（問某事會不會在某日前發生），截止日前的題目才等於考過去事件。正文只寫「真假題與選擇題」，沒提預測框架；結論不受影響，所以沒改。
- 來源標題仍有 Gemini 型號（2.5 Flash、3.5 Flash、3.8 Flash），因為那是頁面標題、網址也帶型號；正文沒有。如果系列連 sources 都不想出現型號，要整組換掉，但這樣「標題對」就做不到。
- 用 3.8 Flash 模型頁支持「不是每個模型頁都有這個欄位」，是用一頁證明「沒有」，Google 之後可能補上欄位；改後的句子只要還有任何一頁沒欄位就成立（今天約 30 頁沒有）。
- Transparency Hub 上，總覽頁的三個現行模型都有條目，但今天這三則都沒有「Knowledge Cutoff Date」段落；有這段的 13 則都是較舊的模型。總覽頁說要到 Hub 看各模型的截止日，但最新模型今天在 Hub 上查不到。文章沒有寫日期，定義句也來自仍在頁上的舊條目，所以不受影響；只是 Hub 改版時，定義句可能跟著舊條目一起消失。
- `research.json` 與 `notes.md` 仍記載 Gemini 3 開發指南與舊說法（「較新的幾個 Gemini 模型頁沒有欄位」）。本次只准改 pack.json、diagram-1.svg、verify-1.md，所以沒動；協調者 ingest 前可同步。
- dry-run 只有一個 warning：`no_summary`（第一個 H2 前沒有 summary 區塊）。brief 沒要求，結構不在查核範圍，沒有加。
- Cheng 等人一般認為發表於 COLM 2024，但 arXiv 頁沒有標示，我沒再查會議頁；正文只寫「2024 年的論文」，沒有寫會議，所以不影響。

facts_changed: 6
