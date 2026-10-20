---
id: 2026-10-20-curio-s41-qin-book-burning-source
title: Curio S41 Qin book burning source feasibility
status: review
priority: P2
area: docs
owner: codex-s41-qin-feasibility
claimed_at: 2026-10-20T07:16:02Z
created_at: 2026-10-20T07:15:56Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s41
---

# Curio S41 Qin book burning source feasibility

## Why

The familiar phrase 「焚書坑儒」 can make the Qin order sound like an order to burn every book. The surviving Han-era accounts instead enumerate a narrower but still coercive set of books, explicit exceptions, and a separate later prosecution. A new S-series episode needs a pinned source base before a script can make claims about scope, enforcement, survival or loss.

## Definition of done

- [x] A distinct S41 topic with an A/B brief and a one-question answer, without colliding with the existing S01–S40 or H26 Qin mausoleum topic.
- [x] Directly accessible, commit-pinned early texts with raw hashes, source-tier caveats and a claim matrix fit for independent audit.
- [x] No script, site review, voice, music or images before the evidence and story angle have been reviewed.

## Steps

- [x] Check the S-axis topic list and active task scopes for duplication.
- [x] Locate and reopen the relevant Shiji and Hanshu passages at fixed Git commits.
- [x] Draft `docs/videos/curio-s41/brief.md`, `research.md`, and a narrow `claims.md` feasibility matrix.
- [x] Request independent source interpretation and scene-risk review before any full script.

## How to verify

Reopen each raw GitHub URL in `research.md` at its exact commit; compare SHA-256 and cited line numbers. Check all claims against the cited lines, particularly the historian-record clause, `博士官` exception, practical-book exceptions and 460-person passage. Run `npm run check:tasks`. No video lint is meaningful until a `video.json` exists.

## Notes

2026-10-20: The S-axis README lists S01–S36 and excludes the Qin mausoleum H26; no S41/焚書 scope or topic was found. Task and claim are therefore new. Kanripo GitHub raw fixed witnesses: `KR2a0001@1c19dc6f` Shiji annals and biographies, `KR2a0007@683113d4` Hanshu vol. 2 and 30. Both are transmitted historical texts, not a surviving Qin edict or a count of actual books burned. Keep the later 460-person prosecution separate from the book-order question; Shiji uses `諸生` in the annals and `術士` in the Rulin overview, while Fusu says those prosecuted recited Confucius. Do not assert they were all one kind of practitioner.

2026-10-20: Independent auditor reopened four raw files, matched all four SHA-256 digests, checked Q01–Q15 against one-based source lines, and validated all 48 pinned blob-link ranges. Initial precision problems in Q06, Q10, Q15 and the historian-record phrase were corrected and re-reviewed to PASS. Durable receipt: `docs/videos/curio-s41/verify-sources.md`. A future full script needs a separate claimed task, source-bound scene review, and the site's outline/script decisions before any media work.
