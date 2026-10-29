---
id: 2026-10-26-dub-settled-service-retake
title: Count a bounded dub retake after settled transcription failures
status: done
priority: P2
area: tools
owner: codex-dub-retake
claimed_at: 2026-10-26T08:16:08Z
created_at: 2026-10-26T08:14:23Z
completed_at: 2026-10-26T11:04:36Z
branch: codex/ai-editable-animation-20261025
depends_on: []
scope:
  - tools/video/automation/service-retake.mjs
  - tools/video/automation/service-retake.test.mjs
---

# Count a bounded dub retake after settled transcription failures

## Why

The Thai dub of ai-editable-explainer-animation has met six explicit settled Gemini OTHER/no-transcript responses for the same cab285 WAV. The ordinary automation retries ASR after backoff because no transcript exists; it never enters the retake branch, which requires a genuine mismatch result. One of the native two retake rounds is still available. A new take may help, but it must not be represented as an audio pass or buy the same redo again after a crash: native dub releases its completed speech journal as soon as its cache is saved.

## Definition of done

- [x] Provide a source-bound operator adapter that can reserve only the existing final retake round after the genuine due time, perform at most one exact one-line synthesis POST, and leave all voice acceptance to normal ASR/Jev.
- [x] Preserve permanent intent, actual response, source/raw archives and protected receipts. Unknown or interrupted operations are held without replay, counter refund, journal forgetting, fake flags or changed native limits.
- [x] Cover source/gate/due/lease/STOP/cap/clip/journal changes, crash boundaries, exact response installation, identical returned bytes, post-ASR failure, and protected evidence using isolated fixtures and injected transports.
- [x] Root independently reviews the final diff, completes the required broader checks, and reviews the scoped helper integration before declaring the feature complete.

## Steps

- [x] Confirm the current native retake path and its service-error gap without changing media or making API calls.
- [x] Implement service-retake.mjs and its required producer-entry hold guard.
- [x] Run 84 targeted tests with no real API/provider requests; all passed.
- [x] Prepare an external incident driver and a dry-run-validated patch for the original three scoped producer wrappers, without modifying those live wrappers.
- [x] Root reviews/applies the required guard patch and verifies all three expected helper hashes before considering a real execution.
- [x] Root reviews source-bound actual state at/after the existing due time; a future execution is not performed or claimed by this task's implementation agent.

## How to verify

`node --test tools/video/automation/service-retake.test.mjs` (84 tests, 84 pass, no skips; actual run by implementation and independent test agent). `node --check` passes for the module and external driver; all three patch candidates parse as modules. `patch --dry-run --batch -p0 < service-retake-helper.patch` succeeds from `/workspace/work/ai-animation-01` and changes no live helper.

The external driver defaults to offline status. `node /workspace/work/ai-animation-01/service-retake.mjs plan` was actually run read-only against the old project: 101 current clips, nine protected files, source final review d1a5872b-b500-409a-a119-ecc825b40040, exact selected request 65 characters, and existing due 2026-10-26T10:07:17.313Z (18:07:17 Taiwan). It reported earliest_execution_reached=false. No actual API, TTS, counter write, intent, STOP or media modification was performed.

## Notes

- Implementation: tools/video/automation/service-retake.mjs SHA eb68d968592ab82b8ff7bb25494cb8c915830bcb417b49d959938de01ab0e8c1; tests SHA ae05815a7fbe91621e19c2dd1c6d374560a113247b262a1ace86850801ae67a0. Test author/reviewer: OpenAI Codex /root/th_retake_recovery_audit/journal_guard; tests use real native planning, WAV conversion/trim and speech-journal behavior with fixture files and injected fake transport.
- **The module must not execute before producer guards are integrated.** A STOP placed before synthesis would itself stop native dub. Instead the adapter writes a permanent intent before reservation/dispatch; every controlled producer must inspect that intent before paid work. The guard creates its own intent-bound STOP under a verified lease, never overwrites/removes another STOP, and rejects prepared/reserved/dispatched/held/corrupt operations. Without a lease it rejects without writing.
- External patch: /workspace/work/ai-animation-01/service-retake-helper.patch SHA 203958dd2b035f2a890291c185b1a5a954ea0437031e85532ad1b9af142bc5b0. Metadata and exact candidate files are in service-retake-helper-patch.json and service-retake-{languages,flow,cli}.mjs.candidate. All live helpers remain unchanged. Required original→patched hashes: languages 0a99da6421412b9da48d1027f2bbc8d6db3ecc557e142f51e1c508d27d8ad7ff → b88301aaf04a6b8decd39880d4c22e858226b764d2d3304264e66d94dabc3534; flow 29e54f4238e03307fed3d44831b30ce4f09f34337147cc6ede444bd48ba9b660 → c6da84dd3f3c6b018ae33f4dfde0b7ed4cddd39fd913a865f7772b955a4c18f0; cli 5ef19855d5f30b93fb6961bfad9b27ce660e4455e0ba4711d96e76c2934718b7 → 954eb7d00d825abcb288c2e569453f41dd50f23afea195779f5dba9e84e4a0e4.
- External driver /workspace/work/ai-animation-01/service-retake.mjs SHA 2e5b4e86eaf2f4f28cae7393f44d4af5a5b3ae9848b51efa05b87b0e6333cda1. It pins module bytes, the real sixth-failure receipt and all three actually integrated helper SHAs. Default status/plan are local read-only. An explicit run requires an exact saved review-plan SHA, all integrated helpers and the true due time. Regenerate/review the driver if module bytes change.
- Scope limitation: these integration patches cover the known original scoped wrappers only. Generic unscoped repo CLI/other host workers are not altered by this two-file feature; do not bypass the permanent hold through them. System-wide enforcement would require a separately scoped integration into shared producer entrypoints.
- The adapter admits only the actual settled sixth-refusal receipt and its original preflight, primary local/remote approval, eleven distinct native QA items, current source/translation/voice/body hash, all current clips, native rounds1/1/0, and unchanged journal/protected evidence. It does not infer success from raw existence, wrapper exit0, unchanged WAV bytes, or a model's estimated byte count.
- At the actual POST it rechecks source/gates/protected/cache/fit/reservation and permits only the exact native current-process sent journal. It archives the actual HTTP response before native cleanup and verifies the raw installed by native 24→48k conversion and silence trimming. An applied history remains valid through later legitimate native rewording, while damaged historical proof holds again.
- Only one exact synthesis POST is allowed, even if native would normally retry a settled network/service refusal. Any unusable response, crash, partial reservation or bookkeeping ambiguity holds conservatively, with the reserved round retained; no automatic undo/retry/reconciliation route exists here. A same-byte successful response still counts as one used opportunity.
- A successful new take is still voice_ready=false/check_stopped=true; follow only with plain native makeDub/dub and actual ASR/Jev, preserving the six-failure backoff history and all existing caps. It may fail again or need native source-review boundaries. Existing English unknown receipt and KO/PT/ID skip files are never cleared or rewritten.

- Implementation handoff recorded 2026-10-26T08:48:26.391048+00:00. Task intentionally remains in-progress for root review; no feature completion or real retake is asserted.

- Final review also binds the complete current video.json bytes to the actual sixth-failure preflight media_source_sha256; a fresh plan cannot silently pair an edited visual source with the old approved cut. This has its own passing test.

- Scoped-wrapper race correction, reviewed candidate only: flow and CLI now acquire the actual native filesystem lease before the hold guard and retain it through all awaited settings/work/main calls. Flow injects this same lease into flow.leases, preventing a nested-stage deadlock; finally releases its step leases and unit lease. Languages already checked under its acquired lease. This closes the earlier candidate's unsafe precheck/await/dead-lease-takeover window; it is not an unscoped limitation.
- The two new subprocess fixtures use real separate Node PIDs, real filesystem lease creation/dead-holder archival, and actual adapter intent plus native speech-journal release. One SIGKILLs the retake after journal release and before applied persistence, then proves an earlier-prechecked helper is refused under its acquired lease, creates its own intent-bound STOP, and performs zero further fake-paid work. The other holds the helper lease across await and proves the competing adapter is refused before any intent, reservation or dispatch. Global network fetch is disabled in both child processes; the only paid-like actions are isolated fixture log entries.
- Fresh final targeted run: 84 tests/84 pass/0 skipped on 2026-10-26 around 09:02 UTC. The module stayed eb68 throughout the two race additions. All three candidate syntax checks, updated driver syntax and patch dry-run passed. The 09:03 UTC offline driver status/plan still reported native rounds shorten1/retakes1/reword0, defer_count6, no real intent/STOP, all three live helper integrations false, and the real due time still unreached.
- Earlier broad log /workspace/work/ai-animation-01/service-retake-full-tools-tests.log remains historical evidence. Its two service-retake assertion failures were not baseline: the run loaded an intermediate new source-preflight guard and older expected-error regexes while the implementation was changing. The actual guards correctly refused both source changes; final 84 verifies the matching assertions. Root must run a fresh final targeted and broad suite on frozen hashes before approval.
- Final implementation freeze for root review: module eb68d968592ab82b8ff7bb25494cb8c915830bcb417b49d959938de01ab0e8c1; tests ae05815a7fbe91621e19c2dd1c6d374560a113247b262a1ace86850801ae67a0; external patch 203958dd2b035f2a890291c185b1a5a954ea0437031e85532ad1b9af142bc5b0; driver 2e5b4e86eaf2f4f28cae7393f44d4af5a5b3ae9848b51efa05b87b0e6333cda1. No implementation, test, driver or patch edits after this freeze without notifying root first. No actual API/paid call or canonical media/counter/flag mutation has occurred.

- Root completion review 2026-10-26T11:00Z: frozen module/tests/patch/driver SHA all match the independently reviewed final candidates. Fresh root targeted log reports84/84 pass. Final full tools log reports2831total/2820pass/6fail/5skip; the six unchanged managed-sandbox a01capture fixture failures remain separately filed in2026-10-26-make-a01-capture-fixtures-work-in. This is NOT a full-suite pass. No failing film/audio QA was skipped.
- All three actual scoped helpers were installed under a real exclusive project lease, with exact old-byte backups and expected post-SHAs validated; installation receipt docs/videos/ai-editable-explainer-animation/research/media-checkpoints/service-retake-helper-installation-20261026.json. Generic unscoped CLI/host workers remain outside this two-file integration and must never bypass the permanent hold.
- Actual reviewed due-time plan f69830e69fa536d145707228bbcd5997ca4cafea60e8f36889dcfefb4ea71b1c ran once after the native10:07:17Z due. Permanent intent80314efb1c9db5dbc40cfac786078904bf9e0711e5f0c7e8ff4ac9c9ab72ed41 is applied. Exactly1actual synthesisPOST/HTTP200/65reportedbillablechars installed newcab285raw f662f9a863bdd2cdc59da1934221fe700c6f0ea7cfb0fb8b2981622d3f9ae00b (4.42s), reserving native retake1→2. All100otherraws and9protected files unchanged. True receipt th-counted-retake-20261026.json SHA576bbb86d87de1b608ec2d081b38b8a13ed2b53145b6a45cf8417fb084a9585a. Actual outcome is voice_ready=false/asr_performed=false, not audio acceptance. Never repeat this redo.
- The ordinary native ASR/Jev continuation is delegated separately under the unchanged caps/history and existing meaning-review boundaries; this feature completion does not complete the film or claim foreign voice approval.
