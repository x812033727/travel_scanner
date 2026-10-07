# Approved language packages for YouTube

Implementation status: the API and VPS consume the contract below, and
`review-push --gate languages` produces it for every video (a renewed final through
`tools/video/review/renewal.mjs`, any other through `bindLanguageSource` in
`tools/video/review/sync.mjs`). A contract test feeds the producer's actual bytes to
the consumer (see "Producer" below). Language reviews sent before this change carry
no manifest and still need resubmitting; that is a release action, not automatic.

An upload confirmation can be approved before the owner chooses additional
languages. The API and independent VPS uploader must compose that confirmation
with the current approved language review, rather than send the old confirmation
alone and report a successful original-language upload.

## Review contract

The language producer submits two JSON attachments in addition to the chosen
description, caption and dub files:

- `metadata`: the actual upload metadata containing translated titles and descriptions.
- `languages_manifest`: a versioned manifest whose bytes SHA-256 is the language
  review's `content_sha256`.

Version 1 contains `schema_version`, `slug`, `source`, `choice`, `locales` and
`files`. `source` records the server review IDs and content hashes for the
approved `publish` and `final` reviews, and the applicable `script` review. It
also records branding, speech and compilation hashes where applicable. The
producer validates the current local artifacts before submission. Final and
script review identities, the final video hash and branding are independently
checked by the consumer against the approved source.

A manifest may also carry `follows`, the identity of the newest language review when
it was sent. The producer adds it only when the same bytes were already sent as an
older review (an owner who returns to an earlier choice): the server answers repeated
bytes with that older review, while the consumer reads the newest one. The consumer
does not read it.

`choice.locales` contains the complete normalized metadata/captions/dub choice.
`choice.decided_at` is an audit timestamp, not a choice revision: the site keeps
the first decision time even when the owner later changes the selected parts.
`locales` retains the per-part ready or explicitly skipped states used by the
review page. `files` lists the exact role, SHA-256, byte size and content type of
every attached metadata, description, caption and dub file. It excludes the
manifest itself to avoid a circular hash.

## Producer

`review-push --gate languages` sends the parts that are made, then binds the batch
before posting it: it uploads the current `upload/metadata.json` as `metadata`, writes
the manifest to `review/languages.json` (the file `review-pull` records the approval
against) and uploads it as `languages_manifest`, whose hash becomes the review's
content hash. `source` names the site's newest final, which must be approved; the
newest upload confirmation, approved or still pending (a pending one that the owner
then approves unchanged carries the batch; a newer confirmation sent after it is read
without the batch, from its own package); and, for a drama that is not a compilation,
the newest screenplay review, which must be approved. `speech_hash` and
`compilation_hash` come from `timeline.json`, and `branding_hash` from the approved
final.

Nothing is posted while the batch cannot be bound. The producer refuses when there is
no confirmation yet or it was rejected, when the final or screenplay is not approved,
when `metadata.json` was written for another final, branding or choice, when the
choice on the site is not the one copied into `languages.json`, when a description
file is not its title and description in `metadata.json`, or when the narration's own
captions differ from the approved confirmation's. A selected dub of the narration's
own language goes as an explicit skip; no duplicate track is sent.

`tools/video/review/language-contract.mjs` runs the real `package` and `review-push`
on fixture videos against a double of the review site. It keeps what the site then
holds in `apps/api/tests/fixtures/video_language_contract/`, and
`apps/api/tests/test_video_youtube_language_contract.py` feeds that through the real
consumer, with file verification. `tools/video/review/language-contract.test.mjs`
fails while the committed copy is not what the producer emits; it writes the copy
again when run with `LANGUAGE_CONTRACT_WRITE=1`.

## Consumption and retries

The original confirmation continues to supply the video, thumbnail, default
language content and upload settings. The language batch supplies only the
selected translated titles/descriptions and captions. Both approval identities,
the choice and attachment contents are checked before composing a package.

API requests pin the complete approval identity. Queued runs and retries must
refuse changed approvals or choices before writing to YouTube. VPS jobs use the
composed package hash, so a newer language batch cannot be mistaken for the
already staged or completed original-language package. Progress remains readable
when an old job no longer matches the current approved package.

Original-language uploads and existing complete publish packages remain supported.
A separate legacy language review without source identities and a hash-bound
manifest requires resubmission; filenames or an unapproved current metadata file
cannot establish which approved video a translation belongs to.

A review with a ready dub still requires owner approval. The pending-dub first
private upload sequence is tracked in
`tasks/open/2026-09-30-clarify-first-upload-of-pending-dubbed.md`; the uploader
does not bypass that approval on the strength of a ready UI status.

## Release and acceptance

The regression tests use real review-store files and SQLite review records with
fake YouTube and VPS HTTP boundaries. They establish package selection, approval
and hash validation, version pinning and caption forwarding. They do not establish
Google login, production deployment, Studio persistence, audio-track availability
or owner playback acceptance.

Deploying this change and resubmitting any existing legacy language reviews are
separate release actions. Existing public-video protections and scheduling rules
continue to apply; this change does not automatically backfill published videos.
