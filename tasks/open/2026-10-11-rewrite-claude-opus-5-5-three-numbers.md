---
id: 2026-10-11-rewrite-claude-opus-5-5-three-numbers
title: Rewrite the explainer claude-opus-5-5-three-numbers with the facts it lacks
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
  - docs/videos/claude-opus-5-5-three-numbers
---

# Rewrite the explainer claude-opus-5-5-three-numbers with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `claude-opus-5-5-three-numbers`, 「Claude Opus 5.5 便宜了 40%？其實是三個不同的數字」.
- On the site: on YouTube, YouTube id `UOgxCymxb1I` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked. A second reader: rework, 7 failed.
- The reader's reason: 片名說「三個數字」，全片卻一個數字都沒講，表格和算式都只寫「以官網為準」，觀眾看完還是得自己去官網查才知道便宜多少。
- What it needs, in the reader's words: 把三個百分比和 Opus 5 與 5.5 的實際牌價寫上標明出處的卡片，並用一個具體用量（例如快取讀取占多數的寫程式工作）把新舊帳單實際算一遍。需要補上公告與價目表上的實際數字（新事實，不需要實測），其餘只要改寫並刪掉重複的「以官網為準」與比喻句。
- Kind of work: new facts or runs, then a rewrite.

What it failed: the title's question answered with a specific answer (T1); a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/claude-opus-5-5-three-numbers/video.json` in the video-worker container. Copy it into `docs/videos/claude-opus-5-5-three-numbers/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug claude-opus-5-5-three-numbers
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
