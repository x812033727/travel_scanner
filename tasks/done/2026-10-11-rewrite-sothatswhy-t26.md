---
id: 2026-10-11-rewrite-sothatswhy-t26
title: Remake or retire sothatswhy-t26: the blind reading called it a drop
status: done
priority: P2
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T14:21:16Z
created_at: 2026-10-11T11:44:30Z
completed_at: 2026-10-24T14:21:16Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - docs/videos/sothatswhy-t26
---

# Remake or retire sothatswhy-t26: the blind reading called it a drop

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `sothatswhy-t26`, 「為什麼日本常端飯碗，韓國卻常放桌上？｜原來如此事務所」.
- On the site: on YouTube, not uploaded.
- Read as an explainer. Verdict: drop. Failed 7 of the 12 questions asked.
- The reader's reason: 片名問「為什麼」，全片卻只描述兩邊怎麼吃、還明說起因要另找歷史證據，180 句旁白裡能帶走的事實五行就寫完，其餘多是想像畫面與「先看一下、再問人」這類通用叮嚀，等於要從企劃重做。
- Kind of work: remake from the plan, or retire.

What it failed: the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/sothatswhy-t26/` on main.

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
node tools/video/cli.mjs lint --slug sothatswhy-t26
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.


### 2026-10-24 owner-directed editorial retirement

站主已選擇「只保留常青實測教學（建議）」；本票屬明列的38張封存清單，取消後續重寫／重製。封存原因：日韓飯碗禮儀的通識題，原盲讀判drop；不因封存此票改動已製作影片或歷史。

本次僅接手任務紀錄並結案；原驗收未勾項保持歷史原貌，不代表已完成重寫。保留所有既有素材、核准、STOP、費用紀錄、YouTube ID及其他獨立製作任務；未呼叫模型、合成、上傳、下架或刪除影片。
