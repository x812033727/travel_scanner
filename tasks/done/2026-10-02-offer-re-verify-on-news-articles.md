---
id: 2026-10-02-offer-re-verify-on-news-articles
title: Offer re-verify on news articles saved after failing hard checks
status: done
priority: P3
area: web
owner: codex-news-reverify-20261003
claimed_at: 2026-10-03T09:48:47Z
created_at: 2026-10-02T14:53:57Z
completed_at: 2026-10-03T10:05:32Z
branch: codex/unfinished-tickets-20261003
depends_on:
  - 2026-09-24-save-news-drafts-that-fail-hard
scope:
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages
---

# Offer re-verify on news articles saved after failing hard checks

## Why

Since task 2026-09-24-save-news-drafts-that-fail-hard, a news candidate whose five-locale
article fails a hard check (a missing FAQ block, a missing topic link, a forbidden word in
one locale) is saved as an unpublished guide article and waits in 待審查 as `manual_review`
with `error_code = news_hard_checks_failed` and `guide_article_id` set. The API lets an
editor fix it in the guide editor and press 重新查核 (`POST …/verify`, which
`service.reverify_candidate` accepts for any `manual_review`). `/admin/news` does not offer
that button in every case (`situationOf` in `apps/web/components/admin-news-workspace.tsx`):

- An owner-confirmed candidate (`human_decision = "publish"`) falls into `translationHold`,
  which offers only 「重新翻譯並發布」 and 退件. The editor links show (the page shows them
  whenever `guide_article_id` is set), but after editing there is no 重新查核, and
  「重新翻譯並發布」 translates the four locales again over the editor's fixes.
- An unconfirmed (automatic-mode) candidate falls into `fixArticle` (重新查核, 退件), which is
  right, but its explanation reads "the edited article did not pass its checks again",
  which is wrong for an article nobody has edited yet.

## Definition of done

- [x] A `manual_review` candidate with `news_hard_checks_failed` and a saved article offers
      重新查核 and 退件 (and, when confirmed, still 「重新翻譯並發布」), whether or not the
      owner confirmed it.
- [x] Its explanation says the article is saved unpublished, which locales failed are
      listed under the lint, and that it should be fixed in the guide editor then
      re-verified; in all five locales.

## Steps

- [x] A situation (or a branch in `situationOf`) for `news_hard_checks_failed` with
      `guide_article_id`, placed before the `translationHold` fallback.
- [x] Its copy in `apps/web/lib/admin-news-messages/*.json` (five locales).
- [x] A row in the situation table test of `admin-news-workspace.test.tsx`.

## How to verify

```bash
cd apps/web && npx vitest run components/admin-news-workspace.test.tsx
npm run typecheck:web && npm run lint:web && npm run check:i18n
```

## Notes

- 2026-10-03 (codex-news-reverify-20261003): force-claimed only this new ticket after
  verifying that the two overlapping 9/30 review scopes belong to the merged
  `claude/gifted-rubin-umw5s4` work (PR #1041, merge
  `f72279ff58e7b7375f376229f33e9937a9de902d`, an ancestor of current main
  `5af4ffebfcea96fd23b387288901e513ed63d4f7`). Their remaining work and task files
  are preserved. Fresh checks found no other active changes to these seven files
  across four fully paginated open PRs, 35 remote heads and 38 visible worktrees.
  Private receipt: `news-reverify-collision-20261003/collision-snapshot.json`.
  This was a routine coordination decision within the requested task cleanup,
  not a separate user instruction to force a claim. This claim remains on
  `codex/unfinished-tickets-20261003` for PR #1175.
- 2026-10-03: added `hardChecksHold` only for a saved article in `manual_review`
  with the exact hard-check error. Both owner-decision states now offer Re-verify
  and Reject; Translate again and publish remains available only after owner
  confirmation. Unsaved and unrelated holds retain their previous actions.
  The five localized explanations identify the unpublished saved article,
  language-specific lint and the edit-then-reverify path. API, action endpoints,
  reason requirements and management permission guards were not changed.
- Validation: with the six new regression cases, the original component failed
  three cases and passed 30 (exit 1): confirmed saved articles lacked Re-verify,
  and both owner-decision states displayed the wrong explanation. After the fix,
  `vitest run components/admin-news-workspace.test.tsx` passed all 33 (exit 0;
  Node 24.19.0, Vitest 5.0.2). Cases cover saved/unsaved boundaries, both owner
  decisions, existing editor links, per-locale lint, required/trimmed reasons
  and the exact `/verify` request without a translation request.
  Private logs and hashes: `news-reverify-collision-20261003/`
  (`red.log`, `green.log`, `green-typed-fixture.log`, `implementation-receipt.json`).
  The first full typecheck found a missing property in the new test's inferred
  fixture type. The fixture now explicitly supplies a distinct article ID and
  asserts that same ID in all five editor links; no `any` or suppression was used.
  Focused tests again passed 33/33, then complete web typecheck, complete web lint
  and staged i18n checks (five locales / 25 namespaces) all exited 0.
- Independent review passed for all seven final files, including the corrected
  fixture. The review binds their exact hashes and confirms that existing API
  verification reads the edited saved documents without translating them again.
  This closes the local interface repair in draft #1175; production/browser
  acceptance and any publication remain separate.
- Filed by claude-opus-5-5-news-drafts while doing the API side; the API needs nothing
  more: `reverify_candidate` already accepts `manual_review`, and publication still runs
  every check (`service.publication_bundle`).
