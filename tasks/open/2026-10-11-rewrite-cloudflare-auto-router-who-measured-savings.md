---
id: 2026-10-11-rewrite-cloudflare-auto-router-who-measured-savings
title: Rewrite the explainer cloudflare-auto-router-who-measured-savings with the facts it lacks
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
  - docs/videos/cloudflare-auto-router-who-measured-savings
---

# Rewrite the explainer cloudflare-auto-router-who-measured-savings with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `cloudflare-auto-router-who-measured-savings`, 「AI 幫你挑模型就一定省錢？Cloudflare Auto Router 的省錢數字是誰測的」.
- On the site: on YouTube, YouTube id `cc09kA17Xsw` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 片名問的是「省錢數字」，整支片卻沒有說出任何一個數字，省幾成、成功率、每次成功的成本全都寫成「以官網為準」，觀眾看完只拿到定性的排序和一條沒有代入數字的公式。
- What it needs, in the reader's words: 要把 Cloudflare 原文的實際數字（最多省幾成、三組的成功率與成本、每次成功的成本）放上卡片，並用真實單價把「簡單題佔幾成」算一次給觀眾看（例如七成簡單與兩成簡單各省多少）。這需要補新的事實與一次實算，不是只改寫；同時刪掉大半的比喻句和重複的「以官網為準」。
- Kind of work: new facts or runs, then a rewrite.

What it failed: a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/cloudflare-auto-router-who-measured-savings/video.json` in the video-worker container. Copy it into `docs/videos/cloudflare-auto-router-who-measured-savings/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug cloudflare-auto-router-who-measured-savings
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
