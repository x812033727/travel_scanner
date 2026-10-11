---
id: 2026-10-11-rewrite-mcdonalds-ai-pricing-engine-who-said-what
title: Tighten the explainer mcdonalds-ai-pricing-engine-who-said-what
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:49:18Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/mcdonalds-ai-pricing-engine-who-said-what
---

# Tighten the explainer mcdonalds-ai-pricing-engine-who-said-what

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `mcdonalds-ai-pricing-engine-who-said-what`, 「麥當勞用 AI 估你願意付多少？近 14,000 家餐廳的「定價引擎」，三方說法怎麼聽」.
- On the site: on YouTube, YouTube id `qWlnIpZtfeI` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 前三章有料（定店不定人、截圖原句、施壓三件事、Fresno 差 21%），但後兩章約三分之一的旁白在教百分比和「十塊乘八次」這種不需要影片的算術，再加上三十多句「報導說」和一堆比喻，把真正的內容稀釋掉了。
- What it needs, in the reader's words: 把第四、五章的比價算術縮成一張卡，刪掉菜市場、騎樓、傳話遊戲等比喻和重複的出處句（出處留在卡片上），讓片長回到前三章的事實；這部分只需要改寫。另外要補一個新事實：這套系統講的是美國門市，台灣麥當勞是否各店不同價、是否適用，片中完全沒交代。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/mcdonalds-ai-pricing-engine-who-said-what/video.json` in the video-worker container. Copy it into `docs/videos/mcdonalds-ai-pricing-engine-who-said-what/` to rewrite it here.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.
- [ ] The owner decides what happens to the cut that is already on YouTube: a video's file
      cannot be replaced there, so a rewrite is a new upload.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Cut what repeats and add the one thing the reader says is missing.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug mcdonalds-ai-pricing-engine-who-said-what
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
