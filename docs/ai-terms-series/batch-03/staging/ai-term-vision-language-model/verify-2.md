# 查核紀錄 verify-2：ai-term-vision-language-model

查核日 2026-10-03。第二輪查核者，不是撰稿者，也不是第一輪查核者。11 個 `sources` 今天以 `curl -sSL`（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新打開，全部 200、標題與 `sources` 相符；九篇 arXiv 另抓 PDF 以 pdftotext 逐條對照原文。新增一筆來源：國家教育研究院樂詞網（查詢頁 200，詞條在伺服器端產生；網址要帶 `query_op=`，少了它只回預設瀏覽清單，第一輪因此以為由前端載入）。dry-run 通過（只剩協調者處理的 `no_summary` 警告），`_body_length` 由 2668 變 2686。

## 修改

1. 第 18 段「有三個答「有」的比例接近 99%」→「有三個答「有」的比例在三種挑法下都超過 95%」｜事實：表 3 這三個模型在 random、popular、adversarial 的 Yes 比例是 95.37%–100%，隨機設定下 LLaVA 95.37%、mPLUG-Owl 96.23%，稱不上接近 99%；第 5.2 節的 near 99% 是作者的概括，正文改用表 3 都成立的下限｜https://arxiv.org/abs/2305.10355 （表 3、第 5.2 節）
2. 第 16 段「計分時一對圖的兩題都答對才算對，亂猜約得 25%；人類平均答對 95.7%，多數受測模型卻低於 25%」→「論文的使用者測試裡，人平均答對 95.7% 的題目；模型的計分是一對圖的兩題都答對才算對，這樣亂猜約得 25%，多數受測模型卻低於 25%」｜事實：論文只說四位志願者 answer an average of 95.7% of the questions，沒寫人的分數是否也成對計；原句先講成對計分再接 95.7%，等於說兩者同一算法。成對計分改成只寫在模型那句（Fig. 2、Fig. 3 圖說都寫明是模型的計分）。同段「判斷明顯不同」改「分得出差別」是措辭｜https://arxiv.org/abs/2401.06209 （第 2.3 節、Fig. 2–4、附錄 B.4）
3. 第 10 段「主要貢獻在資料」→「論文列的第一項貢獻是資料」｜事實：論文導論列四項貢獻（多模態指令資料、大型多模態模型、LLaVA-Bench、開源），沒有說哪一項是主要的；改成可在原文查到的說法｜https://arxiv.org/abs/2304.08485 （第 1 節）
4. 第 3 段「連接層把影像特徵換成語言模型讀得懂的形式；語言模型再把這些影像 token 和你的問題一起讀」→「連接層把影像特徵換成語言模型讀得懂的影像 token；語言模型再參照這些 token 讀你的問題」；`diagram-1.svg` 語言模型格「影像 token＋問題一起讀」→「參照影像 token 讀問題」，`<desc>` 同步｜事實：「一起讀」只符合 LLaVA 把影像 token 放進語言模型序列的接法；Flamingo 的影像不進序列，由交叉注意力層以視覺 token 當 key／value 去讀。「參照」兩種接法都成立，第 4 段再說明差別。重新渲染 1600×900，新文字沒有超框｜https://arxiv.org/abs/2204.14198 （第 2.3 節、Fig. 4）；https://arxiv.org/abs/2304.08485 （第 4.1 節式 (1)）
5. 小標「最常見的三種錯：數量、位置、看見不存在的東西」→「三種常見的錯：數量、位置、看見不存在的東西」｜事實：MMVP、What'sUp、POPE 各量一種錯，沒有來源把這三種排成「最常見」；指派的 angle 也只寫「常見的錯」｜（無來源支持最高級，刪去）
6. 第 0 段「中文照英文字面寫成「視覺語言模型」」→「中文採國家教育研究院樂詞網收錄的譯名「視覺語言模型」」，`sources` 新增樂詞網｜台灣用語（不算事實修改）：樂詞網 vision-language model (VLM) 譯「視覺語言模型」（視覺藝術名詞；vision language model (VLM) 另見土木工程名詞-測量及圖學）；同站 gated／gating 譯「閘控」（電子計算機名詞、資訊與通訊術語大辭典），「門控」只見於醫學名詞-放射醫學，第一輪改的「閘控」因此有了依據｜https://terms.naer.edu.tw/search/?match_type=phrase&query_op=&query_field=title&query_term=vision-language+model ；https://terms.naer.edu.tw/search/?match_type=phrase&query_op=&query_field=title&query_term=gated
7. 第 18 段設定精簡：「舊的 CHAIR 指標會隨提示詞變動，兩句相近的指令量出的數值甚至翻倍；他們改問是非題」→「舊指標 CHAIR 從模型寫的圖說裡挑錯，結果會隨提示詞大幅變動，於是改問是非題」；「設定是從 MSCOCO 驗證集取 500 張標註超過 3 個物體的圖，每張問 6 題，有無各半」→「他們從 MSCOCO 取 500 張照片，每張問 6 題、有無各半」；「而常和圖中物體同時出現的東西最容易被說成有」→「整體來看，最常一起出現的那一組最容易被說成有」｜精簡（不算事實修改）：給一般讀者刪去驗證集與標註數門檻（細節留在 notes.md）；補一句 CHAIR 在量什麼；「整體來看」是因為表 3 中 mPLUG-Owl 的 popular 與 adversarial 幾乎相同，第 5.2 節的 consistently decreases 是作者的概括｜https://arxiv.org/abs/2305.10355 （第 3 節、表 1、第 5.2 節、表 3）
8. 第 17 段精簡：「每組只改變擺放位置，例如同一個杯子在桌子上、下、左、右」→「例如同一個杯子放在桌子上、下、左、右」；「只差一個介系詞的說明」→「只差一個介系詞的英文說明」；「在一個大型圖文資料集的說明裡」→「作者也發現，大型圖文資料集的說明裡」；「「左邊」以誰為準」保留｜精簡（不算事實修改）：What'sUp 的說明是英文句子（例 A mug under a table），讀者才知道「介系詞」指什麼；0.2% 補上是作者對 LAION-2B 的分析｜https://arxiv.org/abs/2310.19785 （第 1、2.1 節、表 4）
9. 第 9 段「閘控係數初始為 0，訓練之初輸出和原本的語言模型相同」→「閘控係數從 0 開始，所以訓練之初輸出和原本的語言模型相同」｜措辭（不算事實修改）：補出因果，原文 To ensure that at initialization, the conditioned model yields the same results as the original language model, we use a tanh-gating mechanism｜https://arxiv.org/abs/2204.14198 （第 2.2 節）

## 查過、沒問題的主要主張

第一輪 7 處修改逐條重查：

- Flamingo 的交叉注意力層以視覺特徵為 key／value、語言輸入為 query（第 2.3 節）；LLaVA 以 W 把 Zv 轉成與詞嵌入同維度的 Hv，和指令一起送進語言模型（式 (1)）。第 4 段成立。
- Google 繁中詞彙表「多模態模型：輸入、輸出或兩者包含多個「模態」的模型」，例子是圖片加文字說明兩種模態輸入、輸出是否相符的分數；「兩種以上」成立。
- MMVP 的 25%：Fig. 2、Fig. 3 圖說寫明模型要一對圖兩題都對才得分；Fig. 4 的 Random Guess 25.0。成立（本輪另修人的分數，見修改 2）。
- What'sUp：820 張、205 組每組 4 張，Subset A 408 張、Subset B 412 張；一組是 mug on, under, left of, right of a table。成立。
- POPE 第 3 節 We select five recently released LVLMs。成立。
- 閘控：樂詞網 gated／gating 譯「閘控」，Flamingo 的 α 初始為 0（偽碼 init at 0）。成立。
- 收據示例「可能的失敗」：示例未實測，維持。

從其餘 34 條事實主張以亂數（seed 20261003）抽 12 條重查，全部成立：

- Flamingo 自稱 a family of Visual Language Models (VLM)；LLaVA 自稱 large multimodal model (LMM)。
- Zhang 等綜述：VLM 以大量網路圖文對預訓練，靠嵌入比對做零樣本預測，CLIP 為代表。
- Hugging Face：Image-text-to-text models, also known as vision language models (VLMs), are language models that take an image input。
- CLIP：jointly trains an image encoder and a text encoder；predict which of the N × N possible (image, text) pairings actually occurred，不預測 exact words。
- MMVP：the majority of open-source MLLMs use the off-the-shelf CLIP vision encoders。
- Flamingo：可接收任意圖文交錯序列，以提示中的示範做少量樣本的上下文學習。
- LLaVA：a simple linear layer to connect image features into the word embedding space。
- Google 詞彙表的多模態模型例子（圖片＋說明 → 相符分數）。
- MMVP：150 pairs with 300 questions；九類含 Orientation and Direction、Quantity and Count、Positional and Relational Context。
- POPE：兩個語意相近的指令可讓 CHAIR 數值翻倍（doubled values）。
- POPE：表現由 random、popular 到 adversarial 下降，常出現或常共同出現的物體容易被幻覺（第 5.2 節；表 3 大致如此，mPLUG-Owl 的 popular 與 adversarial 幾乎相同，正文加「整體來看」）。

另外順讀時核對：Flamingo 附錄 D.1 與 Fig. 13 寫 answers that seem likely given the text only, but are wrong given the image；LLaVA 冰箱草莓優格例與 Hallucination 段 critical applications (e.g., medical)；What'sUp 18 個模型、many performing just a few points above random chance、LAION-2B 空間介系詞 less than 0.2%（第 3 節 only 0.2%，表 4 less than 0.22%，正文「約 0.2%」）；CLIP 第 6 節 counting the number of objects；POPE 500 張、每張 6 題、1:1。

系列規矩：topics 含 `ai-terms`；「本文」「這篇」全篇 0 次；正文沒有查證過程；推論／推理都沒出現；沒有型號、價格、排名或「已達人類水準」；示例標明未實測；指派的 5 個站內連結都在、沒有額外連結；6 個 H2、恰好一個表格、1 個 callout。token、上下文、提示詞照系列用語。圖上數字 2021、2022、2023、4、64、15.8、2026 都在正文（`missing_diagram_numbers` 為空）。

## 我懷疑但沒改的事

- 「交叉注意力」在樂詞網與 Google 繁中詞彙表都沒有完整詞條（cross attention、cross-attention 查無結果）；由詞彙表的「交叉熵」與「自注意力」兩個譯法組成，保留。
- 樂詞網來源是查詢網址，不是固定詞條頁（詳細頁網址不帶 `seq` 會導回首頁）；網址少了 `query_op=` 就只回預設清單，日後網站改版可能失效。
- 字數 2686 仍高於第三批目標 2,200–2,600，在 3,000 上限內；本輪刪掉 POPE 與 What'sUp 的部分設定，但為了把人的分數與 CHAIR 交代清楚又補了字，再刪就得拿掉指派要的設定或結論。

facts_changed: 5
