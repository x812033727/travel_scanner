# 查核紀錄 1：ai-term-local-inference

查核者：獨立查核（非撰稿者）。查核日 2026-10-03。依 `batch-03/VERIFY.md`、`batch-03/brief.md`（含 batch-02 brief 與它指定的文件）、`catalogue.json` 的指派逐條核對。
抓頁一律 `curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。作者的 notes.md／research.json 只當線索，每條都回到一手來源重讀。

## 修改

- 「Google 的 Android 繁中開發者文件也寫「在本機執行」」→「Google 的 Android 開發者文件繁中版（頁面註明由 AI 翻譯）也寫「在本機執行」」｜這一頁的頁首寫「Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯」，是機器翻譯，不是人工在地化。原句拿它當台灣用語的依據，會讓人以為是 Google 的正式譯名。另外，sources 該筆標題也補上「Google 以 AI 翻譯」｜https://developer.android.com/ai/gemini-nano?hl=zh-tw
- 「…注意力頭數、每個頭的維度與層數，所以會隨上下文長度線性增加。」→ 後面補「同一份指南也指出，讓多個頭共用 key 與 value 的設計（MQA、GQA）能大幅縮小它。」｜Hugging Face 指南給的公式是每個頭各存一份 key／value 的算法，同一節緊接著（§3.2.2、§3.2.3）就說 MQA 只存 1 組、GQA 存 n < n_head 組，能大幅降低 KV 快取用量。只寫公式、不寫這一點，會把標準多頭注意力的算法當成所有模型的通則｜https://huggingface.co/docs/transformers/en/llm_tutorial_optimization
- （措辭，不計入事實修改）「Foundry Local 隨 App 安裝」→「Foundry Local 則不是系統內建，而是隨 App 安裝」｜它放在「作業系統內建的裝置端模型」一節，原句容易被讀成 Windows 內建。Microsoft 的說法是「your application ships with」，並支援 Windows、macOS 與 Linux｜https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local

pack.json 改完後，同目錄的 notes.md 與 research.json 已同步：補了查核紀錄，修正「整份放進顯示記憶體通常最快」的來源對應，`running_text_characters` 依 `_body_length` 實算從 2594 改成 2659。dry-run 通過，只有預期的 `no_summary` 警告。

## 查過、沒問題的主要主張

- llama.cpp README（raw.githubusercontent.com 200）：目標是在各種硬體上做 LLM 推論，「locally and in the cloud」；支援 1.5、2、3、4、5、6、8 位元整數量化，用來加快推論、降低記憶體用量；CPU＋GPU 混合推論可以部分加速超過顯示記憶體總量的模型。
- Ollama FAQ（docs.ollama.com/faq 200，GitHub 上的 faq.mdx 對照一致）：
  - 本機執行時看不到提示詞；用雲端託管模型時，由他們的服務處理提示詞與回答。
  - 用 `~/.ollama/server.json` 的 `disable_ollama_cloud` 或 `OLLAMA_NO_CLOUD=1` 關閉雲端功能，重新啟動後生效，之後不能用雲端模型與網路搜尋。
  - 預設綁定 127.0.0.1 的 11434 埠。
  - 2K 上下文配 4 個並行請求等於 8K 上下文。
  - `ollama ps` 會顯示 CPU／GPU 比例。
  - macOS 與 Windows 會自動下載更新。
- Hugging Face 指南（200）：以 bfloat16／float16 載入時，每十億參數約需 2 GB 顯示記憶體；KV cache 的數值個數是 2 × 序列長度 × 頭數 × 每頭維度 × 層數，記憶體隨 token 數線性增加；4 位元量化的結果實務上常與 8 位元或 bfloat16 不同。正文「代價是精度可能下降」有這一條支持。示例換算（80 億參數 → 16 GB → 4 位元約 4 GB）算術正確，正文也標了「示例換算」和「這只是下限」。
- Apple 開發者文件（各頁的 /tutorials/data/….json，200）：
  - 框架提供 Apple Intelligence 的裝置端模型與私密雲端運算模型。
  - 可用與否取決於裝置與地區是否支援 Apple Intelligence，開啟 Apple Intelligence 後模型要時間下載。
  - SystemLanguageModel 隨例行作業系統更新。
  - 改一行程式（`LanguageModelSession(model: PrivateCloudComputeLanguageModel())`）就能走私密雲端運算，換得較大的上下文與較強的推理（reasoning），但需要網路連線。
  - 資料超出上下文視窗時，建議分段處理再合併。
- Apple 支援繁中頁（200，英文版對照一致）：
  - Apple Intelligence 會先分析請求能否在裝置上處理，較複雜的可使用私密雲端運算。
  - 路徑是「設定」→「隱私權與安全性」→「Apple Intelligence 報告」，期間可選過去 15 分鐘（預設）或過去 7 天，輸出的是送往私密雲端運算的要求。
- Android Gemini Nano 英文頁（200，Last updated 2026-09-08）：
  - Gemini Nano 在 AICore 系統服務裡執行。
  - AICore 沒有直接的網際網路存取，包括模型下載在內的連線，都經由開放原始碼的 Private Compute Services 轉送。
  - 每個請求彼此隔離，處理後不保存輸入與輸出。
  - 省掉網路延遲，但推論速度取決於裝置硬體。這一條支持表格的「速度」列。
- Microsoft Learn（兩頁皆 200）：
  - Foundry Local 的提示詞與輸出在本機處理；仍會為下載模型與執行元件連網；使用者回報問題時可選擇分享紀錄檔；診斷收集依條款。
  - 沒有每個 token 的費用；模型首次使用時下載並快取，之後可離線推論；啟動時可能更新模型目錄。
  - Windows AI APIs 需要配備 NPU 的 Copilot+ PC，資料在裝置上處理，輸入不送往 Microsoft 伺服器。
- 系列規矩：
  - 沒有顯示卡型號、價格、跑分、排行榜，也沒有模型的上下文 token 數。Gemini Nano 是指派建議來源點名的系統模型。
  - 示例一節標了「示例，未實測」，沒有寫成觀察到的結果。
  - 推論（inference）與推理（reasoning）第一次出現都附了英文，各只用在對的地方。
  - callout 明寫「本機推論不等於絕對安全」，全篇沒有保證句。
  - 台灣用語檢查過：沒有信息、默認、激活、優化、內存、芯片、軟件、網絡、數據等。
- batch-03 的差異規則：
  - topics 含 `ai-terms`。
  - 全篇（含 description）「本文」「這篇」0 次。
  - 正文沒有查證過程，日期寫成「資料截至 2026 年 10 月」。
  - 第一段就寫明操作步驟見兩篇實作篇並連過去。
  - 指派的 7 個站內連結都在，沒有多連。
- 結構：6 個 H2、恰好一個表（3 欄）、1 個 callout、diagram-1.svg 與 hero.svg 各一張。重新渲染後沒有壓線、超框或疊字。圖上唯一的數字 2026 在正文出現過。desc 和圖上文字都與正文一致。
- 兩篇實作篇（local-llm-why-and-when、local-llm-hardware-requirements）的內容確實是入門路線與硬體算法，第一段的「安裝與選購硬體見⋯⋯」說法正確。

## 我懷疑但沒改的事

- 字數 2659，超過 brief 的目標 2,200–2,600，但在上限 3,000 以內。為了不重寫，沒有刪別的句子。
- github.com 在這個環境經代理一律回 403（代理沒對這個 session 開放 GitHub），所以只讀到 raw.githubusercontent.com 上同一份 README，沒有打開 sources 裡寫的 GitHub 頁面本身。
- 「同一個框架改一行程式，就能把請求送到私密雲端運算」是 Apple 自己的說法，但它沒寫出兩個前提：`PrivateCloudComputeLanguageModel` 要 iOS 27／macOS 27 以上，開發者還要符合資格、申請 entitlement。句子本身不算錯，沒改。
- 「模型整份放進顯示記憶體通常最快」沒有一手來源直接這樣說。只能從 llama.cpp 的「partially accelerate」，以及 Ollama 談單一 GPU 對多張 GPU 時講的 PCI 匯流排理由間接支持。正文用了「通常」，所以沒改。
- 「本機推論」這個譯名缺少人工審定的台灣來源：國家教育研究院樂詞網用 curl 讀不到，Google 機器學習詞彙表繁中版與 Android 繁中頁都是 AI 翻譯。人工在地化的 Apple 繁中頁寫的是「在裝置上執行」。
- Ollama「本機執行時看不到你的提示詞」與 Android「處理後不保存輸入與輸出」是廠商的自我陳述，無法獨立驗證。正文都寫成「某某寫明」，沒有改成保證句。

facts_changed: 2
