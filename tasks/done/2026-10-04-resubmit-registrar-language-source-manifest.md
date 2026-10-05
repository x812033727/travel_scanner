---
id: 2026-10-04-resubmit-registrar-language-source-manifest
title: Resubmit Registrar language source manifest
status: done
priority: P1
area: ops
owner: codex-video-registrar-resubmit
claimed_at: 2026-10-04T23:24:34Z
created_at: 2026-10-04T23:24:21Z
completed_at: 2026-10-04T23:59:20Z
branch: codex/video-native-followups-20261004-1525
depends_on: []
scope:
  - docs/ops/video-registrar-language-source-resubmission.md
---

# Resubmit Registrar language source manifest

## Why

The owner explicitly requested a replacement language review for
`cloudflare-registrar-renewal-price-ai-agent`. Its approved legacy review has ten
valid stored attachments, but the deployed YouTube consumer returns
`409 video_youtube_languages_invalid` because the language source manifest and
metadata are missing. Reuse the successful existing language results without
speech regeneration, approval or YouTube operations.

## Definition of done

- [x] One new pending language review contains a schema 1 source manifest,
      existing metadata and all ten original attachments with verified bytes.
- [x] Old approvals, canonical files, language choices, protected settings and
      existing YouTube fields remain unchanged; original Korean skip remains exact.
- [x] Durable one-shot submission and final read-only source/store verification
      are recorded in the scoped operational document.

## Steps

- [x] Confirm the exact project, owner authorization, current approved sources,
      legacy refusal and actual bytes of the ten original ReviewStore files.
- [x] Prepare an offline schema 1 packet and Registrar-only one-shot driver;
      test the actual request adapter and normal pending language flow.
- [x] Independently review the builder/driver and test the actual backend source
      contract without network, paid calls or database writes.
- [x] Freeze the exact packet, helper and evidence; complete root whole-source
      review and a fresh read-only launch preflight.
- [x] Execute only the separately authorized two small JSON PUTs and one review
      POST; record the exact new pending review identity.
- [x] Verify the real pending batch, original files and durable receipts.

## How to verify

Run the candidate `offline.test.mjs` with the bundled Node runtime and
`backend-contract-test.py` with the API virtual environment. The preparation run
passed 14 Node cases and 12 backend contract cases. Backend fixture composition
uses `verify_files=False`; actual large attachment hashes come from the frozen
read-only production evidence, not synthetic test bytes.

Before submission, recheck current owner, decisions, choices, retry/acknowledgment,
source and metadata bytes, protected settings, upload/session state, item jobs and
locks, and the exact fixed receipt directory. After submission, read all twelve
new and ten old ReviewStore files and call the read-only consumer once to confirm
that the new pending batch still requires owner approval.

## Notes

- Read-only production snapshot: 2026-10-04 23:13:20.467111Z through
  23:13:25.733925Z. Compact SHA-256:
  `8767dd0aa0d6b26b99c43d13a446a28a92b89ac0af991ab7742dc87824226f03`.
- Existing language review `2b5511ac-c76c-4585-a42a-85cd1498b5fd` was approved at
  22:45:27.764923Z. Four descriptions, four caption files and two successful
  EN/JA dubs are reusable; Korean retains its exact Jev skip receipt.
- Final approval contains existing assemble/pace/captions/policy warnings. This
  supplement preserves those findings and does not repair or waive them.
- Temporary packet has twelve refs: original ten, unchanged current metadata,
  and new schema 1 manifest. Canonical legacy manifest is preserved.
- Fixed one-shot receipt namespace:
  `/var/lib/mokaair/video-work/cloudflare-registrar-renewal-price-ai-agent/review/ops/registrar-language-schema1-20261004`.
  Any prior POST intent prohibits another POST or a replacement namespace.
- Existing YouTube ID, publish/removal timestamps must be pinned exactly if
  present; they do not cancel the authorized review supplement. No YouTube route
  is allowed. Empty jobs/process/lock observations are snapshots, not leases.
- Frozen candidate identity: manifest
  `56699d993c077ed8011626a28b87073bce9ef3ca6f9521af51872e75d59f49a5`,
  request `c31f2a841a3047db7c9e04abbf273d54448f477047af3801c520a7e872c85189`.
- Root completed the reviewed single submission with exit 0 and no stderr.
  New review `4b83ae77-ddce-438b-8121-10612541b5e0` is pending. Do not submit
  again: the fixed namespace now has durable intent/response/acceptance/readback.
- Fresh preflight sampled 23:34:17.328653Z through 23:34:22.481973Z. The only
  canonical file difference was the choice file's worker `synced_at` refresh;
  exact choices and original decision were unchanged, as already allowed by the
  frozen driver. No baseline was replaced. Full proof SHA-256:
  `d01b21c1888f93f56c357c192a3b225b0aa0d119e444e7b7aed621d6e107f3dc`.
- Actual-only post-submit verification at 23:53:53.983698-23:53:59.462664Z
  passed 30/30 guards: twelve new and ten old real ReviewStore attachments,
  exact schema/metadata/source, five stable receipts, original approvals,
  choices, owner, nonce and protected settings. New review remains pending,
  with no decision actor or timestamp. Real `verify_files=True` consumer returns
  `409 video_youtube_languages_invalid`: “最新語言包尚未核准，請完成語言審核後再送出”.
- Final full evidence, 182,397 bytes, SHA-256:
  `0f64e1095102a76128d71868d5dc29d9dc793fae3364e5319a7236658c20049f`.
  Compact evidence, 78,624 bytes, SHA-256:
  `0459a4ce070f07e2ec35adf6f822c6b64c8c5cd55d01563f34f0a6fab428f96d`.
- The final verification used one SHA-guarded SSH reader execution, exit 0 with
  empty stderr, no HTTP/provider call, fake approval, overlay, remote filesystem,
  DB or Redis data write. No speech generation, owner approval, YouTube
  operation, canonical edit, deployment or restart occurred in this supplement.
- Technical handoff is complete; the owner decides the new pending review.
  Official task completion and commit are left to root.
