import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CSP_BASELINE, buildStrictContentSecurityPolicy, createNonce } from "./csp";

describe("content security policy", () => {
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

  it("builds a nonce-based strict policy that only relaxes eval outside production", () => {
    const production = buildStrictContentSecurityPolicy({ nonce: "abc123", production: true });
    expect(production).toContain("script-src 'self' 'nonce-abc123' 'strict-dynamic'");
    expect(production).toContain("default-src 'self'");
    expect(production).toContain("upgrade-insecure-requests");
    expect(production).not.toContain("'unsafe-eval'");
    expect(production).not.toContain("'unsafe-inline' https://");
    expect(production).toContain("https://emrldtp.cc");
    expect(production).toContain("https://*.tp.media");
    const development = buildStrictContentSecurityPolicy({ nonce: "abc123", production: false });
    expect(development).toContain("'unsafe-eval'");
    expect(development).not.toContain("upgrade-insecure-requests");
  });

  it("creates unpredictable base64 nonces", () => {
    const first = createNonce();
    expect(first).toMatch(/^[A-Za-z0-9+/]{22}==$/);
    expect(createNonce()).not.toBe(first);
  });
});
