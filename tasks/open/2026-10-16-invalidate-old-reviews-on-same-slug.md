---
id: 2026-10-16-invalidate-old-reviews-on-same-slug
title: Invalidate old reviews on same-slug story final replacement
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-16T14:27:48Z
completed_at:
branch:
depends_on:
  - 2026-10-16-allow-brand-story-dub-preselection-while
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews.py
---

# Invalidate old reviews on same-slug story final replacement

## Why

When a story already has an approved final, publish and language review, generic
`submit_review(gate=final)` accepts a different final under the same slug but supersedes only
pending final reviews. `publish_approved_at` and `language_states` still read the old approved
reviews. While the new final is pending, the admin may report old language parts as uploaded
and `ready_to_upload=true`. The YouTube and VPS upload paths separately bind the current final
SHA to the publish package and reject the stale package; this ticket is about the misleading
API state and old review chain, not a demonstrated upload bypass.

The documented owner `renew_final` route supersedes final, publish, languages and dubs and is
safe for its supported same-body replacement. A01's first final has no old chain, so its
early dub preselection is handled by the prerequisite ticket.

## Definition of done

- [ ] A new story final submitted on an already approved slug cannot make the API report the
  old approved publish and languages as current for the new cut.
- [ ] Scheduling readiness and language progress reflect the current final SHA and review
  chain throughout pending, approved, rejected and renewal states.
- [ ] The owner-facing replacement route and audit history remain clear; upload guards still
  reject stale packages.

## Steps

- [ ] Choose one supported same-slug replacement path: require the bound renewal flow or
  invalidate the older approval chain as soon as generic new-final submission is accepted.
- [ ] Add API regression tests for old-approved cut A, new pending/approved/rejected cut B,
  and the real renewal route; verify what the list and detail return.

## How to verify

`cd apps/api && uv run pytest tests/test_video_reviews.py` and the related long-review renewal
tests; inspect `ready_to_upload`, `publish_approved_at` and per-language states in readback.

## Notes

2026-10-16 read-only audit: `admin_service.py` generic submission supersedes pending reviews
of the same gate only; its publish and language summary helpers see previous approved rows.
`video_youtube/sync.py` and `video_youtube/vps.py` require the current final SHA to match the
approved publish package before upload and recheck during sync. The documentation-only task
`2026-10-11-write-down-how-an-approved-film` mentions this generic-path edge but explicitly
leaves the product decision open. Coordinate with that task before choosing a new rule.
