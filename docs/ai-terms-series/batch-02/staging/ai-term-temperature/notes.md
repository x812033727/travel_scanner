# 查證與編輯紀錄：ai-term-temperature

格式：主張｜來源網址｜查證日｜讀取方式。所有頁面皆以 `curl -sSL`（User-Agent 為 Mokaair-editorial/1.0，不帶任何個資）讀取，狀態碼 200，再把 HTML 或 PDF 轉成純文字比對原文。

## 機制與定義

softmax 加溫度 t 的做法；t 通常設為 1；t 越高機率分布越「軟」｜https://arxiv.org/abs/1503.02531（PDF 第 2 節 Distillation，原文 "T is a temperature that is normally set to 1. Using a higher value for T produces a softer probability distribution over classes"）｜2026-10-03｜arxiv.org/abs 與 arxiv.org/pdf，pdftotext
給定 logits 與溫度 t，softmax 重新估計為 exp(u_l/t) 除以總和；t 在 [0,1) 會把分布推向高機率事件、降低尾端質量｜https://arxiv.org/abs/1904.09751（PDF 第 3.3 節 Sampling with Temperature，式 4）｜2026-10-03｜arxiv.org/pdf，pdftotext
top-p（nucleus sampling）定義：由高到低取機率累積至少達 p 的最小集合，其餘不抽並重新配比；2019 年 4 月提交，ICLR 2020 收錄｜https://arxiv.org/abs/1904.09751（第 3.1 節式 2、頁尾 "Published as a conference paper at ICLR 2020"；abs 頁 Submitted on 22 Apr 2019）｜2026-10-03｜arxiv.org/abs 與 pdf
top-k 只從機率最高的 k 個取樣；固定 k 在不同情境不合適（分布平坦時太小、集中時太大），top-p 的候選數隨分布增減｜https://arxiv.org/abs/1904.09751（第 3.2 節 Difficulty in choosing a suitable value of k）｜2026-10-03｜arxiv.org/pdf
論文設定：論文用的 Large 模型（762M 參數，正文寫「一個約 7.6 億參數的語言模型」，不寫型號）、生成 5,000 段、最長 200 個 token；作者結論有範圍限定：要生成品質高（以人工評估衡量）、又和人寫的一樣多樣的長篇文字，nucleus sampling 是當時最好的解碼策略（PDF 摘要原文 "Nucleus Sampling is currently the best available decoding strategy for generating long-form text that is both high-quality — as measured by human evaluation — and as diverse as human-written text"）｜https://arxiv.org/abs/1904.09751（第 4.1 節、PDF 摘要）｜2026-10-03｜arxiv.org/pdf
溫度低於 0.9 的純溫度取樣重複明顯增加（圖 9 說明 "Sampling with temperatures lower than 0.9 severely increase repetition"）；純取樣的尾端不可靠、會讓模型「confusing itself」｜https://arxiv.org/abs/1904.09751（第 4.2、5.3 節、圖 9）｜2026-10-03｜arxiv.org/pdf
先用溫度塑形再做 top-k 是既有做法（引 Radford 2018、Fan 2018；正文寫「Holtzman 等人提到過去有人…」，不是作者自己的建議）｜https://arxiv.org/abs/1904.09751（第 3.3 節）｜2026-10-03｜arxiv.org/pdf
溫度很低或參數調太小時的重複：「all stochastic methods face repetition issues when their tuning parameters are set too low, which tends to over-truncate」（支持表格「top-p 調小：候選變少，輸出變單調」）；純取樣「sampling too many unlikely tokens」（支持清單「會抽到太多不可靠的冷門候選」）｜https://arxiv.org/abs/1904.09751（第 4.2、5.3 節）｜2026-10-03｜arxiv.org/pdf

## 官方 API 文件

OpenAI：temperature 範圍 0 到 2；「一般建議調整 temperature 或 top_p，不要兩個都調」；top_p 為 nucleus sampling 的替代做法｜https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create（Create chat completion，temperature 與 top_p 欄位）｜2026-10-03｜curl 讀 developers.openai.com，200。platform.openai.com 同一頁回 403，改讀搬遷後的 developers.openai.com；Responses 參考頁的 temperature、top_p 欄位文字相同
OpenAI：seed 參數標為 Deprecated 與 Beta；系統盡力讓相同 seed 與參數得到相同結果，「Determinism is not guaranteed」，並以 system_fingerprint 監看後端變動（正文只寫前半，未寫 system_fingerprint）｜同上（seed 欄位）｜2026-10-03｜同上
OpenAI：推理強度不是 none 時，要移除 temperature、top_p、top_logprobs（正文未列型號）｜https://developers.openai.com/api/docs/guides/latest-model（頁名 "Using GPT-6"，Migration 區的 "Unsupported parameters"）｜2026-10-03｜curl 讀 developers.openai.com，200
OpenAI：Structured Outputs 是讓模型回應符合你提供的 JSON Schema 的功能｜https://developers.openai.com/api/docs/guides/structured-outputs｜2026-10-03｜curl 讀 developers.openai.com，200（官方原文用 "ensures"，正文不採用保證語氣，只寫「讓回應符合」並註明是官方說法）
Anthropic：temperature 標 Deprecated；較新的模型不支援設定；1.0 被接受、其他值回 400；預設 1.0；範圍 0.0 到 1.0；分析與選擇題靠近 0.0、創作靠近 1.0；「即使溫度 0.0 結果也不會完全確定」｜https://platform.claude.com/docs/en/api/messages/create（Create a Message，temperature 欄位）｜2026-10-03｜curl 讀 platform.claude.com（docs.anthropic.com 會轉址到此），200，HTML 轉純文字。頁面用具體型號寫「Models released after ... do not support」，正文刻意不寫型號
Anthropic：top_k、top_p 同樣標 Deprecated，較新模型不接受（top_p 只接受 0.99 以上）；兩者 "Recommended for advanced use cases only"｜同上｜2026-10-03｜同上（正文只用到 temperature 的棄用；top_p、top_k 的棄用寫進 research.json，未寫進正文以節省篇幅）
Google：GenerationConfig 的 temperature 範圍 [0.0, 2.0]；預設值依模型而異；topP、topK 說明；topK 欄位空白代表該模型不套用 top-k 也不允許設定｜https://ai.google.dev/api/generate-content（GenerationConfig）｜2026-10-03｜curl 讀 ai.google.dev，200
Google：溫度 0 是確定的（原文 "A temperature of 0 is deterministic, meaning that the highest probability response is always selected."）；順序為先 topK、再 topP，最後用溫度取樣；較低溫適合較確定、較不開放的提示詞，較高溫較多樣或創意｜https://ai.google.dev/gemini-api/docs/prompting-strategies（Experiment with model parameters）｜2026-10-03｜curl 讀 ai.google.dev，200
貪婪解碼（greedy decoding）＝每一步只取機率最高的候選：Google 同頁是在 topK 的說明裡用這個詞（原文 "A topK of 1 means the selected token is the most probable among all the tokens in the model's vocabulary (also called greedy decoding)"），不是在溫度 0 那句。正文第 7 段只用它定義這個詞，不再寫成 Google 對溫度 0 的稱呼｜同上｜2026-10-03｜同上
Google：對其較新一代模型強烈建議維持預設，調到 1.0 以下可能出現重複循環或複雜數學與推理任務表現下降（正文未列型號）｜https://ai.google.dev/gemini-api/docs/prompting-strategies 同段 Note；另見 https://ai.google.dev/gemini-api/docs/gemini-3 的 Temperature 段｜2026-10-03｜curl 讀 ai.google.dev，200
vLLM：預設為了效能不保證結果可重現；要重現得讓排程確定（離線模式設 VLLM_ENABLE_V1_MULTIPROCESSING=0）或啟用批次不變性讓輸出不受排程影響（線上模式只能用後者）；即使如此，也只在相同硬體與相同 vLLM 版本下重現｜https://docs.vllm.ai/en/latest/usage/reproducibility/（頁尾標 April 28, 2026）｜2026-10-03｜curl 讀 docs.vllm.ai，200
vLLM 是什麼（正文寫「模型推論（inference）軟體 vLLM」）：文件首頁原文 "vLLM is a fast and easy-to-use library for LLM inference and serving."｜https://docs.vllm.ai/en/latest/｜2026-10-03｜curl 讀 docs.vllm.ai，200（只用來寫這個括注，未列入 sources）

## 實驗論文（只寫該論文在它的設定下量到的）

Renze 與 Guven：九個模型（摘要）、五種提示詞寫法、從十個標準評測題庫抽出的選擇題考卷（1,000 題與 100 題兩種）；溫度 0.0 到 1.0 沒有統計上顯著的正確率差異；超過 1.0 後快速下降；只有其中一個模型（搭配逐步思考提示、100 題考卷）掃到 2.0，超過 1.0 後正確率快速下降，約 1.6 時文字不連貫、正確率趨近 0，其餘組合只測 0.0–1.0（第 4.2 節限制段 "except for GPT-3.5 using CoT prompting on the 100-question exam"；正文寫「只讓其中一個模型把溫度調到 1.0 以上」，未寫型號）；同一模型分十個題目領域檢定時，LSAT-AR（p < 0.001）與 SAT-Math（p = 0.019）兩個領域達到顯著（第 3.1 節、Table 5），作者歸因於 0.0 時全對或全錯的行為、平均正確率仍相近；作者註明只測選擇題，開放式任務可能不同｜https://arxiv.org/abs/2402.05201（摘要、第 2.3 節、第 3.1 節、第 4.1、4.2、4.4 節）｜2026-10-03｜arxiv.org/abs 與 pdf，pdftotext。abs 頁另載已收錄於 Findings of EMNLP 2024
Atil 等人（預印本，頁面標 Under review）：五個模型、八項任務、各 10 次、temperature 0、top-p 1、固定 seed、同一運算環境；多次執行間準確率差異最多 15%（摘要 "accuracy variations up to 15% across naturally occurring runs"，圖 1 為 10 次中最高減最低）；作者懷疑連續批次處理、chunk prefilling、prefix caching 等加速手法可能造成差異，但受測模型都在他們無法控制的 API 後面，只能推測（第 8.1 節 "all are hosted behind APIs we don't control, we can only speculate about the reason for this behavior"）；正文把連續批次處理白話成「把多筆請求併在一起算」，依據摘要 "co-mingled data in input buffers"｜https://arxiv.org/abs/2408.04667（摘要、第 5 節、第 8 節）｜2026-10-03｜arxiv.org/abs 與 pdf，pdftotext

## 示例數字（原創，未實測任何模型）

示例機率 70%、20%、10% 以 p 的 1/t 次方正規化計算（等同 logit 取對數後除以 t）：t=0.5 得 90.7、7.4、1.9，寫成 91、7、2；t=2 得 52.3、27.9、19.8，寫成 52、28、20；總和皆為 100。top-p=0.85：70 小於 85，70 加 20 等於 90 達標，重新配比為 77.8 與 22.2，寫成 78 與 22。Google 文件也有同類算例（A、B、C 為 0.3、0.2、0.1 且 topP 為 0.5 時選 A 或 B）。計算以 Python 重算過。
旅客留言與重跑 5 次是假設的教學流程，未執行。

## 圖與用字

diagram-1.svg 與 hero.svg 為原創向量圖，非 AI 產圖。圖上數字（0.5、1、2、91、7、70、20、10、52、28、0.85、85、90、78、22、2026）皆出現在正文或表格圖說；2026 為製圖年份，同時出現在表格圖說的查證年月。已用 pack_ingest 的 missing_diagram_numbers 驗證無缺漏。
「推論（inference）」只在 vLLM 那句出現一次，「推理（reasoning）」第一次出現在 OpenAI 參數那句，兩者第一次都附英文。模型名、價格、排行榜分數一律未寫；Holtzman 論文的設定以參數量描述（約 7.6 億參數），不寫型號。來源標題裡的「Gemini API」是 Google 的 API 產品名，只出現在 sources，不在正文。
字數：pack_ingest 的 `_body_length`（含 rich_paragraph 內連結文字）為 2734；不含連結文字為 2681（第二輪查核後）。

## 與指派不一致或需協調者決定的地方

1. 指派要寫「為什麼不建議同時大幅調兩個」：目前只有 OpenAI 的參考明寫「一般建議只調其中一個」，沒有說明原因；Anthropic 現行參考頁已不含「不要同時調」的舊句，改標棄用與僅供進階；Google 描述的是先後順序，沒有叫人別同時調。正文因此寫成 OpenAI 的建議，加上標明為「本文的解讀」的理由，並補上各家先後順序不同。
2. 指派說「官方文件對 temperature 0 不保證確定性」：Anthropic 明寫不完全確定；OpenAI 的說法在 seed 參數；Google 的提示策略頁反而寫溫度 0 是確定的（deterministic，選機率最高者）。兩者談的層次不同（選擇規則與整個服務的結果），正文第 21 段照字面並列 Google 的「確定的」與 Anthropic 的「不完全確定」，第 22 段標明這是本文的解讀，沒有說哪一家錯。
3. 指派預期各家都能調：今日官方頁寫明部分模型不支援（Anthropic 棄用且新模型拒絕非預設值、OpenAI 推理模式需移除、Google 新一代建議維持預設），正文只寫文件的說法、不列型號。
4. Thinking Machines 的 Defeating Nondeterminism in LLM Inference（2025-09-10）讀過，但是研究團隊自家技術文章，不是論文或官方文件，依指派的來源規則未收錄；機制句改由 vLLM 官方文件與 Atil 預印本支撐。
5. Holtzman 的 arXiv 摘要頁文字（v2）與 ICLR 版 PDF 內摘要措辭不同；正文只用 PDF 內的定義與結論。
6. Renze 與 Guven 摘要與正文寫九個模型，演算法段寫十個；正文採摘要的九個。
7. 指派的渲染指令用 chromium-1194 的 chrome，在這個容器裡視窗高度只有約 812 像素，下方約 88 像素被裁成白色（連範本 ai-term-sandbox 的頁尾也看不到）。自查改用 1600×1000 視窗完整檢視；hero 內容放在 y 小於 700 以內，不受影響。
8. dry-run 只有一則 warning：no_summary（沒有摘要區塊）。範本與指派都沒有要求，未改。
9. 兩輪獨立查核的修改見同目錄 verify-1.md 與 verify-2.md；本檔與 research.json 已依第二輪定稿同步（2026-10-03）。
