import { afterEach, describe, expect, it, vi } from "vitest";
import { forwardedClientAddress, forwardedClientHeaders } from "./client-address";

describe("forwarded client address", () => {
  it("takes the right-most proxy entry, which is the only one we appended ourselves", () => {
    expect(forwardedClientAddress(new Headers({ "x-forwarded-for": "192.0.2.1, 198.51.100.8" }))).toBe("198.51.100.8");
  });

  it("falls back to x-real-ip", () => {
    expect(forwardedClientAddress(new Headers({ "x-real-ip": "203.0.113.9" }))).toBe("203.0.113.9");
  });

  it("bounds the value so a header cannot become an unbounded cache key", () => {
    expect(forwardedClientAddress(new Headers({ "x-real-ip": "x".repeat(65) }))).toBeUndefined();
  });

  it("is undefined when nothing forwarded an address", () => {
    expect(forwardedClientAddress(new Headers())).toBeUndefined();
  });
});

describe("forwarded client headers", () => {
  afterEach(() => vi.unstubAllEnvs());

  it("sends the address alone when no token is configured", () => {
    expect(forwardedClientHeaders(new Headers({ "x-real-ip": "203.0.113.9" }))).toEqual({
      "X-Travel-Client-IP": "203.0.113.9",
    });
  });

  it("vouches for the address with the token once one is configured", () => {
    vi.stubEnv("INTERNAL_PROXY_TOKEN", "shared-secret");
    expect(forwardedClientHeaders(new Headers({ "x-real-ip": "203.0.113.9" }))).toEqual({
      "X-Travel-Client-IP": "203.0.113.9",
      "X-Travel-Proxy-Token": "shared-secret",
    });
  });

  // The token says "this address came from us". With no address there is nothing to say it
  // about, and sending it anyway would leak the secret to upstreams that had no use for it.
  it("sends nothing at all when there is no address to vouch for", () => {
    vi.stubEnv("INTERNAL_PROXY_TOKEN", "shared-secret");
    expect(forwardedClientHeaders(new Headers())).toEqual({});
  });
});
