---
id: 2026-10-11-rewrite-sothatswhy-b26
title: Rewrite the explainer sothatswhy-b26 with the facts it lacks
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
  - docs/videos/sothatswhy-b26
---

# Rewrite the explainer sothatswhy-b26 with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `sothatswhy-b26`, 「為什麼超市常把牛奶放在最裡面？｜原來如此事務所」.
- On the site: on YouTube, not uploaded.
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked.
- The reader's reason: 全片能帶走的內容五行就寫完，卻有大量句子在聲明範圍、交代出處和解說卡片，結論停在「位置不等於動機」，蔬果研究也沒給任何增幅數字。
- What it needs, in the reader's words: 把兩種理由和「沒人測量過」提前到開頭、重複的範圍聲明每個來源只留一句、三個問題放上卡片，這部分只要改寫。蔬果研究要補上論文裡的實際銷售增幅數字，需要從原論文補事實，不需要新的實測。
- Kind of work: new facts or runs, then a rewrite.

What it failed: one exact thing to do, check or decide, in full on a card (A1); more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/sothatswhy-b26/` on main.

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
node tools/video/cli.mjs lint --slug sothatswhy-b26
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
