import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CSP_BASELINE, buildStrictContentSecurityPolicy, createNonce } from "./csp";

/** What every response outside the two advertising article routes carries, in full. */
const STRICT_PRODUCTION = [
  "default-src 'self'",
  "script-src 'self' 'nonce-abc123' 'strict-dynamic' https://www.googletagmanager.com https://oapi.map.naver.com https://emrldtp.cc",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data: blob: https:",
  "font-src 'self' data:",
  "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://oapi.map.naver.com https://*.map.naver.com https://*.pstatic.net https://emrldtp.cc https://*.tp.media https://*.travelpayouts.com",
  "frame-src https://www.google.com https://www.stay22.com https://www.youtube-nocookie.com",
  "worker-src 'self' blob:",
  "manifest-src 'self'",
  "media-src 'self'",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self' https:",
  "frame-ancestors 'none'",
].join("; ");

describe("content security policy", () => {
  it("permits the exact Stay22 frame origin without allowing its scripts or parent connections", () => {
    const directives = buildStrictContentSecurityPolicy({ nonce: "n", production: true }).split("; ");
    expect(directives.find((value) => value.startsWith("frame-src"))).toBe("frame-src https://www.google.com https://www.stay22.com https://www.youtube-nocookie.com");
    expect(directives.filter((value) => !value.startsWith("frame-src")).join(";")).not.toContain("stay22");
  });
  it("permits only the privacy-enhanced YouTube frame, not provider parent scripts or connections", () => {
    const directives = buildStrictContentSecurityPolicy({ nonce: "n", production: true }).split("; ");
    const frames = directives.find((value) => value.startsWith("frame-src"))!;
    expect(frames).toContain("https://www.youtube-nocookie.com");
    expect(frames).not.toContain("https://www.youtube.com");
    expect(frames).not.toContain("*.youtube");
    expect(directives.filter((value) => !value.startsWith("frame-src")).join(";")).not.toContain("youtube");
  });
  afterEach(() => vi.unstubAllEnvs());
  it("allows only the configured media origin, with local HTTP limited to development", () => {
    vi.stubEnv("COMMUNITY_MEDIA_ORIGIN", "https://media.example.test");
    expect(buildStrictContentSecurityPolicy({ nonce: "n", production: true }).split(";").find((x) => x.includes("connect-src"))).toContain("https://media.example.test");
    vi.stubEnv("COMMUNITY_MEDIA_ORIGIN", "http://127.0.0.1:9000");
    expect(buildStrictContentSecurityPolicy({ nonce: "n", production: false })).toContain("http://127.0.0.1:9000");
    expect(buildStrictContentSecurityPolicy({ nonce: "n", production: true })).not.toContain("http://127.0.0.1:9000");
    for (const value of ["https://*.example.test", "https://user:pass@media.example.test", "https://media.example.test/path", "https://media.example.test; script-src *", "http://external.example.test"]) {
      vi.stubEnv("COMMUNITY_MEDIA_ORIGIN", value);
      expect(buildStrictContentSecurityPolicy({ nonce: "n", production: false })).not.toContain("external.example.test");
      expect(buildStrictContentSecurityPolicy({ nonce: "n", production: false })).not.toContain("media.example.test");
    }
  });
  it("keeps the enforced baseline identical in next.config.ts", () => {
    const config = readFileSync(resolve(__dirname, "..", "next.config.ts"), "utf8");
    expect(config).toContain(CSP_BASELINE);
    expect(CSP_BASELINE).toContain("frame-ancestors 'none'");
    expect(CSP_BASELINE).toContain("object-src 'none'");
    expect(CSP_BASELINE).toContain("form-action 'self' https:");
  });

  it("builds a nonce-based report-only policy that only relaxes eval outside production", () => {
    const production = buildStrictContentSecurityPolicy({ nonce: "abc123", production: true });
    expect(production).toContain("script-src 'self' 'nonce-abc123' 'strict-dynamic'");
    expect(production).toContain("default-src 'self'");
    expect(production).not.toContain("upgrade-insecure-requests");
    expect(production).not.toContain("'unsafe-eval'");
    expect(production).not.toContain("'unsafe-inline' https://");
    expect(production).toContain("https://emrldtp.cc");
    expect(production).toContain("https://*.tp.media");
    const development = buildStrictContentSecurityPolicy({ nonce: "abc123", production: false });
    expect(development).toContain("'unsafe-eval'");
    expect(development).not.toContain("upgrade-insecure-requests");
  });

  it("serves every non-article response this exact policy", () => {
    // Pinned in full on purpose. Advertising is meant to change the policy for two article
    // routes and nothing else, and an assertion like
    // `build({adsense: false}) === build({})` would only prove the default parameter works —
    // it would still pass if both had been widened together. This is the string the rest of
    // the site gets, so widening it anywhere has to be a deliberate edit here.
    vi.stubEnv("COMMUNITY_MEDIA_ORIGIN", "");
    expect(buildStrictContentSecurityPolicy({ nonce: "abc123", production: true })).toBe(STRICT_PRODUCTION);
    expect(buildStrictContentSecurityPolicy({ nonce: "abc123", production: true, adsense: false }))
      .toBe(STRICT_PRODUCTION);
    // Outside production the only difference is eval, and it is added in place rather than
    // dragging any other source along with it.
    expect(buildStrictContentSecurityPolicy({ nonce: "abc123", production: false }))
      .toBe(STRICT_PRODUCTION.replace("https://emrldtp.cc", "https://emrldtp.cc 'unsafe-eval'"));
  });

  it("relaxes exactly three directives for an article page carrying ads, and no others", () => {
    vi.stubEnv("COMMUNITY_MEDIA_ORIGIN", "");
    const strict = buildStrictContentSecurityPolicy({ nonce: "abc123", production: true });
    const ads = buildStrictContentSecurityPolicy({ nonce: "abc123", production: true, adsense: true });
    const byName = (policy: string) =>
      new Map(policy.split("; ").map((directive) => [directive.split(" ")[0], directive]));
    const before = byName(strict), after = byName(ads);
    // No directive appears or disappears — the relaxation is only ever a widening of three.
    expect([...after.keys()]).toEqual([...before.keys()]);
    expect([...before.keys()].filter((name) => before.get(name) !== after.get(name)))
      .toEqual(["script-src", "connect-src", "frame-src"]);
    // Google documents that the ad code needs eval and that the domains it reaches change
    // without notice, so host allowlists are unsupported for frames and connections.
    expect(after.get("script-src")).toBe(`${before.get("script-src")} 'unsafe-eval' https:`);
    expect(after.get("connect-src")).toBe(`${before.get("connect-src")} https:`);
    expect(after.get("frame-src")).toBe(`${before.get("frame-src")} https:`);
    // Relaxed, not abandoned: the nonce still gates which scripts may start the chain, and
    // nothing about framing, plugins or form targets moves.
    expect(ads).toContain("script-src 'self' 'nonce-abc123' 'strict-dynamic'");
    expect(ads).not.toContain("upgrade-insecure-requests");
  });

  it("creates unpredictable base64 nonces", () => {
    const first = createNonce();
    expect(first).toMatch(/^[A-Za-z0-9+/]{22}==$/);
    expect(createNonce()).not.toBe(first);
  });
});
