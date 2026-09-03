import createMiddleware from "next-intl/middleware";
import type { NextRequest } from "next/server";
import { routing } from "./i18n/routing";
import { buildStrictContentSecurityPolicy, createNonce } from "./lib/csp";

const handleLocale = createMiddleware(routing);

export default function proxy(request: NextRequest) {
  const nonce = createNonce();
  const policy = buildStrictContentSecurityPolicy({
    nonce,
    production: process.env.NODE_ENV === "production",
  });
  // next-intl copies the incoming request headers into NextResponse.next({ request }), so the
  // renderer sees this header, applies the nonce to Next.js' own inline scripts, and the layout can
  // read the nonce for the theme bootstrap script.
  request.headers.set("content-security-policy-report-only", policy);
  request.headers.set("x-nonce", nonce);
  const response = handleLocale(request);
  response.headers.set("Content-Security-Policy-Report-Only", policy);
  return response;
}

export const config = {
  matcher: ["/((?!api|_next|_vercel|.*\\..*).*)"],
};
