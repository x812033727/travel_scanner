---
id: 2026-10-02-a-dropped-shorts-topic-frees-its
title: A dropped Shorts topic frees its planned slot and does not count toward the monthly cap
status: done
priority: P2
area: api
owner: claude-opus-5-5-shorts-gaps
claimed_at: 2026-10-02T19:56:23Z
created_at: 2026-10-02T19:56:10Z
completed_at: 2026-10-02T20:07:37Z
branch: claude/shorts-dropped-topic-slots
depends_on: []
scope:
  - apps/api/app/video_shorts/jobs.py
  - apps/api/app/video_shorts/topics.py
  - apps/api/app/video_shorts/slots.py
  - apps/api/tests/test_video_shorts_automation.py
---

# A dropped Shorts topic frees its planned slot and does not count toward the monthly cap

## Why

PR #1130 made a highlight topic the worker finishes as `dropped` drop its empty video too. Three
gaps stayed, found while checking that ticket (`2026-10-02-a-highlight-topic-finished-as-dropped`):

1. **The calendar slot stays taken.** The weekly plan gives a topic a slot (`status: planned`,
   `topic_slug`, `line`, `series`; `apps/api/app/video_shorts/plan.py` `apply_plan`). When the
   topic is dropped, by the worker (`POST shorts/{topic}/done` with `outcome: dropped`,
   `finish_topic` in `jobs.py`) or by the owner (`patch_topic` with `dropped: true` in
   `topics.py`), nothing touches that slot. `shorts_slots.release` only empties slots a video
   holds, and an empty video never held one. The slot stays `planned` for a topic nobody will
   make: the worker skips it (`next_job_for` wants a makeable topic), the planner cannot use it
   (`plan.is_open` wants `open` with no topic), and its `line` still counts against that week's
   line quota (`plan.week_counts`). It can only be filled from the library when it falls due, or
   it is missed.
2. **A dropped topic still uses up the month.** `_started_this_month` counted every topic started
   this month, so a highlight the worker started only to find no passage worth a Short (and
   dropped with its empty video) still took one of `max_per_month`.
3. **A drop without a note took an older note.** When `done` carried no note, the dropped video's
   `dropped_note` fell back to whatever note the topic already had (the owner's, say), which is
   not the reason it was dropped.

## Definition of done

- [x] A topic dropped by the worker or by the owner gives back its slots still ahead that no Short
      holds: `open`, with no topic, line or series, so the next plan can fill them and the week's
      line quotas no longer count them.
- [x] A past slot, or one a Short already holds, stays as it is.
- [x] A topic given up before its Short was made (its video has no review and is not on YouTube)
      does not count toward `max_per_month`; one whose Short reached the owner or YouTube still
      does.
- [x] A `done` without a note gives the dropped video the fixed reason, not an older note.
- [x] Tests for each, failing before the change.

## Steps

- [x] Re-check the three findings against `origin/main` after #1130 (all three still held).
- [x] `slots.unplan`: free a dropped topic's future `planned` slots with no video.
- [x] Call it from `finish_topic` (outcome `dropped`) and from `patch_topic` (`dropped: true`);
      the owner's audit row records `freed_slots`.
- [x] `_started_this_month` leaves out dropped topics whose Short was never made.
- [x] `finish_topic` passes the `done` note, not the topic's, to `_drop_empty_video`.
- [x] Three tests in `test_video_shorts_automation.py`.

## How to verify

```bash
cd apps/api
uv run ruff check . && uv run mypy app && uv run mypy tests
uv run pytest tests/test_video_shorts*.py -q
```

On `origin/main` the three new tests fail (`test_a_dropped_topic_gives_its_planned_slots_back_to_the_plan`,
`test_a_topic_dropped_before_its_short_was_made_leaves_the_month_s_cap`,
`test_a_drop_without_a_note_does_not_give_the_video_an_older_note`); with the change all pass.
Takes effect on the site after an API deploy.

## Notes

- 2026-10-03 (claude-opus-5-5-shorts-gaps): filed from the findings left after PR #1130 and done
  in the same PR. `slots.py` was added to the scope: the new `unplan` sits next to `release`,
  which empties the slots a dropped video holds; `topics.py` and `jobs.py` both call it.
- A freed slot loses `line` and `series` as well as `topic_slug`. Keeping the line would leave
  the week counting it in `week_counts` and a re-plan of the same slot would count it twice; an
  open slot with a line would also be kept from Shorts of the other lines in `rules.assign_slot`.
- Only `planned` slots with no `project_slug` and `starts_at` after now are freed. A slot a Short
  holds (`assigned` and later) is that Short's; a past one is history. A planned slot already
  inside the lock window is freed too: `lock_due` treats `open` and `planned` alike, so it is
  filled from the library or missed as before.
- The monthly cap: the data model has no "made" flag on a topic, so "its Short was made" is read
  from the topic's video, the same way #1130's `_drop_empty_video` reads it: the video has a
  review (it reached the owner) or a YouTube id. A dropped topic with neither made no Short and
  is not counted; a dropped topic whose Short reached the owner or YouTube still counts, even if
  the video was dropped later. Topics that are `making` or `made` count as before. The rule sits
  in `_started_this_month`, so `next_job_for`'s hold and `start_topic`'s 409 agree.
- Trade-off: the owner's "drop, then take back" to remake a topic used to keep the topic's slot;
  now the drop gives the slot back and the topic returns to the pool for the next plan.
- Not done here: slots left `planned` for topics dropped before this deploy are not swept. To
  check on the host: `SELECT s.id, s.starts_at, s.topic_slug FROM video_shorts_slots s JOIN
  video_shorts_topics t ON t.slug = s.topic_slug WHERE t.status = 'dropped' AND s.status =
  'planned' AND s.project_slug IS NULL AND s.starts_at > now();` and clear any with the calendar's
  slot actions, or drop the topic again (`patch_topic` with `dropped: true` frees them now).
- Not done here either: a topic still `making` whose video the owner dropped keeps its planned
  slot (`release` puts it back to `planned` for the topic) until the owner drops or retakes the
  topic; `next_job_for` skips it meanwhile.
