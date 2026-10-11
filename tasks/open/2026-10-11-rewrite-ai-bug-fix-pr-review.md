---
id: 2026-10-11-rewrite-ai-bug-fix-pr-review
title: Rewrite the tutorial ai-bug-fix-pr-review from real runs
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
  - docs/videos/ai-bug-fix-pr-review
---

# Rewrite the tutorial ai-bug-fix-pr-review from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-bug-fix-pr-review`, 「AI 修好 Bug 就能合併？三個 PR 檢查點」.
- On the site: on YouTube, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 9 of the 16 questions asked.
- The reader's reason: AI 的修補在三道關全部過關，整支片沒有任何一關真的抓到問題，剩下的大半是通用審查守則和「這不是真實 PR」的範圍聲明。
- What it needs, in the reader's words: 需要新的實跑：換成或加上一份「AI 自寫測試全綠、卻在某一關被擋下」的修補（例如刪掉輸入驗證或把特例寫死），並把看差異、拿舊碼跑驗收的實際指令與原始輸出放上卡片。十多句範圍聲明與結尾重複的通用守則則只需刪改，不必新事實。
- Kind of work: new runs, then a rewrite.
- Made by a Codex session. The owner said on 2026-10-11 that the Claude sessions take the rewrite over.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); more than ten narration sentences that hold without the subject (D2); the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2); the example can be followed without an unseen download (E3). Also D3, D4, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-bug-fix-pr-review/` on main.

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
node tools/video/cli.mjs lint --slug ai-bug-fix-pr-review
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
