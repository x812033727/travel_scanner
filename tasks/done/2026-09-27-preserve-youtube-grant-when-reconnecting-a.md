---
id: 2026-09-27-preserve-youtube-grant-when-reconnecting-a
title: Preserve YouTube grant when reconnecting a channel
status: done
priority: P1
area: api
owner: codex
claimed_at: 2026-09-27T15:28:13Z
created_at: 2026-09-27T15:27:57Z
completed_at: 2026-09-27T15:38:45Z
branch: codex/youtube-relink-grant-fix
depends_on: []
scope:
  - apps/api/app/video_youtube/connection.py
  - apps/api/tests/test_video_youtube.py
---

# Preserve YouTube grant when reconnecting a channel

## Why

After a YouTube channel is reconnected, the admin card briefly reports success,
then "授權失效" when it checks the new token. `finish_link` revokes the previous
refresh token after Google issues a replacement. Google's revocation applies to
the entire OAuth grant for the project, so it also invalidates the replacement.

## Definition of done

- [x] Reconnecting a channel leaves its new refresh token usable by Verify in the API test.
- [x] An explicit unlink still revokes the grant in the API test.

## Steps

- [x] Confirm the failure against Google's OAuth revocation documentation.
- [x] Stop revoking the previous token during reconnection.
- [x] Add a regression test and run focused API checks.

## How to verify

`cd apps/api && uv run pytest tests/test_video_youtube.py -q`
`cd apps/api && uv run ruff check app/video_youtube/connection.py tests/test_video_youtube.py`
Live acceptance after an approved deployment: reconnect Mokaair's channel and
press "確認授權". This release step needs the site owner's separate approval.

## Notes

Google's web-server OAuth guide states revocation removes every scope granted
to a project and invalidates all issued access/refresh tokens for its clients:
https://developers.google.com/identity/protocols/oauth2/web-server#tokenrevoke
The bug was observed in production on 2026-09-27 while recording the OAuth
verification demonstration. This code change has not been deployed.
`uv run pytest tests/test_video_youtube.py -q`: 23 passed.
`uv run ruff check app/video_youtube/connection.py tests/test_video_youtube.py`: passed.
