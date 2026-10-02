---
id: 2026-09-30-invalidate-dubs-when-target-pronunciation-changes
title: Invalidate dubs when target pronunciation changes
status: done
priority: P2
area: tools
owner: claude-opus-5-5-dubs-fingerprint
claimed_at: 2026-10-01T12:54:00Z
created_at: 2026-09-30T04:26:12Z
completed_at: 2026-10-01T13:11:50Z
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
  - tools/video/review/renewal.test.mjs
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
  `dubSpeechCurrent` (state.mjs), which calls `speechCurrent` (plan.mjs). A mismatch makes a
  track `stale` ("made with an older voice or pronunciation"). It also makes an over-budget fit
  `stale` instead of `over`, because its budgets were measured on the old speech. The worker
  re-runs `dub` for anything not current or skipped, as before.
- Legacy decision, revised after review: the first version made every record without a
  fingerprint `stale`. That would have flipped every dub on the host on deploy, including
  approved and uploaded ones, and kept them out of packages until `dub` was run by hand. Now a
  record without `speech_fingerprint` is judged by `dubs/<locale>/audio/cache.json`, which
  holds the clip key each line was synthesized with.
  - It is current when every line of today's plan (`dubRequests` with the record's
    `style_override`) has its line key or request key in the cache. Those are the keys `dub`
    would reuse a clip for.
  - A missing or unreadable cache, or any absent or different key, makes it `stale` with an
    explicit note: "made before dubs recorded their pronunciation" for a track, "the last run
    was over budget before dubs recorded their pronunciation" for an over-budget fit.
  - The same rule applies to over-budget `fit.json` records. Records with a fingerprint use
    only the fingerprint.
  - A `dub` rerun of a stale legacy dub retakes only the lines whose keys changed.
- One guard: for a legacy track, the cache stops counting as evidence when `fit.json` carries
  a fingerprint. That combination means a run with this code synthesized and did not write a
  new timeline (over budget), so the cache may hold clips the track does not.
- Remaining caveat: the cache can also run ahead of a legacy track when a run did not finish
  and left no fingerprinted `fit.json`. This covers a STOP file or a crash during synthesis, and
  an over-budget run of the old code. Such a track whose cached keys match today's plan reads as
  current although it was laid from older clips. This is rare, and the next `dub` run for that
  locale resolves it. Recorded dubs on the host have not been audited.
- Target-language dictionary: `loadProject` now also returns `shelfLexicon`, the raw shelf
  dictionary from the same directory it already used (so `--file` projects use their own shelf).
  `dubRequests` filters that by the target locale for both `dub` and the status and upload
  checks, so they cannot disagree. Before, the CLI re-read the file itself.
- Scope grew by five test files: `stages.test.mjs`, `captions-package.test.mjs`,
  `review/sync.test.mjs`, `automation/automation.test.mjs` and `review/renewal.test.mjs` (from
  #1077, merged meanwhile). They hand-write dub records with no clip cache to stand in for
  `dub`, so even under the cache rule those records are stale. Each now records
  `speech_fingerprint: dubFingerprint(project, locale)` the way `dub` does, a one-line change
  per file. `check:tasks` warns that `automation.test.mjs` is also in
  `2026-09-30-video-worker-moves-two-videos-at`, whose PR #999 is already merged (a stale claim).
- Verified with synthetic clips and mocked speech and ffmpeg:
  - `node --test tools/video/dubs/freshness.test.mjs tools/video/dubs/plan.test.mjs
    tools/video/dubs/dubs.test.mjs`: 24 pass.
  - `npm run test:tools`: everything passes except the known Windows-only
    `tts/check.test.mjs` test "a second transcript clears a line only Gemini misheard...".
  - The freshness tests cover a legacy record whose cache matches (current), a changed target
    alias (stale), and an unreadable or missing cache (stale). They also cover the
    fingerprinted-`fit.json` guard and a rerun that retakes one line.
