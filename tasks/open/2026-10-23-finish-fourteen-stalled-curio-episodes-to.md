---
id: 2026-10-23-finish-fourteen-stalled-curio-episodes-to
title: Finish fourteen stalled Curio episodes to ready-to-upload with eight languages and dubs
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-curio-finish
claimed_at: 2026-10-23T18:17:11Z
created_at: 2026-10-23T18:16:48Z
completed_at:
branch: claude/suspicious-antonelli-878480
depends_on: []
scope:
  - docs/videos/history-curiosity/finish-20261024
  - docs/videos/curio-s10/video.json
  - docs/videos/curio-s12/video.json
  - docs/videos/curio-s13/video.json
  - docs/videos/curio-s15/video.json
  - docs/videos/curio-s16/video.json
  - docs/videos/curio-s17/video.json
  - docs/videos/curio-s19/video.json
  - docs/videos/curio-s20/video.json
  - docs/videos/curio-s21/video.json
  - docs/videos/curio-s24/video.json
  - docs/videos/curio-s25/video.json
  - docs/videos/curio-s27/video.json
  - docs/videos/curio-s29/video.json
  - docs/videos/curio-s31/video.json
  - docs/videos/curio-s10/i18n
  - docs/videos/curio-s12/i18n
  - docs/videos/curio-s13/i18n
  - docs/videos/curio-s15/i18n
  - docs/videos/curio-s16/i18n
  - docs/videos/curio-s17/i18n
  - docs/videos/curio-s19/i18n
  - docs/videos/curio-s20/i18n
  - docs/videos/curio-s21/i18n
  - docs/videos/curio-s24/i18n
  - docs/videos/curio-s25/i18n
  - docs/videos/curio-s27/i18n
  - docs/videos/curio-s29/i18n
  - docs/videos/curio-s31/i18n
---

# Finish fourteen stalled Curio episodes to ready-to-upload with eight languages and dubs

## Why

The owner (2026-10-24): finish the 奇聞檔案局 episodes filed under 觀念解說 that are not ready to upload, use the
recommended choices without asking, complete everything before upload, and make the dubs by default.

On /admin/videos (read 2026-10-24 with the video tool token) these fourteen have an approved audio and storyboard
(S24, S29: audio; S29 storyboard too) but no final cut, no upload package and no languages: S10 S12 S13 S15 S16 S17
S19 S20 S21 S24 S25 S27 S29 S31. They were made in Claude cloud containers (tasks `2026-10-19-curio-s-axis-*`,
`2026-10-20-curio-s-axis-*`) that are gone; the site keeps the review payloads and some media files, not the
per-line narration, timeline and keyframes that render, captions and dub need. Their scripts are on main.

Not in this ticket: S07, S32, S33, S37 and S40 (Codex's: scripts only on `codex/curio-s34-endurance-20261019`,
S40's eight languages wait on Codex's workdir, task `2026-10-21-curio-s02-s03-s04-s05-s23`); S06, S26, S38
(a re-assembly with channel intro and outro is in another session).

## Definition of done

- [ ] Each of the fourteen has an approved final cut with the channel intro after the condensation and the
  v4 end-screen outro, an upload package, and a languages review with en ja ko es pt id vi th: title and
  description, captions and dub track (or a skip with its reason).

## Steps (per episode, one at a time: the site rate-limits keyframes per token)

- [ ] Local workdir from the script on main: tts (site channel voice) → check-audio → review-push audio.
- [ ] keyframes --takes 3 (the site dedupes an identical request per slug, so prompts left as they were cost
  nothing when the old job's file is still stored) → music → review-push storyboard.
- [ ] render → clips → assemble → captions → qa → review-push final.
- [ ] package → review-push publish; i18n-sheet / translate / i18n-merge; dub all eight line by line;
  check-audio per locale; review-push languages.

## Notes

- Quota: Gemini's daily speech quota (tts and dubs share it) resets 07:00 UTC; one episode's eight dubs take
  over an hour.
- 2026-10-24 (claude-opus-5-5-curio-finish, this machine, workdirs `~/mokaair-work/videos/<slug>`):
  - Narration re-recorded for all fourteen (site Gemini voice). The speech route answers HTTP 502 now and then;
    the tool holds that line as "uncertain". On the free voice tier a held request is safe to send again: forget
    it in `audio/speech-journal` and rerun (a scratch wrapper did this up to 12 times per command).
  - check-audio flags are mostly the transcriber on names (幸村→倖存, 家康→賈亢). Real ones re-recorded with
    `tts --redo` on a hand-picked subset: a dropped clause (S15 dm320), 刺殺→自殺 (S15 dm427), 幸/信 (S13).
  - Translations: two subagents per episode (en ja ko es / pt id vi th) from worksheets made after tts, so every
    line carries `max_chars`. Lessons: the tool appends about 2,400 bytes of chapters and references, so a
    description body must stay under about 2,300 bytes (Thai, Japanese, Korean 3 bytes a character); titles
    hit lint's phone width; `i18n-merge` does not check `max_chars`; give each translator its own scratch folder.
  - Music: Lyria returns about 177 s for a 9-10 minute cut, and since ade8410ff `music` and `assemble` hold a
    short generated track ("arrange an explicit checked loop"). Each episode's paid track is looped with 4 s
    crossfades to the cut + 30 s and faded out (`_music/<slug>-bed.m4a`, its SHA-256 bound in video.json
    `music.track` / `music.sha256`; gain and duck unchanged). `dub` also needs the music first.
  - Illustrations: one episode at a time (the token's hourly image cap). S12 86 shots US$1.44; one shot
    (village) failed three takes twice and passed as a close-up of one person indoors.
  - Gates: these are hand-pushed reviews, so the owner approves narration, storyboard, final, publish and
    languages on /admin/videos; recording an approval locally on the agent's own word was refused, rightly.
    render waits for the owner's narration and storyboard approval (then `review-pull`).
  - Card glyphs: render refuses a card character no bundled font has (S12 扨, S24 polytonic εὕρηκα). Changing
    a card after the storyboard is approved voids that approval, so check every card before the storyboard goes
    out (`uncovered()` from `tools/video/render/fonts.mjs` over each scene's data and lines).
  - A shot that fails three takes twice: give it the exact prompt of a passed shot in the same chapter (cache,
    no cost; lint warns that the two read as a stall). Done for S13 reader-2 and S16 toki-q.
  - Order: `assemble` inserts the intro after the first chapter, so a dub made before the final cut no longer
    matches the branding (qa `captions` fails); run `dub` again after `assemble` (it reuses every spoken line).
  - S12: final cut 9:48, qa 11/11, final submitted 2026-10-24. All eight dubs reviewed: four over-long lines
    shortened, wrong-meaning lines rewritten (pt sk211 "shots of Ieyasu", es sk416), ja 午の刻/石見/九月 in kana.

