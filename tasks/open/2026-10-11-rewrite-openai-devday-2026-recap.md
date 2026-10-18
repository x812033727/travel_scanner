---
id: 2026-10-11-rewrite-openai-devday-2026-recap
title: Tighten the explainer openai-devday-2026-recap
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
  - docs/videos/openai-devday-2026-recap
---

# Tighten the explainer openai-devday-2026-recap

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `openai-devday-2026-recap`, 「DevDay 2026 的 25 項，你今天碰得到幾項？照方案分五張清單，這週就能做」.
- On the site: final video approved, YouTube id `MO6lHFIn3yA` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 3 of the 12 questions asked.
- The reader's reason: 片子有實在的數字和界線（登入只給三樣、10/14 退場、只有 Pro 500 含 Ultrafast、6 倍與 8 份），但 25 項裡多數只唸出名字再接一句「以官網為準」或一個比喻，觀眾帶得走的集中在少數幾段。
- What it needs, in the reader's words: 把約 19 句「以官網為準／頁上沒寫」和約 14 句比喻換成每一項「它做什麼、誰今天能用」的一句話，講不清的項目（工作站、私密智慧、Decisions API、Bedrock）要嘛說明用途要嘛刪掉。「這週做的一件事」要在卡片上寫完整：dot 先核准的設定在哪裡、Codex 該改選哪個模型、Sol 月帳單的公式直接列出來而不是指向另一支片；主要是改寫，後面這三點需要補查少量事實。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: only questions that nearly every film failed. Also D3, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/openai-devday-2026-recap/` on main.

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
node tools/video/cli.mjs lint --slug openai-devday-2026-recap
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
