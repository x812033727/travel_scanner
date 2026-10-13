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
      blind `narrative` gate before paid speech.
- [ ] Inspect old backend projects and resolve their superseded status before
      registering new slugs; keep old approvals and media intact.
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
H04-v2 has an approved outline A and 8:49 narration. The first TTS batch made
100 takes (2005 billable characters); audio checking flagged 17 sentences, a
bounded redo reduced this to eight, and those eight were rewritten for clarity,
independently checked, and synthesized as eight new takes (169 characters;
92 reused). A final one-sentence wording repair cost 25 characters. Audio
checking now reports 101/101 sentences checked with zero flags; the backend
approved the audio gate and local `review-pull` recorded it. H04 illustration
generation is running. Full render and package are pending. H05/H06 old backend abandon remains an owner
decision because it clears the old backend reviews/previews.

All three v2 scripts now have source-bound claim records and independent
`verify-1.md` reviews bound to the final document hashes. Each blind narrative
panel passed 11/11. H04 lint has 0 errors and 0 warnings; H05 and H06 have 0
errors and one documented static-outro pacing warning each. No v2 final MP4,
captions or upload package exists yet.

Draft PR #1484 contains the three independently reviewed scripts, source
records and asset provenance. Its first CI run passed `test:docs-videos` but
failed `test:tools` because new prose leaked absolute local user paths. The
paths were replaced with `<home>` placeholders and the focused
`repo-hygiene.test.mjs` now passes 3/3 locally; a fresh CI run is pending.

Local checks on 2026-10-14: `npm run check:tasks` passed (existing stale-claim
warnings elsewhere). `npm run test:docs-videos` ran 215 tests: 214 pass, one
unrelated Windows child-process crash in
`imported-long-languages/runner.test.mjs` (`package-runtime.mjs` exits
3221226505 with no output). The exact single test fails the same way in the
untouched `a8cd` checkout and this new worktree; it is not a v2 document
regression. CI on Linux remains to be checked after PR creation.
