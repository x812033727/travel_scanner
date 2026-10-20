---
id: 2026-10-20-plan-the-codex-beginner-guide-video
title: Plan the Codex beginner guide video for non-technical viewers (codex-first-task-no-code)
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-ai-videos
claimed_at: 2026-10-20T16:04:39Z
created_at: 2026-10-20T16:04:15Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/codex-first-task-no-code
---

# Plan the Codex beginner guide video for non-technical viewers (codex-first-task-no-code)

## Why

The owner asked on 2026-10-20 for AI videos that match or beat two reference films, the second being
《Codex 新手教學，非技術人員也能上手的 AI Agent 新手指南》 (Gary Chen). A tutorial under the
content-value rules needs real runs; Codex needs a ChatGPT login that no agent has, so the brief is
written with the runs spelled out for the owner and the script waits for them.

## Definition of done

- [x] `docs/videos/codex-first-task-no-code/brief.md`: audience, outcomes (each tied to a run), the
      simple way (plain ChatGPT chat) and why Codex beats it, 要先實作 R1–R4 with exact files and
      prompts, two outline options, facts to re-check, sources, what the film leaves out.
- [ ] Owner runs R1–R4 (twice each) in the ChatGPT desktop app and fills the 執行紀錄 table.
- [ ] Writer agent produces `video.json` and `claims.md` from the record; fact-check; the rest of the
      pipeline as for any tutorial.

## Steps

- [x] Plan the brief from the site article `codex-beginner-guide` and today's OpenAI pages.
- [ ] Owner: the four runs (see the brief's 要先實作), then release this task to a writer.

## How to verify

The brief's 執行紀錄 table has no 「未實測」 left before anyone writes narration.

## Notes

- Official pages opened 2026-10-20 (all HTTP 200): developers.openai.com/codex/quickstart, /codex/pricing,
  /codex/permissions, /codex/cli, /codex/skills. help.openai.com returned 403 to the editorial UA.
- The brief recommends outline A (the chat-vs-Codex contrast as the chapter-4 turn, the file change in
  the opening); the owner may move the missing-file test to the opening if Codex invents content.
