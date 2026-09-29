# Imported long-video language continuation, 2026-09-29

The owner asked this chat to continue the six selected long videos after the
language summary fix was merged and deployed. The independent one-shot job uses
the existing running video-worker image and paired home volume. It does not
rebuild, restart or deploy a website service.

- Code commit at launch: `4d7a204b`.
- Bundle SHA-256: `bae2677918ad1894fd080c79227f2bbd20060f0753dcea4277d4cfe3809c78b3`.
- Runtime receipt: 218 files checked after transfer.
- Worker image: `sha256:1003f5856f23311eee68cd18eef5f4055cda431df1700f03db249add46d420ae`.
- Container: `mokaair-imported-languages-20260929`.
- Container ID: `0602308a1de361698314eb7521ad88b34498b4f331d978d7d44ec267f2b8ce3c`.
- Started: `2026-09-29T11:42:33.586502155Z` (19:42 Taiwan).
- In-container batch: `/var/lib/mokaair/video-work/imported-long-languages-20260929/batch`.
- Arguments: `--phase all --max-units 100 --apply`.
- Initial units expected: 24 translations, then 18 selected dubs; shortening or
  failed QA can pause a project and is not counted as completion.

Before launch, 22 focused tests passed, task validation passed, all 554 original
caption cues matched source timing within 0.5 ms, and the host dry run verified
the exact final approvals and owner language choices for every project.

The manifest retains the preparation code hash used to create its artifacts.
The frozen runtime has the subsequent additional SRT-to-timing validation
(`prepare.mjs` SHA `a67e71ad362c6219291fe1394c0fa3f50aea2e4327e063412e498cf211424764`),
which was also run read-only against the existing bundle before transfer.

## Transport finding

The first translator run completed in the backend after 302,552 ms at
`2026-09-29T11:47:37.770926Z`. The BFF deadline is 295,000 ms, so the successful
answer did not reach the runner and its initial client retried. The original
container was stopped at `2026-09-29T11:51:45.952531019Z` (exit 143), with no
language submission yet. The script, final and source timing stayed unchanged.

The retry's translator finished at `11:51:19.946885Z` (228,706 ms), and all 94
translated lines were recovered from its worksheet. A copy is preserved under
`batch/recovery/image-trust-en-translator-before-transport-fix.json`, SHA
`c8bb62965381d8ce9d44932245911a6b65e6ae32216790d6e135ef59743e7a2f`.
Its independent reviewer finished at `11:53:09.002631Z` after the old container
stopped, so that lost review result cannot count as review acceptance. Resume
validates the saved translation against the source and reruns only the reviewer.

The corrective transport is an explicit opt-in for this isolated host job:
`MOKAAIR_SITE=http://web:3000` with
`VIDEO_LANGUAGE_API_ORIGIN=http://api:8000`. Only the language model POST goes
directly to the existing internal API with the same token and authorization.
Native HTTP allows a bounded 1,020-second response, including the subscription's
900-second execution and queue allowance. POSTs are never automatically retried.
Other routes retain their existing transport. The shared worker's equivalent
problem is recorded separately in the task board.

The corrected runner SHA is
`c869420eb1a966e1d2b1b6098051c95984bdebc42c104146d8af26e36942092d`.
After 29 passing focused tests and independent review, the delta was installed
only after the old container had exited; all 218 runtime hashes were rechecked.
The old runner and runtime receipt were preserved in `batch/recovery/`. The
abandoned batch lock and this job's STOP file were removed after confirming exit.

A fresh six-project dry run passed. The active replacement is
`mokaair-imported-languages-20260929-v2`, ID
`6f37f9919309ad5d3b73ffba3074471758aec4234c6509f0739fb06baafb8bc8`,
started `2026-09-29T12:01:31.863243928Z` (20:01 Taiwan), with the same manifest and
media. The existing web, API and regular worker services were not changed.

## Continuation

Read the container state, `batch/progress.json`, and `batch/events.jsonl`. Use
`status.mjs` with the existing site pairing to verify persisted review IDs, part
states and file hashes. An active process is not evidence that a review exists.
The host's batch is now the authoritative continuation state. The original local
archive is a launch snapshot: do not run its separate local copy concurrently.

The runner holds `batch/runner.lock`, does not automatically restart, and retains
completed work. If interrupted, confirm the exact container has stopped before
removing an abandoned lock or launching a replacement. Resume against this same
manifest; do not re-prepare over it. Changes to approved cuts or owner choices
require a fresh review of the continuation inputs.

Language-ready state does not establish human audio acceptance or Studio upload.
The separate publication package and owner publication decision remain outside
this job.
