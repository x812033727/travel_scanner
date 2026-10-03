# ai-term-kv-cache 查核紀錄（verify-1）

查核者：Claude（獨立查核，不是撰稿者）｜查核日：2026-10-03
讀法：`curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。arXiv 讀 abs 頁與 PDF 全文（pdftotext）。docs.vllm.ai 三頁對 curl 回 429（Cloudflare 挑戰頁），改讀官方 repo 的文件原始檔與 Wayback 快照，兩邊內容一致。其餘來源都是 HTTP 200；OpenAI 原網址 301 轉到 developers.openai.com，轉址後 200。

## 修改

- 「在該論文的實驗中，既有系統只有 20.4% 至 38.2% 的 KV 快取記憶體真正存著 token 狀態；在相近延遲下，vLLM 的吞吐量為⋯⋯2 至 4 倍」→「該論文用 ShareGPT、Alpaca 資料集改編的請求做實驗：作者自行重做的三種 Orca 配置，只有 20.4% 至 38.2%⋯⋯；在相同延遲水準下，vLLM 的吞吐量為⋯⋯2 至 4 倍」｜Fig. 2 的「既有系統」是作者自己實作的三種 Orca 配置（Max、Pow2、Oracle；Orca 原系統未公開），數字取自 §6.2 的 ShareGPT／Alpaca 實驗。原句沒寫設定，讀者會以為量的是線上真實系統；摘要原文是 same level of latency，不是「相近」｜https://arxiv.org/abs/2309.06180（PDF Fig. 2 圖說、§6.1 Baseline 2、§6.2、摘要）
- 「KIVI 論文（Liu 等人 2024）在所測模型上以 2 位元存快取，品質接近原本」→「KIVI 論文（Liu 等人 2024）把大部分快取壓到 2 位元、最近一小段 token 維持完整精度，在所測模型上品質接近原本」｜KIVI 把最近一段 token 的 key 與 value 留在完整精度，§4.2 明說這段滑動視窗對 GSM8K 等難題的品質很關鍵；只做 2 位元假量化的結果明顯較差。原句漏了這個讓品質成立的條件｜https://arxiv.org/abs/2402.02750（PDF §3.3、§4.2）
- 表格「保留多久」的提示詞快取欄：「依服務規則逾時淘汰」→「依服務規則淘汰，如逾時或空間不足」｜表格圖說列了 vLLM，而 vLLM 字首快取是在需要新區塊時以 LRU 淘汰，不看時間；只有 OpenAI 與 Anthropic 是依存活時間到期。新增 vLLM 設計文件為來源｜https://docs.vllm.ai/en/latest/design/prefix_caching/（Eviction (LRU) 段）；https://developers.openai.com/api/docs/guides/prompt-caching（Cache lifetime 段）；https://platform.claude.com/docs/en/build-with-claude/prompt-caching（Data retention 段）
- 圖說「由上往下看：每一步只新增一組 key 與 value」→「由上往下看：第 1 步一次存下提示的 3 組 key 與 value，之後每步只新增一組」；`diagram-1.svg` 的 `<desc>`「每步只新算一組」→「第 2 步起每步只新算一組」｜讀入提示那一步一次算出並存下所有提示 token 的 key 與 value，正文第 1 步與圖本身也是 3 組，原圖說把這個機制寫錯了｜https://arxiv.org/abs/2309.06180（§2.2 prompt phase）；https://huggingface.co/docs/transformers/en/cache_explanation
- （來源，不算事實）OpenAI 來源網址 `platform.openai.com/docs/guides/prompt-caching` → `developers.openai.com/api/docs/guides/prompt-caching`｜原網址 301 轉到新網址｜https://developers.openai.com/api/docs/guides/prompt-caching
- （來源，不算事實）新增 `vLLM 官方文件：Prefix Caching 設計說明（區塊雜湊與 LRU 淘汰）`，支撐上面的表格修改｜https://docs.vllm.ai/en/latest/design/prefix_caching/

## 查過、沒問題的主要主張

- 注意力機制以 query 比對 key、加權混合 value；解碼器自注意力以遮罩只看自己與之前的位置，產生時把先前輸出當作輸入（Vaswani §3、§3.2、§3.2.3）。
- 因果遮罩讓過去的 K、V 可以快取重用，只需最後一個 token 的 query，而且快取逐層進行。不快取時每步注意力成本隨序列長度平方成長，有快取時是線性、記憶體線性增加。快取只用於推論。每層快取張量形狀為 [batch_size, num_heads, seq_len, head_dim]（HF How caching works）。
- 滑動視窗或分塊注意力的層，快取長到視窗大小就停止增加。上下文短且記憶體夠用時，量化快取可能拖慢延遲（HF Cache strategies）。
- KV 快取是每層注意力的 key 與 value 張量，在整段解碼期間存在記憶體。和權重不同，KV 快取每條序列各一份。MQA 讓 KV 快取縮為 n_heads 分之一。設定為 500B 以上多頭注意力模型、批次 512、上下文 2048 時，每產生一個 token 都要載入 KV 快取，期間運算核心幾乎閒置。小批次、短序列時以讀權重為主，大批次、長序列時以讀 KV 快取為主。批次小則 MFU 差，每個 token 的成本較高。注意力的推論成本隨輸入長度平方成長（Pope §1、§2、§2.1、§3.3）。
- PagedAttention 以固定大小區塊、按需配置；批次大小受 KV 快取空間限制；一個 token 的 KV 快取取決於前面所有 token；請求結束後區塊可釋放；單 token 快取量的因素是 key／value、隱藏維度、層數、位元組數（Kwon §1、§2.2、§3、§4.2）。
- MQA 讓所有頭共用一組 key 與 value，降低逐步解碼的記憶體頻寬需求，品質只略降（Shazeer 摘要、§4.2）。
- GQA 把 query 頭分組、每組共用一組 key 與 value，介於 MHA 與 MQA 之間。論文以約原預訓練 5% 的計算量（α = 0.05）改訓既有多頭模型（Ainslie 摘要、§2.2、§3.1）。
- OpenAI：提示詞快取保存可重用字首的 KV 狀態，存的是 KV 張量而非 token，整段字首須相符，命中的輸入以 cached-input 費率另計。Anthropic：KV 快取表示與雜湊只放在記憶體、不做靜態儲存，快取讀取另有計價。
- vLLM：APC 重用既有請求的 KV 快取，只縮短 prefill、不縮短 decode。vLLM 支援 FP8 KV 快取量化以減少記憶體。
- 譯名：樂詞網的資訊名詞（中小學教科書、高中以下）是「快取（記憶體）」，電子計算機名詞是「高速緩衝記憶體；快取」；Google 機器學習詞彙表繁中版用「快取」、inference 用「推論」。
- 系列規矩：topics 含 `ai-terms`；「本文」「這篇」0 次；正文沒有查證過程，日期寫「資料截至 2026 年 10 月」；只用「推論」，沒有「推理」；沒有模型名、價格、KV 快取大小或排行；示例標了「示例」與「未實測／未量測」；沒有保證式說法；沒有中國用語（激活、信息、默認、優化、緩存、內存等皆 0）；指派的 5 個站內連結都在；6 個 H2、1 個表、1 個 callout；圖上數字 1–6 與 2026 正文都有；hero 無文字、無 logo。
- 渲染：`diagram-1.svg` 以預設 headless shell 渲染為 1600×900，沒有壓線、超框或疊字。

## 我懷疑但沒改的事

- Shazeer 的「品質略低於基準」只在 dev 集成立；test 集 beam-4 時 MQA 的 BLEU 反而最高。正文照論文摘要的 minor quality degradation 寫，沒有改。
- Pope「小批次、短序列時主要耗時是讀權重」講的是記憶體搬運時間（memory time），不是總時間；正文寫「主要耗時」，略為放寬，沒有改。
- 正文先寫 HF「有快取時每步注意力成本是線性」，後面又引 Pope「注意力的推論成本隨輸入長度平方成長」。兩者講的是每步與整體，都對，但讀者可能覺得互相矛盾。
- vLLM 論文的「2 至 4 倍」是摘要的總括數字；§6.2 對 FasterTransformer 的請求率差距最高到 22 倍。正文照摘要寫。
- docs.vllm.ai 今天直接打開都是 429。三頁內容是從 GitHub 原始檔與 Wayback（2026-09-03、2026-10-01）確認的，沒有讀到即時頁。
- Google 機器學習詞彙表沒有 cache 的獨立詞條，「快取」只出現在離線推論等條目的內文；譯名主要靠樂詞網支撐。
- 正文 `_body_length` 修改後為 2,662，超過第三批目標 2,200–2,600，但在上限 3,000 內。

facts_changed: 4
