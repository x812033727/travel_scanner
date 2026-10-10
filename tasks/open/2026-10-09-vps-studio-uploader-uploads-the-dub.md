---
id: 2026-10-09-vps-studio-uploader-uploads-the-dub
title: VPS Studio uploader uploads the dub tracks after the video
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-09T14:49:23Z
completed_at:
branch:
depends_on:
  - 2026-09-28-vps-youtube-studio-deployment-and-live
scope:
  - services/youtube-uploader
  - apps/api/app/video_youtube/vps.py
  - docs/videos/VPS-UPLOADER.md
  - docs/videos/DUBS.md
---

# VPS Studio uploader uploads the dub tracks after the video

## Why

On 2026-10-09 the owner learned that the sixteen dub tracks they had "approved" were never
on YouTube (they thought the button uploaded them) and asked that from now on the dubs go
up with the video: 「也要幫我修之後的也會一起傳」.

The Data API has no audio track method (DUBS.md, checked 2026-09-27), so the site's
`youtube-sync` cannot do it and the owner's hand upload in Studio is today's only path.
The one thing in the repository that can press Studio's buttons is the VPS uploader
(`services/youtube-uploader`, docs/videos/VPS-UPLOADER.md), a Playwright operator that
already knows the steps `final`, `thumbnail`, `captions_<locale>` and
`localizations_<locale>` (`studio.mjs` `step()`). It is not deployed, not logged in and
has never uploaded a real video; its live acceptance is `2026-09-28-vps-youtube-studio-deployment-and-live`,
and this ticket waits for it.

## Definition of done

- [ ] The approved language package the API hands the uploader (`vps.py`, the
      `captions_<locale>` entries) also carries `dub_<locale>` files for every ready dub,
      with their sha256 from the review.
- [ ] `studio.mjs` has a `dub_<locale>` step: Studio left menu「語言」→ this video →「新增語言」→
      the locale →「配音」→「新增」→ set the file →「發布」, idempotent on a re-run (a language
      row that already has a dub is skipped, not duplicated), and an unexpected page pauses
      the job with a screenshot as the other steps do.
- [ ] The `languages` review that carries a dub is approved by the uploader's receipt
      (track placed, with the Studio language row as evidence), and no longer by the owner's
      button; the button stays for the hand path and reads as the owner's statement
      (`2026-10-09-languages-card-says-the-site-cannot`).
- [ ] Acceptance on one private video with one locale first, then the three locales of
      a public video the owner names, recorded in VPS-UPLOADER.md with versions and the
      Studio behaviour that DUBS.md left untested: whether Studio accepts `.m4a` (else
      `--format mp3`), whether a private video takes a track, whether the track's「發布」
      touches the video's privacy.
- [ ] DUBS.md §站主要做的事 says the owner's two one-time settings (Advanced features on,
      automatic dubbing off) are still theirs, and that the per-video upload is the
      uploader's when the service is live.

## Steps

- [ ] Wait for the live acceptance ticket; do not touch production before it.
- [ ] Extend the package in `vps.py` and the uploader's asset naming (`asset()` in
      `studio.mjs` maps roles to extensions; add `dub_` → `.m4a`/`.mp3`/`.wav` by content type).
- [ ] Observe the live「語言」page once, write the selectors from the observation, add a
      sanitized fixture, then the step.
- [ ] Wire the receipt to the review approval in `apps/api` (a separate api-area ticket if
      the scope grows beyond `vps.py`).

## How to verify

Service tests, `apps/api` tests for `vps.py`, then the two acceptance uploads above; a
public watch page of the accepted video lists the locales under
`ytInitialPlayerResponse.streamingData.adaptiveFormats[].audioTrack`.

## Notes

- YouTube's terms require written permission for automated access; VPS-UPLOADER.md
  already says the operator must settle this before enabling the service. A dub step does
  not change that question, it only adds one more thing the operator does.
- Until this lands, the owner uploads by hand from the card; the card now says so.
- 2026-10-10: the code half is merged as #1414 and deployed (1bd1d47ce): the approved pack
  carries `dub_<locale>` assets and the uploader has the step, tested against the synthetic
  Studio (selectors `dubCell`, `dubFile` provisional). The Data API still has no audio track
  resource (discovery revision 20261006). Open for: the live acceptance, the receipt
  approving the languages review (`vps.py` `action()` "record"; `compose()` only releases an
  approved batch, so the button's meaning has to change with it), a label for the step in
  `admin-video-vps-upload.tsx`, and whether already-public videos may be opened.
