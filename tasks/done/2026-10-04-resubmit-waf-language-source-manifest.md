---
id: 2026-10-04-resubmit-waf-language-source-manifest
title: Resubmit WAF languages with verifiable source manifest and metadata
status: done
priority: P1
area: ops
owner: codex-video-stall-followthrough
claimed_at: 2026-10-04T16:10:14Z
created_at: 2026-10-04T16:10:01Z
completed_at: 2026-10-04T16:45:11Z
branch: codex/video-native-followups-20261004-1525
depends_on: []
scope:
  - docs/ops/video-waf-language-source-resubmission.md
---

# Resubmit WAF languages with verifiable source manifest and metadata

The owner explicitly requested a new review for
cloudflare-ai-attacks-own-waf-49-findings because the old languages approval
lacks a verifiable source list and metadata. This authorization is limited
to source-correct resubmission; it does not approve a new review, generation,
upload/publication, or deployment of PR1210.

- [x] Freeze current owner choices, final/publish identities, canonical source,
      metadata/package and every existing attachment; preserve old review
      ab622864-79de-4290-bce0-0ed9a3d1d36d and its exact files.
- [x] Prepare a source-bound manifest and actual metadata attachment with
      verified file bytes; keep the original final and genuine JA/KO skip
      receipts, with no paid regeneration.
- [x] Independently validate the complete payload against the deployed backend
      contract and review the exact single-submit route before writing.
- [x] Submit once under the owner's explicit request. For an unknown response,
      reconcile the same content identity rather than blindly POST again.
- [x] Verify persisted new review/files/hash, attachment contents and source
      validation; leave new review pending for the owner.
- [x] Preserve settings, budgets, uploader state and all historical approvals.
      Record outcome without claiming upload, publication or human listening.

Known old review payload contains only locales and nine files
(four descriptions, four captions, one English dub). It lacks the
languages_manifest and metadata roles required by the deployed consumer.
Implementation paths are held by existing claims; operational preparation
must not edit or release those owners' repository code.

Single submission succeeded through the official review API. New review
02095208-b5de-4291-8428-4f92e792fbe5 is pending with eleven files and source-bound
manifest e22ec95719d3c549a3e81c60eadcd512b5397f74fdb7eb852aecdaa9ed5ccba4.
The fixed durable receipt prevents another POST. Old approval/history and all
source/canonical files passed the real post-submit API readback and file guards.
Final independent full-file consumer validation passed at 16:42:06-16:42:10Z:
new 11/11 and old 9/9 actual ReviewStore bytes/size/SHA matched, source-bound
composition passed with a transient simulation only, and the real pending
consumer correctly refused use before owner approval. Database session remained
clean; original review, final, choices and protected settings remained stable.
Final proof SHA d1c83bf3ce957ab6cfe769a9a1bba5769f24c271b95dc7a374f7f874f36efc95.
Operational record is docs/ops/video-waf-language-source-resubmission.md.
