# 查證與編輯紀錄：ai-term-attention-mechanism

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律是實際打開該頁的 2026-10-03。
讀取方式：「abs」＝`curl -sSL` 讀 arXiv 摘要頁（HTTP 200，含投稿歷史）；「全文」＝`curl -sSL https://arxiv.org/pdf/<id>`（HTTP 200）下載後以 pdftotext 轉成文字，逐節核對；User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，沒有帶任何人的 email 或個資。沒有使用 Wayback。

## 歷史：翻譯對齊（Bahdanau 等，arXiv:1409.0473，ICLR 2015）

2014 年投稿（v1 為 2014-09-01）；ICLR 2015 口頭報告｜https://arxiv.org/abs/1409.0473｜2026-10-03｜abs（投稿歷史與 Comments 欄）
當時的編碼器—解碼器把原文壓成固定長度向量；作者推測這是瓶頸｜https://arxiv.org/abs/1409.0473｜2026-10-03｜abs 摘要 + 全文第 1 節
解碼器每產生一個目標詞，用對齊模型 a(s_{i-1}, h_j) 打分，經 softmax 得到權重 α_ij，再把各位置的 annotation 加權和成 context vector c_i（式 5、6）｜https://arxiv.org/abs/1409.0473｜2026-10-03｜全文第 3.1 節
對齊模型是與整個系統共同訓練的前饋網路（附錄 A.1.2 為單隱藏層 MLP）｜https://arxiv.org/abs/1409.0473｜2026-10-03｜全文第 3.1 節、附錄 A.1.2
論文自己的說法：「Intuitively, this implements a mechanism of attention in the decoder」，即以「注意」比喻加權｜https://arxiv.org/abs/1409.0473｜2026-10-03｜全文第 3.1 節（文中「注意力不是人類專注、是數學加權」是本文編輯框架，不是論文語句）
英法翻譯實驗：RNNencdec 的表現隨句長明顯下滑；RNNsearch-50（訓練句長上限 50 個詞）在 50 個詞以上的句子沒有看到下滑。訓練句長上限 30／50 兩種設定見第 4.2 節｜https://arxiv.org/abs/1409.0473｜2026-10-03｜全文第 4.2、5.1 節與圖 2。文章只寫趨勢與設定，不寫 BLEU 數字

## 歷史與機制：只用注意力（Vaswani 等，arXiv:1706.03762）

2017 年投稿（v1 為 2017-06-12）｜https://arxiv.org/abs/1706.03762｜2026-10-03｜abs
注意力多半與遞迴網路並用；提出完全依賴注意力、不用遞迴與卷積的 Transformer｜https://arxiv.org/abs/1706.03762｜2026-10-03｜abs 摘要 + 全文第 1 節
注意力＝把 query 與一組 key-value 對對應到輸出；輸出是 value 的加權和；權重由 query 與對應 key 的相容性函數算出｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文第 3.2 節
縮放點積注意力：query 與所有 key 內積、除以 √d_k、softmax、對 value 加權（式 1）；縮放理由「We suspect that…」是作者推測，文章寫「推測」｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文第 3.2.1 節
query、key、value 由學到的線性投影得到；多頭＝投影 h 次、平行做注意力、串接、再投影｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文第 3.2.2 節
基本設定 h=8、d_k=d_v=d_model/h=64、d_model=512；每頭縮小後總計算量與單頭全維度相近；理由「With a single attention head, averaging inhibits this」｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文第 3.2.2 節與第 3.1 節（d_model=512）
三種用法：encoder-decoder attention（query 來自解碼器上一層，key、value 來自編碼器輸出，並說明這是在模仿 seq2seq 模型中常見的做法，引用文獻含 Bahdanau 等）、編碼器自注意力、解碼器自注意力加遮罩（不合法連線設為 −∞）｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文第 3.2.3 節
每層運算量與最長路徑：自注意力 O(n²·d)、O(1)；遞迴 O(n·d²)、O(n)；只看 r 個鄰近位置的自注意力 O(r·n·d)、O(n/r)｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文 Table 1 與第 4 節
頭數過多品質下降（消融實驗，英德翻譯開發集 newstest2013，計算量不變）｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文第 6.2 節與 Table 3 (A)（h=1 為 24.9、h=8 與 16 為 25.8、h=32 為 25.4 BLEU；文章不寫數字）
附錄圖 4：編碼器第 5 層（共 6 層）兩個頭處理 its，作者寫「apparently involved in anaphora resolution」；圖 5 說明許多頭的行為「seems related to the structure of the sentence」。文章只轉述為作者的觀察，並註明不保證重現｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文附錄 Attention Visualizations（圖 3–5）

## 注意力權重與解釋（Jain & Wallace；Wiegreffe & Pinter）

Jain & Wallace 發表於 NAACL 2019（N19-1357，2019 年 6 月）｜https://aclanthology.org/N19-1357/｜2026-10-03｜curl 讀 ACL Anthology 頁（HTTP 200，citation meta 與 Anthology ID）
設定：帶注意力的 BiLSTM（對照有平均編碼器與 CNN），任務為文本分類、問答、自然語言推論，英文資料集；未涵蓋 seq2seq｜https://arxiv.org/abs/1902.10186｜2026-10-03｜全文第 2 節與第 6 節（「we have not considered seq2seq tasks」）
結果一：遞迴編碼器上，注意力權重與梯度、leave-one-out 兩種特徵重要性的相關性弱且不一致（Kendall τ）｜https://arxiv.org/abs/1902.10186｜2026-10-03｜全文第 4.1 節與摘要
結果二：固定其他參數（含 h、θ），可構造出重心完全不同卻預測幾乎相同的對抗注意力分布；隨機打亂權重常只造成小幅輸出變化。文章寫「常能」，因論文原文是「very often」「often」｜https://arxiv.org/abs/1902.10186｜2026-10-03｜全文第 1 節、第 4.2 節
結論：標準注意力模組不提供有意義的解釋，不應被當成有；作者自陳限制（相關性指標本身有爭議、只考慮少數注意力變體、尚有 plausible 解釋可能多個）｜https://arxiv.org/abs/1902.10186｜2026-10-03｜摘要與第 6 節
Wiegreffe & Pinter 發表於 EMNLP-IJCNLP 2019（D19-1002，2019 年 11 月）｜https://aclanthology.org/D19-1002/｜2026-10-03｜curl 讀 ACL Anthology 頁（HTTP 200）
結論取決於「解釋」的定義（faithful 與 plausible 之分）；測試必須考慮模型所有部分；提出四項檢驗（均勻權重基線、隨機種子變異校準、凍結權重的診斷 MLP、端到端對抗訓練）｜https://arxiv.org/abs/1908.04626｜2026-10-03｜abs 摘要 + 全文第 1、5、6 節
對抗分布確實能找到，但模型一致訓練下沒有先前做法那麼極端，且在診斷 MLP 上表現不如原本學到的注意力，所以「先前工作並未證明注意力無用於解釋」｜https://arxiv.org/abs/1908.04626｜2026-10-03｜全文第 1 節末與第 6 節
部分資料集上凍結成均勻權重的表現與學到的權重相近（文章已略）｜https://arxiv.org/abs/1908.04626｜2026-10-03｜全文第 1 節（§3.2）

## 成本與上下文視窗

自注意力的時間與記憶體複雜度對序列長度是平方；FlashAttention 是「精確」注意力演算法，靠減少 GPU 記憶體階層間的讀寫加速，結果與標準注意力相同。文章不寫速度倍數、序列長度或準確率數字｜https://arxiv.org/abs/2205.14135｜2026-10-03｜abs 摘要（只讀摘要，沒有讀全文）
推論時可快取先前 token 的 key、value，每步只算新 token 的；記憶體隨序列長度線性增加（文件原文：memory grows linearly）｜https://huggingface.co/docs/transformers/en/cache_explanation｜2026-10-03｜curl -sSL 讀 HTML（HTTP 200），轉成文字後核對「How caching works」一頁
n×n 個分數、長度加倍約四倍：由 Table 1 的 n² 項直接推得的算術，只說明分數個數，不是實測時間｜https://arxiv.org/abs/1706.03762｜2026-10-03｜全文 Table 1（編輯推算）

## 編輯說明

示例：「小雅把行李箱放進後車廂，因為它太重了。」與權重 0.55／0.25／0.10／0.10（總和 1）全是為教學編的數字，文內與圖內都標明「示例」「非實測」；沒有取任何真實模型的權重。分詞僅為示意。
query＝我要找什麼、key＝我能被怎樣比對、value＝被選中時交出的內容，是教學用的比喻，文內寫「粗略的理解」；三篇原論文沒有這樣的白話定義。
簡報與來源的差異（來源為準）：（1）簡報寫 Wiegreffe & Pinter「反駁」，原文結論是「結論取決於解釋的定義」、「先前工作並未證明注意力無用於解釋」，並且確認對抗分布在部分任務找得到，故文章寫「回應」而非「反駁」。（2）Vaswani 等「只用注意力」：原文第 2 節寫「據作者所知」是第一個完全依賴自注意力的轉換模型，文章沒有寫「第一個」，只寫「完全依賴注意力、不用遞迴與卷積」。
正文字數（同 _body_length 算法）：2524；不含連結文字：2490。圖解與 hero 為原創向量圖；圖上數字 0.10、0.55、0.25、1 皆在正文出現，2026 為製圖年份（正文有「2026 年」）。
乾跑結果：`pack_cli ingest --dry-run` 無錯誤，僅 `no_summary` 警告（與範本相同，簡報未要求摘要區塊）。
