---
id: 2026-10-11-rewrite-gpt-6-sol-luna-where-to-use
title: Rewrite the explainer gpt-6-sol-luna-where-to-use with the facts it lacks
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
  - docs/videos/gpt-6-sol-luna-where-to-use
---

# Rewrite the explainer gpt-6-sol-luna-where-to-use with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `gpt-6-sol-luna-where-to-use`, 「GPT-6 出了，為什麼我的 ChatGPT 對話裡沒有？Sol 與 Luna 在哪裡用、API 怎麼算」.
- On the site: languages sent, YouTube id `KurEPz5z7hA` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked.
- The reader's reason: 全片能帶走的內容五行就寫完，而且「API 降價跟誰比」那一章從頭到尾沒有任何一個價格或降幅，帳單試算只剩一條填不了數字的公式。
- What it needs, in the reader's words: API 那一章要補上官網價目表的實際單價（Sol、Luna 對 GPT-5.6 促銷價與原價），用真實數字把帳單算完，並刪掉重複約九次的「一般對話還沒有」和約四分之一的串場句，壓成四到五分鐘。這需要新的事實（價目表數字，最好再加各入口模型選單的實際畫面），不是只改寫就夠。
- Kind of work: new facts or runs, then a rewrite.

What it failed: a number or a case worked through on screen (X2); key facts in the source's own words on cards that name it (X3). Also D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/gpt-6-sol-luna-where-to-use/video.json` in the video-worker container. Copy it into `docs/videos/gpt-6-sol-luna-where-to-use/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug gpt-6-sol-luna-where-to-use
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
