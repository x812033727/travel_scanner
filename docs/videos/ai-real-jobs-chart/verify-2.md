# Verification round 2: ai-real-jobs-chart

Verifier: claude-opus-5-5, 2026-09-28. This session is separate from the writer's and from round 1's. I fetched every page below myself today with the editorial user agent (curl, redirects followed, at least 1 s between requests to one host). Before reading, I stripped comments, scripts and tags. I read both PDFs as text in the scratchpad. I did not treat any of round 1's saved pages as evidence. Web searches used: 0 of 3.

Helper files are in `/tmp/claude-0/-home-user-travel-scanner/674d9bf2-c3b1-5d19-bf6c-31efd377fe1e/scratchpad/verify2-ai-real-jobs-chart/`:

- `recheck-list.md`, written before any fetch
- `flatdiff.py`: round 1's pre-edit copy compared with today's draft, which shows round 1's changes and the coordinator's edits
- `sample.py` / `sample.txt`: the random draw
- `video.before-r2.json` and `claims.before-r2.md`: copies taken before my edits
- `pages/`, `fetch-log.txt`, `lb_entries.py`

## What this round covered

- **Round-1 changes (R1):**
  - verify-1 #32: `rejected.data.note`
  - verify-1 #38: `frontier/8vis`. The coordinator has since rewritten it again.
  - verify-1 #50: `layoffs.data.source`
  - The Challenger PDF, which round 1 added to `sources` as a dependant.
  - claims.md c8, c9 and c11.
- **Coordinator edits after verify-1 (K):** every string the diff shows. That covers the description, which gained the O*NET credit; `sources` order; `test.data.steps[0]`; nsjk; the stakes label; qarp; dr78; the frontier heading; 8vis; 6d9q; the demo title, columns and cells; bk7j; the outro slide's third line; njt2; and the note in claims.md.
- **Random sample (S):** a third of round 1's 62 CONFIRMED claims, which is 21. I drew them with `random.Random(20260928).sample` from the 41 confirmed claims that neither round 1 nor the coordinator touched, because the other 21 are re-checked above anyway. The draw was verify-1 #1, 4, 5, 9, 11, 16, 17, 21, 23, 24, 25, 27, 28, 29, 35, 36, 43, 45, 46, 47 and 53.

## Pages fetched

| URL | HTTP | What it gave |
| --- | --- | --- |
| https://labs.scale.com/leaderboard/rli | 200 | The live table and the page's entry data. GPT 6 Astra: 20.83, NEW, company openai, added 2026-09-17. Fable 5.1: 17.92, NEW, company anthropic, added 2026-09-17. Fable 5: 15.80, added 2026-07-01. claude-opus-4-5-20251101-thinking: 3.75, added 2026-01-09. claude-opus-4-6 (CoWork): 4.17, added 2026-03-05. Manus 1.0: 2.50, added 2025-10-27. No entry is deprecated, provisional or marked for contamination, and the page says "There is no confidence interval for Automation Rate." Also on the page: "Each of the 240 projects…", "Total Economic Value: $143,991", "Median: 11.5 hours", "Median: $200", "performed manually by trained experts", "Analysis of failed projects…", and "At the time this leaderboard was launched, the highest-performing agent (Manus) achieved a 2.5% automation rate" |
| https://scale.com/blog/rli | 200 | Launch post dated October 29, 2025. It says "Scale and the Center for AI Safety (CAIS)", "median of around 11.5 hours… median value of $200", "real-world, paid freelance projects", "240 real-world projects spanning 23 domains", "earned a combined $143,991", "45.6% of failed submissions…" and "A single failed project often exhibited several of these patterns" |
| https://arxiv.org/abs/2510.26787 | 200 | Only v1 exists, submitted 30 Oct 2025. The abstract gives the best score as 2.5% |
| https://arxiv.org/html/2510.26787v1 | 200 | Same text as the PDF on each sentence quoted here |
| https://www.remotelabor.ai/paper.pdf | 200 | The paper. It says: "sourcing the majority of projects from freelancing platforms"; "The majority of projects in RLI were paid for by clients"; 207 + 7 + 33 sourced projects, 550 initial, 240 final; "23 Upwork subcategories"; medians of 11.5 h and $200; "The profit earned from completing all projects would be $143,991"; cost is "earned by the freelancer … or a fair price estimated by the professional", self-reported, with "Costs are available for 95% of projects"; "all evaluations are performed manually by trained workers and subject experts"; Table 2 is the "Percentage of AI deliverables exhibiting issues" over "roughly 400 evaluations", and its categories overlap. The first request failed with a TLS reset (HTTP 000). The retry 24 s later returned 200 |
| https://safe.ai/blog/significant-increase-in-digital-labor-automation | 200 | The CAIS post of July 1, 2026. It says "jointly developed by the Center for AI Safety and Scale Labs" and gives Fable 5 at 15.8%. The ring is "qualitatively much better than deliverables from previous AIs". For the ad, "visual quality improves noticeably with the newer models". The floor plans are "visibly more accurate … Fable 5 strongest". It also says "none of the three Fable 5 deliverables above would be accepted as finished work". Section 3 is titled "Human Judges Remain Necessary" and gives "roughly 3× for GPT‑5.5 and ~2.5× for Opus 4.8". On scaffolds it says "We run Anthropic models in Claude Code" and "Both GPT and Claude models are run…". It also says "stays out of reach, such as transcribing music or playtesting a real-time game" |
| https://www.challengergray.com/blog/challenger-report-august-job-cuts-up-58-consumer-products-food-lead/ | 200 | The page shows "Publication date: Sep 02" and says "a report released Thursday". On AI it says: 116,175 cuts, "approximately 22% of all cuts", "a five-month run, beginning in March", and fourth place in August with 3,462 cuts |
| https://www.challengergray.com/wp-content/uploads/2026/09/Challenger-Report-August-2026.pdf | 200 | "FOR RELEASE AT 5:30 A.M. ET, THURSDAY, SEPTEMBER 3, 2026" and "CHICAGO, September 3, 2026". Table 4 gives Restructuring 16,173, Market/Economic Conditions 15,260, Closing 6,743 and AI 3,462 in August; AI's year-to-date total is 116,175 of 529,914 (21.9%) |
| https://www.onetonline.org/link/summary/13-1161.00 | 200 | 13 tasks ("5 of All 13 displayed"), "Updated 2026" and "Site updated August 25, 2026". The CC BY 4.0 notice credits the U.S. Department of Labor, Employment and Training Administration |
| https://www.onetonline.org/help/license | 200 | Users must "credit this website and the U.S. Department of Labor, Employment and Training Administration", "link to the license", and "indicate where any changes were made to the original". The page gives a credit text for modified information, which ends "USDOL/ETA has not approved, endorsed, or tested these modifications". It also says "The trademark symbol must be properly displayed when referring to O*NET" |
| https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=z3kaLM8Oj4o&format=json | 200 | Title "AI Fails at 96% of Jobs (New Study)", channel ColdFusion |
| https://www.youtube.com/watch?v=z3kaLM8Oj4o | 200 | The page data gives the date as "Feb 13, 2026" |

## Claim table

Set: R1 = changed in round 1; K = edited by the coordinator after verify-1; S = random sample; "v1 #n" is the claim's number in verify-1.md.

| # | Claim | Where | URL | HTTP | Verdict | Before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [R1, v1 #32] Failure shares are "Share of rejected deliverables; one can fail for several reasons" | rejected.data.note | remotelabor.ai/paper.pdf (Table 2: "Percentage of AI deliverables exhibiting issues", ~400 evaluations, categories overlap); scale.com/blog/rli ("of failed submissions"); labs.scale.com/leaderboard/rli ("Analysis of failed projects") | 200 | CONFIRMED | — (round 1's change holds) |
| 2 | [R1, v1 #38] 8vis no longer says "a year ago" | frontier/8vis | safe.ai post (compares with "previous AIs" and "the newer models"; gives no time span) | 200 | CONFIRMED | — (round 1's change holds; the coordinator's later wording is #15) |
| 3 | [R1, v1 #50] "Challenger, Gray & Christmas, report of September 3, 2026" | layoffs.data.source | challengergray.com PDF (release line and dateline September 3, 2026, a Thursday); web post ("released Thursday"; "Sep 02" is the post's own date) | 200 | CONFIRMED | — (round 1's change holds) |
| 4 | [R1, dependant of v1 #50] Source "Job Cut Announcement Report, August 2026 (PDF, for release September 3, 2026)", its URL, checked_on 2026-09-28 | sources[5] | challengergray.com PDF | 200 | CONFIRMED | — |
| 5 | [R1] claims.md c8 (base is rejected deliverables), c9 (no time span), c11 (September 3; Table 4) | claims.md | paper; scale.com/blog/rli; safe.ai post; Challenger PDF | 200 | CONFIRMED | — (evidence only: c9 now describes the coordinator's 8vis and heading) |
| 6 | [K, v1 #2] "A benchmark of 240 real, paid freelance projects" | youtube.description | paper ("The majority of projects in RLI were paid for by clients"; "sourcing the majority of projects from freelancing platforms"); scale.com/blog/rli ("real-world, paid freelance projects") | 200 | CHANGED | "A benchmark of 240 real, paid freelance projects shows" → "A benchmark of 240 real projects, mostly paid freelance jobs, shows". This depends on the coordinator's "mostly paid freelance jobs" in nsjk and steps[0], which the description had not followed |
| 7 | [K] O*NET credit: "Task list: O*NET OnLine, U.S. Department of Labor, Employment and Training Administration, used under CC BY 4.0." | youtube.description | onetonline.org/help/license (credit, **link to the license**, **indicate changes**; credit text for modified information); onetonline.org/link/summary/13-1161.00 | 200 | CHANGED | → "Task list: information from O*NET OnLine by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 license (https://creativecommons.org/licenses/by/4.0/). O*NET® is a trademark of USDOL/ETA. The task statements are shortened in this video; USDOL/ETA has not approved, endorsed, or tested these modifications." The old line lacked the licence link and the notice of changes that the licence page requires |
| 8 | [K re-read, v1 #2–3] Rest of the description: 2.5% → 20.83% "at a quality a client would accept", "in eleven months"; RLI "by Scale AI and the Center for AI Safety"; leaderboard read 2026-09-28; the August 2026 Challenger report; "labelled as such" | youtube.description | leaderboard; scale.com/blog/rli; safe.ai post; Challenger post | 200 | CONFIRMED | — (the opinion label now sits in the narration and on the count slide, see opinion notes) |
| 9 | [K] "240, mostly paid freelance jobs" | test.data.steps[0].detail | paper; leaderboard ("Each of the 240 projects … sourced directly from experienced freelance professionals") | 200 | CONFIRMED | — |
| 10 | [K, v1 #12–13] "They collected two hundred forty real projects, most of them paid freelance jobs, across twenty three kinds of work." | test/nsjk | paper §3.2 (550 initial → 240 final), App. C ("23 Upwork subcategories"), "majority … paid for by clients" | 200 | CONFIRMED | — |
| 11 | [K, v1 #20] "$143,991": "combined value of the projects" | stakes.data.stats[3] | leaderboard ("Total Economic Value: $143,991"); paper ("would be $143,991"); scale.com/blog/rli ("combined $143,991") | 200 | CONFIRMED | — |
| 12 | [K, v1 #20] "Together, the projects were worth about one hundred forty four thousand dollars." | stakes/dr78 | same; paper Fig. 4 ("valued at over $140,000") | 200 | CONFIRMED | — (the sum covers the 95% of projects that have costs, and some values are estimates; see suspicions) |
| 13 | [K, v1 #18–19] "The median project took a professional about eleven and a half hours. The median value was about two hundred dollars." | stakes/qarp; stakes.data.stats[1–2] | scale.com/blog/rli ("median of around 11.5 hours … median value of $200"); leaderboard; paper ("median of $200") | 200 | CONFIRMED | — (the two medians are now separate sentences, as round 1 asked) |
| 14 | [K] "Better, not yet acceptable" over ring, ad and floor plans | frontier.data.left.heading | safe.ai post ("much better", "improves noticeably", "visibly more accurate … Fable 5 strongest"; none "would be accepted as finished work") | 200 | CONFIRMED | — |
| 15 | [K, v1 #38–39] "The researchers call the ring much better than earlier AI work, and still say none of those three would be accepted as finished work." | frontier/8vis | safe.ai post ("qualitatively much better than deliverables from previous AIs"; "none of the three Fable 5 deliverables above would be accepted as finished work") | 200 | CONFIRMED | — ("much better" now belongs to the ring only) |
| 16 | [K, v1 #54] "I think they cut where AI already speeds up the tasks, and keep fewer people to check the rest." | two-sentences/6d9q | — | — | OUT OF SCOPE | opinion, now marked "I think"; agrees with 站主觀點 |
| 17 | [K, v1 #58] Title "One real job, task by task" | demo.data.title | onetonline.org 13-1161.00 (a real occupation's official task list) | 200 | CONFIRMED | — (the title no longer carries "my reading"; see opinion notes) |
| 18 | [K, v1 #58] Columns "O*NET task, shortened", "Can AI draft it?", "Checker" | demo.data.columns | onetonline.org; licence page ("indicate where any changes were made") | 200 | CONFIRMED | — ("shortened" marks the change on screen) |
| 19 | [K, v1 #59] "Reports and charts" ← task 1 "Prepare reports of findings, illustrating data graphically…" | demo.data.rows[0][0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 20 | [K, v1 #60] "Customer data analysis" ← task 4 "Collect and analyze data on customer demographics, preferences, needs, and buying habits…" | demo.data.rows[1][0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 21 | [K, v1 #61] "Competitor prices" ← task 6 "Gather data on competitors and analyze their prices, sales, and method of marketing and distribution." | demo.data.rows[2][0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 22 | [K, v1 #62] "Industry trends" ← task 8 "Monitor industry statistics and follow trends in trade literature." | demo.data.rows[3][0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 23 | [K, v1 #63] "Survey design" ← task 5 "Devise and evaluate methods and procedures for collecting data, such as surveys, opinion polls, or questionnaires…" | demo.data.rows[4][0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 24 | [K, v1 #64] "Campaign results" ← task 10 "Measure the effectiveness of marketing, advertising, and communications programs and strategies." | demo.data.rows[5][0] | onetonline.org | 200 | CONFIRMED | loose but fair; zb5d says "campaign measurement" (see suspicions) |
| 25 | [K, v1 #65] "Directing interviewers" ← task 9 "Direct trained survey interviewers." | demo.data.rows[6][0] | onetonline.org | 200 | CONFIRMED | fair shortening |
| 26 | [K, v1 #66] "Proposals to management" ← task 12 "Attend staff conferences to provide management with information and proposals…" | demo.data.rows[7][0] | onetonline.org | 200 | CONFIRMED | fair shortening; the 1, 4, 6, 8, 5, 10, 9, 12 mapping holds |
| 27 | [K, v1 #67] Marks and checkers: "Yes, check sources", "Slides only", "You" for Campaign results, column "Checker" | demo.data.rows | — | — | OUT OF SCOPE | the owner's reading; consistent with 2p9b, zb5d and ss53 |
| 28 | [K dependant, v1 #68] "4 of 8 / 2 of 8 / 2 of 8" and udm6 against the new marks | count.data.stats, count/udm6 | the demo rows (0–3 "Yes…"; 4–5 "A first draft"/"Partly"; 6–7 "No, people work"/"Slides only") | — | CONFIRMED | — |
| 29 | [K, v1 #71] "The chart moved eightfold in eleven months, so I'd expect your list to move too." | this-week/bk7j | leaderboard; scale.com/blog/rli (20.83 / 2.5 = 8.33; 2025-10-29 → 2026-09-28 is 334 days) | 200 | CONFIRMED | — (the prediction is now marked "I'd expect") |
| 30 | [K] "Checking is still human work" | outro.data.lines[2] | leaderboard ("relies entirely on rigorous manual evaluation by trained experts"); safe.ai post ("Human Judges Remain Necessary"; an automated judge is "not a substitute for human evaluation of absolute capability") | 200 | CONFIRMED | — (true of the test; see opinion notes on how it reads on screen) |
| 31 | [K, v1 #74] "My view: the valuable skill is telling good work from almost good work. That's the part the test still needs human judges for." | outro/njt2 | paper §3.4 ("performed manually by trained workers and subject experts"); safe.ai post ("Human Judges Remain Necessary"; "Scale Labs run the manual evaluations for RLI") | 200 | CONFIRMED | — (second sentence; the first is labelled opinion) |
| 32 | [K reorder, v1 #6] Eight sources: titles, URLs, checked_on 2026-09-28 | sources | all pages above | 200 | CONFIRMED | — |
| 33 | [K] Coordinator note: most projects came from freelance platforms, and some values are the freelancers' estimates | claims.md | paper §1, §3.2, App. C.5 | 200 | CONFIRMED | — |
| 34 | [S, v1 #1] "AI Can Now Do 21% of Real Freelance Jobs. Last October It Was 2.5%." | youtube.title | leaderboard (20.83 rounds to 21); scale.com/blog/rli (2.5%, October 29, 2025) | 200 | CONFIRMED | — ("real freelance jobs" follows the leaderboard's "sourced directly from experienced freelance professionals") |
| 35 | [S, v1 #4] Tags "GPT-6 Astra", "Claude Fable 5" are real entries | youtube.tags | leaderboard ("GPT 6 Astra", company openai; "Fable 5", company anthropic); safe.ai post (Fable 5 is evaluated with "Anthropic models in Claude Code", among the "Claude models") | 200 | CONFIRMED | — |
| 36 | [S, v1 #5] "REAL PAID WORK", "2.5% → **21%**", "in eleven months" | thumbnail.data | leaderboard; scale.com/blog/rli ("real-world, paid freelance projects") | 200 | CONFIRMED | — (the paper says the majority were paid; see suspicions) |
| 37 | [S, v1 #9] "It was right, at the time." | hook/eqsu | YouTube page data ("Feb 13, 2026"); oEmbed title; leaderboard (best score 3.75% from 2026-01-09 until the 4.17% entry of 2026-03-05) | 200 | CONFIRMED | — |
| 38 | [S, v1 #11] Scale AI and the Center for AI Safety built the RLI | test/xjp3 | scale.com/blog/rli; safe.ai post ("jointly developed") | 200 | CONFIRMED | — |
| 39 | [S, v1 #16] Human judges ask whether it is as good as the professional's work and whether a client would accept it | test/mafu, test.data.steps[3] | leaderboard ("at least as well as the reference, such that it would be accepted by a reasonable client"); paper §3.4 | 200 | CONFIRMED | — |
| 40 | [S, v1 #17] 240 projects; "There are two hundred forty of them." | stakes.data.stats[0], stakes/h865 | scale.com/blog/rli; leaderboard; paper ("The final RLI dataset contains 240 projects") | 200 | CONFIRMED | — |
| 41 | [S, v1 #21] "Scale AI and the Center for AI Safety, October 2025" | stakes.data.source | scale.com/blog/rli (October 29, 2025); arXiv v1 (30 Oct 2025) | 200 | CONFIRMED | — |
| 42 | [S, v1 #23] Chapter "The curve: 2.5% to 21% in eleven months"; "Best automation rate on the leaderboard" | curve.chapter, curve.data.title | leaderboard | 200 | CONFIRMED | — |
| 43 | [S, v1 #24] "Oct 2025, launch", Manus, 2.5%; "the best system, an agent called Manus" | curve.data.rows[0], curve/raaw | leaderboard ("At the time this leaderboard was launched, the highest-performing agent (Manus) achieved a 2.5% automation rate"); scale.com/blog/rli | 200 | CONFIRMED | — |
| 44 | [S, v1 #25] "Feb 2026", "Claude Opus 4.5, thinking", 3.75%; "In February, the best score was three point seven five percent." | curve.data.rows[1], curve/cign | leaderboard page data (3.75, added 2026-01-09; the next higher entry was added 2026-03-05) | 200 | CONFIRMED | — |
| 45 | [S, v1 #27] "Jul 2026", "Claude Fable 5", 15.8%; "the Center for AI Safety reported" | curve.data.rows[2], curve/dgig | safe.ai post (July 1, 2026, "15.8%"); leaderboard (15.80, added 2026-07-01, company anthropic) | 200 | CONFIRMED | — |
| 46 | [S, v1 #28] "Sep 28, 2026", GPT-6 Astra, 20.83%; "with Claude Fable 5.1 close behind" | curve.data.rows[3], curve/pukd | leaderboard (20.83 rank 1; Fable 5.1 17.92 rank 2; both NEW, added 2026-09-17) | 200 | CONFIRMED | — |
| 47 | [S, v1 #29] "From 2.5% to 20.83%", "8× in 11 months", "more than eight times better in eleven months" | eightfold.data, eightfold/kdwz | arithmetic on #43 and #46 (8.33×; 334 days) | — | CONFIRMED | — |
| 48 | [S, v1 #35] Technical or file problems 17.6%, "about one in six" | rejected.data.items[2], rejected/2hih | paper Table 2 ("Corrupted files 17.6"); scale.com/blog/rli; leaderboard | 200 | CONFIRMED | — (1/6 = 16.7%) |
| 49 | [S, v1 #36] Inconsistent across files 14.8%, "about one in seven" | rejected.data.items[3], rejected/2hih | same | 200 | CONFIRMED | — (1/7 = 14.3%) |
| 50 | [S, v1 #43] "Center for AI Safety, July 2026: why the test uses human judges" | graders.data.source | safe.ai post (July 1, 2026, §3 "Human Judges Remain Necessary") | 200 | CONFIRMED | — |
| 51 | [S, v1 #45] "US job cuts where employers cited AI, 2026"; Challenger counts announced US job cuts and the reasons | layoffs.data.title, layoffs/fvxx | Challenger post and PDF (Table 4 "Job cuts by reason") | 200 | CONFIRMED | — |
| 52 | [S, v1 #46] 116,175 cuts citing AI, January to August | layoffs.data.stats[0], layoffs/98gw | PDF Table 4 (YTD 116,175); post | 200 | CONFIRMED | — |
| 53 | [S, v1 #47] ≈ 22% of all announced cuts | layoffs.data.stats[1], layoffs/9s5c | post ("approximately 22%"); PDF (116,175 / 529,914 = 21.9%) | 200 | CONFIRMED | — |
| 54 | [S, v1 #53] "Today: about 1 in 5"; "Today, that's about one in five." | two-sentences.data.right, two-sentences/i3ws | leaderboard (20.83%) | 200 | CONFIRMED | — |

## Summary

**Verdicts (54 claims):** CONFIRMED 50, CHANGED 2, NOT FOUND 0, PLAUSIBLE-VIA-REPORT 0, OUT OF SCOPE 2. No claim is unresolved.

**Round-1 changes:** all three still hold: the rejected-deliverables note, no "a year ago" in 8vis, and September 3, 2026. So does the Challenger PDF that round 1 added to `sources`.

**Coordinator edits:** all hold as facts, with two exceptions in the description:

- The coordinator's "mostly paid freelance jobs" did not reach the description, which still said "240 real, paid freelance projects". Fixed (#6).
- The new O*NET credit lacked two things O*NET's licence page requires: the licence link and a notice that the text was changed. It now follows the licence page's own credit text for modified information (#7).

The demo slide lost its on-screen opinion label; that is reported below and not changed. "Combined value", the two separate medians, "much better" for the ring only, the "Better" heading, the shortened cells, the unchanged 4/2/2 count and the new opinion markers all check out.

**Changes to video.json:** `youtube.description` only (#6, #7). claims.md: the header, c4, c9, c12, c13, one suspicion bullet and 進度. These are evidence edits and do not count as fact changes.

**Facts that expire soon:**

- The live leaderboard. GPT 6 Astra (20.83) and Fable 5.1 (17.92) were added 2026-09-17 and carry a NEW badge. Nothing marks them provisional, and no score has a confidence interval. A new top score changes the title, thumbnail, hook, curve row 4, eightfold, bk7j, two-sentences, outro and description.
- Challenger's September report is due in early October. No page I read gives its date. After it, neb9 and b7gr stay true as history.
- O*NET 13-1161.00 shows "Updated 2026", the site shows "Site updated August 25, 2026", and the licence page says the site's data comes mainly from the O*NET 31.0 database. The count of 13 and the task order can change with an update.

**Opinion labelling:**

- These are marked and agree with 站主觀點: a8f7 and sg7d ("My reading"), 6d9q ("I think", new), bevd ("my reading … opinion"), udm6 ("in my count"), the count slide (its title and source), bk7j ("I'd expect", new), rh8y ("My answer") and njt2 ("My view", new).
- **Report:** the demo slide's title changed from "Market research analyst: my reading" to "One real job, task by task". The marks in "Can AI draft it?" and "Checker" now carry no label on screen. bevd says just before them that they are opinion, and the count slide labels them. The table template has no source line, so the title is the only place a label fits. The owner could put "my reading" back in it.
- The outro slide's "Checking is still human work" is true of the test, but on screen it reads as a general claim. g39p ("None of the eight is safe to hand over unchecked") is still unlabelled, as in round 1.
- njt2's "the valuable skill is…" is labelled, but it sits close to the career advice that 不做的事 rules out. The description disclaims career advice.

**Listener pass (report only):** the longest sentence is 25 words (udm6); 8vis is 24. There are no URLs or parentheses in the narration, and every scene reveals the same number of items its slide has.

**Lint after edits:** `node tools/video/cli.mjs lint --slug ai-real-jobs-chart` → 0 errors, 1 warning. The warning, left alone, is the existing one about the opening chapter running about 35 s against a 30 s target.

**Suspicions left alone:**

- (a) Four places still call the whole set paid work: the title ("Real Freelance Jobs"), the "REAL PAID WORK" tag on the thumbnail and the hook slide, and z8yk ("real paid projects"). z8yk is the brief's approved hook text. These follow Scale's launch post ("real-world, paid freelance projects"), while the paper says the majority were paid for by clients. The owner decides.
- (b) "Campaign results" is a looser shortening of task 10 than the earlier "Campaign effectiveness"; the narration says "campaign measurement".
- (c) O*NET's licence page says "The trademark symbol must be properly displayed when referring to O*NET". The slides say "O*NET task, shortened" and "eight O*NET tasks" without ®. Only the description's credit now carries "O*NET®". This is not a fact, so I did not change it.
- (d) $143,991 sums the cost values available for 95% of projects, and some of those values are the professionals' estimates. "Worth about" covers this.
- (e) Round 1's (e) to (i) still stand, and I did not re-open them: "close behind" is 2.9 points; CAIS's X post said 16.1%; 230 projects are private and 240 in all; the link from 96% to 3.75% rests on third-party summaries; ≈2.5× is ≈2.3× in the post's table.

**Third round:** not required. This round made two fact changes, both in the description, and the rule calls for a third round only above three.
