---
id: 2026-10-26-verifier-claims-evidence-preservation
title: Preserve primary claims evidence when verifier returns a placeholder summary
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-26T09:29:59Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Preserve primary claims evidence when verifier returns a placeholder summary

## Why

The native verifier accepts any string answer.claims and overwrites claims.md. In ai-pdf-quotes-to-comparison the model returned a statement that earlier evidence was retained, but omitted the actual c1–c31 ledger and original page excerpts. Later fact-checks correctly reported that those excerpts were unavailable in their payload. The real source files and initial git version remain recoverable; a summary must not silently replace primary evidence.

## Definition of done

- [ ] Original evidence survives an incomplete or placeholder verifier response; new findings and genuine corrections remain auditable.
- [ ] A response claiming previous content is preserved cannot erase that content or count as verification of missing material.
- [ ] Regressions cover a complete update, a placeholder-only update, real claim corrections and resume/crash behavior without inventing approval.

## Steps

- [ ] Coordinate with existing active flow.mjs scope holders before claiming; no competing core modification was made by the discovering controller.
- [ ] Define a source-bound claims update contract or conservative preservation policy, preserving the actual returned response separately.

## How to verify

Run focused automation tests and required tools checks. A second verification payload must still contain the original excerpts after a first response omits them, while actual corrections remain distinguishable from historical evidence.

## Notes

- Exact original ledger: a2c088e49e93f1a6c0ccea8730a23da43bde74ee:docs/videos/ai-pdf-quotes-to-comparison/claims.md, 29,857 bytes, SHA256 91e1de197b7f157603dc989dd8ff56a195599469cc71211c6802c9c75bec3e3f.
- a46e8d5e1 contains the observed placeholder, 2,931 bytes/47 lines. Native verify reports1–7 are actual history, not retroactively changed.
- Discovery/recovery branch codex/ai-pdf-comparison-20261026, draft PR1864 no-auto-merge; external root /workspace/work/ai-pdf-01. The controller is restoring real evidence before the next verification, without changing facts or passing a failed quality gate.
