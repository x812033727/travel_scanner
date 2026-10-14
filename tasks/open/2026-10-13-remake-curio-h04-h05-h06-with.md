---
id: 2026-10-13-remake-curio-h04-h05-h06-with
title: Remake Curio H04 H05 H06 with the current narrative video workflow
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-curio-remake
claimed_at: 2026-10-13T17:06:56Z
created_at: 2026-10-13T17:06:49Z
completed_at:
branch: codex/curio-h04-h06-v2-20261014
depends_on: []
scope:
  - docs/videos/curio-h04-v2
  - docs/videos/curio-h05-v2
  - docs/videos/curio-h06-v2
---

# Remake Curio H04 H05 H06 with the current narrative video workflow

## Why

The existing H04 and H06 cuts follow the earlier chapter-by-chapter Curio format;
H05 is still in narration and pilot images. The owner requested all three to be
made again under the 2026-10-13/14 narrated-video workflow: one continuous
evidence-bound story, a scene-first condensation with paid-off hooks, the current
channel bookends, and fresh media and review evidence. Preserve the original
cuts, receipts, draft PRs and H05's unfinished work.

## Definition of done

- [x] H04-v2, H05-v2 and H06-v2 each have a separately checked complete zh-TW
      script, source records, `loops` and a passing blind narrative review
      bound to their latest visual/story structure.
- [ ] Each new slug has checked narration, source-bound artwork, current branding,
      8+ minutes of body, synchronized zh-TW CC and a newly QA-checked full MP4.
- [ ] Each new upload package and backend review binds the new hashes. Keep
      owner playback and Studio upload/publication as separate recorded gates.

## Steps

- [x] Audit origin/main workflow, H04-H06 source branches/workdirs and active
      ownership; create isolated v2 scope and claim it.
- [x] Rewrite and independently check the three scripts, then run lint and the
      blind `narrative` gate before further paid speech. All three have
      historical 11/11 results; later visual edits require renewed checks.
- [x] Inspect old backend projects and resolve their superseded status before
      registering new slugs; keep old approvals and media intact. The v2 slugs
      are independent, so destructive abandonment of old H05/H06 is unnecessary.
- [ ] Build and review new audio, illustrations, edit, captions, QA and packages
      one episode at a time with persisted receipts and readback.

## How to verify

For each slug: `node tools/video/cli.mjs lint --slug <slug>`;
`node tools/video/cli.mjs narrative --slug <slug>` with independently supplied
answers; `status`, `check-audio`, `qa`, `package`, and review/backend readback
against the exact new file hashes. Confirm new MP4 playback and CC separately.
Run `npm run test:docs-videos` and `npm run check:tasks` for repository changes.

## Notes

New worktree: `codex/curio-h04-h06-v2-20261014` from origin/main
`7d22aba63`. Old draft PRs #1460/#1470/#1476 and their workdirs are outside
scope. H04/H06 historical cuts were approved; H04's local package did not record
its later private upload, while H06 was not uploaded. H05
had six audio flags and three pilot images, with three uncommitted source edits
in its existing worktree. Current local branding is
`mokaair-brand-package-v4-endscreen` (`416c8768...`), 150-frame intro and
630-frame outro. New slugs/workdirs keep the old state intact.

Live `/admin/videos` readback on 2026-10-14: H04 old cut was privately
uploaded and linked to YouTube as `9Kqll3q6riE`. H05 has only outline approval,
no worker or upload. H06 has an approved old package and no upload. H05/H06
show a `放棄` control; the UI says it irreversibly clears pending review items
and previews. Neither old project has been abandoned. H04 has no abandon
control after upload.

H04-v2 outline A was submitted to `/admin/videos`; Jev preferred A but did not
auto-approve because its demonstration score was below the configured gate.
The owner explicitly chose A in this task. The production review now records
"已核准 · 選了選項 A" (2026-10-14 01:38 Asia/Taipei), and local
`review-pull --gate outline` records that choice. The old H04 final file remains
at `<home>/mokaair-work/videos/curio-h04/final.mp4` (SHA-256
`262b2018a767cd7c1bdee9ff51cd54534e14e4199ec169ca9eb2b9a203ea3d86`);
old H06 final remains at `<home>/mokaair-work/videos/curio-h06/final.mp4`
(SHA-256 `9a34efba5583956e76ad184aad244b991040d3eb31432f0e9e1528e6a941d8d3`).
H04-v2 outline A and current narration are approved. After bounded wording and
cadence repairs, the exact current narrative hash `e9062e4ca246f5d0` passed
11/11 blind questions. TTS measures 8:40; `check-audio` checked 100/100 lines
with zero flags, and backend audio autoapproval was pulled into the local gate.
The synthesized timeline has no >8-second picture states and 54.07% shot time.
H04's image attempts, including two further three-shot pilots and one failed
object study, generated 208 MiniMax images and 206 judge calls in total (about
US$2.78). The third three-shot pilot
has 0/3 frames that pass both judge and human inspection: a red signature on
the tent scene, crevasses instead of old boot-track remnants, and a photoreal
backpack instead of the stated 2D drawing. The subsequent felt-boot study was
also rejected as photographic and replaced by an original, expressly
illustrative SVG diagram. The current 49-shot source-first hybrid plan has
51.2945% shot time and a 7.5-second longest visual state on the actual audio
timeline. Its narrative hash is `461d52806a07de55`; fresh blind review is
pending. The owner raised the monthly judge
limit to 11,000; although the backend later displayed a higher site setting,
this task retains the owner-approved 11,000-call ceiling. The owner manually
removed H04's STOP; its exact path was read back absent. Partial diagram/card
rendering exists, but no approved full storyboard, full render, captions,
final MP4 or package exists.
H05/H06 old backend abandon would clear old reviews/previews; their independent
v2 slugs were registered without abandoning the old projects.

All three have historical independent blind passes and source-bound claim
records. H06's `349cf912c147f530` and H05's
`e0d2eb7016aea429` scripts each passed 11/11 before later visual revisions;
the new narrative hashes need fresh reviews. H04 lint has 0 errors
and three topic-frequency warnings; H05/H06 latest lint has 0 errors and 0
warnings. H05 outline A is approved and 8:55.8 of narration is synthesized.
Its initial `speech/transcribe` call returned HTTP 504; after provider-usage
review, the owner authorized one retry. The journal is no longer held and
`check-audio` checked 108/108 lines. Local Whisper cleared 10 of the 22
original flags; bounded TTS corrections of three lines left 12 flagged lines
on the exact current audio. The owner listened and approved that H05 audio
in `/admin/videos`; `review-pull` and `status` read back narration approved
before the later visual cadence edit. Three successive three-shot image
pilots exposed childlike proportions, incorrect counter/ticket relations,
fake text, extra objects and inconsistent photographic versus 2D style.
None provides an accepted generated opening. An isolated 15.2-second
source-card/FBI ticket-photo opening was rendered and inspected, then adopted
in the main visual plan. The former 8.2-second single-state outro was changed
to real same-scene reveals; all 108 audio files and line timings remain the
same, but the rebuilt `timeline.json` changes SHA and makes backend audio
approval stale. Its latest narrative hash needs renewed independent review.
H06 outline A was chosen by
the owner and pulled back from the backend. After bounded rerecording, its
current 104-line timeline measures 8:20.93. The formal check examined all
104 lines and retained eight transcription flags; the owner listened and
approved that exact audio, confirmed by `review-pull` and `status` before the
later visual cadence edit. H06's
first three-shot pilot produced two photographic frames that failed the 2D
storyboard judge and one accepted illustrated hospital frame. A single canal
retry passed the judge but failed human/source review for an invented
pre-rescue pose; the next prompt depicts an empty canal and has not been
purchased. H06 fixed two over-eight-second visual states with true card
reveals while retaining all 104 audio files and line timings; its rebuilt
timeline also makes backend audio approval stale, and its new narrative hash
needs renewed review. H05/H06 still
have no approved full storyboard. No v2 final MP4, captions or upload
package exists yet.

Before another paid image call, all three `image-01` prompt sets were audited
for the series rule that `look.negative` stays empty and visible composition
is described positively. The older H04/H05/H06 dry-runs passed for 52/65/51
shots; the newer hybrid plans have 49/62/51 shots and need current-hash
preflight before further image work. These are plans, not inspected or approved
image frames. The inspected three-shot
pilots were `opening-question,trail-search-start,journey-pack` for H04,
`open-counter,open-ticket,open-aisle` for H05, and
`hook-canal-rail,hook-canal-rail-beat-2,hook-hospital-door` for H06.
H04 has source-card/diagram preflight but must prove the remaining generated
style in a bounded pilot; old judge passes cannot be carried forward. The
owner manually removed
both H04 and H06 STOP files, and both exact paths were independently read
back absent. Visual production is now limited by pilot quality.

Draft PR #1484 contains the prior independently reviewed scripts, source
records and asset provenance; the unpushed visual edits need renewed reviews.
Its first CI run passed `test:docs-videos` but
failed `test:tools` because new prose leaked absolute local user paths. The
paths were replaced with `<home>` placeholders and the focused
`repo-hygiene.test.mjs` passes 3/3 locally. All 21 Linux CI checks on pushed
`556c97e7866ecaa046382b00a5f28f44bcd48f88` passed; later edits need
another run.

Local checks on 2026-10-14: `npm run check:tasks` passed (existing stale-claim
warnings elsewhere). `npm run test:docs-videos` ran 215 tests: 214 pass, one
unrelated Windows child-process crash in
`imported-long-languages/runner.test.mjs` (`package-runtime.mjs` exits
3221226505 with no output). The exact single test fails the same way in the
untouched `a8cd` checkout and this new worktree; it is not a v2 document
regression. The Linux PR checks passed at `556c97e`; new edits need recheck.

2026-10-14 current checkpoint: all three current scripts now have exact-hash
11/11 blind passes and approved zh-TW narration. H04's owner-directed search
case-file/callback revision is narrative hash `bd49404ff2771d33`, timeline
SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71`;
100/100 audio lines checked with zero flags and backend approval read back.
H04 actual audio is 8:47.57; 49 planned shots occupy 50.3128% and its longest
visual state is 7.7 seconds. H05 narrative hash `65c64491d8a53b77` and H06
`02a39e4e1fb460a7` also have fresh passes with current-timeline audio
approvals; their visual coverage/cadence checks are recorded in each v2 doc.
The owner chose to retain MiniMax and do offline visual planning only after
the pilots repeatedly failed style/source review. H04/H05/H06 visual audits
cover their planned 49/62/51 shots, with no new paid images in this revision.
None has an accepted complete storyboard, rendered final video, CC, upload
package, owner playback approval or Studio upload. This ticket remains open.
H06's prompt-only MiniMax repair has current `video.json` SHA-256
`52e29bceaa443ce740ba0db5ff9eb64cca27613340828f813c56dcee00d2607a`;
all 51 shot prompts passed dry-run, lint is 0/0, and its narrative/audio hashes
and approval remained current. The rejected canal image still sits at the
thumbnail reference and must not be used. Paid images remain on owner hold.

2026-10-14 subsequent checkpoint: the owner lifted the offline-only image
restriction **for one MiniMax pilot image per episode**. Exactly one image and
one judge call were made for each H04/H05/H06 (US$0.0135 each, US$0.0405
incremental total), with preflight and retained receipts. H04's empty briefing
room scored 10/10 and was visually accepted only as a generic transition
candidate; 48 planned shots still lack images. H05 `open-note` scored 9.29 but
was manually rejected for invented passengers and an oversized paper. H06
`hook-canal-rail` scored 9/10 but failed both judge and human inspection for a
mountain lake and fake small text. Those two rejected scenes now use original,
source-labelled SVG diagrams with inspected static renders; rejected images
remain evidence, not production frames. H05 has 61 remaining shots, H06 has 49.

The scene-template edits invalidated the H05/H06 narrative and audio-timeline
bindings. H06's new `a8b72a5524beace9` narrative passed 11/11 blind review;
`tts --refresh-evidence` rebuilt `timeline.json` SHA-256
`829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2`
with 0 syntheses and identical 104 line timings/WAV hashes. H05's first new
blind review found two missing explicit payoffs; only `h5v029` and `h5v103`
were rewritten, then a fresh reader passed `31f279e4aaa020c5` 11/11. TTS
synthesized only those two clips (53 billable characters, 100 requests reused),
and check-audio checked 108/108; both new lines match, while the previous 12
owner flags remain. New H05 timeline SHA-256 is
`db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee`.
On actual audio H05's 61 shots cover 58.5658% with maximum state 7.833s;
H06's 49 shots cover 50.3061%, just 46 frames above 50%, with maximum state
7.967s. Both have zero cadence problems. New audio cards were sent to
`/admin/videos` and read back **pending** for owner approval; previous approvals
bind older timeline hashes. Body-only zh-TW CC previews have full cue coverage
but no full render, approved storyboard, completed thumbnail, branded final CC,
MP4, package, owner playback, or Studio upload. Keep this ticket open.

2026-10-14 latest checkpoint: the owner listened and approved both H05/H06
new audio cards. `review-pull --gate audio` read back approvals for exact
current timeline SHA-256 values: H05
`db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee`,
H06 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2`.
H04 remains approved at its current timeline SHA. Thus all three current
narration gates are approved; this does not approve pictures or final videos.

The owner then raised the **bounded MiniMax pilot** scope to three different
adjacent shots per episode, one image and one judge call per shot (nine total),
after the prior one-per-episode pilots. All nine authorized attempts finished
with no same-shot retry: each slug incurred 3 MiniMax images, 3 Gemini judges
and US$0.0405, for **US$0.1215 incremental** across the three. H04
`opening-search/opening-inside/opening-gear` yielded 2 machine PASS and 1
FAIL, but 0/3 human-accepted frames as a continuous opening (wrong spatial
relationship, painterly style, mismatched camera/space). H05
`open-threat/open-tail/open-boy` yielded 2 machine PASS and 1 FAIL, but 0/3
human-accepted frames: invented passengers and props, fake lettering, and a
conspicuous orange-red ground mark. H06
`hook-hospital-door/hook-hospital-door-beat-2/hook-three-answers` yielded 1
machine PASS and 2 FAIL; the flat symbolic second frame is only a single-shot
candidate, while the sequence fails photo-to-flat style and scene continuity.
The original images, both successful and adverse judge decisions, exact
ledgers and before/after manifests are retained externally under each v2
workdir's named pilot receipt folder. See each v2 `visual-pilot-*` record in
this PR. No storyboard was submitted, full image batch started, or final MP4
rendered. Keep the ticket open and decide a revised visual route before more
paid images; the 50% shot-time floor has only about 50 frames of slack for
H04 and 46 frames for H06, so a diagram substitution needs new cadence and
audio-timeline binding checks.

2026-10-14 mixed-pilot checkpoint: the owner authorized exactly six further
MiniMax pilot images with one normal judge per image: H04 three adjacent
opening shots, H06 two revised shots around its retained middle candidate,
and H05 one night-cloud atmosphere shot after adopting three original,
source-labelled opening diagrams. The six requests and six judge calls are
complete with no same-shot retry or outstanding reservation. Actual incremental
cost was US$0.0810: H04 US$0.0405, H05 US$0.0135, H06 US$0.0270. Raw images,
judge results, requests, ledgers, SHA snapshots and separate human decisions
are retained outside the repo and summarized in each v2 pilot document.

H05's three diagram substitutions changed the narrative and timeline hashes.
A new independent reader passed all 11 narrative questions. TTS rebuilt the
timeline using unchanged WAVs, with zero synthesis or billable characters;
the 108 existing audio checks and 12 owner-accepted flags remain applicable.
The owner approved the new audio card, and `review-pull` records exact current
timeline SHA-256 `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`.
H04/H06 current audio approvals remain valid. The new H05 night-clouds image
is a single atmospheric candidate, not an accepted sequence.

Human visual review still holds the H04/H06 continuous openings: H04 has one
conditional search image and two rejected tent/gear images; H06's two new
images have prompt/source and continuity defects despite model PASS results.
H04/H06 generated-shot durations exceed the 50% minimum by only 49/46 frames,
so source-diagram substitutions require revised trustworthy illustration
windows and another narrative/timeline/audio binding. No episode has an
approved complete storyboard, thumbnail, full render, final CC/MP4, QA,
upload package, playback acceptance or Studio upload. Keep this ticket claimed
and PR #1484 draft; the next visual production route needs an owner decision.
