# DuckDB fifth film — complete Korean author draft

This is an offline text draft for `duckdb-agent-full-export`, authored by
`/root/branding_restore`. It has not been adopted into the repository or work
directory. Root must independently review all 111 source/target pairs and the
metadata before a later normal `i18n-merge`.

Review these files:

- `ko.draft.reviewed.todo.json`: complete native worksheet, changing only `text`.
- `source-target-complete-111.md` and `.json`: all 111 Chinese/Korean pairs and six
  untimed chapter titles; JSON also contains full title, description, tags and
  thumbnail source/target fields.
- `pass2-critique.json`: ten actual author corrections, preserving the first draft.
- `author-pass3-semantic-ledger.json`: author notes for every line and the numeric,
  predicate, JSON, code-name, provenance and publication-link checks.
- `ko.native-pure-merge-preview.json`: native `mergeSheet` result in scratch only.
- `ko.metadata-compose-untimed-preview.json`: native title/description composition
  with `timeline: null`; no real or estimated chapter timestamps.
- `protected-before-and-after.json`: all 13 protected file hashes and sizes unchanged,
  including source/claims/script, both adopted EN and JA, lexicon and native modules.

The same author completed three passes: complete drafting; full reread and
critique with eight line corrections plus thumbnail/description corrections; then
full 111-line semantic review and native pure validation. This is not an
independent review or root approval. Internal glossary assistance supplied no
independent acceptance claim.

The reviewed draft explicitly says the preview displays 40 rows in total from
1,200 inputs, while 1,160 rows are omitted from display. The strict filter produces
480 delivered records with `actual_days > promised_days`; the revised `>=` query
produces a separate 720-record list, including 240 with zero lateness. These lists
serve different requirements. In-transit NULL is not zero, and the original 960/240
status counts and R2/R3 counts of 240 each remain distinct.

The intentional typo is `actual_day` versus `actual_days`; the computed alias is
`days_late`. Startup text plus one valid JSON line does not mean DuckDB emitted
broken JSON or that a real third-party consumer failed. The metadata preserves
the fictional CC0 exercise, same DuckDB 2.0.0 binary, existing CSV/SQL/COPY/Parquet
capabilities, absence of an AI model or performance/token/cost benchmark, and both
immutable public URLs at commit `410633ab4addde4d4590dfecc0e138d48d072d3b`.

Native pure validation exited 0 with zero merge problems and zero notes. All
111 lines and six chapters refresh as current in an in-memory worksheet. The
composed Korean title includes the native CC suffix; composed description is
2,732 UTF-8 bytes. The instrumented pure region made zero network calls,
subprocess calls and file-write attempts. Native source hashes were generated
only by `mergeSheet`.

No CLI merge, work `i18n` write, auth/API/paid request, TTS, ASR, media stage, state,
approval, repository edit, git action or binary redistribution occurred. Korean
audio duration, cue timing, reading fit, thumbnail rendering and backend delivery
remain untested. EN and JA are still the only adopted foreign texts; this draft
does not change that production count. The PT and ES unknown request holds remain
outside this task.
