# 查核紀錄 1：ai-term-attention-mechanism

查核者不是撰稿者。查核日 2026-10-03。所有網址都在今天用 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新抓過；
八筆 `sources` 全部 HTTP 200，標題與作者對得上。五篇 arXiv 論文另抓了 `https://arxiv.org/pdf/<id>`（HTTP 200），用 pdftotext 轉成文字逐節核對；
FlashAttention 除了摘要，也讀了全文的 Theorem 1。ACL Anthology 兩頁讀了 citation metadata。沒有用 Wayback。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

1. description「也討論計算量隨長度平方成長」→「也討論標準做法的計算量隨長度平方成長」｜ 不加限定時讀起來像所有注意力都是平方；同一篇文章的表格裡，只看鄰近 r 個位置的自注意力就是 O(r·n·d)。正文已經限定在標準做法，description 補成一致 ｜ https://arxiv.org/abs/1706.03762（Table 1）
2. 首段「替其他每個位置打相關分數」→「替它可參考的每個位置（自注意力時也包括它自己）打相關分數」｜ 自注意力裡每個位置也會對自己打分；編碼器可看所有位置，解碼器可看「到自己為止（含自己）」的位置。「其他」把自己排除了，與機制不符 ｜ https://arxiv.org/abs/1706.03762（第 3.2.3 節）
3. 「作者的理由是單頭的加權平均會抹掉不同表示子空間的資訊」→「作者的理由是多頭讓模型能同時從不同表示子空間、不同位置取用資訊，只用單頭時，加權平均會妨礙這一點」｜ 原文是「allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this」，是「妨礙」不是「抹掉資訊」 ｜ https://arxiv.org/abs/1706.03762（第 3.2.2 節）
4. 「該論文的翻譯消融實驗顯示頭數過多品質反而下降」→「該論文的英德翻譯消融實驗（總計算量固定）顯示，單頭比最佳設定差，頭數過多品質也會下降」｜ 系列規則要寫出論文的設定：Table 3 (A) 是英德翻譯開發集 newstest2013，頭數與每頭維度一起變、總計算量固定；原文同時寫了單頭比最佳設定差 0.9 BLEU（文章不寫數字） ｜ https://arxiv.org/abs/1706.03762（第 6.2 節、Table 3）
5. 「他們的凍結權重診斷顯示，在其資料集上，對抗構造的分布不如原本學到的注意力，所以先前工作並未證明⋯⋯」→「他們改用整個模型一起訓練出對抗注意力，再放進凍結權重的診斷模型：四個英文二元分類資料集中，有三個明顯不如原本學到的注意力（另一個作者另有解釋），據此主張先前工作並未證明⋯⋯」｜ Table 3：Diabetes 0.503 對 0.753、SST 0.592 對 0.824、IMDb 0.700 對 0.905，但 Anemia 0.932 對 0.931 並沒有比較差，作者在註 8 自己說這是例外並解釋原因。「在其資料集上」會讀成全部都是。另外放進診斷的是作者自己第 4 節「一致訓練」的對抗分布，不是 Jain & Wallace 逐例構造的那種，補上避免混淆；結論改成明確歸屬於作者的主張 ｜ https://arxiv.org/abs/1908.04626（第 3.4 節、Table 3、第 4 節與註 8、第 6 節）
6. （補充，不計入事實修改）同段開頭補「他們認為相關性那部分的實驗有說服力，爭議在後半」｜ 原文第 2 節：「We find the experiments in this part of the paper convincing and do not focus our analysis here」。補上才看得出這是有保留的回應，不是全面反駁 ｜ https://arxiv.org/abs/1908.04626（第 2 節）
7. （呈現，不計入事實修改）表格圖說「整理自 Vaswani 等人 2017 的 Table 1」→「節錄自 Vaswani 等人 2017 的 Table 1（略去卷積層一列與循序運算數一欄）」｜ 文中表格只取了原表四列中的三列、四欄中的兩欄，避免讀者以為原表只有這些 ｜ https://arxiv.org/abs/1706.03762（Table 1）

修改後正文字數（同 `_body_length` 算法）2,643，仍在 1,800–3,000 之內；結構未動（6 個 H2、1 個表、1 個 callout、五個指派連結都在）。圖 `diagram-1.svg` 沒有改。
dry-run：`pack_cli ingest --dry-run` 通過，只有 `no_summary` 警告（改前改後相同）。

## 查過、沒問題的主要主張

- **Table 1 每一格**都對過原論文：自注意力 O(n²·d)、最長路徑 O(1)；遞迴 O(n·d²)、O(n)；限定鄰域 r 的自注意力 O(r·n·d)、O(n/r)；n 是序列長度、d 是表示維度、r 是鄰域大小。
- Bahdanau 等：v1 於 2014-09-01 上 arXiv，ICLR 2015 口頭報告；固定長度向量是瓶頸是作者「conjecture」（文章寫「推測」）；式 5、6 的加權和與 softmax 權重；對齊模型是與整個系統一起訓練的前饋網路（附錄 A.1.2 是單層 MLP）；英法翻譯中 RNNencdec 隨句長大幅下滑，RNNsearch-50（以最長 50 詞的句子訓練）在 50 詞以上的句子也「shows no performance deterioration」。
- Vaswani 等：當時注意力「In all but a few cases」與遞迴網路並用；Transformer 完全依賴注意力、不用遞迴與卷積；注意力的定義（query、key-value 對、相容性函數、value 加權和）；內積、除以 √d_k、softmax、加權四步，縮放理由是「We suspect」；h=8、d_k=d_v=64、d_model=512、總計算量與單頭全維度相近；encoder-decoder attention 的 query 來自解碼器、key/value 來自編碼器輸出；解碼器自注意力的遮罩（設為 −∞）；Bahdanau 是 additive attention（單隱藏層前饋網路），Vaswani 是內積；附錄圖 4 是第 5 層（共 6 層）兩個頭、看的是 its、原文是「apparently involved in anaphora resolution」。
- 示例權重：行李箱 0.55＋後車廂 0.25＋小雅 0.10＋其餘 0.10＝1.00；正文、圖上文字、圖的 `<desc>` 順序與數字一致；長條寬度 220／100／40／40 px（滿格 400 px）與權重成比例；標了「示例」「非實測」，沒有寫成觀察結果。圖上數字 0.10、0.55、0.25、1、2026 正文都有。
- Jain & Wallace：NAACL 2019（N19-1357，2019 年 6 月）；帶注意力的 BiLSTM，任務是文本分類、問答、自然語言推論，資料集都是英文；遞迴編碼器的注意力與梯度、leave-one-out 的相關「Only weakly and inconsistently」；「very often possible」構造出預測等價的對抗分布；摘要結論「standard attention modules do not provide meaningful explanations and should not be treated as though they do」；第 6 節自承沒涵蓋 seq2seq。
- Wiegreffe & Pinter：EMNLP-IJCNLP 2019（D19-1002，2019 年 11 月）；標題是「Attention is not not Explanation」；結論取決於解釋的定義（plausible 或 faithful）；測試要考慮模型所有部分；第 6 節確認 LSTM 在某些分類任務上確實找得到對抗分布，第 1 節說一致訓練的對抗分布沒有先前做法那麼極端。文章寫「回應」而不是「反駁」，與原文相符。
- 兩篇都只研究帶注意力的遞迴模型與英文資料，文章「不能直接外推到今日的大型 Transformer 語言模型」的保留是對的。
- FlashAttention：摘要寫自注意力的時間與記憶體複雜度對序列長度是平方、是 IO-aware 的 exact attention、減少 HBM 與 SRAM 之間的讀寫；全文 Theorem 1：輸出就是 softmax(QKᵀ)V，FLOPs 仍是 O(N²d)。文章沒有寫速度倍數或準確率數字。
- Hugging Face「How caching works」：每步只算目前 token 的 K、V，過去的 K、V 存在快取重用；原表寫「memory grows linearly」；只用於推論（inference）。
- 平方成長的說法在正文都限定在「標準做法」或「標準自注意力」；「n×n 個分數、長度加倍約四倍」是算術，文章沒有說成實測時間。
- 系列規則：沒有模型型號、價格、截止日期、排行榜分數或 BLEU 數字；「推論」只出現在「自然語言推論」（NLI），沒有出現「推理」；用語是台灣用法（記憶體、快取、演算法、資料集、遞迴、網路）；沒有「用了就不會」式保證；只連了指派的五個 slug。

## 我懷疑但沒改的事

- FlashAttention「結果與標準做法相同」：論文是說「exact」（Theorem 1 數學上回傳同一個結果）；實際浮點運算的輸出可能與其他實作有極小數值差異。這是論文本身的說法，沒有改。
- callout「要檢查答案是否依賴某段輸入，就改動或移除它，看答案有沒有跟著變」：這類移除或擾動測試（如 leave-one-out）本身也不是標準答案，Jain & Wallace 第 6 節自己說這些指標不是 ground truth。文章沒有寫成保證，所以沒改。
- Vaswani 第 4 節原文說「individual attention heads clearly learn to perform different tasks」，口氣比文章「這不表示每個頭固定負責一種語意」的保留更強。文章的保留是簡報要求的編輯立場，沒有和原文矛盾，沒有改。
- 「放得下也不等於用得好」這句在本文沒有來源，靠站內連結的上下文視窗文章支撐。
- `research.json` 的 `running_text_characters`（2524）與 `notes.md` 現在已經過期（改後 2,643），而且兩份檔案對 Wiegreffe & Pinter 診斷結果的描述（「perform poorly on the diagnostic」，沒有提到 Anemia 是例外）仍是改前的說法。這次查核只准寫 pack.json、diagram-1.svg、verify-1.md，所以沒有動這兩份檔案。
- 改後正文 2,643 字，超過目標 2,100–2,500，但在 1,800–3,000 的硬性範圍內。
- Hugging Face 文件是會更新的線上頁面，今天的內容日後可能改版。

facts_changed: 5
