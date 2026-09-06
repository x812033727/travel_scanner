import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import { SearchExperience } from "@/components/search-experience";
import { SiteHeader } from "@/components/site-header";
import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("searchTitle"), description: t("searchDescription") };
}


export default async function SearchPage() {
  const t = await getTranslations("search");
  return <><SiteHeader /><Suspense fallback={<main className="mx-auto max-w-6xl px-5">{t("understanding")}</main>}><SearchExperience /></Suspense></>;
}
