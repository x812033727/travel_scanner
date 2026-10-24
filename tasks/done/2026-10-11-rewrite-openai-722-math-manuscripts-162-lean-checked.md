---
id: 2026-10-11-rewrite-openai-722-math-manuscripts-162-lean-checked
title: Tighten the explainer openai-722-math-manuscripts-162-lean-checked
status: done
priority: P3
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T14:21:08Z
created_at: 2026-10-11T11:44:30Z
completed_at: 2026-10-24T14:21:08Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - docs/videos/openai-722-math-manuscripts-162-lean-checked
---

# Tighten the explainer openai-722-math-manuscripts-162-lean-checked

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `openai-722-math-manuscripts-162-lean-checked`, 「OpenAI 公開 722 篇 AI 數學手稿，機器檢查過的只有 162 篇：「AI 解開數學題」的新聞怎麼讀」.
- On the site: languages, not uploaded.
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked.
- The reader's reason: 內容有料（只有 22% 有檢查紀錄、Lean 不管陳述是否等於原題、提示零公開所以無法重做），但 125 句旁白裡約四成是五套比喻、出處口白和最後一章的泛用提醒，把這些事實稀釋掉了。
- What it needs, in the reader's words: 刪掉果菜市場、驗車、碼頭、茶行、夜市五套比喻，並把最後一章「套回自己用 AI」的泛用建議縮成三問一張卡，篇幅留給 Lean 檢查範圍、4,000 題挑選與無法重現這三件事。只需要改寫，不需要新事實；若能補一篇手稿的實例說明「陳述與原題對不上」會更好，那才需要新資料。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/openai-722-math-manuscripts-162-lean-checked/video.json` in the video-worker container. Copy it into `docs/videos/openai-722-math-manuscripts-162-lean-checked/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug openai-722-math-manuscripts-162-lean-checked
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.


### 2026-10-24 owner-directed editorial retirement

站主已選擇「只保留常青實測教學（建議）」；本票屬明列的38張封存清單，取消後續重寫／重製。封存原因：特定數學手稿發布與Lean驗證範圍的新聞解讀，相關已刊文章更正與其他影片交付票保持獨立。

本次僅接手任務紀錄並結案；原驗收未勾項保持歷史原貌，不代表已完成重寫。保留所有既有素材、核准、STOP、費用紀錄、YouTube ID及其他獨立製作任務；未呼叫模型、合成、上傳、下架或刪除影片。
