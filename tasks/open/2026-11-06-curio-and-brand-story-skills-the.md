---
id: 2026-11-06-curio-and-brand-story-skills-the
title: Curio and brand-story skills: the eye check, the closed-eye fallback, and re-judging after a judge question changes
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-06T01:10:27Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
---

# Curio and brand-story skills: the eye check, the closed-eye fallback, and re-judging after a judge question changes

## Why

原來如此事務所 found odd eyes the keyframe judge had passed (站主 2026-11-05: 「眼珠怪怪的 … 不只一次」).
The judge's `anatomy` question now asks about eyes (task `2026-11-05-keyframe-judge-checks-the-eyes-mismatched`),
and that applies to every series, curio and brand stories included. Two lessons from P02/P05 belong in their
skills too, after PR #2027 (which rewrites both skills) has merged:

1. The judge still lets slight cross-eyes through; before the storyboard goes to the owner, an agent checks
   every face enlarged. A face that fails three takes is drawn with closed happy eyes, from behind, or replaced
   by an object close-up.
2. A changed judge question re-stamps every verdict: the next `keyframes` run re-judges every drawn shot and
   redraws what fails, approved storyboards included. Host episodes mid-keyframes when that change deploys
   will be re-judged; deploy it between episodes, or keep approved shots on their old question.

## Definition of done

- [ ] curio-episode and brand-story skills (both copies, byte-identical) carry the two lessons.
- [ ] `npm run test:tools` passes.

## Notes

- Wait for PR #2027 to merge: it rewrites §插圖提示詞怎麼寫 and the acceptance list in both skills.
