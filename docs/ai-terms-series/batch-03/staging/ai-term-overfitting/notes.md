# ai-term-overfitting 查證紀錄

格式：主張｜來源網址｜查證日｜讀取方式。所有頁面以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 讀取，狀態碼 200。

## 譯名

overfitting 在樂詞網有 7 筆：過度擬合（氣象、地球科學－大氣、電子工程、土木工程－測量及圖學）、過度配適（統計）、過擬合（電機工程）、過度適配；過度擬合{人工智慧}（視覺藝術名詞欄位）｜https://terms.naer.edu.tw/search/?&query_term=overfitting&query_field=title&query_op=and｜2026-10-03｜curl 帶 cookie，檢索結果頁 HTML 轉文字（detail 頁直接開會被導回首頁）
underfitting 在樂詞網為「低度擬合」（氣象、地球科學－大氣）｜https://terms.naer.edu.tw/search/?&query_term=underfitting&query_field=title&query_op=and｜2026-10-03｜同上
regularization 在樂詞網數學、物理、力學名詞為「正則化」；Google 繁中詞彙表寫「L2 正則化」「丟棄正則化」（dropout regularization）「提早中止訓練」（early stopping）｜https://developers.google.com/machine-learning/glossary?hl=zh-tw｜2026-10-03｜curl，HTML 轉文字後搜尋
Google 繁中速成課程頁標題為「過度配適」，內文混用「過度擬合」，underfitting 寫「配適不足」／「欠配」｜https://developers.google.com/machine-learning/crash-course/overfitting/overfitting?hl=zh-tw｜2026-10-03｜curl，HTML 轉文字
採用決定：正文用「過度擬合」（樂詞網多數領域與標註人工智慧的條目都有，也和站上 ai-term-machine-learning、ai-term-fine-tuning 的寫法一致），標題並列「過擬合」方便搜尋；underfitting 用樂詞網的「低度擬合」，和「過度擬合」成對。

## 定義與資料切分

過度擬合＝模型貼近（記住）訓練集到無法對新資料正確預測；低度擬合連訓練資料都預測不好；泛化是過度擬合的相反｜https://developers.google.com/machine-learning/crash-course/overfitting/overfitting｜2026-10-03｜curl，HTML 轉文字
兩條損失曲線先相似後分岔（訓練降、驗證升）強烈暗示過度擬合（Figure 15 圖說「strongly implies overfitting」）｜同上｜2026-10-03｜同上
過度擬合原因粗分兩類：訓練集不足以代表真實資料、模型太複雜｜同上｜2026-10-03｜同上
建議切成訓練、驗證、測試三份；驗證集在訓練中做初步測試，測試集最後複查｜https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets｜2026-10-03｜curl，HTML 轉文字
驗證集與測試集反覆使用會「wear out」，要收集更多資料更新；依測試集結果反覆調超參數會讓模型隱性配合測試集｜同上｜2026-10-03｜同上
切分後要刪掉驗證集、測試集裡與訓練集重複的例子（垃圾郵件 99% 精確率的例子，正文最後未寫出這個數字）｜同上｜2026-10-03｜同上
每筆資料只能屬於三份中的一份｜https://developers.google.com/machine-learning/glossary（test set 條目）｜2026-10-03｜curl，HTML 轉文字
underfitting 常見原因：特徵選錯、訓練輪數太少或學習率太低、正則化率太高、隱藏層太少｜https://developers.google.com/machine-learning/glossary（underfitting 條目）｜2026-10-03｜同上（正文表格「可以先試」欄依此）

## Goodfellow、Bengio、Courville《Deep Learning》

5.2：低度擬合＝訓練誤差不夠低；過度擬合＝訓練誤差與測試誤差差距太大；容量＝能配合多種函數的能力，高容量可能記住對測試集沒用的訓練集性質｜https://www.deeplearningbook.org/contents/ml.html｜2026-10-03｜官網 pdf2htmlEX 頁，解析文字層（連字 ﬁ 還原）
5.3：測試集不能以任何方式參與模型選擇（含超參數）；驗證集從訓練資料切出，約 80% 訓練、20% 驗證；驗證誤差會低估泛化誤差，但通常比訓練誤差低估得少｜同上｜2026-10-03｜同上
5.3：同一測試集多年被反覆用來比較演算法、打破紀錄，評估會偏樂觀，基準會過時｜同上｜2026-10-03｜同上
5.2.2：沒有最好的正則化形式（no free lunch），要依任務選擇｜同上｜2026-10-03｜同上（正文最後版本未保留這句）
7.1.1：L2 參數範數懲罰常稱權重衰減，把權重拉向原點｜https://www.deeplearningbook.org/contents/regularization.html｜2026-10-03｜同上
7.4：讓模型泛化更好的最佳辦法是用更多資料；資料擴增如影像平移幾個像素，不能套用會改變正確類別的變換｜同上｜2026-10-03｜同上
7.8：提早停止在驗證誤差最低時保存參數、訓練結束時回傳那組參數｜同上｜2026-10-03｜同上

## Google 速成課程：正則化與提早停止

minimize(loss + complexity)；L2 正則化＝權重平方和，把權重推向 0；正則化率越高越不易過度擬合｜https://developers.google.com/machine-learning/crash-course/overfitting/regularization｜2026-10-03｜curl，HTML 轉文字
提早停止＝模型完全收斂前結束訓練（驗證損失開始上升時）；「quick, but rarely optimal」｜同上｜2026-10-03｜同上
簡單模型在新資料上常比複雜模型好；新專案先從一兩個特徵開始｜https://developers.google.com/machine-learning/crash-course/overfitting/model-complexity｜2026-10-03｜curl，HTML 轉文字

## Dropout

訓練時隨機拿掉單元（連同連線），避免單元過度共同適應；測試時用不拿掉的單一網路、權重乘上保留機率 p；目的是處理參數眾多的深度網路的過度擬合；在視覺、語音辨識、文件分類、計算生物學的監督式任務上改善表現｜https://jmlr.org/papers/v15/srivastava14a.html｜2026-10-03｜摘要頁 curl；全文 https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf，pdftotext
dropout 讓神經元不能只依賴特定其他神經元｜https://developers.google.com/machine-learning/glossary（co-adaptation、dropout regularization 條目）｜2026-10-03｜curl
dropout 最早見於 Hinton 等人 2012 年 7 月的預印本（摘要：訓練時隨機省略一半特徵偵測器以大幅減少過度擬合，並稱之為 random dropout）；JMLR 2014 是後來的完整期刊版，正文改寫為「最早見於 2012 年預印本，2014 年期刊論文再完整說明」（verify-1）｜https://arxiv.org/abs/1207.0580｜2026-10-03｜摘要頁 curl 200

## Zhang 等人 2017（ICLR 2017）

隨機標籤：CIFAR10 上 Inception、MLP 3x512 訓練準確率 100.0%，AlexNet 99.82%、MLP 1x512 99.34%（表 1），正文寫「降到 0 或接近 0」；ImageNet 上 Inception V3 未調超參數，隨機標籤 top-1 訓練準確率 95.20%（沒到 100%，表 2 末三列與第 2 節），測試 top-1 約 0.1%，等同亂猜；隨機像素與高斯雜訊的實驗在 CIFAR10（圖 1）。摘要與引言籠統寫「CIFAR10 和 ImageNet 上訓練誤差 0」，正文依論文自己的表改寫（verify-1）｜https://arxiv.org/abs/1611.03530｜2026-10-03｜摘要頁 curl；全文 https://arxiv.org/pdf/1611.03530（v2），pdftotext
表 1：Inception（1,649,402 參數）CIFAR10，random crop 否、weight decay 否：train 100.0、test 85.75；fitting random labels：train 100.0、test 9.78｜同上｜2026-10-03｜同上
結論：有效容量足以記住整份資料；VC 維度、Rademacher 複雜度、一致穩定性無法解釋；顯式正則化可能改善泛化但非必要、單靠也不足以控制泛化誤差（論文定義為訓練與測試誤差的差）；還沒找到能說明這些大模型「簡單」的正式指標｜同上｜2026-10-03｜同上

## Nakkiran 等人 2019

雙下降：模型變大時測試表現先變差再變好；也會隨訓練輪數出現；部分設定中增加樣本反而變差｜https://arxiv.org/abs/1912.02292｜2026-10-03｜摘要頁 curl；全文 https://arxiv.org/pdf/1912.02292，pdftotext
設定：CIFAR-10、CIFAR-100、IWSLT'14 de-en，CNN、ResNet、Transformer，SGD、Adam；測試誤差高峰在插值門檻（訓練誤差接近 0）；有標籤雜訊時最明顯；臨界區間寬度如何決定作者尚未完全了解｜同上｜2026-10-03｜同上

## 資料汙染與基準測試

最嚴重的資料汙染＝LLM 用某基準的測試切分訓練，再用同一基準評測；造成成績高估（立場論文）｜https://arxiv.org/abs/2310.18018｜2026-10-03｜摘要頁 curl
GSM1k：人工照 GSM8k 風格與難度寫 1,205 題，發表時不公開；準確率最多下降 8%（論文寫法 "up to 8%"）；數個模型系列幾乎所有大小都有系統性過度擬合跡象；生成 GSM8k 例題的機率與落差正相關（Spearman r² = 0.36）；許多模型、尤其前沿模型幾乎沒有過度擬合跡象，所有模型大致都能泛化到新題｜https://arxiv.org/abs/2405.00332｜2026-10-03｜摘要頁 curl（v4，NeurIPS 2024 Datasets and Benchmarks camera ready）；全文 https://arxiv.org/pdf/2405.00332，pdftotext
GSM1k 第 5 節：過度擬合不完全來自資料汙染，可能來自收集與基準相似的資料、依基準分數挑選 checkpoint；少量汙染不一定造成過度擬合｜同上｜2026-10-03｜同上
Recht 等人：照原流程為 CIFAR-10、ImageNet 重建測試集，準確率下降 3%–15% 與 11%–14%；原測試集上的進步會轉成新測試集上更大的進步；下降不是 adaptivity 造成，而是無法泛化到稍難的圖片｜https://arxiv.org/abs/1902.10811｜2026-10-03｜摘要頁 curl

## 示例與圖

旅館評論分類器的錯誤率（第 1 輪 30%／31%、第 8 輪 8%／12%、第 20 輪 1%／20%）是編寫的教學數字，未實際訓練；diagram-1.svg 的曲線依這組數字加上中間插值繪製，圖上數字 1、8、20、30、31、12、1% 與 20% 都在正文清單裡；2026 是製圖年份。
hero.svg 是手繪向量插圖（資料點、彎折線、平順線、新點），沒有文字、沒有 logo。

## 刻意不寫

模型名稱、產品價格、排行榜分數都不寫；GSM1k 論文點名的模型系列不寫。「模型越大越容易過度擬合」只以 Nakkiran 等人的設定反駁為不能當通則，不推廣雙下降。
