# Verification round 1: gpt6-vs-opus55-worth-paying

Verifier: claude-fable-5-1 (independent of the writer), 2026-09-28. Every price below was read on the vendor's own page today with the editorial user agent (curl, comments stripped; 1 s between requests to one host); third-party pages were not used. Web search calls used: 0. Helper files: `/tmp/claude-0/-home-user-travel-scanner/674d9bf2-c3b1-5d19-bf6c-31efd377fe1e/scratchpad/verify-gpt6-vs-opus55/` (claims-list.md, downloaded pages, video.before.json).

Pages fetched (all HTTP 200 unless noted):

| URL | HTTP | Note |
| --- | --- | --- |
| https://platform.openai.com/docs/pricing | 200 | price tables as HTML plus embedded JSON |
| https://developers.openai.com/api/docs/models/gpt-6-astra | 200 | "Input $10.00 Cached input $1.00 Cache writes $12.50 Output $50.00" |
| https://developers.openai.com/api/docs/guides/prompt-caching | 200 | cache-write billing rule (added to sources) |
| https://www.anthropic.com/news/claude-opus-5-5 | 200 | pricing table incl. cache writes, fast mode |
| https://platform.claude.com/docs/en/build-with-claude/prompt-caching | 200 | token classes and multipliers (added to sources) |
| https://www.anthropic.com/pricing | 200 | lands on https://claude.com/pricing; Opus 5.5 Read $0.20 / Write $5 / In $4 / Out $20 |
| https://docs.x.ai/docs/models | 200 | one redirect to https://docs.x.ai/developers/models; rendered text shows $2.00 / $6.00 / 500k only |
| https://docs.x.ai/developers/models/grok-4.7 | 200 | "Cached tokens $0.50 / 1M tokens"; 200K threshold |
| https://docs.x.ai/developers/pricing | 200 | grok-4.7 $2.00 $0.50 $6.00 / long context ≥200k $4.00 $1.00 $12.00 |
| https://ai.google.dev/gemini-api/docs/pricing | 200 | Gemini 3.8 Flash block, 2027 prices, storage price |

openai.com/index/… and openai.com/api/pricing/ were not fetched (403 to both methods per the brief).

## Claim table

| # | Claim | Where | URL | HTTP | Verdict | Before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Model names GPT-6 Astra, Claude Opus 5.5, Gemini are current products | youtube.title | platform.openai.com/docs/pricing; anthropic.com/news/claude-opus-5-5; ai.google.dev pricing | 200 | CONFIRMED | — |
| 2 | Priced on Astra, Sol, Opus 5.5, Grok 4.7, Gemini 3.8 Flash; "official list prices of September 28, 2026"; "Recorded 2026-09-28" | youtube.description | the five source pages | 200 | CONFIRMED | — |
| 3 | Tag names (Claude Opus 5.5, GPT-6 Astra, Gemini 3.8 Flash, Grok 4.7) | youtube.tags | as above | 200 | CONFIRMED | — |
| 4 | "$50 vs $20", "same job, per million tokens" = Astra vs Opus 5.5 output price | thumbnail | developers.openai.com Astra page; anthropic.com news | 200 | CONFIRMED | — |
| 5 | Five sources, checked_on 2026-09-28 | sources[] | all five | 200 | CHANGED | two sources added: OpenAI prompt caching guide, Anthropic prompt caching docs (the corrected job-2 arithmetic rests on them) |
| 6 | GPT-6 Astra $50 per M output | hook iut8 | platform.openai.com/docs/pricing | 200 | CONFIRMED | — |
| 7 | Claude Opus 5.5 $20 per M output | hook iut8 | anthropic.com/news/claude-opus-5-5 | 200 | CONFIRMED | — |
| 8 | Gemini 3.8 Flash under $4 per M output ($3.75) | hook iut8 | ai.google.dev pricing | 200 | CONFIRMED | — |
| 9 | "Pick by benchmark and you overpay…", "The winner is not the smartest model" | hook 4f5z, 4vsv | — | — | OUT OF SCOPE | opinion |
| 10 | "official rates as of today" | hook ed4s | — | — | OUT OF SCOPE | process; date is true |
| 11 | "Official list prices, per million tokens, 2026-09-28" | sheet title | all five | 200 | CONFIRMED | — |
| 12 | Astra $10 / $1 cached / $50 | sheet row + mpni | platform.openai.com/docs/pricing (thead: Input, Cached input, Cache writes, Output) | 200 | CONFIRMED | — |
| 13 | Sol $2 / $0.20 / $10 | sheet row + bgt8 | platform.openai.com/docs/pricing | 200 | CONFIRMED | — |
| 14 | Opus 5.5 $4 / $0.20 / $20 | sheet row + a8eb | anthropic.com/news/claude-opus-5-5 | 200 | CONFIRMED | — |
| 15 | Grok 4.7 under 200k: $2 / $0.50 / $6 | sheet row + xiua | docs.x.ai/docs/models → developers/models; cached price on developers/models/grok-4.7 and developers/pricing | 200 | CONFIRMED | — |
| 16 | Gemini 3.8 Flash $0.75 / $0.075 / $3.75 | sheet row + qx54 | ai.google.dev pricing | 200 | CONFIRMED | — |
| 17 | Flash price holds until the end of the year, then doubles | sheet 39yb | ai.google.dev pricing: "through December 31, 2026", $1.50 / $7.50 / $0.15 "starting January 1, 2027" | 200 | CONFIRMED | — |
| 18 | Google lists no Pro price for the 3.8 generation | sheet 39yb | ai.google.dev pricing (3.8 entries: Flash, Flash TTS, Flash-Lite TTS, Live; Pro line is 3.1 Pro Preview) | 200 | CONFIRMED | — |
| 19 | "read from each company's own pricing page today" | sheet zeh4 | — | — | OUT OF SCOPE | process |
| 20 | Formula: "+ cache writes × write price, where listed" as an additive term | formula code slide | platform.openai.com tooltip: "writes are not an additive fee"; platform.claude.com: read + creation + input classes | 200 | CHANGED | additive line → "(fresh tokens written to a cache: the write price replaces the input price, where a vendor lists one)"; highlight lines 1–4 untouched |
| 21 | Job 1: 30k in + 1k out × 30 days = 0.9M in, 0.03M out | formula slide, yvm3, uia6 | arithmetic | — | CONFIRMED | — |
| 22 | Astra $10.50 | job1 + uwys | 0.9×10 + 0.03×50 | — | CONFIRMED | — |
| 23 | Opus 5.5 $4.20 | job1 + uwys | 0.9×4 + 0.03×20 | — | CONFIRMED | — |
| 24 | Sol $2.10 | job1 + d8vw | 0.9×2 + 0.03×10 | — | CONFIRMED | — |
| 25 | Gemini 3.8 Flash $0.79 | job1 + d8vw | 0.675 + 0.1125 = 0.7875 | — | CONFIRMED | — |
| 26 | Grok 4.7 about $1.98 ("about two dollars") | job1 source + d8vw | 1.80 + 0.18 | — | CONFIRMED | — |
| 27 | 0.6M fresh, 2.4M cached, 150k out a day × 20 = 12M / 48M / 3M | job2 steps + xupq, ph5f, xexs | arithmetic | — | CONFIRMED | — |
| 28 | Astra job 2: $168 / $150 / $150 / $468; "about four hundred seventy… a third of that is cache writes, a fee OpenAI lists for this generation" | job2-table row + wz7s | OpenAI tooltip and caching guide: a token is Input, Cached Input or Cache Write; writes 1.25× for GPT-5.6 and later | 200 | CHANGED | $48 / $150 / $150 / $348; "about three hundred forty eight dollars a month. A hundred fifty of that is cache writes, a fee OpenAI lists for its newer models" |
| 29 | Sol job 2: $34 / $30 / $30 / $94; "about ninety four" | job2-table row + mcai | same rule; 12×2.5 + 48×0.2 + 3×10 = 69.60 | 200 | CHANGED | $10 / $30 / $30 / $70; "about seventy" |
| 30 | Opus 5.5 job 2: $58 / $60 / $60 / $178; "about one hundred seventy eight, sixty of it cache writes" | job2-table row + mcai | platform.claude.com prompt caching: writes replace base input; 12×5 + 48×0.2 + 3×20 = 129.60 | 200 | CHANGED | $10 / $60 / $60 / $130; "about one hundred thirty, sixty of it cache writes" |
| 31 | Grok 4.7 job 2: $48 / not listed / $18 / $66 | job2-table row + z6g3 | 12×2 + 48×0.5 + 3×6; no write fee on any xAI page | 200 | CONFIRMED | — |
| 32 | Gemini 3.8 Flash job 2: $13 / not listed / $11 / $24 | job2-table row + z6g3 | 9 + 3.6 + 11.25 = 23.85 | 200 | CONFIRMED | — |
| 33 | "Neither lists a cache write fee on its price page" | z6g3 | ai.google.dev: "$0.50 / 1,000,000 tokens per hour (storage price)" for context caching | 200 | CHANGED | "Neither lists a cache write fee, though Google bills hourly cache storage, which I left out" |
| 34 | "a twenty fold price range" (468 / 23.85 = 19.6) | cv6f | 348 / 23.85 = 14.6 | — | CHANGED | "almost a fifteen fold price range" |
| 35 | 10,000 × (3k in + 300 out) = 30M in, 3M out | job3 zyt2 | arithmetic | — | CONFIRMED | — |
| 36 | Astra $450 | job3 + 4e86 | 300 + 150 | — | CONFIRMED | — |
| 37 | Opus 5.5 $180 | job3 + 4e86 | 120 + 60 | — | CONFIRMED | — |
| 38 | Grok 4.7 $78 | job3 + gbsu | 60 + 18 (3k-token prompts are under 200k) | — | CONFIRMED | — |
| 39 | Gemini 3.8 Flash $34 | job3 + gbsu | 22.5 + 11.25 = 33.75 | — | CONFIRMED | — |
| 40 | Sol $90 | job3 source + gbsu | 60 + 30 | — | CONFIRMED | — |
| 41 | "where the money goes: input" | job3 b3ge | input is two thirds of every job-3 bill | — | CONFIRMED | — |
| 42 | Flash $24 + 1 h/week at $40 = about $160 more, total about $184 | retry left + mbxu, pmjw | 23.85 + 4×40 = 183.85 | — | CONFIRMED | — |
| 43 | Opus 5.5 $178, "Total about $178", "Opus 5.5 at one seventy eight … is now the cheaper option" | retry right + xauy | dependant of #30 (129.60) | — | CHANGED | "$130", "Total about $130", "Opus 5.5 at one hundred thirty"; still cheaper than $184 |
| 44 | The hour and the rate are the owner's example | retry bxqs | brief 站主觀點 | — | CONFIRMED | marked as the owner's |
| 45 | "retries multiply everything" | rule | — | — | OUT OF SCOPE | opinion |
| 46 | Cheaper siblings: Sol under Astra, Flash under Pro, smaller Claude models under Opus | test ez5e | platform.openai.com (gpt-6-sol); ai.google.dev (Flash vs Pro); anthropic.com footer (Sonnet, Haiku) | 200 | CONFIRMED | — |
| 47 | Picks table and the "do not switch for a chart" line | picks | brief 站主觀點 1, 2, 6 | — | OUT OF SCOPE | opinion, labelled "My picks, as opinion" and "these are opinions, not measurements" |
| 48 | Last video's agent fetched two of these price pages and hit a wall on the third; "Five moves, one 403, an honest blank cell" | agent-cta d539, a6h2, slide | docs/videos/always-on-agent-explained/demo-log.md (Anthropic and xAI read; openai.com/index/gpt-6-astra/ → 403) | — | CONFIRMED | — |
| 49 | "Every price … on September 28, 2026"; "The links are in the description" | outro ypij | tools/video/core/metadata.mjs composeDescription appends `sources` | — | CONFIRMED | — |
| 50 | Outro slide formula summary | outro slide | — | — | OUT OF SCOPE | style |
| 51 | Astra 1,050,000-token context window, 128,000 max output tokens | claims.md c1 | developers.openai.com Astra page | 200 | CONFIRMED | — |
| 52 | Opus 5.5 fast mode $8 / $40 | claims.md c3 | anthropic.com news; claude.com/pricing "2x standard pricing" | 200 | CONFIRMED | — |
| 53 | Grok 4.7 at 200k and above: $4 / $12 / $1 cached | claims.md c4 | docs.x.ai/developers/pricing | 200 | CONFIRMED | — |
| 54 | Flash from 2027-01-01: $1.50 / $7.50 / $0.15 | claims.md c5 | ai.google.dev pricing | 200 | CONFIRMED | — |
| 55 | Gemini 3.1 Pro Preview $2–$4 in / $12–$18 out by context length | claims.md c6 | ai.google.dev pricing (≤200k / >200k) | 200 | CONFIRMED | — |

## Summary

**Counts.** 55 claims: CONFIRMED 41, CHANGED 8 (#5, 20, 28, 29, 30, 33, 34, 43), NOT FOUND 0, OUT OF SCOPE 6. Distinct fact corrections: cache writes are not additive (drives #20, 28, 29, 30, 34, 43), Google's hourly cache-storage price (#33), plus the two added sources (#5).

**OpenAI table headers.** The rendered `<thead>` on platform.openai.com/docs/pricing has two header rows: a group row "" | "Short context" (tooltip "≤272K input tokens") | "Long context" (">272K input tokens"), and a column row Model | Input | Cached input | Cache writes | Output | Input | Cached input | Cache writes | Output. The embedded JSON headings read "Model", "Short context input", "Short context cached input", "Short context cache writes", "Short context output", then the four long-context columns. The 5-value rows `[["gpt-6-astra"],[10],[1],[12.5],[50]]` are the short-context Input, Cached input, Cache writes, Output; the long-context cells are derived (2× input and cache, 1.5× output: $20 / $2 / $25 / $75). So 12.5 is the cache-write price, as the script assumed, and the Astra model page prints the same four numbers under "Text tokens". The page carries three more tables with the same headers: two at 50% (Batch, Flex: $5 / $0.50 / $6.25 / $25) and one at 2× (Fast mode: $20 / $2 / $25 / $100); the $10 table is Standard. The tooltip on "Cache writes": "Input tokens are either Input, Cached Input, or Cache Write and writes are not an additive fee." The caching guide: "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate"; earlier models have "No additional cache-write charge". Anthropic's docs split input the same way (`total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`; writes "25% more than base input tokens"). The writer had charged the 12M fresh tokens at the input price and again at the write price; the corrected job-2 totals are Astra $348, Sol $70, Opus 5.5 $130 (Grok $66 and Flash $24 unchanged).

**Facts that expire soon.** Gemini 3.8 Flash $0.75 / $3.75 / $0.075 and the $0.50 per million tokens per hour storage price hold "through December 31, 2026" and double on 2027-01-01 (the video says so in 39yb). OpenAI's page has one promotional note, GPT-5.6 Sol "at least through November 21, 2026", which is not in the video; GPT-6 Sol carries no promotional note. All other prices are undated list prices, dated 2026-09-28 in the video.

**Opinion mismatches (站主觀點).** None. The picks table is titled "My picks, as opinion" and wpuc says "these are opinions, not measurements"; the retry example's hour and rate are declared the owner's in bxqs; msvn matches stance "a new model is not a reason to switch". Not opinion but scope: the brief planned a second table of subscription tiers and a closing link to the cost-quality-latency article; the script has neither (the tooling adds the article link only when a pack exists).

**Listener pass (report only).** No sentence over 25 words; no URL or parenthesis in any narration line; digits appear only in model names and the date. Lint warnings: four lines over 50 spoken units (gjky 52, dsie 52, h2z3 52 from the writer; z6g3 54 after my storage caveat) and the hook chapter at about 41 s against a 30 s target. Reveal before its sentence: the `compare` template shows a whole card per reveal, so at mbxu the left card already displays "At $40 an hour: about $160 more" and "Total about $184" one sentence before pmjw says them; the job1 and job3 footers show Grok $1.98 and Sol $90 from the first frame, before d8vw and gbsu reach them. Light process talk in zeh4 ("read from each company's own pricing page today") and d539 (the previous video's fetch).

**Lint.** `node tools/video/cli.mjs lint --slug gpt6-vs-opus55-worth-paying`: 0 errors, 5 warnings (listed above). 13 scenes and 49 line ids unchanged; no reveals added; JSON re-serialises byte-identically apart from the edits.

**Suspicions left alone.**
- OpenAI says prompt caching is "enabled by default" and implicit caching on GPT-5.6 and later writes the latest eligible message (minimum 1,024 tokens) at 1.25×. A one-off prompt such as job 1 or each job-3 chat could therefore be billed at $12.50 rather than $10 on Astra unless the developer uses explicit-only mode, or gain cache reads on a shared prefix; jobs 1 and 3 stay at the plain input price as list-price arithmetic, and the video does not say this.
- Job 2 on Grok 4.7 uses the under-200k rates; a long agent conversation could cross the threshold ($4 / $1 / $12).
- The Gemini storage charge is stated but not counted; implicit caching avoids it, explicit caches do not.
- The job2-table column "Input + cached" now holds only cached reads for Astra, Sol and Opus 5.5 (their fresh tokens are billed in the "Cache writes" column); the header was kept.
- docs.x.ai is titled "SpaceXAI Docs" today; its pricing page still says "the public xAI API", so "xAI's Grok 4.7" stands.
- The picks row "Cache writes and redo time dominate" is opinion; on the corrected numbers writes are 46% of Opus 5.5's $130.

**Second round.** Required: more than three fact changes (job-2 totals for three models, the formula term, the price-range ratio, the retry figure, the storage caveat).
