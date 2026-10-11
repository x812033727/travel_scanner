---
id: 2026-10-11-rewrite-github-copilot-local-sandbox-hands-on
title: Rewrite the tutorial github-copilot-local-sandbox-hands-on from real runs
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
  - docs/videos/github-copilot-local-sandbox-hands-on
---

# Rewrite the tutorial github-copilot-local-sandbox-hands-on from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `github-copilot-local-sandbox-hands-on`, 「GitHub Copilot 本機沙盒教學：同一句要求，沙盒開與不開差在哪」.
- On the site: languages, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 13 of the 16 questions asked.
- The reader's reason: 整支片的結果欄全是「預期・未實測」，連開啟沙盒的設定名稱都留空，觀眾看完既不知道開與關實際差在哪，也沒辦法照著做。
- What it needs, in the reader's words: 要實際把沙盒關與開各跑一次，把官方的設定名稱與位置、被擋下時的訊息原文，以及改檔跑測試、寫入、網路三題的真實輸出放上卡片，並拿掉十多句「這支影片沒有測」的旁白。這需要新的實跑紀錄與官方原文，不是只改寫就能解決。
- Kind of work: new runs, then a rewrite.
- Paused on the host on 2026-10-11 by the owner's decision: a `STOP` file is in its work folder, so the worker pays for nothing more. Remove it only when the rewrite is ready to be produced.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); the main result can be had the simple way with nothing lost (W2); the content of the thing taught is on screen (W3); the viewer could make or change one from what is shown (W4); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2); the example can be followed without an unseen download (E3). Also D3, D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/github-copilot-local-sandbox-hands-on/video.json` in the video-worker container. Copy it into `docs/videos/github-copilot-local-sandbox-hands-on/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug github-copilot-local-sandbox-hands-on
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
