---
id: 2026-10-11-rewrite-google-vids-omni-free-quota
title: Rewrite the explainer google-vids-omni-free-quota with the facts it lacks
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
  - docs/videos/google-vids-omni-free-quota
---

# Rewrite the explainer google-vids-omni-free-quota with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `google-vids-omni-free-quota`, 「Google Vids 免費用 AI 做影片：誰能用？每月額度兩份說明頁寫得不一樣，怎麼讀」.
- On the site: on YouTube, YouTube id `S88lbAsLz2E` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked.
- The reader's reason: 片名問的「每月額度」和「中文提示可不可以」都沒有給出具體答案，全片約四分之一的旁白在講「說明頁寫了什麼、沒寫什麼」，觀眾看完還是得自己去查數字、自己去試。
- What it needs, in the reader's words: 需要新的事實與實測：把兩份說明頁當天的每月上限數字連同查閱日期放上畫面並實際算一次能做幾支，再用中文提示實際生成一段、把結果給觀眾看。其餘「以說明頁為準」「官方沒寫」的重複句子只要改寫刪減即可。
- Kind of work: new facts or runs, then a rewrite.

What it failed: the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/google-vids-omni-free-quota/video.json` in the video-worker container. Copy it into `docs/videos/google-vids-omni-free-quota/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug google-vids-omni-free-quota
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
