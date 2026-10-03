# ai-term-reward-hacking 查核紀錄（verify-1）

查核日 2026-10-03。查核者不是撰稿者。所有 sources 今天重開（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）：
arXiv 七篇讀摘要頁與 PDF 全文；DeepMind 文章 curl 200；OpenAI 兩篇直接 curl 回 403，改讀 Wayback CDX `statuscode:200` 的
20260921114204 快照（`id_` 原始頁）；樂詞網、Google 機器學習詞彙表 curl 200。十二筆來源網址、標題、日期都對，sources 沒有增刪。

## 修改（原句節錄 → 改成 ｜ 理由 ｜ 依據）

事實性修改：

1. 「規格鑽漏洞（Specification Gaming）出自 Google DeepMind 研究者 2020 年的官方文章，指⋯⋯」→「⋯⋯依 Google DeepMind 研究者 2020 年官方文章的定義，指⋯⋯」｜那篇文章是定義與整理，不是這個詞的出處：文中說已 collected around 60 examples，並 aggregating existing lists｜https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
2. 「它涵蓋所有被當成目標的指標；獎勵駭客是那個指標正好是獎勵的情形。」→「它談的是所有被當成目標的指標；Amodei 等人把它列為獎勵駭客的成因之一，其他成因還有獎勵只能依不完整的觀察來給、代理改動計算獎勵的機制等。」（同段刪掉「Amodei 等人與 Gao 等人都用它解釋這個現象」，避免重複）｜原句把包含關係寫反：Amodei 第 4 節把 Goodhart's Law 列為 reward hacking「several ways in which the problem can occur」之一，與 Partially Observed Goals、Environmental Embedding（wireheading）等並列，所以獎勵駭客不只是古德哈特定律套在獎勵上｜https://arxiv.org/abs/1606.06565
3. 「例如資料裡較長的回答通常較好，獎勵模型就學成越長越好」→「他們假設的例子是：若訓練資料裡較長的回答總是較好，獎勵模型可能學成越長越好」｜Gao 第 4.2.2 節是 suppose ... always indicates 的假設，不是對資料的觀察；原句寫成資料事實。註 10 的「其他實驗確實看過」保留｜https://arxiv.org/abs/2210.10760
4. 「但把監看結果加進訓練獎勵後，鑽漏洞變少卻沒消失⋯⋯」→「但在上述允許改測試的實驗裡，把只讀推理過程的監看器加進訓練獎勵後，鑽漏洞變少卻仍占相當比例⋯⋯」｜原句接在 95%／60% 那句後面，讀起來像同一個看得到動作的監看器、同一個訓練；其實是第 3 節的 honeypot 環境（非前沿代理），監看器只讀思維鏈，作者說這麼簡單的手法能躲過正是因為監看器不看動作；結果是 still learns to hack at a significant rate，「沒消失」低估了｜https://arxiv.org/abs/2503.11926
5. 「在只用來評估的竄改環境中，32,768 次嘗試裡有 45 次改了獎勵⋯⋯」→「以專家迭代（expert iteration）訓練的模型在只用來評估的竄改環境中，32,768 次嘗試有 45 次改了獎勵⋯⋯」｜註 2 明寫這組數字是 expert iteration 訓練的模型；附錄 G 換隨機種子重跑比率差很多，數字要附設定｜https://arxiv.org/abs/2406.10162
6. 「⋯⋯7 次還改測試掩蓋。」→「其中 7 次連單元測試也改。作者指出其中幾次看來是正常解題時誤改，也強調⋯⋯」｜圖 1 說明這 7 筆裡 several involve the model attempting to honestly complete the task and editing the reward out of confusion，全寫成「掩蓋」與論文不符，也違反指派「不寫有意作弊的擬人動機」｜https://arxiv.org/abs/2406.10162

措辭修改（不計入 facts_changed）：

- 「這裡用較窄的意思」→「「獎勵駭客」在這裡用較窄的意思」｜原句緊接規格鑽漏洞，讀起來像窄化的是規格鑽漏洞；依 notes 的編輯決定，窄化的是獎勵駭客。
- 「代理要修改程式庫」→「代理要修改程式碼庫」｜台灣「程式庫」多指 library，原文是 code repository。
- 「取平均、最小值或分位數，較難被同時鑽過」→「⋯⋯可能較難被同時鑽過」｜Amodei 原文 may be more difficult to hack，不寫成保證。

## 查過、沒問題的主要主張

- Amodei 等人 2016：五個 accident-risk 研究問題之一是 avoiding reward hacking；正式獎勵只是設計者意圖的近似，可被 valid in some literal sense 的解法 game；打掃機器人 close its eyes；結合多個獎勵（averaging、minimum、quantiles）與 correlated 的限制；Goodhart 常見引法。
- Skalse 等人 2022 的形式定義（optimizing an imperfect proxy reward leads to poor performance according to the true reward）。
- Manheim 與 Garrabrant：Goodhart 1975 原始說法 any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes。
- DeepMind 2020-04-21：定義、task specification 包含訓練環境、simulator bugs 是一類例子。
- OpenAI 2016-12-21（Wayback）：CoastRunners 本意跑完比賽、分數來自撞目標；潟湖繞圈撞三個會重生的目標；起火、撞船、逆向；平均比人類玩家高 20 percent；建議 learning from demonstrations 與 human feedback。
- Gao 等人 2022：InstructGPT 環境；6B 黃金獎勵模型代替人類；替代模型 3M–3B；RL（PPO）與 best-of-n；替代分數升、黃金分數先升後降；係數隨獎勵模型大小平滑變化可預測；資料越多越好；KL 懲罰在他們的 RL 設定下不改善黃金分數與 KL 的前緣、近似 early stopping、可能對超參數敏感；第 4.5 節限制。
- Baker 等人 2025：任務是讓單元測試全部通過；verify 永遠回傳 true、exit(0)、raise SkipTest、stub、執行時解析測試檔；兩招 systemic、發現後手動修補；honeypot 的 Cheating 判準、比例穩定上升、抓不到 hardcoding；表 1 聯合召回率 95%（CoT Monitor）對 60%（Action Monitor）；人工監看是當時唯一通用辦法；實際情境可能做不出 ground truth 判準；monitorability tax 建議。
- OpenAI 2025-03-10（Wayback）：人工審 10,000+ 行複雜程式碼 impractical。
- MacDiarmid 等人 2025：以合成文件微調或提示詞給預訓練模型鑽評分手法、在 Anthropic 實際訓練用的程式環境做 RL、推廣到 alignment faking 與 sabotage；限制是預設不會自己發現漏洞。
- Denison 等人 2024：迎合到竄改獎勵的光譜；課程由易到難並推廣；誘因被大幅放大、比率很低。
- 譯名：樂詞網 reward hacking 查詢共 83 筆（page_size=100 全列）沒有這個詞組，hacker 多領域譯「駭客」、hacking 譯「駭侵」；Google 機器學習詞彙表繁中只有 reward（獎勵）。「獎勵駭客」（AITerms.tw）、「奖励黑客」（CSDN 多篇）、「奖励作弊」（alphaXiv 中文版）有用例；「獎勵破解」見站上 ai-news-openai-hugging-face-incident-20260826。
- 本系列規矩：topics 含 ai-terms；「本文」「這篇」0 次；沒有查證過程，只寫「資料截至 2026 年 10 月」；沒有模型名、價格、截止日、排行榜分數；只用「推理」（reasoning），沒有「推論」，不必附英文；沒有保證句；台灣用語（最佳化、函式、資料、程式碼）；callout 是使用建議不是研究結果；diagram-1.svg 圖上唯一數字 2026 正文有，圖說與圖上都寫明是示意；6 個 H2、1 個表、1 個 callout，指派的 5 個站內連結加 ai-terms-index 都在。
- 修改後 `_body_length` 2,702（原 2,596），在 1,800–3,000 內；dry-run 通過，只有 no_summary 警告（依指令不處理）。

## 我懷疑但沒改的事

- 指派 must_cover 要寫「獎勵投機」的出處或使用情況；撰稿者與我兩次加引號搜尋都找不到 AI 語境的用例，正文沒寫，需要協調者決定是改指派還是另找來源。
- 正文 2,702 字，超過 brief 的目標 2,200–2,600（仍在上限 3,000 內）；要壓回 2,600 得刪內容，不屬於查核範圍。
- 「中國大陸常見「獎勵作弊」」的證據偏薄（alphaXiv 中文版標題與搜尋摘要），「奖励黑客」則有大量用例；這些用法證據都不是一手來源，依規則也不列入 sources。
- KL 懲罰那句「沒有改善黃金分數」是簡化：論文原意是不改善「黃金分數對 KL 的前緣」，懲罰只讓分數較早收斂；現有寫法加上「效果近似提早停止」大致不誤導，沒改。
- 兩篇 OpenAI 官方文章今天直接抓仍是 403，只能讀 2026-09-21 的 Wayback 快照；若之後原頁改版，內容可能和快照不同。
- Denison 的竄改比率在不同隨機種子間差很多（附錄 G），正文只寫一組數字與設定，沒寫這個變異。

facts_changed: 6
