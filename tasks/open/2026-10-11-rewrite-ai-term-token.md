---
id: 2026-10-11-rewrite-ai-term-token
title: Tighten the explainer ai-term-token
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-term-token
---

# Tighten the explainer ai-term-token

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-term-token`, 「Token 是什麼？AI 算的不是字數，是它自己的單位｜AI 名詞十分鐘」.
- On the site: storyboard approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked. A second reader: rework, 4 failed.
- The reader's reason: 名詞講清楚了、數字也是實算的，但「常用整塊、少見拆片」同一件事用比喻重講了七八次，而觀眾真正要動手的「量一次」沒說用什麼量，省下的 5,600 個 token 值多少也沒說。
- What it needs, in the reader's words: 把重複的比喻句刪到同一個概念只留一個（只需改寫），並補上不懂程式的人實際能用的計數方式（名稱與位置）。再把 56×100＝5,600 個 token 換成金額或佔上限的比例，讓「什麼時候該在意」有門檻；這兩項需要補新事實。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: only questions that nearly every film failed. Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-term-token/` on main.

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
- [ ] Cut what repeats and add the one thing the reader says is missing.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-term-token
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
