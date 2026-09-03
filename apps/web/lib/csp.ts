/**
 * Content Security Policy helpers.
 *
 * `CSP_BASELINE` is enforced on every response from `next.config.ts`: it only contains directives
 * that cannot break a page (no plugins, no framing, no foreign <base>, form posts limited to this
 * site and HTTPS partners). The strict policy below is delivered as Report-Only from `proxy.ts`
 * so that violations show up in the browser console without breaking maps or analytics; switch it
 * to `Content-Security-Policy` once the console stays clean in production.
 */
export const CSP_BASELINE =
  "frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self' https:";

const ANALYTICS_CONNECT_SOURCES = [
  "https://*.google-analytics.com",
  "https://*.analytics.google.com",
  "https://*.googletagmanager.com",
];
const NAVER_MAP_SOURCES = ["https://oapi.map.naver.com", "https://*.map.naver.com", "https://*.pstatic.net"];

export function createNonce(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return btoa(String.fromCharCode(...bytes));
}

export function buildStrictContentSecurityPolicy({
  nonce,
  production,
}: {
  nonce: string;
  production: boolean;
}): string {
  const scriptSources = [
    "'self'",
    `'nonce-${nonce}'`,
    "'strict-dynamic'",
    // GA4 tag and the NAVER Maps loader are added by next/script; the host entries keep browsers
    // without 'strict-dynamic' support working.
    "https://www.googletagmanager.com",
    "https://oapi.map.naver.com",
    ...(production ? [] : ["'unsafe-eval'"]),
  ];
  const directives = [
    "default-src 'self'",
    `script-src ${scriptSources.join(" ")}`,
    // Tailwind output is a stylesheet, but React inline styles and the map SDKs need inline CSS.
    "style-src 'self' 'unsafe-inline'",
    // Provider photos and hotspot thumbnails come from arbitrary HTTPS hosts.
    "img-src 'self' data: blob: https:",
    "font-src 'self' data:",
    `connect-src 'self' ${[...ANALYTICS_CONNECT_SOURCES, ...NAVER_MAP_SOURCES].join(" ")}`,
    // Google Maps Embed API iframe in route-map.tsx.
    "frame-src https://www.google.com",
    "worker-src 'self' blob:",
    "manifest-src 'self'",
    "media-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self' https:",
    "frame-ancestors 'none'",
  ];
  if (production) directives.push("upgrade-insecure-requests");
  return directives.join("; ");
}
