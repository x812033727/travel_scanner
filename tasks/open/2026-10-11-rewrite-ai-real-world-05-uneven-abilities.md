---
id: 2026-10-11-rewrite-ai-real-world-05-uneven-abilities
title: Rewrite the explainer ai-real-world-05-uneven-abilities with the facts it lacks
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
  - docs/videos/ai-real-world-05-uneven-abilities
---

# Rewrite the explainer ai-real-world-05-uneven-abilities with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-real-world-05-uneven-abilities`, 「AI 都能解難題了，為什麼還會犯這種錯？」.
- On the site: final video approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 8 of the 12 questions asked.
- The reader's reason: 片名問「為什麼還會犯這種錯」，全片卻沒有出現任何一個真實的錯誤，只有一個 IMO 成績加上比喻、虛構例子與大量「我們沒有實測」的聲明，觀眾帶走的只有四個提問。
- What it needs, in the reader's words: 需要補新事實：至少一兩個有來源的真實失誤案例，並把「四個條件」實際套在 IMO 成績上逐欄填出來，讓片名的問題有具體答案。同時刪掉大部分談影片自己沒做什麼的句子與比喻，這部分只需改寫。
- Kind of work: new facts or runs, then a rewrite.
- Made by a Codex session. The owner said on 2026-10-11 that the Claude sessions take the rewrite over.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: Codex's local folder, `docs/ai-video-season-01/media/<episode>/script-storyboard.md` (also on the branch `origin/claude/ai-video-planning-l43qas`). The site holds only the finished cut.

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
node tools/video/cli.mjs lint --slug ai-real-world-05-uneven-abilities
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
