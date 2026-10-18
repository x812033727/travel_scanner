---
id: 2026-10-11-rewrite-gemini-4-argon-who-can-use-it
title: Rewrite the explainer gemini-4-argon-who-can-use-it with the facts it lacks
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
  - docs/videos/gemini-4-argon-who-can-use-it
---

# Rewrite the explainer gemini-4-argon-who-can-use-it with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `gemini-4-argon-who-can-use-it`, 「Gemini 4 Argon 發布了，為什麼你的 Gemini 裡找不到？誰能用、數字是誰說的、現在該做什麼」.
- On the site: on YouTube, YouTube id `uoVKy-nFXB4` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked.
- The reader's reason: 問題選得對、答案也明確，但全片能帶走的只有五句話，沒有放出任何一個實際的成績或價格數字，其餘大半是排隊、三扇門、考卷這類比喻和換哪個模型都適用的通用提醒。
- What it needs, in the reader's words: 把 Google 公告裡實際的成績、案例和 API 價格連同出處原文放上卡片，並拿一個情境算給觀眾看（例如現在訂 Ultra 換得到什麼、換不到什麼），同時刪掉比喻句和通用提醒，把長度壓到事實撐得起的範圍。需要回公告補事實，不需要新的實測。
- Kind of work: new facts or runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/gemini-4-argon-who-can-use-it/video.json` in the video-worker container. Copy it into `docs/videos/gemini-4-argon-who-can-use-it/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug gemini-4-argon-who-can-use-it
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
