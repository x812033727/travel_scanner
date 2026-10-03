# 查證與編輯紀錄：ai-term-vision-language-model

格式：主張｜來源網址｜查證日｜讀取方式

## 名稱與定義（兩種用法都列）

窄義：image-text-to-text 模型「also known as vision language models (VLMs)」，是能接收圖片輸入的語言模型｜https://huggingface.co/docs/transformers/tasks/image_text_to_text｜2026-10-03｜curl -sSL 200，HTML 轉純文字
Flamingo 自稱「a family of Visual Language Models (VLM)」，輸入圖文交錯、輸出自由文字｜https://arxiv.org/abs/2204.14198｜2026-10-03｜arXiv abs 頁 200＋PDF 全文（pdftotext）
LLaVA 自稱 large multimodal model（LMM）｜https://arxiv.org/abs/2304.08485｜2026-10-03｜arXiv abs 頁＋PDF 全文
POPE 用 large vision-language models（LVLM）｜https://arxiv.org/abs/2305.10355｜2026-10-03｜arXiv abs 頁＋PDF 全文
廣義：綜述把影像編碼器＋文字編碼器、以嵌入比對做零樣本預測的模型（CLIP 類）稱為 VLM｜https://arxiv.org/abs/2304.00685｜2026-10-03｜arXiv abs 頁＋PDF 第 3 節
台灣譯名：多模態模型（定義含「輸入圖片與說明、輸出是否相符的分數」例子）、編碼器、嵌入、零樣本、少量樣本、指令調整／指令微調、定界框｜https://developers.google.com/machine-learning/glossary?hl=zh-TW｜2026-10-03｜curl 200，HTML 轉純文字搜尋關鍵詞
gate 的台灣譯名：Google 繁中詞彙表把 LSTM 的 forget gate 譯為「忘記閘」，因此 Flamingo 的 gated cross-attention 寫「閘控交叉注意力層」，不用「門控」｜https://developers.google.com/machine-learning/glossary?hl=zh-TW｜2026-10-03｜查核者 curl 200，HTML 轉純文字搜尋「閘」
多模態模型的定義是輸入、輸出或兩者包含「多個」模態（模態例舉數字、文字、圖片、影片、音訊），所以正文寫「兩種以上資料形式」｜https://developers.google.com/machine-learning/glossary?hl=zh-TW｜2026-10-03｜查核者 curl 200
國家教育研究院樂詞網：用 curl 查 vision-language model、vision encoder、contrastive learning、projection layer，回傳頁面只有分類清單、沒有詞條結果（查詢結果由前端載入），因此譯名以 Google 繁中詞彙表為準｜https://terms.naer.edu.tw/｜2026-10-03｜curl 200，未取得詞條

## 三段結構

ViT：把圖片切成固定大小的 patch，逐塊線性嵌入、加位置嵌入，送進標準 Transformer；patch 的處理方式和 NLP 的 token 相同｜https://arxiv.org/abs/2010.11929｜2026-10-03｜arXiv abs 頁＋PDF 第 1、3 節
大多數開源多模態語言模型直接用現成的 CLIP 視覺編碼器（支持「它的影像編碼器後來成了許多視覺語言模型的第一段」）｜https://arxiv.org/abs/2401.06209｜2026-10-03｜PDF 第 1、2 節
「語言模型可能依常見說法補上合理答案」：Flamingo 作者懷疑語言模型先驗與偶發幻覺有關，例子是只看文字合理、對照圖片卻錯的答案（Fig. 13、附錄 D.1）｜https://arxiv.org/abs/2204.14198｜2026-10-03｜PDF 第 5 節與附錄 D.1

## 里程碑（只寫論文自己的貢獻）

CLIP：網路收集 4 億組（400 million）圖文配對（WIT）；同時訓練影像與文字編碼器，預測一批 N 組裡 N×N 種配法中哪些真正成對（對比式目標），不預測說明的確切文字｜https://arxiv.org/abs/2103.00020｜2026-10-03｜abs 摘要＋PDF 第 2.2–2.3 節
CLIP：以類別名稱的文字做零樣本轉移；只能在給定概念中挑選，不像影像說明能產生新輸出；計算圖中物體數量等抽象工作表現弱（第 3.1 節 CLEVRCounts、第 6 節 Limitations）｜https://arxiv.org/abs/2103.00020｜2026-10-03｜PDF
Flamingo 與 LLaVA 的接法不同：Flamingo 的交叉注意力層以視覺特徵當 key／value、語言輸入當 query，影像不進語言模型的序列（Fig. 4、第 2.3 節）；LLaVA 以 W 把影像特徵轉成與詞嵌入同維度的影像 token Hv，和指令一起送進語言模型（第 4.1 節式 (1)）。正文第 4 段據此改寫，不再說「不同的只是上下文裡多了影像 token」｜https://arxiv.org/abs/2204.14198 ； https://arxiv.org/abs/2304.08485｜2026-10-03｜查核者 PDF pdftotext
Flamingo：預訓練的視覺編碼器與語言模型都凍結；Perceiver Resampler 把數量不定的影像特徵轉成固定 64 個視覺輸出；在凍結的語言模型層之間插入從頭訓練的 GATED XATTN-DENSE 層；tanh 門控的 α 初始為 0，初始化時輸出等於原語言模型｜https://arxiv.org/abs/2204.14198｜2026-10-03｜PDF 第 2.1–2.2 節
Flamingo：可接收任意圖文交錯序列，靠在提示中放入（圖片, 文字）示範做少量樣本的上下文學習｜https://arxiv.org/abs/2204.14198｜2026-10-03｜PDF 第 2.3–2.5 節
LLaVA：CLIP ViT-L/14 視覺編碼器＋可訓練投影矩陣 W（一層線性層）接到語言模型詞嵌入空間｜https://arxiv.org/abs/2304.08485｜2026-10-03｜PDF 第 4.1 節
LLaVA：用只吃文字的 GPT-4／ChatGPT，輸入 COCO 圖片的說明文字與定界框（symbolic representations），生成 158K（15.8 萬）筆指令資料：對話 58K、細節描述 23K、複雜推理 77K｜https://arxiv.org/abs/2304.08485｜2026-10-03｜PDF 第 3 節（正文不寫模型名，只寫「只能讀文字的大型語言模型」）
LLaVA：兩階段訓練：Stage 1 凍結編碼器與語言模型、只訓練 W；Stage 2 視覺編碼器保持凍結，更新 W 與語言模型｜https://arxiv.org/abs/2304.08485｜2026-10-03｜PDF 第 4.2 節

## 常見錯誤

Tong 等（MMVP）：CLIP-blind pairs＝CLIP 嵌入餘弦相似度 > 0.95、DINOv2（不靠語言訓練的自監督視覺模型）< 0.6 的圖片對；設計 150 對、300 題；一對圖的兩題都答對才算該對答對，所以隨機猜測為 25%（第 2.3 節、Fig. 4）；九類視覺型態含方向、數量、位置關係；人類平均答對 95.7%；除兩個模型外都低於隨機猜測（25%）；CLIP 吃力的型態與多模態語言模型的錯誤明顯相關｜https://arxiv.org/abs/2401.06209｜2026-10-03｜PDF 第 2–3 節
Kamath 等：What'sUp 自拍 820 張家用物品照片、205 組每組 4 張：Subset A 408 張是物件在桌子、椅子或扶手椅的上、下、左、右，Subset B 412 張是兩物件的前、後、左、右；杯子在桌子上下左右只是其中一組例子（第 1、2.1 節）；給正確說明與 1 或 3 個只差介系詞的干擾說明；18 個圖文模型（對比式與生成式都有）全部遠落後人類估計值（97.3%–100%），許多只比隨機高幾個百分點；LAION-2B 說明中 under、left of 等空間介系詞約 0.2%；「左」以觀看者或圖中主體為準有歧義｜https://arxiv.org/abs/2310.19785｜2026-10-03｜abs＋PDF 第 1–3 節
POPE：CHAIR（說明中提到但圖中沒有的物體比例）會受指令影響，兩個語意相近指令可使數值翻倍｜https://arxiv.org/abs/2305.10355｜2026-10-03｜PDF 第 3 節
CHAIR 原始論文：影像說明的物件幻覺指標｜https://arxiv.org/abs/1809.02156｜2026-10-03｜arXiv abs 頁
POPE：是非題「Is there a <object> in the image?」；不存在物體以 random、popular（資料集最常見）、adversarial（最常與圖中物體共同出現）三種方式抽樣；有無比例 1:1；MSCOCO 驗證集隨機 500 張、標註超過 3 個物體，每張 6 題；受測五個 LVLM 中有三個（LLaVA、MultiModal-GPT、mPLUG-Owl）回答 Yes 的比例接近 99%（第 5.2 節原文 near 99%；表 3 隨機設定下 LLaVA 95.37%、mPLUG-Owl 96.23%）；表現由 random、popular 到 adversarial 依序下降；被幻覺的物體多是視覺指令資料中常出現或常共同出現的物體｜https://arxiv.org/abs/2305.10355｜2026-10-03｜PDF 第 4–5 節與表 3
LLaVA：冰箱只有優格與草莓，模型卻回答有草莓口味優格（作者稱它有時把圖片當成 bag of patches）；Hallucination 段落點名醫療等關鍵應用的風險｜https://arxiv.org/abs/2304.08485｜2026-10-03｜PDF 實驗章節的 Limitations 段落與附錄的 Hallucination 段落

## 編輯說明

- 示例（小吃店收據、地圖方位）是原創教學情境，正文標明「示例，未實測任何產品，內容皆為虛構」，沒有寫成觀察結果；收據中的「8」「6」只是讀錯數字的假設。查核時把「常見失敗有三種」改為「可能的失敗有三種」，避免把想像情境寫成觀察到的頻率。
- 正文不寫模型產品名、價格、排名；論文裡受測模型（GPT-4V 等）與 LLaVA 的語言模型名稱都不寫。
- 標題草稿的「看懂圖片」改為「讀圖片」，避免暗示理解程度。
- 圖上數字 2021、2022、2023、4、64、15.8、2026 都在正文段落出現；2026 為製圖年份與「資料截至 2026 年 10 月」。
- SVG 為手繪向量圖，不是 AI 產圖。
- 正文字數（app.guides.pack_ingest._body_length）：撰稿交件 2587；查核修改後實算 2668。

## 查核紀錄（verify-1，2026-10-03）

- 查核者今天重新 curl -sSL 打開全部 11 個來源（全 200、標題相符），arXiv 九篇另抓 PDF 以 pdftotext 逐條對照；User-Agent 用 Mokaair-editorial/1.0。
- 沒有換掉任何來源；修改見 verify-1.md：Flamingo 接法的過度概括、多模態「一種以上」改「兩種以上」、MMVP 的 25% 補上成對計分、What'sUp 的照片設定、POPE 補「受測五個模型」、門控改閘控、示例的「常見」改「可能」。
