# 查核紀錄 2：ai-term-data-poisoning

第二輪查核者，不是撰稿者，也不是第一輪查核者。查核日 2026-10-03。依 `docs/ai-terms-series/batch-03/VERIFY.md` 執行：9 筆 `sources` 今天以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開（9 筆皆 200）；5 篇 arXiv 論文抓 `arxiv.org/pdf/<id>`（皆 200）用 pdftotext 讀全文；NIST 讀 CSRC 頁與 `nvlpubs.nist.gov` 的 PDF 全文（200）；OWASP 三頁 HTML 轉純文字。作者的 notes.md、research.json 與 verify-1.md 只當索引，每條主張都回到原文核對。

範圍：逐條重查第一輪改過的 4 處事實與 1 處措辭；從其餘 34 條事實主張以固定種子隨機抽 12 條（約三分之一）重查；處理第一輪留下的 7 個疑點；以台灣一般讀者讀一遍，精簡論文設定堆疊的段落。

## 修改

1. 「這個定義涵蓋 RAG 用的嵌入資料，但兩份文件對 RAG 知識庫的歸類不一致」→「⋯⋯嵌入（embedding，把文字轉成數值向量）資料被操弄⋯⋯；第八項談 RAG 的向量與嵌入，也把資料投毒列為風險。RAG 知識庫該歸哪類，兩份文件說法不一」｜第一輪疑點：LLM04 只說 embedding，沒提 RAG，原句是編輯推論。LLM08 開頭寫明向量與嵌入的弱點出現在使用 RAG 的系統，Common Examples 第 4 項就是「Data Poisoning Attacks」，改成這個有原文的說法；括號裡的白話解釋取自 LLM04 自己的「embedding (converting text into numerical vectors)」｜https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ ；https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/
2. 「作者估算以 2023 年的情況，只要 60 美元，就能控制⋯⋯0.01%」→「作者以 2023 年的網域價格估算，每年 60 美元以內，就能控制⋯⋯0.01%」｜第一輪疑點：第 4.2 節寫「At least 0.01% of each dataset can be controlled for less that $60 USD per year」，成本是以 2023 年 7 月 Google Domains 價格買網域的年費，圖 1 也寫「≤ $60 USD」。原句沒寫是每年的費用｜https://arxiv.org/abs/2302.10149（PDF 第 4.2 節、圖 1）
3. 「Carlini 等人也未發現分裂視圖投毒被實際利用的跡象」→「Carlini 等人檢查了兩個資料集，也沒找到⋯⋯」｜第一輪疑點：第 4.4 節的開頭句確實很概括（「we could not find any evidence of this」），但實際只分析了 CC3M 與 LAION-400M，LAION-400M 那段還寫「no evidence at present that this attack would have been exploited against this dataset」。加上檢查範圍，免得讀者以為 10 個資料集都查過｜https://arxiv.org/abs/2302.10149（PDF 第 4.4 節）
4. 對照表「效果持續」的提示詞注入欄「通常只在當次互動」→「只在讀到注入內容時」｜第一輪疑點：NIST 第 3.4.2 節的 Self-propagating injections 指出，惡意提示可以像蠕蟲一樣被模型轉寄出去；第 3.4 節也說間接注入是透過模型讀到的資源（資料通道）進來。所以效果不限於當次互動，而是只要注入內容還會被讀到就會作用。原句的「通常」雖有保留，仍與 NIST 描述的機制不符｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final（PDF 第 3.4、3.4.2 節）
5. 「但不能判斷資料原本是否惡意，快照前就被改的內容，雜湊照樣吻合」→「但雜湊只確認下載到的和發布者當初收錄的一樣，不能判斷資料原本是否惡意」｜第一輪疑點：原句是編輯推論。Carlini 第 1 節寫 integrity verification「ensuring that clients observe the same data as when maintainers first indexed and annotated it」，第 6.2 節的雜湊是對「prior to any attack」的原始內容計算；NIST 第 3.2.3 節也只把雜湊當成確認網域沒被劫持的基本完整性檢查。改成原文直接支持的說法｜https://arxiv.org/abs/2302.10149（PDF 第 1、6.2 節）；https://csrc.nist.gov/pubs/ai/100/2/e2025/final（PDF 第 3.2.3 節）
6. 「過濾與異常偵測：能去掉重複或明顯異常的樣本。」→「過濾與異常偵測：嘗試在訓練前剔除可疑的樣本。」｜第一輪疑點：NIST 與 OWASP 的投毒段落都沒有「重複」。NIST 第 3.2.3 節是「Data filtering can also attempt to remove poisoned samples」，OWASP LLM04 是「Use anomaly detection techniques to filter out adversarial data」，改寫成兩者都支持的說法，「嘗試」也對應 NIST 的「attempt」｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final（PDF 第 3.2.3 節）；https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/
7. （措辭，不計入事實修改）Souly 段落重排：先交代設定（從頭預訓練 6 億到 130 億參數、亂碼後門、容易量測），再寫結果，並把「附錄另一組較小的實驗」改成「附錄裡另一種後門的實驗」。附錄 I 用的是改用德文回答的後門，其中 GPT-3.5-turbo 是微調實驗，說「另一種後門」比說「較小」準確｜https://arxiv.org/abs/2510.07192（PDF 第 3.1、3.2 節、附錄 I 圖 26）
8. （措辭，不計入）RAG 界線段刪掉 LLM08／LLM01 代號，改成「算作資料投毒情境／算作提示詞注入情境」，原文對應不變；frontrunning 補上摘要原有的例子「維基百科這類」；VIA 句子加逗號、改成「傳到下游」；「若罕見字詞讓輸出一致偏向同一答案，就值得回頭追查訓練資料」是沒有來源的建議，為了精簡刪掉。

改後 `_body_length` = 2,672（第一輪後 2,658）。結構不變：6 個 H2、1 張表、1 個 callout，指派的 4 個 slug 加 `ai-terms-index` 都在，topics 含 `ai-terms`。dry-run 通過，只有協調者另加的 `no_summary` 警告。`diagram-1.svg`、`hero.svg` 未改；圖上唯一數字 2026 正文仍有。

## 第一輪修改的重查（全部維持）

- NIST 分類面向：CSRC 摘要寫「key types of ML methods, life cycle stages of attack, and attacker goals, objectives, capabilities, and knowledge」，PDF 第 2.1 節列出四個面向。「從攻擊發生的階段、攻擊者的目標與能力等面向分類」正確。
- BadNets：第 2.3.3 節寫「changing their label to a target class ... misclassified to the target class」，「分成攻擊者指定的類別」正確。
- Souly 後訓練：第 6 節寫「our work has not assessed how likely are backdoors to persist through realistic (safety) post-training」；附錄 A 寫「our pretraining attacks do not persist through post-training」；附錄 I 圖 26：GPT-3.5-turbo 加至少 100 筆模擬對齊樣本後 ASR 低於 30%，Pythia-6.9B 降到接近零。正確，第 7 項只調整措辭。
- Hubinger 持續性：摘要寫「most persistent in the largest models and in models trained to produce chain-of-thought reasoning」，第 1 節寫「Backdoor persistence is contingent」，圖 11 段落寫「all of our backdoors are substantially easier to remove in smaller models」。正確。
- frontrunning 的「被管理者還原」：第 1 節寫「even if a content moderator detects and reverts malicious modifications after-the-fact」。正確。

## 隨機抽查（種子 20261003，34 條抽 12 條），全部沒問題

- C1 譯名並存：數位時代用「資料中毒攻擊」（bnext.com.tw/article/84742，今天打開，200），聯合新聞網用「對資料下毒攻擊」（udn.com/news/story/6811/9113984，200）。只用來證明用法，不列入 sources。
- C2 NIST 第 2.1.1 節：投毒在訓練階段，資料投毒是「inserting or modifying training samples」，模型投毒是「controls the model and its parameters」。
- C4 OWASP LLM04 定義：「pre-training, fine-tuning, or embedding data is manipulated to introduce vulnerabilities, backdoors, or biases」。
- C5 NIST 第 3.2.1 節：資料集發布者可能只提供網址清單，攻擊者可能買下網域換掉內容。
- C10 Carlini 摘要：split-view 讓「a dataset annotator's initial view of the dataset differs from the view downloaded by subsequent clients」。
- C13 Souly 第 1、3.1 節：600M、2B、7B、13B「pretrained from scratch」，Chinchilla 最適資料量。
- C16 Souly 第 3.1 節：DoS 後門在觸發字串後輸出亂碼；第 4.1 節說它「can be measured during pretraining without requiring fine-tuning」。
- C17 Souly 第 1 節：微調實驗「absolute sample count similarly dominates over poisoning percentage」。
- C20 VIA 摘要：合成資料訓練對既有攻擊「strong resistance」，主因「different distribution patterns between poisoning data and queries」；VIA 讓下游 ASR「comparable to those observed in the poisoned upstream models」；arXiv 註記 NeurIPS 2025 Spotlight（v2，2025-10-24）。
- C22 NIST 第 3.1.1 節：GenAI 分「Training-time attacks」與「Inference-time attacks」，提示詞注入在部署階段。
- C27 NIST 第 3.2.3 節：「the provider publishes cryptographic hashes, and the downloader verifies the training data」。
- C30 Hubinger 摘要：提示寫 2023 年寫安全程式碼、寫 2024 年插入「exploitable code」。

處理修改時一併重讀、也沒問題的：NIST 第 2.3 節（可用性投毒整體退化，目標式與後門投毒只影響少數樣本）、第 2.3.5 節（真實世界不易執行，案例都針對持續更新的系統）、第 2.3.3 節引述 [193]（無額外假設時後門與自然特徵無法區分）、第 3.4.2 節（知識庫投毒以 PoisonedRAG 為例，列在間接提示詞注入之下）；Souly 第 3.2 節（250 份成功、100 份不成功、0.00016%）與第 2 節（「typical model evaluation protocols can fail to detect their presence」、外部約聘人員）；PoisonedRAG 摘要（5 段、數百萬段、90%，「To appear in USENIX Security Symposium 2025」）、第 1 節（改寫、困惑度偵測不足）、指令與捏造知識之分；OWASP LLM08 Scenario #1、LLM01 Scenario #4 與建議 4、5、6；NIST AI 100-2 仍以 E2025 為最新版（CSRC 出版物搜尋只列 E2023 與 E2025，e2026 的 final／ipd 網址 404）。

系列規矩：「本文／這篇」0 次；正文沒有「推論／推理」；沒有型號、價格、排行榜、截止日期（60 美元是論文估算的攻擊成本，附年份與「每年」）；示例標「示例（虛構情境，未實測）」；沒有「用了就不會」式保證；正文沒有查證過程；未發現中國用語（信息、默認、優化、數據、用戶等 0 次）。

## 我懷疑但沒改的事

- 字數 2,672，仍高於 brief 的目標 2,200–2,600（在 3,000 上限內）；精簡省下的字被第 1、2 項補上的來源說法抵掉，沒有再刪實質內容。
- 「NIST 也建議把模型當成不受信任的元件，例如限制它能呼叫的工具與權限」：前半是 NIST 第 3.2.3 節原意，「例如」後面是編輯舉例，最接近的是第 3.4.4 節的「multiple LLMs with different permissions」與 OWASP LLM01 的最小權限，NIST 沒有逐字這樣寫。
- 新的表格格子「只在讀到注入內容時」是依 NIST 第 3.4 節（注入經由資料通道進入）與第 3.4.2 節（自我散播）歸納的摘要，不是原文句子。
- 「有紀錄的案例多半針對持續用新資料更新的系統」：NIST 第 2.3.5 節對它列出的三個案例寫的是「In all these incidents」，「多半」比原文保守，沒改。

facts_changed: 6
