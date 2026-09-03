import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { CSP_BASELINE, buildStrictContentSecurityPolicy, createNonce } from "./csp";

describe("content security policy", () => {
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
