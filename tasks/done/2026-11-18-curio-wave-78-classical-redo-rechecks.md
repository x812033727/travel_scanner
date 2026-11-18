---
id: 2026-11-18-curio-wave-78-classical-redo-rechecks
title: Curio wave 78, classical redo, rechecks and So That's Why OpenStax
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T02:24:38Z
created_at: 2026-11-18T02:24:20Z
completed_at: 2026-11-18T02:24:40Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
---

# Curio wave 78, classical redo, rechecks and So That's Why OpenStax

## Why

The owner (2026-11-18) chose: fold N7566 into N425, give G06 and G08 real sources in place of OpenStax, redo the topics lost because classical Chinese texts could not be read, recheck wave 77's needs-check topics, and expand curio again.

## Definition of done

- [x] N7566 folded into N425 as a chapter (editorial merge).
- [x] Waves 76 and 77 needs-check topics rechecked by non-authors; results recorded as `recheck`.
- [x] Four classical-text rejects redone from archive.org scans (N7581–N7584).
- [x] Curio wave 78: directions scored before research, top 40 researched and reviewed, cores selected and scored.
- [x] So That's Why G06 and G08 rebuilt without OpenStax; G06 stays ready, G08 drops to reserve with the reason.
- [x] Both pools and the admin bundle rebuild and pass.

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
npm run check:tasks
```

## Notes

- Classical texts: zh.wikisource, ctext, github.com and kanripo.org are all blocked. Reading archive.org scan PDFs (Siku Huiyao, Ming editions) as page images with pdftoppm works; every quote cites the PDF page and juan, and reviewers spot-check by rendering pages themselves. No transcription errors were found.
- Rechecks: 6 of 15 resolved (N7508, N7524 selected; N7516, N7549, N7562, N7575 held as chapters); 9 stay needs-check.
- Wave 78: 135 self-proposed directions, 111 after dedup and red-line drops, 40 researched plus 4 redone. 37 adopted, 5 needs-check, 2 not added. 23 cores selected (1694 -> 1717); 23 of the 25 newly selected cores score 6.5 or above.
- So That's Why: G06 now cites 11 new cards from readable sources (12.75 weighted facts, audience 6.73). G08 reached 14.75 facts but scored 6.48 (6.32 after repack), so it is reserve; ready long themes 57 -> 56. 1,048 selected cards pool-wide still cite only OpenStax; not addressed.
