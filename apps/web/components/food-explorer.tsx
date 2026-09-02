"use client";

import { ExternalLink, MapPin, Search, SlidersHorizontal, Soup, Sparkles, UtensilsCrossed, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { FormEvent, useEffect, useState } from "react";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { TravelCardActions } from "@/components/travel-card-actions";

type MapLink = { provider: "google" | "naver"; label: string; url: string; primary: boolean };
type FoodDestination = {
  id: string;
  name: string;
  local_name: string | null;
  english_name: string | null;
  country_code: string;
  role: "primary" | "secondary" | "extension";
  parent_destination_id: string | null;
};
type FoodHotspot = {
  hotspot_id: string;
  slug: string;
  name: string;
  local_name: string | null;
  destination_id: string;
  latitude: number;
  longitude: number;
  map_links: MapLink[];
};
type FoodMerchant = {
  merchant_id: string;
  slug: string;
  name: string;
  local_name: string;
  destination_id: string;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  coordinate_source: { type: string; url: string; verified_at: string | null };
  map_links: MapLink[];
  verified_at: string | null;
  sources: { source_type: string; title: string; url: string; edition_year: number | null; distinction: string | null; last_verified_at: string }[];
};
type FoodItem = {
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
  recommended_merchants: FoodMerchant[];
};
type FoodsResponse = {
  total: number;
  has_more: boolean;
  next_cursor: string | null;
  items: FoodItem[];
};
type FacetsResponse = {
  total: number;
  countries: { code: string; name: string; count: number }[];
  destinations: (FoodDestination & { count: number })[];
  food_kinds: { code: string; count: number }[];
  meal_types: { code: string; count: number }[];
};

const kinds = ["", "main", "noodle_soup", "street_food", "dessert", "drink"] as const;
const meals = ["", "breakfast", "lunch", "dinner", "snack", "dessert", "drink"] as const;

export function FoodExplorer() {
  const t = useTranslations("foods");
  const [query, setQuery] = useState("");
  const [country, setCountry] = useState("");
  const [destination, setDestination] = useState("");
  const [kind, setKind] = useState("");
  const [meal, setMeal] = useState("");
  const [facets, setFacets] = useState<FacetsResponse | null>(null);
  const [foods, setFoods] = useState<FoodsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filtersOpen, setFiltersOpen] = useState(false);

  async function load(
    append = false,
    overrides: { country?: string; destination?: string } = {},
  ) {
    setLoading(true);
    setError("");
    const selectedCountry = overrides.country ?? country;
    const selectedDestination = overrides.destination ?? destination;
    const params = new URLSearchParams({ limit: "20" });
    if (query.trim()) params.set("q", query.trim());
    if (selectedCountry) params.set("country_code", selectedCountry);
    if (selectedDestination) params.set("destination_id", selectedDestination);
    if (kind) params.set("food_kind", kind);
    if (meal) params.set("meal_type", meal);
    if (append && foods?.next_cursor) params.set("cursor", foods.next_cursor);
    try {
      const result = await api<FoodsResponse>(`/foods?${params}`);
      setFoods(append && foods ? { ...result, items: [...foods.items, ...result.items] } : result);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    Promise.all([api<FacetsResponse>("/foods/facets"), api<FoodsResponse>("/foods?limit=20")])
      .then(([facetResult, foodResult]) => {
        setFacets(facetResult);
        setFoods(foodResult);
      })
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setLoading(false));
  }, []);

  const visibleDestinations = facets?.destinations.filter(
    (item) => !country || item.country_code === country,
  ) ?? [];
  return <main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
    <section className="pb-7 pt-5 md:pb-9 md:pt-9">
      <p className="flex items-center gap-2 text-sm font-semibold text-[var(--coral)]"><Sparkles size={16} />{t("eyebrow")}</p>
      <h1 className="mt-3 text-3xl font-bold tracking-[-.035em] md:text-5xl">{t("title")}</h1>
      <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p>
      <div className="mt-5 flex flex-wrap gap-2" role="list" aria-label={t("countryTabs")}>
        <button type="button" onClick={() => { setCountry(""); setDestination(""); void load(false, { country: "", destination: "" }); }} className={`min-h-11 rounded-full px-4 text-sm font-semibold ${country === "" ? "bg-[var(--ink)] text-white" : "border border-[var(--line)] bg-white"}`}>{t("allCountries")} · {facets?.total ?? 0}</button>
        {facets?.countries.map((item) => <button key={item.code} type="button" onClick={() => { setCountry(item.code); setDestination(""); void load(false, { country: item.code, destination: "" }); }} className={`min-h-11 rounded-full px-4 text-sm font-semibold ${country === item.code ? "bg-[var(--ink)] text-white" : "border border-[var(--line)] bg-white"}`}>{item.name} · {item.count}</button>)}
      </div>
    </section>

    <button type="button" onClick={() => setFiltersOpen(true)} className="mb-3 flex min-h-12 w-full items-center justify-between rounded-2xl border border-[var(--line)] bg-white px-4 font-semibold shadow-[var(--shadow-sm)] md:hidden"><span className="flex items-center gap-2"><SlidersHorizontal size={18} />{t("filters")}</span><span className="rounded-full bg-[var(--coral-soft)] px-2.5 py-1 text-xs">{[destination, kind, meal].filter(Boolean).length}</span></button>
    {filtersOpen && <button type="button" aria-label={t("filters")} onClick={() => setFiltersOpen(false)} className="fixed inset-0 z-[70] bg-slate-950/40 md:hidden" />}
    <form onSubmit={(event: FormEvent<HTMLFormElement>) => { event.preventDefault(); setFiltersOpen(false); void load(); }} className={`${filtersOpen ? "mobile-filter-sheet-open" : ""} mobile-filter-sheet grid gap-3 rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-[var(--shadow-lg)] md:grid-cols-[1.35fr_repeat(3,1fr)_auto] md:p-5`} aria-label={t("filters")}>
      <div className="mb-1 flex items-center justify-between md:hidden"><strong>{t("filters")}</strong><button type="button" onClick={() => setFiltersOpen(false)} aria-label={t("filters")} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]"><X size={19} /></button></div>
      <label className="relative"><span className="sr-only">{t("searchPlaceholder")}</span><Search className="pointer-events-none absolute left-4 top-3.5 text-[var(--muted)]" size={19} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t("searchPlaceholder")} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-11 pr-4 outline-none focus:border-[var(--teal)]" /></label>
      <select value={destination} onChange={(event) => setDestination(event.target.value)} aria-label={t("allDestinations")} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3"><option value="">{t("allDestinations")}</option>{visibleDestinations.map((item) => <option key={item.id} value={item.id}>{item.name} ({item.count})</option>)}</select>
      <select value={kind} onChange={(event) => setKind(event.target.value)} aria-label={t("allKinds")} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3">{kinds.map((item) => <option key={item} value={item}>{item ? t(`kinds.${item}`) : t("allKinds")}</option>)}</select>
      <select value={meal} onChange={(event) => setMeal(event.target.value)} aria-label={t("allMeals")} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3">{meals.map((item) => <option key={item} value={item}>{item ? t(`meals.${item}`) : t("allMeals")}</option>)}</select>
      <button type="submit" className="h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white">{t("submit")}</button>
    </form>

    <section className="mt-7" aria-live="polite" aria-busy={loading}>
      <div className="mb-4 flex items-center justify-between gap-4"><h2 className="flex items-center gap-2 text-xl font-bold"><UtensilsCrossed size={20} className="text-[var(--coral)]" />{t("catalog")}</h2><p className="text-sm text-[var(--muted)]">{t("loaded", { shown: foods?.items.length ?? 0, total: foods?.total ?? 0 })}</p></div>
      {loading && <div className="rounded-3xl border border-[var(--line)] bg-white p-8 text-[var(--muted)]">{t("loading")}</div>}
      {!loading && error && <div role="alert" className="rounded-3xl bg-[var(--coral-soft)] p-6">{error}</div>}
      {!loading && !error && foods?.items.length === 0 && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white p-8 text-center"><Soup className="mx-auto text-[var(--teal)]" /><h3 className="mt-3 font-bold">{t("emptyTitle")}</h3><p className="mt-2 text-sm text-[var(--muted)]">{t("emptyBody")}</p></div>}
      {!loading && !error && foods && <div className="grid gap-5 md:grid-cols-2">{foods.items.map((food) => <article key={food.id} className={`travel-result-card travel-result-card-food flex flex-col rounded-3xl border border-[var(--line)] bg-white p-5`}>
        <div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[.14em] text-[var(--coral)]">{food.country_name}</p><h3 className="mt-1 text-2xl font-bold">{food.name}</h3><p className="mt-1 text-sm text-[var(--muted)]">{food.local_name}{food.romanized_name !== food.name && ` · ${food.romanized_name}`}</p></div><span className="rounded-full bg-[var(--teal-soft)] px-3 py-1 text-xs font-semibold text-[var(--teal-dark)]">{t(`kinds.${food.food_kind}`)}</span></div>
        <p className="mt-4 leading-7 text-[var(--muted)]">{food.summary}</p>
        <div className="mt-4 flex flex-wrap gap-2">{food.meal_types.map((item) => <span key={item} className="rounded-full border border-[var(--line)] px-2.5 py-1 text-xs">{t(`meals.${item}`)}</span>)}{food.dietary_notes.map((item) => <span key={item} className="rounded-full bg-amber-50 px-2.5 py-1 text-xs text-amber-950">{item}</span>)}</div>
        <div className="mt-5 border-t border-[var(--line)] pt-4"><p className="text-xs font-semibold text-[var(--muted)]">{t("cities")}</p><p className="mt-1 text-sm font-semibold">{food.destinations.map((item) => item.name).join("、")}</p></div>
        <div className="mt-4"><p className="text-xs font-semibold text-[var(--muted)]">{t("recommendedMerchants")}</p><div className="mt-2 grid gap-2">{food.recommended_merchants.slice(0, 3).map((merchant) => { const map = merchant.map_links.find((link) => link.primary) ?? merchant.map_links[0]; return map ? <a key={merchant.merchant_id} href={map.url} target="_blank" rel="noopener noreferrer" aria-label={`${map.label}: ${merchant.name}`} className="flex min-h-11 items-center gap-2 rounded-2xl bg-[var(--paper)] px-3 py-2 text-sm font-semibold text-[var(--teal)] underline-offset-4 hover:underline"><MapPin size={15} /><span className="mr-auto text-[var(--ink)]">{merchant.name}{merchant.local_name !== merchant.name && <span className="ml-1 text-xs font-normal text-[var(--muted)]">· {merchant.local_name}</span>}</span><ExternalLink size={13} /></a> : null; })}{food.recommended_merchants.length === 0 && <p className="rounded-2xl bg-[var(--paper)] px-3 py-3 text-sm text-[var(--muted)]">{t("noVerifiedMerchant")}</p>}</div></div>
        {food.food_hotspots.length > 0 && <div className="mt-4"><p className="text-xs font-semibold text-[var(--muted)]">{t("foodAreas")}</p><p className="mt-1 text-sm text-[var(--muted)]">{food.food_hotspots.slice(0, 3).map((area) => area.name).join("、")}</p></div>}
        <div className="mt-auto flex flex-wrap items-center gap-2 pt-5">{food.destinations[0] && <Link href={`/hotspots?category=food&destination_id=${encodeURIComponent(food.destinations[0].id)}`} className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white">{t("viewFoodAreas")}</Link>}{food.source_urls[0] && <a href={food.source_urls[0]} target="_blank" rel="noopener noreferrer" className="ml-auto inline-flex min-h-11 items-center gap-1 px-2 text-xs font-semibold text-[var(--muted)]">{t("source")}<ExternalLink size={13} /></a>}</div>
        <TravelCardActions type="food" id={food.id} title={food.name} selectionPath={`/foods/${food.id}/trip-selections`} merchantId={food.recommended_merchants[0]?.merchant_id} />
      </article>)}</div>}
      {!loading && !error && foods?.has_more && <div className="mt-7 text-center"><button type="button" onClick={() => void load(true)} className="min-h-12 rounded-xl border border-[var(--teal)] bg-white px-7 font-semibold text-[var(--teal)]">{t("loadMore")}</button></div>}
      <p className="mt-8 rounded-2xl bg-white px-5 py-4 text-sm leading-6 text-[var(--muted)]">{t("merchantNotice")}</p>
    </section>
  </main>;
}
