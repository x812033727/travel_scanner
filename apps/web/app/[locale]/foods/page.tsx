import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { ExploreSwitch } from "@/components/explore-switch";
import { FoodBrowser } from "@/components/food-browser";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { breadcrumbs } from "@/lib/structured-data";
import { getInitialFoods } from "@/lib/foods.server";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("foodsTitle"), description: t("foodsDescription") };
}

export default async function FoodsPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  const [initial, nav] = await Promise.all([
    getInitialFoods(locale),
    getTranslations({ locale, namespace: "navigation" }),
  ]);
  return (
    <>
      <SiteHeader />
      <StructuredData data={breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: nav("foods"), path: "/foods" }])} />
      <ExploreSwitch />
      <FoodBrowser initialCities={initial.cities} initialCategories={initial.categories} initialMerchants={initial.merchants} />
    </>
  );
}
