---
id: 2026-10-11-rewrite-vibe-coding-first-website-2026
title: Rewrite the tutorial vibe-coding-first-website-2026 from real runs
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
  - docs/videos/vibe-coding-first-website-2026
---

# Rewrite the tutorial vibe-coding-first-website-2026 from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `vibe-coding-first-website-2026`, 「Claude、ChatGPT、Gemini 哪個最適合做第一個網站？不會寫程式也能免費上線」.
- On the site: final video approved, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 8 of the 16 questions asked.
- The reader's reason: 片名問三家哪個最適合，但整支片沒有任何一家實際做出來的網頁，答案只剩「挑你帳號用得到的那家」，上線也只講限制沒有步驟。
- What it needs, in the reader's words: 需要新的實跑：把同一段需求真的貼進三家，把各自做出來的頁面和差異放上卡片並據此給出選擇，再把一次免費上線的完整步驟逐步放上畫面。另外只需改寫的部分是把十來句「官方寫」收成來源卡，不必每句都講出處。
- Kind of work: new runs, then a rewrite.

What it failed: the title's question answered with a specific answer (T1); the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2); the example can be followed without an unseen download (E3). Also D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/vibe-coding-first-website-2026/` on main.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
      For a tutorial that means real runs in the run log, the simple way run beside the
      subject on the same input, and no narration about the making.
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Make the missing runs on the owner's machine (the host worker runs nothing) and record them.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug vibe-coding-first-website-2026
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
