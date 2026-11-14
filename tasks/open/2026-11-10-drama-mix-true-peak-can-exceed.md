---
id: 2026-11-10-drama-mix-true-peak-can-exceed
title: Drama mix true peak can exceed -1 dBTP when TTS lines clip
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-10T23:57:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
---

# Drama mix true peak can exceed -1 dBTP when TTS lines clip

## Why

`assemble` for a narrated drama (奇聞檔案局, 品牌故事) mixes the narration with the music bed and
normalises the mix with a two-pass, linear `loudnorm` to -14 LUFS / TP -1
(`tools/video/assemble/drama.mjs` `mixFilter`, `measureMixArgs`, `mixArgs`). Linear loudnorm moves
the whole mix by one gain and never limits, so if the narration itself has inter-sample peaks near
0 dBTP the cut keeps them. `checkLoudness` (`plan.mjs`) then fails the cut with
`CHECK true peak 0.1 dBFS, above -1` and exit 1, and nothing in video.json can fix it.

2026-11-10, curio-s14-v2: 140 Gemini (Sulafat) lines, several with true peaks above 0 dBTP
(mv901 +0.8, mv811 +0.6, mv415 +0.6, mv318 +0.5). The cut measured -14.1 LUFS, true peak +0.1 dBFS
and failed. curio-s13-v2, same voice and day, passed at -1.9 dBFS, so it depends on the lines.

## Definition of done

- [ ] A narrated drama whose TTS lines peak above 0 dBTP assembles with the cut's true peak at or
      below -1 dBTP and the integrated loudness still at -14 LUFS, without re-recording any line.
- [ ] Cuts whose narration already peaks low come out unchanged (or the change is a deliberate,
      documented re-mix of unapproved cuts only).

## Steps

- [ ] Limit the voice before it is mixed and measured, e.g. `alimiter=limit=0.79:level=0` after
      `${STEREO}` in `mixFilter` (and `effectsFilter`), or a true-peak-aware limiter after loudnorm.
- [ ] Decide whether the change belongs in a hash the approvals or checks.json bind (a re-mix of an
      approved final must not happen silently).
- [ ] Test in `drama.test.mjs`: the filter string carries the limiter.

## How to verify

Re-assemble curio-s14-v2 (or any cut with a hot line) and read the last line of `assemble`:
`true peak` at or below -1 dBFS, `-14 LUFS`, exit 0.

## Notes

- Workaround used on 2026-11-10 for curio-s14-v2 only: the line above patched into a local checkout
  of `drama.mjs`, assemble + captions + qa re-run (the 140 segments were reused, only the sound was
  re-mixed), then the file was restored. Result: -14 LUFS, true peak -2.2 dBFS, qa 11/11. The
  narration, timeline and storyboard approvals were not touched.
- Dubs (`dubs/encode.mjs`) reuse `mixArgs`; check them too.
