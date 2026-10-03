# ai-term-overfitting 查核紀錄（verify-1）

查核者不是撰稿者。2026-10-03 以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開所有來源：
`sources` 原有 15 筆全部 200，新增 1 筆也 200。論文全文以 pdftotext 讀（arXiv 1611.03530 v2、1912.02292、2405.00332 v4、JMLR dropout PDF），
《Deep Learning》第 5、7 章讀作者官網 pdf2htmlEX 頁的文字層，樂詞網讀檢索結果頁 HTML 裡的結果列。

## 修改

1. 「dropout 出自 Srivastava 等人 2014 年的論文，目的是減少大型神經網路的過度擬合」→「dropout 最早見於 Hinton 等人 2012 年的預印本，Srivastava 等人 2014 年的期刊論文再完整說明，目的是減少大型神經網路的過度擬合」｜dropout 最早見於 2012 年 7 月的 arXiv 預印本（摘要已用 "dropout" 一詞並報告減少過度擬合），JMLR 2014 是後來的完整期刊版，寫「出自 2014 年論文」是錯的出處｜https://arxiv.org/abs/1207.0580 、https://jmlr.org/papers/v15/srivastava14a.html
2. 「把 CIFAR10 與 ImageNet 的標籤換成隨機亂標⋯⋯訓練誤差仍降到 0，測試表現只剩亂猜的程度；圖片換成純雜訊也一樣」→「⋯⋯CIFAR10 上訓練誤差仍降到 0 或接近 0，ImageNet 上訓練準確率也有 95.20%，測試則都只剩亂猜的程度；在 CIFAR10 上把圖片換成純雜訊也背得下來」｜論文自己的表 2 與第 2 節：ImageNet 隨機標籤（Inception V3、未調超參數）top-1 訓練準確率 95.20%，沒到 0 訓練誤差；CIFAR10 表 1 隨機標籤訓練準確率 99.34%–100%；隨機像素與高斯雜訊實驗在 CIFAR10（圖 1）。原句照摘要與引言的籠統說法，對不上論文自己的數字｜https://arxiv.org/abs/1611.03530 （全文 https://arxiv.org/pdf/1611.03530 v2）
3. （措辭，不計入）「Goodfellow 等人的《Deep Learning》第 5 章更嚴格：」→「⋯⋯第 5 章說得更明確：」｜Google 的 Dividing the original dataset 練習題已明說依測試集結果調超參數會讓模型隱性配合測試集，「更嚴格」暗示 Google 允許這麼做｜https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets
4. `sources` 在 Srivastava 2014 後新增 Hinton 等人 2012（arXiv:1207.0580），支援修改 1。共 16 筆。

改完 `_body_length` = 2,674（原 2,598），在 1,800–3,000 內但超過 2,600 的目標。dry-run 通過，只剩協調者另外處理的 `no_summary` 警告。
`notes.md`、`research.json` 已同步（新增來源、Zhang 2017 主張改寫、`running_text_characters` 2674）。`diagram-1.svg`、`hero.svg` 不需修改。

## 查過、沒問題的主要主張

- 樂詞網 overfitting 7 筆：過度擬合 ×4（氣象、地球科學－大氣、電子工程、土木工程－測量及圖學）、過度配適（統計）、過擬合（電機工程）、過度適配；過度擬合{人工智慧}（視覺藝術）。underfitting 2 筆皆為「低度擬合」。第一段「多數領域與標註人工智慧的條目寫過度擬合，也收過擬合、過度配適」正確。
- Google 速成課程 Overfitting：定義（貼近／記住訓練集，無法正確預測新資料）、低度擬合連訓練資料都預測不好、泛化是過度擬合的相反；Figure 15「strongly implies overfitting」、兩條曲線先相似後分岔；原因粗分兩類（訓練集不具代表性、模型太複雜）。
- Google Dividing the original dataset：三份切分、驗證集先測、測試集最後複查；驗證集與測試集反覆使用會 wear out，要補新資料；刪掉驗證集與測試集裡和訓練集重複的例子。詞彙表 test set 條目：每筆資料只屬於一份。
- Google L2 regularization：正則化率越高越不易過度擬合；正則化率相對學習率太高會預測不好；提早停止「quick, but rarely optimal」。詞彙表 underfitting 條目：特徵錯、訓練輪數太少、正則化率太高、隱藏層太少（表格「可以先試」欄依此）。Model complexity：簡單模型在新資料常較好、先從少數特徵開始、minimize(loss + complexity)。
- 詞彙表 co-adaptation／dropout regularization：dropout 讓神經元不能只依賴特定其他神經元；繁中詞彙表譯「丟棄正則化」。
- 《Deep Learning》5.2：低度擬合＝訓練誤差不夠低、過度擬合＝訓練與測試誤差差距太大、容量的定義與高容量會記住對測試集無用的性質。5.3：測試集不得以任何方式參與選擇（含超參數）、驗證集從訓練資料切出、約 80%／20%；同一測試集多年反覆使用使評估偏樂觀、基準過時。
- 《Deep Learning》7.1.1：L2 參數範數懲罰常稱權重衰減、把權重拉向原點；7.4：更多資料是讓模型泛化更好的最佳辦法、影像平移幾個像素、不可改變正確類別；7.8：回傳驗證誤差最低時的參數。
- Srivastava 2014 摘要：大型深度網路過度擬合嚴重、訓練時隨機拿掉單元以防共同適應、在視覺、語音、文件分類、計算生物學改善表現。
- Zhang 2017：ICLR 2017（arXiv 註記 Published in ICLR 2017）；表 1 Inception、無 random crop、無 weight decay：真實標籤 train 100.0／test 85.75，隨機標籤 train 100.0／test 9.78；有效容量足以記住整份資料；VC 維度、Rademacher 複雜度、一致穩定性無法解釋；顯式正則化（weight decay、dropout、資料擴增）可能改善泛化但既非必要、單靠也不足；尚無正式指標說明這些模型為何「簡單」；實驗皆為影像分類。
- Nakkiran 2019：CIFAR-10、CIFAR-100、IWSLT'14 de-en 等設定；欠參數區呈 U 形、過了插值門檻後測試誤差再降；高峰在 EMC 約等於樣本數（剛好能把訓練誤差壓到接近 0）；「all forms of double descent most strongly in settings with label noise」；部分設定增加樣本反而更差。正文有寫設定，沒有推廣成通則。
- Sainz 2023 摘要：最嚴重的資料汙染＝LLM 用基準的測試切分訓練、再用同一基準評測，造成成績高估；立場論文。
- GSM1k（Hugh Zhang 等人，arXiv v4，NeurIPS 2024 Datasets and Benchmarks）：1,205 題、純人工撰寫、照 GSM8k 風格與難度、發表時不公開；準確率最多下降 8%（論文寫 "up to 8%"）；Spearman r² = 0.36；許多模型、尤其前沿模型幾乎沒有過度擬合跡象，所有模型大致能泛化到新題；第 5 節：過度擬合不完全來自汙染，可能來自收集與基準相似的資料或依基準分數挑選 checkpoint，少量汙染不一定造成過度擬合。正文未點名任何模型。
- Recht 2019 摘要：照原流程重建 CIFAR-10、ImageNet 測試集，準確率下降 3%–15% 與 11%–14%；下降不是 adaptivity 造成，而是對稍難圖片泛化不足。
- 示例：標「示例（數字為編寫，未實際訓練）」，沒有寫成觀察結果。diagram-1.svg 的折線座標換算回去正好是 30／31、8／12、1／20，驗證誤差最低點在第 8 輪、訓練誤差單調下降；圖上數字 1、8、20、8%、12%、1%、20%、2026 正文都有。渲染無疊字、超框。
- 系列規矩：topics 含 `ai-terms`；「本文」「這篇」0 次；正文沒有查證過程；沒有「推論」「推理」；沒有型號、價格、截止日期、排行榜分數；過度擬合的兩種定義（Google：新資料表現差；Goodfellow：訓練與測試誤差差距太大）都寫了；沒有「用了就不會」式保證（對策段寫「都不保證有效」）；「模型越大越容易過度擬合」只以否定形式出現；台灣用語（雜訊、資料、權重衰減、最佳）。指派的 5 個站內連結都在，沒有多餘連結。結構：7 個 H2、恰好 1 個表、1 個 callout。

## 我懷疑但沒改的事

- 第一段「Google 繁中教材多寫『過度配適』」：繁中 Overfitting 課程頁標題用「過度配適」，但內文「過度配適」「過度擬合」各 11 次；繁中詞彙表 18 比 10。合計確實較多，所以沒改，但只看課程頁其實是各半。
- GSM1k 的「最多下降約 8%」照論文 "up to 8%"；論文沒寫清楚是百分點還是相對比例，正文也沒寫。
- 「L2 正則化（又稱權重衰減）」照《Deep Learning》7.1.1 的說法；用 Adam 這類自適應最佳化器時兩者並不等價，正文沒提，對概念篇可接受。
- Sainz 等人的 arXiv 註記寫 "Accepted at EMNLP2024-Findings"，和我記得的 2023 年不同；正文只寫「2023 年的立場論文」（arXiv 2023-10-27），不受影響，沒有再查會議頁。
- 正文 2,674 字，超過 brief 2,200–2,600 的目標（仍在 3,000 上限內）；為了不改寫沒問題的段落，沒有另外刪字。

facts_changed: 2
