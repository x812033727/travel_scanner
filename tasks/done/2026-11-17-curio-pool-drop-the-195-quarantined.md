---
id: 2026-11-17-curio-pool-drop-the-195-quarantined
title: Curio pool: drop the 195 quarantined cards and recheck six wave-75 topics
status: done
priority: P2
area: docs
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T14:01:56Z
created_at: 2026-11-17T14:01:55Z
completed_at: 2026-11-17T14:29:40Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - apps/api/app/video_pools/data
---

# Curio pool: drop the 195 quarantined cards and recheck six wave-75 topics

## Why

After wave 75 the owner chose (2026-11-17) to remove the 195 cards still in quarantine and to give the
six `needs_check` topics of wave 75 one more round of source research.

## Definition of done

- [x] The 195 quarantined wave 58–71 cards are `drop` in `dedup-decisions.json`, each with its own reason, and no longer held.
- [x] The six topics are researched again and reviewed by a non-author; what passes is selected or held, scored, and written up.
- [x] The pool and the admin bundle rebuild and pass their checks.

## Steps

- [x] Drop dispositions (24 collide or repeat, 171 scored below 7.15).
- [x] Three research agents (ZU0–ZU2), three reviewers (R760–R762), merged into the wave 75 batch and receipt (`recheck` per verdict).
- [x] Demand and audience scores for the two new cores, README.

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
npm run check:tasks
```

## Notes

- Four of six found their missing source: N7408 and N7409 are selected (N7408 passes 6.5 at 6.65, N7409 is 6.23), N7415 and N7428 are held as chapters.
- N7404 still has no primary or institutional source for the 1933 find; the next route is the museum's own accession record, since the site that holds the finder's family account refuses automated requests. N7421 still rests on the participants' own writing; a 2023 journal article and the contemporary Toronto papers were not reachable.
- A research agent's "found it" was wrong twice about the twist (N7428, N7415's role). The non-author review is what caught it.
