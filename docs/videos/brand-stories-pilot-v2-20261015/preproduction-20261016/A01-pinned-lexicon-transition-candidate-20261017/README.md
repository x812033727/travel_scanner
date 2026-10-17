# A01 historical pronunciation pin — offline candidate

Status: **HOLD**. This directory contains a local planner and synthetic readback tests. It has no host installer, provider calls, database writes, retry reset or release command. No actual 81st event has been written.

## Why this transition exists

A01's 80-event audit tip used the historical ebfa590a dictionary. The captured shared dictionary is now e6403c82, with 23 unrelated additions. Runtime draft PR #1548 requires an immutable dictionary per story and refuses to initialize legacy A01 automatically. This candidate preserves the historical dictionary bytes instead of adopting those additions.

The planner authenticates the captured chain through the existing e640 rebaseline validator, then creates the exact immutable version/event/current format consumed by #1548. Only two state fields are added: story.lexicon_sha256 and story.lexicon_head_event_sha256. Retry counters, chapter states, narrative decisions and every historical audit byte remain unchanged. The state metadata makes the new audit source distinct; an unchanged source would create a self-edge in the old equality-based audit graph.

## Evidence and boundaries

- Four synthetic tests pass: intact transition, old-file mutation/addition rejection, partial publication/shared drift/extra approval rejection, and evidence identity/state mutation rejection. Synthetic owner/review strings are test data only.
- local-plan-summary.json records a read-only plan against the captured 80-event source; 185 historical evidence files were hashed. This is a plan, not a persisted migration or permission to publish it.
- snapshot-format.mjs is the #1548 format module with only its two relative imports adjusted. Restoring those import paths gives SHA-256 66e11923b9de4a0ac065a1f4f9b38819c665ee7fa53a32957490069286434982.
- preparePinnedEvent requires separately supplied review and owner-record bytes, bound to this plan and source hashes. Matching strings cannot authenticate a person or create authorization; the future caller must verify authority separately.
- verifyPinnedTransition checks complete historical file sets and bytes, exactly one new audit event/revision, exactly three snapshot files, unchanged shared dictionary, strict runtime readback and the complete resulting source tuple. It continues to return HOLD and paid_work_allowed:false.

## Local use

Run transition.test.mjs with Node 24.19 or later using --test. The planning CLI accepts only --snapshot <local-capture-root> --old-lexicon <historical-json>. It prints a plan and never writes outputs.

## Still required

Independent review of this candidate; a guarded host adoption protocol covering atomic visibility of both docs and work-state files; a fresh matching production export and explicit host action authorization; resolution of the uncertain legacy job; and an updated 81-to-82 narrative transition bound to the pinned dictionary. The older e640 round20 bridge does not validate this new source. A01 must pass factual, listening and storytelling gates before paid media. Nothing here approves a script, resets retries, changes the shared dictionary, releases a HOLD, deploys #1548, or completes a film.
