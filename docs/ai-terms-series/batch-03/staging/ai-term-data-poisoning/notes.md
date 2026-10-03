# 查證與編輯紀錄：ai-term-data-poisoning

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律是實際打開該頁的 2026-10-03。User-Agent 為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL`，以下各頁狀態碼皆 200。arXiv 讀 abs 頁，再抓 `arxiv.org/pdf/<id>` 用 pdftotext 讀全文。

## 定義與分類（NIST、OWASP）

NIST AI 100-2 E2025 是目前最新版（2025-03-24 定稿；CSRC 頁的 Document History 只有這一版，試抓 e2026 的 final／ipd 網址皆 404）｜https://csrc.nist.gov/pubs/ai/100/2/e2025/final｜2026-10-03｜CSRC 頁 HTML 轉純文字
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
檢索資料：OWASP 把嵌入資料列入投毒範圍；RAG 知識庫投毒見下方 PoisonedRAG｜https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/｜2026-10-03｜網頁
合成資料：以合成資料訓練的流程對既有投毒與後門攻擊有相當抵抗力，主因是投毒資料與產生合成資料的提問分布不同；作者的 VIA 方法讓合成資料中的投毒內容大增，下游模型攻擊成功率接近被投毒的上游模型（NeurIPS 2025 Spotlight）｜https://arxiv.org/abs/2509.23041｜2026-10-03｜abs 頁摘要；正文不描述其方法細節（must_not：不提供可操作步驟）

## 後門

後門投毒讓模型把觸發圖樣與目標結果連結；2017 年 Gu 等人提出 BadNets，是第一個後門投毒攻擊（影像分類器、小圖塊觸發、改成目標類別）（第 2.3.3 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文
後門是文獻中唯一同時需要訓練資料與測試資料控制的攻擊（第 2.1.2 節）｜同上｜2026-10-03｜同上
旅遊網站評論摘要的後門示例：原創虛構情境，正文標「示例（虛構情境，未實測）」，沒有任何實驗或觀察結果｜—｜2026-10-03｜編輯自撰

## 研究結果（各論文自己的設定）

Carlini 等：兩種攻擊 split-view（整理者收錄時看到的內容與使用者之後下載的不同，缺少密碼學完整性保護）與 frontrunning（定期快照的群眾編輯內容，在快照前修改，事後還原仍留在快照）｜https://arxiv.org/abs/2302.10149｜2026-10-03｜abs 頁與 PDF（v2，2024-05-06）第 1、3 節
以 2023 年的情況，60 美元可控制 LAION-400M 或 COYO-700M 的 0.01%（原文 "or"，正文寫「兩個公開圖文資料集其中任一個」；兩者分別約 4 億、7 億筆圖文配對）｜同上｜2026-10-03｜abs 摘要與 PDF 第 1 節
作者沒有實際投毒（自有網址一律回 404），並已通知 10 個資料集的維護者，其中 6 個採用建議的完整性檢查｜同上｜2026-10-03｜PDF 第 1 節 Responsible disclosure、第 4.3 節 Ethical considerations
作者找不到分裂視圖攻擊曾被實際利用的證據（第 4.4 節）｜同上｜2026-10-03｜PDF 第 4.4 節
防禦：完整性驗證（公布所有內容的密碼雜湊）對付 split-view；以時間為主的防禦（隨機化快照順序、延遲收錄並套用可信管理者的還原）對付 frontrunning｜同上｜2026-10-03｜PDF 第 1 節
Souly 等（UK AI Security Institute、Anthropic、Alan Turing Institute 等）：從頭預訓練 600M、2B、7B、13B 參數模型，Chinchilla 最適資料量（約每參數 20 token，6B 到 260B token）；投毒文件數 100、250、500｜https://arxiv.org/abs/2510.07192｜2026-10-03｜abs 頁與 PDF（v1，2025-10-08）第 1、3 節
250 份可在 600M 到 13B 各種大小的模型植入後門；100 份未觀察到成功（附錄 D）；250 份占 13B 模型訓練 token 的 0.00016%、600M 的 0.0035%｜同上｜2026-10-03｜PDF 第 3.2 節
後門是 denial-of-service：觸發字串後輸出亂碼；選它是因為能在預訓練期間量測｜同上｜2026-10-03｜PDF 第 3.1 節
成敗取決於投毒樣本的絕對數量而非比例；微調實驗（乾淨資料由 1,000 增到 100,000 筆）也一樣｜同上｜2026-10-03｜PDF 第 3.2、5.2 節；正文不寫微調用的模型名
作者未評估後門能否撐過實際的（安全）後訓練；只研究一小類後門｜同上｜2026-10-03｜PDF 第 6 節
一般評測流程可能察覺不到後門｜同上｜2026-10-03｜PDF 第 2 節（"typical model evaluation protocols can fail to detect their presence"）
被投毒的微調模型在標準 NLP 基準上表現與未投毒的相近（附錄 F.5）｜同上｜2026-10-03｜PDF 第 5.2 節；正文刪減後未保留此句
PoisonedRAG：每個目標問題注入 5 段惡意文字、知識庫有數百萬段文字時，攻擊成功率 90%（摘要）；改寫問題與困惑度偵測等防禦不足；作者指出提示詞注入用指令，PoisonedRAG 用捏造的知識；USENIX Security 2025｜https://arxiv.org/abs/2402.07867｜2026-10-03｜abs 頁與 PDF（v2）第 1、2、7 節
Hubinger 等：刻意訓練後門模型，提示寫 2023 年寫安全程式碼、寫 2024 年插入可被利用的程式碼；監督式微調、強化學習、對抗訓練未能移除；對抗訓練可能讓模型更會辨認觸發條件｜https://arxiv.org/abs/2401.05566｜2026-10-03｜abs 頁摘要

## 不寫成「任何模型都已被投毒」

投毒需要攻擊者控制部分訓練流程，在真實世界不易執行；有紀錄的案例針對早期聊天機器人、垃圾郵件過濾、惡意程式分類等持續用新資料更新的系統（第 2.3.5 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文；正文不點名產品

## 和提示詞注入的界線

OWASP LLM01:2025 Scenario #4：攻擊者修改 RAG 應用使用的文件庫中的文件，被檢索到時惡意指令改變輸出｜https://genai.owasp.org/llmrisk/llm01-prompt-injection/｜2026-10-03｜網頁 HTML 轉純文字（頁面標題確認為 LLM01:2025）
OWASP LLM08:2025 Scenario #1「Data Poisoning」：履歷藏白底白字的隱形指令，進入用 RAG 做初篩的求職系統｜https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/｜2026-10-03｜網頁 HTML 轉純文字
對照表的「主要防線」：投毒側取自 OWASP LLM04 與 NIST 第 3.2.3 節；注入側取自 NIST 第 3.4.4 節（分隔可信與不可信資料、不同權限的模型、透過明確介面接觸不可信資料）與站內提示詞注入文章的分工｜同上各頁｜2026-10-03｜同上

## 防禦

OWASP：追蹤資料來源與轉換（CycloneDX、ML-BOM）、資料版本控制（DVC）、異常偵測過濾、紅隊、監看訓練損失與模型行為｜https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/｜2026-10-03｜網頁
NIST：提供者公布密碼雜湊、下載者核對；在大型語料中偵測投毒資料可能非常困難（第 3.2.3 節）｜https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf｜2026-10-03｜PDF 全文
NIST：若對攻擊不做額外假設，後門與資料中自然存在的特徵無法區分（第 2.3.3 節引述 [193]）｜同上｜2026-10-03｜同上
NIST：把模型當成不受信任的系統元件，設計應用以降低攻擊者控制模型輸出時的風險（第 3.2.3 節）；正文「例如限制它能呼叫的工具與權限」是編輯舉例，對應第 3.4.4 節「不同權限的多個模型」｜同上｜2026-10-03｜同上
「快照前就被改的內容，雜湊照樣吻合」：由 Carlini 等把雜湊對應 split-view、另以時間為主的防禦對應 frontrunning 推得，屬編輯推論｜https://arxiv.org/abs/2302.10149｜2026-10-03｜PDF 第 1 節

## 譯名

國家教育研究院樂詞網以 "data poisoning"、"backdoor attack"、「資料投毒」「資料中毒」查詢皆 0 筆；"poisoning" 只有化工、醫學等領域的「中毒」「毒化」｜https://terms.naer.edu.tw/search/｜2026-10-03｜POST 查詢後讀結果頁
Google 機器學習詞彙表繁中版沒有 poisoning、backdoor 條目｜https://developers.google.com/machine-learning/glossary?hl=zh-tw｜2026-10-03｜網頁 HTML 搜尋關鍵字
台灣用法並存：數位時代用「資料中毒攻擊」、工研院產業學院用「資料下毒攻擊」、數位發展部國家資通安全情勢報告用「模型中毒（Model Poisoning）」；正文採 catalogue 指定的「資料投毒」並在第一段說明理由｜WebSearch 摘要與 https://www-api.moda.gov.tw/File/Get/acs/zh-tw/xcIAJQzhitab5T1｜2026-10-03｜數位部 PDF 以 pdftotext 讀到「模型中毒（Model Poisoning）」；其餘為搜尋結果標題，未當成內容來源

## 圖與其他

diagram-1.svg 上唯一的數字是製圖年份 2026，正文「資料截至 2026 年 10 月」有出現。hero.svg 無文字。兩張皆為手繪向量圖，非 AI 產圖。
正文不寫查證過程；日期範圍寫「資料截至 2026 年 10 月」。正文字數以 app.guides.pack_ingest._body_length 實算。
