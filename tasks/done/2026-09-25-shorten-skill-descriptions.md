---
id: 2026-09-25-shorten-skill-descriptions
title: Shorten the English half of the shared skill descriptions
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T15:03:40Z
created_at: 2026-09-25T15:03:32Z
completed_at: 2026-09-25T15:04:22Z
branch: claude/skills-token-optimization-dc7d44
depends_on: []
scope:
  - .agents/skills
  - .claude/skills
  - AGENTS.md
---

# Shorten the English half of the shared skill descriptions

## Why

Every skill description is loaded into every Claude Code and Codex session, whether
the skill is used or not. The five shared skills each described themselves twice, a
full Chinese paragraph and then a full English paragraph saying the same thing, which
came to about 5.3 KB of fixed context per session.

## Definition of done

- [x] Each description keeps its full Chinese half (the trigger list) and ends with one
      English sentence, so English-first agents still match the skill.
- [x] `.agents/skills` and `.claude/skills` stay byte-identical.

## Steps

- [x] Shorten catchtable-discovery, content-pipeline, deploy, task-board, youtube-video.
- [x] List the seven new skills (PRs 768, 769, 771, 775–778) in AGENTS.md so agents look for them first.

## How to verify

```bash
node --test tools/skills.test.mjs
```

## Notes

The descriptions went from 687–812 characters to 308–393. The Chinese halves are
untouched because the owner and most prompts write in Chinese and those halves carry
the trigger phrases.
