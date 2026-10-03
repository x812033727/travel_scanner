---
id: 2026-09-22-respect-per-slug-publish-holds-in
title: Respect per-slug publish holds in localization bundle publisher
status: done
priority: P1
area: tools
owner: codex-p1-publish-holds
claimed_at: 2026-09-29T01:55:32Z
created_at: 2026-09-22T07:16:20Z
completed_at: 2026-09-29T02:17:31Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/article-localization/publish_bundle.py
  - docs/article-localization/test_publish_bundle.py
  - apps/api/app/guides/publish_holds.json
---

# Respect per-slug publish holds in localization bundle publisher

## Why

PR #651 added `apps/api/app/guides/publish_holds.json` protection to
`guides-import --publish`, but `docs/article-localization/publish_bundle.py`
directly calls `admin_service.publish_locale` and does not consult that list.
A held slug could therefore still be published through this separate entrypoint.
Existing journal, version and visibility guards do not enforce an editorial hold.

## Definition of done

- [x] A current per-slug publication hold causes bundle publish phases to refuse
      that slug before any publication mutation, with the hold reason recorded.
- [x] Draft-only work remains private, and unrelated unheld targets remain scoped.
- [x] A hold added after initial dry-run is rechecked before publication; retries
      and lost-response reconciliation cannot bypass it or erase prior evidence.
- [x] Tests cover held, unheld, draft-only and newly-held-between-phases cases.

## Steps

- [x] Reconcile the existing hold-list loader and every bundle publication path.
- [x] Implement the bounded guard without broadening targets or overriding holds.
- [x] Run publisher transaction tests locally; retain PostgreSQL variants for CI.

## How to verify

Use explicit held/unheld fixture slugs and a bundle journal to assert no held
publication action occurs, including a hold inserted after dry-run. Preserve the
existing idempotence, concurrent edit, private-draft and source-correction tests.

## Notes

Discovered while comparing main `e001679728f35bd1c514da8c592272ddb7e9b398`
with PR #652. Exact impact receipt is
`<home>/.codex/article-localization-release/batch015/publish-hold-impact-review-e0016797.json`,
SHA256 `0a146220af2efec0c983c97a456102cc68932364b917ffde85795f34b9a7adc2`.
At that version only the two Singapore batch010 slugs were held. Current batch015
`thailand-esim-sim-wifi` and private batch016 `llms-txt-evaluation` were absent;
the release must freshly confirm absence in the exact deployed hold file.
This finding does not authorize removal or modification of any existing hold.
The preservation feature task owns the publisher until it is merged/handed back;
claim this follow-up only after resolving that active scope.

### 2026-09-29 P1 audit implementation

- Claim succeeded without an override after inspecting current tasks, local/remote
  branches and the open PR list. The old preservation PR #652 is closed; no open
  PR changes this publisher. Work is on `codex/p1-task-audit`.
- The publisher uses the existing `load_publish_holds` at dry-run and publication
  phase entry, again for each operation, and immediately before the publish
  service call after persisting the durable intent. Both article and hub phases
  refuse with the current reason. The journal records a stop without changing
  prior progress. A pending publication cannot be reconciled through any phase
  while held, including after a lost response; clearing the hold permits exact
  commit reconciliation without publishing a second revision.
- Draft-only manifests remain private and can proceed. A hold outside the
  selected scope does not affect the bundle. Invalid hold data refuses publication.
- Scope includes `publish_holds.json` solely to remove the two superseded
  Singapore entries. The user's P1 cleanup instruction covers unnecessary work;
  the committed `releases/2026-09-22/README.md` explicitly supersedes #647's
  pre-release assertions. `batch010-singapore/release-evidence.json` records
  independently approved source corrections, 115/115 numeric equivalences,
  10 committed publications with no pending operation, and successful 20-case
  browser QA. All six referenced review receipts were rehashed and match their
  recorded SHA-256 values. Git history shows no later hold decision after #651.
  This repository cleanup neither publishes content nor changes deployed files.
- Local publisher suite: **69 passed, 68 skipped**, exit 0. The skipped cases
  require isolated PostgreSQL services; their transaction fixtures are run by
  the existing `article-localization.yml` release-safety job. New cases verify
  the refusal leaves the database/revision count unchanged, preserves pending
  intents and history, and reconciles a committed lost response exactly once.
- Scoped Ruff and `git diff --check` pass. Production was not contacted.
- Existing API hold suite: **8 passed, 3 skipped**, exit 0, including the
  shipped-list/real-pack check against the now-empty hold registry.
