---
id: 2026-11-10-news-topic-atom-subscriptions
title: Per-locale news topic Atom subscriptions
status: done
priority: P2
area: web
owner: codex-layout-review-topic-feed
claimed_at: 2026-11-10T13:01:17Z
created_at: 2026-11-10T13:01:15Z
completed_at: 2026-11-10T13:27:49Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/web/app/[locale]/life/topics/[topic]/feed.xml/route.ts
  - apps/web/app/[locale]/life/topics/[topic]/feed.xml/route.test.ts
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/components/guides/topic-feed-subscription.tsx
  - apps/web/components/guides/topic-feed-subscription.test.tsx
  - apps/web/lib/topic-feed.ts
  - apps/web/lib/topic-feed-messages
---

# Per-locale news topic Atom subscriptions

## Why

News topic and related-article links help readers browse once, but do not give them a topic-specific subscription they can keep in their own reader. The existing `/feed.xml` is a single zh-TW feed across the site. Add a real Atom address for each supported news topic and locale without accounts, outbound notifications, or treating a topic as one event timeline.

## Definition of done

- [x] The five locales expose an Atom feed for ai-news, crypto and tech-news, with the current locale's published public articles and stable entry identifiers.
- [x] News topic hubs offer a selectable/copyable feed address, localized instructions and Atom autodiscovery metadata.
- [x] Unknown locale/topic is 404, upstream failure is 503, and a truly empty topic remains a valid empty feed.
- [x] Existing global feed and ordinary topic behavior remain compatible under focused tests.
- [x] Independent review and shared full validation complete before the parent includes the changes in its PR update.

## Steps

- [x] Audit exact paths against active scopes, local/worktree branches, remote branches, open PRs and main history; claim this task.
- [x] Implement a bounded 30-item localized feed with XML escaping, valid author metadata and actual publication dates.
- [x] Add five-language subscription UI with clipboard denial fallback and no automatic clipboard writes.
- [x] Test route, UI, metadata and original topic/global-feed regressions.
- [x] Receive independent review from the parent team's e2e agent; fix any actionable findings.

## How to verify

From `apps/web`:

`npx vitest run 'app/[locale]/life/topics/[topic]/feed.xml/route.test.ts' components/guides/topic-feed-subscription.test.tsx components/guides/topic-hub-page.test.tsx app/feed.xml/route.test.ts --maxWorkers=1`

Result: 4 files / 54 tests PASS on 2026-11-10. Scoped ESLint on the seven TS/TSX files also passed. Parent owns shared typecheck, i18n, build and browser verification; no second build was started by this task.

Open a supported localized news topic, expand the subscription, copy the URL, and inspect its Atom response. Deny clipboard access and verify the read-only address remains selectable. Compare an unavailable API response with a genuinely empty topic; they must be 503 and 200 respectively.

## Notes

- Exact scope audit found no active task overlap. The only matching open PR was this same branch's #2061 for topic-hub-page.tsx; all new route/copy/component paths had no other open PR match. The worktree/remote audit also completed before claim.
- This provides newly published articles, not a guarantee that edits to older articles appear as new feed items. All five catalogs explicitly disclose that limitation and the item cap. Feed readers choose their own polling interval.
- Feed entries reuse the existing public list/locale rules; no private candidate evidence, new account data, notifications, migration or production writes are involved.
- Read RFC 4287 on 2026-11-10, including required author/id/title/updated and alternate links. New feed includes a feed-level Mokaair author. The old global feed's missing author is separately recorded in `2026-11-10-global-atom-author-metadata`; this task does not change that endpoint.
- Initial test failures were unsupported jest-dom matchers in this repository and copy that could sound like a fixed current article count. Changed to existing Chai assertions and explicit maximum-cap wording; kept the original empty-topic assertion. Final 54 tests pass.
- Web scope frozen for independent review on 2026-11-10; no commit, push, merge or deployment performed by this task.
- Independent reviewer `/root/news_layout_e2e` reported PASS and independently ran the same four suites: 54 tests exit 0. Its `atom-independent-review.md` records route, public filters, locale, XML and failure-semantics checks. Parent-coordinated build/browser verification is still separate.
- `node tools/tasks.mjs check` validated 2395 task files with exit 0 after the two local task files were completed; unrelated pre-existing overlap warnings remain outside this scope.
- Parent-coordinated validation completed: full web lint, i18n, typecheck and production build; 54 Playwright cases; five-language subscription previews, eight captured Atom responses and real clipboard-copy/readback. Final capture covered 35 page states with no page errors and passed independent visual review. These are local checks; the updated PR head still requires its own CI before merge.
