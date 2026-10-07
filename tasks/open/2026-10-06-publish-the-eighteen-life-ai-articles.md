---
id: 2026-10-06-publish-the-eighteen-life-ai-articles
title: Publish the eighteen life AI articles from #1268 and queue the eight AI-gap slides videos
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-06T13:35:14Z
completed_at:
branch:
depends_on: []
scope:
  - docs/life-ai-income-investing/records
  - docs/life-ai-office-productivity/records
---

# Publish the eighteen life AI articles from #1268 and queue the eight AI-gap slides videos

## Why

The train `claude/train-1323-1324-1268` lands #1268 with twelve zh-TW packs from
`2026-10-05-life-ai-income-investing-batch` and six from `2026-10-05-life-ai-head-to-head-office`,
plus the admin slides-video queue from `2026-10-05-videos-ai-gap-batch`. Those three tickets were
closed with the train because their code and content are complete in the branch; each left one
unticked step that can only happen on production after a deploy and with the owner's explicit
go-ahead (content-pipeline rule 8). This ticket holds those steps so they are not lost with the
archived files.

## Definition of done

- [ ] The eighteen articles are published on mokaair.com in zh-TW and answer 200 with their
      heroes and diagrams.
- [ ] The owner has queued the eight AI-gap slides videos from /admin/videos (a request is refused
      for an article that is not yet a published zh-TW life article, so this follows the first
      item).

## Steps

- [ ] Confirm the train is deployed (skill `deploy`), and get the owner's explicit go-ahead with
      an options question.
- [ ] For each slug in `docs/life-ai-income-investing/records/` and
      `docs/life-ai-office-productivity/records/`: `guides-import --slug <slug> --locale zh-TW
      --dry-run`, then `--publish` (skill `content-pipeline`).
- [ ] `guides-links-rebuild`, then `verify_public.py` for the eighteen slugs.
- [ ] Hand the owner the order and finance note for the eight videos from PR #1268's description.

## How to verify

`verify_public.py` for the eighteen slugs, and the slides queue on /admin/videos listing eight
requests.

## Notes

- Filed by claude-opus-5-5-train-1323-1324-1268 when closing the three stale review tickets in
  the train.
