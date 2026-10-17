# Resume101 independent code and no-model review

Reviewer: codex-independent-a01-lexicon-1017. Final remaining findings: 0 P1 / 0 P2. Local offline review only; no host, provider, paid, merge or production execution by reviewer.

## Byte bindings

- review-resume-101.mjs: f851f26b3a6e2c27fcb31b1fe38dbb3d6b069c94b7234082fa02b5dafc468a75
- inspect-review-progress.mjs: 4be6618c7d1e5aeebed6903b3dce20356120092be4be9b4896aae0e021176e8d (previously reviewed implementation)
- capture/resume-review-101-host.sh: 52e70fcbb9f8ca7cf24146b0ba49a34a9d8ab611ec1ca3b8452a99a601693e7d
- capture/resume101-independent-harness.mjs: 949e5298b051773557024af85c97ad55401a2bfe9e561c959652c5cf0840158b
- capture/resume101-independent-drift-harness.mjs: 8e66f77f46a1c8050da78645164ad05726f10baad28ad2540986af92fcf056b3

## Scope and static observations

Reviewed full driver, installed listenChapter/advanceStory dispatch semantics, and caller. Driver requires actual101-link source af7bcc178e7cd7b92fedec401c2f1971f3213ab88d3cab4cbad18e3a7b2da803 before any run, exact original line, blocked prompt_fixes:narrative state, engine check_rounds2/narrative_fixes2, durable stage requests and the scoped STOP. Only listener/verifier story or verifier narrative stages are callable; no writer/media. Narrow first listener permits only r12e03 exact proposed text and no nonempty drop. Unknown listener fields are not consumed by installed listenChapter, which reads only patch/drop. Pending stays inside the same unit without settling or replacing the intent.

The installed listener actually marks engine.listened true on success. Wrapper correctly invalidates engine.checked and aggregate verified after that saved edit; it does not reset the completed real listener or any review/fix counter. Subsequently official advanceStory selects engine check, then the whole panel. Raw succeeded/adopted journal bytes are copied to immutable audit, source/readback checked, aftercapture and committed record persisted before settlement. STOP is restored in finally and handled termination paths; project lease released. No claim of SIGKILL/power-loss finally recovery is made.

Caller holds four deploy locks; requires exact clean4f02734769f683615d1ca8b641026ac8cf1f87b5, no existing global hold and a fresh unique release; acquires its own hold, checks actual staged driver/inspector bytes, zero queued/running A01 jobs and exact budget before running. After run requires STOP and zero active jobs, records budget after, then clears only its own hold. Any nonzero command preserves that hold. Independently ran bash -n: exit0.

## Independent no-model tests

Copied genuine snapshot101 and true80/81/82 baseline captures into unique OS Temp split roots. Kept real capture/inspection/lexicon/lease modules; replaced automation stage and advanceStory with local mocks, shortened polling wait, and skipped directory fsync only on Windows in harness. Thus this tests driver sequencing/guards, not installed model correctness or real provider dispatch.

One four-case run completed successfully:
1. Success: one stage answer and one settle. Mock settle asserts immutable audit/index and committed record already exist. engine.checked=false, verified=false; engine.listened=true/listener_done=true from completed mock listener; check_rounds2 and narrative_fixes2 unchanged. STOP exact bytes restored.
2. Extra r12e04 patch: rejected before applying changes. Original engine/auto bytes unchanged; raw journal retained; zero settle; STOP restored.
3. RUN_PENDING: two attempts using the same retained request key, one successful answer and one settle; same successful invalidation/counter/STOP assertions.
4. Nonempty drop: rejected before applying changes; original engine/auto unchanged, journal retained, zero settle and STOP restored.

Separate source-drift case appended one space to real video.json in Temp. Real source inspector refused before mocked stage invocation (no metric/stage record); STOP remained intact. Harness output label retains inherited HARNESS_RESUME97 text, but source/hash bindings and actual input are explicitly101.

## Limits

No remaining code-review blocker in these exact bytes. This review is not a formal fact/listener/narrative verdict, owner authorization, rendered-duration proof, paid approval or production success. It preserves the round10 failure and does not manufacture PASS. Actual successful listener adoption and the subsequent check/panel require genuine durable receipts and structural readback from the operator; mocks cannot substitute for them. Filesystem power-loss behavior and real provider pending-key implementation were not simulated end-to-end.
