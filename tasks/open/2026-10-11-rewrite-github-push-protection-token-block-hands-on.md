---
id: 2026-10-11-rewrite-github-push-protection-token-block-hands-on
title: Rewrite the tutorial github-push-protection-token-block-hands-on from real runs
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
  - docs/videos/github-push-protection-token-block-hands-on
---

# Rewrite the tutorial github-push-protection-token-block-hands-on from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `github-push-protection-token-block-hands-on`, 「GitHub 推送保護教學：把一次性權杖推上去，看它在哪一行擋下」.
- On the site: narration synthesized, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 7 of the 16 questions asked. A second reader: rework, 6 failed.
- The reader's reason: 片名說是實作，但全片沒有跑過任何一次 push，被擋、改乾淨、密碼對照三個結果都只是「預期｜未實測」，觀眾拿到的等於官方文件的整理。
- What it needs, in the reader's words: 要真的跑一次 push-guard-demo，把權杖被擋的原始訊息、amend 後重推成功、自由格式密碼擋不擋、git check-ignore 的輸出換成帶日期的實際結果，並補上較早提交的處理指令，同時刪掉「沒有跑過」這類交代。這需要新的實測，不是只改稿。
- Kind of work: new runs, then a rewrite.
- Paused on the host on 2026-10-11 by the owner's decision: a `STOP` file is in its work folder, so the worker pays for nothing more. Remove it only when the rewrite is ready to be produced.

What it failed: the title's question answered with a specific answer (T1); the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2). Also D3, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/github-push-protection-token-block-hands-on/video.json` in the video-worker container. Copy it into `docs/videos/github-push-protection-token-block-hands-on/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug github-push-protection-token-block-hands-on
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
