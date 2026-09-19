import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { ExploreSwitch } from "@/components/explore-switch";
import { FoodBrowser } from "@/components/food-browser";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { breadcrumbs, foodEstablishments } from "@/lib/structured-data";
import { getInitialFoods } from "@/lib/foods.server";
import { readFoodBrowserFilters } from "@/lib/foods";
import type { Locale } from "@/i18n/routing";

/** The distinction badges the merchant card draws (`food-merchant-card.tsx`), by catalog key,
 *  so the graph names the same six awards and no other. */
const DISTINCTIONS = ["three_star", "two_star", "one_star", "green_star", "bib_gourmand", "selected"] as const;

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("foodsTitle"), description: t("foodsDescription") };
}

export default async function FoodsPage({ params, searchParams }: {
  params: Promise<{ locale: Locale }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const [{ locale }, query] = await Promise.all([params, searchParams]);
  const search = new URLSearchParams();
  for (const key of ["destination_id", "city", "area", "category", "style", "q"]) {
    const value = query[key];
    const first = Array.isArray(value) ? value[0] : value;
    if (first !== undefined) search.set(key, first);
  }
  const filters = readFoodBrowserFilters(search.toString());
  const [initial, nav, foods] = await Promise.all([
    getInitialFoods(locale, filters),
    getTranslations({ locale, namespace: "navigation" }),
    getTranslations({ locale, namespace: "foods" }),
  ]);
  const awards = Object.fromEntries(DISTINCTIONS.map((key) => [key, foods(`distinctions.${key}`)]));
  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: nav("foods"), path: "/foods" }]),
          // The first page as the server drew it, from the same seed the browser renders. The list
          // the browser fetches after hydration is never marked up.
          ...foodEstablishments(locale, initial.merchants, awards),
        ]}
      />
      <ExploreSwitch />
      <FoodBrowser key={search.toString()} initialCities={initial.cities} initialCategories={initial.categories} initialMerchants={initial.merchants} initialFilters={filters} />
    </>
  );
}
