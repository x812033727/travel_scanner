---
id: 2026-10-09-windows-rename-confirmed-answer-backoff
title: Preserve confirmed speech answers through longer Windows rename holds
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T18:15:17Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/core/paths.mjs
  - tools/video/core/paths.test.mjs
---

# Preserve confirmed speech answers through longer Windows rename holds

## Why

Two stopped Embedding continuations received complete ASR HTTP200 answers but
Windows refused the final canonical journal rename after the reviewed630ms
backoff. Both answers were preserved and promoted with zero provider requests.
The production process holding the destination has not been identified.

A private rename-only10230ms candidate reproduced a real two-second destination
hold successfully while the original630ms implementation failed. The remaining
repository work is to review and adopt an appropriately bounded local persistence
policy,without adding any provider retry or weakening uncertain-request holds.

## Definition of done

- [ ] Transient Windows destination holds longer than630ms can preserve and
      commit the same complete temp bytes within a documented bounded interval.
- [ ] Exhaustion preserves the old destination and complete temp and returns the
      original error. No sender retries,forget or fabricated confirmed results.
- [ ] Existing platform/error behavior and interrupted-response recovery remain
      covered by meaningful fault fixtures.

## Steps

- [ ] Compare current main/PR1379 with the scoped private0316d2bf candidate.
- [ ] Reproduce an actual delete-denied destination hold and permanent refusal.
- [ ] Review the latency bound,implement the selected narrow persistence policy,
      and run the relevant path/journal checks before submitting a PR.

## How to verify

Use a real temporary destination held without delete-sharing. Check old bytes
during the hold,same new bytes after a successful rename,and both old/temp bytes
after permanent refusal. Assert bounded rename attempts and zero provider retries.
Run the current core paths tests and related journal recovery tests.

## Notes

A separate postproduction DB-receipt rename EPERM closed SH5 v2 with zero
LANG transport (d4e7dcd1). Three private relays now retry only EPERM/EBUSY from
renameSync of the exact fsynced temporary bytes, checking original raw SQL/host
timestamps and the same SHA on every attempt; no unlink,restamp or API replay.
Defaults20 attempts/100ms pause allow at most1.9s intentional waiting. All23
focused cases pass and retained temp95 bytes5716b0e9 remain exact. Neither this
wrapper nor the earlier10.23s speech wait proves a universal Windows fix or an
identified lock holder. Repository persistence adoption remains open/unclaimed.


- The next real V6-segment2 run still refused canonical9cd rename after the
  full10230ms wait: last HTTP200 at18:29:48.495Z,resultd7e902a2 at18:29:58.899Z,
  closed3 receipt98caeddd. Do not call this private backoff a universal fix or
  keep extending its timeout. Closed-only Restart Manager and DELETE-access
  probes found no visible holder/permanent ACL denial; failure-time cause is
  unproved. The separate staged-answer journal follow-up owns the narrow
  current-own completed-response fallback and crash recovery compatibility.
- Operational evidence is outside Git under
  `<home>/mokaair-work/stalled-video-completion-20261008/embedding-audio/listener-round2/selected-language-finishing-20261009`.
- `windows-rename-10230ms-actual-fault-fixture.result.json`,SHAefc5cae7,
  passed3/3 actual cases: old630ms fails after683ms; private10230ms succeeds
  after2632ms on a two-second hold; permanent refusal is bounded at10230ms
  and retains the original plus complete temp. This does not prove the
  production handle owner or a fix for every Windows failure.
- Known5575 promotionc344099b and139d promotion665f3321 both reused genuine
  answers with sender0; all paid receipts/WAVs and original historical holds
  remain preserved. Do not replay either request as part of this follow-up.
- This ticket records unfinished repository adoption; the private production
  continuation and its original correction/cost/owner gates are separate.

Findings, decisions and dead ends, so the next agent does not repeat them.
