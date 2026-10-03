# 查證與編輯紀錄：ai-term-data-poisoning

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律是實際打開該頁的 2026-10-03。User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL`，以下各頁狀態碼皆 200。arXiv 讀 abs 頁，再抓 `arxiv.org/pdf/<id>` 用 pdftotext 讀全文。

## 定義與分類（NIST、OWASP）

NIST AI 100-2 E2025 是目前最新版（2025-03-24 定稿；CSRC 頁的 Document History 只有這一版，試抓 e2026 的 final／ipd 網址皆 404）｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final｜2026-10-03｜CSRC 頁 HTML 轉純文字
NIST 的分類層級包含 ML 方法類型、攻擊的生命週期階段、攻擊者的目標、能力與知識（不是只依階段）；正文寫「從攻擊發生的階段、攻擊者的目標與能力等面向分類」｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final｜2026-10-03｜CSRC 摘要與 PDF 第 2.1 節（verify-1 補）
投毒攻擊發生在訓練階段；資料投毒＝攻擊者新增或修改部分訓練樣本；模型投毒＝攻擊者控制模型參數，常見於聯邦學習與供應鏈（第 2.1.1 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文 pdftotext
GenAI 的模型投毒例子：提供動過手腳的預訓練模型（第 3.2.2 節）｜同上｜2026-10-03｜同上
可用性投毒造成整體退化；目標式與後門投毒只讓少數目標樣本出錯，屬完整性破壞（第 2.1.2、2.3 節）｜同上｜2026-10-03｜同上
GenAI 的攻擊分訓練階段（資料投毒、模型投毒）與部署階段（提示詞注入、間接提示詞注入）（第 3.1.1 節 Training-time / Inference-time attacks）｜同上｜2026-10-03｜同上
知識庫投毒（以 PoisonedRAG 為例）列在間接提示詞注入的完整性攻擊技術之下（第 3.4.2 節 Knowledge base poisoning）｜同上｜2026-10-03｜同上
OWASP LLM04:2025 定義：預訓練、微調或嵌入資料被操弄，以植入漏洞、後門或偏見；投毒屬完整性攻擊；後門可能在觸發前不改變行為，因此難以測試｜https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/｜2026-10-03｜網頁 HTML 轉純文字
OWASP 該清單為 2025 年版，第四項（LLM04）；網站選單只有 2025 與 2023/24 兩版｜同上｜2026-10-03｜同上

## 四個位置

預訓練：資料集發布者可能只提供網址清單，攻擊者可能買下提供這些網址的網域並換掉內容（第 3.2.1 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文
微調：投毒也可能影響指令微調與人類回饋強化學習，這些資料可能刻意向大量參與者蒐集（第 3.2.1 節）｜同上｜2026-10-03｜同上
微調資料常由外部約聘人員蒐集，可能被有心人滲透（第 2 節 Threat Model）｜https://arxiv.org/abs/2510.07192｜2026-10-03｜PDF 全文
檢索資料：OWASP LLM04 把嵌入資料（embedding, converting text into numerical vectors）列入投毒範圍；RAG 知識庫投毒見下方 PoisonedRAG｜https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/｜2026-10-03｜網頁
OWASP LLM08:2025 開頭寫明向量與嵌入的弱點出現在使用 RAG 的系統，Common Examples 第 4 項就是 Data Poisoning Attacks；正文「第八項談 RAG 的向量與嵌入，也把資料投毒列為風險」據此（verify-2 改，取代原本「這個定義涵蓋 RAG 用的嵌入資料」的編輯推論）｜https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/｜2026-10-03｜網頁 HTML 轉純文字
合成資料：以合成資料訓練的流程對既有投毒與後門攻擊有相當抵抗力，主因是投毒資料與產生合成資料的提問分布不同；作者的 VIA 方法讓合成資料中的投毒內容大增，下游模型攻擊成功率接近被投毒的上游模型（NeurIPS 2025 Spotlight）｜https://arxiv.org/abs/2509.23041｜2026-10-03｜abs 頁摘要；正文不描述其方法細節（must_not：不提供可操作步驟）

## 後門

後門投毒讓模型把觸發圖樣與目標結果連結；2017 年 Gu 等人提出 BadNets，是第一個後門投毒攻擊（影像分類器、小圖塊觸發、改成目標類別）（第 2.3.3 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文
後門是文獻中唯一同時需要訓練資料與測試資料控制的攻擊（第 2.1.2 節）｜同上｜2026-10-03｜同上
旅遊網站評論摘要的後門示例：原創虛構情境，正文標「示例（虛構情境，未實測）」，沒有任何實驗或觀察結果｜—｜2026-10-03｜編輯自撰

## 研究結果（各論文自己的設定）

Carlini 等：兩種攻擊 split-view（整理者收錄時看到的內容與使用者之後下載的不同，缺少密碼學完整性保護）與 frontrunning（定期快照的群眾編輯內容，在快照前修改，事後還原仍留在快照）｜https://arxiv.org/abs/2302.10149｜2026-10-03｜abs 頁與 PDF（v2，2024-05-06）第 1、3 節
以 2023 年的情況，60 美元可控制 LAION-400M 或 COYO-700M 的 0.01%（原文 "or"，正文寫「兩個公開圖文資料集其中任一個」；兩者分別約 4 億、7 億筆圖文配對）。60 美元是網域年費：第 4.2 節「for less that $60 USD per year」，價格取自 2023 年 7 月的 Google Domains，圖 1「≤ $60 USD」；正文寫「以 2023 年的網域價格估算，每年 60 美元以內」（verify-2 補「每年」）｜同上｜2026-10-03｜abs 摘要與 PDF 第 1、4.2 節
作者沒有實際投毒（自有網址一律回 404），並已通知 10 個資料集的維護者，其中 6 個採用建議的完整性檢查｜同上｜2026-10-03｜PDF 第 1 節 Responsible disclosure、第 4.3 節 Ethical considerations
作者找不到分裂視圖攻擊曾被實際利用的證據；實際只分析 CC3M 與 LAION-400M 兩個資料集，正文寫「檢查了兩個資料集」（verify-2 補範圍）｜同上｜2026-10-03｜PDF 第 4.4 節
防禦：完整性驗證（公布所有內容的密碼雜湊）對付 split-view；以時間為主的防禦（隨機化快照順序、延遲收錄並套用可信管理者的還原）對付 frontrunning｜同上｜2026-10-03｜PDF 第 1 節
Souly 等（UK AI Security Institute、Anthropic、Alan Turing Institute 等）：從頭預訓練 600M、2B、7B、13B 參數模型，Chinchilla 最適資料量（約每參數 20 token，6B 到 260B token）；投毒文件數 100、250、500｜https://arxiv.org/abs/2510.07192｜2026-10-03｜abs 頁與 PDF（v1，2025-10-08）第 1、3 節
250 份可在 600M 到 13B 各種大小的模型植入後門；100 份未觀察到成功（附錄 D）；250 份占 13B 模型訓練 token 的 0.00016%、600M 的 0.0035%｜同上｜2026-10-03｜PDF 第 3.2 節
後門是 denial-of-service：觸發字串後輸出亂碼；選它是因為能在預訓練期間量測｜同上｜2026-10-03｜PDF 第 3.1 節
成敗取決於投毒樣本的絕對數量而非比例；微調實驗（乾淨資料由 1,000 增到 100,000 筆）也一樣｜同上｜2026-10-03｜PDF 第 3.2、5.2 節；正文不寫微調用的模型名
作者未評估後門能否撐過實際的（安全）後訓練；只研究一小類後門｜同上｜2026-10-03｜PDF 第 6 節
附錄 I 的模擬對齊訓練（另一組 Pythia 與 GPT-3.5-turbo 的德文切換後門）大幅降低後門成功率：Pythia-6.9B 降到接近零，GPT-3.5-turbo 加至少 100 筆對齊樣本降到 30% 以下；附錄 A 寫「我們的預訓練攻擊撐不過後訓練」｜同上｜2026-10-03｜PDF 附錄 A、附錄 I 圖 26（verify-1 補）
一般評測流程可能察覺不到後門｜同上｜2026-10-03｜PDF 第 2 節（"typical model evaluation protocols can fail to detect their presence"）
被投毒的微調模型在標準 NLP 基準上表現與未投毒的相近（附錄 F.5）｜同上｜2026-10-03｜PDF 第 5.2 節；正文刪減後未保留此句
PoisonedRAG：每個目標問題注入 5 段惡意文字、知識庫有數百萬段文字時，攻擊成功率 90%（摘要）；改寫問題與困惑度偵測等防禦不足；作者指出提示詞注入用指令，PoisonedRAG 用捏造的知識；USENIX Security 2025｜https://arxiv.org/abs/2402.07867｜2026-10-03｜abs 頁與 PDF（v2）第 1、2、7 節
Hubinger 等：刻意訓練後門模型，提示寫 2023 年寫安全程式碼、寫 2024 年插入可被利用的程式碼；監督式微調、強化學習、對抗訓練未能移除；對抗訓練可能讓模型更會辨認觸發條件｜https://arxiv.org/abs/2401.05566｜2026-10-03｜abs 頁摘要
持續性有條件：最大的模型與思維鏈訓練的模型最持久，較小的模型的後門「substantially easier to remove」；正文因此寫「最大的模型⋯⋯仍保有後門，較小的模型則容易移除得多」｜同上｜2026-10-03｜PDF v3 第 1 節與圖 11 說明，pdftotext（verify-1 補）

## 不寫成「任何模型都已被投毒」

投毒需要攻擊者控制部分訓練流程，在真實世界不易執行；有紀錄的案例針對早期聊天機器人、垃圾郵件過濾、惡意程式分類等持續用新資料更新的系統（第 2.3.5 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文；正文不點名產品

## 和提示詞注入的界線

OWASP LLM01:2025 Scenario #4：攻擊者修改 RAG 應用使用的文件庫中的文件，被檢索到時惡意指令改變輸出｜https://genai.owasp.org/llmrisk/llm01-prompt-injection/｜2026-10-03｜網頁 HTML 轉純文字（頁面標題確認為 LLM01:2025）
OWASP LLM08:2025 Scenario #1「Data Poisoning」：履歷藏白底白字的隱形指令，進入用 RAG 做初篩的求職系統｜https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/｜2026-10-03｜網頁 HTML 轉純文字
對照表「效果持續」的注入欄「只在讀到注入內容時」：NIST 第 3.4 節（間接注入經由模型讀到的資源進入）與第 3.4.2 節 Self-propagating injections（惡意提示可像蠕蟲般被轉寄）；原本的「通常只在當次互動」與自我散播不符（verify-2 改）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文
對照表的「主要防線」：投毒側取自 OWASP LLM04 與 NIST 第 3.2.3 節；注入側取自 NIST 第 3.4.4 節（分隔可信與不可信資料、不同權限的模型、透過明確介面接觸不可信資料）與站內提示詞注入文章的分工｜同上各頁｜2026-10-03｜同上

## 防禦

OWASP：追蹤資料來源與轉換（CycloneDX、ML-BOM）、資料版本控制（DVC）、異常偵測過濾、紅隊、監看訓練損失與模型行為｜https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/｜2026-10-03｜網頁
NIST：提供者公布密碼雜湊、下載者核對；在大型語料中偵測投毒資料可能非常困難（第 3.2.3 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文
NIST：若對攻擊不做額外假設，後門與資料中自然存在的特徵無法區分（第 2.3.3 節引述 [193]）｜同上｜2026-10-03｜同上
NIST：把模型當成不受信任的系統元件，設計應用以降低攻擊者控制模型輸出時的風險（第 3.2.3 節）；正文「例如限制它能呼叫的工具與權限」是編輯舉例，對應第 3.4.4 節「不同權限的多個模型」｜同上｜2026-10-03｜同上
「雜湊只確認下載到的和發布者當初收錄的一樣」：Carlini 等第 1 節 integrity verification「ensuring that clients observe the same data as when maintainers first indexed and annotated it」，第 6.2 節雜湊對「prior to any attack」的原始內容計算（verify-2 改，取代原本「快照前就被改的內容，雜湊照樣吻合」的編輯推論）｜https://arxiv.org/abs/2302.10149｜2026-10-03｜PDF 第 1、6.2 節
「過濾與異常偵測：嘗試在訓練前剔除可疑的樣本」：NIST 第 3.2.3 節「Data filtering can also attempt to remove poisoned samples」；OWASP LLM04「Use anomaly detection techniques to filter out adversarial data」（verify-2 刪掉沒有來源的「重複」）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf；https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/｜2026-10-03｜PDF 全文、網頁

## 譯名

國家教育研究院樂詞網以 "data poisoning"、"backdoor attack"、「資料投毒」「資料中毒」查詢皆 0 筆；"poisoning" 只有化工、醫學等領域的「中毒」「毒化」｜https://terms.naer.edu.tw/search/｜2026-10-03｜POST 查詢後讀結果頁
Google 機器學習詞彙表繁中版沒有 poisoning、backdoor 條目｜https://developers.google.com/machine-learning/glossary?hl=zh-tw｜2026-10-03｜網頁 HTML 搜尋關鍵字
台灣用法並存：數位時代用「資料中毒攻擊」、工研院產業學院用「資料下毒攻擊」、數位發展部國家資通安全情勢報告用「模型中毒（Model Poisoning）」；正文採 catalogue 指定的「資料投毒」並在第一段說明理由｜WebSearch 摘要與 https://www-api.moda.gov.tw/File/Get/acs/zh-tw/xcIAJQzhitab5T1｜2026-10-03｜數位部 PDF 以 pdftotext 讀到「模型中毒（Model Poisoning）」；其餘為搜尋結果標題，未當成內容來源

## 圖與其他

diagram-1.svg 上唯一的數字是製圖年份 2026，正文「資料截至 2026 年 10 月」有出現。hero.svg 無文字。兩張皆為手繪向量圖，非 AI 產圖。
正文不寫查證過程；日期範圍寫「資料截至 2026 年 10 月」。正文字數以 app.guides.pack_ingest._body_length 實算。

## 查核修訂（verify-1，2026-10-03）

獨立查核者今天重新打開全部 9 筆來源（皆 200）並讀全文，修了 4 處事實：NIST 分類不只依階段、BadNets 是分成攻擊者指定的類別、Souly 等附錄 I 的模擬對齊結果、Hubinger 等的持續性只在最大的模型最明顯；另把 frontrunning 的「事後還原」改成「被管理者還原」（措辭）。沒有換掉或刪除任何來源。細節見同目錄 verify-1.md。
NIST AI 100-2 E2025 仍是最新版：CSRC Document History 只有 03/24/25 Final，出版物搜尋依日期排序只列 e2025；2025-06-03 勘誤只改目錄索引 ID｜https://csrc.nist.gov/files/pubs/ai/100/2/e2025/final/docs/nist.ai.100-2e2025_potential_updates.pdf｜2026-10-03｜PDF pdftotext
PoisonedRAG 的 USENIX Security '25 議程頁｜https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag｜2026-10-03｜curl 200
VIA 在 NeurIPS 2025 論文頁可查到｜https://neurips.cc/virtual/2025/papers.html?search=Virus+Infection+Attack｜2026-10-03｜curl 200
OWASP LLM Top 10 索引頁目前列的仍是 2025 年版十項｜https://genai.owasp.org/llm-top-10/｜2026-10-03｜curl 200
修改後正文字數（verify-1 後，app.guides.pack_ingest._body_length 實算）：2,658。

## 查核修訂（verify-2，2026-10-03）

第二輪獨立查核者今天重新打開全部 9 筆來源（皆 200），5 篇 arXiv 與 NIST 讀 PDF 全文。重查第一輪的 4 處事實修改，全部維持；從其餘 34 條主張隨機抽 12 條重查，沒有問題。處理第一輪的疑點，修了 6 處事實：OWASP 嵌入與 RAG 的銜接改用 LLM08 原文、60 美元補「每年」、Carlini 第 4.4 節補「檢查了兩個資料集」、對照表注入欄改成「只在讀到注入內容時」、雜湊句改成 Carlini 原文支持的說法、過濾刪掉「重複」。另外精簡了 Souly 段與 RAG 界線段的措辭。沒有換掉或刪除任何 sources；新增讀取 OWASP LLM08 的 Common Examples 第 4 項（同一筆來源）。細節見同目錄 verify-2.md。
譯名用法再確認：數位時代「資料中毒攻擊」｜https://www.bnext.com.tw/article/84742/anthropic-data-poisoning｜2026-10-03｜curl 200；聯合新聞網「對資料下毒攻擊」｜https://udn.com/news/story/6811/9113984｜2026-10-03｜curl 200。兩者只證明用法，不列入 sources。
修改後正文字數（verify-2 後，app.guides.pack_ingest._body_length 實算）：2,672。
