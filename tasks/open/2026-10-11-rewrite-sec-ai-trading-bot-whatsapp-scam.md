---
id: 2026-10-11-rewrite-sec-ai-trading-bot-whatsapp-scam
title: Tighten the explainer sec-ai-trading-bot-whatsapp-scam
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
  - docs/videos/sec-ai-trading-bot-whatsapp-scam
---

# Tighten the explainer sec-ai-trading-bot-whatsapp-scam

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `sec-ai-trading-bot-whatsapp-scam`, 「「AI 交易機器人」保證幫你賺？SEC 起訴的兩組詐騙，餌是這樣組成的」.
- On the site: on YouTube, YouTube id `9mTPp71uBu8` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 全片能帶走的新東西五行就寫完，102 句旁白裡約三成是比喻、場景和通用防詐叮嚀，連「自己去哪個網站查」都只說以主管機關官網為準，撐不起十分鐘。
- What it needs, in the reader's words: 要補上起訴內容裡的具體細節（承諾的報酬與機器人租金、受害規模、偽造文件的樣子、提款被擋的過程），並把「自己查」寫成叫得出名字的查核網站與步驟，這部分需要新查的事實。同時刪掉比喻段落，把「1,500 萬怎麼讀」一章壓成一張卡，這部分只需改寫。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/sec-ai-trading-bot-whatsapp-scam/video.json` in the video-worker container. Copy it into `docs/videos/sec-ai-trading-bot-whatsapp-scam/` to rewrite it here.

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
- [ ] Cut what repeats and add the one thing the reader says is missing.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug sec-ai-trading-bot-whatsapp-scam
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
