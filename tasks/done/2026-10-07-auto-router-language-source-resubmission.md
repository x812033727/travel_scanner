---
id: 2026-10-07-auto-router-language-source-resubmission
title: Resubmit Auto Router language review with verifiable sources
status: done
priority: P1
area: ops
owner: codex-auto-router-resubmit
claimed_at: 2026-10-07T06:41:06Z
created_at: 2026-10-07T06:40:48Z
completed_at: 2026-10-07T06:49:41Z
branch: codex/auto-router-language-resubmit-20261007
depends_on: []
scope:
  - docs/ops/video-auto-router-language-source-resubmission.md
---

# Resubmit Auto Router language review with verifiable sources

## Why

Owner requested replacement for the approved legacy language review of
`cloudflare-auto-router-who-measured-savings`. The actual upload consumer rejects
its missing source manifest and metadata. Preserve existing selected assets and
all original approvals/skips; supplement provenance without paid regeneration.

## Definition of done

- [x] One new language review contains source manifest, unchanged metadata and
      all eight original description/caption attachments.
- [x] Actual persisted review passes the deployed consumer with file hashing.
- [x] Original choices, final/publish/legacy approvals, media and canonical
      artifacts remain unchanged; operation evidence is recorded.

## Steps

- [x] Confirm exact project, actual legacy refusal and current source approvals.
- [x] Validate frozen schema 1 candidate using deployed consumer and actual bytes.
- [x] Independently review the one-shot driver and recheck frozen source state.
- [x] Submit through official review API once and verify actual readback.

## How to verify

Use deployed `read_approved_package(..., verify_files=True)` in a read-only DB
transaction; rehash source/current/store attachments and compare authority,
choices, metadata and canonical artifact snapshots before and after submission.
Validate task protocol with `node tools/tasks.mjs check` and `git diff --check`.

## Notes

Four metadata/caption pairs are complete. EN/JA/KO dubs all retain explicit
original skips; no dub attachment is ready. Existing API policy automatically
approves a language batch without ready dubs; no owner approval is fabricated.
The ordinary producer defect is already covered by PR #1363's follow-up task
`2026-10-07-normal-video-language-submissions-omit-source` and source scope is
owned by another task. Do not repeat ordinary `review-push` as a repair.

Preparation used temporary candidate JSON files and in-memory review status
only; database session remained read-only. Candidate has 10 attachments.
Manifest `bf1304f629460a67d8a9a2e5125460ebc0c69bd3f247bc7e3868bd57e53662c1`.
Full operational record: `docs/ops/video-auto-router-language-source-resubmission.md`.

Actual POST HTTP 201 at 2026-10-07 06:48:23.818600Z created approved language
review `751edf71-c6ff-411a-b691-6b83bf82e34f`. All ten real stored attachment
hashes/sizes pass; deployed actual consumer accepts the persisted review.
Four localized metadata entries plus five caption locales compose successfully.
Canonical files, original approval rows, choices and skip payloads unchanged.
No YouTube delivery state introduced and verification DB session was read-only.
Six private durable receipt files independently verified in the original worker.
The fixed namespace has an intent; never POST again or bypass via new namespace.

Deployed worker predates the new lease module. Initial launch failed before any
HTTP request; absence of intent was reconciled read-only. Adapted bounded source
guards were independently reviewed and fresh proof matched the frozen packet.
No producer exclusion, new lock installation or worker restart is claimed.
