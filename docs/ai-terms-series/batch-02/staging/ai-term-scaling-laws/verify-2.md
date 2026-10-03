# 查核紀錄 2：ai-term-scaling-laws（縮放定律）

第二輪查核者，不是撰稿者，也不是第一輪查核者。查證日 2026-10-03。12 個 arXiv abs 頁（11 筆 sources 加上被換掉的 2604.01411）都用
`curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"` 重抓，全部 HTTP 200，`citation_title` 與 sources 標題相符；
11 筆 sources 的 PDF 都從 `https://arxiv.org/pdf/<id>` 重抓，用 `pdftotext -layout` 讀全文。依據都來自論文原文，沒有拿 notes 或 verify-1 當依據。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

這一輪沒有事實錯誤要改。以下都是可讀性修改：補上一般讀者需要的脈絡，數字不變；新加的每句都回到原文查過。

- 「參數量加倍，損失約變成原來的 0.95 倍，少了約 5%。所以資源加倍的收益不會變大，下一次進步要花的絕對資源比上一次更多。」→「……少了約 5%；再加倍一次，也只再少約 5%，這次要多投入的資源卻是上一次的兩倍。」｜措辭：原句「收益不會變大」「絕對資源」太抽象，改成讀者可以自己驗算的說法（N→2N 多投入 N，2N→4N 多投入 2N；每次都乘 2^−0.076 ≈ 0.95）｜https://arxiv.org/abs/2001.08361（§1.2 式 1.1 與「doubling the number of parameters yields a loss that is smaller by a factor 2^−αN = 0.95」）
- 「Chinchilla 論文的公式還多一項不會再降的損失」→「下一節會談到的 Chinchilla 論文，公式還多一項不會再降的損失」｜措辭：Chinchilla 到下一節才介紹，這裡先出現，讀者會不知道是什麼｜https://arxiv.org/abs/2203.15556（§3.3）
- Pearce 與 Song 句「不算嵌入層」→「不算嵌入層（把 token 及其位置轉成向量的部分）」；Porian 句「沒計入最後一層的計算成本」→「沒計入最後一層（輸出層）的計算成本」｜措辭：兩個術語加白話註解。Pearce §2.1：Kaplan 排除「the embedding layers for the vocabulary and position indices」，所以註解寫 token「及其位置」；Porian 的 last layer 是「the head (last decoding layer)」（§3.1、§3.2）｜https://arxiv.org/abs/2406.12907 、 https://arxiv.org/abs/2406.19146
- 差異段末尾加一句「這兩部分在小模型裡占比較大，Kaplan 的實驗又以小模型為主，漏算就讓結論偏向把預算多花在放大模型。」｜可讀性：原段列完兩篇論文的因素就結束，沒告訴讀者「漏算」為什麼會變成「多放大模型」的結論，概念被論文細節蓋過。依據：Pearce §7「At larger values of N_T, the embedding parameter counts become negligible」、摘要「the primary cause of Kaplan's original overestimation」（N 的指數 0.73 對 0.50）；Porian §5.2「with scale, the contribution of the model head becomes negligible」、圖 1 計入最後一層後指數 0.835→0.706；Hoffmann §2：Kaplan 多數模型「significantly smaller—many being less than 100M」。這是補說明、沒有改既有事實，不計入 facts_changed｜https://arxiv.org/abs/2406.12907 、 https://arxiv.org/abs/2406.19146 、 https://arxiv.org/abs/2203.15556
- 「Besiroglu 等人用從論文圖表重建的資料，重做 Chinchilla 的第三種擬合，發現原報告的數值與前兩種方法不一致」→「Chinchilla 論文用三種方法估計最佳配置，Besiroglu 等人用從論文圖表重建的資料重做第三種，發現……」｜措辭：原文沒交代 Chinchilla 有三種方法，「第三種」「前兩種」對讀者沒有指涉。Hoffmann §3 開頭「We present three different approaches」；Besiroglu 摘要「Hoffmann et al. (2022) propose three methods」｜https://arxiv.org/abs/2203.15556 、 https://arxiv.org/abs/2404.10102
- 「發現覆蓋率隨取樣次數增加，跨越約四個數量級。但沒有自動驗證器時，覆蓋率不等於最終答對率」→「發現在橫跨約四個數量級的取樣次數內，覆蓋率都持續上升。程式題這類能自動驗證答案的題目，覆蓋率上升就直接轉成實際表現；沒有自動驗證器時，覆蓋率不等於最終答對率」｜措辭：原句「跨越約四個數量級」沒說是什麼跨越四個數量級；「自動驗證器」沒例子，讀者看不出覆蓋率什麼時候有用。Brown 摘要「In domains like coding and formal proofs, where answers can be automatically verified, these increases in coverage directly translate into improved performance」｜https://arxiv.org/abs/2407.21787

`_body_length`：2580 → 2705（站內連結文字 24 字，扣除後 2681）。結構不變：5 個 H2（verify-1 寫 6 個是筆誤，實數為 5，仍符合 ≥5）、1 個 3 欄表格、1 個 callout、1 張圖，指派的五個站內連結都在。

## 第一輪的 5 項事實修改，逐項對全文重查

1. **「Chinchilla 論文的解釋是……兩篇後續研究重做了比較，都發現學習率排程不是主因」**：成立。Hoffmann §2：「the authors use a fixed number of training tokens and learning rate schedule for all models」，也說 Kaplan 多數模型「significantly smaller」。Porian 摘要「Counter to a hypothesis implied in Hoffmann et al. [25], we find that careful learning rate decay is not essential」，§1「disprove Hoffman et al.'s hypothesis」，最後吻合 Chinchilla 的設定「uses a constant learning rate schedule」。Pearce §1 說最佳化方案的說法「incomplete」，§4 Experiment 2「affects coefficients only marginally (counter to Chinchilla's explanation)」，Result 2「optimization scheme has a smaller impact on scaling coefficients than switching from N_T to N_\E」。「不是主因」對兩篇都準確。
2. **「Pearce 與 Song 認為很大一部分差異來自 Kaplan 計參數時不算嵌入層，加上分析在小規模進行」**：成立。摘要與 §1 都是「much of this discrepancy」；§2.1 排除詞彙與位置兩種嵌入。摘要另說「explaining the primary cause」，「很大一部分」不誇大也不低估。重疊句「沒有算進嵌入層或最後一層」也成立：Porian §5.1 說 Pearce 與 Song「identify the last layer FLOP count as a cause」，§3.2 推測 Kaplan 因 head 與嵌入共用權重，連帶把 head 的 FLOPs 也扣掉；Pearce §6 也把 Porian 的第一項讀成「counting non-embedding rather than total compute」。
3. **Sardana 等人取代 2026 預印本**：成立。arXiv:2401.00448 abs 頁 HTTP 200，comments 欄寫「In the 41st International Conference on Machine Learning, 2024」，PDF 頁尾「Proceedings of the 41st International Conference on Machine Learning, Vienna, Austria. PMLR 235, 2024」；v1 2023-12-31、v2 2024-07-18、v3 2025-04-14。摘要「these formulas, including the popular Deepmind Chinchilla scaling laws, neglect to include the cost of inference」與「researchers expecting reasonably large inference demand (~1B requests) should train models smaller and longer than Chinchilla-optimal」。正文「2024 年」對得上 ICML 2024；「看更多 token」對應「longer」。注意它的最佳化目標是「給定品質與推論需求下總成本最低」，文章寫的是結論，沒寫成固定算力，沒有誤讀。
4. **Brown「進步最多的做法也只從 40.50% 升到 41.41%」**：成立。§1：「when using majority voting or reward models to select final answers, the biggest performance increase is only from 40.50% to 41.41% over the same sample range」；82.9%（100 次）→ 98.44%（10,000 次）、Llama-3-8B-Instruct（開放權重，文中不寫名）、MATH 都對。
5. **Snell「題目簡單或中等、或推論量少時……題目很難、或推論量大時……」**：成立。§7 Takeaways：「On easy and medium questions, which are within a model's capabilities, or in settings with small inference requirement, test-time compute can easily cover up for additional pretraining. However, on challenging questions … or under higher inference requirement, pretraining is likely more effective」，以及「not 1-to-1 "exchangeable"」。

第一輪不計入 facts_changed 的措辭修改（92% 的清單出處、Besiroglu 的「重建資料」與「相容」、Snell「使用效率提高約 2 至 4 倍」）也對過原文，沒問題。

## 查過、沒問題的主要主張（隨機抽三分之一，外加示例與圖）

把第一輪沒改的事實主張拆成 22 條，用固定種子隨機抽 7 條（C01、C05、C10、C11、C16、C20、C22）；C20 與上面的 Snell 重查重疊，所以另外加查 C04 與 C14。

- C01 定義：Kaplan 摘要「The loss scales as a power-law with model size, dataset size, and the amount of compute used for training」，圖 1 說明「improves smoothly」「when not bottlenecked by the other two」；量的是「cross entropy loss」。正文「在特定的模型、資料與訓練設定下」已經把條件帶到。
- C04 0.95 倍：§1.2 式 1.1 條件「limited number of parameters, trained to convergence on sufficiently large datasets」，αN ≈ 0.076，2^−0.076 = 0.9487。
- C05 雙對數圖上是直線：純冪律的數學性質，Kaplan 圖 9 說明（§4）也寫「For large D, performance is a straight power law in N」。正文只說冪律本身，帶下限的 Chinchilla 式另段說明，沒有混用。
- C10 5.5 倍、1.8 倍：Hoffmann §1「given a 10× increase computational budget, they suggests that the size of the model should increase 5.5× while the number of training tokens should only increase 1.8×」，正文寫成「Chinchilla 論文把前者的建議換算成」，出處歸屬正確。「超過 400 個模型」見摘要與 §1。
- C11 Besiroglu：摘要「fitting a parametric function to a reconstruction of data from their plots … inconsistent with their first two estimation methods … our re-derivation … compatible with the findings from the first two」。
- C14 Wei：定義（§2「not present in smaller models but is present in larger models」）、近隨機後明顯高於隨機（§2）、不給部分分數的指標「at best an incomplete explanation, because emergent abilities are still observed on many classification tasks」、六項 BIG-Bench 任務交叉熵早已改善但「does not explain why … or enable us to predict the scale at which emergence occurs」（§5.1）。
- C16 Schaeffer 92%：§1 與 §4（verify-1 寫 §3，實為 §4 Meta-Analysis）「hand-annotated task-metric-model family triplets [32] … 2 metrics account for > 92% of claimed emergent abilities (Fig. 5C): Multiple Choice Grade and Exact String Match」；兩種指標的定義在 §1。§7「nothing in this paper should be interpreted as claiming that large language models cannot display emergent abilities」也對。
- C22 表格：第 1 列對 Kaplan 摘要；第 3 列對 Wei §2；第 2 列「特定題集上多取樣或修改後的答對率」對 Snell（search 與 revision 後量的是 MATH 答對率），見下方懷疑項。
- 示例算術：0.5^5 = 0.03125 → 3%、0.7^5 = 0.16807 → 17%、0.9^5 = 0.59049 → 59%、0.95^5 = 0.77378 → 77%，正文、`<desc>`、圖上數字一致；獨立性是近似，Schaeffer §2 註腳說明，正文有寫。
- 圖的長條：兩張圖都以 y=640 為基線、每 1% 3.6 px。左 180/252/324/342 px 對 50/70/90/95%；右 11/61/212/277 px 對四捨五入後的 3/17/59/77%（未四捨五入應為 11.2/60.5/212.6/278.6 px，差距都在 2 px 內）。數字標籤都在長條頂端上方 14–17 px。圖上數字 50、70、90、95、3、17、59、77、5、2026 正文或表格圖說都有。照 brief 用預設 headless shell 跑 `render_svg`，輸出完整 1600×900：沒有疊字、壓線、超框，y=870 的頁尾也看得到。
- 系列規矩：沒有型號、價格、截止日期、排行榜分數；「推論」第一次出現附 inference，全文沒有「推理」；示例標「示例（假設數字，未實測）」；沒有保證句；用 grep 查中國用語（視頻、網絡、軟件、信息、質量、默認、數據、優化、硬件、程序、算法），零筆。

## 同步

- `notes.md`：2604.01411 那行改成 Sardana 等人（2401.00448）的主張，另留一行「已換掉」交代初稿用過什麼；Pearce 改成「很大一部分」並補上嵌入層範圍；第一輪改過的說法（學習率排程、重疊之處、92% 的清單、Brown 進步最多的做法、Snell 的「或」）改成現行文字；新增本輪補說明的依據（三種方法、小模型占比、程式題可自動驗證）；字數改成 2705；補記本輪的渲染結果。
- `research.json`：sources 第 11 筆換成 2401.00448（含 access 與 claims），其他筆的 claims 對齊現行正文；`running_text_characters` 2705（`app.guides.pack_ingest._body_length` 實算），`notes` 一併更新。
- dry-run：`cd apps/api && .venv/bin/python -m app.guides.pack_cli ingest --from ../../docs/ai-terms-series/batch-02/staging --slug ai-term-scaling-laws --dry-run` → `dry run: nothing written`，只有一個 warning：`no_summary`（與第一輪相同，結構不准改，所以沒加 summary）。

## 我懷疑但沒改的事

- 字數 2705 在 1,800–3,000 內，但超過 brief 的目標 2,100–2,500（第一輪後已是 2580）。本輪多出的 125 字都是讓一般讀者看懂的補說明；若要壓回目標，可以先刪 Porian 三個因素的逐項列舉。
- 表格第 2 列「多取樣或修改後的答對率」對 Snell 準確，但 Brown 量的是覆蓋率，正文又特別強調覆蓋率不等於答對率。這一格沒有錯，只是比正文鬆；沒改，因為表格是摘要，改了會牽動欄寬。
- Brown 摘要「over four orders of magnitude」可讀成「跨越四個」也可讀成「超過四個」；實驗取樣次數從 1 到 10,000，正文保留「約四個數量級」。
- Snell 的效率倍數三處寫法不一（摘要「more than 4×」、§1「about 4x」、各節圖說「up to 4x」、§8「2 − 4×」），第一輪已記；正文「約 2 至 4 倍」照 §8，仍沿用。
- Sardana 的「推論需求夠大」門檻是約 10 億次請求，而且是給定品質下比總成本；正文只寫「預期請求量夠大時」，沒寫數字也沒寫最佳化目標，讀者不會誤讀成固定算力，但精確度有限。
- `notes.md` 第 70 行說 `render_svg` 在這台機器只輸出上方約 812 px；本輪照 brief 用預設 headless shell 渲染是完整 900 px。可能是撰稿時設了 `CHROMIUM_BIN`，我只在 notes 補記本輪結果，沒刪原紀錄。
- Schaeffer 的 arXiv PDF 仍標「Preprint. Under review.」，Snell 的 abs 頁沒有會議註記；文章與 sources 都沒寫它們的發表場合，所以不影響。

facts_changed: 0
