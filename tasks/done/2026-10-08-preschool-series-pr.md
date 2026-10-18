---
id: 2026-10-08-preschool-series-pr
title: Validate and open preschool series pull request
status: done
priority: P2
area: tools
owner: codex-preschool-pr
claimed_at: 2026-10-08T00:22:10Z
created_at: 2026-10-08T00:22:09Z
completed_at: 2026-10-08T00:32:14Z
branch: codex/preschool-english-series-20261008
depends_on: []
scope:
  - tools/video/preschool
  - docs/videos/english-preschool-pilot
  - docs/videos/english-preschool-series
---

# Validate and open preschool series pull request

## Why

Deliver the completed preschool course as reviewable source and reusable local production tooling, while keeping large media outside the public repository. Review found that resumable sidecars and mux-only pictures needed stronger source and file integrity checks before reusing this pipeline for elementary lessons.

## Definition of done

- [x] The 48-episode curriculum and original five pilots are represented in source with English picture text, five audio tracks and four non-English CC tracks.
- [x] Sidecar tampering and stale-picture muxing are rejected; existing 48 deliveries remain verifiable without rewriting them.
- [x] Relevant repository and media checks pass; source and the draft PR description are ready for review without enabling automatic merge.

## Steps

- [x] Check local branches/worktrees, remote heads, open PRs and task ownership; branch from current origin/main.
- [x] Independently review production code and retained media provenance.
- [x] Fix integrity findings and run regression checks.
- [x] Repeat collision checks and prepare the source-only commit and draft PR handoff.

## How to verify

- `npm run test:tools` and `npm run check:tasks`.
- `PYTHONPATH=/tmp/preschool-simd:/tmp/preschool-tts python3 tools/video/preschool/verify_series.py --source docs/videos/english-preschool-series/lessons.json --output /workspace/preschool-series-output --report /tmp/preschool-pr-series-checks.json`.
- New integrity regression checks under `tools/video/preschool/` cover tampered audio/subtitles and same-duration stale picture sources.
- Inspect staged files for media and credentials before committing; inspect the returned PR URL and draft state after creating it.

## Notes

- The existing 48 media episodes and five verified offline ZIPs remain outside Git at `/workspace/preschool-series-output`. Original pilot media are retained unchanged.
- Initial `npm run test:tools`: exit 0, 2,006 passed / 3 skipped. Final targeted integrity results are recorded below after completion.
- Voice tracks use Microsoft Edge read-aloud trial voices, not configured production backend voices. Full media decode and jsdom player checks passed; no claim of human pronunciation review or real-browser playback validation.
- User explicitly requested opening a PR then continuing with the elementary English series. The next course is the first lower-elementary season; backend integration remains a separate open task.
- Repository workflow auto-merges eligible non-draft PRs. This PR will be a draft because merging was not requested.

Final integrity validation: 10/10 dependency-free regressions passed; independent follow-up review found no remaining P1/P2. Read-only series verification and packaging preflight both passed 48/48 with zero errors, including mixed new/legacy receipt checks. Report: `/tmp/preschool-integrity-verification.json`. No delivered media, metadata or ZIP was rewritten.

Final full `npm run test:tools`: exit 0, 2,007 passed / 3 skipped (2,010 total), including the wrapper running 10 Python integrity regressions. `npm run check:tasks`: passed with only five unrelated stale-claim warnings.
