---
id: 2026-10-11-rewrite-grok-4-7-bedrock-output-doubles
title: Rewrite the explainer grok-4-7-bedrock-output-doubles with the facts it lacks
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
  - docs/videos/grok-4-7-bedrock-output-doubles
---

# Rewrite the explainer grok-4-7-bedrock-output-doubles with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `grok-4-7-bedrock-output-doubles`, 「Grok 4.7 上了 Amazon Bedrock：分數變高，每項任務的輸出卻多一倍，帳單該怎麼算」.
- On the site: on YouTube, YouTube id `1I0KIfGi-0Q` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 8 of the 12 questions asked.
- The reader's reason: 全片沒有任何一個真實數字（輸出倍數和單價都叫觀眾自己去官網查，「兩倍」只是假設），92 句旁白裡約 30 句是放到任何模型都成立的建議、約 22 句是比喻，看完只比標題多知道「分數是在最高推理強度下測的」這一行。
- What it needs, in the reader's words: 需要補新的事實，不只是改寫：把評測量到的每任務輸出 token 倍數、Bedrock 定價頁某一天的新舊模型輸出單價寫上卡片並標日期，用真實數字把算式算完，並指出推理強度那個設定叫什麼、在哪裡調。同時把比喻句和通用建議砍掉大半，讓片長配得上內容。
- Kind of work: new facts or runs, then a rewrite.

What it failed: the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); the takeaway can be had from the title or the source's first paragraph (X1); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/grok-4-7-bedrock-output-doubles/video.json` in the video-worker container. Copy it into `docs/videos/grok-4-7-bedrock-output-doubles/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug grok-4-7-bedrock-output-doubles
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
