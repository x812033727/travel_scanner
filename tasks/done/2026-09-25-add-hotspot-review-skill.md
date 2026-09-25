---
id: 2026-09-25-add-hotspot-review-skill
title: Add the hotspot-review skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-hotspot-review
claimed_at: 2026-09-25T15:10:23Z
created_at: 2026-09-25T15:10:08Z
completed_at: 2026-09-25T15:17:17Z
branch: claude/skill-hotspot-review
depends_on: []
scope:
  - .agents/skills/hotspot-review
  - .claude/skills/hotspot-review
---

# Add the hotspot-review skill

## Why

Clearing the hotspot, hotspot-guide and merchant-coordinate review queues was only written
down in three long batch logs under `docs/` and in per-machine agent memory. Every session
re-derived the same rules (the queue is a Place ID backlog, approval is one quota-free call,
rejections are tombstones that need two skeptics, Google coordinates never enter the catalog)
and some of the memory had gone stale against the code.

## Definition of done

- [x] `.agents/skills/hotspot-review/` exists with SKILL.md, references and agents/openai.yaml,
      and `.claude/skills/hotspot-review/SKILL.md` is its byte-identical copy.
- [x] Every endpoint, CLI flag, error code and symbol it names was checked against main.
- [x] `node --test tools/skills.test.mjs` passes.

## Steps

- [x] Read the source memory notes and `docs/hotspot-review-next-batch.md`,
      `docs/hotspot-intelligence.md`, `docs/hotspot-review-editor.md`.
- [x] Verify against the code: review endpoint and its validator, map-candidates,
      places autocomplete, usage meter SKUs, CLI commands, coordinate queue, discovery.
- [x] Write SKILL.md (rules, workflow, pointer table) and six references.
- [x] Mirror SKILL.md and run the skills test.

## How to verify

```bash
node --test tools/skills.test.mjs
```

## Notes

Stale memory corrected while writing it, so nobody copies it back:

- Discovery is no longer capped at the 100 nearest articles within 10 km: `search_points`
  in `apps/api/app/hotspots/discovery.py` covers a larger radius with a lattice of 10 km
  circles and `GEOSEARCH_PAGE_LIMIT` is 500.
- The merchant coordinate queue no longer writes Google coordinates as `admin_verified`;
  approval records only the Place ID and leaves coordinates to an independent source.
- Rows with a hand-entered Place ID no longer stay unverified forever: `_verify_from_profile`
  and the admin place-profile `_sync_map_match_status` now flip them.
- The review endpoint recomputes `area_code` and rewrites `search_text` on a move itself.
- `hotspot_guide_ai_max_output_tokens` now defaults to 16,000.
- Releasing a tombstone's Place ID with `update` must also send
  `map_match_status: unverified` if the tombstone is still marked verified, or local
  validation refuses it.
