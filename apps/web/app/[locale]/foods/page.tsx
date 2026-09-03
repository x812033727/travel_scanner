import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { FoodBrowser } from "@/components/food-browser";
import { SiteHeader } from "@/components/site-header";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("foodsTitle"), description: t("foodsDescription") };
}

export default function FoodsPage() {
  return <><SiteHeader /><FoodBrowser /></>;
}
