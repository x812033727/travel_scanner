import { render, screen, within } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { DestinationGuide } from "@/components/destination-guide";
import { locales } from "@/i18n/routing";
import { destinationDecisions } from "@/lib/destination-decisions";
import { guideHref, type GuideSummary } from "@/lib/guides";

vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: { destinationId: string; placement?: string; modules?: string[] }) => (
    <div data-testid="affiliate" data-destination={props.destinationId} data-placement={props.placement} data-modules={(props.modules ?? []).join(",")} />
  ),
}));
import { destinationsCopy } from "@/lib/destinations-copy";
import type { DestinationSummary } from "@/lib/destinations.server";

const tokyo: DestinationSummary = {
  id: "tokyo", city: "東京", localName: "東京", englishName: "Tokyo",
  country: "日本", countryCode: "JP", role: "primary", parentDestinationId: null,
  extensionIds: ["yokohama"], areas: ["新宿", "澀谷"],
  recommendedDays: { min: 4, max: 6 }, timezone: "Asia/Tokyo", currency: "JPY",
  center: { latitude: 35.68, longitude: 139.76 }, reason: "第一次去日本最順的城市。",
};
const yokohama: DestinationSummary = { ...tokyo, id: "yokohama", city: "橫濱", localName: "横浜", extensionIds: [], role: "extension", parentDestinationId: "tokyo" };
const copy = destinationsCopy("zh-TW");
const emptyGuides = { articles: [], next_cursor: null, available: true };
const article: GuideSummary = {
  slug: "published-tokyo-guide", kind: "howto", destination_id: "tokyo", destination_label: "Tokyo",
  topics: [], title: "Published Tokyo transport guide", description: "A published transport overview.",
  published_at: "2026-10-03T00:00:00Z", valid_until: null, featured: false,
};

function draw(overrides: Partial<Parameters<typeof DestinationGuide>[0]> = {}) {
  return render(
    <DestinationGuide
      locale="zh-TW"
      destination={tokyo}
      hotspotsEnabled
      places={[{ id: "p1", name: "淺草寺", detail: "上野／淺草" }]}
      merchants={[{ id: "m1", name: "一蘭", detail: "新宿" }]}
      related={[yokohama]}
      guides={emptyGuides}
      {...overrides}
    />,
  );
}

describe("DestinationGuide", () => {
  it("puts the city name in the only h1", () => {
    draw();
    const headings = screen.getAllByRole("heading", { level: 1 });
    expect(headings).toHaveLength(1);
    expect(headings[0].textContent).toBe("東京");
  });

  it("renders the places and merchants as text, not a filter to be hydrated", () => {
    draw();
    expect(screen.getByText("淺草寺")).toBeTruthy();
    const places = screen.getByText(copy.seeTitle).parentElement as HTMLElement;
    expect(within(places).getByText("上野／淺草")).toBeTruthy();
    expect(screen.getByText("一蘭")).toBeTruthy();
  });

  it("shows the catalog facts and the Tokyo stay decisions", () => {
    const { container } = draw();
    expect(screen.getByText(`4–6 ${copy.daysUnit}`)).toBeTruthy();
    expect(screen.getByText("Asia/Tokyo")).toBeTruthy();
    expect(screen.getByText("JPY")).toBeTruthy();
    const decisions = destinationDecisions("zh-TW", "tokyo")!;
    const areas = within(container).getByText(decisions.title).parentElement as HTMLElement;
    expect(within(areas).getAllByRole("heading", { level: 3 }).map((heading) => heading.textContent))
      .toEqual(decisions.areas.map((area) => area.name));
  });

  it("says so plainly when a section has nothing reviewed yet", () => {
    draw({ places: [], merchants: [] });
    expect(screen.getByText(copy.emptyPlaces)).toBeTruthy();
    expect(screen.getByText(copy.emptyFood)).toBeTruthy();
  });

  it("mounts the partner entrances once, for this city, labelled as the city surface", () => {
    draw();
    const panels = screen.getAllByTestId("affiliate");
    expect(panels).toHaveLength(1);
    expect(panels[0].getAttribute("data-destination")).toBe("tokyo");
    expect(panels[0].getAttribute("data-placement")).toBe("city");
    // All modules: the city page is the reader's general entrance, not a topic page.
    expect(panels[0].getAttribute("data-modules")).toBe("");
  });

  it("links outward to the surfaces that hold the rest of the content", () => {
    draw();
    const hrefs = screen.getAllByRole("link").map((link) => link.getAttribute("href"));
    expect(hrefs).toContain("/hotspots?destination_id=tokyo");
    expect(hrefs).toContain("/foods?destination_id=tokyo");
    expect(hrefs).toContain("/search/new");
    expect(hrefs).toContain("/destinations/tokyo/services");
    expect(hrefs).toContain("/destinations");
  });

  it("links related destinations both ways", () => {
    const { container } = draw();
    const nearby = within(container).getByText(copy.nearbyTitle).parentElement;
    expect(within(nearby as HTMLElement).getByRole("link", { name: "橫濱" }).getAttribute("href")).toBe("/destinations/yokohama");
  });

  it("shows the original-script name only when it differs from the heading", () => {
    draw();
    expect(screen.getByText("日本")).toBeTruthy();
    const { container } = render(
      <DestinationGuide locale="en" destination={{ ...tokyo, city: "Tokyo", localName: "東京" }} hotspotsEnabled places={[]} merchants={[]} related={[]} guides={emptyGuides} />,
    );
    expect(container.textContent).toContain("東京");
  });

  it("hides the closed hotspot section including stale entries and its action", () => {
    draw({ hotspotsEnabled: false });
    expect(screen.queryByText("淺草寺")).toBeNull();
    expect(screen.queryByText(copy.seeTitle)).toBeNull();
    expect(screen.queryByRole("link", { name: copy.browsePlaces })).toBeNull();
    expect(screen.getByText("一蘭")).toBeTruthy();
  });

  it("links this city's intel and guides, filtered to it", () => {
    draw({});
    const intel = screen.getByRole("link", { name: copy.guidesIntel });
    const howto = screen.getByRole("link", { name: copy.guidesHowto });
    expect(intel.getAttribute("href")).toBe("/guides/intel?destination=tokyo");
    expect(howto.getAttribute("href")).toBe("/guides/howto?destination=tokyo");
    expect(screen.getByText(copy.guidesTitle)).toBeTruthy();
  });

  it("still offers the guides when both catalog listings are unavailable", () => {
    // They are separate systems: an article about the city is readable even when the
    // hotspot and merchant services are not.
    draw({ places: null, merchants: null, hotspotsEnabled: false });
    expect(screen.getByRole("link", { name: copy.guidesIntel })).toBeTruthy();
  });

  it("distinguishes failed listing services from genuinely empty review queues", () => {
    draw({ places: null, merchants: null });
    expect(screen.getByText(copy.unavailablePlaces)).toBeTruthy();
    expect(screen.getByText(copy.unavailableFood)).toBeTruthy();
    expect(screen.queryByText(copy.emptyPlaces)).toBeNull();
    expect(screen.queryByText(copy.emptyFood)).toBeNull();
  });

  it.each(locales)("renders four complete, sourced decision cards in %s", (locale) => {
    const decisions = destinationDecisions(locale, "tokyo")!;
    const { container } = draw({ locale });
    const section = screen.getByRole("region", { name: decisions.title });
    const cards = within(section).getAllByRole("heading", { level: 3 });
    expect(cards.map((heading) => heading.textContent)).toEqual(decisions.areas.map((area) => area.name));
    for (const area of decisions.areas) {
      const card = within(section).getByRole("heading", { name: area.name }).parentElement as HTMLElement;
      expect(within(card).getByText(area.suitable)).toBeTruthy();
      expect(within(card).getByText(area.tradeoff)).toBeTruthy();
      expect(within(card).getByText(area.check)).toBeTruthy();
      for (const source of area.sources) {
        expect(within(card).getByRole("link", { name: source.label }).getAttribute("href")).toBe(source.url);
      }
    }
    expect(container.querySelector("time")?.getAttribute("datetime")).toBe(decisions.checkedOn);
  });

  it("preserves the catalog area list for other destinations without Tokyo comparisons", () => {
    draw({ destination: yokohama });
    const areas = screen.getByText(copy.areasTitle).parentElement as HTMLElement;
    expect(within(areas).getAllByRole("listitem").map((item) => item.textContent)).toEqual(yokohama.areas);
    expect(destinationDecisions("zh-TW", "yokohama")).toBeNull();
    expect(screen.queryByRole("region", { name: destinationDecisions("zh-TW", "tokyo")!.title })).toBeNull();
    expect(screen.queryByRole("link", { name: /GO TOKYO/ })).toBeNull();
  });

  it("renders fetched published titles and descriptions with internal article links", () => {
    draw({ guides: { ...emptyGuides, articles: [article] } });
    expect(screen.getByRole("link", { name: article.title }).getAttribute("href"))
      .toBe(guideHref(article.kind, article.slug));
    expect(screen.getByText(article.description)).toBeTruthy();
    expect(screen.queryByText(copy.emptyGuides)).toBeNull();
    expect(screen.getByRole("link", { name: copy.guidesHowto }).getAttribute("href"))
      .toBe("/guides/howto?destination=tokyo");
  });

  it.each(locales)("distinguishes empty and unavailable articles in %s without a fallback article", (locale) => {
    const localized = destinationsCopy(locale);
    const { rerender } = draw({ locale });
    expect(screen.getByText(localized.emptyGuides)).toBeTruthy();
    rerender(<DestinationGuide locale={locale} destination={tokyo} hotspotsEnabled places={[]} merchants={[]} related={[]}
      guides={{ articles: [article], next_cursor: null, available: false }} />);
    expect(screen.getByText(localized.unavailableGuides)).toBeTruthy();
    expect(screen.queryByText(localized.emptyGuides)).toBeNull();
    expect(screen.queryByRole("link", { name: article.title })).toBeNull();
    expect(screen.getByRole("link", { name: localized.guidesIntel })).toBeTruthy();
  });

  it("includes decision evidence and article cards in server HTML before partner options", () => {
    const decisions = destinationDecisions("en", "tokyo")!;
    const html = renderToStaticMarkup(<DestinationGuide locale="en" destination={tokyo} hotspotsEnabled places={[]} merchants={[]}
      related={[]} guides={{ ...emptyGuides, articles: [article] }} />);
    const partnerAt = html.indexOf('data-testid="affiliate"');
    expect(partnerAt).toBeGreaterThan(-1);
    expect(html.indexOf(decisions.areas[0].suitable)).toBeGreaterThan(-1);
    expect(html.indexOf(decisions.areas[0].suitable)).toBeLessThan(partnerAt);
    expect(html.indexOf(decisions.areas[0].sources[0].url)).toBeLessThan(partnerAt);
    expect(html.indexOf(article.title)).toBeGreaterThan(-1);
    expect(html.indexOf(article.title)).toBeLessThan(partnerAt);
    expect(html.indexOf(article.description)).toBeLessThan(partnerAt);
  });
});
