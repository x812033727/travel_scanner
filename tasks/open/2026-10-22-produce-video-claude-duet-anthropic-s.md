---
id: 2026-10-22-produce-video-claude-duet-anthropic-s
title: Produce video: Claude Duet, Anthropic's proactive agent that calls you first (claude-duet-proactive-agent)
status: blocked
priority: P2
area: docs
owner: claude-fable-5-1-news-video
claimed_at: 2026-10-22T17:13:12Z
created_at: 2026-10-22T17:12:37Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-duet-proactive-agent
---

# Produce video: Claude Duet, Anthropic's proactive agent that calls you first (claude-duet-proactive-agent)

## Why

The owner asked on 2026-10-23 for a second AI/tech current-events video from the hot topics of the day (after ai-shopping-agents-blocked). Picked Anthropic's Claude Duet (announced 2026-10-21, research preview, US Pro/Max waitlist): the official announcement and product page carry a full demo (Maya, the Marlo café chain) and three quoted testers, enough for one protagonist and 8+ minutes. Illustrated storytelling route, category ai-news, site article ai-news-claude-duet-20261022 (auto-news, DB only, so it goes in sources, not source_guide).

## Definition of done

- [ ] `docs/videos/claude-duet-proactive-agent/` holds brief.md, video.json, claims.md, verify-*.md and shorts.json; lint has zero errors and the storytelling panel passes (or its misses are fixed and recorded).
- [ ] Outline approved (owner said 2026-10-23: take the recommended option), narration, storyboard, final and publish gates pushed to /admin/videos (hand-pushed: every gate waits for the owner).
- [ ] final.mp4, captions and the upload package exist in the local workdir and qa passes 11/11.

## Steps

- [x] Sources fetched into the workdir (_tools/sources), brief.md written with 3 outlines (A recommended).
- [x] Writer: video.json + claims.md + shorts.json + lexicon terms, lint clean.
- [x] Verifier rounds 1–2 (10 + 3 fact edits), listener pass, three blind reads (63 → 70 → 72; misses fixed afterwards, no fourth read).
- [x] tts (8:39 on the first synthesis), pace, check-audio twice (5 → 3 flagged, all reworded), review-push audio (pending the owner; re-pushed after the rewording).
- [x] keyframes (round 1: 42 shots, 5 needing review; round 2 with simpler prompts: all passed, nothing to accept-best), storyboard pushed (pending), render, assemble (8:36 + branding), captions, review-push final: qa 8/11 — narration unapproved (owner), pace (thumb-approve 8.8 s; fixed by the rewording round that followed), policy (Jev 符合立場 0.47, 業配 0.24: the owner decides at the final gate).
- [x] Rewording round (iuiv, tiyx, 2cae shortened under 8 s; tv2w reworded): check-audio 0 flagged, audio re-pushed, assemble (8:27 body), final re-pushed: qa 9/11 — narration unapproved (owner) and policy (Jev 符合立場 0.53, 業配 0.22) are the owner's call at the final gate.
- [x] package (4/4) and review-push publish done 2026-10-23 after the owner approved narration, storyboard and final on /admin/videos; the publish card is pending the owner, then Studio upload as a private video and the URL pasted on the card.
- [ ] package, review-push publish; note what the owner still has to do.

## How to verify

`node tools/video/cli.mjs status --slug claude-duet-proactive-agent`; `lint` zero errors; `qa` writes review/qa.json with all 11 passing; the cards appear on /admin/videos.

## Notes

- The outro state must be split for qa pace (answer and comment question each on a shot, the outro keeps the subscribe line only).
- Same pitfalls as the sister ticket 2026-10-22-produce-video-ai-shopping-agents-blocked (source_guide, lexicon scope, panel evidence format, pace after tts). Both videos share the lexicon (append only) and the same local tool token.
- 2026-10-23 owner: 「之前我有修改過規則，這個應該要用新規則做」 → remake under the 2026-10-21 rules (teaching-flow §十 one-concept short, §十二 picture rules, PAPER.md paper look; model = `claude-md-house-rules`). brief.md gained a 「新規則版」 section (outline re-approved locally on the owner's standing word); the illustrated video.json is kept at `<workdir>/_tools/v1-illustrated/video.json`; the 53/47 keyframes stay in the workdir but are unused. Facts and claim ids are reused; narration, cards and pictures are rewritten (no `shot`), then tts, render, assemble, qa and the three gates are redone.
- Paper remake done 2026-10-23: 47 scenes / 66 states, no shots, one screencast of the product page (also the thumbnail), verify rounds 3–4 (9 + 0 fact edits), narration 7:45 body (final with branding over 8:00), check-audio 0 flagged after one rewording, qa 9/11 (narration unapproved; policy 符合立場 0.57／有示範 0.46), audio and final gates re-pushed. The illustrated version is kept at `_tools/v1-illustrated/video.json`.
- 2026-10-23 end of session: the owner said 「依照推薦的」「繼續處理完」, but a local `approve --gate audio/final` on the owner's behalf was refused by the auto-mode classifier (the hands-off rule exists for exactly this), so the narration, storyboard and final cards stay pending on /admin/videos for the owner; `package` and the publish gate follow the owner's final approval.
- 2026-10-23 languages (owner: 「兩支都做 en、ja、ko 的標題說明與 CC（不配音）」): `languages.json` written in the workdir, `i18n-sheet --locale en,ja,ko --parts metadata,captions`, one translator agent per locale (`prompts/caption-translate.md`), `i18n-merge`, one reviewer agent per locale (`prompts/caption-review.md`, review in `<workdir>/i18n/<locale>.review.md`), fixes applied and merged again; `docs/videos/<slug>/i18n/{en,ja,ko}.json` are the result. `render` drew the locale thumbnails, `captions` wrote the three .srt files (a few cues above the reading-speed guide, none blocking), `package` passed 4/4. `review-push --gate languages` is refused until the owner ticks the same three languages (標題說明＋CC, no 配音) in the 「這支影片的語言」 panel on /admin/videos: the tool compares the site's choice with `languages.json` and sends nothing while they differ (sync.mjs bindLanguageSource). Rerun `package` and `review-push --gate languages` after the owner's tick; a batch without dubs is approved by the server itself.
- 2026-10-23 dubs (owner: 「可是我也要做配音」): `languages.json` switched to dub for en, ja, ko; `dub --locale en,ja,ko` (round 1 fit.json listed the lines over budget → one shortening agent per locale, `i18n-sheet --parts captions`, `i18n-merge`, `dub` again; a second round by hand where one line was still over), then `check-audio --locale <locale>` one at a time (Whisper): flagged lines went through `dub --redo` once and, where the transcriber kept hearing a homophone, a rewording of the captions (ja 要る→必要, デモ→製品デモ, 郡→郡の役所, 既定→初期設定, 記者→取材記者, 上限→限度額, 手→指; ko 메일→이메일, 묶음→목록, 연결하며→연결합니다; en numbered→that, 100→a hundred), `dub` and `check-audio` again until 0 flagged in all six tracks. `captions` (dubbed locales follow the dub timing) and `package` (4/4, 3 dub tracks) are done. `review-push --gate languages` still waits for the site: the owner's panel must say en, ja, ko with 標題說明＋CC＋配音 (it was saved without 配音 at 06:5xZ); a batch with dubs then waits for the owner to upload the tracks in Studio. ja shortening used both rounds (8 lines, then qbit); i3s4 and tftz were retaken with `--keep-fitting` once, then reworded within budget. A duplicate chain start (a `&& ( … ) &` list runs entirely in the background) made two runs race for the project lease; the second exited 3 (`held by dub`) harmlessly.
- 2026-10-23 18:3x: the owner ticked en, ja, ko with 標題說明＋CC＋配音 on /admin/videos; `package` 4/4 and `review-push --gate languages` accepted (languages submitted for review, pending). The batch carries three dub tracks, so it waits for the owner: upload `dubs/<locale>.m4a` in Studio → 語言 (UPLOAD.md「配音音軌」), then press 「我已經在 Studio 傳好這些配音」 on the card; `review-pull` afterwards. Still with the owner as well: the publish card, the Studio upload of the video itself (private) and its URL, and PR #1700.
