---
id: 2026-10-24-preflight-required-sfx-before-paid-dub
title: Preflight required sound effects before paid dub speech
status: done
priority: P2
area: tools
owner: codex-open-tasks-sfx
claimed_at: 2026-10-24T15:03:10Z
created_at: 2026-10-24T13:26:50Z
completed_at: 2026-10-24T16:21:39Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Preflight required sound effects before paid dub speech

## Why

Independent review found required SFX are validated by sfxInputs inside dubSound only after paid synthesize. Missing or hash-stale SFX can spend narration before failing. This is separate from the completed music preflight.

## Definition of done

- [x] Malformed/missing/hash-stale required SFX refuse before speech status/synthesis, creating no new cache or journal.
- [x] Existing paid history remains; mix-time validation still catches a later race.
- [x] Focused regressions and independent duration binding pass.

## Steps

- [x] Recheck active scope and claim the ticket before editing.
- [x] Reproduce failure with fake provider, then apply a narrow preflight and retain negative cases.

## How to verify

Run the scoped dubs suite, full tools checks, independent long-form receipt check and task validation. No actual provider request is needed.

## Notes

Found in2026-10-24 independent review: dubs/cli.mjs sfxInputs inside dubSound, paid synthesize before that call; assemble/sound.mjs performs manifest/file/SHA validation. Preserve retained media/provider receipts. No production or paid action authorized by this ticket.

2026-10-24 implementation by `codex-open-tasks-sfx`: the board steward recorded
the exact two-file handoff before the official claim. Read-only ownership evidence
is retained in `%TEMP%/sfx-ownership-recommendation-20261024.json`: #1548 and #1614
merged their code, #1518 is closed and never touched these two files, and only our
#1831 among 27 open PRs touches them. The A01 transition and five-language pilot,
paid-work and host-setting ownership remain with their original tickets. The
active curio-s27 producer uses its own clean checkout; it was not stopped or changed.

The shared `dubSfx` guard checks the declared set using the existing `sfxInputs`
contract before credentials, speech status or synthesis, and is called again at
the original mix-time location. It does not require `build/sfx.wav`: a valid set
whose assembled track is absent retains the existing omission note and null
`sfx_hash`. Existing music preflight and all source/manifest hash semantics remain.

Bundled Node 24.19.0 ran the unchanged-source red test first (actual exit 1): all
six invalid source/manifest cases reached fake speech work before refusal. The
repair's focused run passed 10/10, zero skips, actual exit 0. These cases assert
zero additional HTTP/status/vendor calls, no new locale dub directory, unchanged
paid narration journal, and byte-identical state, script and retained SFX files.
The positive case permits a valid set without an assembled track; a source changed
after speech starts still refuses the final mix while retaining completed speech.

The first full four-file dub suite retained an actual exit 1 (61 passed, 3 failed
including the enclosing subtest, zero skips): two existing narration-fixture cases
hit Windows `EPERM` on speech-journal atomic rename before the SFX preflight.
The unchanged-source full sequential retry also retained actual exit 1
(60 passed, 4 failed including the enclosing SFX subtest, zero skips): three
speech-journal `EPERM` errors occurred during narration fixture setup or the
existing target-alias audio check. No assertion was removed and no journal
retry/workaround was introduced. The exact results and actual source hashes are recorded in
`%TEMP%/sfx-preflight-validation-manifest-20261024.json`. Logs remain separately
named `sfx-preflight-red`, `sfx-preflight-green`, `sfx-preflight-dubs-full` and
`sfx-preflight-dubs-sequential`, each suffixed `-20261024.log`.

Product sources are frozen at CLI SHA-256
`4ac25a59de9549389d3a9cf353ecfb9a1ed2ca7cb6d4c5e6321ab886eef15ed4`
and test SHA-256
`41fcb0eb694fdea3011b3bea6accb79ec21bfaea9aeab80ed59b647510d1496c`.
Independent duration binding of `dubs.test.mjs` remains for a distinct reviewer;
the author did not edit the receipt or rebind it. The coordinator owns final Linux
CI against the new head, including all four dub test files. This task remains
in progress until that required check and independent review pass; the native
full-suite failures are not green evidence. No third native retry or Linux setup
was attempted. No real provider request, production write or media change.


2026-10-24 independent DURATION_ONLY accepted by codex-independent-sfx-preflight-20261024: one binding advanced from reviewed ae8d6948,107 unchanged; full prior report preserved. Current108 hashes and frozen2 sources reverified; receipt checks2/2 and473plans actualexit0. ReportSHA9a10afd0144a7b0d473c9b537a0a7ff7a0a775bc03a0b58318652947af0a31fe; receiptSHAd2ca7c73240e864127b9afe7e49296471049196679bbe6973aadb470b3fc6ac1. Required new-head Linux coverage remains pending before archival. Existing Windows rename failures remain tracked by the earlier Windows speech-journal tasks; no duplicate task or journal rewrite added.


### 2026-10-24 coordinator acceptance

Required Linux acceptance is complete on exact head e2436c4333c38f103ed2b8c2b4b325200c13ca85: all8 workflows and all17 primary CI jobs succeeded (https://github.com/x812033727/travel_scanner/actions/runs/40109449526). Both Linux full-tools logs explicitly pass all10 new SFX guard cases and all24 task-inventory cases. ffmpeg/Chromium fulltools2755passed/3intentional skips; video-docs236/236; VideoTooling2437passed/4intentional skips plus all5 real-media smokes. The earlier native full-dub EPERM failures remain recorded above and in existing Windows journal tickets. Frozen CLI/test hashes4ac25a59de9549389d3a9cf353ecfb9a1ed2ca7cb6d4c5e6321ab886eef15ed4/41fcb0eb694fdea3011b3bea6accb79ec21bfaea9aeab80ed59b647510d1496c reverified after CI. Independent merged108-binding receipt retains both main/branch histories; guards2/2 and473plans actual0, reportcd99059aa3f7f6ddc904c5cb27b6682ed4fc4795dc479530989d6b314d479b19,receipt27f4fb12bc69d2f5843a328c04cbdbd7fe2d31944149a2a4de6a531e1fc62afb. Local implementation accepted; merge/deployment and paid media remain separate.
