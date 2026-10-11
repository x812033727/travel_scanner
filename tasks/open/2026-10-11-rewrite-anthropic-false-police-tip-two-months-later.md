---
id: 2026-10-11-rewrite-anthropic-false-police-tip-two-months-later
title: Tighten the explainer anthropic-false-police-tip-two-months-later
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/anthropic-false-police-tip-two-months-later
---

# Tighten the explainer anthropic-false-police-tip-two-months-later

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `anthropic-false-police-tip-two-months-later`, 「AI 代理送出去的東西，你多久才會知道？假線報據報兩個多月才被發現」.
- On the site: retrying, not uploaded.
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked.
- The reader's reason: 新聞本身三分鐘就講完，後面四章是「每句標出處」和「每週看一次所以最晚第 7 天」這類不看片也知道的通則，沒有任何一個實際代理產品的紀錄位置或設定，觀眾看完做不了具體的事。
- What it needs, in the reader's words: 把第二章的出處分類縮成一張卡，第三到五章改成至少一個真實代理產品的實際畫面：送出紀錄在哪裡看、「送出前要人確認」的設定叫什麼、在哪裡開。這需要新的事實與實際操作，不是只改寫就能補上。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/anthropic-false-police-tip-two-months-later/video.json` in the video-worker container. Copy it into `docs/videos/anthropic-false-police-tip-two-months-later/` to rewrite it here.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Cut what repeats and add the one thing the reader says is missing.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug anthropic-false-police-tip-two-months-later
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
