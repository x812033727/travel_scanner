---
id: 2026-10-11-rewrite-ai-agent-permissions
title: Tighten the explainer ai-agent-permissions
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
  - docs/videos/ai-agent-permissions
---

# Tighten the explainer ai-agent-permissions

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-agent-permissions`, 「AI 代理人被擋下後，自己找路進去？三起越界事件，和你該先設好的三道權限」.
- On the site: on YouTube, YouTube id `itKTQl3ehQE` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 5 of the 12 questions asked.
- The reader's reason: 三起事件講得有來源、有數字，但標題答應的「三道權限怎麼設」只給了一段沒說是哪個工具哪個檔案的 JSON，Sandbox 和金鑰都沒有可照做的步驟，卻反覆叫觀眾「自己測一次」。
- What it needs, in the reader's words: 權限那一半要補上實際內容：allow／deny 寫在哪個工具的哪個設定檔、怎麼測到它真的被擋（附一次真實執行的輸出）、Sandbox 怎麼開怎麼驗、金鑰用觀眾自己做得到的方式隔開，而不是講頻道自己的配對流程。這需要新的實測，不只是改寫；另外把重複四次的「不要不是界線」和十多句交代來源的旁白刪減。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

the branch `origin/claude/video-batch-2`, `docs/videos/ai-agent-permissions/`; whether that is the cut that was produced was not confirmed.

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
node tools/video/cli.mjs lint --slug ai-agent-permissions
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
