---
id: 2026-10-11-rewrite-sothatswhy-t27
title: Rewrite the explainer sothatswhy-t27 with the facts it lacks
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/sothatswhy-t27
---

# Rewrite the explainer sothatswhy-t27 with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `sothatswhy-t27`, 「日本垃圾桶少？旅客調查說了什麼｜原來如此事務所」.
- On the site: on YouTube, not uploaded.
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 整支片真正的新資訊只有 17.2% 與 43.7% 兩個數字加一個複選示意，五行就講得完，重點在第三個畫面就已說完，其餘一百多句多半是任何調查都適用的提醒、比喻和「這只是示意」的聲明。
- What it needs, in the reader's words: 需要補新事實，光改寫不夠：調查裡其他困擾項目的名次與比例、題目原文與真實選項（現在的複選示意用的是自編選項）、與前次調查的比較，最好再加上垃圾桶為何少的有來源說明。同時把第三、五、六章的通則、比喻與重複收尾刪到剩三分之一左右，並讓數字卡直接標出來源名稱。
- Kind of work: new facts or runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/sothatswhy-t27/` on main.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Find the missing facts at their sources, or make the missing run, and record where each came from.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug sothatswhy-t27
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
