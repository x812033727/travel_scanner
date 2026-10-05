---
id: 2026-10-05-sfx-library-loudness-cue-sheet
title: Sound-effect library with measured loudness, a cue sheet in video.json, and an audibility check
status: in-progress
priority: P2
area: tools
owner: claude-fable-5-1-sfx
claimed_at: 2026-10-05T17:00:10Z
created_at: 2026-10-05T16:08:26Z
completed_at:
branch: claude/sfx-library-cue-sheet
depends_on:
  - 2026-10-03-illustrated-slides-lint-heuristics-the-shorts
scope:
  - tools/video/assemble/sfx.mjs
  - tools/video/assemble/sfx.test.mjs
  - tools/video/assemble/sound.mjs
  - tools/video/assemble/synthetic.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Sound-effect library with measured loudness, a cue sheet in video.json, and an audibility check

## Why

Sound effects are a fixed set of three (`assemble/sfx.mjs SFX_SOUNDS`: stamp, whoosh, pop)
placed by rules, with one `gain_db` for all, no measurement of the files' loudness, no cue
sheet, and `sfx_hash` covering only `{set, gain_db}`. The faceless-shorts repo (MIT) shows the
working shape: a catalogued library normalised to a loudness target, a declarative cue sheet
per video, and audibility verified by measurement, not by ear alone.

## Definition of done

- [x] Manifest v2 accepts any named sounds (the three rule-based ones still required) with
      `lufs_i` / `peak_dbtp` measured by a new `assemble sfx-measure` step (`ebur128`); each cue
      is gained to a per-sound target momentary loudness instead of one `gain_db`.
- [x] `video.json.sfx.cues[]` (`{scene | frame, sound, gain_db?}`) adds hand-placed cues on top
      of `sfxPlan`; `sfx_hash` covers the cues and the file hashes.
- [x] An audibility check (effects track momentary loudness at each cue versus the bed + voice
      mix, `ebur128` windows) fails assembly when an effect is masked (< 6 dB above the bed) or
      clips the voice; the illustrated smoke exercises it.

## Steps

- [x] `sfx.mjs`: manifest v2, measurement, per-sound gain, cue sheet merge, audibility windows;
      `sound.mjs` hashes; `synthetic.mjs` stand-ins; tests.
- [x] `core/drama.mjs`: `SFX_KEYS` += `cues`, `validateSfx`, `sfxHash`; `drama.test.mjs`.
- [x] `assemble/cli.mjs` step and `checks.json` metrics; `ILLUSTRATED.md` §配樂與音效.
- [ ] Receipt increment by an independent agent (`core/drama.mjs`, `core/drama.test.mjs`,
      `assemble/cli.mjs`, `assemble/assemble.test.mjs`).

## How to verify

```bash
node --test tools/video/assemble/sfx.test.mjs tools/video/assemble/assemble.test.mjs tools/video/core/drama.test.mjs
node tools/video/assemble/smoke.mjs --fixture illustrated --workdir /tmp/smoke-illustrated
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `core/drama.mjs`, `core/drama.test.mjs`, `assemble/cli.mjs`, `assemble/assemble.test.mjs`.
- Shorts (`shortSfxPlan`, `soundErrors`) are left out to stay clear of the Shorts tickets; a
  Shorts cue sheet is a follow-up.
- Claimed with `--force` over `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`: every
  item of that ticket is ticked except its own receipt rebind, which is not a precondition for
  this work (both tickets touch `core/drama.mjs`, each branch gets its own receipt increment).
- What landed (branch `claude/sfx-library-cue-sheet`), and the decisions behind it:
  - `sfx-measure` is a positional step of the assemble command (`assemble sfx-measure --set NAME
    | --slug S`), because the command table in `tools/video/cli.mjs` is outside this scope. It
    pads each file with a second of silence before `ebur128`: ffmpeg 6.1 reports no window at
    all for a 250 ms file on its own (I -70, M -120.7), with padding the loudest window is real.
  - Each cue's gain is computed toward its sound's target in the finished mix. The mix under the
    effects (voice and ducked bed) is measured first; its integrated loudness gives the gain the
    final loudnorm will add, so a target at -14 LUFS programme level becomes a level on the
    track. Verified on the smoke: every cue lands within 0.3 LU of its target.
  - `sfx_hash` in checks.json stays `sfxHash(doc)` because `state.mjs`, `package/cli.mjs` and
    `dubs/cli.mjs` (out of scope) compare it with exactly that; it now covers the cue sheet and
    the optional `sfx.sha256` (the set manifest's hash, which lists every file's hash, the same
    pattern as `music.sha256`). `sfx_set_hash` beside it adds the file hashes and the targets
    unconditionally, for a reader of the file; nothing out of scope compares it yet.
  - The audibility gate is against the ducked bed (>= 6 dB) plus the true-peak ceiling of the
    whole mix in the cue's window (loudnorm turns dynamic, squashing the voice, when the linear
    gain would pass -1 dBTP). The voice margin is recorded, not gated: a reveal pop sits on the
    line's first syllable by the rule, and 6 dB above the voice without clipping is impossible.
  - The synthetic set is now a measured version 2 set with a fourth sound (`chime`) so a cue
    sheet has a name only it can call; the Shorts smoke reads it as a version 1 placement still.
  - A version 1 set hashes as before (`sfxSetHash` pinned at `861f78911382114e` in the test) so
    the Shorts build id does not move.
- Noticed, not fixed: `dubs/cli.mjs` reuses `build/sfx.wav` on `sfx_hash` alone and never sees
  `sfx_set_hash`; `shorts/build.mjs` passes a version 2 set's resolved `gain_db` (-12) as the
  track gain, so Shorts effects are as quiet as the long video's were before this ticket.
- The illustrated fixture (`tools/video/core/fixtures/illustrated`) is in the dependency
  ticket's scope, so it carries no cue sheet; the cue tests build their sheets in memory.
- `core/drama.mjs` is also named by the worker-drama, round-2 and montage tickets (unclaimed).
