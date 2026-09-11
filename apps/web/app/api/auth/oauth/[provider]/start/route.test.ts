import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { siteUrl } from "@/lib/seo";
import { GET } from "./route";

describe("OAuth start redirects behind the reverse proxy", () => {
  // In production the request reaches Next at the container's bind address, so its own
  // origin is https://0.0.0.0:3000. A redirect built on it strands the browser.
  const publicOrigin = new URL(siteUrl).origin;
  const start = (query: string) => GET(
    new NextRequest(`https://0.0.0.0:3000/api/auth/oauth/google/start?${query}`),
    { params: Promise.resolve({ provider: "google" }) },
  );

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("falls back to the public login page when the API is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("connection refused")));
    const location = new URL((await start("locale=ja")).headers.get("location") ?? "");
    expect(location.origin).toBe(publicOrigin);
    expect(location.pathname).toBe("/ja/login");
    expect(location.searchParams.get("oauth_error")).toBe("oauth_provider_unavailable");
  });

  it("returns a refused link attempt to the public account page", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ code: "oauth_link_session_invalid" }), { status: 401 }),
    ));
    const location = new URL((await start("locale=ja&intent=link")).headers.get("location") ?? "");
    expect(location.origin).toBe(publicOrigin);
    expect(location.pathname).toBe("/ja/account");
    expect(location.searchParams.get("oauth_error")).toBe("oauth_link_session_invalid");
  });
});
