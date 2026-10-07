---
id: 2026-10-07-recover-confirmed-speech-answers-when-windows
title: Recover confirmed speech answers when Windows cannot replace journal files
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T11:42:40Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/paths.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/check-journal.test.mjs
---

# Recover confirmed speech answers when Windows cannot replace journal files

## Why

On Windows, native `tts` and `check-audio` received complete successful server
answers, saved native confirmed temporary journal files, then failed replacing
the existing sent journal with `EPERM`. The existing 630 ms rename retry did not
resolve both observed failures. The next run correctly stopped at the sent
record instead of purchasing the answer again, but recovery currently requires
an operator to bind the actual response, current audio and native temporary file.

## Definition of done

- [ ] Reproduce the replacement failure on Windows and determine its cause from actual filesystem evidence.
- [ ] Recover an intact, source-bound native confirmed answer without another provider request or losing the sent record.
- [ ] Missing, changed or ambiguous answers remain held; existing unknown-request protection still passes.

## Steps

- [ ] Inspect the exact failure, native temporary bytes, hard-link lifecycle and Windows access behavior before choosing a repair.
- [ ] Add meaningful recovery tests for synthesis and inline transcript/judge answers, including interrupted and mismatched recovery.

## How to verify

Run the relevant native journal/atomic-write tests and a Windows reproduction.
Record the provider dispatch count before and after recovery, requiring zero new
dispatches. A Linux-only green run is insufficient to establish Windows recovery.

## Notes

Observed during `ai-agent-vs-chatbot` continuation on 2026-10-07. Evidence is
outside Git under `<home>/mokaair-work/ai-agent-continuation-20261007/`.

- First TTS exit: `logs/20261007T111324Z-tts.exit.json`, code 1; actual response
  and native confirmed WAV were independently bound before promoting the exact
  confirmed bytes. Request SHA `0807a4bad44f205fce034b9c566d45dceb90e89d98867cae0bd4919a36350647`.
- ASR exit: `logs/20261007T113420Z-check-audio.exit.json`, code 1, child 37444.
  Request SHA `91678030d616b75e3effd484aa0d2ed05de241786f09d4cfefc2e4e5798201a8`
  has a captured actual HTTP 200 answer and intact native confirmed temporary
  file. A subsequent guarded run exited 3 without sending it again.
- Operator validation bound the exact native 16 kHz downsample of `ag006`,
  captured request and response bytes, native answer hash and closed producer.
  Node rename and Python `os.replace` both failed after this validation. File
  attributes were Archive; the observed ACL contained inherited user FullControl.
  This does not establish the cause, nor prove a scanner caused the failure.
- Immutable sent/tmp snapshots were preserved. Restoring the exact validated
  native confirmed bytes with flush/fsync succeeded; readback SHA
  `9761bc1451fd3acceb6349ad0110958c4dff90d103dbc73f70db0b7b7a4ac8ba`.
  Its recovery receipt explicitly records zero network calls and preserved tmp.
- The local operator workaround is not a repository fix. No uncertain citation
  request was cleared, retried or changed by this recovery.
