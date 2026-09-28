# AI Can Now Do 21% of Real Freelance Jobs. Last October It Was 2.5%.

slug：`ai-real-jobs-chart`｜narration_locale：en｜企劃日 2026-09-28｜季企劃第 2 支（原 `ai-fails-96-percent-jobs`，前提已過期，見「與季企劃不同的地方」）

## 觀眾

Working adults in offices, agencies and freelancing who have seen both headlines of 2026: "AI fails at 96% of real jobs" (ColdFusion, February, about 900K views) and a year of layoff announcements that cite AI. They want to know which is true and what it means for their own job, in plain terms. Searches: "will ai take my job 2026", "ai fails 96% of jobs", "remote labor index", "ai layoffs 2026", "which jobs will ai replace".

## 觀眾看完能做到的事

- Read the Remote Labor Index number correctly: the share of real, paid freelance projects where an AI's deliverable was judged as good as a professional's, which went from 2.5% (October 2025) to 20.83% (GPT-6 Astra on the leaderboard, 2026-09-28), and which still means about four in five real projects fail.
- Run a three-question test on their own task list this week (can AI draft this into something I can inspect, who checks it, what does a wrong one cost) and mark each task: AI drafts, a first draft at best, or people work; then repeat it in six months.

## 站主觀點

套用立場：3、5

I read the study before the headline, and I show where the number comes from and what it does not cover. The February headline was right when it was made and is wrong now: the same test moved more than eightfold in eleven months, and it still says the best AI fails about four in five real projects. Both are true, and a layoff memo and a benchmark answer different questions, so neither "AI can't do real work" nor "AI is taking every job" survives the data. The action is a task list, not a feeling about the future. My task-by-task reading of a real job description is opinion and is labelled as mine; nothing here is career or financial advice.

## 示範或實算

1. The curve on a `table` slide, from the official sources: Remote Labor Index launch 2025-10-29, best agent Manus 2.5% (scale.com); the 3.75% best score behind February's "96% fail" headline (Claude Opus 4.5 thinking on the leaderboard; ColdFusion's video of 2026-02-13 says 96.25%); Claude Fable 5 at 15.8% on 2026-07-01 (safe.ai); GPT-6 Astra at 20.83% with Claude Fable 5.1 at 17.92%, read on the leaderboard 2026-09-28 (labs.scale.com). Arithmetic on a `big` slide: 20.83 ÷ 2.5 = 8.3, "more than eightfold in eleven months"; 100 − 20.83 = 79.17, "about four in five still fail".
2. A real job description decomposed task by task on a `table` slide: the US Department of Labor's O*NET list for Market Research Analysts and Marketing Specialists (13-1161.00, 13 tasks, updated 2026-08-25), eight tasks shown, each marked with the owner's reading; the count on a `stats` slide (4 AI drafts, you check; 2 first draft at best; 2 people work).

## 大綱

### 選項 A：從過期的標題開始，畫出曲線，再回到你的工作（建議）

Angle: the February headline as the hook, the curve as the payoff, the layoffs as the tension, the task list as the action. Differs from B, which starts from layoffs.

Hook (spoken, ≤30 s): "In February, one widely shared video said AI fails at ninety six percent of real jobs. It was right, at the time. The same test now says the best AI finishes about twenty one percent of real paid projects. Last October, it was two and a half. Here's what that test measures, why companies are cutting people anyway, and three questions that tell you what it means for your job."

| # | Chapter | s | Scenes |
| --- | --- | --- | --- |
| 1 | The number that changed since February | 25 | `title` |
| 2 | What the Remote Labor Index measures | 75 | `steps`: real projects, 23 kinds of work, same brief, human judges; `stats`: 240, 11.5 h, $200, $143,991 |
| 3 | The curve: 2.5% to 21% in eleven months | 60 | `table`: Oct 2025 → Feb 2026 → Jul 2026 → Sep 28, 2026; `big`: more than 8× in 11 months, still about 4 in 5 fail |
| 4 | What AI still gets wrong | 95 | `bullets`: why deliverables were rejected at launch; `compare`: much better but not yet acceptable vs still out of reach; `stats`: AI graders overrate AI work about 3× and 2.5× |
| 5 | So why are companies cutting people? | 80 | `stats`: 116,175 cuts citing AI Jan–Aug 2026, about 22%, top reason March–July; `compare`: what a layoff memo says vs what the test measures |
| 6 | Test your own job in three questions | 150 | `steps`: three questions; `table`: O*NET task list with my reading; `stats`: my count; `bullets`: do this week |
| 7 | So will AI take your job? | 35 | `outro` |

Worked example: chapters 3 and 6. Closing next step: a comment question ("Which task on your list moved first?"). Total ≈ 520 s by the estimator.

### 選項 B：從裁員開始

Angle: 116,175 US job cuts citing AI this year first, then the test that says four in five real projects still fail, then the task list. Stronger emotionally, higher risk of sounding like advice.

Hook: "This year, US employers have blamed AI for more than a hundred thousand job cuts. The best AI still fails four out of five real paid projects. Somebody's wrong, or they're answering different questions."

Chapters: The layoffs (80 s) → The test (75 s) → The curve (60 s) → What AI still gets wrong (95 s) → Your task list (150 s) → `outro` (35 s).

## 會過期的事實

| Fact | Re-check on writing day at |
| --- | --- |
| Leaderboard rates (GPT-6 Astra 20.83%, Claude Fable 5.1 17.92%, Claude Fable 5 15.80%, Claude Opus 4.5 thinking 3.75%, Manus 2.5%) | https://labs.scale.com/leaderboard/rli — a live leaderboard; the title number changes if the top score changes |
| Launch facts (240 projects, 23 domains, median 11.5 h and $200, $143,991, failure-mode shares) | https://scale.com/blog/rli (2025-10-29), https://arxiv.org/abs/2510.26787 |
| July results, examples, automated-grader overestimate | https://safe.ai/blog/significant-increase-in-digital-labor-automation (2026-07-01) |
| AI-cited job cuts (116,175 Jan–Aug, about 22%, top reason March–July, fourth in August) | https://www.challengergray.com/blog/challenger-report-august-job-cuts-up-58-consumer-products-food-lead/ (2026-09-02); the September report comes out in early October |
| O*NET task list for 13-1161.00 | https://www.onetonline.org/link/summary/13-1161.00 (updated 2026-08-25) |
| February headline | https://www.youtube.com/watch?v=z3kaLM8Oj4o (2026-02-13) |

## 素材

- Original slides only: tables, stats, the compare cards. No screenshots of the leaderboard, of ColdFusion's video or of any company.
- O*NET task text is US government work (public domain), quoted in shortened form with the occupation code.

## 不做的事

- No career, financial or legal advice; no predictions of unemployment rates; no "learn AI or be replaced".
- No company is named as having replaced people with AI; layoff reasons are Challenger's counts of what employers said.
- No criticism of ColdFusion: its number was correct in February; the video says so.
- No claim that the Remote Labor Index measures whole jobs; it measures freelance projects, and the video says so.
