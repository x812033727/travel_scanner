---
id: 2026-11-09-localize-four-retrieval-graph-concepts
title: Localize four retrieval graph concepts
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-graph16-localization
claimed_at: 2026-11-09T08:34:08Z
created_at: 2026-11-09T08:34:05Z
completed_at:
branch: codex/localize-retrieval-graphs-20261109
depends_on:
  - 2026-10-30-release-corrected-retrieval-concept-sources
scope:
  - apps/api/app/guides/content/ai-term-hybrid-search.json
  - apps/api/app/guides/content/ai-term-knowledge-graph.json
  - apps/api/app/guides/content/ai-term-graph-rag.json
  - apps/api/app/guides/content/ai-term-agentic-rag.json
  - apps/web/public/guides/ai-term-hybrid-search
  - apps/web/public/guides/ai-term-knowledge-graph
  - apps/web/public/guides/ai-term-graph-rag
  - apps/web/public/guides/ai-term-agentic-rag
---

# Localize four retrieval graph concepts

## Why

Hybrid search, knowledge graph, GraphRAG and Agentic RAG are public in zh-TW but
still lack en, ja, ko and zh-CN. The prerequisite source corrections are now
published and recorded in merged PR #2052. The owner resumed language completion;
this ticket prepares the sixteen translations against the accepted new sources.

## Definition of done

- [ ] All sixteen target documents and their translated image text are complete.
- [ ] Original zh-TW documents and original assets are unchanged.
- [ ] Independent text, visual, glyph and link reviews bind the exact final artifacts.
- [ ] Native assembly/install/replay and scoped content checks pass.
- [ ] A content PR passes CI; separate publication work remains explicitly gated.

## Steps

- [x] Check task/worktree/remote/PR ownership and claim this narrow scope.
- [x] Verify fresh published sources against the accepted four-source baseline.
- [ ] Prepare and translate sixteen native jobs with no automatic retry.
- [ ] Render localized assets, apply independent findings and seal final reviews.
- [ ] Assemble and install only this cohort; verify original-source preservation.
- [ ] Run scoped checks, finish this content task in the PR and obtain merge approval.

## How to verify

Use the unchanged localization pipeline's prepare, run, materialize and status
commands, followed by render.mjs and independent hash-bound review.json files.
Assemble/install the exact reviewed bundle and verify a no-change replay. Run
scoped pack lint, content-pack tests, translation checks, localization tooling
tests, check:tasks and git diff --check. Require green exact-head CI before merge.

## Notes

Accepted source baseline SHA-256:
`872688a9d52fde51b48e122045d62b80969231277f820a179e9b2589e962703a`.
It was captured after the November 9 source release and independently reviewed
(`831d6494`); source versions are hybrid 12, knowledge 10, GraphRAG 8 and Agentic 10.
All sixteen target rows were absent and repository/source differences were zero.
Fresh authoring readback and source readiness remain separate checks.

No active task claimed these four packs during the new scope survey. PR #1857
appears in the historical diff because its base is a different video branch;
all sixteen relevant source/asset Git blobs at its exact head `3e0f7218` equal
current main `b50394c2`. It has no competing source or translation edits here.
The new worktree starts at that main commit; older worktrees remain untouched.

Use Route A, native ChatGPT-login pipeline, at most three workers, retries zero.
Private baseline, raw responses, jobs, renders and reviews stay outside Git.
Fresh independent source review `6fbc92ca` passed: current public documents and
versions match the baseline, eight public assets match, eleven source-language
internal links are published, and first-party sources and all original images
were actually inspected. Independent native-input review `bdef7d39` passed all
70 checks for sixteen prepared jobs and source/tool/ownership pins.

This ticket does not authorize production writes, deployment, migration or merge.
Whole-site language completion remains open; this is only the next four articles.
