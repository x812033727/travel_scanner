---
id: 2026-10-11-rewrite-icann-ai-tld-agent-preorder-check
title: Tighten the explainer icann-ai-tld-agent-preorder-check
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
  - docs/videos/icann-ai-tld-agent-preorder-check
---

# Tighten the explainer icann-ai-tld-agent-preorder-check

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `icann-ai-tld-agent-preorder-check`, 「AI 公司搶申請 .agent 網址，你現在買得到嗎？ICANN 收到 1,615 份申請，結果最早明年」.
- On the site: retrying, not uploaded.
- Read as an explainer. Verdict: rework. Failed 3 of the 12 questions asked.
- The reader's reason: 答案和查證動作都有，但 108 句旁白裡約 38 句是郵局、菜市場、港口、超商的比喻，真正的新資訊五行就寫完，而且觀眾最想知道的「十家搶一個怎麼決定、預購到底賣什麼、何時才能註冊」都沒講。
- What it needs, in the reader's words: 刪掉大半比喻句，補上十家搶同一個後綴怎麼決定、所謂預購賣的是什麼與錢退不退、核准後一般人何時能註冊，並把在 ICANN 頁面查 .agent 的實際結果秀在畫面上。這需要補查新事實和一次實際查詢畫面，不是只改寫就夠。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: only questions that nearly every film failed. Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/icann-ai-tld-agent-preorder-check/video.json` in the video-worker container. Copy it into `docs/videos/icann-ai-tld-agent-preorder-check/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug icann-ai-tld-agent-preorder-check
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
