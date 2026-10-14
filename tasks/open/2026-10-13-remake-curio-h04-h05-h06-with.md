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
      bound to their latest visual/story structure. (All three prior versions
      passed; repeat the blind review after the source-card storyboard change.)
- [x] Each new slug has checked narration, source-bound artwork, current branding,
      8+ minutes of body, synchronized zh-TW CC and a newly QA-checked full MP4.
- [x] Each new upload package and backend review binds the new hashes. Keep
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
- [x] Build and review new audio, illustrations, edit, captions, QA and packages
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

2026-10-14 no-cost rough-cut checkpoint: the owner chose original source cards
and isolated audio rough cuts before any further paid images. H04 now has two
original source-bound SVG candidates and a 20.700-second, three-scene opening
preview; H06 has two SVG candidates and a 15.433-second, three-scene static and
reveal preview with a two-line CC stress test. H05 has two isolated approved-WAV
previews: three opening source cards (14.567 seconds) and the tail-stairs to
night-clouds transition (18.033 seconds). A source-safe `forest-unknown` SVG
was also substituted for the latter preview's gray placeholder in an isolated
second 18.033-second cut, but the night-cloud-to-card jump is conspicuous and
the whole preview has not been accepted. H05's tail-stairs source footer
touches double-line CC in the formal template; an isolated 80px raise clears
720p/1080p samples but has not been formally adopted. Sampled frames and cue
timings were checked; complete normal-speed audible playback and owner visual
acceptance remain pending. No paid request or formal script, timeline, WAV,
approval, manifest, or ledger mutation occurred. See the dated rough-cut
records in each v2 docs directory.

The 50% illustration-time calculations remain **conditional allocations**, not
completed usable frames: H04's two opening diagram substitutions would reduce
planned shot time to 7,561/15,827 (47.7728%); two proposed source-safe shots
of 143+231 frames would yield 7,935/15,827 (50.1358%) if both pass. H06's
two diagram substitutions would reduce it to 7,249/15,028 (48.2366%);
two proposed shots of 214+154 frames would yield 7,617/15,028 (50.6854%)
only if both pass. H05 presently allocates 9,053/16,204 (55.8689%) to 58
shot slots, but only night-clouds is a single-image candidate; substituting a
source card for forest-unknown would leave 8,888/16,204 (54.8507%) before
further art. A proposed next paid pilot is two named shots per episode,
one MiniMax image and one normal judge per shot, no retries or bulk generation:
six image/judge pairs, roughly US$0.081 at the last actual unit price. This is
not yet authorized or run. The rough cuts must be watched, the H05 footer
fixed, and all new formal hashes and gates reopened if any diagrams are adopted.

2026-10-14 H04/H05 postflight checkpoint for the owner-authorized six-image
pilot: H04 and H05 have each consumed exactly two MiniMax images and two normal
judges, with no same-shot retries or outstanding ledger reservations. This
four-image portion cost US$0.054 (US$0.027 per slug). H04 ledger is now
US$2.906 / 217 images / 215 judges; H05 is US$0.216 / 16 / 16. Both current
script structures passed fresh 11/11 independent narrative review, and audio
approvals were read back for exact current timeline SHA values: H04
`12b18320ed0e246b25ace3ea844f55bbc91f17374e95bc87c85fe1d2bd9b6790`,
H05 `f8d106653941b3b90c9d3d6d6adf50f8bbb653bffde941073b43ce721e414468`.
H05 moved unchanged h5v063–065 WAVs after h5v084 to repair a 2020-before-1980
chronology error; all 108 per-line audio hashes and sample counts match, but
the composite WAV and playback-order hash changed.

Normal judges passed both H04 images (9.29 each), but human and separate
static-image cold review retained `tent-opening-question` only as an art
direction candidate and rejected `model-paper-card` for a fabricated yellow
tent, trees and overly specific slab. H05 `arrival-cabin` passed 10/10 yet is
only an art direction candidate because a yellow seat shape reads as an
unsupported left-behind object. H05 `aircraft-search` failed normal judge
despite 9.71 overall (`subject=0`) and was human-rejected for seated passengers
and an aisle person in the intended vacant cabin. None of these four frames
has formal human adoption; cold review inspected still images only, not a
normal-speed audible cut. H04 planned 7,935/15,827 shot frames (50.1358%) and
H05 planned 8,888/16,204 (54.8507%) remain conditional allocations, not
delivered usable illustration coverage. H04/H05 visual branches stop at pilot;
no same-shot redraw, storyboard submission or bulk image batch. Exact image
SHA, judge/human split, receipts and preflight corrections are in each v2
`authorized-six-pilot-postflight-20261014.md`. H06's two authorized shots are
outside this checkpoint and require their own narrative/audio gate and review.

2026-10-14 current-audio and H06 pilot checkpoint: H05's two source-card
substitutions and removal of repeated `h5v038`/`h5v100` are now formal. A fresh
independent blind review passed 11/11; 106 original line WAVs were reused with
zero synthesis, yielding 8:50.4 and current timeline SHA-256
`fd724a0c4318fe76fcb4a1811dadbf09f0aeff47d0849bfc025ceb03fed50fbc`.
The owner approved this exact hash in the backend and `review-pull` recorded it.
H06 re-recorded only the two owner-authorized DNA payoff lines once each
(57 billable characters), passed fresh 11/11 blind review and audio checks,
yielding 101 lines / 8:09.23; the owner also approved exact timeline SHA-256
`8c825dd0a0131fdd6ff358f14d90b791ab4a8c7554ff3d89d8bc05a0166c301b`.
The three current H04/H05/H06 timeline approvals now match their formal files.

With these gates clear, H06 generated only the authorized `dna-hair-and-box`
single MiniMax take and one normal judge, costing US$0.0135. The judge's 9.29
PASS did not survive original-image and independent cold review: multiple red
shapes, thick hair-like strip and photographic paper/shadows violate its one-
accent, flat 2D brief. It is not accepted or counted toward illustration time.
H06 ledger is US$0.162 / 12 images / 12 judges / 0 reserved. No paid call was
made for the second named H06 shot. If the rejected 214-frame slot becomes a
source card, even a passing second shot leaves only 7,250/14,677 planned shot
frames (49.40%); the repeated visual defects and sub-50% route therefore stop
this pilot without redraw or batch. The six-image authorization has used five
image/judge pairs, US$0.0675 total this round. H04/H06 need an owner decision
between a source-card-led slide specification and a new source-safe illustration
production route; see their dated route/postflight docs. H05's latest isolated
five-scene preview and source-card subtitle clearance are under review; no full
v2 final MP4, QA, storyboard approval or Studio upload exists.

2026-10-14 H05 research-control source-card follow-up: `burial-edge` is now a
formal source-labelled diagram based on the Kaye/Meltzer 2020 methods and
results, rather than an unmade `shot`. A fresh independent 11/11 narrative
review passed; the first CLI submission had an answer-wrapper format error,
preserved separately, and the corrected round 25 passed. All 106 line WAVs,
their order/windows, and the master WAV were unchanged; `tts` synthesized 0
new lines and `check-audio` checked 106/106 with 11 older owner-reviewed flags.
New timeline SHA-256 is
`d01d24050ec6cd6a7d5cd720b677ccb64b7bfdbd5368c02b0b08327206f5d391`,
15,912 frames / 8:50.4. The owner approved this exact new H05 audio card in
the backend and `review-pull` recorded the matching SHA. Planned `shot` time
is now 8,314/15,912 = 52.2499%; 54 planned shots still lack human-accepted
images. The isolated five-scene H05 preview decoded and kept the same PCM
samples, but source-card/CC clearance and full-speed visual acceptance are
still pending. See `burial-edge-formal-adoption-20261014.md`; there is still no
full v2 final MP4, QA, storyboard approval or Studio upload.

2026-10-14 owner visual-route decision: after five of the six authorized
MiniMax image/judge pairs, the owner selected source-card-led slides for
H04-H06 and explicitly relaxed the earlier minimum 50% illustration-time
specification. The old 50% calculations above are historical comparisons,
not a current acceptance gate. We are preparing source-bound, varied cards
and offline audiovisual checks within the three v2 projects; no further
paid image batch is implied by this decision. Any formal scene/template
change needs a fresh independent narrative review, timeline rebuild using
the unchanged accepted WAV takes, exact backend audio approval for the new
hash, and then scene-by-scene render/CC and continuous playback QA before
storyboard or final-video approval. Rejected MiniMax frames stay rejected.

2026-10-14 source-card production checkpoint: H04 is now 88 scenes / 100
lines / 0 shots, 8:47.57; formal blind review passed 11/11 and exact audio
timeline SHA `967955adb1a861e3facbdd69285654a2a293b7a275b8bfe6745ced283a97e2f5`
was auto-approved and read back. Its first full frame render passed, but
actual CC overlay inspection found lower source labels crossing the caption
reserve, so that render is not final. H05 is 89 scenes / 102 lines / 0 shots,
8:32.70 after owner-selected no-recap deletions; fresh blind review passed
11/11, and the owner approved the exact timeline SHA
`c43d09a858bfd8a39882510b52e3b8cda79563be07c978854387940489f6ac76`,
read back locally. H06 is 82 scenes / 100 lines / 0 shots, 8:06.07 after
owner-selected deletions and one owner-authorized new fact line `dm7x`.
The new line was synthesized exactly once (24 billable characters) and
transcribed word for word; 100/100 lines were checked with eight previously
reviewed flags. Fresh blind review passed 11/11, and the owner approved the
exact timeline SHA
`8683ca0e61c7e8bf83cd5e390618435467e21da1e3329eed125f216a0c31ac05`,
read back locally. No full MP4, final QA, package or v2 Studio upload exists.
The three episode docs have a separate ticket for an opt-in CC-safe renderer
rule (`2026-10-14-keep-curio-source-card-footers-clear`); after flagging
affected scenes, verify timelines stay approved, rerender and inspect actual
1080p/720p CC before assembly.

2026-10-14 full-production checkpoint (supersedes the preceding no-MP4
snapshot): all three source-card-led versions now have complete 1080p H.264/AAC
MP4s, original credited thumbnails, approved exact narration timelines,
8+ minutes of measured body, zh-TW CC, checked source cards, and fresh QA.
H04: 9:13.600 final, SHA-256 `ae9b62809dae82eaf96059fb4474c485f28d969f5d3ce47fd723303da1d88f0e`,
11/11 QA. H05: 8:58.700 final, SHA-256
`32cdc6403dbd321300c3a53ed2d2953696a3aa79da9ede5e977c00423499eb79`,
10/11 QA: seven FBI/FAA URLs return 403 to the local editorial GET;
independent browser opening succeeded, but the automated links item remains
failed. H06: 8:32.100 final, SHA-256
`f6eb1afd271d774fde36300bf57e63287e9a1013cf85c9ff7b7dc55a532eee3a`,
11/11 QA. H04 and H06 final gates are backend-approved and read back; their
zh-TW upload packages pass 4/4 and their publish-package gates are approved
and read back. H05 final review was approved by the owner in the backend with
the real 10/11 report and read back at the same MP4 SHA; its zh-TW upload
package passes 4/4 and its publish-package gate is approved and read back.
No new v2
video has been uploaded to YouTube or published. Language selections are undecided;
`languages.json` records `decided_at:null`, not a zh-TW-only owner decision.

Local-only cleanup remains outside this PR: three obsolete
`diagrams/thumbnail-subject.png` candidates and nine hidden H05 temporary
files are untracked and unstaged after automatic approval review rejected
their removal. `tasks done` wrote the completed CC-safe ticket to `tasks/done/`
but could not remove its local `tasks/open/` copy; a direct exact-path
`Remove-Item` was also rejected as `blocked by policy` without further reason.
The PR contains only the done copy; the open copy remains untracked locally.
Do not report any of these files as deleted or stage them accidentally.

2026-10-14 multilingual delivery checkpoint (supersedes the undecided-language
snapshot above): the owner selected English, Japanese and Korean titles,
descriptions and CC for all three v2 cuts, without additional dubs. The live
admin choices were read back as `metadata=true`, `captions=true`, `dub=false`
for each locale and episode. Nine source-bound translations were independently
reviewed and merged; final `captions` generation has no pace warnings. H04,
H05 and H06 four-language upload packages each passed 4/4. H06's zh-TW
description was corrected to describe the newly available translated metadata
and CC; its publish package was reapproved for the new metadata hash.

The backend `/api/video/reviews/{slug}` readback confirms all six selected
components per video are `ready`, each latest language review is approved, and
all three are `ready_to_upload=true`. Language review SHA-256 values are H04
`ea201bd9b9f94a85c05f81635554ad806b33715b5cd71978411f9310b7e61c13`,
H05 `f30ba7eeed5b38cd9499880d758684cfe596cc224335a522586da6949a214a74`,
and H06 `e97e05b41c44b4e2bb60bb892f9a5a0948b3fb6fe77b6260ed5f22b9fc34acf5`.
Package metadata SHA-256 prefixes are H04 `5bd63e0f02c8`, H05
`83d5bd2f7e06`, and H06 `b11d7a35f424`. All three local `review-pull
--gate languages` commands recorded approval. The final MP4 bytes did not
change. No v2 cut has been uploaded to YouTube or published; the owner handles
the private Studio upload and later release as separate gates.

Validation: all three packages 4/4 and captions without pace warnings. A full
215-test docs-videos run using bundled Node 24.19 passed 214 tests; one unrelated
Windows temp-file rename returned EPERM, then that exact test passed when run
alone. A full run with system Node 24.13 passed 214 and hit the previously
documented native child-process crash in a different test. `check:tasks` is
blocked by the duplicate completed CC-safe ticket under untracked
`tasks/open/`, whose exact deletion was previously rejected by automatic
approval review. Neither test issue changes the upload package checks.

2026-10-14 foreign-dub continuation: the owner enabled English, Japanese and
Korean dubs for all three v2 projects in `/admin/videos`. Live backend readback
showed all nine dub components `working` while metadata and captions remained
`ready`; `ready_to_upload` is now false until a new language batch is complete.
The three external `languages.json` mirrors were updated to match. A free
dry-run estimated 35,398 billable characters for nine tracks, with the speech
service reporting more than nine million characters of monthly headroom.
Production started line by line, preserving paid clips in cache.

During concurrent synthesis, Windows returned `EPERM` while promoting complete
speech-journal confirmations after the provider answered. H06 Japanese request
`0ec434e13061bcf819c9d80e95c329a170e79aef9a74f35fc0182464db7d0589`
had an intact 483,884-byte WAV (SHA-256
`1958800b90a296696bf2545a9ff7965f0024e6c25e224805595257297553f2a8`)
and matching `confirmed` temporary receipt; its original `sent` receipt was
atomically backed up and replaced with the validated confirmation, without a
second provider request. H05 English request
`7ff7dc416ad6156829a0c816ae689456ca26ef9a9ebd4abffd50f0bb1f9e8720`
likewise retained a 422,444-byte WAV (SHA-256
`655d847ff6cfa68e9bb1b9d9017b71cc90d63818a089b29e838e932af9805240`);
its original `sent` receipt was backed up and atomically replaced with the
matching confirmation, again without a second provider request. Project `STOP` files now protect all
three external workdirs while the existing unclaimed Windows journal task is
investigated. Cached recordings are retained, no complete foreign audio track
or new language review has been claimed yet, and the original approved MP4s
are unchanged.

Offline dubbing preparation after that hold: H04 ko was tightened in 40
source-checked lines and independently reviewed, H04 ja corrected two source
nuances; H05 en/ja/ko was tightened and independently reviewed, including the
2020 bill-stack diatom wording in all three locales; H06 en/ko was tightened
and independently reviewed. All three slugs lint at 0/0 and translations are
source-current. H04 ja/ko and all H05 locales have zero estimated unfit
windows. H04 en has 11 estimated over windows but 92 cached paid WAVs, so use
actual `fit.json` before changing that text. H06 ja has one estimated over
window with 44 cached WAVs; H06 ko has one estimated over window (`v228`,
Russian anthropologists' qualified first-grave view) retained for source
accuracy until actual timing is measured. H06 en has zero estimated over
windows. No new paid speech was requested during this offline preparation.

The H04 project STOP removal attempted from this task was automatically
rejected by policy. The owner has been asked to remove that exact new STOP on
the production workstation; local readback still showed it present. H05 and
H06 STOPs also remain, so no locale track is ready yet. `test:docs-videos`
passed 214/215 under system Node 24.13.0; the one unrelated portable-runtime
freeze test crashed its child process (`3221226505`) and passed when run alone
under bundled Node 24.19.0. `check:tasks` remains blocked by the unrelated
untracked duplicate `tasks/open/2026-10-14-keep-curio-source-card-footers-clear.md`;
its prior removal was automatically rejected. Do not stage or silently delete
that duplicate.

After the owner removed all three STOPs, H04 en resumed from paid cache. Actual
fit required shortening only `h4v103` to "Which clue?"; two bounded retake
rounds reduced four Jev flags to one, and `h4v093` was then reworded to "But
both articles report the same observations." to avoid repeated `described` /
`describe` confusion. Final en check-audio: 100/100 checked, 96 exact, four
Jev-cleared, zero flags; 100 windows fit, max tempo 1.12x. The local en.m4a is
19,956,526 bytes, SHA-256
`2a396b6ada1a0c203a924c94a913fd6b6f1320e09474ebacbde8a5f6f0d495e7`;
timeline speech hash `939e267cecc8f2cb`, translation hash `dd0a14dadf3733d0`.
This is a local output, not yet in a language review or YouTube Studio.

One H04 en transcript response hit the Windows journal rename EPERM. Original
`sent` and temp `confirmed` receipts for
`d77427bb0c25afefb23be7d363705205595085d777f9e37feb6899684670e94e`
had identical request and sent time; the inline answer hash verified. The
original was backed up before exact replacement, read back as confirmed, and
the subsequent check reused that paid answer without another POST. Do not
turn this per-request recovery into a general retry; draft PRs #1379 and #1391
still own the shared journal/atomic-write fix paths.

The owner then removed all three new STOP files and this workstation read
each path back as absent. H04 ja was synthesized line by line. Its first
100-line check flagged 20 lines; a local independent Whisper medium transcript
cleared seven likely Gemini errors. Thirteen source-faithful lines were
reworded, with `h4v019` shortened again after actual audio exceeded its
window. Two residual flags were reworded and rerecorded. Current H04 ja fits
all 100 windows (max 1.19x) and `check-audio` is 100/100: 82 exact, 10
Jev-cleared, eight independently cleared, zero flags. The local `ja.m4a` is
22,352,920 bytes, SHA-256
`5bc87a7039417228e48a8294ef1a69ef0c977016372c139cf1711a3bf7d463b4`.
The independent checker used an external PyAV-19 compatibility wrapper around
the repository's script; the repository script itself was not changed.

H05 en now has a local `en.m4a` (18,919,297 bytes, SHA-256
`f3bb257d97b1f889ccc52a3158eb402eeb7dc4edd870a5f44c3477af0068d89b`)
from 97 line recordings, reusing earlier paid WAVs where available; its formal
`check-audio` is still pending. H04 ko `h4v019`, H05 ja/ko `h5v010`, and
H06 en `v229` were narrowed offline against the original narration before
their new paid requests. All three slugs currently lint at 0 errors and zero
warnings. These are local audio and translation artifacts, not a language
review approval, Studio upload, or published video.

Several Windows journal replacements failed after a provider answer. For H04
ja (`f3829bd4`, `f8a12c98`, and `4237a45b`) and H05 en (`fc45ea16`), the
original `sent` and temporary `confirmed` receipts had the same request and
sent time; each complete WAV or inline answer matched its recorded SHA and
bytes. Original and temporary evidence copies were saved, then the exact
canonical receipt was replaced and read back as confirmed. The later CLI run
reused each paid answer. No generic retry, forgotten receipt, or duplicate
provider request was used to cross an uncertain outcome.

H04 ko's second transcript cleared five of ten initial flags; five
source-faithful lines were narrowed and rerecorded once each. The new 100-line
check is 77 exact, 18 Jev-cleared, five independent-transcript-cleared, zero
flags; every window fits at 1.00x. The local `ko.m4a` is 20,568,518 bytes,
SHA-256 `0bfbb0c02054504119db280ed5bac8e08b57028aaac187e97e5cb29d16e4dbdc`.
H04 now has en/ja/ko local tracks passing fit and check-audio. Captions were
rebuilt in four languages and `package` passed 4/4, listing all three dub
tracks; upload metadata SHA-256 prefix `5666854ddb15`. `review-push --gate
languages` submitted the H04 language card, and backend owner approval is
pending. This is not a Studio upload, player verification, or publication.

H05 ja synthesized 97 requests (2,507 billable characters), with 102 windows
fitting after timing adjustment; two short overruns were absorbed by following
pauses. Its local `ja.m4a` is 20,801,740 bytes, SHA-256
`67db831a0bfb7b65d043d0ac610906a3bffc4f5b55e7568858a6b01392a59638`.
Formal per-line audio check is pending. H06 ja `v228` was shortened before its
first paid recording; current dry-run has zero windows forecast to exceed
1.15x and H06 still lints 0/0. H06 ko `v228` remains source-faithful until
actual recorded timing resolves its single forecast overrun.

H05 en check-audio hit a further Windows journal rename EPERM after a paid
transcript returned. For request `a0f4a3703194f0459a40e0b41d4bf3536f75b5af8370e57b79b1c665f670876c`,
the original `sent` and temporary `confirmed` had identical request and sent
time; the inline answer hash matched `73b80e57d94bdca654ac776e642de583b82988cdc67cf586c470e7d68943e054`.
The producer PID was dead. Original and temporary evidence copies were saved,
then the exact canonical receipt was atomically replaced and read back as
confirmed with a sent backup. The resumed checker reuses this answer; it must
not POST that request again.

The resumed H05 en `check-audio` completed 102/102: 88 exact, five
Jev-cleared, five independent-transcript-cleared, four flagged (`h5v037`,
`h5v082`, `h5v084`, `h5v091`). It reused the recovered paid answer and made
no duplicate request for it. `h5v037` sounded like "shoe" rather than "chute";
`h5v082` had plural "bills" where the claim needs one recovered bill.
`h5v084` (Kaye/Kay) and `h5v091` (Tena Bar/Tina Bar) were same-sound spelling
flags, not evidence of wrong factual pronunciation. Four localized sentences
were rewritten before any retake: the parachute and single-bill wording is
clearer; the author names and Tena Bar remain explicit in their same-scene
source cards while the spoken translation refers to the two researchers and
the discovery site. H05 en lint is 0/0, dry-run is four new requests and
zero forecast unfit windows. The old en check does **not** validate the newly
worded track. H05 ja check-audio is now running under the project lease; no
other paid H05 tool may start until it ends.
