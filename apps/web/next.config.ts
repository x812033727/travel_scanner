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
  ...(process.env.NODE_ENV === "production"
    ? [{ key: "Strict-Transport-Security", value: "max-age=31536000" }]
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
