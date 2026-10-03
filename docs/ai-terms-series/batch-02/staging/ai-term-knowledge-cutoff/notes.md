# 查證與編輯紀錄：ai-term-knowledge-cutoff

查證日一律 2026-10-03（本日實際開啟）。User-Agent：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL`，皆回 200 且內容非空殼。
格式：主張｜來源網址｜查證日｜讀取方式

## 各家怎麼標示

Anthropic 模型總覽頁把「Reliable knowledge cutoff」與「Training data cutoff」分成兩列，並指向 Transparency Hub 看各模型截止日｜https://platform.claude.com/docs/en/models/overview｜2026-10-03｜curl -sSL（docs.claude.com 與 docs.anthropic.com 舊網址皆導向此頁）；頁上並列的模型有三款兩列相同、一款訓練資料截止日晚於可靠知識截止日（文中不寫日期與型號）
可靠知識截止日的定義：「knowledge base is most extensive and reliable on information and events up to [date]」；並明寫有的模型 training data cutoff 比 reliable knowledge cutoff 晚（該頁的一則條目）｜https://www.anthropic.com/transparency｜2026-10-03｜curl -sSL，頁面標示 Model Report 2026-10-02；與 brief 指定的「模型總覽文件」不同：總覽頁只有兩列數值，定義句在透明度頁
OpenAI 模型清單與單一模型頁各有一個「Knowledge cutoff」欄位與一個日期；兩頁都沒有另外定義它指訓練資料或可靠知識（只讀了清單頁與一個模型頁）｜https://developers.openai.com/api/docs/models ；https://developers.openai.com/api/docs/models/gpt-6-astra｜2026-10-03｜curl -sSL（platform.openai.com/docs/models 導向 developers.openai.com）；單一模型頁未列入 sources，只作核對
Google：Gemini 3 指南有「Knowledge Cutoff」表格欄位，常見問題寫「For more recent information, use the Search Grounding tool」｜https://ai.google.dev/gemini-api/docs/gemini-3｜2026-10-03｜curl -sSL
Google：Gemini 2.5 Flash（與 2.5 Pro）模型頁有「Knowledge cutoff」欄位｜https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash｜2026-10-03｜curl -sSL
**與 brief 衝突**：brief 說 Gemini「模型文件頁的 knowledge cutoff 欄位」，但今天讀到的較新模型頁（3.8 Flash、3.7 Flash、3.6 Flash、3.5 Flash、3.1 Pro Preview）全文都沒有 knowledge cutoff 字樣，只有較舊的 2.5 系列頁有欄位；文章寫成「較新的幾個 Gemini 模型頁沒有這個欄位」｜https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash（其餘幾頁同樣檢查過，未列入 sources）｜2026-10-03｜curl -sSL 後去標籤，搜尋 cutoff 無結果

## 研究結果

有效截止日（effective cutoff）的定義：某模型對某資源，最接近的資源版本日期；可不同於供應商標示｜https://arxiv.org/abs/2403.12958（全文讀 https://arxiv.org/html/2403.12958v2）｜2026-10-03｜curl -sSL
該論文的設定：主要分析訓練資料公開的模型（Pythia、GPT-Neo、GPT-J、RedPajama、Falcon、OLMo、LLaMA），WikiSpan（5000 篇最常被編輯的 Wikipedia 條目，2016-04 至 2023-04 每月版本）與 NewsSpan，量困惑度、取最小值為有效截止日（文中不寫模型名與日期）｜同上｜2026-10-03｜同上
有些模型有效截止日比標示早得多，其中一個（RedPajama）含較新 Wikipedia 傾印，有效截止日卻在 2019 年前後，差距以年計（文中不寫模型名與年份）｜同上，Section 5.2、6.2｜2026-10-03｜同上
原因兩點：CommonCrawl 新傾印含大量舊內容；去重複流程擋不住語意重複與字面近似重複｜同上，Section 6｜2026-10-03｜同上
有模型與標示吻合（以 Pile 訓練的模型，Wikipedia 日期被刻意放大取樣三倍）｜同上，Section 5.2、6.1｜2026-10-03｜同上
Appendix D 對閉源模型的結果是作者自述「speculation」，文章不採用｜同上｜2026-10-03｜同上
截止日前幾個月答對率緩慢下降（Gradual Decline in the Recent Past），作者寫「likely due to a lack of representation of recent news in the training data」；截止日之後幾個模型在選擇題上下滑加快｜https://arxiv.org/abs/2411.08324（全文讀 https://arxiv.org/html/2411.08324）；ICML 2025｜2026-10-03｜curl -sSL；Section 4.3；觀察到的模型為其中三個（文中不寫模型名）；文章把「資料較少」寫成作者推測，圖上也寫「可能」
Daily Oracle 設定：每日新聞自動產生真假題與選擇題；closed-book 設定不給資料｜同上｜2026-10-03｜同上，Section 3、4.1
受限檢索（constrained open-book）：BM25 取前 5 篇、每篇截至 512 words；資料庫停在某天，成績在那天之後下滑；Llama-3-8B（文中不寫）在檢索截止日早於其知識截止日時可能比 closed-book 更差｜同上｜2026-10-03｜同上，Section 4.1、4.2
gold article 設定：直接給含答案原文，整體可接近約 90%，但多數模型仍隨時間下滑（文中只寫「多數模型仍隨時間下滑」）｜同上｜2026-10-03｜同上，Section 4.2
LLMLagBench：1,713 題新聞問答（截至 2025 年 10 月）、用另一個模型當評審、PELT 變點偵測；有的模型有多個「部分截止點」｜https://arxiv.org/abs/2511.12116（全文讀 https://arxiv.org/html/2511.12116）｜2026-10-03｜curl -sSL；Section 3、4；**這是 arXiv v1 預印本**，未見同儕審查標示，文章標「預印本」
模型自述截止日與量到邊界落差：論文中有一個模型自述早了一年以上、另一個約兩年；作者在 Introduction 寫「instruction-following models can exhibit contradictory behavior: they may declare overly conservative cutoff dates while simultaneously hallucinating about events far beyond their actual training period」（文章用「作者並指出模型可能自述保守，卻對更晚的事作答」，不寫模型名與日期）｜同上，Section 1、4.1、4.3｜2026-10-03｜同上

## 補救與失敗點

Anthropic 搜尋工具：「Claude determines when to search based on the prompt」；請求涉及時效或訓練資料以外才搜，穩定知識直接答；可用系統提示詞調整｜https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool｜2026-10-03｜curl -sSL（舊網址 /build-with-claude/tool-use/web-search-tool 導向此頁）
Anthropic：「A search that succeeds but matches no results returns an empty content list, not an error」；錯誤也以 200 回傳、錯誤放在 body｜同上｜2026-10-03｜同上
Anthropic：「answer questions with up-to-date information beyond its knowledge cutoff」，回應含引用｜同上｜2026-10-03｜同上
OpenAI：「the model can choose to search the web or not based on the content of the input prompt」（Responses API web_search）；Chat Completions 的搜尋模型則一律先搜，文章以「（Responses API）」限定｜https://developers.openai.com/api/docs/guides/tools-web-search｜2026-10-03｜curl -sSL（platform.openai.com/docs/guides/tools-web-search 導向此頁）
OpenAI：external_web_access:false 為 offline/cache-only 模式（預設 true）；sources 欄位列出全部讀取的 URL，「The number of sources is often greater than the number of citations」｜同上｜2026-10-03｜同上
Google 接地：「The model analyzes the prompt and determines if a Google Search can improve the answer」；回應以 url_citation 標註對應文字片段與來源｜https://ai.google.dev/gemini-api/docs/google-search｜2026-10-03｜curl -sSL（/grounding 導向此頁）
Anthropic：網頁版與手機應用程式用系統提示詞在每次對話開頭提供目前日期；「These system prompt updates do not apply to the Claude API」。「用 API 時自己放日期比較保險」是本文的做法建議，不是文件原句｜https://platform.claude.com/docs/en/release-notes/system-prompts/overview｜2026-10-03｜curl -sSL（舊網址 /release-notes/system-prompts 導向此頁）

## 編輯說明

- 全文不寫任何模型名稱、截止日期、價格、排行榜分數；論文中的模型名與年份刻意略去，只寫設定與現象。
- 「示範」一節的「濱海光影節」與三段回答全為虛構示例，文中標明未對任何模型實測。
- 正文字數以 `app.guides.pack_ingest._body_length` 計：2,500（含連結文字；不含連結文字為 2,431）。
- diagram-1.svg 唯一的數字是頁尾「© Mokaair 製圖 2026」的年份（brief 規定的版權行），其餘無數字；正文無需另帶。
- WebSearch 曾列出數篇部落格整理的截止日對照表，屬二手來源，未引用、未取數。
- SVG 為原創向量插圖，非 AI 產圖。
- 渲染：此機器上 `render_svg`（--window-size=1600,900）實際視窗約少 88 px，輸出圖底部被白邊切掉，頁尾 y=870 的版權行不入鏡；另以 1600×1000 視窗渲染確認頁尾與全圖無疊字、無超框。內容最低處（方框底 y=805）在兩種渲染下都可見。
