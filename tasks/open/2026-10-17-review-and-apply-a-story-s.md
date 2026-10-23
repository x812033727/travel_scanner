---
id: 2026-10-17-review-and-apply-a-story-s
title: Review and apply a story's pronunciation proposals (story-lexicon-revise CLI)
status: in-progress
priority: P1
area: tools
owner: claude-opus-5.5-lexicon-revise
claimed_at: 2026-10-17T13:34:29Z
created_at: 2026-10-17T13:34:04Z
completed_at:
branch: claude/story-lexicon-revise-cli
depends_on: []
scope:
  - tools/video/core/lexicon-revision.mjs
  - tools/video/core/lexicon-revision.test.mjs
  - tools/video/cli.mjs
  - docs/videos/story-lexicon-revision.md
---

# Review and apply a story's pronunciation proposals (story-lexicon-revise CLI)

## Why

#1548 pins each story's pronunciation dictionary. When a story writer later uses a Latin word the
pinned dictionary lacks, `proposeStoryLexicon` saves an immutable proposal under
`<workdir>/story/lexicon-proposals/` and the story blocks ("pronunciation proposals saved for
reviewed revision"). Publishing the next version needs `reviseStoryLexicon` with a review
SHA-256, and nothing in the repository produced one, so every such story stayed blocked for good.
Production's `story-adapt-michelin-guide-stars` is blocked on `{"Paul": null, "Bocuse": "博古斯"}`.

## Definition of done

- [x] An operator can list a story's proposals (current, stale, applied, invalid) and get a review
      receipt template without writing anything.
- [x] A filled receipt (slug, current lexicon SHA-256, proposal SHA-256s, a decision per term,
      an independent reviewer, reviewed_at, independent: true) is checked; `--apply` publishes the
      pinned dictionary plus the accepted terms through `reviseStoryLexicon`, bound to the SHA-256 of
      the receipt's exact bytes, and keeps those bytes immutably in the work directory.
- [x] Every refusal (wrong work directory, stale proposal or receipt, bad reviewer, ...) happens
      before any lease or write; reapplying the same receipt is a no-op.

## Steps

- [x] `tools/video/core/lexicon-revision.mjs` (inspect, evaluate, apply).
- [x] `node tools/video/cli.mjs story-lexicon-revise`.
- [x] Tests in `tools/video/core/lexicon-revision.test.mjs`.
- [x] `docs/videos/story-lexicon-revision.md` (host steps, retry on /admin/videos).
- [ ] On the host (not part of this PR): review and apply `story-adapt-michelin-guide-stars`, then
      retry it on /admin/videos.

## How to verify

```bash
node --test tools/video/core/lexicon-revision.test.mjs tools/video/core/lexicon-store.test.mjs tools/video/core/lexicon-migration.test.mjs tools/video/cli.test.mjs
npm run check:tasks
```

## Notes

- Claimed with `--force`: `tools/video/cli.mjs` is also in the scope of
  `2026-10-17-migrate-a-story-started-before-lexicon`, whose PR #1550 is merged and whose branch is
  gone; the change here only adds one subcommand next to `story-lexicon-migrate`.
- `lexicon-store.mjs`, `story-lexicon.mjs` and `story-lexicon-integration.md` belong to
  `2026-10-16-bind-story-audits-and-narration-to` and are only imported, not changed. The work
  directory proof is `workdirProof` from `lexicon-migration.mjs` (#1550).
- Race safety: the apply takes the project lease and the dictionary-writer lease itself, re-checks
  everything, then calls `reviseStoryLexicon`, which joins both (leases are reentrant within a
  process). Without that, a second revision between the check and the publish would have been
  overwritten, since `planStoryLexiconRevision` accepts any previous version.
- A rejected term keeps the story blocked (`advanceStory` waits for every `lexicon_pending` term);
  follow-up `2026-10-17-story-worker-a-rejected-pronunciation-proposal`.
