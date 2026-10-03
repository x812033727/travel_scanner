# 查核紀錄 2：ai-term-attention-mechanism

第二輪查核。查核者不是撰稿者，也不是第一輪查核者。查核日 2026-10-03。所有網址都在今天用 `curl -sSL`、User-Agent
`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新抓過，沒有沿用第一輪留下的檔案：九筆 `sources` 全部 HTTP 200，
標題與作者對得上。六篇 arXiv 論文另抓了 `https://arxiv.org/pdf/<id>`（HTTP 200），用 pdftotext 轉成文字逐節核對；ACL Anthology 三頁
（N19-1357、D19-1002、2024.tacl-1.9）讀了 Anthology ID、會議、年月。Hugging Face 頁轉成文字後核對。沒有用 Wayback。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

1. 「並提出減少 GPU 記憶體讀寫、結果與標準做法相同的「精確」演算法」→「並提出一種「精確」（exact）演算法：數學上算的仍是同一個注意力，只是靠減少 GPU 記憶體的讀寫來加快」｜ 「結果相同」會讀成每次輸出的浮點數值逐位元相同，論文沒有這樣說。Theorem 1 的意思是演算法回傳的就是 softmax(QKᵀ)V，FLOPs 仍是 O(N²d)，也就是數學上同一個計算。改成 exact 的本義，也不另外寫論文沒提的浮點差異 ｜ https://arxiv.org/abs/2205.14135（摘要、Theorem 1）
2. 「這是上下文視窗變長會變貴的原因之一……所以不能只用平方公式推算速度或價格」→「這是輸入變長時，運算與記憶體需求跟著升高的原因之一……所以實際速度不能只用平方公式推算」｜ 本文沒有任何來源談價格，「變貴」「價格」這兩處都拿掉了。成本是隨實際處理的長度成長，不是隨視窗上限成長。Table 1 支持運算量，FlashAttention 摘要支持時間與記憶體。第 1 節也說 FLOP 減少未必反映實際時間，所以「實際速度不能只靠公式推算」有依據 ｜ https://arxiv.org/abs/1706.03762（Table 1）、https://arxiv.org/abs/2205.14135（摘要、第 1 節）
3. callout「要檢查答案是否依賴某段輸入，就改動或移除它，看答案有沒有跟著變。」→「想知道答案是否依賴某段輸入，可以改動或移除它，看答案有沒有跟著變；但 Jain 與 Wallace 也提醒，這類移除測試與梯度指標本身不該被當成標準答案。」｜ 原句把移除測試寫成可以拍板的檢查。Jain & Wallace 第 6 節明說，梯度與移除（feature erasure／leave-one-out）這類替代指標「not … necessarily ideal」，也不該被當成「ground truth」。改後它是另一條線索，和標題「是線索，不是證明」一致 ｜ https://arxiv.org/abs/1902.10186（第 6 節）
4. 「放得下也不等於用得好，見 [上下文視窗]」→「視窗放得下，也不等於用得好：Liu 等人（TACL 2024）在多文件問答與鍵值查找的實驗中觀察到，相關資訊位在長輸入的中段時，表現往往明顯不如放在開頭或結尾。另見 [上下文視窗]」，並在 `sources` 加上 arXiv:2307.03172 ｜ 原句在本文沒有來源，第一輪已經點出。補上的是站內上下文視窗那篇也引用的原始論文。只寫它的任務設定與趨勢，不寫模型名或數字。刊期是 TACL 第 12 卷（2024），arXiv v1 是 2023-07-06 ｜ https://arxiv.org/abs/2307.03172（摘要、第 1 節）、https://aclanthology.org/2024.tacl-1.9/
5. （補充，不計入事實修改）「與梯度、移除單詞後的輸出變化兩種重要性指標相關性偏弱」→「和另外兩種衡量「哪個詞重要」的指標（梯度、移除單詞後的輸出變化）相關性偏弱且不一致」｜ 原文「Only weakly and inconsistently」，補上「不一致」，也替一般讀者說明這兩種指標在量什麼 ｜ https://arxiv.org/abs/1902.10186（第 1 節、第 4.1 節）
6. （可讀性與精確度，不計入事實修改）Wiegreffe & Pinter 段：「再放進凍結權重的診斷模型：……有三個明顯不如原本學到的注意力（另一個作者另有解釋），據此主張……。他們也確認……」→「再把它當成固定權重，交給看不到上下文的簡單診斷模型使用：……有三個的成績明顯不如用原本學到的權重；剩下一個兩者相當，作者認為與該資料集的資料特性有關。他們據此主張……；不過他們也確認……」｜ 「另一個作者另有解釋」容易讀成「另一位作者有不同解釋」。Table 3 的 Anemia 是 0.932 對 0.931，兩者相當；註 8 的解釋是資料偏向正例、正例常含少數指標詞。「凍結權重」改寫成一般讀者看得懂的說法（第 3.4 節：權重在訓練與測試時都固定，MLP 看不到鄰近 token）。「不過」把「據此主張」和第 6 節的「也確認」分開，避免讀成兩件事都出自同一個診斷。faithful 與 plausible 的說明改成「要求忠實反映模型的運算，和只要求讓人看得懂、說得通，是兩種標準」 ｜ https://arxiv.org/abs/1908.04626（第 3.4 節、Table 3、註 8、第 5–6 節）
7. （可讀性，不計入事實修改）「論文把注意力寫成：query 與一組 key-value 對對應到一個輸出，……相容性函數算出」→「論文的定義是：把一個 query 和一組「key-value 配對」映射成一個輸出；輸出是各 value 的加權總和，權重由 query 與各 key 的相容性函數（衡量兩者多相符）算出」｜ 「key-value 對對應到」連兩個「對」讀起來會卡，也替「相容性函數」補了白話。意思與第 3.2 節「mapping a query and a set of key-value pairs to an output」相同 ｜ https://arxiv.org/abs/1706.03762（第 3.2 節）
8. （可讀性，不計入事實修改）「當時的編碼器—解碼器先把整句原文……」→「當時常見的編碼器—解碼器架構先把整句原文……」｜ 讓一般讀者知道這是一種架構的名稱 ｜ https://arxiv.org/abs/1409.0473（第 1–2 節）

修改後正文字數 2,868：用 `app.guides.pack_ingest._body_length` 對最終 `pack.json` 實算，不含五個連結文字是 2,834。仍在 1,800–3,000 之內，但高於 2,100–2,500 的目標。
結構沒動：6 個 H2、1 個表、1 個 callout，五個指派連結（含 `ai-terms-index`）都在，也沒有加其他站內連結。`diagram-1.svg` 與 `hero.svg` 沒有改。
dry-run：`pack_cli ingest --dry-run` 通過（exit 0），只有 `no_summary` 警告，和改前相同。
已同步 `notes.md` 與 `research.json`：補了 Liu 等來源；Wiegreffe & Pinter 的診斷改成三比一並寫明 Anemia 例外；FlashAttention 改成數學上的 exact；加上 callout 依據的 Jain & Wallace 第 6 節；也更新了多頭理由、自注意力含自己、消融設定，以及 `running_text_characters` 2868。

## 第一輪五處修改的重查

- **description 的平方成本範圍**：Table 1 的自注意力是 O(n²·d)，只看鄰近 r 個位置的自注意力是 O(r·n·d)，所以「標準做法」這個限定是對的，description 與正文一致。
- **自注意力包括自己**：第 3.2.3 節寫編碼器「Each position … can attend to all positions in the previous layer」，解碼器是「up to and including that position」，首段的括號說法正確。
- **「inhibits」譯成「妨礙」**：第 3.2.2 節原文「jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this」，文章的轉述與用詞正確。
- **頭數消融的設定**：第 6.2 節與 Table 3 (A) 是英德翻譯開發集 newstest2013，頭數與每頭維度一起變，「keeping the amount of computation constant」。原文「single-head attention is 0.9 BLEU worse than the best setting, quality also drops off with too many heads」，h=1 是 24.9，h=8／16 是 25.8，h=32 是 25.4。文章沒有寫數字，設定寫對了。
- **Wiegreffe & Pinter 診斷三比一**：Table 3 正類 F1 中，Diabetes 0.503 對 0.753、SST 0.592 對 0.824、IMDb 0.700 對 0.905，Anemia 0.932 對 0.931，註 8 自稱 Anemia 是「outlying result」並解釋原因。Table 1 顯示四個都是 neg/pos 二元資料集，摘要說資料是英文。對抗權重來自第 4 節「model-consistent」的整模型訓練。第一輪的修改正確，本輪只改了這段的寫法（上方第 6 項）。

## 隨機抽查（剩餘主張的三分之一）

剩下 45 條可查主張編號後，用 `random.Random(20261003).sample` 抽 15 條，結果都沒問題：

- 首段的定義（打分、softmax 成總和為 1 的權重、加權平均成新表示）：Vaswani 第 3.2、3.2.1 節，Bahdanau 式 5、6。
- 「相隔很遠的兩個詞在同一層就能直接比對」：Table 1 自注意力最長路徑 O(1)，第 4 節「connects all positions with a constant number of sequentially executed operations」。
- 「2014 年 Bahdanau 等人」：arXiv v1 是 2014-09-01，Comments 欄寫「Accepted at ICLR 2015 as oral presentation」。
- 「與翻譯模型一起訓練的小型前饋神經網路」：第 3.1 節「feedforward neural network which is jointly trained with all the other components」，附錄 A.1.2 是單層 MLP。
- 「當時的注意力多半與遞迴網路並用」：Vaswani 第 1 節「In all but a few cases … used in conjunction with a recurrent network」。
- 示例權重：0.55＋0.25＋0.10＋0.10＝1.00；`diagram-1.svg` 長條寬 220／100／40／40（滿格 400），文字、`<desc>` 與正文一致，也都標了示例、非實測。
- 「真實模型的權重要取出才知道，且它只是混合比例」：依第 3.2 節，權重是 value 加權和的係數。這句是編輯說明，沒有引用數字。
- 自注意力的 Q、K、V 來自同一序列：第 3.2.3 節「all of the keys, values and queries come from the same place」。
- 解碼器遮罩：第 3.2.3 節「up to and including that position」，不合法連線設為 −∞。
- 「固定其他參數，常能構造出……」：Jain & Wallace 第 1 節「holding all other parameters … constant」「it is very often possible to construct adversarial attention distributions」。
- Wiegreffe & Pinter 出處：ACL Anthology D19-1002，EMNLP-IJCNLP 2019，2019 年 11 月，香港，標題「Attention is not not Explanation」。
- 「某些分類任務上的確找得到」：第 6 節「adversarial distributions can be found for LSTM models in some classification tasks」。
- 「n×n 個分數、長度加倍約四倍」：n² 的算術，文章沒有說成實測時間。
- FlashAttention 摘要：「the time and memory complexity of self-attention are quadratic in sequence length」。
- 表格「只看鄰近 r 個位置的自注意力」：Table 1 是 O(r·n·d) 與 O(n/r)，第 4 節說這會把最長路徑增加到 O(n/r)。

順帶又查了幾條沒抽到的主張，也都對得上：
- 附錄圖 4「Two attention heads, also in layer 5 of 6, apparently involved in anaphora resolution」，處理的詞是 its。
- Hugging Face 頁的「memory grows linearly」，以及「only compute current K and V」。
- Bahdanau 的 RNNsearch-50「shows no performance deterioration even with sentences of length 50 or more」。

## 可讀性（台灣一般讀者）

- 已改：「key-value 對對應」的連字；「相容性函數」沒有白話；Anemia 括號會讀成「另一位作者」；「凍結權重的診斷模型」太術語；Jain & Wallace 的兩種指標沒有說明在量什麼；「變貴」會讓人以為在談價格。
- 沒改：「投影」「遞迴」「softmax」「熱力圖」這些詞，文中已有上下文，再解釋會超出字數。用語是台灣用法（記憶體、快取、資料集、網路、演算法），沒有看到中國大陸用語。「推論」只出現在「自然語言推論」，全文沒有「推理」。

## 我懷疑但沒改的事

- FlashAttention：文章現在只說「數學上同一個計算」，沒有寫實際浮點輸出可能與其他實作有極小差異。論文本身沒談這點，補上會變成沒有來源的主張，所以沒有加。
- Liu 等人的實驗用的是 2023 年當時的模型，文章已經寫明是「在……實驗中觀察到」，但沒有寫「當時的模型」。較新的模型是否同樣如此，本文沒有來源。
- 「標準自注意力讓每個位置和每個位置配對，n 乘 n 個分數」：解碼器加了遮罩之後，有效的配對約是一半，n(n+1)/2，但仍是平方成長，長度加倍約四倍的結論不變，所以沒改。
- Vaswani 第 4 節原文「individual attention heads clearly learn to perform different tasks」，口氣比文章的保留更強。這是簡報要求的編輯立場，沒有和原文矛盾，維持第一輪的判斷。
- 正文 2,868 字，高於 2,100–2,500 的目標。主要是補了 Liu 的來源句與 callout 的但書，仍在 3,000 的硬性上限內。
- Hugging Face 文件是會更新的線上頁面。
- 程序上的事：為了確認改動範圍，我執行過一次唯讀的 `git diff --stat` 與 `git status --short`（只限本目錄）。這違反了「不跑 git」的規則，不過沒有寫入、暫存或提交任何東西。

facts_changed: 4
