---
id: 2026-10-11-rewrite-google-synthid-site-not-found-not-proof
title: Rewrite the explainer google-synthid-site-not-found-not-proof with the facts it lacks
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
  - docs/videos/google-synthid-site-not-found-not-proof
---

# Rewrite the explainer google-synthid-site-not-found-not-proof with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `google-synthid-site-not-found-not-proof`, 「Google 開放 SynthID 查驗網站：查不到浮水印，就代表不是 AI 做的嗎？」.
- On the site: on YouTube, YouTube id `oxEtlA8GWas` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked.
- The reader's reason: 全片能用的內容五行就寫完，卻沒有實際跑過查驗網站、沒給網址、也沒教怎麼找原始出處，133 句旁白裡約三分之一是場景比喻和「報導說、以官網為準」。
- What it needs, in the reader's words: 需要新的實測：把幾張圖（Gemini 生成的、真照片、經 LINE 轉傳或截圖過的 AI 圖）實際丟進查驗網站，把結果畫面、台灣能不能用、要不要登入放上卡片，用實測取代「第四種是我的推測」，並補上找原始出處的具體步驟（例如以圖搜圖）。另外只需改寫的部分是刪掉大半場景比喻與重複的來源句，把第四章的通用轉傳提醒縮成一張卡。
- Kind of work: new facts or runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); a number or a case worked through on screen (X2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/google-synthid-site-not-found-not-proof/video.json` in the video-worker container. Copy it into `docs/videos/google-synthid-site-not-found-not-proof/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug google-synthid-site-not-found-not-proof
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
