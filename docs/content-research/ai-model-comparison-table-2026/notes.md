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
