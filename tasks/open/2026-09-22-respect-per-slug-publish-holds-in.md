---
id: 2026-09-22-respect-per-slug-publish-holds-in
title: Respect per-slug publish holds in localization bundle publisher
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-22T07:16:20Z
completed_at:
branch:
depends_on: []
scope:
  - docs/article-localization/publish_bundle.py
  - docs/article-localization/test_publish_bundle.py
---

# Respect per-slug publish holds in localization bundle publisher

## Why

PR #651 added `apps/api/app/guides/publish_holds.json` protection to
`guides-import --publish`, but `docs/article-localization/publish_bundle.py`
directly calls `admin_service.publish_locale` and does not consult that list.
A held slug could therefore still be published through this separate entrypoint.
Existing journal, version and visibility guards do not enforce an editorial hold.

## Definition of done

- [ ] A current per-slug publication hold causes bundle publish phases to refuse
      that slug before any publication mutation, with the hold reason recorded.
- [ ] Draft-only work remains private, and unrelated unheld targets remain scoped.
- [ ] A hold added after initial dry-run is rechecked before publication; retries
      and lost-response reconciliation cannot bypass it or erase prior evidence.
- [ ] Tests cover held, unheld, draft-only and newly-held-between-phases cases.

## Steps

- [ ] Reconcile the existing hold-list loader and every bundle publication path.
- [ ] Implement the bounded guard without broadening targets or overriding holds.
- [ ] Run publisher unit and PostgreSQL transaction tests plus task validation.

## How to verify

Use explicit held/unheld fixture slugs and a bundle journal to assert no held
publication action occurs, including a hold inserted after dry-run. Preserve the
existing idempotence, concurrent edit, private-draft and source-correction tests.

## Notes

Discovered while comparing main `e001679728f35bd1c514da8c592272ddb7e9b398`
with PR #652. Exact impact receipt is
`C:/Users/x8120/.codex/article-localization-release/batch015/publish-hold-impact-review-e0016797.json`,
SHA256 `0a146220af2efec0c983c97a456102cc68932364b917ffde85795f34b9a7adc2`.
At that version only the two Singapore batch010 slugs were held. Current batch015
`thailand-esim-sim-wifi` and private batch016 `llms-txt-evaluation` were absent;
the release must freshly confirm absence in the exact deployed hold file.
This finding does not authorize removal or modification of any existing hold.
The preservation feature task owns the publisher until it is merged/handed back;
claim this follow-up only after resolving that active scope.
