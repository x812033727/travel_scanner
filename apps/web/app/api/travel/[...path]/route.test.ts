import { describe, expect, it } from "vitest";
import { preserveRequestId } from "./request-id";
import { renewedSession, upstreamLocale } from "./route";

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
