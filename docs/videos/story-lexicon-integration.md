# Story lexicon integration — draft release gate

Each new story pins immutable pronunciation bytes before its first chapter or approval. The strict format/reader is reused from draft #1528; the integration adds a filesystem admission shared by ordinary dictionary writers and story publishers. Project loading, worker draft/listener guards, TTS, audio checks and dubs read the selected per-story version. Ordinary videos retain their shared dictionary behavior.

Reviewed story-plan names seed valid Latin tokens with `null` only at genesis, preserving existing shared pronunciations. A later writer's new terms are immutable proposals: its successful chapter is saved, the story blocks, and neither shared nor selected story bytes change. An explicit reviewed revision selects new bytes; the next worker pass invalidates chapter checking/listening without resetting their retry ceilings. Speech hashes invalidate dependent audio approvals and caches normally. No publisher accepts a missing review hash as a revision review.

## Transactions and recovery

The publisher holds the project's existing LEASE and a common dictionary-writer LEASE. It checks project/global STOP, writes durable work and docs intents, writes immutable version/event files, selects the docs current pointer, validates the full chain, and writes a work receipt. It clears both intents only after that readback. Readers with a pending marker HOLD. Paid callers check the work-volume intent too under their project lease and reject a dictionary different from the one loaded for their request plan.

`recoverCommittedStoryLexicon` only clears intents when the committed receipt, both remaining intents, current pointer and full immutable chain match exactly. Earlier crash phases stay held for separate operator review. A killed process may also leave the existing lease mechanism held; it is not a permission to clear an unknown holder.

## A01: deployment and production transition remain HOLD

A01's real 80-event chain must not use automatic genesis. Existing chapter files, an audit directory, a composed video, approvals or a narration timeline prevent initialization. Read-only legacy project loading remains compatible, while worker advance and paid speech stop with `STORY_LEXICON_MIGRATION_REQUIRED`.

Before releasing this integration for A01, prepare and independently review a separate exact-delta legacy transition against a fresh full host capture. It must preserve all original 80 event bytes, bind the actual old/current lexicon bytes (the latest observed delta was `ebfa590a… → e6403c82…`, not the historical two-term successor), include the snapshot version/event/current hashes in a genuine append-only 81st audit event, and update the source inspector to read pinned bytes from that transition onward. Docs/work intents must fence both publication steps and make a partially appended audit a HOLD. The existing uncertain stage job requires its own disposition. This branch does not implement or authorize that host-specific audit append, deploy, retry, model call or media production.

The fixture with 80 historical links proves only refusal and byte preservation. It is not a migrated production chain, an A01 source review or a script approval. Keep the integration task open until the legacy transition compatibility fixture and independent release review are complete.

## Verification

Bundled Node 24.19 is used for the focused suites. Core tests cover restart/shared-file isolation, a second writer, deliberate revision and stale project detection, exact 80-link preservation, and six crash points. Worker tests cover saved successful chapter/proposals and retained retry counters. The actual TTS entry test proves an unpinned legacy story makes zero server requests. Full affected suites, duration receipt review and hosted CI remain required.
