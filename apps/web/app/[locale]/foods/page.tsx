import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { ExploreSwitch } from "@/components/explore-switch";
import { FoodBrowser } from "@/components/food-browser";
import { SiteHeader } from "@/components/site-header";
import type { Locale } from "@/i18n/routing";
import { getInitialFoods } from "@/lib/foods.server";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("foodsTitle"), description: t("foodsDescription") };
}

export default async function FoodsPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  const initial = await getInitialFoods(locale);
  return <><SiteHeader /><ExploreSwitch /><FoodBrowser initialCities={initial.cities} initialCategories={initial.categories} /></>;
}
