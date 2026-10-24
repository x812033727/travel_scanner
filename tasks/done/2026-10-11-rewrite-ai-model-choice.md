---
id: 2026-10-11-rewrite-ai-model-choice
title: Rewrite the explainer ai-model-choice with the facts it lacks
status: done
priority: P2
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T14:20:46Z
created_at: 2026-10-11T11:44:30Z
completed_at: 2026-10-24T14:20:46Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - docs/videos/ai-model-choice
---

# Rewrite the explainer ai-model-choice with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-model-choice`, 「AI 模型這麼多，到底該怎麼挑？排行榜第一名不一定適合你」.
- On the site: script passes lint, not uploaded.
- Read as an explainer. Verdict: rework. Failed 7 of the 12 questions asked.
- The reader's reason: 全片真正的內容五行就寫得完，核心數字建立在自訂的三成升級比例和講者自己的延遲推論上，沒有任何一次實測，卻用了一百五十多句、其中大量重複的安撫話來講。
- What it needs, in the reader's words: 需要新的實測，不只是改寫：拿一組真實任務實際跑一次級聯，量出升級比例、p95 延遲和答錯率，並把「自己打分數」怎麼做（評測集、升級門檻）以及所用模型的名稱與單價放上卡片。同時刪掉前七個場景裡重複的心情句與「不是你的工作」的反覆說法，把篇幅留給算式和量到的結果。
- Kind of work: new facts or runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

the branch `origin/claude/video-batch-2`, `docs/videos/ai-model-choice/`; whether that is the cut that was produced was not confirmed.

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
- [ ] Find the missing facts at their sources, or make the missing run, and record where each came from.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-model-choice
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.


### 2026-10-24 owner-directed editorial retirement

站主已選擇「只保留常青實測教學（建議）」；本票屬明列的38張封存清單，取消後續重寫／重製。封存原因：模型挑選與級聯評測屬模型比較/價格題，需另建評測專案才能轉成常青實作；本票仍是概念解說。

本次僅接手任務紀錄並結案；原驗收未勾項保持歷史原貌，不代表已完成重寫。保留所有既有素材、核准、STOP、費用紀錄、YouTube ID及其他獨立製作任務；未呼叫模型、合成、上傳、下架或刪除影片。
