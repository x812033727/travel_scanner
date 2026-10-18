---
id: 2026-10-11-rewrite-claude-code-plugins-hands-on
title: Rewrite the tutorial claude-code-plugins-hands-on from real runs
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-plugins-hands-on
---

# Rewrite the tutorial claude-code-plugins-hands-on from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `claude-code-plugins-hands-on`, 「Claude Code Plugin 教學：Skill、hook 包成外掛，載進第二個專案逐一驗」.
- On the site: on YouTube, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 6 of the 13 questions asked.
- The reader's reason: 主軸「載入 3 次對沒載入 3 次」是誰都猜得到的結果，真正有料的「驗證通過但守門沒執行、專案與外掛並存時跑兩遍、專案外的範本讀不到」被埋在後半，又沒有跟直接複製 .claude 資料夾比較，完整的載入指令也沒上畫面，應改以這幾個坑為主軸重剪。
- What it needs (the coordinating session's summary of the reader's sheet): 補跑「直接把 .claude 資料夾複製過去」當對照，主軸改成驗證通過但守門沒執行、專案與外掛並存時跑兩遍這幾個坑，完整的載入指令放上卡片。需要新的實跑。
- Kind of work: new runs, then a rewrite.

What it failed: the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); every step to repeat is on a card in full (E2); the example can be followed without an unseen download (E3). Also D1, D3, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/claude-code-plugins-hands-on/` on main.

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
node tools/video/cli.mjs lint --slug claude-code-plugins-hands-on
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
