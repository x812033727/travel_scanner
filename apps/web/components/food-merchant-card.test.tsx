import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { FoodMerchant } from "@/lib/foods";
import { FoodMerchantCard } from "./food-merchant-card";
import { SavedItemsProvider } from "./saved-items-provider";

const merchant: FoodMerchant = {
  id: "merchant-1",
  slug: "seoul-hankook-jib",
  name: "Hankook Jib",
  local_name: "한국집",
  destination_id: "seoul",
  destination_name: "首爾",
  country_code: "KR",
  area: { id: "area-1", slug: "seoul-myeongdong", name: "明洞", local_name: "명동" },
  categories: [
    { slug: "home-style", name: "定食／家常菜", is_primary: true },
    { slug: "rice-dishes", name: "飯食／粥品", is_primary: false },
  ],
  signature_dishes: [
    {
      food_id: "food-1",
      slug: "kr-bibimbap",
      name: "韓式拌飯",
      local_name: "비빔밥",
      food_kind: "main",
      meal_types: ["lunch", "dinner"],
    },
  ],
  address: "Seoul, Jung-gu",
  latitude: 37.57,
  longitude: 126.99,
  coordinate_source: {
    type: "official_tourism",
    url: "https://english.visitseoul.net/restaurants",
    verified_at: "2026-09-01T00:00:00Z",
  },
  official_website_url: "https://hankookjib.example/",
  map_links: [
    {
      provider: "naver",
      label: "Naver Map",
      url: "https://map.naver.com/p/entry/place/123456",
      primary: true,
    },
  ],
  verified_at: "2026-09-01T00:00:00Z",
  sources: [
    {
      source_type: "michelin_licensed",
      source_scope: "merchant_listing",
      title: "Michelin Guide Seoul",
      url: "https://guide.michelin.example/hankook-jib",
      claims: ["display_name"],
      edition_year: 2026,
      distinction: "bib_gourmand",
      last_verified_at: "2026-09-01T00:00:00Z",
    },
  ],
};

function renderCard(item: FoodMerchant) {
  const onSelectCategory = vi.fn();
  const onSelectArea = vi.fn();
  vi.stubGlobal(
    "fetch",
    vi.fn(async () => new Response(JSON.stringify({ items: [] }))),
  );
  render(
    <SavedItemsProvider>
      <FoodMerchantCard
        merchant={item}
        onSelectCategory={onSelectCategory}
        onSelectArea={onSelectArea}
      />
    </SavedItemsProvider>,
  );
  return { onSelectCategory, onSelectArea };
}

describe("FoodMerchantCard", () => {
  it("shows the area, cuisines, signature dish, safe links and sources", async () => {
    const { onSelectCategory, onSelectArea } = renderCard(merchant);

    expect(await screen.findByRole("heading", { name: "Hankook Jib" })).toBeTruthy();
    expect(screen.getByText("한국집")).toBeTruthy();
    expect(screen.getByText("首爾")).toBeTruthy();
    expect(screen.getByText("必比登推介")).toBeTruthy();
    expect(screen.getByText("韓式拌飯")).toBeTruthy();
    expect(screen.getByText("Seoul, Jung-gu")).toBeTruthy();
    const naver = screen.getByRole("link", { name: "Naver Map: Hankook Jib" });
    expect(naver.getAttribute("href")).toBe("https://map.naver.com/p/entry/place/123456");
    expect(naver.getAttribute("target")).toBe("_blank");
    expect(naver.getAttribute("rel")).toContain("noopener");
    expect(screen.getByRole("link", { name: /官方網站/ }).getAttribute("href")).toBe(
      "https://hankookjib.example/",
    );
    fireEvent.click(screen.getByText("來源：1 筆官方佐證"));
    expect(screen.getByRole("link", { name: "Michelin Guide Seoul" })).toBeTruthy();
    expect(screen.getByText("米其林（授權）")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "只看飯食／粥品" }));
    expect(onSelectCategory).toHaveBeenCalledWith("rice-dishes");
    fireEvent.click(screen.getByRole("button", { name: "只看明洞" }));
    expect(onSelectArea).toHaveBeenCalledWith("seoul-myeongdong");
    const addToTrip = screen.getByRole("button", { name: "加入行程" });
    expect(addToTrip.hasAttribute("disabled")).toBe(false);
  });

  it("never renders unsafe map or website links", async () => {
    renderCard({
      ...merchant,
      map_links: [
        { provider: "google", label: "Google Maps", url: "javascript:alert(1)", primary: true },
      ],
      official_website_url: "data:text/html,hi",
      sources: [],
    });

    expect(await screen.findByRole("heading", { name: "Hankook Jib" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: /Google Maps/ })).toBeNull();
    expect(screen.queryByRole("link", { name: /官方網站/ })).toBeNull();
  });
});
