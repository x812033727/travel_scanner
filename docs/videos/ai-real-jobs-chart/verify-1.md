# Verification round 1: ai-real-jobs-chart

Verifier: claude-opus-5-5, a separate session from the writer's, 2026-09-28. Every number was read today on the official or primary page with the editorial user agent (curl, comments, scripts and tags stripped; at least 1 s between requests to one host). The Challenger PDF and the RLI paper PDF were read as text through a scratchpad-only `pypdf`. Third-party pages were used only to find out what the February video said, never to confirm a number. Web searches used: 2 of 5. Helper files: `/tmp/claude-0/-home-user-travel-scanner/674d9bf2-c3b1-5d19-bf6c-31efd377fe1e/scratchpad/verify-ai-real-jobs-chart/` (claims-list.md written before checking, raw-strings.txt, pages/, fetch-log.txt, leaderboard-entries.txt, listener.py, video.before.json, claims.before.md).

## Pages fetched

| URL | HTTP | What it gave |
| --- | --- | --- |
| https://labs.scale.com/leaderboard/rli | 200 | Live table plus the page's own entry data (`score`, `isNew`, `createdAt`, `deprecated`); method text (automation rate, 3-point scale, "trained experts", failure modes, Manus 2.5% at launch) |
| https://scale.com/blog/rli | 200 | Launch post, October 29, 2025: 240 projects, 23 domains, median 11.5 h and $200, "earned a combined $143,991", "45.6% of failed submissions…" |
| https://arxiv.org/abs/2510.26787 | 200 | Abstract, v1 submitted 30 Oct 2025, best 2.5% |
| https://arxiv.org/html/2510.26787v1 | 200 | Full paper: sourcing (§3.2, App. C), evaluation (§3.3), failure modes (§4.3, Table 2), 23 subcategories |
| https://www.remotelabor.ai/paper.pdf | 200 | Same paper (PDF created 2025-10-29): best 2.5%, "trained workers and subject experts", Table 2 over "roughly 400 evaluations" |
| https://www.remotelabor.ai/ | 200 | Project site; its leaderboard loads by script and shows no rows to a fetcher (not used for numbers) |
| https://safe.ai/blog/significant-increase-in-digital-labor-automation | 200 | CAIS post, July 1, 2026: Fable 5 15.8%, Opus 4.8 8.3%, GPT-5.5 6.3%, "previous published leader sat at 4.17%", examples, grader table, "stays out of reach" |
| https://www.challengergray.com/blog/challenger-report-august-job-cuts-up-58-consumer-products-food-lead/ | 200 | Web post, "Publication date: Sep 02"; AI paragraph |
| https://www.challengergray.com/wp-content/uploads/2026/09/Challenger-Report-August-2026.pdf | 200 | The report: "FOR RELEASE AT 5:30 A.M. ET, THURSDAY, SEPTEMBER 3, 2026", "CHICAGO, September 3, 2026"; Table 4 (reasons) |
| https://www.onetonline.org/link/summary/13-1161.00 | 200 | 13 task statements, "Updated 2026", "Site updated August 25, 2026", CC BY 4.0 credit to the U.S. Department of Labor, Employment and Training Administration |
| https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=z3kaLM8Oj4o&format=json | 200 | YouTube's own endpoint: title "AI Fails at 96% of Jobs (New Study)", channel ColdFusion |
| https://www.youtube.com/watch?v=z3kaLM8Oj4o | 200 | Visible text is only the footer, and the player data is login-gated; the page's embedded data still gives the title, "Feb 13, 2026", 969,789 views, and the description (links the RLI paper; no percentage) |
| https://open.spotify.com/episode/4QFBt9Fu0ZtuHRyjrGGevg | 200 | ColdFusion's own podcast episode of the same title, `music:release_date` 2026-02-12T16:21:00Z |
| https://recapio.com/digest/ai-fails-at-96-of-jobs-new-study-by-coldfusion | 200 | Third-party summary (meta description): "worse than humans in 96.25% of real-world job tasks" |
| https://codehelper.me/articles/ai-automation-reality-check/ | 200 | Third-party article of 16 February 2026 prompted by the video: "fail to match human quality on 96.25%", "Claude Opus 4.5: 3.75% success rate (best performer)" |
| https://aatventure.news/posts/coldfusion-ai-fails-at-96-of-jobs | 200 | Aggregator page; nothing on the figure (not used) |
| https://podcasts.apple.com/ca/podcast/ai-fails-96-of-real-freelance-jobs-coldfusion-3-min-summary/id1848404899?i=1000749617485 | 200 | Redirects to the show page, which no longer lists the episode (not used) |

Search results only (not fetched): CAIS's X post of 2026-07-01 16:45 UTC (status id decoded) announcing Fable 5 at "16.1%", and ColdFusion's X announcement of the video, 2026-02-12 23:49 UTC.

Leaderboard entries as served today (from the page data):

| Entry | Score | Badge | Added (`createdAt`) |
| --- | --- | --- | --- |
| GPT 6 Astra | 20.83 | NEW | 2026-09-17 |
| Fable 5.1 (Anthropic) | 17.92 | NEW | 2026-09-17 |
| Fable 5 | 15.80 | — | 2026-07-01 |
| Opus 4.8 | 8.33 | — | 2026-07-01 |
| Codex GPT 5.5 | 6.25 | — | 2026-07-01 |
| Gemini 3.7 Flash | 5.00 | — | 2026-08-24 |
| claude-opus-4-6 (CoWork) | 4.17 | — | 2026-03-05 |
| claude-opus-4-5-20251101-thinking | 3.75 | — | 2026-01-09 |
| Manus_1.6 (Max) | 2.92 | — | 2026-03-05 |
| gpt-5.2-2025-12-11 (medium) | 2.50 | — | 2026-01-29 |
| Manus 1.5 / Manus 1.0 | 2.50 / 2.50 | — | 2025-11-21 / 2025-10-27 |

Lower entries (2.08 and below) are all under 2.5. No entry is marked provisional or preliminary, none is deprecated or carries a contamination message, and the legend says "There is no confidence interval for Automation Rate."

## Claim table

| # | Claim | Where | URL | HTTP | Verdict | Before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | "AI Can Now Do 21% of Real Freelance Jobs. Last October It Was 2.5%." (20.83% rounded; launch best 2.5%) | youtube.title | labs.scale.com/leaderboard/rli; scale.com/blog/rli | 200 | CONFIRMED | — |
| 2 | 240 real, paid freelance projects; best AI from 2.5% to 20.83% "at a quality a client would accept", in eleven months | youtube.description | scale.com/blog/rli; leaderboard | 200 | CONFIRMED | — |
| 3 | RLI "by Scale AI and the Center for AI Safety"; leaderboard read 2026-09-28; "the August 2026 job-cuts report" from Challenger; recorded 2026-09-28 | youtube.description | scale.com/blog/rli; safe.ai post; challengergray.com | 200 | CONFIRMED | — |
| 4 | Tags "GPT-6 Astra", "Claude Fable 5" name real leaderboard entries | youtube.tags | leaderboard | 200 | CONFIRMED | — |
| 5 | "REAL PAID WORK", "2.5% → 21%", "in eleven months" | thumbnail.data | leaderboard; scale.com/blog/rli | 200 | CONFIRMED | — |
| 6 | Seven source titles, URLs and `checked_on` 2026-09-28; ColdFusion id z3kaLM8Oj4o, title, February 2026 | sources | all of the above; YouTube oEmbed | 200 | CONFIRMED | Source added as a dependant of #50: the Challenger PDF (the corrected date rests on it) |
| 7 | "AI can now do 21% of real freelance jobs"; "Last October it was 2.5%" | hook.data | leaderboard; scale.com/blog/rli | 200 | CONFIRMED | — |
| 8 | In February, one widely shared video said AI fails at 96% of real jobs | hook/eqsu | YouTube oEmbed and page data; Spotify episode | 200 | CONFIRMED | — (title "AI Fails at 96% of Jobs (New Study)"; YouTube shows Feb 13, 2026, and the channel's Spotify episode and X post are 2026-02-12 UTC; 969,789 views) |
| 9 | "It was right, at the time." | hook/eqsu | leaderboard page data | 200 | CONFIRMED | — (the best score from 2026-01-09 to 2026-03-05 was 3.75%, so 96.25% of projects were not automated) |
| 10 | The best AI now finishes about 21% of real paid projects; last October two and a half | hook/z8yk | leaderboard; scale.com/blog/rli | 200 | CONFIRMED | — |
| 11 | Scale AI and the Center for AI Safety built the RLI | test/xjp3 | scale.com/blog/rli; safe.ai post ("jointly developed by the Center for AI Safety and Scale Labs"); arXiv | 200 | CONFIRMED | — |
| 12 | "240 real projects that people had paid freelancers to do"; "240 paid jobs from freelance sites" | test/nsjk, test.data.steps[0] | scale.com/blog/rli ("real-world, paid freelance projects"); arXiv HTML §3.2 | 200 | CONFIRMED | — (the launch post's wording; the paper says "the majority", see suspicions) |
| 13 | 23 kinds of work | test/nsjk, test.data.steps[1].title | scale.com/blog/rli ("23 domains"); arXiv App. C ("23 Upwork subcategories") | 200 | CONFIRMED | — |
| 14 | "Design, 3D, data, video, audio, code" | test.data.steps[1].detail | arXiv App. C (Graphic & Editorial Design, 3D Modeling & CAD, Data Analysis & Testing, Video & Animation, Audio & Music Production, Web Development, Game Design & Development…) | 200 | CONFIRMED | — |
| 15 | Each AI gets the same brief and the same files the freelancer got | test/hkyj, test.data.steps[2] | arXiv §3.1 ("the brief and input files are provided by the professional"), §3.3, App. C.2 ("similar or identical phrasing to original client requests") | 200 | CONFIRMED | — |
| 16 | Human judges ask: as good as the professional's work, good enough that a client would accept it? | test/mafu, test.data.steps[3] | arXiv §3.3 (3-point scale, "would be accepted by a reasonable client as the commissioned work"; "performed manually by trained workers and subject experts"); leaderboard | 200 | CONFIRMED | — |
| 17 | 240 projects | stakes.data.stats[0], stakes/h865 | scale.com/blog/rli | 200 | CONFIRMED | — |
| 18 | 11.5 h median time for a professional | stakes.data.stats[1], stakes/qarp | scale.com/blog/rli; leaderboard ("Median: 11.5 hours"); arXiv | 200 | CONFIRMED | — |
| 19 | $200 median value ("paid about two hundred dollars") | stakes.data.stats[2], stakes/qarp | scale.com/blog/rli; leaderboard ("Median: $200") | 200 | CONFIRMED | — |
| 20 | $143,991 "paid to the humans, in total"; "the humans who did them earned about one hundred forty four thousand dollars" | stakes.data.stats[3], stakes/dr78 | scale.com/blog/rli ("earned a combined $143,991") | 200 | CONFIRMED | — (paper's cost definition noted in suspicions) |
| 21 | Source line "Scale AI and the Center for AI Safety, October 2025" | stakes.data.source | scale.com/blog/rli (October 29, 2025) | 200 | CONFIRMED | — |
| 22 | Automation rate = share of projects where the AI's work was judged as good as the human's, or better | stakes/x4it | leaderboard; safe.ai post (same wording); arXiv §3.3 | 200 | CONFIRMED | — |
| 23 | Chapter "The curve: 2.5% to 21% in eleven months"; title "Best automation rate on the leaderboard" | curve.chapter, curve.data.title | leaderboard | 200 | CONFIRMED | — |
| 24 | Oct 2025, launch: Manus 2.5%, "the best system, an agent called Manus" | curve.data.rows[0], curve/raaw | scale.com/blog/rli; leaderboard (Manus 1.0 added 2025-10-27) | 200 | CONFIRMED | — |
| 25 | Feb 2026: best 3.75%, Claude Opus 4.5 thinking | curve.data.rows[1], curve/cign | leaderboard page data (added 2026-01-09; next higher entry, Opus 4.6 CoWork 4.17%, added 2026-03-05); safe.ai post ("previous published leader sat at 4.17%") | 200 | CONFIRMED | — (the Feb row and cign stand) |
| 26 | "That's where the ninety six percent headline came from." | curve/cign | leaderboard; YouTube title; recapio.com and codehelper.me (third-party, for the video's 96.25%) | 200 | CONFIRMED | — (100 − 3.75 = 96.25; no other February leaderboard score rounds to 96) |
| 27 | Jul 2026: Claude Fable 5 15.8%, "the Center for AI Safety reported" | curve.data.rows[2], curve/dgig | safe.ai post (July 1, 2026, "15.8%"); leaderboard (15.80, added 2026-07-01) | 200 | CONFIRMED | — (CAIS's X announcement said 16.1%, see suspicions) |
| 28 | Sep 28, 2026: GPT-6 Astra 20.83%, "with Claude Fable 5.1 close behind" (17.92%) | curve.data.rows[3], curve/pukd | leaderboard | 200 | CONFIRMED | — (both badged NEW, added 2026-09-17, not marked provisional) |
| 29 | "From 2.5% to 20.83%", "8× in 11 months", "more than eight times better in eleven months" | eightfold.data, eightfold/kdwz | arithmetic on #24 and #28: 20.83 / 2.5 = 8.33; 2025-10-29 → 2026-09-28 = 11 months | — | CONFIRMED | — |
| 30 | "still about 4 in 5 real projects fail"; "fails about four out of every five" | eightfold.data.sub, eightfold/7yny | arithmetic: 100 − 20.83 = 79.17% | — | CONFIRMED | — |
| 31 | "Why AI work was rejected, at launch"; the researchers sorted the rejections; one project could fail for more than one reason | rejected.data.title, rejected/ygm7 | arXiv §4.3 ("rejections predominantly cluster…"); scale.com/blog/rli ("A single failed project often exhibited several of these patterns") | 200 | CONFIRMED | — |
| 32 | Note: the shares are of projects | rejected.data.note | arXiv Table 2 ("Percentage of AI deliverables exhibiting issues", from "roughly 400 evaluations"); scale.com/blog/rli ("45.6% of failed submissions") | 200 | CHANGED | "Share of projects; one project can fail for several reasons" → "Share of rejected deliverables; one can fail for several reasons" |
| 33 | Below professional quality 45.6%, "Nearly half" | rejected.data.items[0], rejected/y6mx | arXiv Table 2; scale.com/blog/rli | 200 | CONFIRMED | — |
| 34 | Incomplete or malformed 35.7%, "About a third" | rejected.data.items[1], rejected/9zx8 | same | 200 | CONFIRMED | — (35.7% ≈ 1/2.8; "about a third" holds) |
| 35 | Technical or file problems 17.6%, "about one in six" | rejected.data.items[2], rejected/2hih | same | 200 | CONFIRMED | — (1/6 = 16.7%) |
| 36 | Inconsistent across files 14.8%, "about one in seven" | rejected.data.items[3], rejected/2hih | same | 200 | CONFIRMED | — (1/7 = 14.3%) |
| 37 | July report: Fable 5 made a 3D ring redesign, a flat 2D animated ad, floor plans with renders | frontier/ztcf, frontier.data.left | safe.ai post §2 | 200 | CONFIRMED | — |
| 38 | "All much better than a year ago." | frontier/8vis | safe.ai post: "much better than deliverables from previous AIs" (ring), "improves noticeably with the newer models" (ad), "visibly more accurate" (floor plans); no time span given | 200 | CHANGED | "All much better than a year ago." → "All much better than earlier models managed." |
| 39 | The researchers say none of those three would be accepted as finished work | frontier/8vis | safe.ai post ("none of the three Fable 5 deliverables above would be accepted as finished work") | 200 | CONFIRMED | — |
| 40 | Still out of reach: transcribing music, playtesting a real-time game | frontier/9j6u, frontier.data.right | safe.ai post §5 ("stays out of reach, such as transcribing music or playtesting a real-time game") | 200 | CONFIRMED | — |
| 41 | When the researchers let AI grade AI, the graders overrated the work | graders/htip, graders.data.title | safe.ai post §3 (a calibrated automated judge "badly overshot" on the two newest models) | 200 | CONFIRMED | — |
| 42 | ≈ 3× for GPT-5.5, ≈ 2.5× for Opus 4.8 | graders.data.stats, graders/uwbw | safe.ai post ("roughly 3× for GPT‑5.5 and ~2.5× for Opus 4.8"; table ≈ 2.9× and ≈ 2.3×) | 200 | CONFIRMED | — |
| 43 | Source "Center for AI Safety, July 2026: why the test uses human judges" | graders.data.source | safe.ai post ("Human Judges Remain Necessary") | 200 | CONFIRMED | — |
| 44 | "My reading: … expect a rosier answer than a client would give." | graders/a8f7 | — | — | OUT OF SCOPE | labelled opinion |
| 45 | "US job cuts where employers cited AI, 2026"; Challenger counts announced US job cuts and the reasons employers give | layoffs.data.title, layoffs/fvxx | challengergray.com post and PDF | 200 | CONFIRMED | — |
| 46 | 116,175 cuts citing AI, January to August | layoffs.data.stats[0], layoffs/98gw | post; PDF Table 4 (AI YTD 116,175) | 200 | CONFIRMED | — |
| 47 | ≈ 22% of all announced cuts | layoffs.data.stats[1], layoffs/9s5c | post ("approximately 22%"); PDF (116,175 / 529,914 = 21.9%) | 200 | CONFIRMED | — |
| 48 | Top reason every month from March to July (5 months) | layoffs.data.stats[2], layoffs/9s5c | post and PDF ("a five-month run, beginning in March, in which AI was the leading monthly reason") | 200 | CONFIRMED | — |
| 49 | In August, AI fell to the fourth most cited reason, with 3,462 cuts | layoffs/neb9 | post; PDF Table 4 (Restructuring 16,173; Market/Economic Conditions 15,260; Closing 6,743; AI 3,462) | 200 | CONFIRMED | — |
| 50 | Source "report of September 2, 2026" | layoffs.data.source | PDF: "FOR RELEASE AT 5:30 A.M. ET, THURSDAY, SEPTEMBER 3, 2026", "CHICAGO, September 3, 2026", "a report released Thursday" (September 2, 2026 is a Wednesday); the web post shows "Publication date: Sep 02" | 200 | CHANGED | "report of September 2, 2026" → "report of September 3, 2026"; claims.md c11 likewise |
| 51 | "One month isn't a trend, but it's worth watching." | layoffs/b7gr | — | — | OUT OF SCOPE | hedge |
| 52 | What a layoff memo says (reorganizing around AI, more output with fewer people, money moves to AI) | two-sentences.data.left, hgvq, g23i | — | — | OUT OF SCOPE | a generic illustration that names no company; see opinion notes |
| 53 | The benchmark asks whether AI can deliver a whole project a client would accept; "Today: about 1 in 5" | two-sentences.data.right, two-sentences/i3ws | leaderboard (20.83%) | 200 | CONFIRMED | — |
| 54 | "My reading: companies don't wait for five in five." / "They cut where AI already speeds up the tasks…" | two-sentences/sg7d, 6d9q | — | — | OUT OF SCOPE | opinion (see opinion notes) |
| 55 | The three questions and their details | three-questions | — | — | OUT OF SCOPE | method |
| 56 | "the US Labor Department's official task list for market research analysts" | demo/fkh7 | onetonline.org (credits the U.S. Department of Labor, Employment and Training Administration; occupation "Market Research Analysts and Marketing Specialists") | 200 | CONFIRMED | — |
| 57 | "It lists thirteen tasks. Here are eight of them … This is opinion, not a measurement." | demo/bevd | onetonline.org ("5 of All 13 displayed") | 200 | CONFIRMED | — |
| 58 | Title "Market research analyst: my reading"; column "Task, from O*NET 13-1161.00" | demo.data | onetonline.org | 200 | CONFIRMED | — |
| 59 | "Reports and charts of findings" ← task 1 "Prepare reports of findings, illustrating data graphically and translating complex findings into written text." | demo.data.rows[0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 60 | "Customer data and buying habits" ← task 4 "Collect and analyze data on customer demographics, preferences, needs, and buying habits…" | demo.data.rows[1] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 61 | "Competitors' prices and marketing" ← task 6 "Gather data on competitors and analyze their prices, sales, and method of marketing and distribution." | demo.data.rows[2] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 62 | "Industry statistics and trends" ← task 8 "Monitor industry statistics and follow trends in trade literature." | demo.data.rows[3] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 63 | "Survey and questionnaire design" ← task 5 "Devise and evaluate methods and procedures for collecting data, such as surveys, opinion polls, or questionnaires…" | demo.data.rows[4] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 64 | "Campaign effectiveness" ← task 10 "Measure the effectiveness of marketing, advertising, and communications programs and strategies." | demo.data.rows[5] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 65 | "Directing survey interviewers" ← task 9 "Direct trained survey interviewers." | demo.data.rows[6] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 66 | "Proposals to management" ← task 12 "Attend staff conferences to provide management with information and proposals concerning the promotion, distribution, design, and pricing…" | demo.data.rows[7], demo/ss53 ("presenting to management") | onetonline.org | 200 | CONFIRMED | fair shortening; the claims.md mapping 1, 4, 6, 8, 5, 10, 9, 12 is right (positions in the list as the page orders it today) |
| 67 | The marks per task and lines 2p9b, zb5d, ss53 | demo | — | — | OUT OF SCOPE | labelled opinion |
| 68 | "4 of 8 / 2 of 8 / 2 of 8" and udm6 | count.data.stats, count/udm6 | the demo rows (4 "Yes…", 2 "A first draft"/"Partly", 2 "No, people work"/"The slides, not the room") | — | CONFIRMED | — (the count matches the demo rows; opinion labelled on both slides) |
| 69 | "None of the eight is safe to hand over unchecked. That's what a four in five failure rate feels like at a desk." | count/g39p | #30 | — | OUT OF SCOPE | opinion; the "four in five" figure is #30 |
| 70 | The this-week bullets, z3fe, 8yi9 | this-week | — | — | OUT OF SCOPE | method |
| 71 | "The chart moved eightfold in eleven months" | this-week/bk7j | arithmetic (#29) | — | CONFIRMED | — |
| 72 | "2.5% to 20.83% in eleven months"; "Still about 4 in 5 real projects fail" | outro.data.lines | #29, #30 | — | CONFIRMED | — |
| 73 | "My answer: it's taking tasks first, and faster than February's headline suggested." | outro/rh8y | — | — | OUT OF SCOPE | labelled opinion |
| 74 | "That's the part the test still pays humans for." | outro/njt2 | arXiv §3.3 ("trained workers and subject experts"); leaderboard ("time-consuming and expensive" manual evaluation); safe.ai post ("Human Judges Remain Necessary"; Scale Labs runs the manual evaluations) | 200 | CONFIRMED | — (the first sentence is advice, see opinion notes) |
| 75 | Remaining chapter titles and signposting (md86, hgvq, 6baw, pxdi, outro CTA) | various | — | — | OUT OF SCOPE | framing |

## Summary

**Verdicts (75 claims):** CONFIRMED 62, CHANGED 3, NOT FOUND 0, PLAUSIBLE-VIA-REPORT 0, OUT OF SCOPE 10. No claim is unresolved.

**Changes to video.json (three fact changes):**

1. `rejected.data.note`: the failure-mode shares are of rejected AI deliverables (paper Table 2, about 400 evaluations; Scale: "of failed submissions"), not of projects. The narration ("sorted the rejections") was already right.
2. `frontier/8vis`: "than a year ago" → "than earlier models managed". The CAIS post compares Fable 5 with earlier models and gives no time span.
3. `layoffs.data.source`: September 2 → September 3, 2026. The report's own release line and dateline say Thursday, September 3; the web post's "Sep 02" is its CMS date. The PDF was added to `sources` as a dependant.

claims.md: c8, c9 and c11 now match the fixes. c1, c3, c6 and c12 have today's evidence: dates, badges, the time-zone note and the O*NET site-date wording. The writer's three open questions are resolved in place.

**Conflicts with brief.md (the source wins; brief.md not edited):**

- The brief dates the Challenger report 2026-09-02. The report says September 3, 2026, and the change is applied.
- The brief calls the O*NET text "US government work (public domain)". The page licenses it under CC BY 4.0 with credit to the U.S. Department of Labor, Employment and Training Administration. The slide cites the occupation code, but the YouTube description has no O*NET credit. I did not add one; the owner should decide whether to add a credit line.
- The brief says O*NET was "updated 2026-08-25". That is the site-wide date; the occupation itself shows "Updated 2026".
- The brief gives the ColdFusion video as 2026-02-13 with about 900K views. YouTube shows Feb 13, 2026 and 969,789 views. The channel's Spotify episode (2026-02-12 16:21 UTC) and X post (2026-02-12 23:49 UTC) put it on February 12 in UTC. The narration says only "February", so nothing changes.

**Facts that expire soon:**

- The live leaderboard. GPT 6 Astra (20.83) and Fable 5.1 (17.92) were added 2026-09-17 and carry a NEW badge. Neither is marked provisional, and no score has a confidence interval. A new top score changes the title, thumbnail, hook, curve row 4, eightfold, two-sentences, outro and description.
- Challenger's September report is due in early October on a Thursday; no page I read gives its date. After it, the "January through August" and August lines stay true as history, but the August dip will no longer be the latest month.
- The O*NET list ("Updated 2026") can be revised. The ColdFusion view count is not narrated.

**Opinion check (report only):**

- The demo and count slides and the "My reading" and "My answer" lines are labelled and agree with 站主觀點.
- `two-sentences/6d9q` ("They cut where AI already speeds up the tasks, and keep fewer people to check the rest.") continues sg7d's "My reading" but is its own caption. On screen it reads as an unsourced fact.
- `this-week/bk7j` "so your list will move too" is an unlabelled prediction.
- `outro/njt2` "Your leverage is being the person who can tell good work from almost good work" and the outro line "Be the one who checks" sit close to the career advice the brief rules out.
- `two-sentences/g23i` describes layoff memos in general with no source. It names no company, so it is consistent with 不做的事.

**Listener pass (report only):**

- No sentence is over 25 words; count/udm6 is exactly 25.
- No URLs, parentheses or process narration in any line.
- Reveal counts match every slide, and each reveal lands on the sentence that names its item.
- Lint still warns that the opening chapter runs about 35 s against the 30 s target. I did not touch it.

**Lint after edits:** `node tools/video/cli.mjs lint --slug ai-real-jobs-chart` → 0 errors, 1 warning (the hook length above). No lexicon change was needed.

**Suspicions left alone:**

- (a) "240 paid jobs from freelance sites" and "projects that people had paid freelancers to do" follow Scale's launch post. The paper says the majority came from freelance platforms. Of 247 candidates before final filtering, 207 came from Upwork freelancers' past work, 7 were commissioned, and 33 were online portfolio pieces with a value the author reported.
- (b) "earned" / "paid to the humans" $143,991 is the launch post's wording. The paper defines each project's cost as the freelancer's earnings or a fair price the professional estimated, and the values are self-reported.
- (c) "The median one took … and paid …" fuses two separate medians.
- (d) "Much better" (slide heading and 8vis) is the post's word for the ring only. The ad and floor plans are "noticeably" and "visibly" better.
- (e) "Close behind" is 2.9 points (17.92 vs 20.83).
- (f) CAIS announced Fable 5 at 16.1% on X on 2026-07-01; its post and the leaderboard say 15.8% today, and the script keeps 15.8.
- (g) The leaderboard and paper say a 230-project private set is used for scoring. Yet every score except 15.80 is a whole number of projects out of 240, so the video's 240 is kept.
- (h) The link from the video's 96% to the 3.75% score is arithmetic plus the leaderboard's dates. The video's own description cites only the October 2025 paper (best 2.5%), and its 96.25% comes from third-party summaries.
- (i) The ≈ 2.5× for Opus 4.8 is the post's summary; its table shows ≈ 2.3×.

**Second round:** not required by the rule (three fact changes; more than three triggers one). The claims.md evidence edits are not counted. The owner may still want one because of suspicions (a), (b) and (d).
