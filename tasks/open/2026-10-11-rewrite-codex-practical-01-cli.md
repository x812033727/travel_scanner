---
id: 2026-10-11-rewrite-codex-practical-01-cli
title: Rewrite the tutorial codex-practical-01-cli from real runs
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
  - docs/videos/codex-practical-01-cli
---

# Rewrite the tutorial codex-practical-01-cli from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `codex-practical-01-cli`, 「Codex 實作 01 CLI：讀懂專案與測試，別把「跑完」當成「做對」」.
- On the site: on YouTube, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 7 of the 13 questions asked. A second reader: rework, 9 failed.
- The reader's reason: 主要成果（2 過 1 敗、visibleTasks 沒用 filter）自己跑一次 node --test 就看得到，片中也沒有任何 Codex「跑完卻沒做對」的實例，真正新的只有 exec 只讀指令與兩個退出碼，卻被四十多句通用叮嚀和約二十句製作說明撐成 60 個場景。
- What it needs (the coordinating session's summary of the reader's sheet): 主要成果自己跑一次測試就看得到：主例要有 Codex 跑完卻沒做對、被這套做法抓到的實例，把 Codex 的實際回覆攤開逐項核對，並刪掉約五十句通用叮嚀與約二十句製作說明。需要新的實跑。
- Kind of work: new runs, then a rewrite.
- Made by a Codex session. The owner said on 2026-10-11 that the Claude sessions take the rewrite over.

What it failed: the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); more than ten narration sentences that hold without the subject (D2); the example can be followed without an unseen download (E3). Also D1, D3, D4, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

the branch `origin/codex/codex-practical-series-20261011` (pull request 1429), `docs/videos/codex-practical-01-cli/`.

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
node tools/video/cli.mjs lint --slug codex-practical-01-cli
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
