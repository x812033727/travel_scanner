---
id: 2026-10-29-correct-annotation-links-in-vector-database
title: Correct annotation links in Vector Database and Chunking sources
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-29T10:48:31Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-vector-database.json
  - apps/api/app/guides/content/ai-term-chunking.json
---

# Correct annotation links in Vector Database and Chunking sources

## Why

The published-source packs for Vector Database and Chunking link the word
`標記` in a manual data-annotation context to `ai-term-token`. Readers following
the link are taken to the model-token concept rather than data annotation.
Resolve these two source references before creating their translation baseline.

## Definition of done

- [ ] Fresh production source readback confirms the two references and records source versions, canonical hashes and clean draft/publication guards.
- [ ] Independent review confirms the smallest correction: retain the visible wording and change only the two misleading ArticleInline references to ordinary text.
- [ ] Source lint and an exact semantic diff prove that all other content, metadata, aliases, related entries and assets remain unchanged.
- [ ] Any production source correction has its own reviewed plan and owner authorization, followed by native readback and public acceptance; create a new translation baseline only after publication succeeds.

## Steps

- [ ] Check active worktree/branch/PR ownership before claiming this source scope.
- [ ] Compare each current source pack and live source at `/locales/zh-TW/blocks/18/inlines/1`.
- [ ] Prepare the bounded correction, obtain independent source review and follow the content PR/release workflow.

## How to verify

Run the existing native source lint and compare normalized documents before and
after the edit. The two visible paragraphs must be byte-identical after text
projection; only the inline type/link target changes. Compare full source rows,
aliases, related entries and asset hashes after any authorized publication.

## Notes

- Local inspection used target `9dc9dca54b4cc2660fefe635ef76c42d5a82dd8f`.
  Both exact pointers contain
  `{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`.
- Vector Database discusses making a small manually annotated set pairing
  questions with the equipment list that should appear in results. Chunking
  discusses manually marking where an answer occurs in the original text.
- The two packs were excluded from the next translation candidates. No source
  edit, live baseline, correction publication or translation is claimed here.
- Filing checks found no exact-slug match in 72 registered worktrees' open task
  directories or in open GitHub PR text searches for either slug. This does not
  replace a fresh changed-file/scope check before claiming the task.
- This ticket is unclaimed. The broader article-language completion task remains
  open; the current sixteen-translation release has a separate scope.
