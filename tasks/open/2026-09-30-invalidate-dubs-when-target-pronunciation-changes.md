---
id: 2026-09-30-invalidate-dubs-when-target-pronunciation-changes
title: Invalidate dubs when target pronunciation changes
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-30T04:26:12Z
completed_at:
branch:
depends_on:
  - 2026-09-29-dubs-spell-out-app-as-a
scope:
  - tools/video/core/state.mjs
  - tools/video/core/stages.mjs
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/freshness.test.mjs
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

- [ ] A changed pronunciation or voice in a target locale makes its old dub stale and
      excludes it from the upload package until it is regenerated.
- [ ] Unused dictionary entries, equivalent filtered aliases and another locale's changes
      do not invalidate an unaffected dub.
- [ ] Missing fingerprints in legacy timelines are handled explicitly and safely, including
      tracks whose last attempt was over budget; reruns reuse unchanged per-line clips.
- [ ] Chinese dubs of non-Chinese originals resolve the raw shelf dictionary by target
      language, including `--file` projects.

## Steps

- [ ] Define a stable fingerprint of the target's effective voice and request contents.
- [ ] Persist it with successful and over-budget dub records, and compare it in status and
      upload eligibility without paying for synthesis during these read-only checks.
- [ ] Add regressions covering changed target aliases, legacy records, unaffected terms,
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
