---
id: 2026-10-11-rewrite-siri-ai-ios-27-how-to-get-it
title: Tighten the explainer siri-ai-ios-27-how-to-get-it
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
  - docs/videos/siri-ai-ios-27-how-to-get-it
---

# Tighten the explainer siri-ai-ios-27-how-to-get-it

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `siri-ai-ios-27-how-to-get-it`, 「手機上已經有 ChatGPT 和 Gemini，為什麼還要 Siri AI？機型、語言、怎麼打開」.
- On the site: final video approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 3 of the 12 questions asked.
- The reader's reason: 機型、只有英文得整台改語言、等候名單這些事實對觀眾有用，但全片是轉述 Apple 頁面，片名問的「為什麼還要」只用「住在系統裡」這句比喻回答、沒有任何一題實際比給觀眾看，「只有英文」「Apple 沒說，以官網為準」又各講了四到六次。
- What it needs, in the reader's words: 把重複的「只有英文」「住在系統裡」「以官網為準」各留一次，開頭直接給台灣使用者結論（機型、整台改英文、等候名單、台灣資格未知），這部分只要改寫。片名的三家比較若要保留，需要新跑一次：至少把 Apple 的食譜例子在已連接帳號的 ChatGPT 和 Gemini 上實際做一遍並把結果放上卡片，否則就拿掉片名的比較承諾。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: only questions that nearly every film failed. Also D3, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/siri-ai-ios-27-how-to-get-it/` on main.

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
node tools/video/cli.mjs lint --slug siri-ai-ios-27-how-to-get-it
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
