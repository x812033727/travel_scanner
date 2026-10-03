# Long anime production inputs

`long-anime-v1` preserves a long ensemble drama's story-body budget and declared
closed ending. It is an explicit policy on a native series request and its episode
`video.json`. The `anime` category or `anime-2d` drawing style alone does not grant
the duration or ending exceptions.

The Borrowed Dawn planning package remains a planning artifact. Its 12 documents,
120 episode outlines, historical support gaps and `ready_for_import: false` flags
are preserved. The adapter below prepares a separate, source-bound production
draft; it does not create or unlock a series, approve a document, start a worker,
generate media or publish anything.

## Runtime contract

The native request has `kind: "series"`, `category: "anime"`,
`style_preset: "anime-2d"`, `genre: "custom"`, `lead: "ensemble"`,
`production_policy: "long-anime-v1"`, `hands_off: false` and
`compilation: false`. The policy and runtime specification must be supplied
together. Unknown, incomplete or invalid policy markers fail validation.

| Runtime field | Borrowed Dawn | Validation |
| --- | ---: | --- |
| `body_target_seconds` | 1320 (22 minutes) | Whole minutes from 9 to 30, expressed as integer seconds |
| `op_ed_budget_seconds` | 180 (3 minutes) | Integer from 0 to 300 |
| `broadcast_slot_seconds` | 1800 (30 minutes) | Positive integer, at most 3600 |
| `slot_reserve_seconds` | 300 (5 minutes) | Integer from 0 to 900 |

These are the only four `runtime_spec` keys. Body + OP/ED budget + slot reserve
must equal the broadcast slot exactly. `SeriesIn.target_minutes` must equal the
body target in minutes; episode `video.json.target_minutes` is `[22, 22]` for this
source. The 30-minute slot is a scheduling allocation, not a generated-film
duration.

Measured story body must be within the fixed ±60-second tolerance: 1260–1380
seconds, or 21–23 minutes, for a 22-minute target. QA uses the current actual
unwrapped body timeline on the 30 fps grid. OP/ED cannot make an undersized body
pass. A passing delivery also needs the current speech and runtime-policy hashes,
matching presentation/final frame counts and the actual `final.mp4` SHA-256.
Changing runtime policy makes the old timeline and final checks stale; unchanged
voice clips remain reusable when TTS rebuilds the timeline.

Runtime receipts bind the series slug, episode, chapter, declared episode count,
open/closed status and finale flag as well as the budgets. Native script, audio,
final and publish approvals expire when this context changes, even if media bytes
remain identical. The API resolves the server-created episode rather than trusting
a worker's series label; estimated, stale or out-of-range evidence cannot be
approved manually. Publish also requires the current approved final receipt.

The three-minute OP/ED figure is a budget. Existing channel intro and outro
assets remain limited to 30 seconds each. Actual OP/ED must fit its budget, and
the actual presentation must fit `broadcast_slot_seconds - slot_reserve_seconds`.
The five-minute reserve is never rendered. Do not describe a body plus current
branding as an actual 30-minute episode or a completed three-minute OP/ED.

Ordinary drama keeps its 1–8-minute series guard and existing retention rules.
Knowledge videos, nonfiction stories, explainers, Shorts and compilations retain
their own contracts. This policy does not change their durations or create a
shortcut through `story`, `flat-explainer` or a compilation request.

## Narrative and writer contract

Each anime episode retains two distinct high-tension events, in the first and
second halves, with an event, stakes and continuing consequence. Character and
location references, setup/payoff lists and all five continuity-state fields are
required. Meaningful results or mystery payoffs remain necessary across rolling
four-episode windows, including chapter boundaries. These events are not
fabricated satisfaction beats for an unrelated genre preset.

Normal episodes still finish with tension at least 4 and varied ending types.
Only the declared last episode of a series with `open_ended: false` and an
explicit `closed_ending: true` may close with `emotion` and final tension 1–3.
Borrowed Dawn preserves episode 120's actual final score of 2 and its eight-year
epilogue. An earlier episode cannot use this exception; a closed last episode
must declare its resolution. The ending does not need a new enemy or sequel
crisis.

Long-anime writing uses bounded scene groups so a full 22-minute screenplay does
not depend on a single short-drama output budget. Its outlines, screenplay
verification and listener passes retain the anime event and continuity policy.
Directed silent action may occupy a shot's `action_seconds` from 1 to 8 with no
spoken lines; the timeline includes this real action without inventing speech.
The shot still needs visible causal motion. Pauses, frozen frames, repeated
narration and slow playback cannot supply missing story time. A screenplay's
estimated duration does not replace the measured audio and film gates.

## Offline adapter

Run from the repository root with Node 22 or newer:

```bash
node tools/video/production/anime-input.mjs --help
node tools/video/production/anime-input.mjs \
  --out /tmp/borrowed-dawn-production-draft.json
node --test tools/video/production/anime-input.test.mjs
```

The destination must be a new file outside the repository. The CLI refuses to
overwrite an existing file, including through a directory symlink into the
checkout. With no `--out`, it emits the complete draft JSON to stdout. An optional
`--source` accepts only this checkout's canonical
`docs/videos/series-plans/borrowed-dawn` directory. Symlink source paths, missing
or extra files, unsafe manifest paths and oversized files are rejected.

Before conversion, the adapter validates the full flat package's actual UTF-8
bytes, all source/support/generated SHA-256 receipts, strict JSON, source
semantics, every readable Markdown/continuity projection and every `body_json` /
`body_md` document twin. Rehashing forged twins does not make them valid.
The repository's fixed trusted validator supplies source semantics; the adapter
contains its own read-only render checks. Bundle copies of `build.mjs`,
`validate.mjs` and tests are hashed as inert text and are never executed or
imported. No Python installation, API environment, database or provider
credentials are needed for the Node adapter.

The resulting envelope contains:

- `series_request`: native `SeriesIn` fields, with slug
  `borrowed-dawn-production`, 120 episodes, 12 episodes per chapter, a closed
  ending, native tone `no-romance` and the runtime policy above.
- `source_bundle`: the exact complete portable planning package, including its
  original metadata and all support files.
- `source_binding`: the source path/slug, exact manifest hash, hashes of every
  file and the canonical complete bundle SHA-256. The canonical bundle hash
  matches the Python planning importer's `bundle_hash`.
- `documents` and `episodes`: the original 12 planning documents and all 120
  episode beats, including all 240 high-tension events. These are outlines,
  not complete screenplays or approval receipts.
- `source_metadata`: the original prose tone, runtime, support gaps and source
  note. Historical gaps remain intact even when this code supports the native
  policy.
- `production_requirements`: separate pending casting and design requirements,
  plus script, media, caption and approval requirements. Measured durations are
  `null`, the reserve is marked ungenerated, and readiness remains false.

The envelope sets `ready_for_import`, `ready_for_production`,
`admin_series_created`, `media_generated`, `published` and `approvals_recorded`
to false. Its document bodies do not gain voices, satisfaction beats, approvals
or production designs during conversion. Source voice provider/name assignments
are currently absent for all 16 listed characters. Character and narrator
casting, performance direction, source-bound auditions and listening acceptance
remain necessary.

Revalidate a draft against the current checkout before any later authorized
handoff:

```bash
node --input-type=module <<'JS'
import { readFileSync } from 'node:fs';
import {
  parseSourceJson, readAnimeSourceFiles, validateAnimeProductionInput,
} from './tools/video/production/anime-input.mjs';
const draft = parseSourceJson(
  readFileSync('/tmp/borrowed-dawn-production-draft.json', 'utf8'), 'draft',
);
validateAnimeProductionInput(draft, readAnimeSourceFiles());
console.log('Source binding, native request and pending requirements are current.');
JS
```

Any source-file change, including a review/support change with refreshed hashes,
invalidates an existing draft's binding. Rebuild and review that version.
Document, script, voice, design and final-media approvals bind their own source
and asset versions; an earlier version's approval is not transferred by this
adapter.

## Later native create and production handoff

The full draft envelope, `source_bundle`, `documents.json` and source `plan.json`
are not native series-create bodies. A later separately authorized create sends
only the reviewed `series_request` to the normal admin series-create endpoint.
That explicit policy creates a **paused** production series. The request carries
no `status`, `planning_only`, `planning_spec` or `source_binding` fields.

The existing `borrowed-dawn` planning row stays protected. Native create uses the
separate slug `borrowed-dawn-production`; it does not patch the planning row,
clear `planning_only` or bypass planning-only worker/action guards. Retain the
draft's source binding as the review handoff. Native creation alone neither
imports these documents nor records their approval.

Native documents and media reviews wait for the owner even when ordinary-series
automatic approval switches are enabled. Existing drafts can be submitted for
review while paused. A fresh native series with no documents has an explicit
Start Planning action; approving its outline pauses it again before production
can be resumed. Resuming requires the latest setting and outline approvals.
Changing an episode's beats still validates its chapter and neighboring payoff
windows; starting an episode rechecks the approved chapter and actual cached
beats before a production request is queued.

Native screenplay review payloads have a bounded 1 MiB envelope after their
explicit runtime/context declaration is validated against the actual series.
Ordinary reviews retain the 256 KiB envelope. This capacity does not supply
casting, approve a screenplay or execute the adapter's source documents.

Before activation, use the documented document/script workflow to preserve and
review the source content, assign consistent zh-TW character and narrator
voices, approve character designs and shot looks, and prepare a complete
screenplay, timed storyboard/animatic and representative pilot. Provider
capability checks include actual ages and appearances; the adapter does not
select or verify a production provider. Casting/design selection is distinct
from rendered or listened acceptance. Paid auditions, image/video generation
and pilot production require their own authorized workflow and existing budget
and retake controls.

Chinese audio, the complete film and switchable CC are accepted first. Drama
character dubbing in ja/ko/en follows its own implementation and acceptance
status; this duration policy does not add that capability. Existing media QA,
package, review, language and owner publication gates still apply. Planning
validation cannot establish narrative quality, natural performance or a
finished film.

## Validation evidence

The adapter's tests exercise the real source pack and native field values;
exact 12-document/120-episode/240-event coverage; final-episode closure;
actual-file hash tampering; rehashed Markdown, JSON and continuity drift;
source semantic failures; duplicate-key/nonfinite JSON; unsafe paths/symlinks;
inert bundle code; missing voices; source-version invalidation; local-only CLI
output and overwrite refusal. The direct CLI is also run with unreachable
proxy settings to establish that it does not depend on a live API or provider.

An offline cross-language check validates the emitted request with
`SeriesIn.model_validate`, the complete portable source with
`planning.validate_bundle`, and equality of Node/Python canonical bundle hashes.
These checks passed without a database session, paid generation or a remote
write. For the wider pipeline, run the affected API anime policy/series and
migration suites, Node series/writer/timeline/duration/QA/package/review suites,
the web editor/review checks and `npm run check:tasks`. Those regressions cover
ordinary boundaries, invalid markers, early-finale rejection, real body versus
OP/ED/slot checks and paused creation; they do not claim a produced 120-episode
season.

Related contracts: [SERIES.md](SERIES.md), [DRAMA.md](DRAMA.md),
[DRAMA-FLOW.md](DRAMA-FLOW.md), [LANGUAGES.md](LANGUAGES.md) and
[animation production](../../.agents/skills/youtube-video/references/animation-production.md).
