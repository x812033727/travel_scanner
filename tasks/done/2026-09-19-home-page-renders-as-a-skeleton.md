---
id: 2026-09-19-home-page-renders-as-a-skeleton
title: Home page renders as a skeleton to crawlers: SSR the discovery feed
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-19T13:55:21Z
created_at: 2026-09-19T13:55:04Z
completed_at: 2026-09-19T16:00:02Z
branch: claude/google-indexing-issues-efbfb9
depends_on: []
scope:
  - apps/web/app/[locale]/page.tsx
  - apps/web/components/discovery/explorer.tsx
---

# Home page renders as a skeleton to crawlers: SSR the discovery feed

## Why

Fetched live as Googlebot, `https://mokaair.com/zh-TW` answers 227KB of HTML containing
**361 characters of visible text**, and the text is "正在載入旅行靈感" -- the loading skeleton.
`/en` is the same at 753. The hero, the quick cards and the 33-city destination rail are all
absent from the response body. This is the site's strongest page and it looks empty to a
crawler, which is a direct cause of "已檢索－目前尚未建立索引" in Search Console.

`app/[locale]/page.tsx:196` wraps the whole body in `<DiscoveryHomeGate>`, and
`components/discovery/explorer.tsx:33` returned `<DiscoveryExplorer home initialEnabled={...} />`
with **no `initialFeed`** -- so `useDiscoveryResource` had no data on the first render and
`Results` fell through to `<DiscoverySkeleton/>`. `body` was discarded, not merged.

The seam already existed: `DiscoveryExplorer` accepts `initialFeed`, the doc comment above it
already says that without one "this component's whole body is a skeleton in the response --
nothing for a crawler to read", and `/explore` has been passing one since it was written
(`app/[locale]/explore/page.tsx:21`). The home page simply never did.

## Definition of done

- [x] `/zh-TW` and `/en` carry the feed's first page in the response body, not a skeleton
- [x] a failed or empty feed read renders the marketing body instead, never a skeleton
- [x] a test fails without the fix

## Steps

- [x] `page.tsx` calls `getInitialDiscoveryFeed(locale, discoveryFeedPath({}, discovery.enabled))`
- [x] `DiscoveryHomeGate` takes `initialFeed` and forwards it to `DiscoveryExplorer`
- [x] seed the gate with `discovery.enabled && Boolean(feed)` so the failure path is the
      marketing body rather than a skeleton
- [x] two cases in `app/[locale]/page.seo.test.tsx`

## How to verify

```bash
npx vitest run "app/[locale]/page.seo.test.tsx"     # 4 passed
```

Both new cases were confirmed to fail against the pre-fix code (`git checkout` the two
source files, rerun, `2 failed`), so they genuinely cover the bug.

After deploying, against production:

```bash
curl -sA Googlebot https://mokaair.com/zh-TW | python -c "import sys,re;h=sys.stdin.read();b=re.sub(r'(?is)<script.*?</script>|<style.*?</style>','',h);print(len(re.sub(r'\s+',' ',re.sub(r'(?s)<[^>]+>',' ',b)).strip()))"
```

Was 361. Expect the feed's card titles and summaries instead.

## Notes

**The existing tests never covered this.** `page.seo.test.tsx` ran only with
`state.enabled = false`, and `tools/e2e-runtime-api.mjs:151-153` serves `{"enabled": false}`
to the e2e suite with a comment claiming it matches production -- production is plainly
discovery-on. So `e2e/seo.spec.ts` has never exercised the configuration that is actually
deployed. Worth a follow-up task: give the fixture a discovery-on mode.

**Deliberately not done here:** moving the destination rail (`page.tsx:133-186`) outside the
gate so its 33 city links are in the HTML in both states. That is worth doing -- it takes the
home page's only internal-linking hub out of the feed read's failure domain -- but it changes
what a reader sees when discovery is on, which is a product decision rather than a crawler
fix. The footer's `/destinations` link still reaches all 33.

`resolveDiscoveryStatus` (`lib/discovery.ts:84`) returns the server prop while the client store
is loading, so seeding `initialEnabled` with `false` on a failed read causes no hydration
mismatch: both sides render the marketing body on the first pass and the store corrects after.

**Verified on production after #566 (`ecc6cbc0`) deployed 2026-09-19 15:56 UTC.** Visible
text as Googlebot: `/zh-TW` **361 -> 1,775 chars**, `/en` **753 -> 3,991**. The skeleton
string (正在載入旅行靈感 / Loading travel ideas) is gone from both.
