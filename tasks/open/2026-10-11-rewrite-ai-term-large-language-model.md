---
id: 2026-10-11-rewrite-ai-term-large-language-model
title: Rewrite the explainer ai-term-large-language-model with the facts it lacks
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
  - docs/videos/ai-term-large-language-model
---

# Rewrite the explainer ai-term-large-language-model with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-term-large-language-model`, 「大型語言模型是什麼？會接話，為什麼不等於查到資料？｜AI 名詞十分鐘」.
- On the site: on YouTube, YouTube id `vxv8KrNual8` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked.
- The reader's reason: 全片沒有任何一次真實模型輸出，核心示範只是用 Python 數六筆虛構資料得到 6、4、2，錯誤回答全是編輯自己寫的，觀眾看不到任何事前料不到的結果。
- What it needs, in the reader's words: 把離線 Python 示範換成真實模型的實測：同一份清單問缺的欄位，對照有沒有加「無法確認請寫未知」的前後輸出（附產品、版本、日期），再用真實 tokenizer 數一句中文的 token。同時刪掉大部分比喻、免責聲明和泛用的核對叮囑；這需要新的實測，不是只改寫。
- Kind of work: new facts or runs, then a rewrite.

What it failed: a concrete problem or result in the first three scenes (W1); an observed result or sourced fact the viewer would not have predicted (W5); more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-term-large-language-model/` on main.

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
node tools/video/cli.mjs lint --slug ai-term-large-language-model
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
