---
id: 2026-10-22-measure-generated-lyria-duration-and-guard
title: Measure generated Lyria duration and guard music loop seams
status: review
priority: P1
area: tools
owner: codex-gpt6-lyria-duration-guard
claimed_at: 2026-10-22T02:57:00Z
created_at: 2026-10-22T01:02:17Z
completed_at:
branch: codex/lyria-duration-guard
depends_on: []
scope:
  - tools/video/media/music.mjs
  - tools/video/assemble/sound.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/media/music-duration.test.mjs
  - tools/video/media/clips.test.mjs
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

- [x] A generated music artifact records its **decoded actual duration** separately
      from the requested duration. The stage output and manifest do not report the
      request as delivered length, including on cache reuse.
- [x] When the source is shorter than the planned soundtrack, the assembly path
      either stops with an actionable hold or uses an explicit, measured loop plan
      whose joins pass an audio check. A 174-second answer for a 600-second
      request cannot silently become a passing long-film music receipt.
- [x] The policy works for a sufficiently long generated track and a short track;
      failures preserve the existing artifact, job identity, hash and ledger, with
      no automatic paid replacement.

## Steps

- [x] Trace the request, download, cache and manifest through `music.mjs`, then
      the manifest read and FFmpeg input through `sound.mjs`, `cli.mjs` and
      `drama.mjs`. Decide whether this route should hold or make a checked loop;
      document the rule in the task before changing code.
- [x] Measure the decoded file duration after download and on reuse. Keep the
      requested duration as request metadata, and expose the actual duration in
      the persisted receipt and console output.
- [x] Enforce the selected short-track rule before a final music/assemble success;
      if looping is allowed, record join positions and inspect or measure the joins.
- [x] Add tests using decodable short audio. Existing `clips.test.mjs` fakes
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

2026-10-22 implementation choice before editing code: retain the paid generated file, job key, hash and ledger; measure its **fully decoded** duration after download and on cache reuse. If a generated track is shorter than the cut, `assemble` will stop before encoding with an actionable message rather than silently repeating it. This is the ticket's allowed hold route. A future explicit loop and seam QA can resume the film with the retained source; this change will not buy another track automatically. The existing `clips.test.mjs` media stub returns literal `ID3` text rather than decodable audio, so its one music-generation fixture must become a real decodable short MP3; the four other tickets mentioning that file are unclaimed/open when this scope was added.

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

2026-10-22 implementation and checks: `music` now locates FFmpeg before a paid
request, fully decodes the downloaded or cached file, writes distinct
`requested_seconds` and `actual_seconds`, and returns an owner hold on a short
answer while preserving the same paid file, key, SHA and ledger. `assemble`
checks the generated file's SHA and measured duration against the current cut
before encoding segments. A one-second decodable MP3 exercises the short and
cache paths; a two-second MP3 exercises both short and sufficient assembly
inputs. With the supported bundled Node, the focused media and assembly suite
passed; `npm run check:tasks` and `git diff --check` passed. The
retained C03 MP3 was read only: FFmpeg full decode ended at 174.001633 s,
ffprobe reported 174.001583 s and 4,182,166 bytes, while its old manifest still
says `seconds: 600`. No vendor call or media rewrite occurred in that check.
Draft PR #1669 is stacked on C03 #1652; the ticket moved to review after the
push. Neither PR was merged or deployed.

Independent review of the first PR head found two bypasses, now corrected in
the same draft: `dub` called the shared music lookup without an explicit cut
length, and `Stage.generate` could buy a replacement after a missing or changed
cached file. The shared lookup now requires full-decode evidence for every
generated track and infers the cut length from the saved timeline when its
caller does not pass one. The `music` command validates a retained manifest or
cache entry before entering `Stage.music`; a prior paid or reserved music row
without a recoverable artifact or pending job stops for owner reconciliation.
Tests cover missing cache, corrupt paid bytes, changed request key and the dub
caller shape; 53 focused media/assembly tests pass. The illustrated dub fixture
hit a transient Windows `EPERM` while renaming its unrelated speech journal in
the combined run; the exact failing test passed on a focused rerun. The full
`test:tools` run was stopped after an extended silent period, so it is not
recorded as passed.

Existing request-only manifests may still look complete in `pipelineStatus`
until `music` is rerun for cached measurement. `assemble` rejects them; status
reconciliation has its own open follow-up task
`2026-10-22-reconcile-legacy-generated-music-manifests-in`, dependent on the
active A01 lexicon task that owns `tools/video/core/state.mjs`.
