---
id: 2026-10-20-build-wd-40-x06-local-concept
title: Build WD-40 X06 local concept preview
status: in-progress
priority: P1
area: docs
owner: codex-x06-media
claimed_at: 2026-10-20T17:53:00Z
created_at: 2026-10-20T17:52:57Z
completed_at:
branch: codex/brand-story-wd40-x06
depends_on: []
scope:
  - docs/videos/story-everyday-wd40-x06
---

# Build WD-40 X06 local concept preview

## Why

X06 has a source-checked, blind-reviewed six-chapter script and a pinned story
pronunciation snapshot, but no Sulafat audio, MiniMax illustrations, measured
body duration, captions, music, or local preview. The site can accept paired
media commands, while the selected official 5-second intro and 21-second outro
and YouTube Studio end-screen access are not present in this workspace. A clearly
labeled concept preview is the next reviewable video deliverable.

## Definition of done

- [x] Actual Sulafat audio measures at least eight minutes of substantive body:
      hook 46.000 s, substantive body 523.333 s, native closing 14.533 s
      after a bounded 11-line retake (20 October 2026). The body excludes the hook,
      native closing, and any concept bookends.
- [ ] A local MP4 preview with the required chapter order, 5-second concept
      intro, 21-second concept outro, optional CC, sourced cards, and reviewed
      MiniMax image-01 illustrations is available outside git.
- [ ] An exact-hash media/QA and cost report shows all-in spending within US$25,
      and PR #1623 links the accurate local delivery without calling it an
      official release or claiming clickable Studio links.

## Steps

- [x] Run pinned Sulafat TTS and audio QA serially; 95/95 lines checked. The
      latest check flags 23 lines for human listening, so this is not an
      approved narration. A single 11-line retake cleared one flag and made
      several critical phrases clearer; no unrestricted retake loop.
- [ ] Check all-in quote and generate up to three MiniMax takes per shot.
- [ ] Render cards, add provenance-checked concept music, compose CC and cut.
- [ ] Watch/measure the export, update delivery notes and PR, run touched checks.

## How to verify

Use `--workdir /workspace/.brand-video-workdir` for every CLI media command and
paired home `/workspace/.video-tool-home` without exposing the token. Check
`media-status` and the local ledger between paid stages. `ffprobe` the output;
inspect real TTS scene/chapter times and the keyframe manifest. Run repository
video lint and `npm run test:docs-videos`; keep the MP4 and audio outside git.

## Notes

The X06 `video.json` SHA reviewed by source and both blind readers is
`4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba`.
The reviewed pronunciation snapshot has SHA
`3b4da9b2e82c5a69ca31c1f5af5832530bcf0cc02434c53da2b4458c606e9fc7`.
Its TTS dry-run listed 95 Sulafat requests/2,337 characters in the free tier.
The actual 95-request TTS run completed on 20 October 2026, followed by one
bounded 11-line retake (290 additional free-tier characters). The current
`timeline.json` SHA-256 is
`ed4302c6b986a0a6da9a773e74a084cbfe0d1c9711ac6c158cdf1d92a73f65b0`;
`narration.wav` SHA-256 is
`fdc9c4b490e8502df30fa733974ca01e8cfb6efd45970030c7d134e66494168a`.
`review/check.json` SHA-256 is
`89a3b8308229d4cf4fd5f1fd2838e949cc02af8b42f8a4b3a16c91935b`;
`review/check-flags.json` SHA-256 is
`32f3c4b03f9f03edee3bda9c6d3c60c5e6c640ffec23680967cb7cf50aa20822`.
X05 is a separate active slug; the site's monthly new-music quota is exhausted,
so a concept preview may reuse a provenance-checked already generated track
only if its terms and prompt are compatible. Never claim this is the official
selected channel music/animation.

The first X06 art gate stopped on 20 October after 21 MiniMax takes and 21
judge calls (US$0.2835, no pending reservations). The 12 selected slots include
11 machine passes but only 4/12 are provisionally usable on human inspection;
8 are held out of any preview. The unchanged originals, manifest and ledger
are archived outside git. See `reviews/local-preview-art-gate.md` for the
exact failure list and hashes. Rewrite the full set of high-risk visual prompts,
renew exact-hash review binding where needed, then test 2–3 difficult scenes
before any larger paid batch. The workdir STOP remains in place.

An independently signed prompt-only source/narrative delta binds the revised
`video.json` SHA `907f8e3ff45f3edf0bbed64a54216c761696e8e954d51c315a8a228069e204d1`.
The three-shot isolated pilot reused four unchanged takes and generated four
new images/judgments for US$0.0540. All three selected takes passed the model
judge, but human inspection holds `x06-b02-s01` (spray can became a shipping
drum) and `x06-b02-s02` (hinge became a rod with a printed background panel).
Only `x06-b02-s06` is provisionally usable. The merged main ledger is
US$0.3375 (25 images, 25 judge calls, zero reservations), and the main STOP
never moved. See `reviews/local-preview-art-gate.md`; next work is an offline
prompt strategy before any more paid generation.
