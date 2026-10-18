---
id: 2026-10-11-rewrite-gemini-live-guided-vision-read-and-find
title: Rewrite the tutorial gemini-live-guided-vision-read-and-find from real runs
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
  - docs/videos/gemini-live-guided-vision-read-and-find
---

# Rewrite the tutorial gemini-live-guided-vision-read-and-find from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `gemini-live-guided-vision-read-and-find`, 「Gemini Live 的 Guided Vision 怎麼用？讓 AI 唸細字、找東西，還提示你怎麼拿鏡頭」.
- On the site: languages, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 7 of the 16 questions asked.
- The reader's reason: 三個任務的結果全部標成「預期、尚未實測」，觀眾只拿到開啟步驟和一句要說的話，沒看到 Guided Vision 實際怎麼提示鏡頭、唸得對不對。
- What it needs, in the reader's words: 需要新的實測：在真的手機上把帳單、鑰匙、門口三個任務跑過，放上它實際說的鏡頭提示與唸出的內容（日期、機型、版本、唸錯的地方），並用同一張帳單跟 Lens 比一次。實測補上後，刪掉「預期 vs 實際」那張卡和二十多句通用的核對叮嚀，這部分只需要改寫。
- Kind of work: new runs, then a rewrite.
- Paused on the host: a `STOP` file another session placed on 2026-10-10 is in its work folder, and on 2026-10-11 the owner decided it stays paused, so the worker pays for nothing more. Remove it only when the rewrite is ready to be produced.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); more than ten narration sentences that hold without the subject (D2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1). Also D3, D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/gemini-live-guided-vision-read-and-find/video.json` in the video-worker container. Copy it into `docs/videos/gemini-live-guided-vision-read-and-find/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug gemini-live-guided-vision-read-and-find
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
