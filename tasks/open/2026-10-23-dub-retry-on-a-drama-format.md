---
id: 2026-10-23-dub-retry-on-a-drama-format
title: Dub retry on a drama-format video (brand stories) is always refused as stale
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-23T13:15:32Z
created_at: 2026-10-23T13:15:24Z
completed_at:
branch: claude/dub-retry-drama-clips
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/package-refusal.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Dub retry on a drama-format video (brand stories) is always refused as stale

## Why

On 2026-10-23 the owner pressed 「再做一次」 for the ja, ko, es and id dubs of
`story-adapt-a4-paper-size`. The worker refused all four within the hour with
「成片不在了，或它的檢查記錄比現在的腳本和畫面舊，上傳包寫不出來…」, the same refusal as on 10-20.
The cut was current: inside the production worker, speech, visual and mix hashes all matched and
`checksCurrent(doc, lexicon, checks, clips)` was true. `packageRefusal` in `flow.mjs` called
`checksCurrent` with `clips = null`, and for a drama-format doc (every brand story is
`format: "drama"`) `checksCurrent` requires the clips manifest's hash, so it was false every time.
`package/cli.mjs` itself passes the clips; only the retry's pre-check did not. Every dub retry on a
brand story or a drama was refused this way.

## Definition of done

- [x] `packageRefusal` reads `clips/manifest.json` for a drama, as `package` does.
- [x] A test fails with the old call and passes with the fix (`package-refusal.test.mjs`).
- [x] Duration review increment for `flow.mjs` by an independent reviewer (`claude-pr-review-dub-retry-clips-20261023`, PASS).
- [ ] Merged and deployed; the owner presses 「再做一次」 for A4's ja/ko/es/id again and the worker takes them.

## How to verify

`node --test tools/video/automation/package-refusal.test.mjs`;
`node --test --test-name-pattern=dub tools/video/automation/automation.test.mjs` (42 pass);
`node tools/video/long-form/cli.mjs check`.

## Notes

- A refused request stays refused: after deploy the owner (or an agent in the logged-in admin
  page) has to press 「再做一次」 again for each language.
- The admin button asks `window.confirm`; in a hidden in-app browser pane the dialog answers
  cancel by itself, so a click there sends nothing.
