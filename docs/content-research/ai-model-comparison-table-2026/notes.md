# 查證記錄：ai-model-comparison-table-2026

格式：`主張｜來源網址｜查證日`。查證日全部是 2026-09-16（除非另註）。
官網沒有公布的欄位一律寫「官網未公布」，不從第三方或記憶補。

## OpenAI

來源：https://developers.openai.com/api/docs/pricing（2026-09-16）
定價頁只有價格，沒有上下文與最大輸出，那兩欄另查 models 頁。

- gpt-6-astra 輸入 10.00 美元／百萬 token、輸出 50.00 美元｜https://developers.openai.com/api/docs/pricing｜2026-09-16
- gpt-5.6-sol 輸入 4.00、輸出 20.00｜同上｜2026-09-16
- gpt-5.6-terra 輸入 2.00、輸出 12.00｜同上｜2026-09-16
- gpt-5.6-luna 輸入 0.20、輸出 1.20｜同上｜2026-09-16
- gpt-5.4-mini 輸入 0.75、輸出 4.50｜同上｜2026-09-16
- gpt-5-nano 輸入 0.05、輸出 0.40（全表最便宜）｜同上｜2026-09-16

注意：2026-09-16 官網的 gpt-5.6-sol 是 4.00／20.00。第三方比價站當天寫 5／30，與官網不符，
不採用；這正是「只照官網欄位排」的理由。

## Anthropic

來源：https://platform.claude.com/docs/en/about-claude/pricing（2026-09-16）

- Claude Fable 5.1 輸入 10 美元／百萬 token、輸出 50｜2026-09-16
- Claude Opus 5 輸入 5、輸出 25｜2026-09-16
- Claude Sonnet 5 輸入 2、輸出 10｜2026-09-16
  官網註記：原訂 2026-09-01 調到 3／15 不會發生，2／10 已成標準價。
- Claude Haiku 4.5 輸入 1、輸出 5｜2026-09-16
- Claude 4.6 以後的模型，100 萬 token 上下文視窗一律標準價（沒有長脈絡加價）｜2026-09-16
- Claude Mythos 5.1 是限量存取（Project Glasswing），不列進公開總表。

## OpenAI 上下文與最大輸出

來源：https://developers.openai.com/api/docs/models（2026-09-16）
- gpt-6-astra 上下文 1.05M、最大輸出 128K｜2026-09-16
- gpt-5.6-sol／terra／luna 上下文 1.05M、最大輸出 128K｜2026-09-16
- gpt-5.4-mini、gpt-5-nano：該頁當天沒有列出，寫「官網未公布」。

## Google Gemini

來源：https://ai.google.dev/gemini-api/docs/pricing（2026-09-16）
- gemini-3.1-pro-preview：20 萬 token 內輸入 2.00／輸出 12.00；超過 4.00／18.00｜2026-09-16
- gemini-3.8-flash：輸入 0.75／輸出 3.75（官網標到 2026-12-31，之後 1.50／7.50）｜2026-09-16
- gemini-3.5-flash-lite：輸入 0.30／輸出 2.50｜2026-09-16
- gemini-2.5-flash-lite：輸入 0.10／輸出 0.40（text/image/video）｜2026-09-16
上下文：https://ai.google.dev/gemini-api/docs/models 當天沒有在總表列出 token 上限，寫「官網未公布」。

## xAI

來源：https://docs.x.ai/developers/models（2026-09-16）
- grok-4.6 上下文 500k；20 萬 token 內輸入 2.00／輸出 6.00，超過 4.00／12.00｜2026-09-16
- grok-4.3 上下文 1M；20 萬內 1.25／2.50，超過 2.50／5.00｜2026-09-16
- grok-build-0.1 上下文 256k；20 萬內 1.00／2.00｜2026-09-16
該頁沒有列最大輸出，寫「官網未公布」。

## DeepSeek

來源：https://api-docs.deepseek.com/quick_start/pricing/（2026-09-16）
欄位結構：輸入分「快取命中」與「快取未命中」，每個再分離峰與尖峰。
**第一次抓取誤把「快取命中」當成輸入價，已重查更正。** 表格要用的是「快取未命中」。
- deepseek-v4-pro：上下文 1M、最大輸出 384K；快取未命中輸入 尖峰 1.32／離峰 0.66；輸出 尖峰 3.96／離峰 1.98｜2026-09-16
- deepseek-flash：上下文 1M、最大輸出 384K；快取未命中輸入 尖峰 0.30／離峰 0.15；輸出 尖峰 1.20／離峰 0.60｜2026-09-16
- 尖峰是週一至週五 UTC 01:00–04:00 與 06:00–10:00，其餘離峰對折｜2026-09-16
表格一律採**尖峰價**，caption 註明。

## Mistral

來源：https://mistral.ai/pricing/api/（2026-09-16）
- Mistral Large 3 輸入 0.50／輸出 1.50｜2026-09-16
- Mistral Medium 3.5 輸入 1.50／輸出 7.50｜2026-09-16
- Mistral Small 4 輸入 0.15／輸出 0.60｜2026-09-16
- Ministral 3 (3B) 0.10／0.10；(8B) 0.15／0.15；(14B) 0.20／0.20｜2026-09-16
該頁沒有列上下文，寫「官網未公布」。
名字與價位帶對不上：掛 Large 的比掛 Medium 的便宜，這點寫進正文。

## 阿里雲百鍊（Qwen，新加坡站美元價）

來源：https://www.alibabacloud.com/help/en/model-studio/model-pricing（2026-09-16）
- qwen3.8-max 上下文 1M；輸入 2／輸出 6｜2026-09-16
- qwen3.7-plus 上下文 1M；輸入 0.40–1.2／輸出 1.60–4.8（階梯價）｜2026-09-16
- qwen3.8-flash 上下文 1M；輸入 0.15／輸出 0.47｜2026-09-16
該頁沒有列最大輸出，寫「官網未公布」。

## MiniMax

來源：https://platform.minimax.io/docs/guides/pricing-paygo（2026-09-16）
- MiniMax-M3 上下文 512k；51.2 萬 token 內輸入 0.30／輸出 1.20（官網標「永久五折」），超過 0.60／2.40｜2026-09-16
- MiniMax-M2.7 輸入 0.30／輸出 1.20｜2026-09-16
該頁沒有列最大輸出，寫「官網未公布」。

## Moonshot Kimi

來源：https://platform.kimi.ai/docs/pricing/chat（2026-09-16，原網址 platform.moonshot.ai 301 轉此）
- kimi-k3 上下文 1,048,576 token；快取未命中輸入 3.00／輸出 15.00（快取命中輸入 0.30）｜2026-09-16
- kimi-k2.7-code 上下文 262,144；快取未命中輸入 0.95／輸出 4.00｜2026-09-16
該頁沒有列最大輸出，寫「官網未公布」。

## Z.AI（GLM）

來源：https://docs.z.ai/guides/overview/pricing（2026-09-16）
- GLM-5.3 輸入 1.40／輸出 4.40｜2026-09-16
- GLM-5.3-Flash 輸入 0.15／輸出 0.50｜2026-09-16
- GLM-4.7-Flash、GLM-4.5-Flash 官網標免費｜2026-09-16
該頁沒有列上下文，也沒有列權重授權，兩欄都寫「官網未公布」。

## Anthropic 上下文與最大輸出

來源：https://platform.claude.com/docs/en/about-claude/models/overview（2026-09-16）
- Claude Fable 5.1 上下文 1M、最大輸出 128K｜2026-09-16
- Claude Opus 5 上下文 1M、最大輸出 128K｜2026-09-16
- Claude Sonnet 5 上下文 1M、最大輸出 128K｜2026-09-16
- Claude Haiku 4.5 上下文 200K、最大輸出 64K｜2026-09-16

## 效能：查證結果（這是本篇的重點發現）

查了六家官網，結論是**各家連量的東西都不一樣**，所以「同級距的效能」沒辦法排成一把尺。

- **OpenAI**：GPT-6 Astra GPQA Diamond 96.0%｜https://openai.com/index/gpt-6-astra/｜2026-09-16
  註：openai.com 對本環境回 403，改用限定 openai.com 網域的 WebSearch 取得，摘要引用的就是該announcement頁。
  sources 仍寫原始官網網址（brief §5 允許的做法）。
- **Google DeepMind**：Gemini 3.1 Pro GPQA Diamond 94.3%、SWE-Bench Verified 80.6%（單次嘗試）；
  上下文 1M、輸出 64K｜https://deepmind.google/models/model-cards/gemini-3-1-pro/｜2026-09-16
- **Anthropic**：Claude Opus 5 的 announcement 提到 Frontier-Bench v0.1、CursorBench 3.2、ARC-AGI 3、
  Zapier AutomationBench、OSWorld 2.0、GDPval-AA v2、Terminal-Bench 等，但**沒有列出確切數字**，
  只有相對說法（ARC-AGI 3「三倍於次佳模型」、Zapier AutomationBench「1.5 倍」）。
  模型文件頁（platform.claude.com/docs/en/models/opus-5/overview）也沒有跑分表。
  ｜https://www.anthropic.com/news/claude-opus-5｜2026-09-16
- **xAI**：Grok 4.6 的發布頁**有**跑分表，但用的是 AA Intelligence Index、GDPVal-AA v2、CursorBench v3.2、
  DeepSWE v1.1、FrontierCode v1.1、APEX-Agents、Terminal-Bench v3.0、APEX-SWE、AA-Briefcase、Harvey LAB，
  **沒有 GPQA Diamond，也沒有 SWE-bench Verified**｜https://x.ai/news/grok-4-6｜2026-09-16
- **DeepSeek**：API 文件沒有跑分表｜https://api-docs.deepseek.com/quick_start/pricing/｜2026-09-16
- **Qwen**：Qwen3.8-Max 的官方 blog 用自家 agent scaffold 跑 SWE-Bench 系列
  （bash 與 file-edit 工具、temperature 1.0、top_p 0.95、20 萬 token 上下文），
  是自己的測試環境，不是共用 harness｜https://qwen.ai/blog?id=qwen3.8｜2026-09-16

## 查不到、所以不寫的

- **Meta Llama 現行版本**：llama.com 301 轉 developer.meta.com/ai/，該頁只在導覽列出現 Llama 4 與 Llama 3，
  沒有版本、上下文或授權；developer.meta.com/ai/models/llama 回 404；ai.meta.com/blog 明確「沒有提到」。
  2026-09-16 查不到現行版本，**因此不列進表**，正文寫明查不到。
- **開放權重的授權條款**：Z.AI、MiniMax、Moonshot、Mistral 的 API 定價頁都不寫權重授權。
  原本規劃的「開放權重表」因此改成「各家官網揭露的效能資訊」表，授權的事連到站上既有文章
  （`ai-open-vs-closed-models`、`llama-models-explained`、`minimax-m-series-models-explained`）。
- **Gemini 的上下文**：ai.google.dev/gemini-api/docs/models 當天總表沒有 token 上限欄，
  只有 Gemini 3.1 Pro 從 DeepMind 模型卡拿到（1M／64K），其餘寫「官網未公布」。


## 開放權重表的查證（2026-09-16 補做）

第一版說「查不到 Meta 的現行開放權重模型」是**錯的**。當時只查了 llama.com、developer.meta.com 與
ai.meta.com/blog 三個地方，而權重授權本來就不寫在那裡——它在權重發布頁、GitHub repo 的 LICENSE 檔
與廠商自己的 Hugging Face organization。改查那些地方之後，十二家全部查到。

做法：一家一個 agent 只讀該廠商自己的官網／GitHub org／HF org，每筆結果再由兩個獨立的懷疑者驗證
（一個專攻授權名稱、一個專攻版本現行性，兩者都預設聲明是錯的）。兩票都沒推翻才進表。

### 進表的十二列

- **Meta｜Muse Glimmer 30B**｜Apache License 2.0｜https://huggingface.co/meta-models/Muse-Glimmer-30B｜2026-09-16
  - 參數：密集（非 MoE）模型，safetensors 實測 29,776,626,688 參數，官方稱 30B；另有 Muse-Glimmer-30B-assistant 3B 推測解碼 drafter
  - 上下文：131,072 tokens（config.json text max_position_embeddings=131072；官方開發者部落格寫「預設 128K，可再拉長」）
  - 限制：無額外限制（Meta 開發者部落格自述為「我們用過最寬鬆的開放模型授權」；模型卡另有非授權性質的使用指引，如未滿 18 歲不宜使用、須遵守貿易法規）
- **阿里巴巴｜Qwen3.8-Flash-Next**｜Qwen Community License 1.0（HF license_name: qwen-community-1.0）｜https://huggingface.co/Qwen/Qwen3.8-Flash-Next｜2026-09-16
  - 參數：主模型 125B，另含 51B N-gram 嵌入與 4B MTP，每 token 啟用 6B（HF safetensors 實測總量約 180B）
  - 上下文：原生 262,144 tokens，可延伸至 1,000,000 tokens
  - 限制：MAU 逾 1 億或月營收逾 2,000 萬美元的產品須在介面顯著標示模型名稱，且拿去做 Model-as-a-Service 或 AI 辦公/程式助理類產品須另外向 Qwen 取得商用授權（純內部使用不受限）。
- **阿里巴巴｜Qwen3.8-2.4T-A95B**｜Qwen3.8-Max License（HF license_name: qwen3.8-max，license: other）｜https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B｜2026-09-16
  - 參數：總參數 2.4T（2.4 兆），啟用 95B；92 層、512 experts（每 token 啟用 10 routed + 1 shared）
  - 上下文：原生 262,144 tokens，可延伸至 1,010,000 tokens
  - 限制：MAU 逾 1 億或月營收逾 2,000 萬美元須介面標示模型名稱；連續 12 個月營收逾 5,000 萬美元的 Model-as-a-Service 或 AI 辦公/程式助理業者，部署前須另簽商用授權（純內部使用不受限）。
- **DeepSeek｜DeepSeek-V4.1-Flash**｜MIT License｜https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash｜2026-09-16
  - 參數：總量 552B backbone，啟用 8B（prefill）／16B（decode）。另含 Engram 條件記憶模組 196B（稀疏查表存取），HF safetensors 索引全量約 763B
  - 上下文：1,000,000 tokens（config.json 的 max_position_embeddings = 1048576）
  - 限制：無額外限制
- **Mistral｜Mistral Medium 3.5 128B**｜Modified MIT License｜https://huggingface.co/mistralai/Mistral-Medium-3.5-128B｜2026-09-16
  - 參數：密集（dense）128B，非 MoE
  - 上下文：256k tokens
  - 限制：公司（或雇主）全球合併月營收超過 2,000 萬美元者不得依本授權使用該權重或其衍生模型，須另向 Mistral 洽談商用授權。
- **Z.AI｜GLM-5.3-Flash**｜MIT License（HF frontmatter: license: mit）｜https://huggingface.co/zai-org/GLM-5.3-Flash｜2026-09-16
  - 參數：總量 320B，啟用 18B（官方寫法 320B-A18B；MoE，45 層、288 專家、每 token 取 8 個，混合稀疏＋線性注意力）
  - 上下文：1,000,000 tokens（config.json 的 max_position_embeddings = 1048576；模型卡評測設定另寫最大 300,000 tokens）
  - 限制：無額外限制
- **MiniMax｜MiniMax-M3**｜MiniMax Community License（權重庫 LICENSE 檔標題為「MINIMAX COMMUNITY LICENSE」；HF 卡片 license_name: minimax-community）｜https://huggingface.co/MiniMaxAI/MiniMax-M3｜2026-09-16
  - 參數：MoE：總量 約 428B，啟用 約 23B／token（官方 platform.minimax.io 寫「approximately 428B total parameters」「approximately 23B activated parameters per token」；HF 權重檔實測 427,040,140,160）
  - 上下文：1,000,000 tokens（1M）；權重 config.json 的 max_position_embeddings = 1048576
  - 限制：商用須在網站或文件顯著標示「Built with MiniMax M3」，年營收逾 2,000 萬美元的公司須事先取得 MiniMax 書面授權（未達門檻者僅需通知 api@minimax.io），並受禁止用途條款（違法內容、軍事用途、危害未成年、蓄意假訊息、歧視言論）約束。
- **Moonshot｜Kimi K3**｜Kimi K3 License（廠商自訂授權，HF metadata license_name 為 kimi-k3、license 欄為 other）｜https://huggingface.co/moonshotai/Kimi-K3｜2026-09-16
  - 參數：總量 2.8T，啟用 104B（MoE，官方技術部落格描述為 Stable LatentMoE，每次啟用 896 個專家中的 16 個）
  - 上下文：1,048,576 tokens（官方稱 1-million-token context window）
  - 限制：自訂商業門檻授權：經營 Model as a Service 且連續 12 個月合計營收超過 2,000 萬美元者，商用前須另與 Moonshot AI 簽約；商用產品若超過 1 億月活躍用戶或月營收 2,000 萬美元，須在介面顯著標示「Kimi K3」（內部使用與透過 Moonshot 官方產品／認證推論夥伴存取不受限）。
- **Google｜Gemma 4 31B**｜Apache 2.0｜https://huggingface.co/google/gemma-4-31B｜2026-09-16
  - 參數：30.7B（密集模型，非 MoE）
  - 上下文：256K tokens
  - 限制：無額外限制
- **OpenAI｜gpt-oss-120b**｜Apache License 2.0｜https://huggingface.co/openai/gpt-oss-120b｜2026-09-16
  - 參數：總量 117B，啟用 5.1B（MoE）
  - 上下文：131,072 tokens
  - 限制：無額外限制
- **NVIDIA｜NVIDIA Nemotron 3.5 Lightning 30B-A3B (repo: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16)**｜OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)｜https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16｜2026-09-16
  - 參數：總量 30B，啟用 3B（hybrid Mamba-2 + MoE）
  - 上下文：最長 1M tokens（單張 H100 部署官方建議 256K）
  - 限制：Linux Foundation／PyTorch Foundation 的寬鬆模型授權，可商用，但轉散布時須保留授權全文與原始出處聲明，且若對他人提起專利／著作權訴訟則授權自動終止；未列於 OSI 認可清單。
- **Ai2｜Olmo Hybrid 7B（allenai/Olmo-Hybrid-7B）**｜Apache License 2.0｜https://huggingface.co/allenai/Olmo-Hybrid-7B｜2026-09-16
  - 參數：官方寫法 7B（稠密混合架構，非 MoE）。HF safetensors 中繼資料實測總參數 7,430,870,688。架構為 32 層，hidden size 3840，其中 75% 的層用 gated DeltaNet 遞迴子層、每 3 層接 1 層多頭注意力
  - 上下文：65,536 tokens（模型卡架構表 Context Length 欄位；config.json 的 max_position_embeddings 亦為 65536）
  - 限制：無額外限制（授權本身為標準 Apache 2.0；模型卡另附一句非拘束性說明「intended for research and educational use in accordance with Ai2's Responsible Use Guidelines」，那是使用指引不是授權條款）

同家族的 Gemma 4 12B Unified（11.95B、26.2 萬、Apache 2.0，https://huggingface.co/google/gemma-4-12B）也查證通過，因為授權與上下文跟 31B 相同，表上只留 31B。

### `sources` 只放得下四筆權重頁

schema 上限 20 筆（`schemas.py:369`），文章本來就用掉 18 筆。這次騰出兩個名額：

- 拿掉 Anthropic 定價頁，因為模型總覽頁同時有價格、上下文與最大輸出，兩筆重複。
- 拿掉第一版那筆「Meta 開發者 AI 頁（當天查不到現行 Llama 版本）」——那個結論本身是錯的。

四個名額給了條款最會影響讀者的四家：Meta（Apache 2.0，推翻第一版的結論）、
Qwen（同家族兩份不同授權）、MiniMax（商用須標示 Built with MiniMax M3）、
Moonshot（Model-as-a-Service 營收門檻）。
其餘八家的權重頁網址就是上面那份清單，沒有進 `sources`，但每一筆都是當天從那個網址讀到的。

### 被推翻、所以沒進表的十一筆

全部都是「規格對、但版本不是最新」——這正是對抗式驗證要抓的東西：

- Meta｜Llama 4 Maverick → 已被 Muse Glimmer 取代
- DeepSeek｜DeepSeek-V4-Pro-0813 → 已被 DeepSeek-V4.1-Flash 取代
- Mistral｜Mistral Small 4 119B A6B（HF repo：Mistral-Small-4-119B-2603） → 已被 官方寫法為「Mistral Small 4」 取代
- Z.AI｜GLM-5.3 → 已被 （見上表） 取代
- MiniMax｜MiniMax-M2.7 → 已被 MiniMax-M3 取代
- Moonshot｜Kimi K2.7 Code → 已被 Kimi K3 取代
- OpenAI｜gpt-oss-safeguard-120b → 已被 模型名稱本身無需更正 取代
- NVIDIA｜NVIDIA Nemotron 3 Ultra 550B-A55B (repo: NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16) → 已被 名稱寫法本身無誤，但若要指「NVIDIA 最新的開放權重模型」應為 NVIDIA Nemotron 3.5 Lightn 取代
- Ai2｜Olmo 3.1 32B Think（allenai/Olmo-3.1-32B-Think） → 已被 無需更正 取代
- Microsoft｜Phi-Ground-Any-4B (HF repo: microsoft/Phi-Ground-Any) → 已被 就「Microsoft 最新開放權重模型」而言應為 microsoft/VibeVoice-ASR-Streaming- 取代
- Microsoft｜Phi-4-Reasoning-Vision-15B → 已被 模型本身名稱正確 取代

### Microsoft 沒有進表

兩筆都被推翻。Phi-4-Reasoning-Vision-15B（2026-03-04、MIT、15B、1.6 萬上下文）規格全部對得上，
但驗證者指出 Microsoft 之後發布的是 VibeVoice-ASR-Streaming-7B——那是語音辨識模型，
不是同一類的通用語言模型。「Microsoft 現行的開放權重語言模型是哪一個」當天無法乾淨地判定，
依「兩票都過才進表」的標準，這家就不列。下次重查時再看。

