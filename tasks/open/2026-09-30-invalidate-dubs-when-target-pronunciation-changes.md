---
id: 2026-09-30-invalidate-dubs-when-target-pronunciation-changes
title: Invalidate dubs when target pronunciation changes
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-dubs-fingerprint
claimed_at: 2026-10-01T12:54:00Z
created_at: 2026-09-30T04:26:12Z
completed_at:
branch: claude/dubs-target-fingerprint
depends_on:
  - 2026-09-29-dubs-spell-out-app-as-a
scope:
  - tools/video/core/state.mjs
  - tools/video/core/stages.mjs
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/freshness.test.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/dubs/captions-package.test.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/automation/automation.test.mjs
---

# Invalidate dubs when target pronunciation changes

## Why

Dub status and upload eligibility check the source narration's `speech_hash` and the
translation's text hash, but do not bind the target voice's actual pronunciation requests.
Changing a target alias can therefore leave a finished dub marked `current` and eligible
for packaging even though running `dub` would generate different speech. Workers that skip
current locales will not discover the changed request.

The App alias correction exposed this existing gap: a zh-TW source stays unchanged while
English `App Store` changes from `A P P Store` to `App Store`. The request and clip keys
change, but the source and translation hashes do not. A direct `dub` rerun correctly
regenerates those clips; status and upload selection need the same freshness guarantee.

## Definition of done

- [x] A changed pronunciation or voice in a target locale makes its old dub stale and
      excludes it from the upload package until it is regenerated.
- [x] Unused dictionary entries, equivalent filtered aliases and another locale's changes
      do not invalidate an unaffected dub.
- [x] Missing fingerprints in legacy timelines are handled explicitly and safely, including
      tracks whose last attempt was over budget; reruns reuse unchanged per-line clips.
- [x] Chinese dubs of non-Chinese originals resolve the raw shelf dictionary by target
      language, including `--file` projects.

## Steps

- [x] Define a stable fingerprint of the target's effective voice and request contents.
- [x] Persist it with successful and over-budget dub records, and compare it in status and
      upload eligibility without paying for synthesis during these read-only checks.
- [x] Add regressions covering changed target aliases, legacy records, unaffected terms,
      locale isolation and a successful rerun becoming current again.

## How to verify

`node --test tools/video/dubs/freshness.test.mjs tools/video/dubs/plan.test.mjs
tools/video/dubs/dubs.test.mjs`, followed by `npm run test:tools` and `npm run check:tasks`.
Use synthetic clips and mocked speech/encoding services; no production or paid calls.

## Notes

- 2026-09-30 independent review on main `72069973` plus the App correction reproduced this
  with a temporary status-only fixture: unchanged zh-TW source; English translation
  `Open the App Store.`; old request key `1fc643fc28e51477`, new key `97587decd3adf6cb`.
  An old timeline with the same source/translation hashes still returned `current` from
  `dubsStatus`, and `dubsForUpload` still included `en`. This did not inspect real audio.
- Keep this separate from the request-text correction. Existing recordings and publication
  status have not been audited, and regeneration or publication requires its own scope.
- Recheck PR, branch, worktree and active-claim ownership before claiming; this scope
  overlaps the predecessor until that PR lands.
- 2026-10-01 (claude-opus-5-5-dubs-fingerprint). The fingerprint is `speechFingerprint` in
  `tools/video/dubs/plan.mjs`: a hash of every line's clip key (`[id, key]`) from
  `planRequests`. A clip key already binds the effective voice (name, model, style) and the
  line's parts with the aliases actually applied, so unused entries, aliases the target
  discards alike, and another locale's edits leave it unchanged. It is computed from the plan
  alone: no network or paid call. `dub` writes it as `speech_fingerprint` into
  `dubs/<locale>/timeline.json` and into an over-budget `fit.json`, with `style_override` (the
  `--style` it was made with, else null) so a hand-styled dub is compared in its own style.
- `dubsStatus` (state.mjs) and `currentDub`/`dubsForUpload` (stages.mjs) compare it through
  `speechCurrent`. A mismatch makes a track `stale` ("made with an older voice or
  pronunciation"), and an over-budget fit `stale` instead of `over`, because its budgets were
  measured on the old speech. The worker re-runs `dub` for anything not current or skipped, as
  before.
- Legacy decision: a record without `speech_fingerprint` (every dub made before this change)
  is `stale`. This applies to tracks and to over-budget fits, each with its own note ("made before
  dubs recorded their pronunciation" / "the last run was over budget before dubs recorded their
  pronunciation"). Nothing proves which aliases such a track was made with, so it is never
  packaged until `dub` runs again. That rerun synthesizes only lines whose clip keys changed:
  the other clips come from `audio/cache.json`, so an unaffected legacy dub costs a status
  call and an encode. The regression shows zero speech requests for that rerun.
- Target-language dictionary: `loadProject` now also returns `shelfLexicon`, the raw shelf
  dictionary from the same directory it already used (so `--file` projects use their own shelf).
  `dubRequests` filters that by the target locale for both `dub` and the status and upload
  checks, so they cannot disagree. Before, the CLI re-read the file itself.
- Scope grew by four test files: `stages.test.mjs`, `captions-package.test.mjs`,
  `review/sync.test.mjs` and `automation/automation.test.mjs` hand-write dub records to stand in
  for `dub`. Under the legacy rule those records are stale, so each now records
  `speech_fingerprint: dubFingerprint(project, locale)` the way `dub` does. `check:tasks`
  warns that `automation.test.mjs` is also in `2026-09-30-video-worker-moves-two-videos-at`,
  whose PR #999 is already merged (a stale claim); the edit here is one line in `fakeDub`.
- Verified: `node --test tools/video/dubs/freshness.test.mjs tools/video/dubs/plan.test.mjs
  tools/video/dubs/dubs.test.mjs`: 24 pass. `npm run test:tools`: 1032 pass, 1 skipped, 1
  fail (the known Windows-only `tts/check.test.mjs` "a second transcript clears a line only
  Gemini misheard..."). All use synthetic clips and mocked speech and ffmpeg.
- Not done here: existing recorded dubs on the host have not been audited. After deploy,
  `status` reports every older dub as stale until `dub` runs again for it. Real dubs keep their
  per-line cache, so that rerun re-encodes; it re-synthesizes only lines whose request changed.
- Consequence to watch, not verified here: the worker re-dubs only locales the site still
  reports as in the making. An older dub that is already approved or uploaded stays stale in
  `status`, and a later `package`, `review-push --gate final` or `languages` batch leaves it
  out until someone runs `dub --locale <it>` by hand. That is the safe direction (nothing
  unproven is sent), but a languages batch that omits an already-uploaded dub has not been
  checked against the site's handling.
