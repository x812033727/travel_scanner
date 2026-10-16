---
id: 2026-10-11-rewrite-ai-term-embedding
title: Rewrite the explainer ai-term-embedding with the facts it lacks
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
  - docs/videos/ai-term-embedding
---

# Rewrite the explainer ai-term-embedding with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-term-embedding`, 「嵌入向量是什麼？搜尋第一名，為什麼還不能當答案｜AI 名詞」.
- On the site: upload package approved, YouTube id `a10UMT6xqws` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked. A second reader: rework, 7 failed.
- The reader's reason: 全片的「證據」是作者手填座標安排出來的結果，旁白有二十多句在聲明「沒有測模型、只是示意」，觀眾看完只得到「第一名要回原文核對」這句常識，連一個真正的向量長什麼樣子都沒看到。
- What it needs, in the reader's words: 需要新的實跑，不是只改寫：用一個真實嵌入模型把這六筆文字和查詢算出向量與分數，在卡片上給出向量的樣子與真實排序（寫著「今天休館」那筆是否仍排在前面），取代手填座標。再把二十多句「沒有測、只是示意」和十多句比喻場景各刪到兩句以內，並在卡片上補一個確切可做的動作，這部分只需改寫。
- Kind of work: new facts or runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); one exact thing to do, check or decide, in full on a card (A1); more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-term-embedding/` on main.

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
node tools/video/cli.mjs lint --slug ai-term-embedding
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
