# Claims: gpt6-vs-opus55-worth-paying

Written 2026-09-28 (writer: claude-fable-5-1). Format: `id｜claim｜source URL｜checked｜scene`. All prices are list prices per million tokens as shown on the vendor's page on 2026-09-28.

c1｜GPT-6 Astra: $10 input, $1 cached input, $50 output; the pricing table also shows a $12.50 column read as the cache-write price (column header to be confirmed by the verifier); the model page confirms $10 / $50, a 1,050,000-token context window and 128,000 max output tokens｜https://platform.openai.com/docs/pricing and https://developers.openai.com/api/docs/models/gpt-6-astra (both HTTP 200 with the editorial user agent; openai.com/api/pricing/ and the Astra launch page answered 403)｜2026-09-28｜hook, sheet, job2-table
c2｜GPT-6 Sol: $2 input, $0.20 cached, $2.50 cache write, $10 output｜https://platform.openai.com/docs/pricing｜2026-09-28｜sheet, job2-table, job3
c3｜Claude Opus 5.5: $4 input, $20 output, $0.20 cache read, $5 cache write; fast mode $8 / $40｜https://www.anthropic.com/news/claude-opus-5-5｜2026-09-28｜sheet, job2-table
c4｜Grok 4.7: $2.00 input, $6.00 output, $0.50 cached input for prompts under 200k tokens ($4 / $12 / $1 at 200k and above); no cache-write fee listed｜https://docs.x.ai/docs/models｜2026-09-28｜sheet, job2-table
c5｜Gemini 3.8 Flash: $0.75 input, $3.75 output, $0.075 context caching through 2026-12-31; $1.50 / $7.50 / $0.15 from 2027-01-01; no cache-write fee listed (a per-hour cache storage charge, if shown, is not counted)｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-28｜sheet, job2-table
c6｜Google's pricing page lists no Pro model of the 3.8 generation; the Pro line shown is Gemini 3.1 Pro Preview at $2–$4 input / $12–$18 output by context length｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-28｜sheet
c7｜Job 1 arithmetic: 0.9M input + 0.03M output a month → Astra 0.9×10 + 0.03×50 = $10.50; Opus 5.5 3.60 + 0.60 = $4.20; Sol 1.80 + 0.30 = $2.10; Grok 4.7 1.80 + 0.18 = $1.98; Gemini 3.8 Flash 0.675 + 0.1125 = $0.79｜c1–c5｜2026-09-28｜formula, job1
c8｜Job 2 arithmetic: 12M fresh input, 48M cached input, 12M cache writes, 3M output a month → Astra 120 + 48 + 150 + 150 = $468; Sol 24 + 9.6 + 30 + 30 = $93.60; Opus 5.5 48 + 9.6 + 60 + 60 = $177.60; Grok 4.7 24 + 24 + 0 + 18 = $66; Gemini 3.8 Flash 9 + 3.6 + 0 + 11.25 = $23.85｜c1–c5｜2026-09-28｜job2, job2-table
c9｜"A third of Astra's job-2 bill is cache writes": 150 of 468 = 32%; "twenty fold range": 468 / 23.85 = 19.6｜c8｜2026-09-28｜job2-table
c10｜Job 3 arithmetic: 30M input, 3M output → Astra 300 + 150 = $450; Opus 5.5 120 + 60 = $180; Sol 60 + 30 = $90; Grok 4.7 60 + 18 = $78; Gemini 3.8 Flash 22.5 + 11.25 = $33.75｜c1–c5｜2026-09-28｜job3
c11｜Retry example: Flash $23.85 + 4 hours × $40 = $183.85 versus Opus 5.5 $177.60; the hour and the rate are stated as the owner's assumptions｜c8｜2026-09-28｜retry
c12｜Picks and the "do not switch for a chart" line are the owner's opinion (stance 1, 2, 6)｜brief.md 站主觀點｜2026-09-28｜picks, outro

## 與企劃不同的地方

- GPT-6 Sol joins the table as the "cheaper sibling" the test asks about; the brief listed only Astra, Opus 5.5 and Grok.
- Gemini is represented by 3.8 Flash because Google's page lists no 3.8 Pro; the narration says so.
- Cache writes are included in job 2 for the two vendors that list them, which the brief's planning numbers did not do; the totals are therefore higher than the brief's.

## 我懷疑但沒動的事

- The OpenAI pricing table's column order (input, cached input, 12.5, output) was read from the page's data; the header names were not captured. If the $12.50 column is not cache writes, the Astra and Sol job-2 rows change.
- Whether xAI or Google bill anything for writing to a cache that the script's "not listed" glosses over.
- Fast-mode prices (OpenAI 2x, Anthropic $8 / $40) are deliberately left out of the arithmetic.

## 進度

All 14 scenes written; lint pending in this session. Awaiting verification round 1.
