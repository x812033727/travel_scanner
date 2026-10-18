---
id: 2026-10-11-rewrite-ai-terms-prompt-to-graph-engineering
title: Tighten the explainer ai-terms-prompt-to-graph-engineering
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
  - docs/videos/ai-terms-prompt-to-graph-engineering
---

# Tighten the explainer ai-terms-prompt-to-graph-engineering

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-terms-prompt-to-graph-engineering`, 「提示詞、上下文、駕馭、迴圈、圖形工程是什麼？AI 出錯，先別急著改指令｜AI 名詞十分鐘」.
- On the site: storyboard approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 3 of the 12 questions asked.
- The reader's reason: 樓層圖和症狀對照表有用，但片名說的「先別急著改指令」從頭到尾沒有一個改指令沒用、換一層才修好的實例，三到五樓的例子又都是頻道自己的製片產線，不寫程式的觀眾拿不到能在自己工具上做的事。
- What it needs, in the reader's words: 補一個真的跑過的前後對照（指令改了幾次都沒用、把缺的資料送進去才對），並把三到五樓約十五句講自家產線的旁白換成觀眾在自己用的代理工具上看得到的情況與該檢查的項目，同時刪掉「一家模型公司給了定義」這類只交代出處的句子。前後對照需要一次新的實跑，其餘只要改寫。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: only questions that nearly every film failed. Also D3, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-terms-prompt-to-graph-engineering/` on main.

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
node tools/video/cli.mjs lint --slug ai-terms-prompt-to-graph-engineering
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
