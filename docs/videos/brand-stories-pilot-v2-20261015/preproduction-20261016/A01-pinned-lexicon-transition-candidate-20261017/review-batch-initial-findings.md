# Independent bounded real-review driver review — initial findings

Reviewer: codex-independent-a01-lexicon-1017. Date: 2026-10-17 (Asia/Taipei).

Reviewed review-batch.mjs SHA-256 e374eac44201ed9c9e281536105ce65ab2691b19fe93b95089e11ea1339bf71a, after the author added halted/skipped checks. **Verdict: HOLD; one P1 and two P2 fixes required before using --run.** No host, --preflight or --run was executed by this reviewer. Imports target the real installed /opt runtime and are unsuitable for an unmodified local invocation.

## P1 — successful source mutations are settled without an append-only audit edge

The driver directly calls advanceStory, which rewrites chapter/canonical/source state. It then calls api.settleRuns and clears runSlugs, but never appends a corresponding story/recheck-audit edge or preserves raw successful request-journal bytes. Installed run-receipts.mjs settle explicitly unlinks consumed successful journals. The installed Automation.advanceStory/flow path does not itself append this task's bespoke 80/81/82 audit format. Therefore successful real-review units can leave current source beyond the immutable82 tip with no genuine request/source edge and erase the local recoverable stage evidence.

Fix: capture the exact pinned before-source tuple, execute one bounded unit, preserve all actual request/response journal bytes and exact after-source tuple in an immutable audit event, read/verify the edge and linked raw bytes, then settle. Include initial relint/source-only mutation even when it makes zero model calls. Exceptions or readback failure must retain original journals, restore STOP and stop. A copied summary or fabricated receipt is not a substitute for the real successful journal. Source hashing must select pinned ebfa bytes rather than the unrelated shared4d3 dictionary.

## P2 — durable request mode is assumed but not required

The driver checks settings.enabled only. automationClient.settings configures its internal durable flag from settings.durable_stage_runs===true. If disabled, the driver can use legacy non-durable stage calls even though the bounded polling/recovery design assumes durable receipt/key identity. Require durable_stage_runs===true before removing STOP or dispatching any review request. Preserve the same durable key/receipt on RUN_PENDING; do not treat the log phrase “same durable request” as verification by itself.

## P2 — new block events can be missed when the reason string is unchanged

The added halted/skipped check correctly stops retryLater/defer, but Automation.block itself sets neither halted nor skipped. The initial state is already blocked, so comparing status cannot detect a new block. Comparing state.blocked text misses a repeated identical reason. Initial advanceStory(script passes lint) can also block for lint.other while every chapter lint array remains empty; the current driver then enters the model loop anyway. Wrap/observe actual block invocation, set a per-unit didBlock flag, and stop after initial relint or any later unit if block/halt/skip occurred, even when the block string matches its old value.

## Other observations

The five-level payload-relative path is correct for this fixed ASCII POSIX candidate layout (candidate/preproduction/brand/videos/docs back to payload). The absolute /opt runtime imports deliberately use installed code, while the source inspector comes from the reviewed payload. The project lease is held, registered in Automation.leases and verified before units; stage uses the installed fence. Global/scoped STOP checks, stage/slug/format allowlist and finite successful-unit/call/pending ceilings are present. Writer/media calls through stage are refused. Using next='verified' does not call script approval or media paths. State remains blocked throughout; this driver does not falsely activate it.

The finally block and signal handlers attempt to restore original STOP bytes. They cannot guarantee recovery after SIGKILL, host failure or process crash before finally; the host wrapper should retain its own deployment hold and preserve journals on failure. Restoring STOP must not silently overwrite a new STOP written by another actor.

RUN_PENDING retries use the installed client with unchanged state/payload until a unit succeeds, so client journal identity can protect reuse when durable mode is enforced. An exhausted pending bound throws and restores STOP. Other exceptions currently escape and leave journals, which is safer than issuing another request; ensure any audit wrapper preserves that behavior.

This report does not approve spending, formal factual/listening/storytelling gates, provider availability or owner identity. The original all-in pilot budget is a separate API gate. The proposed driver needs focused no-model tests for success audit-before-settle, unchanged-reason block, initial lint.other block, retryLater/defer and pending receipt retention before a real run. Historical structural reviews do not accept this new executable path.
