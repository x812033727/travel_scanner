import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { ExploreSwitch } from "@/components/explore-switch";
import { FoodBrowser } from "@/components/food-browser";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { breadcrumbs } from "@/lib/structured-data";
import { getInitialFoods } from "@/lib/foods.server";
import { readFoodBrowserFilters } from "@/lib/foods";
import type { Locale } from "@/i18n/routing";

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
  for (const key of ["destination_id", "area", "category", "style", "q"]) {
    const value = query[key];
    const first = Array.isArray(value) ? value[0] : value;
    if (first !== undefined) search.set(key, first);
  }
  const filters = readFoodBrowserFilters(search.toString());
  const [initial, nav] = await Promise.all([
    getInitialFoods(locale, filters),
    getTranslations({ locale, namespace: "navigation" }),
  ]);
  return (
    <>
      <SiteHeader />
      <StructuredData data={breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: nav("foods"), path: "/foods" }])} />
      <ExploreSwitch />
      <FoodBrowser key={search.toString()} initialCities={initial.cities} initialCategories={initial.categories} initialMerchants={initial.merchants} initialFilters={filters} />
    </>
  );
}
