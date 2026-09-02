import { describe, expect, it } from "vitest";
import {
  forwardedClientAddress,
  isAllowedMutationOrigin,
  observedRequestOrigin,
  safeRedirectLocation,
  validateProxyPath,
} from "./proxy-security";

describe("travel API proxy security", () => {
  it("encodes ordinary segments and rejects traversal or separator smuggling", () => {
    expect(validateProxyPath(["shared-trips", "台北 token"])).toBe(
      "shared-trips/%E5%8F%B0%E5%8C%97%20token",
    );
    expect(validateProxyPath(["..", "ready"])).toBeUndefined();
    expect(validateProxyPath(["trips/../../ready"])).toBeUndefined();
    expect(validateProxyPath(["trips\\..\\ready"])).toBeUndefined();
  });

  it("rejects cross-site state changes while allowing reads and same-site posts", () => {
    expect(isAllowedMutationOrigin("GET", "https://evil.example", "https://mokaair.com")).toBe(true);
    expect(isAllowedMutationOrigin("POST", "https://mokaair.com", "https://mokaair.com")).toBe(true);
    expect(isAllowedMutationOrigin("POST", "https://evil.example", "https://mokaair.com")).toBe(false);
    expect(isAllowedMutationOrigin("POST", null, "https://mokaair.com")).toBe(false);
  });

  it("uses the observed Host when Next normalizes a development URL", () => {
    const observed = observedRequestOrigin(
      new Headers({ host: "127.0.0.1:3000" }),
      "http://localhost:3000",
    );
    expect(observed).toBe("http://127.0.0.1:3000");
    expect(isAllowedMutationOrigin("POST", observed, observed)).toBe(true);
  });

  it("only forwards relative, same-origin HTTP, or HTTPS redirects", () => {
    expect(safeRedirectLocation("/login", "https://mokaair.com")).toBe("/login");
    expect(safeRedirectLocation("https://www.booking.com/", "https://mokaair.com")).toBe("https://www.booking.com/");
    expect(safeRedirectLocation("javascript:alert(1)", "https://mokaair.com")).toBeUndefined();
    expect(safeRedirectLocation("http://evil.example/", "https://mokaair.com")).toBeUndefined();
  });

  it("uses the right-most proxy address and bounds forwarded header length", () => {
    expect(forwardedClientAddress(new Headers({ "x-forwarded-for": "192.0.2.1, 198.51.100.8" }))).toBe("198.51.100.8");
    expect(forwardedClientAddress(new Headers({ "x-real-ip": "203.0.113.9" }))).toBe("203.0.113.9");
    expect(forwardedClientAddress(new Headers({ "x-real-ip": "x".repeat(65) }))).toBeUndefined();
  });
});
