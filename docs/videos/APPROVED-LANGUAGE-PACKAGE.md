# Approved language packages for YouTube

Implementation status: API/VPS consumption and regression coverage are implemented.
The producer patch is prepared separately and awaits permission to edit the two
paths held by an older task. This draft must not be deployed before that contract
is integrated and verified; see the open approved-languages-sync task.

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

`choice.locales` contains the complete normalized metadata/captions/dub choice.
`choice.decided_at` is an audit timestamp, not a choice revision: the site keeps
the first decision time even when the owner later changes the selected parts.
`locales` retains the per-part ready or explicitly skipped states used by the
review page. `files` lists the exact role, SHA-256, byte size and content type of
every attached metadata, description, caption and dub file. It excludes the
manifest itself to avoid a circular hash.

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
