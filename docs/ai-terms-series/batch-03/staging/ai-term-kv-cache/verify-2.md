# ai-term-kv-cache 查核紀錄（verify-2）

查核者：Claude（第二輪獨立查核，不是撰稿者，也不是第一輪查核者）｜查核日：2026-10-03
讀法：`curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。arXiv 六篇重讀 abs 頁與 PDF 全文（pdftotext）。Hugging Face 兩頁、OpenAI、Anthropic、Google 詞彙表（繁中版與英文版）、樂詞網都是 HTTP 200，OpenAI 舊網址仍 301 轉到現在的網址。docs.vllm.ai 三頁對 curl 仍回 429（Cloudflare 挑戰頁），這次改用 WebFetch 讀到即時頁（WebFetch 用工具自己的 User-Agent，不帶任何個資），並和官方 repo main 分支的文件原始檔逐段對照，內容一致。Wayback 這天經代理連線被重設，所以沒有重讀快照。

## 修改

- 「在相同延遲水準下，vLLM 的吞吐量為 FasterTransformer 與 Orca 的 2 至 4 倍」→「論文總結，在相同延遲水準下，vLLM 的吞吐量是當時既有系統的 2 至 4 倍」｜2–4 倍是摘要、§1、§10 的總結數字。§6.2 的個別比較範圍更大：ShareGPT 上對 Orca (Oracle) 1.7–2.7 倍、對 Orca (Max) 2.7–8 倍、對 FasterTransformer 最高 22 倍。原句把 2–4 倍分別套到兩個系統上，FasterTransformer 那一半不成立｜https://arxiv.org/abs/2309.06180（摘要、§1、§6.2、§10）
- 「Shazeer 的翻譯實驗中品質略低於基準」→「Shazeer 的實驗裡品質與原本相近，多數指標略差」｜Table 1 中 dev ln(PPL) 1.439 對 1.424、dev BLEU 26.5 對 26.7、test greedy 27.5 對 27.7 都略差，test beam-4 卻是 28.5 對 28.4，MQA 最高；Table 3 語言模型 dev-PPL 30.2 對 29.9 略差。原句只寫「略低」，漏了 test 集的結果｜https://arxiv.org/abs/1911.02150（§4.2、Table 1、Table 3）
- 「批次小、序列短時，主要耗時才是讀權重」→「批次小、序列短時，搬資料的時間才以讀權重為主」｜Pope 等人說的是 memory time，也就是把權重與 KV 快取從 HBM 搬進運算核心的時間，不是總時間。原句把範圍放寬成總時間｜https://arxiv.org/abs/2211.05102（§2 Memory costs）
- （措辭，不算事實）「該論文用 ShareGPT、Alpaca 資料集改編的請求做實驗：作者自行重做的三種 Orca 配置，只有 20.4% 至 38.2% 的 KV 快取記憶體真正存著 token 狀態」→「作者在實驗中重做三種預先保留連續空間的舊做法，量到只有 20.4% 至 38.2% 的 KV 快取記憶體真正用來存 token 的 key 與 value」｜為一般讀者拿掉資料集與配置名稱，但保留「作者自己重做、在實驗中量到」這個設定。三種 Orca 配置都預先保留空間，只差保留多少；資料集名稱改記在 notes.md｜https://arxiv.org/abs/2309.06180（§1、Fig. 2 圖說、§6.1 Baseline 2）
- （措辭，不算事實）「他們也提到，注意力的推論成本隨輸入長度平方成長」→「他們也提到，以整段輸入計，注意力的推論成本隨長度平方成長（前面說的線性是指每一步）」｜處理第一輪的疑點。Hugging Face 說的是有快取時每一步的成本與長度成線性，Pope 說的是整段輸入，兩句都對；補一句說明範圍，讀者就不會以為兩句互相矛盾｜https://huggingface.co/docs/transformers/en/cache_explanation；https://arxiv.org/abs/2211.05102（§1）
- （措辭，不算事實）「cache 依國家教育研究院資訊名詞與 Google 機器學習詞彙表繁中版譯為『快取』」→「cache 採國家教育研究院資訊名詞的譯法『快取』，Google 機器學習詞彙表繁中版內文也這樣用」｜Google 詞彙表沒有 cache 的獨立詞條，只在離線推論條目把 caching (saving) 寫作「快取 (儲存)」（和英文版同條目對照過）。pack 的來源標題也一併改掉「cache 譯為快取」｜https://terms.naer.edu.tw/search/?query_term=cache&query_field=title&query_op=&match_type=phrase；https://developers.google.com/machine-learning/glossary?hl=zh-tw
- （措辭，不算事實）「Pope 等人指出，權重由所有請求共用」→「權重整批共用」｜原文是 unlike the weights, the KV cache is unique for each sequence in the batch｜https://arxiv.org/abs/2211.05102（§2 Compute costs）
- （措辭，不算事實）「這是官方文件的說法：OpenAI 寫明提示詞快取存的是 key-value 張量而非文字，Anthropic 提到快取的 KV 表示只放在記憶體，vLLM 的字首快取也是重用 KV 快取」→「OpenAI、Anthropic 與 vLLM 的官方文件都寫明，提示詞快取存的是 KV 狀態」｜精簡。OpenAI 原文寫的是 not the tokens themselves，「而非文字」不夠準，就一併拿掉｜https://developers.openai.com/api/docs/guides/prompt-caching；https://platform.claude.com/docs/en/build-with-claude/prompt-caching；https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
- （措辭，不算事實）第二段刪掉「以下從四步示例講到長上下文的成本」與「標『示例』者為教學設計，未實測」，示例段的「未量測」改成「未實測」｜示例段本身就標了「示例」「未實測」，第二段那句是重複；字數因此從 2,662 降到 2,596，落進第三批的目標 2,200–2,600。「另外，⋯⋯都另外計價」改成「至於⋯⋯都另外計價」，避免同一句用兩次「另外」。

## 第一輪修改的重查

- vLLM 20.4%–38.2%：Fig. 2 圖說是 during the experiment in §6.2；Orca (Max) 20.4、Orca (Pow2) 26.8、Orca (Oracle) 38.2；§6.1 寫明 Orca 未公開，作者自行實作三種版本。摘要原文是 with the same level of latency。成立，這輪只精簡寫法。
- KIVI：§3.3 與 Algorithm 1 把最近一段 token 的 key 與 value 留在完整精度（full precision sliding window），§4.2 說這段視窗對 GSM8K 等難題很關鍵；摘要寫 maintain almost the same quality。成立。
- 表格「依服務規則淘汰，如逾時或空間不足」：vLLM 設計文件 Eviction (LRU) 段是在需要新區塊時淘汰最久沒用的區塊，不看時間（WebFetch 即時頁與 GitHub 原始檔一致）；OpenAI Cache lifetime 段寫 Cache entries are not stored indefinitely 並有存活時間；Anthropic Data retention 段寫 minimum lifetime of 5 minutes (standard) or 1 hour (extended)。成立。
- 圖說與 `diagram-1.svg` 的 `<desc>`「第 1 步一次存下提示的 3 組」：vLLM §2.2 寫 prompt phase 時一次算出 k1…kn 與 v1…vn，之後每次迭代只算新 token 的。成立。
- OpenAI 網址：`platform.openai.com/docs/guides/prompt-caching` 今天仍 301 到 `developers.openai.com/api/docs/guides/prompt-caching`，轉址後 200。成立。
- 新增的 vLLM Prefix Caching 設計文件：即時頁與原始檔都有 Eviction (LRU) 段。成立。

## 隨機抽查（其餘 30 條事實主張抽 10 條，seed 20261003）

- KV 快取是推論時的暫存，每步每層存前面各位置的 key 與 value，下一步只補算新 token：HF How caching works（stored kv pairs … reused for subsequent tokens；Caching should only be used for inference）。
- Vaswani 2017 解碼器自注意力以遮罩只看自己與之前的位置：§3.2.3（prevent leftward information flow … masking out）、§3.1。
- 某 token 某層的 key 與 value 不因後面的新 token 改變：HF（Once a token is processed, its representation never changes with respect to future tokens）。
- 記憶體成長因素清單：HF 快取張量形狀 [batch_size, num_heads, seq_len, head_dim]；Kwon §3 的單 token 估算是 2 × 隱藏維度 × 層數 × 位元組數；Pope §2 權重整批共用、KV 快取每條序列各一份。
- 滑動視窗層的快取長到視窗大小就停止：HF Cache strategies（Default cache 段，sliding window 或 chunked attention）。
- PagedAttention 不縮小每個 token 的快取，而是讓同樣記憶體放進更多請求：Kwon §4、§6.2（enable batching more requests）。
- MQA 所有頭共用一組 key 與 value，快取縮為頭數分之一：Shazeer 摘要；Pope §3.3（reduces the size of the KV cache tensors by a factor of nheads）。
- 量化是 Hugging Face 與 vLLM 都提供的選項：HF QuantizedCache（hqq、quanto）；vLLM Quantized KV Cache（FP8）。
- 注意力的推論成本隨輸入長度平方成長：Pope §1。
- 命中提示詞快取的輸入，OpenAI 與 Anthropic 都另外計價：OpenAI 寫 input tokens use the uncached-input, cached-input, or cache-write rate；Anthropic 寫 Cache read tokens are 0.1 times the base input tokens price。正文沒寫倍數。

順手另查：GQA 用約原預訓練 5% 的計算量改訓（摘要、§3.1 α = 0.05）；樂詞網「快取（記憶體）」（高中以下資訊名詞）與「高速緩衝記憶體；快取」（電子計算機名詞）；callout「下一輪對話接得上，是因為對話紀錄又被放進輸入」，由 vLLM APC 文件 Example workloads 段支撐（多輪對話每輪都要重新處理整段對話紀錄），已補進 notes.md 與 research.json。

## 系列規矩

topics 含 `ai-terms`；「本文」「這篇」0 次；正文沒有查證過程；只用「推論」，沒有「推理」；沒有模型名、價格、KV 快取大小或排行；示例段標了「示例」與「未實測」；沒有保證式說法；沒有中國用語（激活、信息、默認、優化、緩存、內存、數據、質量都是 0）；指派的 5 個站內連結都在；6 個 H2、1 個表、1 個 callout，結構沒變；圖上的數字 1–6 與 2026 正文都有，SVG 沒改。`_body_length` 2,596。dry-run 只有 `no_summary` 警告（依 brief 不用處理）。

## 我懷疑但沒改的事

- docs.vllm.ai 三頁對 curl 仍回 429。即時頁是用 WebFetch 讀的，經過工具的摘要模型轉述，再和 GitHub main 分支的原始檔逐字對照；沒有用系列規定的 User-Agent 直接拿到即時頁原文。
- 「以整段輸入計」是為了區分每步與整體加上的說明；Pope §1 原文只寫 scales quadratically with input sequence length，而且是引用其他文獻的一般說法，不是 Pope 自己的量測。
- vLLM 段精簡後不再寫資料集名稱，只寫「作者在實驗中重做三種⋯⋯舊做法」；如果編輯要求論文數字一定要寫出完整設定，可以把 ShareGPT、Alpaca 加回去，約多 20 字。

facts_changed: 3
