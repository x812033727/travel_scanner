---
id: 2026-10-11-rewrite-cloudflare-ai-attacks-own-waf-49-findings
title: Tighten the explainer cloudflare-ai-attacks-own-waf-49-findings
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
  - docs/videos/cloudflare-ai-attacks-own-waf-49-findings
---

# Tighten the explainer cloudflare-ai-attacks-own-waf-49-findings

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `cloudflare-ai-attacks-own-waf-49-findings`, 「Cloudflare 叫 AI 當駭客打自家防火牆：1,107 次嘗試、49 筆發現，這兩個數字該怎麼讀？」.
- On the site: on YouTube, YouTube id `UWYoO3JfOK0` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked. A second reader: publish, 3 failed.
- The reader's reason: 數字拆解（607＝558＋49、95.6% 不是官方數字）確實有料，但 104 句旁白裡約四成是店鋪警衛之類的比喻和「記得更新」的通用勸告，五行講得完的內容被稀釋了。
- What it needs, in the reader's words: 把二十多句比喻砍到兩三句，補上片中只提到卻沒交代的內容（五個審查問題、六類攻擊各是什麼、Cloudflare 客戶要檢查的設定名稱與位置），清點表至少給一個常見系統的實際選單路徑。以重寫為主，只需補來源頁面與官方文件已有的少量事實，不需要新的實測。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/cloudflare-ai-attacks-own-waf-49-findings/video.json` in the video-worker container. Copy it into `docs/videos/cloudflare-ai-attacks-own-waf-49-findings/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug cloudflare-ai-attacks-own-waf-49-findings
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
