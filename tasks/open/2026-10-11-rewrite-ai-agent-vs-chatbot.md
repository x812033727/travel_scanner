---
id: 2026-10-11-rewrite-ai-agent-vs-chatbot
title: Tighten the explainer ai-agent-vs-chatbot
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
  - docs/videos/ai-agent-vs-chatbot
---

# Tighten the explainer ai-agent-vs-chatbot

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-agent-vs-chatbot`, 「AI 代理跟聊天機器人差在哪？一個行程任務看懂」.
- On the site: on YouTube, not uploaded.
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 臺博館「週一休館卻在教師節開館」的例子確實講清楚了差別，但全片沒有任何真實的聊天機器人或代理輸出（聊天回答是自製範例、查詢是製作者自己開網頁），其餘大半是互相重疊的驗收清單和通用叮嚀。
- What it needs, in the reader's words: 需要新的實跑：把同一句交辦分別丟給沒有工具的聊天和有查網頁工具的代理，把兩邊的真實輸出放上卡片，讓差別是看到的而不是講的。其餘只要改寫：把四欄交辦、三題驗收、三層資訊、四塊交付物併成一張清單，並刪掉十多句「沒有錄製、沒有實測」的製作說明。
- Kind of work: mostly rewriting, plus the one thing the reader names.
- Made by a Codex session. The owner said on 2026-10-11 that the Claude sessions take the rewrite over.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-agent-vs-chatbot/` on main.

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
node tools/video/cli.mjs lint --slug ai-agent-vs-chatbot
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
