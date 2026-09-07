import { afterEach, describe, expect, it, vi } from "vitest";
import { NextRequest } from "next/server";
import { POST } from "./route";
import { preserveRequestId } from "./request-id";
import { forwardedAnalyticsSession, renewedSession, upstreamLocale } from "./proxy-context";

vi.mock("next/headers", () => ({ cookies: async () => new Map() }));
afterEach(() => vi.unstubAllGlobals());

describe("saved service clickout BFF", () => {
  it("routes unified hotel option forms by saved IDs with their controlled locale", async () => {
    const fetcher = vi.fn(async () => new Response(null, { status: 303, headers: { Location: "https://www.booking.com/hotel/jp/fixture.html" } }));
    vi.stubGlobal("fetch", fetcher);
    const id = "00000000-0000-4000-8000-000000000001";
    const path = ["travel-services", id, "booking-options", id, "clickout"];
    const response = await POST(new NextRequest(`https://mokaair.test/api/travel/${path.join("/")}?locale=ja&placement=trip`, { method: "POST", headers: { Origin: "https://mokaair.test" } }), { params: Promise.resolve({ path }) });
    expect(response.status).toBe(303);
    const [target, options] = (fetcher.mock.calls as unknown as [string, RequestInit][])[0];
    expect(target).not.toContain("locale=");
    expect(target).toContain("placement=trip");
    expect(new Headers(options.headers).get("X-Travel-Locale")).toBe("ja");
    expect(options.redirect).toBe("manual");
  });
  it("proxies saved ordinary hotel links with safe new-tab 303 and no affiliate rewriting", async () => {
    const fetcher = vi.fn(async () => new Response(null, { status: 303, headers: { Location: "https://hotel.example.com/stay" } }));
    vi.stubGlobal("fetch", fetcher);
    const id = "00000000-0000-4000-8000-000000000001";
    const response = await POST(new NextRequest(`https://mokaair.test/api/travel/travel-services/${id}/hotel-links/official/clickout?locale=ko`, { method: "POST", headers: { Origin: "https://mokaair.test" } }), { params: Promise.resolve({ path: ["travel-services", id, "hotel-links", "official", "clickout"] }) });
    expect(response.status).toBe(303);
    expect(response.headers.get("location")).toBe("https://hotel.example.com/stay");
    expect(response.headers.get("cache-control")).toBe("no-store");
    const [target, options] = (fetcher.mock.calls as unknown as [string, RequestInit][])[0];
    expect(target).not.toContain("locale=");
    expect(new Headers(options.headers).get("X-Travel-Locale")).toBe("ko");
    expect(options.redirect).toBe("manual");
  });
  it("uses a controlled form locale, keeps 303 and strips the locale query upstream", async () => {
    const fetcher = vi.fn(async () => new Response(null, { status: 303, headers: { Location: "https://tp.st/fixture" } }));
    vi.stubGlobal("fetch", fetcher);
    const id = "00000000-0000-4000-8000-000000000001";
    const request = new NextRequest(`https://mokaair.test/api/travel/affiliates/offers/${id}/clickout?locale=ja&placement=trip`, { method: "POST", headers: { Origin: "https://mokaair.test" } });
    const response = await POST(request, { params: Promise.resolve({ path: ["affiliates", "offers", id, "clickout"] }) });
    expect(response.status).toBe(303);
    expect(response.headers.get("location")).toBe("https://tp.st/fixture");
    expect(response.headers.get("referrer-policy")).toBe("no-referrer");
    const [target, options] = (fetcher.mock.calls as unknown as [string, RequestInit][])[0];
    expect(target).toContain("placement=trip");
    expect(target).not.toContain("locale=");
    expect((options.headers as Headers).get("X-Travel-Locale")).toBe("ja");
    expect(options.redirect).toBe("manual");
  });

  it("rejects a cross-site POST before contacting the API", async () => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    const request = new NextRequest("https://mokaair.test/api/travel/affiliates/offers/fixture/clickout", { method: "POST", headers: { Origin: "https://evil.example" } });
    expect((await POST(request, { params: Promise.resolve({ path: ["affiliates", "offers", "fixture", "clickout"] }) })).status).toBe(403);
    expect(fetcher).not.toHaveBeenCalled();
  });
});

describe("travel BFF request tracing", () => {
  it("preserves the API request ID on the browser response", () => {
    const upstream = new Response("{}", {
      headers: { "X-Request-ID": "route-preview-7f98" },
    });
    const response = preserveRequestId(new Response("{}"), upstream);

    expect(response.headers.get("x-request-id")).toBe("route-preview-7f98");
  });
});

describe("travel BFF session renewal", () => {
  function upstreamWith(...cookies: string[]) {
    const headers = new Headers();
    for (const cookie of cookies) headers.append("Set-Cookie", cookie);
    return new Response("{}", { headers });
  }

  it("carries a slid-forward session and its lifetime back to the browser", () => {
    const upstream = upstreamWith(
      "travel_access=renewed.jwt.value; HttpOnly; Path=/; SameSite=Lax; Max-Age=3600",
    );

    expect(renewedSession(upstream)).toEqual({ token: "renewed.jwt.value", maxAge: 3600 });
  });

  it("falls back to an hour when the API states no lifetime", () => {
    expect(renewedSession(upstreamWith("travel_access=renewed; Path=/"))?.maxAge).toBe(3600);
  });

  it("caps an implausibly long lifetime rather than trusting it", () => {
    const upstream = upstreamWith("travel_access=renewed; Max-Age=99999999");

    expect(renewedSession(upstream)?.maxAge).toBe(60 * 60 * 24);
  });

  it("ignores other cookies the API happens to set", () => {
    const upstream = upstreamWith("travel_locale=ja; Path=/", "other=1; Path=/");

    expect(renewedSession(upstream)).toBeNull();
  });

  it("reports nothing when the session was not renewed", () => {
    expect(renewedSession(new Response("{}"))).toBeNull();
  });
});

describe("travel BFF upstream locale", () => {
  it("answers in the locale of the page the browser is showing", () => {
    expect(upstreamLocale("en", "zh-TW")).toBe("en");
    expect(upstreamLocale("ja", undefined)).toBe("ja");
  });

  it("falls back to the preference remembered at sign-in, then to the catalog language", () => {
    expect(upstreamLocale(null, "ko")).toBe("ko");
    expect(upstreamLocale(undefined, undefined)).toBe("zh-TW");
  });

  it("ignores values that are not site locales", () => {
    expect(upstreamLocale("fr", "ja")).toBe("ja");
    expect(upstreamLocale("../etc", "zh-CN; drop")).toBe("zh-TW");
  });
});

describe("travel BFF analytics session", () => {
  it("forwards an id so a server event counts as the session that caused it", () => {
    const id = "3f2504e0-4f89-41d3-9a0c-0305e82c3301";
    expect(forwardedAnalyticsSession(id)).toBe(id);
    expect(forwardedAnalyticsSession(id.toUpperCase())).toBe(id.toUpperCase());
  });

  it("drops anything a caller could have chosen for itself", () => {
    // The value becomes an HMAC input server-side. A caller that can pick it can file
    // its own rows under someone else's hash, so only a real id gets through.
    for (const value of ["", "anonymous", "../etc/passwd", "3f2504e0", "x".repeat(400)]) {
      expect(forwardedAnalyticsSession(value)).toBeNull();
    }
    expect(forwardedAnalyticsSession(null)).toBeNull();
  });
});
