# 查核紀錄（第 2 輪）：ai-term-temperature

查核者：第二輪獨立查核（不是撰稿者，也不是第一輪查核者）。查核日 2026-10-03。依 `VERIFY.md` 的規則，先讀 `brief.md`、`catalogue.json` 的指派與 `verify-1.md`。
11 筆 `sources` 今天全部以 `curl -sSL`（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓取，都回 200；四篇 arXiv 另抓 `arxiv.org/pdf/<id>`（200），用 pdftotext 轉文字；
HTML 轉純文字後逐句比對。為了替 vLLM 加括注，另讀了 https://docs.vllm.ai/en/latest/（200）。以下引文都是今天頁面上的原文，沒有沿用 notes.md 或 verify-1.md 的引文。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

1. 「作者結論是 nucleus sampling 是當時生成長篇文字最好的解碼策略」→「作者的結論是：要生成品質高、又像人寫的一樣多樣的長篇文字，nucleus sampling 是當時最好的解碼策略」｜第一輪已加上「長篇」，但論文的「最好」還有兩個條件，就是品質高（以人工評估衡量）和多樣性跟人寫的一樣。少了這兩個條件，讀者會以為不管目標是什麼，它都是生成長篇文字最好的方法。原文 "Nucleus Sampling is currently the best available decoding strategy for generating long-form text that is both high-quality — as measured by human evaluation — and as diverse as human-written text."｜https://arxiv.org/abs/1904.09751（PDF 摘要）
2. 「t 趨近 0 時領先者幾乎獨占；Google 的文件寫明溫度 0 時永遠選機率最高的候選，這種選法稱為貪婪解碼（greedy decoding）」→「t 越接近 0，領先者越接近獨占，極端時等於每一步都只取機率最高的候選；這種選法稱為貪婪解碼（greedy decoding）」｜原句讓「貪婪解碼」看起來是 Google 對溫度 0 的稱呼。Google 頁面上溫度那句是 "A temperature of 0 is deterministic, meaning that the highest probability response is always selected."，沒有用 greedy；這個詞出現在 topK 的說明："A topK of 1 means the selected token is the most probable among all the tokens in the model's vocabulary (also called greedy decoding)"。改後只拿它當詞的定義，不再歸給 Google 的溫度 0 那句。Google 對溫度 0 的說法第 21 段已照字面寫出，這裡刪掉不會少掉資訊｜https://ai.google.dev/gemini-api/docs/prompting-strategies
3. （措辭，不計入）第 6 段「t 越高分布越「軟」」→ 後面加「，也就是各候選的機率越接近」｜一般讀者看不懂「軟」；原文 "Using a higher value for T produces a softer probability distribution over classes"｜https://arxiv.org/abs/1503.02531
4. （措辭，不計入）第 12 段「比較多種解碼法」→「比較多種解碼法（從機率挑出下一個 token 的方法）。」，並把長句拆成兩句｜「解碼」第一次出現，沒有解釋｜https://arxiv.org/abs/1904.09751
5. （措辭，不計入）第 13 段「Holtzman 等人提到先用溫度塑形再做 top-k」→「Holtzman 等人提到過去有人先用溫度塑形再做 top-k」｜論文是在引述別人的做法，不是自己的建議；原文 "Low temperature sampling has also been used to partially alleviate the issues of top-k sampling discussed above, by shaping the distribution before top-k sampling (Radford et al., 2018; Fan et al., 2018)."｜https://arxiv.org/abs/1904.09751（第 3.3 節）
6. （措辭，不計入）清單第 2 項「Holtzman 等人指出純取樣會抽到不可靠的尾端；Renze 與 Guven 只讓其中一個模型把溫度掃過 1.0」→「Holtzman 等人指出，不截尾、直接照完整機率抽（純取樣）會抽到太多不可靠的冷門候選；Renze 與 Guven 只讓其中一個模型把溫度調到 1.0 以上」｜「純取樣」「掃過」是術語；原文 "the model is confusing itself: sampling too many unlikely tokens"｜https://arxiv.org/abs/1904.09751（第 4.2 節）、https://arxiv.org/abs/2402.05201
7. （措辭，不計入）第 17 段「從標準評測抽出的選擇題，溫度由 0.0 掃到 1.0」→「從常用評測題庫抽出的選擇題，溫度從 0.0 逐步調到 1.0」｜白話；原文 "randomly sampling problems from standard LLM benchmarks"｜https://arxiv.org/abs/2402.05201
8. （措辭，不計入）第 21 段「OpenAI 在 seed 參數的說明（該欄位標為 Beta 與棄用）寫道」→「OpenAI 的 seed（亂數種子）欄位標為 Beta 與棄用，說明寫道」｜seed 第一次出現時沒有解釋，原句又有兩組括號連在一起；原文 "Deprecated." "This feature is in Beta."｜https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
9. （措辭，不計入）第 22 段「連續批次處理」→「把多筆請求併在一起算（連續批次處理）」；「vLLM 官方文件」→「模型推論（inference）軟體 vLLM 的官方文件」；「要重現得固定排程」→「要重現，得讓排程（哪些請求一起算）固定」｜一般讀者不知道 vLLM 是什麼，也不知道批次和排程指什麼。白話依據：Atil 摘要 "co-mingled data in input buffers"、vLLM 首頁 "vLLM is a fast and easy-to-use library for LLM inference and serving."。「推論（inference）」與第 25 段的「推理（reasoning）」第一次出現都附英文，符合系列規矩｜https://arxiv.org/abs/2408.04667、https://docs.vllm.ai/en/latest/

改完：`_body_length` 2,619 → 2,734（在 1,800–3,000 內；不含連結文字為 2,681）。H2 六個、表格一個、callout 一個；指派的五個站內連結都在（what-is-a-large-language-model、ai-term-token、ai-hallucination-fact-check、ai-term-structured-outputs、ai-terms-index）；
`missing_diagram_numbers` 為空；標題、description、圖檔未改。
dry-run：`dry run: nothing written`（exit 0），只有一則 warning `no_summary`（改前就有）。
圖：`render_svg` 把 diagram-1.svg 渲染成 `/tmp/ai-term-temperature-d1.png`（1600×900）並看過：沒有字壓線、超框或疊字；圖上的 91/7/2、70/20/10、52/28/20、0.85、85%、累積 70%/90%、78/22 都和正文一致，用 p^(1/t) 重算為 90.7/7.4/1.9、52.3/27.9/19.8，重新配比為 77.8/22.2。hero.svg 也渲染看過，和 alt 描述相符。

## 第一輪六處事實修改的複查（今天的原文）

- **Holtzman 等人「最好」的範圍**（第一輪第 2 項）：方向正確，但範圍還不夠完整，本輪再收窄（見上方修改 1）。設定句「一個約 7.6 億參數的語言模型，生成 5,000 段最長 200 個 token 的文字」也成立：原文 "We perform experiments using the Large model (762M parameters). Our analysis is based on generating 5,000 text passages, which end upon reaching an end-of-document token or a maximum length of 200 tokens."｜https://arxiv.org/abs/1904.09751（第 4.1 節）
- **Renze 與 Guven：只有一個模型掃過 1.0**（第一輪第 3 項）：成立。原文 "First, we instructed GPT-3.5 to complete the 100-question (small) exam using the CoT prompt with temperatures ranging from 0.0 to 2.0 in increments of 0.1." "Performance began to drop rapidly after a temperature of 1.0 until the generated text became incoherent at 1.6. As a result, we stopped the initial temperature sweep at 1.6 and limited the rest of our sweeps from 0.0 to 1.0."，限制段 "we had to limit the sampling temperature range we explored from 0.0 to 1.0 for all combinations of models, prompts, and exams, except for GPT-3.5 using CoT prompting on the 100-question exam."｜https://arxiv.org/abs/2402.05201（第 2.3、4.2 節）
- **Renze 與 Guven：十個領域中兩個顯著**（第一輪第 4 項）：成立。原文 "Finally, we analyzed the performance of GPT-3.5 using the CoT prompt on all ten exams. … However, the LSAT-AR and SAT-Math exams showed statistically significant differences in the Kruskal-Wallis p-values."；Table 5 列十個題庫，LSAT-AR p < 0.001、SAT-Math p = 0.019，其餘八個（含 ARC Challenge p = 0.089，作者在註 6 明說視為不顯著）都大於 0.05。「整體未見顯著差異」也成立："Using GPT-3.5 with a CoT prompt on the 1,000-question exam from 0.0 to 1.0, the Kruskal-Wallis test yielded H(10) = 10.439, p = 0.403."；按模型（Table 3）與按提示詞（Table 4）的 p 值都大於 0.05｜https://arxiv.org/abs/2402.05201（第 3.1 節）
- **Google 把溫度 0 稱為 deterministic**（第一輪第 5 項）：成立，原文 "A temperature of 0 is deterministic, meaning that the highest probability response is always selected."｜https://ai.google.dev/gemini-api/docs/prompting-strategies
- **Atil 等人的推測**（第一輪第 6 項）：成立，原文 "However, engineering optimizations to run LLMs faster, such as continuous batching, chunk prefilling, or prefix caching, might lead to non-deterministic behavior. Since many of the the models are close-sourced (GPT-3-5, GPT-4o), and all are hosted behind APIs we don't control, we can only speculate about the reason for this behavior."｜https://arxiv.org/abs/2408.04667（第 8.1 節）
- **vLLM 的排程與批次不變性條件**（第一輪第 7 項）：成立，原文 "vLLM does not guarantee the reproducibility of the results by default, for the sake of performance. To achieve reproducible results: In offline mode, you can either set VLLM_ENABLE_V1_MULTIPROCESSING=0 which makes scheduling deterministic, or enable batch invariance to make the outputs insensitive to scheduling. In online mode, you can only enable batch invariance." "Even with the above settings, vLLM only provides reproducibility when it runs on the same hardware and the same vLLM version."（頁尾 April 28, 2026）｜https://docs.vllm.ai/en/latest/usage/reproducibility/

## Anthropic API 參考（複查，原文）

頁面標題 "Create a Message - Claude API Reference"，三個取樣參數旁邊都標 "Deprecated"：

- temperature："Amount of randomness injected into the response. Deprecated. Models released after [特定型號] do not support setting temperature. A value of 1.0 will be accepted for backwards compatibility, all other values will be rejected with a 400 error. Defaults to 1.0. Ranges from 0.0 to 1.0. Use temperature closer to 0.0 for analytical / multiple choice, and closer to 1.0 for creative and generative tasks. Note that even with temperature of 0.0, the results will not be fully deterministic."
- top_k："Only sample from the top K options for each subsequent token. Deprecated. Models released after [特定型號] do not accept top_k; any value will be rejected with a 400 error. … Recommended for advanced use cases only."
- top_p："Use nucleus sampling. Deprecated. Models released after [特定型號] do not support setting top_p. A value >= 0.99 will be accepted for backwards compatibility, all other values will be rejected with a 400 error. … Recommended for advanced use cases only."

正文「把 temperature、top_p、top_k 標為棄用，寫明較新的模型不支援設定溫度：只接受預設值 1.0，其他值回 400 錯誤」與第 15、21 段的 Anthropic 說法都成立。頁面上寫的是具體型號，正文以「較新的模型」代替，符合系列規矩。｜https://platform.claude.com/docs/en/api/messages/create

## 隨機抽查（其餘主張的三分之一）

把第一輪修改與 Anthropic 以外的可查主張列成 27 條，用亂數抽出 9 條：1、2、4、5、7、9、19、20、27。

- [1] 第 0 段：溫度是取樣設定，每個 token 先算出候選機率再抽：Google 原文 "The temperature controls the degree of randomness in token selection."；Holtzman 式 4 是對整個詞彙表的 softmax。成立。
- [2] 第 3 段：替詞彙表中每個候選打分、換算成加總 100% 的機率再抽：Holtzman 式 4 "Given the logits u1:|V| and temperature t, the softmax is re-estimated as exp(ul/t) / Σl' exp(ul'/t)"。成立。
- [4] 第 6 段：分數（logit）除以 t 再換算成機率：同上式 4。成立。
- [5] 第 6 段：Hinton 等人寫 t 通常為 1，越高越軟：原文 "where T is a temperature that is normally set to 1. Using a higher value for T produces a softer probability distribution over classes."（PDF）。成立。
- [7] 第 7 段示例數字：重算後 t=0.5 為 90.7/7.4/1.9，t=2 為 52.3/27.9/19.8，四捨五入成立。
- [9] 第 11 段 top-k、top-p 的定義與 2019 年：原文 "we define its top-p vocabulary V(p) ⊂ V as the smallest set such that Σ P(x|x1:i−1) ≥ p" 與式 3 重新配比；top-k "the set of size k which maximizes Σ P(x|x1:i−1)"；abs 頁 "Submitted on 22 Apr 2019"，Comments "Published in ICLR 2020"。示例 70/90、20/90 = 77.8/22.2。成立。
- [19] 第 21 段：Anthropic 寫溫度 0.0 也不完全確定（原文見上）；OpenAI seed "Deprecated." "This feature is in Beta." "If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed"。成立。
- [20] 第 22 段 Atil 的設定與 15%：首頁 "Preprint. Under review."；"We set the temperature at 0, top-p at 1, and fix the seed. We use the same compute infrastructure, inputs, and configurations."；摘要 "non-determinism in five LLMs configured to be deterministic when applied to eight common tasks in across 10 runs … We see accuracy variations up to 15% across naturally occurring runs"；圖 1 是 "Percentage difference between maximum and minimum accuracy in 10 runs"。成立。
- [27] hero.svg 和 alt：渲染後中間是左藍右橘的旋鈕，左邊一高兩低的藍色長條，右邊三根高度相近的橘色長條，和 alt 描述相符。成立。

## 第一輪留下的懷疑

- **「貪婪解碼」是否被說成 Google 對溫度 0 的稱呼**：是，已改（修改 2）。改後全文只有一處「貪婪解碼」，沒有歸給 Google。
- **來源標題裡的「Gemini API」**：保留。這是 Google 的 API 產品名，和頁面標題一致（"Generating content | Gemini API | Google AI for Developers"、"Prompt design strategies | Gemini API | Google AI for Developers"），只出現在 `sources`。正文、表格、callout、圖說、圖上文字與 description 掃過都沒有型號（掃 Gemini、GPT、Claude、Llama、Mistral、Mixtral、Opus、Sonnet、Haiku 等）。Google 對新一代的建議在正文寫成「較新一代模型」。
- **notes.md 與 research.json 和定稿不一致**：已同步，見下方。

## 可讀性（台灣一般讀者）

從頭讀一次，卡住的地方都是沒解釋的術語：「軟」、解碼、純取樣、掃（sweep）、seed、連續批次處理、vLLM、排程。都只加了短括注或換成白話（修改 3–9），沒有新增段落，也沒有改結構。用語都是台灣慣用（迴圈、程式、提示詞、亂數種子）。

## 同步 notes.md 與 research.json

- notes.md：Holtzman 的設定改成以參數量描述，刪掉 GPT-2 的寫法，結論加上範圍原文；貪婪解碼另列一行，寫明 Google 是在 topK 為 1 時用這個詞；Renze 補上單一模型掃過 1.0 和十個領域中兩個顯著；Atil 補上作者的假設原文；vLLM 補上排程與批次不變性條件，並列出首頁的自我描述（只用於括注，沒有列入 sources）；「推論／推理」與字數改為 2,734（不含連結 2,681）；第 9 點指向兩份查核紀錄。
- research.json：同步上述 claims；`running_text_characters` 2503 → 2734；notes 欄刪掉 GPT-2 的寫法並更新字數。字數用 `app.guides.pack_ingest._body_length` 實算。

## 查過、沒問題的主要主張

- OpenAI：temperature 範圍 "between 0 and 2"，兩個欄位都寫 "We generally recommend altering this or top_p but not both." / "… or temperature but not both."，沒寫原因（正文標「本文的解讀」，正確）；top_p "An alternative to sampling with temperature, called nucleus sampling"。｜https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
- OpenAI 新模型指南：原文 "Unsupported parameters: When reasoning effort is not none, remove temperature, top_p, and top_logprobs."（在當前旗艦系列的遷移說明裡，正文沒列型號）。｜https://developers.openai.com/api/docs/guides/latest-model
- OpenAI 結構化輸出：原文 "Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema"；正文不用保證語氣，並註明是官方說法。｜https://developers.openai.com/api/docs/guides/structured-outputs
- Google：先 topK、再 topP、最後用溫度取樣（原文 "the topK tokens with the highest probabilities are sampled. Tokens are then further filtered based on topP with the final token selected using temperature sampling."）；低溫較確定、高溫較多樣（原文 "Lower temperatures are good for prompts that require a more deterministic or less open-ended response, while higher temperatures can lead to more diverse or creative results."）；新一代建議維持預設（原文 "we strongly recommend keeping them at their default values for [新一代] models. Changing these parameters (for example, setting the temperature below 1.0) can cause unexpected behavior, such as looping or degraded performance, particularly in complex mathematical or reasoning tasks."）。｜https://ai.google.dev/gemini-api/docs/prompting-strategies
- Google GenerationConfig：原文 "Note: The default value varies by model" "Values can range from [0.0, 2.0]."；正文寫各家範圍是「0 到 1 或 0 到 2」，成立（Anthropic 0.0–1.0、OpenAI 0–2、Google 0.0–2.0）。｜https://ai.google.dev/api/generate-content
- Holtzman 等人：固定 k 的問題（原文 "The presence of flat distributions makes the use of a small k in top-k sampling problematic, while the presence of peaked distributions makes large k's problematic."）；溫度小於 1（原文 "Setting t ∈ [0, 1) skews the distribution towards high probability events"）；低溫重複（圖 9 原文 "Sampling with temperatures lower than 0.9 severely increase repetition."）；top-p 調太小（原文 "all stochastic methods face repetition issues when their tuning parameters are set too low, which tends to over-truncate, mimicking greedy search"，支持表格「候選變少，輸出變單調」）。｜https://arxiv.org/abs/1904.09751
- Renze 與 Guven：九個模型、五種提示詞（摘要 "we used nine popular LLMs with five prompt-engineering techniques"）；只測選擇題（原文 "The limited effects of sampling temperature in our experiments may have simply resulted from the constraints imposed by the structure of MCQA problems."）。｜https://arxiv.org/abs/2402.05201
- 規矩：正文沒有型號、價格、截止日期、排行榜分數；兩個示例都標「示例（未實測）」；推論＝inference、推理＝reasoning，第一次出現都附英文；沒有保證語氣；圖上每個數字正文都有。

## 我懷疑但沒改的事

- 第 13 段「各家的先後順序還不同」：寫法沒錯，但順序其實只對 top-p 有影響。溫度不改變排名，所以 top-k 的入選名單和最後的機率不受順序影響。用本文示例算：先把溫度調到 2 再做 top-p 0.85，前兩名只累積 80%，三個候選都留下；先做 top-p，鍋燒意麵就被排除。如果編輯希望讀者看懂「順序為什麼重要」，可以補這一句（約 60 字），但要標成本文的計算。
- Atil 等人在第 8.1 節也在本機不開加速、跑了一個開放模型，得到確定的結果，用來支持他們的假設。正文照論文原話寫「只能推測」，沒有提這個本機實驗，屬取捨。
- Renze 與 Guven 的 arXiv 頁寫明已收錄於 Findings of EMNLP 2024，來源標題只寫 arXiv 編號，沒錯，沒改。作者另外建議解題任務把溫度設為 0.0（理由是可重現、又不損失正確率），正文沒寫，但和「溫度越低越準得不到支持」不衝突。
- vLLM 的條件在正文簡化成「讓排程固定，或讓輸出不受排程影響」，沒寫線上模式只能用後者。
- 正文 2,734 字，超過撰稿目標 2,100–2,500，但在 1,800–3,000 的硬性範圍內；多出來的主要是給一般讀者的括注。
- dry-run 的 `no_summary` warning 沒處理（指派沒要求）。
- 程序：查核中途誤跑了一次唯讀的 `git status`（只看這個目錄），沒有其他 git 操作。

facts_changed: 2
