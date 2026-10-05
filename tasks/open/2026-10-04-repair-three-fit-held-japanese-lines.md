---
id: 2026-10-04-repair-three-fit-held-japanese-lines
title: Repair three fit-held Japanese lines without rebuying whole batches
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-04T15:51:39Z
completed_at:
branch:
depends_on:
scope:
  - docs/ops/video-native-ja-fit-recovery.md
---

# Repair three fit-held Japanese lines without rebuying whole batches

## Observed failure

Native Grok and WAF Japanese dubbing now have real skipped receipts, rather
than a stalled producer. Grok t3ut/uaxy remain too long at the existing 1.15x
maximum; rejected shorten attempts triggered the number-preservation guard.
WAF paid retakes were saved, but the 7s78/2qxb shared window still exceeded its
limit by 0.10 seconds after the two locale-wide shorten rounds had been used.
Do not call changed WAVs passed by attaching their previous checks.

At 2026-10-04 15:39 UTC, Grok has four caption languages and English/Korean
92-line audio checks complete. Its languages review
178a957d-19f9-451d-b1cc-fe516f4d2b2e is pending; manifest SHA256
6837b14635018e7b9a0a0a3fdd6124ff2648f668b4628f6bb109e53ccfb275f7
and its package must remain intact. Japanese is explicitly skipped. WAF
Korean was still being checked and had not produced its new language review.

## Prepared evidence

The source-bound plan is
TEMP/mokaair-video-ja-three-line-source-bound-plan-v2-20261004.json,
SHA256 52746b515d49fe445fa4f011a8f6b7f39963ba582af48d491da0b7aa6dd21604.
It proposes only t3ut/uaxy/7s78 wording changes, preserves exact number
sequences, body windows, Sulafat, Gemini and the selected model, and does not
increase the 1.15x ceiling. No candidate has been adopted or synthesized.

The plan protects another 193 original raw Japanese WAVs and all existing
stretched media; the three original target WAVs and source/skip receipt hashes
are pinned separately. Full protected inventory SHA256:
6b2048c79ef793d00098f35a7c3ae0d8bc11007f71c2f56042caaf6bd626d31a.
Read-only failure evidence SHA256:
30fc0930686c2113186faa9a8678b3e18b0c52cc24eaf377b369a9147eab957f.

## Acceptance

- [ ] Recheck the exact current source/final approval, owner choices, provider,
      voice, selected model, lexicon, current reviews, STOP/drop state, quotas
      and producer ownership. Stale snapshots do not authorize execution.
- [ ] Independently review a concrete single-attempt helper and zero-network
      crash/refusal/replay tests before any paid request. Use a separate
      operation namespace and preserve raw intents/results before consumers.
- [ ] Keep a maximum of three new single-line synthesis POSTs and 89 rendered
      billable characters, with no retry of unknown responses or a second
      take of the same payload. Do not substitute the image budget or finite
      six-image-video allowance for speech accounting.
- [ ] Preserve the existing 10,000,000-character monthly speech cap and
      200/day Jev limit; freshly enforce remaining quota for actual ASR and
      Jev work. USD/token cost is not inferred from character counts.
- [ ] Fit and judge the new candidates against the original windows and true
      audio. WAF's 11 newly paid retakes require fresh checks; its other 93
      current passed entries remain untouched. Grok Japanese still needs its
      real complete audio checks; no synthetic listening approval.
- [ ] Do not rebuild a worker or mutate a project while another producer is
      active. Canonical adoption requires verified exclusion; STOP alone is
      insufficient, as recorded in native-video-project-stop-and-producer-exclusion.
- [ ] Preserve existing pending manifests/packages/reviews. Create and verify
      any appropriate successor only after the source/producer/review contract
      actually permits it; do not silently overwrite or resend a pending batch.
- [ ] If a new limited candidate still fails, retain it and its paid receipt
      and stop. Record the exact remaining content/owner decision; never buy
      the entire Japanese batch again.
- [ ] Distinguish candidate preparation, synthesized/checked audio, backend
      delivery, human listening acceptance and upload/publication.

## State

Only read-only diagnosis and offline candidate preparation have occurred.
There is no live helper execution, new payment, canonical source adoption,
approval change, resubmission or deployment. Existing native producers and
the pending Grok review remain in place.

