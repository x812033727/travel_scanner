---
id: 2026-10-13-should-brand-stories-be-dubbed-over
title: Owner decision: may a brand story be dubbed over its burned-in zh-TW subtitles
status: in-progress
priority: P2
area: meta
owner: codex-gpt6
claimed_at: 2026-10-15T13:19:17Z
created_at: 2026-10-13T13:07:39Z
completed_at:
branch: codex/brand-story-switchable-cc-dubs-20261015
depends_on:
  - 2026-10-13-dub-narrator-only-explainer-dramas-tool
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_anime_review_policy.py
  - apps/api/tests/test_video_long_review_renewal.py
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/automation/story-prompts.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - docs/videos/DUBS.md
  - docs/videos/LANGUAGES.md
  - docs/videos/STORY.md
  - docs/videos/README.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/story.md
  - .claude/skills/youtube-video/SKILL.md
---

# Brand stories use switchable Chinese CC before manual dubs

## Why

Since `2026-10-13-dub-narrator-only-explainer-dramas-tool`, a drama is dubbed when the narrator
tells it alone. The dub tool (`tools/video/dubs/cli.mjs` `spokenByCharacter`) reads the script
and accepts any drama in which no line has a speaker other than `narrator`. A brand story
(category `story`) is such a drama: `core/story.mjs` lint refuses any other speaker, and the
story's recurring figures (`storyCast` in `tools/video/automation/story.mjs`) are drawn, never
heard; they carry the narrator's voice only because lint wants one. So the tool would dub a story.

The site does not offer it. The server (`apps/api/app/video_reviews/admin_service.py`
`DUBBABLE_DRAMA_CATEGORIES`) and the language panel (`apps/web/components/admin-video-reviews.tsx`
`DUBBABLE_DRAMA_CATEGORIES`) allow a drama's dub for category `explainer` only, because a brand
story burns its zh-TW subtitles into the picture (`composeStory` writes
`subtitles: { burn_in: true }`). An English, Japanese or Korean dub would play under Chinese text
that cannot be switched off. Whether that is acceptable is a product call for the owner, not
something to unlock as a side effect.

Nothing here changes an automatic default either way: a hands-off brand story gets its languages
from the server (`drama_caption_locales`: titles, descriptions and captions, never a dub). Turning
dubs on there would dub every brand story automatically and spend money nobody approved; that
would be a separate decision.

## The question for the owner

1. May the owner tick a dub for a brand story by hand, over its burned-in zh-TW subtitles?
   (A: yes, add `story` to both `DUBBABLE_DRAMA_CATEGORIES`; B: only after stories stop burning
   subtitles and use switchable CC; C: no.)
2. If yes, should hands-off stories ever get a dub automatically? (Default: no.)

Owner answered on 2026-10-15: choose B. New brand stories use switchable zh-TW CC before
English/Japanese/Korean narration dubs can be selected by hand. Automatic dubs remain off.
Already burned-in story cuts must remain ineligible. A01's saved `video.json` and final-review
state must be checked before treating the deployed change as effective for that video.

## Definition of done

- [x] The owner chose switchable zh-TW CC followed by manually selected story dubs.
- [x] New story `video.json` uses non-burned subtitles; prompt and current docs match.
- [x] Final QA records hash-bound evidence that this exact cut has non-burned subtitles and
  valid zh-TW CC; old story cuts and stale or missing reviews fail closed.
- [x] API and language panel use the same per-video dub eligibility; other drama categories,
  relabelled stories, and renewed final cuts cannot bypass it.
- [x] Focused producer, QA, API, web, i18n, docs and board checks pass.

## How to verify

`cd apps/api && uv run pytest tests/test_video_reviews.py -k languages_once` and
`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx`.

## Notes

Claimed after the owner answered B. `--force` was needed because the predecessor ticket remains
in `review` although its code is already on `origin/main` as #1482; other reported overlaps
were stale claims with no open PR touching this ticket's API file. This ticket now covers the
necessary B-route files listed above. No paid dub or publication is implied by this code work.

Implementation: final QA binds the non-burned subtitle marker to the same passing final hash;
detail and both locale endpoints share eligibility. New submission, renewal, and approval of
a pre-existing pending replacement withdraw old dub choices for both canonical and standalone
stories. Metadata/CC choices remain. An independent review found the standalone case and the
follow-up review confirmed its fix, including a real SQLite renewal regression.

Local checks so far: story automation 27/27, QA 18/18, API review/short renewal/long renewal
99/99, web review component 79/79, i18n, web typecheck/lint, scoped Ruff/mypy, docs videos
215/215, and task check. Independent duration receipt: all 14 baseline bindings verified,
473 plans PASS, receipt tests 2/2; commit eefe69c66. Windows video tests use bundled Node
24.19.0 after system Node 24.13.0 crashed. Full local tools/web attempts were stopped under
memory pressure (0.46 GB free); a bounded tools attempt was also stopped while the machine
remained constrained. These interrupted runs are not passes; full CI is required before merge.

Pre-PR collision recheck found #1387 touching the two QA files for unrelated caption-selection
logic and tests; this branch only adds the story subtitle marker and its coverage. That PR is
an older draft and was not changed. Current origin/main remains a1b6b1149.

Existing A01 media conversion and production verification are separate from this code change.
Historical pilot readback at 09:15 UTC was 2/12, no readable video.json or media spend; this
turn's authenticated browser read timed out, so current live stage is unverified. Language
controls can appear early from locales_decided_at and do not establish final approval. After
deploy, inspect host status, chapters, video.json, reviews, assets, locks/jobs and the US$25
ledger first. If merged video.json already exists with burn_in=true, deploying the new composer
alone will not rewrite it; recompose from chapters and independently re-review its changed
hash before the existing paid pilot resumes. Retain any paid assets. No dub, upload or
production mutation was performed by this implementation.

### Authorized CI follow-up, 2026-10-15

The owner approved merging PR #1512 after green CI, deployment after host preflight, and A01
application within the existing pilot authorization. No additional merge approval is needed
for these narrow CI fixes. The first CI run passed web, video tools, containers and full-stack
smoke; two API shards failed. The native-anime test's scalar mock needed the new series-kind
answer, and a drama Short detail should skip the irrelevant long-series lookup because Shorts
are ineligible for dubbing. Those fixes pass 198 review/anime/Shorts tests, scoped Ruff/mypy.
The task was reopened under its existing owner; the added anime test path has no active claim.

The fresh authorized host preflight could not connect: hostinger2 timed out before any remote
output. Public website returned HTTP 200. Authenticated admin UI shows the deployment feature
disabled, and A01 blocked at the storytelling panel's no_spoiler check after two passes. This
is a current script-stage blocker, not final-cut approval. The owner has been asked to restore
the existing connection or open the Hostinger console; no retry, review override, or production
write followed the unavailable host entrance.
