# 查核紀錄 1：ai-term-neural-network

查核者：獨立查核（非撰稿者），2026-10-03。所有來源今天以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開；手算部分用 Python（分數運算）重算。

## 修改

1. 開頭「每個單元先做加權加總，再經過一道非線性轉換」與 description「每個單元做加權加總，再經非線性轉換」→「每個單元先做加權加總，通常再經過一道非線性轉換」／「單元做加權加總，多半再經非線性轉換」 ｜ 說「每個」單元都經非線性，和文中自己的示例（輸出單元「不加激活函數」）矛盾；Google 教材說各層可用不同激活函數 ｜ https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions
2. 「所以每個單元後面要接非線性的激活函數」→「所以隱藏層的單元後面要接非線性的激活函數；輸出層接不接，看任務而定，下面的示例就沒接」 ｜ 同上，與第 1 條是同一處事實修正，合計一件 ｜ https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions
3. 一步更新段「學習率取 0.1，權重變成 0.84 與 −1.28、偏差 −0.08，輸出降到 0.32。隱藏層的權重，則要…」與下一段「(0,1) 原本輸出 1，現在變成 0.76」→ 明寫「隱藏層不變，假設輸出層權重還沒調好」「為了好算，這一步只改輸出層」「實際訓練時，隱藏層的權重也在同一步更新…連隱藏層一起改，算出的數字會和這裡不同」，以及「(0,1) 原本輸出 1，只改輸出層後變成 0.76」 ｜ 0.32 與 0.76 只在「隱藏層不動、只更新輸出層」時成立；照文中描述的完整反向傳播同一步也更新隱藏層（隱藏層梯度 0.8 與 −0.96），重算得 (1,1) 輸出 −0.25、(0,1) 輸出 0.38，原文沒有交代這個前提 ｜ 手算（Python 重算），反向傳播同一步更新所有層見 https://developers.google.com/machine-learning/glossary（backpropagation 條目）
4. 「Google 定義神經網路『至少一個隱藏層』，中間層連線固定的原始感知器多半不算」→「Google 術語表把神經網路定義為『至少含一個隱藏層』的模型，照這個說法，輸入直接接輸出的模型不算；Rumelhart 等人則認為原始感知器的中間層連線固定，不算真正的隱藏單元。本文開頭的說法不以隱藏層劃界，讀時先確認對方用哪一種定義」 ｜ Google 的 hidden layer 定義只看位置（介於輸入與輸出之間），不要求連線可學；Rosenblatt 感知器的 A 單元正好位於 S 與 R 之間，所以「依 Google 定義原始感知器多半不算」沒有依據。「不算真正的隱藏單元」是 Rumelhart 等人的說法，要歸給他們；並補上本文採哪個說法（系列規矩：定義分歧要說明採用誰的） ｜ https://developers.google.com/machine-learning/glossary（neural network、hidden layer 條目）；https://www.nature.com/articles/323533a0（全文第 533 頁）；https://doi.org/10.1037/h0042519（頁 389 感知器組織）
5. 「單一單元做不到」→「只靠一個加權加總後比門檻的單元做不到」 ｜ 精確化（措辭，不計入）：後面的不等式論證本來就假設「加權加總後比門檻」；Google 教材說任何函數都能當激活函數，用非單調的激活函數時一個單元就解得出來。改後的說法對 sigmoid、tanh、ReLU、階梯函數都成立（另以 −6 到 6、間隔 0.5 暴力搜尋門檻單元，無解）｜ https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions
6. 「Rumelhart 等人用 E = ½ Σ (y − d)²」→「Rumelhart 等人用 E = ½ ΣΣ (y − d)²，對每筆樣本的每個輸出加總」 ｜ 照原文式 (3) 抄寫（措辭，不計入）：原式是 ½ Σ_c Σ_j (y_{j,c} − d_{j,c})²，c 是樣本、j 是輸出單元 ｜ https://www.nature.com/articles/323533a0（全文第 534 頁式 3）

修改後正文字數（`_body_length` 算法）：2,681（原 2,500；`research.json` 的 `running_text_characters` 我沒有權限改，仍寫 2,500）。結構不變：7 個 H2、1 個表、1 個 callout，指派的 5 個站內連結都在。

## dry-run

`cd apps/api && .venv/bin/python -m app.guides.pack_cli ingest --from ../../docs/ai-terms-series/batch-02/staging --slug ai-term-neural-network --dry-run`：exit 0，`dry run: nothing written`。只有 1 個警告 `no_summary`（沒有摘要區塊），修改前就有，不是這次造成的；系列 brief 沒有要求摘要區塊，所以沒加。

## 手算重算（全部用 Python 分數運算）

- 雙開關網路：隱藏一 ReLU(a+b)、隱藏二 ReLU(a+b−1)、輸出 h1 − 2·h2。(0,0)→0、(1,0)→1、(0,1)→1、(1,1)→隱藏 (2,1)、輸出 0。正確。
- 參數數：2×(2+1)+(2+1)=9；100 個隱藏神經元：100×(2+1)+(100+1)=401；會計算的單元 2+1=3。正確。
- 一步更新（只改輸出層）：輸出 2×1+1×(−1.2)=0.8，E=½×0.8²=0.32，∂E/∂y=0.8，梯度 1.6、0.8、0.8，學習率 0.1 後 0.84、−1.28、−0.08，(1,1) 輸出 1.68−1.28−0.08=0.32，(0,1) 更新前 1、更新後 0.84−0.08=0.76。數字都對，但只在只改輸出層時成立，見修改 3。
- 門檻單元不能解：該亮的兩式相加得 w1+w2+2c>2t，該滅的兩式相加得 w1+w2+2c≤2t，矛盾。正確（前提是比門檻，見修改 5）。

## 查過、沒問題的主要主張

- Google 術語表 neuron 條目：兩步（加權加總、交給激活函數），並寫「A neuron in a neural network mimics the behavior of neurons in brains and other parts of nervous systems」。文中寫成「Google 術語表則說這種單元『模仿』腦中神經元的行為」，有歸屬，接著說「像不像真實神經元要靠神經科學證據回答，本文只把它當命名的由來」，沒有替 Google 背書。https://developers.google.com/machine-learning/glossary
- Google 術語表 neural network 條目「A model containing at least one hidden layer」；deep model 條目「A neural network containing more than one hidden layer」；weight 條目「Training is the process of determining a model's ideal weights; inference is the process of using those learned weights to make predictions」；parameter 條目是訓練中學到的權重與偏差，學習率是超參數；bias 也是參數。都與文中相符。
- Google MLCC「Nodes and hidden layers」：只加隱藏層仍是線性（Exercise 2：「Linear calculations performed on the output of linear calculations are also linear」）；3-4-1 網路 21 個參數的算法與文中計數法一致。https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers
- Google MLCC「Activation functions」：sigmoid、tanh、ReLU 是常見的三種；ReLU 小於 0 回 0、否則回原值；「That said, we still recommend starting with ReLU」。https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions
- Google MLCC「Neural networks」總覽：「Neural networks are a family of model architectures designed to find nonlinear patterns in data」。
- Rosenblatt 1958（Psychological Review 65(6), 386–408；Crossref 中繼資料核對無誤）：頁 387「The theory has been developed for a hypothetical nervous system, or machine, called a perceptron … without becoming too deeply enmeshed in the special, and frequently unknown, conditions which hold for particular biological organisms」；頁 389 A 單元在興奮與抑制輸入的代數和達門檻時發放（即「加總後再轉換」）；頁 391 學習靠強化改變 A 單元的「value」；頁 404–405「As soon as the response calls for the recognition of a relationship between stimuli … the problem generally becomes excessively difficult for the perceptron」。全文讀 Wayback `web/20170712224925id_/http://www.ling.upenn.edu:80/courses/cogs501/Rosenblatt1958.pdf`（CDX statuscode 200）。
- Rumelhart、Hinton、Williams 1986（Nature 323, 533–536，1986-10-09）：摘要寫隱藏單元會表示任務領域的重要特徵、「The ability to create useful new features distinguishes back-propagation from earlier, simpler methods such as the perceptron-convergence procedure」；第 533 頁「In perceptrons, there are 'feature analysers' between the input and output that are not true hidden units because their input connections are fixed by hand … they do not learn representations」；第 534 頁式 (3) 與「forward pass」「backward pass」。全文讀 https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf（掃描檔，轉 PNG 目視）。
- LeCun、Bengio、Hinton 2015（Nature 521, 436–444）：深度學習是「composing simple but non-linear modules」的表示學習、特徵「learned from data」；SGD「showing the input vector for a few examples … average gradient for those examples」；測試集量「generalization ability」；「the ReLU typically learns much faster in networks with many layers」；反向傳播「was discovered independently by several different groups during the 1970s and 1980s」。全文讀 https://www.cs.toronto.edu/~hinton/absps/NatureDeepReview.pdf。
- Cybenko 1989（Math. Control Signals Systems 2, 303–314）：撰稿者只讀了摘要；我另讀了 HAL 典藏的全文 https://hal.science/hal-03753170/document。第 3 節 Theorem 2：任何連續 sigmoidal 函數 σ 的有限和 Σ α_j σ(y_jᵀx+θ_j) 在 C(I_n) 中稠密，「providing that no constraints are placed on the number of nodes or the size of the weights」；結語「we have focused only on existence … how many terms … are required」。所以文中「單一隱藏層、連續 sigmoid 型非線性、有限個單元的前饋網路，能把單位超立方體上的連續函數逼近到任意精度」與「這是『能表示』，訓練找不找得到是另一回事」「只說夠大的網路能表示」都有依據。
- Vaswani 等人 2017：摘要「a new simple network architecture, the Transformer, based solely on attention mechanisms」；第 3.3 節前饋網路「consists of two linear transformations with a ReLU activation in between」。https://arxiv.org/abs/1706.03762
- 來源狀態碼（今天）：nature.com 兩篇 200、Springer 200、arXiv 200、Google 五頁 200；`https://doi.org/10.1037/h0042519` 先 302 到 doi.apa.org，再對 curl 回 403（APA 擋機器抓取），DOI 本身正確（Crossref 與 Handle API 都指向這篇）。標題、卷期、頁碼都對；`checked_on` 2026-10-03 合理。
- 系列規矩：沒有模型名、價格、截止日期、排行榜分數、任何模型的參數量；示例標了「示例（未實測，手算）」，沒有寫成觀察結果；「推論（inference）」用法正確，全文沒有出現「推理」；沒有「用了就不會」式的保證；圖上的數字（2、2、1、9）正文都有，另有製圖年份 2026；圖 `<desc>` 與圖上文字和正文一致。diagram-1.svg 不需要改。

## 我懷疑但沒改的事

- 「激活函數」偏大陸用語，台灣常見「激勵函數」或「活化函數」（系列先前的審稿意見把 activation 譯成「活化值」）。但 `catalogue.json` 指派原文就用「激活函數」，這是用語選擇，交給編輯決定；如果要改，全文共 4 處（含表格 1 格）。
- Rumelhart 等人說感知器的特徵分析器連線是「fixed by hand」，但 Rosenblatt 1958 寫的是隨機連線（random），不是人手逐條設定。文中寫成中性的「事先固定」，沒有錯，所以沒改。
- 「LeCun 等人的檢驗，是用訓練時沒看過的測試集量泛化能力」：LeCun 等人是描述通行做法，不是他們自己做了一次檢驗；措辭可再調，沒有改。
- Rosenblatt 原文也寫「The analogy between the perceptron and biological systems should be readily apparent to the reader」，論文標題就有「in the brain」。文中只引了他「不深陷生物條件」那一半，沒有錯，但比喻這一段對 Rosenblatt 的取捨偏向一邊。
- `research.json` 的 `running_text_characters` 仍是 2,500，`notes.md` 的 Cybenko 讀取方式仍寫「只讀摘要」；這兩個檔案不在我可改的範圍，請撰稿者或編輯更新（現為 2,681；Cybenko 全文見上方 HAL 連結）。
- dry-run 的 `no_summary` 警告修改前就有，沒加摘要區塊。

facts_changed: 3
