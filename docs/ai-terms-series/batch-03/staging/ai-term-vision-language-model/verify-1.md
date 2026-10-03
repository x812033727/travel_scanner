# 查核紀錄 verify-1：ai-term-vision-language-model

查核日 2026-10-03。查核者不是撰稿者。11 個 `sources` 今天以 `curl -sSL`（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新打開，全部 200、標題與 `sources` 相符；九篇 arXiv 另抓 PDF 以 pdftotext 逐條對照原文。沒有換掉或刪除任何來源。dry-run 通過（只剩協調者處理的 `no_summary` 警告），`_body_length` 由 2587 變 2668。

## 修改

1. 第 4 段「；不同的只是上下文裡多了來自圖片的 token。」→「；LLaVA 這類接法把影像 token 直接放進上下文，Flamingo 則在層間另加交叉注意力去讀影像特徵。」｜事實：Flamingo 的影像不進語言模型的序列，而是作為新插入的交叉注意力層的 key／value，原句的「只是」和第 9 段自相矛盾；LLaVA 才是把投影後的影像 token 和指令一起送進語言模型｜https://arxiv.org/abs/2204.14198 （Fig. 4、第 2.3 節）；https://arxiv.org/abs/2304.08485 （第 4.1 節式 (1)）
2. 第 12 段「處理一種以上資料形式的系統都算」→「處理兩種以上資料形式的系統都算」｜事實：依台灣「以上」連本數計算的慣例，「一種以上」包含只處理一種形式的系統；詞彙表定義是輸入、輸出或兩者包含「多個」模態，表格也寫「兩種以上」｜https://developers.google.com/machine-learning/glossary?hl=zh-TW
3. 第 16 段「人類平均答對 95.7%，多數受測模型低於隨機猜測的 25%」→「計分時一對圖的兩題都答對才算對，亂猜約得 25%；人類平均答對 95.7%，多數受測模型卻低於 25%」｜事實：25% 來自 MMVP 的成對計分（每題二選一，兩題都對才算該對答對）；原句沒寫這個設定，讀者會以為二選一題的隨機水準是 25%｜https://arxiv.org/abs/2401.06209 （第 2.3 節、Fig. 4）
4. 第 17 段「Kamath 等人 2023 年拍下同一個杯子在桌子上、下、左、右的照片」→「Kamath 等人 2023 年自己拍了 820 張家用物品照片，每組只改變擺放位置，例如同一個杯子在桌子上、下、左、右」｜事實：What'sUp 是 820 張（205 組、每組 4 張），物件與參照物各組不同，還有兩物件前後左右的 Subset B；杯子在桌子上下左右只是論文舉的一組例子｜https://arxiv.org/abs/2310.19785 （第 1、2.1 節）
5. 第 18 段「結果有三個模型答「有」的比例接近 99%」→「結果受測的五個模型裡，有三個答「有」的比例接近 99%」｜設定補充（不算事實修改）：POPE 第 3 節選了五個 LVLM，第 5.2 節說其中三個 near 99%｜https://arxiv.org/abs/2305.10355
6. 第 9 段「插入新的門控交叉注意力層，門控初始值為 0」→「插入新的閘控交叉注意力層，閘控係數初始為 0」；`diagram-1.svg` 圖上文字與 `<desc>` 的「門控」同步改「閘控」｜台灣用語（不算事實修改）：Google 繁中詞彙表把 gate 譯為「閘」（忘記閘），「門控」是對岸常見寫法；論文中初始為 0 的是 tanh 閘控的係數 α，改「係數」較準｜https://developers.google.com/machine-learning/glossary?hl=zh-TW ；https://arxiv.org/abs/2204.14198 （第 2.2 節）
7. 第 25 段「常見失敗有三種」→「可能的失敗有三種」｜系列規矩（不算事實修改）：收據是未實測的示例，「常見」等於宣稱觀察到的頻率｜（示例，無來源）

## 查過、沒問題的主要主張

- 名稱用法：Flamingo 自稱 a family of Visual Language Models (VLM)；LLaVA 自稱 large multimodal model (LMM)；POPE 用 LVLM；Zhang 等綜述把以圖文對比預訓練、靠嵌入比對做零樣本預測的 CLIP 類模型稱為 VLM；Hugging Face 文件寫 image-text-to-text models, also known as vision language models (VLMs), are language models that take an image input。第一段兩種用法都寫了，並說明採窄義與譯名理由。
- ViT 把圖片切成固定大小的 patch，處理方式和 NLP 的 token 相同（第 1 節、Fig. 1；ICLR 2021）。
- CLIP：4 億組網路圖文配對；同時訓練影像與文字編碼器，預測一批 N×N 種配法中哪些成對，不預測說明的確切文字；以類別名稱做零樣本分類；只能從給定概念中挑選、不能像影像說明那樣產生新輸出；數物體數量是第 6 節自列的弱點。
- 多數開源多模態語言模型直接用預訓練的 CLIP 視覺編碼器（MMVP 第 1、2 節）。
- Flamingo：視覺編碼器與語言模型預訓練後凍結；Perceiver Resampler 把數量不定的影像特徵轉成固定 64 個視覺輸出；tanh 閘控係數初始為 0，初始化時輸出等於原語言模型；可讀圖文交錯序列，以（圖片, 文字）示範做少量樣本的上下文學習；第 5 節與附錄 D.1、Fig. 13 記錄只看文字合理、對照圖片卻錯的幻覺答案。NeurIPS 2022。
- LLaVA：一層可訓練線性投影；以只吃文字的 GPT-4／ChatGPT 讀 COCO 的說明與定界框，生成 158K（15.8 萬）筆指令資料；兩階段（先只訓練 W，再更新 W 與語言模型，視覺編碼器始終凍結）；冰箱只有優格和草莓卻對「有沒有草莓口味優格」答 yes；Hallucination 段點名 critical applications (e.g., medical)。NeurIPS 2023。
- POPE：CHAIR 在兩個語意相近的指令下可差到翻倍；是非題輪詢；不存在物體以 random、popular、adversarial 三種方式取樣；有無 1:1；MSCOCO 驗證集隨機 500 張、標註超過 3 個物體、每張 6 題；表現由 random 到 adversarial 依序下降，常出現或常共同出現的物體容易被幻覺。EMNLP 2023。
- CHAIR 是 Rohrbach 等提出的影像說明物件幻覺指標（EMNLP 2018）。
- MMVP：CLIP 嵌入餘弦相似度 > 0.95、DINOv2 < 0.6 的 CLIP-blind 圖片對；150 對、300 題；九類視覺型態含方向、數量、位置；人類 95.7%；除 GPT-4V 與 Gemini 外都低於 25%（Fig. 4 共 8 個模型、6 個低於 25%，「多數」成立）；LLaVA-1.5 與 InstructBLIP 各型態表現和 CLIP 的皮爾森相關係數 > 0.7。
- What'sUp：18 個圖文模型（對比式與生成式都有）全部遠落後人類，不少只比隨機高幾個百分點；LAION-2B 說明中 under、left of 等空間介系詞只占 0.2%；「左」可從觀看者或圖中主體的角度理解。EMNLP 2023。
- Google 繁中詞彙表多模態模型的例子：輸入圖片與文字說明、輸出相符分數；模態例舉數字、文字、圖片、影片、音訊。
- 「上面的數字出自 2021 到 2024 年的論文」：CLIP 2021、Flamingo 2022、LLaVA／POPE／What'sUp 2023、MMVP 2024，正文的數字都出自這幾篇。
- 系列規矩：topics 含 `ai-terms`；「本文」「這篇」全篇 0 次；正文沒有查證過程，日期寫「資料截至 2026 年 10 月」；沒有型號、價格、排名或「已達人類水準」；推論／推理都沒出現；收據與地圖示例標明未實測、內容虛構；指派的 5 個站內連結都在、沒有額外連結；5 個 H2、恰好一個 3 欄表格、1 個 callout。
- 圖上數字 2021、2022、2023、4（億）、64、15.8（萬）、2026 都在正文出現；重新渲染 1600×900，沒有壓線、超框或疊字。hero 沒有文字、沒有 logo。

## 我懷疑但沒改的事

- MMVP 正文說人類答對 95.7% of the questions，模型則以成對計分，論文沒寫清楚人類分數是否也成對計；正文照論文並列兩個數字。
- POPE「接近 99%」是論文第 5.2 節的概括；表 3 隨機設定下 LLaVA 95.37%、mPLUG-Owl 96.23%，popular／adversarial 才在 97%–100%。正文照論文的說法。
- 圖解「語言模型：影像 token＋問題一起讀」較貼近 LLaVA 的接法，對 Flamingo 是簡化；正文第 4 段已寫出差別，圖不改。
- 「LLaVA 主要貢獻在資料」是編輯取捨：論文列四項貢獻（資料、模型、LLaVA-Bench、開源），資料排第一、摘要也以資料為主軸，所以保留。
- 樂詞網查詢結果由前端載入，curl 取不到詞條；「視覺語言模型」「閘控」「交叉注意力」的台灣譯名只對過 Google 繁中詞彙表（只有「閘」，沒有這三個完整詞）。
- 字數 2668 超過第三批目標 2,200–2,600，仍在 3,000 上限內；為了不重寫，沒有刪句。

facts_changed: 4
