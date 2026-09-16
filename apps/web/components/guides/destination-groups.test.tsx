import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { DestinationGroups, groupByCountry } from "./destination-groups";

const labels = { heading: "依目的地瀏覽", lead: "先選國家，再選城市。", countryAll: "{country}全部" };
const facets = [
  { id: "tokyo", label: "東京", country: "japan", country_label: "日本", count: 11 },
  { id: "osaka-kyoto", label: "大阪／京都", country: "japan", country_label: "日本", count: 9 },
  { id: "seoul", label: "首爾", country: "south-korea", country_label: "韓國", count: 9 },
  { id: "jeju", label: "濟州", country: "south-korea", country_label: "韓國", count: 0 },
];

describe("browsing the travel hub by destination", () => {
  it("groups cities under their country in catalog order and sums the counts", () => {
    expect(groupByCountry(facets).map((group) => [group.country, group.count, group.cities.map((c) => c.id)])).toEqual([
      ["japan", 20, ["tokyo", "osaka-kyoto"]],
      ["south-korea", 9, ["seoul"]],
    ]);
  });

  it("links the country to the country filter and each city to the destination filter", () => {
    render(<DestinationGroups destinations={facets} labels={labels} />);
    expect(screen.getByRole("heading", { level: 2 }).textContent).toBe("依目的地瀏覽");
    expect(screen.getByRole("link", { name: /日本全部/ }).getAttribute("href")).toBe("/guides/howto?country=japan");
    const tokyo = screen.getByRole("link", { name: /東京/ });
    expect(tokyo.getAttribute("href")).toBe("/guides/howto?destination=tokyo");
    // The facet count decides which pills draw (below); the pill never prints it.
    expect(tokyo.textContent).toBe("東京");
    // A city with nothing published here leads to an empty list, so it gets no pill.
    expect(screen.queryByRole("link", { name: /濟州/ })).toBeNull();
  });

  it("draws nothing when no destination has an article in this language", () => {
    const { container } = render(<DestinationGroups destinations={[]} labels={labels} />);
    expect(container.innerHTML).toBe("");
  });
});
