---
id: 2026-09-25-add-catalog-import-skill
title: Add the catalog-import skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-catalog-import
claimed_at: 2026-09-25T15:15:22Z
created_at: 2026-09-25T15:14:49Z
completed_at: 2026-09-25T15:26:06Z
branch: claude/skill-catalog-import
depends_on: []
scope:
  - .agents/skills/catalog-import
  - .claude/skills/catalog-import
---

# Add the catalog-import skill

## Why

The host-side data CLIs (`apps/api/app/cli.py`, 58 KB and 30 subcommands, plus the `*_cli`
modules under foods, hotspots, guides and catalog_review) had no single place that says which
subcommand does what, which ones write by default, where a file has to be for the container to
see it, and in what order a merchant batch goes. Every session re-read the CLI or a memory note.
A repo skill loads the order and the gates on demand, with a compact command table in references.

## Definition of done

- [x] `.agents/skills/catalog-import/` exists with SKILL.md, `references/commands.md`,
      `references/merchants.md`, `references/reservation-links.md`, `references/other-data.md`
      and `agents/openai.yaml`; `.claude/skills/catalog-import/SKILL.md` is the byte-identical copy.
- [x] Every flag and path in it was checked against the current argparse definitions and modules.
- [x] Article pack import (content-pipeline), CatchTable batches (catchtable-discovery), review
      queues and Place IDs (hotspot-review) and the deploy (deploy) are linked, not duplicated.
- [x] `node --test tools/skills.test.mjs` passes.

## Steps

- [x] Read `cli.py` and the sibling CLI modules; list every subcommand with its write flag.
- [x] Condense the merchant enrichment and non-Korean reservation-link notes, README's admin and
      hotspot sections and the generic import format of `apps/api/app/foods/data/catchtable/README.md`.
- [x] Write SKILL.md (under 8 KB) and the four references; copy SKILL.md to `.claude/skills/`.

## How to verify

```bash
node --test tools/skills.test.mjs
```

## Notes

- Inverted write flags are the trap: `seed-foods`, `collect-hotspots`, `backfill-trip-item-names`,
  `guides-search-reindex`, `guides-aliases-seed`, `guides-links-rebuild`, `fill-hotspot-labels`,
  `match-hotspot-places` and `guides-import` write unless `--dry-run` (the first two have none).
- The api image holds only `apps/api` at `/app`: no `docs/`, no repo `candidates/`. So
  `guides-aliases-seed` without file arguments seeds series keywords only on the host, and
  `generate-hotspot-candidates` without `--dry-run` writes a file that the next deploy discards.
- `export-food-merchant-worklist --out` writes inside the container; read stdout instead.
- `fill-simplified-names` is split: emit the mapping on the host (the AI key is in the admin DB),
  apply it locally with `--from-mapping`.
