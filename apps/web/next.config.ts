import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

// Mirrors CSP_BASELINE in lib/csp.ts (next.config.ts cannot import application modules); the strict
// nonce-based policy is sent as Report-Only from proxy.ts.
const cspBaseline =
  "frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self' https:";

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), browsing-topics=()" },
  { key: "Content-Security-Policy", value: cspBaseline },
  // `includeSubDomains` added 2026-09-14, on the owner's confirmation that nothing under
  // mokaair.com is served over plain HTTP. It has to be asked rather than inferred: a browser
  // that sees this honours it for a year, so a subdomain still on HTTP goes dark for everyone
  // who visited the site once, and the repository cannot enumerate the DNS.
  // `preload` is deliberately not here. It is the same promise made to browser vendors
  // instead of to one visitor, and removing an entry from the preload list takes months.
  ...(process.env.NODE_ENV === "production"
    ? [{ key: "Strict-Transport-Security", value: "max-age=31536000; includeSubDomains" }]
    : []),
];

const nextConfig: NextConfig = {
  output: "standalone",
  allowedDevOrigins: ["127.0.0.1"],
  poweredByHeader: false,
  async headers() {
    return [
      { source: "/:path*", headers: securityHeaders },
      {
        // Next sends config headers before Route Handler headers and will not
        // overwrite them. Clickouts own their policy: no-referrer on a 303,
        // same-origin on recoverable HTML so the retry POST retains its Origin.
        source: "/:path((?!api/travel/.*/clickout/?$).*)",
        headers: [{ key: "Referrer-Policy", value: "strict-origin-when-cross-origin" }],
      },
    ];
  },
};
export default withNextIntl(nextConfig);
