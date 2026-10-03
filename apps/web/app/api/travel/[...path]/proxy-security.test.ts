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

  it("refuses a relative location that a browser would resolve to another host", () => {
    const sameSite = "https://mokaair.com";
    // Why each of these is dangerous: for http(s) a browser reads `\` as `/` and drops tab and
    // newline before parsing, so every one of them lands on evil.example.
    const offSite = ["/\\evil.example/x", "/\\\\evil.example/x", "/\\/evil.example/x", "//evil.example/x", "/\t/evil.example/x", "/\n/evil.example/x"];
    for (const location of offSite) {
      expect(new URL(location, sameSite).host).toBe("evil.example");
      expect(safeRedirectLocation(location, sameSite)).toBeUndefined();
    }
    // Any other control character is refused too: a header value cannot carry it, and a
    // relative path never needs one.
    for (const location of ["/login\r\nSet-Cookie: a=b", "/login\0", "/login\u007f"]) {
      expect(safeRedirectLocation(location, sameSite)).toBeUndefined();
    }
    // An escaped backslash stays a path on this site, so it is still forwarded unchanged.
    expect(new URL("/%5Cevil.example/x", sameSite).host).toBe("mokaair.com");
    expect(safeRedirectLocation("/%5Cevil.example/x", sameSite)).toBe("/%5Cevil.example/x");
    expect(safeRedirectLocation("/zh-TW/trips?tab=flights#top", sameSite)).toBe("/zh-TW/trips?tab=flights#top");
  });

  it("uses the right-most proxy address and bounds forwarded header length", () => {
    expect(forwardedClientAddress(new Headers({ "x-forwarded-for": "192.0.2.1, 198.51.100.8" }))).toBe("198.51.100.8");
    expect(forwardedClientAddress(new Headers({ "x-real-ip": "203.0.113.9" }))).toBe("203.0.113.9");
    expect(forwardedClientAddress(new Headers({ "x-real-ip": "x".repeat(65) }))).toBeUndefined();
  });
});
