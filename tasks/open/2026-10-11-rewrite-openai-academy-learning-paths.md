---
id: 2026-10-11-rewrite-openai-academy-learning-paths
title: Rewrite the explainer openai-academy-learning-paths with the facts it lacks
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
  - docs/videos/openai-academy-learning-paths
---

# Rewrite the explainer openai-academy-learning-paths with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `openai-academy-learning-paths`, 「OpenAI Academy 免費課程：台灣能修嗎？四條路徑怎麼挑，徽章算不算證照」.
- On the site: languages sent, YouTube id `nG2-qsQCZmE` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked.
- The reader's reason: 標題問的三個問題（要不要錢、台灣能不能修、徽章算不算證照）全片都只回答「以官網為準、自己登入確認」，觀眾看完得到的只有首頁上本來就看得到的四條路徑名稱。
- What it needs, in the reader's words: 需要新的事實：實際用台灣帳號登入、開一門課，把有沒有要求付費、能不能開始上課、完課後拿到的東西官方叫什麼名字，直接放上畫面回答三個問題。只改寫旁白不夠，並且要刪掉大量「以官網為準」與通用的履歷、挑課建議。
- Kind of work: new facts or runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); the takeaway can be had from the title or the source's first paragraph (X1). Also D3, D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/openai-academy-learning-paths/video.json` in the video-worker container. Copy it into `docs/videos/openai-academy-learning-paths/` to rewrite it here.

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
- [ ] Find the missing facts at their sources, or make the missing run, and record where each came from.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug openai-academy-learning-paths
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
