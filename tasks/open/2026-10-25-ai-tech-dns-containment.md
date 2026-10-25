---
id: 2026-10-25-ai-tech-dns-containment
title: Produce AI tech news video on OpenAI DNS containment and retain overseas reference workflow
status: in-progress
priority: P2
area: docs
owner: codex-ai-tech-news
claimed_at: 2026-10-25T09:45:59Z
created_at: 2026-10-25T09:45:54Z
completed_at:
branch: codex/ai-tech-dns-20261025
depends_on: []
scope:
  - docs/videos/openai-dns-containment
  - .agents/skills/ai-tech-news-video
  - .claude/skills/ai-tech-news-video
---

# Produce AI tech news video on OpenAI DNS containment and retain overseas reference workflow

## Why

The owner requested a new AI/technology news video and authorized learning from
recent popular overseas YouTube videos. Retain a reusable research skill and a
source-checked, original zh-TW production draft, then use the established channel
workflow for narration, review, rendering and upload packaging.

## Definition of done

- [x] Recent overseas references have dated, attributed view snapshots and honest observation limits.
- [x] A new mirrored AI/tech-news research skill adds useful evidence and production rules without changing running host prompts.
- [x] A full 8+ minute draft, claims, worked timeline calculation and independent fact/narrative reviews are saved.
- [ ] Channel narration, media and upload package are complete after the required pairing and review gates.

## Steps

- [x] Inspect existing channel rules, other branches and current official news.
- [x] Draft the recommended event story and alternative outlines; preserve the submitted brief hash.
- [x] Independently review the facts, narration and actual visual samples; record residual editorial findings honestly.
- [x] Pair this task's tool with the channel and record delegated outline approval.
- [ ] Complete formal narration, audio check, assembly, CC, final QA and upload package.

## How to verify

```bash
node tools/video/cli.mjs lint --slug openai-dns-containment --json
node tools/video/cli.mjs narrative --slug openai-dns-containment --workdir /workspace/work/videos
node --test tools/skills.test.mjs
npm run check:tasks
node tools/video/cli.mjs status --slug openai-dns-containment --workdir /workspace/work/videos
```

## Notes

- Started from origin/main c29462d34 on branch codex/ai-tech-dns-20261025; checked local worktrees, remote branches and open PRs. Other current AI-news work covers shopping agents, Claude Duet and Google ads, not this event.
- The news hook is OpenAI's 2026-10-23 infrastructure disclosure. The DNS event occurred 2026-09-20; the specific incident report was updated 2026-09-25. Do not call it a new public ChatGPT escape.
- Initial environment had no tool pairing or SSH configuration. The owner completed device pairing during this task; private credentials remain in the external work directory and are never committed or printed.
- Owner subsequently instructed: 「之後依據你的推薦或jev選擇就好 不用問我」. This supersedes the old per-gate question requirement for this work. Retained in the new mirrored skill. No auto.json is manufactured.
- The topic/brief was submitted to /admin/videos. Jev selected C but its demonstration score 0.42 failed the 0.6 threshold; coordinator chose recommended A under the owner's delegation and recorded the actual rationale with the native approve command. The backend outline card remains pending; do not claim an admin UI click happened.
- Independent fact/reuse review verify-2 ends in PASS. Final blind panel has two residual editorial findings, preserved in narrative-review.md and accepted by the coordinator under the owner's explicit delegation; no fake all-pass receipt.
- Gemini Sulafat is ready; dry-run confirmed sufficient monthly allowance. Formal TTS has started. Native render produced the full contact sheet; six word-break corrections were rendered without changing narration.
- Working media and private pairing state belong under /workspace/work. The client-designated /codex/browser/projectless/0004-ai-yt-skill/output is absent and its parent cannot be created by this executor (permission denied). Use the review PR for user-facing text until a deliverable surface is available; do not mislabel scratch files as outputs.
