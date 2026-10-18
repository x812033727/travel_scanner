---
id: 2026-10-11-rewrite-cloudflare-workers-per-worker-permissions-ai-agent
title: Tighten the explainer cloudflare-workers-per-worker-permissions-ai-agent
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
  - docs/videos/cloudflare-workers-per-worker-permissions-ai-agent
---

# Tighten the explainer cloudflare-workers-per-worker-permissions-ai-agent

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `cloudflare-workers-per-worker-permissions-ai-agent`, 「給 AI 代理的金鑰該開多大？Cloudflare Workers 單一 Worker 權限與四種角色」.
- On the site: on YouTube, YouTube id `8N52Ul9CYfc` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked.
- The reader's reason: 全片是把 Cloudflare 公告的四種角色換句話說，再配上示意的 5−1=4 和二十幾句鑰匙、門、租船的比喻，沒有任何一步告訴觀眾在控制台怎麼設，也沒有實際驗證權限真的擋得住，看完知道有這功能卻做不出來。
- What it needs, in the reader's words: 需要新的實測而不只是改寫：在控制台實際建立一張只限單一 Worker 的 API token（卡片上寫出選單位置與欄位），並放上用它去動另一個 Worker、刪除 Worker、改路由時被拒絕的實際輸出。再把二十多句比喻和重複的「示意」「以官網為準」刪掉，篇幅留給四種角色各自擋得住什麼。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: only questions that nearly every film failed. Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/cloudflare-workers-per-worker-permissions-ai-agent/video.json` in the video-worker container. Copy it into `docs/videos/cloudflare-workers-per-worker-permissions-ai-agent/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug cloudflare-workers-per-worker-permissions-ai-agent
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
