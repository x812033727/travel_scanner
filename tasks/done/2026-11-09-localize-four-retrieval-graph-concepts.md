---
id: 2026-11-09-localize-four-retrieval-graph-concepts
title: Localize four retrieval graph concepts
status: done
priority: P2
area: docs
owner: codex-gpt6-graph16-localization
claimed_at: 2026-11-09T08:34:08Z
created_at: 2026-11-09T08:34:05Z
completed_at: 2026-11-09T09:18:07Z
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

- [x] All sixteen target documents and their translated image text are complete.
- [x] Original zh-TW documents and original assets are unchanged.
- [x] Independent text, visual, glyph and link reviews bind the exact final artifacts.
- [x] Native assembly/install/replay and scoped content checks pass.
- [ ] A content PR passes CI; separate publication work remains explicitly gated.

## Steps

- [x] Check task/worktree/remote/PR ownership and claim this narrow scope.
- [x] Verify fresh published sources against the accepted four-source baseline.
- [x] Prepare and translate sixteen native jobs with no automatic retry.
- [x] Render localized assets, apply independent findings and seal final reviews.
- [x] Assemble and install only this cohort; verify original-source preservation.
- [x] Run scoped checks and prepare the content/task handoff in the PR.
- [ ] Obtain exact-head green CI and owner merge approval before merging.

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

## Completed local authoring

The native ChatGPT-login run completed all sixteen jobs with three workers and
zero retries. Independent reviewers accepted all sixteen final documents and
actual rendered images, with zero unresolved findings. Five localized corrections
were applied by the coordinator and independently re-reviewed: two Agentic RAG
diagram labels were shortened to avoid arrow overlap; two Japanese first-term
definitions were made grammatical; the Korean knowledge-graph example now refers
to natural-language phrases consistently with its localized example. Original
attempts, failed renders and pre-correction artifacts remain preserved privately.

The final native bundle contains four packs and forty-eight new localized assets.
Manifest SHA-256:
`d75508487a32e3faebc1faa78d2eb5e6991f5c62e0fd8bf7f0880195e8d3beae`.
Independent bundle review passed 197 checks with zero findings; review SHA-256:
`8194baf57508e2e20f0b5de896bdb0ca5551151e451ec907cf604571a3bf42e1`.
Independent local-install preparation review SHA-256:
`248978fd13cda0b6e0dd8132f30dbbef533a8caebee5e801d500977a61e3491f`.

The unchanged native installer exited 0 and wrote exactly fifty-two destinations:
four packs and forty-eight new images. All sixteen native admission checks passed.
The journal, four original-pack backups and four article receipts are retained.
Actual installation verification receipt SHA-256:
`965e70a9ae3b06f3ca879b87b2eaf232ffe6a6cd9f9bd85e0c962ffa57c5d8ed`.
An actual second native install exited 0 and left every content byte/mtime,
the twelve original assets, journal, receipts, mirror and authority unchanged.
Replay receipt SHA-256:
`b68c8a8b004a7255dae1b5599265985cead7c41b8735c580da932f9a1336e92a`.

Local checks passed: 35 pipeline tests, 25 artifact/layout tests, 68 bundle/
installation tests and 9 content-pack tests (137 passed total). Five PostgreSQL
content-pack cases were skipped locally; no local PostgreSQL coverage is claimed.
CI must verify the configured integration/release-safety cases before merge.
Scoped lint passed all four packs with only English body-length advisories:
Agentic RAG 7,345; GraphRAG 7,693; hybrid search 7,238; knowledge graph 7,387
characters. Full reviewed translations were retained. Translation character checks
reported zero hits. Two initial check-wrapper launches could not resolve the
relative Windows executable; the checks did not start. Fresh runs using the
absolute executable completed successfully; initial output files were retained.

Unchanged normalized zh-TW identities:

| Article | Source SHA-256 |
| --- | --- |
| ai-term-agentic-rag | `bb7772cb28692526d8ed07068bbde4f58b47f8fa59efbb19a0257d491cea0895` |
| ai-term-graph-rag | `1c0dea04721fd72d34051a5c46abc7db2c58e05757465ce81abf9c49636bafca` |
| ai-term-hybrid-search | `972610411149ea1010e2e8b0a23d4086181e0cb18de0dc222ae771e43dba46c5` |
| ai-term-knowledge-graph | `64f41fb947553be82d8eb0e8641265d8ed721ce5965875ffb09dd3df12f3f7be` |

Native serialization makes schema defaults explicit and normalizes pack metadata;
raw pack JSON formatting is not claimed unchanged. Original normalized documents,
effective metadata, links, source dates and twelve original image bytes are preserved.

The content task is closed in its PR per task-board protocol. The remaining
unchecked items are exact-head CI and owner merge gates, not publication claims;
the PR must carry `no-auto-merge` until separately approved. Publication remains in
the open, unclaimed dependent ticket
`2026-11-09-release-localized-retrieval-graph-concepts`. No production action or
new merge approval occurred in this authoring wave. The last global census remains
764 incomplete articles and 3,056 missing public locale documents; these sixteen
local translations have not been subtracted.

Final independent actual-install and task-handoff review passed with zero findings.
Receipt SHA-256:
`fa90a9de9feb85e28e3b0a5611baa4bc258a4b9c177b8a8c76fd6307a5f0bb0e`.
