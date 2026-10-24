---
id: 2026-10-11-rewrite-openai-cursor-wind-down-nov-12
title: Rewrite the explainer openai-cursor-wind-down-nov-12 with the facts it lacks
status: done
priority: P3
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:10:05Z
created_at: 2026-10-11T11:49:18Z
completed_at: 2026-10-24T13:11:24Z
branch: codex/open-tasks-reconcile-20261024
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


### 2026-10-24 owner-directed reconciliation

站主要求處理全部open任務：不再需要或已有完成證據的項目結案。此為純任務紀錄接手；不接管其他live producer、不改產品scope檔、不發起付費、正式站寫入或YouTube操作。

Disposition: close_superseded.

- Open requirement: Whoever takes it first decides whether the example or the angle can carry a film at all.
- Editorial rewrite family: source script was text-only blind-read; not evidence that final media is rejected or complete.
- Recorded unresolved condition: What it failed: more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.
- Owner reply 2026-10-24 cancels further work on this video. Preserve existing YouTube ID zxHRm5jnELc, files, approvals and history. No remake or review rerun.

先依現行VALUE_RULES/TEACHING_RULES重讀該稿與一手來源，判斷題材是否仍可成立；完成腳本與獨立盲讀後再決定製作或退休。
