# Auto Router language source resubmission

The owner requested resubmission for
`cloudflare-auto-router-who-measured-savings` after the upload consumer refused
the approved legacy language batch with
`video_youtube_languages_invalid`: “舊語言審核缺少可驗證的來源清單與 metadata，請重新送審”.

The normal language producer still omits the schema 1 source manifest and
multilingual metadata. This operation supplements its existing results through
the official review endpoint; it is not a producer deployment or a new media run.

The current source approvals are:

- Final `f6ebea4c-f2d1-494e-850f-4d4c157df9d5`, approved 2026-10-07
  03:35:57.335082Z, final SHA-256
  `8b62706e16982b666a561aaedd17cf282668d5ae5d156303c30d24a777a15451`.
- Publish `372131a8-d1e5-48c8-8940-81a42d1632e0`, approved 03:55:45.350646Z,
  metadata/content SHA-256
  `3cdde0a7ec209e8013082d3b86cf714420d8e28fda4ab1ca6d4a9bc98c68051f`.
- Legacy languages `100abbc4-2a21-47de-b73d-b52458f5c75e`, automatically
  approved 05:55:38.845907Z, content SHA-256
  `02bc586eace84e06060164c8e09be39e60f30c6ac2f8abfc80d18c847a3fe489`.

The original choice at 03:36:05.565615Z selects metadata and captions for en,
ja, ko and zh-CN, plus dubs for en, ja and ko. All three dubs retain their exact
original explicit skips: English contains a line that does not fit at 1.15x;
Japanese and Korean failed the existing Jev retake/rewording limit. No partial
dub is attached or represented as ready.

The supplement reuses all eight original description/caption descriptors and
bytes. The two additional attachments are the unchanged current multilingual
metadata and a schema 1 `languages_manifest` binding current approved source
identities, branding/speech hashes, current choice, original decision timestamp,
exact locale payload and every attachment descriptor. Derived multilingual tags,
caption/thumbnail inventory remain part of the existing metadata; the composed
base package retains its approved original title, description and tags.

Candidate manifest SHA-256:
`bf1304f629460a67d8a9a2e5125460ebc0c69bd3f247bc7e3868bd57e53662c1`.
Candidate request SHA-256:
`a779ba849cd9e230a12fb4bae025752674a1d4ee6e95af92b2fd098af8e0a539`.

Preparation ran against the deployed `read_approved_package` with
`verify_files=True`, actual stored source bytes and two temporary candidate JSON
files. Its hypothetical approved review existed only in memory; the database
transaction was read-only with zero new, dirty or deleted objects. The candidate
composes four localized metadata entries and five caption locales. This is a
technical provenance check, not new audiovisual acceptance.

The approved final's pace/captions/policy findings and sixteen retained picture
warnings remain intact. This source supplement does not repair or waive them.

The one-shot driver restricts requests to this project's review GET, two JSON
PUTs and one POST. It checks frozen canonical/source bytes and current
approvals/choices again, saves
a durable intent before POST and preserves raw response before parsing. An
existing intent permanently forbids another POST. Its fixed receipt directory is
`/var/lib/mokaair/video-work/cloudflare-auto-router-who-measured-savings/review/ops/auto-router-language-schema1-20261007`.

No translation, picture, speech, dub or video generation, settings change,
worker restart, deployment or YouTube operation is included.

The deployed worker predates the new project-lease module. The first launcher
stopped at its missing import, before credentials were read or any API request
was sent. Read-only reconciliation confirmed no submission intent. The adapted
driver uses the proven bounded source/state checks: worker remains done,
no queued/submitted media jobs or queued/running stage jobs, no source drift and
no item lease. These are snapshots, not producer exclusion. No lock module is
installed and no worker is restarted.

## Actual result

The official review POST completed once with HTTP 201 at
2026-10-07 06:48:23.818600Z (14:48 Taiwan time). New language review
`751edf71-c6ff-411a-b691-6b83bf82e34f` is approved under the existing automatic
rule: every selected dub is explicitly skipped, so no ready dub requires owner
Studio confirmation. The old approval was not copied or modified.

Actual-only post-submit verification confirmed all ten stored attachments match
their real SHA-256 and size, including the unchanged 12,607-byte metadata
`08812226aaa49aa6831679d66b9e1d87368e4ae2c5241feaafc853400cdcdf0f`
and 4,003-byte source manifest. The deployed
`read_approved_package(..., verify_files=True)` accepts the persisted approved
batch and composes four localized title/descriptions plus five caption locales.
This final verification uses no hypothetical approval or candidate overlay.

Original final/publish/language review identities, decisions, payloads and
attachments remain intact. Current choices, all three exact skip reasons,
canonical language artifact, metadata, media source bytes and local approvals
remain unchanged. No YouTube ID, schedule, sync or upload session was introduced.
The verification database transaction remained read-only with zero new, dirty
or deleted objects.

The worker-side receipt reader independently verified six durable receipt files,
the HTTP 201 raw response, intent/request binding, exact accepted identity and
readback. The API reader cannot read the worker's private receipt directory;
verification therefore ran in each original container without loosening file
permissions. The fixed namespace now contains a submission intent and must never
be submitted again or bypassed with a new namespace.

Technical provenance repair and resubmission are complete. The native producer
defect remains covered by the separate
`2026-10-07-normal-video-language-submissions-omit-source` follow-up in PR #1363.
This record claims neither audiovisual re-acceptance nor YouTube delivery.

Actual consumer/source verification output SHA-256:
`5e9aad34aaebb4f1b4c4ab018b86c68888ca4fe455da9d9fefb9932f9f5f9d0b`.
Separate durable receipt verification output SHA-256:
`24626f4346beb1e965e15f4d8cc85f9ad6b3aabdd81bd3fa5e8d171283c82b8e`.
