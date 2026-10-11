---
id: 2026-10-11-rewrite-cloudflare-registrar-renewal-price-ai-agent
title: Rewrite the explainer cloudflare-registrar-renewal-price-ai-agent with the facts it lacks
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
  - docs/videos/cloudflare-registrar-renewal-price-ai-agent
---

# Rewrite the explainer cloudflare-registrar-renewal-price-ai-agent with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `cloudflare-registrar-renewal-price-ai-agent`, 「網域第一年便宜，第五年呢？Cloudflare 把續約價擺上搜尋結果，還讓 AI 代理能替你下單」.
- On the site: on YouTube, YouTube id `LzAwyF-7-H4` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 8 of the 12 questions asked.
- The reader's reason: 標題問「第五年呢」，全片卻只給一條沒填數字的算式，價格表寫「以官網為準／自己算」、代理對話標明非實測，觀眾從標題和說明欄就能拿到同樣的東西。
- What it needs, in the reader's words: 需要補新的事實與實測：挑兩個後綴，把某一天官網顯示的註冊價和續約價實際填進算式算出五年合計，並列出網域相關的權杖權限名稱（最好附一次沙盒實跑的輸出）。同時把二十多句比喻場景和十多句「官網說／以官網為準」刪到只剩必要的，這部分只需要改寫。
- Kind of work: new facts or runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the title's question answered with a specific answer (T1); the takeaway can be had from the title or the source's first paragraph (X1); a number or a case worked through on screen (X2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/cloudflare-registrar-renewal-price-ai-agent/video.json` in the video-worker container. Copy it into `docs/videos/cloudflare-registrar-renewal-price-ai-agent/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug cloudflare-registrar-renewal-price-ai-agent
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
