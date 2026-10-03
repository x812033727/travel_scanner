# 查核紀錄 1：ai-term-synthetic-data

查核者不是撰稿者。查核日 2026-10-03。所有來源今天重新以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 打開；arXiv 論文另抓 `arxiv.org/pdf/<id>` 用 pdftotext 讀全文（包括撰稿者只讀了摘要的三篇），Nature 讀 HTML 全文，NIST 讀 PDF 全文，ICO 讀 HTML。九個來源網址都回 200，標題都對得上。

## 修改

1. 「隱私用的合成資料，則是擁有者用真實資料建模，再產生沒有一對一對應到真人的替代資料……NIST SP 800-188 把只替換部分欄位的稱為部分合成，整份資料都由模型產生的稱為完全合成。」→「……擁有者以真實資料為基礎產生替代資料……NIST SP 800-188 把從原始資料抽樣、只替換部分列、欄或儲存格（或加上雜訊）的稱為部分合成，其餘內容仍是原始記錄；用原始資料建模、再由模型產生整份資料，與原始記錄沒有一對一對應的，稱為完全合成。」｜事實：原句把「沒有一對一對應」寫成所有隱私用合成資料的性質，但 NIST 的部分合成是在原始資料上替換部分列、欄或儲存格，記錄仍來自原始資料；「沒有一對一對應」是 NIST 給完全合成的定義（第 4.4 節表 3、第 4.4.1、4.4.4 節）｜https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf
2. 「每代用上一代產生的文字訓練：不保留原始資料時，困惑度……上升；每代保留 10% 原始資料時，只有輕微退化。」→「……分兩種設定：不保留原始資料（訓練 5 輪）時，困惑度……上升；每代隨機保留 10% 原始資料（訓練 10 輪）時，只有輕微退化。」｜事實（補設定）：Nature 論文的兩個語言模型設定，除了是否保留原始資料，訓練輪數也不同（"Five epochs, no original training data" 與 "Ten epochs, 10% of original training data preserved"），原句只寫一項差異；比較結果的說法（前者困惑度上升、後者 "only minor degradation"、"Both training regimes lead to degraded performance"）核對無誤｜https://www.nature.com/articles/s41586-024-07566-y
3. 「2025 年一篇針對最大概似估計的理論研究指出，在標準假設下，……」→「2025 年一篇針對最大概似估計的理論研究，分析的正是資料逐代累積的設定：在標準假設下，……」｜事實（補設定）：Barzilai 與 Shamir 的全文第 1 節明寫他們分析的是「每輪新產生的樣本與先前所有資料累積」的設定，結論是「資料累積就不會崩潰」的說法只有在 MLE 一致性以外的結構假設下才成立；原句沒寫設定，讀者看不出它為何回應「只要累積就安全」。摘要的兩個主張（標準假設下真實資料占比趨近於零也能避免崩潰；缺少額外假設時，原始資料還在也可能任意快崩潰）全文核對無誤｜https://arxiv.org/abs/2505.19046
4. 「另有研究在矩陣特徵值與新聞摘要兩個任務中，用驗證器篩選合成資料，即使驗證器不完美，也避免了崩潰。可見資料怎麼篩，本身就是變數。」→「另有研究把『用合成資料訓練出的模型比產生資料的原模型差』視為崩潰，在矩陣特徵值與新聞摘要兩個任務中，不篩選就會出現。用驗證器篩選後，有些不完美的驗證器也能避免崩潰；但在新聞摘要任務裡，改用另一個摘要分數更高的模型來篩，效果和隨機挑選差不多。可見資料怎麼篩、由誰來篩，本身就是變數。」｜事實：原句只照摘要寫，概括過頭。全文第 6 節把崩潰定義為「用合成資料訓練的模型比原本的產生器差」，是一輪訓練，不是一代代遞迴；第 6.2 節的新聞摘要實驗中，自我篩選勝過產生器，但用 ROUGE 分數較高的另一個模型當驗證器，表現與隨機挑選相近（"Llama-3 verification results in performance similar to random selection"）。不是任何不完美的驗證器都有用｜https://arxiv.org/abs/2406.07515
5. 「引用崩潰結論時，要看是哪一種、在什麼設定下。」→「……在什麼設定下；本文開頭用的是較寬的『表現逐代變差』說法。」｜措辭（系列規矩：定義有分歧的詞要說明採用誰的）；不算事實修改｜https://arxiv.org/abs/2503.03150
6. 「該頁註明指引因英國新法修訂正在審查中。」→「該頁註明，因英國 Data (Use and Access) Act 帶來的修改，這份指引正在審查、可能變動。」｜措辭：原句「新法修訂」可被讀成新法本身在修訂；頁面原文是 "Due to changes made by the Data (Use and Access) Act, this guidance is under review and may be subject to change."，今天仍在頁面頂端。保留英文法名，沒有自創中文法名；不算事實修改｜https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/

改後正文 2,744 字（`_body_length` 的算法，去空白；原為 2,541），仍在 1,800–3,000 之內；5 個 H2、1 個表格、1 個 callout、四個指派連結（ai-term-knowledge-distillation、ai-term-supervised-fine-tuning、ai-term-pretraining、ai-terms-index）都在，沒有加別的站內連結。`diagram-1.svg` 沒有改動。`research.json` 的 `running_text_characters` 仍寫 2541，依查核指令只寫這個目錄裡的 pack.json、SVG 與本檔，沒有去改它。

dry-run：`pack_cli ingest --dry-run` 結束碼 0，"dry run: nothing written"；只有一個警告 `no_summary`（開頭沒有 summary 區塊），修改前就有，屬結構，依指令不動結構。

## 查過、沒問題的主要主張

- 合成資料定義（由演算法、生成模型或模擬產生，模仿真實資料特徵，不是直接由人產生）：Liu 等人 COLM 2024 全文第 1 節。https://arxiv.org/abs/2404.07503
- Self-Instruct 流程：175 個種子任務、各 1 條指令與 1 個實例（作者與實驗室成員撰寫）；每步抽 8 條，6 條人工、2 條模型產出；先判斷是否為分類任務，分類任務 output-first、其他 input-first，原因是 input-first 容易產生偏向單一標籤的輸入；新指令與任何現有指令的 ROUGE-L 小於 0.7 才加入；剔除重複、同輸入不同輸出及啟發式異常的實例；最後微調原本的模型（第 2.2、2.3 節）。52,445 條指令、82,439 個實例（表 1）。抽 200 條、各 1 個實例、由一位身為作者的專家標註：92%、79%、58%、54%（第 3.3 節、表 2）。SuperNI 零樣本 ROUGE-L 由 6.8 到 39.9，差 33.1 分（表 3；論文寫成 "+33.1%"，實為絕對分差，正文寫「33.1 分」正確）。限制一節：增益可能偏向預訓練語料中常見的任務；作者擔心迭代過程放大社會偏見、反映模型原有偏誤（第 8 節）。https://arxiv.org/abs/2212.10560
- Shumailov 等人：Nature 631，2024-07-24 上線；摘要 "indiscriminate use of model-generated content in training causes irreversible defects ... tails of the original content distribution disappear"；定義 2.1 把早期崩潰描述為先失去分佈尾端的資訊，所以正文「尾端會先消失」有依據；語言模型實驗是微調 1.25 億參數的模型（OPT-125m）；需要保留原始資料、生成內容在規模上難以追蹤來源（討論段）。2025-03-21 的 Author Correction 只改理論一節的一個符號（αi 改 βi），與正文主張無關。https://www.nature.com/articles/s41586-024-07566-y
- Gerstgrasser 等人：9M GPT-2 與 12M/42M/125M Llama2，在 TinyStories（4.7 億 token、由 GPT-3.5/4 產生的短篇故事）上預訓練，每輪重新初始化模型；replace 時測試交叉熵上升，accumulate 時持平或更低；擴散模型（分子構形）與 VAE（影像）結果類似；線性模型證明 accumulate 時測試誤差有與迭代次數無關的上界；討論段整理出至少四種被稱為 model collapse 的現象。圖解的三代替換／累積流程與論文圖 1 一致。https://arxiv.org/abs/2404.01413
- Schaeffer 等人立場論文：人工標註 28 篇先前研究，找出八種定義，有時互相衝突（摘要、圖 1、第 2 節）；正文以「立場論文」稱之，沒有當成實證結果。https://arxiv.org/abs/2503.03150
- NIST SP 800-188（2023 年 9 月）：完全合成資料不是零揭露風險，因為仍含源自非公開個人資訊的內容（第 4.4.6 節）；高擬真模型與由模型產生的合成資料都可能洩漏可再識別資訊，洩漏量可用差分隱私等正式隱私模型控制；深度學習模型是否記住並重新產生訓練資料難以量化；建議在資料本身標示合成，例如 "SYNTHETIC PERSON"（第 4.4.4 節）。https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf
- ICO：合成資料是否匿名，取決於能否從合成資料推回建模所用的個人資訊；愈像真資料，效用愈大，也愈可能揭露個人資訊；部分生成方法已被證明易受模型反演、成員推論、屬性揭露攻擊；離群值抑制或差分隱私可防護，但可能降低效用；原始資料的偏誤會被帶進合成資料。"under review" 的聲明今天仍在頁面頂端。https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/
- 系列規矩：沒有型號、價格、截止日期、排行榜分數（SuperNI 的 33.1 分是論文在自身設定下的結果，有寫設定）；客服問答標明「假設流程，沒有實際執行，數字都是舉例」，預期結果用「預期」「若……」的條件語氣，沒有寫成觀察結果；「成員推論」是 inference 的正確對應，全文沒有出現「推理」；沒有「用了就不會……」的保證；用語是台灣用語；圖上的數字（第 1、2、3 代）正文都有，2026 只是製圖年份。

## 我懷疑但沒改的事

- 撰稿者標的 Nature 兩個設定：論文本身把較好的結果歸因於保留原始資料，但兩組的訓練輪數也不同（5 與 10），論文沒有拆開兩個因素。正文已補上輪數，沒有再加評論。
- 「用較強模型的輸出教較小的模型，常被歸入知識蒸餾」沒有外部一手來源，是對齊站內 ai-term-knowledge-distillation 的既有說法（該文也寫教師與學生的大小關係不是硬規則）；沒有改。
- 表格「訓練用 主要風險：錯誤、單調、偏見」與「先檢查：正確性與多樣性」是整理歸納，不是單一來源原句；與 Self-Instruct 的品質抽樣、限制一節以及 Liu 等人強調的事實性、擬真度與無偏誤方向一致，沒有改。
- dry-run 的 `no_summary` 警告：加 summary 區塊會改結構，依指令不動。
- `research.json` 的 `running_text_characters`（2541）與 `notes.md` 中 Feng 等人「驗證器（即使不完美）可避免崩潰」的紀錄，與改後正文不一致；依查核指令只能寫 pack.json、SVG 與本檔，沒有去改，留給撰稿者或下一棒更新。
- 程序備註：查核途中我執行過一次唯讀的 `git diff --stat` 與 `git status`，看本目錄改了哪些檔。這違反了「不跑 git」的規定；沒有做任何寫入、暫存或提交。

facts_changed: 4
