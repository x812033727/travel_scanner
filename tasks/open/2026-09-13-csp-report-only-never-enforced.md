---
id: 2026-09-13-csp-report-only-never-enforced
title: Promote the strict CSP from Report-Only to enforced
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-13T23:37:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/proxy.ts
  - apps/web/lib/csp.ts
  - apps/web/next.config.ts
  - apps/web/lib/csp.test.ts
---

# Promote the strict CSP from Report-Only to enforced

## Why

Two policies ship on every page and only the weak one is enforced.

`next.config.ts` sends `CSP_BASELINE` as a real `Content-Security-Policy`:

```
frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self' https:
```

That stops framing, plugins, a foreign `<base>` and off-site form posts. It says nothing
about `script-src`, so it stops no script at all. The policy that does —
`buildStrictContentSecurityPolicy()` in `lib/csp.ts`, with `'nonce-…' 'strict-dynamic'` —
is sent by `proxy.ts` as `Content-Security-Policy-Report-Only`, which browsers log and
then ignore.

So today an injected `<script>` anywhere in the tree executes. Every other part of the
XSS story is already done — no `dangerouslySetInnerHTML` outside JSON-LD and the two
nonce'd bootstrap scripts, structured content blocks instead of stored HTML, a shared
link sanitizer — which is exactly why the last step is worth taking: the nonce plumbing
is built and the strict policy is already being evaluated by every visitor's browser,
just with its verdict discarded.

`docs/security-audit-2026-09.md` WEB-02 introduced the report-only policy on 2026-09-03
and listed promotion as recommendation #3, conditional on "a week or two" of clean
production console output. That window has now passed in calendar terms, but nobody has
recorded whether the console is actually clean — see Notes.

While here: `Strict-Transport-Security` is `max-age=31536000` with no `includeSubDomains`
(WEB-12), so a subdomain served over plain HTTP is still a downgrade path.

## Definition of done

- [ ] An injected `<script>` without the request's nonce does not execute on a production
      page, and the browser console shows the refusal from `Content-Security-Policy`, not
      from `Content-Security-Policy-Report-Only`.
- [ ] Maps, GA4, Stay22, Travelpayouts and the theme/text-size bootstrap scripts all still
      work in all five locales, signed in and signed out.
- [ ] `Strict-Transport-Security` carries `includeSubDomains`, or a note here says which
      subdomain is not on HTTPS and therefore blocks it.

## Steps

- [ ] Collect the evidence first: load the article, explore, planner, trip, community and
      admin routes in production (or a production build against production config) and
      record every `Content-Security-Policy-Report-Only` violation. Nothing below is safe
      until that list is empty.
- [ ] Add any domain the evidence proves is needed to `lib/csp.ts`, one entry per domain,
      with the reason in a comment.
- [ ] `proxy.ts`: change the **response** header from `Content-Security-Policy-Report-Only`
      to `Content-Security-Policy`. Leave the **request** header alone — the renderer reads
      it to apply the nonce to Next.js' own inline scripts, and renaming it silently drops
      the nonce from every script tag.
- [ ] Decide what AdSense does to this. With ads on, `buildStrictContentSecurityPolicy`
      already relaxes an article page to `script-src … https: 'unsafe-eval'` plus
      `frame-src https:` and `connect-src https:`, which once enforced means article pages
      with ads get roughly no script protection. Either accept that in writing here, or
      gate ads behind a stricter arrangement.
- [ ] `upgrade-insecure-requests` is currently omitted because it is ignored in Report-Only
      and Chromium logs the misuse. Once enforced it becomes meaningful — add it.
- [ ] `next.config.ts`: add `includeSubDomains` to HSTS after confirming every subdomain is
      HTTPS. Leave `preload` for a separate decision; it is hard to undo.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
npm run build:web
npx playwright test e2e/navigation.spec.ts
```

Then, against a production build, load one page per route family with the console open and
confirm zero CSP violations and that every `<script>` carries the request's nonce. The
2026-09 audit used a custom Playwright script for exactly this check (§8 of
`docs/security-audit-2026-09.md`); reusing it is cheaper than inventing one.

## Notes

- Do not flip the header without the evidence pass. A wrong `script-src` here takes down
  maps and analytics on every page at once, and Report-Only exists precisely so that
  evidence can be gathered for free.
- The enforced baseline in `next.config.ts` and `CSP_BASELINE` in `lib/csp.ts` are
  deliberately duplicated — `next.config.ts` cannot import application modules. If you edit
  one, edit the other.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`), which
  found no new exploitable defect and rates this the largest remaining gap.
