---
id: 2026-11-17-curio-wave-76-and-so-that
title: Curio wave 76 and So That's Why redo of the quarantined themes
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-17T18:05:15Z
created_at: 2026-11-17T18:05:04Z
completed_at: 2026-11-17T18:31:31Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
---

# Curio wave 76 and So That's Why redo of the quarantined themes

## Why

The owner asked for the next step after every curio core was scored (chose half self-proposed directions, half reference-channel directions, scored before research), and then asked to expand So That's Why too (chose to redo the 30 themes quarantined for fabricated sources).

## Definition of done

- [x] Curio wave 76: directions scored first, the top 40 researched and reviewed, adopted cores selected and scored.
- [x] So That's Why: the quarantined themes redone from real sources; those that meet the material bar and the 6.5 audience gate are ready again, the rest stay reserve with what is missing.
- [x] Both pools and the admin bundle rebuild and pass.

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
npm run check:tasks
```

## Notes

- Curio: 154 directions scored, top 40 researched, 12 cores selected (all pass 6.5), 8 held as chapters, 8 need sources. Cores at 6.5 or above 380 -> 392.
- So That's Why: 14 duplicate themes dropped from the redo, 22 redone, 11 met the material bar, 3 passed the audience gate (G668, G679, G685). Ready long themes 54 -> 57.
- Two lessons: co-authorship between research networks must be checked (Europe PMC author queries merged networks in 8 themes), and the old high scores leaned on fabricated claims, so honest rewrites score much lower.
- OpenStax pages forbid ingestion by large language models and are CC BY-NC-SA; it no longer counts as a source. Earlier rounds that used it are not yet audited.
- Write-time dedup must also check `pool.json` not_added and `DEDUP.md`; seven wave-76 directions were old rejections.
