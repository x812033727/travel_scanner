import {
  decodeFlowCookie,
  encodeFlowCookie,
  isOAuthProvider,
  localizedPath,
} from "./_shared";
import { describe, expect, it } from "vitest";

describe("OAuth BFF helpers", () => {
  it("accepts only supported providers", () => {
    expect(isOAuthProvider("google")).toBe(true);
    expect(isOAuthProvider("line")).toBe(true);
    expect(isOAuthProvider("apple")).toBe(true);
    expect(isOAuthProvider("github")).toBe(false);
  });

  it("round-trips the short-lived browser flow cookie", () => {
    const flow = {
      flowId: "flow-id",
      state: "state",
      binding: "binding",
      locale: "zh-TW" as const,
      next: "/trips/123?tab=plan",
      intent: "link" as const,
    };
    expect(decodeFlowCookie(encodeFlowCookie(flow))).toEqual(flow);
    expect(decodeFlowCookie("not-json")).toBeNull();
  });

  it("keeps redirects on the current site and preserves localized paths", () => {
    expect(localizedPath("ja", "/trips/123?tab=plan")).toBe("/ja/trips/123?tab=plan");
    expect(localizedPath("ko", "/zh-TW/account")).toBe("/zh-TW/account");
    expect(localizedPath("en", "//evil.example/path")).toBe("/en");
    expect(localizedPath("en", "/\\evil.example/path")).toBe("/en");
  });
});
