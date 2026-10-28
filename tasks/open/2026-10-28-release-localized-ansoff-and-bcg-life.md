---
id: 2026-10-28-release-localized-ansoff-and-bcg-life
title: Release localized Ansoff and BCG life guides
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-28T02:26:36Z
completed_at:
branch:
depends_on:
  - 2026-10-28-localize-ansoff-and-bcg-life-guides
scope:
  - docs/article-localization/releases/two-life-20261028
---

# Release localized Ansoff and BCG life guides

## Why

The authoring task adds eight reviewed en/ja/ko/zh-CN documents for two already
public life articles. Their current zh-TW v4 sources remain unchanged. Publication
must follow the merged/deployed content and fresh database guards, separately
from the owner's approval of the older seventeen-article wave.

## Definition of done

- [ ] Content PR merged with required checks and exact runtime content/assets verified.
- [ ] Fresh source/target versions, visibility and holds match the reviewed bundle.
- [ ] Concrete owner release decision, verified backup and isolated rehearsal precede writes.
- [ ] Eight missing target documents published through the native journal; no source changes.
- [ ] Idempotent replay, five-language public API/image/link/desktop/mobile acceptance and sanitized release records complete.

## Steps

- [ ] Verify the content merge and deployed image, avoiding unnecessary rebuilds.
- [ ] Refresh snapshot and scoped dry-run; obtain the concrete release decision.
- [ ] Back up, rehearse and publish only the two selected articles/four target languages.
- [ ] Verify actual public state and write release receipts before closing this task.

## How to verify

Use the unchanged localization publisher with the exact manifest, native journal
and fresh source guards. Verify all ten public locale pages and media through the
public API/browser, including exact canonical/hreflang and publication-aware
related links. Unpublished Similarweb target references remain plain text.

## Notes

Authoring manifest SHA256:
`5717849d1e3407a3dd1fe762a96067236837562aed3fc8c1faeb575c160668d1`.
The seventeen-article release decision on October 28 does not authorize this new
two-article merge, deployment or publication. Keep this release task open/unclaimed.
