import { describe, expect, it } from "vitest";
import { locales } from "@/i18n/routing";
import { alternatesFor, languageAlternates, localeUrl, routePathFromRequest, siteUrl } from "@/lib/seo";

describe("routePathFromRequest", () => {
  it("strips the locale prefix", () => {
    expect(routePathFromRequest("/en/foods")).toBe("/foods");
    expect(routePathFromRequest("/zh-TW/flights/status")).toBe("/flights/status");
  });

  it("reduces a locale home page to the site root path", () => {
    expect(routePathFromRequest("/en")).toBe("/");
    expect(routePathFromRequest("/zh-CN/")).toBe("/");
  });

  it("drops the query and the fragment", () => {
    // Filtered views of one document, not separate documents: /hotspots?destination_id=tokyo
    // and /hotspots must not compete with each other in search results.
    expect(routePathFromRequest("/zh-TW/hotspots?destination_id=tokyo&area=shibuya")).toBe("/hotspots");
    expect(routePathFromRequest("/en/explore?content=video:abc#top")).toBe("/explore");
  });

  it("does not let a repeated slash into the canonical", () => {
    // Next 308-redirects repeated slashes before proxy.ts sets the header, so this is not
    // reachable over HTTP today -- but this is an exported builder, and `//foods` would have
    // gone into the canonical and all six hreflang links.
    expect(routePathFromRequest("/en//foods")).toBe("/foods");
    expect(routePathFromRequest("/en///a//b")).toBe("/a/b");
  });

  it("keeps nested dynamic segments", () => {
    expect(routePathFromRequest("/ja/destinations/tokyo/services")).toBe("/destinations/tokyo/services");
  });

  it("falls back to the root for anything it does not recognise", () => {
    // The header is set by proxy.ts for every matched request, so these are the cases where it
    // is missing entirely. Degrading to the locale home page is the previous behaviour.
    expect(routePathFromRequest(null)).toBe("/");
    expect(routePathFromRequest(undefined)).toBe("/");
    expect(routePathFromRequest("")).toBe("/");
    expect(routePathFromRequest("not-a-path")).toBe("/");
    expect(routePathFromRequest("/foods")).toBe("/");
  });
});

describe("localeUrl", () => {
  it("does not leave a trailing slash on a locale home page", () => {
    expect(localeUrl("en", "/")).toBe(`${siteUrl}/en`);
  });

  it("joins the locale and the path", () => {
    expect(localeUrl("zh-TW", "/foods")).toBe(`${siteUrl}/zh-TW/foods`);
  });
});

describe("languageAlternates", () => {
  it("lists every locale including the current one, plus x-default", () => {
    const languages = languageAlternates("/foods");
    expect(Object.keys(languages).sort()).toEqual([...locales, "x-default"].sort());
    for (const locale of locales) expect(languages[locale]).toBe(`${siteUrl}/${locale}/foods`);
  });

  it("points x-default at the English version", () => {
    expect(languageAlternates("/pricing")["x-default"]).toBe(`${siteUrl}/en/pricing`);
  });
});

describe("alternatesFor", () => {
  it("canonicalizes a page to itself, not to the locale home page", () => {
    // The defect this module exists for: every page used to declare ${siteUrl}/${locale}.
    const alternates = alternatesFor("en", "/hotspots");
    expect(alternates?.canonical).toBe(`${siteUrl}/en/hotspots`);
    expect(alternates?.canonical).not.toBe(`${siteUrl}/en`);
  });

  it("still canonicalizes a locale home page to the locale home page", () => {
    expect(alternatesFor("ko", "/")?.canonical).toBe(`${siteUrl}/ko`);
  });
});
