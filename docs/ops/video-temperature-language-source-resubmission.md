# Temperature language source resubmission

The owner requested a replacement language review for `ai-term-temperature`:
“溫度（Temperature）是什麼？調低不等於更準，設成 0 也不保證每次一樣｜AI 名詞十分鐘”.
The approved legacy review lacked the source manifest and metadata required by
the deployed language-package consumer. This operation supplements existing
results; it does not authorize media generation, approval, YouTube or deployment.
Dates below use Asia/Taipei; immutable receipts retain their UTC timestamps.

At 2026-10-08 08:24, one replacement language review was submitted and read back:

- New review: `d084189d-b95c-438c-8acd-7ff4225899da`, **pending**.
- Manifest SHA:
  `0707616d22c08ca4dd0bd459fe5b8d5606fa8106157e29082f584ffbe565b36c`.
- Request-body SHA:
  `00fe12e086be5872d015f488cf386d182b0049511b7bfc0e244de7112de4943f`.
- Retained old review: `d524a6a0-92c2-4d3e-9d99-4e3f72d230a2`, approved,
  SHA `8aa426924ebdac53e9a2e7fd31cf88c5229204b5598d4b21060eb38929d0e9ff`.

The new review contains eleven references: all nine existing attachments, the
current multilingual metadata and a schema 1 `languages_manifest`. The original
attachments are four descriptions, four caption files and the English dub.
Japanese and Korean retain their original complete skipped objects and reasons;
no skipped track is attached or regenerated. Simplified Chinese has no selected
dub. The ready English dub makes this new batch require owner review. The old
approval was not copied to the replacement.

The manifest binds the unchanged approved sources:

- Final `ace25f27-29d7-45a6-b36c-fd4ffd16fddb`, SHA
  `a6690235f47be486c7371dc277b80f0b99138f8baae813a29d47493e09e511f9`.
- Base publish `80ba5755-6318-45fd-9830-9403058601e0`, SHA
  `ec4095e0f2854776a344252d70df4703a8ad1c9f40bfa9a385ea1e538b380a5e`.
- Current multilingual metadata, 12,011 bytes, SHA
  `a111c4ab831839f16d44261ddc45f3e4a3b64b55c9deae797507fec9bcf23d65`.
- Original choice at 2026-10-07 19:52:46.820587, speech hash
  `cee209ae2dca2979`, branding hash
  `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`.

The manifest preserves all owner choices and locale states. Description bytes
match the existing localized metadata serialization. Original final QA findings,
decision and payload remain unchanged; the supplement makes no new video-quality
or human-listening claim. The base publish metadata is an older original-language
package, so its SHA is deliberately different from current multilingual metadata.

Independent source review and sixteen extracted-function, zero-network cases
passed. They exercise source/choice/asset drift, eleven references, ready/skipped
states, item locks, file and directory fsync before POST, a lost response followed
by permanent refusal of a second POST, and readback recovery without submission.
The small mock attachments test transport behavior; the real media hashes are
established by the production reader below. Node syntax and Python compilation
passed for the frozen operator sources.

The actual preflight used the installed consumer on production revision
`af596412c8f433b184c1e544d432f44145f666a8` in a physically read-only,
repeatable-read transaction. It reproduced the old missing-manifest/metadata
refusal, verified the original stored attachments and validated the candidate
with a detached approved copy in memory. That copy was never attached to a DB
session or persisted. Active exact-slug stage/media jobs, including submitted
media jobs, were absent. These observations are snapshots, not a producer lease.
Protected runtime settings were read to obtain ReviewStore; they were not changed
or independently frozen under a global settings digest.

The bounded transport performed two small JSON PUTs and one review POST.
Its durable exclusive submission intent was fsynced, along with the parent
directory, before POST. The fixed namespace is:

`/var/lib/mokaair/video-work/_recovery/temperature-language-resubmit-20261008/ai-term-temperature`.

An existing intent permanently prevents another submission. Lost or malformed
responses require persisted readback; changing namespace is not permission to
retry. This operation has completed, so its producer must not be invoked again.

After exact persisted readback, the original canonical `review/languages.json`
was retained as `original-review-languages.json` in the operation directory,
then atomically replaced by the verified source manifest. Its file mode was
preserved and its directory fsynced. Canonical approvals, timeline, metadata,
all original media and owner language choices remain unchanged. No project or
settings PUT, provider request, worker restart, deployment or YouTube call ran.

The actual post validator at 08:25:19 verified all eleven stored references and
exact metadata/manifest bytes, source identities, choices, skipped states and
new pending review. DB new/dirty/deleted objects and ReviewStore writes remained
zero. The actual consumer now reports:

“最新語言包尚未核准，請完成語言審核後再送出”.

The former missing-source/metadata blocker is repaired. Actual package consumption
remains refused until owner approval. A separately recorded in-memory approved
copy passes composition; that result is not real approval or upload readiness.
At 08:26:29 an additional readback verified all nine canonical attachment hashes,
unchanged approvals/timeline/metadata, the exact retained original manifest and
the aligned new manifest. Auto remains done, with no STOP or running lock.

Evidence and temporary operators remain outside Git under
`C:/Users/x8120/mokaair-work/handoff/temperature-language-resubmit-20261008`;
host sources and receipt copies are retained under
`/root/temperature-language-resubmit-20261008`. The authoritative durable
submission receipts remain in the fixed work-volume namespace above.

- `temperature-independent-source-review.json`, SHA
  `400ed7ed45b742cbd66e116763451170d058f58e70a4044f911b783729e6b42b`.
- `prepare.mjs`, SHA
  `3b5e494268a4f65a5fc6b4b7191093e250876b02c178e8f9eb99ff310634928b`.
- `submit-v2.mjs`, SHA
  `9e7621b2022e12133939e4ffbf26381651fe1a7c1c7bafc7bbf79dc8324bb7ee`.
- `validate-v2.py`, SHA
  `af1c50329a7ccb53b7b7a88c34f0556e0a4bce2c5d3384fc5aa703a3624528d5`.
- Actual preflight receipt SHA:
  `6d75067e50a5c49d3066e3291bee8afa78a01acce963dd6e8bb422bf46332bee`.
- `temperature-actual-post-validation.json`, SHA
  `6ea4dd61fc9f70b73963e61ed9f9c86e97e47d3ffa5f13c091b9154562d816f8`.
- `temperature-final-artifacts-readonly-bundle.json`, SHA
  `0b74c41cd6077286cc782a21a2d94f57651a3d14b44a6e56e06800c3a9a68fe4`.
- Durable submission intent SHA:
  `124723fec6379f5af2fc0ace7d0e80f2f0af95ed3bd08880cbdb1a114df938e9`.
- `temperature-independent-final-evidence-review.json`, SHA
  `58ef4f693bf694f393534b683cbee0c0c784afd121bd252823366f67fbcb8667`;
  57 actual-evidence checks passed. This independent review decodes and validates
  root's actual reader/validator evidence locally; it does not claim a second
  remote media rehash or another provider call.

The scoped resubmission is complete. Owner approval, Studio audio handling and
upload/publication remain separate. Native producer integration is already
tracked by `2026-09-30-youtube-approved-languages-sync`; this packet repair
does not modify that shared implementation.
