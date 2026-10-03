# 查證與編輯紀錄：ai-term-inference

查證日一律 2026-10-03（當天實際打開）。格式：主張｜來源網址｜查證日｜讀取方式。
抓頁一律 `curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，狀態碼 200 且內容含該條目才算讀到。

## 定義與訓練／推論的分界

推論的定義：傳統機器學習是把訓練好的模型套用到未標記樣本做預測；大型語言模型是用訓練好的模型針對輸入提示產生回應；統計學裡的 inference 意義略有不同｜https://developers.google.com/machine-learning/glossary（inference 條目）｜2026-10-03｜curl 200，HTML 去標籤後讀條目
訓練的定義：決定模型參數（權重與偏差）的過程，系統讀入範例並逐步調整參數｜https://developers.google.com/machine-learning/glossary（training 條目）｜2026-10-03｜同上
「推論時權重不變」是由上述兩條定義推得（推論＝套用已訓練模型；調整參數＝訓練），詞彙表沒有逐字寫這句；文中只寫成定義上的分界，沒有寫成對任何產品的保證｜同上｜2026-10-03｜編輯推論，非逐字引用
服務商是否保存對話、日後用於訓練：文中只說「是產品條款與設定的問題，不屬於推論本身」，不對任何供應商做事實主張｜無（範圍界定，非事實主張）｜2026-10-03｜無
表格「成本結構」：推論成本以每個 token 的晶片時間或金額衡量（Pope 等人 §2 Inference cost tradeoffs）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜arXiv 摘要頁 200，另抓 https://arxiv.org/pdf/2211.05102 以 pdftotext 讀 §2、§2.1

## prefill 與 decode

提示詞的 token 全部已知，prompt phase 可用矩陣乘矩陣平行處理，同時算出第一個新 token 的機率並產生各位置的 key／value｜https://arxiv.org/abs/2309.06180｜2026-10-03｜arXiv 摘要頁 200，PDF（https://arxiv.org/pdf/2309.06180）以 pdftotext 讀 §2.2（LLM Service & Autoregressive Generation；2026-10-03 查核時更正節次）
generation phase 每步只輸入一個 token，前面位置的 key／value 已快取只補新的；結束條件是最大長度或結束符號；各步因資料相依無法平行、GPU 使用率低、受記憶體限制、佔單一請求延遲大部分｜同上｜2026-10-03｜同上（§2.2）
prefill／decode 的稱呼、輸入全部已知所以可一次平行前向、decode 是 Lgen 步的循環、兩段效能特性不同｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF §2.2（Inference Setup）
每次前向（prefill 或 decode 一步）都要把權重與 KV cache 從 HBM 搬到運算核心一次；小批次時載入權重時間為主、大批次與長序列時載入 KV cache 為主｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF §2（Memory costs）
文中「每步都要讀取模型權重與 KV 快取」＝上一條的白話；「輸出越長步數越多」＝decode 是長度為輸出 token 數的循環（Pope §2.2、Kwon §2.2）｜同上｜2026-10-03｜編輯整理
OpenAI：產生 token 幾乎總是使用 LLM 時延遲最高的一步；輸入 token 減少通常不是主要因素，除非是非常大的上下文｜https://platform.openai.com/docs/guides/latency-optimization｜2026-10-03｜網址後加 `.md`（https://platform.openai.com/docs/guides/latency-optimization.md）200 讀 Markdown；HTML 版也 200。頁面另有「少產生 50% 輸出約少 50% 延遲」「減半提示僅 1–5% 改善」兩個啟發式百分比，依本批規則（不寫供應商速度數字）未寫入

## 延遲指標與吞吐量

TTFT＝從送出請求到收到第一個 token；e2e 延遲＝TTFT＋產生時間；TTFT 通常包含排隊、prefill、網路延遲；較長提示增加 TTFT；ITL 各工具對是否含首個 token 定義不同；系統總吞吐量隨同時請求增加到飽和，每位使用者的速度下降；「各工具實作不同，定義一致才能比較」｜https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html｜2026-10-03｜curl 200；頁尾標示 Last updated Jul 20, 2026
TTFT 是從送出提示到模型產生第一個 token 的時間，串流時特別相關；串流讓使用者即時看到輸出、改善感受上的回應速度｜https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency｜2026-10-03｜curl 200，HTML 去標籤。頁內建議以特定模型名稱為例，未寫入
可調手段：選模型（大小）、縮短提示與輸出、串流（Anthropic 同頁；OpenAI 同上列）｜同上兩頁｜2026-10-03｜同上

## 成本與三類降本做法（只點名）

小批次延遲可較低但硬體利用率（MFU）較差、每個 token 成本較高；離線、不在意延遲時加大批次最有效率（該論文在 TPU v4 上分析大型 Transformer 的設定）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF §2.1「Expected tradeoffs and challenges」；設定見摘要（TPU v4 slices、500B+ 參數模型）
高吞吐服務需要同時批次處理足夠多請求；每個請求的 KV cache 很大且動態增減，碎片與重複造成浪費、限制批次大小；PagedAttention 為其解法（本文只點名，未引用該論文的倍率）｜https://arxiv.org/abs/2309.06180｜2026-10-03｜摘要頁 200，PDF §1–§2.2。論文報告的吞吐量倍數屬速度數字，依本批規則未寫入
Pope 等人的 PaLM 實驗設定用了 int8 權重量化（只寫「用了」，未寫延遲數字）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜摘要頁
把會變動的內容放在提示詞後段，使請求對 KV cache 更友善、每次要處理的輸入 token 更少（OpenAI 的原話為 maximize shared prompt prefix）｜https://platform.openai.com/docs/guides/latency-optimization｜2026-10-03｜`.md` 版 200

## 雲端與本機

雲端：e2e 延遲包含排隊、批次、網路延遲｜https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html｜2026-10-03｜curl 200（End-to-End Request Latency 段）
本機：llama.cpp 的主要目標是在各種硬體上以最少設定做 LLM 推論，「locally and in the cloud」；提供 1.5 位元至 8 位元整數量化以加速並降低記憶體用量；也有 CPU＋GPU 混合推論處理大於 VRAM 的模型（文中只寫了前兩點，未寫位元數）｜https://github.com/ggml-org/llama.cpp｜2026-10-03｜github.com 回 403；改讀 https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md（200）的 Description 段
「本機通常少了網路往返與他人的請求」是對本機執行方式的一般描述，文中已加「通常」；沒有單獨來源，也沒有寫任何速度比較｜無｜2026-10-03｜編輯描述

## 用語：推論與推理

Google 機器學習詞彙表繁體中文版：inference 譯為「推論」，並在說明黑盒模型與常識推理資料集時用「推理」描述模型的推導過程｜https://developers.google.com/machine-learning/glossary?hl=zh-tw｜2026-10-03｜curl 200，HTML 去標籤；讀「推論」條目與「黑盒模型」「ReCoRD」條目
樂詞網（國家教育研究院）中 inference 在各學科詞表的譯名：經濟學、統計學名詞、藥學、機械工程名詞等為「推論」；電子計算機名詞、資訊與通訊術語大辭典為「推理」；數學名詞、新聞傳播學名詞、教育學、電機工程名詞等兩者並列；inference engine 在電子計算機名詞為「推理引擎；推理機」；reasoning 在電子計算機名詞為「推理；推論；推導」｜https://terms.naer.edu.tw/detail/8bc45e654bd178e8380ebefabc5e389b/｜2026-10-03｜該站搜尋需先取首頁 cookie 與 csrf token，再以 GET 帶 query_term=inference／reasoning／inference engine、category=學術名詞；結果頁的詳細頁連結即上列網址（無 cookie 直接開也回 200，頁內含「以 inference 進行詞彙精確檢索結果」對照表）
結論：本站「推論＝inference、推理＝reasoning」是編輯慣例，不是詞典統一規定；與樂詞網電子計算機名詞（inference＝推理）不一致，已在文中明說｜同上兩條｜2026-10-03｜編輯判斷；此點與批次指令「inference＝推論」衝突之處見 research.json notes

## 編輯說明

- 「示例」段（民宿助理兩種問法）是原創教學情境，未實測，沒有任何速度數字，已在文中標示。
- 圖解 diagram-1.svg 圖上除版權年份 2026（正文表格圖說有）外沒有數字；hero.svg 無文字、無標誌、無人臉。
- 純正文字數（算法同 `_body_length`，含 rich_paragraph 內的連結文字 86 字）：2499。若不算連結文字為 2413。
- 沒有寫任何價格、模型名、排行榜分數、截止日期。vLLM 論文的吞吐量倍數、Pope 論文的每 token 延遲與 MFU、OpenAI 頁的百分比啟發式，都讀到了但依規則未寫入。
- ingest dry-run 的 `no_summary` 警告與範本 ai-term-sandbox 相同，批次指令未要求摘要區塊，未處理。
