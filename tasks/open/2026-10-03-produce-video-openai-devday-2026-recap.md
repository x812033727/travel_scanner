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
- [ ] Planner panel (ultracode workflow): independent briefs, judged, one synthesized `brief.md`; lint; `review-push --gate outline`.
- [ ] Writer, verifier round 1 (and 2 if more than three fact changes), listener pass; lint zero errors.
- [ ] `tts --dry-run`, `tts`, `check-audio`, `review-push --gate audio`, `review-pull`.
- [ ] `keyframes`, `render`, `assemble`, `captions`, `qa`, `review-push --gate final`, `package`, `review-push --gate publish`.

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
