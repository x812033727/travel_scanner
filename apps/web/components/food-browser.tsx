"use client";

import { Search, SlidersHorizontal, Sparkles, Store, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useModalSheet } from "@/lib/modal-sheet";
import { api } from "@/lib/api";
import { FoodCityGrid, FoodCitySelect } from "@/components/food-city-picker";
import { FoodDishesSection } from "@/components/food-dishes-section";
import { FoodFilterChips, type FilterChipItem } from "@/components/food-filter-chips";
import { FoodMerchantCard } from "@/components/food-merchant-card";
import {
  OTHER_AREA,
  activeFilterCount,
  findCity,
  foodBrowserSearch,
  merchantsQuery,
  readFoodBrowserFilters,
  type FacetCategory,
  type FoodBrowserFilters,
  type FoodCategoriesResponse,
  type FoodCitiesResponse,
  type FoodCountry,
  type FoodMerchantsResponse,
} from "@/lib/foods";
import { useClientSearch } from "@/lib/use-client-search";
import { useSharedAnchor } from "@/lib/use-shared-anchor";

type ActiveChip = { key: string; label: string; clear: () => void };

function isCitiesResponse(value: unknown): value is FoodCitiesResponse {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Partial<FoodCitiesResponse>;
  return Array.isArray(candidate.countries);
}

function isCategoriesResponse(value: unknown): value is FoodCategoriesResponse {
  if (typeof value !== "object" || value === null) return false;
  return Array.isArray((value as Partial<FoodCategoriesResponse>).items);
}

/**
 * `initialCities` and `initialCategories` are the server's copy of the two lists that do
 * not depend on any filter. The city chooser is 2,492 pixels tall on a phone, so arriving
 * after hydration meant shoving the whole page down about four seconds in.
 */
export function FoodBrowser({ initialCities, initialCategories }: {
  initialCities?: unknown;
  initialCategories?: unknown;
} = {}) {
  const t = useTranslations("foods");
  const seededCities = useMemo(
    () => (isCitiesResponse(initialCities) ? initialCities.countries ?? [] : null),
    [initialCities],
  );
  const seededCategories = useMemo(
    () => (isCategoriesResponse(initialCategories) ? initialCategories.items ?? [] : null),
    [initialCategories],
  );
  const search = useClientSearch();
  const initialFilters = useMemo(() => readFoodBrowserFilters(search ?? ""), [search]);
  const [filterState, setFilterState] = useState<FoodBrowserFilters | null>(null);
  const filters = filterState ?? initialFilters;
  const [queryInput, setQueryInput] = useState<string | null>(null);
  const queryValue = queryInput ?? filters.query;
  const [countries, setCountries] = useState<FoodCountry[]>(seededCities ?? []);
  const [siteCategories, setSiteCategories] = useState<FacetCategory[]>(seededCategories ?? []);
  const [result, setResult] = useState<FoodMerchantsResponse | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  // Kept apart from `error`: losing the city list must not blank the merchants.
  const [citiesError, setCitiesError] = useState("");
  const [appending, setAppending] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const filterSheetRef = useModalSheet<HTMLFormElement>(filtersOpen, () => setFiltersOpen(false));
  const hydrated = useRef(false);

  const loadCities = useCallback(() => {
    api<FoodCitiesResponse>("/foods/cities")
      .then((response) => {
        setCountries(response.countries ?? []);
        setCitiesError("");
      })
      .catch((reason: Error) => setCitiesError(reason.message));
  }, []);

  useEffect(() => {
    // Both lists came with the HTML unless the server call failed, and asking again would
    // only repaint the same rows.
    if (seededCities === null) loadCities();
    if (seededCategories !== null) return;
    api<FoodCategoriesResponse>("/foods/categories")
      .then((response) => setSiteCategories(response.items ?? []))
      .catch(() => undefined);
  }, [loadCities, seededCategories, seededCities]);

  useEffect(() => {
    // Later replaceState calls change the snapshot; only the first client value seeds the list.
    if (search === null || hydrated.current) return;
    hydrated.current = true;
    api<FoodMerchantsResponse>(`/foods/merchants?${merchantsQuery(initialFilters)}`)
      .then(setResult)
      .catch((reason: Error) => setError(reason.message));
  }, [initialFilters, search]);

  useSharedAnchor(Boolean(result?.items.length));

  function apply(next: FoodBrowserFilters, options: { append?: boolean } = {}) {
    setFilterState(next);
    setQueryInput(null);
    setError("");
    setFiltersOpen(false);
    setPending(true);
    setAppending(Boolean(options.append));
    const cursor = options.append ? result?.next_cursor : undefined;
    api<FoodMerchantsResponse>(`/foods/merchants?${merchantsQuery(next, cursor)}`)
      .then((response) => {
        setResult((current) =>
          options.append && current
            ? { ...response, items: [...current.items, ...response.items] }
            : response,
        );
      })
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setPending(false));
    if (!options.append) {
      const query = foodBrowserSearch(next);
      window.history.replaceState(
        null,
        "",
        `${window.location.pathname}${query ? `?${query}` : ""}`,
      );
    }
  }

  const withTypedQuery = (next: Partial<FoodBrowserFilters>) =>
    apply({ ...filters, query: queryValue.trim(), ...next });
  const selectCity = (destinationId: string) => withTypedQuery({ destinationId, area: "" });
  const toggleArea = (area: string) => withTypedQuery({ area });
  const toggleCategory = (category: string) => withTypedQuery({ category });
  const clearFilters = () =>
    apply({ destinationId: filters.destinationId, area: "", category: "", query: "" });
  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    apply({ ...filters, query: queryValue.trim() });
  };

  const city = findCity(countries, filters.destinationId);
  const loading = pending || (result === null && !error);
  const areaItems: FilterChipItem[] = (result?.facets?.areas ?? []).map((area) => ({
    key: area.slug,
    label: area.name,
    count: area.merchant_count,
  }));
  const unassigned = result?.facets?.unassigned_area_count ?? 0;
  if (unassigned > 0 || filters.area === OTHER_AREA) {
    areaItems.push({ key: OTHER_AREA, label: t("otherArea"), count: unassigned });
  }
  const categoryItems: FilterChipItem[] = (result?.facets?.categories ?? siteCategories).map(
    (category) => ({
      key: category.slug,
      label: category.name,
      count: category.merchant_count,
    }),
  );
  const showDishFallback =
    Boolean(filters.destinationId)
    && result !== null
    && result.total === 0
    && !filters.area
    && !filters.category
    && !filters.query;
  const activeChips: ActiveChip[] = [];
  if (city) {
    activeChips.push({
      key: "city",
      label: city.name,
      clear: () => apply({ ...filters, destinationId: "", area: "" }),
    });
  }
  if (filters.area) {
    activeChips.push({
      key: "area",
      label: areaItems.find((item) => item.key === filters.area)?.label ?? filters.area,
      clear: () => toggleArea(""),
    });
  }
  if (filters.category) {
    activeChips.push({
      key: "category",
      label:
        categoryItems.find((item) => item.key === filters.category)?.label ?? filters.category,
      clear: () => toggleCategory(""),
    });
  }
  if (filters.query) {
    activeChips.push({
      key: "query",
      label: filters.query,
      clear: () => apply({ ...filters, query: "" }),
    });
  }

  return (
    <main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
      <section className="pb-7 pt-5 md:pb-9 md:pt-9">
        <p className="flex items-center gap-2 text-sm font-semibold text-[var(--coral)]">
          <Sparkles size={16} />
          {t("eyebrow")}
        </p>
        <h1 className="mt-3 text-3xl font-bold tracking-[-.035em] md:text-5xl">{t("title")}</h1>
        <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p>
      </section>

      <button
        type="button"
        onClick={() => setFiltersOpen(true)}
        className="mb-3 flex min-h-12 w-full items-center justify-between rounded-2xl border border-[var(--line)] bg-white px-4 font-semibold shadow-[var(--shadow-sm)] md:hidden"
      >
        <span className="flex items-center gap-2">
          <SlidersHorizontal size={18} />
          {t("filters")}
        </span>
        <span className="rounded-full bg-[var(--coral-soft)] px-2.5 py-1 text-xs">
          {activeFilterCount(filters)}
        </span>
      </button>
      {filtersOpen && (
        <button
          type="button"
          aria-label={t("closeFilters")}
          onClick={() => setFiltersOpen(false)}
          className="fixed inset-0 z-[70] bg-slate-950/40 md:hidden"
        />
      )}
      {/* A dialog only while it is the sheet; on a wide screen this is the filter bar. */}
      <form
        ref={filterSheetRef}
        {...(filtersOpen ? { role: "dialog" as const, "aria-modal": true } : {})}
        onSubmit={submit}
        className={`${filtersOpen ? "mobile-filter-sheet-open" : ""} mobile-filter-sheet grid gap-3 rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-[var(--shadow-lg)] md:grid-cols-[1.35fr_1fr_auto] md:p-5`}
        aria-label={t("filters")}
      >
        <div className="mb-1 flex items-center justify-between md:hidden">
          <strong>{t("filters")}</strong>
          <button
            type="button"
            onClick={() => setFiltersOpen(false)}
            aria-label={t("closeFilters")}
            className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]"
          >
            <X size={19} />
          </button>
        </div>
        <label className="relative">
          <span className="sr-only">{t("searchPlaceholder")}</span>
          <Search
            className="pointer-events-none absolute left-4 top-3.5 text-[var(--muted)]"
            size={19}
          />
          <input
            value={queryValue}
            onChange={(event) => setQueryInput(event.target.value)}
            placeholder={t("searchPlaceholder")}
            className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-11 pr-4 outline-none focus:border-[var(--teal)]"
          />
        </label>
        <FoodCitySelect
          countries={countries}
          value={filters.destinationId}
          onChange={selectCity}
          label={t("cityLabel")}
          allLabel={t("allCities")}
        />
        <button type="submit" className="h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white">
          {t("submit")}
        </button>
      </form>

      {filters.destinationId && (
        <FoodFilterChips
          label={t("areaLabel")}
          allLabel={t("allAreas")}
          items={areaItems}
          value={filters.area}
          onChange={toggleArea}
        />
      )}
      <FoodFilterChips
        label={t("categoryLabel")}
        allLabel={t("allCategories")}
        items={categoryItems}
        value={filters.category}
        onChange={toggleCategory}
      />
      {activeChips.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-2 text-sm" aria-label={t("activeFilters")}>
          <span className="text-[var(--muted)]">{t("activeFilters")}</span>
          {activeChips.map((chip) => (
            <button
              key={chip.key}
              type="button"
              onClick={chip.clear}
              aria-label={`${t("clearFilters")}: ${chip.label}`}
              className="inline-flex min-h-9 items-center gap-1 rounded-full border border-[var(--line)] bg-white px-3 text-xs font-semibold"
            >
              {chip.label}
              <X size={13} />
            </button>
          ))}
          <button
            type="button"
            onClick={clearFilters}
            className="min-h-9 px-2 text-xs font-semibold text-[var(--teal)]"
          >
            {t("clearFilters")}
          </button>
        </div>
      )}

      {!filters.destinationId && citiesError && (
        <div role="alert" className="mt-7 flex flex-wrap items-center justify-between gap-3 rounded-3xl bg-[var(--coral-soft)] p-6">
          <span>{citiesError}</span>
          <button type="button" onClick={loadCities} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-4 font-semibold">
            {t("retry")}
          </button>
        </div>
      )}

      {!filters.destinationId && countries.length > 0 && (
        <section className="mt-7" aria-labelledby="food-cities-title">
          <h2 id="food-cities-title" className="text-xl font-bold">
            {t("chooseCityTitle")}
          </h2>
          <p className="mt-1 text-sm text-[var(--muted)]">{t("chooseCityBody")}</p>
          <div className="mt-4">
            <FoodCityGrid
              countries={countries}
              onSelect={selectCity}
              countLabel={(count) => t("cityCount", { count })}
            />
          </div>
        </section>
      )}

      <section className="mt-7" aria-live="polite" aria-busy={loading}>
        <div className="mb-4 flex items-center justify-between gap-4">
          <h2 className="flex items-center gap-2 text-xl font-bold">
            <Store size={20} className="text-[var(--coral)]" />
            {city ? city.name : t("merchantList")}
          </h2>
          <p className="text-sm text-[var(--muted)]">
            {t("loadedMerchants", { shown: result?.items.length ?? 0, total: result?.total ?? 0 })}
          </p>
        </div>
        {loading && !result && (
          <div className="rounded-3xl border border-[var(--line)] bg-white p-8 text-[var(--muted)]">
            {t("loading")}
          </div>
        )}
        {error && (
          <div role="alert" className="mb-4 rounded-3xl bg-[var(--coral-soft)] p-6">
            {error}
            <button
              type="button"
              onClick={() => apply(filters, { append: appending })}
              className="ml-3 min-h-11 font-semibold underline underline-offset-4"
            >
              {t("retry")}
            </button>
          </div>
        )}
        {!error && result && result.items.length === 0 && !showDishFallback && (
          <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white p-8 text-center">
            <h3 className="font-bold">{t("emptyFiltersTitle")}</h3>
            <p className="mt-2 text-sm text-[var(--muted)]">{t("emptyFiltersBody")}</p>
            <button
              type="button"
              onClick={clearFilters}
              className="mt-4 min-h-11 rounded-xl border border-[var(--teal)] px-4 text-sm font-semibold text-[var(--teal)]"
            >
              {t("clearFilters")}
            </button>
          </div>
        )}
        {!error && showDishFallback && city && (
          <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white p-8 text-center">
            <h3 className="font-bold">{t("emptyCityTitle", { city: city.name })}</h3>
            <p className="mt-2 text-sm text-[var(--muted)]">{t("emptyCityBody")}</p>
          </div>
        )}
        {result && result.items.length > 0 && (
          <div className="grid gap-5 md:grid-cols-2">
            {result.items.map((merchant) => (
              <FoodMerchantCard
                key={merchant.id}
                merchant={merchant}
                onSelectArea={(slug) =>
                  merchant.destination_id === filters.destinationId
                    ? toggleArea(slug)
                    : apply({ ...filters, destinationId: merchant.destination_id, area: slug })
                }
                onSelectCategory={toggleCategory}
              />
            ))}
          </div>
        )}
        {result?.has_more && (
          <div className="mt-7 text-center">
            <button
              type="button"
              disabled={pending}
              onClick={() => apply(filters, { append: true })}
              className="min-h-12 rounded-xl border border-[var(--teal)] bg-white px-7 font-semibold text-[var(--teal)] disabled:opacity-50"
            >
              {t("loadMore")}
            </button>
          </div>
        )}
        <p className="mt-8 rounded-2xl bg-white px-5 py-4 text-sm leading-6 text-[var(--muted)]">
          {t("merchantNotice")}
        </p>
      </section>

      {showDishFallback && city && (
        <FoodDishesSection destinationId={city.id} countryCode={city.country_code} />
      )}
    </main>
  );
}
