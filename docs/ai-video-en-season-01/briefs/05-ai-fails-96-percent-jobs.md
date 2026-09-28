# AI Fails at 96% of Real Jobs. So Why Are Companies Still Cutting People?

slug：`ai-fails-96-percent-jobs`｜第 5 支，建議 2026-11-03 上架｜英文旁白、8–12 分鐘｜企劃日 2026-09-28

> **2026-09-28 更新：這份企劃的前提已過期。** 同一個 Remote Labor Index 的排行榜現在是 20.83%（GPT-6 Astra），不是二月的 3.75%。改寫後的企劃與稿子在 `docs/videos/ai-real-jobs-chart/`（slug 改為 `ai-real-jobs-chart`）。這份保留為原始版本。

## 觀眾

Working adults in offices, agencies and freelancing who feel two contradictory headlines at once: studies saying AI fails most real work, and layoff announcements that name AI. They want to know which part of their own job is exposed, in plain terms. Searches: "will ai take my job 2026", "ai fails 96% of jobs study", "remote labor index", "which jobs are safe from ai".

## 觀眾看完能做到的事

- Separate three things that headlines mix: whole jobs vs tasks, capability vs adoption, and layoffs attributed to AI vs layoffs caused by it.
- Run a three-question test on their own task list this week (can AI produce a checkable deliverable for this task, who checks it, what does a wrong one cost) and mark each task can / cannot yet / needs a checker.

## 站主觀點

套用立場：3、5

I read the study before I read the headline, and I show the viewer where the number comes from and what it does not cover. The 96% figure measures whether frontier models matched human freelance work on real briefs at one point in time; it does not say "your job is safe", and layoff announcements do not say "AI did your job". Both can be true because companies and models are answering different questions. The action at the end is a task list, not a feeling about the future; and I give no career or financial advice beyond that list.

## 示範或實算

One real, public job description (an entry-level marketing coordinator or a junior analyst, from a public posting on writing day, employer name removed) decomposed into 10–15 tasks on `table` and `steps` slides (chapter 5). For each task the three questions are answered on screen, and the result is counted on a `stats` slide: how many tasks AI can produce a checkable deliverable for today, how many it cannot yet, how many need a human checker. Then the study's four failure modes (corrupt files, incomplete deliveries, low professional quality, inconsistent assets, as ColdFusion's summary lists them and as the paper states) are mapped onto that same list.

## 大綱

### 選項 A：研究說什麼、沒說什麼、對你的任務清單意味著什麼（建議）

Angle: study → what it does not say → the viewer's own tasks. Differs from B, which starts from the layoff headlines.

Hook: "A study gave frontier AI models real freelance jobs, the kind people actually get paid for, and the models failed to match human work ninety-six percent of the time. The same year, layoff announcement after layoff announcement named AI as the reason. Both are true. Once you see why, you'll know which part of your own job is actually exposed, and I'll give you a three-question test to find it."

| # | Chapter | s | Scenes |
| --- | --- | --- | --- |
| 1 | What the 96% study measured | 110 | `title`; `quote`: the study's own sentence; `stats`: 96.25%, number of briefs, models tested (from the paper); `bullets`: the four failure modes |
| 2 | What it did not measure | 80 | `compare`: whole jobs vs tasks; `quote`: ILO 2025 update, about one in four workers in an occupation with some exposure, "transformation more likely than replacement" |
| 3 | The jagged frontier: brilliant here, useless there | 80 | `big`: the 758-consultant field experiment; `bullets`: tasks inside vs outside the frontier |
| 4 | Layoffs and AI: two different sentences | 90 | `steps`: "we are cutting because of AI" vs "AI is doing the work"; `table`: what public statements actually say (quoted, sourced, employer names only where the statement is official); `chat`: a manager's version vs an employee's |
| 5 | The three-question test on a real job description | 140 | `table`: 10–15 tasks × three questions; `stats`: can / cannot yet / needs a checker; `steps`: the four failure modes mapped onto the list |
| 6 | Do this with your own list this week | 60 | `steps`: write tasks, answer three questions, mark; `cta`: the Mokaair article on AI at work if published |
| 7 | So will AI take your job? | 40 | `outro`: "it will take tasks first, the checkable ones; your leverage is being the checker"; next step: comments: "which task on your list surprised you?" |

Total ≈ 600 s.

### 選項 B：從裁員公告開始

Angle: news first, study second. Stronger emotionally; higher risk of sounding like advice.

Hook: "This year's layoff announcements keep saying the same word: AI. But when researchers gave AI real jobs to do, it failed ninety-six percent of them. Somebody is wrong, or the two are talking about different things. Here's which."

Chapters: The word in every announcement (80 s: `quote`) → The study (110 s) → Whole jobs vs tasks (80 s) → The jagged frontier (80 s) → Your task list (140 s) → This week (60 s) → `outro` (40 s).

## 會過期的事實

| Fact | Re-check at |
| --- | --- |
| The Remote Labor Index results (96.25% and the failure modes), models and date | the original paper and the index page on writing day (ColdFusion's 2026-02-13 video summarized it; we cite the paper, not the video) |
| ILO "Generative AI and jobs: a 2025 update" figures | ilo.org/publications/generative-ai-and-jobs-2025-update |
| The jagged-frontier experiment (758 consultants, 2023) | aiinstitute.hbs.edu/navigating-the-jagged-technological-frontier/ |
| Any layoff statements quoted | the employers' own releases or filings on writing day; no third-party paraphrase |
| Newer studies published before recording | search on writing day; if a newer measurement supersedes 96%, the title changes |

## 素材

- Original tables; `quote` slides with sources and dates; the job description reproduced only as a task list (no employer name, no personal data).
- Mokaair AI-at-work article if published; otherwise the closing is the comment question.

## 不做的事

- No career, financial or legal advice; no predictions of unemployment numbers.
- No naming of individual laid-off people; no company blamed beyond its own quoted statement.
- No "learn AI or be replaced" framing.

## 附錄：包裝與破百萬的理由

| Item | A (news) | B | C (evergreen) |
| --- | --- | --- | --- |
| Title | AI Fails at 96% of Real Jobs. So Why Are Companies Still Cutting People? | Will AI Take Your Job? The Study Everyone Misread (and a 3-Question Test) | The 96% Problem: What AI Still Can't Do at Work in 2026 |
| Thumbnail label / big / small | NEW STUDY / 96% FAIL / so why the layoffs? | — / YOUR JOB? / a 3-question test | — |

Why one million is plausible: the closest comparable is direct, ColdFusion's video on the same study at about 900K views in the planning snapshot (`sources.json` S10), and jobs is the most-searched AI worry; ours adds the layoff contradiction and a real task-list demo. Overlaps Codex's episode 4 in theme but not in language, hook or demo. Risk: sounding like advice; the stance keeps it to a task list.
