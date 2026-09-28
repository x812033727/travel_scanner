# Claims: ai-real-jobs-chart

Written 2026-09-28 (writer: claude-opus-5-5). Format: `id｜claim as narrated or shown｜source URL｜checked｜scene`.

c1｜In February 2026 a widely shared video said AI fails at 96% of real jobs; the figure was right at the time (ColdFusion, "AI Fails at 96% of Jobs (New Study)", 2026-02-13, 96.25% failure, about 900K views in a search snapshot)｜https://www.youtube.com/watch?v=z3kaLM8Oj4o (video page returns only its footer to the fetcher; title, date and the 96.25% figure from search results and summaries of the video)｜2026-09-28｜hook, curve
c2｜The best automation rate at launch was 2.5% (Manus), 2025-10-29｜https://scale.com/blog/rli ; https://arxiv.org/abs/2510.26787 (v1 2025-10-30: "the highest-performing agent achieving an automation rate of 2.5%")｜2026-09-28｜hook, curve
c3｜The leaderboard on 2026-09-28 shows GPT-6 Astra at 20.83% (marked new), Claude Fable 5.1 at 17.92% (new), Claude Fable 5 at 15.80%, Claude Opus 4.5 thinking at 3.75%, Manus 1.0 and 1.5 at 2.50%｜https://labs.scale.com/leaderboard/rli｜2026-09-28｜hook, curve
c4｜RLI: built by Scale AI and the Center for AI Safety; 240 real projects from freelance platforms across 23 domains; median about 11.5 hours for a professional and a median value of $200; the human freelancers earned $143,991 in total｜https://scale.com/blog/rli｜2026-09-28｜test, stakes
c5｜The AI gets the same brief and inputs as the freelancer; human evaluators judge whether the AI deliverable is at least as good as the professional's, i.e. acceptable as commissioned work｜https://arxiv.org/abs/2510.26787 ; https://www.remotelabor.ai/ ("fail to complete the vast majority of projects at a quality level that would be accepted as commissioned work")｜2026-09-28｜test, stakes
c6｜Claude Fable 5 reached 15.8% by July 2026 (Center for AI Safety, 2026-07-01); the 3.75% best score in February is the one behind the 96.25% failure headline｜https://safe.ai/blog/significant-increase-in-digital-labor-automation ; c1, c3｜2026-09-28｜curve
c7｜Arithmetic: 20.83 / 2.5 = 8.33 → "more than eight times", "eightfold"; October 2025 to September 2026 = 11 months; 100 − 20.83 = 79.17% → "about four out of every five" fail｜c2, c3｜2026-09-28｜eightfold, this-week, outro
c8｜At launch, rejected AI deliverables: 45.6% below professional quality, 35.7% incomplete or malformed, 17.6% technical or file-integrity problems, 14.8% inconsistent across files; categories overlap｜https://scale.com/blog/rli｜2026-09-28｜rejected
c9｜July 2026: Fable 5 produced a ring redesign (3D/CAD), a flat-design 2D animated ad and floor plans with renders, much better than earlier AIs, but "none of the three Fable 5 deliverables above would be accepted as finished work"; transcribing music and playtesting a real-time game remain out of reach｜https://safe.ai/blog/significant-increase-in-digital-labor-automation｜2026-09-28｜frontier
c10｜Automated judges overestimate AI capability by about 3× for GPT-5.5 and about 2.5× for Opus 4.8, which is why the RLI uses human judges｜https://safe.ai/blog/significant-increase-in-digital-labor-automation｜2026-09-28｜graders
c11｜Challenger, Gray & Christmas, 2026-09-02: AI cited in 116,175 announced US job cuts January–August 2026, about 22% of all cuts, the leading reason year to date; AI was the top monthly reason March through July; in August it fell to fourth with 3,462 cuts｜https://www.challengergray.com/blog/challenger-report-august-job-cuts-up-58-consumer-products-food-lead/｜2026-09-28｜layoffs
c12｜O*NET 13-1161.00 Market Research Analysts and Marketing Specialists lists 13 tasks (page updated 2026-08-25); the eight on the slide are shortened from its task statements 1, 4, 6, 8, 5, 10, 9 and 12｜https://www.onetonline.org/link/summary/13-1161.00｜2026-09-28｜demo
c13｜The task-by-task marks and the count (4 AI drafts, 2 first draft at best, 2 people work) are the owner's reading, labelled as opinion on the slide and in the narration｜brief.md 站主觀點｜2026-09-28｜demo, count

## 與季企劃不同的地方

- The season brief's premise ("AI fails at 96% of real jobs") is out of date: the same leaderboard now shows 20.83%. The title, hook and slug changed (`ai-fails-96-percent-jobs` → `ai-real-jobs-chart`), as the season brief's expiring-facts table required.
- The demo uses the US Department of Labor's O*NET task list instead of a private job posting: official, public and without an employer to name.
- No company's layoff statement is quoted; Challenger's counts carry the layoff side, so no company is presented as having replaced people with AI.

## 我懷疑但沒動的事

- The dates in the curve table's first column: Oct 2025 (launch) and Jul 2026 (CAIS post) are dated sources; "Feb 2026" for 3.75% rests on ColdFusion's February figure matching the leaderboard's Claude Opus 4.5 thinking entry; "Sep 28, 2026" is the day we read the live leaderboard. A verifier should confirm there was no higher score before February 13.
- Whether the leaderboard's "NEW" entries (GPT-6 Astra, Claude Fable 5.1) are final or provisional.
- The failure-mode shares are of which base (all projects or rejected ones); the narration says "sorted the rejections".

## 進度

All 15 scenes written; lint 0 errors. Awaiting verification round 1.
