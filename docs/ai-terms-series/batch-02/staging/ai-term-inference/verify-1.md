# 查核紀錄 1：ai-term-inference

查核者：獨立查核（非撰稿者）。查核日 2026-10-03。所有來源今天以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開；arXiv 兩篇另抓 PDF 以 pdftotext 讀全文。

## 修改

- 「輸入變長則主要加重那一次 prefill。」→「輸入變長則主要加重那一次 prefill，也讓之後每步要讀的 KV 快取變大。」｜事實：原句只說輸入影響 prefill，但 KV 快取隨輸入長度變大，每個 decode 步都要讀取它；NVIDIA 頁寫明注意力成本與「目前為止的輸入與輸出長度」成正比，Pope §2 Memory costs 寫序列長時載入 KV 快取的時間成為主因（計入 facts_changed）｜https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html ；https://arxiv.org/abs/2211.05102
- 「Pope 等人的 PaLM 實驗用了 int8 權重量化。」→「Pope 等人的實驗比較了 bfloat16 與量化成 int8 的權重。」｜事實範圍：論文的實驗權重是 bfloat16 或 int8 兩種（§4 寫明 weights in either bfloat16 or int8，高吞吐情境用 bfloat16），原句讀起來像全部用 int8；同時拿掉模型名 PaLM（本系列不寫模型名）（計入 facts_changed）｜https://arxiv.org/abs/2211.05102
- 「快取只省讀入提示那段，不縮短逐個產生。」→「提示詞快取只省讀入提示那段，不縮短逐個產生。」｜事實：泛稱「快取」與前文矛盾，decode 每步正是靠 KV 快取省掉重算；只有提示詞快取（重用相同字首）才是只省 prefill（計入 facts_changed）｜https://arxiv.org/abs/2309.06180 （§2.2）；https://platform.openai.com/docs/guides/latency-optimization
- 「NVIDIA 的文件指出 TTFT 通常包含排隊、prefill 與網路延遲，要分段量。」→「……與網路延遲；要知道慢在哪，得分段量。」｜歸屬：NVIDIA 頁沒有「要分段量」的建議，改寫成本文自己的結論（措辭，不計入）｜https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html
- 「他們在 TPU v4 上分析大型 Transformer 時指出」→「他們分析超大型 Transformer 在多顆加速晶片上的推論時指出」｜系列規矩：不寫型號；這句沒有引用論文數字，保留「超大型模型、多晶片」的設定範圍即可（不計入）｜https://arxiv.org/abs/2211.05102
- 「國家教育研究院樂詞網的詞表則兩個詞都用：」→「國家教育研究院樂詞網的各學科詞表則兩種譯法都有：」｜措辭：原句可誤讀為 inference 與 reasoning 兩個英文詞，實指 inference 有推論、推理兩種譯法（不計入）｜https://terms.naer.edu.tw/detail/8bc45e654bd178e8380ebefabc5e389b/
- 第一節第一段句末加「詞彙表也註明，統計學裡的 inference 意義略有不同；本文用的是機器學習的意思。」｜系列規矩：定義有分歧的詞兩邊都寫並說明採用誰的；Google 詞彙表 inference 條目原文即有此句（不計入）｜https://developers.google.com/machine-learning/glossary
- 來源：Kwon 等的標題由縮寫「…for LLM Serving…」改為論文原標題「Efficient Memory Management for Large Language Model Serving with PagedAttention」（標題對齊，不計入）｜https://arxiv.org/abs/2309.06180
- 來源：新增「國家教育研究院樂詞網：inference engine 精確檢索結果」。文中「inference engine 是推理引擎或推理機」原本引用的 inference 詳細頁上沒有這一筆；檢索頁今天不帶 cookie 也回 200 且列出六筆（電子計算機名詞「推理引擎；推理機」、管理學名詞「推理引擎」、海事等「推理機」）（不計入）｜https://terms.naer.edu.tw/search/?query_term=inference+engine&query_field=title&query_op=&match_type=phrase

改完正文字數（`_body_length`）：2583。H2 六個、表格一個（三欄）、callout 一個、指派的五個站內連結都在，結構未動。dry-run 通過，只有範本也會出現的 `no_summary` 警告。

## 查過、沒問題的主要主張

- Google 詞彙表英文版 inference 條目：傳統機器學習是把訓練好的模型套用到未標記樣本做預測；大型語言模型是用訓練好的模型針對輸入提示產生回應。training 條目：決定模型參數（權重與偏差）的過程，系統讀入範例並逐步調整參數。兩條都與文中一致（200）。
- Google 詞彙表繁體中文版：inference 條目譯為「推論」；「黑盒模型」「可解釋性」條目用「推理過程」描述模型的推導（200）。
- 樂詞網（作者標的需要 session cookie 的部分）：今天詳細頁與檢索頁不帶 cookie 都讀得到，另用首頁 cookie＋csrf 重跑一次結果相同。inference：統計學名詞「推論」、電子計算機名詞「推理」、資訊與通訊術語大辭典「推理」，數學、教育學、新聞傳播學、心理學等兩者並列；inference engine：電子計算機名詞「推理引擎；推理機」；reasoning：電子計算機名詞「推理；推論；推導」。文中「推論＝inference、推理＝reasoning 是本站用法，不是詞典規定」的寫法與證據相符，不需軟化。
- vLLM（Kwon 等，SOSP 2023）§2.2：prompt phase 提示 token 全部已知、可用矩陣乘矩陣平行處理，算出第一個新 token 的機率並產生 key／value；generation phase 每步輸入一個 token、前面位置的 key／value 已快取只算新的；到最大長度或 <eos> 結束；因資料相依無法平行、嚴重用不滿 GPU 運算、受記憶體限制、佔單一請求延遲的大部分。摘要：高吞吐服務需要批次夠多請求；KV 快取大且動態增減，碎片與重複浪費限制批次大小；提出 PagedAttention。文中未寫吞吐量倍數，符合規矩。
- Pope 等（arXiv 2211.05102）§2：延遲可拆成 prefill 與 decode；成本以每 token 的晶片秒數或金額計；小批次延遲較低但 MFU 差、每 token 成本較高；離線、不在意延遲時加大批次最有效率；權重與 KV 快取每次前向（prefill 或 decode 一步）都從 HBM 搬一次。§2.2：輸入全部已知可一次平行前向（prefill），輸出是 Lgen 步的循環（decode），兩段效能特性不同。
- NVIDIA NIM Metrics（頁尾 Last updated Jul 20, 2026）：TTFT＝送出到收到第一個 token；TTFT 通常含排隊、prefill、網路延遲；e2e＝TTFT＋Generation_time（第一個到最後一個 token）；ITL 各工具對是否含 TTFT 不同；「Tool implementations vary, so compare results only when definitions align」；同時請求增加時系統總 TPS 上升到飽和、每位使用者 TPS 下降。callout 與第四節、圖解的「完整回答時間＝首個 token 時間＋產生時間」都對得上。
- Anthropic「Reducing latency」：TTFT 是從送出提示到產生第一個 token 的時間，串流時特別相關；串流可明顯改善感受上的回應速度；降延遲手段為選模型、縮短提示與輸出、串流。頁內的模型名未進文章。
- OpenAI「Latency optimization」（.md 版 200）：產生 token 幾乎總是延遲最高的一步；減少輸入通常不是主要因素，除非是非常大的上下文；Maximize shared prompt prefix、把會變動的內容放後段讓請求對 KV 快取友善；模型大小是推論速度的主因；串流。頁內百分比未進文章。
- llama.cpp README（raw.githubusercontent.com 200）：主要目標是在各種硬體上「locally and in the cloud」做 LLM 推論；提供整數量化以加速並降低記憶體用量。
- 系列規矩：沒有價格、速度數字、截止日期、排行榜分數；改後也沒有模型名與硬體型號；示例段標「示例，未實測」，只寫「預期」；推論／推理用法一致，兩詞第一次同時出現附英文；沒有「推論時模型在學習」；沒有保證式句子；台灣用語（查無大陸用語）；圖上唯一數字 2026 在表格圖說中出現；圖上文字與 `<desc>` 與正文一致。

## 我懷疑但沒改的事

- OpenAI 來源網址 `platform.openai.com/docs/guides/latency-optimization` 今天會轉址到 `developers.openai.com/api/docs/guides/latency-optimization`（最終 200），沒改網址；若之後轉址失效，換成新網址。
- `github.com/ggml-org/llama.cpp` 經代理回 403，今天只讀到 raw.githubusercontent.com 上同一份 README；網址本身沒有直接確認。
- Google 繁中詞彙表本身並不整齊：ReCoRD 條目名稱譯作「閱讀理解與常識推論資料集」（reasoning→推論），內文又寫「常識推理」。文中說它「以推理描述模型的推導」仍屬實，但它不是乾淨的推論／推理分工，沒有加寫。
- 示例 A（貼長須知、首個字較晚）：OpenAI 指南說除非上下文非常大，縮短輸入對延遲影響通常不大，實際差異可能不明顯。文中已寫成「預期」並附「若實測與預期不同」段，沒改。
- 表格「發生頻率」「成本結構（訓練）」兩格是編輯歸納，圖說寫「依 Google 詞彙表與 Pope 等人的論文整理」，兩份來源並沒有逐字支持這兩格；內容本身無誤，沒改。
- 「推論時權重不變」是定義上的分界；研究上有在測試階段更新權重的做法（test-time training），文中沒有提，對一般服務情境不構成錯誤，沒改。
- 圖解「輸入越長，主要拉長首個 token 時間」沒有反映 KV 快取變大對 decode 的影響；已用「主要」限定、正文已補一句，圖沒改。
- `notes.md` 把 vLLM 的 prompt／generation phase 記成 §2.1，實際在 §2.2；`research.json` 的 `running_text_characters` 仍是 2499（改後為 2583），也沒有列新增的樂詞網檢索頁。這兩份不在查核者可寫範圍，請協調者更新。

facts_changed: 3
