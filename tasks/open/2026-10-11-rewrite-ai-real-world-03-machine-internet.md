---
id: 2026-10-11-rewrite-ai-real-world-03-machine-internet
title: Rewrite the explainer ai-real-world-03-machine-internet with the facts it lacks
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
  - docs/videos/ai-real-world-03-machine-internet
---

# Rewrite the explainer ai-real-world-03-machine-internet with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-real-world-03-machine-internet`, 「如果留言、照片、影片都是 AI，網路會變成什麼樣？」.
- On the site: final video approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 8 of the 12 questions asked.
- The reader's reason: 全片只有三個事實（53%、兩篇研究）而且各只講一句，66 句旁白裡大半是提醒、來源但書和關於本片自己的聲明，片名問的「網路會變成什麼樣」沒有具體回答。
- What it needs, in the reader's words: 需要補新事實，不只是改寫：把 53% 拆開（報告裡好、壞機器人各占多少）、用帶數字的例子把「請求不等於人頭」算一次、說出兩篇研究各自在什麼設定下看到什麼結果，並在卡片上寫出來源名稱與原文數字。同時刪掉關於本片畫面與製作原則的句子，結尾對片名給一個有條件的明確答案。
- Kind of work: new facts or runs, then a rewrite.
- Made by a Codex session. The owner said on 2026-10-11 that the Claude sessions take the rewrite over.

What it failed: the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

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
node tools/video/cli.mjs lint --slug ai-real-world-03-machine-internet
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
