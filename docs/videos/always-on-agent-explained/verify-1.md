# Verify round 1: always-on-agent-explained

Checked 2026-09-28 by claude-fable-5-1 (not the writer's session). Every page was fetched with `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`, one request per host at a time, plus one WebFetch and three web searches. demo-log.md is the channel's own record of the run and counts as primary for the run's numbers; third-party pages never confirm a number. Saved copies of every page are in the verifier's helper folder (`scratchpad/verify-always-on-agent-explained/pages/`).

## Claim table

| # | Claim | Where | URL | HTTP | Verdict | Before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | "Chatbots Are Over. Here's How an AI Agent Actually Works (and Fails)." | youtube.title | — | — | OUT OF SCOPE | framing, no number |
| 2 | "records one real AI agent run, step by step" | youtube.description | demo-log.md | — | CONFIRMED | — |
| 3 | "a coding agent asked to read three official pricing pages and write a table" | youtube.description | demo-log.md (prompt) | — | CONFIRMED | — |
| 4 | "every tool call, the one page that refused, and the file it wrote are shown as they happened on 2026-09-28" | youtube.description | demo-log.md | — | CONFIRMED | true now that the `result` slide carries all four rows of prices.md (see #41) |
| 5 | "The computer-use score on screen is Anthropic's own for Claude Opus 5.5" | youtube.description | https://www.anthropic.com/news/claude-opus-5-5 | 200 (→ /claude-opus-5-5) | CONFIRMED | — |
| 6 | "OpenAI's score for GPT-6 Astra is on its launch page, linked below" | youtube.description | https://openai.com/index/gpt-6-astra/ | 403 (curl and WebFetch) | NOT FOUND ON OFFICIAL PAGE | kept by instruction (c3); no official OpenAI page that answers carries an OSWorld figure for Astra: system card, safety overview, developer model page, model guide, community announcement all checked |
| 7 | "Reports about OpenAI's next assistant are labelled as reports" | youtube.description | video.json xc6d, always-on bullet 4 | — | CONFIRMED | wording says "reported", "a report, not an announcement" |
| 8 | "Recorded 2026-09-28" | youtube.description | demo-log.md | — | CONFIRMED | — |
| 9 | "linked below" / "Both pages are linked in the description" (u5vx) | description, fail.u5vx | tools/video/core/metadata.mjs composeDescription appends `sources` | — | CONFIRMED | sources[0] and sources[2] are appended to the description; the log-link promise is #48 |
| 10 | tags "Claude Code", "OpenAI DevDay" | youtube.tags | https://code.claude.com/docs/en/cli-reference ; https://devday.openai.com/ | 200 ; 200 | CONFIRMED | — |
| 11 | "CHATBOT vs AGENT", "one real run, five moves" | thumbnail | video.json moves (5 steps), demo-log.md | — | CONFIRMED | — |
| 12 | category_id 28 | youtube | docs/videos/README.md (分類 28 科學與技術) | — | CONFIRMED | — |
| 13 | "Anthropic: Introducing Claude Opus 5.5 (OSWorld 2.0 81.8% partial; API prices)" | sources[0] | https://www.anthropic.com/news/claude-opus-5-5 | 200 (redirects to anthropic.com/claude-opus-5-5) | CONFIRMED | page dated September 22, 2026; "Computer use, OSWorld 2.0, partial, 81.8%"; "$4 and $20 per million" |
| 14 | "OpenAI: GPT-6 Astra model page (price, context window)" | sources[1] | https://developers.openai.com/api/docs/models/gpt-6-astra | 200 | CONFIRMED | $10 / $50 per 1M, 1,050,000 context window (not shown in the video) |
| 15 | "OpenAI: GPT-6 Astra launch page (its OSWorld 2.0 score)" | sources[2] | https://openai.com/index/gpt-6-astra/ | 403 | NOT FOUND ON OFFICIAL PAGE | kept by instruction; the page exists in search listings ("GPT-6 Astra: A new generation of intelligence") but its content, and whether it carries an OSWorld score, could not be read |
| 16 | "xAI: models and pricing (Grok 4.7)" | sources[3] | https://docs.x.ai/docs/models | 200 (redirects to docs.x.ai/developers/models) | CONFIRMED | Grok 4.7 "$2.00 / 1M tokens" input, "$6.00 / 1M tokens" output |
| 17 | "NVIDIA: Sparks Fly, local AI at IFA 2026 (the Windows agent framework)" | sources[4] | https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/ | 200 | CONFIRMED | title "Sparks Fly: NVIDIA Accelerates Local AI at IFA 2026", September 3, 2026 |
| 18 | "OpenAI: Announcing DevDay 2026" | sources[5] | https://openai.com/index/devday-2026/ → https://devday.openai.com/ | 403 → 200 | CHANGED | link replaced by OpenAI's own DevDay page, which states "Tuesday, September 29, 2026", Fort Mason, San Francisco, keynote 10:00 a.m. with Sam Altman |
| 19 | "Claude Code CLI reference (the flags used in the run)" | sources[6] | https://code.claude.com/docs/en/cli-reference | 200 | CONFIRMED | `-p`/`--print`, `--tools`, `--allowedTools`, `--max-turns`, `--output-format` (text, json, stream-json), `--verbose` all present |
| 20 | "Every AI company is now selling you an agent, and next ... one that never logs off" | hook.hx5y | — | — | OUT OF SCOPE | rhetorical generalisation; consistent with the brief's hook |
| 21 | "Most explanations stop at: it can use tools" | hook.prkk | — | — | OUT OF SCOPE | opinion |
| 22 | "I gave one agent a boring task and recorded every step ... five moves" | hook.7iga | demo-log.md; moves slide | — | CONFIRMED | — |
| 23 | "tasks that still go wrong, by the makers' own numbers" | hook.bdiv | anthropic page (c2) | 200 | CONFIRMED | — |
| 24 | chatbot vs agent (compare slide, hpt2, db9w, p7nm, qvb8) | difference | brief.md 站主觀點 (c9) | — | OUT OF SCOPE | owner's framing, marked as such in claims.md |
| 25 | "That is how you get last week's headlines" | three-words.vaxb (also shapes.gb65) | https://www.nextgov.com/cybersecurity/2026/09/openai-says-its-advanced-models-may-have-gone-after-government-websites/416250/ | 200 | CONFIRMED | headline dated September 25, 2026, "UPDATED Saturday, Sept. 26"; 2026-09-28 is the following Monday |
| 26 | Owner: "Find three official prices, write a table." | task.data.messages[0] | demo-log.md prompt | — | CONFIRMED | paraphrase of the prompt |
| 27 | Agent: "I'll fetch each of the three pages." | task.data.messages[1] | demo-log.md step 1 | — | CONFIRMED | first clause of "I'll fetch each of the three pages to look for pricing information." |
| 28 | "find three official model prices and write a table" | task.eyuh | demo-log.md prompt | — | CONFIRMED | — |
| 29 | "named the three pages ... leave blank any cell it could not read ... never to guess a number" | task.uf2w | demo-log.md prompt ("using only these pages", "leave its cells blank; never guess a number") | — | CONFIRMED | — |
| 30 | "its plan in one line: I will fetch each of the three pages" | task.6gvp | demo-log.md step 1 | — | CONFIRMED | — |
| 31 | "Three fetches, three pages" | moves.steps[1] | demo-log.md steps 2–4 | — | CONFIRMED | — |
| 32 | "Two answers, one 403 error" | moves.steps[2] | demo-log.md | — | CONFIRMED | — |
| 33 | "Writes the table, blanks the failed one" | moves.steps[3] | demo-log.md step 5, prices.md | — | CONFIRMED | — |
| 34 | "What it did, what it could not" | moves.steps[4] | demo-log.md step 6 | — | CONFIRMED | — |
| 35 | "it fetched all three pages we had named" | moves.6ifa | demo-log.md | — | CONFIRMED | three WebFetch calls; the refusal is stated in the next line (loose wording, left alone) |
| 36 | "Two pages answered with prices. The third refused with a 403 error, access forbidden." | moves.zdw7 | demo-log.md ("HTTP 403 Forbidden") | — | CONFIRMED | — |
| 37 | "wrote the table and left the failed model's cells blank" | moves.n96a | prices.md in demo-log.md | — | CONFIRMED | — |
| 38 | "two sentences ... Five turns, twenty two seconds" | moves.9e9d | demo-log.md ("5 turns, 22,116 ms"; step 6 is two sentences) | — | CONFIRMED | — |
| 39 | Claude Opus 5.5 · $4 · $20 · Anthropic's announcement | result.rows[0] | demo-log.md; https://www.anthropic.com/news/claude-opus-5-5 | 200 | CONFIRMED | matches the file and today's page |
| 40 | GPT-6 Astra · — · — · "Page returned 403; not read" | result.rows[1] | demo-log.md; https://openai.com/index/gpt-6-astra/ | 403 today too | CONFIRMED | — |
| 41 | Grok 4.7, under 200k · $2.00 · $6.00 · xAI model docs; the file's fourth row | result.rows[2], rows[3] | demo-log.md; https://docs.x.ai/developers/models/grok-4.7 | 200 | CHANGED (table) | row 3 confirmed on the page ("$2.00 / 1M tokens", "$6.00 / 1M tokens", "different rates for requests which exceed the 200K context window"); the slide had dropped the file's fourth row, added: "Grok 4.7, 200k and over · $4.00 · $12.00 · xAI model docs" as the agent wrote it (the higher tier sits in a collapsed Details block on the page, not readable statically) |
| 42 | "Two rows filled ... One row honest about being empty" | result.qpg5 | prices.md in demo-log.md (four rows, three filled) | — | CHANGED | "Two rows filled" → "Three rows filled" |
| 43 | "An agent that guesses when a page fails is an agent you cannot use" | result.6zh7 | brief.md 站主觀點 | — | OUT OF SCOPE | opinion, consistent with the stance |
| 44 | Agent: "I fetched two pages and wrote their prices." / "The third page returned 403, so I left it blank." | report.data.messages | demo-log.md step 6 | — | CONFIRMED | paraphrase of the two-sentence report (not verbatim; the slide is labelled as its report) |
| 45 | "in two sentences we had asked for" | report.5dmh | demo-log.md prompt ("Finish with two sentences") | — | CONFIRMED | — |
| 46 | "The page refused, so I left it blank, rather than guessing." | report.2ph2 | demo-log.md step 6 | — | CONFIRMED | paraphrase |
| 47 | 5 turns · 3 pages fetched (one refused) · 1 file written · 22 s | run-numbers.stats | demo-log.md (22,116 ms) | — | CONFIRMED | — |
| 48 | "Recorded 2026-09-28 with two tools allowed; the log is linked in the description" | run-numbers.data.source | video.json sources; composeDescription | — | CHANGED | the description carries only `sources`, none of which is the log → "Recorded 2026-09-28 with two tools allowed: one to fetch pages, one to write files" |
| 49 | "five turns, three pages fetched, one of them refused, one file written, twenty two seconds" | run-numbers.6wdb | demo-log.md | — | CONFIRMED | — |
| 50 | "a failure became a blank cell, not an invented number, because we said so up front" | shows | demo-log.md prompt | — | CONFIRMED | — |
| 51 | 81.8% · Claude Opus 5.5 on OSWorld 2.0 · "partial credit, as Anthropic reports it" | fail.stats[0] | https://www.anthropic.com/news/claude-opus-5-5 | 200 | CONFIRMED | page: "OSWorld 2.0 · partial · 81.8%"; "partial" is the page's only qualifier, "partial credit" is the script's gloss |
| 52 | "≈ 1 in 5 tasks not fully completed, at that score" | fail.stats[1] | arithmetic | — | CONFIRMED | 100 − 81.8 = 18.2% ≈ one in 5.5; with partial scores the share of tasks short of full completion is at least 18.2%, so "about one in five" is a rounded lower bound |
| 53 | "anthropic.com, 2026-09-22; OpenAI's GPT-6 Astra score is on its launch page" | fail.data.source | anthropic page | 200 | CONFIRMED (date) | page dated September 22, 2026; the OpenAI half is #56 |
| 54 | "how often their agents finish tasks on a real computer, on a benchmark called OSWorld" | fail.gxyd | https://os-world.github.io/ (→ osworld-v1.xlang.ai) | 200 | CONFIRMED | "real computer environment for multimodal agents"; "2026-06-26: OSWorld 2.0 is now available" |
| 55 | "Anthropic reports 81.8 percent for Claude Opus 5.5, with partial credit ... about one task in five is not fully done" | fail.73y9 | anthropic page | 200 | CONFIRMED | see #51, #52 |
| 56 | "OpenAI publishes a score for GPT-6 Astra on its launch page too, and it is lower." | fail.u5vx | https://openai.com/index/gpt-6-astra/ ; https://deploymentsafety.openai.com/gpt-6-astra ; .../safety-overview-gpt-6-astra ; developer model page and guide | 403 ; 200 ; 200 ; 200 | NOT FOUND ON OFFICIAL PAGE | kept by instruction: the script states no figure. Neither "publishes a score on its launch page" nor "lower" could be confirmed; Anthropic's table shows "—" for Astra on OSWorld 2.0 |
| 57 | four failure shapes | shapes | brief.md 站主觀點 (c9) | — | OUT OF SCOPE | owner's taxonomy; the "last week" reference in gb65 is #25 |
| 58 | "It runs in the background under the operating system's control, NVIDIA and Microsoft say" / txqe | always-on.items[2], txqe | https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/ ; https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/ | 200 ; 200 | CHANGED | the sentence is NVIDIA's ("Paired with the new Windows Agent framework, it enables agents that run safely in the background under OS level control"); Microsoft's own blog describes OS-enforced containment (MXC) but not "background" or that framework name → bullet "…NVIDIA says of the new Windows agent framework"; txqe "NVIDIA says the new Windows agent framework, part of its work with Microsoft, runs such agents in the background, under the operating system's control." |
| 59 | "A persistent OpenAI assistant: reported, not announced, as we record" / xc6d "widely reported" | always-on.items[3], xc6d | https://www.testingcatalog.com/openai-to-announce-o-always-on-agent-during-devday/ ; https://devday.openai.com/ | 200 ; 200 | PLAUSIBLE-VIA-REPORT | TestingCatalog 2026-09-26 reports "O" from ChatGPT configuration strings and an upgrade-page mention, citing an @OpenAIDevs "72 hours to OpenAI DevDay" post; DevDay 2026-09-29 confirmed on OpenAI's page; the script labels it a report and does not name the product |
| 60 | "the next step everyone is building" | always-on.sy22 | — | — | OUT OF SCOPE | rhetorical |
| 61 | "Last video was about the three walls ... tools, network, secrets" | walls-cta.7w3r | docs/videos/openai-agents-broke-in/video.json (`walls`, `outro`) | — | CONFIRMED | video 1 has no video_id yet; release order matters |
| 62 | three questions; bad ask / good ask | questions, delegation | brief.md 觀眾看完能做到的事 | — | OUT OF SCOPE | advice, matches the brief |
| 63 | "Next time, the same agent priced three models for us." | outro.p8zt | docs/videos/gpt6-vs-opus55-worth-paying/video.json, claims.md | — | CHANGED | the next video prices five models from the vendors' pages (two with the numbers this run found); this run priced two of three → "Next time, we start from the prices this agent found and I will show you which model is actually worth paying for." |
| 64 | "Next: which AI is actually worth paying for" | outro.data.lines[2] | video 3 title | — | CONFIRMED | — |
| 65 | voice Gemini "Sulafat" | voice | — | — | OUT OF SCOPE | configuration, not spoken |
| 66 | Claude Code 2.1.283 | claims.md c1 (not spoken) | https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | 200 | CONFIRMED | top entry of the changelog today |

## Summary

**Counts (66 rows):** CONFIRMED 47 · CHANGED 6 rows (5 distinct edits: the `result` table row and qpg5 count as one fact) · NOT FOUND ON OFFICIAL PAGE 3 (#6, #15, #56, all one claim, c3, kept by instruction) · PLAUSIBLE-VIA-REPORT 1 (#59) · OUT OF SCOPE 9.

**Fact changes in the script (4):** the `result` table now shows all four rows of prices.md and qpg5 says "Three rows filled"; the `run-numbers` source line no longer promises a log link the description does not carry; `always-on` bullet 3 and txqe attribute the background / OS-control sentence to NVIDIA (Microsoft named as the partner, not as a speaker); p8zt no longer says the same agent priced three models. Plus one source fix: `sources[5]` now points at https://devday.openai.com/ (HTTP 200) instead of the 403 openai.com URL. claims.md updated (c1–c7, new c10–c12, 進度).

**Expires soon:** OpenAI DevDay is tomorrow, 2026-09-29 (Fort Mason, keynote 10:00 Pacific, per devday.openai.com): re-check the always-on chapter (bullet 4, xc6d) and the "always-on" tag before TTS. NVIDIA's post (2026-09-03) gives no ship date for the Windows Agent framework itself; the RTX Spark Windows PCs it pairs with "arrive October 2026"; Microsoft's containment (MXC) was "available today in Windows Insider builds, with more coming through our developer preview program" on 2026-06-02. All prices are as of today. Video 1 (the "last week" headlines, the three walls) must be public before this one.

**Opinion check:** every opinion is voiced as the owner's and matches 站主觀點 (evidence first, boundaries before magic, "one task in four or five"). No mismatch. Note the brief states Astra's 72.6% as fact from DataCamp; the script rightly omits it (c3 unconfirmed), and the DataCamp page itself answered 403 today.

**Listener pass (report only):** no sentence over 25 words (7iga is two sentences, 52 spoken units in one line, lint WARN); hook chapter about 42 s (lint WARN, pre-existing); mild self-reference "from this video" (agxs) and time marker "As we record" (xc6d), neither in the lint list; no URLs or parentheses in narration; reveal counts equal item counts in every scene and no reveal precedes its sentence.

**Lint:** `node tools/video/cli.mjs lint --slug always-on-agent-explained` → 0 errors, 2 warnings (both pre-existing, above). Estimate 8.6 min.

**Suspicions left alone:** (1) c3: u5vx, the description and `sources[2]` still assert OpenAI "publishes a score ... on its launch page" and that it is "lower"; unverifiable today, kept by instruction — round 2 should retry the page or soften to "OpenAI's own page is linked in the description". (2) "≈ 1 in 5" rounds 18.2% (one in 5.5) and is a lower bound under partial scoring. (3) 6ifa "fetched all three pages" although one refused (clarified in the next line). (4) The report slide's two messages are paraphrases, not quotes. (5) Anthropic's qualifier is the single word "partial"; "partial credit" is a gloss. (6) Video 3's `agent-cta` slide says "The agent that read these price pages for us", which this run did not do for three of its five models — fix in video 3, not here. (7) The demo log has no public URL in `sources`; add one before publishing if the owner wants the log linked. (8) sources[0] and sources[3] redirect (anthropic.com/claude-opus-5-5; docs.x.ai/developers/models); both fine for viewers.

**SECOND ROUND: required** (four fact changes, more than three).
