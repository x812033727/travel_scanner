---
id: 2026-10-15-h09-ja-localization
title: Localize Curio H09 Japanese metadata and captions
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h09
claimed_at: 2026-10-15T10:08:01Z
created_at: 2026-10-15T08:17:17Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/i18n/ja.json
---

# Localize Curio H09 Japanese metadata and captions

## Why

The owner selected Japanese metadata, captions, and a dub for H09 after approving
the final cut. The approved Chinese story has 100 timed narration lines; Japanese
text must preserve its uncertainty and fit the per-line dub budget before the
independent reviewer and audio stages can proceed.

## Definition of done

- [x] Japanese metadata, thumbnail wording, eight chapter names, and all 100
  narration lines are merged against the current H09 source.
- [x] Every translated line fits its worksheet `max_chars` limit.
- [x] An independent reviewer checks meaning, names, cue order, and
  readability; accepted fixes are merged.

## Steps

- [x] Claim this narrow scope and read the approved source and translation rules.
- [x] Draft Japanese metadata and captions in `ja.todo.json`.
- [x] Compare against the Chinese source and glossary, revise, then run
  `i18n-merge --slug curio-h09 --locale ja`.
- [x] Hand the merged file to an independent reviewer and apply confirmed fixes.

## How to verify

With `VIDEO_WORKDIR` set to the media root containing `curio-h09`:

```text
node tools/video/cli.mjs i18n-merge --slug curio-h09 --locale ja
node tools/video/cli.mjs lint --slug curio-h09
npm run check:tasks
```

Also compare all 100 translated line IDs and their lengths with the worksheet's
`max_chars` values, and confirm title, description, tags, thumbnail, and all
eight chapters are populated.

## Notes

First merge wrote 100 lines with no missing entries. Kept Electra, Itasca,
Colorado, Lexington, TIGHAR, ALI, and Taraia Object in Latin script; rendered
Earhart as イアハート, Howland as ハウランド島, Nikumaroro as ニクマロロ島, and Gardner as
ガードナー島 throughout. The source's 2026-10-14 investigation remains pending;
the translation does not claim an identified wreck.

Self-review corrected one Lexington line over its initial dub budget, an
unnatural Japanese word for colonial official, the water-fed probe term, the
call to subscribe, and the distinction between a completed identification and
a mere research result. All 100 current lines fit `max_chars`. No audio, paid
QA, or other locale files were touched.

ALI's published plan describes the hydroprobe as a pipe with water flowing
through it. `h1lrep92` now says `水を通す探針` so the Japanese line does not imply
a pressure-only instrument. Source: https://www.archaeologychannel.org/taraia/

The Chinese description changed while this translation was in progress. A
fresh `i18n-sheet` flagged only that field; the Japanese description was
updated to say that findings before public release will be rechecked and the
description updated. The final merge lists no problems, and a fresh sheet
reports 0/100 lines and 0/8 chapters needing translation. The Japanese title
was shortened to 29 characters to remove the mobile-list lint warning.

Verification: H09 lint exits 0 (0 errors; three pre-existing scene warnings),
`npm run check:tasks` exits 0 (shared-board warnings), and a schema-aware
comparison finds 100/100 merged lines identical to the worksheet and under
their per-line dub budgets.

Independent English translator reviewed this Japanese draft read-only, and
identified seven line/metadata corrections: remove the channel name from the
localized title/tags; keep alleged signals neutral; do not imply the team had
already entered the lagoon, touched the object, found surface debris, or begun
data analysis; preserve the distinction between Earhart being on the island
and this object being her plane; keep the Navy crash site explicitly inferred.
All were corrected and the reviewer then found no remaining issue in those
fields. Final `i18n-sheet` reports 0/100 lines and 0/8 chapters pending;
`i18n-merge` lists no problems. Leave this ticket in progress for the H09
coordinator to commit and close with the episode's draft PR.

- 2026-10-15 coordinator continuation: the owner explicitly authorized transfer of this narrow file scope from the ended Japanese subtask. The coordinator claimed it with --force for that authorized transfer. Fourteen final lines differ from HEAD, followed by one ALI-name retake; paid batches used 466 + 42 characters and retained cached takes. The current 100-line dub fits every window (4 sped up, maximum 1.12x). Incremental QA retains nine flags; the owner reviewed the hash-bound listening page and replied "日語旁白可以". Local review/dub-ja-owner-acceptance.json binds track SHA-256 4f091b943757ba5005d3814a893a3ea25bce08074352272dc16aafdcddc9b695. Original QA flags remain; no Studio upload or language-gate approval is implied.

- Final targeted-rewrite independent review by h09_retake_text_audit: PASS. Compared 14 changed lines against HEAD, Chinese source and surrounding context; no remaining material issue in facts, uncertainty or naturalness. Current translation SHA-256: 9C0CF73530280BAF32074945A53FCE0AD73C89C8A7CE0C7BFC72C04790366338. This is a text review only, not audio acceptance.
