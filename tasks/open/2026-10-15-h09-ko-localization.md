---
id: 2026-10-15-h09-ko-localization
title: Localize Curio H09 Korean metadata and captions
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h09
claimed_at: 2026-10-15T10:45:58Z
created_at: 2026-10-15T08:17:21Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/i18n/ko.json
---

# Localize Curio H09 Korean metadata and captions

## Why

H09's approved Traditional Chinese film needs source-bound Korean lines and upload metadata for the language components selected by the owner. The translation must keep the uncertainty in the radio, bones, sonar and 2026 survey evidence.

## Definition of done

- [x] Korean file contains all 100 captions, 8 chapter labels, title, description, 8 tags and localized thumbnail words with current source hashes.
- [x] An independent Korean reviewer checks meaning, names, caption pacing and upload copy before the Korean language package is submitted.

## Steps

- [x] Claim the Korean-only scope and fill the generated worksheet.
- [x] Rebuild the worksheet after the Chinese description correction and merge with zero stale-field problems.
- [x] Check dub character budgets and video lint.
- [x] Have a separate reviewer verify and resolve any edits through a fresh worksheet and merge.

## How to verify

With `VIDEO_WORKDIR` set to the media root containing `curio-h09`:

- `node tools/video/cli.mjs i18n-sheet --slug curio-h09 --locale ko --parts metadata,captions` reported 0 of 100 lines, 0 of 8 chapters, no metadata todo.
- `node tools/video/cli.mjs lint --slug curio-h09` returned 0 errors; its three remaining warnings concern the unchanged Chinese shot duration and narrative hooks.
- `npm run check:tasks` passed (the board emitted only existing old-claim/scope warnings).

## Notes

- The first independent reviewer compared all 100 captions with the Traditional Chinese script and flagged register, uncertainty, institution/model names, a hydroprobe description, metadata, and one dub length issue. This revision addresses those findings; a second independent pass is still pending.
- All 100 narration entries now use formal Korean narration or intentional fragments/quotes, and all 100 fit their own `max_chars` limits. `h1negb6i` is now 10/10 characters.
- The draft preserves the tentative radio signals, the Navy's likely-sea-crash inference, the uncertain 1940 bones and 2026 Taraia evidence, and the fact that survey data await analysis. It distinguishes the Howland deep-sea sonar target from Taraia Object in the island lagoon.
- `Electra` and `Taraia Object` retain their Latin names. The first ALI mention names the Archaeological Legacy Institute in Korean and notes that it opened the new survey. The title and tags omit the unapproved Korean channel-name coinage; the narration CTA retains the source's Chinese channel name.
- The corrected metadata uses the current Chinese description source. Fresh `i18n-sheet` reports zero pending entries; `i18n-merge` wrote all 100 lines without problems. Video lint returned 0 errors and the same three warnings about unchanged Chinese pacing/hooks; `npm run check:tasks` passed with unrelated existing board warnings.
- No paid model, TTS, external QA, caption render, or Korean dub was run for this localization step.
- Final independent Korean re-review: READY. The reviewer confirmed 100/100 unique IDs, zero lines above max_chars, and resolution of all factual, register, proper-name, and metadata findings. The task remains in progress for the coordinator's final language-package dry run and commit.

- 2026-10-15 coordinator continuation: the owner explicitly replied "同意移交韓語檔案" for this narrow scope; --force claim transferred it from the ended Korean subtask to codex-gpt6-curio-h09. Initial audio QA retained 14 flags. Five evidence-backed rewrites clarify 13 specimens of bones/fragments, later in the same year, bones unavailable for re-examination, the lagoon versus deep sea off Howland, and the distinction between reaching the island and identifying its object. The fresh worksheet was regenerated before merge; dry run confirms only five stale clips / 175 characters, zero unfit windows. Targeted synthesis is running; the other 95 takes are preserved.

- Final targeted-rewrite independent review by h09_retake_text_audit: PASS. Compared 5 changed lines against HEAD, Chinese source and surrounding context; no remaining material issue in facts, uncertainty or naturalness. Current translation SHA-256: BF7132AC422DDB0F8B3D57E96EF1F2E907B8600D6EF8EAF966A77364ACFA2FBE. This is a text review only, not audio acceptance.
