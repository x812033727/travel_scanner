---
id: 2026-10-03-produce-video-openai-devday-2026-recap
title: Produce video: OpenAI DevDay 2026 recap, what the 20-plus announcements change for you
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1-devday
claimed_at: 2026-10-03T11:42:15Z
created_at: 2026-10-03T11:40:42Z
completed_at:
branch: claude/video-devday-2026-recap
depends_on: []
scope:
  - docs/videos/openai-devday-2026-recap
  - docs/videos/lexicon.json
---

# Produce video: OpenAI DevDay 2026 recap, what the 20-plus announcements change for you

## Why

The owner asked on 2026-10-03 for a video about OpenAI DevDay 2026 (2026-09-29) from the official recap page
<https://openai.com/zh-Hant/index/devday-2026-recap/>: the 26 announcements in five groups (dots, GPT-6.1 Sol,
Ultrafast, Private Intelligence; Codex Cloud, CLI, code review, Security Cloud, Decisions API, computer use in the
Agents API, Bedrock Managed Agents; plugin extensions, builder, workstations, MCP events; Spaces, dynamic pages,
collaborative slides, teams and shared tasks, @ChatGPT in Slack and Teams, meeting plugin, shareable profiles;
Sign in with ChatGPT, the US$500 Pro tier, the OpenAI Marketplace). The video is an illustrated-slides explainer on the
automated route (skill `youtube-video`, `docs/videos/ILLUSTRATED.md`), zh-TW narration, 8–12 minutes, sorted by what
each announcement changes for a Taiwan viewer's plan, bill and settings rather than by OpenAI's order.

## Definition of done

- [ ] `docs/videos/openai-devday-2026-recap/brief.md` with the eight sections, 2–3 genuinely different outlines, the
      stance line 「套用立場：N、M」 against the site's 10-point channel stance, and a worked example on today's official
      numbers; Jev picked an outline on the outline gate (`review-push --gate outline`) or the owner did.
- [ ] `video.json` (illustrated slides: `shot` scenes under at least half of the runtime, no `look`, `subtitles.burn_in`
      false, `thumb` with `data.shot`), `claims.md`, `shorts.json`; lint zero errors; two independent fact-check rounds
      (`verify-1.md`, `verify-2.md`) and a listener pass; every changeable fact re-read on its official page on writing day.
- [ ] Narration synthesized and checked (`tts`, `check-audio`, audio gate), illustrations drawn (`keyframes`), cut assembled,
      zh-TW captions, `qa` 11 of 11, final and publish gates approved; the owner uploads privately per `UPLOAD.md`.

## Steps

- [x] File and claim the task; branch `claude/video-devday-2026-recap` from origin/main.
- [x] Capture the official pages openai.com refuses to crawlers (403 to curl and WebFetch) through a browser into
      `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/sources/` for the planner, writer and verifiers.
- [x] Planner panel (ultracode workflow, 16 agents): three candidate briefs (money-and-plan, who-can-use-it-today,
      the-one-thread), three judges (all picked the who-can-use-it-today brief), one synthesized `brief.md` with three
      options, four critics (Jev simulation, facts, coverage, format) in two rounds: 18 blocking findings fixed in round
      1, all four passed in round 2; round-2 minor notes applied by `_tools/polish-brief.mjs`.
- [x] Outline gate 2026-10-03 12:49Z through `_tools/outline-gate.mjs` (the worker's submitOutline calls, since
      `review-push` needs a video.json): Jev picked A at 0.85 (stance 0.91, demo 0.94, advice 0.01), approved on arrival
      (review `59570a68-7a03-43b5-99c2-25372710b391`); `review-pull` recorded it (brief.md sha256 `37676d25…`).
- [x] Writer (cut off by the session limit after `video.json`; a second agent wrote `claims.md`, `shorts.json` and the
      dictionary entries), three report-only checkers (numbers, availability, names), verifier round 1 (23 fact changes),
      round 2 (4 more narrowings), listener pass (52 edits), cadence / register / stance / fact-drift critics with three
      re-check rounds, three picture critics (33 of 47 prompts rewritten, 15 shots added so no state runs over 8 s and
      pictures cover over half), pause beats set by `setPauseBeats`, then a final verification of the polished text
      (`verify-3.md`). Lint zero errors.
- [x] `tts` (narration 13:05), pace measured on the real timeline (17 states over 8 s: shots split, reveals added,
      seven sentences cut at their punctuation, 12 shots added; none over 8 s now), `check-audio` (150 lines, none
      flagged after three passes and nine reworded lines), `review-push --gate audio` approved, `review-pull` recorded.
- [x] `render`: every card fits (the 「還不能碰的」 card went from six bullets to five); thumbnail drawn.
- [x] `keyframes`: all 74 shots pass the judge (US$29.48; the owner raised the cap to US$35 on 2026-10-04);
      `review-push --gate storyboard` approved, `review-pull` recorded.
- [x] `assemble` (13:22, -14 LUFS), `captions` (zh-TW, 161 cues), `qa` 10 of 11: only `links` fails (seven
      openai.com / help.openai.com / chatgpt.com links answer 403 to the checker, as they do to curl). The policy item
      first scored the demonstration 0.40 and 0.44 (needs 0.6): the table card `uf-worked` and three lines carry the
      brief's 實算二 as a calculation the viewer can follow (0.67 to 0.69 since). Three cards whose text was cut off
      inside their boxes in the finished cut were shortened (card text only).
- [x] `review-push --gate final` on 2026-10-04: submitted, **waiting for the owner on /admin/videos** (it cannot be
      approved automatically while `links` fails).
- [ ] After the owner approves: `review-pull`, `package`, `review-push --gate publish`; the owner uploads privately per
      `UPLOAD.md`. Re-open the official pages named under "Expiring facts" on upload day.

## How to verify

```bash
node tools/video/cli.mjs lint --slug openai-devday-2026-recap
node tools/video/cli.mjs status --slug openai-devday-2026-recap
```

## Notes

- Claimed with `--force`: the only overlap is the shared pronunciation dictionary `docs/videos/lexicon.json`, which is
  append-only and also in the scope of three stale video tickets (`2026-09-27-developer-ai-coding-tool-comparison-video`,
  `2026-09-28-en-video-01-openai-agents-broke`, `2026-09-29-ai-terms-video-pilot`). This task only adds terms.
- Site settings read on 2026-10-03 (`GET /api/video/automation/settings`): channel stance has 10 points, `auto_pick_outline`
  true, `auto_approve_final` true, `auto_approve_audio` true, `slides_media_enabled` true (gemini-3.1-flash-image, US$20 cap,
  storyboard auto-approved), no `slides_music_track` and no `slides_sfx_set`, target 8–12 minutes, `caption_locales` en/ja/ko.
- The site's own voice `style` still carries the old wording; `tts/requests.mjs` rewrites the accent at synthesis time
  (`tools/video/core/accent.mjs`), and this video's `video.json` writes `STORY_VOICE_STYLE` from `register.mjs` directly.
- No Mokaair article covers DevDay 2026 (no content pack mentions it), so there is no `source_guide` and no `cta` scene;
  `always-on-agent-explained` (PR #1019) already explains dots in depth, so this video only places dots and points to it.
- The recap's 「瞭解詳情」 links for computer use and plugin extensions point at vercel preview deployments, not official
  documentation URLs: treat them as unconfirmed and write 「以官網為準」 where they are the only source.
- The branch is checked out in the worktree `video-audio-taiwanese-mandarin-5419c4`, so the work from the script stage
  on happened in the worktree `video-devday-2026-recap-61f1b1` (the branch merged in, commits pushed as
  `HEAD:claude/video-devday-2026-recap`). The agents' rules, the checkers' reports, the picture findings and the
  snapshots of each stage are in `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/` (`COMMON.md`, `verify/`,
  `critic-pictures/findings.json`, `listen/`, `snapshots/`).
- The recap page lists 25 items (4+7+4+7+3), not 26; the script's five lists hold 9+1+6+5+4.
- Where `brief.md` and the official pages disagree the script follows the pages, and `brief.md` stays as approved (the
  outline approval is bound to its hash): the brief says the earlier video explained how dots works and fails (it explains
  AI agents and gives dots one sentence); 「一律不給／永遠不給」 for what sign-in shares (the help page: not shared by
  sign-in itself, an app can request access separately); 「官網說登入就有 9 項」 (our count; the page never says it, and one
  of the nine is not yet on Enterprise / Edu / Healthcare); four contradictions called 「同一頁」 (only Codex 雲端 is);
  「訂過」 for the Pro 200 window (an active subscription at any point in it); scheduled whole-repository scans as a
  company extra (all Codex users); 「行動版只能看」 for Spaces (the recap says mobile is coming); one action for each of
  five lists (the last chapter has four).
- Expiring facts, to re-open before the upload: Decisions API was 「限量預覽…預計未來幾天內全面推出」 on 2026-09-29 and
  the developer docs showed no change on 2026-10-03; GPT-5.5 leaves ChatGPT on 2026-10-14 (the Plus step in the last
  chapter reads as past after that day); the Pro 200 old allowance ends 2026-10-29; dots' higher cap is first-month only;
  GPT-6.1 Sol Ultrafast is 「即將推出」 on the recap.
- Lint keeps one warning on purpose: the opening chapter runs about 38 s against the 20 s hook target (the question and
  the 「你以為…其實…」 turn land in the first three lines, about 12 s; the final gate's pace check does not fail on it).
- Length: the narration runs 13:05 against `target_minutes` `[8, 12]`. The owner decided on 2026-10-04 that a video
  only has to be 8 minutes or more, so nothing was cut; the lint warning about the upper end goes away with
  x812033727/travel_scanner#1186 (its own ticket, `2026-10-03-video-length-floor-only`).
- The storytelling voice read slower than lint's estimate (12.2 estimated, 13.07 measured), so the pace was fixed on the
  real timeline: `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/pace/pace.mjs` prints every state's real seconds.
  Changing a `reveal` makes the narration approval stale (run `check-audio`, `review-push --gate audio`, `review-pull`
  again); changing card text does not.
- Illustrations: the judge's scores top out at about 7.04 and the pass threshold is 7 (the owner decided on 2026-10-04 to
  keep 7 and redraw), so about a quarter of the takes pass and a picture that passed can fail when it is judged again.
  `keyframes` judges every cached picture again whenever one prompt changes, so before each rerun
  `_tools/judge/carry-over.mjs <video.json as it was> --write` keeps the entries that passed and whose prompt and camera
  did not change (it marks nothing as passed that the judge did not pass). Prompts were rewritten three times: by rule
  from the judge's feedback (about half passed), then by agents who opened the drawn takes and described what the model
  draws cleanly (22 of 24 passed). The last two shots failed twelve takes each and became different pictures of the
  kind that passed in their chapter. US$29.48 in all for 259 images and 332 judge calls.
- No languages are chosen yet: `<VIDEO_WORKDIR>/openai-devday-2026-recap/languages.json` says `{"locales": {},
  "decided_at": null}` so `qa` and `captions` look at zh-TW only; the owner's choice on the video page replaces it.
- The `table` and `steps` templates do not draw `data.note`, and text that overflows a step box or a compare column is
  cut off without a layout error from `render`: look at frames from `final.mp4` (the last state of each such card)
  before the final gate. `verify-3.md` row 23 was relabelled CHANGED: the QA facts item reads the first column of a
  NOT FOUND row as a claim id.
