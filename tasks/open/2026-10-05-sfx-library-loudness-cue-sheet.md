---
id: 2026-10-05-sfx-library-loudness-cue-sheet
title: Sound-effect library with measured loudness, a cue sheet in video.json, and an audibility check
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:26Z
completed_at:
branch:
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

- [ ] Manifest v2 accepts any named sounds (the three rule-based ones still required) with
      `lufs_i` / `peak_dbtp` measured by a new `assemble sfx-measure` step (`ebur128`); each cue
      is gained to a per-sound target momentary loudness instead of one `gain_db`.
- [ ] `video.json.sfx.cues[]` (`{scene | frame, sound, gain_db?}`) adds hand-placed cues on top
      of `sfxPlan`; `sfx_hash` covers the cues and the file hashes.
- [ ] An audibility check (effects track momentary loudness at each cue versus the bed + voice
      mix, `ebur128` windows) fails assembly when an effect is masked (< 6 dB above the bed) or
      clips the voice; the illustrated smoke exercises it.

## Steps

- [ ] `sfx.mjs`: manifest v2, measurement, per-sound gain, cue sheet merge, audibility windows;
      `sound.mjs` hashes; `synthetic.mjs` stand-ins; tests.
- [ ] `core/drama.mjs`: `SFX_KEYS` += `cues`, `validateSfx`, `sfxHash`; `drama.test.mjs`.
- [ ] `assemble/cli.mjs` step and `checks.json` metrics; `ILLUSTRATED.md` §配樂與音效.
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
- `core/drama.mjs` is also named by the worker-drama, round-2 and montage tickets (unclaimed).
