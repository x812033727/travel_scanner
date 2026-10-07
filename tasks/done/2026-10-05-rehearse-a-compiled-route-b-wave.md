---
id: 2026-10-05-rehearse-a-compiled-route-b-wave
title: Rehearse a compiled Route B wave on the deployed API image
status: done
priority: P2
area: ops
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T04:56:18Z
created_at: 2026-10-05T09:54:38Z
completed_at: 2026-10-07T06:11:01Z
branch: codex/article-missing-locales-20261007
depends_on:
  - 2026-09-29-route-b-reviewed-bundle-compiler
scope:
  - docs/article-localization/releases/route-b-rehearsal
---

# Rehearse a compiled Route B wave on the deployed API image

## Why

`docs/article-localization/prepare_route_b_bundle.py` compiles a reviewed Route B wave
into a bundle for `publish_bundle.py`. Its tests use synthetic inputs, SQLite locally and
the PostgreSQL service in the `release-safety` CI job, which runs the repository's Python
environment, not the API image that would publish. The release plan
(`docs/work-status-2026-09-29-article-release-plan.md`, step 2) requires a same-image,
isolated PostgreSQL rehearsal for each route before any production write: success,
editor conflict, hide/expiry, interrupted resume with the same state directory, and
rollback. No ticket held that gate for Route B.

## Definition of done

- [x] One real reviewed wave (T1 is the first candidate) is frozen into the compiler's
      `route-b-candidate-v1` and `route-b-review-v1` inputs from exact Git blobs and the
      original review evidence, with no invented review receipt.
- [x] Inside the selected API image, against an isolated PostgreSQL restored from a
      synthetic or approved snapshot, the compiled bundle passes dry-run, drafts,
      publish-articles and publish-hubs, and a rerun writes nothing.
- [x] The conflict, hide/expiry, held-slug and interrupted-resume cases stop or resume
      exactly as the publisher documents, with no write outside the selected locales.
- [x] A sanitized record (hashes, counts, image digest, results; no machine paths,
      database or actor ids) is committed under the scope directory.

## Steps

- [x] Select the deployed API image and a synthetic isolated snapshot within the authorized rehearsal scope.
- [x] Freeze the wave's candidate and review inputs outside the repository and pin them.
- [x] Build the baseline from that snapshot, compile, and record the manifest SHA-256.
- [x] Run the publisher phases and the failure cases in the image; keep raw evidence
      outside the repository.
- [x] Write the sanitized record.
- [ ] Merge the reviewed record and close the ticket.

## How to verify

The record lists the image digest, input pins, manifest SHA-256 and each case's
publisher result, and a second person can recompile the same inputs to the same
manifest SHA-256 (`route-b-bundle.md` §Output says the output is deterministic).

## Notes

Split from `2026-09-29-route-b-reviewed-bundle-compiler`, which deliberately stopped at
local and CI PostgreSQL tests. This is not a production release: the actual
publication, its fresh preflight, backup and owner consent stay with each wave's own
release ticket (for T1, `2026-09-28-localize-marketing-mix-and-brand-tone`). The frozen
T1/T2 package from `2026-09-29-prepare-frozen-t1-and-t2-localization` uses its own
schema and a historical snapshot; it is evidence for the freeze, not compiler input as is.

2026-10-07: all 13 cases passed using the deployed image, synthetic PostgreSQL and
the genuinely reviewed T1 candidate. Record SHA
`eaea56580f83ff71090ecdb8393f38ebc39bdc338abcc3936c34eda17bb41502` in
`docs/article-localization/releases/route-b-rehearsal/20261007-t1.json`.
Production writes: zero. Hub writes: zero because this wave contains life articles;
the record explicitly does not claim real hub dependency coverage. Raw evidence,
failed initial seed harness output and restore dump remain outside the repository.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
