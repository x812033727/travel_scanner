---
id: 2026-10-07-look-clips-music-and-speech-commands
title: Look, clips, music and speech commands take the project lease and check STOP before their canonical writes
status: done
priority: P2
area: tools
owner: claude-opus-5-5-lease-gaps
claimed_at: 2026-10-07T02:28:04Z
created_at: 2026-10-07T02:01:52Z
completed_at: 2026-10-07T03:09:18Z
branch: claude/sharp-bardeen-ob6fn9
depends_on:
  - 2026-10-04-native-video-project-stop-and-producer-exclusion
scope:
  - tools/video/media/look.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/music.mjs
  - tools/video/media/media.test.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/core/project-lease.mjs
  - tools/video/core/project-lease.test.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - docs/videos/AUTOMATION.md
  - .agents/skills/deploy/SKILL.md
  - .claude/skills/deploy/SKILL.md
  - .agents/skills/prod-host-ops/SKILL.md
  - .claude/skills/prod-host-ops/SKILL.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Look, clips, music and speech commands take the project lease and check STOP before their canonical writes

## Why

`2026-10-04-native-video-project-stop-and-producer-exclusion` added the project lease
(`tools/video/core/project-lease.mjs`, `<workdir>/LEASE`), and STOP fences. They cover:
- the worker's unit and the owner retry;
- every paid media request and judge call (`Stage.hold()` in `media/stages.mjs`);
- the `keyframes` command at entry;
- the worker's own writes (`Automation.fence()`).

Commands that other code or a person runs by hand are still open between their paid calls:
- `look`, `clips` and `music` write their manifests, choices and sheets with no lease and no STOP check at entry.
- `tts`, `dub` and `check-audio` have their own STOP handling, but no lease.
- `discuss.mjs restoreVideo` puts back video.json after an unusable answer. It runs inside a step that now holds the lease through `fence()`, but it has no fence of its own.

A person who runs one of these while the worker holds the project, or while a STOP file is
there, can still change the project's canonical files.

## Definition of done

- [x] `look`, `clips` and `music` refuse to start under STOP or without the lease, as `keyframes` does (`mayWrite` in `media/keyframes.mjs`). Each one exits without writing anything, and a test shows it.
- [x] `tts`, `dub` and `check-audio` take the lease (or join the worker's) before their first paid request or write. Their existing STOP behaviour and exit codes stay as they are.
- [x] `restoreVideo` in `discuss.mjs` checks the fence before writing video.json.
- [x] Losing the lease inside a command the worker runs in-process sets the video aside, as `fence()` does, rather than blocking it as the owner's (exit 3). Review nit 6 of 2026-10-07.
- [ ] Inside the worker, a media command that finds no unit or step lease refuses instead of taking the lease until `auto` exits (review nit 7). No such call exists today, so this guards future code.
- [ ] Optional: a lease held for more than a few hours shows on `/admin/videos` (holder, since when), not only in the worker log.
- [x] `docs/videos/AUTOMATION.md` and the `deploy` / `prod-host-ops` skills say to run video commands by hand with
      `docker compose exec video-worker`, never `docker compose run`. A `run` container shares the fixed
      hostname but has its own pid namespace, so it could judge a live lease dead and take it over (re-review of
      2026-10-07). Widen the scope to those files when this is claimed.
- [x] `fence()` on a series document's discussion does not create a work directory named after the series slug
      (`acquireProjectLease` makes the directory; re-review nit).

## Steps

- [x] Reuse `requireProjectLease` / `mayWrite` and do not add a second mechanism.
- [ ] Run `node tools/video/long-form/cli.mjs check`. If a bound file changes, an independent reviewer adds an increment to `docs/videos/long-form/review.md` (scope it in then).

## How to verify

```bash
node --test tools/video/media/*.test.mjs tools/video/tts/*.test.mjs tools/video/dubs/*.test.mjs tools/video/automation/*.test.mjs
npm run test:tools
```

## Notes

- The lease is taken over only when its holder is certainly dead. That means the same host and the same boot, and the pid is free or now belongs to another process, judged by `/proc` start time.
- `docker-compose.prod.yml` gives `video-worker` the fixed `hostname: video-worker`, so a lease that a worker killed mid-unit by a deploy leaves behind is taken over by the next worker.
- A lease from another container (for example a `docker compose run`) still counts as held until a person removes it.

### 2026-10-07 implementation (claude-opus-5-5-lease-gaps)

- `media/stages.mjs` exports `mayWriteProject(ctx, workdir, owner)`. It returns false under STOP and raises an owner MediaError when the lease is held elsewhere. `keyframes`, `look` (drawing and `--choose`), `clips`, `clips import` and `music` (generated, and the owner's own track) call it right before their first write.
  - `clips import` under a STOP that is already there now stops before it copies the clip in. The existing test's message changed; it still asserts that nothing was recorded or held.
- `tts`, `dub` and `check-audio` call `requireProjectLease(..., { as })` before their first request or write. The new `as` option turns a refusal into the command's own SpeechError, so it exits 3. Their STOP handling and exit codes are unchanged.
- `flow.mjs`:
  - `restoreVideo()` (the discussion's revert) checks the lease but not STOP, so a STOP never leaves a broken script behind.
  - `media()` runs the fence before acting on an exit 3, so a command that lost the lease sets the video aside instead of blocking it.
  - `fence()` takes no lease, and makes no directory, for a slug that has no work directory, such as a series document.
- Docs: `docs/videos/AUTOMATION.md` explains the lease and the exec-not-run rule. The `deploy` skill says a killed worker's `LEASE` is taken over. `prod-host-ops` rule 7 is exec, not run. Both skill copies stay byte-identical.
- Not done:
  - **Review nit 7** (refuse to take the lease inside the worker without a unit): `auto` runs the Shorts step in the same process outside any unit, and its media commands would be refused. Decided against; the item stays unticked with this reason.
  - **The optional `/admin/videos` lease row** needs an API field and UI. Not done; it is left for a ticket of its own if wanted.
- Tests:
  - tts / check-audio, dub: a foreign lease means no speech request and no write.
  - clips / music, look: STOP and a foreign lease each mean nothing bought and nothing written.
  - automation: `restoreVideo` under STOP and under a foreign lease; an exit 3 after the lease went; no directory for a series slug.
- Code review (2026-10-07) found:
  - **Blocking:** tts, dub and check-audio, when the lease went mid-unit, still gave a dub up or blocked the video.
    Fixed: `Automation.speech()` runs the fence on a non-uncertain exit 3 before any handling. An uncertain answer keeps its own.
  - **Should-fix:** a STOP during a discussion's lint repairs left the broken script.
    Fixed: `discuss.mjs` restores the last good script when `saveAndLint` throws PROJECT_HELD.
  - **Nit:** the comment on the `fence()` skip was wrong.
    Fixed: it now names a new draft's slug too.
  - **Nit:** a STOP removed at the wrong moment could pass for a stage done.
    Fixed: the commands exit 6 under STOP at entry, and `media()` fences that exit instead of blocking.
- Re-review (2026-10-07): no blocking issue.
  - The one should-fix is fixed: a STOP removed between a media command's exit 6 and the worker reading it blocked the video. `media()` and `acceptBestPictures` now defer on exit 6 with no backoff, as a stopped tts does. There is a test.
  - Removed the orphaned `restoreVideo` one-line comment.
  - Pre-existing, filed as `2026-10-07-a-discussion-s-refused-script-revision`: a refused revision's lexicon terms are not rolled back.
