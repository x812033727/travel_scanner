---
id: 2026-10-11-rewrite-threads-parental-supervision-apac-four-settings
title: Rewrite the explainer threads-parental-supervision-apac-four-settings with the facts it lacks
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
  - docs/videos/threads-parental-supervision-apac-four-settings
---

# Rewrite the explainer threads-parental-supervision-apac-four-settings with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `threads-parental-supervision-apac-four-settings`, 「Threads 家長監護來到亞太：家長看得到孩子的貼文嗎？先看懂 Meta 公布的四項設定」.
- On the site: on YouTube, YouTube id `643HAqtOWoM` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked.
- The reader's reason: 全片能用的資訊五行就寫完，分鐘數、時段、年齡門檻和台灣有沒有開放全都推給「以官網為準」，觀眾看完還是不知道自己的帳號能不能設、要怎麼設。
- What it needs, in the reader's words: 需要新的事實與實測：先確認台灣帳號有沒有這項功能，實際打開家庭中心把每一項的畫面、可選的分鐘數與時段、年齡門檻放上卡片，並附上公告的原句與日期。其餘只要改寫：砍掉大部分情境插圖、比喻和重複的「以官網為準」，壓成四到五分鐘。
- Kind of work: new facts or runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/threads-parental-supervision-apac-four-settings/video.json` in the video-worker container. Copy it into `docs/videos/threads-parental-supervision-apac-four-settings/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug threads-parental-supervision-apac-four-settings
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
