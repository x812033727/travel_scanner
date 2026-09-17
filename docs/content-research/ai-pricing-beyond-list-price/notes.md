# 查證記錄：ai-pricing-beyond-list-price

格式 `主張｜來源網址｜查證日`。全部查證日 2026-09-17，每一筆都是當天重新開官網讀到的，
沒有沿用姊妹篇 `ai-model-comparison-table-2026`（查證日 2026-09-16）的數字。

## 為什麼另開一篇而不是加進姊妹篇

姊妹篇的 `sources` 已經用滿 schema 上限 20 筆（`apps/api/app/guides/schemas.py:369`）。
要把快取與長上下文兩欄加進去，至少還要 Anthropic 定價頁與 xAI 定價頁兩筆新來源
（姊妹篇引的是 Anthropic 模型總覽頁與 xAI 模型頁，那兩頁沒有快取倍率與門檻規則）。
擠不進去，硬塞只能砍掉現有的載重來源。這篇自己帶 8 筆來源，兩篇互相連。

## 快取命中價

- OpenAI 快取輸入價（standard tier，每百萬 token）：gpt-6-astra 1.00、gpt-5.6-sol 0.40、
  gpt-5.6-terra 0.20、gpt-5.6-luna 0.02、gpt-5.4-mini 0.075、gpt-5-nano 0.005 美元。
  全部都正好是該型號輸入價的十分之一｜https://developers.openai.com/api/docs/pricing｜2026-09-17
- Anthropic 快取倍率表：5 分鐘寫入 1.25 倍、1 小時寫入 2 倍、命中 0.1 倍
  （Claude Fable 5.1 與 Claude Mythos 5.1 是 0.025 倍）。官網並寫明 5 分鐘那種讀一次回本、
  1 小時要讀兩次。對應金額：Opus 5 命中 0.50、Sonnet 5 命中 0.20、Haiku 4.5 命中 0.10、
  Fable 5.1 命中 0.25 美元｜https://platform.claude.com/docs/en/about-claude/pricing｜2026-09-17
- Google 內容快取：gemini-3.1-pro-preview 每百萬 0.20 美元（20 萬 token 以內）／0.40 美元（超過），
  **另收儲存費每百萬 token 每小時 4.50 美元**；gemini-3.8-flash 快取 0.075 美元（標到 2026-12-31，
  2027-01-01 起 0.15），儲存費每小時 0.50 美元（2027 起 1.00）
  ｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-17
- xAI 快取輸入價：grok-4.6 0.50 美元（20 萬 token 以下）／1.00 美元（達到 20 萬以上）；
  grok-4.3 0.20／0.40 美元｜https://docs.x.ai/developers/pricing｜2026-09-17
- DeepSeek 快取命中：deepseek-v4-pro 尖峰 0.044／離峰 0.022；deepseek-flash 尖峰 0.006／離峰 0.003 美元。
  表格採尖峰價｜https://api-docs.deepseek.com/quick_start/pricing/｜2026-09-17（欄位結構 2026-09-16 已查證）
- Moonshot 快取命中：kimi-k3 0.30 美元（未命中 3.00）、kimi-k2.7-code 0.19 美元（未命中 0.95）
  ｜https://platform.kimi.ai/docs/pricing/chat｜2026-09-17（2026-09-16 已查證，數字未變）
- MiniMax 快取讀取：MiniMax-M3 0.06 美元（51.2 萬 token 以內）／0.12 美元（超過）；
  MiniMax-M2.7 讀取 0.06、寫入 0.375 美元。M3 的快取寫入價官網未列
  ｜https://platform.minimax.io/docs/guides/pricing-paygo｜2026-09-17

表上的「命中價是原價的」百分比是本站用同一頁的原輸入價相除後四捨五入，不是官網欄位，
caption 已註明。xAI 的 25%（0.50／2.00）與 16%（0.20／1.25）是全表最高，DeepSeek 的 2% 最低。

## 長上下文加價門檻

- **Anthropic 沒有門檻**：官網長脈絡段落明寫「Claude 4.6 and later models ... include the full
  1M token context window at standard pricing. (A 900k-token request is billed at the same
  per-token rate as a 9k-token request.)」｜https://platform.claude.com/docs/en/about-claude/pricing｜2026-09-17
- Google 20 萬 token：gemini-3.1-pro-preview 輸入 2.00 → 4.00、輸出 12.00 → 18.00 美元，
  快取 0.20 → 0.40 美元｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-17
- **xAI 20 萬 token，且整筆改價**：官網原文「requests whose prompt reaches the listed token
  threshold are billed at the higher rate for all tokens in the request」。
  grok-4.6 輸入 2.00 → 4.00、輸出 6.00 → 12.00｜https://docs.x.ai/developers/pricing｜2026-09-17
- MiniMax 51.2 萬 token：輸入 0.30 → 0.60、輸出 1.20 → 2.40 美元
  ｜https://platform.minimax.io/docs/guides/pricing-paygo｜2026-09-17
- OpenAI：定價頁有 Short context 與 Long context 兩欄，但**當天頁面沒有寫切換的 token 數**，
  所以表上寫「官網未標門檻」，不從第三方補｜https://developers.openai.com/api/docs/pricing｜2026-09-17

## Tokenizer

- Anthropic 定價頁註記原文：「Claude 4.7 and later models and Claude Mythos Preview use a newer
  tokenizer ... This tokenizer produces approximately 30% more tokens for the same text. The exact
  increase depends on the content and workload shape. Claude Sonnet 4.6 and earlier models use the
  previous tokenizer.」｜https://platform.claude.com/docs/en/about-claude/pricing｜2026-09-17
- 模型總覽頁另有同一件事的另一種說法：100 萬 token 在新 tokenizer 約等於 55.5 萬字，
  舊 tokenizer 約 75 萬字｜https://platform.claude.com/docs/en/about-claude/models/overview｜2026-09-17
- **其他家沒有可引用的對照說明**，所以正文寫明「只能自己拿同一份文件分別去數」，不替它們填數字。

## 當天讀不到的

- 阿里雲百鍊（Qwen）的快取規則：`https://www.alibabacloud.com/help/en/model-studio/model-pricing`
  2026-09-17 回 HTTP 503，讀不到，因此這篇沒有列阿里雲的快取價。下次更新時再試。
- Mistral 與 Z.AI 的快取價當天沒有查（這篇的表以已確認的七家為準），不是「沒有」而是「沒查」，
  下次要補的話從它們的定價頁開始。
