import { NextRequest } from "next/server";
import { siteUrl } from "@/lib/seo";
import {
  callback,
  decodeFlowCookie,
  encodeFlowCookie,
  flowCookieName,
  isOAuthProvider,
  localizedPath,
} from "./_shared";
import { afterEach, describe, expect, it, vi } from "vitest";

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

describe("OAuth callback body handling", () => {
  it("rejects an oversized form_post body before buffering it", async () => {
    const request = new NextRequest("https://mokaair.com/api/auth/oauth/google/callback", {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: `state=x&code=${"a".repeat(64 * 1024)}`,
    } as unknown as ConstructorParameters<typeof NextRequest>[1]);
    const response = await callback(request, "google");
    expect(response.status).toBeGreaterThanOrEqual(300);
    expect(response.status).toBeLessThan(400);
    const location = new URL(response.headers.get("location") ?? "", "https://mokaair.com");
    expect(location.searchParams.get("oauth_error")).toBe("oauth_token_invalid");
  });

  it("still reads a normal form_post body", async () => {
    // No flow cookie is present, so a small, well-formed body must reach the state
    // check (proving it was parsed) and fail there rather than on the size limit.
    const request = new NextRequest("https://mokaair.com/api/auth/oauth/google/callback", {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: "state=some-state&code=some-code",
    } as unknown as ConstructorParameters<typeof NextRequest>[1]);
    const response = await callback(request, "google");
    const location = new URL(response.headers.get("location") ?? "", "https://mokaair.com");
    expect(location.searchParams.get("oauth_error")).toBe("oauth_state_invalid");
  });
});

describe("OAuth callback redirects behind the reverse proxy", () => {
  // In production the request reaches Next at the container's bind address, so its own
  // origin is https://0.0.0.0:3000. A redirect built on it strands the browser.
  const internal = "https://0.0.0.0:3000/api/auth/oauth/google/callback";
  const publicOrigin = new URL(siteUrl).origin;

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns a failed callback to the public login page", async () => {
    const response = await callback(new NextRequest(`${internal}?state=bogus&code=bogus`), "google");
    const location = new URL(response.headers.get("location") ?? "");
    expect(location.origin).toBe(publicOrigin);
    expect(location.pathname).toMatch(/\/login$/);
    expect(location.searchParams.get("oauth_error")).toBe("oauth_state_invalid");
  });

  it("returns a successful sign-in to the public site", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ access_token: "token", expires_in: 3600 }), { status: 200 }),
    ));
    const flow = {
      flowId: "flow-id",
      state: "state",
      binding: "binding",
      locale: "ja" as const,
      next: "/trips/123",
      intent: "login" as const,
    };
    const request = new NextRequest(`${internal}?state=state&code=code`, {
      headers: { cookie: `${flowCookieName("google")}=${encodeFlowCookie(flow)}` },
    });
    const response = await callback(request, "google");
    const location = new URL(response.headers.get("location") ?? "");
    expect(location.origin).toBe(publicOrigin);
    expect(location.pathname).toBe("/ja/trips/123");
    expect(response.cookies.get("travel_access")?.value).toBe("token");
  });
});
