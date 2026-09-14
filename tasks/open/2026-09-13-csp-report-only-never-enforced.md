---
id: 2026-09-13-csp-report-only-never-enforced
title: Promote the strict CSP from Report-Only to enforced
status: review
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-14T00:10:45Z
created_at: 2026-09-13T23:37:40Z
completed_at:
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - apps/web/proxy.ts
  - apps/web/lib/csp.ts
  - apps/web/next.config.ts
  - apps/web/lib/csp.test.ts
  - apps/web/e2e/csp.spec.ts
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

- [x] An injected `<script>` without the request's nonce does not execute on a production
      page, and the browser console shows the refusal from `Content-Security-Policy`, not
      from `Content-Security-Policy-Report-Only`.
- [x] Maps, GA4, Stay22, Travelpayouts and the theme/text-size bootstrap scripts all still
      work in all five locales, signed in and signed out.
- [ ] `Strict-Transport-Security` carries `includeSubDomains`, or a note here says which
      subdomain is not on HTTPS and therefore blocks it. **Left open — see Notes.**

## Steps

- [x] Collect the evidence first. Done twice, against a production build: 20 routes across
      all five locales, before and after the change, with a control that proves the harness
      detects both a script and a connection refusal. Zero violations either time.
- [x] Add any domain the evidence proves is needed. Two were missing from `script-src`:
      `https://maps.googleapis.com` and `https://scripts.stay22.com`, both injected at
      runtime by `route-map.tsx` and `stay22-script.tsx`.
- [x] Enforce the script half from `proxy.ts`. Not the whole policy — see the decision below.
- [x] Decide what AdSense does to this. Written down in `buildEnforcedContentSecurityPolicy`:
      the two article routes with ads on widen to `'unsafe-eval' https:` and are now the only
      documents on the site without real script protection. Accepted, not gated further.
- [ ] `upgrade-insecure-requests`: still omitted, and still correctly so. It is a resource
      directive, so it belongs with the half that is still Report-Only, where Chromium logs
      its own console error for the misuse. It goes in when the rest is promoted.
- [ ] HSTS `includeSubDomains`: not done. See Notes.

## What was actually done, and what was deliberately not

The policy was split rather than flipped whole.

`buildEnforcedContentSecurityPolicy` — `script-src` with the nonce and `'strict-dynamic'`,
plus the four baseline directives — is now sent as a real `Content-Security-Policy` from
`proxy.ts`. `buildStrictContentSecurityPolicy` stays Report-Only with the full directive set.

Enforcing the script half is the whole of the XSS control and carries no feature risk:
`'strict-dynamic'` admits anything a nonce-carrying script injects, which is how every
third-party SDK on this site loads. Enforcing the resource half would have carried real
risk and almost no additional security: **`connect-src` names no Google Maps host**, and
`components/route-map.tsx` loads `maps.googleapis.com`, whose API then makes its own XHR.
No local run can reproduce that — the e2e runtime API serves no map browser key — so
enforcing `connect-src` today would have broken the map the first time production served a
real key, and the ten-day Report-Only window never surfaced it because nobody read the
reports.

So the work left is narrower and now has an owner: read production reports for the resource
directives, add what they prove is needed, then promote them and add
`upgrade-insecure-requests`. `e2e/csp.spec.ts` has the expectation that has to change when
that happens, named in a comment.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run check:i18n && npm run test:web
npm run build:web
cd apps/web && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/csp.spec.ts \
  e2e/guides-adsense.spec.ts e2e/stay22-script.spec.ts e2e/navigation.spec.ts
```

`e2e/csp.spec.ts` is the evidence pass, kept rather than thrown away: it fails on a
Report-Only violation as well as an enforced one, so the reports that decide the rest of
this work cannot go unread again.

## Notes

- **HSTS `includeSubDomains` was not added, on purpose.** It cannot be decided from the
  repository: `COMMUNITY_MEDIA_ORIGIN` is a configurable subdomain and production validation
  already forces it to HTTPS, but nothing here can enumerate the rest of `mokaair.com`, and a
  browser that sees the directive honours it for a year. Getting it wrong takes a subdomain
  off the air for everyone who visited once. Whoever knows the DNS should add
  `includeSubDomains` to `next.config.ts`; `preload` is a separate, harder-to-undo decision.
- Evidence that the enforcement is real, from the control case: before, an injected
  `<img src=x onerror=...>` executed and produced a `disposition: "report"` entry. After, the
  same payload produces `disposition: "enforce"` and does not execute. That case is now
  `e2e/csp.spec.ts::an injected inline handler is refused, not merely reported`.
- Google Maps, NAVER Maps and the GTM tag were each loaded under the enforced `script-src`
  with no `'unsafe-eval'`, in a standalone probe: none of them violated it. That was the one
  risk that could not be ruled out by reading code, and it is why enforcing without eval is
  safe here.
- Rolling back is one line: send `reported` instead of `enforced` on the response header in
  `proxy.ts`. No environment variable was added for this — a knob that is in neither
  `.env.example` nor the compose file is worse than a revert.
- `proxy.ts` now sets the request header as `content-security-policy` rather than
  `content-security-policy-report-only`. Next reads the former first and only falls back to
  the latter (`next/dist/server/app-render/app-render.js`), so the nonce arrived either way;
  the rename just stops a reader having to know about the fallback.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
