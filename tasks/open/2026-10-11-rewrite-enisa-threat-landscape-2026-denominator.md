---
id: 2026-10-11-rewrite-enisa-threat-landscape-2026-denominator
title: Rewrite the tutorial enisa-threat-landscape-2026-denominator from real runs
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:49:18Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/enisa-threat-landscape-2026-denominator
---

# Rewrite the tutorial enisa-threat-landscape-2026-denominator from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `enisa-threat-landscape-2026-denominator`, 「資安報告說 60.4% 攻擊靠漏洞？分母只有 5.2%：看懂 ENISA 2026 威脅報告」.
- On the site: on YouTube, YouTube id `HCpjTmKqQrQ` (already uploaded).
- Read as a tutorial. Verdict: rework. Failed 7 of the 16 questions asked.
- The reader's reason: 全片只有一組假設數字（10% × 50% = 5%），沒有拿任何一份真實報告來套這三個問題，三問又前後複述了四遍，內容五行就寫得完。
- What it needs, in the reader's words: 拿一份真實的資安報告，把它的統計期間、統計範圍和一個真實百分比的分母原文放上卡片並實際換算一次，同時刪掉重複的三問複述與章節預告。這需要新的事實（讀原始報告取得數字與原文），不是只改寫就能補上。
- Kind of work: new runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); more than ten narration sentences that hold without the subject (D2); the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1). Also D4, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/enisa-threat-landscape-2026-denominator/video.json` in the video-worker container. Copy it into `docs/videos/enisa-threat-landscape-2026-denominator/` to rewrite it here.

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
- [ ] The owner decides what happens to the cut that is already on YouTube: a video's file
      cannot be replaced there, so a rewrite is a new upload.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Make the missing runs on the owner's machine (the host worker runs nothing) and record them.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug enisa-threat-landscape-2026-denominator
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
