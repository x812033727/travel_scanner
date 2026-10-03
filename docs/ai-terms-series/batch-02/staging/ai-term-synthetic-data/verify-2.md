# 查核紀錄 2：ai-term-synthetic-data

第二輪查核者，不是撰稿者，也不是第一輪查核者。查核日 2026-10-03。照 `VERIFY.md` 的規則，今天用 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開全部九個來源：六篇 arXiv 的 abs 頁（標題都對）與 `arxiv.org/pdf/<id>` 全文（pdftotext），Nature 的 HTML 全文，NIST SP 800-188 的 PDF 全文，ICO 的 HTML。九個網址都回 200。

做法：先逐條重查第一輪的四處事實修改，對照一手全文；再從其餘主張抽三分之一查核（固定亂數種子從 32 條中抽 11 條）；最後以台灣一般讀者的角度把全文讀一遍，修改讀起來吃力的地方。

## 修改

1. 「本文以訓練用途為主……內容依據 Self-Instruct 論文、模型崩潰的相關研究，以及美國 NIST 與英國 ICO 的文件；客服問答是假設示例，沒有實測，論文的數字也只代表該論文的設定。」→「本文以訓練用途為主，隱私用途另用一節說明。客服問答是假設示例，沒有實測；論文的數字也只代表該論文的設定。」｜措辭：description 與各節已寫出來源，這裡的來源列舉重複，刪掉後開頭比較短｜無
2. 「NIST SP 800-188 把從原始資料抽樣、只替換部分列、欄或儲存格（或加上雜訊）的稱為部分合成，其餘內容仍是原始記錄；……」→「NIST SP 800-188 把只替換原始資料中部分列、欄或儲存格（或加上雜訊）、其餘仍是原始記錄的，稱為部分合成；……」｜措辭：原句讀到「稱為部分合成」才補「其餘內容仍是原始記錄」，句子不好跟。內容沒變，和第 4.4 節列舉的兩種做法、表 3、第 4.4.1 節一致｜https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf
3. 清單「新指令與池中任何一條的 ROUGE-L 相似度要小於 0.7」→「……ROUGE-L 相似度（看文字重疊多少）要小於 0.7」｜措辭：一般讀者不知道 ROUGE-L 是什麼，後文的 33.1 分也用它｜https://arxiv.org/abs/2212.10560
4. 「原始內容分佈的尾端會先消失」→「原始內容分佈的尾端（少見的內容）會先消失」｜措辭：補白話說明。論文把尾端寫成 low-probability events，定義早期崩潰為先失去尾端資訊｜https://www.nature.com/articles/s41586-024-07566-y
5. 「他們用約 900 萬到 1.25 億參數的小型語言模型，訓練資料是一份由另一個模型產生的短篇故事集，每代重新訓練新模型：……；影像與分子的生成模型有類似結果，線性模型的理論分析也證明累積時誤差有上界。」→「他們用約 900 萬到 1.25 億參數的幾種小型語言模型，資料是一份由另一個模型產生的短篇故事集：……。影像與分子的生成模型結果類似；簡化的線性模型也證明，累積時誤差不會無限上升。」｜措辭：「有上界」改成白話（論文寫的是 "a finite upper bound independent of the number of iterations"）；刪掉「每代重新訓練新模型」這個一般讀者用不到的設定細節，只是省略，不影響結論｜https://arxiv.org/abs/2404.01413
6. 「2025 年一篇針對最大概似估計的理論研究，分析的正是資料逐代累積的設定：在標準假設下，即使真實資料占比趨近於零也能避免崩潰，但缺少額外假設時，即使原始資料還在，崩潰也可能任意快地發生。」→「2025 年一篇理論研究同樣分析資料逐代累積，對象是最大概似估計這種統計方法：在標準假設下，真實資料占比趨近於零也能避免崩潰；少了額外假設，即使原始資料還在，也可能很快崩潰。」｜措辭：讓讀者知道最大概似估計是一種統計方法；「任意快地發生」是直譯，改成「很快」。第一輪補的「累積設定」保留｜https://arxiv.org/abs/2505.19046
7. 「另有研究把『用合成資料訓練出的模型比產生資料的原模型差』視為崩潰，在矩陣特徵值與新聞摘要兩個任務中，……用驗證器篩選後，有些不完美的驗證器也能避免崩潰；但在新聞摘要任務裡，改用另一個摘要分數更高的模型來篩，效果和隨機挑選差不多。可見資料怎麼篩、由誰來篩，本身就是變數。」→「……在計算矩陣特徵值與新聞摘要兩個任務中，不篩選就會出現。先用驗證器（判斷資料好壞的程式或模型）篩過，即使驗證器不完美，有些也能避免崩潰。但在新聞摘要任務裡，讓產生資料的模型自己挑，結果勝過原模型；改用另一個摘要分數更高的模型來挑，效果卻和隨機挑選差不多。可見資料由誰篩、怎麼篩，本身就是變數。」｜措辭：原句的「改用」沒說是相對於什麼，讀者看不出對照組。補上的那句今天在全文核對過，第 6.2 節原文是 "self-selection leads to better performance than the generator, while Llama-3 verification results in performance similar to random selection"。第一輪改過的事實沒有變。這處是新增已核對的主張，不是更正錯誤，不算事實修改｜https://arxiv.org/abs/2406.07515
8. 「深度學習模型是否背下訓練資料也難以量化」→「深度學習模型背下多少訓練資料也難以量化」｜措辭：照原文 "difficult to quantify the extent to which the model is memorizing" 寫得更貼切｜https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf

改後正文 2,731 字，直接用 `app.guides.pack_ingest._body_length` 算（第一輪後是 2,744）。字數只少了一點：白話說明加了字，刪掉的重複內容抵掉這些。模型崩潰一節仍有五篇研究，但每篇只剩一個結論，加上必要的設定，術語都有白話說明。結構沒變：5 個 H2、1 個表格、1 個 callout、1 張圖解；四個指派連結（ai-term-knowledge-distillation、ai-term-supervised-fine-tuning、ai-term-pretraining、ai-terms-index）都在。SVG 沒有改，圖上的 1、2、3 代正文都有。

同步更新了 `notes.md`（NIST 部分合成的說法、Barzilai–Shamir／Schaeffer／Feng 改記全文讀法與 Feng 等人的定義與篩選結果、NIST 記憶化的說法、字數，以及一行第二輪備註）和 `research.json`（上述三篇的 access 與 claims、Nature 兩個設定的輪數、NIST 與 ICO 的 claim 措辭、`running_text_characters` 改為 2731、notes 中「只讀到摘要」一句）。

dry-run：`pack_cli ingest --from ../../docs/ai-terms-series/batch-02/staging --slug ai-term-synthetic-data --dry-run` 結束碼 0，輸出 "dry run: nothing written"。只有既有的 `no_summary` 警告，屬結構問題，沒有動。

## 重查第一輪的修改（全文核對，都成立）

- NIST 部分合成與完全合成：第 4.4 節列兩種做法，一是抽樣後對高揭露風險的儲存格加雜訊或換成插補值（部分合成），二是用原始資料建模、再由模型產生資料集（完全合成）。表 3 寫部分合成是 "selectively replacing rows, columns, or cells ... with values produced by a statistical model or by the addition of unrelated statistical noise"，完全合成是 "no one-to-one mapping between the records of the original and synthetic datasets"。第 4.4.4 節又寫建模是做完全合成的「一種」方法。正文寫法相符。https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf
- Shumailov 等人的兩個設定："Five epochs, no original training data" 與 "Ten epochs, 10% of original training data preserved ... a random 10% of the original data points is sampled"。前者困惑度上升（圖 1 說明 "increase in perplexity"），後者 "only minor degradation"，"Both training regimes lead to degraded performance"。微調的是 OPT-125m。https://www.nature.com/articles/s41586-024-07566-y
- Barzilai 與 Shamir：摘要寫 "a natural setting where synthetic data is gradually added to the original data set"；第 1 節寫起初 n 筆真實樣本，每輪最新模型產生 n 筆新樣本，與先前所有資料累積後訓練下一個模型；並寫 "such claims [資料累積就不會崩潰] can only be true under structural assumptions beyond MLE consistency"。兩個主要結論與正文一致。v3（2026-03-26）是 NeurIPS 2025 論文，arXiv 首版 2025 年 5 月，正文寫「2025 年」合理。https://arxiv.org/abs/2505.19046
- Feng 等人：第 6 節 "we refer to model collapse whenever the performance of the model trained on synthetic data is worse than that of the original generator"。第 6.1 節不驗證時，即使用 1,000 萬筆（原訓練集的 50 倍）也不如產生器；加雜訊的驗證器在 p* 約 0.65 以上時勝過產生器。第 6.2 節隨機挑選、資料量相同時不如產生器，自我篩選勝過產生器，用 Llama-3（ROUGE-1 較高）驗證與隨機挑選相近。https://arxiv.org/abs/2406.07515

## 抽查其餘主張（11 條，都成立）

- 合成資料定義（演算法、生成模型或模擬產生，模仿真實資料特徵，不是直接由人產生、不是從真實世界收集）：Liu 等人第 1 節與第 4 節（"artificially generated rather than collected from real-world sources"）。https://arxiv.org/abs/2404.07503
- 兩種用法：Liu 等人同時寫到訓練資料與隱私（"mitigate privacy concerns by creating anonymized or de-identified datasets"）。ICO 也寫合成資料可用於訓練 AI。
- 以指令與答案配對做監督式微調：Self-Instruct 第 2.3 節 "train the model to generate the instance output in a standard supervised way"。https://arxiv.org/abs/2212.10560
- 生成文字混入網路語料與來源追蹤：Nature 討論段 "it is unclear how content generated by LLMs can be tracked at scale"。Feng 等人摘要也寫生成文字會成為預訓練語料的一部分。
- ROUGE-L 小於 0.7 才收進任務池、剔除重複與啟發式異常、最後微調原模型：Self-Instruct 第 2.2、2.3 節。
- 52,445 條指令、82,439 個實例：Self-Instruct 表 1。
- 1.25 億參數：Nature 寫 "We fine-tune the OPT-125m causal language model"。
- 替換與累積的定義（第 1 代真實資料；替換只用上一代輸出；累積保留全部）：Gerstgrasser 等人圖 1 與第 2.1 節 "either replace or concatenate the previous dataset with the newly generated dataset"。https://arxiv.org/abs/2404.01413
- 影像與分子生成模型結果類似：摘要 "diffusion models for molecule conformation generation and variational autoencoders for image generation"。VAE 累積時誤差仍會上升，但 "significantly slower"，正文寫「類似」不算過頭。
- NIST 建議在資料本身標示 SYNTHETIC PERSON：第 4.4.4 節。
- 表格六格：「不給真資料也能測試、分析」對應 NIST 第 4.4.4 節 "without exposing real data"；「仍可能洩漏個人資訊」「能否推回真人」對應 NIST 第 4.4.4、4.4.6 節與 ICO；「錯誤、單調、偏見」「正確性與多樣性」對應 Self-Instruct 的品質抽樣（58% 輸出正確）、ROUGE-L 多樣性過濾，以及限制一節講的偏見。這兩格是歸納，不是單一來源原句，與第一輪判斷相同。

另外順手核對了不在抽樣內、但改寫時碰到的句子：Self-Instruct 的 92%／79%／58%／54%、一位作者標註、6.8→39.9（+33.1）；限制一節 "Tail phenomena" 與 "Reinforcing LM biases"；ICO 的匿名判準、擬真度取捨、三種攻擊、離群值抑制與差分隱私可能降低效用、偏誤被帶進合成資料、頁首 "under review" 聲明（今天仍在）；Schaeffer 等人人工標註 28 篇、八種定義（摘要、圖 1）；Gerstgrasser 等人討論段的「至少四種相關現象」。都成立。

系列規矩：沒有型號、價格、截止日期、排行榜分數；示例標明假設、沒寫成觀察結果；「成員推論」是 inference 的對應，全文沒有「推理」；沒有保證式說法；用語是台灣用語。

## 我懷疑但沒改的事

- Nature 兩個設定的「5 輪／10 輪」：論文寫 "trained for five epochs starting on the original dataset" 與 "trained for ten epochs on the original dataset"，沒有明說輪數是每一代都一樣，還是只指第一個模型。正文寫「（訓練 5 輪）」，沒有加「每代」，保留了這個模糊。兩組同時改了輪數與是否保留原始資料，論文沒有把兩個因素拆開。
- Feng 等人的新聞摘要任務：隨機挑選的資料量加大後，結果 "nearly match the performance of the generator"。正文「不篩選就會出現」指的是資料量相同時的比較，沒有再細分。
- 「本文開頭用的是較寬的『表現逐代變差』說法」：Feng 等人只比較一次訓練，不是逐代。這個說法與 Schaeffer 等人摘要的廣義定義（後代模型用前代產生的資料訓練後表現下降）一致，所以保留。
- 「兩份文件都把差分隱私列為控制洩漏量的方法」：NIST 原文就是控制洩漏量；ICO 是把它列為保護離群值記錄、防連結攻擊的方法。兩者方向相同，正文的概括略寬，沒有改。
- 字數 2,731，仍高於 brief 的目標區間 2,100–2,500，但在 1,800–3,000 之內。再刪就要刪 brief 要求寫出的論文設定（輪數、保留比例、模型規模、標註方式），所以沒有再刪。
- `no_summary` 警告：加 summary 區塊會改結構，依指令不動。
- 「分佈」：台灣教育部標準字是「分布」，但「分佈」在台灣也常用，全文用法一致，沒有改。
- 程序備註：本機的 scratchpad 目錄有其他平行查核者在用。我第一次放在那裡的計數腳本與 pack 備份被別篇的同名檔案覆蓋，其中一次是別人的唯讀計數腳本讀了本篇（印出 2754），沒有寫入。之後改用自己的子目錄，並在每個腳本裡檢查 slug。本篇的改前原文以我開工時讀到的版本為準。沒有跑 git，也沒有寫本目錄以外的 repo 檔案。

facts_changed: 0
