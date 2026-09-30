---
id: 2026-09-30-zh-cn-uses-the-taiwan-word
title: zh-CN uses the Taiwan word 备援 in nine published articles; replace it by context
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T13:00:15Z
created_at: 2026-09-30T12:23:51Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-claude-fable-5-access-20260609.json
  - apps/api/app/guides/content/ai-news-claude-opus-55-20260922.json
  - apps/api/app/guides/content/ai-news-gpt-6-sol-luna-20260923.json
  - apps/api/app/guides/content/ai-news-nvidia-rubin-20260105.json
  - apps/api/app/guides/content/codex-agents-md-scopes.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/tech-news-taiwan-6g-spectrum-20260910.json
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-20260623.json
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-tm4-20260918.json
---

# zh-CN uses the Taiwan word 备援 in nine published articles; replace it by context

## Why

The zh-CN reviewer of batch 4.10 (2026-09-30) flagged 「备援」 as Taiwan usage; mainland readers
write 回退／回退机制 (a model or system falling back), 冗余 or 备份 (redundant cables and links)
depending on the sense. It appears 44 times in the zh-CN locale of nine published packs.

## Definition of done

- [ ] Each occurrence replaced by the word its context needs (fallback → 回退机制; redundancy →
      冗余; backup → 备份), zh-CN only, zh-TW untouched.
- [ ] `pack_cli lint` clean and the changed packs re-imported with `guides-import --slug`.

## Notes

- Not a find-and-replace: the Matsu cable articles mean redundancy, the model articles mean
  fallback.
