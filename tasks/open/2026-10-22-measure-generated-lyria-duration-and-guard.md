---
id: 2026-10-22-measure-generated-lyria-duration-and-guard
title: Measure generated Lyria duration and guard music loop seams
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-22T01:02:17Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/music.mjs
  - tools/video/assemble/sound.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/media/music-duration.test.mjs
  - tools/video/assemble/music-loop.test.mjs
---

# Measure generated Lyria duration and guard music loop seams

## Why

During C03 (`story-everyday-moleskine-c03`), `music --dry-run` requested a 600-second
Gemini Lyria 3.5 track. The completed `music` command wrote
`music/manifest.json` with `seconds: 600`, but `ffprobe` and a full FFmpeg decode
of the downloaded MP3 measured **174.0016 seconds** (4,182,166 bytes). That
manifest field and the command's success text currently describe the requested
length as though it were the delivered length. `assemble` uses FFmpeg
`-stream_loop -1` to fill the film, so this track can repeat at least three
times with unchecked joins. C03 media and its ledger must be retained; this is
a tool defect affecting other long videos, not a reason to re-buy the track.

## Definition of done

- [ ] A generated music artifact records its **decoded actual duration** separately
      from the requested duration. The stage output and manifest do not report the
      request as delivered length, including on cache reuse.
- [ ] When the source is shorter than the planned soundtrack, the assembly path
      either stops with an actionable hold or uses an explicit, measured loop plan
      whose joins pass an audio check. A 174-second answer for a 600-second
      request cannot silently become a passing long-film music receipt.
- [ ] The policy works for a sufficiently long generated track and a short track;
      failures preserve the existing artifact, job identity, hash and ledger, with
      no automatic paid replacement.

## Steps

- [ ] Trace the request, download, cache and manifest through `music.mjs`, then
      the manifest read and FFmpeg input through `sound.mjs`, `cli.mjs` and
      `drama.mjs`. Decide whether this route should hold or make a checked loop;
      document the rule in the task before changing code.
- [ ] Measure the decoded file duration after download and on reuse. Keep the
      requested duration as request metadata, and expose the actual duration in
      the persisted receipt and console output.
- [ ] Enforce the selected short-track rule before a final music/assemble success;
      if looping is allowed, record join positions and inspect or measure the joins.
- [ ] Add tests using decodable short audio. Existing `clips.test.mjs` fakes
      MP3 bytes with `ID3` text, so it cannot prove duration or join behavior.

## How to verify

Run `node --test tools/video/media/music-duration.test.mjs
tools/video/assemble/music-loop.test.mjs` and the affected video tests. With
the retained C03 MP3, compare the manifest's actual duration to
`ffprobe -v error -show_entries format=duration,size -of json <file>` and run
`ffmpeg -v error -xerror -i <file> -f null -` for a full decode. Check that the
600-second request / 174.0016-second answer produces the selected explicit
hold or a verified loop receipt, without another vendor request.

## Notes

The C03 measurement above came from the production handoff on 2026-10-22;
this ticket audit read the tool path, not the media bytes. `music.mjs` computes
`trackSeconds()` (maximum 600), sends that value to `Stage.music()`, and writes
it as `manifest.seconds` without probing the download. The Gemini adapter
(`apps/api/app/video_media/providers/gemini_music.py`) requests an **about**
length in prompt text; that is no guarantee of actual duration.
`sound.mjs` checks the manifest's mix hash and file path but not duration;
`drama.mjs` loops the input indefinitely to the film length. No existing open
task was found for this duration mismatch. Scope is limited to the listed tool
files and new tests; no C03 files, media or provider code are assigned here.
