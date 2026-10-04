---
id: 2026-10-03-jev-noul-criteria-keys-yes-no
title: Jev noul criteria are sent as yes/no; TypeSafe documents true/false
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-03T17:48:46Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_video_automation_judge.py
---

# Jev noul criteria are sent as yes/no; TypeSafe documents true/false

## Why

TypeSafe documents a noul's optional `criteria` as an object with `true` and `false`
descriptions: "An object with `true` and `false` descriptions of what a yes and a no mean"
(https://docs.typesafe.ai/primitives/noul, opened 2026-10-03); the API reference lists only
those two properties (https://docs.typesafe.ai/api), and the Python SDK schema forbids extra
keys. The site sends `yes` / `no` instead, in four places:

- `apps/api/app/video_automation/judge.py:228` (`NOUL_CRITERIA`)
- `apps/api/app/video_speech/checking.py:125-126`
- `apps/api/app/news_automation/ai.py:344-345` (publish question) and `:410-411` (duplicate check)

The calls succeed, so the HTTP API accepts the request. Whether it uses or silently ignores the
`yes` / `no` descriptions is undocumented. If it ignores them, every one of these questions has
been answered without the clarification it was written with.

## Definition of done

- [ ] All four places send `true` / `false`.
- [ ] `NoulQuestion.criteria` cannot be built with any other keys (the type lives in
      `apps/api/app/ai/jev.py:97`; that file is in the scope of
      `2026-10-03-jev-comments-drifted-from-vendor-docs`, so do this after it or widen with care).
- [ ] The `checking.py:11-14` docstring says what happens now: a line below the threshold (0.5
      by default, `tools/video/tts/check.mjs:53`) is flagged, and a narration with every line
      checked and none flagged is approved on arrival while the auto-approve setting is on
      (`apps/api/app/video_reviews/admin_service.py:1446-1458`). It currently says the owner
      still approves the narration.

## Steps

- [ ] Rename the keys and update the tests that pin them (`apps/api/tests/test_video_automation_judge.py`).
- [ ] Because fixing the keys may change the answers, re-check a few known lines and news
      candidates after deploy and note any shift here.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_judge.py
```

## Notes

- Do not claim the API rejects or ignores `yes` / `no`; only the mismatch with the documented
  contract is established.
