import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  CSP_BASELINE,
  buildEnforcedContentSecurityPolicy,
  buildStrictContentSecurityPolicy,
  createNonce,
} from "./csp";

const SCRIPT_SOURCES = "'self' 'nonce-abc123' 'strict-dynamic' https://www.googletagmanager.com https://oapi.map.naver.com https://maps.googleapis.com https://scripts.stay22.com https://emrldtp.cc";

/** What every response outside the two advertising article routes carries, in full. */
const STRICT_PRODUCTION = [
  "default-src 'self'",
  `script-src ${SCRIPT_SOURCES}`,
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
  it("permits the exact Stay22 frame origin and its loader, but never a parent connection to it", () => {
    const directives = buildStrictContentSecurityPolicy({ nonce: "n", production: true }).split("; ");
    expect(directives.find((value) => value.startsWith("frame-src"))).toBe("frame-src https://www.google.com https://www.stay22.com https://www.youtube-nocookie.com");
    // `components/stay22-script.tsx` injects scripts.stay22.com into the public document, so
    // naming it in script-src is describing what already happens rather than widening anything:
    // 'strict-dynamic' admits a runtime-injected script whatever the host list says. The entry
    // exists for browsers that ignore the keyword, and is the exact host, not a wildcard.
    const scripts = directives.find((value) => value.startsWith("script-src"))!;
    expect(scripts).toContain("https://scripts.stay22.com");
    expect(scripts).not.toContain("*.stay22.com");
    // The parent page still may not talk to Stay22 — only frame it and load its loader.
    expect(directives.filter((value) => !/^(frame|script)-src/.test(value)).join(";")).not.toContain("stay22");
  });

  it("enforces script execution and nothing that could break a page's resources", () => {
    const enforced = buildEnforcedContentSecurityPolicy({ nonce: "abc123", production: true });
    expect(enforced).toBe([
      `script-src ${SCRIPT_SOURCES}`,
      "object-src 'none'",
      "base-uri 'self'",
      "form-action 'self' https:",
      "frame-ancestors 'none'",
    ].join("; "));
    // The resource directives stay out on purpose: enforcing connect-src today would cut the
    // map's own XHR, which names no Google host. They remain in the Report-Only policy.
    for (const directive of ["default-src", "connect-src", "style-src", "font-src", "img-src", "frame-src", "media-src"]) {
      expect(enforced).not.toContain(directive);
    }
  });

  it("gates scripts identically in the enforced and the reported policy", () => {
    // A script allowed by one and refused by the other would make every report meaningless.
    const scriptSrc = (policy: string) => policy.split("; ").find((value) => value.startsWith("script-src"));
    for (const options of [
      { nonce: "abc123", production: true },
      { nonce: "abc123", production: false },
      { nonce: "abc123", production: true, adsense: true },
    ]) {
      expect(scriptSrc(buildEnforcedContentSecurityPolicy(options)))
        .toBe(scriptSrc(buildStrictContentSecurityPolicy(options)));
    }
  });

  it("keeps every enforced baseline directive in the enforced policy", () => {
    const enforced = buildEnforcedContentSecurityPolicy({ nonce: "n", production: true });
    // proxy.ts replaces the next.config.ts header on documents it handles, so anything the
    // baseline protects has to survive that replacement.
    for (const directive of CSP_BASELINE.split("; ")) expect(enforced).toContain(directive);
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
  it("promises HSTS for the subdomains too, and does not promise the preload list", () => {
    const config = readFileSync(resolve(__dirname, "..", "next.config.ts"), "utf8");
    // The header's own value, not the file: the paragraph above it in next.config.ts
    // explains why `preload` is absent, so a whole-file search finds the word either way.
    const hsts = /"Strict-Transport-Security",\s*value:\s*"([^"]*)"/.exec(config)?.[1];
    expect(hsts).toBe("max-age=31536000; includeSubDomains");
    // `preload` is a promise to browser vendors rather than to one visitor, and an entry
    // takes months to remove. Adding it is a separate decision, not a tidy-up of this line.
    expect(hsts).not.toContain("preload");
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
