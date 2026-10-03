# 查核紀錄 1：ai-term-data-poisoning

查核者不是撰稿者。查核日 2026-10-03。依 `docs/ai-terms-series/batch-03/VERIFY.md` 執行：每筆 `sources` 今天以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開（9 筆皆 200），arXiv 讀 abs 頁並抓 `arxiv.org/pdf/<id>` 用 pdftotext 讀全文，NIST 讀 CSRC 頁與 `nvlpubs.nist.gov` 的 PDF 全文，OWASP 三頁 HTML 轉純文字。作者的 notes.md 與 research.json 只當索引，每條都回到原文核對。

## 修改

1. 「NIST 的 AI 100-2 E2025 報告依攻擊發生的階段分類。」→「⋯⋯報告從攻擊發生的階段、攻擊者的目標與能力等面向分類。」｜NIST 的分類不是只依階段：CSRC 摘要寫明分類層級包含 ML 方法類型、攻擊的生命週期階段、攻擊者的目標、能力與知識，第 2.1.2 節的圖 1 更是依攻擊目標分三個圈。原句把多個分類軸說成只有一個｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final（PDF 第 2.1.1、2.1.2 節）
2. 「BadNets：影像分類器看到特定小圖塊，就分錯類別。」→「⋯⋯就分成攻擊者指定的類別。」｜NIST 第 2.3.3 節：BadNets 在部分訓練影像加小圖塊觸發並把標籤改成目標類別，分類器學到觸發與目標類別的關聯。「分錯類別」漏掉後門是指定目標，也和前一句「攻擊者想要的結果」不一致｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final（PDF 第 2.3.3 節）
3. 「微調實驗呈現同樣趨勢，但作者沒有測試後門能否撐過實際的安全訓練。」→「微調實驗呈現同樣趨勢。作者沒有評估後門能否撐過實際的安全訓練；在附錄另一組較小的實驗裡，模擬的對齊訓練就大幅降低了後門成功率。」｜論文第 6 節確實說沒有評估「實際的（安全）後訓練」，但附錄 I 做了模擬對齊：Pythia-6.9B 的 ASR 降到接近零，GPT-3.5-turbo 微調版加至少 100 筆對齊樣本就把 ASR 壓到 30% 以下；附錄 A 也寫「我們的預訓練攻擊撐不過後訓練」。原句說「沒有測試」與附錄不符，也漏了對降低恐慌最重要的反向結果｜https://arxiv.org/abs/2510.07192（PDF 第 6 節、附錄 A、附錄 I 圖 26）
4. 「在他們的設定下，監督式微調、強化學習與對抗訓練都沒能移除後門」→「在他們的設定下，最大的模型經過監督式微調、強化學習與對抗訓練仍保有後門，較小的模型則容易移除得多」｜Hubinger 等摘要：後門持續性在最大的模型、以及用思維鏈訓練的模型最強；引言（第 1 節）「Backdoor persistence is contingent」，圖 11 段落「all of our backdoors are substantially easier to remove in smaller models」。原句把只在大模型成立的結果寫成通則｜https://arxiv.org/abs/2401.05566（PDF 第 1 節與圖 11 說明）
5. （措辭，不計入事實修改）「快照前修改，事後還原，快照裡仍是改過的版本」→「快照前修改，即使事後被管理者還原，快照裡仍是改過的版本」｜原句沒寫是誰還原，讀起來像攻擊者自己還原；原文是內容管理者事後偵測並還原｜https://arxiv.org/abs/2302.10149（PDF 第 1 節）

改後 `_body_length` = 2,658（原 2,584），結構不變：6 個 H2、1 張表、1 個 callout、指派的 4 個 slug 加 `ai-terms-index` 都在。dry-run 通過，只剩協調者另加的 `no_summary` 警告。`diagram-1.svg`、`hero.svg` 未改。

## 查過、沒問題的主要主張

- NIST AI 100-2 E2025 是目前最新版：CSRC 頁 Document History 只有 03/24/25 Final；CSRC 出版物搜尋依發布日排序只列 e2025；e2026 的 final／ipd 網址 404。2025-06-03 的勘誤只改目錄索引 ID，不影響引用段落。
- 資料投毒＝插入或修改部分訓練樣本，模型投毒＝控制模型參數（2.1.1）；可用性投毒造成整體退化，目標式與後門投毒只影響少數目標樣本（2.3）；後門是唯一同時需要控制訓練與測試資料的攻擊（2.1.2）；BadNets 2017 是第一個後門投毒攻擊（2.3.3）。
- 預訓練資料集只提供網址清單、網域可被買下換內容；指令微調與 RLHF 可能向大量參與者蒐集資料（3.2.1）；Souly 等第 2 節：微調資料常來自外部約聘人員。
- GenAI 的訓練階段攻擊與部署階段（提示詞注入）分開（3.1.1）；知識庫投毒以 PoisonedRAG 為例列在間接提示詞注入的完整性攻擊之下（3.4.2）。
- 發布者公布雜湊、下載者核對；在大型語料中偵測投毒可能非常困難；把模型當不受信任元件（3.2.3）；無額外假設時後門與自然特徵無法區分（2.3.3）；投毒需控制訓練流程、真實世界不易執行，有紀錄的案例都針對持續更新的系統（2.3.5）。
- OWASP LLM04:2025 的定義（預訓練、微調、嵌入資料被操弄，植入漏洞、後門或偏見）、建議（CycloneDX／ML-BOM、DVC、異常偵測、紅隊、監看訓練損失）；OWASP 索引頁目前仍是 2025 年版。
- OWASP LLM01:2025 Scenario #4（修改 RAG 文件庫中的文件）、LLM08:2025 Scenario #1「Data Poisoning」（白底白字隱形指令的履歷進入 RAG 初篩）；對照表的注入防線（最小權限、人工核准高風險動作、隔離並標示外部內容）對得到 LLM01 建議 4、5、6 與 NIST 3.4.4。
- Carlini 等：split-view 與 frontrunning 的機制；「for just $60 USD, we could have poisoned 0.01% of the LAION-400M or COYO-700M datasets in 2023」；作者不實際投毒（自有網址回 404）、通知 10 個資料集的維護者；第 4.4 節找不到被實際利用的證據。
- Souly 等：從頭預訓練 600M–13B 模型、Chinchilla 最適資料量；成敗取決於絕對數量；250 份可靠植入、100 份不成功（附錄 D、圖 14）；250 份占 13B 訓練 token 的 0.00016%；DoS 亂碼後門、可在預訓練期間量測；微調同樣趨勢；第 2 節「typical model evaluation protocols can fail to detect their presence」。
- PoisonedRAG：摘要「90% attack success rate when injecting five malicious texts for each target question into a knowledge database with millions of texts」；改寫與困惑度偵測不足；作者區分「注入用指令、PoisonedRAG 用惡意知識」；USENIX Security '25 議程頁存在。
- Liang 等（VIA）：合成資料訓練對既有攻擊有相當抵抗力，主因分布差異；VIA 讓下游 ASR 接近被投毒的上游；arXiv 註記 NeurIPS 2025 Spotlight，NeurIPS 2025 論文頁可查到。
- Hubinger 等：2023／2024 年份觸發的程式碼後門；對抗訓練可能讓模型更會辨認觸發條件。
- 譯名：數位時代用「資料中毒」、工研院產業學院用「資料下毒」、數位部報告用「模型中毒」，確實沒有統一譯名。
- 系列規矩：topics 含 `ai-terms`；「本文／這篇」0 次；沒有型號、價格、排行榜；60 美元是論文估算的攻擊成本並附年份與設定；示例標「示例（虛構情境，未實測）」且沒寫成觀察結果；沒有「用了就不會」式保證；正文沒有查證過程；台灣用語；圖上唯一數字 2026 正文有。

## 我懷疑但沒改的事

- 字數 2,658，超過 brief 的目標 2,200–2,600（仍在 3,000 上限內）；新增的兩句是事實必要，沒有為了字數刪別段。
- Carlini 第 4.4 節的「找不到被實際利用的證據」只檢查了 CC3M 與 LAION-400M；作者自己的措辭就是概括的，正文沒加範圍。
- Carlini 的 60 美元是買網域的費用，第 4.2 節（圖 1）寫「per year」；正文沒寫「每年」。
- 「過濾與異常偵測：能去掉重複⋯⋯的樣本」的「重複」不在 NIST／OWASP 的投毒段落裡，是一般資料清理常識，沒刪。
- OWASP LLM04 原文只說 embedding，沒寫 RAG；「這個定義涵蓋 RAG 用的嵌入資料」是靠 LLM08（嵌入用於 RAG）銜接的編輯推論。
- 對照表「提示詞注入效果通常只在當次互動」：NIST 3.4.2 提到會自我散播的注入，有記憶的代理也可能延續，「通常」算是有保留。
- 防禦清單「快照前就被改的內容，雜湊照樣吻合」是由 Carlini 把雜湊對應 split-view、時間防禦對應 frontrunning 推得的編輯推論，不是原文句子。

facts_changed: 4
