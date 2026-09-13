import createMiddleware from "next-intl/middleware";
import type { NextRequest } from "next/server";
import { routing } from "./i18n/routing";
import { adsenseRequestGate } from "./lib/adsense";
import { fetchAdsenseConfig } from "./lib/adsense-config";
import { buildStrictContentSecurityPolicy, createNonce } from "./lib/csp";

const handleLocale = createMiddleware(routing);

export default async function proxy(request: NextRequest) {
  const nonce = createNonce();
  // Only a request that could actually be served an ad relaxes anything: same host, DNT/GPC
  // and path gate the renderer applies, plus advertising being switched on. Every other
  // response keeps the strict policy unchanged. `fetchAdsenseConfig` answers from a
  // process-local cache and fails closed, so this is not a round trip per request and an
  // unreachable API cannot loosen the policy.
  //
  // Two costs, both deliberate. For up to the cache's lifetime after the owner switches
  // advertising on, article pages still carry the strict policy — harmless while it is
  // Report-Only, a minute of blocked ads once enforced. And an article URL whose article does
  // not exist still gets the relaxed policy, because the renderer establishes that with an
  // API read this cannot afford per request; that page carries no ad code either way.
  const adsense = adsenseRequestGate({
    host: request.headers.get("host"),
    dnt: request.headers.get("dnt"),
    gpc: request.headers.get("sec-gpc"),
    pathname: request.nextUrl.pathname,
  }) !== null && (await fetchAdsenseConfig()).enabled;
  const policy = buildStrictContentSecurityPolicy({
    nonce,
    production: process.env.NODE_ENV === "production",
    adsense,
  });
  // next-intl copies the incoming request headers into NextResponse.next({ request }), so the
  // renderer sees this header, applies the nonce to Next.js' own inline scripts, and the layout can
  // read the nonce for the theme bootstrap script.
  request.headers.set("content-security-policy-report-only", policy);
  request.headers.set("x-nonce", nonce);
  // Nested server layouts use this trusted request header to retain the exact
  // in-app destination when an unauthenticated administrator is sent to login.
  request.headers.set("x-travel-pathname", `${request.nextUrl.pathname}${request.nextUrl.search}`);
  const response = handleLocale(request);
  response.headers.set("Content-Security-Policy-Report-Only", policy);
  return response;
}

export const config = {
  matcher: ["/((?!api|_next|_vercel|.*\\..*).*)"],
};
