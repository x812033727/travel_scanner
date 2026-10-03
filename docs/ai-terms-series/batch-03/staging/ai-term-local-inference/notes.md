# 查證與編輯紀錄：ai-term-local-inference

查證日一律 2026-10-03（當天實際打開）。格式：主張｜來源網址｜查證日｜讀取方式。
抓頁一律 `curl -sSL`，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，狀態碼 200 且內容含該段落才算讀到。

## 用語

Android 開發者文件繁中版寫「裝置端生成式 AI 會在本機執行提示」「裝置端 AI」，據此採「本機推論」，並說明作業系統內建模型稱「裝置端」｜https://developer.android.com/ai/gemini-nano?hl=zh-tw｜2026-10-03｜curl 200，HTML 去標籤。查核補記：頁首註明「Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯」，是機器翻譯不是人工在地化，正文已改成「Android 開發者文件繁中版（頁面註明由 AI 翻譯）」。Google 機器學習詞彙表繁中版（https://developers.google.com/machine-learning/glossary?hl=zh-tw）同樣有 AI 翻譯標示；國家教育研究院樂詞網的搜尋結果由 JavaScript 載入，curl 讀不到。人工在地化的對照：Apple 繁中支援文件寫「在裝置上執行」（https://support.apple.com/zh-tw/guide/iphone/iphe3f499e0e/ios）
推論＝inference、推理＝reasoning 沿用系列規則；第一次出現各附英文｜docs/ai-terms-series/batch-02/brief.md｜2026-10-03｜系列規則，非事實主張

## 權重與計算在本機，其他不一定

llama.cpp 的主要目標是在各種硬體上以最少設定做 LLM（與 VLM）推論，「locally and in the cloud」｜https://github.com/ggml-org/llama.cpp｜2026-10-03｜github.com 經代理回 403；改讀同一份 README：https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md（200）的 Description 段
「同一套軟體裝在筆電上是本機、裝在租來的伺服器上就是雲端」是上一條的白話推演，不是逐字引用｜同上｜2026-10-03｜編輯整理
Ollama：在本機執行時看不到提示詞或資料；使用雲端託管模型時由其服務處理提示詞與回答（官方另說不儲存、不記錄、不拿來訓練，文中未寫）；網路搜尋屬雲端功能｜https://docs.ollama.com/faq｜2026-10-03｜curl 200（渲染頁含同段文字）；另讀 GitHub 原始檔 https://raw.githubusercontent.com/ollama/ollama/main/docs/faq.mdx（200）對照，兩者一致
Ollama 在 macOS 與 Windows 會自動下載更新（清單「下載與更新」中的軟體更新）｜https://docs.ollama.com/faq｜2026-10-03｜同上（How can I upgrade Ollama?）
Foundry Local：提示詞與模型輸出在本機處理；仍會為下載模型檔與執行元件連網；使用者回報問題時可選擇分享紀錄檔；診斷資料的收集依產品條款與 Microsoft 隱私權聲明｜https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local｜2026-10-03｜curl 200；頁面 ms.date 2026-05-15，updated_at 2026-08-04
Foundry Local 啟動時可能更新模型目錄（清單「模型目錄」）；網路流量只有初次下載與可選的目錄中繼資料更新｜https://learn.microsoft.com/en-us/windows/ai/faq｜2026-10-03｜curl 200；頁面 ms.date 2026-05-10
「紀錄同步與分享」一項是一般描述（存進會同步的資料夾或使用分享功能就會離開裝置），沒有單獨來源，也不指任何特定產品｜無｜2026-10-03｜編輯描述

## 記憶體

以 bfloat16／float16 載入時，X 十億參數約需 2X GB 顯示記憶體（float32 為 4X GB，文中未寫）｜https://huggingface.co/docs/transformers/en/llm_tutorial_optimization｜2026-10-03｜curl 200，HTML 去標籤讀 §1 Lower Precision
「80 億參數約需 16 GB、量化成 4 位元約剩四分之一、4 GB 左右」是用上一條規則做的示例換算（16 位元→4 位元＝四分之一），文中已標「示例換算」，未指任何特定模型｜同上｜2026-10-03｜編輯換算
KV cache 要存的數值個數＝2 × 序列長度 × 注意力頭數 × 每頭維度 × 層數；使用 KV cache 時最大記憶體隨產生的 token 數線性增加｜https://huggingface.co/docs/transformers/en/llm_tutorial_optimization｜2026-10-03｜同上，§3.2 The key-value cache
查核補記：上面的公式是每個頭各存一份 key／value 的算法；同一份指南 §3.2.2–3.2.3 說 MQA 只存 1 組、GQA 存 n < n_head 組，能大幅減少 KV 快取記憶體（它的範例在 16000 token 下從 15 GB 降到不到 400 MB，文中未寫數字）。正文已補一句「讓多個頭共用 key 與 value 的設計（MQA、GQA）能大幅縮小它」｜https://huggingface.co/docs/transformers/en/llm_tutorial_optimization｜2026-10-03｜curl 200，HTML 去標籤讀 §3.2.2 Multi-Query-Attention、§3.2.3 Grouped-Query-Attention
llama.cpp 支援 1.5、2、3、4、5、6、8 位元整數量化，用於加快推論、降低記憶體用量；支援 CPU＋GPU 混合推論，處理大於顯示記憶體總量的模型｜https://github.com/ggml-org/llama.cpp｜2026-10-03｜raw README（同上）
「代價是精度可能下降」：Hugging Face 同頁寫 4 位元量化實務上常與 8 位元或 bfloat16 推論結果不同；Ollama 寫 K/V 快取量化有精度損失｜https://huggingface.co/docs/transformers/en/llm_tutorial_optimization；https://docs.ollama.com/faq｜2026-10-03｜同上
並行請求會放大上下文：2K 上下文配 4 個並行請求＝8K 上下文並配置額外記憶體｜https://docs.ollama.com/faq｜2026-10-03｜How does Ollama handle concurrent requests?
ollama ps 的 PROCESSOR 欄顯示 100% GPU、100% CPU 或 CPU/GPU 比例｜https://docs.ollama.com/faq｜2026-10-03｜同上
「模型整份放進顯示記憶體通常最快」：依據改為 llama.cpp README 的「CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity」（放不下時只能部分加速）。查核補記：原紀錄引的 Ollama「能整份放進單一 GPU 時通常效能最好，因為減少 PCI 匯流排傳輸」講的是單一 GPU 對多張 GPU，不是 GPU 對 CPU＋GPU，只能當旁證；Ollama 的 gpu.mdx、troubleshooting.mdx 也沒有直接的說法。正文用「通常」，未改｜https://github.com/ggml-org/llama.cpp；https://docs.ollama.com/faq｜2026-10-03｜raw README；Ollama FAQ
NPU 的白話說明（專做神經網路運算的處理器）是一般描述｜無｜2026-10-03｜編輯描述

## 作業系統內建的裝置端模型

Foundation Models framework 提供 Apple Intelligence 的裝置端模型與私密雲端運算模型｜https://developer.apple.com/documentation/foundationmodels｜2026-10-03｜HTML 頁 200 但為 JS 殼；內容改讀同站資料端點 https://developer.apple.com/tutorials/data/documentation/foundationmodels.json（200）
模型可用性取決於裝置與地區是否支援 Apple Intelligence；開啟 Apple Intelligence 後模型需要時間下載；大量資料超出上下文視窗時，建議分段、各自處理再合併｜https://developer.apple.com/documentation/foundationmodels/generating-content-and-performing-tasks-with-foundation-models｜2026-10-03｜資料端點 .json（200）
Apple 會在例行作業系統更新中更新 SystemLanguageModel｜https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel｜2026-10-03｜資料端點 .json（200）
裝置端模型不需要網路；建立工作階段時改一行程式即可改走私密雲端運算，取得較大上下文與較強推理；私密雲端運算需要網路連線；開發者另須符合資格申請 entitlement（文中未寫）｜https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute｜2026-10-03｜資料端點 .json（200）。頁內的上下文 token 數與每日額度屬產品快照，未寫入
Apple Intelligence 會先分析請求能否在裝置上處理，較複雜的可使用私密雲端運算；iPhone「設定」→「隱私權與安全性」→「Apple Intelligence 報告」，可選過去 15 分鐘（預設）或過去 7 天，輸出送往私密雲端運算的要求紀錄（Apple_Intelligence_Report.json）｜https://support.apple.com/zh-tw/guide/iphone/iphe3f499e0e/ios｜2026-10-03｜curl 200（繁中版取介面名稱「私密雲端運算」「隱私權與安全性」「Apple Intelligence 報告」）；英文版 https://support.apple.com/guide/iphone/apple-intelligence-and-privacy-iphe3f499e0e/ios（200）對照
Gemini Nano 在 AICore 系統服務執行；AICore 無直接網際網路存取，包括模型下載在內的連線經開放原始碼的 Private Compute Services 轉送；每個請求隔離，處理後不保存輸入與輸出紀錄；裝置端少了網路延遲但推論速度取決於裝置硬體（表格「速度」列）｜https://developer.android.com/ai/gemini-nano｜2026-10-03｜curl 200；頁尾 Last updated 2026-09-08 UTC
Windows AI APIs 需要具 NPU 的 Copilot+ PC；資料在裝置上由 NPU 處理，輸入不送往 Microsoft 伺服器｜https://learn.microsoft.com/en-us/windows/ai/faq｜2026-10-03｜curl 200
Foundry Local 隨 App 一起提供（"an end-to-end local AI solution that your application ships with"，支援 Windows、macOS、Linux），不是作業系統內建，正文在「作業系統內建」一節補了「則不是系統內建」；模型首次使用時下載並快取在本機，之後可離線推論｜https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local；https://learn.microsoft.com/en-us/windows/ai/faq｜2026-10-03｜curl 200

## 取捨表與檢查方法

本機沒有每個 token 的費用（Foundry Local 原文 no per-token costs）｜https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local｜2026-10-03｜curl 200
雲端可用較大模型與較長上下文：以 Apple 私密雲端運算為例（larger, server-based models；larger context）；「費用多半依用量或方案計算」「伺服器硬體通常較強」為一般描述，已加「多半」「通常」，未寫任何價格｜https://support.apple.com/zh-tw/guide/iphone/iphe3f499e0e/ios；https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute｜2026-10-03｜同上
Ollama 停用雲端功能：~/.ollama/server.json 設 disable_ollama_cloud，或環境變數 OLLAMA_NO_CLOUD=1；重新啟動後生效，紀錄顯示 Ollama cloud disabled: true；停用後不能用雲端模型與網路搜尋｜https://docs.ollama.com/faq｜2026-10-03｜How do I disable Ollama Cloud features?
Ollama 預設綁定 127.0.0.1 的 11434 埠，用 OLLAMA_HOST 改綁定位址才會對網路開放｜https://docs.ollama.com/faq｜2026-10-03｜How can I expose Ollama on my network?
斷網測試與網路監看的說明、callout 的風險描述為一般安全常識的整理，沒有單獨來源；沒有寫成保證｜無｜2026-10-03｜編輯描述

## 示例與圖

會議筆記示例為原創教學設計，已標「示例，未實測」，沒有寫任何觀察到的輸出。
diagram-1.svg 與 hero.svg 為手繪向量圖，不是 AI 產圖。圖上唯一的數字是製圖年份 2026，正文「資料截至 2026 年 10 月」有出現。
字數以 app.guides.pack_ingest._body_length 實算：2659（含 rich_paragraph 的站內連結文字；查核前 2594，查核補兩句後 2659）。

## 查核（2026-10-03，獨立查核者）

全部 12 筆來源今天重新以 curl -sSL 打開：github.com 經本環境代理回 403（代理對這個 session 未開放 GitHub，不是網站問題），同一份 README 從 raw.githubusercontent.com 讀到 200；Apple 開發者頁 HTML 是 JS 殼，改讀 /tutorials/data/….json（200）；其餘皆 200。逐條對照與修改見 verify-1.md。
