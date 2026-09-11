import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { DestinationGuide } from "@/components/destination-guide";
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

function draw(overrides: Partial<Parameters<typeof DestinationGuide>[0]> = {}) {
  return render(
    <DestinationGuide
      locale="zh-TW"
      destination={tokyo}
      hotspotsEnabled
      places={[{ id: "p1", name: "淺草寺", detail: "上野／淺草" }]}
      merchants={[{ id: "m1", name: "一蘭", detail: "新宿" }]}
      related={[yokohama]}
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
    expect(screen.getByText("上野／淺草")).toBeTruthy();
    expect(screen.getByText("一蘭")).toBeTruthy();
  });

  it("shows the catalog facts and the areas", () => {
    const { container } = draw();
    expect(screen.getByText(`4–6 ${copy.daysUnit}`)).toBeTruthy();
    expect(screen.getByText("Asia/Tokyo")).toBeTruthy();
    expect(screen.getByText("JPY")).toBeTruthy();
    // Scoped: 新宿 is both an area of Tokyo and the area label on the merchant below it.
    const areas = within(container).getByText(copy.areasTitle).parentElement as HTMLElement;
    expect(within(areas).getByText("新宿")).toBeTruthy();
    expect(within(areas).getByText("澀谷")).toBeTruthy();
  });

  it("says so plainly when a section has nothing reviewed yet", () => {
    draw({ places: [], merchants: [] });
    expect(screen.getByText(copy.emptyPlaces)).toBeTruthy();
    expect(screen.getByText(copy.emptyFood)).toBeTruthy();
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
      <DestinationGuide locale="en" destination={{ ...tokyo, city: "Tokyo", localName: "東京" }} hotspotsEnabled places={[]} merchants={[]} related={[]} />,
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

  it("distinguishes failed listing services from genuinely empty review queues", () => {
    draw({ places: null, merchants: null });
    expect(screen.getByText(copy.unavailablePlaces)).toBeTruthy();
    expect(screen.getByText(copy.unavailableFood)).toBeTruthy();
    expect(screen.queryByText(copy.emptyPlaces)).toBeNull();
    expect(screen.queryByText(copy.emptyFood)).toBeNull();
  });
});
