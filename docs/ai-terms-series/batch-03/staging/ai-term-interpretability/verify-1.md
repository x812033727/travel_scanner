# 查核紀錄 1：ai-term-interpretability

查核者不是撰稿者，查核日是 2026-10-03。所有網址今天都用 `curl -sSL` 和 User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新抓過，沒有參考作者的 notes 結論。
16 筆 `sources` 全部回 HTTP 200，標題、作者和年份都對得上；兩個 NIST DOI 會轉到 nvlpubs.nist.gov 的 PDF。
十篇 arXiv 論文另外抓了 `https://arxiv.org/pdf/<id>`（HTTP 200），用 pdftotext 轉成文字逐節核對：Doshi-Velez & Kim、Lipton、Rudin、LIME、SHAP、Jacovi & Goldberg、Adebayo、Slack、Jain & Wallace、Turpin。
兩份 NIST PDF 也逐節讀過。Distill「Zoom In」、Transformer Circuits「Scaling Monosemanticity」、Google 繁中詞彙表、華藝書目頁則讀 HTML 去標籤後的文字。沒有用 Wayback。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

1. 「Slack 等人（2020）做出只看種族的分類器⋯⋯在他們的三個資料集上，LIME 被騙過，SHAP 多數時候也沒把種族排第一」→「做出只看種族（德國信用資料改看性別）的分類器⋯⋯LIME 都被騙過，SHAP 在多數資料點上也沒把這個敏感特徵排第一」｜ 論文的 biased classifier f 在 COMPAS 和 Communities and Crime 只看種族，在 German credit 只看性別（圖 4 的敏感特徵也是 Gender）。原句把三個資料集都寫成種族。SHAP 的數字是「把重要度從敏感特徵移開」的資料點比例：單一無關特徵時 COMPAS 84%、CC 100%、German 85%，兩個特徵時 67%、71% ｜ https://arxiv.org/abs/1911.02508（Experimental Setup「Biased Classifier f」段、Effectiveness of Adversarial Classifiers 段、圖 2–4）
2. 「語言模型也一樣。注意力機制的權重，Jain 與 Wallace（2019）發現常和梯度式重要度不相關」→「處理文字的模型也一樣。注意力機制的權重，Jain 與 Wallace（2019）在文字分類、問答等任務的模型上發現，常和梯度式重要度不相關」｜ 論文研究的是帶注意力的 BiLSTM（另比較 CNN 和平均編碼器），任務是文字分類、問答和自然語言推論，不是語言模型。原句把它放在「語言模型」底下，論文設定寫錯了。Turpin 等人研究的確實是大型語言模型，新寫法兩篇都涵蓋。第二批的注意力機制專文（`batch-02/staging/ai-term-attention-mechanism`）也是這樣描述它的設定 ｜ https://arxiv.org/abs/1902.10186（摘要、第 2 節、第 3 節）
3. （系列規則，不計入事實修改）第一節最後「先問是誰的定義。」後面補上「以下採較寬的用法：和 Lipton 一樣，把事後解釋也算進可解釋性。」｜ VERIFY 第 3 點要求，定義有分歧時要說明採用誰的。原文列完 Doshi-Velez & Kim、Lipton、Rudin、NIST 之後，沒有說自己用哪一種。可是第二類「事後歸因」照 Rudin 的窄用法並不算 interpretable，所以一定要交代 ｜ https://arxiv.org/abs/1606.03490（第 3 節開頭與第 3.2 節 Post-hoc Interpretability）
4. （來源標題，不計入事實修改）四筆 `sources` 補全標題或場合：SHAP 加「NIPS 2017」；Jacovi、Goldberg 補副標題「How should we define and evaluate faithfulness?」；Jain、Wallace 加「NAACL 2019」；Turpin 等補副標題「Unfaithful Explanations in Chain-of-Thought Prompting」和「NeurIPS 2023」｜ 原標題被截短，或沒寫場合 ｜ 各篇 abs 頁的 Title 與 Comments 欄

改完後 `_body_length` 是 2,669（改前 2,598），在 1,800–3,000 之內，但比 brief 的目標上緣 2,600 多 69 字。結構沒動：5 個 H2、恰好 1 個表（3 欄）、1 個 callout、diagram 與 hero 各一張，指派的五個連結（含 `ai-terms-index`）都還在。
`diagram-1.svg` 和 `hero.svg` 沒改；diagram 用 `render_svg`（headless shell，1600×900）重新渲染檢查過，沒有超框或疊字。
dry-run：`pack_cli ingest --dry-run` 通過（exit 0），只有 `no_summary` 警告，改前改後一樣。
`notes.md` 和 `research.json` 已經同步：Slack 的敏感特徵、Jain & Wallace 的設定、定義採用、四筆標題，以及 `running_text_characters` 改成 2669。

## 查過、沒問題的主要主張

- **Doshi-Velez & Kim**（v1 2017-02-28）：定義原文是「the ability to explain or to present in understandable terms to a human」。第 2 節說需要可解釋性是因為問題的形式化不完整（incompleteness），舉的情境有 Safety（無法列出所有失敗情境）和 Ethics（公平太抽象，無法完整編進系統）。「there are no significant consequences」或「sufficiently well-studied and validated」的系統不需要解釋。第 3 節的三層評估是：真人真任務、真人簡化任務、不找人用代理任務（proxy tasks）。
- **Lipton**（v1 2016-06-10，ICML 2016 WHI 工作坊）：原文寫「no formal technical meaning」「not a monolithic concept」，動機「diverse and occasionally discordant」，第 2 節列了信任、因果、可遷移、資訊性、公平。第 3 節分成 transparency（simulatability 就是人能一步步算完模型）和 post-hoc。post-hoc 的摘要句列的是 natural language explanations、visualizations、explanations by example，和文中「文字、視覺化、舉例」一致。第 4.1 節說維度高或特徵經過大量工程時，線性模型會失去 simulatability 或 decomposability。
- **Rudin**（Nature Machine Intelligence, Vol 1, May 2019）：Introduction 區分「Explainable ML」（另做一個 posthoc 模型解釋黑盒）和 inherently interpretable models，後者「faithful to what the model actually computes」；interpretability 是 domain-specific。第 2 節 (i) 說，在有有意義特徵的結構化資料上，複雜模型和簡單模型常常沒有顯著差異。
- **NIST AI RMF 1.0**（AI 100-1，2023 年 1 月）第 3.5 節：explainability 是「a representation of the mechanisms underlying AI systems' operation」，回答 how；interpretability 是輸出在設計用途下的意義，回答 why。
- **Google 繁中機器學習詞彙表**有「可解釋性」條目（id `interpretability`），定義是「以人類可理解的用語，說明或呈現機器學習模型的推理過程」，詞彙表裡沒有 explainability 條目。**黃詩淳**（臺大法學論叢 52 卷 S 期，2023/11，頁 931–972）的摘要同時寫「AI的可解釋性（explainability）」和「可解釋性（interpretability）」，足以支持第一段說的譯名相撞。
- **LIME**：摘要寫「learning an interpretable model locally around the prediction」。
- **SHAP**（NIPS 2017）：Shapley 值來自 cooperative game theory。base value E[f(z)] 是「if we did not know any features」時的預測，SHAP 值說明怎麼從它走到 f(x)。Theorem 1 說在 additive feature attribution 這一類方法中，滿足 local accuracy、missingness、consistency 的解只有一個。原文也寫「exact computation of SHAP values is challenging」。
- **航班延誤示例**：0.20＋0.25＋0.12＋0.08−0.03＝0.62，正文、圖上文字、`<desc>` 三處一致。圖上長條以 280 px 代表 1.0，寬度 56／70／34／22／8／174 px 都和數字成比例。這段標了「示例」「未實測」，也沒有寫成觀察結果。
- **Zoom In**（Distill，2020-03-10）：原文說三個主張「deliberately speculative」。features「correspond to directions」，指某一層活化向量空間裡的方向；circuit 是「a computational subgraph」。InceptionV1 的 4e:55 同時回應 cat faces、fronts of cars、cat legs。
- **Scaling Monosemanticity**（Templeton 等，2024-05-21）：對象是「Anthropic's medium-sized production model」，文中沒有寫型號。SAE 訓練在中間層的殘差流上，殘差流是「the sum of the outputs of all previous layers」。三個 SAE 分別是 1,048,576、4,194,304、33,554,432 個特徵，重建「explained at least 65% of the variance」。特徵 multilingual、multimodal。金門大橋特徵在 forward pass 中 clamp 到「10× its maximum activation value」後，模型「starts to self-identify as the Golden Gate Bridge」。限制段原文是「orders of magnitude short」，倫敦行政區那個例子在 34M SAE 只找到約 60%。原文還寫「a difference ... between knowing about lies, being capable of lying, and actually lying」，「test set for safety」是「One hope」，觀察「very preliminary」。
- **Jacovi & Goldberg**（ACL 2020）：plausibility 是「how convincing the interpretation is to humans」，faithfulness 是「how accurately it reflects the true reasoning process」，原文說「possible to satisfy one of these properties without the other」，也說「Faithfulness evaluation should not involve human-judgement」。「推理過程」對應 reasoning，符合系列用法；全文沒有出現「推論」。
- **NISTIR 8312**（2021 年 9 月）：Meaningful 原則是「understandable to the intended consumer(s)」；「Explanation accuracy is a distinct concept from decision accuracy」。
- **Adebayo 等**（NeurIPS 2018）：model parameter randomization test 拿訓練好的模型和「a randomly initialized untrained network of the same architecture」比較。Guided BackProp 和 Guided GradCAM「invariant to higher layer parameters」；原文也說「visual inspection is a poor guide」。v3 修正了 Guided Backprop 的 bug：較低層權重隨機化後結果會變。文章只寫「較高層參數」，所以仍然正確。
- **Turpin 等**（NeurIPS 2023）：把選項重排成答案總是 (A) 等偏向線索，模型「systematically fail to mention」；被帶向錯誤答案時「frequently generate CoT explanations rationalizing those answers」。
- **系列規則**：topics 含 `ai-terms`；全篇（含 description）沒有「本文」「這篇」；正文沒有查證過程，日期寫「資料截至 2026 年 10 月」；沒有型號、價格、截止日期、排行榜分數。兩個假設案例（航班延誤、訂房網站）都標了「示例」和「未實測」。沒有「用了就不會」式保證；「說得通不等於忠實」那個 callout 寫的是「只能當待查線索」。用語是台灣用法（活化、自動編碼器、網路、資料、決策樹），沒有出現信息、默認、激活、數據、算法。只連了指派的五個 slug。沒有寫「某公司已經看懂模型」，Scaling Monosemanticity 那段明寫「不能讀成已經看懂模型」。

## 我懷疑但沒改的事

- 第一節說 NIST 的用法「正好和下文機制可解釋性的用法相反」。NIST 的「mechanisms underlying AI systems' operation」比較像系統層級的運作說明，不一定指網路內部的特徵與電路，所以兩者是用詞上的對照，概念上未必衝突。文中寫的是「用法」，沒有改。
- 修改後正文 2,669 字，超出 brief 的目標 2,200–2,600，但沒超過上限 3,000。我沒有刪作者的句子來湊字數。
- 黃詩淳那篇只讀了華藝的中文摘要，沒有讀全文，只拿來支持「中文兩個詞都譯成可解釋性」。
- Jacovi & Goldberg 的指引寫「Do not trust inherent interpretability claims」，和 Rudin「天生可讀模型的解釋就是忠實」立場相反。正文寫的是「Rudin 認為」，圖底部也要求三類都檢查忠實度，所以沒改；不過表格第一列「要小心的地方」只寫了「讀不完」。
- Doshi-Velez & Kim 的第三層原文是「proxy tasks」，文中寫「代理指標」；Zoom In 原文是「networks often contain polysemantic neurons」，文中寫「一個神經元常身兼數職」。兩處都是措辭上的小差距，不影響主張，沒有改。

facts_changed: 2
