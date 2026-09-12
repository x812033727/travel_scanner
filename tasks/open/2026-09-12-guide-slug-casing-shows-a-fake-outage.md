---
id: 2026-09-12-guide-slug-casing-shows-a-fake-outage
title: A capitalised guide slug shows a fake outage instead of the article
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-12T02:41:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/app/[locale]/guides/[kind]/[slug]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/[slug]/page.test.tsx
---

# A capitalised guide slug shows a fake outage instead of the article

## Why

`/en/guides/howto/Narita-To-Tokyo` — any inbound link, email or CMS paste that capitalised the
slug — renders the red "暫時無法取得這篇文章，請稍後再試" alert, as if the backend were down.
The article is live and the API found it.

The API looks the article up with `GuideArticle.slug == slug.casefold()` and answers with the
canonical lowercase `slug`. `loadGuideArticle`'s defensive equality check then rejects that
response on casing alone:

```ts
if (!body || body.slug !== slug || body.locale !== locale || !isGuideKind(body.kind)) return unavailable;
```

Nothing upstream normalises case: `proxy.ts` handles only locale and CSP, and `next.config.ts`
defines no redirects.

Refusing to serve content under a non-canonical URL is right. Telling the reader the service is
broken is not — a redirect to the canonical slug, or a 404, would both say something true. The
`unavailable` branch is `noindex`, so the cost is reader-facing, not indexing.

Found while comparing PR #401 against the merged PR #404; it predates both and arrived with #398.

## Definition of done

- [ ] A mixed-case slug either reaches the article or answers 404, never the "temporarily
      unavailable" alert.
- [ ] The guard still rejects a response that is genuinely for another article, locale or kind.
- [ ] A test covers the casing case, so the guard cannot regress into accepting anything.

## Steps

- [ ] Decide between redirecting to the canonical URL and answering 404. A redirect keeps the
      inbound link working; a 404 is simpler and honest. Either beats the current message.
- [ ] Implement in `loadGuideArticle` or in the page, keeping the mismatch guard for the other
      fields.
- [ ] Test.

## How to verify

```bash
cd apps/web && npx vitest run lib/guides.server.test.ts "app/[locale]/guides/[kind]/[slug]/page.test.tsx"
```

Then, against a running stack, open `/en/guides/howto/<a published slug, capitalised>`.

## Notes

- A slug that never existed anywhere answers 200 with "this article has not been written in the
  language you chose", which is also the wrong sentence. The obvious discriminator is not
  available to the web layer: `apps/api/app/guides/service.py` folds "no such article" and
  "inactive article" into one response with an empty `published_locales`. Fix that in the API
  first if this task wants to tell the two apart.
