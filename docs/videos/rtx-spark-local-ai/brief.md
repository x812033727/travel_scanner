# NVIDIA RTX Spark 筆電來了：128 GB 的本機 AI，能取代 ChatGPT 嗎？

slug：`rtx-spark-local-ai`｜旁白繁體中文（台灣）；五語 CC（zh-TW、zh-CN、ja、ko、en），en、ja、ko 配音音軌｜企劃日 2026-09-28｜長度 8–10 分鐘｜季企劃：`docs/ai-video-en-season-01/briefs/04-rtx-spark-local-ai.md`（季排程建議 2026-10-27，機器出貨之後）｜文中的 F1–F20 是事實代號，網址都在「會過期的事實」

## 觀眾

台灣與其他華語觀眾優先：看過 NVIDIA RTX Spark 的新聞（5 月底在台北 GTC 發表，F3；9 月初在 IFA 說十月出貨，F2）、每個月付一個 AI 訂閱、一直聽到「本機 AI」「在自己電腦跑 AI」的人。他們想知道一台最多 128 GB 記憶體（F1）的筆電，能不能讓他們不再付 ChatGPT 這類訂閱。他們會用 ChatGPT，但不知道參數、量化、統一記憶體、上下文各要佔多少記憶體，也分不出 NVIDIA 公布的是哪一種數字。想在本機跑 AI 代理的開發者是第二群。英語、日語、韓語觀眾透過 CC 字幕與配音音軌收看。

中文搜尋：「RTX Spark」「RTX Spark 筆電」「本機 AI」「本地端 LLM」「128GB 可以跑什麼模型」「筆電跑 LLM」「AI PC 值得買嗎」「本機 AI 取代 ChatGPT」；英文搜尋：「rtx spark」「rtx spark local ai」「run llm locally 128gb」「local ai vs chatgpt」「how much ram to run an llm」。

## 觀眾看完能做到的事

- 看到「這台電腦跑得動某某模型」的說法，自己驗算一次：到模型的官方頁面看參數量或檔案大小，用「參數量 × 每個參數的位元組」（16 位元是 2、8 位元是 1、4 位元是 0.5）估出至少要多少記憶體，再跟自己在「工作管理員 → 效能」看到的記憶體、專用 GPU 記憶體比一比，並記得 Windows 自己也要留位置。
- 為本機 AI 花錢之前，先說出自己在隱私、品質、成本、速度裡最在意哪一件，再用「機器多花的錢 ÷ 每月省下的訂閱費」算出要幾個月才回本。

## 站主觀點

套用立場：1、2、4、6

我關心本機 AI，是因為它是一道看得見的界線：資料沒有離開我自己的電腦，這是技術上做到的事，不是條款裡的一句承諾；機器也是一次付清，不是按月、按用量算。我關心的不是一台筆電能不能打贏資料中心。所以這支影片不回答「要不要買」，而是先把算得出來的帳算清楚：一個模型要多少記憶體，用參數量乘上每個參數的位元組就算得出來，128 GB、64 GB、16 GB 各裝得下什麼，觀眾自己就能驗算。算不出來的，我不猜。RTX Spark 十月才出貨，我們手上沒有實機，NVIDIA 也還沒公布它跑語言模型的速度和記憶體頻寬，影片裡只放 NVIDIA 自己的說法，並且標明是廠商說的；價格一律以官網為準。代理在背景自己跑，安全要靠 Windows 真的擋住檔案和網路，不是靠提示詞裡的一句「不要」。最後，新硬體上市不是換工具的理由：如果你的資料可以上雲、你的工作需要最強的模型，每月的訂閱仍然可能比較划算；本機 AI 真正值得的，是那些必須留在家裡、又天天在跑的工作。這些是我的看法，影片裡會明說是我的看法。

## 示範或實算

以下數字都是 2026-09-28 打開官方頁面讀到的；算式是這支影片自己算的，觀眾拿同一個網址就能重算。

**實算一：128 GB 裝得下什麼（主軸）。**選項 A 第 3–4 章、B 第 3–4 章、C 第 4 章；`stats`、`code`、兩張 `table`、`chat`、`stats`。

1. 規則：記憶體 ≈ 參數量 × 每個參數的位元組；16 位元 = 2、8 位元 = 1、4 位元 = 0.5。
2. 用一個模型驗證規則。Llama 3.3 70B Instruct 有 70,553,706,496 個參數（Hugging Face 的 safetensors 統計，https://huggingface.co/api/models/meta-llama/Llama-3.3-70B-Instruct ）。乘 2 是 141.1 GB，官方 BF16 檔案合計正好 141.1 GB（https://huggingface.co/api/models/meta-llama/Llama-3.3-70B-Instruct?blobs=true ）。乘 1 是 70.6 GB，乘 0.5 是 35.3 GB。Ollama 上同一個模型的檔案是 fp16 141GB、q8_0 75GB、q4_K_M 43GB（預設）、q4_0 40GB（https://ollama.com/library/llama3.3/tags ），換算成每個參數 16.0、8.5、4.9、4.5 位元：多出來的是每一小段數字共用的縮放值，所以實際檔案比算式大 6–22%。
3. 六個模型對三種記憶體。檔案大小來自各模型頁與 API 的檔案清單：gpt-oss-20b 13.8 GB、gpt-oss-120b 65.2 GB（https://huggingface.co/api/models/openai/gpt-oss-20b?blobs=true 、https://huggingface.co/api/models/openai/gpt-oss-120b?blobs=true ），DeepSeek-V4-Flash 159.6 GB（https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Flash?blobs=true ）。記憶體規格的 GB 以 1,024³ 位元組計，16／64／128 GB 等於 17.2／68.7／137.4 GB（檔案的算法）。判斷方式：先扣掉 Windows 11 自己的最低需求 4 GB（https://www.microsoft.com/en-us/windows/windows-11-specifications ），檔案小於剩下的就「放得下」，介於剩下的和整個記憶體之間是「太擠」，比整個記憶體還大就「放不下」。這裡只算模型本身，還沒算上下文。

   | 模型（精度） | 檔案 | 16 GB | 64 GB | 128 GB | 出處 |
   | --- | --- | --- | --- | --- | --- |
   | gpt-oss-20b（MXFP4） | 13.8 GB | 太擠 | 放得下 | 放得下 | F11 |
   | Llama 3.3 70B（4 位元 q4_K_M） | 43 GB | 放不下 | 放得下 | 放得下 | F10 |
   | gpt-oss-120b（MXFP4） | 65.2 GB | 放不下 | 太擠 | 放得下 | F11 |
   | Llama 3.3 70B（8 位元 q8_0） | 75 GB | 放不下 | 放不下 | 放得下 | F10 |
   | Llama 3.3 70B（原版 BF16） | 141.1 GB | 放不下 | 放不下 | 放不下 | F9 |
   | DeepSeek-V4-Flash（FP4＋FP8） | 159.6 GB | 放不下 | 放不下 | 放不下 | F14 |

   第一列要一起講 OpenAI 自己的說法：gpt-oss-20b「run within 16GB of memory」（https://huggingface.co/openai/gpt-oss-20b ）。照記憶體的算法，16 GB 的電腦放下它之後只剩約 3.2 GB，所以是「剛好」，不是「寬鬆」；64 GB 那一級放下 gpt-oss-120b 之後剩約 3.3 GB，同樣少於 Windows 的 4 GB。畫面上不要寫「65.2 GB 比 64 GB 大」這種跨單位的比較。
4. 驗算一個常見說法：「128 GB 連 405B 都跑得動」。4,050 億 × 0.5 ＝ 202.5 GB，放不下。2026-09-28 有一篇自稱不是實機評測的 RTX Spark 解說頁這樣寫，同一句還說能跑「Llama 3.1 70B at full precision」，但 700 億參數用 16 位元存就要約 141 GB（Llama 3.3 70B 的原版檔案是 141.1 GB，F9）。我們當天用的搜尋工具，AI 摘要也照抄了這兩句。影片裡只把它當成觀眾的問題來算，不點名網站。
5. 上下文也吃記憶體（KV 快取），算式是：2 × 全注意力層數 × KV 頭數 × 每頭維度 × 2 位元組 × token 數。gpt-oss-120b 的 config.json 有 36 層，一半是只看最近 128 個 token 的滑動視窗層，另一半是全注意力層，8 個 KV 頭，每頭 64 維，最長 131,072 個 token（https://huggingface.co/openai/gpt-oss-120b/raw/main/config.json ）。所以每個 token 要 36,864 位元組，讀滿約 4.83 GB（滑動層只有約 4.7 MB），65.2 ＋ 4.8 ≈ 70 GB。備用例子：Qwen3.8-27B 有 27,781,427,952 個參數，BF16 檔案 55.6 GB，4 位元算式是 13.9 GB；它的 64 層裡每 4 層有 1 層全注意力，共 16 層，4 個 KV 頭，每頭 256 維，最長 262,144 個 token（https://huggingface.co/Qwen/Qwen3.8-27B/raw/main/config.json ）。所以每個 token 要 65,536 位元組，讀滿 17.2 GB，比它 4 位元的權重還大。
6. 一般電腦的對照：Copilot+ PC 的最低記憶體是 16 GB（F16）。電競筆電的顯示卡另有自己的記憶體，GeForce RTX 5060 筆電版是 8 GB，RTX 5090 筆電版是 24 GB（F17）。RTX Spark 最多 128 GB，另一級筆電最多 64 GB（F1）。Windows 為 GPU 能用的系統記憶體設了上限，Microsoft 只說調高了，沒有公布數字（F4）。
7. 可選的對照，站主可刪：NVIDIA 另一台同樣 128 GB 的桌機 DGX Spark，官網寫能跑「AI models up to 200 billion parameters」（F15）。2,000 億 × 0.5 ＝ 100 GB，剛好是這條算式。畫面上要寫清楚那不是 RTX Spark。

**實算二：訂閱和自己的機器怎麼比。**A 第 7 章、B 第 6 章、C 第 6 章；`compare`、`code`、`stats`。

- Claude Pro 月繳 20 美元，年繳每月 17 美元（一次付 200 美元），用量每 5 小時滾動重置，付費方案另有每週上限（https://claude.com/pricing ）。ChatGPT Plus 以官網為準：chatgpt.com 與 openai.com 的價格頁今天都回 403（F18）。RTX Spark 筆電與桌機的價格以官網為準，NVIDIA 與 OEM 頁面都還沒有列（F7）。
- 回本月數 ＝ 機器多花的錢 ÷ 每月省下的訂閱費。每多 1,000 美元 ÷ 20 美元 ＝ 50 個月，約 4.2 年；用年繳的 17 美元算，約 59 個月。
- 電費上限 ＝ 晶片 TDP × 小時 × 天 ÷ 1,000 × 你電費單上的每度價格。NVIDIA 產品頁的 TDP 是筆電 45–80 W、桌機 140 W（F1）：桌機 140 W × 24 小時 × 30 天 ＝ 100.8 度；筆電 80 W × 8 小時 × 30 天 ＝ 19.2 度。TDP 是晶片的設計功耗上限，不是整台電腦在插座端的實測；每度電價以台電官網或自己的帳單為準（F20）。

**實算三：同一台機器上，MoE 模型為什麼可能快很多（只講比例）。**A 第 5 章、B 第 5 章、C 第 5 章；`stats`。

- Llama 3.3 70B 不是 MoE，每產生一個 token 要動到全部約 705.5 億個參數（F9）。gpt-oss-120b 總共 1,170 億個參數，每個 token 只動 51 億個（「117B parameters with 5.1B active parameters」，F11）。兩者差約 14 倍。只用來說明「每個字要搬的資料少很多」，不換算成每秒幾個 token：實際速度還要看精度、軟體和記憶體頻寬，RTX Spark 的頻寬 NVIDIA 沒有公布（F1）。

**可選的實機示範（站主決定，沒做就不放）：**站主在自己的一般電腦（不是 RTX Spark，也不需要 NVIDIA 顯示卡）用 Ollama 跑 gpt-oss-20b，用一個固定的提示詞，記下機型、處理器、記憶體、作業系統、Ollama 版本、模型標籤和 `--verbose` 印出的 eval rate，放在一張 `stats`，畫面標明硬體，不拿去和 RTX Spark 比。記憶體少於 16 GB 的電腦不做。

## 大綱

### 選項 A：從 NVIDIA 的一句話算回來（推薦）
一行說明：開場並排兩個數字：NVIDIA 說能跑 1,200 億參數，但 700 億參數的 Llama 3.3 原版 141 GB 卻裝不下。接著教一條記憶體算式，再用它看速度、代理和訂閱。和從觀眾自己電腦往上爬的 B、從隱私切入的 C 相比，A 最能接住「RTX Spark」的上市搜尋，算式從頭到尾都是主軸。
開場鉤子（口播）：「NVIDIA 說，十月上市的 RTX Spark 筆電，能跑 1,200 億參數的模型。可是 700 億參數的 Llama 3.3，原版就有 141 GB，這台筆電裝不下。這兩句不衝突，差在一個你自己算得出來的數字。這集就用它，算出這台筆電裝得下什麼。再看它缺了哪個數字、能不能取代你的訂閱。」

鉤子裡的數字：1,200 億（F3）、141 GB（F9、F10）、最多 128 GB（F1）、十月（F2）。鉤子約 29.5 秒（工具的估法），畫面換 4 次：`title` → `big` → `chat` → `bullets`，`bullets` 再多一次逐條出現。

| # | 章節（觀眾看到的名稱） | 秒 | 畫面狀態 | 場景（`template`：呈現內容） |
| --- | --- | --- | --- | --- |
| 1 | 128 GB 的 AI 筆電，裝得下什麼？（What can a 128 GB AI laptop hold?） | 30 | 5 | `title`：問題當標題，標籤「NVIDIA RTX Spark」；`big`：「141 GB」，上面寫「Llama 3.3 70B 原版檔案」，下面寫「RTX Spark 最多 128 GB」；`chat`：觀眾的疑問「能跑 1,200 億，卻裝不下 700 億？」；`bullets`：這集要算的三件事，分兩句出完 |
| 2 | RTX Spark 是什麼：NVIDIA 公布的規格（RTX Spark on one spec sheet） | 60 | 8 | `table`：兩級筆電與桌機的 GPU 核心、CPU 核心、記憶體、功耗上限（4 列逐列出現；不寫官網兩欄重複的型號）[F1]；`compare`：一般筆電（系統記憶體，Copilot+ PC 最低 16 GB；顯示卡另有 8 GB，例如 RTX 5060 筆電版）vs 統一記憶體（CPU 與 GPU 共用，最多 128 GB，GPU 能用多少由 Windows 設上限，沒有公布數字）[F16][F17][F4]；`quote`：新聞稿原文 "run 120-billion-parameter large language models with 1 million tokens context"，下一句出中文翻譯 [F3]。可以加一句：5 月底在台北 GTC 發表，CPU 是和聯發科合作設計的 Arm 晶片，x86 程式靠 Prism 模擬 [F3][F4] |
| 3 | 一個 AI 模型要多少記憶體？一條算式（How much memory does a model need?） | 95 | 10 | **實算一**。`stats`：每個參數佔 2／1／0.5 位元組（逐一出現）；`code`：705.5 億 × 2／× 1／× 0.5 ＝ 141／71／35 GB（旁白兩句內講完）[F9]；`table`：算式 vs Ollama 上的實際檔案，141 對 141、71 對 75、35 對 40–43 GB（3 列逐列出現，標亮第 3 列）[F10]；`big`：「檔案多大，記憶體至少就要多大」；`quote`：DGX Spark 頁 "AI models up to 200 billion parameters" 加翻譯，旁白算 2,000 億 × 0.5 ＝ 100 GB（可刪）[F15] |
| 4 | 128 GB、64 GB、16 GB 各跑得動哪些模型（What fits in 128, 64 and 16 GB） | 110 | 13 | **實算一的後半**。`table`：六個模型對上檔案、16 GB、64 GB、128 GB，格子寫「放得下／太擠／放不下」，不用符號（6 列逐列出現）[F9–F14]；`chat`：「聽說 128 GB 連 405B 都跑得動？」→「4,050 億 × 0.5，兩百多 GB，放不下。」（2 則）；`quote`：PAIR 常見問題 "PAIR doesn't combine them into one virtual GPU" 加翻譯：家裡兩台不會變成一顆 256 GB 的 GPU [F6]；`code`：上下文的記憶體，gpt-oss-120b 每個 token 36,864 位元組 × 131,072 ≈ 4.8 GB，65.2 ＋ 4.8 ≈ 70 GB [F13]；`stats`：64 GB 那一級放下 gpt-oss-120b 後剩「不到 4 GB」vs Windows 11 最低需求「4 GB」（2 個逐一出現）[F1][F11][F16] |
| 5 | RTX Spark 跑多快？NVIDIA 還沒說的數字（How fast is it? The number NVIDIA hasn't given） | 75 | 9 | `quote`：產品頁 "Up to 1 Petaflop FP4 AI Performance"，翻譯「最高每秒一千兆次 4 位元運算」[F1]；`bullets`：有公布的（算力、記憶體容量、功耗）／沒公布的（記憶體頻寬、每秒幾個 token）／還沒有的（出貨後的獨立評測）[F1][F8]；`compare`：讀進一大段文件主要看算力 vs 一個字一個字回答主要看記憶體頻寬（這句今天沒有官方頁面可引；撰稿日找一份 NVIDIA 或 llama.cpp 的技術文件當出處，找不到就刪這張）；`stats`：**實算三**，每個 token 動到的參數，Llama 3.3 70B 約 705.5 億 vs gpt-oss-120b 51 億（註明是同一台機器上的差距，不是速度實測）[F9][F11] |
| 6 | AI 代理在背景跑：Windows 加了哪道牆（Agents in the background: the wall Windows adds） | 45 | 6 | `quote`：NVIDIA 部落格 "agents that run safely in the background under OS level control" 加翻譯 [F2]；`bullets`：檔案和網路只能碰政策允許的（Microsoft Execution Containers，MXC）／代理用自己的身分，紀錄分得開／現況是早期預覽，很多功能先在 Windows Insider 版 [F5]；`cta`：三道牆的真實示範在第 1 支影片（`openai-agents-broke-in`） |
| 7 | AI 訂閱 vs 自己的電腦：回本要幾個月（Subscription vs your own machine: the payback math） | 75 | 7 | **實算二**。`compare`：雲端訂閱（每月付；Claude Pro 月繳 20 美元，ChatGPT 以官網為準；用量每 5 小時重置）vs 自己的機器（一次付清，RTX Spark 價格以官網為準，另外付電費）[F18][F7]；`code`：回本月數的算式，每多 1,000 美元 ÷ 20 美元 ＝ 50 個月；`stats`：電費上限，桌機 100.8 度／筆電 19.2 度，乘上你自己的每度電價 [F1][F20]；`chat`：觀眾「那我該買嗎？」→「先說你最在意哪一件事。」 |
| 8 | 本機 AI 能取代 ChatGPT 嗎？（Can local AI replace ChatGPT?） | 45 | 5 | `table`：你最在意的事 → 比較適合的做法：隱私 → 本機（資料不離開電腦）；品質 → 雲端（各家最新的旗艦模型只在雲端）；成本 → 先算回本月數；速度 → 等出貨後的評測（4 列逐列出現）；`outro`：「要留在家的工作，本機做得到；要最強的模型，還在雲端」，加上下一步 |

實算在第 3–4 章（記憶體）、第 5 章（每個 token 動到的參數）、第 7 章（回本月數與電費）。

結尾的下一步：「打開工作管理員的『效能』，記下你的記憶體和專用 GPU 記憶體，拿一個你想跑的模型，用今天的算式算一次。」

總長約 535 秒（8.9 分鐘），中文旁白約 2,000–2,200 字（以每分鐘 250 字計）。每一章平均每個畫面狀態 5.6–10.7 秒。`code` 沒有逐條出現，旁白限兩句，不超過 12 秒。和前四支的版型順序相似度 40–47%（用 lint 的算法算）；不以 `steps` 的「三個問題」收尾。

### 選項 B：從你的電腦爬到 128 GB
一行說明：從觀眾自己的電腦開始，一格一格往上爬（8、16、24、64、128 GB），RTX Spark 到第 5 章才出場，代理只帶一句。比 A 更像教學，也更早教觀眾看自己的記憶體；上市當週的搜尋流量比 A 吃虧，但三個月後還有人在搜「我的電腦能跑什麼模型」。
開場鉤子（口播）：「先別急著看新筆電，你現在這台電腦，說不定已經跑得動 AI。OpenAI 說，它的開放權重模型 gpt-oss-20b，16 GB 記憶體就能跑。那 NVIDIA 的 128 GB 筆電，能多跑什麼？這集從你的電腦開始，一格一格往上爬。每一格都用同一條算式，算到 128 GB 為止。」

鉤子裡的數字：16 GB（F11）、128 GB（F1）。約 27.6 秒，畫面換 4 次：`title` → `big` → `chat` → `stats`，`stats` 再多一次逐條出現。

| # | 章節 | 秒 | 畫面狀態 | 場景 |
| --- | --- | --- | --- | --- |
| 1 | 你的電腦跑得動 AI 嗎？（Can your computer run AI?） | 28 | 5 | `title`；`big`：「16 GB」，上面寫「OpenAI：gpt-oss-20b 只要」，下面寫「Copilot+ PC 的最低記憶體也是 16 GB」[F11][F16]；`chat`：「那 128 GB 的筆電能多跑什麼？」；`stats`：16／64／128 GB 三格，分兩句出完 [F1] |
| 2 | 先看你的電腦有多少記憶體（Check how much memory you have） | 55 | 6 | `steps`：工作管理員 → 效能 → 記憶體與 GPU 的「專用 GPU 記憶體」（3 步；介面字樣在撰稿日核對，F19）；`compare`：系統記憶體（CPU 用，Copilot+ PC 最低 16 GB）vs 專用 GPU 記憶體（顯示卡自己的，RTX 5060 筆電版 8 GB、RTX 5090 筆電版 24 GB）[F16][F17]；`big`：「模型要整個放進去，才跑得順」 |
| 3 | 一條算式：參數量 × 位元組（One formula: parameters × bytes） | 85 | 8 | **實算一**。`stats`：2／1／0.5 位元組；`code`：Llama 3.3 70B × 2／1／0.5 [F9]；`table`：算式 vs Ollama 檔案（3 列）[F10]；`big`：「檔案多大，記憶體至少就要多大」 |
| 4 | 記憶體階梯：8、16、24、64、128 GB 各裝得下什麼（The memory ladder） | 140 | 14 | **實算一的後半**。`table`：5 格階梯。8 GB 顯示卡放不下 gpt-oss-20b；16 GB 對 gpt-oss-20b 太擠，雖然 OpenAI 說能跑；24 GB 顯示卡放得下 gpt-oss-20b；64 GB 放得下 Llama 3.3 70B 4 位元，gpt-oss-120b 太擠；128 GB 放得下 gpt-oss-120b 和 Llama 3.3 70B 8 位元 [F1][F10][F11][F16][F17]；`quote`：NVIDIA 部落格說 OpenClaw 的 Windows App 要 "any RTX GPU with at least 24GB of VRAM"，加翻譯 [F2]；`table`：128 GB 也放不下的（Llama 3.3 70B 原版 141 GB、DeepSeek-V4-Flash 160 GB，2 列）[F9][F14]；`chat`：405B 的說法 → 算式回答（2 則）；`code`：上下文 4.8 GB [F13]；`stats`：64 GB 放下 gpt-oss-120b 後剩不到 4 GB vs Windows 11 最低 4 GB [F16] |
| 5 | RTX Spark 在第幾格？（Where RTX Spark sits on the ladder） | 80 | 11 | `table`：規格 4 列 [F1]；`quote`：120B 那句加翻譯 [F3]；`bullets`：有公布／沒公布／還沒有獨立評測 [F1][F8]；`stats`：**實算三**，每個 token 動到的參數 705.5 億 vs 51 億 [F9][F11] |
| 6 | 多爬這幾格值不值得：帳怎麼算（Is the climb worth it? The math） | 75 | 8 | **實算二**。`compare`：訂閱 vs 自己的機器 [F18][F7]；`code`：回本月數；`stats`：電費上限 [F1]；`big`：「每多 1,000 美元，等於 50 個月的 20 美元訂閱」；`chat`：「那我要爬到哪一格？」→「看你最在意哪一件事。」 |
| 7 | 你需要爬到 128 GB 嗎？（Do you need 128 GB?） | 45 | 5 | `bullets`：隱私、品質、成本、速度各自對到本機還是雲端（4 條）；`outro` |

實算在第 3–4 章（記憶體）、第 5 章（每個 token 動到的參數）、第 6 章（錢）。結尾的下一步：「拿你剛剛記下的記憶體，套今天的算式，算一個你想跑的模型。」總長約 510 秒（8.5 分鐘），中文旁白約 1,900–2,100 字；和前四支的相似度 46–50%。

### 選項 C：資料留在家的代價
一行說明：先講資料走哪條路、代理在背景跑要靠什麼牆（立場 4），再算「把 AI 留在家」要付出的記憶體、速度和錢。A、B 以算式為主軸，C 以界線為主軸，把代理那一章提前到第 3 章；適合在意隱私的觀眾，但對「RTX Spark」的搜尋流量最弱。
開場鉤子（口播）：「你問 ChatGPT 的每一句話，都要先離開你的電腦，才拿得到回答。NVIDIA 說，十月開始有一種筆電，讓 AI 留在你家裡跑。資料不用出門，但模型要塞得進這台電腦。代價寫在一個數字上：記憶體。這集算給你看，留在家要放棄多少能力、要付多少錢，以及哪些工作值得。」

鉤子裡的數字：十月（F2）。約 29.3 秒，畫面換 5 次：`title` → `compare`（左右各出一次）→ `big` → `bullets`，`bullets` 再多一次逐條出現。

| # | 章節 | 秒 | 畫面狀態 | 場景 |
| --- | --- | --- | --- | --- |
| 1 | 你問 AI 的話，去了哪裡？（Where do your prompts go?） | 29 | 6 | `title`；`compare`：雲端（送到廠商的伺服器處理）vs 本機（留在你的電腦），兩句各出一邊；`big`：「記憶體」，上面寫「留在家的代價」；`bullets`：這集要算的三件事，分兩句出完 |
| 2 | 雲端和本機：資料各走哪條路（Cloud vs local: the data path） | 80 | 8 | `steps`：雲端的路是你的電腦 → 網路 → 廠商的伺服器 → 回答（4 步）；`chat`：「本機就完全不用連網嗎？」→「以 NVIDIA PAIR 為例：運作時不用網路，下載模型才要。」[F6]；`quote`：新聞稿說 OpenShell 能 "disguise personal information in queries sent to cloud models"，加翻譯，標明是 NVIDIA 的說法 [F3] |
| 3 | AI 代理在背景跑：牆要是真的（Agents in the background need real walls） | 70 | 8 | `quote`："under OS level control" 那句加翻譯 [F2]；`bullets`：MXC 限制檔案與網路／代理有自己的身分／早期預覽 [F5]；`compare`：提示詞裡的「不要」vs 作業系統真的擋住的權限；`cta`：第 1 支影片 |
| 4 | 留在家的代價：模型得塞進記憶體（The price of staying home: memory） | 130 | 16 | **實算一**。`stats`：2／1／0.5 位元組；`code`：Llama 3.3 70B [F9]；`table`：算式 vs Ollama（3 列）[F10]；`table`：16／64／128 GB 裝得下什麼（6 列）[F9–F14]；`chat`：405B 的說法；`code`：上下文 4.8 GB [F13] |
| 5 | 速度和品質：還沒有人量過（Speed and quality: nobody has measured it yet） | 70 | 8 | `quote`："Up to 1 Petaflop FP4 AI Performance" 加翻譯 [F1]；`bullets`：有公布／沒公布／還沒有評測 [F8]；`stats`：**實算三**，705.5 億 vs 51 億 [F9][F11]；`big`：「夠不夠用，拿你自己的工作試」 |
| 6 | 一次付清還是每月付：帳怎麼算（Pay once or pay monthly） | 75 | 7 | **實算二**。`compare`、`code`、`stats`，內容同 A 第 7 章；`chat`：「那哪些工作值得留在家？」 |
| 7 | 哪些工作值得留在家跑？（Which work is worth keeping at home?） | 50 | 5 | `table`：工作類型對到本機或雲端。含個資或公司機密的文件 → 本機；要最新旗艦模型的難題 → 雲端；天天大量跑的同一件事 → 算回本月數；偶爾用 → 訂閱（4 列）；`outro` |

實算在第 4 章（記憶體）、第 5 章（每個 token 動到的參數）、第 6 章（錢）。結尾的下一步：「打開工作管理員的『效能』，記下你的記憶體，算一次你想留在家跑的那個模型裝不裝得下。」總長約 505 秒（8.4 分鐘），中文旁白約 1,900–2,100 字；和前四支的相似度 41–46%。

**推薦 A 的理由：**季企劃的公式是「新聞當鉤子、常青問題當標題、可複算的實算當骨幹」，A 最貼近。開場兩個數字都來自官方頁面，看起來互相矛盾，其實不衝突，而且觀眾會在第 3 章親手算出答案。「NVIDIA 公布了什麼、還沒公布什麼」自成一章，正好是我們沒有實機時最誠實的寫法。

## 會過期的事實

撰稿日（十月出貨後）每一列都重開一次；數字變了，連同用到它的鉤子、表格和算式一起改。

| 代號 | 事實（2026-09-28 官方頁面的寫法） | 撰稿日重查的網址 |
| --- | --- | --- |
| F1 | RTX Spark 規格：「Up to 1 Petaflop FP4 AI Performance」；GPU 最多 6,144 核心、CPU 最多 20 核心、最多 128 GB 統一記憶體。筆電有兩種：6,144 核心 GPU、20 核心 CPU、最多 128 GB LPDDR5X，以及 5,120 核心、18 核心、最多 64 GB，兩欄都標「RTX Spark N1X」。筆電 TDP 45–80 W，桌機 140 W；桌機寫「Built to run personal AI agents 24/7」。頁面沒有記憶體頻寬，也沒有價格。列出的六款筆電：ASUS ProArt P16、Dell XPS 16、HP OmniBook Ultra 16、Lenovo Yoga Pro 9n、Microsoft Surface Laptop Ultra、MSI Prestige N16 Flip AI+ | https://www.nvidia.com/en-us/products/rtx-spark/ |
| F2 | IFA 部落格（2026-09-03）：「NVIDIA RTX Spark arrives in October」、「newly announced designs join the existing six OEMs shipping in October」；Lenovo Yoga Pro 9n 與 Yoga 9n，Acer 的桌機概念機；「Paired with the new Windows Agent framework, it enables agents that run safely in the background under OS level control」。「Up to 1.9x faster local inference」量在 GeForce RTX 5090，不是 RTX Spark。OpenClaw 的 Windows App 與 Perplexity Portable Computer 要「at least 24GB」VRAM。DeepSeek v4 Flash「can run locally on 2x DGX Spark cluster and DGX Station」 | https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/ |
| F3 | NVIDIA 新聞稿（2026-05-31，GTC Taipei）：「run 120-billion-parameter large language models with 1 million tokens context」；6,144 CUDA 核心、第五代 Tensor 核心支援 FP4、20 核心 Grace CPU，CPU 與 MediaTek 合作設計。OpenShell：使用者定義代理能做什麼，依隱私政策把查詢導向本機模型，並能「disguise personal information in queries sent to cloud models」。上市時間寫「this fall」，廠商是 ASUS、Dell、HP、Lenovo、Microsoft Surface、MSI，Acer 與 GIGABYTE 之後。「Features, pricing, availability and specifications are subject to change without notice」 | https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark |
| F4 | Microsoft Windows Experience Blog（2026-05-31）：最多 20 個 Arm 架構核心；x86 程式由 Prism 模擬；「a new higher, smarter limit on total system memory accessible by the GPU」，沒有數字；「These PCs will join the Copilot+ PC category」；「Beginning this Fall」 | https://blogs.windows.com/windowsexperience/2026/05/31/introducing-a-powerful-new-chapter-for-windows-pcs-accelerated-by-nvidia-rtx-spark/ |
| F5 | Microsoft Windows Developer Blog（2026-06-02）：Microsoft Execution Containers（MXC）SDK 是「early preview」，開發者定限制、Windows 在執行時強制。process isolation 限制政策以外的檔案與網路網域；代理用獨立帳號，身分是本機 ID 或 Entra。「Our initial release will support non-interactive sessions」；「NVIDIA brings OpenShell to Windows, built on MXC」；「Many of these capabilities are available today in Windows Insider builds」 | https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/ |
| F6 | NVIDIA PAIR：beta；支援 Ollama、LM Studio；GeForce RTX 20 系列以後、DGX Spark、Mac M4 以後；記憶體 8 GB 以上；網路「None required for operation／Required for model download」；「PAIR doesn't combine them into one virtual GPU」 | https://www.nvidia.com/en-us/ai-on-rtx/personal-ai-router/ |
| F7 | 價格：NVIDIA 與 OEM 頁面都沒有列，以官網為準。Surface Laptop Ultra 寫「Up to 128GB unified memory」，FCC 尚未核准；Surface RTX Spark Dev Box 寫「Pre-release product」；Dell XPS 16 寫「up to 128GB of unified memory」 | https://www.microsoft.com/en-us/surface/devices/surface-laptop-ultra 、https://www.microsoft.com/en-us/surface/devices/surface-rtx-spark-dev-box 、https://www.dell.com/en-us/blog/dell-and-nvidia-bring-serious-performance-to-creators/ ；其他 OEM 從 F1 的機型清單找 |
| F8 | 獨立評測：2026-09-28 找不到任何 RTX Spark 實機的語言模型速度測試。Tom's Hardware（2026-08-09）報導的是量產前的 Geekbench CPU 分數，不是 AI 速度。一篇 9/16 更新的 RTX Spark 解說頁自稱「not … a hands-on review」，頁中「70B 每秒 30 個以上 token」是轉述，不用。出貨後重搜，只用有名有姓、當天打開過的評測，並寫明測試者、日期、硬體 | 撰稿日重搜；參考 https://www.tomshardware.com/pc-components/cpus/two-variants-of-nvidias-rtx-spark-show-up-on-geekbench-revealing-a-cut-down-18-core-model-full-20-core-beats-most-x86-mobile-chips-across-multi-core-and-single-core-tests |
| F9 | Llama 3.3 70B Instruct：70,553,706,496 個參數（BF16），官方檔案合計 141.1 GB；下載要申請（gated），Llama 3.3 授權；它的 config.json 要登入才看得到，所以上下文的算法不用它 | https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct 、https://huggingface.co/api/models/meta-llama/Llama-3.3-70B-Instruct?blobs=true |
| F10 | Ollama 的 llama3.3：fp16 141GB、q8_0 75GB、q6_K 58GB、q5_K_M 50GB、q4_K_M 43GB（預設）、q4_0 40GB、q3_K_M 34GB、q2_K 26GB；128K context window | https://ollama.com/library/llama3.3/tags |
| F11 | gpt-oss：「gpt-oss-120b … fit into a single 80GB GPU … (117B parameters with 5.1B active parameters)」；「gpt-oss-20b … (21B parameters with 3.6B active parameters)」、「run within 16GB of memory」；Apache 2.0；檔案 65.2 GB 與 13.8 GB | https://huggingface.co/openai/gpt-oss-120b 、https://huggingface.co/openai/gpt-oss-20b （檔案大小：網址後加 `?blobs=true` 的 API） |
| F12 | Ollama 的 gpt-oss：20b 14GB、120b 65GB，128K context window；MXFP4 是「4.25 bits per parameter」 | https://ollama.com/library/gpt-oss |
| F13 | 上下文的算法。gpt-oss-120b 的 config.json：36 層，滑動視窗 128 與全注意力交替，8 個 KV 頭，head_dim 64，max_position_embeddings 131,072。Qwen3.8-27B：27,781,427,952 個參數，BF16 檔案 55.6 GB；64 層，每 4 層一層全注意力，4 個 KV 頭，head_dim 256，最長 262,144 | https://huggingface.co/openai/gpt-oss-120b/raw/main/config.json 、https://huggingface.co/Qwen/Qwen3.8-27B/raw/main/config.json 、https://huggingface.co/Qwen/Qwen3.8-27B |
| F14 | DeepSeek-V4-Flash：284B 參數（13B activated），1M context，「FP4 + FP8 Mixed」，MIT；檔案 159.6 GB | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash |
| F15 | DGX Spark（可選的對照）：128 GB；「AI models up to 200 billion parameters」；273 GB/s；「Up to 1 PFLOP FP4」的註腳寫「Theoretical FP4 TOPS using the sparsity feature」；最多四台用 ConnectX 串起來跑 7,000 億參數。RTX Spark 的頁面沒有這個註腳，不要把它套過去；DGX Spark 能串機、PAIR 不能，兩者別混在一起講 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ |
| F16 | Windows 11 最低記憶體 4 GB；Copilot+ PC 最低「16 GB DDR5/LPDDR5」、NPU 40+ TOPS | https://www.microsoft.com/en-us/windows/windows-11-specifications |
| F17 | GeForce RTX 50 系列筆電 GPU 的記憶體：5090 是 24 GB、5080 是 16 GB、5070 Ti 是 12 GB、5070 是 12 GB 或 8 GB、5060 是 8 GB、5050 是 8 GB | https://www.nvidia.com/en-us/geforce/laptops/50-series/ |
| F18 | 訂閱：Claude Pro 月繳 20 美元，年繳每月 17 美元（一次付 200 美元），Max 每月 100 美元起；用量每 5 小時滾動重置，付費方案另有每週上限。ChatGPT Plus 以官網為準：chatgpt.com/pricing、openai.com/chatgpt/pricing、help.openai.com 對我們的抓取都回 403，要由真人打開 | https://claude.com/pricing 、https://chatgpt.com/pricing/ |
| F19 | Windows 繁中介面字樣：工作管理員 → 效能 → 記憶體，以及 GPU 的「專用 GPU 記憶體」。Microsoft Learn 的繁中頁面是機器翻譯（寫成「任務管理員」），撰稿日在繁中 Windows 11 上實際看一次再定稿 | https://learn.microsoft.com/zh-tw/troubleshoot/windows-client/performance/gpu-process-memory-counters-report-wrong-value |
| F20 | 每度電價：用觀眾自己的電費單；台電費率以台電官網為準（今天沒有查，所以影片不寫數字） | https://www.taipower.com.tw/ |

另外兩件撰稿日要看的：影片預計十月底上架，鉤子的「十月上市」屆時可能要改成「已經上市」；NVIDIA 若公布了 RTX Spark 的記憶體頻寬或每秒 token 數，第 5 章改放 NVIDIA 的數字並標明是廠商公布的。

## 素材

- 官方頁面的文字：F1–F7、F15–F18。`quote` 只放短句原文，加中文翻譯與出處、日期，不轉載整頁。
- 模型與檔案資料：Hugging Face 的模型頁、API 與 config.json（F9、F11、F13、F14），以及 Ollama 模型庫（F10、F12）。只引用數字，不散布任何模型檔。授權：gpt-oss 與 Qwen3.8-27B 是 Apache 2.0，DeepSeek-V4-Flash 是 MIT，Llama 3.3 是 Llama 3.3 授權。
- 圖片：不用。NVIDIA 新聞稿附的產品圖（iprsoftwaremedia.com 上的 nvidia-rtx-spark.png）、OEM 產品照、任何公司的 Logo 都是別人的素材。縮圖只放文字，沿用季企劃的方向（例如大字「128 GB」、小字「裝得下什麼」）。
- 可選的原創圖（站主決定）：為這支影片畫一張 SVG 記憶體長條圖，16／64／128 GB 對上六個模型的檔案大小，放在 `docs/videos/rtx-spark-local-ai/memory-bars.svg`，是頻道自己的作品。做了就在第 4 章用 `diagram` 取代一張 `table`；不做就維持 `table`。
- 可選的實機紀錄（站主決定）：見「示範或實算」最後一段，紀錄放 `docs/videos/rtx-spark-local-ai/demo-log.md`。

## 不做的事

- 不宣稱測過 RTX Spark。畫面和旁白不出現任何 RTX Spark 的每秒 token 數，除非是 NVIDIA 自己公布的（標明是廠商說的），或出貨後有名有姓、撰稿當天打開過的獨立評測。網路上轉述的速度（例如「70B 每秒 30 個以上 token」）不用。
- 不拿 DGX Spark 的實測數字代替 RTX Spark；不用 DGX Spark 的註腳解讀 RTX Spark 的 1 petaflop。
- 不給購買建議，不推薦特定筆電，不比較 OEM 機型；不談 NVIDIA、聯發科或任何公司的股價、財報與投資（立場 7）。
- 不做遊戲、影音剪輯與創作軟體的效能。
- 不重講第 1 支影片的三道牆示範，只放一張 `cta`；不用「三個問題」的 `steps` 收尾，前三支都這樣收過。
- 不點名寫錯算式的網站或作者；405B 的說法只當成觀眾的問題來算。
- 不放產品照片、Logo、新聞稿圖片或任何人的影像；新聞稿裡高層的引言不用，也不出現任何人名。
- 不評論雲端廠商怎麼處理資料，不做法律解讀；資料條款以各家官網為準。
- 不示範需要 NVIDIA 顯示卡的本機執行。要實測，只在站主自己的一般電腦上做，並標明硬體。
- 旁白不說「經查證」「根據官方文件」這類話；出處放在畫面的 `quote` 與說明欄。
