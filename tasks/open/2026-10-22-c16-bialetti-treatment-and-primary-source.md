---
id: 2026-10-22-c16-bialetti-treatment-and-primary-source
title: C16 Bialetti Treatment and primary-source matrix
status: in-progress
priority: P2
area: docs
owner: codex-bialetti-c16
claimed_at: 2026-10-22T18:14:51Z
created_at: 2026-10-22T18:14:47Z
completed_at:
branch: codex/brand-story-bialetti-c16-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16
---

# C16 Bialetti Treatment and primary-source matrix

## Why

C16 is only a topic in the 20-episode plan. The familiar 1933 invention story is not interchangeable with the dated patent records, and a moka pot does not make café-standard espresso. A source-bound Treatment is needed before the owner can approve a script direction.

## Definition of done

- [ ] A six-chapter, chronological, hook-led C16 Treatment and a direct-source M01–Mxx matrix exist under `docs/videos/story-everyday-bialetti-c16/`.
- [ ] An independent reviewer checks every proposed factual claim against the cited source and records a content hash and unresolved gaps.
- [ ] A draft PR targets `codex/brand-stories-new-series-20261020`; the owner still controls Treatment approval. No script or paid production is started.

## Steps

- [x] Check C16 task, PR, local branch, remote branch and worktree ownership; none overlapped this scope.
- [x] Create and claim this narrow task on `codex/brand-story-bialetti-c16-treatment`.
- [x] Write Treatment, sources and claim boundaries.
- [ ] Obtain independent source review, amend any finding, and bind final file hashes.
- [ ] Run relevant checks and open a draft stacked PR.

## How to verify

`npm run check:tasks`; inspect direct source URLs and the review receipt; compare reviewer SHA-256 with the final files; `git diff --check`; inspect PR base/head and draft state.

## Notes

2026-10-22 UTC: Bialetti's 2007 IPO prospectus and several museum retrospectives attribute a 1933 design to Alfonso, but the Italian patent-office exhibition catalog identifies utility-model records #34833 (1950-07-05) and #37736 (1951-05-05). No original 1933 Bialetti patent was found in this review. The laundry-boiler anecdote is explicitly called a legend by the exhibition catalog. Original attribution to Luigi De Ponti and an alleged 1937 Spadini design/court dispute are unresolved without directly read original records. Avoid sole-inventor certainty, a 1933 patent, the exact original marketing-slogan date, sales totals, or espresso equivalence.

2026-10-23 TST: Treatment and M01–M18 matrix authored. The key catalog citation now uses the Italian ministry's own hosted PDF. **Independent source review remains pending; hold Treatment owner gate, script and production until its hash-bound receipt is recorded.**

Author checks: `git diff --cached --check` and `npm run check:tasks` pass. The broad `npm run test:docs-videos` has six unrelated failures because this fresh worktree has no `pinyin-pro` installed in `node_modules`; this task changes only Markdown and the task record.
