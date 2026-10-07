---
id: 2026-10-07-imported-long-videos-language-batches-carry
title: Imported long videos' language batches carry no source proof
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T08:03:28Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/imported-long-languages/runner.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal-handoff.test.mjs
---

# Imported long videos' language batches carry no source proof

## Why

YouTube sync takes a language batch only with a `metadata` attachment and a `languages_manifest`
whose hash is the review's content hash (docs/videos/APPROVED-LANGUAGE-PACKAGE.md). Two paths for
imported long videos do not meet that:

- `docs/videos/imported-long-languages/runner.mjs` `submitSnapshot()`, for a video that is not a
  renewal, posts its own `{schema_version: 1, provenance, locales_decided_at, locales, files}`
  manifest (saved as `language-package/<sha>.json`), with neither attachment. The consumer
  refuses it: "舊語言審核缺少可驗證的來源清單與 metadata，請重新送審".
- `tools/video/review/renewal-handoff.mjs` `bindManualLanguageSubmission()` (a manual-import
  renewal) writes its manifest to `language-package/renewed-languages-manifest.json` but never to
  `review/languages.json`, which `review-pull` and the worker's `pulled()` check the approval
  against; reached through `review-push`, the file keeps `languagesSubmission`'s own bytes, so no
  site review matches it and the approval is never recorded, without a word.

## Definition of done

- [ ] An imported video's language batch, renewal or not, is accepted by the real consumer
      (`read_approved_package` with files verified).
- [ ] An approved manual-import language batch is recorded by `review-pull`.

## Steps

- [ ] Wait for, or rebase on, PR #1359 (it rewrites `runner.mjs` `submitSnapshot()`).
- [ ] Bind the runner's non-renewal batch the way `bindLanguageSource` in
      `tools/video/review/sync.mjs` does (or call it), and write the manual-import manifest to
      `review/languages.json` as `bindRenewalSubmission` does.
- [ ] Add a case to `tools/video/review/language-contract.mjs` so the API contract test reads it.

## How to verify

`node --test docs/videos/imported-long-languages/runner.test.mjs tools/video/review/renewal-handoff.test.mjs`
and `cd apps/api && uv run pytest tests/test_video_youtube_language_contract.py`.

## Notes

- Found while binding normal batches to their source (claude-opus-5-5-happy-carson, PR #1361).
