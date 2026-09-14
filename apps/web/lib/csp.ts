/**
 * Content Security Policy helpers.
 *
 * Three policies, and which one is enforced is the whole point of this file.
 *
 * `CSP_BASELINE` is enforced from `next.config.ts` on every response, including the ones
 * `proxy.ts` never sees — its matcher skips `/api`, `/_next` and anything with a file
 * extension. It carries only directives that cannot break a page, and nothing about scripts.
 *
 * `buildEnforcedContentSecurityPolicy` is enforced from `proxy.ts` on every document. It is
 * the half that decides whether a script runs at all: the nonce, `'strict-dynamic'`, and the
 * four baseline directives. Enforcing it is what stops an injected `<script>` or an
 * `onerror=` attribute, and it is safe to enforce because every script on the site either
 * carries the request nonce or is injected by one that does — see the evidence in
 * `e2e/csp.spec.ts`.
 *
 * `buildStrictContentSecurityPolicy` is the full policy and stays Report-Only, because the
 * resource directives are not yet proven. `connect-src` in particular names no Google Maps
 * host, so enforcing it today would break the map the first time a real browser key is
 * present — which no local run can reproduce, because the mock API serves no map keys.
 * Promote the rest only after production reports come back empty; the directives are
 * already being evaluated in every visitor's browser, so that evidence is free to collect.
 */
export const CSP_BASELINE =
  "frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self' https:";

const ANALYTICS_CONNECT_SOURCES = [
  "https://*.google-analytics.com",
  "https://*.analytics.google.com",
  "https://*.googletagmanager.com",
];
const TRAVELPAYOUTS_DRIVE_SOURCES = [
  "https://emrldtp.cc",
  "https://*.tp.media",
  "https://*.travelpayouts.com",
];
const NAVER_MAP_SOURCES = ["https://oapi.map.naver.com", "https://*.map.naver.com", "https://*.pstatic.net"];

export function createNonce(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return btoa(String.fromCharCode(...bytes));
}

/**
 * `adsense` relaxes the policy for one request, and only the two article routes with
 * advertising actually switched on ever ask for it (`proxy.ts`).
 *
 * Google's own guidance is that the ad code needs a nonce policy with `'unsafe-eval'`, and
 * that the domains it reaches change without notice, so host allowlists are unsupported and
 * "stricter policies may break without warning". That is a real loss, which is why it is
 * scoped this narrowly instead of being applied site-wide or to every article: with
 * advertising off — today, and the default — every response keeps the policy it has now.
 */
type PolicyOptions = { nonce: string; production: boolean; adsense?: boolean };

/**
 * Who may start a script chain. Shared so the enforced policy and the Report-Only one can
 * never disagree about it: a script the browser refuses under one and allows under the other
 * would make every report meaningless.
 *
 * The host entries are a fallback for browsers without `'strict-dynamic'` (Safari below
 * 15.4), which ignore the keyword and fall back to the list. Browsers that do support it
 * ignore the hosts entirely, so the entries cost nothing there — but while the policy was
 * only reporting, a missing host was invisible, and under enforcement it is a map that does
 * not draw. `maps.googleapis.com` (`components/route-map.tsx`) and `scripts.stay22.com`
 * (`components/stay22-script.tsx`) are both injected at runtime and were both absent.
 */
function scriptSources({ nonce, production, adsense = false }: PolicyOptions): string[] {
  return [
    "'self'",
    `'nonce-${nonce}'`,
    "'strict-dynamic'",
    "https://www.googletagmanager.com",
    "https://oapi.map.naver.com",
    "https://maps.googleapis.com",
    "https://scripts.stay22.com",
    "https://emrldtp.cc",
    ...(production && !adsense ? [] : ["'unsafe-eval'"]),
    ...(adsense ? ["https:"] : []),
  ];
}

/**
 * The enforced policy: script execution plus the four directives `CSP_BASELINE` already
 * carries. Deliberately no `default-src` — that would restrict connections, styles and fonts,
 * which is the half this does not yet claim to have verified.
 *
 * Enforcing this is not free of consequence for an article page carrying ads: `scriptSources`
 * widens to `'unsafe-eval' https:` there, which is close to no script restriction at all.
 * That is the same trade Google's own guidance forces (see `buildStrictContentSecurityPolicy`),
 * and it is now a real one rather than a reported one — the two article routes with
 * advertising switched on are the only documents on the site without script protection.
 */
export function buildEnforcedContentSecurityPolicy(options: PolicyOptions): string {
  return [
    `script-src ${scriptSources(options).join(" ")}`,
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self' https:",
    "frame-ancestors 'none'",
  ].join("; ");
}

export function buildStrictContentSecurityPolicy({
  nonce,
  production,
  adsense = false,
}: PolicyOptions): string {
  const mediaSources: string[] = [];
  try {
    const value = process.env.COMMUNITY_MEDIA_ORIGIN?.trim();
    if (value) {
      const url = new URL(value);
      const loopback = ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
      if (!url.username && !url.password && !url.hostname.includes("*") &&
          url.pathname === "/" && !url.search && !url.hash &&
          (url.protocol === "https:" || (!production && loopback && url.protocol === "http:"))) {
        mediaSources.push(url.origin);
      }
    }
  } catch { /* Invalid configuration never broadens policy. */ }
  const directives = [
    "default-src 'self'",
    `script-src ${scriptSources({ nonce, production, adsense }).join(" ")}`,
    // Tailwind output is a stylesheet, but React inline styles and the map SDKs need inline CSS.
    "style-src 'self' 'unsafe-inline'",
    // Provider photos and hotspot thumbnails come from arbitrary HTTPS hosts.
    `img-src 'self' data: blob: https:${mediaSources.length ? " " + mediaSources.join(" ") : ""}`,
    "font-src 'self' data:",
    `connect-src 'self' ${[...ANALYTICS_CONNECT_SOURCES, ...NAVER_MAP_SOURCES, ...TRAVELPAYOUTS_DRIVE_SOURCES, ...mediaSources, ...(adsense ? ["https:"] : [])].join(" ")}`,
    // External lodging and video frames load only after an explicit action;
    // neither needs provider scripts or connections in the parent page.
    `frame-src https://www.google.com https://www.stay22.com https://www.youtube-nocookie.com${adsense ? " https:" : ""}`,
    "worker-src 'self' blob:",
    "manifest-src 'self'",
    "media-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self' https:",
    "frame-ancestors 'none'",
  ];
  // `upgrade-insecure-requests` is ignored in Report-Only policies and Chromium
  // reports that misuse as a console error on every document. Transport
  // enforcement remains the responsibility of HTTPS plus the production HSTS
  // header until this strict policy is promoted from Report-Only.
  return directives.join("; ");
}
