---
id: 2026-10-11-rewrite-macos-full-disk-access-terminal-check
title: Rewrite the tutorial macos-full-disk-access-terminal-check from real runs
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
  - docs/videos/macos-full-disk-access-terminal-check
---

# Rewrite the tutorial macos-full-disk-access-terminal-check from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `macos-full-disk-access-terminal-check`, 「AI 代理叫你開「完整磁碟取用權限」？先用一行指令查終端機現在拿到什麼」.
- On the site: languages, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 7 of the 16 questions asked.
- The reader's reason: 全片的輸出都標著「預期、尚未實際跑過」，連「代理沿用終端機權限」這個最關鍵的說法也只是站主看法，觀眾拿到的只有一行 ls 加上 Apple 說明頁的整理，五行就寫得完。
- What it needs, in the reader's words: 要在真的 Mac 上把開、驗、關跑一次，並讓一個命令列代理在開與關兩種狀態下實際去讀 Safari 或郵件的資料，把真實輸出放上卡片，同時刪掉重複三次的前後對照和「尚未實際跑過」的聲明。這需要新的實跑，不是只改寫。
- Kind of work: new runs, then a rewrite.
- Paused on the host on 2026-10-11 by the owner's decision: a `STOP` file is in its work folder, so the worker pays for nothing more. Remove it only when the rewrite is ready to be produced.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1). Also D3, D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/macos-full-disk-access-terminal-check/video.json` in the video-worker container. Copy it into `docs/videos/macos-full-disk-access-terminal-check/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug macos-full-disk-access-terminal-check
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
