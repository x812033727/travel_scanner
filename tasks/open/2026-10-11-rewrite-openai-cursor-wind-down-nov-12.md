---
id: 2026-10-11-rewrite-openai-cursor-wind-down-nov-12
title: Rewrite the explainer openai-cursor-wind-down-nov-12 with the facts it lacks
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
  - docs/videos/openai-cursor-wind-down-nov-12
---

# Rewrite the explainer openai-cursor-wind-down-nov-12 with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `openai-cursor-wind-down-nov-12`, 「OpenAI 要停供 Cursor 的模型？11 月 12 日是「建議日」不是生效日：先分清三件事」.
- On the site: on YouTube, YouTube id `zxHRm5jnELc` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked.
- The reader's reason: 片名主打「建議日」，全片卻沒說出建議日是哪一天、通知期有多長，真正來自公告的事實只有四五條，其餘約三十句是任何期限都適用的算日子與盤點通則。
- What it needs, in the reader's words: 把公告日、建議日與通知期天數直接放上卡片並實際算一次，引用公告原句，補上 Cursor 目前可選的非 OpenAI 模型，再刪掉通用的算日子教學與盤點叮嚀。需要補新事實（公告原文的日期與字句、Cursor 模型頁），不需要新的實測。
- Kind of work: new facts or runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/openai-cursor-wind-down-nov-12/video.json` in the video-worker container. Copy it into `docs/videos/openai-cursor-wind-down-nov-12/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug openai-cursor-wind-down-nov-12
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
