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
      script, source records, `loops` and a passing blind narrative review.
- [ ] Each new slug has checked narration, source-bound artwork, current branding,
      8+ minutes of body, synchronized zh-TW CC and a newly QA-checked full MP4.
- [ ] Each new upload package and backend review binds the new hashes. Keep
      owner playback and Studio upload/publication as separate recorded gates.

## Steps

- [x] Audit origin/main workflow, H04-H06 source branches/workdirs and active
      ownership; create isolated v2 scope and claim it.
- [x] Rewrite and independently check the three scripts, then run lint and the
      blind `narrative` gate before further paid speech. All three have
      current-hash 11/11 results; H05 and H06 were rebound after edits.
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
H04's earlier image attempts and bounded pilot generated 201 MiniMax images and
199 judge calls in total (about US$2.69), but a subsequent look/prompt revision
invalidated their approval. The owner raised the monthly judge limit to 11,000;
the last readback was 10,014/11,000 judge calls and 9,139/10,000 images. H04's
new-look three-shot pilot is ready for a one-take run, but the project STOP
remains after its removal was blocked by automatic policy. No v2 storyboard,
render, captions, final MP4 or package exists.
H05/H06 old backend abandon would clear old reviews/previews; their independent
v2 slugs were registered without abandoning the old projects.

All three have current-hash independent blind passes and source-bound claim
records. H06's earlier passes are historical; the current `349cf912c147f530`
script has a persisted 11/11 narrative gate. H05's earlier 11/11 review became
stale after pronunciation and redundancy edits; the current
`e0d2eb7016aea429` script passed a fresh independent 11/11. H04 lint has 0 errors
and three topic-frequency warnings; H05/H06 latest lint has 0 errors and 0
warnings. H05 outline A is approved and 8:55.8 of narration is synthesized.
Its initial `speech/transcribe` call returned HTTP 504; after provider-usage
review, the owner authorized one retry. The journal is no longer held and
`check-audio` checked 108/108 lines. Local Whisper cleared 10 of the 22
original flags; bounded TTS corrections of three lines left 12 flagged lines
on the exact current audio. H05's current narrative hash
`e0d2eb7016aea429` passed an independent 11/11 recheck. The audio review was
pushed and read back as waiting for owner listening, so it is not approved and
image production remains gated. H06 outline A was
chosen by the owner and pulled back from the backend. Initial TTS and audio
check produced 104 lines, an 8:19 timeline and 16 flags; eight targeted takes
were then redone before H06's STOP halted the batch. Edits after that point
make the old timeline stale. H06 audio is not approved and no H06 image has
been generated. H05/H06 have no new approved images. No v2 final MP4,
captions or upload package exists yet.

Before another paid image call, all three `image-01` prompt sets were audited
for the series rule that `look.negative` stays empty and visible composition
is described positively. H04/H05/H06 dry-runs pass for 52/65/51 shots; these
are plans, not inspected or approved image frames. H04's next pilot under the
revised look is `opening-question,trail-search-start,journey-pack`; H05's is
`open-counter,open-ticket,open-aisle`; H06's is
`hook-canal-rail,hook-canal-rail-beat-2,hook-hospital-door` after outline and
audio approval. H04 must regenerate its current-hash images and manually
inspect them; old judge passes cannot be carried forward. H06's separate STOP
also remains; neither STOP has been bypassed or removed.

Draft PR #1484 contains the three independently reviewed scripts, source
records and asset provenance. Its first CI run passed `test:docs-videos` but
failed `test:tools` because new prose leaked absolute local user paths. The
paths were replaced with `<home>` placeholders and the focused
`repo-hygiene.test.mjs` passes 3/3 locally. All Linux CI checks on pushed
`450684784` passed; later edits need another run.

Local checks on 2026-10-14: `npm run check:tasks` passed (existing stale-claim
warnings elsewhere). `npm run test:docs-videos` ran 215 tests: 214 pass, one
unrelated Windows child-process crash in
`imported-long-languages/runner.test.mjs` (`package-runtime.mjs` exits
3221226505 with no output). The exact single test fails the same way in the
untouched `a8cd` checkout and this new worktree; it is not a v2 document
regression. The Linux PR checks passed at `450684784`; new edits need recheck.
