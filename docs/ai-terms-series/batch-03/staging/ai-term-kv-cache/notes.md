# ai-term-kv-cache 查證紀錄

格式：主張｜來源網址｜查證日｜讀取方式。全部於 2026-10-03 以 `curl -sSL`（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）取得，HTTP 200；arXiv 讀 abs 頁的 citation_abstract 與 PDF 全文（pdftotext）。

查核者 2026-10-03 複查：docs.vllm.ai 三頁對 curl 回 429（Cloudflare 挑戰頁），改讀官方 repo 的文件原始檔（`raw.githubusercontent.com/vllm-project/vllm/main/docs/...`）與 Wayback 快照（APC 20260903211531、Quantized KV Cache 20261001145005、Prefix Caching 設計 20261001004106），內容一致；`sources` 仍寫原網址。OpenAI 原網址 301 轉到 `developers.openai.com/api/docs/guides/prompt-caching`，`sources` 已改成轉址後的網址。

第二位查核者 2026-10-03 再複查（verify-2）：arXiv 六篇、Hugging Face 兩頁、OpenAI、Anthropic、Google 詞彙表、樂詞網重新以 curl 讀取，皆 HTTP 200。docs.vllm.ai 三頁對 curl 仍回 429（Cloudflare 挑戰頁）；改用 WebFetch 讀到即時頁（WebFetch 用工具自己的 User-Agent，不帶任何個資），並與官方 repo main 分支的文件原始檔逐段對照，內容一致。Wayback 這天經代理連線被重設，沒有重讀快照。

## 定義與機制

cache 在台灣資訊名詞譯為「快取（記憶體）」，電子計算機名詞為「高速緩衝記憶體；快取」｜https://terms.naer.edu.tw/search/?query_term=cache&query_field=title&query_op=&match_type=phrase｜2026-10-03｜精確檢索結果頁 HTML
Google 機器學習詞彙表繁中版沒有 cache 的獨立詞條，但離線推論條目內文把 caching (saving) 寫作「快取 (儲存)」（與英文版同條目對照）；inference 詞條譯為推論。正文因此寫「採國家教育研究院資訊名詞的譯法，Google 詞彙表繁中版內文也這樣用」（verify-2 改寫）｜https://developers.google.com/machine-learning/glossary?hl=zh-tw｜2026-10-03｜全文 HTML（繁中版與英文版對照）
注意力把 query 與一組 key-value 映射成輸出，輸出是 value 的加權和，權重由 query 與 key 的相容性函數算出｜https://arxiv.org/abs/1706.03762｜2026-10-03｜PDF 3.2 節
解碼器自迴歸：產生下一個符號時把先前產生的符號當作額外輸入；解碼器自注意力以遮罩阻止位置看到後面的位置｜https://arxiv.org/abs/1706.03762｜2026-10-03｜PDF 3 節、3.2.3 節
因果遮罩下，token 處理後的表示不會因未來 token 改變，所以過去的 K、V 可快取重用；只需最後一個 token 的 query；快取逐層進行｜https://huggingface.co/docs/transformers/en/cache_explanation｜2026-10-03｜全文 HTML（Attention matrices 段）
不快取：每步重算所有先前 K、V，每步注意力成本隨序列長度平方；快取：每步只算當前 K、V，每步成本線性，記憶體線性增加｜https://huggingface.co/docs/transformers/en/cache_explanation｜2026-10-03｜全文 HTML（比較表）
快取只應用於推論，訓練時開啟可能出錯｜https://huggingface.co/docs/transformers/en/cache_explanation｜2026-10-03｜全文 HTML
每層的 key 與 value 快取張量形狀為 [batch_size, num_heads, seq_len, head_dim]｜https://huggingface.co/docs/transformers/en/cache_explanation｜2026-10-03｜全文 HTML（Cache storage implementation 段）
「每一層注意力的 key 與 value 張量」稱為 KV 快取，整段解碼期間要存在記憶體｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 第 1 節
權重整批共用，KV 快取每條序列各一份（正文寫「權重整批共用」）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 第 2 節 Compute costs
讀入提示時 key、value 一次算出；之後每次迭代只算新 token 的 key 與 value，1 到 n+t−1 的已快取｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 2.2 節
單一 token 的快取量以「2（key、value）× 隱藏維度 × 層數 × 每個數值的位元組數」估算（論文舉例的特定模型數字未寫入正文）｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 第 3 節 Large KV cache
滑動視窗或分塊注意力的層，快取長到視窗大小就不再增加｜https://huggingface.co/docs/transformers/en/kv_cache｜2026-10-03｜全文 HTML（Default cache 段）
請求結束後其 KV 區塊可釋放給其他請求｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 4.2 節

## 三種減量做法

PagedAttention 把每個請求的 KV 快取切成固定大小的區塊，不必放在連續空間，用到才配置；靈感來自作業系統的虛擬記憶體與分頁｜https://arxiv.org/abs/2309.06180｜2026-10-03｜abs 摘要與 PDF 第 1、4 節
既有系統依請求最大長度預先配置連續空間，造成預留、內部與外部碎片｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 3.1 節
該論文的量測中，既有系統只有 20.4%–38.2% 的 KV 快取記憶體存放實際 token 狀態；Fig. 2 的「既有系統」是作者自行重做的三種 Orca 配置（Max、Pow2、Oracle，三者都預先保留連續空間，只差保留多少），量測取自 §6.2 實驗（ShareGPT、Alpaca 改編的請求）。verify-2 為一般讀者精簡成「作者在實驗中重做三種預先保留連續空間的舊做法」，資料集名稱只留在這裡｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 第 1 節、Fig. 2 圖說、§6.1 Baseline 2、§6.2
論文總結：在相同延遲水準下，vLLM 吞吐量為既有系統（FasterTransformer、Orca）的 2–4 倍（摘要、§1、§10）。§6.2 的個別比較範圍更大：ShareGPT 上對 Orca (Oracle) 1.7–2.7 倍、對 Orca (Max) 2.7–8 倍、對 FasterTransformer 最高 22 倍。正文因此只寫「論文總結……是當時既有系統的 2 至 4 倍」，不再把 2–4 倍分別套到兩個系統上（verify-2 改寫）｜https://arxiv.org/abs/2309.06180｜2026-10-03｜abs 摘要、§1、§6.1、§6.2、§10
一批能同時處理的請求數受 GPU 記憶體中 KV 快取的空間限制，服務吞吐量受記憶體限制｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 第 3 節開頭
MQA：不同頭共用一組 key 與 value，大幅縮小這兩個張量與逐步解碼的記憶體頻寬需求｜https://arxiv.org/abs/1911.02150｜2026-10-03｜abs 摘要與 PDF 第 3 節
Shazeer 的實驗：WMT14 英德翻譯的 dev 集兩項指標（ln(PPL) 1.439 對 1.424、BLEU 26.5 對 26.7）略差，test 集 greedy 27.5 對 27.7 略差、beam-4 為 28.5 對 28.4 反而最高；Billion-Word 語言模型 dev-PPL 30.2 對 29.9 略差。正文因此寫「品質與原本相近，多數指標略差」（verify-2 改寫，原句只寫略低於基準）｜https://arxiv.org/abs/1911.02150｜2026-10-03｜PDF 4.2 節、Table 1、Table 3
MQA 讓 KV 快取張量縮小為原本的 n_heads 分之一｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 第 3 節 Partitioning the attention layer 段
GQA 把 query 頭分成 G 組、每組共用一組 key 與 value 頭，介於 MHA 與 MQA 之間；GQA-1 等於 MQA，GQA-H 等於 MHA｜https://arxiv.org/abs/2305.13245｜2026-10-03｜PDF 2.2 節
以約原預訓練 5% 的計算量（α = 0.05）把既有多頭模型改訓成 MQA／GQA（uptraining）｜https://arxiv.org/abs/2305.13245｜2026-10-03｜abs 摘要與 PDF 3.1 節
KV 量化：減少 KV 快取的位元組數；KIVI 以 2 位元量化，在所測模型上品質幾乎不變（論文設定：key 依 channel、value 依 token 分組量化）｜https://arxiv.org/abs/2402.02750｜2026-10-03｜abs 摘要
KIVI 把最近一段 token（residual 視窗，論文估 value 約 R 個、key 約 R/2 個）的 key 與 value 留在完整精度；論文說這段完整精度的滑動視窗對 GSM8K 等難題很關鍵（有它時 GSM8K 只掉約 2%，只做 2 位元假量化則明顯變差）。正文因此寫「大部分快取壓到 2 位元、最近一小段 token 維持完整精度」｜https://arxiv.org/abs/2402.02750｜2026-10-03｜PDF 第 3.3 節、第 4.2 節（查核者補）
Transformers 提供 QuantizedCache；上下文短且 GPU 記憶體足夠時，量化快取可能拖慢延遲｜https://huggingface.co/docs/transformers/en/kv_cache｜2026-10-03｜全文 HTML（Quantized cache 段）
vLLM 提供 FP8 KV 快取量化，以減少記憶體占用｜https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/｜2026-10-03｜GitHub 原始檔與 Wayback 20261001145005；verify-2 以 WebFetch 讀即時頁（FP8 KV Cache Overview 段）

## 和提示詞快取的關係

模型處理輸入時算出 key-value 狀態；提示詞快取保存可重用字首的這份狀態；快取存的是 KV 張量，不是 token 本身；整段字首須完全相符才能重用｜https://developers.openai.com/api/docs/guides/prompt-caching｜2026-10-03｜全文 HTML（What is the prompt cache? 段）
Anthropic：KV（key-value）快取表示與雜湊只放在記憶體、不做靜態儲存；快取條目有最短存活時間；cache read tokens 另有計價｜https://platform.claude.com/docs/en/build-with-claude/prompt-caching｜2026-10-03｜全文 HTML（Data retention 與 pricing 段）
OpenAI：輸入 token 依未快取、已快取、快取寫入三種費率計算｜https://developers.openai.com/api/docs/guides/prompt-caching｜2026-10-03｜全文 HTML（開頭計價說明）
vLLM 自動字首快取重用既有請求的 KV 快取；只縮短讀入提示（prefill），不縮短產生新 token（decode）｜https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/｜2026-10-03｜GitHub 原始檔與 Wayback 20260903211531（Introduction、Limits 段）；verify-2 以 WebFetch 讀即時頁
多輪對話每輪都要重新處理整段對話紀錄，字首快取讓後續輪次重用（支撐 callout「下一輪對話接得上，是因為對話紀錄又被放進輸入」）｜https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/｜2026-10-03｜GitHub 原始檔（Example workloads 段）與 WebFetch 即時頁（verify-2 補）
提示詞快取的淘汰不只看時間：vLLM 字首快取在需要新區塊時以 LRU 淘汰已快取的區塊；OpenAI 與 Anthropic 則依快取存活時間（TTL）到期。表格「保留多久」因此寫「依服務規則淘汰，如逾時或空間不足」｜https://docs.vllm.ai/en/latest/design/prefix_caching/｜2026-10-03｜GitHub 原始檔與 Wayback 20261001004106（Eviction (LRU) 段），verify-2 以 WebFetch 讀即時頁同段；OpenAI Cache lifetime 段；Anthropic Data retention 段（查核者補）
一個 token 的 KV 快取取決於它之前所有的 token，同一個 token 出現在不同位置時快取不同｜https://arxiv.org/abs/2309.06180｜2026-10-03｜PDF 2.2 節

## 長上下文的成本

每產生一個 token 都要從 HBM 載入 KV 快取，期間運算核心幾乎閒置（論文設定：500B 以上、多頭注意力的模型，大批次、長上下文）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 2.1 節
記憶體搬運時間（論文稱 memory time，不是總時間）：批次與序列小時以讀權重為主；批次與序列大時以讀 KV 快取為主。正文寫「搬資料的時間才以讀權重為主」（verify-2 改寫，原句「主要耗時」把範圍放寬成總時間）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 第 2 節 Memory costs
批次小延遲較低，但 MFU 較差，每個 token 的總成本較高｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 2.1 節
注意力機制的推論成本隨輸入序列長度平方成長。正文註明這是以整段輸入計，和 Hugging Face「有快取時每步線性」講的範圍不同，避免讀者以為兩句互相矛盾（verify-2 補）｜https://arxiv.org/abs/2211.05102｜2026-10-03｜PDF 第 1 節
逐步解碼受反覆載入 K、V 的記憶體頻寬限制｜https://arxiv.org/abs/1911.02150｜2026-10-03｜abs 摘要與 PDF 2.4.1 節

## 編寫說明

- 「台南／早餐／推薦」四步示例、圖解與 hero 都是原創教學設計，未對任何模型實測；分詞僅示意。第 1 步（讀入提示）一次存下 3 組，第 2 步起每步只新增一組；圖說與 SVG `<desc>` 已照這個寫（查核者修正）。圖上數字（第 1–4 步、3–6 組、製圖年 2026）都出現在正文。
- 依指派，不寫任何模型的 KV 快取大小或價格。vLLM 論文的特定模型每 token 快取量、Pope 等人的特定模型快取總量都讀過但未寫入。
- OpenAI 頁面同時列有特定型號的提示詞快取最短長度與費率倍數，屬產品快照，未寫入正文；只寫「命中的輸入另外計價」。
- vLLM 設計文件稱字首快取「被許多公開端點廣泛使用（例如 OpenAI、Anthropic）」，這是第三方轉述，未採用；改引 OpenAI 與 Anthropic 自己的文件。
- 字首（prefix）用字沿用系列既有的提示詞快取與推論兩篇。
- 正文字數以 `app.guides.pack_ingest._body_length` 實算：2,596（verify-2 修正與精簡後；verify-1 後為 2,662）。
- verify-2 為一般讀者精簡：vLLM 段拿掉資料集與 Orca 配置名稱、提示詞快取段把三家文件合成一句、第二段刪掉與示例段重複的「未實測」說明（示例段仍標「示例」「未實測」）。
