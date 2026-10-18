---
id: 2026-10-11-rewrite-ai-real-world-01-image-trust
title: Rewrite the explainer ai-real-world-01-image-trust with the facts it lacks
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
  - docs/videos/ai-real-world-01-image-trust
---

# Rewrite the explainer ai-real-world-01-image-trust with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-real-world-01-image-trust`, 「照片不能當證據之後，我們還能相信什麼？」.
- On the site: final video approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 8 of the 12 questions asked. A second reader: rework, 10 failed.
- The reader's reason: 全片沒有任何真實案例、數字或可操作的工具，三個查證步驟只停在口頭提問，觀眾看完得到的是五行就寫得完的通用媒體識讀原則。
- What it needs, in the reader's words: 需要補新的事實與實際操作：用至少一張真實被錯置脈絡的圖片，把三個步驟實際走一遍（以圖搜圖、查內容憑證的工具名稱與位置、查到的結果），並把要問的問題完整放上畫面。同時刪掉第 09 段與各段的自我聲明，這部分只需改寫，但前者光靠改寫做不到。
- Kind of work: new facts or runs, then a rewrite.
- Made by a Codex session. The owner said on 2026-10-11 that the Claude sessions take the rewrite over.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); one exact thing to do, check or decide, in full on a card (A1); more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

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
node tools/video/cli.mjs lint --slug ai-real-world-01-image-trust
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
