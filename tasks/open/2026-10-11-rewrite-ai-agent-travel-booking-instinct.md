---
id: 2026-10-11-rewrite-ai-agent-travel-booking-instinct
title: Tighten the explainer ai-agent-travel-booking-instinct
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
  - docs/videos/ai-agent-travel-booking-instinct
---

# Tighten the explainer ai-agent-travel-booking-instinct

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-agent-travel-booking-instinct`, 「AI 代理最常被拿來訂旅程？創辦人口中的「近十億美元」該怎麼聽」.
- On the site: on YouTube, YouTube id `Ztg1vzKfLBM` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 全片真正屬於這則新聞的內容只有兩個未經證實的數字、一個「不能相乘」的提醒和餐廳訂位爭議，其餘九十六句裡約五十句是通用的付款叮嚀、來源交代與畫面描寫，後半的三道界線也沒有任何一次代理實際訂位或付款的結果支撐。
- What it needs, in the reader's words: 新聞段要砍掉場景句與重複的來源交代，壓到現在的一半以內；第五章的通用付款叮嚀要換成觀眾用得到的代理實際訂一次旅程的結果（它在哪一步停下來要你確認、哪裡訂錯、單筆上限與刷卡通知實際在哪裡設），這需要新的實測與新事實，只改寫不夠。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/ai-agent-travel-booking-instinct/video.json` in the video-worker container. Copy it into `docs/videos/ai-agent-travel-booking-instinct/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug ai-agent-travel-booking-instinct
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
