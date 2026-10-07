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

- A third confirmed-answer replacement failure occurred during English dub ASR:
  `logs/20261007T142725Z-check-audio-en.exit.json`, code 1, child 32892,
  closed at `2026-10-07T14:32:19.602465Z`. Request SHA
  `0a725f16e704643b4d7cf535e0e549bd0c2872d7b1a66810049b97e9940c3d98`
  had already received HTTP 200 and saved an intact confirmed temporary record.
  Operator recovery verified the exact current English `ag027` raw clip,
  its native 16 kHz ASR request, unique captured response and dead producer,
  preserved the sent/tmp/cache snapshots, then promoted the exact confirmed
  bytes at `2026-10-07T14:38:21Z`, with zero network calls. Response/answer SHA
  `a564266e8785d5aec293d109f997b953533d21394c293c95f247e8dc45255117`;
  restored native record SHA
  `cb3268df8f93493a0ee8491e2af716096eb0889ae40251a4d79082405f55460f`.
  This recovery succeeded with a rename after process closure; it does not
  establish the underlying cause or repair the native implementation.

- A fourth confirmed-answer replacement failure occurred during Japanese dub
  synthesis: `logs/20261007T145007Z-dub-ja.exit.json`, code 1, child 32756,
  closed at `2026-10-07T14:53:07.590760Z`. The four-line task-spec request SHA
  `1b2cc8136b746d1f3387515e8e3a7095ab060f45de3f42127fb1b7c0db2ee262`
  had a captured HTTP 200 response and intact native confirmed temporary record.
  Operator recovery bound the current Japanese request, native-converted 48 kHz
  WAV, captured response, sent/confirmed records and closed producer before
  promoting the exact confirmed bytes at `2026-10-07T14:58:30Z`, with zero network
  calls. Captured response SHA
  `5dc071b9d604ab728e5959b5967398400f47c8aaebc38637ed00cce8047b5897`;
  confirmed WAV SHA
  `95ca824c53539d694d5c195bc10469bbee0c47a36b2f38c6837fabeffe91033c`;
  restored record SHA
  `f644a0b75897a39f4c4369754e779798e9346126f1c35351f2625572be98b03c`.
  The resumed run reused its already-paid answer; no uncertain request was
  cleared. This remains an operator workaround, not a native Windows fix.

- A fifth replacement failure interrupted the second ordinary Japanese retake:
  `logs/20261007T164749Z-dub-ja.exit.json`, code 1, child 39000, closed at
  `2026-10-07T16:49:54.829529Z`. Single-line ag131 request SHA
  `72285f4cff35caa0be063b4c2f0af3197c147afa43f3ef06624d37e477baccd6`
  had received HTTP 200 / 17 billable characters. Three historical captures
  share this body hash; the audit binds only the current producer PID/time.
  Actual response SHA
  `80ba67e08938057177e84f1cb26af83cfa08e0bbec71c60b33124a386cf93c51`
  converts byte-for-byte to confirmed native WAV SHA
  `7f1e3c484716555d7f41385ded9089db4bf45e9c603c8ffc4e2d1677e7084e3a`.
  Independent recovery review SHA
  `03596d246bd264124b64a38ce59580dc4c3b2ee3850f3bb90576723e0d77b272`
  binds the current source/translation, exact response and closed producer.
  The exact confirmed record was restored at `2026-10-07T16:57:01.939Z`
  after exclusive snapshots and readback, with zero network calls; record SHA
  `58c1265b4eb90fd5877749fb3a8769c24d04272e2f0e65a4f9da4b361afb9797`.
  Ten of the fifteen retake clips had already been written. Continuation must
  retain them and redo only the five unfinished IDs, reusing the recovered
  ag131 answer. Restarting all fifteen would buy completed clips again.
  This local recovery changes neither the unrelated held Korean request nor
  native implementation; the underlying Windows cause remains unproved.
