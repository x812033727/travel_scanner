---
id: 2026-10-11-rewrite-gemini-student-offer
title: Rewrite the explainer gemini-student-offer with the facts it lacks
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
  - docs/videos/gemini-student-offer
---

# Rewrite the explainer gemini-student-offer with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `gemini-student-offer`, 「Google AI 學生方案免費一年，台灣大學生真的符合資格嗎？四道關卡全解析」.
- On the site: on YouTube, YouTube id `FYHFsj0SB7Q` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked.
- The reader's reason: 片名問「台灣大學生符不符合」，片尾卻說「問號留給你自己回答」，中間又塞了一段用虛構公告、沒真的問過模型的 AI 筆記示範，真正有用的內容五行就寫完。
- What it needs, in the reader's words: 需要新的事實：實際用台灣大學生身分走一次兌換與 SheerID 驗證（或查出台灣學校在不在支援名單），給出「可以／不行／卡在哪一關」的答案。其餘只要改寫：刪掉虛構公告的筆記示範與即時語音那段，把重複的「沒被排除不等於可以領」和設提醒的叮嚀各留一次。
- Kind of work: new facts or runs, then a rewrite.

What it failed: the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

the branch `origin/claude/video-batch-2`, `docs/videos/gemini-student-offer/`; whether that is the cut that was produced was not confirmed.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.
- [ ] The owner decides what happens to the cut that is already on YouTube: a video's file
      cannot be replaced there, so a rewrite is a new upload.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Find the missing facts at their sources, or make the missing run, and record where each came from.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug gemini-student-offer
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
