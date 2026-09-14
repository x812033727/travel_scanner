---
id: 2026-09-14-article-image-ci
title: Validate article image rate rules in CI
status: review
priority: P1
area: ops
owner: codex-image-ci
claimed_at: 2026-09-14T01:15:43Z
created_at: 2026-09-14T01:15:42Z
completed_at:
branch: codex/article-image-retry
depends_on: []
scope:
  - .github/workflows/ci.yml
---

# Validate article image rate rules in CI

## Why

Six article covers returned HTTP 429 in the user's browser. The image fix has a real
nginx request test, but it must run in CI to keep static image exemptions from regressing.

## Definition of done

- [x] CI invokes the real nginx request test in a disposable nginx 1.28 container.
- [ ] PR is reviewed and merged; host activation is separately tracked by article-image-retry.

## Steps

- [x] Retain the existing syntax check and add image/page request assertions.
- [ ] Verify the new CI job and publish the focused image PR.

## How to verify

The containers job runs `tools/test-guide-image-rate-limit.py` against nginx 1.28-alpine.
The same harness already passed locally with nginx 1.28.3: 120 image requests allowed,
page budget preserved, HTML requests limited and seven non-image patterns excluded.
Check workflow YAML, task metadata and scoped frontend tests before push.

Workflow YAML parsed successfully; task validation passed with existing overlap/stale
warnings. The combined guide image, article/content blocks and draft tests pass (133).
The actual nginx request harness passed again with nginx 1.28.3 before publishing.

## Notes

The image branch is stacked on PR #468's draft-preservation CI fix. Use
codex/travel-articles-batch5 as its PR base until #468 merges, then retarget to main.
No production activation or merge is authorized by this continuation.
