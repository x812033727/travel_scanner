# WAF language source resubmission

Project: `cloudflare-ai-attacks-own-waf-49-findings`.

On 2026-10-04 the owner explicitly requested a new language review because the
approved legacy batch lacks a verifiable source manifest and metadata. The request
authorizes resubmission of existing results, without new speech generation,
approval, deployment, YouTube upload or publication.

The deployed consumer reproduces `409 video_youtube_languages_invalid` for legacy
review `ab622864-79de-4290-bce0-0ed9a3d1d36d`. That batch has four descriptions,
four captions and one English dub. All nine stored files match their canonical
bytes and SHA-256. Japanese and Korean dubs have explicit skip receipts; their
partial tracks must not be attached as completed dubs.

The replacement must retain the original locale choice decision and bind these
current approved sources:

- Final review `6c303f84-c426-4cf4-8c51-4ad27f69b583`, SHA-256
  `47b1c4f40a789b130886318468272d6f8ae97f19507fcd023fe2030f006c0efa`.
- Publish review `6edd7506-a9d1-4758-bd07-5bc44acc8fa4`, SHA-256
  `60a97968b17208a01aecc98e475b983bd79769f7eb28f90fbcf04acf7da05f3a`.
- Existing multilingual metadata SHA-256
  `39df3fa8036b0362367734dc68c5b1b133e3f2dc4ddfda3a8c5ab669a95a026a`.

Schema 1 `languages_manifest` must contain the source identities and hashes,
original choice, exact ready/skipped locales and all ten attachment descriptors
(the original nine plus metadata). Review files additionally contain the manifest,
and the review content hash is the exact manifest byte hash.

Read-only source evidence was sampled through 16:12:03Z. Compact evidence SHA-256:
`31448eff79decb253972d35f6b2e7e8524ac11d75fcb9b3e2da37b0f51a6cad1`.
Full evidence SHA-256:
`1e8a76de4534691edf35be30036dac4b3ec0347d3912a56e9576bd5c6b996150`.
The only language-choice file drift was the worker's `synced_at`; semantic choices
and the original decision time remained identical to the database.

The ordinary producer still builds the legacy manifest. The bounded operational
resubmission must therefore use the existing review API directly, preserve the
canonical legacy manifest and old review, and submit one new content identity.
Validate against deployed consumer bytes first, recheck live source and owner
choices before submission, persist a one-shot receipt before POST, and reconcile
an uncertain response before considering any further action.

The exact packet passed ten backend contract cases, eleven submission and normal
flow cases, and sixteen independent tests using the actual request adapter. These
tests used no real network or paid calls. Complete pending locale state returns
from the normal language flow before package or legacy review-push; the canonical
legacy manifest remains intact.

A fresh read-only production snapshot at 16:33:31-16:33:36Z confirmed the current
owner, original decisions, source identities, nine ReviewStore files and protected
settings. Snapshot SHA-256:
`532167e2908c401228e35714bcc2158b30308a9dd0570faed5d89d17d9a1b857`.

The owner-authorized operation succeeded with two small JSON file PUTs and one
review POST. New review `02095208-b5de-4291-8428-4f92e792fbe5` is pending, with eleven
files and manifest SHA-256
`e22ec95719d3c549a3e81c60eadcd512b5397f74fdb7eb852aecdaa9ed5ccba4`.
The existing tool account performed the operation; no credential was printed or
stored in evidence. POST intent, raw response, acceptance and project readback are
persisted in the fixed directory:
`/var/lib/mokaair/video-work/cloudflare-ai-attacks-own-waf-49-findings/review/ops/waf-language-schema1-20261004`.
An existing intent permanently prohibits another POST from this helper.

The real post-submit API readback and canonical file guards passed. The old approved
review, source and original nine files remain intact. Japanese and Korean retain
their exact skip reasons, and English dub is ready in the pending batch. No speech
generation, owner approval, source change, worker restart or YouTube action occurred.
Final independent read-only verification passed at 16:42:06-16:42:10Z: all eleven
new and nine old ReviewStore attachments match their actual bytes, sizes and
SHA-256. The real consumer correctly refuses the still-pending review with
"latest language package is not approved". A separate transient in-memory copy
passed full source-bound composition with `verify_files=True`; no real approval
or database write occurred. The database session remained clean, and the stored
new review remained pending throughout.

Final evidence SHA-256:
`d1c83bf3ce957ab6cfe769a9a1bba5769f24c271b95dc7a374f7f874f36efc95`.
All five durable receipt files, old decisions, original final, semantic choices,
owner and protected settings remained stable. The source/metadata defect is
resolved for this replacement; the owner must review the new pending batch.
