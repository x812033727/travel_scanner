# Claims: always-on-agent-explained

Written 2026-09-28 (writer: claude-fable-5-1). Format: `id｜claim｜source URL｜checked｜scene`.

c1｜Demo run, 2026-09-28, Claude Code 2.1.283, tools WebFetch and Write only: the agent planned in one line, made three WebFetch calls (Anthropic page: $4 in / $20 out; openai.com page: HTTP 403; xAI docs: Grok 4.7 $2.00 / $6.00 under 200k), wrote prices.md with the failed model's cells blank and reported in two sentences; 5 turns, 22,116 ms｜demo-log.md in this folder｜2026-09-28｜task, moves, result, shows
c2｜Claude Opus 5.5 scores 81.8% (partial) on OSWorld 2.0, per Anthropic｜https://www.anthropic.com/news/claude-opus-5-5｜2026-09-28｜fail
c3｜OpenAI publishes an OSWorld 2.0 score for GPT-6 Astra on its launch page, lower than 81.8% (third-party write-ups of the page give 72.6%; the script states no figure because the page answered HTTP 403 to our fetcher)｜https://openai.com/index/gpt-6-astra/ (403 on 2026-09-28; secondary: https://www.datacamp.com/blog/gpt-6-astra)｜2026-09-28｜fail
c4｜NVIDIA and Microsoft's Windows agent framework runs agents "safely in the background under OS level control"｜https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/｜2026-09-28｜always-on
c5｜OpenAI DevDay is 2026-09-29; a persistent "always-on" OpenAI assistant was reported from code leaks and a teaser, not announced, as of 2026-09-28｜https://openai.com/index/devday-2026/ ; report: https://www.testingcatalog.com/openai-to-announce-o-always-on-agent-during-devday/｜2026-09-28｜always-on
c6｜Claude Opus 5.5 API price: $4 per million input tokens, $20 per million output｜https://www.anthropic.com/news/claude-opus-5-5｜2026-09-28｜result
c7｜Grok 4.7: $2.00 input / $6.00 output per million tokens for prompts under 200k tokens｜https://docs.x.ai/docs/models｜2026-09-28｜result
c8｜The openai.com GPT-6 Astra page answered HTTP 403 to the agent's fetch during the run｜demo-log.md｜2026-09-28｜result
c9｜Chatbot versus agent framing (goal, tools, loop, stop) and the four failure shapes are the owner's explanation, not a measurement｜brief.md 站主觀點｜2026-09-28｜difference, three-words, shapes

## 與企劃不同的地方

- DevDay had not happened on writing day, so the script uses the brief's fallback: the hook is the "everyone is building always-on agents" line and the always-on chapter labels OpenAI's assistant as a report. **Before TTS, on or after 2026-09-29, update `always-on` (lines xc6d and the fourth bullet) with what DevDay actually announced, or leave the wording if nothing shipped.**
- The GPT-6 Astra OSWorld figure is not spoken or shown because the official page could not be read; the stats card carries Anthropic's number only. If a verifier opens the OpenAI page, add the figure to the card and to line u5vx.

## 我懷疑但沒動的事

- "Approximately one in five tasks not fully completed" is the complement of 81.8% partial credit; partial credit means the benchmark counts partly finished tasks, so "not fully completed" is the safe reading. A verifier may prefer "about one task in five loses points".
- The last-week headlines referenced in vaxb and gb65 are video 1's story (OpenAI's agents and government sites), so the order of release matters: this video assumes video 1 is public.

## 進度

All 14 scenes written; lint pending in this session. Awaiting verification round 1.
