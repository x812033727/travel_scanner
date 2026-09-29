# Independent second fact review — ai-agents-explained-what-they-cost

Reviewer: codex-p1-audit (different from the original writer and first independent reviewer). Date: 2026-09-29.

**Second independent factual review complete. Publication remains blocked by owner opinion/outline acceptance, unresolved article CTA and media acceptance. This report does not approve production or publication.**

Input video SHA256: `43c1c3da14cd8b2cb7e4bb0a666a95547834ec63dfd3241f21c9e392ac6c98a8`
Output video SHA256: `011464da52ed357f38894a1d80ce9417ea0ca1b1dcff7e55cf1d9433588cf2c6`

Read the full first-round claim table and changed-field appendix, extracted the full draft, checked every changed/removed fact group against official page bodies opened today, and independently recomputed the arithmetic. Raw HTTP 200 receipts and comment-stripped official text are retained in the audit scratch folder (`video-source-http.json`, `round2-source-*.txt`). Prior author checks are not treated as independent evidence. Random third of first-round CONFIRMED groups, Python Random seed 20260929: a12, c8. Also read the other directly related pricing/limitation passages.

## Claim review

| First-round IDs | Verdict | Official evidence and scope |
|---|---|---|
| c1, c2, a10 | CONFIRMED after corrections | [Agents observability](https://developers.openai.com/api/docs/guides/agents-api/observability) separates model usage, subagents, tools/sandbox and third-party costs. Histories can repeat; caching is conditional. No universal doubling, fixed multiplier or maximum bill claim. Remaining description/summary dependencies fixed below. |
| c3 | CONFIRMED after corrections | [API pricing](https://developers.openai.com/api/docs/pricing): Sol standard short-context 2/10 per million input/output. Five rounds recalculated below, clearly illustrative rather than measured equal-quality work. |
| c6 | CONFIRMED after corrections | [Spend limits](https://developers.openai.com/api/docs/guides/spend-limits): enforce hard limit must be enabled; alerts notify only; organization/project limits return 429, propagation may permit excess usage. Title guarantee narrowed below. |
| a9 | CONFIRMED after corrections | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [Agents overview](https://developers.openai.com/api/docs/guides/agents-api/overview): tools and dynamic control matter; sandbox is an execution option, not mandatory for all agents. |

Confirmed sample and related limitations: the Anthropic article distinguishes predefined workflows from dynamically selected steps/tools; OpenAI Agents API overview specifies US residency and no ZDR (including self-hosted sandbox), separate third-party tool boundaries; observability explicitly calls token usage best effort, possibly null, mutable and not the final bill. These product-specific rules are not generalized to every agent.

## Independent arithmetic

Inputs `[20000, 45000, 75000, 110000, 150000]`, outputs `[2000, 2500, 3000, 3000, 4000]`; Decimal token fees `['0.06', '0.115', '0.18', '0.25', '0.34']` total `0.945` USD. Input total 400000, output14500; .945/.06 = 15.75 (rounded16). Input cost .8/.945 = 84.656%, so the revised summary is true only for this illustrative scenario. No cache/tool/sandbox/third-party charges included.

## Second-round dependency corrections

| JSON path | Before | After |
|---|---|---|
| `/youtube/title` | AI 代理是什麼、跑一次多少錢，以及那個能阻止它亂花錢的設定 | AI 代理是什麼、跑一次多少錢，以及控制預算前該確認的設定 |
| `/youtube/description` | AI 代理到底是什麼、為什麼同一件事做成代理會貴十幾倍、委託前該問什麼。這支用一個五輪代理的帳單示意，把錢花在哪講清楚。<br>給常聽到「AI 代理」「自動化」，但分不清它跟聊天差在哪、又怕帳單失控的人。<br><br>涵蓋聊天、固定流程與代理的差別、代理由模型加指示加工具加環境組成、每輪重讀歷史為何讓成本暴增、委託時要問的權限紀錄停止與預算，以及資料落地與零資料保留兩個合規限制。表格數字為示意，用來說明結構。<br>五輪帳單是 token 費用示例，未計快取、工具、沙箱或第三方費用。OpenAI API 硬支出上限須啟用且可能有延遲，不能保證完全不超額。 | AI 代理到底是什麼、多輪呼叫如何增加費用、委託前該問什麼。這支用一個五輪代理的帳單示意，把錢花在哪講清楚。<br>給常聽到「AI 代理」「自動化」，但分不清它跟聊天差在哪、又怕帳單失控的人。<br><br>涵蓋聊天、固定流程與代理的差別、模型、指示、工具與執行環境等常見部分、反覆處理歷史可能如何增加成本、委託時要問的權限紀錄停止與預算，以及資料落地與零資料保留兩個合規限制。表格數字為示意，用來說明結構。<br>五輪帳單是 token 費用示例，未計快取、工具、沙箱或第三方費用。OpenAI API 硬支出上限須啟用且可能有延遲，不能保證完全不超額。 |
| `/scenes/9/lines/5/text` | 這就是為什麼代理的帳單，重點在重讀的歷史。 | 這個示例的費用，主要來自反覆處理的輸入。 |

These are residual wording dependencies of the first-round facts, grouped into at most two factual issues (not new scenes or opinion rewrites); no third round threshold is triggered. Scene/line IDs, reveals, brief and shared lexicon remain unchanged. No edited line contains a say override.

## Remaining acceptance

No independent performance benchmark, population study or live source-article CTA acceptance was performed. First-round opinion/brief conflicts remain owner decisions. Official rates and beta capabilities expire: recheck before TTS/publication. Listener findings from round one remain report-only; no audio, image, caption, render or player acceptance is implied. Scoped lint must pass with zero errors before handoff; its final result is recorded below.

## Commit-byte receipt

Final lint on Node 24.21.0: exit 0, 0 errors and 0 warnings; 105 lines, estimated 8.6 minutes. No synthesis or render was run.

Final `video.json` SHA-256 with repository LF line endings: `011464da52ed357f38894a1d80ce9417ea0ca1b1dcff7e55cf1d9433588cf2c6`. Use this final hash for handoff and invalidate any older media/approval bound to a different script.
