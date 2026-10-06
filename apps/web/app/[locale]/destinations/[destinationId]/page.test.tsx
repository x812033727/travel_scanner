import { render, screen } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { beforeEach, describe, expect, it, vi } from "vitest";
import DestinationGuidePage from "./page";
import { locales } from "@/i18n/routing";
import { destinationDecisions } from "@/lib/destination-decisions";
import { destinationsCopy } from "@/lib/destinations-copy";
import { guideHref, type GuideSummary } from "@/lib/guides";
import { openSiteVisibility } from "@/lib/site-features";

const mocks = vi.hoisted(() => ({
  catalog: vi.fn(), places: vi.fn(), merchants: vi.fn(), visibility: vi.fn(), guides: vi.fn(),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: () => <div data-testid="affiliate" />,
}));
vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: mocks.visibility }));
vi.mock("@/lib/guides.server", () => ({ getGuideList: mocks.guides }));
vi.mock("@/lib/destinations.server", () => ({
  getDestinations: mocks.catalog, getDestination: vi.fn(),
  getGuidePlaces: mocks.places, getGuideMerchants: mocks.merchants,
}));

const tokyo = {
  id: "tokyo", city: "Tokyo", country: "Japan", countryCode: "JP", role: "primary",
  localName: null, englishName: null, parentDestinationId: null, extensionIds: [],
  areas: [], recommendedDays: null, timezone: "Asia/Tokyo", currency: "JPY", center: null, reason: "Visit Tokyo",
};
const params = Promise.resolve({ locale: "en" as const, destinationId: "tokyo" });
const article: GuideSummary = {
  slug: "published-tokyo-guide", kind: "howto", destination_id: "tokyo", destination_label: "Tokyo",
  topics: [], title: "Published Tokyo transport guide", description: "A published transport overview.",
  published_at: "2026-10-03T00:00:00Z", valid_until: null, featured: false,
};

beforeEach(() => {
  vi.clearAllMocks();
  mocks.catalog.mockResolvedValue([tokyo]);
  mocks.places.mockResolvedValue([{ id: "p1", name: "Reviewed shrine", detail: null }]);
  mocks.merchants.mockResolvedValue([{ id: "m1", name: "Reviewed cafe", detail: null }]);
  mocks.visibility.mockResolvedValue({ status: "ready", features: openSiteVisibility });
  mocks.guides.mockResolvedValue({ articles: [article], next_cursor: null, available: true });
});

describe("destination guide publication boundaries", () => {
  it("renders current reviewed places when the feature is enabled", async () => {
    render(await DestinationGuidePage({ params }));
    expect(mocks.places).toHaveBeenCalledWith("en", "tokyo");
    expect(screen.getByText("Reviewed shrine")).toBeTruthy();
  });

  it.each(["closed", "unavailable"])("does not fetch or render hotspots when visibility is %s", async (state) => {
    mocks.visibility.mockResolvedValue({
      status: state === "unavailable" ? "unavailable" : "ready",
      features: { ...openSiteVisibility, hotspots_enabled: state === "unavailable" },
    });
    render(await DestinationGuidePage({ params }));
    expect(mocks.places).not.toHaveBeenCalled();
    expect(screen.queryByText("Reviewed shrine")).toBeNull();
    expect(screen.queryByRole("link", { name: "Browse every reviewed place" })).toBeNull();
    expect(screen.getByText("Reviewed cafe")).toBeTruthy();
  });

  it("keeps a catalog outage distinct from a missing destination without fetching lists", async () => {
    mocks.catalog.mockResolvedValue(null);
    await expect(DestinationGuidePage({ params })).rejects.toThrow("Destination catalog unavailable");
    expect(mocks.places).not.toHaveBeenCalled();
    expect(mocks.merchants).not.toHaveBeenCalled();
    expect(mocks.guides).not.toHaveBeenCalled();
  });

  it.each(locales)("requests published travel articles filtered to the city in %s", async (locale) => {
    render(await DestinationGuidePage({ params: Promise.resolve({ locale, destinationId: "tokyo" }) }));
    expect(mocks.guides).toHaveBeenCalledExactlyOnceWith(locale, { section: "travel", destination: "tokyo" }, 3);
    expect(screen.getByRole("link", { name: article.title }).getAttribute("href"))
      .toBe(guideHref(article.kind, article.slug));
    expect(screen.getByText(article.description)).toBeTruthy();
  });

  it("filters another destination's article request while retaining its catalog areas", async () => {
    const other = { ...tokyo, id: "busan", city: "Busan", areas: ["Haeundae", "Seomyeon"] };
    mocks.catalog.mockResolvedValue([tokyo, other]);
    mocks.guides.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    render(await DestinationGuidePage({ params: Promise.resolve({ locale: "en", destinationId: "busan" }) }));
    expect(mocks.guides).toHaveBeenCalledExactlyOnceWith("en", { section: "travel", destination: "busan" }, 3);
    expect(screen.getByText(other.areas[0])).toBeTruthy();
    expect(screen.getByText(other.areas[1])).toBeTruthy();
    expect(screen.queryByRole("region", { name: destinationDecisions("en", "tokyo")!.title })).toBeNull();
    expect(screen.getByRole("link", { name: destinationsCopy("en").guidesHowto }).getAttribute("href"))
      .toBe("/guides/howto?destination=busan");
  });

  it("renders Seoul's sourced stay decisions before partner options in server HTML", async () => {
    const seoul = { ...tokyo, id: "seoul", city: "Seoul", areas: ["Myeongdong", "Hongdae", "Dongdaemun", "Gangnam"] };
    mocks.catalog.mockResolvedValue([tokyo, seoul]);
    mocks.guides.mockResolvedValue({ articles: [], next_cursor: null, available: true });
    const html = renderToStaticMarkup(await DestinationGuidePage({ params: Promise.resolve({ locale: "en", destinationId: "seoul" }) }));
    const decisions = destinationDecisions("en", "seoul")!;
    const partnerAt = html.indexOf('data-testid="affiliate"');
    expect(partnerAt).toBeGreaterThan(-1);
    expect(html).toContain(decisions.title);
    expect(html).not.toContain(destinationDecisions("en", "tokyo")!.title);
    for (const row of decisions.areas) {
      expect(html.indexOf(row.tradeoff.replaceAll("&", "&amp;"))).toBeGreaterThan(-1);
      expect(html.indexOf(row.sources[0].url)).toBeGreaterThan(-1);
      expect(html.indexOf(row.sources[0].url)).toBeLessThan(partnerAt);
    }
  });

  it.each([true, false])("renders an honest article state when available=%s and the list is empty", async (available) => {
    mocks.guides.mockResolvedValue({ articles: [], next_cursor: null, available });
    render(await DestinationGuidePage({ params }));
    const copy = destinationsCopy("en");
    expect(screen.getByText(available ? copy.emptyGuides : copy.unavailableGuides)).toBeTruthy();
    expect(screen.queryByText(available ? copy.unavailableGuides : copy.emptyGuides)).toBeNull();
    expect(screen.queryByRole("link", { name: article.title })).toBeNull();
    expect(screen.getByRole("link", { name: copy.guidesIntel })).toBeTruthy();
    expect(screen.getByRole("region", { name: destinationDecisions("en", "tokyo")!.title })).toBeTruthy();
  });

  it("awaits three published articles and renders evidence before partner options in server HTML", async () => {
    const articles = [article, { ...article, slug: "second-guide", title: "Second published article" },
      { ...article, slug: "third-guide", title: "Third published article" }];
    mocks.guides.mockResolvedValue({ articles, next_cursor: "more", available: true });
    const html = renderToStaticMarkup(await DestinationGuidePage({ params }));
    const partnerAt = html.indexOf('data-testid="affiliate"');
    expect(partnerAt).toBeGreaterThan(-1);
    for (const row of articles) {
      expect(html.indexOf(row.title)).toBeGreaterThan(-1);
      expect(html.indexOf(row.title)).toBeLessThan(partnerAt);
      expect(html).toContain(guideHref(row.kind, row.slug));
    }
    for (const row of destinationDecisions("en", "tokyo")!.areas) {
      expect(html.indexOf(row.sources[0].url)).toBeGreaterThan(-1);
      expect(html.indexOf(row.sources[0].url)).toBeLessThan(partnerAt);
    }
  });
});
