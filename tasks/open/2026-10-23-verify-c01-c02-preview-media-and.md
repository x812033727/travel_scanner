---
id: 2026-10-23-verify-c01-c02-preview-media-and
title: Verify C01/C02 preview media and complete outstanding QA
status: blocked
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T01:04:38Z
created_at: 2026-10-23T12:27:00Z
completed_at:
branch: codex/c01-c02-preview-media-inventory-20261024
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020/reviews/c01-c02-preview-media-and-qa-20261023.md
---

# Verify C01/C02 preview media and complete outstanding QA

## Why

PR #1610's C01 Crocs and C02 Tupperware text production packages are preserved
on main, but the non-Git previews and paid source media were recorded under
older `/workspace/` paths. This Windows checkout cannot yet read those media
paths. C01's automatic audio check and C02's local preview do not establish
formal worker, brand, owner playback or final-video acceptance. C02 still has
ten audio flags, including c020901, c021504 and c021904 that may alter meaning.
The old PR carried two open QA tasks that are not on the main task board;
this task preserves those obligations before the superseded PR is closed.

## Definition of done

- [x] Read-only existence, size and SHA-256 checks locate or explicitly mark
      missing/unverified each C01/C02 preview, subtitle, thumbnail and source
      asset named in their `local-preview.md` and handoff files. Record source,
      durable backup location and readback evidence in the scoped receipt.
- [ ] Independently listen to C02's ten flagged lines, starting with c020901,
      c021504 and c021904; distinguish TTS error from ASR error. Propose only
      evidence-backed line retakes, followed by subtitle/source recheck.
- [x] Record C01's outstanding formal worker, brand and owner playback review,
      including the 5 s / 21 s brand choices. Distinguish local preview,
      formal QA, `final.mp4`, backend plan/script intake, upload and publication.
- [ ] If media must move to durable storage, copy, verify hashes/readback and
      write the receipt before considering any source deletion. Preserve paid
      takes and the original files.

## Steps

- [x] Start with main's C01/C02 `local-preview.md`, C02 `reviews/audio-check.md`
      and both `publishing-handoff.md` files; verify original storage without
      treating a prior document's assertion as current file existence.
- [ ] For found files, run `Get-FileHash`, `ffprobe` and a complete local decode
      where applicable; note exact expected-versus-actual hashes and sizes.
- [ ] Listen to the original flagged audio and retain only confirmed defects.
- [x] Write the scoped receipt and run `npm run check:tasks` and docs hygiene.

## How to verify

Read the actual media and compare SHA-256; keep C01/C02 absent from approved
script intake until they pass their separate owner/review gate. Do not buy
voice, images or music, import a formal worker project, upload or publish from
this evidence task. Any paid retake follows the existing per-film approval and
budget gates.

## Notes

2026-10-23 read-only inventory: expected Windows folders
`<home>/mokaair-work/videos/story-everyday-crocs-c01` and
`<home>/mokaair-work/videos/story-everyday-tupperware-c02` were absent. The
older `/workspace/.brand-video-workdir/...` and
`/workspace/brand-story-preview/tupperware-c02/...` were not readable from this
checkout; their current existence is unverified. Recorded preview baselines:
C01 MP4 SHA-256 `5ba761f9cb0b68cdaa96da4855b6c66e35cb0414f57c26a49a15bb1f1b432322`
(about 189 MiB, 19,553 frames); C02 MP4 SHA-256
`f146606206290086cec6215f46250bf0cbaf6ec3e3795950deac1e82eaa1f9da`
(163,204,884 bytes, 19,169 frames); C02 thumbnail
`f63c6de3797e381ec8e7235261c8ea685e01ef463975e61177160e14f63655d4`,
SRT `90c91afa9e983bb954f1e547150b1965b529acf764ba23747590e3db528fdb34`,
VTT `4207c52d32f9141d7480f95bd4767dff1c462751e579e24a4284d6175ca4ed0a`.
These are earlier recorded hashes to verify, not proof of present media. C01
and C02 were not included among the ten approved/backend script cards.

2026-10-24 read-only update: the scoped
`reviews/c01-c02-preview-media-and-qa-20261023.md` records exact negative
Windows/G: and `hostinger2` path checks, historical hashes and the inability
to renew hash, decode or listening evidence without source bytes. The original
cloud `/workspace` is a different environment and remains unverified. No media
was moved or deleted. C02's ten WAV flags and both formal final-film gates
remain open. The owner has been asked for the original cloud workspace or a
named verified backup; this task must remain blocked until media can be read.
`npm run check:tasks` and `git diff --check` passed. `npm run
test:docs-videos` ran 235/236 tests green; the pre-existing Windows child-Node
failure at `docs/videos/imported-long-languages/runner.test.mjs:679` again
exited 3221226505 with no stderr. This receipt does not touch that runner.
