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

The independent second visual delta binds only the two revised prompts
`x06-b02-s01` and `x06-b02-s02` to video SHA
`d1ac6f93e15396813dda6ac2d76028f6539be2d746d647d1fd44e4790dd5d0c5`.
The source/blind findings and five provisionally usable image takes stay bound
through the exact visual-review chain. A fresh paired-site quota and US$25
all-in ledger check preceded an isolated two-shot pilot capped at three takes
each. The pilot generated three images and three judge calls for US$0.0405;
both selected images passed the model judge (9.29). Initial manual viewing
held both for prompt-level action and object discrepancies; an independent
re-read against the actual narration and curio-episode illustration rule found
neither contradicted a spoken/source fact, showed legible print or logo, or
drifted from cute-mystery. The initial strict gate is preserved as history;
both selected frames are now provisionally usable, making **7/78** in total.
At that stage the main media ledger was
US$0.3780 (28 images, 28 judge calls, zero reservations), while STOP remains.
The prior pilot's manifest, ledger, gate and vulnerable image filenames were
archived under `review/local-preview/v1-pilot-evidence/` before merging the
second pilot. The current gate SHA and per-image reasons are in
`reviews/local-preview-art-gate.md`. No MP4, source-cleared music, final art
approval, official branding assets or Studio end-screen setup exists. Next:
three representative untested visual families in a bounded isolated pilot,
then stop and inspect before considering the remaining 68 frames.

The third isolated pilot tested route symbolism (`x06-b03-s09`), household
carpet care (`x06-b04-s14b`), and a finance-size comparison (`x06-b05-s01`).
Each passed the model judge on take 2 and full-size human inspection under the
series illustration rule, with no legible text, logo, source contradiction or
style drift. Six image and six judge calls added US$0.0810, below the
US$0.1215 pilot ceiling. The current 10/78 selected frames include the exact
prior seven takes unchanged. Main ledger: US$0.4590, 34 image/34 judge calls,
zero reservations. Main STOP remains; any further drawing must use bounded
shot allowlists in an isolated work volume and recheck live quota/budget first.

Two serial isolated 12-shot batches followed without moving main STOP.
Batch 1 spent 17 MiniMax/17 judge calls, US$0.2295, and all 12 selected frames
passed judge and human viewing. Batch 2 spent 21 MiniMax/21 judge calls,
US$0.2835; of its 12 selected frames, 10 are provisionally usable, one
(`x06-b03-s07`) failed all three judge attempts because of a red signature-like
watermark, and one (`x06-b03-s12`) is held on independent full-size inspection
because a shop sign has clear Chinese-like characters despite judge PASS.
All takes and the collision-prone historical files were retained with
SHA-bound gates outside git. The current main ledger is **US$0.9720**
(72 images, 72 judge calls, zero reservations); **32/78** illustrations are
provisionally usable, two are HOLD and 44 are unattempted. Main STOP remains.

A two-prompt v3 proposal at `reviews/visual-v3-offline-proposal.md` changes
only the two HOLD shots, freezing new video SHA
`931efad38297c832fd11a2aedfc12cc2ef5c61373e36632a1fcd916dbdf0fc68`.
The 93-scene non-prompt JSON is deeply equal to the prior version, and lint
reports 0 errors/0 warnings. The independent prompt-only PASS is
`reviews/visual-v3-independent.md` (SHA `5ab635105dc384bbec80b4f32346697247c0ebdcdcff539391674f7b436c84a7`).
A zero-cost bridge to visual hash `1ceea6211d4c482a` verified all 32
previously usable take objects, prompts and original image hashes unchanged;
the two old HOLD entries were archived and removed from the active manifest.
Bridge receipt SHA `14f66c1f9177df1c01b82d72a9d6d88b175e80d385c9e52dddbf2a7e4669dbd2`;
current manifest SHA `66e2f7a1d0fbbd28fc1b9392c06bd8511a96aa328db21b98b1722b37173a9d03`,
current STOP gate SHA `8c0dcc76b7b48ceabc96a19636784f22f986ce933ef6f2e194a0abcf5c4e8e0f`.
The ledger remains unchanged at US$0.9720, 72 image/72 judge calls, zero
reservations. Site music quota
remains zero; a matching owner-generated X03 Lyria track passed provenance
checks and was copied only into `review/local-preview/` for a labeled local
concept reuse, not official music approval. Its source and copied MP3 SHA are
`452887ff91f0f6956d350b9c902cc273b82cc3c1fdae9a7524e330ddcda7b2de`;
the concept sidecar SHA is
`12bcc14a6a23355660832acde3005fba51f31553131b773379188c581a817805`.
No X06 music quota or new fee was used; official `music/manifest.json` is absent.
After batch 2, live judge quota was 342; X06 worst-case remaining demand is
132 for 44 new shots plus up to 6 for reviewed HOLD retries. X09 needs at least
99 calls and X05 also uses the same site, so X06 paid stage stays paused until
cross-episode capacity is established. X05 reported 300 remaining site judge
calls at 19:40 UTC and will cap its next use near 63, preserving X06's 138
worst-case calls and X09's 99. Check quota afresh before each isolated batch.
No MP4 or Studio link exists.

The v3 two-shot retry used exactly three MiniMax images and three judge calls
for US$0.0405. `x06-b03-s07` take 2 is provisionally usable at SHA
`34497aa6adbf808f7b5818d94fea011904121f97710e2bc31511f5f79266abc9`;
the independent full-size read agreed the unlabeled Y-track graphic neither
contradicts narration nor contains text, logo or watermark. `x06-b03-s12`
take 1 passed the judge but remains HOLD at SHA
`e87f305702162306a9f2c7e59219603cf4008edbc035d48e20d8c677c29cb5c0`:
two childlike figures and a full-size counter imply an actual sale instead
of the company's future plan. Main ledger is US$1.0125 (75 image/75 judge,
no reservations), 33/78 frames provisionally usable, one HOLD, 44 untried;
main STOP remains. The old held files, new take evidence and bounded merge
receipt are in the media workdir, with exact hashes in
`reviews/local-preview-art-gate.md`. A new prompt-only review is required
before reattempting the held shot. A serial isolated 12-shot batch of
untried scenes then stopped at the first safe boundary because two of its
first three selected scenes each failed all three judge takes on incorrect
people, props or actions. The fourth scene had one paid image but no judge
call or manifest selection when STOP was seen; its original file and
US$0.0035 cost are preserved. That batch spent 8 images/7 judge calls,
US$0.0980, and only `x06-b03-s15b` passed both judge and full-size human
viewing; the independent read also agreed. Main ledger is now **US$1.1105**
(83 images, 82 judge calls, zero reservations), 34/78 provisional usable,
3 HOLD (`s12`, `s16`, `s02`) and 41 unattempted. Main STOP remains. Exact
media receipt, selected-file hashes and cost evidence are in
`reviews/local-preview-art-gate.md`. The site judge quota was 246 after
the stop: X06's remaining worst case 132 plus X09's 99 leaves only 15
headroom, so no broader paid art batch is warranted without a reviewed
prompt strategy and renewed shared quota plan.

An **offline-only** three-HOLD prompt proposal is at
`reviews/visual-v4-offline-proposal.md` (SHA
`b697f096e66f2e82eda849ea16166049dc66443aba26346f6554e070212d9219`).
It replaces the false in-store sale, extra people/sack, and shopper/packet
failures with unlabeled planning or category-object comparisons. The old
prompts and narration were checked byte-for-byte against the unchanged v3
script; no new video SHA, manifest bridge or image generation has occurred.
It awaits independent source/visual review before any script edit.

The independent **offline-proposal** review has since passed at
`reviews/visual-v4-independent.md` (SHA
`58569e6d6377a24c45d2aadb12c8bef676d3473eb254ea3d105e0779a08e6beb`).
Exactly those three reviewed prompts were applied; `video.json` is now SHA
`acfeb244c3d67578223516a749617c89b2dad8f3df28766f85bae4e6f460ccb4`.
Deep comparison found no other field change, and lint has 0 errors/warnings.
A zero-cost bridge retained all 34 unchanged provisionally usable takes and
their file hashes, retired the three old HOLD selections to evidence, and
preserved the US$1.1105 ledger plus unjudged paid image. New visual hash
`2f613d75fac3591d`, manifest SHA
`39635fc22fc2dec9b71e736fc61137d0f50c22baff1adbcac127a821e5488080`,
STOP gate SHA `c48c604145128b5b98bb02ba9d3a5b2ba31ab6f478a2aba9541e9b248d6b7b5d`,
and bridge receipt SHA
`fc0054acbb4ac8f95dee244c0d6b3191fda77772383171b778b49bb7d9075ae8`.
The v4 **post-apply** independent review is still pending. No new image,
judge call, audio change or paid transaction occurred under this SHA; both
main STOP and the cross-episode quota hold remain.
