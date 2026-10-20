---
id: 2026-10-20-curio-s49-1904-st-louis-marathon
title: 1904 St Louis marathon official-report source access follow-up
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T15:02:33Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/topic-checks/1904-st-louis-marathon.md
---

# 1904 St Louis marathon official-report source access follow-up

## Why

The proposed S49 episode needs the 1904 St Louis Olympic Games official report to distinguish Fred Lorz's car ride and Thomas Hicks's finish from later embellishment. In this cloud environment, the report hosts tested on 2026-10-20 (`olympics.com`, `digital.la84.org`, `archive.org`) returned proxy `CONNECT 403`. GitHub code and repository searches found no verifiable report copy. Parent directed that S49 use another source-ready topic rather than fill gaps from memory. This ticket keeps the marathon as a future source-access follow-up; it does not reserve `docs/videos/curio-s49`.

## Definition of done

- [ ] Pin an authoritative official-report scan or faithful transcription at a stable URL and SHA.
- [ ] Compare its marathon account with an independently accessible contemporary report before proposing any episode.

## Steps

- [ ] Obtain report through authorized environment network access or a verifiable mirror.
- [ ] Record precise page locations for Lorz and Hicks and source limits.

## How to verify

Open the pinned report, verify its hash and cited pages, and record source boundaries in the topic-check file.

## Notes

The browser-facing sites were not tested as readable; the observed failure is the egress proxy. `raw.githubusercontent.com` and `api.github.com` worked. No marathon script or visual claims were written.
