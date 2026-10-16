---
id: 2026-10-11-rewrite-gemini-skills-replace-gems-move-checklist
title: Rewrite the explainer gemini-skills-replace-gems-move-checklist with the facts it lacks
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
  - docs/videos/gemini-skills-replace-gems-move-checklist
---

# Rewrite the explainer gemini-skills-replace-gems-move-checklist with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `gemini-skills-replace-gems-move-checklist`, 「Gemini 推出 skills、Gems 要退場：你調好的 Gem 會怎樣？搬家前先查兩個日期」.
- On the site: on YouTube, YouTube id `xSrFAMk_udE` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked.
- The reader's reason: 片名和開場賣的是「到期日」和「時程」，但整支片沒有任何一個日期，每一格都寫「以官網為準」，觀眾看完還是得自己去讀公告。
- What it needs, in the reader's words: 把公告裡三類帳戶的實際停止支援日與 Opal 關閉日寫上卡片並算出剩餘天數，再實際把一個 Gem 的指令做成 skill 並呈現結果，這需要補新事實與一次實測，不是只改寫。同時刪掉約三十句比喻與場景句、十多句「以官網為準」式的出處句，把篇幅留給日期、Labs／Opal 的例外和實際操作。
- Kind of work: new facts or runs, then a rewrite.

What it failed: the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/gemini-skills-replace-gems-move-checklist/video.json` in the video-worker container. Copy it into `docs/videos/gemini-skills-replace-gems-move-checklist/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug gemini-skills-replace-gems-move-checklist
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
