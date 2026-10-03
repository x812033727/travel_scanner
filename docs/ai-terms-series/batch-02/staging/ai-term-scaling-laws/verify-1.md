# 查核紀錄 1：ai-term-scaling-laws（縮放定律）

查核者不是撰稿者。查證日 2026-10-03。每筆 `sources` 都用 `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"`
抓 `https://arxiv.org/abs/<id>`（12 筆全部 HTTP 200，`citation_title` 與 sources 標題相符），再抓 `https://arxiv.org/pdf/<id>` 用 `pdftotext -layout`
讀正文。沒有用撰稿者的 notes 當依據，數字都回到論文原文對過。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

- 「Chinchilla 論文指出，Kaplan 對所有模型用同樣的訓練長度與學習率排程……2024 年的兩篇後續研究重做了比較：」→「Chinchilla 論文的解釋是：……2024 年的兩篇後續研究重做了比較，都發現學習率排程不是主因：」｜原文把 Hoffmann 的推測寫成「指出」，也沒說兩篇後續研究都反駁了學習率排程這一點。Porian 摘要：「Counter to a hypothesis implied in Hoffmann et al., we find that careful learning rate decay is not essential」，§1 說「disprove Hoffman et al.'s hypothesis」，且最後吻合 Chinchilla 的設定用的是固定學習率；Pearce 與 Song §1 說這類解釋「incomplete」，Experiment 2 說多個訓練長度「affects coefficients only marginally (counter to Chinchilla's explanation)」｜https://arxiv.org/abs/2406.19146 、 https://arxiv.org/abs/2406.12907 、 https://arxiv.org/abs/2203.15556（§2）
- 「Pearce 與 Song 認為大部分差異來自 Kaplan 計參數時扣掉詞彙嵌入層」→「Pearce 與 Song 認為很大一部分差異來自 Kaplan 計參數時不算嵌入層」｜原文是「much of this discrepancy」，不是「most」；Kaplan 排除的是詞彙與位置兩種嵌入（Pearce §2：「embedding layers for the vocabulary and position indices」），只寫「詞彙」太窄｜https://arxiv.org/abs/2406.12907
- 「兩篇的歸因不完全相同，共通點是都指向參數與算力的計算方式。」→「……重疊之處是 Kaplan 計算參數與算力時，沒有算進嵌入層或最後一層。」｜措辭：寫明重疊點。Porian §5.1 自己說 Pearce 與 Song「identify the last layer FLOP count as a cause」，Porian 另外兩個因素（暖身、最佳化器設定）是 Pearce 沒有的（不計入 facts_changed）｜https://arxiv.org/abs/2406.19146
- 「估計本身有誤差：Besiroglu 等人重做 Chinchilla 的第三種擬合……重做後則相符。」→「估計本身也可能出錯：Besiroglu 等人用從論文圖表重建的資料，重做……重做後則與前兩種相容。」｜措辭與方法交代：摘要寫的是「a reconstruction of data from their plots」與「compatible with the findings from the first two」（不計入 facts_changed）｜https://arxiv.org/abs/2404.10102
- 「2026 年一篇尚在審查的預印本把推論（inference）時重複取樣的成本算進去，在它的八項任務上，最佳配置是比 Chinchilla 建議更小、卻訓練得更久的模型。」→「Sardana 等人 2024 年把模型上線後的推論（inference）成本也算進去，結論是預期請求量夠大時，該訓練比 Chinchilla 建議更小、看更多 token 的模型。」｜arXiv:2604.01411 確實存在、PDF 標「Preprint. Under review.」、只有 v1（2026-04-01），內容也如原文所述；但它是未審稿的單一預印本，而文中要說的「最佳只算訓練成本」有同行審查過的一手來源：Sardana 等人（ICML 2024）摘要寫 Chinchilla 定律「neglect to include the cost of inference」，並得出預期推論需求夠大時應「train models smaller and longer than Chinchilla-optimal」。改用它，sources 第 11 筆同步替換｜https://arxiv.org/abs/2401.00448
- 「他們分析 BIG-Bench 上被標為湧現的能力，超過 92% 出現在兩種指標下」→「他們統計一份人工標注的 BIG-Bench 湧現能力清單，超過 92% 出現在兩種指標下」｜措辭：92% 是對文獻 [32]（Jason Wei〈137 emergent abilities of large language models〉，2022，手動標注的 task-metric-model family 組合）算的，不是 Wei 等人論文本身，也不是 BIG-Bench 全部任務（§3「hand-annotated task-metric-model family triplets [32] … 2 metrics account for > 92% of claimed emergent abilities」）（不計入 facts_changed）｜https://arxiv.org/abs/2304.15004
- 「用多數決或獎勵模型挑答案，卻只從 40.50% 升到 41.41%」→「改用多數決或獎勵模型挑答案，進步最多的做法也只從 40.50% 升到 41.41%」｜論文 §1 原文是「the biggest performance increase is only from 40.50% to 41.41% over the same sample range」，指三種挑選法裡進步最多的那一種，不是每一種都是這兩個數字｜https://arxiv.org/abs/2407.21787
- 「比一律取樣再挑最好的省約 2 至 4 倍算力」→「論文估計推論算力的使用效率比一律取樣再挑最好的提高約 2 至 4 倍」｜措辭：照 §8 原文「improve the efficiency of test-time compute scaling by a factor of 2 − 4×」改寫，避免「省 4 倍」的說法；數字不變（不計入 facts_changed）｜https://arxiv.org/abs/2408.03314
- 「題目簡單、推論量少時多算推論較划算，題目很難、推論量大時預訓練較有效」→「題目簡單或中等、或推論量少時，多算推論較划算；題目很難、或推論量大時，預訓練較有效」｜§7 Takeaways 的條件是「或」不是「且」：「On easy and medium questions … or in settings with small inference requirement」「on challenging questions … or under higher inference requirement」；原句用頓號並列讀起來像兩個條件要同時成立，也漏了中等難度｜https://arxiv.org/abs/2408.03314

## 查過、沒問題的主要主張

- Kaplan 等人（2001.08361）：損失是在測試文字上量的交叉熵（§1.3「cross entropy loss in nats」）；損失對參數量、資料量、計算量各自近似冪律（摘要、§1.1）；「doubling the number of parameters yields a loss that is smaller by a factor 2^−αN = 0.95」，條件是參數有限、資料足夠、訓練到收斂（§1.2 式 1.1）；新增算力大多應花在放大模型（圖 3 說明、§1.1 D ∼ C^0.27）；Appendix C「we do not have a solid theoretical understanding … difficult to determine in what circumstances they can be trusted」；§8 要檢驗損失改善是否轉成「relevant language tasks」。
- Hoffmann 等人（2203.15556）：訓練超過 400 個模型（摘要）；模型大小與 token 數應「scaled in equal proportions」；把 Kaplan 換算成 10 倍預算→模型 5.5 倍、token 1.8 倍（§1，是 Hoffmann 的換算）；§2 對差異的兩點說明（固定 token 數與學習率排程；Kaplan 多數模型較小）；式 2 的 E 項「should correspond to the entropy of natural text」。
- Porian 等人（2406.19146，NeurIPS 2024 spotlight）：三個因素「last layer computational cost, warmup duration, and scale-dependent optimizer tuning」，暖身「too long for smaller models」，修正後「excellent agreement」。
- Besiroglu 等人（2404.10102）：確實存在，v2 2024-05-15，只在 arXiv；摘要支持「第三種擬合與前兩種不一致、重做後相容」。保留：它補上「Chinchilla 自己的估計也有問題」這層，且 Pearce 與 Porian 都用到它重建的資料。
- Wei 等人（2206.07682，TMLR）：定義「not present in smaller models but is present in larger models」、近隨機後上升（§2）；§5.1 不給部分分數的指標「at best an incomplete explanation, because emergent abilities are still observed on many classification tasks」；六項 BIG-Bench 任務交叉熵早已改善，但「does not explain … or enable us to predict the scale at which emergence occurs」。
- Schaeffer 等人（2304.15004）：非線性或不連續指標產生表面湧現（摘要）；兩種指標的定義（§1）；「nothing in this paper should be interpreted as claiming that large language models cannot display emergent abilities」（§7）；獨立性假設「is not true」但近似結果在質性上吻合（§2 註腳）。
- 示例算術：0.5^5=0.031、0.7^5=0.168、0.9^5=0.590、0.95^5=0.774，四捨五入 3%、17%、59%、77%，與正文、`diagram-1.svg` 的長條數字與 `<desc>` 一致；兩張圖的長條高度都是每 1% 3.6 px，比例正確；圖上數字（50、70、90、95、3、17、59、77、5、2026）正文或表格圖說都有。
- Brown 等人（2407.21787）：覆蓋率的定義與「over four orders of magnitude」（摘要）；MATH、Llama-3-8B-Instruct（開放權重，文中沒寫名字）覆蓋率 100 次 82.9%→10,000 次 98.44%（§1）。
- Snell 等人（2408.03314）：MATH、PaLM 2-S* 微調來做修改與 PRM 驗證；FLOPs 相同下與「14× larger」模型比較；「Test-time and pretraining compute are not 1-to-1 "exchangeable"」（§7）。
- Villalobos 等人（2211.04325）：摘要確實在估公開人類文字的存量與資料需求；文章沒寫它的預測年份，符合「不預測撞牆」。
- 系列規矩：沒有價格、截止日期、排行榜分數；Chinchilla 是指派點名的論文通稱；「推論」第一次出現附 inference，全文沒有「推理」；示例有標「示例（假設數字，未實測）」；沒有保證句；指派的五個站內連結（model-parameters、pretraining、test-time-compute、benchmark、ai-terms-index）都在；台灣用語沒看到中國用語。
- 結構：6 個 H2、1 個 3 欄表格、1 個 callout、1 張圖；改後 `_body_length` = 2580（原 2497）。

## 我懷疑但沒改的事

- Snell 的效率數字三處不一：摘要「more than 4×」、§1「about 4x」、§5–6 的圖說「up to 4x less」（例：64 對 256 次取樣）、§8「2 − 4×」。保留「約 2 至 4 倍」，它和正文實驗與結論一致，只有摘要寫得比較強。
- Brown 摘要說多數決與獎勵模型「plateau beyond several hundred samples」，§1 與 §3 寫「approximately 100 samples」。文章沒寫持平點，所以沒改。
- `research.json` 與 `notes.md` 還列著 arXiv:2604.01411（Roberts 等人）和它的主張，Sardana 等人（2401.00448）不在裡面。這次只准寫 `pack.json`、`diagram-1.svg`、`verify-1.md`，所以沒動；後續若要用 `research.json` 的 sources，請把 2604.01411 換成 2401.00448。
- Schaeffer 的 arXiv PDF 仍標「Preprint. Under review.」，Snell 的 abs 頁沒有會議註記。文章與 sources 都沒寫它們的發表場合，所以不必改；我今天沒去開會議頁確認。
- Hoffmann 說 Kaplan 對所有模型用「fixed number of training tokens」，這是 Hoffmann 對 Kaplan 的描述，Kaplan 自己的 L(N, D) 實驗其實有改資料量。文章已寫成「Chinchilla 論文的解釋是」，歸給 Hoffmann，沒再細分。
- Sardana 等人的結論以「reasonably large inference demand (~1B requests)」為條件，文章寫「預期請求量夠大時」，沒寫數字。
- dry-run 有一個 warning：`no_summary`（第一節前沒有 summary 區塊）。這批其他稿子也都沒有 summary 區塊，而且查核規定結構不變，所以沒加。

facts_changed: 5
