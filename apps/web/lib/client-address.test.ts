import { describe, expect, it } from "vitest";
import { forwardedClientAddress } from "./client-address";

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
