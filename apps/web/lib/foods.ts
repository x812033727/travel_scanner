export type MapLink = { provider: string; label: string; url: string; primary: boolean };

export type FoodCity = {
  id: string;
  name: string;
  local_name: string | null;
  english_name: string | null;
  country_code: string;
  role: string;
  parent_destination_id: string | null;
  merchant_count: number;
  area_count: number;
};
export type FoodCountry = { code: string; name: string; merchant_count: number; cities: FoodCity[] };
export type FoodCitiesResponse = { total_merchants: number; countries: FoodCountry[] };

export type FoodAreaRef = { id: string; slug: string; name: string; local_name: string | null };
export type FoodCategoryRef = { slug: string; name: string; is_primary: boolean };
export type FacetArea = FoodAreaRef & { merchant_count: number };
export type FacetCategory = { slug: string; name: string; merchant_count: number };
export type SignatureDish = {
  food_id: string;
  slug: string;
  name: string;
  local_name: string;
  food_kind: string;
  meal_types: string[];
};
export type MerchantSource = {
  source_type: string;
  source_scope: string;
  title: string;
  url: string;
  claims: string[];
  edition_year: number | null;
  distinction: string | null;
  last_verified_at: string | null;
};
export type FoodMerchant = {
  id: string;
  slug: string;
  name: string;
  local_name: string;
  destination_id: string;
  destination_name: string;
  country_code: string;
  area: FoodAreaRef | null;
  categories: FoodCategoryRef[];
  signature_dishes: SignatureDish[];
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  coordinate_source: { type: string | null; url: string | null; verified_at: string | null };
  official_website_url: string | null;
  map_links: MapLink[];
  verified_at: string | null;
  sources: MerchantSource[];
};
export type MerchantFacets = {
  areas: FacetArea[];
  unassigned_area_count: number;
  categories: FacetCategory[];
};
export type FoodMerchantsResponse = {
  total: number;
  has_more: boolean;
  next_cursor: string | null;
  items: FoodMerchant[];
  facets: MerchantFacets;
};
export type FoodCategoriesResponse = { items: FacetCategory[] };

export type FoodDestination = {
  id: string;
  name: string;
  local_name: string | null;
  english_name: string | null;
  country_code: string;
  role: "primary" | "secondary" | "extension";
  parent_destination_id: string | null;
};
export type FoodHotspot = {
  hotspot_id: string;
  slug: string;
  name: string;
  local_name: string | null;
  destination_id: string;
  latitude: number;
  longitude: number;
  map_links: MapLink[];
};
export type RecommendedMerchant = {
  merchant_id: string;
  slug: string;
  name: string;
  local_name: string;
  destination_id: string;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  map_links: MapLink[];
  verified_at: string | null;
  area?: FoodAreaRef | null;
  categories?: FoodCategoryRef[];
};
export type FoodItem = {
  id: string;
  slug: string;
  country_code: string;
  country_name: string;
  name: string;
  local_name: string;
  romanized_name: string;
  summary: string;
  food_kind: "main" | "noodle_soup" | "street_food" | "dessert" | "drink";
  meal_types: string[];
  ingredient_tags: string[];
  dietary_notes: string[];
  source_urls: string[];
  destinations: FoodDestination[];
  food_hotspots: FoodHotspot[];
  recommended_merchants: RecommendedMerchant[];
};
export type FoodsResponse = {
  total: number;
  has_more: boolean;
  next_cursor: string | null;
  items: FoodItem[];
};

export type FoodBrowserFilters = {
  destinationId: string;
  area: string;
  category: string;
  query: string;
};

export const OTHER_AREA = "other";

export const emptyFoodBrowserFilters: FoodBrowserFilters = {
  destinationId: "",
  area: "",
  category: "",
  query: "",
};

export function readFoodBrowserFilters(search: string): FoodBrowserFilters {
  const params = new URLSearchParams(search);
  return {
    destinationId: (params.get("destination_id") ?? "").trim(),
    area: (params.get("area") ?? "").trim(),
    category: (params.get("category") ?? "").trim(),
    query: (params.get("q") ?? "").trim(),
  };
}

export function foodBrowserSearch(filters: FoodBrowserFilters): string {
  const params = new URLSearchParams();
  if (filters.destinationId) params.set("destination_id", filters.destinationId);
  if (filters.area) params.set("area", filters.area);
  if (filters.category) params.set("category", filters.category);
  if (filters.query) params.set("q", filters.query);
  return params.toString();
}

export function merchantsQuery(
  filters: FoodBrowserFilters,
  cursor?: string | null,
  limit = 20,
): string {
  const params = new URLSearchParams(foodBrowserSearch(filters));
  params.set("limit", String(limit));
  if (cursor) params.set("cursor", cursor);
  return params.toString();
}

export function activeFilterCount(filters: FoodBrowserFilters): number {
  return [filters.destinationId, filters.area, filters.category, filters.query].filter(Boolean)
    .length;
}

export function primaryMapLink(links: MapLink[]): MapLink | undefined {
  return links.find((link) => link.primary) ?? links[0];
}

export function sortCitiesByMerchants(cities: FoodCity[]): FoodCity[] {
  return [...cities].sort((left, right) => {
    if ((left.merchant_count > 0) !== (right.merchant_count > 0)) {
      return left.merchant_count > 0 ? -1 : 1;
    }
    return right.merchant_count - left.merchant_count;
  });
}

export function findCity(countries: FoodCountry[], destinationId: string): FoodCity | undefined {
  for (const country of countries) {
    const city = country.cities.find((item) => item.id === destinationId);
    if (city) return city;
  }
  return undefined;
}
