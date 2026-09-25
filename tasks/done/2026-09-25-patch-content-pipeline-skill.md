---
id: 2026-09-25-patch-content-pipeline-skill
title: Fill the content-pipeline skill with what only memory knew
status: done
priority: P2
area: tools
owner: claude-opus-5-5-patch-content-pipeline-skill
claimed_at: 2026-09-25T15:18:00Z
created_at: 2026-09-25T15:12:46Z
completed_at: 2026-09-25T15:21:27Z
branch: claude/patch-content-pipeline-skill
depends_on: []
scope:
  - .agents/skills/content-pipeline
  - .claude/skills/content-pipeline
---

# Fill the content-pipeline skill with what only memory knew

## Why

A coverage audit of Claude's private memory files against the shared repo skills found
lessons from the 2026-09 content batches (news batch 4, Korea food specials, the
reader-first rewrite, AI news batches) that only Claude's memory knew, so Codex and any
fresh session repeated them. It also found two stale statements in the skill: the
`SITEMAP_LIMIT` 1,000-row cap (gone since #531 made `/sitemap.xml` an index) and a
word-count target for food specials that the rewrite ruling scrapped.

## Definition of done

- [x] The content-pipeline references carry the missing lessons, each verified against main.
- [x] The two stale statements are corrected.
- [x] `.claude/skills/content-pipeline/SKILL.md` is a byte-identical copy (only SKILL.md is mirrored) and `node --test tools/skills.test.mjs` passes.

## Steps

- [x] `references/pitfalls.md`: intake errors, stock phrases, two root causes of "can't understand", diagram checks, pointer to `content-blocks.tsx` for diagram width, local tooling notes, PR branch in another worktree, background in-app browser, usage control, seed file vs production, seeder adoption, Naver search links, final publish click, sitemap fix.
- [x] `references/publish-runbook.md`: cmp the re-run dry-run, diff `document` through `GuideDocument`, pg_dump + scoped publish in one plink script, `unavailableTitle` trap, series API path, sitemap fix.
- [x] `references/travel-batch.md`: food specials have no word-count target, new subtopics need migration + taxonomy constant, affiliate panel by topic, `?category=` takes a category slug, visitseoul Chinese site.
- [x] `references/news-batch.md`: explicit slugs for prefix scripts, COUNT rule, wrong slug dates, NCC SPA, review grouping.
- [x] `SKILL.md`: one-line pointer to the usage numbers.

## How to verify

```bash
cmp .agents/skills/content-pipeline/SKILL.md .claude/skills/content-pipeline/SKILL.md
node --test tools/skills.test.mjs
```

## Notes

- Skipped on purpose: item 49 (read-only agents creating a git-ignored `.venv`, harmless) and item 57 (English length warning, known and accepted).
- Item 54 (diagram display width) is web code; the skill only points at the comment in `apps/web/components/content-blocks.tsx`, which already explains the 728/335/226 px numbers.
- The `description:` lines were not touched (PR #767 rewrites them).
