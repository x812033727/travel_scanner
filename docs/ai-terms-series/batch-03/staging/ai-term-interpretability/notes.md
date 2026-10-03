# 查證與編輯紀錄：ai-term-interpretability

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律是實際打開該頁的 2026-10-03。
讀取方式：「abs」＝`curl -sSL` 讀 arXiv 摘要頁（HTTP 200，含投稿歷史與 Comments 欄）；「全文」＝`curl -sSL https://arxiv.org/pdf/<id>`（HTTP 200）後以 pdftotext 轉文字逐節核對；「網頁」＝`curl -sSL` 取 HTML（HTTP 200）去標籤後閱讀。User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，沒有帶任何人的 email 或個資。沒有使用 Wayback。
本檔已依查核（verify-1.md，2026-10-03）同步到最終文字：Slack 等的敏感特徵、Jain 與 Wallace 的模型設定兩處事實已更正，並補上採用哪個定義。

## 譯名

interpretability 譯「可解釋性」，定義為「以人類可理解的用語，說明或呈現機器學習模型的推理過程」｜https://developers.google.com/machine-learning/glossary?hl=zh-tw#interpretability｜2026-10-03｜網頁（繁中版詞彙表，「可解釋性」條目與「黑盒模型」條目）
中文把 explainability 與 interpretability 都譯成「可解釋性」：臺大法學論叢論文摘要同時寫「AI 的可解釋性（explainability）」與「可解釋性（interpretability）」｜https://www.airitilibrary.com/Article/Detail/a0000446-N202312050009-00001｜2026-10-03｜網頁（華藝書目頁的中文摘要；全文 PDF 在作者個人網站，curl 連線被重設，沒有讀到全文，只用摘要支持「譯名相撞」這一點）
國教院樂詞網：以 `terms.naer.edu.tw/search/?q=interpretability` 查詢，回傳的是未套用查詢條件的總覽頁，沒有取得條目；文中不引用樂詞網。

## 定義分歧

Doshi-Velez 與 Kim 的定義「the ability to explain or to present in understandable terms to a human」｜https://arxiv.org/abs/1702.08608｜2026-10-03｜全文第 1 節
需要可解釋性源自問題形式化不完整（incompleteness），情境含安全、倫理、目標錯置等；後果不嚴重或已在實際應用充分驗證的系統不需要解釋｜https://arxiv.org/abs/1702.08608｜2026-10-03｜全文第 2 節
評估三層：application-grounded（真人真任務）、human-grounded（真人簡化任務）、functionally-grounded（不找人、代理任務）｜https://arxiv.org/abs/1702.08608｜2026-10-03｜全文第 3 節與圖 1
論文年份：v1 2017-02-28｜https://arxiv.org/abs/1702.08608｜2026-10-03｜abs
Lipton：可解釋性「has no formal technical meaning」、「not a monolithic concept」；動機（trust、causality、transferability、informativeness、fair and ethical decision-making）多元且有時衝突｜https://arxiv.org/abs/1606.03490｜2026-10-03｜摘要 + 全文第 1、2 節
Lipton 把性質分為 transparency（simulatability、decomposability、algorithmic transparency）與 post-hoc（text、visualization、local explanations、explanation by example）；文中只舉「人能在腦中跑完模型」為例，並寫「例如」｜https://arxiv.org/abs/1606.03490｜2026-10-03｜全文第 3 節
Lipton 質疑線性模型必然比深度網路好懂；維度夠高的線性模型也不透明｜https://arxiv.org/abs/1606.03490｜2026-10-03｜全文 3.1.1 節與 4.1 節
Lipton 論文年份與場合：v1 2016-06-10；Comments：presented at 2016 ICML Workshop on Human Interpretability in Machine Learning (WHI 2016)｜https://arxiv.org/abs/1606.03490｜2026-10-03｜abs
Rudin 區分 Explainable ML（另建 posthoc 模型解釋黑盒）與 inherently interpretable models；interpretability 是 domain-specific，沒有通用定義｜https://arxiv.org/abs/1811.10154｜2026-10-03｜全文第 1 節（Introduction）
Rudin：可解釋模型提供的解釋 faithful to what the model actually computes；準確度與可解釋性必然取捨是迷思，在有意義特徵的資料上這種取捨不典型（文中寫成她的「主張」）｜https://arxiv.org/abs/1811.10154｜2026-10-03｜全文第 2 節 (i)(ii)
Rudin 文章年份：Nature Machine Intelligence 2019（arXiv Comments 欄）｜https://arxiv.org/abs/1811.10154｜2026-10-03｜abs
NIST AI RMF 1.0（2023 年 1 月）第 3.5 節：explainability 是 AI 系統運作機制的表示、回答 how；interpretability 是輸出在設計用途下的意義、回答 why｜https://doi.org/10.6028/NIST.AI.100-1｜2026-10-03｜全文（`curl -sSL https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf`，HTTP 200，pdftotext）
「和機制可解釋性的用法正好相反」是編輯對照：NIST 把「機制」放在 explainability，Olah 等與 Anthropic 的研究把研究內部機制稱為 interpretability｜同上兩筆與 https://distill.pub/2020/circuits/zoom-in/｜2026-10-03｜編輯判斷

## 三類方法

天生可讀的模型例子（稀疏線性模型、規則清單、決策樹）｜https://arxiv.org/abs/1606.03490 、https://arxiv.org/abs/1811.10154｜2026-10-03｜全文
LIME：在單一預測附近學一個可解釋的局部模型｜https://arxiv.org/abs/1602.04938｜2026-10-03｜abs 摘要
SHAP：Shapley 值；從不知道任何特徵時的期望預測（base value）加到目前輸出；在 additive feature attribution 這一類中，同時滿足 local accuracy、missingness、consistency 的解唯一（Theorem 1）｜https://arxiv.org/abs/1705.07874｜2026-10-03｜全文第 2、3、4 節與圖 1
SHAP 精確計算困難，以近似估計（Kernel SHAP 等），可選擇假設特徵獨立與模型線性｜https://arxiv.org/abs/1705.07874｜2026-10-03｜全文第 4 節
航班延誤的 SHAP 拆解（0.20、+0.25、+0.12、+0.08、−0.03、0.62）是教學編造的示例，文中與圖上都標「示例／未實測」；加總 0.20+0.25+0.12+0.08−0.03=0.62 已手算｜—｜2026-10-03｜自編
機制可解釋性：Olah 等三個「deliberately speculative」主張（features 對應 directions；circuits 是 computational subgraph；universality）｜https://distill.pub/2020/circuits/zoom-in/｜2026-10-03｜網頁（Distill，2020-03-10）
多義神經元：InceptionV1 的 4e:55 同時回應貓臉、車頭與貓腿｜https://distill.pub/2020/circuits/zoom-in/｜2026-10-03｜網頁「Polysemantic Neurons」節

## 代表研究（Scaling Monosemanticity）

發表 2024-05-21，Anthropic；對象是該公司「medium-sized production model」（文中不寫型號，寫「中型商用語言模型」；sources 標題用短題名，不含型號）｜https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html｜2026-10-03｜網頁
SAE 訓練在中間層（middle layer）的 residual stream；residual stream 是之前各層輸出的總和｜同上｜2026-10-03｜網頁「Sparse Autoencoders」節與「Cross-Layer Superposition」段
三個 SAE：1,048,576（約 100 萬）、4,194,304（約 400 萬）、33,554,432（約 3,400 萬）個特徵；重建至少解釋 65% 的變異｜同上｜2026-10-03｜網頁 SAE 設定段落
特徵多語言、多模態（文字與圖片）｜同上｜2026-10-03｜網頁開頭摘要與 Golden Gate Bridge 例
把 Golden Gate Bridge 特徵 clamp 到最大活化值的 10 倍，模型開始自稱是金門大橋｜同上｜2026-10-03｜網頁「Influence on Behavior」
未找到全部特徵，即使只看中間層也可能差好幾個數量級（orders of magnitude short）｜同上｜2026-10-03｜網頁「Limitations, Challenges, and Open Problems」
模型能列出所有倫敦行政區，34M SAE 只找到約 60% 行政區的特徵｜同上｜2026-10-03｜網頁「Feature Completeness」
知道謊言、能說謊、真的說謊不同；不要從安全相關特徵的存在推論太多｜同上｜2026-10-03｜網頁開頭與 Discussion
可解釋性作為「test set for safety」的期望；觀察 very preliminary｜同上｜2026-10-03｜網頁「Generalization and Safety」

## 解釋的忠實度

plausibility 是對人的說服力，faithfulness 是準確反映模型真實推理過程；兩者可只滿足其一；忠實度評估不應依賴人的判斷｜https://arxiv.org/abs/2004.03685｜2026-10-03｜全文第 2、3 節（ACL 2020，abs Comments 欄）
NISTIR 8312（2021 年 9 月）四原則：Explanation、Meaningful、Explanation Accuracy、Knowledge Limits；explanation accuracy 與 decision accuracy 是不同概念；Meaningful 要求解釋讓預期對象理解，開發者與使用者需求不同｜https://doi.org/10.6028/NIST.IR.8312｜2026-10-03｜全文（`curl -sSL https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8312.pdf`，HTTP 200，pdftotext；第 2 節）
Adebayo 等：model parameter randomization test（訓練好的模型 vs 同架構隨機初始化網路）；Guided BackProp、Guided GradCAM 對較高層參數不敏感，Gradients 與 GradCAM 通過；只靠肉眼判斷會誤導｜https://arxiv.org/abs/1810.03292｜2026-10-03｜全文第 1 節 Contributions 與第 4 節（NeurIPS 2018；v3 修正 Guided Backprop 實驗、結論不變）
Slack 等：只依敏感屬性判斷的分類器（COMPAS 與 Communities and Crime 看種族，German credit 看性別；論文 Experimental Setup「Biased Classifier f」段）加上辨識擾動樣本（OOD）的外殼；三個資料集（COMPAS、Communities and Crime、German credit）；LIME 在三個資料集都被騙過；SHAP 單一無關特徵攻擊下 COMPAS 84%、CC 100%、German 85% 的資料點把重要度從敏感特徵移開，兩個特徵時 67%、71%（文中寫「在多數資料點上也沒把這個敏感特徵排第一」）｜https://arxiv.org/abs/1911.02508｜2026-10-03｜全文第 1 節與實驗結果段（AIES 2020）
注意力權重常與梯度式重要度不相關；可找到很不同的注意力分布但預測相同｜https://arxiv.org/abs/1902.10186｜2026-10-03｜abs 摘要（另見已上線的注意力機制專文）
Jain 與 Wallace 的設定：帶注意力的 BiLSTM（另比較 CNN 與平均編碼器），任務是文字分類、問答與自然語言推論，不是語言模型；所以文中寫「處理文字的模型」與「文字分類、問答等任務的模型」｜https://arxiv.org/abs/1902.10186｜2026-10-03｜全文第 1、2、3 節（`curl -sSL https://arxiv.org/pdf/1902.10186`，HTTP 200，pdftotext；NAACL 2019 見 abs Comments 欄）
思維鏈：加入偏向線索（如把選項重排讓答案總是 A），模型的步驟不提線索，卻替被帶偏的答案找理由｜https://arxiv.org/abs/2305.04388｜2026-10-03｜abs 摘要（另見已上線的思維鏈專文）

## 編輯判斷

定義採用：第一節列完各家說法後寫「以下採較寬的用法：和 Lipton 一樣，把事後解釋也算進可解釋性」。Lipton 把 post-hoc interpretability 列為可解釋性的兩大類之一（全文第 3.2 節）；Rudin 的窄用法會把第二類方法排除在 interpretable 之外，所以要說明。
讀者三問（給誰、什麼方法、忠實度驗證）是依 NIST Meaningful／Explanation Accuracy 原則與 Doshi-Velez 與 Kim 的評估分層整理出的讀法，不是任何來源的原句。
訂房推薦理由的例子是虛構情境，標「示例（虛構情境，未實測）」。
文中沒有型號、價格、排行榜分數。
