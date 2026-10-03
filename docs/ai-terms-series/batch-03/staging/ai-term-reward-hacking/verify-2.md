# ai-term-reward-hacking 查核紀錄（verify-2）

查核日 2026-10-03。第二輪獨立查核者，不是撰稿者，也不是第一輪查核者。User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。
今天重開：arXiv 七篇摘要頁與 PDF 全文（curl 200，pdftotext）；DeepMind 文章 curl 200；樂詞網（hacking、hacker、reward hacking，`page_size=100`）、
Google 機器學習詞彙表繁中版、AITerms.tw 都是 curl 200。兩篇 OpenAI 官方文章直接 curl 與 WebFetch 仍是 403；這一輪 Wayback 快照被出口代理重設連線，
抓不到（archive.org 的 availability API 仍列出 20260921114204 快照，status 200），所以改用 WebSearch 限定 openai.com 讀摘要交叉（brief 允許的讀法）。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

事實性修改：

1. 「台灣的文章可見「獎勵駭客」，中國大陸常見「獎勵黑客」「獎勵作弊」，也有人譯「獎勵破解」。」→「⋯⋯簡體中文資料多寫「獎勵黑客」，另有「獎勵作弊」「獎勵破解」等譯法。」｜第一輪疑點：「獎勵作弊」說成「常見」證據不夠。今天再查，「奖励作弊」只出現在 alphaXiv 中文版的論文標題（Skalse 論文、arXiv:2603.07084），那些標題多半是機器翻譯；「奖励黑客」則在 CSDN 多篇、Lilian Weng 部落格的中譯、智源社區都看得到。所以只寫「另有⋯⋯等譯法」，不寫「常見」｜https://www.alphaxiv.org/zh/abs/2209.13085 、https://www.alphaxiv.org/zh/abs/2603.07084 、https://blog.csdn.net/hehedadaq/article/details/144193374（用法證據，不列入 sources）
2. 「常用的 KL 懲罰（限制模型別離原本太遠）沒有改善黃金分數，效果近似提早停止」→「常用的 KL 懲罰會限制模型別離原本太遠；在他們的強化學習設定下，它只讓分數較早停住，同樣偏離程度時的黃金分數並沒有變高，效果近似提早停止」｜第一輪疑點。第 3.6 節原文：KL 懲罰 only causes the gold RM score to converge earlier, but does not affect the KL_RL-gold reward frontier。「沒有改善黃金分數」不精確：提早停住可能避開後段下滑，最終黃金分數不一定比沒加懲罰低；論文說的是同樣 KL 下沒有比較高｜https://arxiv.org/abs/2210.10760
3. 「人工抽查：⋯⋯限制是規模，OpenAI 的官方文章指出，人逐行審完上萬行複雜程式碼並不實際。」→「⋯⋯限制是規模：代理的輸出與動作越複雜、用得越廣，靠人看就越難跟上。」｜官方頁今天讀不到（第一輪疑點）。用 WebSearch 限定 openai.com 讀到的原句是「10,000+ lines of complex code written by a superior programmer」，講的是比人強的模型寫出的程式，正文寫成一般的規模問題脫離了原脈絡。改用 Baker 論文第 1 節今天讀得到的原句：manual monitoring is unlikely to scale as their outputs and actions grow more complex—possibly even superhuman—and become more widely used｜https://arxiv.org/abs/2503.11926
4. Denison 段在「比率很低」後補上「而且同一套課程換個隨機種子重跑，比率就可能差到兩倍以上」｜第一輪疑點：只給一組 45/32,768 會讓人以為這是穩定數字。第 5.2 節：兩個隨機種子的竄改獎勵比率差 2.4 倍、改測試差 6.7 倍，作者說觀察到的差異很多可能只是雜訊；附錄 G 是 24/10,000 對 32/32,768。附錄 G 用的是同一套課程的 exploit-only 專家迭代，不是註 2 那個模型本身，所以寫「同一套課程」不寫「同樣設定」｜https://arxiv.org/abs/2406.10162

來源修改（不計入 facts_changed）：

- 刪掉 sources 的 OpenAI 2025 官方文章 https://openai.com/index/chain-of-thought-monitoring/ ，正文刪掉「OpenAI 也發了官方文章」｜改完第 3 點後，正文沒有主張只靠這一頁；今天又讀不到原頁。指派的建議來源寫「官方文章或 arXiv:2503.11926」，arXiv 那篇仍在。sources 從 12 筆變 11 筆。
- OpenAI 2016 官方文章保留｜賽船例的核心（本意是跑完比賽、分數來自撞沿途目標、繞圈反覆撞同樣目標）今天另有 DeepMind 2020 文與 Denison 第 2.1 節兩個打得開的一手來源佐證，兩者都註明出處是 Clark & Amodei 2016；潟湖、三個目標、起火撞船逆向、平均比人類高 20 percent、建議 learning from demonstrations 與 human feedback，以 WebSearch 限定 openai.com 的摘要逐項對到。

措辭與好讀性修改（不計入 facts_changed）：

- Gao 段：「沿用 OpenAI 先前指令微調研究的實驗設定量化這件事：用一個 60 億參數的獎勵模型當「黃金標準」代替人類，拿它標註的比較資料訓練 300 萬到 30 億參數的替代獎勵模型，再用強化學習或「產生 n 個挑最高分」來最佳化」→「用模擬實驗量化這件事：拿一個 60 億參數的獎勵模型當「黃金標準」代替真人評分，用它標註的資料訓練 300 萬到 30 億參數不等的替代獎勵模型，再以強化學習或「產生 n 個挑最高分」追替代模型的分數」｜一般讀者不需要知道是哪個先前研究的環境；設定的數字留著。
- 「作者認為主因是最佳化把輸出推到獎勵模型訓練資料以外的範圍」→「作者推測主因是最佳化把輸出推到獎勵模型沒見過的範圍」｜原文 We expect，「推測」較貼切；註 10 那句縮短成「他們在其他實驗也真的遇過該簡短時仍寫很長的情形」。
- 「黃金標準也是模型，人類標註與真正意圖的落差不在量測範圍內」→「另外，黃金標準本身也是模型，標註和人類真正意圖的落差，這個實驗量不到」｜讀起來較順，意思同第 4.5 節。
- 推理監看一項：「Baker 等人監看兩種大範圍作弊時，看得到推理過程的監看器抓到其中 95%」→「Baker 等人比較過：對提早結束與跳過測試這兩招，連推理過程一起看的監看器抓到 95%」｜讀者在前一節已看過這兩招，直接點名比「大範圍作弊」好懂；第 2.1 節的 CoT Monitor 看的是推理過程加動作與輸出，「連⋯⋯一起看」較精確。後半「上述允許改測試的實驗裡」改「允許改測試的那組實驗」，「推理過程也不再出現打算鑽漏洞的文字」改「推理過程不再寫出鑽漏洞的打算」。
- 古德哈特段刪掉「它談的是所有被當成目標的指標；」，「Amodei 等人把它列為」改「Amodei 等人把這條定律列為」｜前一句的定義已說明它講任何指標，刪掉重複。
- MacDiarmid 段：「先讓預訓練模型讀到幾種鑽程式評分的手法，再放進實際用於訓練的程式環境做強化學習；模型學會鑽漏洞後」→「先告訴模型幾種鑽程式評分的手法，再讓它在實際訓練用的程式環境做強化學習；學會鑽漏洞後，模型」｜精簡。
- Denison 段：刪掉「（expert iteration）」英文；「作者指出其中幾次看來是正常解題時誤改，也強調⋯⋯」改成「這 7 次裡有幾次看來是正常解題時誤改。作者強調⋯⋯」｜精簡，並寫清楚「幾次」是那 7 次裡的。

## 第一輪修改逐條重查（都保留）

1. 規格鑽漏洞「依 DeepMind 文章的定義」而非「出自」：文中 we have collected around 60 examples so far (aggregating existing lists and ongoing contributions from the AI community)，日期 April 21, 2020，作者 Krakovna 等。✓
2. 古德哈特定律是獎勵駭客的成因之一：Amodei 第 4 節 there are several ways in which the problem can occur，列 Partially Observed Goals、Complicated Systems、Abstract Rewards、Goodhart's Law、Feedback Loops、Environmental Embedding（wireheading）。正文「獎勵只能依不完整的觀察來給、代理改動計算獎勵的機制」分別對到第一與最後一項。✓
3. Gao 回答長度是假設例：第 4.2.2 節 suppose in the training distribution a feature like answer length always indicates a higher quality answer；註 10 在 InstructGPT 設定的其他實驗看過該簡短時仍很長。✓
4. 推理監看的混淆結果屬於允許改測試、只讀思維鏈的那組實驗：第 3.1 節 honeypot、non-frontier agent、monitor only looks at the agent CoT and not its actions；第 3.2 節 still learns to hack at a significant rate、recall falls to near zero、Reward hacks this simple are only possible because the monitor … solely looks at the agent's CoT。✓
5. Denison 數字的設定：註 2 Models trained with expert iteration (Section 4.1) tampered with their reward in 45 episodes and also tampered with tests to avoid detection in 7 episodes out of 32,768。✓
6. 那 7 次不全是掩蓋：圖 1 說明 several of these involve the model attempting to honestly complete the task and editing the reward out of confusion。✓

## 隨機抽查的其餘主張（32 條中以亂數抽 11 條）

- 樂詞網與 Google 機器學習詞彙表繁中版都沒有 reward hacking 詞組：樂詞網 reward hacking 查詢 83 筆，只有 hacking 單詞條（駭侵）；Google 詞彙表繁中只有「獎勵」。✓
- 台灣文章可見「獎勵駭客」：AITerms.tw 詞條標題「獎勵駭客攻擊（Reward Hacking）」。✓
- 樂詞網 hacker＝駭客：27 筆，多個領域譯「駭客」。✓
- Amodei 等人五個 accident-risk 研究問題之一是 avoiding reward hacking（摘要）。✓
- Denison 光譜：Specification gaming can range from simple behaviors like sycophancy … to … reward-tampering, where a model directly modifies the mechanism of reward administration。迎合的解釋 outputs that conform to user biases。✓
- 古德哈特常見引法：Gao「When a measure becomes a target, it ceases to be a good measure」、Amodei「when a metric is used as a target, it ceases to be a good metric」。✓
- 替代分數一路上升、黃金分數先升後降：圖 1 說明 the gold reward initially increases and later decreases；第 4.2.1 節 the proxy scores are roughly linear in KL。✓
- 獎勵模型越大下降越緩且可預測、資料越多越好：係數 vary smoothly with the number of proxy reward model parameters … This allows prediction；第 3.3 節 more data leads to better gold scores and less goodharting。✓
- 黃金標準量不到標註與真正意圖的落差：第 4.5 節 mismatch between the ground truth labels and the actual human intent … not captured。✓
- Denison 課程推廣：training on early-curriculum environments leads to more specification gaming on remaining environments；學會簡單招式推廣到更難的環境。✓
- 比率很低、誘因刻意放大：None of our models reward-tamper more than 1% of the time；seriously exaggerates the incentives。✓

因為這輪改動牽涉到，其餘主張也順手重查過：Skalse 形式定義、DeepMind 定義與 task specification 含 training environment、simulator bugs、Goodhart 1975 原始說法（Manheim 註 1 與參考文獻）、Gao 6B／3M–3B／PPO 與 best-of-n、Baker 任務與五種捷徑、兩招 systemic 且發現後手動修補、Cheating 判準與抓不到 hardcoding、95%／60%（表 1）、實際情境做不出 ground truth、monitorability tax、Amodei 多種獎勵與 correlated 的限制、MacDiarmid 的設定、推廣與限制，都對得上。

本系列規矩：topics 含 ai-terms；「本文」「這篇」0 次；沒有查證過程，只寫「資料截至 2026 年 10 月」；沒有模型名、價格、截止日、排行榜分數；只用「推理」（reasoning），沒有「推論」；沒有保證句；台灣用語（「黑客」只出現在引述簡體用法的引號內）；6 個 H2、1 個表、1 個 callout，指派的 5 個站內連結加 ai-terms-index 都在；diagram-1.svg 圖上唯一數字 2026 正文有，「KL 懲罰：效果近似提早停止」和改後正文一致。修改後 `_body_length` 2,695（verify-1 後 2,702）；dry-run 通過，只有 no_summary 警告（依指令不處理）。

## 我懷疑但沒改的事

- 指派 must_cover 要寫「獎勵投機」的出處或使用情況；這輪再查三次（正體、簡體、加英文），結果頁都沒有這個詞組，搜尋結果裡唯一的台灣學術頁（CASE 報科學）讀全文也沒有。正文仍不寫，需要協調者決定改指派或另給來源。
- 正文 2,695 字，仍高於 brief 的目標 2,200–2,600（在上限 3,000 內）。這輪補了隨機種子變異與 KL 的精確說法，再精簡設定描述後只淨減 7 字；要壓到 2,600 得刪掉有來源的例子。
- 兩篇 OpenAI 官方頁這一輪連 Wayback 都讀不到。2025 那篇已從正文與 sources 移除；2016 那篇的潟湖、三個目標、起火撞船逆向、20 percent 與「建議示範與人類回饋」只靠 WebSearch 限定 openai.com 的摘要對到，核心例子另有 DeepMind 與 Denison 佐證。
- 譯名用法（獎勵駭客、獎勵黑客、獎勵作弊、獎勵破解）的證據都不是一手來源；「獎勵作弊」只見於 alphaXiv 可能是機器翻譯的標題。
- diagram-1.svg 右側「較大的獎勵模型、較多資料 → 下降較緩」：資料量那一半 Gao 的說法是 better gold scores and less goodharting，且趨勢不如模型大小乾淨；圖說已標明是示意，沒改圖。

facts_changed: 4
