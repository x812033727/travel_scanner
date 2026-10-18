---
id: 2026-10-11-rewrite-reddit-rss-shutdown-find-your-feeds
title: Rewrite the tutorial reddit-rss-shutdown-find-your-feeds from real runs
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/reddit-rss-shutdown-find-your-feeds
---

# Rewrite the tutorial reddit-rss-shutdown-find-your-feeds from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `reddit-rss-shutdown-find-your-feeds`, 「Reddit 11 月 13 日停 RSS：一行搜尋，找出你閱讀器裡會停的訂閱」.
- On the site: blocked, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 8 of the 16 questions asked.
- The reader's reason: 全片的指令和輸出都沒有實際跑過（卡片上反覆寫「這支影片沒有跑過」），而且 8 筆訂閱裡找 3 筆 Reddit 來源，看一眼閱讀器的訂閱清單就知道，真正帶得走的只有五個日期和「你的用法看哪個日期」那張表。
- What it needs, in the reader's words: 需要新的實跑和查證，不是只改寫：拿一份筆數多到看不完的真實閱讀器匯出檔（指名閱讀器和匯出選單的位置）實際跑出輸出，並讀 Reddit 自己的公告確認日期。刪掉所有講「沒有跑過」的旁白，把篇幅留給受影響的人接下來能換成什麼。
- Kind of work: new runs, then a rewrite.
- Paused on the host on 2026-10-11 by the owner's decision: a `STOP` file is in its work folder, so the worker pays for nothing more. Remove it only when the rewrite is ready to be produced.

What it failed: the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/reddit-rss-shutdown-find-your-feeds/video.json` in the video-worker container. Copy it into `docs/videos/reddit-rss-shutdown-find-your-feeds/` to rewrite it here.

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

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Make the missing runs on the owner's machine (the host worker runs nothing) and record them.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug reddit-rss-shutdown-find-your-feeds
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
