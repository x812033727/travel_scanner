---
id: 2026-10-22-recheck-revised-c12-pyrex-treatment
title: Recheck revised C12 Pyrex Treatment source delta
status: done
priority: P2
area: docs
owner: codex-c12-independent-review
claimed_at: 2026-10-22T14:22:39Z
created_at: 2026-10-22T14:22:12Z
completed_at: 2026-10-22T14:24:27Z
branch: codex/brand-story-pyrex-c12-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-review/revised-treatment-source-delta.md
---

# Recheck revised C12 Pyrex Treatment source delta

## Why

The first independent C12 review held M09 and identified a cold-open rain attribution gap. The author changed the Treatment and source matrix twice. The initial HOLD and PASS were bound to earlier bytes and cannot approve the revised plan without a new independent delta receipt.

## Definition of done

- [x] Recheck the exact changed M04/M09 and cold-open text against their direct sources, bind the decision to both final file hashes, and state which owner gate is next.

## Steps

- [x] Compare the final Treatment and matrix against the first reviewed versions and read S1/S2/S4 directly.
- [x] Record final file hashes, source boundary verdicts, and unchanged-claim inheritance in a separate review receipt.

## How to verify

`Get-FileHash docs/videos/story-everyday-pyrex-c12/treatment.md,docs/videos/story-everyday-pyrex-c12/source-matrix.md -Algorithm SHA256`; `git diff 081ac4e0d..aa558354b --` those two files; direct S1/S2/S4 URLs in the receipt; `git diff --check` and `npm run check:tasks`.

## Notes

Revised M09 now distinguishes Bessie's single sponge-cake experiment from the later transparent commercial ovenware; no easy-cleaning or observing-the-bake result remains. M04 treats rain as the later European brand telling and museum S1 as cold outside air. The cold-open citation explanation was moved into an explicitly non-narrated note. Delta PASS is a Treatment-level source verdict only; owner adoption, script, TTS, images, upload and publication remain separate gates.
