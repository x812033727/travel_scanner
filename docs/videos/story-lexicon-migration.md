# Pinning a story that started before per-story dictionaries

[`story-lexicon-integration.md`](story-lexicon-integration.md) pins each new story's pronunciation
dictionary before its first chapter. `initializeStoryLexicon` refuses a story that already started,
so a story that wrote chapters before that release (#1548) was deployed stops with
`story pronunciation input is held: STORY_LEXICON_MIGRATION_REQUIRED` and never reaches paid speech.

When such a story has not synthesized any narration yet, nothing it produced depends on the shared
dictionary's pronunciations. Pinning it now is the decision genesis would have made, so
`tools/video/core/lexicon-migration.mjs` makes exactly that decision, once, and refuses everything else.
Production's B25 (`story-adapt-seiko-quartz-astron`: six chapters written, checked and heard, script
approved, no timeline, no audio) is the case it was written for.

## Command

```bash
node tools/video/cli.mjs story-lexicon-migrate --slug <slug> [--workdir <base>] [--json]          # dry run
node tools/video/cli.mjs story-lexicon-migrate --slug <slug> [--workdir <base>] --apply           # pin it
```

Without `--apply` nothing is written: it prints `allowed`, `refused` or `already_pinned`, each
precondition with the error code it would raise, the shared dictionary's SHA-256, the plan names it
would seed, and the snapshot SHA-256 it would pin. Exit 0 when allowed, applied or already pinned;
exit 1 when refused or when the apply itself fails.

## Preconditions

Checked in this order, and again under both leases immediately before anything is written:

| check | refuses with |
| --- | --- |
| slug is not A01 (`story-rolling-suitcase-v2`) | `STORY_LEXICON_MIGRATION_EXCLUDED` |
| no docs `pending.json` and no work-volume intent | `LEXICON_TRANSACTION_INCOMPLETE` |
| no project or global `STOP` | `LEXICON_STOPPED` |
| `series.json` kind or `video.json` category is `story` | `STORY_LEXICON_MIGRATION_NOT_A_STORY` |
| the work directory is this story's: it exists, `auto.json` reads, its `slug` is this slug, it has `story` state, and `story/chapters` has a chapter file | `STORY_LEXICON_MIGRATION_WORKDIR_UNPROVEN` |
| no `story/recheck-audit` (A01's audit chain) | `STORY_LEXICON_MIGRATION_AUDIT_PRESENT` |
| no `timeline.json` | `STORY_LEXICON_MIGRATION_TIMELINE_PRESENT` |
| no file under `audio/` and no `narration.wav` | `STORY_LEXICON_MIGRATION_AUDIO_PRESENT` |
| `approvals.json` has only `outline`, `script` or `look` | `STORY_LEXICON_MIGRATION_APPROVAL_PRESENT` |

A story already in snapshot mode is read and returned unchanged, so a rerun is harmless. A story with
no chapter file is left to the worker's normal genesis, and an unreadable `approvals.json` counts as a
later approval. Every refusal happens before either lease is taken, so a refused run writes nothing,
not even a `LEASE` file or an intent.

### The work directory must be the right one

Every check after the first four reads the work directory, and an empty directory passes all of
them. A forgotten `VIDEO_WORKDIR` or a wrong `--workdir` would therefore look like a story with no
narration, which is why `workdir_is_this_story` demands positive proof instead. On the production
host run it where the worker runs, with the worker's work base: inside the container that is
`VIDEO_WORKDIR=/var/lib/mokaair/video-work` (or `--workdir /var/lib/mokaair/video-work`), and the
command appends the slug itself. Read the dry run's `workdir_is_this_story` line before `--apply`.

## What it writes

The same bytes `initializeStoryLexicon` writes for a new story: the current shared
`docs/videos/lexicon.json` plus each plan name's Latin tokens (from `series.json` `names`) as `null`
when absent, genesis version, genesis event (`reason: "initial_snapshot"`, sequence 1) and
`current.json`. A test asserts byte equality. The strict reader accepts no other genesis, so the
event cannot carry the migration; it is recorded instead in:

- `docs/videos/<slug>/story-lexicon/migrations/<event_sha256>.json`, immutable, which the reader
  ignores: `reason: "started_before_pinning"`, the shared dictionary's SHA-256 at migration time, the
  seeded terms, the preconditions checked and the time.
- the work and docs intents and the work receipt (`migration`, `migration_sha256`).

The transaction is the one `lexicon-store.mjs` uses: project LEASE and dictionary-writer LEASE, both
intents, immutable files, current pointer, strict read-back, receipt, then clearing both intents. A
crash after the receipt is recovered by `recoverCommittedStoryLexicon` unchanged; earlier crashes stay
held for review. The function is a copy of `publish`, kept apart only because the A01 integration
task still holds `lexicon-store.mjs`; it can be shared once that task closes.

## Not covered

A01 is out of scope by slug and by its audit directory. Its 80-event chain needs the separate,
independently reviewed append-only transition in `story-lexicon-integration.md`. A story with any
narration timeline, audio or audio-or-later approval needs a reviewed decision about whether that
narration still matches; this command will not make it.

Running it on the production host is an operator step and is not part of the change that adds it.
