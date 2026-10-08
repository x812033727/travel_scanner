---
id: 2026-10-06-an-owner-retry-resets-the-counter
title: An owner retry resets the counter that blocked the video and a new seed replaces an exhausted picture request
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T06:25:34Z
created_at: 2026-10-06T06:24:54Z
completed_at: 2026-10-07T01:03:45Z
branch: claude/video-unstuck-retry
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/media/client.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/media.test.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# An owner retry resets the counter that blocked the video and a new seed replaces an exhausted picture request

## Why

On 2026-10-06 nine host-made slides videos were `blocked` on /admin/videos and the owner's
重試 on every one re-blocked it within hours, because the retry in `flow.mjs` bookkeeping
reset only a stage's failures in a row (`/^([a-z_]+) failed \d+ times in a row:/`):

- A video blocked by `fixPrompts` ("keyframes still fails after 2 prompt fixes …",
  `MAX_PROMPT_FIX_ROUNDS = 2`) kept `prompt_fixes.keyframes = 2`, so the retry ran the paid
  keyframes stage once and blocked at the same line. The same for `fixScript` ("sent the
  screenplay back") and the outline replans.
- Two videos were blocked "keyframes needs the owner: 這個請求已經失敗 3 次；改提示詞或 seed
  再試": the server answers 409 `video_media_job_exhausted` once a request hash (prompt, seed,
  references, model) failed `MAX_ATTEMPTS` = 3 times (`apps/api/app/video_media/jobs.py`).
  PR #1275 made that code the owner's, so keyframes exited 3; seeds were fixed at 1..takes, so
  a retry replayed the identical hashes and got the same 409.
- A `retryRuns` error other than POLICY_HOLD was re-thrown out of bookkeeping before
  `state.retry_request_id` was saved, which ended the whole worker run and repeated every round
  (PR #1337 also throws `RUN_PENDING` from `retryRuns` while the saved job still runs).

## Definition of done

- [x] A video blocked after its prompt fixes, its screenplay rounds, its outline replans or a
      stage's failures in a row runs that stage again when the owner retries, with the counter
      that blocked it reset, and blocks only after spending the rounds once more.
- [x] A video blocked because the server stopped answering for its keyframes requests is
      retried on other seeds (`--seed-offset`, MAX_KEYFRAME_TAKES further each retry), and a
      keyframes run meets a spent seed by moving to the next, not by exiting 3.
- [x] A retry whose saved writer run cannot be verified blocks that video alone with the
      reason and consumes the request; one whose saved run still runs waits without consuming
      it; the videos beside it move in the same round.
- [x] The worker treats `video_ai_subscription_auth_failed` (PR #1338) like a subscription pause.

## Steps

- [x] `flow.mjs`: `block(state, why, kind)` records `blocked_kind`; every caller names its kind;
      `blockedKindOf` reads a legacy reason; `resetForRetry` resets by kind; `media()` passes
      `--seed-offset`; bookkeeping turns POLICY_HOLD, RUN_PENDING and anything else from
      `retryRuns` into a hold, a wait or a block of that video alone.
- [x] `media/client.mjs`: `video_media_job_exhausted` moves out of `OWNER_CODES` into the
      exported `EXHAUSTED_CODES`; `keyframes.mjs` takes `--seed-offset` (0..30), seeds takes at
      `take + offset`, records `seed_offset` on the entries it draws, and treats an exhausted
      seed like a refused one.
- [x] `automation/client.mjs`: `PAUSE_CODES` gains `video_ai_subscription_auth_failed`.
- [x] Tests in `automation.test.mjs` (five), `client.test.mjs`, `media.test.mjs`,
      `look-keyframes.test.mjs`.

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs tools/video/automation/client.test.mjs tools/video/media/media.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/clips.test.mjs tools/video/media/stages.test.mjs
npm run check:tasks
```

On the host after deploy: 重試 one of the nine blocked slides videos on /admin/videos and
watch the worker log: the prompt-fix round starts at 1 again ("keyframes prompts fixed (round
1)"), and a video blocked on 已經失敗 runs `keyframes --seed-offset 3` (auto.json gains
`seed_offsets.keyframes`).

## Notes

- Where a stage lets `video_media_job_exhausted` escape (look, clips, a keyframes end frame or
  style plate), it still exits 3 (`who: "owner"`) and parks that video alone: exit 4 (`later`)
  ends the whole run on that video every round, in front of the videos behind it. Only the
  keyframes take loop moves to the next seed; look.mjs and clips.mjs are out of this task's
  scope and would need the same `exhausted(error)` branch and a `--seed-offset` of their own.
  Until then an owner retry of `media_exhausted:look|clips` gives the prompt-fix rounds back
  but replays the same seeds.
- A keyframes end frame keeps seed 1 whatever the offset (its key goes into `entryStands`'s
  end check); shifting it would redraw every standing shot's end frame after a retry.
- The uncertain-retry block keeps the original `blocked_kind` (read from the legacy reason
  first) rather than `uncertain:writer`, so the retry that finally goes through resets the
  counter that blocked the video; `uncertain:writer` is used only when there was none.
- `media_exhausted:<k>` resets both the seed offset (keyframes only) and `prompt_fixes[k]`:
  a `fixPrompts` block whose summary names 已經失敗 is recorded as exhausted too, since the
  fix did not change the request enough for the server.
- Review of PR #1340: `media()` reads the exhausted wording from the last line of the stage's
  output only (a run that logged a spent seed on its way to the cap is `media_owner`); a
  finished stage (exit 0) drops its `seed_offsets[command]`, so a later rerun starts at seeds
  1..3; bookkeeping blocks a video only on an `AutomationError` or `RunReceiptError` from
  `retryRuns`, any other exception still ends the run (a programming error is not the owner's).
- The report payload carries `blocked_kind` while blocked; the API's `ProjectIn` ignores
  unknown keys today (pydantic default), so a later server change can read it.
- Stacked on PR #1339 (`claude/video-unstuck-prompt-budget`) and PR #1337
  (`claude/video-unstuck-stale-receipts`); the task was claimed with `--force` because those
  two tasks, by the same owner, share `flow.mjs`, `keyframes.mjs` and `client.mjs`.
- The duration-review receipt binds `flow.mjs`, `automation.test.mjs` and
  `look-keyframes.test.mjs`: `node tools/video/long-form/cli.mjs check` is red on them until a
  reviewer re-binds.

### 2026-10-07 標記完成（由站主授權，非原持有者）

- 證據：程式隨 PR #1340 於 2026-10-06 進 main（commit `4674fb86`，標題同本票）；
  後續 #1341（`a435f067`）、#1342、#1344 都疊在它上面合併。分支已刪。
- 票停在 review、持有者 claude-fable-5-1-video-unstuck，佔住 `flow.mjs`、`client.mjs`、
  `keyframes.mjs` 等，擋住約 17 張票（含 `2026-10-04-retain-video-policy-holds-without-new`）。
  站主 2026-10-07 同意由 claude-opus-5-5 代為結案。
- 清單全部已勾，沒有未完成項目要交代去向。上面 Notes 記的 long-form 審查收據重綁仍待審查者處理。
